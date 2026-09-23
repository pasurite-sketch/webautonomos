# -*- coding: utf-8 -*-
"""Page /diagnostico-automatizacion/ : badge retiré, H1 et title sur le mot-clé.

  - le badge « Webs en castellano, valenciano, inglés y francés » disparaît
    (en FR il affichait encore « Plus de 40 indépendants… », retiré ailleurs) ;
  - le grand titre « Recupera entre 10 y 20 horas… » est remplacé, 4 langues :
      « Automatización de procesos para autónomos y pymes. »
    La promesse des 10 à 20 heures reste dans la ligne heroHonest, dessous ;
  - le <title>, og:title, twitter:title et le nom du WebPage (JSON-LD) sont
    alignés sur le H1, le nom du Service (JSON-LD) aussi ;
  - le tout est documenté en point 9 du commentaire « MODIFICATIONS LOCALES ».

À lancer depuis ~/webautonomos. (Remplace patch_diag_h1.py, jamais appliqué.)
Sauvegarde : ~/diagnostico-index.html.bak-h1
"""
import json, os, re, shutil, subprocess, sys, tempfile

PATH = "diagnostico-automatizacion/index.html"
s = open(PATH, encoding="utf-8").read()

if "Automatización de procesos para <em>" in s:
    sys.exit("ABANDON : nouveau H1 déjà présent. Rien modifié.")

H1 = {
    "es": "Automatización de procesos para <em>autónomos y pymes</em>.",
    "ca": "Automatització de processos per a <em>autònoms i pimes</em>.",
    "en": "Process automation for <em>freelancers and small businesses</em>.",
    "fr": "Automatisation des processus pour <em>indépendants et PME</em>.",
}
TITLE = "Automatización de procesos para autónomos: calcula si compensa"   # 62 car.
SOCIAL = "Automatización de procesos para autónomos y pymes: calcula si te compensa"
SERVICE = "Automatización de procesos para autónomos y pymes"

REMPLACEMENTS = [
    # 1) hero : badge supprimé, nouveau H1
    ("hero",
     '    <p class="pill"><span>★</span> <b data-t="social" style="font-weight:600">'
     'Webs en castellano, valenciano, inglés y francés</b></p>\n'
     '    <h1 data-t="h1">Recupera entre 10 y 20 horas al mes en <em>tareas repetitivas</em>.</h1>',
     '    <h1 data-t="h1">%s</h1>' % H1["es"]),

    # 2) le H1 un peu plus large : 3 lignes au lieu de 4 sur ordinateur
    ("CSS .hero h1",
     '.hero h1{color:#fff;max-width:15ch;margin:0 auto 20px}',
     '.hero h1{color:#fff;max-width:18ch;margin:0 auto 20px;text-wrap:balance}'),

    # 3) objet T : clé social supprimée, nouveau h1
    ("T.es",
     'social:"Webs en castellano, valenciano, inglés y francés",\n'
     ' h1:"Recupera entre 10 y 20 horas al mes en <em>tareas repetitivas</em>.",',
     'h1:"%s",' % H1["es"]),
    ("T.ca",
     'social:"Webs en castellà, valencià, anglés i francés",\n'
     ' h1:"Recupera entre 10 i 20 hores al mes en <em>tasques repetitives</em>.",',
     'h1:"%s",' % H1["ca"]),
    ("T.en",
     'social:"Websites in Spanish, Valencian, English and French",\n'
     ' h1:"Get back 10 to 20 hours a month from <em>repetitive tasks</em>.",',
     'h1:"%s",' % H1["en"]),
    ("T.fr",
     'social:"Plus de 40 indépendants nous font déjà confiance",'
     'h1:"Récupérez 10 à 20 heures par mois sur les <em>tâches répétitives</em>.",',
     'h1:"%s",' % H1["fr"]),

    # 4) title et partages sociaux
    ("<title>",
     '<title>Automatizar tareas repetitivas: calcula gratis si te compensa | WebAutonomos</title>',
     '<title>%s</title>' % TITLE),
    ("og:title",
     '<meta property="og:title" content="Recupera entre 10 y 20 horas al mes en tareas repetitivas.">',
     '<meta property="og:title" content="%s">' % SOCIAL),
    ("twitter:title",
     '<meta name="twitter:title" content="Recupera entre 10 y 20 horas al mes en tareas repetitivas.">',
     '<meta name="twitter:title" content="%s">' % SOCIAL),

    # 5) JSON-LD : WebPage = title, Service = libellé du H1
    ("JSON-LD WebPage",
     '"name":"Automatizar tareas administrativas: calcula gratis si te compensa"',
     '"name":"%s"' % TITLE),
    ("JSON-LD Service",
     '{"@type":"Service","name":"Automatización de tareas administrativas para pymes y autónomos",',
     '{"@type":"Service","name":"%s",' % SERVICE),

    # 6) documentation, point 9
    ("commentaire",
     '\n  Vérifié : 0px de débordement',
     '\n  9. Hero, title et libellés alignés sur le mot-clé (23/09/2026).\n'
     '       H1   : Automatización de procesos para <em>autónomos y pymes</em>.\n'
     '       title: ' + TITLE + '  (62 car., ~593 px)\n'
     '     - badge supprimé avec sa clé social, dans les 4 blocs de T (en fr elle\n'
     '       affichait encore « Plus de 40 indépendants… ») ;\n'
     '     - T.h1 traduit dans les 4 blocs ; .hero h1 passe de 15ch à 18ch pour\n'
     '       tenir en 3 lignes sur ordinateur, text-wrap:balance évite un mot\n'
     '       isolé sur la dernière ligne (fr, mobile) ;\n'
     '     - og:title / twitter:title, nom du WebPage (= title) et nom du Service\n'
     '       (= H1 sans balise) alignés dans le JSON-LD ;\n'
     '     - l\'ancienne accroche « Recupera entre 10 y 20 horas » a disparu du\n'
     '       titre ; la promesse reste dans heroHonest et la meta description.\n'
     '\n  Vérifié : 0px de débordement'),
]

for nom, old, new in REMPLACEMENTS:
    n = s.count(old)
    if n != 1:
        sys.exit(f"ABANDON : ancre « {nom} » trouvée {n}x (1 attendue). Rien modifié.")
for nom, old, new in REMPLACEMENTS:
    s = s.replace(old, new)

# ─── contrôles avant écriture ────────────────────────────────────────────────
erreurs = []
# Les comptages de balises ignorent les commentaires HTML : le commentaire
# MODIFICATIONS LOCALES cite des balises (<div class="nav-links">, <em> …).
visible = re.sub(r'<!--.*?-->', '', s, flags=re.S)
if len(re.findall(r'<h1\b', visible)) != 1:
    erreurs.append("il doit rester exactement un <h1>")
if 'social:"' in s or 'data-t="social"' in s:
    erreurs.append("clé social encore présente")
if "Recupera entre 10 y 20 horas al mes en <em>" in s:
    erreurs.append("ancien H1 encore présent")
for tag in ("div", "p", "h1", "header", "section", "em"):
    o = len(re.findall(r'<%s[\s>]' % tag, visible)); c = visible.count('</%s>' % tag)
    if o != c:
        erreurs.append(f"<{tag}> déséquilibré : {o} ouvertures, {c} fermetures")
for bloc in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
    try:
        json.loads(bloc)
    except ValueError as exc:
        erreurs.append(f"JSON-LD invalide : {exc}")
scripts = [m.group(2) for m in re.finditer(r'<script(\s[^>]*)?>(.*?)</script>', s, re.S)
           if 'ld+json' not in (m.group(1) or '') and m.group(2).strip()]
with tempfile.TemporaryDirectory() as tmp:
    for i, js in enumerate(scripts):
        f = os.path.join(tmp, f"s{i}.js")
        open(f, "w", encoding="utf-8").write(js)
        r = subprocess.run(["node", "--check", f], capture_output=True, text=True)
        if r.returncode:
            erreurs.append(f"script {i} : {r.stderr.strip()[:200]}")
if erreurs:
    sys.exit("ABANDON :\n  - " + "\n  - ".join(erreurs) + "\nRien modifié.")

shutil.copy(PATH, os.path.expanduser("~/diagnostico-index.html.bak-h1"))
open(PATH, "w", encoding="utf-8").write(s)
print("  ✓ badge retiré (clé social supprimée des 4 langues)")
print("  ✓ H1 : Automatización de procesos para autónomos y pymes (4 langues)")
print("  ✓ title : %s" % TITLE)
print("  ✓ og:title, twitter:title, JSON-LD WebPage et Service alignés")
print("  ✓ point 9 ajouté au commentaire MODIFICATIONS LOCALES")
print("  ✓ contrôles : 1 seul H1, balises équilibrées, JSON-LD et %d scripts valides" % len(scripts))
print("\nOK — sauvegarde : ~/diagnostico-index.html.bak-h1")
