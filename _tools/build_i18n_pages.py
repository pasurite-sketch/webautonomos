# -*- coding: utf-8 -*-
"""Versions française et anglaise, à leur propre adresse, des pages
/diagnostico-automatizacion/ et /visibilidad-ia/ (plan SEO FR-EN, phase 1).

Pourquoi : ces deux pages affichaient le français et l'anglais via ?lang=fr et
?lang=en, sur la même adresse que l'espagnol, avec un canonical vers la version
espagnole. Pour Google, il n'existait donc ni diagnostic ni page « Visibilité
IA » en français ou en anglais.

Le script :
  1. génère, depuis la page espagnole (la seule qu'on modifie à la main) :
       /fr/diagnostic-automatisation/   /en/automation-diagnostic/
       /fr/visibilite-ia/               /en/ai-visibility/
     avec, pour chaque copie : lang, title, meta description, Open Graph,
     canonical vers elle-même, textes de la langue écrits dans le HTML
     (lisibles sans JavaScript), JSON-LD dans la langue (FAQ comprise), liens
     de navigation et messages WhatsApp dans la langue ;
  2. la première fois seulement, modifie les deux pages espagnoles :
     hreflang en/fr vers les nouvelles adresses ; ?lang=fr et ?lang=en y
     renvoient désormais (gclid et paramètres Ads conservés) ; le menu des
     langues y mène ; point documenté dans « MODIFICATIONS LOCALES » ;
  3. remplace dans tout le site les liens …?lang=fr / …?lang=en de ces deux
     pages par les nouvelles adresses (accueils /fr/ /en/, articles, pages,
     générateurs) ;
  4. apprend à generate_sitemap.py à lister fr/*/index.html et en/*/index.html.

Le valencien (?lang=ca) ne change pas.

À relancer après chaque modification des pages espagnoles :
    python3 _tools/build_i18n_pages.py            (puis generate_sitemap.py)
    python3 _tools/build_i18n_pages.py --check    (contrôle sans écrire)
Sauvegarde : ~/webautonomos-work/backups/i18n_pages_<date>/ avant écriture.
"""
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://webautonomos.es'
LANGS = ('fr', 'en')

DIAG = {'es': '/diagnostico-automatizacion/', 'fr': '/fr/diagnostic-automatisation/',
        'en': '/en/automation-diagnostic/'}
VIS = {'es': '/visibilidad-ia/', 'fr': '/fr/visibilite-ia/', 'en': '/en/ai-visibility/'}

# Liens de navigation vers le reste du site (balises <a> seulement)
NAV = {
    'fr': [('https://webautonomos.es', BASE + '/fr/'),
           ('https://webautonomos.es/#que-incluye', BASE + '/fr/#inclus'),
           ('https://webautonomos.es/#precios', BASE + '/fr/tarifs'),
           ('https://webautonomos.es/#como-funciona', BASE + '/fr/#etapes'),
           ('https://webautonomos.es/#marketing', BASE + '/fr/#services'),
           ('https://webautonomos.es/#preguntas', BASE + '/fr/questions'),
           ('https://webautonomos.es/blog/', BASE + '/blog/#fr'),
           ('https://webautonomos.es/#contacto', BASE + '/demandez-votre-demo#pide-demo')],
    'en': [('https://webautonomos.es', BASE + '/en/'),
           ('https://webautonomos.es/#que-incluye', BASE + '/en/#included'),
           ('https://webautonomos.es/#precios', BASE + '/en/pricing'),
           ('https://webautonomos.es/#como-funciona', BASE + '/en/how'),
           ('https://webautonomos.es/#marketing', BASE + '/en/#services'),
           ('https://webautonomos.es/#preguntas', BASE + '/en/faq'),
           ('https://webautonomos.es/blog/', BASE + '/blog/#en'),
           ('https://webautonomos.es/#contacto', BASE + '/en/contact')],
}


def wa(txt):
    return re.sub(r'[^A-Za-z0-9]', lambda m: ''.join('%%%02X' % b for b in m.group(0).encode()), txt)


PAGES = [
    dict(
        nom='diagnostic', src='diagnostico-automatizacion/index.html', urls=DIAG,
        croise=('/visibilidad-ia/', VIS), ld_id='ld-graph',
        meta={
            'fr': dict(title="Automatisation des processus : calculez si c'est rentable",
                       desc="Calculez gratuitement ce que vous coûtent vos tâches répétitives et s'il est rentable de les automatiser. Prix ferme, devis sous 48 h. 4 questions, 2 minutes.",
                       og_title="Automatisation des processus pour indépendants et PME : calculez si c'est rentable",
                       og_desc="Calculez gratuitement ce que vous coûtent chaque année vos tâches administratives et s'il vaut la peine de les automatiser.",
                       tw_desc="Diagnostic d'automatisation gratuit. Sans inscription.",
                       locale='fr_FR', home='Accueil', crumb="Diagnostic d'automatisation",
                       app_desc="Outil gratuit qui calcule le coût annuel d'une tâche administrative et détermine s'il vaut la peine de l'automatiser, avec quelle technologie minimale et en combien de mois l'investissement est amorti.",
                       browser='Nécessite JavaScript', service_type="Conseil et développement d'automatisations",
                       catalog="Services d'automatisation",
                       offers=[("Diagnostic d'automatisation", "Calcul du coût annuel d'une tâche et de son potentiel d'automatisation."),
                               ("Développement d'une automatisation sur mesure", "Conception, développement, mise en production et maintenance.")],
                       area=['Spain', 'France']),
            'en': dict(title="Process automation for freelancers in Spain: free calculator",
                       desc="Work out for free what your repetitive tasks cost you and whether automating them pays off. Fixed price, quote within 48 hours. 4 questions, 2 minutes.",
                       og_title="Process automation for freelancers and small businesses: does it pay off?",
                       og_desc="Work out for free what your admin tasks cost you each year and whether they are worth automating.",
                       tw_desc="Free automation diagnostic. No sign-up needed.",
                       locale='en_GB', home='Home', crumb='Automation diagnostic',
                       app_desc="Free tool that calculates the annual cost of an admin task and whether automating it pays off, with the minimum technology needed and the payback period in months.",
                       browser='Requires JavaScript', service_type='Automation consulting and development',
                       catalog='Automation services',
                       offers=[('Automation diagnostic', "Annual cost of a task and its automation potential."),
                               ('Custom automation development', 'Design, development, deployment and maintenance.')],
                       area=['Spain']),
        },
        wa={'Hola%2C%20he%20hecho%20el%20diagn%C3%B3stico%20de%20automatizaci%C3%B3n':
                {'fr': wa("Bonjour, j'ai fait le diagnostic d'automatisation"),
                 'en': wa("Hello, I've done the automation diagnostic")},
            'Hola%2C%20me%20interesa%20el%20diagn%C3%B3stico%20de%20automatizaci%C3%B3n':
                {'fr': wa("Bonjour, le diagnostic d'automatisation m'intéresse"),
                 'en': wa("Hello, I'm interested in the automation diagnostic")}},
        point='10', ancre_comm='\n  Vérifié : 0px de débordement de 1300',
    ),
    dict(
        nom='visibilité IA', src='visibilidad-ia/index.html', urls=VIS,
        croise=('/diagnostico-automatizacion/', DIAG), ld_id='faq-schema',
        meta={
            'fr': dict(og_title="ChatGPT vous recommande-t-il quand on cherche votre métier dans votre ville ?",
                       og_desc="Vos clients interrogent déjà l'IA plutôt que Google. Nous vous disons gratuitement si c'est vous qui apparaissez, ou votre concurrent.",
                       locale='fr_FR'),
            'en': dict(og_title="Does ChatGPT recommend you when someone looks for your trade in your city?",
                       og_desc="Your customers already ask AI instead of Google. We tell you for free whether it's you who shows up, or your competitor.",
                       locale='en_GB'),
        },
        wa={'Hola%2C%20quiero%20comprobar%20si%20la%20IA%20recomienda%20mi%20negocio':
                {'fr': wa("Bonjour, je veux vérifier si l'IA recommande mon activité"),
                 'en': wa("Hello, I'd like to check whether AI recommends my business")}},
        point='7', ancre_comm='\n  Vérifié : 0px de débordement de barre',
    ),
]

VAR_LANG = 'var lang = (new URLSearchParams(location.search).get("lang") || "es").toLowerCase();'


def snippet(urls):
    return ('/* Adresses par langue (build_i18n_pages.py). Une langue qui a sa propre\n'
            '   adresse s\'y affiche : ?lang=fr et ?lang=en y renvoient, en gardant les\n'
            '   autres paramètres (gclid, utm) ; le menu des langues y mène. Une langue\n'
            '   sans adresse propre (ca) s\'affiche sur la page espagnole en ?lang=. */\n'
            'var PAGE_LANG = "es";\n'
            'var PAGE_URLS = %s;\n'
            'function cibleLangue(l){\n'
            '  var u = PAGE_URLS[l], q = new URLSearchParams(location.search);\n'
            '  q.delete("lang");\n'
            '  if (!u){\n'
            '    if (location.pathname === PAGE_URLS.es) return null;\n'
            '    u = PAGE_URLS.es; q.set("lang", l);\n'
            '  }\n'
            '  if (u === location.pathname) return null;\n'
            '  var s = q.toString();\n'
            '  return u + (s ? "?" + s : "") + location.hash;\n'
            '}\n'
            'function allerA(l){ var c = cibleLangue(l); if (c) location.href = c; return !!c; }\n'
            '(function(){\n'
            '  var l = (new URLSearchParams(location.search).get("lang") || "").toLowerCase();\n'
            '  if (l && l !== PAGE_LANG && T[l]){ var c = cibleLangue(l); if (c) location.replace(c); }\n'
            '})();\n'
            'var lang = (new URLSearchParams(location.search).get("lang") || PAGE_LANG).toLowerCase();'
            % json.dumps(urls))


EXTRACT = r"""
const fs=require('fs');
let src=fs.readFileSync(process.argv[2],'utf8');
let i=src.search(/(?:var|const|let)\s+T\s*=\s*\{/);
if(i<0){console.error('objet T introuvable');process.exit(2);}
i=src.indexOf('{',i);
let d=0,j=i,q=null;
for(;j<src.length;j++){
  const c=src[j], pv=src[j-1];
  if(q){ if(c===q&&pv!=='\\')q=null; continue; }
  if(c==='"'||c==="'"||c==='`'){q=c;continue;}
  if(c==='/'&&src[j+1]==='/'){j=src.indexOf('\n',j);continue;}
  if(c==='/'&&src[j+1]==='*'){j=src.indexOf('*/',j)+1;continue;}
  if(c==='{')d++; else if(c==='}'&&--d===0){j++;break;}
}
let obj; eval('obj='+src.slice(i,j));
fs.writeFileSync(process.argv[3], JSON.stringify(obj));
"""


def textes(path):
    with tempfile.TemporaryDirectory() as tmp:
        js, out = os.path.join(tmp, 'x.js'), os.path.join(tmp, 'o.json')
        open(js, 'w', encoding='utf-8').write(EXTRACT)
        r = subprocess.run(['node', js, path, out], capture_output=True, text=True)
        if r.returncode:
            abandon('lecture de T dans %s : %s' % (path, r.stderr.strip()[:200]))
        return json.load(open(out, encoding='utf-8'))


def abandon(msg):
    sys.exit('ABANDON : %s\nRien n\'a été modifié.' % msg)


def lire(rel):
    return open(os.path.join(ROOT, rel), encoding='utf-8').read()


def une_fois(s, ancien, nouveau, quoi):
    n = s.count(ancien)
    if n != 1:
        abandon('%s : trouvé %dx (1 attendu)' % (quoi, n))
    return s.replace(ancien, nouveau)


def remplacer_balise(s, motif, nouveau, quoi):
    ms = list(re.finditer(motif, s))
    if len(ms) != 1:
        abandon('%s : trouvé %dx (1 attendu)' % (quoi, len(ms)))
    return s[:ms[0].start()] + nouveau + s[ms[0].end():]


def zones_commentaires(s):
    return [(m.start(), m.end()) for m in re.finditer(r'<!--.*?-->', s, re.S)]


def remplir_data_t(s, tr):
    """Remplace le contenu de chaque élément data-t="clé" par tr[clé] (hors
    commentaires), en suivant l'imbrication des balises de même nom."""
    com = zones_commentaires(s)
    dans_com = lambda i: any(a <= i < b for a, b in com)
    out, pos, n = [], 0, 0
    for m in re.finditer(r'<(\w+)\b[^>]*\bdata-t="([\w.]+)"[^>]*>', s):
        if m.start() < pos or dans_com(m.start()):
            continue
        tag, cle = m.group(1), m.group(2)
        val = tr.get(cle)
        if not isinstance(val, str):
            continue
        d, fin = 1, None
        for t in re.finditer(r'<%s\b|</%s>' % (tag, tag), s[m.end():]):
            d += 1 if not t.group(0).startswith('</') else -1
            if d == 0:
                fin = m.end() + t.start()
                break
        if fin is None:
            abandon('balise <%s data-t="%s"> non refermée' % (tag, cle))
        out.append(s[pos:m.end()]); out.append(val); pos = fin; n += 1
    out.append(s[pos:])
    s = ''.join(out)
    # placeholders
    def ph(m):
        val = tr.get(m.group(2))
        if not isinstance(val, str):
            return m.group(0)
        t = m.group(0)
        v = html.escape(val, quote=True)
        if re.search(r'\bplaceholder="[^"]*"', t):
            return re.sub(r'\bplaceholder="[^"]*"', 'placeholder="%s"' % v, t)
        return t[:-1] + ' placeholder="%s">' % v if not t.endswith('/>') else t[:-2] + ' placeholder="%s"/>' % v
    s = re.sub(r'<(\w+)\b[^>]*\bdata-tph="([\w.]+)"[^>]*>', ph, s)
    return s, n


def liens_a(s, paires):
    """Remplace href="ancien" par href="nouveau" dans les balises <a> seulement."""
    def balise(m):
        t = m.group(0)
        for a, b in paires:
            t = t.replace('href="%s"' % a, 'href="%s"' % b)
        return t
    return re.sub(r'<a\b[^>]*>', balise, s)


def hreflang_bloc(urls, page_es):
    return ('<link rel="alternate" hreflang="es-ES" href="%s%s">\n'
            '<link rel="alternate" hreflang="ca-ES" href="%s%s?lang=ca">\n'
            '<link rel="alternate" hreflang="en" href="%s%s">\n'
            '<link rel="alternate" hreflang="fr" href="%s%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s%s">'
            % (BASE, urls['es'], BASE, page_es, BASE, urls['en'], BASE, urls['fr'], BASE, urls['es']))


HREFLANG_RE = r'<link rel="alternate" hreflang="es-ES"[^>]*>\s*<link rel="alternate" hreflang="ca-ES"[^>]*>\s*<link rel="alternate" hreflang="en"[^>]*>\s*<link rel="alternate" hreflang="fr"[^>]*>\s*<link rel="alternate" hreflang="x-default"[^>]*>'


def patch_source(p, s):
    """Modifications (une seule fois) de la page espagnole."""
    if 'var PAGE_LANG' in s:
        return s, False
    s = remplacer_balise(s, HREFLANG_RE, hreflang_bloc(p['urls'], p['urls']['es']), p['src'] + ' hreflang')
    s = une_fois(s, VAR_LANG, snippet(p['urls']), p['src'] + ' ligne var lang')
    s, k = re.subn(r'(function choisir\(l\)\{\n)(\s*)lang = l;', r'\1\2if (allerA(l)) return;\n\2lang = l;', s)
    if k != 1:
        abandon('%s : fonction choisir() trouvée %dx' % (p['src'], k))
    note = ('\n  %s. Versions FR et EN à leur propre adresse (23/09/2026, build_i18n_pages.py) :\n'
            '       %s   %s\n'
            '     Elles sont GÉNÉRÉES depuis cette page : modifier ici, puis relancer\n'
            '     python3 _tools/build_i18n_pages.py. Ici : hreflang en/fr vers ces\n'
            '     adresses ; PAGE_LANG / PAGE_URLS / allerA() juste avant « var lang » :\n'
            '     ?lang=fr et ?lang=en redirigent (gclid, utm conservés), le menu des\n'
            '     langues y mène. Le valencien reste en ?lang=ca sur cette adresse.\n'
            % (p['point'], p['urls']['fr'], p['urls']['en']))
    s = une_fois(s, p['ancre_comm'], note + p['ancre_comm'], p['src'] + ' commentaire')
    return s, True


def jsonld_diag(g, lang, url, T, m):
    t = T[lang]
    for n in g['@graph']:
        typ = n.get('@type')
        if typ == 'WebPage':
            n.update({'@id': url + '#webpage', 'url': url, 'name': m['title'], 'description': m['og_desc'],
                      'inLanguage': lang})
        elif typ == 'BreadcrumbList':
            n['itemListElement'] = [
                {"@type": "ListItem", "position": 1, "name": m['home'], "item": BASE + '/%s/' % lang},
                {"@type": "ListItem", "position": 2, "name": m['crumb'], "item": url}]
        elif typ == 'WebApplication':
            n.update({'@id': url + '#app', 'url': url, 'name': m['crumb'], 'description': m['app_desc'],
                      'browserRequirements': m['browser']})
        elif typ == 'Service':
            n['name'] = re.sub(r'<[^>]+>', '', t['h1']).rstrip('.')
            n['serviceType'] = m['service_type']
            n['areaServed'] = [{"@type": "Country", "name": a} for a in m['area']]
            cat = n.get('hasOfferCatalog')
            if cat:
                cat['name'] = m['catalog']
                for item, (nom, desc) in zip(cat['itemListElement'], m['offers']):
                    item['itemOffered']['name'] = nom
                    item['itemOffered']['description'] = desc
        elif typ == 'FAQPage':
            n['inLanguage'] = lang
            n['mainEntity'] = [{"@type": "Question", "name": q[0],
                                "acceptedAnswer": {"@type": "Answer", "text": q[1]}} for q in t['faq']]
    return g


def copie(p, src, lang, T):
    m, url = p['meta'][lang], BASE + p['urls'][lang]
    s = src
    s = une_fois(s, 'var PAGE_LANG = "es";', 'var PAGE_LANG = "%s";' % lang, 'PAGE_LANG')
    s = une_fois(s, '<html lang="es">', '<html lang="%s">' % lang, 'balise html')
    s = une_fois(s, '<head>\n', '<head>\n<!-- Page GÉNÉRÉE par _tools/build_i18n_pages.py depuis %s (version %s).\n'
                 '     Ne pas modifier : modifier la page espagnole, puis relancer le script. -->\n'
                 % (p['src'], lang), '<head>')
    t = T[lang]
    title = m.get('title') or t['metaTitle']
    desc = m.get('desc') or t['metaDesc']
    E = lambda x: html.escape(x, quote=True)
    s = remplacer_balise(s, r'<title>[^<]*</title>', '<title>%s</title>' % E(title), 'title')
    s = remplacer_balise(s, r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % E(desc), 'description')
    s = remplacer_balise(s, r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, 'canonical')
    s = remplacer_balise(s, HREFLANG_RE, hreflang_bloc(p['urls'], p['urls']['es']), 'hreflang')
    s = remplacer_balise(s, r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, 'og:url')
    s = remplacer_balise(s, r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % E(m['og_title']), 'og:title')
    s = remplacer_balise(s, r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % E(m['og_desc']), 'og:description')
    s = remplacer_balise(s, r'<meta property="og:locale" content="[^"]*">', '<meta property="og:locale" content="%s">' % m['locale'], 'og:locale')
    if '<meta name="twitter:title"' in s:
        s = remplacer_balise(s, r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="%s">' % E(m['og_title']), 'twitter:title')
    if '<meta name="twitter:description"' in s:
        s = remplacer_balise(s, r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="%s">' % E(m.get('tw_desc') or m['og_desc']), 'twitter:description')
    # JSON-LD
    mo = re.search(r'(<script type="application/ld\+json" id="%s">)(.*?)(</script>)' % p['ld_id'], s, re.S)
    if not mo:
        abandon('%s : JSON-LD #%s introuvable' % (p['src'], p['ld_id']))
    g = json.loads(mo.group(2))
    if p['ld_id'] == 'ld-graph':
        g = jsonld_diag(g, lang, url, T, m)
    else:
        g['inLanguage'] = lang
        g['mainEntity'] = [{"@type": "Question", "name": q[0],
                            "acceptedAnswer": {"@type": "Answer", "text": q[1]}} for q in t['faq']]
    s = s[:mo.start(2)] + '\n' + json.dumps(g, ensure_ascii=False, indent=2) + '\n' + s[mo.end(2):]
    # le contrôle d'intégrité compare le JSON-LD écrit à la FAQ de la page
    s = s.replace('T.es.faq', 'T[PAGE_LANG].faq')
    # textes
    s, n = remplir_data_t(s, t)
    # liens
    ancien, cible = p['croise']
    s = liens_a(s, NAV[lang] + [(ancien, cible[lang])])
    for es_txt, trad in p['wa'].items():
        s = s.replace('?text=' + es_txt + '"', '?text=' + trad[lang] + '"')
    return s, n


def controles(rel, s, src, lang, p):
    err = []
    if re.findall(r'<link rel="canonical" href="([^"]+)"', s) != [BASE + p['urls'][lang]]:
        err.append('canonical')
    if '<html lang="%s">' % lang not in s:
        err.append('lang')
    alt = sorted(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', s))
    alt_src = sorted(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', src))
    if alt != alt_src:
        err.append('hreflang différents de la page espagnole')
    for bloc in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
        try:
            json.loads(bloc)
        except ValueError as exc:
            err.append('JSON-LD invalide (%s)' % exc)
    scripts = [m.group(2) for m in re.finditer(r'<script(\s[^>]*)?>(.*?)</script>', s, re.S)
               if 'ld+json' not in (m.group(1) or '') and m.group(2).strip()]
    with tempfile.TemporaryDirectory() as tmp:
        for k, js in enumerate(scripts):
            f = os.path.join(tmp, 's%d.js' % k)
            open(f, 'w', encoding='utf-8').write(js)
            r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
            if r.returncode:
                err.append('script %d invalide (%s)' % (k, r.stderr.strip()[:120]))

    def ecart(x, tag):
        v = re.sub(r'<!--.*?-->', '', x, flags=re.S)
        v = re.sub(r'<script.*?</script>', '', v, flags=re.S)
        return len(re.findall(r'<%s[\s>]' % tag, v)) - v.count('</%s>' % tag)
    for tag in ('div', 'section', 'a', 'p', 'h1', 'h2', 'h3', 'span', 'button', 'li', 'ul'):
        if ecart(s, tag) != ecart(src, tag):
            err.append('équilibre des <%s> modifié' % tag)
    liens = ' '.join(re.findall(r'<a\b[^>]*>', s))
    if 'href="https://webautonomos.es"' in liens or 'href="%s"' % p['croise'][0] in liens:
        err.append('lien encore vers une page espagnole')
    if err:
        abandon('%s : %s' % (rel, ' ; '.join(err)))


# ─── remplacements dans le reste du site ─────────────────────────────────────
def remplacements_site():
    r = []
    for urls in (DIAG, VIS):
        for l in LANGS:
            r.append((BASE + urls['es'] + '?lang=' + l, BASE + urls[l]))
            r.append(('"' + urls['es'] + '?lang=' + l, '"' + urls[l]))
            r.append(("'" + urls['es'] + '?lang=' + l, "'" + urls[l]))
    return r


SITEMAP_ANCRE = "    return [v for _, v in sorted(list(roots.items()) + list(dirs.items())\n"
SITEMAP_AJOUT = ("    # Pages FR/EN en dossier (fr/diagnostic-automatisation/index.html…),\n"
                 "    # generees par build_i18n_pages.py : servies sous /fr/<dossier>/.\n"
                 "    for lang in ('fr', 'en'):\n"
                 "        for path in sorted(glob.glob(os.path.join(ROOT, lang, '*', 'index.html'))):\n"
                 "            d = os.path.basename(os.path.dirname(path))\n"
                 "            subs['%s/%s/' % (lang, d)] = ('/%s/%s/' % (lang, d), path)\n\n")


def main():
    check = '--check' in sys.argv
    os.chdir(ROOT)
    ecrire = {}          # rel -> contenu
    rapport = []
    sources = {}
    for p in PAGES:
        s0 = lire(p['src'])
        s, modif = patch_source(p, s0)
        sources[p['src']] = s
        if modif:
            ecrire[p['src']] = s
            rapport.append('  ✓ %-38s hreflang, redirection ?lang=, menu (1re fois)' % p['src'])
    # les copies se construisent sur les sources à jour
    for p in PAGES:
        src = sources[p['src']]
        with tempfile.TemporaryDirectory() as tmp:
            f = os.path.join(tmp, 'src.html')
            open(f, 'w', encoding='utf-8').write(src)
            T = textes(f)
        for lang in LANGS:
            rel = p['urls'][lang].strip('/') + '/index.html'
            s, n = copie(p, src, lang, T)
            controles(rel, s, src, lang, p)
            ecrire[rel] = s
            rapport.append('  ✓ %-38s %3d textes en %s' % (rel, n, lang))
    # liens ?lang=fr / ?lang=en dans le reste du site
    remp = remplacements_site()
    exclus = ('.git', 'node_modules', '.wrangler', 'scripts', '.github')
    candidats = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in exclus]
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), ROOT)
            if rel.endswith('.html') or rel in ('_tools/generate_spa_articles.py', '_tools/build_lang_homes.py', 'llms.txt'):
                candidats.append(rel)
    total = 0
    for rel in sorted(candidats):
        s = ecrire.get(rel) or lire(rel)
        s2 = s
        for a, b in remp:
            s2 = s2.replace(a, b)
        if s2 != s:
            k = sum(s.count(a) for a, _ in remp)
            total += k
            ecrire[rel] = s2
            rapport.append('  ✓ %-38s %3d liens ?lang= remplacés' % (rel, k))
    # sitemap
    sm = lire('_tools/generate_sitemap.py')
    if "glob.glob(os.path.join(ROOT, lang, '*', 'index.html'))" not in sm:
        if sm.count(SITEMAP_ANCRE) != 1:
            abandon('ancre introuvable dans generate_sitemap.py')
        ecrire['_tools/generate_sitemap.py'] = sm.replace(SITEMAP_ANCRE, SITEMAP_AJOUT + SITEMAP_ANCRE)
        rapport.append('  ✓ generate_sitemap.py : pages en dossier sous /fr/ et /en/')
    for rel in ('_tools/generate_sitemap.py', '_tools/generate_spa_articles.py', '_tools/build_lang_homes.py'):
        if rel in ecrire:
            try:
                compile(ecrire[rel], rel, 'exec')
            except SyntaxError as exc:
                abandon('%s invalide : %s' % (rel, exc))
    # rien d'ancien ne doit rester
    for rel, s in ecrire.items():
        for a, _ in remp:
            if a in s:
                abandon('%s : %s subsiste' % (rel, a))
    # écriture (seulement ce qui change réellement)
    ecrire = {r: s for r, s in ecrire.items() if not os.path.exists(r) or lire(r) != s}
    print('\n'.join(rapport))
    if check:
        print('\n--check : %d fichiers seraient écrits, rien n\'a été modifié.' % len(ecrire))
        return
    if not ecrire:
        print('\nRien à écrire : tout est déjà à jour.')
        return
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = os.path.expanduser('~/webautonomos-work/backups/i18n_pages_%s' % stamp)
    for rel in ecrire:
        if os.path.exists(rel):
            d = os.path.join(bak, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(rel, d)
    for rel, s in ecrire.items():
        os.makedirs(os.path.dirname(rel) or '.', exist_ok=True)
        open(rel, 'w', encoding='utf-8').write(s)
    print('\nOK — %d fichiers écrits. Sauvegarde : %s'
          % (len(ecrire), bak.replace(os.path.expanduser('~'), '~')))


if __name__ == '__main__':
    main()
