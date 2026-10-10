# -*- coding: utf-8 -*-
"""Page /diagnostico-automatizacion/ — deux correctifs.

  1. LOC ne déclarait pas le français : Intl.NumberFormat(LOC["fr"]) recevait
     undefined et retombait sur la locale du navigateur. Un visiteur français
     dont le navigateur est en anglais voyait « 1,200 € » au lieu de « 1 200 € »,
     sur un outil dont l'argument est précisément de chiffrer un coût annuel.

  2. La page n'avait aucune mesure d'audience : ni GA4 ni Clarity, alors que
     tout le reste du site en est équipé. Ajoutés à l'identique.

Les deux modifications sont consignées dans le commentaire d'en-tête (points 7
et 8), selon la convention déjà en place dans ce fichier : elles devront être
réappliquées si la page est régénérée un jour.

À lancer depuis ~/webautonomos. Sauvegarde : ~/diagnostico-index.html.bak-fix
"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from origine_lead import poser as poser_origine  # script d'origine des leads (origine-lead.js), ne pas retirer

CIBLE = os.path.join("diagnostico-automatizacion", "index.html")

# ─── 1) locale française ──────────────────────────────────────────────────────
ANCIEN_LOC = 'var LOC = { es:"es-ES", ca:"ca-ES", en:"en-GB" };'
NOUVEAU_LOC = 'var LOC = { es:"es-ES", ca:"ca-ES", en:"en-GB", fr:"fr-FR" };'

# ─── 2) mesure d'audience, identique au reste du site ─────────────────────────
ANCRE_HEAD = "</style>\n</head>"
SUIVI = """</style>

<!-- Google Analytics GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-MT6S7CH7N9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-MT6S7CH7N9');
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "wb9354sv4p");
</script>
</head>"""

# ─── 3) notes ajoutées au commentaire d'en-tête ───────────────────────────────
ANCRE_NOTE = ("  Vérifié : 0px de débordement de 1300 à 1600px, barre masquée à 1280px et en\n"
              "  dessous, aucun débordement horizontal de 375 à 1600px. JSON-LD valide, 7\n"
              "  questions identiques à la FAQ affichée en es, ca et en.\n-->")
NOUVELLE_NOTE = """  7. Locale française dans LOC :
       var LOC = { es:"es-ES", ca:"ca-ES", en:"en-GB", fr:"fr-FR" };
     La source omet fr. nfmt() appelle Intl.NumberFormat(LOC[lang]) : sans
     l'entrée, lang="fr" passe undefined et le formatage retombe SILENCIEUSEMENT
     sur la locale du navigateur du visiteur. Un francophone au navigateur
     anglais lit alors « 1,200 € » au lieu de « 1 200 € » — sur les montants
     du devis, c'est-à-dire l'argument central de la page.

  8. Mesure d'audience (GA4 G-MT6S7CH7N9 + Clarity wb9354sv4p), juste avant
     </head>, à l'identique du reste du site. La source régénérée n'en a aucune :
     la page est alors totalement absente des statistiques.

  Vérifié : 0px de débordement de 1300 à 1600px, barre masquée à 1280px et en
  dessous, aucun débordement horizontal de 375 à 1600px. JSON-LD valide, 7
  questions identiques à la FAQ affichée en es, ca et en.
-->"""

EDITS = [
    ("Locale française (fr-FR)",              ANCIEN_LOC, NOUVEAU_LOC,  1),
    ("Mesure d'audience GA4 + Clarity",       ANCRE_HEAD, SUIVI,        1),
    ("Notes 7 et 8 dans l'en-tête",           ANCRE_NOTE, NOUVELLE_NOTE, 1),
]

if not os.path.exists(CIBLE):
    sys.exit(f"ABANDON : fichier introuvable — {CIBLE}")
h = open(CIBLE, encoding="utf-8").read()

if 'fr:"fr-FR"' in h or "G-MT6S7CH7N9" in h:
    sys.exit("ABANDON : correctifs déjà appliqués. Rien modifié.")

errs = [f"    {h.count(o)}× (attendu {n}) : {d}" for d, o, nw, n in EDITS if h.count(o) != n]
if errs:
    print("ABANDON — ancres non conformes, aucun fichier écrit :")
    print("\n".join(errs)); sys.exit(1)

for d, o, nw, n in EDITS:
    h = h.replace(o, nw)
    print(f"  ✓ {d}")

shutil.copy(CIBLE, os.path.expanduser("~/diagnostico-index.html.bak-fix"))
open(CIBLE, "w", encoding="utf-8").write(poser_origine(h))
print("\nOK — locale française et mesure d'audience en place, consignées dans l'en-tête.")
print("Sauvegarde : ~/diagnostico-index.html.bak-fix")
