# -*- coding: utf-8 -*-
"""Ajoute un nouvel article de blog (3 langues) à WebAutonomos.

Usage (depuis ~/webautonomos) :
    python3 add_article.py article_XX.json

Ce que fait le script :
  - lit le JSON de l'article (voir format en bas),
  - vérifie que la catégorie est connue du filtre du blog et traduite dans les 3 langues,
  - calcule le prochain id automatiquement,
  - insère l'entrée ES/VAL/EN dans les bons tableaux avec slugs localisés (es/, val/, en/),
  - complète parseArticleDate si un nom de mois (ex. Julio/Juliol) manque,
  - ajoute le bloc <url> hreflang (es/val/en) au sitemap.xml,
  - sauvegarde index.html + sitemap.xml HORS du dossier servi,
  - ne modifie rien si une vérification échoue.
Puis : npx wrangler deploy
"""
import json, re, sys, shutil, os

F, S = 'index.html', 'sitemap.xml'
path = sys.argv[1] if len(sys.argv) > 1 else 'new_article.json'
for f in (F, S, path):
    if not os.path.exists(f):
        print(f'ERREUR: {f} introuvable (lance depuis ~/webautonomos avec le JSON en argument).'); sys.exit(1)

art = json.load(open(path, encoding='utf-8'))
html = open(F, encoding='utf-8').read()
sm = open(S, encoding='utf-8').read()

# --- 0a) champs obligatoires : sans ce controle, un champ absent remonte en
# KeyError brut au milieu du script. Le message doit dire QUOI manque.
LANGUES = ('es', 'val', 'en', 'fr')
CHAMPS_LANGUE = ('date', 'title', 'seoTitle', 'metaDescription', 'keywords', 'excerpt', 'content', 'faq')
manquants = [c for c in ('slug', 'category', 'image', 'readTime') if c not in art]
for lg in LANGUES:
    if lg not in art:
        manquants.append(f'bloc "{lg}"')
    else:
        manquants += [f'{lg}.{c}' for c in CHAMPS_LANGUE if c not in art[lg]]
if manquants:
    print('ERREUR: champs absents du JSON : ' + ', '.join(manquants))
    print('        (le site est en 4 langues : es, val, en, fr sont tous requis). Abandon.')
    sys.exit(1)

# --- 0b) categorie : doit exister dans le filtre du blog ET dans les 3 blocs de
# libelles. Sans ce controle, une categorie inconnue passe sans erreur : l'article
# sort avec un badge VIDE (t.blog.categories[cat] vaut undefined) et n'apparait
# sous aucun bouton du filtre, seulement sous « Todos ».
CATEGORIES = ('web', 'seo', 'gmb', 'marketing', 'automatizacion', 'legal')
cat = art.get('category')
if cat not in CATEGORIES:
    print(f'ERREUR: category "{cat}" inconnue. Attendu : {", ".join(CATEGORIES)}. Abandon.'); sys.exit(1)
if f"'{cat}'" not in (re.search(r"const categories=\[([^\]]*)\]", html) or type('', (), {'group': lambda *a: ''})()).group(1):
    print(f'ERREUR: "{cat}" absente de const categories=[...] dans {F}. Abandon.'); sys.exit(1)
for bloc in re.findall(r'categories:\{seo:[^}]*\}', html):
    if f'{cat}:"' not in bloc:
        print(f'ERREUR: libelle manquant pour "{cat}" dans un des blocs de traduction. Abandon.'); sys.exit(1)

# --- table de référence des mois (ES + VAL + EN, complets et abrégés) ---
MONTHS = {
 'enero':0,'febrero':1,'marzo':2,'abril':3,'mayo':4,'junio':5,'julio':6,'agosto':7,'septiembre':8,'octubre':9,'noviembre':10,'diciembre':11,
 'ene':0,'feb':1,'mar':2,'abr':3,'may':4,'jun':5,'jul':6,'ago':7,'sep':8,'oct':9,'nov':10,'dic':11,
 'gener':0,'febrer':1,'març':2,'maig':4,'juny':5,'juliol':6,'agost':7,'setembre':8,'octubre':9,'novembre':10,'desembre':11,
 'gen':0,'set':8,'des':11,
 'janvier':0,'février':1,'mars':2,'avril':3,'mai':4,'juin':5,'juillet':6,'août':7,
 'septembre':8,'octobre':9,'novembre':10,'décembre':11,
 'jan':0,'apr':3,'aug':7,'dec':11,'january':0,'february':1,'march':2,'april':3,'june':5,'july':6,'august':7,'september':8,'october':9,'november':10,'december':11,
}

def bracket_match(s, start, op, cl):
    d = 0; i = start; q = False; e = False
    while i < len(s):
        c = s[i]
        if q:
            e = (c == '\\') if not e else False
            if c == '"' and not e: q = False
        else:
            if c == '"': q = True; e = False
            elif c == op: d += 1
            elif c == cl:
                d -= 1
                if d == 0: return s[start:i+1]
        i += 1
    return None

def js(v):
    if isinstance(v, bool): return 'true' if v else 'false'
    if isinstance(v, int): return str(v)
    if isinstance(v, str): return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'
    if isinstance(v, list): return '[' + ','.join(js(x) for x in v) + ']'
    if isinstance(v, dict): return '{' + ','.join(k + ':' + js(val) for k, val in v.items()) + '}'
    raise TypeError(type(v))

# --- 1) compléter parseArticleDate si des mois manquent ---
mobj = re.search(r"const months=\{([^}]*)\};", html)
if not mobj:
    print('ERREUR: parseArticleDate introuvable. Abandon.'); sys.exit(1)
existing = set(re.findall(r"'([^']+)':", mobj.group(1)))
needed = set()
for lg in ('es', 'val', 'en', 'fr'):
    for tok in art[lg]['date'].lower().replace(',', '').split():
        if not tok.isdigit(): needed.add(tok)
missing = [t for t in sorted(needed) if t not in existing]
unknown = [t for t in missing if t not in MONTHS]
if unknown:
    print(f'ERREUR: mois inconnus {unknown} (vérifie les dates du JSON). Abandon.'); sys.exit(1)
if missing:
    add = ''.join(f"'{t}':{MONTHS[t]}," for t in missing)
    html = html.replace(mobj.group(0), "const months={" + add + mobj.group(0)[len("const months={"):], 1)
    print(f'  parseArticleDate: mois ajoutés -> {missing}')

# --- 2) localiser les 3 tableaux + prochain id ---
# Reperage generique : 'articles:[' apparait exactement 4 fois (es/val/en/fr).
# On n'ancre PAS sur {id:1, : le tableau francais est vide avant insertion et
# commence par un autre id apres.
starts = [m.start() + len('articles:') for m in re.finditer(r'articles:\[', html)]
if len(starts) != 4:
    print(f'ERREUR: {len(starts)} tableaux articles trouvés (attendu 4 : es/val/en/fr). Abandon.'); sys.exit(1)
arrays = [bracket_match(html, s, '[', ']') for s in starts]

def lang_of(a):
    m = re.search(r'\{id:33,slug:"([a-z]+)/[^"]*",title:"([^"]+)"', a)
    if not m:
        # tableau sans article #33 : c'est le bloc francais, encore vide
        return 'fr'
    prefixe, t = m.group(1), m.group(2)
    if prefixe in ('es', 'val', 'en', 'fr'): return prefixe
    if t.startswith('Google Ads para'): return 'es'
    if t.startswith('Google Ads per a'): return 'val'
    if t.startswith('Google Ads for'): return 'en'
    return '?'
labels = [lang_of(a) for a in arrays]
if sorted(labels) != ['en', 'es', 'fr', 'val']:
    print(f'ERREUR: identification des tableaux ambiguë {labels}. Abandon.'); sys.exit(1)
nid = max(int(x) for a in arrays for x in re.findall(r'\{id:(\d+),', a)) + 1

# --- slug par langue, avec repli sur le slug racine ---
# art['slug'] reste obligatoire : c'est le slug par défaut ET celui de l'URL
# espagnole, qui sert de <loc> canonique au sitemap. Chaque bloc de langue peut
# le surcharger avec son propre "slug" ; les articles qui n'en déclarent pas se
# comportent exactement comme avant.
SLUGS = {lg: art[lg].get('slug', art['slug']) for lg in LANGUES}
if len(set(SLUGS.values())) > 1:
    print('  slugs par langue : ' + ', '.join(f'{lg}={SLUGS[lg]}' for lg in LANGUES))

# refuser un slug déjà présent, langue par langue
for lg in LANGUES:
    if re.search(r'slug:"%s/%s"' % (lg, re.escape(SLUGS[lg])), html):
        print(f'ERREUR: le slug "{SLUGS[lg]}" existe déjà en {lg}. Abandon.'); sys.exit(1)

def build_entry(lg):
    a = art[lg]
    return js({
        'id': nid, 'slug': f'{lg}/' + SLUGS[lg], 'title': a['title'], 'seoTitle': a['seoTitle'],
        'metaDescription': a['metaDescription'], 'keywords': a['keywords'], 'excerpt': a['excerpt'],
        'category': art['category'], 'date': a['date'], 'readTime': art['readTime'], 'image': art['image'],
        'content': a['content'], 'faq': a['faq'],
    })

new_html = html
for arr, lg in zip(arrays, labels):
    entry = build_entry(lg)
    if new_html.count('articles:' + arr) != 1:
        print(f'ERREUR: tableau {lg} non localisable de façon unique. Abandon.'); sys.exit(1)
    sep = ',' if len(arr) > 2 else ''      # '[]' -> pas de virgule en tete
    new_html = new_html.replace('articles:' + arr, 'articles:' + arr[:-1] + sep + entry + ']')

# --- 3) sitemap : bloc <url> hreflang avant </urlset> ---
sl = SLUGS['es']; lm = art.get('lastmod', '2026-07-20')
# Chaque alternative pointe vers le slug de SA langue : un hreflang qui pointe
# vers une URL inexistante est une erreur signalee par la Search Console.
block = (
 '    <url>\n'
 f'        <loc>https://webautonomos.es/blog/es/{SLUGS["es"]}</loc>\n'
 f'        <xhtml:link rel="alternate" hreflang="es" href="https://webautonomos.es/blog/es/{SLUGS["es"]}"/>\n'
 f'        <xhtml:link rel="alternate" hreflang="ca-ES" href="https://webautonomos.es/blog/val/{SLUGS["val"]}"/>\n'
 f'        <xhtml:link rel="alternate" hreflang="en" href="https://webautonomos.es/blog/en/{SLUGS["en"]}"/>\n'
 f'        <xhtml:link rel="alternate" hreflang="fr" href="https://webautonomos.es/blog/fr/{SLUGS["fr"]}"/>\n'
 f'        <xhtml:link rel="alternate" hreflang="x-default" href="https://webautonomos.es/blog/es/{SLUGS["es"]}"/>\n'
 f'        <lastmod>{lm}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority>\n'
 '    </url>\n')
if f'/blog/es/{sl}<' in sm:
    print('  sitemap: URL déjà présente, non ré-ajoutée.'); new_sm = sm
else:
    new_sm = sm.replace('</urlset>', block + '</urlset>', 1)

# --- 4) vérifications avant écriture ---
errs = []
if new_html.count('{') - new_html.count('}') != html.count('{') - html.count('}'): errs.append('déséquilibre {}')
if new_html.count('[') - new_html.count(']') != html.count('[') - html.count(']'): errs.append('déséquilibre []')
vstarts = [m.start() + len('articles:') for m in re.finditer(r'articles:\[', new_html)]
for s, lg in zip(vstarts, labels):
    a = bracket_match(new_html, s, '[', ']')
    ids = re.findall(r'\{id:(\d+),', a)
    if ids.count(str(nid)) != 1: errs.append(f'tableau {lg}: id {nid} absent/dupliqué')
    if not re.search(r'\{id:%d,slug:"%s/%s"' % (nid, lg, re.escape(SLUGS[lg])), a): errs.append(f'tableau {lg}: slug attendu absent')
if new_sm.count('</urlset>') != 1: errs.append('sitemap: </urlset> anormal')
if errs:
    print('Anomalies détectées, RIEN modifié :'); [print('  -', e) for e in errs]; sys.exit(1)

# validation JS optionnelle via node
try:
    import subprocess, tempfile
    entries = []
    for s, lg in zip(vstarts, labels):
        a = bracket_match(new_html, s, '[', ']')
        m = re.search(r'\{id:%d,slug:' % nid, a)
        entries.append(bracket_match(a, m.start(), '{', '}'))
    tf = tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8')
    tf.write('const E=%s;E.forEach(s=>{const e=eval("("+s+")");if(!e.id||!Array.isArray(e.content)||!Array.isArray(e.faq))throw"bad";});console.log("node OK");' % json.dumps(entries))
    tf.close()
    r = subprocess.run(['node', tf.name], capture_output=True, text=True, timeout=20)
    os.unlink(tf.name)
    print('  ' + (r.stdout.strip() or ('node: ' + r.stderr.strip()[:120])))
    if r.returncode != 0:
        print('Validation JS échouée, RIEN modifié.'); sys.exit(1)
except FileNotFoundError:
    print('  (node absent — validation structurelle Python seule, déjà passée)')

# --- 5) écriture + sauvegardes hors dossier servi ---
home = os.path.expanduser('~')
shutil.copy2(F, os.path.join(home, 'index.html.bak-addarticle'))
shutil.copy2(S, os.path.join(home, 'sitemap.xml.bak-addarticle'))
open(F, 'w', encoding='utf-8').write(new_html)
open(S, 'w', encoding='utf-8').write(new_sm)
print(f'\nArticle #{nid} "{sl}" ajouté (ES/VAL/EN/FR) + sitemap mis à jour.')
print(f'Sauvegardes: {home}/index.html.bak-addarticle , {home}/sitemap.xml.bak-addarticle')
print('Déploie :  npx wrangler deploy')

# ---------------------------------------------------------------------------
# Format JSON attendu :
# {
#   "slug":"web-para-xxx","category":"web","image":"🧭","readTime":11,"lastmod":"2026-07-20",
#   category ∈ web | seo | gmb | marketing | automatizacion | legal
#   Slug par langue (facultatif) : ajouter "slug" DANS un bloc de langue pour
#   qu'elle ait sa propre URL. Sans lui, la langue reprend le slug racine.
#     "slug":"cuanto-cuesta-papeleo-autonomo",
#     "fr":{ "slug":"paperasse-huit-heures-par-semaine", "date":"…", … }
#   Le slug racine reste obligatoire : il sert de <loc> canonique au sitemap.
#   (ajouter une catégorie = la déclarer AUSSI dans const categories=[...] et dans
#    les trois objets categories:{...} de index.html, sinon le script refuse)
#   "es":{"date":"20 Julio 2026","title":"...","seoTitle":"...","metaDescription":"...",
#         "keywords":["..."],"excerpt":"...",
#         "content":[{"type":"intro","text":"..."},{"type":"heading","text":"..."},
#                    {"type":"paragraph","text":"..."},{"type":"conclusion","text":"..."}],
#         "faq":[{"q":"...","a":"..."}]},
#   "val":{... "date":"20 Juliol 2026" ...},
#   "en":{... "date":"Jul 20, 2026" ...}
# }
