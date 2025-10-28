import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt

fasta_path = str()                 
results_store = dict()         

def select_file():
    global fasta_path 
    fasta_path = filedialog.askopenfilename(
        title="Select FASTA file",
        filetypes=(("FASTA files", "*.fasta *.fa *.fna"), ("All files", "*.*"))
    )
    messagebox.showinfo("Info", f"fasta file: {fasta_path}")

def load_fasta_to_df():
    if not fasta_path:
        return None
    records = list(SeqIO.parse(fasta_path, "fasta"))
    if not records:
        return None
    return pd.DataFrame({
        "id": [r.id for r in records],
        "description": [r.description for r in records],
        "sequence": [str(r.seq) for r in records]
    })

def find_motif_positions(sequence: str, motif: str):
    if not motif:
        return []
    return [i for i in range(len(sequence)) if sequence.startswith(motif, i)]

def scan_all_genes(df: pd.DataFrame, motif: str):
    results = []
    for _, row in df.iterrows():
        gene_id = row["id"]
        seq = row["sequence"]
        positions = find_motif_positions(seq, motif)
        results.append({"gene_id": gene_id, "length": len(seq), "positions": positions})
    return results

def add_to_store(motif: str, results: list[dict]):
    for r in results:
        key = (motif, r["gene_id"])
        if key not in results_store:
            results_store[key] = {"positions": r["positions"], "length": r["length"]}

# Buttons
def on_search_click():
    df = load_fasta_to_df()
    if df is None:
        messagebox.showwarning("No data", "Load a FASTA file first.")
        return

    motif = entry_search_motif.get().strip()
    if not motif:
        messagebox.showwarning("No motif", "Enter a motif to search for.")
        return

    results = scan_all_genes(df, motif)
    add_to_store(motif, results)

    lines = list()
    for id, row in enumerate(results):
        lines.append(f"in: {row['gene_id']} hits: {len(results)} in: {row['positions']}")
    msg = f"motif: {motif} \n" + "\n".join(lines)
    messagebox.showinfo("Search results", msg)

def on_plot_click():
    df = load_fasta_to_df()
    if df is None:
        messagebox.showwarning("No data", "Load a FASTA file first.")
        return

    motif = entry_plot_motif.get().strip()
    if not motif:
        messagebox.showwarning("No motif", "Enter a motif to plot.")
        return

    results = scan_all_genes(df, motif)
    add_to_store(motif, results)

    plt.close('all')

    max_len = max((r["length"] for r in results), default=1)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_title(f"Distribution of motif '{motif}' (each row = gene)")
    ax.set_xlabel("Position in sequence")
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_xlim(0, max_len)

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    for i, r in enumerate(results):
        color = colors[i % len(colors)]
        y0 = i
        ax.vlines(r["positions"], ymin=y0, ymax=y0 + 0.8, linewidth=6, color=color)

    ax.set_yticks([j + 0.4 for j in range(len(results))])
    ax.set_yticklabels([f"gene_{j+1}" for j in range(len(results))])

    plt.tight_layout()
    plt.show(block=False)  

def on_save_click():
    if not results_store:
        return
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV file", "*.csv"), ("All files", "*.*")],
        title="Save results to CSV"
    )
    if not save_path:
        return

    rows = []
    for (motif, gene_id), data in results_store.items():
        rows.append({
            "gene_id": gene_id,
            "motif": motif,
            "hit_count": len(data["positions"]),
            "positions": ";".join(map(str, data["positions"])),
            "sequence_length": data["length"]
        })
    pd.DataFrame(rows).to_csv(save_path, index=False, encoding="utf-8")

# GUI

root = tk.Tk()
root.title("DNA Motif Analysis")
root.geometry("520x420")

# file picker
btn_load = ttk.Button(root, text="Load FASTA file", command=select_file)
btn_load.pack(pady=6)

# search (popup, no plot)
entry_search_motif = ttk.Entry(root, width=60)
entry_search_motif.pack(pady=3)
entry_search_motif.insert(0, "TATA")
btn_search = ttk.Button(root, text="Search (all genes)", command=on_search_click)
btn_search.pack(pady=4)

# plot (draw all genes, different colors)
lbl_plot = ttk.Label(root, text="Motif to plot:")
lbl_plot.pack(pady=(10, 2))
entry_plot_motif = ttk.Entry(root, width=60)
entry_plot_motif.pack(pady=2)
entry_plot_motif.insert(0, "TATA")
btn_plot = ttk.Button(root, text="Plot (all genes)", command=on_plot_click)
btn_plot.pack(pady=8)

# save CSV
btn_save = ttk.Button(root, text="Save results to CSV", command=on_save_click)
btn_save.pack(side="bottom", pady=12)

root.mainloop()
