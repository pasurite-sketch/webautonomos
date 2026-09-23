# -*- coding: utf-8 -*-
"""Plan SEO FR-EN, phase 1 — les articles FR et EN du blog renvoient vers
l'accueil de leur langue (/fr/, /en/) au lieu de l'accueil espagnol.

Deux parties :

A. _tools/generate_spa_articles.py (articles issus des données du SPA :
   10 en français, 56 en anglais)
   - option --lang : ne régénérer qu'une ou plusieurs langues. Indispensable
     ici : un --force sans filtre réécrirait aussi les articles espagnols,
     dont 5 ont été retouchés à la main le 14/09 (commit 61b0d6d) ;
   - adresses par langue : logo, fil d'Ariane, BreadcrumbList (JSON-LD),
     lien « Blog », « Retour au blog », logo et « Contact » du pied de page.
       fr : /fr/   /blog/#fr   contact -> formulaire de /demandez-votre-demo
       en : /en/   /blog/#en   contact -> /en/contact
     es et val : inchangés, octet pour octet.

B. Les 44 articles français produits par l'ancien gabarit (absents des
   données du SPA, donc jamais régénérés) : correction directe.
     logo, « Accueil », fil d'Ariane, JSON-LD  -> /fr/
     « Voir mon site gratuit » (/pide-tu-demo)  -> /demandez-votre-demo
     menu Services (/#servicios)                -> /fr/prestations
     menu Tarifs (/#precios)                    -> /fr/tarifs
     Contact (/#contacto et /contacto)          -> formulaire de /demandez-votre-demo
     Blog (/blog)                               -> /blog/#fr
     drapeaux de langue (…/slug.html)           -> …/slug (sans redirection 307)

Sauvegarde : ~/webautonomos-work/backups/blog_home_links_<date>/
Abandon total, rien d'écrit, si une vérification échoue.

À lancer depuis ~/webautonomos, puis :
    python3 _tools/generate_spa_articles.py --force --lang fr --lang en
"""
import datetime
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
GEN = '_tools/generate_spa_articles.py'


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


# ─── A. générateur ───────────────────────────────────────────────────────────
GEN_REMPL = [
    # table des adresses par langue, juste avant les libellés d'interface
    ("# Libelles d'interface\nUI = {",
     "# Adresses de navigation par langue (23/09/2026, plan SEO FR-EN) : les\n"
     "# articles FR et EN renvoient vers l'accueil de leur langue. es et val\n"
     "# gardent exactement les adresses d'avant.\n"
     "NAV_URLS = {\n"
     "    'es':  dict(home=BASE, blog=BASE + '/blog/', contact=BASE + '/contacto'),\n"
     "    'val': dict(home=BASE, blog=BASE + '/blog/', contact=BASE + '/contacto'),\n"
     "    'en':  dict(home=BASE + '/en/', blog=BASE + '/blog/#en', contact=BASE + '/en/contact'),\n"
     "    'fr':  dict(home=BASE + '/fr/', blog=BASE + '/blog/#fr',\n"
     "                contact=BASE + '/demandez-votre-demo#pide-demo'),\n"
     "}\n\n"
     "# Libelles d'interface\nUI = {"),
    # NAV
    ('            <a href="{base}" style="display:flex; align-items:center; gap:8px; text-decoration:none;">',
     '            <a href="{home_url}" style="display:flex; align-items:center; gap:8px; text-decoration:none;">'),
    ('            <a href="{base}/blog/" style="color:#374151; text-decoration:none; font-size:14px; font-weight:500;">{blog}</a>',
     '            <a href="{blog_url}" style="color:#374151; text-decoration:none; font-size:14px; font-weight:500;">{blog}</a>'),
    # FOOTER
    ('        <a href="{base}" style="font-weight:800; font-size:1rem; color:rgba(255,255,255,0.85); text-decoration:none;">&#127760; webautonomos.es</a>',
     '        <a href="{home_url}" style="font-weight:800; font-size:1rem; color:rgba(255,255,255,0.85); text-decoration:none;">&#127760; webautonomos.es</a>'),
    ('            <a href="{base}/contacto" style="color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem;">{contact}</a>',
     '            <a href="{contact_url}" style="color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem;">{contact}</a>'),
    # fil d'Ariane et retour au blog
    ('            <a href="{base}" class="hover:text-purple-600 transition">{home}</a>',
     '            <a href="{home_url}" class="hover:text-purple-600 transition">{home}</a>'),
    ('            <a href="{base}/blog/" class="hover:text-purple-600 transition">{blog}</a>',
     '            <a href="{blog_url}" class="hover:text-purple-600 transition">{blog}</a>'),
    ('            <a href="{base}/blog/" style="color:#2563eb; text-decoration:none; font-weight:500;">{back}</a>',
     '            <a href="{blog_url}" style="color:#2563eb; text-decoration:none; font-weight:500;">{back}</a>'),
    # JSON-LD BreadcrumbList
    ('''            {"@type": "ListItem", "position": 1, "name": ui['home'], "item": BASE},''',
     '''            {"@type": "ListItem", "position": 1, "name": ui['home'], "item": NAV_URLS[lang]['home']},'''),
    # format()
    ("        nav=NAV.format(base=BASE, blog=E(ui['blog'])),",
     "        nav=NAV.format(base=BASE, blog=E(ui['blog']), home_url=NAV_URLS[lang]['home'],\n"
     "                       blog_url=NAV_URLS[lang]['blog']),\n"
     "        home_url=NAV_URLS[lang]['home'], blog_url=NAV_URLS[lang]['blog'],"),
    ("        footer=FOOTER.format(base=BASE, legal=E(ui['legal']),",
     "        footer=FOOTER.format(base=BASE, legal=E(ui['legal']),\n"
     "                             home_url=NAV_URLS[lang]['home'],\n"
     "                             contact_url=NAV_URLS[lang]['contact'],"),
    # option --lang
    ("    args = ap.parse_args()\n\n    translations = load_translations()",
     "    ap.add_argument('--lang', action='append', choices=['es', 'val', 'en', 'fr'],\n"
     "                    help='limite l ecriture aux articles de cette langue (repetable). '\n"
     "                         'Ex : --force --lang fr --lang en regenere le francais et '\n"
     "                         'l anglais sans toucher aux articles espagnols retouches a la main.')\n"
     "    args = ap.parse_args()\n\n    translations = load_translations()"),
    ("        if wanted and slug not in wanted:\n            continue\n",
     "        if wanted and slug not in wanted:\n            continue\n"
     "        if args.lang and lang not in args.lang:\n            continue\n"),
]

# ─── B. articles FR de l'ancien gabarit ─────────────────────────────────────
DEMO_FR = BASE + '/demandez-votre-demo'
ANCIEN_REMPL = [
    ('href="%s"' % BASE, 'href="%s/fr/"' % BASE),
    ('href="%s/pide-tu-demo"' % BASE, 'href="%s"' % DEMO_FR),
    ('href="%s/#servicios"' % BASE, 'href="%s/fr/prestations"' % BASE),
    ('href="%s/#precios"' % BASE, 'href="%s/fr/tarifs"' % BASE),
    ('href="%s/#contacto"' % BASE, 'href="%s#pide-demo"' % DEMO_FR),
    ('href="%s/contacto"' % BASE, 'href="%s#pide-demo"' % DEMO_FR),
    ('href="%s/blog"' % BASE, 'href="%s/blog/#fr"' % BASE),
]


def corriger_ancien(s):
    n = 0
    # seulement dans les balises <a> : les <link> (canonical, hreflang) ne bougent pas
    def balise(m):
        nonlocal n
        t = m.group(0)
        for a, b in ANCIEN_REMPL:
            if a in t:
                t = t.replace(a, b)
                n += 1
        t2, k = re.subn(r'(href="%s/blog/(?:es|val|en|fr)/[^"]+?)\.html"' % re.escape(BASE), r'\1"', t)
        n += k
        return t2
    s = re.sub(r'<a\b[^>]*>', balise, s)
    # JSON-LD BreadcrumbList : 1er élément
    s, k = re.subn(r'("item":\s*)"%s"' % re.escape(BASE), r'\1"%s/fr/"' % BASE, s)
    return s, n + k


def main():
    os.chdir(ROOT)
    gen = open(GEN, encoding='utf-8').read()
    if 'NAV_URLS' in gen:
        abandon('générateur déjà modifié (NAV_URLS présent).')
    for a, _ in GEN_REMPL:
        if gen.count(a) != 1:
            abandon('ancre du générateur trouvée %dx : %s' % (gen.count(a), a.strip()[:70]))
    for a, b in GEN_REMPL:
        gen = gen.replace(a, b)
    if '{base}"' in gen.split('def render')[0] or 'href="{base}"' in gen:
        abandon('un lien {base} vers l\'accueil subsiste dans le générateur.')
    try:
        compile(gen, GEN, 'exec')
    except SyntaxError as exc:
        abandon('générateur invalide après modification : %s' % exc)

    # articles FR absents des données du SPA (deux variantes de l'ancien
    # gabarit coexistent : on les identifie par les données, pas par leur HTML)
    sys.path.insert(0, os.path.join(ROOT, '_tools'))
    import generate_spa_articles as g
    tr = g.load_translations()
    spa = {a['slug'] for l in tr for a in (tr[l].get('blog') or {}).get('articles') or []}
    anciens = {}
    for f in sorted(os.listdir('blog/fr')):
        if not f.endswith('.html') or 'fr/' + f[:-5] in spa:
            continue
        rel = 'blog/fr/' + f
        s2, n = corriger_ancien(open(rel, encoding='utf-8').read())
        anciens[rel] = (s2, n)
    if len(anciens) != 44:
        abandon('%d articles FR à l\'ancien gabarit trouvés (44 attendus).' % len(anciens))
    err = []
    for rel, (s, n) in anciens.items():
        liens = ' '.join(re.findall(r'<a\b[^>]*>', s))
        for motif in ('href="%s"' % BASE, '/pide-tu-demo"', '/#servicios"', '/#precios"',
                      '/#contacto"', 'webautonomos.es/contacto"', 'webautonomos.es/blog"'):
            if motif in liens:
                err.append('%s : %s subsiste' % (rel, motif))
        if re.search(r'"item":\s*"%s"' % re.escape(BASE), s):
            err.append('%s : JSON-LD vers l\'accueil espagnol' % rel)
        if s.count('<a ') != open(rel, encoding='utf-8').read().count('<a '):
            err.append('%s : nombre de liens modifié' % rel)
    if err:
        abandon('vérifications :\n  - ' + '\n  - '.join(err[:15]))

    # sauvegarde puis écriture
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = os.path.expanduser('~/webautonomos-work/backups/blog_home_links_%s' % stamp)
    for rel in [GEN] + list(anciens):
        d = os.path.join(bak, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(rel, d)
    open(GEN, 'w', encoding='utf-8').write(gen)
    total = 0
    for rel, (s, n) in anciens.items():
        open(rel, 'w', encoding='utf-8').write(s)
        total += n
    print('  ✓ generate_spa_articles.py : adresses par langue + option --lang')
    print('  ✓ %d articles FR à l\'ancien gabarit corrigés (%d liens)' % (len(anciens), total))
    print('\nOK — sauvegarde : %s' % bak.replace(os.path.expanduser('~'), '~'))
    print('Étape suivante : python3 _tools/generate_spa_articles.py --force --lang fr --lang en')


if __name__ == '__main__':
    main()
