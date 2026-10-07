# -*- coding: utf-8 -*-
"""Accueil espagnol (SPA d'index.html) et /precios, 07/10/2026 : « + IVA » après les prix, comme dans les
messages de prospection depuis le 07/10, et fin de « El precio que ves es el precio que pagas », que l'IVA
rendait inexact. Demande d'Angelino du 07/10/2026 ; VERITE.md : prix affichés sans IVA, IVA de 21 % facturée.

1. translations.es : « + IVA » après chaque prix annoncé sur l'accueil (sous-titre du héros, comparaison,
   étape 3, carte tarifaire, services additionnels, quatre réponses de la FAQ). Sur la carte : « 15€ /mes + IVA »
   et « 349€ + IVA », avec « Pago único · Mismos servicios » dessous (au lieu de « Una sola cuota · … »).
   Les rappels du type « incluido en los 15€/mes » restent tels quels : la réponse sur les coûts cachés dit
   désormais que seule l'IVA s'ajoute. Chaque remplacement vérifie qu'il trouve sa chaîne une seule fois dans le
   bloc es.
2. Formulaire de contact de l'application (ContactPage) : la tuile « 15€/mes », écrite en dur, affiche
   t.pricing.price + « € » + t.pricing.period, comme la carte tarifaire ; la tuile 349 € lit déjà
   t.pricing.oneShotPeriod (« + IVA » en espagnol). Sans cela, seule l'option 349 € aurait porté l'IVA. En val,
   en et fr, la tuile affiche la période de leur carte (« /mes », « /month », « /mois ») au lieu de « /mes ».
3. Repli <div id="fallback"> et JSON-LD FAQPage du <head> : régénérés depuis translations.es, avec les
   fonctions de patch_home_es_20261006.py (liens des pages métier avec slash final, comme depuis
   patch_slash_secteurs_20261007.py ; ligne du prix mensuel lue dans pricing.period). Avant d'écrire, le
   script vérifie qu'elles reproduisent à l'identique le repli et la FAQPage en place : rien d'autre ne change.
4. precios.html : même phrase remplacée. /precios est en observation jusqu'au 22/10 : title, H1 et H2
   inchangés, comme pour la correction du 29/09.

Les blocs val, en et fr de translations ne changent pas, ni le <title> et les métadonnées de l'accueil. Non
rejouable : si une ancre manque (correctif déjà appliqué), le script s'arrête sans rien écrire. À lancer
depuis la racine du dépôt :
  python3 _tools/patch_prix_iva_accueil_20261007.py [--sortie DOSSIER]
(--sortie écrit index.html et precios.html dans DOSSIER, pour relecture, au lieu de les remplacer.)
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = sys.argv[sys.argv.index('--sortie') + 1] if '--sortie' in sys.argv else ROOT

# Espace insécable entre « + » et « IVA » là où la ligne est étroite (carte tarifaire, héros) : à 360 px de large,
# « /mes + IVA » se coupait en « /mes + » et « IVA ». Écrit sous la forme d'échappement JavaScript  .
INSEC = chr(92) + 'u00a0'

REMPLACEMENTS = [
    # Héros, comparaison, étape 3
    ('subtitle:"Solo 15€/mes · Sin alta · Sin permanencia"', 'subtitle:"Solo 15€/mes +' + INSEC + 'IVA · Sin alta · Sin permanencia"'),
    ('"<strong>Precio fijo y claro:</strong> 15€/mes, todo incluido.', '"<strong>Precio fijo y claro:</strong> 15€/mes + IVA, todo incluido.'),
    ('step3Desc:"Aceptas, pagas 15€/mes y tu web', 'step3Desc:"Aceptas, pagas 15€/mes + IVA y tu web'),
    # Carte tarifaire : « 15€ /mes + IVA » et « 349€ + IVA », « pago único » descendant sur la ligne du dessous
    # (« + IVA · pago único » se coupait sur mobile) ; il remplace « Una sola cuota », qui disait la même chose
    ('price:"15",period:"/mes",', 'price:"15",period:"/mes +' + INSEC + 'IVA",'),
    ('oneShotPeriod:"pago único",oneShotTerms:"Una sola cuota · Mismos servicios"',
     'oneShotPeriod:"+' + INSEC + 'IVA",oneShotTerms:"Pago único · Mismos servicios"'),
    # Services additionnels (formule de VERITE §5)
    ('seo:{title:"SEO Local",price:"15€/mes",', 'seo:{title:"SEO Local",price:"15€/mes + IVA",'),
    ('gmb:{title:"Google My Business",price:"29€/mes",', 'gmb:{title:"Google My Business",price:"29€/mes + IVA",'),
    ('"Creación de ficha: 49€ (pago único)"', '"Creación de ficha: 49€ + IVA (pago único)"'),
    # FAQ
    ('ni costes de activación. El precio que ves es el precio que pagas, sin sorpresas."',
     'ni costes de activación. Al precio que ves solo se suma el IVA, sin sorpresas."'),
    ('Sigue costando 15 €/mes, o 349 € en pago único.', 'Sigue costando 15 €/mes + IVA, o 349 € + IVA en pago único.'),
    ('por 15 €/mes o 349 € en pago único, y tus clientes', 'por 15 €/mes + IVA o 349 € + IVA en pago único, y tus clientes'),
    ('El SEO Local (+15€/mes) es lo que hace', 'El SEO Local (15€/mes + IVA) es lo que hace'),
    ('Con la gestión de tu ficha de Google (+29€/mes) nos encargamos', 'Con la gestión de tu ficha de Google (29€/mes + IVA) nos encargamos'),
    ('la creamos y verificamos por 49€ (pago único). También puedes contratarla sin la web.',
     'la creamos y verificamos por 49€ + IVA (pago único). También puedes contratarla sin la web.'),
]

# Tuile « 15€/mes » du formulaire de contact de l'application
TUILE = ('{className:"text-2xl font-bold text-gray-800"},"15€/mes")',
         '{className:"text-2xl font-bold text-gray-800"},t.pricing.price,"€",t.pricing.period)')

PRECIOS = ('ni costes de activación. El precio que ves es el precio que pagas. Cancelas cuando quieras',
           'ni costes de activación. Al precio que ves solo se suma el IVA. Cancelas cuando quieras')


def fin_bloc(s, i):
    """Indice de l'accolade fermante qui correspond à s[i] == '{' (chaînes JS ignorées)."""
    d, k, q = 0, i, None
    while k < len(s):
        c = s[k]
        if q:
            if c == '\\':
                k += 2
                continue
            if c == q:
                q = None
        elif c in '"\'`':
            q = c
        elif c == '{':
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                return k
        k += 1
    raise ValueError('accolade non fermée')


def lire_translations(s):
    i = s.index('const translations=') + len('const translations=')
    obj = s[i:fin_bloc(s, i) + 1]
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write('process.stdout.write(JSON.stringify(' + obj + '));')
    r = subprocess.run(['node', f.name], capture_output=True, text=True)
    os.unlink(f.name)
    if r.returncode:
        sys.exit('translations illisibles : ' + r.stderr[:500])
    return json.loads(r.stdout)


def e(x):
    return html.escape(x, quote=False).replace(chr(0xA0), '&nbsp;')


def repli(t):
    """Repli statique : chaînes de translations.es, dans l'ordre des sections de l'accueil SPA."""
    h, hw, b, c, f, p, u, ts, fq, ct = (t['hero'], t['howItWorks'], t['benefits'], t['comparison'], t['forWho'],
                                         t['pricing'], t['upsells'], t['testimonials'], t['faq'], t['cta'])
    L = ['<div id="fallback">',
         '    <h1>%s %s</h1>' % (e(h['title']), e(h['titleHighlight'])),
         '    <p>%s</p>' % e(h['subtitle']), '    <p>%s</p>' % e(h['trusted']), '',
         '    <h2>%s</h2>' % e(b['title']), '    <ul>']
    L += ['      <li><strong>%s</strong> — %s</li>' % (e(b['benefit%d' % i]), e(b['benefit%dDesc' % i])) for i in (1, 2, 3, 4)]
    # les puces de la comparaison contiennent déjà du HTML (<strong>), telles quelles dans l'application
    L += ['    </ul>', '', '    <h2>%s</h2>' % e(c['title']), '    <p>%s</p>' % e(c['subtitle']),
          '    <h3>%s</h3>' % e(c['othersTitle']), '    <ul>'] + ['      <li>%s</li>' % x for x in c['others']] + \
         ['    </ul>', '    <h3>%s</h3>' % e(c['usTitle']), '    <ul>'] + ['      <li>%s</li>' % x for x in c['us']] + ['    </ul>', '']
    L += ['    <h2>%s</h2>' % e(f['title']), '    <p>%s</p>' % e(f['subtitle']), '    <ul>']
    L += ['      <li><a href="/%s/">%s</a></li>' % (k, e(f[k])) for k in
          ('electricistas', 'fontaneros', 'carpinteros', 'dentistas', 'fisioterapeutas', 'psicologos', 'reformas')]
    L += ['    </ul>', '    <p>%s <a href="/mejores-creadores-paginas-web-autonomos">%s</a></p>' % (e(f['cmpQ']), e(f['cmpCta'])), '',
          '    <h2>%s</h2>' % e(hw['title']), '    <p>%s</p>' % e(hw['subtitle']), '    <ul>']
    L += ['      <li><strong>%s</strong> — %s</li>' % (e(hw['step%d' % i]), e(hw['step%dDesc' % i])) for i in (1, 2, 3)]
    items = [p[k] for k in sorted((k for k in p if re.fullmatch(r'item\d+', k)), key=lambda k: int(k[4:]))]
    L += ['    </ul>', '', '    <h2>%s</h2>' % e(p['title']),
          '    <p>%s — %s</p>' % (e(p['subtitle']), e(p['subTerms'])),
          '    <p>15&nbsp;&euro;%s · %s</p>' % (e(p['period']), e(p['guarantee'])),
          '    <p>%s</p>' % e(p['includes']), '    <ul>', '      ' + ''.join('<li>%s</li>' % e(x) for x in items), '    </ul>',
          '    <p>%s : 349&nbsp;&euro; %s — %s</p>' % (e(p['separator']), e(p['oneShotPeriod']), e(p['oneShotTerms'])), '',
          '    <h2>%s — %s</h2>' % (e(u['seo']['title']), e(u['seo']['price'])), '    <p>%s</p>' % e(u['seo']['desc']), '',
          '    <h2>%s</h2>' % e(ts['title']), '    <p>%s/5 — %s</p>' % (e(ts['ratingScore']), e(ts['ratingLabel']))]
    n = 1
    while 'testimonial%d' % n in ts:
        job, tr = ts.get('testimonial%dJob' % n, ''), ts.get('testimonial%dTranslated' % n, '')
        L.append('    <blockquote><p>%s</p><footer>%s%s%s</footer></blockquote>' % (
            e(ts['testimonial%d' % n]), e(ts['testimonial%dAuthor' % n]), (' · ' + e(job)) if job else '',
            (' (' + e(tr) + ')') if tr else ''))
        n += 1
    L += ['', '    <h2>%s</h2>' % e(fq['title']), '    <p>%s</p>' % e(fq['subtitle']), '    <dl>']
    for it in fq['items']:
        L += ['      <dt>%s</dt>' % e(it['q']), '      <dd>%s</dd>' % e(it['a'])]
    L += ['    </dl>', '', '    <h2>%s</h2>' % e(ct['title']), '    <p>%s</p>' % e(ct['subtitle']), '']
    return '\n'.join(L) + '\n'


def faqpage(items):
    d = {'@context': 'https://schema.org', '@type': 'FAQPage',
         'mainEntity': [{'@type': 'Question', 'name': it['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': it['a']}} for it in items]}
    return json.dumps(d, ensure_ascii=False, indent=2)


def bornes_repli(s):
    a = s.index('<div id="fallback">')
    return a, s.index('    <ul>\n      <li><a href="/precios">', a)


def faq_du_head(s):
    m = None
    for x in re.finditer(r'(?s)(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)', s[:s.index('<body')]):
        if '"FAQPage"' in x.group(2):
            m = x
    if not m:
        sys.exit('FAQPage introuvable dans le <head>')
    return m


s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

# 0. Les générateurs reproduisent-ils le repli et la FAQPage en place ?
t0 = lire_translations(s)['es']
a, b = bornes_repli(s)
if repli(t0) + '\n' != s[a:b]:
    sys.exit('le repli en place diffère de celui que régénère ce script : rien n\'est écrit')
if faqpage(t0['faq']['items']) != faq_du_head(s).group(2):
    sys.exit('la FAQPage en place diffère de celle que régénère ce script : rien n\'est écrit')

# 1. bloc es de translations
i0 = s.index('const translations=') + len('const translations=')
ies = s.index('es:{', i0) + 3
fes = fin_bloc(s, ies)
bloc = s[ies:fes + 1]
for ancien, nouveau in REMPLACEMENTS:
    n = bloc.count(ancien)
    if n != 1:
        sys.exit('ancre trouvée %d fois dans le bloc es : %s' % (n, ancien[:90]))
    bloc = bloc.replace(ancien, nouveau)
s = s[:ies] + bloc + s[fes + 1:]

# 2. tuile du formulaire de contact, dans le composant ContactPage
ic = s.index('const ContactPage=')
suivant = re.compile(r'const [A-Z][A-Za-z0-9]*=').search(s, ic + 1)  # composant défini juste après
fc = suivant.start() if suivant else len(s)
if s.count(TUILE[0]) != 1 or not ic < s.index(TUILE[0]) < fc:
    sys.exit('tuile « 15€/mes » du formulaire introuvable ou ambiguë')
s = s.replace(TUILE[0], TUILE[1])
t = lire_translations(s)['es']

# 3. repli statique et JSON-LD FAQPage du <head>
a, b = bornes_repli(s)
s = s[:a] + repli(t) + '\n' + s[b:]
m = faq_du_head(s)
s = s[:m.start(2)] + faqpage(t['faq']['items']) + s[m.end(2):]

# 4. /precios
p = open(os.path.join(ROOT, 'precios.html'), encoding='utf-8').read()
if p.count(PRECIOS[0]) != 1:
    sys.exit('phrase de precios.html trouvée %d fois' % p.count(PRECIOS[0]))
p = p.replace(PRECIOS[0], PRECIOS[1])

os.makedirs(SORTIE, exist_ok=True)
open(os.path.join(SORTIE, 'index.html'), 'w', encoding='utf-8').write(s)
open(os.path.join(SORTIE, 'precios.html'), 'w', encoding='utf-8').write(p)
print('ok : %d remplacements dans translations.es, tuile du formulaire, repli et FAQPage régénérés, '
      'precios.html (%s)' % (len(REMPLACEMENTS), SORTIE))
