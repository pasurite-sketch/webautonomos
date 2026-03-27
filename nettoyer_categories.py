#!/usr/bin/env python3
"""
=============================================================
NETTOYAGE PROSPECTS — Suppression catégories non pertinentes
WebAutonomos.es
=============================================================
Supprime les prospects dont categorie_gmb_1 correspond à
des métiers hors cible, et les reporte dans un fichier séparé.

Usage: python3 nettoyer_categories.py
=============================================================
"""

import csv
from datetime import datetime

INPUT_FILE = "prospects_MOBILES_SCORES.csv"
OUTPUT_CLEAN = "prospects_MOBILES_SCORES_CLEAN.csv"
OUTPUT_REJETES = "prospects_REJETES_CATEGORIE.csv"

# Catégories à supprimer
CATEGORIES_EXCLUES = {
    "gimnasio",
    "bar",
    "tienda",
    "library",
    "peluquería",
    "peluqueria",
    "salón de belleza",
    "salon de belleza",
    "book store",
    "finance",
}

print("=" * 65)
print("🧹 NETTOYAGE PROSPECTS — Catégories non pertinentes")
print(f"   Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 65)

print(f"\n📂 Lecture de {INPUT_FILE}...")

header = None
clean_rows = []
rejected_rows = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    
    # Trouver l'index de categorie_gmb_1
    cat1_idx = header.index("categorie_gmb_1") if "categorie_gmb_1" in header else None
    
    if cat1_idx is None:
        print("❌ Colonne 'categorie_gmb_1' introuvable !")
        exit(1)
    
    for row in reader:
        if len(row) <= cat1_idx:
            clean_rows.append(row)
            continue
        
        cat1 = row[cat1_idx].strip().lower()
        
        if cat1 in CATEGORIES_EXCLUES:
            rejected_rows.append(row)
        else:
            clean_rows.append(row)

print(f"   ✅ {len(clean_rows)} prospects conservés")
print(f"   ❌ {len(rejected_rows)} prospects supprimés")

# ============================================================
# DÉTAIL DES SUPPRESSIONS
# ============================================================

print(f"\n🗑️  Détail des suppressions par catégorie :")
cat_counts = {}
for row in rejected_rows:
    cat = row[cat1_idx].strip()
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   {cat:<25} : {count:>3} supprimés")

# Détail par métier des suppressions
print(f"\n📋 Suppressions par métier :")
metier_counts = {}
for row in rejected_rows:
    m = row[0]
    metier_counts[m] = metier_counts.get(m, 0) + 1

for m, count in sorted(metier_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   {m:<20} : {count:>3} supprimés")

# ============================================================
# ÉCRITURE DES FICHIERS
# ============================================================

# Fichier nettoyé
with open(OUTPUT_CLEAN, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    for row in clean_rows:
        writer.writerow(row)

# Fichier rejetés
with open(OUTPUT_REJETES, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    for row in rejected_rows:
        writer.writerow(row)

print(f"\n{'=' * 65}")
print(f"✅ NETTOYAGE TERMINÉ !")
print(f"{'=' * 65}")
print(f"   📊 {OUTPUT_CLEAN} → {len(clean_rows)} prospects (à importer)")
print(f"   🗑️  {OUTPUT_REJETES} → {len(rejected_rows)} rejetés (pour vérification)")
print(f"\n   Dans Google Sheets :")
print(f"   → Importer {OUTPUT_CLEAN} → 'Remplacer la feuille active'")
print(f"{'=' * 65}")
