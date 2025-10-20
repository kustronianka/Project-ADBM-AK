
import re
import pandas as pd
from Bio import SeqIO

path = r"C:\VisualStudio\ADBM AK\dna_sequences.fasta"

records = list(SeqIO.parse(path, "fasta"))

print(records)

df = pd.DataFrame({
            "id": [r.id for r in records],
            "description": [r.description for r in records],
            "sequence": [str(r.seq) for r in records],
        })
motyw = str(input("podaj motyw: "))

sequence = df["sequence"]

pozycje = {}
for i in range(0, len(df)):
    sequence = df["sequence"][i].upper()
    print(sequence)
    poz = []
    for match in re.finditer(f"(?={re.escape(motyw)})", sequence):
        poz.append(match.start())
        pozycje[i] = poz

pozycje = {}
for i in range(0, len(df)):
    sequence = df["sequence"][i].upper()
    print(sequence)
    poz = []
    for match in re.finditer(f"(?={re.escape(motyw)})", sequence):
        poz.append(match.start())
        pozycje[i] = poz
num_of_pos = {}
for i in pozycje:
    print(pozycje[i])
    num_of_pos[i] = len(pozycje[i])
    

