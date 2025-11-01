import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path
from pandas.api.types import is_numeric_dtype
import matplotlib.dates as mdates

path = str()
results = dict()

def get_path():
    global path
    path = filedialog.askopenfilename(
        title="Wybierz plik CSV",
        filetypes=[("CSV", "*.csv"), ("json", "*.json"), ("Wszystkie pliki", "*.*")])

def read_file():
    global path
    
    if Path(path).suffix == ".csv":
        df_csv = pd.read_csv(path, sep=",", header=0)
        return_datetime(df_csv)
        return df_csv
    if Path(path).suffix == ".json":
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            df_json = pd.json_normalize(data,
                                        record_path=["readings"],
                                        meta=["device", "location"])
            return_datetime(df_json)
            return df_json
        
def calculate():
    global results
    df = read_file()
    columns = df.columns
    for column in columns:
        if is_numeric_dtype(df[column]):
            mean = round(df[column].mean(skipna=True), 2)
            std = round(df[column].std(ddof=1, skipna=True), 2)
            val_min = round(df[column].min(skipna=True), 2)
            val_max = round(df[column].max(skipna=True), 2)
            msg = f" {column}: \n mean: {mean}, \n std: {std}, \n minimum: {val_min}, \n maximum: {val_max}"
            messagebox.showinfo("Results", msg)
            results[column] = (mean, std, val_min, val_max)
            results["names"] = ("mean", "std", "val_min", "val_max")
    return results

def save_to_csv():
    resluts_df = pd.DataFrame(results)
    save_path = filedialog.asksaveasfilename(filetypes=[("CSV", "*.csv"), ("Wszystkie pliki", "*.*")])
    resluts_df.to_csv(save_path, index=None)

def find_col(df, name):
    target = name.casefold()
    for column in df.columns:
        if column.casefold() == target:
            return column
    return None

def plot_charts():
    date_min = combo_date_min.get()
    date_max = combo_date_max.get()
    df = read_file()
    columns = df.columns
    plt.close()
    fig, ax = plt.subplots()
    for column in columns:
        if is_numeric_dtype(df[column]):
            timestamp = find_col(df, 'timestamp')
            x = df[timestamp]
            y = df[column]
            ax.plot(x, y, label=column)
            ax.set_xlabel(timestamp)
            ax.set_ylabel(column)
            ax.grid(True, which='major', linestyle='--', alpha=0.4)
            ax.legend(loc='best')
            if date_min and date_max:
                ax.set_xlim(date_min, date_max)
            locator = mdates.AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(locator)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

    fig.tight_layout()
    plt.show()
    
def return_datetime(df):
    name = find_col(df, "timestamp")
    timestamp = list(df[name])
    combo_date_min.configure(values=timestamp)
    combo_date_max.configure(values=timestamp)
 
root = tk.Tk()
root.title("Case3")
root.geometry("640x520")

read_button = ttk.Button(root, text="Read file", command=get_path).pack(pady=6)
frame_actions = ttk.Frame(root)
frame_actions.pack(fill="x", pady=6)
calculate_button = ttk.Button(frame_actions, text="calculate", command=calculate).pack()
plot_button = ttk.Button(frame_actions, text="plot", command=plot_charts).pack()

frame_filter = ttk.Frame(root)
frame_filter.pack(fill="x")
ttk.Label(frame_filter, text="min date: ").pack()
combo_date_min = ttk.Combobox(frame_filter, values=[])
combo_date_min.pack()
ttk.Label(frame_filter, text="max date: ").pack()
combo_date_max = ttk.Combobox(frame_filter, values=[])
combo_date_max.pack()

save_button = ttk.Button(root, text="save", command=save_to_csv).pack(pady=6)

root.mainloop()
