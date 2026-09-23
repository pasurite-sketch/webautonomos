# -*- coding: utf-8 -*-
"""CTA par categorie dans le generateur des articles statiques.

Les articles de la categorie « automatizacion » renvoyaient vers la demande de
demo de site web (/pide-tu-demo), alors que le SPA les envoie deja vers le
diagnostic (CTA_PAR_CATEGORIE dans index.html). Resultat constate dans la
Search Console le 23/09/2026 : /diagnostico-automatizacion/ ne recevait aucun
lien interne depuis le blog et n'avait aucune impression.

Ce patch ajoute un dictionnaire CTA_CATEGORIE au generateur : titre, texte,
bouton et lien du bloc CTA pour la categorie automatizacion, dans les quatre
langues, avec le bon parametre ?lang= pour que le diagnostic s'ouvre dans la
langue du lecteur. Les autres categories ne changent pas.

A lancer depuis ~/webautonomos.
Sauvegarde : ~/generate_spa_articles.py.bak-cta
"""
import os, shutil, subprocess, sys

PATH = "_tools/generate_spa_articles.py"
s = open(PATH, encoding="utf-8").read()

if "CTA_CATEGORIE" in s:
    sys.exit("ABANDON : CTA_CATEGORIE deja present. Rien modifie.")

# ─── 1) le dictionnaire, insere juste avant la table des mois ────────────────
ANCRE_1 = "# Tous les libelles de mois rencontres dans les 4 blocs de langue.\n"
BLOC = '''# CTA par categorie (23/09/2026). Remplace les cles cta_* de UI pour les
# articles de la categorie indiquee. Meme logique que CTA_PAR_CATEGORIE dans le
# SPA (index.html), mais avec le parametre ?lang= : le diagnostic lit la langue
# dans l'URL (es par defaut, puis ca / en / fr), le lecteur arrive donc dans sa
# langue. Avant ce correctif, les 40 articles d'automatisation renvoyaient vers
# /pide-tu-demo et /diagnostico-automatizacion/ n'avait aucun lien interne.
CTA_CATEGORIE = {
    'automatizacion': {
        'es': dict(cta_title='¿Cuánto te cuestan tus tareas repetitivas?',
                   cta_text='Diagnóstico gratuito: 4 preguntas, unos 2 minutos · '
                            'Precio cerrado · Presupuesto en menos de 48 horas',
                   cta_btn='Calcular lo que me cuesta →',
                   cta_href='/diagnostico-automatizacion/'),
        'val': dict(cta_title='Quant et costen les teues tasques repetitives?',
                    cta_text='Diagnòstic gratuït: 4 preguntes, uns 2 minuts · '
                             'Preu tancat · Pressupost en menys de 48 hores',
                    cta_btn='Calcular el que em costa →',
                    cta_href='/diagnostico-automatizacion/?lang=ca'),
        'en': dict(cta_title='What are your repetitive tasks costing you?',
                   cta_text='Free diagnostic: 4 questions, about 2 minutes · '
                            'Fixed price · Quote within 48 hours',
                   cta_btn='Calculate what it costs me →',
                   cta_href='/diagnostico-automatizacion/?lang=en'),
        'fr': dict(cta_title='Combien vous coûtent vos tâches répétitives ?',
                   cta_text='Diagnostic gratuit : 4 questions, environ 2 minutes · '
                            'Prix ferme · Devis en moins de 48 heures',
                   cta_btn='Calculer ce que ça me coûte →',
                   cta_href='/diagnostico-automatizacion/?lang=fr'),
    },
}

'''

# ─── 2) l'application dans render() ──────────────────────────────────────────
ANCRE_2 = ("    ui = UI[lang]\n"
           "    cat_slug, cat_color, cat_labels = CATEGORIES.get(")
NOUVEAU_2 = ("    ui = UI[lang]\n"
             "    # CTA propre a la categorie, s'il existe (voir CTA_CATEGORIE).\n"
             "    ui = dict(ui, **CTA_CATEGORIE.get(article.get('category'), {}).get(lang, {}))\n"
             "    cat_slug, cat_color, cat_labels = CATEGORIES.get(")

for nom, ancre in (("table des mois", ANCRE_1), ("render()", ANCRE_2)):
    n = s.count(ancre)
    if n != 1:
        sys.exit(f"ABANDON : ancre « {nom} » trouvee {n}x (1 attendue). Rien modifie.")

s = s.replace(ANCRE_1, BLOC + ANCRE_1)
s = s.replace(ANCRE_2, NOUVEAU_2)

# ─── 3) controle de syntaxe avant ecriture ───────────────────────────────────
try:
    compile(s, PATH, "exec")
except SyntaxError as exc:
    sys.exit(f"ABANDON : le resultat ne compile pas ({exc}). Rien modifie.")

shutil.copy(PATH, os.path.expanduser("~/generate_spa_articles.py.bak-cta"))
open(PATH, "w", encoding="utf-8").write(s)
print("  ✓ CTA_CATEGORIE ajoute (automatizacion, 4 langues)")
print("  ✓ render() applique le CTA de la categorie")
print("\nOK — generateur corrige. Sauvegarde : ~/generate_spa_articles.py.bak-cta")
