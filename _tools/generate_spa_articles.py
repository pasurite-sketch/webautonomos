#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere un fichier HTML autonome pour chaque article qui n'existe QUE dans les
donnees du SPA (objet `translations` de index.html) et n'a pas encore de
fichier statique sous blog/{lang}/.

Contexte : wrangler.jsonc utilise assets.not_found_handling = "404-page".
Toute URL sans asset renvoie desormais un vrai 404. Les articles qui n'etaient
rendus que cote client par le routeur React disparaitraient donc du site ; ce
script leur donne un fichier reel.

Sortie : blog/{lang}/{slug}.html  (ou blog/{slug}.html pour les slugs herites
sans prefixe de langue, que le routeur sert sous /blog/{slug}).

Chaque page contient : title, meta description, canonical vers sa propre URL,
hreflang, Open Graph, 4 blocs JSON-LD (BlogPosting, BreadcrumbList, FAQPage,
Organization), le corps complet de l'article, la FAQ, un CTA et le pied de
page NAP.

Usage :
    python3 _tools/generate_spa_articles.py            # ecrit les fichiers manquants
    python3 _tools/generate_spa_articles.py --dry-run  # liste sans ecrire
    python3 _tools/generate_spa_articles.py --force    # reecrit meme si le fichier existe
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')
BASE = 'https://webautonomos.es'

# --------------------------------------------------------------------------
# 1. Extraction des donnees
# --------------------------------------------------------------------------

# L'objet `translations` est un litteral JavaScript (cles non quotees), pas du
# JSON : on le fait evaluer par node, qui est deja une dependance du repo
# (wrangler). On recupere du JSON exploitable.
_EXTRACT_JS = r"""
const fs = require('fs');
const s = fs.readFileSync(process.argv[2], 'utf8');
const i = s.indexOf('const translations=');
if (i < 0) { console.error('objet translations introuvable dans index.html'); process.exit(2); }
let depth = 0, k = s.indexOf('{', i);
const start = k;
for (;; k++) {
  const c = s[k];
  if (c === '{') depth++;
  else if (c === '}') { depth--; if (depth === 0) break; }
}
const value = (0, eval)('(' + s.slice(start, k + 1) + ')');
fs.writeFileSync(process.argv[3], JSON.stringify(value));
"""


def load_translations():
    with tempfile.TemporaryDirectory() as tmp:
        js = os.path.join(tmp, 'extract.js')
        out = os.path.join(tmp, 'translations.json')
        with open(js, 'w', encoding='utf-8') as fh:
            fh.write(_EXTRACT_JS)
        try:
            subprocess.run(['node', js, INDEX, out], check=True,
                           capture_output=True, text=True)
        except FileNotFoundError:
            sys.exit("node est requis pour lire l'objet translations de index.html.")
        except subprocess.CalledProcessError as exc:
            sys.exit("echec de l'extraction : %s" % (exc.stderr or exc.stdout))
        with open(out, encoding='utf-8') as fh:
            return json.load(fh)


# --------------------------------------------------------------------------
# 2. Tables de correspondance
# --------------------------------------------------------------------------

# categorie SPA -> (slug de silo, couleur, libelle par langue)
CATEGORIES = {
    'web':            ('paginas-web',        '#3B82F6',
                       {'es': 'Páginas Web', 'val': 'Pàgines Web',
                        'en': 'Websites', 'fr': 'Sites web'}),
    'seo':            ('seo-local',          '#10B981',
                       {'es': 'SEO Local', 'val': 'SEO Local',
                        'en': 'Local SEO', 'fr': 'SEO local'}),
    'gmb':            ('google-my-business', '#F59E0B',
                       {'es': 'Google My Business', 'val': 'Google My Business',
                        'en': 'Google My Business', 'fr': 'Google My Business'}),
    'marketing':      ('marketing-digital',  '#8B5CF6',
                       {'es': 'Marketing Digital', 'val': 'Màrqueting Digital',
                        'en': 'Digital Marketing', 'fr': 'Marketing digital'}),
    'legal':          ('facturacion-legal',  '#64748B',
                       {'es': 'Facturación y Legal', 'val': 'Facturació i Legal',
                        'en': 'Invoicing & Legal', 'fr': 'Facturation et juridique'}),
    'automatizacion': ('automatizacion',     '#0EA5E9',
                       {'es': 'Automatización', 'val': 'Automatització',
                        'en': 'Automation', 'fr': 'Automatisation'}),
}
DEFAULT_CATEGORY = ('paginas-web', '#3B82F6',
                    {'es': 'Blog', 'val': 'Blog', 'en': 'Blog', 'fr': 'Blog'})

HTML_LANG = {'es': 'es', 'val': 'ca', 'en': 'en', 'fr': 'fr'}
OG_LOCALE = {'es': 'es_ES', 'val': 'ca_ES', 'en': 'en_US', 'fr': 'fr_FR'}

# Libelles d'interface
UI = {
    'es': dict(home='Inicio', blog='Blog', back='← Volver al blog',
               toc='📑 Contenido del artículo', faq='Preguntas frecuentes',
               read='min de lectura', cta_title='¿Quieres una web así para tu negocio?',
               cta_text='Páginas web profesionales por 15 €/mes · Sin alta · Sin permanencia',
               cta_btn='Pedir gratis la demo de tu web →', cta_href='/pide-tu-demo', author_desc=
               'Agencia web especializada en autónomos de la Comunidad Valenciana. '
               'Páginas web profesionales desde 15 €/mes, sin permanencia.',
               legal='Aviso legal', privacy='Privacidad', contact='Contacto'),
    'val': dict(home='Inici', blog='Blog', back='← Tornar al blog',
                toc='📑 Contingut de l\'article', faq='Preguntes freqüents',
                read='min de lectura', cta_title='Vols una web així per al teu negoci?',
                cta_text='Pàgines web professionals per 15 €/mes · Sense alta · Sense permanència',
                cta_btn='Demana gratis la demo de la teua web →', cta_href='/pide-tu-demo', author_desc=
                'Agència web especialitzada en autònoms de la Comunitat Valenciana. '
                'Pàgines web professionals des de 15 €/mes, sense permanència.',
                legal='Avís legal', privacy='Privacitat', contact='Contacte'),
    'en': dict(home='Home', blog='Blog', back='← Back to the blog',
               toc='📑 Article contents', faq='Frequently asked questions',
               read='min read', cta_title='Want a website like this for your business?',
               cta_text='Professional websites for €15/month · No setup fee · No commitment',
               cta_btn='Get a free demo of your website →', cta_href='/get-your-demo', author_desc=
               'Web agency specialising in freelancers across the Valencian Community. '
               'Professional websites from €15/month, no commitment.',
               legal='Legal notice', privacy='Privacy', contact='Contact'),
    'fr': dict(home='Accueil', blog='Blog', back='← Retour au blog',
               toc='📑 Sommaire de l\'article', faq='Questions fréquentes',
               read='min de lecture', cta_title='Vous voulez un site comme celui-ci ?',
               cta_text='Sites web professionnels pour 15 €/mois · Sans frais d\'ouverture · Sans engagement',
               cta_btn='Demander gratuitement la démo de votre site →', cta_href='/demandez-votre-demo', author_desc=
               'Agence web spécialisée dans les indépendants de la Communauté valencienne. '
               'Sites web professionnels à partir de 15 €/mois, sans engagement.',
               legal='Mentions légales', privacy='Confidentialité', contact='Contact'),
}

# Tous les libelles de mois rencontres dans les 4 blocs de langue.
MONTHS = {
    'ene': 1, 'gen': 1, 'jan': 1, 'enero': 1, 'gener': 1, 'january': 1, 'janvier': 1,
    'feb': 2, 'febrero': 2, 'febrer': 2, 'february': 2, 'fev': 2, 'février': 2, 'fevrier': 2,
    'mar': 3, 'marzo': 3, 'març': 3, 'march': 3, 'mars': 3,
    'abr': 4, 'abril': 4, 'apr': 4, 'april': 4, 'avr': 4, 'avril': 4,
    'may': 5, 'mayo': 5, 'maig': 5, 'mai': 5,
    'jun': 6, 'junio': 6, 'juny': 6, 'june': 6, 'juin': 6,
    'jul': 7, 'julio': 7, 'juliol': 7, 'july': 7, 'juillet': 7,
    'ago': 8, 'agosto': 8, 'agost': 8, 'aug': 8, 'august': 8, 'aou': 8, 'août': 8, 'aout': 8,
    'sep': 9, 'sept': 9, 'septiembre': 9, 'setembre': 9, 'september': 9, 'septembre': 9,
    'oct': 10, 'octubre': 10, 'october': 10, 'octobre': 10,
    'nov': 11, 'noviembre': 11, 'novembre': 11, 'november': 11,
    'dic': 12, 'des': 12, 'dec': 12, 'diciembre': 12, 'desembre': 12,
    'december': 12, 'déc': 12, 'décembre': 12, 'decembre': 12,
}

FALLBACK_DATE = '2026-01-01'


def iso_date(raw):
    """'03 Agosto 2026', '15 Ene 2026', 'Jan 15, 2026' -> '2026-08-03'."""
    if not raw:
        return FALLBACK_DATE
    tokens = re.findall(r'[0-9]+|[^\W\d_]+', raw, re.UNICODE)
    day = month = year = None
    for tok in tokens:
        low = tok.lower()
        if low in MONTHS and month is None:
            month = MONTHS[low]
        elif tok.isdigit():
            n = int(tok)
            if n >= 1000 and year is None:
                year = n
            elif 1 <= n <= 31 and day is None:
                day = n
    if not (day and month and year):
        return FALLBACK_DATE
    return '%04d-%02d-%02d' % (year, month, day)


# --------------------------------------------------------------------------
# 3. Chemins et slugs
# --------------------------------------------------------------------------

def split_slug(slug):
    """'es/foo' -> ('es', 'foo') ; 'foo' -> (None, 'foo') (slug herite)."""
    m = re.match(r'^(es|val|en|fr)/(.+)$', slug)
    return (m.group(1), m.group(2)) if m else (None, slug)


def target_path(slug):
    """Chemin disque du fichier a produire, relatif a la racine du repo."""
    prefix, base = split_slug(slug)
    return os.path.join('blog', prefix, base + '.html') if prefix else \
        os.path.join('blog', base + '.html')


def public_url(slug):
    return '%s/blog/%s' % (BASE, slug)


def has_asset(slug):
    """Un asset sert-il deja cette URL ? (fichier .html ou dossier/index.html)"""
    rel = target_path(slug)
    return os.path.isfile(os.path.join(ROOT, rel)) or \
        os.path.isfile(os.path.join(ROOT, rel[:-5], 'index.html'))


# --------------------------------------------------------------------------
# 4. Rendu HTML
# --------------------------------------------------------------------------

E = lambda s: html.escape(s or '', quote=True)
J = lambda s: json.dumps(s or '', ensure_ascii=False)


# --------------------------------------------------------------------------
# Mesure d'audience
# --------------------------------------------------------------------------
#
# Repris a l'identique des landings (fontaneros/index.html) : meme identifiant
# GA4, meme extrait Clarity, meme ordre, meme place — tout a la fin du <head>,
# apres le JSON-LD. Le loader gtag reste en `defer`.
#
# Ces blocs vivent dans une constante et non dans le gabarit format() : le
# JavaScript de Clarity contient des accolades, qui devraient etre doublees
# dans une chaine de format. Une constante evite ce piege.

TRACKING = """<!-- Google Analytics GA4 -->
<script defer src="https://www.googletagmanager.com/gtag/js?id=G-MT6S7CH7N9"></script>
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
</script>"""

NAV = """    <nav style="background:white; box-shadow:0 1px 3px rgba(0,0,0,0.1); position:sticky; top:0; z-index:50;">
        <div style="max-width:1200px; margin:0 auto; padding:0 24px; height:64px; display:flex; align-items:center; justify-content:space-between;">
            <a href="{base}" style="display:flex; align-items:center; gap:8px; text-decoration:none;">
                <div style="width:36px; height:36px; background:linear-gradient(135deg,#2563eb,#16a34a); border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:16px;">W</div>
                <span style="font-weight:700; font-size:18px;"><span style="color:#2563eb;">web</span><span style="color:#16a34a;">autonomos</span><span style="color:#111;">.es</span></span>
            </a>
            <a href="{base}/blog/" style="color:#374151; text-decoration:none; font-size:14px; font-weight:500;">{blog}</a>
        </div>
    </nav>
"""

FOOTER = """    <footer style="background:linear-gradient(135deg,#1a3a8f 0%,#1a7a5a 50%,#22c55e 100%); padding:24px 6%; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; margin-top:48px;">
        <a href="{base}" style="font-weight:800; font-size:1rem; color:rgba(255,255,255,0.85); text-decoration:none;">&#127760; webautonomos.es</a>
        <div style="display:flex; gap:20px; flex-wrap:wrap;">
            <a href="{base}/aviso-legal" style="color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem;">{legal}</a>
            <a href="{base}/privacidad" style="color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem;">{privacy}</a>
            <a href="{base}/contacto" style="color:rgba(255,255,255,0.8); text-decoration:none; font-size:0.9rem;">{contact}</a>
        </div>
        <address style="flex-basis:100%; order:3; margin-top:4px; padding-top:16px; border-top:1px solid rgba(255,255,255,0.12); font-style:normal; font-size:0.78rem; line-height:1.7; color:rgba(255,255,255,0.55); display:flex; flex-direction:column; gap:1px;">
            <strong>WebAutonomos</strong>
            <span>Calle Pintor Josep Segrelles, 26</span>
            <span>46870 Ontinyent, Valencia</span>
            <a href="tel:+34961877356" style="color:rgba(255,255,255,0.55); text-decoration:none;">+34 961 877 356</a>
            <a href="mailto:info@webautonomos.es" style="color:rgba(255,255,255,0.55); text-decoration:none;">info@webautonomos.es</a>
        </address>
    </footer>
"""


def render(article, lang, alternates):
    slug = article['slug']
    url = public_url(slug)

    # Les 6 slugs herites (sans prefixe de langue) sont servis par le routeur sous
    # /blog/{slug} mais dupliquent /blog/es/{slug}, qui est la version de reference.
    # Attention : ces slugs n'ont PAS de jumeau "es/..." dans les donnees SPA — la
    # version espagnole n'existe que sous forme de fichier redige a la main. Le test
    # porte donc sur le disque, pas sur `alternates`.
    prefix, base = split_slug(slug)
    canonical_url = url
    es_twin = 'es/' + base
    if prefix is None and has_asset(es_twin):
        canonical_url = public_url(es_twin)
        # Le hreflang espagnol doit lui aussi pointer vers la version de reference.
        alternates = dict(alternates, es=es_twin)

    ui = UI[lang]
    cat_slug, cat_color, cat_labels = CATEGORIES.get(article.get('category'), DEFAULT_CATEGORY)
    cat_label = cat_labels.get(lang, cat_labels['es'])
    title = article.get('title') or slug
    seo_title = article.get('seoTitle') or (title + ' | WebAutonomos')
    desc = article.get('metaDescription') or article.get('excerpt') or ''
    published = iso_date(article.get('date'))
    read = article.get('readTime') or 8

    blocks = article.get('content') or []
    headings = [b for b in blocks if b.get('type') == 'heading']

    # ---- rendu d'un bloc table (ajoute le 05/09/2026)
    # Bloc attendu : {"type": "table", "caption": "...", "headers": [...],
    #                 "rows": [[...], [...]], "note": "..."}
    # La premiere colonne devient un <th scope="row"> : c'est ce qui permet a
    # Google et aux modeles de rattacher chaque valeur a son libelle.
    def render_table(b):
        heads = b.get('headers') or []
        rows = b.get('rows') or []
        cap = b.get('caption') or ''
        note = b.get('note') or ''
        # Colonne mise en avant : "highlight" (index) si present, sinon celle
        # dont l'en-tete contient WebAutonomos, sinon aucune.
        hl = b.get('highlight')
        if hl is None:
            hl = next((k for k, h in enumerate(heads) if 'webautonomos' in h.lower()), None)
        badge = {'es': 'Nuestra oferta', 'val': 'La nostra oferta',
                 'en': 'Our offer', 'fr': 'Notre offre'}.get(lang, '')
        last = len(rows) - 1

        out = ['            <figure class="my-10">']
        if cap:
            out.append('                <figcaption class="flex items-center gap-3 mb-4">'
                       '<span class="inline-block w-1.5 h-6 rounded-full gradient-wa"></span>'
                       '<span class="text-lg font-bold text-gray-900">%s</span></figcaption>'
                       % E(cap))
        out.append('                <div class="overflow-x-auto rounded-2xl ring-1 ring-gray-200 '
                   'shadow-sm bg-white">')
        out.append('                <table class="w-full min-w-[640px] text-sm border-separate '
                   'border-spacing-0">')
        if cap:
            out.append('                    <caption class="sr-only">%s</caption>' % E(cap))
        if heads:
            out.append('                    <thead><tr>')
            for k, h in enumerate(heads):
                if k == 0:
                    cls = 'sticky left-0 z-10 bg-gray-50 text-left text-gray-900'
                elif k == hl:
                    cls = 'bg-blue-50 text-center text-blue-700'
                else:
                    cls = 'bg-gray-50 text-center text-gray-900'
                inner = E(h)
                if k == hl and badge:
                    inner = ('<span class="block text-[10px] font-semibold uppercase '
                             'tracking-wider text-blue-600 mb-1">%s</span>%s' % (E(badge), inner))
                out.append('                        <th scope="col" class="%s px-4 py-4 font-semibold '
                           'border-b border-gray-200 align-bottom">%s</th>' % (cls, inner))
            out.append('                    </tr></thead>')
        out.append('                    <tbody>')
        for ri, r in enumerate(rows):
            total = (ri == last and last > 0)
            out.append('                        <tr class="%s">'
                       % ('bg-gray-50/70' if total else 'hover:bg-gray-50/60'))
            for k, c in enumerate(r):
                border = 'border-t-2 border-gray-200' if total else 'border-b border-gray-100'
                if k == 0:
                    tag, close = 'th scope="row"', 'th'
                    cls = ('sticky left-0 z-10 text-left ' +
                           ('bg-gray-50 font-bold text-gray-900' if total
                            else 'bg-white font-medium text-gray-800'))
                elif k == hl:
                    tag = close = 'td'
                    cls = 'bg-blue-50/60 text-center ' + (
                        'font-bold text-blue-700 text-base' if total
                        else 'font-medium text-gray-900')
                else:
                    tag = close = 'td'
                    cls = 'text-center ' + ('font-semibold text-gray-900' if total
                                            else 'text-gray-700')
                out.append('                            <%s class="%s %s px-4 py-3.5 leading-snug">'
                           '%s</%s>' % (tag, cls, border, E(c), close))
            out.append('                        </tr>')
        out.extend(['                    </tbody>', '                </table>',
                    '                </div>'])
        if note:
            out.append('                <p class="mt-3 text-xs text-gray-500 leading-relaxed">%s</p>'
                       % E(note))
        out.append('            </figure>')
        return chr(10).join(out)

    # ---- corps + sommaire
    toc, body, n = [], [], 0
    for b in blocks:
        kind, text = b.get('type'), b.get('text') or ''
        if kind == 'heading':
            n += 1
            toc.append('                    <li><a href="#seccion-%d" class="toc-link">%s</a></li>'
                       % (n, E(text)))
            body.append('            <h2 id="seccion-%d" class="text-2xl font-bold text-gray-900 mt-10 mb-4">%s</h2>'
                        % (n, E(text)))
        elif kind == 'intro':
            body.append('            <p class="text-lg text-gray-700 leading-relaxed mb-6">%s</p>' % E(text))
        elif kind == 'conclusion':
            body.append('            <p class="text-lg text-gray-800 leading-relaxed mt-8 mb-6 font-medium">%s</p>' % E(text))
        elif kind == 'table':
            body.append(render_table(b))
        else:
            body.append('            <p class="text-gray-700 leading-relaxed mb-4">%s</p>' % E(text))
    toc.append('                    <li><a href="#faq" class="toc-link">%s</a></li>' % E(ui['faq']))

    # ---- FAQ
    faq = article.get('faq') or []
    faq_html = []
    for item in faq:
        faq_html.append(
            '                <details class="bg-white rounded-xl shadow-sm overflow-hidden">\n'
            '                    <summary class="px-6 py-4 font-semibold text-gray-800 cursor-pointer hover:bg-gray-50 transition">%s</summary>\n'
            '                    <div class="px-6 pb-4 text-gray-600 leading-relaxed">%s</div>\n'
            '                </details>' % (E(item.get('q')), E(item.get('a'))))

    # ---- hreflang
    hreflang = []
    for code, alt_slug in alternates.items():
        tag = {'es': 'es', 'val': 'ca-ES', 'en': 'en', 'fr': 'fr'}[code]
        hreflang.append('    <link rel="alternate" hreflang="%s" href="%s">' % (tag, public_url(alt_slug)))
    if 'es' in alternates:
        hreflang.append('    <link rel="alternate" hreflang="x-default" href="%s">' % public_url(alternates['es']))

    # ---- schemas JSON-LD
    blogposting = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": title, "description": desc,
        "author": {"@type": "Organization", "name": "WebAutonomos", "url": BASE},
        "publisher": {"@type": "Organization", "name": "WebAutonomos",
                      "url": BASE,
                      "logo": {"@type": "ImageObject", "url": BASE + "/logo.png"}},
        "datePublished": published + "T08:00:00+01:00",
        # Un article refondu doit annoncer sa vraie date de revision : sans le
        # champ "updated", dateModified restait colle a datePublished et aucun
        # signal de fraicheur ne partait vers Google.
        "dateModified": iso_date(article.get('updated') or article.get('date'))
                        + "T08:00:00+01:00",
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "articleSection": cat_label,
        "inLanguage": HTML_LANG[lang],
        "wordCount": sum(len((b.get('text') or '').split()) for b in blocks),
        "keywords": ", ".join(article.get('keywords') or []),
    }
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui['home'], "item": BASE},
            {"@type": "ListItem", "position": 2, "name": ui['blog'], "item": BASE + "/blog"},
            {"@type": "ListItem", "position": 3, "name": cat_label,
             "item": "%s/blog?categoria=%s" % (BASE, cat_slug)},
            {"@type": "ListItem", "position": 4, "name": title},
        ],
    }
    faqpage = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": i.get('q'),
                        "acceptedAnswer": {"@type": "Answer", "text": i.get('a')}}
                       for i in faq],
    }
    organization = {
        "@context": "https://schema.org", "@type": "Organization",
        "name": "WebAutonomos", "url": BASE, "logo": BASE + "/logo.png",
        "email": "info@webautonomos.es", "telephone": "+34961877356",
        "address": {"@type": "PostalAddress",
                    "streetAddress": "Calle Pintor Josep Segrelles, 26",
                    "postalCode": "46870", "addressLocality": "Ontinyent",
                    "addressRegion": "Valencia", "addressCountry": "ES"},
        "areaServed": {"@type": "AdministrativeArea", "name": "Comunidad Valenciana"},
    }
    schemas = [blogposting, breadcrumb, organization]
    if faq:
        schemas.insert(2, faqpage)
    schema_html = "\n".join(
        '    <script type="application/ld+json">\n%s\n    </script>'
        % json.dumps(s, ensure_ascii=False, indent=8) for s in schemas)

    faq_section = ''
    if faq_html:
        faq_section = (
            '\n            <section id="faq" class="mt-12">\n'
            '                <h2 class="text-2xl font-bold text-gray-900 mb-6">%s</h2>\n'
            '                <div class="space-y-3">\n%s\n                </div>\n'
            '            </section>\n' % (E(ui['faq']), "\n".join(faq_html)))

    return """<!DOCTYPE html>
<html lang="{htmllang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{seo_title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="author" content="WebAutonomos">

    <link rel="canonical" href="{canonical_url}">
{hreflang}

    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{seo_title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:site_name" content="WebAutonomos">
    <meta property="og:locale" content="{oglocale}">
    <meta property="article:published_time" content="{published}T08:00:00+01:00">
    <meta property="article:modified_time" content="{published}T08:00:00+01:00">
    <meta property="article:section" content="{cat_label}">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{seo_title}">
    <meta name="twitter:description" content="{desc}">

    <link rel="icon" href="{base}/favicon.ico" type="image/x-icon">
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html {{ scroll-behavior:smooth; }}
        .toc-link {{ color:#4b5563; text-decoration:none; }}
        .toc-link:hover {{ color:#6D28D9; }}
        .prose-article p {{ line-height:1.8; }}
        .gradient-wa {{ background:linear-gradient(135deg,#2563eb,#16a34a); }}
    </style>

{schemas}
{tracking}
</head>
<body class="bg-gray-50">

{nav}
    <article class="max-w-3xl mx-auto px-4 py-8 prose-article">

        <nav class="text-sm text-gray-400 mb-6" aria-label="Breadcrumb">
            <a href="{base}" class="hover:text-purple-600 transition">{home}</a>
            <span class="mx-1">&rsaquo;</span>
            <a href="{base}/blog/" class="hover:text-purple-600 transition">{blog}</a>
            <span class="mx-1">&rsaquo;</span>
            <span>{cat_label}</span>
        </nav>

        <header class="mb-8">
            <span style="background:{cat_color}; color:white; padding:4px 14px; border-radius:999px; font-size:13px; font-weight:600;">{cat_label}</span>
            <p class="text-sm text-gray-500 mt-4 mb-3">
                <time datetime="{published}">{date_raw}</time> &middot; {read} {read_label}
            </p>
            <h1 class="text-3xl md:text-4xl font-bold text-gray-900 leading-tight">{title}</h1>
        </header>

        <div class="bg-white rounded-2xl shadow-sm p-6 mb-10" style="border-left:4px solid {cat_color};">
            <p class="font-bold text-gray-900 mb-3">{toc_label}</p>
            <ol class="list-decimal list-inside space-y-1 text-sm">
{toc}
            </ol>
        </div>

        <div class="article-body">
{body}
        </div>
{faq_section}
        <div class="gradient-wa rounded-2xl p-8 text-center text-white mt-12">
            <h2 class="text-2xl font-bold mb-3">{cta_title}</h2>
            <p class="mb-6 opacity-90">{cta_text}</p>
            <a href="{base}{cta_href}" style="background:white; color:#2563eb; padding:14px 30px; border-radius:999px; font-weight:600; text-decoration:none; display:inline-block;">{cta_btn}</a>
        </div>

        <div class="flex items-center gap-4 mt-12 bg-white rounded-2xl p-6 shadow-sm">
            <div class="w-16 h-16 gradient-wa rounded-full flex items-center justify-center text-white text-2xl font-bold flex-shrink-0">W</div>
            <div>
                <p class="font-bold text-gray-900">WebAutonomos</p>
                <p class="text-sm text-gray-600">{author_desc}</p>
            </div>
        </div>

        <p class="mt-10">
            <a href="{base}/blog/" style="color:#2563eb; text-decoration:none; font-weight:500;">{back}</a>
        </p>

    </article>

{footer}
</body>
</html>
""".format(
        htmllang=HTML_LANG[lang], seo_title=E(seo_title), desc=E(desc), url=url,
        canonical_url=canonical_url,
        hreflang="\n".join(hreflang), oglocale=OG_LOCALE[lang], published=published,
        cat_label=E(cat_label), cat_color=cat_color, base=BASE, schemas=schema_html, tracking=TRACKING,
        nav=NAV.format(base=BASE, blog=E(ui['blog'])),
        home=E(ui['home']), blog=E(ui['blog']), date_raw=E(article.get('date') or published),
        read=read, read_label=E(ui['read']), title=E(title),
        toc_label=E(ui['toc']), toc="\n".join(toc), body="\n".join(body),
        faq_section=faq_section, cta_title=E(ui['cta_title']), cta_text=E(ui['cta_text']),
        cta_btn=E(ui['cta_btn']), cta_href=ui.get('cta_href', '/pide-tu-demo'),
        author_desc=E(ui['author_desc']), back=E(ui['back']),
        footer=FOOTER.format(base=BASE, legal=E(ui['legal']),
                             privacy=E(ui['privacy']), contact=E(ui['contact'])),
    )


# --------------------------------------------------------------------------
# 5. Point d'entree
# --------------------------------------------------------------------------


def alternates_disque(connus):
    """Complete les alternates avec les fichiers presents mais absents des donnees.

    On lit les hreflang declares par une variante connue et on retient ceux dont
    le fichier existe reellement. Rien n'est invente : une declaration sans
    fichier sur le disque est ignoree.
    """
    trouves = {}
    for sl in connus.values():
        chemin = os.path.join(ROOT, 'blog', sl + '.html')
        if not os.path.exists(chemin):
            continue
        with open(chemin, encoding='utf-8', errors='replace') as fh:
            html = fh.read()
        for balise in re.findall(r'<link[^>]+rel="alternate"[^>]*>', html):
            tag = re.search(r'hreflang="([^"]+)"', balise)
            href = re.search(r'href="[^"]*?/blog/(es|val|en|fr)/([^"?#]+)"', balise)
            if not tag or not href or tag.group(1) == 'x-default':
                continue
            lang2, slug2 = href.group(1), href.group(2)
            if lang2 in connus or lang2 in trouves:
                continue
            if os.path.exists(os.path.join(ROOT, 'blog', lang2, slug2 + '.html')):
                trouves[lang2] = '%s/%s' % (lang2, slug2)
    return trouves

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='liste sans ecrire')
    ap.add_argument('--force', action='store_true', help='reecrit meme si le fichier existe')
    ap.add_argument('--slug', action='append', metavar='BASE',
                    help='limite le traitement aux articles dont le slug de base '
                         'correspond (repetable). Ex : --slug cuanto-cuesta-pagina-'
                         'web-autonomos-espana. Les quatre langues du groupe sont '
                         'traitees ensemble : leurs hreflang doivent rester coherents.')
    args = ap.parse_args()

    translations = load_translations()

    # Index global slug -> (lang, article), pour calculer les hreflang.
    by_slug, by_base, by_id = {}, {}, {}
    for lang, block in translations.items():
        for art in (block.get('blog') or {}).get('articles') or []:
            slug = art['slug']
            by_slug[slug] = (lang, art)
            prefix, base = split_slug(slug)
            # Un slug herite ("foo") et son equivalent prefixe ("es/foo") vivent
            # dans le meme bloc de langue et se disputent la cle 'es'. La version
            # prefixee est la reference : elle gagne toujours, sinon le canonical
            # croise pointerait la page vers elle-meme.
            variants = by_base.setdefault(base, {})
            key = prefix or lang
            if key not in variants or prefix is not None:
                variants[key] = slug
            # Appariement par identifiant d'article (05/09/2026). Les slugs sont
            # localises depuis la migration EN/VAL/FR : "cuanto-cuesta-..." en
            # espagnol devient "how-much-does-a-website-cost-..." en anglais, et
            # l'appariement par slug de base echoue. L'id, lui, est commun aux
            # quatre langues. C'est la meme logique que link_by_spa_id() dans
            # generate_sitemap.py, qui documentait le defaut sans le corriger ici.
            if art.get('id') is not None:
                by_id.setdefault(art['id'], {})[key] = slug

    # --slug : on filtre sur le slug de BASE, pas sur le slug complet, pour que
    # les quatre variantes linguistiques soient regenerees ensemble. Regenerer
    # l'espagnol seul laisserait les trois autres pointer un hreflang perime.
    # Les traductions portent des slugs de base differents de l'espagnol
    # ("how-much-does-a-website-cost-for-freelancers" pour "cuanto-cuesta-...").
    # On resout donc chaque --slug vers son groupe linguistique via by_base, puis
    # on retient tous les slugs complets du groupe : les quatre langues sont
    # regenerees ensemble et leurs hreflang restent coherents.
    wanted = set()
    if args.slug:
        connus = {split_slug(sl)[1] for sl in by_slug}
        inconnus = set(args.slug) - connus
        if inconnus:
            raise SystemExit('slug inconnu : %s' % ', '.join(sorted(inconnus)))
        for base in args.slug:
            for sl, (l_, a_) in by_slug.items():
                if split_slug(sl)[1] == base:
                    wanted.update((by_id.get(a_.get('id')) or {l_: sl}).values())

    written, skipped, failed = {}, 0, []
    for slug, (lang, art) in sorted(by_slug.items()):
        if wanted and slug not in wanted:
            continue
        if has_asset(slug) and not args.force:
            skipped += 1
            continue
        _, base = split_slug(slug)
        alternates = dict(by_id.get(art.get('id')) or by_base.get(base, {}))
        # 44 articles francais existent sur le disque sans figurer dans les
        # donnees du SPA : produits par un gabarit anterieur, jamais reintegres.
        # Sans ce complement, chaque page du groupe perdait son hreflang "fr" a
        # la regeneration. Meme approche que link_by_hreflang() dans
        # generate_sitemap.py : le disque fait foi quand les donnees sont muettes.
        alternates.update(alternates_disque(alternates))
        try:
            page = render(art, lang, alternates)
        except Exception as exc:                     # noqa: BLE001
            failed.append((slug, repr(exc)))
            continue
        dest = os.path.join(ROOT, target_path(slug))
        if not args.dry_run:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'w', encoding='utf-8') as fh:
                fh.write(page)
        written.setdefault(lang, []).append(target_path(slug))

    verb = 'a ecrire' if args.dry_run else 'ecrits'
    print('Fichiers %s, par langue :' % verb)
    for lang in ('es', 'val', 'en', 'fr'):
        files = written.get(lang, [])
        if files:
            print('  %-4s %3d' % (lang, len(files)))
    print('  %-4s %3d' % ('TOTAL', sum(len(v) for v in written.values())))
    print('Deja presents, ignores : %d' % skipped)
    if failed:
        print('\nEchecs (%d) :' % len(failed))
        for slug, err in failed:
            print('  %s -> %s' % (slug, err))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
