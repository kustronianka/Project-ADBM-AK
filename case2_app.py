import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_path = str()
df_source = None
df_result_store = None

def get_csv():
    global csv_path, df_source
    csv_path = filedialog.askopenfilename(
        title="Wybierz plik CSV",
        filetypes=[("CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
    )
    
    df_source = pd.read_csv(csv_path)

    column_names = ["age", "systolic", "diastolic"]
    for column in column_names:
        if column in df_source.columns:
            df_source[column] = pd.to_numeric(df_source, errors="coerce")

def get_result_to_save():
    if df_result_store is None:
        return df_source
    else:
        return df_result_store
    
def apply_filters():
    df_filtering = df_source.copy()
    df_filtering[["systolic", "diastolic"]] = df_filtering["BloodPressure"].str.split("/", n=1, expand=True)

    if "Age" in df_filtering.columns:
        a_min = entry_age_min.get().strip()
        a_max = entry_age_max.get().strip()
        if a_min:
            df_filtering = df_filtering[df_filtering["Age"] >= float(a_min)]
        if a_max:
            df_filtering = df_filtering[df_filtering["Age"] <= float(a_max)]

    if "Gender" in df_filtering.columns:
        gender = combo_gender.get()
        if gender and gender != "Any":
            df_filtering = df_filtering[df_filtering["Gender"].astype(str).str.lower().str.contains(gender.lower(), na=False)]

    if "BloodPressure" in df_filtering.columns:
        blood_pressure_sys_min = entry_blood_pressure_sys_min.get().strip()
        blood_pressure_sys_max = entry_blood_pressure_sys_max.get().strip()
        blood_pressure_dia_min = entry_blood_pressure_dia_min.get().strip()
        blood_pressure_dia_max = entry_blood_pressure_dia_max.get().strip()
        if blood_pressure_sys_min and blood_pressure_sys_max:
            df_filtering = df_filtering[df_filtering["systolic"].astype("int") >= int(blood_pressure_sys_min)]
            df_filtering = df_filtering[df_filtering["systolic"].astype("int") <= int(blood_pressure_sys_max)]
        if blood_pressure_dia_min and blood_pressure_dia_max:
            df_filtering = df_filtering[df_filtering["diastolic"].astype("int") >= int(blood_pressure_dia_min)]
            df_filtering = df_filtering[df_filtering["diastolic"].astype("int") <= int(blood_pressure_dia_max)]

    if "HeartRate" in df_filtering.columns:
        heart_rate_min = entry_heart_rate_min.get().strip()
        heart_rate_max = entry_heart_rate_max.get().strip()
        if heart_rate_min:
            df_filtering = df_filtering[df_filtering["HeartRate"] >= float(heart_rate_min)]
        if heart_rate_max:
            df_filtering = df_filtering[df_filtering["HeartRate"] <= float(heart_rate_max)]

    if "Symptoms" in df_filtering.columns:
        symptom = entry_sym.get().strip()
        if symptom:
            df_filtering = df_filtering[df_filtering["Symptoms"].astype(str).str.lower().str.contains(symptom.lower(), na=False)]

    if "systolic" and "diastolic" in df_filtering.columns:
        df_filtering = df_filtering.drop(columns=["systolic", "diastolic"])

    return df_filtering

def show_stats():
    df = apply_filters()

    num_of_rows = len(df)
    age = list(df['Age'])
    heart_rate = list(df["HeartRate"])
    mean_age = round(np.mean(age), 2)
    mean_heart_rate = round(np.mean(heart_rate), 2)
    med_age = round(np.median(heart_rate), 2)
    med_heart_rate = round(np.mean(heart_rate), 2)
    msg = f"number of rows: {num_of_rows}, \n mean age: {mean_age}, \n mean Heartrate: {mean_heart_rate}, \n med age: {med_age}, \n med HeartRate: {med_heart_rate}"

    messagebox.showinfo("Statystyki", msg)

def plot_hist():
    df = apply_filters()
    if df is None:
        messagebox.showwarning("Brak danych", "Wczytaj CSV najpierw.")
        return

    column = combo_hist.get().strip()
    if not column:
        messagebox.showwarning("Wybór", "Wybierz kolumnę do histogramu.")
        return
    if not pd.api.types.is_numeric_dtype(df[column]):
        messagebox.showwarning("Uwaga", "Wybrana kolumna nie jest numeryczna.")
        return

    plt.close('all')
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df[column].dropna(), bins=30)
    ax.set_title(f"Histogram: {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    ax.grid(alpha=0.3, linestyle="--")
    plt.tight_layout()
    plt.show(block=False)

def plot_scatter():
    df = apply_filters()
    if df is None:
        messagebox.showwarning("Brak danych", "Wczytaj CSV najpierw.")
        return

    x = combo_x.get().strip()
    y = combo_y.get().strip()
    if not x or not y:
        messagebox.showwarning("Wybór", "Wybierz kolumny X i Y.")
        return
    if not (pd.api.types.is_numeric_dtype(df[x]) and pd.api.types.is_numeric_dtype(df[y])):
        messagebox.showwarning("Uwaga", "Kolumny X i Y muszą być numeryczne.")
        return

    plt.close('all')
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df[x], df[y], s=25, alpha=0.7)
    ax.set_title(f"{x} vs {y}")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.grid(alpha=0.3, linestyle="--")
    plt.tight_layout()
    plt.show(block=False)

def group_by():
    df_to_save = apply_filters()

    if "Gender" in df_to_save.columns:
        counts = df_to_save.groupby('Gender').size().reset_index(name='count')
        msg = counts.to_string(index=False)
        messagebox.showinfo("grupy płci", msg)

def export_csv():
    df_to_save = apply_filters()

    if df_to_save is None:
        messagebox.showwarning("Brak danych", "Brak danych do zapisu.")
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv"), ("Wszystkie pliki", "*.*")],
        title="Zapisz CSV"
    )
    if not path:
        return

    df_to_save.to_csv(path, index=False, encoding="utf-8")
    messagebox.showinfo("Zapisano", "Plik zapisano poprawnie.")

root = tk.Tk()
root.title("Case2")
root.geometry("640x520")

ttk.Button(root, text="Wczytaj CSV", command=get_csv).pack(pady=6)

frame_age = ttk.Frame(root)
frame_age.pack(pady=2, fill="x")
ttk.Label(frame_age, text="Age:").pack(side="left", padx=(0,6))
entry_age_min = ttk.Entry(frame_age, width=8)
entry_age_min.pack(side="left")
ttk.Label(frame_age, text="–").pack(side="left", padx=4)
entry_age_max = ttk.Entry(frame_age, width=8)
entry_age_max.pack(side="left")

frame_gender = ttk.Frame(root)
frame_gender.pack(pady=2, fill="x")
ttk.Label(frame_gender, text="Gender:").pack(side="left", padx=(0,6))
combo_gender = ttk.Combobox(frame_gender, values=["Any", "M", "F"], width=12, state="readonly")
combo_gender.set("Any"); combo_gender.pack(side="left")

frame_bp = ttk.Frame(root)
frame_bp.pack(pady=2, fill="x")

ttk.Label(frame_bp, text="BloodPressure systolic:").pack(side="left", padx=(0,6))
entry_blood_pressure_sys_min = ttk.Entry(frame_bp, width=7)
entry_blood_pressure_sys_min.pack(side="left")
ttk.Label(frame_bp, text="–").pack(side="left", padx=4)
entry_blood_pressure_sys_max = ttk.Entry(frame_bp, width=7)
entry_blood_pressure_sys_max.pack(side="left", padx=(8,16))

ttk.Label(frame_bp, text="BloodPressure diastolic:").pack(side="left", padx=(0,6))
entry_blood_pressure_dia_min = ttk.Entry(frame_bp, width=7)
entry_blood_pressure_dia_min.pack(side="left")
ttk.Label(frame_bp, text="–").pack(side="left", padx=4)
entry_blood_pressure_dia_max = ttk.Entry(frame_bp, width=7)
entry_blood_pressure_dia_max.pack(side="left", padx=(8,16))

frame_hr = ttk.Frame(root)
frame_hr.pack(pady=2, fill="x")

ttk.Label(frame_hr, text="HeartRate:").pack(side="left", padx=(0,6))
entry_heart_rate_min = ttk.Entry(frame_hr, width=7)
entry_heart_rate_min.pack(side="left")
ttk.Label(frame_hr, text="–").pack(side="left", padx=4)
entry_heart_rate_max = ttk.Entry(frame_hr, width=7)
entry_heart_rate_max.pack(side="left")

frame_sym = ttk.Frame(root)
frame_sym.pack(pady=2, fill="x")
ttk.Label(frame_sym, text="Symptoms:").pack(side="left", padx=(0,6))
entry_sym = ttk.Entry(frame_sym, width=40)
entry_sym.pack(side="left")

frame_btn = ttk.Frame(root)
frame_btn.pack(pady=6)
ttk.Button(frame_btn, text="Pokaż statystyki", command=show_stats).pack(side="left", padx=4)
ttk.Button(frame_btn, text="grupuj po płci", command=group_by).pack(side="left", padx=4)

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=8)

frame_hist = ttk.Frame(root)
frame_hist.pack(pady=2, fill="x")
ttk.Label(frame_hist, text="Histogram:").pack(side="left", padx=(0,6))
combo_hist = ttk.Combobox(frame_hist, values=["Age", "HeartRate"], width=30, state="readonly")
combo_hist.pack(side="left", padx=4)
ttk.Button(frame_hist, text="Rysuj", command=plot_hist).pack(side="left", padx=8)

frame_sc = ttk.Frame(root)
frame_sc.pack(pady=2, fill="x")
ttk.Label(frame_sc, text="Scatter X:").pack(side="left", padx=(0,6))
combo_x = ttk.Combobox(frame_sc, values=["Age", "HeartRate"], width=18, state="readonly")
combo_x.pack(side="left", padx=4)
ttk.Label(frame_sc, text="Y:").pack(side="left", padx=6)
combo_y = ttk.Combobox(frame_sc, values=["Age", "HeartRate"], width=18, state="readonly")
combo_y.pack(side="left", padx=4)
ttk.Button(frame_sc, text="Rysuj", command=plot_scatter).pack(side="left", padx=8)

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=8)
ttk.Button(root, text="Eksportuj CSV", command=export_csv).pack(pady=6)

root.mainloop()
