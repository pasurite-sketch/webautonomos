#!/usr/bin/env python3
"""
=============================================================
PROSPECTION COMPLÈTE — Province d'Alicante (141 municipios)
WebAutonomos.es
=============================================================
Recherche tous les prospects SANS site web pour :
- 6 métiers cibles
- Les 141 municipios de la province d'Alicante
- Filtre par population minimum (configurable)

Usage: python3 prospection_alicante_completa.py
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

# ============================================================
# CONFIGURATION
# ============================================================

METIERS = [
    "electricista",
    "fontanero",
    "carpintero",
    "dentista",
    "fisioterapeuta",
    "psicólogo"
]

# Filtre population minimum (modifiable)
# Recommandé : 2000 pour économiser les appels API
# Mettre à 0 pour chercher TOUS les 141 municipios
POPULATION_MIN = 0

# ============================================================
# LES 141 MUNICIPIOS DE LA PROVINCE D'ALICANTE
# avec population (INE 2022) et coordonnées
# ============================================================

MUNICIPIOS = [
    # --- CAMPO DE ALICANTE (L'ALACANTÍ) ---
    {"nom": "Alicante", "pop": 338577, "lat": 38.3452, "lng": -0.4815, "comarca": "Alacantí"},
    {"nom": "San Vicente del Raspeig", "pop": 59587, "lat": 38.3964, "lng": -0.5255, "comarca": "Alacantí"},
    {"nom": "El Campello", "pop": 29409, "lat": 38.4284, "lng": -0.3900, "comarca": "Alacantí"},
    {"nom": "Mutxamel", "pop": 26192, "lat": 38.4153, "lng": -0.4419, "comarca": "Alacantí"},
    {"nom": "San Juan de Alicante", "pop": 24053, "lat": 38.4013, "lng": -0.4362, "comarca": "Alacantí"},
    {"nom": "Jijona", "pop": 6860, "lat": 38.5420, "lng": -0.5095, "comarca": "Alacantí"},
    {"nom": "Agost", "pop": 4948, "lat": 38.4393, "lng": -0.6340, "comarca": "Alacantí"},
    {"nom": "Busot", "pop": 3343, "lat": 38.4866, "lng": -0.4045, "comarca": "Alacantí"},
    {"nom": "Aigües", "pop": 1085, "lat": 38.4872, "lng": -0.3665, "comarca": "Alacantí"},
    
    # --- MARINA ALTA ---
    {"nom": "Dénia", "pop": 43899, "lat": 38.8408, "lng": 0.1057, "comarca": "Marina Alta"},
    {"nom": "Jávea", "pop": 28731, "lat": 38.7837, "lng": 0.1639, "comarca": "Marina Alta"},
    {"nom": "Calpe", "pop": 24096, "lat": 38.6447, "lng": 0.0446, "comarca": "Marina Alta"},
    {"nom": "Teulada", "pop": 12515, "lat": 38.7295, "lng": 0.1038, "comarca": "Marina Alta"},
    {"nom": "Benissa", "pop": 11871, "lat": 38.7138, "lng": 0.0482, "comarca": "Marina Alta"},
    {"nom": "Pego", "pop": 10485, "lat": 38.8428, "lng": -0.1189, "comarca": "Marina Alta"},
    {"nom": "Pedreguer", "pop": 8558, "lat": 38.7923, "lng": 0.0355, "comarca": "Marina Alta"},
    {"nom": "Ondara", "pop": 7085, "lat": 38.8271, "lng": 0.0094, "comarca": "Marina Alta"},
    {"nom": "Gata de Gorgos", "pop": 6364, "lat": 38.7726, "lng": 0.0836, "comarca": "Marina Alta"},
    {"nom": "El Verger", "pop": 5101, "lat": 38.8546, "lng": 0.0167, "comarca": "Marina Alta"},
    {"nom": "Benitatxell", "pop": 4687, "lat": 38.7259, "lng": 0.1433, "comarca": "Marina Alta"},
    {"nom": "Jalón", "pop": 2931, "lat": 38.7325, "lng": -0.0153, "comarca": "Marina Alta"},
    {"nom": "Els Poblets", "pop": 2763, "lat": 38.8565, "lng": 0.0550, "comarca": "Marina Alta"},
    {"nom": "Orba", "pop": 2379, "lat": 38.7998, "lng": -0.0738, "comarca": "Marina Alta"},
    {"nom": "Beniarbeig", "pop": 2267, "lat": 38.8278, "lng": -0.0285, "comarca": "Marina Alta"},
    {"nom": "Alcalalí", "pop": 1349, "lat": 38.7513, "lng": -0.0391, "comarca": "Marina Alta"},
    {"nom": "Benidoleig", "pop": 1232, "lat": 38.8084, "lng": -0.0426, "comarca": "Marina Alta"},
    {"nom": "Parcent", "pop": 1003, "lat": 38.7347, "lng": -0.0762, "comarca": "Marina Alta"},
    {"nom": "Llíber", "pop": 967, "lat": 38.7428, "lng": -0.0094, "comarca": "Marina Alta"},
    {"nom": "La Vall de Laguar", "pop": 873, "lat": 38.7778, "lng": -0.1134, "comarca": "Marina Alta"},
    {"nom": "Sanet y Negrals", "pop": 737, "lat": 38.8175, "lng": -0.0130, "comarca": "Marina Alta"},
    {"nom": "Ràfol d'Almúnia", "pop": 721, "lat": 38.8350, "lng": -0.0590, "comarca": "Marina Alta"},
    {"nom": "Senija", "pop": 670, "lat": 38.7232, "lng": 0.0148, "comarca": "Marina Alta"},
    {"nom": "Adsubia", "pop": 616, "lat": 38.8133, "lng": -0.1520, "comarca": "Marina Alta"},
    {"nom": "Vall de Gallinera", "pop": 581, "lat": 38.8005, "lng": -0.2285, "comarca": "Marina Alta"},
    {"nom": "Murla", "pop": 540, "lat": 38.7572, "lng": -0.0768, "comarca": "Marina Alta"},
    {"nom": "Benigembla", "pop": 512, "lat": 38.7483, "lng": -0.1045, "comarca": "Marina Alta"},
    {"nom": "Benimeli", "pop": 419, "lat": 38.8238, "lng": -0.0495, "comarca": "Marina Alta"},
    {"nom": "Castell de Castells", "pop": 426, "lat": 38.7232, "lng": -0.1872, "comarca": "Marina Alta"},
    {"nom": "Sagra", "pop": 442, "lat": 38.8260, "lng": -0.0700, "comarca": "Marina Alta"},
    {"nom": "Tormos", "pop": 339, "lat": 38.8106, "lng": -0.0888, "comarca": "Marina Alta"},
    {"nom": "Vall d'Ebo", "pop": 230, "lat": 38.8049, "lng": -0.1730, "comarca": "Marina Alta"},
    {"nom": "Vall d'Alcalà", "pop": 174, "lat": 38.7669, "lng": -0.2058, "comarca": "Marina Alta"},
    
    # --- MARINA BAIXA ---
    {"nom": "Benidorm", "pop": 69738, "lat": 38.5410, "lng": -0.1225, "comarca": "Marina Baixa"},
    {"nom": "Villajoyosa", "pop": 36093, "lat": 38.5076, "lng": -0.2334, "comarca": "Marina Baixa"},
    {"nom": "Altea", "pop": 23010, "lat": 38.5990, "lng": -0.0513, "comarca": "Marina Baixa"},
    {"nom": "Alfaz del Pi", "pop": 20668, "lat": 38.5804, "lng": -0.1006, "comarca": "Marina Baixa"},
    {"nom": "La Nucia", "pop": 18624, "lat": 38.6108, "lng": -0.1270, "comarca": "Marina Baixa"},
    {"nom": "Finestrat", "pop": 7909, "lat": 38.5637, "lng": -0.1690, "comarca": "Marina Baixa"},
    {"nom": "Callosa d'en Sarrià", "pop": 7653, "lat": 38.6506, "lng": -0.1232, "comarca": "Marina Baixa"},
    {"nom": "Polop", "pop": 5339, "lat": 38.6282, "lng": -0.1267, "comarca": "Marina Baixa"},
    {"nom": "Relleu", "pop": 1248, "lat": 38.5854, "lng": -0.2798, "comarca": "Marina Baixa"},
    {"nom": "Orxeta", "pop": 840, "lat": 38.5632, "lng": -0.2505, "comarca": "Marina Baixa"},
    {"nom": "Tàrbena", "pop": 630, "lat": 38.6847, "lng": -0.1106, "comarca": "Marina Baixa"},
    {"nom": "Sella", "pop": 607, "lat": 38.6119, "lng": -0.2700, "comarca": "Marina Baixa"},
    {"nom": "Benimantell", "pop": 499, "lat": 38.6627, "lng": -0.1903, "comarca": "Marina Baixa"},
    {"nom": "Bolulla", "pop": 413, "lat": 38.6730, "lng": -0.1263, "comarca": "Marina Baixa"},
    {"nom": "Confrides", "pop": 282, "lat": 38.6713, "lng": -0.2663, "comarca": "Marina Baixa"},
    {"nom": "Guadalest", "pop": 258, "lat": 38.6759, "lng": -0.1918, "comarca": "Marina Baixa"},
    {"nom": "Beniardá", "pop": 218, "lat": 38.6771, "lng": -0.2098, "comarca": "Marina Baixa"},
    {"nom": "Benifato", "pop": 139, "lat": 38.6667, "lng": -0.2268, "comarca": "Marina Baixa"},
    
    # --- EL COMTAT (CONDADO DE COCENTAINA) ---
    {"nom": "Cocentaina", "pop": 11298, "lat": 38.7443, "lng": -0.4423, "comarca": "El Comtat"},
    {"nom": "Muro de Alcoy", "pop": 9303, "lat": 38.7804, "lng": -0.4323, "comarca": "El Comtat"},
    {"nom": "Beniarrés", "pop": 1078, "lat": 38.8213, "lng": -0.3720, "comarca": "El Comtat"},
    {"nom": "Benilloba", "pop": 740, "lat": 38.7080, "lng": -0.3830, "comarca": "El Comtat"},
    {"nom": "Planes", "pop": 699, "lat": 38.8043, "lng": -0.3453, "comarca": "El Comtat"},
    {"nom": "Agres", "pop": 589, "lat": 38.7870, "lng": -0.5157, "comarca": "El Comtat"},
    {"nom": "Lorcha", "pop": 565, "lat": 38.8348, "lng": -0.3417, "comarca": "El Comtat"},
    {"nom": "Gaianes", "pop": 548, "lat": 38.7767, "lng": -0.3848, "comarca": "El Comtat"},
    {"nom": "Alquería de Aznar", "pop": 489, "lat": 38.7497, "lng": -0.4623, "comarca": "El Comtat"},
    {"nom": "Alfafara", "pop": 417, "lat": 38.7792, "lng": -0.5328, "comarca": "El Comtat"},
    {"nom": "Benimarfull", "pop": 410, "lat": 38.7645, "lng": -0.3893, "comarca": "El Comtat"},
    {"nom": "Gorga", "pop": 270, "lat": 38.7148, "lng": -0.3515, "comarca": "El Comtat"},
    {"nom": "Alcocer de Planes", "pop": 254, "lat": 38.7939, "lng": -0.4008, "comarca": "El Comtat"},
    {"nom": "Millena", "pop": 243, "lat": 38.7317, "lng": -0.3620, "comarca": "El Comtat"},
    {"nom": "Alcoleja", "pop": 196, "lat": 38.6917, "lng": -0.3402, "comarca": "El Comtat"},
    {"nom": "Benasau", "pop": 171, "lat": 38.6968, "lng": -0.3232, "comarca": "El Comtat"},
    {"nom": "Quatretondeta", "pop": 133, "lat": 38.7150, "lng": -0.3048, "comarca": "El Comtat"},
    {"nom": "Balones", "pop": 126, "lat": 38.7357, "lng": -0.3280, "comarca": "El Comtat"},
    {"nom": "Almudaina", "pop": 112, "lat": 38.7828, "lng": -0.3480, "comarca": "El Comtat"},
    {"nom": "Benillup", "pop": 108, "lat": 38.7555, "lng": -0.3530, "comarca": "El Comtat"},
    {"nom": "Benimassot", "pop": 93, "lat": 38.7377, "lng": -0.2982, "comarca": "El Comtat"},
    {"nom": "Fageca", "pop": 104, "lat": 38.7292, "lng": -0.2788, "comarca": "El Comtat"},
    {"nom": "Famorca", "pop": 48, "lat": 38.7260, "lng": -0.2597, "comarca": "El Comtat"},
    {"nom": "Tollos", "pop": 40, "lat": 38.7400, "lng": -0.2720, "comarca": "El Comtat"},
    
    # --- L'ALCOIÀ (HOYA DE ALCOY) ---
    {"nom": "Alcoy", "pop": 58960, "lat": 38.6985, "lng": -0.4737, "comarca": "L'Alcoià"},
    {"nom": "Ibi", "pop": 23677, "lat": 38.6268, "lng": -0.5737, "comarca": "L'Alcoià"},
    {"nom": "Castalla", "pop": 11097, "lat": 38.5961, "lng": -0.6710, "comarca": "L'Alcoià"},
    {"nom": "Onil", "pop": 7580, "lat": 38.6247, "lng": -0.6685, "comarca": "L'Alcoià"},
    {"nom": "Banyeres de Mariola", "pop": 7201, "lat": 38.7162, "lng": -0.6585, "comarca": "L'Alcoià"},
    {"nom": "Tibi", "pop": 1808, "lat": 38.5268, "lng": -0.5793, "comarca": "L'Alcoià"},
    {"nom": "Penàguila", "pop": 296, "lat": 38.6720, "lng": -0.3747, "comarca": "L'Alcoià"},
    {"nom": "Torremanzanas", "pop": 702, "lat": 38.6382, "lng": -0.4328, "comarca": "L'Alcoià"},
    {"nom": "Benifallim", "pop": 106, "lat": 38.6608, "lng": -0.4148, "comarca": "L'Alcoià"},
    
    # --- ALT VINALOPÓ ---
    {"nom": "Villena", "pop": 34106, "lat": 38.6362, "lng": -0.8662, "comarca": "Alt Vinalopó"},
    {"nom": "Biar", "pop": 3612, "lat": 38.6323, "lng": -0.7658, "comarca": "Alt Vinalopó"},
    {"nom": "Beneixama", "pop": 1705, "lat": 38.7048, "lng": -0.7397, "comarca": "Alt Vinalopó"},
    {"nom": "Cañada", "pop": 1191, "lat": 38.6897, "lng": -0.7630, "comarca": "Alt Vinalopó"},
    {"nom": "Campo de Mirra", "pop": 433, "lat": 38.7013, "lng": -0.7248, "comarca": "Alt Vinalopó"},
    {"nom": "Salinas", "pop": 1587, "lat": 38.5159, "lng": -0.8692, "comarca": "Alt Vinalopó"},
    
    # --- VINALOPÓ MITJÀ ---
    {"nom": "Elda", "pop": 52297, "lat": 38.4779, "lng": -0.7917, "comarca": "Vinalopó Mitjà"},
    {"nom": "Petrer", "pop": 35197, "lat": 38.4885, "lng": -0.7719, "comarca": "Vinalopó Mitjà"},
    {"nom": "Novelda", "pop": 25592, "lat": 38.3847, "lng": -0.7680, "comarca": "Vinalopó Mitjà"},
    {"nom": "Aspe", "pop": 21191, "lat": 38.3449, "lng": -0.7673, "comarca": "Vinalopó Mitjà"},
    {"nom": "Monóvar", "pop": 12387, "lat": 38.4374, "lng": -0.8417, "comarca": "Vinalopó Mitjà"},
    {"nom": "Monforte del Cid", "pop": 8619, "lat": 38.3800, "lng": -0.7267, "comarca": "Vinalopó Mitjà"},
    {"nom": "Sax", "pop": 10145, "lat": 38.5392, "lng": -0.8167, "comarca": "Vinalopó Mitjà"},
    {"nom": "Pinoso", "pop": 8174, "lat": 38.4011, "lng": -1.0401, "comarca": "Vinalopó Mitjà"},
    {"nom": "Hondón de las Nieves", "pop": 2684, "lat": 38.3116, "lng": -0.8716, "comarca": "Vinalopó Mitjà"},
    {"nom": "Algueña", "pop": 1351, "lat": 38.3729, "lng": -0.9352, "comarca": "Vinalopó Mitjà"},
    {"nom": "Hondón de los Frailes", "pop": 1261, "lat": 38.2901, "lng": -0.9074, "comarca": "Vinalopó Mitjà"},
    {"nom": "La Romana", "pop": 2545, "lat": 38.3637, "lng": -0.8923, "comarca": "Vinalopó Mitjà"},
    
    # --- BAIX VINALOPÓ ---
    {"nom": "Elche", "pop": 235580, "lat": 38.2699, "lng": -0.6986, "comarca": "Baix Vinalopó"},
    {"nom": "Crevillente", "pop": 29881, "lat": 38.2502, "lng": -0.8095, "comarca": "Baix Vinalopó"},
    {"nom": "Santa Pola", "pop": 34587, "lat": 38.1911, "lng": -0.5567, "comarca": "Baix Vinalopó"},
    
    # --- VEGA BAJA DEL SEGURA ---
    {"nom": "Orihuela", "pop": 80468, "lat": 38.0849, "lng": -0.9441, "comarca": "Vega Baja"},
    {"nom": "Torrevieja", "pop": 84838, "lat": 37.9774, "lng": -0.6823, "comarca": "Vega Baja"},
    {"nom": "Pilar de la Horadada", "pop": 25193, "lat": 37.8650, "lng": -0.7921, "comarca": "Vega Baja"},
    {"nom": "Almoradí", "pop": 21401, "lat": 38.1088, "lng": -0.7904, "comarca": "Vega Baja"},
    {"nom": "Callosa de Segura", "pop": 19315, "lat": 38.1243, "lng": -0.8782, "comarca": "Vega Baja"},
    {"nom": "Guardamar del Segura", "pop": 16138, "lat": 38.0894, "lng": -0.6557, "comarca": "Vega Baja"},
    {"nom": "Rojales", "pop": 14974, "lat": 38.0881, "lng": -0.7244, "comarca": "Vega Baja"},
    {"nom": "Albatera", "pop": 12864, "lat": 38.1774, "lng": -0.8659, "comarca": "Vega Baja"},
    {"nom": "Catral", "pop": 8976, "lat": 38.1596, "lng": -0.8019, "comarca": "Vega Baja"},
    {"nom": "Dolores", "pop": 7799, "lat": 38.1397, "lng": -0.7714, "comarca": "Vega Baja"},
    {"nom": "Cox", "pop": 7431, "lat": 38.1384, "lng": -0.8836, "comarca": "Vega Baja"},
    {"nom": "Bigastro", "pop": 7130, "lat": 38.0683, "lng": -0.8929, "comarca": "Vega Baja"},
    {"nom": "Redován", "pop": 8423, "lat": 38.1142, "lng": -0.9078, "comarca": "Vega Baja"},
    {"nom": "San Fulgencio", "pop": 6964, "lat": 38.1082, "lng": -0.6958, "comarca": "Vega Baja"},
    {"nom": "San Miguel de Salinas", "pop": 6555, "lat": 37.9822, "lng": -0.7877, "comarca": "Vega Baja"},
    {"nom": "Benejúzar", "pop": 5480, "lat": 38.0824, "lng": -0.8501, "comarca": "Vega Baja"},
    {"nom": "Los Montesinos", "pop": 5217, "lat": 37.9906, "lng": -0.7289, "comarca": "Vega Baja"},
    {"nom": "Formentera del Segura", "pop": 4446, "lat": 38.0945, "lng": -0.7437, "comarca": "Vega Baja"},
    {"nom": "Algorfa", "pop": 3513, "lat": 38.0533, "lng": -0.7648, "comarca": "Vega Baja"},
    {"nom": "Benijófar", "pop": 3427, "lat": 38.0762, "lng": -0.7294, "comarca": "Vega Baja"},
    {"nom": "Granja de Rocamora", "pop": 2626, "lat": 38.1523, "lng": -0.8589, "comarca": "Vega Baja"},
    {"nom": "Jacarilla", "pop": 2039, "lat": 38.0637, "lng": -0.8369, "comarca": "Vega Baja"},
    {"nom": "Benferri", "pop": 1955, "lat": 38.1425, "lng": -0.9463, "comarca": "Vega Baja"},
    {"nom": "Daya Nueva", "pop": 1758, "lat": 38.1107, "lng": -0.7580, "comarca": "Vega Baja"},
    {"nom": "San Isidro", "pop": 1912, "lat": 38.1863, "lng": -0.8170, "comarca": "Vega Baja"},
    {"nom": "Rafal", "pop": 4396, "lat": 38.1011, "lng": -0.8555, "comarca": "Vega Baja"},
    {"nom": "Daya Vieja", "pop": 683, "lat": 38.1200, "lng": -0.7426, "comarca": "Vega Baja"},
]

# ============================================================
# SSL config pour macOS
# ============================================================
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ============================================================
# FILTRAGE PAR POPULATION
# ============================================================

villes_filtrees = [v for v in MUNICIPIOS if v["pop"] >= POPULATION_MIN]
villes_exclues = len(MUNICIPIOS) - len(villes_filtrees)

# ============================================================
# FONCTIONS
# ============================================================

def search_places(metier, ville):
    """Recherche un métier dans une ville via Google Places API Legacy"""
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    params = {
        "query": f"{metier} en {ville['nom']} Alicante",
        "location": f"{ville['lat']},{ville['lng']}",
        "radius": 8000,
        "language": "es",
        "key": API_KEY
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            
        if data.get("status") != "OK":
            if data.get("status") == "ZERO_RESULTS":
                return []
            print(f"    ⚠️  API status: {data.get('status')}")
            return []
            
        return data.get("results", [])
    except Exception as e:
        print(f"    ❌ Erreur: {e}")
        return []


def get_place_details(place_id):
    """Récupère les détails d'un lieu"""
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,international_phone_number,website,url,rating,user_ratings_total,reviews,photos,opening_hours,types,business_status",
        "language": "es",
        "key": API_KEY
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        if data.get("status") == "OK":
            return data.get("result", {})
        return {}
    except Exception as e:
        print(f"    ❌ Erreur détails: {e}")
        return {}


# ============================================================
# RECHERCHE PRINCIPALE
# ============================================================

print("=" * 65)
print("🔍 PROSPECTION COMPLÈTE — Province d'Alicante")
print(f"   {len(MUNICIPIOS)} municipios au total (141)")
print(f"   {len(villes_filtrees)} municipios avec pop ≥ {POPULATION_MIN}")
print(f"   {villes_exclues} municipios exclus (trop petits)")
print(f"   {len(METIERS)} métiers × {len(villes_filtrees)} villes = {len(METIERS)*len(villes_filtrees)} recherches")
print(f"   Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 65)

all_prospects = []
seen_place_ids = set()
stats = {m: 0 for m in METIERS}
stats_villes = {}
stats_comarcas = {}

total_searches = len(METIERS) * len(villes_filtrees)
search_count = 0
api_calls = 0

for metier in METIERS:
    print(f"\n{'━' * 65}")
    print(f"🔧 MÉTIER : {metier.upper()}")
    print(f"{'━' * 65}")
    
    for ville in villes_filtrees:
        search_count += 1
        progress = f"[{search_count}/{total_searches}]"
        print(f"  {progress} {ville['nom']} ({ville['pop']:,} hab.)...", end=" ", flush=True)
        
        results = search_places(metier, ville)
        api_calls += 1
        
        new_prospects = 0
        for place in results:
            place_id = place.get("place_id")
            
            if place_id in seen_place_ids:
                continue
            seen_place_ids.add(place_id)
            
            details = get_place_details(place_id)
            api_calls += 1
            time.sleep(0.1)
            
            # SANS site web uniquement
            if details.get("website"):
                continue
            
            # Extraire les avis
            avis = []
            for r in details.get("reviews", [])[:5]:
                avis.append({
                    "auteur": r.get("author_name", "Anonyme"),
                    "note": r.get("rating", 0),
                    "texte": r.get("text", ""),
                    "date": r.get("relative_time_description", "")
                })
            
            # Photos URLs
            photos = []
            for photo in details.get("photos", [])[:5]:
                ref = photo.get("photo_reference", "")
                if ref:
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={ref}&key={API_KEY}"
                    photos.append(photo_url)
            
            # Horaires
            horaires = details.get("opening_hours", {}).get("weekday_text", [])
            
            prospect = {
                "metier": metier,
                "nom": details.get("name", place.get("name", "N/A")),
                "adresse": details.get("formatted_address", "N/A"),
                "ville_recherche": ville["nom"],
                "comarca": ville["comarca"],
                "telephone": details.get("formatted_phone_number", ""),
                "telephone_intl": details.get("international_phone_number", ""),
                "note": details.get("rating", 0),
                "nb_avis": details.get("user_ratings_total", 0),
                "google_maps": details.get("url", ""),
                "place_id": place_id,
                "nb_photos": len(photos),
                "photos_urls": photos,
                "avis": avis,
                "horaires": horaires,
                "latitude": place.get("geometry", {}).get("location", {}).get("lat", 0),
                "longitude": place.get("geometry", {}).get("location", {}).get("lng", 0)
            }
            
            all_prospects.append(prospect)
            new_prospects += 1
            stats[metier] += 1
            stats_villes[ville["nom"]] = stats_villes.get(ville["nom"], 0) + 1
            stats_comarcas[ville["comarca"]] = stats_comarcas.get(ville["comarca"], 0) + 1
        
        print(f"→ {len(results)} rés., {new_prospects} nouveaux prospects")
        time.sleep(0.3)

# ============================================================
# RÉSULTATS
# ============================================================

print(f"\n\n{'=' * 65}")
print(f"📊 RÉSULTATS FINAUX")
print(f"{'=' * 65}")
print(f"\n🎯 TOTAL PROSPECTS SANS SITE WEB : {len(all_prospects)}")
print(f"📡 Appels API effectués : {api_calls}")

print(f"\n📋 Par métier :")
for metier, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
    bar = "█" * min(count, 50)
    print(f"  {metier:<16} : {count:>4} {bar}")

print(f"\n🗺️  Par comarca :")
for comarca, count in sorted(stats_comarcas.items(), key=lambda x: x[1], reverse=True):
    bar = "█" * min(count, 50)
    print(f"  {comarca:<20} : {count:>4} {bar}")

print(f"\n🏘️  Top 15 villes :")
for ville, count in sorted(stats_villes.items(), key=lambda x: x[1], reverse=True)[:15]:
    bar = "█" * min(count, 50)
    print(f"  {ville:<25} : {count:>4} {bar}")

# ============================================================
# AFFICHAGE DÉTAILLÉ
# ============================================================

print(f"\n{'=' * 65}")
print(f"📋 LISTE COMPLÈTE DES PROSPECTS")
print(f"{'=' * 65}")

for metier in METIERS:
    prospects_metier = [p for p in all_prospects if p["metier"] == metier]
    if not prospects_metier:
        continue
    
    print(f"\n{'─' * 65}")
    print(f"  🔧 {metier.upper()} ({len(prospects_metier)} prospects)")
    print(f"{'─' * 65}")
    
    for i, p in enumerate(prospects_metier, 1):
        print(f"\n  #{i} {p['nom']}")
        print(f"     📍 {p['adresse']} ({p['comarca']})")
        print(f"     📞 {p['telephone'] or 'Non disponible'}")
        print(f"     ⭐ {p['note']}/5 ({p['nb_avis']} avis) | 📸 {p['nb_photos']} photos")
        print(f"     🔗 {p['google_maps']}")
        if p['avis']:
            best = max(p['avis'], key=lambda x: x['note'])
            texte = best['texte'][:100] + "..." if len(best['texte']) > 100 else best['texte']
            print(f"     💬 \"{texte}\" — {best['auteur']}")

# ============================================================
# SAUVEGARDE JSON
# ============================================================

output = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "province": "Alicante",
    "nb_municipios_total": len(MUNICIPIOS),
    "nb_municipios_cherches": len(villes_filtrees),
    "population_min": POPULATION_MIN,
    "nb_metiers": len(METIERS),
    "total_prospects": len(all_prospects),
    "api_calls": api_calls,
    "stats_metiers": stats,
    "stats_comarcas": stats_comarcas,
    "stats_villes": stats_villes,
    "prospects": all_prospects
}

json_file = "prospects_alicante_141_complet.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# ============================================================
# SAUVEGARDE CSV (pour Google Sheets / CRM)
# ============================================================

csv_file = "prospects_alicante_141_complet.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Métier", "Nom", "Adresse", "Ville Recherche", "Comarca",
        "Téléphone", "Tél International",
        "Note", "Nb Avis", "Nb Photos", "Google Maps", "Place ID",
        "Horaires", "Meilleur Avis", "Photo 1 URL", "Photo 2 URL"
    ])
    for p in all_prospects:
        best_avis = ""
        if p["avis"]:
            best = max(p["avis"], key=lambda x: x["note"])
            best_avis = f"{best['auteur']}: {best['texte'][:200]}"
        
        photo1 = p["photos_urls"][0] if len(p["photos_urls"]) > 0 else ""
        photo2 = p["photos_urls"][1] if len(p["photos_urls"]) > 1 else ""
        horaires = " | ".join(p["horaires"]) if p["horaires"] else ""
        
        writer.writerow([
            p["metier"], p["nom"], p["adresse"], p["ville_recherche"], p["comarca"],
            p["telephone"], p["telephone_intl"],
            p["note"], p["nb_avis"], p["nb_photos"],
            p["google_maps"], p["place_id"],
            horaires, best_avis, photo1, photo2
        ])

# ============================================================
# RÉSUMÉ EXÉCUTIF
# ============================================================

print(f"\n{'=' * 65}")
print(f"✅ PROSPECTION TERMINÉE !")
print(f"{'=' * 65}")
print(f"   🎯 {len(all_prospects)} prospects SANS site web trouvés")
print(f"   📡 {api_calls} appels API effectués")
print(f"   🏘️  {len(villes_filtrees)} villes cherchées (pop ≥ {POPULATION_MIN})")
print(f"   📄 {json_file}")
print(f"   📊 {csv_file}")
print(f"\n🚀 Prochaine étape : générer les URLs Lovable 'Déjà-Fait'")
print(f"   pour chaque prospect !")
print(f"{'=' * 65}")
