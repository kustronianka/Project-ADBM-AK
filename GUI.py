
import tkinter as tk
from tkinter import ttk

def wczytaj_plik():
    pass

def przycisk_przeszukaj():
    pass

def przycisk_drukuj():
    pass

def przycisk_zapisz():
    pass

okno_glowne = tk.Tk()
okno_glowne.title("Analiza motywów DNA")
okno_glowne.geometry("520x420")

# przycisk: wczytaj plik
przycisk_wczytaj = ttk.Button(okno_glowne, text="Wczytaj plik FASTA", command=wczytaj_plik)
przycisk_wczytaj.pack(pady=6)

# pole + przycisk: przeszukaj (popup, bez wykresu)
pole_motyw_szukaj = ttk.Entry(okno_glowne, width=60)
pole_motyw_szukaj.pack(pady=3)
pole_motyw_szukaj.insert(0, "wpisz motyw do wyszukania (np. TATA)")
przycisk_przeszukaj = ttk.Button(okno_glowne, text="Przeszukaj (wszystkie geny)", command=przycisk_przeszukaj)
przycisk_przeszukaj.pack(pady=4)

# pole + przycisk: drukuj (rysuje wszystkie geny, różne kolory)
etykieta_wykres = ttk.Label(okno_glowne, text="Motyw do wykresu:")
etykieta_wykres.pack(pady=(10, 2))
pole_motyw_wykres = ttk.Entry(okno_glowne, width=60)
pole_motyw_wykres.pack(pady=2)
pole_motyw_wykres.insert(0, "np. TATA")
przycisk_drukuj = ttk.Button(okno_glowne, text="Drukuj wykres (wszystkie geny)", command=przycisk_drukuj)
przycisk_drukuj.pack(pady=8)

# przycisk: zapisz CSV (na samym dole)
przycisk_zapisz = ttk.Button(okno_glowne, text="Zapisz wyniki do CSV", command=przycisk_zapisz)
przycisk_zapisz.pack(side="bottom", pady=12)

okno_glowne.mainloop()
