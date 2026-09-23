# -*- coding: utf-8 -*-
"""Plan SEO FR-EN, phase 1 — pages commerciales rangées sous /fr/ et /en/.

Ce script fait, en une seule passe vérifiée :

  1. Déplacement (8 pages) :
       /prestations /tarifs /questions            -> /fr/…
       /services /pricing /faq /how /contact      -> /en/…
     fichiers : X.html -> fr/X.html ou en/X.html (servis sous /fr/X, /en/X).
  2. Réécriture de tous les liens vers ces adresses, dans tout le site (href,
     content, hreflang, JSON-LD). Les pages espagnoles (precios, servicios,
     preguntas, como-funciona, contacto) déclarent donc les nouvelles adresses.
  3. Liens « Accueil » des pages FR/EN (pages déplacées, pages de démo, merci,
     thank-you) vers /fr/ et /en/ au lieu de l'accueil espagnol. Les pages EN
     cessent aussi d'envoyer vers /pide-tu-demo, /contacto et les ancres du SPA
     espagnol.
  4. Pages de démo /demandez-votre-demo et /get-your-demo : suppression du
     2e canonical hérité de la source espagnole (il pointait vers
     /pide-tu-demo et contredisait le premier) ; og:url, og:title,
     og:description dans la langue de la page.
  5. Avis sur les 3 pages de démo (ES, FR, EN) : 4,2 -> 4,3 et 6 -> 8 avis,
     cartes d'Inés et de Sabine O. ajoutées au carrousel.
  6. _redirects : 301 des 8 anciennes adresses (avec et sans barre finale).
  7. generate_sitemap.py : prend en compte fr/*.html et en/*.html.
  8. build_demo_pages.py : avertissement « ne pas relancer » (il ne reproduit
     plus les pages de démo en ligne : il réécrirait des textes espagnols dans
     les pages FR/EN et effacerait ces corrections).

Sauvegarde de chaque fichier modifié ou déplacé dans
~/webautonomos-work/backups/migrate_fr_en_<date>/ avant toute écriture.
Abandon total, rien d'écrit, si une seule vérification échoue.

À lancer depuis ~/webautonomos :   python3 _tools/migrate_fr_en_pages.py
Ensuite : python3 _tools/build_lang_homes.py  puis  python3 _tools/generate_sitemap.py
"""
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'

MOVES = [('prestations', 'fr'), ('tarifs', 'fr'), ('questions', 'fr'),
         ('services', 'en'), ('pricing', 'en'), ('faq', 'en'), ('how', 'en'), ('contact', 'en')]
NEW = {'/' + n: '/%s/%s' % (l, n) for n, l in MOVES}

# Pages dont les liens « Accueil » doivent viser l'accueil de leur langue
PAGES_FR = ['fr/prestations.html', 'fr/tarifs.html', 'fr/questions.html',
            'demandez-votre-demo.html', 'merci/index.html']
PAGES_EN = ['en/services.html', 'en/pricing.html', 'en/faq.html', 'en/how.html',
            'en/contact.html', 'get-your-demo.html', 'thank-you/index.html']

# Pages EN : liens qui envoyaient vers des pages espagnoles
EN_LOCAL = [
    ('/pide-tu-demo', '/get-your-demo'),
    ('/contacto', '/en/contact'),
    ('/#precios', '/en/#pricing'),
    ('/#servicios', '/en/#included'),
    ('/#como-funciona', '/en/#steps'),
    ('/#faq', '/en/#faq'),
]

# Groupes hreflang à contrôler après coup
GROUPES = [
    ['precios.html', 'fr/tarifs.html', 'en/pricing.html'],
    ['servicios.html', 'fr/prestations.html', 'en/services.html'],
    ['preguntas.html', 'fr/questions.html', 'en/faq.html'],
    ['como-funciona.html', 'en/how.html'],
    ['contacto.html', 'en/contact.html'],
]

# ─── avis ajoutés aux carrousels des pages de démo ──────────────────────────
AVIS = {
    'pide-tu-demo.html': dict(
        score=('4,2', '4,3'),
        count=('Valoración media basada en 6 opiniones verificadas en Trustpilot',
               'Valoración media basada en 8 opiniones verificadas en Trustpilot'),
        dot='Opinión',
        cartes=[("Muy buena experiencia con Webautonomos. Angelino hizo mi web teniendo en cuenta mis peticiones y observaciones. Sus consejos, su paciencia y su disponibilidad me han sido de gran ayuda.",
                 "Sabine O. — Terapeuta de bienestar", "traducido del francés"),
                ("Rápidos y eficaces, me gustó mucho cómo quedó la web, muchas gracias.",
                 "Inés — Crecimiento personal", "")]),
    'demandez-votre-demo.html': dict(
        score=('4,2', '4,3'),
        count=('Note moyenne sur 6 avis vérifiés Trustpilot',
               'Note moyenne sur 8 avis vérifiés Trustpilot'),
        dot='Avis',
        cartes=[("Très bonne expérience avec Webautonomos. Angelino a réalisé mon site en tenant compte de mes demandes et observations. Ses conseils, sa patience et sa disponibilité m'ont été d'un grand soutien.",
                 "Sabine O. — Praticienne bien-être", ""),
                ("Rapides et efficaces, j'ai beaucoup aimé le rendu du site, merci beaucoup.",
                 "Inés — Croissance personnelle", "traduit de l'espagnol")]),
    'get-your-demo.html': dict(
        score=('4,2', '4.3'),
        count=('Average rating from 6 verified Trustpilot reviews',
               'Average rating from 8 verified Trustpilot reviews'),
        dot='Review',
        cartes=[("A very good experience with Webautonomos. Angelino built my website taking my requests and comments into account. His advice, his patience and his availability were a great support.",
                 "Sabine O. — Wellbeing practitioner", "translated from French"),
                ("Fast and efficient, I really liked how the website turned out, thank you very much.",
                 "Inés — Personal growth", "translated from Spanish")]),
}

# ─── bloc Open Graph hérité de la source espagnole (pages de démo FR/EN) ────
OG_ANCIEN = """<!-- Canonical -->
<link rel="canonical" href="https://webautonomos.es/pide-tu-demo">
<!-- Open Graph / WhatsApp preview -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://webautonomos.es/pide-tu-demo">
<meta property="og:title" content="Tu Web Profesional Solo 15€/mes — Demo Gratis en 24h">
<meta property="og:description" content="Página web profesional para autónomos por solo 15€/mes. Demo personalizada en 24h. Sin alta, sin permanencia.">"""
OG_NOUVEAU = {
    'demandez-votre-demo.html': """<!-- Open Graph / WhatsApp preview (le canonical est en tête de page) -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://webautonomos.es/demandez-votre-demo">
<meta property="og:title" content="Votre site professionnel pour 15 €/mois — Démo gratuite en 24 h">
<meta property="og:description" content="Site web professionnel pour indépendants à 15 €/mois. Démo personnalisée en 24 h. Sans frais d'installation, sans engagement.">
<meta property="og:locale" content="fr_FR">""",
    'get-your-demo.html': """<!-- Open Graph / WhatsApp preview (canonical is at the top of the page) -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://webautonomos.es/get-your-demo">
<meta property="og:title" content="Your professional website for €15/month — Free demo in 24h">
<meta property="og:description" content="A professional website for the self-employed from €15/month. Personalised demo in 24 hours. No setup fee, no commitment.">
<meta property="og:locale" content="en_GB">""",
}

REDIRECTS = """
# Pages commerciales FR/EN rangees sous /fr/ et /en/ (23/09/2026, plan SEO FR-EN).
# Les fichiers ont ete deplaces dans le meme commit (migrate_fr_en_pages.py).
""" + ''.join('/%s   %s   301\n/%s/  %s   301\n' % (n, NEW['/' + n], n, NEW['/' + n])
              for n, _ in MOVES)

LLMS_AJOUT = """
## English — for English-speaking businesses in Spain
- [Home (English)](https://webautonomos.es/en/)
- [Pricing](https://webautonomos.es/en/pricing)
- [What's included](https://webautonomos.es/en/services)
- [How it works](https://webautonomos.es/en/how)
- [FAQ](https://webautonomos.es/en/faq)
- [Get a free demo](https://webautonomos.es/get-your-demo)

## Français — indépendants en France et en Espagne
- [Accueil (français)](https://webautonomos.es/fr/)
- [Tarifs](https://webautonomos.es/fr/tarifs)
- [Prestations](https://webautonomos.es/fr/prestations)
- [Questions fréquentes](https://webautonomos.es/fr/questions)
- [Demander une démo gratuite](https://webautonomos.es/demandez-votre-demo)
"""
LLMS_ANCRE = "\n## Webs por sector\n"

SITEMAP_ANCRE = "    return [v for _, v in sorted(list(roots.items()) + list(dirs.items()))]\n"
SITEMAP_NOUVEAU = """    # Pages commerciales FR/EN rangees sous /fr/ et /en/ (23/09/2026) :
    # fr/tarifs.html est servi sous /fr/tarifs. fr/index.html et en/index.html
    # sont deja couverts par la boucle des dossiers ci-dessus.
    subs = {}
    for lang in ('fr', 'en'):
        for path in sorted(glob.glob(os.path.join(ROOT, lang, '*.html'))):
            name = os.path.basename(path)
            if name == 'index.html':
                continue
            subs['%s/%s' % (lang, name[:-5])] = ('/%s/%s' % (lang, name[:-5]), path)

    return [v for _, v in sorted(list(roots.items()) + list(dirs.items())
                                 + list(subs.items()))]
"""

DEMO_ANCRE = '"""Génère les versions FRANÇAISE et ANGLAISE des pages de conversion,'
DEMO_AVERT = '''"""⚠ PÉRIMÉ — NE PAS RELANCER (constat du 23/09/2026).
Les pages en ligne ont reçu des corrections après la dernière génération
(hreflang EN, avis, canonical, Open Graph, liens vers /fr/ et /en/). Relancé,
ce script les effacerait et injecterait des textes espagnols dans les pages FR
et EN (mention TVA). Corriger désormais demandez-votre-demo.html et
get-your-demo.html directement.

Génère les versions FRANÇAISE et ANGLAISE des pages de conversion,'''


def lire(rel):
    return open(os.path.join(ROOT, rel), encoding='utf-8').read()


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


def pages_html():
    """Tous les .html publiés (hors dépôts techniques)."""
    exclus = ('.git', 'node_modules', '_tools', '.wrangler', 'scripts', '.github')
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in exclus]
        for f in fn:
            if f.endswith('.html'):
                out.append(os.path.relpath(os.path.join(dp, f), ROOT))
    return sorted(out)


LIEN_RE = re.compile(r'(?P<pre>(?:href|content)="|"(?=https://webautonomos\.es/))'
                     r'(?P<dom>https://webautonomos\.es)?'
                     r'(?P<path>/(?:%s))(?=["#?])' % '|'.join(n for n, _ in MOVES))


def reecrire_liens(s):
    return LIEN_RE.subn(lambda m: m.group('pre') + (m.group('dom') or '') + NEW[m.group('path')], s)


def remplacer_attr(s, ancien, nouveau):
    """Dans les balises <a> SEULEMENT : href="ancien" et
    href="https://webautonomos.es/ancien" -> nouveau. Les <link> (canonical,
    hreflang) ne sont jamais touchés."""
    compte = [0]
    cible = re.compile(r'href="(%s)?%s"' % (re.escape(BASE), re.escape(ancien)))

    def balise(m):
        t, k = cible.subn(lambda x: 'href="%s%s"' % (x.group(1) or '', nouveau), m.group(0))
        compte[0] += k
        return t
    s = re.sub(r'<a\b[^>]*>', balise, s)
    return s, compte[0]


def bloc_div(s, debut):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[debut:]):
        d += 1 if m.group(0) == '<div' else -1
        if d == 0:
            return debut + m.start()          # index du </div> fermant
    return -1


def ajouter_avis(s, conf):
    if 'Sabine O.' in s:
        return s, 'déjà présents'
    a_score = '<span class="tp-score">%s</span>' % conf['score'][0]
    if s.count(a_score) != 1 or s.count(conf['count'][0]) != 1:
        abandon('note ou compteur d\'avis introuvable (%s)' % conf['dot'])
    s = s.replace(a_score, '<span class="tp-score">%s</span>' % conf['score'][1])
    s = s.replace(conf['count'][0], conf['count'][1])
    m = re.search(r'<div class="tp-track" id="tpTrack">', s)
    fin = bloc_div(s, m.start()) if m else -1
    if fin < 0:
        abandon('carrousel introuvable (%s)' % conf['dot'])
    n0 = s.count('class="tp-slide"')
    cartes = ''
    for txt, qui, tr in conf['cartes']:
        cartes += ('<div class="tp-slide"><div class="tp-card"><div class="tp-stars">★★★★★</div>'
                   '<blockquote>« %s »</blockquote><div class="tp-who">— %s%s</div></div></div>'
                   % (txt, qui, '<span class="tp-tr">%s</span>' % tr if tr else ''))
    s = s[:fin] + cartes + s[fin:]
    m = re.search(r'<div class="tp-dots" id="tpDots">.*?</div>', s, re.S)
    if not m:
        abandon('points du carrousel introuvables (%s)' % conf['dot'])
    points = ''.join('<button class="tp-dot" onclick="tpGo(%d)" aria-label="%s %d"></button>'
                     % (k, conf['dot'], k + 1) for k in (n0, n0 + 1))
    s = s[:m.end() - 6] + points + s[m.end() - 6:]
    return s, '%d -> %d cartes' % (n0, n0 + 2)


def controles(fichiers, originaux):
    """Vérifications bloquantes sur le contenu final (dict rel -> texte).
    originaux : rel final -> texte d'origine, pour comparer l'équilibre des
    balises avant/après (certaines pages ont déjà un </div> en trop, que le
    navigateur tolère : on vérifie seulement que le script n'en ajoute pas)."""
    err = []
    ancien = re.compile(r'(?:href|content)="(?:https://webautonomos\.es)?/(?:%s)(?=["#?])'
                        % '|'.join(n for n, _ in MOVES))
    ancien_abs = re.compile(r'https://webautonomos\.es/(?:%s)(?=["#?\s<])'
                            % '|'.join(n for n, _ in MOVES))
    sources = {'%s.html' % n for n, _ in MOVES}
    for rel in pages_html():
        if rel in sources:
            continue
        s = fichiers.get(rel) or lire(rel)
        if ancien.search(s) or ancien_abs.search(s):
            err.append('%s : lien vers une ancienne adresse' % rel)
    for rel in fichiers:
        if rel not in set(pages_html()) and (ancien.search(fichiers[rel]) or ancien_abs.search(fichiers[rel])):
            err.append('%s : lien vers une ancienne adresse' % rel)
    for n, l in MOVES:
        rel = '%s/%s.html' % (l, n)
        s = fichiers[rel]
        can = re.findall(r'<link rel="canonical" href="([^"]+)"', s)
        if can != [BASE + NEW['/' + n]]:
            err.append('%s : canonical %s' % (rel, can))
        if '<html lang="%s"' % l not in s:
            err.append('%s : lang ≠ %s' % (rel, l))
    for rel in ('demandez-votre-demo.html', 'get-your-demo.html'):
        can = re.findall(r'<link rel="canonical" href="([^"]+)"', fichiers[rel])
        if len(can) != 1:
            err.append('%s : %d canonical' % (rel, len(can)))
    for rel in PAGES_FR + PAGES_EN:
        s = fichiers[rel]
        if re.search(r'<a [^>]*href="(?:https://webautonomos\.es)?/"', s):
            err.append('%s : lien encore vers l\'accueil espagnol' % rel)
    for rel in PAGES_EN:
        liens = ' '.join(re.findall(r'<a\b[^>]*>', fichiers[rel]))
        for a, _ in EN_LOCAL:
            if re.search(r'href="(?:https://webautonomos\.es)?%s"' % re.escape(a), liens):
                err.append('%s : lien encore vers %s' % (rel, a))
    # hreflang réciproques dans chaque groupe
    for g in GROUPES:
        jeux = []
        for rel in g:
            alt = sorted(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"',
                                    fichiers[rel]))
            jeux.append(alt)
            for tag, url in alt:
                cible = url.replace(BASE, '').lstrip('/')
                if not (os.path.isfile(os.path.join(ROOT, cible + '.html'))
                        or cible + '.html' in fichiers):
                    err.append('%s : hreflang %s vers une page absente (%s)' % (rel, tag, url))
        if any(j != jeux[0] for j in jeux):
            err.append('hreflang non réciproques dans le groupe %s' % ', '.join(g))
    # structure et scripts
    def ecart(texte, tag):
        vis = re.sub(r'<!--.*?-->', '', texte, flags=re.S)
        vis = re.sub(r'<script.*?</script>', '', vis, flags=re.S)
        return len(re.findall(r'<%s[\s>]' % tag, vis)) - vis.count('</%s>' % tag)
    for rel, s in fichiers.items():
        for tag in ('div', 'section', 'a', 'p', 'ul', 'blockquote', 'button'):
            if ecart(s, tag) != ecart(originaux[rel], tag):
                err.append('%s : équilibre des <%s> modifié (%d -> %d)'
                           % (rel, tag, ecart(originaux[rel], tag), ecart(s, tag)))
        for bloc in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
            try:
                json.loads(bloc)
            except ValueError as exc:
                err.append('%s : JSON-LD invalide (%s)' % (rel, exc))
        scripts = [m.group(2) for m in re.finditer(r'<script(\s[^>]*)?>(.*?)</script>', s, re.S)
                   if 'ld+json' not in (m.group(1) or '') and m.group(2).strip()]
        with tempfile.TemporaryDirectory() as tmp:
            for k, js in enumerate(scripts):
                f = os.path.join(tmp, 's%d.js' % k)
                open(f, 'w', encoding='utf-8').write(js)
                r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
                if r.returncode:
                    err.append('%s : script %d invalide (%s)' % (rel, k, r.stderr.strip()[:120]))
    return err


def main():
    os.chdir(ROOT)
    # ── 0. état de départ ────────────────────────────────────────────────────
    sources = ['%s.html' % n for n, _ in MOVES]
    cibles = ['%s/%s.html' % (l, n) for n, l in MOVES]
    if all(os.path.exists(c) for c in cibles) and not any(os.path.exists(x) for x in sources):
        abandon('migration déjà faite (les 8 pages sont déjà sous /fr/ et /en/).')
    manquants = [x for x in sources if not os.path.isfile(x)]
    presents = [c for c in cibles if os.path.exists(c)]
    if manquants or presents:
        abandon('état inattendu. Sources absentes : %s ; cibles déjà présentes : %s'
                % (manquants or '-', presents or '-'))
    if not os.path.isfile('fr/index.html') or not os.path.isfile('en/index.html'):
        abandon('fr/index.html ou en/index.html absent : lancer d\'abord build_lang_homes.py.')

    # ── 1. contenu final en mémoire ──────────────────────────────────────────
    depl = dict(zip(sources, cibles))
    fichiers, origine, rapport = {}, {}, []
    for rel in pages_html():
        s = lire(rel)
        dest = depl.get(rel, rel)
        s2, n = reecrire_liens(s)
        if n or rel in depl:
            fichiers[dest], origine[dest] = s2, rel
            rapport.append('  liens réécrits : %-32s %2d%s' % (
                dest, n, ('   (déplacé depuis %s)' % rel) if rel in depl else ''))

    def charger(rel):
        if rel not in fichiers:
            fichiers[rel], origine[rel] = lire(rel), rel
        return fichiers[rel]

    # ── 3. canonical et Open Graph des pages de démo FR/EN ───────────────────
    for rel, bloc in OG_NOUVEAU.items():
        s = charger(rel)
        if s.count(OG_ANCIEN) != 1:
            abandon('bloc Open Graph hérité introuvable dans %s' % rel)
        fichiers[rel] = s.replace(OG_ANCIEN, bloc)
        rapport.append('  canonical/OG    : %-32s 2e canonical supprimé' % rel)

    # ── 2. liens « Accueil » et liens espagnols des pages FR/EN ──────────────
    for rel, home in [(r, '/fr/') for r in PAGES_FR] + [(r, '/en/') for r in PAGES_EN]:
        s, n = remplacer_attr(charger(rel), '/', home)
        if rel in PAGES_EN:
            for a, b in EN_LOCAL:
                s, k = remplacer_attr(s, a, b)
                n += k
        fichiers[rel] = s
        rapport.append('  accueil/langue  : %-32s %2d' % (rel, n))

    # ── 4. avis ──────────────────────────────────────────────────────────────
    for rel, conf in AVIS.items():
        fichiers[rel], info = ajouter_avis(charger(rel), conf)
        rapport.append('  avis            : %-32s %s' % (rel, info))

    # ── 5. contrôles ─────────────────────────────────────────────────────────
    err = controles(fichiers, {d: lire(o) for d, o in origine.items()})
    if err:
        abandon('vérifications :\n  - ' + '\n  - '.join(err))

    # ── 6. fichiers techniques ───────────────────────────────────────────────
    red = lire('_redirects')
    if '/tarifs   /fr/tarifs' in red:
        abandon('_redirects contient déjà les règles.')
    if re.search(r'^/(%s)/?\s' % '|'.join(n for n, _ in MOVES), red, re.M):
        abandon('_redirects contient déjà une règle pour une des 8 adresses.')
    sm = lire('_tools/generate_sitemap.py')
    if sm.count(SITEMAP_ANCRE) != 1:
        abandon('ancre introuvable dans generate_sitemap.py')
    dp = lire('_tools/build_demo_pages.py')
    if 'PÉRIMÉ' not in dp and dp.count(DEMO_ANCRE) != 1:
        abandon('ancre introuvable dans build_demo_pages.py')
    llms = lire('llms.txt')
    if '/fr/' not in llms and llms.count(LLMS_ANCRE) != 1:
        abandon('ancre introuvable dans llms.txt')
    techniques = {
        'llms.txt': llms if '/fr/' in llms else llms.replace(LLMS_ANCRE, LLMS_AJOUT + LLMS_ANCRE),
        '_redirects': red.rstrip('\n') + '\n' + REDIRECTS,
        '_tools/generate_sitemap.py': sm.replace(SITEMAP_ANCRE, SITEMAP_NOUVEAU),
        '_tools/build_demo_pages.py': dp if 'PÉRIMÉ' in dp else dp.replace(DEMO_ANCRE, DEMO_AVERT),
    }
    try:
        compile(techniques['_tools/generate_sitemap.py'], 'generate_sitemap.py', 'exec')
        compile(techniques['_tools/build_demo_pages.py'], 'build_demo_pages.py', 'exec')
    except SyntaxError as exc:
        abandon('script technique invalide : %s' % exc)

    # ── 7. sauvegarde puis écriture ──────────────────────────────────────────
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = os.path.expanduser('~/webautonomos-work/backups/migrate_fr_en_%s' % stamp)
    for rel in sorted(set(origine.values()) | set(techniques)):
        d = os.path.join(bak, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(rel, d)
    for dest, s in fichiers.items():
        os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as fh:
            fh.write(s)
    for src in sources:
        os.remove(src)
    for rel, s in techniques.items():
        with open(rel, 'w', encoding='utf-8') as fh:
            fh.write(s)

    print('\n'.join(rapport))
    print('  _redirects      : 16 règles 301 ajoutées')
    print('  generate_sitemap.py : fr/*.html et en/*.html pris en compte')
    print('  build_demo_pages.py : marqué PÉRIMÉ')
    print('  llms.txt        : sections English et Français ajoutées')
    print('\nOK — 8 pages déplacées, %d fichiers écrits. Sauvegarde : %s'
          % (len(fichiers), bak.replace(os.path.expanduser('~'), '~')))


if __name__ == '__main__':
    main()
