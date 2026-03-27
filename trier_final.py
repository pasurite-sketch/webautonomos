#!/usr/bin/env python3
"""
=============================================================
TRI FINAL — Ordre correct par métier + score décroissant
WebAutonomos.es
=============================================================
"""

import csv

INPUT_FILE = "prospects_MOBILES_SCORES_CLEAN.csv"
OUTPUT_FILE = "prospects_MOBILES_SCORES_CLEAN.csv"

# Ordre souhaité des métiers
METIER_ORDER = {
    "carpintero madera": 1,
    "carpintero metal": 2,
    "carpintero (sin clasificar)": 3,
    "dentista": 4,
    "electricista": 5,
    "fisioterapeuta": 6,
    "fontanero": 7,
    "psicólogo": 8,
}

print("📂 Lecture...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

# Trouver les index
metier_idx = 0
score_idx = header.index("SCORE_TOTAL") if "SCORE_TOTAL" in header else None

print(f"   {len(rows)} lignes lues")

# Tri
def sort_key(row):
    metier = row[metier_idx].strip().lower()
    order = METIER_ORDER.get(metier, 99)
    try:
        score = -int(row[score_idx])
    except (ValueError, TypeError, IndexError):
        score = 0
    return (order, score)

rows.sort(key=sort_key)

# Écriture
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)

# Vérification
print(f"\n✅ Trié ! Ordre final :")
current_metier = ""
for row in rows:
    m = row[metier_idx]
    if m != current_metier:
        count = sum(1 for r in rows if r[metier_idx] == m)
        print(f"   {m:<35} : {count} prospects")
        current_metier = m

print(f"\n📊 Fichier : {OUTPUT_FILE} — prêt à importer")
