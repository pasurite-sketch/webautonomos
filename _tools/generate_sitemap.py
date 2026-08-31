# -*- coding: utf-8 -*-
"""Regenere sitemap.xml a partir du DISQUE, en modele A.

Modele A : une <loc> par groupe linguistique, pointant vers la version
espagnole, accompagnee de ses alternates hreflang (es, ca-ES, en, fr) et de
x-default. Les pages hors blog suivent, en <loc> seule.

Le sitemap existant n'est PAS lu comme source de verite : il ne sert qu'a
recuperer les <lastmod> deja publies, pour ne pas repousser artificiellement
la date de toutes les pages a chaque execution.

Usage (depuis la racine du repo) :
    python3 _tools/generate_sitemap.py
    python3 _tools/generate_sitemap.py --dry-run   # affiche le rapport, n'ecrit pas
    python3 _tools/generate_sitemap.py --check     # sort 1 si le fichier n'est pas a jour

Le script n'ecrit rien si une verification echoue.
"""
import argparse
import datetime
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = 'https://webautonomos.es'
SITEMAP = os.path.join(ROOT, 'sitemap.xml')

LANGS = ('es', 'val', 'en', 'fr')
HREFLANG = {'es': 'es', 'val': 'ca-ES', 'en': 'en', 'fr': 'fr'}
# Langue portant la <loc> canonique du groupe, par ordre de preference. L'espagnol
# gagne toujours quand il existe ; les autres ne servent qu'aux groupes orphelins
# (un article traduit dont l'original espagnol n'a jamais ete ecrit).
LOC_ORDER = ('es', 'fr', 'en', 'val')

# --------------------------------------------------------------------------
# 1. Inventaire du disque
# --------------------------------------------------------------------------

# Pages hors blog exclues du sitemap, en plus des noindex detectes :
#   - les gabarits et la page d'erreur, qui ne sont pas des pages publiques ;
#   - les demos client, hors perimetre editorial.
EXCLUDE_PAGES = {'404.html', 'template-article.html', 'index.html'}
EXCLUDE_DIRS = {'blog', 'node_modules', '_tools', 'scripts', '.git',
                '.github', 'demo-carpintero', 'demo-dentistas'}

NOINDEX_RE = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
                        re.I)


def is_noindex(path):
    return NOINDEX_RE.search(read(path)) is not None


_cache = {}


def read(path):
    if path not in _cache:
        with open(path, encoding='utf-8', errors='replace') as fh:
            _cache[path] = fh.read()
    return _cache[path]


def blog_files():
    """{(lang, slug): chemin} pour blog/{lang}/{slug}.html uniquement.

    Sont volontairement ignores :
      - blog/{slug}.html (6 slugs herites) : doublons de blog/es/{slug}.html,
        qui est la version de reference ;
      - blog/{lang}/{slug}/index.html (50 variantes) : meme contenu, meme URL
        a un slash pres.
    """
    out = {}
    for lang in LANGS:
        for path in sorted(glob.glob(os.path.join(ROOT, 'blog', lang, '*.html'))):
            out[(lang, os.path.basename(path)[:-5])] = path
    return out


def page_files():
    """[(url, chemin)] des pages hors blog, en forme canonique.

    Un fichier X.html a la racine est servi sous /X ; un dossier X/index.html
    est servi sous /X/ (Workers normalise /X en 307 vers /X/, ce qui ferait
    entrer une redirection dans le sitemap). Quand les deux existent, la
    version racine gagne : c'est celle qui repond 200 sans redirection.
    """
    roots = {}
    for path in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        name = os.path.basename(path)
        if name in EXCLUDE_PAGES:
            continue
        roots[name[:-5]] = ('/%s' % name[:-5], path)

    dirs = {}
    for path in sorted(glob.glob(os.path.join(ROOT, '*', 'index.html'))):
        name = os.path.basename(os.path.dirname(path))
        if name in EXCLUDE_DIRS or name in roots:
            continue
        dirs[name] = ('/%s/' % name, path)

    return [v for _, v in sorted(list(roots.items()) + list(dirs.items()))]


# --------------------------------------------------------------------------
# 2. Resolution des groupes linguistiques
# --------------------------------------------------------------------------

class Union(object):
    def __init__(self, items):
        self.parent = {i: i for i in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def join(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


HREF_RE = re.compile(r'hreflang=["\']([^"\']+)["\']\s+href=["\']([^"\']+)["\']')
URL_RE = re.compile(r'/blog/(es|val|en|fr)/([^"\'/#?]+)')
BY_HREFLANG = {v: k for k, v in HREFLANG.items()}


def link_by_hreflang(files, uf, stats):
    """Relie les fichiers par les hreflang qu'ils declarent deja.

    Une declaration est ignoree si sa cible n'existe pas sur le disque, ou si
    le prefixe de langue de l'URL contredit le hreflang annonce : le sitemap ne
    doit pas propager une erreur de balisage.
    """
    for node, path in files.items():
        for tag, url in HREF_RE.findall(read(path)):
            lang = BY_HREFLANG.get(tag)
            if lang is None:                      # x-default : redondant ici
                continue
            m = URL_RE.search(url)
            if not m:
                continue
            target = (m.group(1), m.group(2))
            if target not in files:
                stats['dangling'] += 1
                continue
            if target[0] != lang:
                stats['incoherent'] += 1
                continue
            uf.join(node, target)
            stats['linked'] += 1


def link_by_spa_id(files, uf, stats):
    """Relie les fichiers par l'id d'article partage dans les donnees du SPA.

    Indispensable : les articles publies par le pipeline recoivent des slugs
    localises, et generate_spa_articles.py apparie les langues par slug de base.
    Des slugs differents d'une langue a l'autre cassent donc l'appariement, et
    ces fichiers sortent avec un seul hreflang — le leur. L'id, lui, est commun
    aux quatre tableaux de langue.

    Retourne False si les donnees sont illisibles (node absent) : la resolution
    par hreflang reste alors seule, avec un avertissement.
    """
    sys.path.insert(0, HERE)
    try:
        from generate_spa_articles import load_translations, split_slug
        data = load_translations()
    except (ImportError, SystemExit) as exc:      # noqa: BLE001
        stats['spa_error'] = str(exc) or 'donnees SPA illisibles'
        return False

    by_id = {}
    for lang in LANGS:
        for art in ((data.get(lang) or {}).get('blog') or {}).get('articles') or []:
            prefix, base = split_slug(art['slug'])
            node = (prefix or lang, base)
            if node in files:
                by_id.setdefault(art.get('id'), []).append(node)

    for nodes in by_id.values():
        for other in nodes[1:]:
            uf.join(nodes[0], other)
            stats['linked_spa'] += 1
    return True


# Groupes que ni les hreflang ni les donnees du SPA ne peuvent relier. A ce jour
# un seul cas : le guest post « reservas online », ecrit hors pipeline, dont
# aucune des quatre versions ne declare de hreflang et dont la version francaise
# n'existe pas dans les tableaux du SPA. Sans cette table, l'article espagnol et
# ses traductions sortiraient en <loc> etrangeres les unes aux autres.
# Le slug anglais a change le 2026-09-01 avec la migration des slugs EN.
MANUAL_GROUPS = [
    [('es', 'reservas-online-autonomos-2026'),
     ('val', 'reserves-en-linia-per-a-autonoms'),
     ('en', 'online-booking-for-freelancers'),
     ('fr', 'reservation-en-ligne-pour-independants')],
]


def link_manual(files, uf, stats):
    for nodes in MANUAL_GROUPS:
        present = [n for n in nodes if n in files]
        for other in present[1:]:
            uf.join(present[0], other)
            stats['linked_manual'] += 1


def groups(files, stats):
    uf = Union(files)
    link_by_hreflang(files, uf, stats)
    link_manual(files, uf, stats)
    stats['spa_ok'] = link_by_spa_id(files, uf, stats)

    out = {}
    for node in files:
        out.setdefault(uf.find(node), {})[node[0]] = node[1]
    # Un groupe malforme (deux fichiers de la meme langue fusionnes) serait
    # silencieusement ampute par le dict ci-dessus. On compte la perte.
    stats['nodes_kept'] = sum(len(g) for g in out.values())
    return sorted(out.values(), key=lambda g: (g.get('es') or g.get('fr')
                                               or g.get('en') or g.get('val')))


# --------------------------------------------------------------------------
# 3. lastmod
# --------------------------------------------------------------------------

DATE_RE = re.compile(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})')
OG_DATE_RE = re.compile(r'article:published_time["\'][^>]*content=["\'](\d{4}-\d{2}-\d{2})')


def existing_lastmod():
    """{url canonique -> lastmod} lu dans le sitemap actuel, s'il existe."""
    if not os.path.exists(SITEMAP):
        return {}
    txt = read(SITEMAP)
    out = {}
    for block in re.findall(r'(?s)<url>.*?</url>', txt):
        loc = re.search(r'<loc>([^<]+)</loc>', block)
        lm = re.search(r'<lastmod>([^<]+)</lastmod>', block)
        if loc and lm:
            out[loc.group(1).rstrip('/')] = lm.group(1).strip()[:10]
    return out


def lastmod_for(url, path, previous):
    """Date de derniere modification, par ordre de fiabilite decroissante.

    La date deja publiee gagne : la republier telle quelle evite d'annoncer a
    Google une modification qui n'a pas eu lieu. A defaut, la date de
    publication declaree par la page elle-meme. Le mtime n'arrive qu'en
    dernier : sur un runner CI, il vaut l'heure du checkout pour tous les
    fichiers, ce qui daterait le corpus entier d'aujourd'hui.
    """
    prev = previous.get(url.rstrip('/'))
    if prev:
        return prev
    txt = read(path)
    m = DATE_RE.search(txt) or OG_DATE_RE.search(txt)
    if m:
        return m.group(1)
    ts = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    return ts.strftime('%Y-%m-%d')


# --------------------------------------------------------------------------
# 4. Rendu
# --------------------------------------------------------------------------

HEAD = ('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')


def block(loc, lastmod, priority, alternates=(), changefreq='monthly'):
    lines = ['    <url>', '        <loc>%s</loc>' % loc]
    for tag, url in alternates:
        lines.append('        <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                     % (tag, url))
    lines.append('        <lastmod>%s</lastmod><changefreq>%s</changefreq>'
                 '<priority>%s</priority>' % (lastmod, changefreq, priority))
    lines.append('    </url>')
    return '\n'.join(lines) + '\n'


def build(files, grps, pages, previous, stats):
    out = [HEAD]
    out.append(block(BASE + '/', previous.get(BASE, stats['today']), '1.0',
                     changefreq='weekly'))
    out.append(block(BASE + '/blog/', previous.get(BASE + '/blog', stats['today']),
                     '0.9', changefreq='weekly'))

    for g in grps:
        lang = next(l for l in LOC_ORDER if l in g)
        loc = '%s/blog/%s/%s' % (BASE, lang, g[lang])
        alts = []
        if len(g) > 1:
            # Un groupe d'un seul membre n'a rien a declarer : un hreflang
            # solitaire pointant sur soi-meme est du bruit, pas un signal.
            for l in LANGS:
                if l in g:
                    alts.append((HREFLANG[l], '%s/blog/%s/%s' % (BASE, l, g[l])))
            alts.append(('x-default', loc))
        out.append(block(loc, lastmod_for(loc, files[(lang, g[lang])], previous),
                         '0.7', alts))

    for url, path in pages:
        out.append(block(BASE + url, lastmod_for(BASE + url, path, previous), '0.8'))

    out.append('</urlset>\n')
    return ''.join(out)


# --------------------------------------------------------------------------
# 5. Verifications bloquantes
# --------------------------------------------------------------------------

def verify(xml, files, pages):
    errs = []
    try:
        ET.fromstring(xml)
    except ET.ParseError as exc:
        errs.append('XML mal forme : %s' % exc)
        return errs                                # le reste n'a plus de sens

    if xml.count('</urlset>') != 1:
        errs.append('</urlset> present %d fois' % xml.count('</urlset>'))

    locs = re.findall(r'<loc>([^<]+)</loc>', xml)
    dups = sorted({u for u in locs if locs.count(u) > 1})
    if dups:
        errs.append('%d <loc> en double : %s' % (len(dups), ', '.join(dups[:5])))

    page_urls = {BASE + u for u, _ in pages}
    for u in locs:
        if u in (BASE + '/', BASE + '/blog/') or u in page_urls:
            continue
        m = re.match(r'^%s/blog/(es|val|en|fr)/(.+)$' % re.escape(BASE), u)
        if not m or (m.group(1), m.group(2)) not in files:
            errs.append('<loc> sans fichier sur le disque : %s' % u)

    for tag, url in re.findall(r'hreflang="([^"]+)"\s+href="([^"]+)"', xml):
        if tag == 'x-default':
            continue
        m = URL_RE.search(url)
        if not m or (m.group(1), m.group(2)) not in files:
            errs.append('alternate %s sans fichier : %s' % (tag, url))

    if len(locs) != len(set(locs)):
        errs.append('doublons residuels dans les <loc>')
    return errs


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help="n'ecrit pas le fichier")
    ap.add_argument('--check', action='store_true',
                    help='sort 1 si sitemap.xml differe du resultat')
    args = ap.parse_args()

    os.chdir(ROOT)
    stats = {'dangling': 0, 'incoherent': 0, 'linked': 0, 'linked_spa': 0, 'linked_manual': 0,
             'spa_ok': True, 'spa_error': '',
             'today': datetime.date.today().isoformat()}

    files = blog_files()
    pages = [(u, p) for u, p in page_files() if not is_noindex(p)]
    excluded = [(u, p) for u, p in page_files() if is_noindex(p)]
    grps = groups(files, stats)
    previous = existing_lastmod()
    xml = build(files, grps, pages, previous, stats)

    before = len(re.findall(r'<loc>', read(SITEMAP))) if os.path.exists(SITEMAP) else 0
    after = len(re.findall(r'<loc>', xml))

    print('Groupes linguistiques : %d (sur %d fichiers d\'article)'
          % (len(grps), len(files)))
    print('  liens hreflang exploites : %d | via id SPA : %d'
          % (stats['linked'], stats['linked_spa']))
    print('  liens declares a la main : %d' % stats['linked_manual'])
    print('  hreflang morts ignores : %d | incoherents : %d'
          % (stats['dangling'], stats['incoherent']))
    if not stats['spa_ok']:
        print('  ATTENTION : donnees SPA illisibles (%s) — resolution par hreflang '
              'seule, des groupes peuvent rester eclates.' % stats['spa_error'])
    print('Pages hors blog : %d retenues, %d exclues pour noindex'
          % (len(pages), len(excluded)))
    for u, _ in excluded:
        print('    exclue (noindex) : %s' % u)

    partial = [g for g in grps if len(g) < 4]
    print('Groupes incomplets : %d' % len(partial))
    for g in partial:
        print('    [%-11s] %s' % (''.join(l for l in LANGS if l in g),
                                  ' | '.join('%s:%s' % (l, g[l])
                                             for l in LANGS if l in g)))

    errs = verify(xml, files, pages)
    if errs:
        print('\nECHEC des verifications — rien ecrit :')
        for e in errs:
            print('  - %s' % e)
        return 1
    print('\nVerifications : XML valide, 1 </urlset>, 0 doublon, '
          '0 <loc> orpheline. <loc> : %d -> %d' % (before, after))

    if args.check:
        same = os.path.exists(SITEMAP) and read(SITEMAP) == xml
        print('sitemap.xml %s' % ('a jour' if same else 'PERIME'))
        return 0 if same else 1
    if args.dry_run:
        print('(--dry-run : sitemap.xml inchange)')
        return 0
    with open(SITEMAP, 'w', encoding='utf-8') as fh:
        fh.write(xml)
    print('sitemap.xml reecrit.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
