# -*- coding: utf-8 -*-
"""Accueil espagnol (SPA d'index.html), 06/10/2026 : textes conformes à VERITE.md, FAQ enrichie, repli statique
régénéré depuis l'objet translations.

1. translations.es : affirmations absentes de VERITE retirées (agenda en ligne, délais de 24 h pour les
   modifications, « recuperamos tu web en minutos », images professionnelles, contenu du SEO Local et de la
   fiche Google au-delà de VERITE §5, prix et délais des agences sans source dans la comparaison), et six
   questions de FAQ ajoutées. Chaque remplacement vérifie qu'il trouve sa chaîne une seule fois dans le bloc es.
2. Repli <div id="fallback"> (seul HTML que lit un robot sans JavaScript) : reconstruit chaîne par chaîne depuis
   translations.es, dans l'ordre des sections de l'accueil (comparaison et avis Trustpilot compris, comme dans
   l'application) ; liens et adresse finaux conservés.
3. JSON-LD FAQPage du <head> : régénéré depuis la FAQ espagnole.

Les blocs val, en et fr ne changent pas. Non rejouable : si une ancre manque (correctif déjà appliqué), le
script s'arrête sans rien écrire. À lancer depuis la racine du dépôt :
  python3 _tools/patch_home_es_20261006.py [--sortie FICHIER]
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
SORTIE = sys.argv[sys.argv.index('--sortie') + 1] if '--sortie' in sys.argv else SRC

REMPLACEMENTS = [
    # Tarifs : pas d'agenda en ligne (VERITE §2), seulement un lien vers l'outil du client
    ('item9:"Calendario de citas online"', 'item9:"Enlace a tu sistema de reservas"'),
    # Services complémentaires : contenu de VERITE §5 seulement
    ('features:["4 artículos de blog al mes","Optimización de palabras clave locales","Meta títulos y descripciones optimizados","Estructura de URLs amigable","Velocidad de carga optimizada","Schema markup para negocios locales","Informe mensual de posicionamiento"]',
     'features:["4 artículos de blog al mes","Palabras clave de tu zona","Informe mensual de posicionamiento"]'),
    (',"Gestión y respuesta a reseñas","Informe mensual de rendimiento"]', ',"Gestión y respuesta a reseñas"]'),
    # Comparaison : ni prix ni délais d'agences sans source
    ('"<strong>Precios inflados:</strong> Te cobran 500€, 1.000€ o más por una web básica que no necesitas.","<strong>Semanas de espera:</strong> Te dicen 2 semanas y acaban siendo 2 meses.","<strong>Atado con contrato:</strong> Permanencias de 12 meses, penalizaciones si cancelas."',
     '"<strong>Cada proyecto, su factura:</strong> cada página se presupuesta aparte, y el mantenimiento o los cambios pueden cobrarse después.","<strong>Pagar antes de ver:</strong> pides presupuesto, adelantas una parte y esperas semanas para ver el diseño.","<strong>Contratos con permanencia:</strong> algunos servicios te atan durante meses y penalizan si cancelas."'),
    # FAQ
    ('Ninguno, te lo garantizamos. Los 15€/mes incluyen absolutamente todo lo que necesitas: diseño web profesional y personalizado, hosting de alta velocidad,',
     'Ninguno. Los 15€/mes cubren todo lo necesario para tener tu web en marcha: diseño web profesional y personalizado, hosting,'),
    ('Nos dices si quieres cambios (textos, fotos, colores, secciones...) y los hacemos en 24h.',
     'Nos dices si quieres cambios (textos, fotos, colores, secciones...) y los hacemos antes de publicarla, sin límite de ajustes.'),
    ('Tú solo necesitas decirnos qué servicios ofreces, en qué zona trabajas, y compartirnos algunas fotos si las tienes (si no, usamos imágenes profesionales).',
     'Solo tienes que decirnos qué servicios ofreces, en qué zona trabajas, y compartirnos algunas fotos si las tienes (si no, usamos las de tu ficha de Google). No hace falta saber programación ni diseño gráfico, ni dedicarle tiempo.'),
    ('Si en algún momento quieres hacer un cambio, nos escribes y lo hacemos nosotros.',
     'Para cualquier cambio posterior, nos escribes y lo hace nuestro equipo: tienes una modificación al mes incluida.'),
    ('copias de seguridad automáticas diarias (si algo falla, recuperamos tu web en minutos), monitorización 24/7 para detectar caídas y actuar inmediatamente, optimización de velocidad para que tu web cargue rápido, renovación del certificado SSL, y soporte técnico por email y WhatsApp con respuesta en menos de 24h.',
     'copias de seguridad automáticas diarias (si algo falla, podemos restaurarla), monitorización 24/7 para detectar caídas, renovación del certificado SSL, y soporte técnico por email y WhatsApp con respuesta en el día.'),
    ('tienes derecho a una modificación al mes, para siempre: actualizar textos y descripciones de servicios, cambiar fotos e imágenes, modificar horarios y datos de contacto, añadir nuevos servicios o eliminar los que ya no ofreces, ajustes de diseño (colores, tipografías, disposición), añadir nuevas secciones o páginas, integrar tu calendario de reservas, actualizar precios... Todo lo que necesites para mantener tu web siempre actualizada y relevante. Nos escribes por WhatsApp o email, y en 24h tienes los cambios hechos.',
     'tienes derecho a una modificación al mes, sin límite de tiempo: actualizar textos y descripciones de servicios, cambiar fotos e imágenes, modificar horarios y datos de contacto, añadir nuevos servicios o eliminar los que ya no ofreces, poner el enlace a tu sistema de reservas, actualizar precios... Los cambios más grandes, como un rediseño o una nueva sección importante, se hacen con presupuesto cerrado, sin sorpresas. Nos escribes por WhatsApp o email y nos ocupamos.'),
    ('El servicio incluye: 4 artículos de blog optimizados al mes sobre temas de tu sector, investigación y optimización de palabras clave locales, meta títulos y descripciones optimizados para cada página, URLs amigables para buscadores, optimización de velocidad de carga (factor clave para Google), y un informe mensual donde ves tu evolución en el ranking. Es la diferencia entre que te encuentren los clientes de tu zona o que encuentren a tu competencia.',
     'El servicio incluye 4 artículos de blog al mes sobre temas de tu sector, el trabajo de las palabras clave de tu zona y un informe mensual donde ves tu evolución. Puedes contratarlo aunque tu web no esté hecha con nosotros.'),
    ('{q:"¿Qué incluye el servicio de Google My Business?",a:"Con Google My Business (+29€/mes) nos encargamos de gestionar completamente tu perfil de Google para que aparezcas en Google Maps y en las búsquedas locales con la mejor imagen posible. Incluye: optimización completa de tu ficha (categorías, descripción, horarios, atributos, fotos profesionales), publicación de 4 posts al mes con novedades y ofertas para mantener tu perfil activo, gestión y respuesta profesional a todas las reseñas (positivas y negativas), monitorización de tu posición en el Local Pack, y un informe mensual detallado con métricas de rendimiento (visualizaciones, clics, llamadas, solicitudes de ruta). Si aún no tienes ficha de Google, la creamos y verificamos por 49€ (pago único). Es fundamental para un negocio local: es lo que aparece en Google Maps y en las búsquedas de tu zona."}',
     '{q:"¿Qué incluye la gestión de tu ficha de Google?",a:"Con la gestión de tu ficha de Google (+29€/mes) nos encargamos de tu perfil para que aparezcas en Google Maps y en las búsquedas locales con la información correcta. Incluye la optimización de tu ficha (categorías, descripción, horarios, atributos y fotos), la publicación de 4 posts al mes con tus novedades y la respuesta a las reseñas, positivas y negativas. Si aún no tienes ficha de Google, la creamos y verificamos por 49€ (pago único). También puedes contratarla sin la web."}'),
]

# Nouvelles questions, insérées avant celle du SEO Local
NOUVELLES = [
    ('¿Qué debe tener la página web de un autónomo?',
     'Para crear una página que funcione, lo esencial es que tus clientes entiendan en poco tiempo qué haces, dónde trabajas y cómo contactarte: tus servicios explicados de forma clara, tu zona de trabajo, fotos reales de tus trabajos, tus opiniones, un formulario de contacto, el botón de WhatsApp y los textos legales (aviso legal, privacidad y cookies). Todo eso viene en tu página de WebAutonomos, adaptado a tu sector y pensado para verse bien en el móvil.'),
    ('¿Necesito una página web si ya estoy en redes sociales?',
     'Las redes sociales como Instagram o Facebook sirven para compartir contenido de tu día a día y mantener el contacto con tus clientes y tu comunidad, pero no las controlas tú: el alcance depende de cada plataforma y tus publicaciones se pierden con el tiempo. Tu sitio web es tuyo, puede aparecer en la búsqueda de Google y reúne en un solo lugar tus servicios, tu teléfono y la forma de contactarte a través del formulario o de WhatsApp. Lo ideal es usar las dos: incluimos enlaces a tus perfiles en redes sociales sin coste extra.'),
    ('¿Es mejor una plantilla, WordPress o una página hecha por vosotros?',
     'Depende del tiempo que puedas dedicarle. Con un creador de webs con plantillas o con WordPress puedes crear tu página tú mismo, pero tendrás que elegir la herramienta, preparar el contenido, configurar la plataforma y ocuparte del mantenimiento. Una agencia hace un proyecto a medida, que se cobra por proyecto. Con WebAutonomos la preparamos nosotros a partir de la información de tu ficha de Google, por 15 €/mes o 349 € en pago único, y tus clientes te encuentran sin que pierdas tiempo en la parte técnica. Para comparar opciones, tenemos una comparativa de los 6 creadores de webs para autónomos.'),
    ('¿Puedo vender mis productos online?',
     'Sí. Podemos crear una tienda online con catálogo de productos y pago con tarjeta, con un presupuesto aparte: el comercio electrónico no está incluido en los 15 €/mes ni en los 349 €. Para mostrar tus productos y que un cliente te los pida con un mensaje, basta con tu página y su formulario.'),
    ('¿Qué textos legales necesita mi página?',
     'En España, un sitio profesional debe identificar a su titular (aviso legal), explicar qué hace con los datos personales (política de privacidad) e informar sobre las cookies. Redactamos esos tres textos y los incluimos en tu página. Si tu actividad tiene normas propias, como las profesiones sanitarias, revisa también sus requisitos, como el número de colegiado.'),
    ('¿Cómo me ayuda mi página a conseguir más clientes?',
     'Una página no hace milagros, pero trabaja por ti a cualquier hora: cuando alguien necesita tu servicio en tu zona, puede encontrarte, ver tu trabajo y tus opiniones, y escribirte a través de WhatsApp o del formulario. Por eso cuidamos lo básico del posicionamiento: títulos y textos con tu servicio y tu zona, y la misma información que en tu ficha de Google. Para ir más allá, el SEO Local trabaja tu visibilidad cada mes.'),
]
ANCRE_NOUVELLES = '{q:"¿Qué es el SEO Local y por qué lo necesito?"'


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


def js(t):
    return json.dumps(t, ensure_ascii=False)


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
    return html.escape(x, quote=False)


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
    L += ['      <li><a href="/%s">%s</a></li>' % (k, e(f[k])) for k in
          ('electricistas', 'fontaneros', 'carpinteros', 'dentistas', 'fisioterapeutas', 'psicologos', 'reformas')]
    L += ['    </ul>', '    <p>%s <a href="/mejores-creadores-paginas-web-autonomos">%s</a></p>' % (e(f['cmpQ']), e(f['cmpCta'])), '',
          '    <h2>%s</h2>' % e(hw['title']), '    <p>%s</p>' % e(hw['subtitle']), '    <ul>']
    L += ['      <li><strong>%s</strong> — %s</li>' % (e(hw['step%d' % i]), e(hw['step%dDesc' % i])) for i in (1, 2, 3)]
    items = [p[k] for k in sorted((k for k in p if re.fullmatch(r'item\d+', k)), key=lambda k: int(k[4:]))]
    L += ['    </ul>', '', '    <h2>%s</h2>' % e(p['title']),
          '    <p>%s — %s</p>' % (e(p['subtitle']), e(p['subTerms'])),
          '    <p>15&nbsp;&euro;/mes · %s</p>' % e(p['guarantee']),
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


s = open(SRC, encoding='utf-8').read()
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
if bloc.count(ANCRE_NOUVELLES) != 1:
    sys.exit('ancre des nouvelles questions introuvable')
bloc = bloc.replace(ANCRE_NOUVELLES, ''.join('{q:%s,a:%s},' % (js(q), js(a)) for q, a in NOUVELLES) + ANCRE_NOUVELLES)
s = s[:ies] + bloc + s[fes + 1:]
t = lire_translations(s)['es']

# 2. repli statique, liens et adresse finaux conservés
a = s.index('<div id="fallback">')
b = s.index('    <ul>\n      <li><a href="/precios">', a)
s = s[:a] + repli(t) + '\n' + s[b:]

# 3. JSON-LD FAQPage du <head>
m = None
for x in re.finditer(r'(?s)(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)', s[:s.index('<body')]):
    if '"FAQPage"' in x.group(2):
        m = x
if not m:
    sys.exit('FAQPage introuvable dans le <head>')
s = s[:m.start(2)] + faqpage(t['faq']['items']) + s[m.end(2):]

open(SORTIE, 'w', encoding='utf-8').write(s)
print('ok : %d remplacements, %d questions (dont %d nouvelles), repli %d mots' % (
    len(REMPLACEMENTS), len(t['faq']['items']), len(NOUVELLES),
    len(re.sub(r'<[^>]+>', ' ', repli(t)).split())))
