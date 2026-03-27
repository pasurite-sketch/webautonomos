#!/usr/bin/env python3
"""
=============================================================
ENRICHISSEMENT PROSPECTS — Province d'Alicante
WebAutonomos.es
=============================================================
- Lit le JSON existant (1754 prospects)
- Récupère les catégories GMB (types) pour chaque prospect
- Génère un CSV complet avec :
  * metier
  * catégories GMB (5 colonnes)
  * 5 colonnes d'avis
  * 5 colonnes de photos
  * toutes les autres données

Usage: python3 enrichir_prospects.py
=============================================================
"""

import json
import urllib.request
import urllib.parse
import ssl
import time
import csv
from datetime import datetime

API_KEY = "AIzaSyDYOoF-ybVDXPXhmnOq1TChpFQkEgr9meo"

# SSL config pour macOS
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ============================================================
# MAPPING DES TYPES GMB EN ESPAGNOL
# ============================================================

TYPES_ES = {
    "electrician": "Electricista",
    "plumber": "Fontanero",
    "carpenter": "Carpintero",
    "dentist": "Dentista",
    "physiotherapist": "Fisioterapeuta",
    "psychologist": "Psicólogo",
    "general_contractor": "Contratista general",
    "home_improvement_store": "Tienda de reformas",
    "hardware_store": "Ferretería",
    "locksmith": "Cerrajero",
    "painter": "Pintor",
    "roofing_contractor": "Techador",
    "hvac_contractor": "Climatización",
    "moving_company": "Mudanzas",
    "real_estate_agency": "Inmobiliaria",
    "insurance_agency": "Agencia de seguros",
    "accounting": "Contabilidad",
    "lawyer": "Abogado",
    "notary": "Notaría",
    "doctor": "Médico",
    "health": "Salud",
    "hospital": "Hospital",
    "pharmacy": "Farmacia",
    "veterinary_care": "Veterinario",
    "beauty_salon": "Salón de belleza",
    "hair_care": "Peluquería",
    "spa": "Spa",
    "gym": "Gimnasio",
    "restaurant": "Restaurante",
    "cafe": "Cafetería",
    "bar": "Bar",
    "store": "Tienda",
    "shopping_mall": "Centro comercial",
    "car_repair": "Taller mecánico",
    "car_dealer": "Concesionario",
    "gas_station": "Gasolinera",
    "parking": "Aparcamiento",
    "school": "Escuela",
    "university": "Universidad",
    "church": "Iglesia",
    "local_government_office": "Ayuntamiento",
    "post_office": "Correos",
    "bank": "Banco",
    "atm": "Cajero automático",
    "point_of_interest": "Punto de interés",
    "establishment": "Establecimiento",
    "furniture_store": "Tienda de muebles",
    "home_goods_store": "Tienda del hogar",
    "electronics_store": "Tienda de electrónica",
    "clothing_store": "Tienda de ropa",
    "florist": "Floristería",
    "laundry": "Lavandería",
    "dental_clinic": "Clínica dental",
    "medical_center": "Centro médico",
    "counselor": "Consejero",
    "mental_health": "Salud mental",
    "therapy": "Terapia",
    "rehabilitation_center": "Centro de rehabilitación",
    "chiropractor": "Quiropráctico",
    "podiatrist": "Podólogo",
    "optometrist": "Óptico",
    "speech_pathologist": "Logopeda",
}

def translate_type(t):
    """Traduit un type GMB en espagnol, ou retourne le type formaté"""
    if t in TYPES_ES:
        return TYPES_ES[t]
    # Formater : remplacer _ par espace, capitaliser
    return t.replace("_", " ").title()


# ============================================================
# FONCTION API
# ============================================================

def get_place_types(place_id):
    """Récupère uniquement les types/catégories d'un lieu"""
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        "place_id": place_id,
        "fields": "types",
        "language": "es",
        "key": API_KEY
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        if data.get("status") == "OK":
            return data.get("result", {}).get("types", [])
        return []
    except Exception as e:
        print(f"    ❌ Erreur: {e}")
        return []


# ============================================================
# CHARGEMENT DU JSON EXISTANT
# ============================================================

print("=" * 65)
print("🔄 ENRICHISSEMENT PROSPECTS — Province d'Alicante")
print(f"   Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 65)

json_file = "prospects_alicante_141_complet.json"

print(f"\n📂 Chargement de {json_file}...")
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

prospects = data["prospects"]
print(f"   ✅ {len(prospects)} prospects chargés")

# ============================================================
# RÉCUPÉRATION DES CATÉGORIES GMB
# ============================================================

# Types génériques à exclure (pas intéressants pour le client)
TYPES_EXCLUS = {
    "point_of_interest",
    "establishment",
    "political",
    "locality",
    "sublocality",
    "administrative_area_level_1",
    "administrative_area_level_2",
    "country",
    "postal_code",
    "route",
    "street_address",
    "premise",
    "subpremise",
    "geocode",
    "plus_code",
}

print(f"\n📡 Récupération des catégories GMB pour {len(prospects)} prospects...")
print(f"   (Environ {len(prospects) * 0.2:.0f} secondes / {len(prospects) * 0.15 / 60:.0f} minutes)\n")

api_calls = 0
for i, prospect in enumerate(prospects):
    progress = f"[{i+1}/{len(prospects)}]"
    
    if (i+1) % 50 == 0 or i == 0:
        print(f"  {progress} {prospect['nom']}...", flush=True)
    
    types_raw = get_place_types(prospect["place_id"])
    api_calls += 1
    
    # Filtrer les types génériques et traduire
    types_filtered = [t for t in types_raw if t not in TYPES_EXCLUS]
    types_translated = [translate_type(t) for t in types_filtered]
    
    # Stocker dans le prospect
    prospect["categories_gmb"] = types_translated
    
    time.sleep(0.1)  # Respect des quotas

print(f"\n   ✅ {api_calls} appels API effectués")

# ============================================================
# GÉNÉRATION DU CSV COMPLET
# ============================================================

print(f"\n📊 Génération du CSV enrichi...")

csv_file = "prospects_alicante_COMPLET.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    
    # En-tête
    writer.writerow([
        "metier",
        "nom",
        "adresse",
        "ville_recherche",
        "comarca",
        "telephone",
        "telephone_intl",
        "note",
        "nb_avis",
        "nb_photos",
        "google_maps",
        "place_id",
        "horaires",
        "categorie_gmb_1",
        "categorie_gmb_2",
        "categorie_gmb_3",
        "categorie_gmb_4",
        "categorie_gmb_5",
        "avis_1_auteur",
        "avis_1_note",
        "avis_1_texte",
        "avis_2_auteur",
        "avis_2_note",
        "avis_2_texte",
        "avis_3_auteur",
        "avis_3_note",
        "avis_3_texte",
        "avis_4_auteur",
        "avis_4_note",
        "avis_4_texte",
        "avis_5_auteur",
        "avis_5_note",
        "avis_5_texte",
        "photo_1",
        "photo_2",
        "photo_3",
        "photo_4",
        "photo_5",
        "latitude",
        "longitude",
    ])
    
    for p in prospects:
        # Nettoyer les textes (supprimer retours à la ligne)
        def clean(text):
            if not text:
                return ""
            return str(text).replace("\n", " ").replace("\r", " ").strip()
        
        # Catégories GMB (5 colonnes)
        cats = p.get("categories_gmb", [])
        cat_cols = [cats[i] if i < len(cats) else "" for i in range(5)]
        
        # Avis (5 × 3 colonnes : auteur, note, texte)
        avis = p.get("avis", [])
        # Trier par note décroissante pour avoir les meilleurs en premier
        avis_sorted = sorted(avis, key=lambda x: x.get("note", 0), reverse=True)
        
        avis_cols = []
        for i in range(5):
            if i < len(avis_sorted):
                a = avis_sorted[i]
                avis_cols.extend([
                    clean(a.get("auteur", "")),
                    a.get("note", ""),
                    clean(a.get("texte", ""))
                ])
            else:
                avis_cols.extend(["", "", ""])
        
        # Photos (5 colonnes)
        photos = p.get("photos_urls", [])
        photo_cols = [photos[i] if i < len(photos) else "" for i in range(5)]
        
        # Horaires (sur une ligne)
        horaires = " | ".join(p.get("horaires", [])) if p.get("horaires") else ""
        
        writer.writerow([
            clean(p.get("metier", "")),
            clean(p.get("nom", "")),
            clean(p.get("adresse", "")),
            clean(p.get("ville_recherche", "")),
            clean(p.get("comarca", "")),
            clean(p.get("telephone", "")),
            clean(p.get("telephone_intl", "")),
            p.get("note", ""),
            p.get("nb_avis", ""),
            p.get("nb_photos", ""),
            clean(p.get("google_maps", "")),
            clean(p.get("place_id", "")),
            clean(horaires),
            *cat_cols,
            *avis_cols,
            *photo_cols,
            p.get("latitude", ""),
            p.get("longitude", ""),
        ])

# ============================================================
# MISE À JOUR DU JSON
# ============================================================

print(f"📄 Mise à jour du JSON avec les catégories GMB...")

data["prospects"] = prospects
data["enrichi"] = True
data["date_enrichissement"] = datetime.now().strftime("%Y-%m-%d %H:%M")

json_enrichi = "prospects_alicante_141_ENRICHI.json"
with open(json_enrichi, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================
# VÉRIFICATION
# ============================================================

line_count = sum(1 for _ in open(csv_file))
cats_count = sum(1 for p in prospects if p.get("categories_gmb"))
avis_count = sum(1 for p in prospects if p.get("avis"))

print(f"\n{'=' * 65}")
print(f"✅ ENRICHISSEMENT TERMINÉ !")
print(f"{'=' * 65}")
print(f"   📊 CSV : {csv_file}")
print(f"      → {line_count - 1} prospects ({line_count} lignes avec header)")
print(f"      → 41 colonnes (metier + données + 5 catégories + 15 avis + 5 photos + coords)")
print(f"   📄 JSON : {json_enrichi}")
print(f"   📡 Appels API : {api_calls}")
print(f"   🏷️  Prospects avec catégories : {cats_count}/{len(prospects)}")
print(f"   💬 Prospects avec avis : {avis_count}/{len(prospects)}")
print(f"\n🚀 Fichier prêt à importer dans Google Sheets CRM !")
print(f"{'=' * 65}")
