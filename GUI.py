import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt

fasta_path = str()                 # path to FASTA file
results_store = dict()         # key=(motif, gene_id): {"positions": [...], "length": N}

def select_file():
    """Pick a FASTA file from disk."""
    global fasta_path 
    fasta_path = filedialog.askopenfilename(
        title="Select FASTA file",
        filetypes=(("FASTA files", "*.fasta *.fa *.fna"), ("All files", "*.*"))
    )
    if fasta_path:
        messagebox.showinfo("File selected", fasta_path)
    else:
        messagebox.showerror("Error", "No file selected.")

def load_fasta_to_df():
    """Read FASTA to a DataFrame: columns id, description, sequence."""
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
    """Return list of start positions of the motif (with overlaps)."""
    if not motif:
        return []
    return [i for i in range(len(sequence)) if sequence.startswith(motif, i)]

def scan_all_genes(df: pd.DataFrame, motif: str):
    """For each gene, compute motif positions."""
    results = []
    for _, row in df.iterrows():
        gene_id = row["id"]
        seq = row["sequence"]
        positions = find_motif_positions(seq, motif)
        results.append({"gene_id": gene_id, "length": len(seq), "positions": positions})
    return results

def add_to_store(motif: str, results: list[dict]):
    """Save results for (motif, gene) pairs into results_store (no duplicates)."""
    for r in results:
        key = (motif, r["gene_id"])
        if key not in results_store:
            results_store[key] = {"positions": r["positions"], "length": r["length"]}

# ---------- UI ACTIONS ----------

def on_search_click():
    """Scan ALL genes, show concise popup, add to store (no plotting)."""
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

    # concise, readable popup (first 8 genes)
    lines = []
    for i, r in enumerate(results, start=1):
        lines.append(f"gene_{i}: {len(r['positions'])} hits ({r["positions"]})")
    msg = f"Motif: {motif}\nGenes scanned: {len(results)}\n" + "\n".join(lines)
    messagebox.showinfo("Search results", msg)

def on_plot_click():
    """Create a NEW plot for ALL genes (different colors). No globals kept."""
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

    # close previous figures (if any), then open a fresh one
    plt.close('all')

    max_len = max((r["length"] for r in results), default=1)
... (Pozostałe wiersze: 75)