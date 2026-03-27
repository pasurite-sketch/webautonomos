#!/usr/bin/env python3
"""
=============================================================
SCORING & PRIORISATION PROSPECTS MOBILES
WebAutonomos.es
=============================================================
Ajoute un score de priorisation à chaque prospect et trie
par métier puis par score décroissant.

CRITÈRES DE SCORING (sur 100 points) :
- Note Google       : max 30 pts
- Nombre d'avis     : max 25 pts
- Nombre de photos  : max 20 pts
- Avis texte dispo  : max 15 pts
- Catégories GMB    : max 10 pts

Usage: python3 scorer_prospects.py
=============================================================
"""

import csv
from datetime import datetime

INPUT_FILE = "prospects_MOBILES.csv"
OUTPUT_FILE = "prospects_MOBILES_SCORES.csv"

# ============================================================
# FONCTIONS DE SCORING
# ============================================================

def score_note(note):
    """Note Google sur 30 points"""
    try:
        n = float(note)
    except (ValueError, TypeError):
        return 0
    
    if n >= 4.8:
        return 30
    elif n >= 4.5:
        return 25
    elif n >= 4.0:
        return 20
    elif n >= 3.5:
        return 12
    elif n >= 3.0:
        return 5
    else:
        return 0


def score_avis(nb_avis):
    """Nombre d'avis sur 25 points"""
    try:
        nb = int(nb_avis)
    except (ValueError, TypeError):
        return 0
    
    if nb >= 50:
        return 25
    elif nb >= 30:
        return 22
    elif nb >= 20:
        return 18
    elif nb >= 10:
        return 14
    elif nb >= 5:
        return 10
    elif nb >= 1:
        return 5
    else:
        return 0


def score_photos(nb_photos):
    """Nombre de photos sur 20 points"""
    try:
        nb = int(nb_photos)
    except (ValueError, TypeError):
        return 0
    
    if nb >= 5:
        return 20
    elif nb >= 3:
        return 15
    elif nb >= 1:
        return 8
    else:
        return 0


def score_avis_texte(row, header):
    """Avis texte disponibles sur 15 points (3 pts par avis avec texte)"""
    points = 0
    for i in range(1, 6):
        col_name = f"avis_{i}_texte"
        if col_name in header:
            idx = header.index(col_name)
            if idx < len(row) and row[idx].strip():
                points += 3
    return min(points, 15)


def score_categories(row, header):
    """Catégories GMB renseignées sur 10 points"""
    count = 0
    for i in range(1, 6):
        col_name = f"categorie_gmb_{i}"
        if col_name in header:
            idx = header.index(col_name)
            if idx < len(row) and row[idx].strip():
                count += 1
    
    if count >= 3:
        return 10
    elif count >= 2:
        return 7
    elif count >= 1:
        return 4
    else:
        return 0


def priorite_label(score):
    """Attribue un label de priorité"""
    if score >= 75:
        return "🔥 A - Prioritaire"
    elif score >= 55:
        return "⭐ B - Intéressant"
    elif score >= 35:
        return "📋 C - Standard"
    else:
        return "⏳ D - Faible"


# ============================================================
# LECTURE, SCORING ET TRI
# ============================================================

print("=" * 65)
print("🏆 SCORING & PRIORISATION PROSPECTS")
print(f"   Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 65)

print(f"\n📂 Lecture de {INPUT_FILE}...")

rows = []
header = None

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    
    # Index des colonnes clés
    note_idx = header.index("note") if "note" in header else None
    avis_idx = header.index("nb_avis") if "nb_avis" in header else None
    photos_idx = header.index("nb_photos") if "nb_photos" in header else None
    metier_idx = 0
    
    for row in reader:
        if len(row) < len(header):
            continue
        
        # Calculer les scores
        s_note = score_note(row[note_idx] if note_idx is not None else "")
        s_avis = score_avis(row[avis_idx] if avis_idx is not None else "")
        s_photos = score_photos(row[photos_idx] if photos_idx is not None else "")
        s_texte = score_avis_texte(row, header)
        s_cats = score_categories(row, header)
        
        total = s_note + s_avis + s_photos + s_texte + s_cats
        priorite = priorite_label(total)
        
        # Ajouter les colonnes de score
        row_scored = row + [
            str(total),
            priorite,
            str(s_note),
            str(s_avis),
            str(s_photos),
            str(s_texte),
            str(s_cats)
        ]
        
        rows.append(row_scored)

# Trier par métier (ASC) puis par score (DESC)
rows.sort(key=lambda x: (x[metier_idx].lower(), -int(x[len(header)])))

print(f"   ✅ {len(rows)} prospects scorés")

# ============================================================
# ÉCRITURE DU CSV
# ============================================================

# Nouvel en-tête avec colonnes de score
new_header = header + [
    "SCORE_TOTAL",
    "PRIORITE",
    "score_note",
    "score_nb_avis",
    "score_photos",
    "score_avis_texte",
    "score_categories"
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(new_header)
    for row in rows:
        writer.writerow(row)

# ============================================================
# STATISTIQUES
# ============================================================

print(f"\n{'=' * 65}")
print(f"📊 STATISTIQUES DE PRIORISATION")
print(f"{'=' * 65}")

# Par priorité
prio_counts = {}
for row in rows:
    p = row[len(header) + 1]
    prio_counts[p] = prio_counts.get(p, 0) + 1

print(f"\n🏆 Répartition par priorité :")
for p in ["🔥 A - Prioritaire", "⭐ B - Intéressant", "📋 C - Standard", "⏳ D - Faible"]:
    count = prio_counts.get(p, 0)
    pct = count / len(rows) * 100 if rows else 0
    bar = "█" * int(pct / 2)
    print(f"   {p:<25} : {count:>4} ({pct:.0f}%) {bar}")

# Par métier + priorité
print(f"\n📋 Détail par métier :")
metiers = sorted(set(row[metier_idx] for row in rows))

for metier in metiers:
    metier_rows = [r for r in rows if r[metier_idx] == metier]
    prio_a = sum(1 for r in metier_rows if "A - Prioritaire" in r[len(header) + 1])
    prio_b = sum(1 for r in metier_rows if "B - Intéressant" in r[len(header) + 1])
    prio_c = sum(1 for r in metier_rows if "C - Standard" in r[len(header) + 1])
    prio_d = sum(1 for r in metier_rows if "D - Faible" in r[len(header) + 1])
    
    # Meilleur prospect
    best = metier_rows[0]
    best_name = best[1]
    best_score = best[len(header)]
    
    print(f"\n   🔧 {metier.upper()} ({len(metier_rows)} prospects)")
    print(f"      🔥 A:{prio_a}  ⭐ B:{prio_b}  📋 C:{prio_c}  ⏳ D:{prio_d}")
    print(f"      👑 Meilleur: {best_name} (score {best_score}/100)")

# Top 10 global
print(f"\n{'=' * 65}")
print(f"👑 TOP 10 PROSPECTS GLOBAUX")
print(f"{'=' * 65}")

top10 = sorted(rows, key=lambda x: -int(x[len(header)]))[:10]
for i, row in enumerate(top10, 1):
    nom = row[1]
    metier = row[0]
    score = row[len(header)]
    note = row[note_idx] if note_idx else "?"
    nb_av = row[avis_idx] if avis_idx else "?"
    tel = row[5]
    print(f"   #{i:>2} [{score}/100] {nom}")
    print(f"       {metier} | ⭐{note} ({nb_av} avis) | 📱 {tel}")

print(f"\n{'=' * 65}")
print(f"✅ FICHIER GÉNÉRÉ : {OUTPUT_FILE}")
print(f"   → {len(rows)} prospects avec score et priorité")
print(f"   → Trié par métier puis par score décroissant")
print(f"   → Prêt à importer dans Google Sheets")
print(f"{'=' * 65}")
