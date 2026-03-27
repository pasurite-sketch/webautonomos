#!/usr/bin/env python3
"""
=============================================================
RECLASSIFICATION CARPINTEROS — Madera / Metal / Sin clasificar
WebAutonomos.es
=============================================================
Modifie la colonne "metier" pour distinguer :
- Carpintero madera
- Carpintero metal  
- Carpintero (sin clasificar)

Basé sur le nom du business + catégories GMB.

Usage: python3 reclassifier_carpinteros.py
=============================================================
"""

import csv
from datetime import datetime

INPUT_FILE = "prospects_MOBILES_SCORES_CLEAN.csv"
OUTPUT_FILE = "prospects_MOBILES_SCORES_CLEAN.csv"  # Écrase le même fichier

# ============================================================
# MOTS-CLÉS DE CLASSIFICATION
# ============================================================

METAL_KEYWORDS = [
    "aluminio", "aluminios", "alumini", "pvc", "metal", "metálica",
    "metalica", "metálico", "metalico", "metalúrgic", "metalurgic",
    "herrería", "herreria", "herrero", "hierro", "acero",
    "soldadura", "soldador", "cerrajería", "cerrajeria", "cerrajero",
    "persiana", "ventana", "ventanas", "cristalería", "cristaleria",
    "mampara", "mosquitera", "reja", "forja", "inoxidable",
    "ferro", "ferr", "chapa", "galvaniz",
]

WOOD_KEYWORDS = [
    "madera", "ebanist", "mueble", "muebles", "cocina", "cocinas",
    "parquet", "tarima", "armario", "puerta", "puertas",
    "restauración", "restauracion", "barniz", "laquer", "laca",
    "fusta", "roble", "pino", "nogal", "caoba", "melamina",
    "tablero", "contrachapado", "aglomerado",
]


def classify_carpintero(nom, categories):
    """Classifie un carpintero en madera, metal ou sin clasificar"""
    full_text = nom.lower() + " " + " ".join(categories).lower()
    
    metal_score = sum(1 for kw in METAL_KEYWORDS if kw in full_text)
    wood_score = sum(1 for kw in WOOD_KEYWORDS if kw in full_text)
    
    if metal_score > wood_score:
        return "Carpintero metal"
    elif wood_score > metal_score:
        return "Carpintero madera"
    else:
        return "Carpintero (sin clasificar)"


# ============================================================
# LECTURE ET RECLASSIFICATION
# ============================================================

print("=" * 65)
print("🪚 RECLASSIFICATION CARPINTEROS")
print(f"   Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 65)

print(f"\n📂 Lecture de {INPUT_FILE}...")

header = None
rows = []
stats = {"Carpintero madera": 0, "Carpintero metal": 0, "Carpintero (sin clasificar)": 0}
examples = {"Carpintero madera": [], "Carpintero metal": [], "Carpintero (sin clasificar)": []}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    
    metier_idx = 0  # Première colonne
    nom_idx = 1
    
    # Trouver les index des catégories GMB
    cat_indices = []
    for i in range(1, 6):
        col = f"categorie_gmb_{i}"
        if col in header:
            cat_indices.append(header.index(col))
    
    for row in reader:
        if len(row) < len(header):
            rows.append(row)
            continue
        
        metier = row[metier_idx].strip().lower()
        
        if metier == "carpintero":
            nom = row[nom_idx] if nom_idx < len(row) else ""
            categories = [row[idx] for idx in cat_indices if idx < len(row)]
            
            new_metier = classify_carpintero(nom, categories)
            row[metier_idx] = new_metier
            
            stats[new_metier] += 1
            if len(examples[new_metier]) < 5:
                examples[new_metier].append(nom)
        
        rows.append(row)

# ============================================================
# ÉCRITURE
# ============================================================

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)

# ============================================================
# RÉSULTATS
# ============================================================

total_carp = sum(stats.values())
print(f"\n   ✅ {total_carp} carpinteros reclassifiés :\n")

for sous_type, count in sorted(stats.items()):
    pct = count / total_carp * 100 if total_carp else 0
    bar = "█" * int(pct / 2)
    print(f"   {sous_type:<30} : {count:>3} ({pct:.0f}%) {bar}")
    for ex in examples[sous_type]:
        print(f"      → {ex}")

print(f"\n{'=' * 65}")
print(f"✅ FICHIER MIS À JOUR : {OUTPUT_FILE}")
print(f"   → Colonne 'metier' modifiée pour les carpinteros")
print(f"   → Importer dans Google Sheets → 'Remplacer la feuille active'")
print(f"{'=' * 65}")
