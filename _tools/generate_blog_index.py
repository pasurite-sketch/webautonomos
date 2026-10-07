#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenere blog/index.html : l'index statique du blog, servi sous /blog/.

Parcourt blog/es, blog/val, blog/en et blog/fr et affiche chaque article en fiche
(photo, categorie, date, titre, resume), une langue a la fois, avec des filtres par
nature d'article (Todos, Paginas Web, SEO Local, Google My Business, Marketing
Digital, Automatizacion, Facturacion y Legal), comme l'ancien blog de l'application.
Tout vient du disque : titre (H1), resume (meta description), categorie (fil
d'Ariane JSON-LD « blog?categoria= »), date (datePublished) et photo
(_tools/photos/images.json, version 800 px). Une page qui n'a pas l'une de ces
informations la reprend d'une autre version linguistique de la meme page (meme
« sujet » dans images.json). Aucun compteur code en dur.

Sans JavaScript, les quatre langues s'affichent l'une sous l'autre et tous les liens
restent dans le HTML. Avec JavaScript, une seule langue est visible (#es, #val, #en,
#fr dans l'adresse, l'espagnol par defaut) et les filtres apparaissent.

Pas d'intertitre <h2> dans la page : la maquette de _tools/photos se pose ainsi en
fin de page, sous les fiches, et la photo d'en-tete apres le paragraphe .lede.

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
import json
import os
import re
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos'))
from photos_lib import injecter as poser_photo  # photo prévue par _tools/photos/images.json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
OUT = os.path.join(ROOT, 'blog', 'index.html')
IMAGES = os.path.join(ROOT, '_tools', 'photos', 'images.json')

# (code repertoire, intitule de section, nom court de la langue)
LANGS = [
    ('es',  'Artículos en español',  'Español'),
    ('val', 'Articles en valencià',  'Valencià'),
    ('en',  'Articles in English',   'English'),
    ('fr',  'Articles en français',  'Français'),
]

# Categories, dans l'ordre des filtres ; intitules repris des badges des articles.
CATS = [
    ('paginas-web',        '#3B82F6', {'es': 'Páginas Web', 'val': 'Pàgines Web', 'en': 'Websites', 'fr': 'Sites web'}),
    ('seo-local',          '#10B981', {'es': 'SEO Local', 'val': 'SEO Local', 'en': 'Local SEO', 'fr': 'SEO local'}),
    ('google-my-business', '#F59E0B', {'es': 'Google My Business', 'val': 'Google My Business',
                                       'en': 'Google My Business', 'fr': 'Google My Business'}),
    ('marketing-digital',  '#8B5CF6', {'es': 'Marketing Digital', 'val': 'Màrqueting Digital',
                                       'en': 'Digital Marketing', 'fr': 'Marketing digital'}),
    ('automatizacion',     '#0EA5E9', {'es': 'Automatización', 'val': 'Automatització', 'en': 'Automation',
                                       'fr': 'Automatisation'}),
    ('facturacion-legal',  '#64748B', {'es': 'Facturación y Legal', 'val': 'Facturació i Legal',
                                       'en': 'Invoicing & Legal', 'fr': 'Facturation et juridique'}),
]
CAT_DEFAUT = 'paginas-web'
TOUS = {'es': 'Todos', 'val': 'Tots', 'en': 'All', 'fr': 'Tous'}
FILTRER = {'es': 'Filtrar por tema', 'val': 'Filtrar per tema', 'en': 'Filter by topic', 'fr': 'Filtrer par thème'}
MOIS = {
    'es': ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sept', 'oct', 'nov', 'dic'],
    'val': ['gen.', 'febr.', 'març', 'abr.', 'maig', 'juny', 'jul.', 'ag.', 'set.', 'oct.', 'nov.', 'des.'],
    'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
    'fr': ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'],
}

H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S | re.I)
DESC = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
CAT = re.compile(r'blog/?\?categoria=([a-z0-9-]+)')  # /blog/?categoria= depuis le 07/10/2026
DATE = re.compile(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})')
PARA = re.compile(r'<p\b[^>]*>(.*?)</p>', re.S | re.I)


def texte(fragment):
    return H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', fragment))).strip()


def resume_de(s):
    """Meta description, sinon debut du premier paragraphe consistant du corps."""
    m = DESC.search(s)
    if m and m.group(1).strip():
        return H.unescape(m.group(1)).strip()
    corps = s[s.find('<body'):] if '<body' in s else s
    for p in PARA.finditer(corps):
        t = texte(p.group(1))
        if len(t) >= 80:
            if len(t) <= 160:
                return t
            return t[:157].rsplit(' ', 1)[0].rstrip(',;:') + '…'
    return ''


def lire(lang, slug, photos):
    rel = 'blog/%s/%s.html' % (lang, slug)
    with open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace') as fh:
        s = fh.read()
    m = H1.search(s)
    cat, date = CAT.search(s), DATE.search(s)
    return {
        'lang': lang, 'slug': slug, 'rel': rel,
        'titre': texte(m.group(1)) if m else slug,
        'resume': resume_de(s),
        'cat': cat.group(1) if cat else None,
        'date': date.group(1) if date else None,
        'photo': photos.get(rel),
    }


def collect():
    """{lang: [article]} ; les manques sont repris d'une autre langue de la meme page."""
    photos = json.load(open(IMAGES, encoding='utf-8')).get('pages', {})
    data = {}
    for code, _, _ in LANGS:
        d = os.path.join(ROOT, 'blog', code)
        noms = sorted(n for n in os.listdir(d) if n.endswith('.html') and n != 'index.html') if os.path.isdir(d) else []
        data[code] = [lire(code, n[:-5], photos) for n in noms]
    par_sujet = {}
    for arts in data.values():
        for a in arts:
            if a['photo']:
                par_sujet.setdefault(a['photo'].get('sujet'), []).append(a)
    connus = {c for c, _, _ in CATS}
    for arts in data.values():
        for a in arts:
            jumeaux = par_sujet.get((a['photo'] or {}).get('sujet'), [])
            for champ in ('cat', 'date'):
                if not a[champ]:
                    a[champ] = next((j[champ] for j in jumeaux if j[champ]), None)
            if a['cat'] not in connus:
                a['cat'] = CAT_DEFAUT
        # plus recent d'abord, puis par titre
        arts.sort(key=lambda a: (a['titre'].lower()))
        arts.sort(key=lambda a: a['date'] or '', reverse=True)
    return data


def date_lisible(iso, lang):
    if not iso:
        return ''
    a, m, j = iso.split('-')
    return '%d %s %s' % (int(j), MOIS[lang][int(m) - 1], a)


def fiche(a):
    code = a['lang']
    couleur, nom = next((c[1], c[2][code]) for c in CATS if c[0] == a['cat'])
    p = a['photo']
    vignette = f'<span class="vignette vide" style="--c:{couleur}"></span>'  # photo pas encore posée
    if p:
        vignette = ('<span class="vignette"><img src="/assets/%s-800.webp?v=%s" alt="%s" width="800" height="450" '
                    'loading="lazy" decoding="async"></span>' % (p['fichier'], p.get('v', 1), H.escape(p.get('alt', ''))))
    date = ('<time datetime="%s">%s</time>' % (a['date'], date_lisible(a['date'], code))) if a['date'] else ''
    return (f'        <a class="fiche" href="/blog/{code}/{a["slug"]}" data-cat="{a["cat"]}">\n'
            f'          {vignette}\n'
            f'          <span class="corps">\n'
            f'            <span class="infos"><span class="badge" style="background:{couleur}">{H.escape(nom)}</span>{date}</span>\n'
            f'            <span class="titre">{H.escape(a["titre"])}</span>\n'
            f'            <span class="resume">{H.escape(a["resume"])}</span>\n'
            f'          </span>\n'
            f'        </a>')


def build(data):
    total = sum(len(v) for v in data.values())
    langs_present = [(code, label, court) for code, label, court in LANGS if data.get(code)]

    # Enumeration des langues pour la meta description, dans la langue de la page.
    names = {'es': 'español', 'val': 'valenciano', 'en': 'inglés', 'fr': 'francés'}
    listed = [names[c] for c, _, _ in langs_present]
    langs_text = (', '.join(listed[:-1]) + ' y ' + listed[-1]) if len(listed) > 1 else listed[0]

    desc = ('Guías prácticas para autónomos, pequeñas y medianas empresas: páginas web, '
            'SEO local, Google Business Profile y marketing digital. '
            f'{total} artículos en {langs_text}.')
    title = 'Blog para autónomos: webs, SEO local y Google Business | WebAutonomos'

    nav = '\n'.join(
        f'    <a href="#{code}" data-lang="{code}" lang="{"ca" if code == "val" else code}">{court} '
        f'<span class="n">{len(data[code])}</span></a>'
        for code, _, court in langs_present)

    panneaux = []
    for code, label, _ in langs_present:
        arts = data[code]
        boutons = [f'        <button type="button" data-cat="tous" aria-pressed="true">{TOUS[code]} '
                   f'<span class="n">{len(arts)}</span></button>']
        for cle, couleur, noms in CATS:
            n = sum(1 for a in arts if a['cat'] == cle)
            if n:
                boutons.append(f'        <button type="button" data-cat="{cle}" aria-pressed="false" '
                               f'style="--c:{couleur}">{H.escape(noms[code])} <span class="n">{n}</span></button>')
        panneaux.append(
            f'    <div class="panneau" id="{code}" data-lang="{code}" lang="{"ca" if code == "val" else code}">\n'
            f'      <p class="ptitre" role="heading" aria-level="2">{label} <span class="cnt">{len(arts)}</span></p>\n'
            f'      <div class="filtres" role="group" aria-label="{FILTRER[code]}" hidden>\n'
            + '\n'.join(boutons) + '\n'
            f'      </div>\n'
            f'      <div class="grille">\n'
            + '\n'.join(fiche(a) for a in arts) + '\n'
            f'      </div>\n'
            f'    </div>')

    return total, f"""<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Index statique du blog. Existe pour que /blog/ reste un asset servi en 200
     apres le passage de not_found_handling a "404-page".
     Genere par _tools/generate_blog_index.py depuis les articles de blog/es,
     blog/val, blog/en et blog/fr. Ne pas editer a la main : relancer le script
     apres chaque publication d'article. -->
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
  main {{ flex:1; max-width:1120px; width:100%; margin:0 auto; padding:56px 5% 72px; }}
  .crumb {{ font-size:0.9rem; color:var(--gray); margin:0 0 20px; }}
  .crumb a {{ color:var(--blue); text-decoration:none; }}
  h1 {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800;
        font-size:clamp(1.8rem,5vw,2.6rem); line-height:1.2; margin:0 0 16px; }}
  .lede {{ font-size:1.1rem; line-height:1.7; color:var(--gray); margin:0 0 32px; max-width:70ch; }}
  figure {{ max-width:780px; }}
  .langues {{ display:flex; flex-wrap:wrap; gap:10px; margin:36px 0 34px; }}
  .langues a {{ display:inline-flex; align-items:center; gap:8px; padding:9px 18px; border-radius:999px;
                border:1px solid var(--border); background:var(--off); color:var(--blue);
                text-decoration:none; font-size:0.95rem; font-weight:600; }}
  .langues a:hover {{ background:var(--white); }}
  .langues a[aria-current="true"] {{ background:var(--blue); border-color:var(--blue); color:var(--white); }}
  .n {{ font-size:0.78rem; font-weight:600; opacity:0.75; }}
  .panneau {{ margin:0 0 48px; scroll-margin-top:20px; }}
  .ptitre {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1.3rem;
             margin:0 0 16px; display:flex; align-items:center; gap:10px; }}
  .js .ptitre {{ position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }}
  .cnt {{ font-family:'DM Sans',sans-serif; font-size:0.8rem; font-weight:600;
          color:var(--white); background:var(--grad); border-radius:999px; padding:2px 10px; }}
  .filtres {{ display:flex; flex-wrap:wrap; justify-content:center; gap:10px; margin:0 0 30px; }}
  .filtres button {{ font:inherit; font-size:0.95rem; font-weight:600; cursor:pointer;
                     padding:9px 18px; border-radius:999px; border:1px solid #e2e8f0;
                     background:var(--white); color:#334155; box-shadow:0 1px 2px rgba(15,32,64,0.06); }}
  .filtres button:hover {{ border-color:var(--c, var(--blue)); color:var(--c, var(--blue)); }}
  .filtres button[aria-pressed="true"] {{ background:var(--c, var(--blue)); border-color:var(--c, var(--blue));
                                          color:var(--white); }}
  .filtres button[aria-pressed="true"] .n {{ opacity:0.9; }}
  .grille {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(270px,1fr)); gap:24px; }}
  .fiche {{ display:flex; flex-direction:column; background:var(--white); border-radius:18px; overflow:hidden;
            text-decoration:none; color:var(--text); border:1px solid #edf2f7;
            box-shadow:0 1px 3px rgba(15,32,64,0.08); transition:box-shadow .2s, transform .2s; }}
  .fiche:hover {{ box-shadow:0 10px 28px rgba(15,32,64,0.14); transform:translateY(-2px); }}
  .fiche[hidden] {{ display:none; }}
  .vignette {{ display:block; aspect-ratio:16/9; background:var(--off); }}
  .vignette img {{ display:block; width:100%; height:100%; object-fit:cover; }}
  .vignette.vide {{ background:linear-gradient(135deg, var(--c) 0%, #1a3a8f 100%); opacity:0.85; }}
  .corps {{ display:flex; flex-direction:column; gap:10px; padding:18px 20px 22px; }}
  .infos {{ display:flex; flex-wrap:wrap; align-items:center; gap:10px; font-size:0.85rem; color:var(--gray); }}
  .badge {{ color:var(--white); font-size:0.78rem; font-weight:600; padding:3px 12px; border-radius:999px; }}
  .titre {{ font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:1.12rem; line-height:1.35; }}
  .fiche:hover .titre {{ color:var(--blue); }}
  .resume {{ font-size:0.95rem; line-height:1.6; color:var(--gray);
             display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }}
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
  @media (max-width:560px) {{
    main {{ padding:40px 16px 56px; }}
    .langues a, .filtres button {{ padding:8px 14px; font-size:0.9rem; }}
    .grille {{ grid-template-columns:1fr; }}
  }}
</style>
</head>
<body>

<main>
  <p class="crumb"><a href="/">Inicio</a> &rsaquo; Blog</p>

  <h1>Blog para autónomos</h1>
  <p class="lede">
    Guías prácticas sobre páginas web, SEO local, Google Business Profile y marketing
    digital para autónomos, pequeñas y medianas empresas. {total} artículos disponibles.
  </p>

  <nav class="langues" aria-label="Idioma de los artículos">
{nav}
  </nav>

{chr(10).join(panneaux)}
</main>

<footer>
  <a class="fl" href="/"><span>&#127760;</span> webautonomos.es</a>
  <div class="flinks">
    <a href="/aviso-legal/">Aviso legal</a>
    <a href="/privacidad/">Privacidad</a>
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

<script>
/* Une langue a la fois (#es, #val, #en, #fr ; espagnol par defaut) et filtres par theme. */
(function () {{
  var doc = document.documentElement;
  doc.className = doc.className.replace('no-js', 'js');
  var panneaux = [].slice.call(document.querySelectorAll('.panneau'));
  var liens = [].slice.call(document.querySelectorAll('.langues a'));
  function filtrer(panneau, cat) {{
    [].forEach.call(panneau.querySelectorAll('.fiche'), function (f) {{
      f.hidden = !(cat === 'tous' || f.getAttribute('data-cat') === cat);
    }});
    [].forEach.call(panneau.querySelectorAll('.filtres button'), function (b) {{
      b.setAttribute('aria-pressed', b.getAttribute('data-cat') === cat ? 'true' : 'false');
    }});
  }}
  function montrer(code) {{
    if (!panneaux.some(function (p) {{ return p.id === code; }})) code = panneaux.length ? panneaux[0].id : '';
    panneaux.forEach(function (p) {{
      p.hidden = p.id !== code;
      p.querySelector('.filtres').hidden = false;
      if (p.id === code) filtrer(p, 'tous');
    }});
    liens.forEach(function (a) {{ a.setAttribute('aria-current', a.getAttribute('data-lang') === code ? 'true' : 'false'); }});
  }}
  liens.forEach(function (a) {{
    a.addEventListener('click', function (e) {{
      e.preventDefault();
      var code = a.getAttribute('data-lang');
      if (history.replaceState) history.replaceState(null, '', '#' + code);
      montrer(code);
    }});
  }});
  document.addEventListener('click', function (e) {{
    var b = e.target.closest ? e.target.closest('.filtres button') : null;
    if (b) filtrer(b.closest('.panneau'), b.getAttribute('data-cat'));
  }});
  window.addEventListener('hashchange', function () {{ montrer(location.hash.slice(1)); }});
  montrer(location.hash.slice(1));
}})();
</script>

</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='verifie sans ecrire')
    args = ap.parse_args()

    data = collect()
    total, page = build(data)

    # --- verification : chaque fiche vise un fichier reellement present, sans .html,
    #     et chaque vignette un fichier d'assets present
    problems = []
    hrefs = re.findall(r'<a class="fiche" href="(/blog/[^"]+)"', page)
    for href in hrefs:
        if href.endswith('.html'):
            problems.append(('extension .html', href))
        rel = href.lstrip('/')
        if not (os.path.isfile(os.path.join(ROOT, rel + '.html'))
                or os.path.isfile(os.path.join(ROOT, rel, 'index.html'))):
            problems.append(('cible inexistante', href))
    if len(hrefs) != total:
        problems.append(('fiches', f'{len(hrefs)} fiches pour {total} articles'))
    for src in re.findall(r'<img src="/assets/([^"?]+)\?', page):
        if not os.path.isfile(os.path.join(ROOT, 'assets', src)):
            problems.append(('vignette absente', src))
    # Fiche incomplete : simple avertissement. Un article qui vient de paraitre n'a pas encore
    # sa photo (le robot photo la pose ensuite) ; bloquer ici ferait echouer la publication.
    incompletes = [(a['rel'], [k for k in ('photo', 'date', 'resume') if not a[k]])
                   for arts in data.values() for a in arts]
    incompletes = [(rel, manque) for rel, manque in incompletes if manque]

    # --- verification : aucun compteur fige hors de ceux qu'on vient de calculer
    counters = [int(n) for n in re.findall(r'<span class="cnt">(\d+)</span>', page)]
    expected = [len(data[c]) for c, _, _ in LANGS if data.get(c)]
    if counters != expected:
        problems.append(('compteurs de section', f'{counters} != {expected}'))
    # Le total doit apparaitre dans le lede, la meta description et og:description.
    if page.count(f'{total} artículos') < 3:
        problems.append(('total', f'"{total} artículos" trouve {page.count(f"{total} artículos")}x, attendu 3'))
    # Aucun autre compteur fige : tout "<n> artículos" doit valoir le total courant.
    stale = {n for n in re.findall(r'(\d+) artículos', page) if int(n) != total}
    if stale:
        problems.append(('compteur fige', 'valeurs parasites : ' + ', '.join(sorted(stale))))
    # La maquette doit pouvoir se poser en fin de page : aucun intertitre <h2>.
    if '<h2' in page:
        problems.append(('intertitre', 'la page ne doit pas contenir de <h2> (placement de la maquette)'))

    for code, _, _ in LANGS:
        cats = {}
        for a in data[code]:
            cats[a['cat']] = cats.get(a['cat'], 0) + 1
        print('  blog/%-4s %3d  %s' % (code, len(data[code]), ', '.join('%s %d' % kv for kv in sorted(cats.items()))))
    print('  %-9s %3d' % ('TOTAL', total))
    for rel, manque in incompletes:
        print('  avertissement : %s sans %s' % (rel, ', '.join(manque)))

    if problems:
        print('\nAnomalies, RIEN ecrit :')
        for kind, detail in problems:
            print('  - %s : %s' % (kind, detail))
        return 1

    if args.check:
        print('\n--check : aucune anomalie, fichier non modifie.')
        return 0

    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(poser_photo(OUT, page))
    print('\nblog/index.html ecrit : %d octets, %d fiches.' % (len(page.encode('utf-8')), total))
    return 0


if __name__ == '__main__':
    sys.exit(main())
