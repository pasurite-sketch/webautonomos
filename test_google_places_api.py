import json, urllib.request, urllib.parse, ssl

API_KEY = "AIzaSyDYOoF-ybVDXPXhmnOq1TChpFQkEgr9meo"

# Step 1: Text Search (ancienne API) pour trouver les electricistas
query = "electricista en Elche Alicante"
params = urllib.parse.urlencode({"query": query, "location": "38.2699,-0.6986", "radius": 10000, "language": "es", "key": API_KEY})
url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?{params}"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url)
result = json.loads(urllib.request.urlopen(req, context=ctx).read().decode("utf-8"))

if result.get("status") != "OK":
    print(f"Erreur API: {result.get('status')} - {result.get('error_message', 'N/A')}")
    exit(1)

places = result.get("results", [])
print(f"\n🔍 Recherche: \"{query}\"")
print(f"📊 {len(places)} résultats trouvés\n")

# Step 2: Place Details pour chaque résultat (téléphone, site web, avis)
prospects = []
for p in places:
    place_id = p["place_id"]
    detail_params = urllib.parse.urlencode({
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,international_phone_number,website,url,rating,user_ratings_total,photos,reviews,opening_hours,types",
        "language": "es",
        "key": API_KEY
    })
    detail_url = f"https://maps.googleapis.com/maps/api/place/details/json?{detail_params}"
    detail_req = urllib.request.Request(detail_url)
    detail = json.loads(urllib.request.urlopen(detail_req, context=ctx).read().decode("utf-8"))
    d = detail.get("result", {})

    if not d.get("website"):
        prospects.append(d)

print(f"🎯 {len(prospects)} PROSPECTS SANS SITE WEB sur {len(places)} trouvés\n")
print("=" * 70)

for i, p in enumerate(prospects, 1):
    print(f"\n#{i} {p.get('name', 'N/A')}")
    print(f"  📍 {p.get('formatted_address', 'N/A')}")
    print(f"  📞 {p.get('formatted_phone_number', 'N/A')}")
    print(f"  ⭐ {p.get('rating', 0)}/5 ({p.get('user_ratings_total', 0)} avis) | 📸 {len(p.get('photos', []))} photos")
    print(f"  🔗 {p.get('url', '')}")
    for r in p.get("reviews", [])[:2]:
        author = r.get("author_name", "Anonyme")
        text = r.get("text", "")[:120]
        stars = "⭐" * r.get("rating", 0)
        print(f"  💬 {stars} {author}: \"{text}\"")
    print()
