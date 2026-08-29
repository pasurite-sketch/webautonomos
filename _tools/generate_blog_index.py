#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenere blog/index.html : l'index statique du blog, servi sous /blog/.

Parcourt blog/es, blog/val, blog/en et blog/fr, extrait la balise de titre reelle
de chaque article et reconstruit la liste complete groupee par langue. Tous les
compteurs affiches (total, par section, meta description) sont derives du disque :
aucune valeur codee en dur, pour que la page ne se desynchronise plus.

Exclusion volontaire : les 6 slugs herites a la racine de blog/ (blog/{slug}.html,
servis sous /blog/{slug}). Ils declarent un canonical croise vers /blog/es/{slug},
donc les lier depuis l'index enverrait du maillage interne vers des URL qui se
declarent elles-memes non canoniques, et afficherait deux fois le meme titre.

Usage :
    python3 _tools/generate_blog_index.py
    python3 _tools/generate_blog_index.py --check   # verifie sans ecrire
"""

import argparse
import html as H
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
OUT = os.path.join(ROOT, 'blog', 'index.html')

# (code repertoire, intitule de section)
LANGS = [
    ('es',  'Artículos en español'),
    ('val', 'Articles en valencià'),
    ('en',  'Articles in English'),
    ('fr',  'Articles en français'),
]

TITLE_SUFFIX = re.compile(r'\s*[|–—-]\s*WebAutonomos(\.es)?\s*$', re.I)
TITLE_TAG = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)


def article_title(path, slug):
    """Titre affichable, tire de la balise <title> du fichier."""
    with open(path, encoding='utf-8', errors='replace') as fh:
        head = fh.read(20000)
    m = TITLE_TAG.search(head)
    if not m:
        return slug
    text = H.unescape(re.sub(r'\s+', ' ', m.group(1)).strip())
    return TITLE_SUFFIX.sub('', text).strip() or slug


def collect(lang):
    """[(slug, titre)] tries par titre, pour le repertoire blog/{lang}."""
    d = os.path.join(ROOT, 'blog', lang)
    if not os.path.isdir(d):
        return []
    items = []
    for name in sorted(os.listdir(d)):
        if not name.endswith('.html') or name == 'index.html':
            continue
        slug = name[:-5]
        items.append((slug, article_title(os.path.join(d, name), slug)))
    return sorted(items, key=lambda x: x[1].lower())


def build(data):
    total = sum(len(v) for v in data.values())
    langs_present = [(code, label) for code, label in LANGS if data.get(code)]

    # Enumeration des langues pour la meta description, dans la langue de la page.
    names = {'es': 'español', 'val': 'valenciano', 'en': 'inglés', 'fr': 'francés'}
    listed = [names[c] for c, _ in langs_present]
    langs_text = (', '.join(listed[:-1]) + ' y ' + listed[-1]) if len(listed) > 1 else listed[0]

    desc = ('Guías prácticas para autónomos de la Comunidad Valenciana: páginas web, '
            'SEO local, Google Business Profile y marketing digital. '
            f'{total} artículos en {langs_text}.')
    title = 'Blog para autónomos: webs, SEO local y Google Business | WebAutonomos'

    sections = []
    for code, label in langs_present:
        lis = '\n'.join(
            f'      <li><a href="/blog/{code}/{slug}">{H.escape(t)}</a></li>'
            for slug, t in data[code])
        sections.append(
            f'    <section class="grp" id="{code}">\n'
            f'      <h2>{label} <span class="cnt">{len(data[code])}</span></h2>\n'
            f'      <ul>\n{lis}\n      </ul>\n'
            f'    </section>')

    return total, f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Index statique du blog. Existe pour que /blog/ reste un asset servi en 200
     apres le passage de not_found_handling a "404-page".
     Genere par _tools/generate_blog_index.py depuis les balises de titre reelles
     de blog/es, blog/val, blog/en et blog/fr. Ne pas editer a la main : relancer
     le script apres chaque publication d'article. -->
<title>{title}</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{BASE}/blog/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">

<link rel="alternate" hreflang="es" href="{BASE}/blog/">
<link rel="alternate" hreflang="x-default" href="{BASE}/blog/">

<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/blog/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="WebAutonomos">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="{BASE}/favicon.ico" type="image/x-icon">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">

<style>
  :root {{
    --blue:#1a3a8f; --blue-dark:#0f2060; --green:#22c55e;
    --grad:linear-gradient(135deg,#1a3a8f 0%,#1a7a5a 50%,#22c55e 100%);
    --white:#ffffff; --off:#f4fbf7; --gray:#64748b; --border:#d1e8d9; --text:#0f2040;
  }}
  * {{ box-sizing:border-box; }}
  html, body {{ margin:0; padding:0; }}
  body {{ font-family:'DM Sans',sans-serif; color:var(--text); background:var(--white);
         min-height:100vh; display:flex; flex-direction:column; }}
  main {{ flex:1; max-width:940px; width:100%; margin:0 auto; padding:64px 6% 72px; }}
  .crumb {{ font-size:0.9rem; color:var(--gray); margin:0 0 20px; }}
  .crumb a {{ color:var(--blue); text-decoration:none; }}
  h1 {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800;
        font-size:clamp(1.8rem,5vw,2.6rem); line-height:1.2; margin:0 0 16px; }}
  .lede {{ font-size:1.1rem; line-height:1.7; color:var(--gray); margin:0 0 32px; max-width:70ch; }}
  .jump {{ display:flex; flex-wrap:wrap; gap:10px; margin:0 0 44px; padding:0; list-style:none; }}
  .jump a {{ display:inline-block; padding:8px 16px; border-radius:999px;
             border:1px solid var(--border); background:var(--off);
             color:var(--blue); text-decoration:none; font-size:0.92rem; font-weight:600; }}
  .jump a:hover {{ background:var(--white); }}
  .grp {{ margin:0 0 44px; scroll-margin-top:24px; }}
  .grp h2 {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800;
             font-size:1.3rem; margin:0 0 16px; padding-bottom:10px;
             border-bottom:2px solid var(--border);
             display:flex; align-items:center; gap:10px; }}
  .cnt {{ font-family:'DM Sans',sans-serif; font-size:0.8rem; font-weight:600;
          color:var(--white); background:var(--grad);
          border-radius:999px; padding:2px 10px; }}
  .grp ul {{ list-style:none; margin:0; padding:0; }}
  .grp li {{ border-bottom:1px solid var(--border); }}
  .grp li a {{ display:block; padding:12px 4px; color:var(--text);
               text-decoration:none; font-size:1.02rem; line-height:1.5; }}
  .grp li a:hover {{ color:var(--blue); background:var(--off); }}
  footer {{ padding:24px 6%; background:var(--grad); display:flex; flex-wrap:wrap;
            align-items:center; justify-content:space-between; gap:12px; }}
  .fl {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1rem;
         color:rgba(255,255,255,0.85); text-decoration:none;
         display:flex; align-items:center; gap:6px; }}
  .flinks {{ display:flex; gap:20px; flex-wrap:wrap; }}
  .flinks a {{ color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem; }}
  .flinks a:hover {{ color:#fff; }}
  .fnap {{ flex-basis:100%; order:3; margin-top:4px; padding-top:16px;
           border-top:1px solid rgba(255,255,255,0.12);
           font-style:normal; font-size:0.78rem; line-height:1.7;
           color:rgba(255,255,255,0.55); display:flex; flex-direction:column; gap:1px; }}
  .fnap a {{ color:rgba(255,255,255,0.55); text-decoration:none; }}
  .fnap a:hover {{ color:rgba(255,255,255,0.85); }}
</style>
</head>
<body>

<main>
  <p class="crumb"><a href="/">Inicio</a> &rsaquo; Blog</p>

  <h1>Blog para autónomos</h1>
  <p class="lede">
    Guías prácticas sobre páginas web, SEO local, Google Business Profile y marketing
    digital para autónomos de la Comunidad Valenciana. {total} artículos disponibles.
  </p>

  <ul class="jump">
{chr(10).join(f'    <li><a href="#{c}">{l}</a></li>' for c, l in langs_present)}
  </ul>

{chr(10).join(sections)}
</main>

<footer>
  <a class="fl" href="/"><span>&#127760;</span> webautonomos.es</a>
  <div class="flinks">
    <a href="/aviso-legal">Aviso legal</a>
    <a href="/privacidad">Privacidad</a>
    <a href="/contacto">Contacto</a>
  </div>
  <address class="fnap">
    <strong>WebAutonomos</strong>
    <span>Calle Pintor Josep Segrelles, 26</span>
    <span>46870 Ontinyent, Valencia</span>
    <a href="tel:+34961877356">+34 961 877 356</a>
    <a href="mailto:info@webautonomos.es">info@webautonomos.es</a>
  </address>
</footer>

</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='verifie sans ecrire')
    args = ap.parse_args()

    data = {code: collect(code) for code, _ in LANGS}
    total, page = build(data)

    # --- verification : chaque lien vise un fichier reellement present, sans .html
    problems = []
    for href in re.findall(r'<li><a href="(/blog/[^"]+)"', page):
        if href.endswith('.html'):
            problems.append(('extension .html', href))
        rel = href.lstrip('/')
        if not (os.path.isfile(os.path.join(ROOT, rel + '.html'))
                or os.path.isfile(os.path.join(ROOT, rel, 'index.html'))):
            problems.append(('cible inexistante', href))

    # --- verification : aucun compteur fige hors de ceux qu'on vient de calculer
    counters = [int(n) for n in re.findall(r'<span class="cnt">(\d+)</span>', page)]
    expected = [len(data[c]) for c, _ in LANGS if data.get(c)]
    if counters != expected:
        problems.append(('compteurs de section', f'{counters} != {expected}'))
    # Le total doit apparaitre dans le lede, la meta description et og:description.
    if page.count(f'{total} artículos') < 3:
        problems.append(('total', f'"{total} artículos" trouve {page.count(f"{total} artículos")}x, attendu 3'))
    # Aucun autre compteur fige : tout "<n> artículos" doit valoir le total courant.
    stale = {n for n in re.findall(r'(\d+) artículos', page) if int(n) != total}
    if stale:
        problems.append(('compteur fige', 'valeurs parasites : ' + ', '.join(sorted(stale))))

    for code, _ in LANGS:
        print('  blog/%-4s %3d' % (code, len(data[code])))
    print('  %-9s %3d' % ('TOTAL', total))

    if problems:
        print('\nAnomalies, RIEN ecrit :')
        for kind, detail in problems:
            print('  - %s : %s' % (kind, detail))
        return 1

    if args.check:
        print('\n--check : aucune anomalie, fichier non modifie.')
        return 0

    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(page)
    print('\nblog/index.html ecrit : %d octets, %d liens.' % (len(page.encode('utf-8')), total))
    return 0


if __name__ == '__main__':
    sys.exit(main())
