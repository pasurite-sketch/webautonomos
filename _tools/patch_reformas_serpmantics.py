# -*- coding: utf-8 -*-
"""Réécriture SEO/GEO de /reformas/ (guide SERPmantics « paginas web para empresa de reformas », 24/09/2026)."""
import sys, re, json, html as H

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:90], c, n)
    s = s.replace(a, b)

# ── <head> ───────────────────────────────────────────────────────────────
NEW_TITLE = 'Página web para empresas de reformas: diseño web a 15 €/mes'
NEW_DESC = ('Diseño web para empresas de reformas: tus obras con fotos del antes y el después, SEO local '
            'y solicitudes de presupuesto por WhatsApp. 15 €/mes, sin permanencia.')
rep('<title>Página web para empresas de reformas: 15 €/mes, demo en 24h</title>', f'<title>{NEW_TITLE}</title>')
rep('<meta property="og:title" content="Página web para empresas de reformas: 15 €/mes, demo en 24h">',
    f'<meta property="og:title" content="{NEW_TITLE}">')
old_desc = 'Web profesional para empresas de reformas. Galería de proyectos, presupuestos online y optimizada para Google. 15€/mes, sin alta ni permanencia.'
n = s.count(old_desc)
assert n >= 1, 'meta description'
s = s.replace(old_desc, NEW_DESC)

# ── HERO ─────────────────────────────────────────────────────────────────
rep('<h1>Página web para <span class="ul">empresas de reformas</span> que trae presupuestos</h1>',
    '<h1>Diseño de páginas web para <span class="ul">empresas de reformas</span> que traen presupuestos</h1>')
rep('<span class="pill">✓ Galería para mostrar sus proyectos de reforma</span>',
    '<span class="pill">✓ Tus obras con fotos del antes y el después</span>')

# ── répétitions signalées par le guide (gratis, alta, galería, secteurs) ──
rep('Sin permanencia, sin alta, sin letra pequeña. Lo verás en la demo antes de pagar.',
    'Sin permanencia ni letra pequeña. Lo verás en la demo antes de pagar.')
rep('<summary>¿Puedo mostrar una galería de mis trabajos?</summary>',
    '<summary>¿Puedo mostrar fotos de mis obras?</summary>')
rep('<p>Sí. La galería es una de las secciones más importantes para una empresa de reformas. Mostramos sus proyectos de reforma integral, baños, cocinas y obras terminadas con fotos antes/después de alta calidad. Los clientes quieren ver su trabajo antes de pedir presupuesto.</p>',
    '<p>Sí, y es una de las secciones más importantes para una empresa de reformas. Mostramos tus proyectos de reforma integral, baños, cocinas y obras terminadas con fotos del antes y el después. Los clientes quieren ver tu trabajo antes de solicitar presupuesto.</p>')
rep('<summary>¿Puedo añadir nuevos proyectos a la galería?</summary>',
    '<summary>¿Puedo añadir obras nuevas a mi web?</summary>')
rep('<p>Claro. Nos envía las fotos por WhatsApp o email y las añadimos a su web. Incluido en los 15€/mes.</p>',
    '<p>Claro. Nos envías las fotos por WhatsApp o email y las añadimos a tu web. Está incluido en los 15 €/mes.</p>')
rep('<summary>¿Vosotros entendéis mi sector?</summary>', '<summary>¿Conocéis el sector de las reformas?</summary>')
rep('<p>Sí. Trabajamos con autónomos y pequeños negocios en toda España: profesionales de la salud, oficios (electricistas, fontaneros, carpinteros), servicios personales. Cada sector tiene sus códigos y nosotros los conocemos. Si tienes dudas específicas, contáctanos y te respondemos con ejemplos reales.</p>',
    '<p>Sí. Sabemos que quien encarga una reforma compara varias empresas, quiere ver obras terminadas y teme los retrasos. Por eso tu web enseña proyectos reales, explica cómo trabajas y permite solicitar presupuesto en pocos segundos.</p>')

# boutons « gratis » des cartes de prix et accroche du formulaire
rep('Pedir mi demo gratis →', 'Pedir mi demo sin compromiso →', 2)
rep('Es gratis y sin compromiso', 'Sin coste y sin compromiso')
rep('font-weight:600;margin-bottom:18px;">✓ Sin alta, sin permanencia</p>', 'font-weight:600;margin-bottom:18px;">✓ Sin permanencia</p>')
rep('<strong>Sin alta, sin permanencia</strong><span>Cancela cuando quieras</span>',
    '<strong>Sin permanencia</strong><span>Cancela cuando quieras</span>')

# ── NOUVEAU CONTENU (après l'exemple, avant la FAQ) ─────────────────────
CSS = '''
  /* Guía de contenido /reformas/ (24/09/2026) */
  .gd{padding:56px 20px;max-width:820px;margin:0 auto}
  .gd h2{margin-bottom:18px}
  .gd p{font-size:1.02rem;line-height:1.7;color:#334155;margin:0 0 16px}
  .gd h3{font-family:'Bricolage Grotesque',sans-serif;font-size:1.2rem;font-weight:700;color:var(--blue-dark);margin:28px 0 8px}
  .gd ul{margin:0 0 16px 1.2rem;padding:0;color:#334155;line-height:1.7;font-size:1.02rem}
  .gd li{margin-bottom:8px}
  .gd a{color:var(--green-mid);font-weight:600}
  .gd-band{background:var(--off)}
  .gd .wy-grid{margin-top:24px}
  .gd .wy-card{cursor:default}
'''
i = s.find('</style>')
assert i > 0
s = s[:i] + CSS + s[i:]

GUIA = '''
<!-- GUÍA: DISEÑO WEB PARA EMPRESAS DE REFORMAS (24/09/2026) -->
<section class="gd rev" id="diseno-web-reformas">
  <p class="ey">Diseño web para reformas</p>
  <h2>Diseño web para empresas de reformas: lo que necesita tu negocio</h2>
  <p>Quien busca una empresa de reformas en Google no decide por impulso. Compara varias empresas, mira fotos de obras terminadas, lee opiniones y solo entonces solicita presupuesto. Una buena web de reformas responde a esas dudas antes de que te llamen: qué tipo de obras haces, en qué zona trabajas, cómo trabajas y por qué pueden confiar en ti.</p>
  <p>Por eso el diseño web para empresas de reformas no va de colores bonitos, sino de convertir visitas en solicitudes de presupuesto. Muchas empresas del sector siguen dependiendo del boca a boca y de los directorios de profesionales, donde el cliente llega comparando tu precio con el de otras cinco empresas. Con tu propia página web, el cliente llega después de ver tus proyectos y ya sabe lo que ofreces.</p>
</section>

<div class="gd-band">
<section class="gd rev" id="que-debe-tener">
  <p class="ey">Contenido</p>
  <h2>Qué debe tener la web de una empresa de reformas</h2>
  <p>Estos son los elementos que incluimos en cada página web para empresas de reformas, porque son los que más pesan en la decisión del cliente.</p>
  <h3>Fotos de obras reales, con el antes y el después</h3>
  <p>Es el contenido que más convence. Organizamos tus proyectos por tipo de obra (reforma integral, baño, cocina, pintura, carpintería) con fotos del antes y el después y una breve descripción de cada trabajo: tipo de vivienda, metros, plazo y lo que se hizo. Nada de fotos de stock: el cliente lo nota y pierde la confianza justo cuando quería ver tu trabajo.</p>
  <h3>Una sección para cada tipo de obra</h3>
  <p>No es lo mismo buscar «reforma de baño» que «reformas integrales». Si tu web presenta cada servicio por separado, Google puede mostrarla a quien busca exactamente ese tipo de obra, y el cliente encuentra la información que necesita sin tener que preguntarla.</p>
  <h3>Un formulario de contacto corto y el botón de WhatsApp</h3>
  <p>Nombre, teléfono, tipo de obra y zona: cuantos más datos pides, menos solicitudes recibes. Añadimos además el botón de WhatsApp para que el cliente te envíe fotos del espacio que quiere reformar directamente desde el móvil.</p>
  <h3>Opiniones y datos que dan confianza</h3>
  <p>Mostramos las reseñas de tu ficha de Google, tu experiencia, la zona donde trabajas y los datos legales de tu empresa. En un sector donde el cliente teme las obras que no se terminan, estos elementos marcan la diferencia frente a la competencia.</p>
  <h3>Rápida, segura y pensada para el móvil</h3>
  <p>La web carga rápido, tiene certificado SSL y se ve bien en cualquier teléfono, porque muchos clientes te buscan desde la misma vivienda que quieren reformar. Nosotros nos ocupamos del alojamiento, la seguridad y el mantenimiento: tú no tienes que tocar ninguna plataforma.</p>
</section>
</div>

<section class="gd rev" id="servicios-reformas">
  <p class="ey">Servicios</p>
  <h2>Los servicios de reformas que tu web puede presentar</h2>
  <p>Tú eliges qué servicios mostrar y en qué orden. Cada uno tiene su espacio, con fotos de tus obras y la información que el cliente busca antes de solicitar presupuesto.</p>
  <div class="wy-grid">
    <div class="wy-card"><div class="wy-icon">🏠</div><div class="wy-title">Reformas integrales</div><div class="wy-desc">Viviendas completas, locales y oficinas: planificación, plazos y coordinación de gremios, contada con proyectos terminados.</div></div>
    <div class="wy-card"><div class="wy-icon">🛁</div><div class="wy-title">Reformas de baños</div><div class="wy-desc">Cambio de bañera por plato de ducha, alicatado, fontanería y muebles, con el antes y el después de cada baño.</div></div>
    <div class="wy-card"><div class="wy-icon">🍳</div><div class="wy-title">Reformas de cocinas</div><div class="wy-desc">Distribución, muebles, encimeras e iluminación: el espacio que mejor enseña la calidad de tu trabajo.</div></div>
    <div class="wy-card"><div class="wy-icon">🎨</div><div class="wy-title">Pintura y decoración</div><div class="wy-desc">Interiores, fachadas y acabados decorativos para quien quiere renovar su hogar sin grandes obras.</div></div>
    <div class="wy-card"><div class="wy-icon">🪚</div><div class="wy-title">Carpintería</div><div class="wy-desc">Puertas, armarios a medida, suelos de madera y muebles de cocina hechos a medida.</div></div>
    <div class="wy-card"><div class="wy-icon">🧱</div><div class="wy-title">Albañilería y construcción</div><div class="wy-desc">Tabiques, cerramientos, rehabilitación de viviendas y pequeñas obras de construcción.</div></div>
  </div>
  <p style="margin-top:24px">Si mañana empiezas a ofrecer un servicio nuevo, lo añadimos a tu web dentro de la modificación mensual incluida.</p>
</section>

<div class="gd-band">
<section class="gd rev" id="seo-local-reformas">
  <p class="ey">SEO local</p>
  <h2>SEO local: aparecer cuando buscan reformas en tu zona</h2>
  <p>La mayoría de búsquedas del sector incluyen una ciudad o un barrio: «reformas integrales en Sevilla», «empresa de reformas cerca de mí», «reforma de baño en Alicante». Para aparecer en esas búsquedas, tu web tiene que decir con claridad dónde trabajas y estar conectada con tu ficha de Google.</p>
  <p>Por eso cada web que hacemos incluye la optimización SEO básica: títulos y textos con tu servicio y tu zona, datos de contacto coherentes con tu ficha de Google, una estructura clara y una carga rápida. Si quieres ir más allá, el servicio de <a href="https://webautonomos.es/precios">SEO Local por 15 €/mes</a> añade contenidos pensados para las búsquedas de tu zona.</p>
  <p>¿Trabajas en Cataluña, la Comunitat Valenciana, Galicia o el País Vasco? Tu web puede estar también en catalán, valenciano, gallego o euskera, además de castellano, inglés y francés: hasta cuatro idiomas sin coste extra. Así también te encuentran los clientes que buscan en su idioma, incluidos los extranjeros que compran vivienda en la costa.</p>
</section>
</div>

<section class="gd rev" id="errores-webs-reformas">
  <p class="ey">Errores frecuentes</p>
  <h2>Errores frecuentes en las webs de reformas</h2>
  <p>Estos fallos se repiten en muchas webs del sector y hacen perder clientes cada semana.</p>
  <ul>
    <li><strong>Una sola página que dice «hacemos de todo».</strong> El cliente no sabe si haces su tipo de obra y Google no sabe en qué búsquedas mostrarte.</li>
    <li><strong>Fotos de stock o de mala calidad.</strong> Transmiten desconfianza justo donde el cliente necesita ver tu trabajo real.</li>
    <li><strong>Ninguna zona de trabajo indicada.</strong> Sin ciudad ni provincia, la web no aparece en las búsquedas locales.</li>
    <li><strong>Formularios interminables.</strong> Pedir quince datos antes de dar un presupuesto hace que el cliente llame a otra empresa.</li>
    <li><strong>Una web que nadie actualiza.</strong> Si la última obra es de hace años, parece que la empresa ya no trabaja. Con WebAutonomos, añadir obras nuevas está incluido.</li>
    <li><strong>Pensada solo para ordenador.</strong> Buena parte de tus clientes te buscará desde el móvil: si la web no se lee bien en una pantalla pequeña, se van.</li>
  </ul>
  <p>Si quieres comparar precios antes de decidir, consulta <a href="https://webautonomos.es/blog/es/cuanto-cuesta-pagina-web-autonomos-espana">cuánto cuesta una página web en 2026</a> frente a agencias, freelances y constructores web.</p>
</section>
'''
anchor = '<!-- FAQ -->\n<section class="faq">'
rep(anchor, GUIA + '\n' + anchor)

# ── FAQ : nouvelles questions ────────────────────────────────────────────
NEW_FAQ = [
 ("¿Qué tipo de empresas de reformas pueden tener esta web?",
  "Empresas de reformas integrales, autónomos que hacen reformas de baños y cocinas, pintores, carpinteros, albañiles y pequeñas constructoras. La estructura se adapta a los servicios que ofreces y a la zona donde trabajas."),
 ("¿Cómo recibo las solicitudes de presupuesto?",
  "Por email, cada vez que un cliente rellena el formulario de contacto de tu web, y por WhatsApp si prefiere escribirte directamente. Tú decides qué datos pedir: tipo de obra, zona, plazo o fotos del espacio."),
 ("¿Mi web aparecerá en Google?",
  "La web se entrega optimizada para búsquedas locales: títulos y textos con tu servicio y tu zona, carga rápida y datos coherentes con tu ficha de Google. El posicionamiento depende también de la competencia en tu zona; si quieres acelerar resultados, el servicio de SEO Local está disponible por 15 €/mes."),
 ("¿Puedo tener la web en catalán o en otros idiomas?",
  "Sí. Hasta cuatro idiomas sin coste extra: castellano, inglés, francés y catalán, valenciano, gallego o euskera. Redactamos nosotros cada versión y la modificación mensual incluida se aplica en todos los idiomas."),
]
items = ''.join('\n    <details class="faq-item">\n      <summary>%s</summary>\n      <p>%s</p>\n    </details>\n' % (q, a) for q, a in NEW_FAQ)
i = s.find('<!-- FAQ -->'); j = s.find('  </div>\n</section>', i)
assert i > 0 and j > i
s = s[:j] + items + '\n' + s[j:]

# ── FAQPage JSON-LD construit depuis la FAQ visible ─────────────────────
i = s.find('<!-- FAQ -->'); j = s.find('</section>', i)
faq_html = s[i:j]
qa = re.findall(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>', faq_html, re.S)
clean = lambda x: re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', '', x))).strip()
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": clean(q),
                          "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in qa]}
assert '"@type": "FAQPage"' not in s and '"@type":"FAQPage"' not in s
block = '<script type="application/ld+json">\n' + json.dumps(faq_ld, ensure_ascii=False, indent=2) + '\n</script>\n'
k = s.find('</head>')
s = s[:k] + block + s[k:]

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(qa), 'questions FAQ')

# ── 2e passe : termes encore sous la cible du guide ──────────────────────
s = open(dst, encoding='utf-8').read()
R2 = [
 ("Compara varias empresas, mira fotos de obras terminadas, lee opiniones y solo entonces solicita presupuesto.",
  "Compara varias empresas, pide presupuestos a dos o tres, mira fotos de obras terminadas y lee opiniones de otros clientes."),
 ("Una buena web de reformas responde a esas dudas antes de que te llamen:",
  "Una buena web de reformas responde a esas dudas antes de que te llamen:"),
 ("Con tu propia página web, el cliente llega después de ver tus proyectos y ya sabe lo que ofreces.</p>",
  "Con tu propia página web, el cliente llega después de ver tus proyectos y ya sabe lo que ofreces.</p>\n  <p>En WebAutonomos hacemos diseño web para reformistas, pintores, carpinteros y pequeñas empresas de construcción de toda España. Cada web de reformas se escribe con los datos reales de tu empresa: tus servicios, tu zona, tus fotos y las reseñas de tus clientes.</p>"),
 ("Estos son los elementos que incluimos en cada página web para empresas de reformas, porque son los que más pesan en la decisión del cliente.",
  "Estos son los elementos que incluimos en cada diseño web para empresas de reformas, porque son los que más pesan en la decisión del cliente y los que más confianza generan."),
 ("con fotos del antes y el después y una breve descripción de cada trabajo: tipo de vivienda, metros, plazo y lo que se hizo.",
  "en una galería de obras con fotos del antes y el después y una breve descripción de cada proyecto: tipo de vivienda, metros, plazo y lo que se hizo, de la albañilería a los acabados."),
 ("Mostramos las reseñas de tu ficha de Google, tu experiencia, la zona donde trabajas y los datos legales de tu empresa.",
  "Mostramos las reseñas de tu ficha de Google, tus años de experiencia, la zona donde trabajas y los datos legales de tu empresa."),
 ("Si mañana empiezas a ofrecer un servicio nuevo, lo añadimos a tu web dentro de la modificación mensual incluida.",
  "Si mañana empiezas a ofrecer un servicio nuevo, lo añadimos a tu web dentro de la modificación al mes incluida."),
 ("Para aparecer en esas búsquedas, tu web tiene que decir con claridad dónde trabajas y estar conectada con tu ficha de Google.",
  "Las páginas web de reformas que aparecen primero en esas búsquedas dicen con claridad dónde trabajan y están conectadas con su ficha de Google."),
 ("Por eso cada web que hacemos incluye la optimización SEO básica:",
  "Por eso cada diseño web que hacemos incluye la optimización SEO básica:"),
 ("Redactamos nosotros cada versión y la modificación mensual incluida se aplica en todos los idiomas.",
  "Redactamos nosotros cada versión y la modificación al mes incluida se aplica en todos los idiomas."),
 ("pintores, carpinteros, albañiles y pequeñas constructoras.",
  "pintores, carpinteros, albañiles y pequeñas empresas de construcción."),
 ("<li><strong>Una sola página que dice «hacemos de todo».</strong> El cliente no sabe si haces su tipo de obra y Google no sabe en qué búsquedas mostrarte.</li>",
  "<li><strong>Una sola página que dice «hacemos de todo».</strong> El cliente no sabe si haces su tipo de obra (reforma integral, baño, cocina, carpintería) y Google no sabe en qué búsquedas mostrarte.</li>"),
 ("<li><strong>Fotos de stock o de mala calidad.</strong> Transmiten desconfianza justo donde el cliente necesita ver tu trabajo real.</li>",
  "<li><strong>Fotos de stock o de mala calidad.</strong> Restan confianza justo donde el cliente necesita ver tu trabajo real.</li>\n    <li><strong>Un diseño web anticuado.</strong> Una web lenta o de hace diez años da la misma impresión que una obra mal acabada: el cliente duda antes de pedir presupuestos.</li>"),
]
for a, b in R2:
    assert s.count(a) >= 1, a[:80]  # FAQ : texte visible + JSON-LD
    s = s.replace(a, b)
open(dst, 'w', encoding='utf-8').write(s)
print('passe 2 ok')
