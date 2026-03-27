#!/usr/bin/env python3
"""
=============================================================
TRI PROSPECTS — Mobile vs Autres
WebAutonomos.es
=============================================================
Sépare les prospects en 2 fichiers :
- MOBILES : téléphone commençant par 6 ou 7 (WhatsApp-ready)
- AUTRES : pas de téléphone, ou fixe (9xx), ou format inconnu

Les deux fichiers sont triés par métier.

Usage: python3 trier_prospects_telephone.py
=============================================================
"""

import csv
from datetime import datetime

INPUT_FILE = "prospects_alicante_COMPLET.csv"
OUTPUT_MOBILES = "prospects_MOBILES.csv"
OUTPUT_AUTRES = "prospects_AUTRES.csv"

def is_mobile(telephone):
    """Vérifie si un numéro espagnol est un mobile (commence par 6 ou 7)"""
    if not telephone or not telephone.strip():
        return False
    
    # Nettoyer : enlever espaces, tirets, points, parenthèses, +34
    clean = telephone.strip()
    clean = clean.replace(" ", "").replace("-", "").replace(".", "")
    clean = clean.replace("(", "").replace(")", "")
    
    # Enlever le préfixe international +34 ou 0034
    if clean.startswith("+34"):
        clean = clean[3:]
    elif clean.startswith("0034"):
        clean = clean[4:]
    
    # Vérifier si commence par 6 ou 7
    return len(clean) >= 9 and clean[0] in ("6", "7")

# ============================================================
# LECTURE ET TRI
# ============================================================

print("=" * 65)
print("📱 TRI PROSPECTS — Mobile vs Autres")
print(f"   Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 65)

print(f"\n📂 Lecture de {INPUT_FILE}...")

mobiles = []
autres = []
header = None

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    
    # Trouver l'index de la colonne téléphone
    tel_idx = header.index("telephone") if "telephone" in header else 5
    metier_idx = 0  # Première colonne
    
    for row in reader:
        if len(row) < len(header):
            continue
        
        telephone = row[tel_idx] if tel_idx < len(row) else ""
        
        if is_mobile(telephone):
            mobiles.append(row)
        else:
            autres.append(row)

# Trier par métier (1ère colonne)
mobiles.sort(key=lambda x: x[metier_idx].lower())
autres.sort(key=lambda x: x[metier_idx].lower())

# ============================================================
# ÉCRITURE DES FICHIERS
# ============================================================

print(f"\n📊 Résultats :")
print(f"   📱 Mobiles (6xx/7xx) : {len(mobiles)} prospects → WhatsApp-ready ✅")
print(f"   📞 Autres (fixes/vides) : {len(autres)} prospects → feuille séparée")

# Fichier MOBILES
with open(OUTPUT_MOBILES, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    for row in mobiles:
        writer.writerow(row)

# Fichier AUTRES
with open(OUTPUT_AUTRES, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    for row in autres:
        writer.writerow(row)

# ============================================================
# STATS PAR MÉTIER
# ============================================================

print(f"\n📱 MOBILES par métier :")
metier_counts_mob = {}
for row in mobiles:
    m = row[metier_idx]
    metier_counts_mob[m] = metier_counts_mob.get(m, 0) + 1
for m, c in sorted(metier_counts_mob.items(), key=lambda x: x[1], reverse=True):
    print(f"   {m:<16} : {c:>4}")

print(f"\n📞 AUTRES par métier :")
metier_counts_aut = {}
for row in autres:
    m = row[metier_idx]
    metier_counts_aut[m] = metier_counts_aut.get(m, 0) + 1
for m, c in sorted(metier_counts_aut.items(), key=lambda x: x[1], reverse=True):
    print(f"   {m:<16} : {c:>4}")

# Détail des "autres" : combien sans tél vs fixes
sans_tel = sum(1 for row in autres if not row[tel_idx].strip())
fixes = len(autres) - sans_tel
print(f"\n   Détail 'Autres' :")
print(f"   → Sans téléphone : {sans_tel}")
print(f"   → Fixes (9xx)    : {fixes}")

print(f"\n{'=' * 65}")
print(f"✅ FICHIERS GÉNÉRÉS :")
print(f"   📱 {OUTPUT_MOBILES} → {len(mobiles)} prospects (importer dans feuille principale)")
print(f"   📞 {OUTPUT_AUTRES} → {len(autres)} prospects (importer dans feuille adjacente)")
print(f"\n   📋 Importer dans Google Sheets 'Prospects Alicante' :")
print(f"      1. Feuille 'prospects_alicante_COMPLET' → remplacer par {OUTPUT_MOBILES}")
print(f"      2. Nouvelle feuille 'Prospects Sans Mobile' → importer {OUTPUT_AUTRES}")
print(f"{'=' * 65}")
