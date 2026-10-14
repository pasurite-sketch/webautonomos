# -*- coding: utf-8 -*-
"""Accueil espagnol (SPA d'index.html), 15/10/2026 : guide pratique « página web para autónomos » et répétitions
allégées, pour le guide SERPmantics de la requête (note 76 le 15/10, position moyenne 6,5).

1. translations.es : reformulations sans changement de sens qui allègent les mots trop répétés face au top 10
   (« web », « página », « Google », « incluye », « quieras », « datos », « contacto », « nombre »…). Chaque
   remplacement vérifie qu'il trouve sa chaîne une seule fois dans le bloc es.
2. translations.es.guide et translations.val.guide : cinq sections (ce que gagne un autónomo avec une web, les
   étapes pour la créer, ce qu'elle coûte avec tableau comparatif sourcé, plantillas et IA, erreurs fréquentes),
   avec cinq photos déjà présentes dans assets/ (texte alternatif dans chaque langue) et des liens vers des pages
   existantes du site (articles du blog dans la langue de la section). Faits sur WebAutonomos : VERITE.md §2, §4 ;
   prix freelance et agence : VERITE.md §7 (Social Media Pymes, lien vers la source).
3. Composant GuideSection (entre les marqueurs « guide-accueil »), affiché entre les avis et la FAQ de l'accueil.
   Il ne s'affiche que si la langue a un bloc guide : en et fr n'en ont pas (leurs accueils sont /en/ et /fr/).
4. Repli <div id="fallback"> et JSON-LD FAQPage du <head> : régénérés depuis translations.es, avec les fonctions
   de patch_prix_iva_accueil_20261007.py, plus le guide entre les avis et la FAQ. Avant d'écrire, le script
   vérifie qu'elles reproduisent à l'identique le repli et la FAQPage en place (sinon il s'arrête).

Les blocs en et fr ne changent pas ; dans le bloc val, seul le guide est ajouté (les reformulations espagnoles
gardent leur sens, le valencien reste juste). Le <title>, la meta description, les balises de partage, les
hreflang et les autres JSON-LD ne changent pas. Rejouable : un second passage ne change rien. À lancer depuis la
racine du dépôt :
  python3 _tools/patch_home_es_20261015.py [--sortie FICHIER]
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


def js(t):
    return json.dumps(t, ensure_ascii=False)


# ───────────────────────── 1. reformulations du bloc es ─────────────────────────
REMPLACEMENTS = [
    # Avantages, comparaison, étapes, carte tarifaire, appel final
    ('benefit3Desc:"Tu nombre de empresa con extensión profesional"', 'benefit3Desc:"Una dirección propia para tu negocio"'),
    ('benefit4Desc:"Cancela cuando quieras, sin penalizaciones"', 'benefit4Desc:"Cancela en cualquier momento, sin penalizaciones"'),
    ('"<strong>Precio fijo y claro:</strong> 15€/mes + IVA, todo incluido.', '"<strong>Cuota fija y clara:</strong> 15€/mes + IVA, todo incluido.'),
    ('"<strong>Tu web en 24 horas:</strong> Creamos tu web antes de que pagues.', '"<strong>Tu web en 24 horas:</strong> la creamos antes de que pagues.'),
    ('step3Desc:"Aceptas, pagas 15€/mes + IVA y tu web está en línea con tu dominio."',
     'step3Desc:"Aceptas, pagas 15€/mes + IVA y queda en línea con tu dominio."'),
    ('item1:"Diseño web profesional"', 'item1:"Diseño personalizado"'),
    ('subtitle:"Creamos tu web gratis. Solo pagas si te gusta."', 'subtitle:"La creamos gratis. Solo pagas si te gusta."'),
    # FAQ
    ('Los 15€/mes cubren todo lo necesario para tener tu web en marcha: diseño web profesional y personalizado, hosting, '
     'dominio .es incluido el primer año (renovación ~12€/año después), certificado SSL para que tu web sea segura (https), '
     'mantenimiento técnico continuo, copias de seguridad automáticas, y soporte por email y WhatsApp. No hay pagos de '
     'instalación, ni comisiones ocultas, ni costes de activación.',
     'Los 15€/mes cubren todo lo necesario para tenerlo todo en marcha: diseño web personalizado, hosting, dominio .es '
     'incluido el primer año (renovación ~12€/año después), certificado SSL (https), mantenimiento técnico continuo, copias '
     'de seguridad automáticas y soporte por email y WhatsApp. No hay cuotas de instalación, ni comisiones ocultas, ni gastos '
     'de activación.'),
    ('a:"Tu web estará lista en menos de 24 horas, gracias a nuestro método Déjà-Fait. Así funciona: primero creamos una demo '
     'personalizada con tu información (nombre, servicios, zona, colores de tu marca). Te la enviamos por email y WhatsApp para '
     'que la revises tranquilamente. Nos dices si quieres cambios (textos, fotos, colores, secciones...) y los hacemos antes de '
     'publicarla, sin límite de ajustes. Cuando apruebes el diseño final, conectamos tu dominio y tu web está online."',
     'a:"En menos de 24 horas, con nuestro método Déjà-Fait. Así funciona: primero creamos una demo personalizada con tu '
     'información (tu negocio, lo que ofreces, tu zona, los colores de tu marca). Te la enviamos por email y WhatsApp para que '
     'la revises tranquilamente. Nos indicas los cambios que deseas (textos, fotos, colores, secciones...) y los hacemos antes '
     'de publicarla, sin límite de ajustes. Cuando apruebes el diseño final, conectamos tu dominio y queda online."'),
    ('Cancelas cuando quieras, es así de simple.', 'Cancelas cuando lo decidas, es así de simple.'),
    ('Incluso podemos ayudarte con la migración si lo necesitas. Creemos que la mejor forma de retenerte es dándote un buen '
     'servicio, no atándote con contratos."', 'Incluso podemos ayudarte con la migración."'),
    ('textos optimizados para SEO,', 'textos pensados para buscadores,'),
    ('ni dedicarle tiempo. No tendrás que tocar código, ni paneles de control, ni gestionar nada técnico. Para cualquier',
     'ni dedicarle tiempo. Para cualquier'),
    ('Sí, es nuestra filosofía de trabajo. Creamos tu web personalizada ANTES de que pagues ni un céntimo.',
     'Sí, es nuestra filosofía de trabajo: la creamos personalizada ANTES de que pagues ni un céntimo.'),
    ('podrás ver exactamente cómo quedará tu web: diseño, colores, textos, fotos, todo. La revisas con calma, la enseñas a quien '
     'quieras, y nos dices si quieres cambios.',
     'podrás ver exactamente cómo quedará: diseño, colores, textos, fotos, todo. La revisas con calma, se la enseñas a quien te '
     'parezca y nos dices qué cambiarías.'),
    ('{q:"¿Qué incluye el servicio de mantenimiento?",', '{q:"¿En qué consiste el mantenimiento?",'),
    ('copias de seguridad automáticas diarias (si algo falla, podemos restaurarla)', 'copias automáticas diarias (si algo falla, podemos restaurarla)'),
    ('con respuesta en el día. Básicamente, nos encargamos de que tu web funcione perfectamente para que tú te centres en tu '
     'negocio."', 'con respuesta en el día."'),
    ('Después de la publicación de tu web, tienes derecho a una modificación al mes, sin límite de tiempo: actualizar textos y '
     'descripciones de servicios, cambiar fotos e imágenes, modificar horarios y datos de contacto, añadir nuevos servicios o '
     'eliminar los que ya no ofreces,',
     'Después de la publicación, tienes derecho a una modificación al mes, sin límite de tiempo: actualizar textos y '
     'descripciones, cambiar fotos e imágenes, modificar horarios, teléfono o dirección, añadir servicios nuevos o eliminar los '
     'que ya no ofreces,'),
    ('{q:"¿Puedo tener mi página web en varios idiomas?",a:"Sí. En WebAutonomos, tu página web puede estar en hasta cuatro idiomas',
     '{q:"¿Puedo tener mi página en varios idiomas?",a:"Sí. Con WebAutonomos, puede estar en hasta cuatro idiomas'),
    ('para que tus clientes te encuentren en Google en su idioma.', 'para que tus clientes te encuentren en su idioma.'),
    ('Registramos el dominio .es directamente a tu nombre con tus datos de contacto.', 'Registramos el dominio .es directamente a tu nombre.'),
    ('El primer año está incluido en el precio, y después', 'El primer año está incluido, y después'),
    ('Te damos los códigos de transferencia y te ayudamos con el proceso si lo necesitas.',
     'Te damos los códigos de transferencia y te ayudamos con el proceso.'),
    ('a:"Para crear una página que funcione, lo esencial es', 'a:"Para que funcione, lo esencial es'),
    ('Todo eso viene en tu página de WebAutonomos, adaptado', 'Todo eso viene incluido con WebAutonomos, adaptado'),
    ('puedes crear tu página tú mismo,', 'puedes crearla tú mismo,'),
    ('sin que pierdas tiempo en la parte técnica. Para comparar opciones, tenemos una comparativa de los 6 creadores de webs '
     'para autónomos."', 'sin que pierdas tiempo en la parte técnica."'),
    ('puede aparecer en la búsqueda de Google y reúne', 'puede aparecer en los resultados de búsqueda y reúne'),
    ('con un presupuesto aparte: el comercio electrónico', 'que se presupuesta aparte: el comercio electrónico'),
    ('Redactamos esos tres textos y los incluimos en tu página.', 'Redactamos esos tres textos y los incluimos.'),
    ('a:"Una página no hace milagros, pero trabaja por ti', 'a:"No hace milagros, pero trabaja por ti'),
    ('cuando alguien de tu zona busca tus servicios.', 'cuando alguien de tu zona necesita lo que ofreces.'),
    ('El servicio incluye 4 artículos de blog al mes', 'Con él tienes 4 artículos de blog al mes'),
    ('Puedes contratarlo aunque tu web no esté hecha con nosotros.', 'Puedes contratarlo aunque tu página no esté hecha con nosotros.'),
    ('desc:"Posicionamiento en Google para tu zona"', 'desc:"Posicionamiento en buscadores para tu zona"'),
    ('{q:"¿Qué incluye la gestión de tu ficha de Google?",', '{q:"¿En qué consiste la gestión de tu ficha de Google?",'),
    ('Incluye la optimización de tu ficha', 'Abarca la optimización de tu ficha'),
    ('Si aún no tienes ficha de Google, la creamos', 'Si aún no tienes ficha, la creamos'),
    ('Con la gestión de tu ficha de Google (29€/mes + IVA) nos encargamos', 'Con este servicio (29€/mes + IVA) nos encargamos'),
    ('También puedes contratarla sin la web.', 'También puedes contratarlo por separado.'),
]

# ───────────────────────── 2. guide (es, val) ─────────────────────────
CL = 'text-blue-600 font-semibold hover:underline'
SOURCE = 'https://www.socialmediapymes.com/cuanto-cuesta-una-web/'  # VERITE.md §7


def a(href, texte):
    ext = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
    return '<a href="%s" class="%s"%s>%s</a>' % (href, CL, ext, texte)


def img(fichier, alt):
    return {'img': {'file': fichier, 'v': '1', 'width': 1600, 'height': 900, 'alt': alt}}


GUIDE_ES = {'sections': [
    {'id': 'guia-por-que', 'title': '¿Qué gana un autónomo con tener su propio sitio en internet?', 'items': [
        {'p': 'Gana un escaparate abierto a cualquier hora. Muchos de tus clientes te buscarán desde el móvil antes de llamarte, '
              'y ahí encuentran lo esencial: qué haces, en qué área trabajas, qué opinan otros clientes y cómo escribirte.'},
        {'p': 'Su principal beneficio es reunir en un solo lugar lo que alguien necesita para decidirse:'},
        {'ul': [
            '<strong>Confianza.</strong> Quien no te conoce ve tus trabajos, tu zona y tus opiniones antes de escribirte.',
            '<strong>Contactos a cualquier hora.</strong> Te escriben a través del formulario, que envía cada solicitud a tu '
            'correo, o del botón de WhatsApp mientras estás en una obra o en consulta.',
            '<strong>Menos llamadas repetidas.</strong> Horarios, tarifas y forma de trabajar quedan explicados una vez, y así '
            'puedes responder antes a quien ya tiene claro lo que necesita.',
            '<strong>Visibilidad en tu zona.</strong> Bien trabajada, puede aparecer en la búsqueda local cuando alguien de Elche '
            'o de Alicante necesita lo que haces.']},
        img('small-business-owner-website-spain', 'Una autónoma con delantal revisa la web de su tienda en un portátil y en el '
            'móvil, en una terraza de Valencia al atardecer'),
    ]},
    {'id': 'guia-pasos', 'title': 'Los pasos para crear tu sitio web de autónomo', 'items': [
        {'p': 'Tanto si lo haces tú como si lo encargas, el camino tiene las mismas etapas. Seguirlas en orden evita rehacer '
              'tareas y alargar el plazo.'},
        {'h3': 'Fija el objetivo'},
        {'p': 'Cada negocio parte de una necesidad distinta. En el caso de un fontanero de Valencia, lo primero es el teléfono '
              'para urgencias; para una psicóloga, que pedir cita sea fácil; para una empresa de reformas, recibir peticiones de '
              'presupuestos, y para una tienda, las ventas. Ese objetivo decide la estructura: qué va arriba, qué botón se ve primero y cuántas secciones hacen '
              'falta.'},
        {'p': 'Un análisis rápido de dos o tres competidores de tu zona te muestra qué explican ellos y qué podrías contar mejor tú.'},
        {'h3': 'Prepara los contenidos'},
        {'p': 'Reúne lo que tus clientes quieren saber: lo que ofreces explicado con palabras sencillas, tu área de actuación (por '
              'ejemplo, Elda, Petrer y alrededores), tus horarios, las mejores fotos de trabajos terminados y las opiniones que ya '
              'tienes. Unos contenidos propios, escritos para tu negocio y no copiados, son la base de todo lo demás.'},
        {'p': 'Si escribir no es lo tuyo, te explicamos ' + a('/blog/es/crear-contenido-web-sin-saber-escribir',
                                                              'cómo redactar tus textos sin saber escribir') + '.'},
        img('crear-contenido-web-artesano-grabando', 'Un herrero artesano explica su oficio junto a un pequeño micrófono, '
            'mientras al fondo se trabaja el metal con una amoladora.'),
        {'h3': 'Elige quién la hace'},
        {'p': 'Hay tres caminos: hacerla tú con una herramienta de plantillas, encargar el desarrollo a un freelance o a una '
              'agencia, que trabajan por proyectos, o confiarla a un servicio que lo prepara todo por una cuota. Más abajo '
              'comparamos lo que supone cada opción.'},
        {'h3': 'Dominio, alojamiento y textos legales'},
        {'p': 'El dominio es tu dirección en internet (tunegocio.es), parte de tu imagen empresarial, y conviene que sea de tu propiedad, para llevártelo si '
              'cambias de proveedor. El alojamiento lo mantiene todo funcionando, con su certificado SSL. Y no pueden faltar los '
              'textos legales que exige la normativa española. Te lo contamos en '
              + a('/blog/es/como-elegir-dominio-web-negocio', 'cómo elegir el dominio de tu negocio') + ' y en '
              + a('/blog/es/aviso-legal-privacidad-cookies-web', 'la guía de textos legales') + '.'},
        {'h3': 'Publica, conecta y revisa'},
        {'p': 'Una vez publicado, enlázalo desde tu ficha de Google y tus perfiles, comprueba que se ve bien en el móvil y revisa '
              'cada pocos meses que horarios, tarifas y fotos siguen al día. Así podrás mejorar lo que no funcione. Es una '
              'estrategia sencilla: que todo lo que publicas diga lo mismo; las pequeñas mejoras, mes a mes, se acumulan. Aquí '
              'tienes ' + a('/blog/es/optimizar-ficha-google-business-profile', 'cómo optimizar tu ficha paso a paso') + '.'},
    ]},
    {'id': 'guia-precio', 'title': '¿Cuánto vale una página web para autónomos?', 'items': [
        {'p': 'Depende de quién se encargue y de la necesidad de tu negocio. Como referencia, los proyectos encargados a un '
              'freelance van de 800 € a 2.000 €, y los de una agencia, de 1.500 € a 4.000 €, sin contar el mantenimiento, según '
              + a(SOURCE, 'Social Media Pymes') + ' (2026).'},
        {'table': {'head': ['Opción', 'Inversión', 'Quién se encarga', 'A tener en cuenta'], 'highlight': 3, 'rows': [
            ['Tú, con un creador de webs', 'La suscripción de la herramienta y tu tiempo',
             'Tú: textos, fotos, configuración y mantenimiento', 'Control completo; el resultado depende de las horas que le dediques'],
            ['Freelance', 'Entre 800 € y 2.000 €', 'Una sola persona, con tu ayuda', 'Mantenimiento aparte'],
            ['Agencia', 'Entre 1.500 € y 4.000 €', 'Un equipo, con un desarrollo a medida', 'Mantenimiento aparte'],
            ['WebAutonomos', '15 €/mes + IVA en alquiler o 349 € + IVA en propiedad', 'Nosotros, a partir de tu ficha y tus fotos',
             'Demo en menos de 24 horas, antes de pagar; una modificación al mes incluida']]}},
        {'p': 'Alquiler significa pagar 15 €/mes + IVA, sin pago inicial ni permanencia. Propiedad significa un pago único de '
              '349 € + IVA: pagas una vez y es tuya. Las dos fórmulas incluyen lo mismo, y si empiezas en alquiler puedes pasar '
              'después a la propiedad con un 10 % de descuento sobre los 349 €.'},
        {'p': 'En nuestro caso, tras tu solicitud, ves la demo antes de pagar: funciona como una prueba sin compromiso y, si no te convence, no pagas '
              'nada. Consulta ' + a('/precios', 'todas las tarifas') + ', lee '
              + a('/blog/es/cuanto-cuesta-pagina-web-autonomos-espana', 'nuestra guía sobre el coste real de cada opción en España')
              + ' o ' + a('/pide-tu-demo', 'pide tu demo gratis') + '.'},
        img('cuanto-cuesta-web-presupuesto-restaurante', 'Una pareja de restauradores conversa en una mesa de su comedor vacío '
            'antes del servicio, con dos tazas de café.'),
    ]},
    {'id': 'guia-plantillas-ia', 'title': 'Plantillas, inteligencia artificial o un sitio hecho para ti', 'items': [
        {'p': 'Los creadores con plantillas y las herramientas de IA son soluciones rápidas para empezar en poco tiempo, pero los '
              'textos, las fotos y la puesta a punto siguen siendo tareas tuyas.'},
        img('inteligencia-artificial-autonoma-despacho', 'Una traductora autónoma dicta a su teléfono sobre un soporte en un '
            'despacho luminoso lleno de plantas.'),
        {'h3': 'Cuándo son una buena solución'},
        {'p': 'Si te gusta la parte técnica y tienes tiempo, son una buena opción: puedes crear el tuyo eligiendo un modelo, '
              'cambiando colores y añadiendo secciones sin saber programar. Algunas herramientas de IA hasta proponen unos '
              'primeros textos.'},
        {'h3': 'Lo que siguen pidiendo de ti'},
        {'ul': [
            'Textos que expliquen tu oficio a tu manera: los genéricos se parecen a los de cualquier otro negocio.',
            'Configurar el dominio, el correo electrónico, los textos legales y, si los usas, los sistemas de reservas o de pago.',
            'Cuidar el rendimiento: una carga rápida y una navegación accesible desde cualquier teléfono.',
            'Mantenerlo al día con el paso de los años: actualizaciones, copias y cambios.']},
        {'p': 'Si prefieres no dedicarle esas horas, en WebAutonomos no partimos de una plantilla genérica: escribimos los textos '
              'con la información de tu ficha, montamos todo y nos ocupamos del mantenimiento técnico. Para comparar herramientas, '
              'consulta ' + a('/mejores-creadores-paginas-web-autonomos', 'los 6 creadores de webs para autónomos') + ', '
              + a('/blog/es/wix-o-wordpress', 'Wix o WordPress') + ' y '
              + a('/blog/es/inteligencia-artificial-autonomos-herramientas', 'herramientas de IA para autónomos') + '.'},
    ]},
    {'id': 'guia-errores', 'title': 'Errores frecuentes que te hacen perder clientes', 'items': [
        {'p': 'Revisa si alguno de estos fallos te suena: casi todos se arreglan sin empezar de cero.'},
        {'ul': [
            '<strong>No decir dónde trabajas.</strong> Si tu zona no aparece, un vecino de Alicante no sabe si te desplazas hasta '
            'su casa.',
            '<strong>Ponérselo difícil para escribirte.</strong> El teléfono, el botón de WhatsApp y el formulario deben verse a '
            'primera vista.',
            '<strong>Fotos de banco de imágenes.</strong> Una foto real, hecha por ti, transmite más calidad y confianza que una '
            'genérica.',
            '<strong>Una carga lenta en el móvil.</strong> Si tarda o se ve mal en el teléfono, puedes perder la visita antes de '
            'que lea nada. Lo explicamos en ' + a('/blog/es/velocidad-web-y-posicionamiento', 'velocidad y posicionamiento') + '.',
            '<strong>Horarios que no coinciden.</strong> Si tu ficha dice una cosa y tu sitio otra, nadie sabe cuál creer.']},
        img('elementos-web-profesional-muestras-maquette-es', 'Ejemplo de web de interiorismo en un portátil y un móvil: Estudio '
            'Nido, con una diseñadora organizando muestras de materiales.'),
        {'p': 'Para repasar uno a uno lo imprescindible, lee ' + a('/blog/es/que-debe-tener-web-profesional-autonomo',
                                                                 'los siete elementos que no pueden faltar')
              + ' y, si quieres verlo aplicado a tu oficio, ' + a('/pide-tu-demo', 'pide tu demo') + '.'},
    ]},
]}

GUIDE_VAL = {'sections': [
    {'id': 'guia-per-que', 'title': 'Què guanya un autònom amb tindre el seu propi lloc en internet?', 'items': [
        {'p': "Guanya un aparador obert a qualsevol hora. Molts dels teus clients et buscaran des del mòbil abans de telefonar-te, "
              "i allí troben l'essencial: què fas, en quina àrea treballes, què opinen altres clients i com escriure't."},
        {'p': "El seu principal benefici és reunir en un sol lloc el que algú necessita per a decidir-se:"},
        {'ul': [
            "<strong>Confiança.</strong> Qui no et coneix veu els teus treballs, la teua zona i les teues opinions abans "
            "d'escriure't.",
            "<strong>Contactes a qualsevol hora.</strong> T'escriuen a través del formulari, que envia cada sol·licitud al teu "
            "correu, o del botó de WhatsApp mentre estàs en una obra o en consulta.",
            "<strong>Menys telefonades repetides.</strong> Horaris, tarifes i manera de treballar queden explicats una vegada, i "
            "així pots respondre abans a qui ja té clar el que necessita.",
            "<strong>Visibilitat en la teua zona.</strong> Ben treballada, pot aparéixer en les cerques locals quan algú d'Elx o "
            "d'Alacant necessita el que fas."]},
        img('small-business-owner-website-spain', "Una autònoma amb davantal revisa la web de la seua botiga al portàtil i al "
            "mòbil, en una terrassa de València al capvespre"),
    ]},
    {'id': 'guia-passos', 'title': "Els passos per a crear el teu lloc web d'autònom", 'items': [
        {'p': "Tant si el fas tu com si l'encarregues, el camí té les mateixes etapes. Seguir-les en orde evita refer tasques i "
              "allargar el termini."},
        {'h3': "Fixa l'objectiu"},
        {'p': "Cada negoci partix d'una necessitat diferent. En el cas d'un fontaner de València, el primer és el telèfon per a "
              "urgències; per a una psicòloga, que demanar cita siga fàcil; per a una empresa de reformes, rebre peticions de "
              "pressupostos, i per a una botiga, les vendes. Eixe objectiu decidix l'estructura: què va dalt, quin botó es veu primer i quantes seccions fan falta."},
        {'p': "Una anàlisi ràpida de dos o tres competidors de la teua zona et mostra què expliquen ells i què podries contar "
              "millor tu."},
        {'h3': 'Prepara els continguts'},
        {'p': "Reunix el que els teus clients volen saber: el que oferixes explicat amb paraules senzilles, la teua àrea d'actuació "
              "(per exemple, Elda, Petrer i rodalia), els teus horaris, les millors fotos de treballs acabats i les opinions que ja "
              "tens. Uns continguts propis, escrits per al teu negoci i no copiats, són la base de tota la resta."},
        {'p': "Si escriure no és el teu fort, t'expliquem " + a('/blog/val/crear-contingut-sense-saber-escriure',
                                                               'com redactar els teus textos sense saber escriure') + '.'},
        img('crear-contenido-web-artesano-grabando', "Un ferrer artesà explica el seu ofici al costat d'un micròfon menut, mentre "
            "al fons treballen el metall amb una esmoladora."),
        {'h3': 'Tria qui la fa'},
        {'p': "Hi ha tres camins: fer-la tu amb una eina de plantilles, encarregar el desenvolupament a un freelance o a una "
              "agència, que treballen per projectes, o confiar-la a un servei que ho prepara tot per una quota. Més avall comparem "
              "el que suposa cada opció."},
        {'h3': 'Domini, allotjament i textos legals'},
        {'p': "El domini és la teua adreça en internet (elteunegoci.es), part de la teua imatge empresarial, i convé que siga de la teua propietat, per a endur-te'l si "
              "canvies de proveïdor. L'allotjament ho manté tot funcionant, amb el seu certificat SSL. I no poden faltar els textos "
              "legals que exigix la normativa espanyola. T'ho contem en "
              + a('/blog/val/triar-el-domini-del-teu-negoci', 'com triar el domini del teu negoci') + ' i en '
              + a('/blog/val/avis-legal-privacitat-cookies-web', 'la guia de textos legals') + '.'},
        {'h3': 'Publica, connecta i revisa'},
        {'p': "Una vegada publicat, enllaça'l des de la teua fitxa de Google i els teus perfils, comprova que es veu bé en el mòbil "
              "i revisa cada pocs mesos que horaris, tarifes i fotos continuen al dia. Així podràs millorar el que no funcione. És "
              "una estratègia senzilla: que tot el que publiques diga el mateix; les xicotetes millores, mes a mes, s'acumulen. "
              "Ací tens " + a('/blog/val/optimitzar-fitxa-google-business-profile', 'com optimitzar la teua fitxa pas a pas') + '.'},
    ]},
    {'id': 'guia-preu', 'title': 'Quant val una pàgina web per a autònoms?', 'items': [
        {'p': "Depén de qui se n'encarregue i de la necessitat del teu negoci. Com a referència, els projectes encarregats a un "
              "freelance van de 800 € a 2.000 €, i els d'una agència, de 1.500 € a 4.000 €, sense comptar el manteniment, segons "
              + a(SOURCE, 'Social Media Pymes') + ' (2026).'},
        {'table': {'head': ['Opció', 'Inversió', "Qui se n'encarrega", 'A tindre en compte'], 'highlight': 3, 'rows': [
            ['Tu, amb un creador de webs', "La subscripció de l'eina i el teu temps",
             'Tu: textos, fotos, configuració i manteniment', 'Control complet; el resultat depén de les hores que hi dediques'],
            ['Freelance', 'Entre 800 € i 2.000 €', 'Una sola persona, amb la teua ajuda', 'Manteniment a banda'],
            ['Agència', 'Entre 1.500 € i 4.000 €', 'Un equip, amb un desenvolupament a mida', 'Manteniment a banda'],
            ['WebAutonomos', '15 €/mes + IVA en lloguer o 349 € + IVA en propietat',
             'Nosaltres, a partir de la teua fitxa i les teues fotos',
             'Demo en menys de 24 hores, abans de pagar; una modificació al mes inclosa']]}},
        {'p': "Lloguer significa pagar 15 €/mes + IVA, sense pagament inicial ni permanència. Propietat significa un pagament únic "
              "de 349 € + IVA: pagues una vegada i és teua. Les dues fórmules inclouen el mateix, i si comences en lloguer pots "
              "passar després a la propietat amb un 10 % de descompte sobre els 349 €."},
        {'p': "En el nostre cas, després de la teua sol·licitud, veus la demo abans de pagar: funciona com una prova sense compromís i, si no et convenç, no pagues "
              "res. Consulta " + a('/precios', 'totes les tarifes') + ', llig '
              + a('/blog/val/quant-costa-una-pagina-web-per-a-autonoms', 'la nostra guia sobre el cost real de cada opció a Espanya')
              + ' o ' + a('/pide-tu-demo', 'demana la teua demo gratis') + '.'},
        img('cuanto-cuesta-web-presupuesto-restaurante', "Una parella de restauradors conversa en una taula del menjador buit "
            "abans del servici, amb dues tasses de café."),
    ]},
    {'id': 'guia-plantilles-ia', 'title': 'Plantilles, intel·ligència artificial o un lloc web fet per a tu', 'items': [
        {'p': "Els creadors amb plantilles i les eines d'IA són solucions ràpides per a començar en poc temps, però els textos, les "
              "fotos i la posada a punt continuen sent tasques teues."},
        img('inteligencia-artificial-autonoma-despacho', "Una traductora autònoma dicta al mòbil sobre un suport en un despatx "
            "lluminós ple de plantes."),
        {'h3': 'Quan són una bona solució'},
        {'p': "Si t'agrada la part tècnica i tens temps, són una bona opció: pots crear el teu triant un model, canviant colors i "
              "afegint seccions sense saber programar. Algunes eines d'IA fins i tot proposen uns primers textos."},
        {'h3': 'El que continuen demanant-te'},
        {'ul': [
            "Textos que expliquen el teu ofici a la teua manera: els genèrics s'assemblen als de qualsevol altre negoci.",
            "Configurar el domini, el correu electrònic, els textos legals i, si els utilitzes, els sistemes de reserves o de "
            "pagament.",
            "Cuidar el rendiment: una càrrega ràpida i una navegació accessible des de qualsevol telèfon.",
            "Mantindre-ho al dia amb el pas dels anys: actualitzacions, còpies i canvis."]},
        {'p': "Si preferixes no dedicar-hi eixes hores, en WebAutonomos no partim d'una plantilla genèrica: escrivim els textos amb "
              "la informació de la teua fitxa, ho muntem tot i ens ocupem del manteniment tècnic. Per a comparar eines, consulta "
              + a('/mejores-creadores-paginas-web-autonomos', 'els 6 creadors de webs per a autònoms') + ' (en castellà), '
              + a('/blog/val/wix-o-wordpress', 'Wix o WordPress') + ' i '
              + a('/blog/val/ia-per-a-autonoms-eines-concretes', "eines d'IA per a autònoms") + '.'},
    ]},
    {'id': 'guia-errors', 'title': 'Errors freqüents que et fan perdre clients', 'items': [
        {'p': "Revisa si alguna d'estes errades et sona: quasi totes s'arreglen sense començar de zero."},
        {'ul': [
            "<strong>No dir on treballes.</strong> Si la teua zona no apareix, un veí d'Alacant no sap si et desplaces fins a sa "
            "casa.",
            "<strong>Posar-ho difícil per a escriure't.</strong> El telèfon, el botó de WhatsApp i el formulari s'han de veure a "
            "primera vista.",
            "<strong>Fotos de bancs d'imatges.</strong> Una foto real, feta per tu, transmet més qualitat i confiança que una de "
            "genèrica.",
            "<strong>Una càrrega lenta en el mòbil.</strong> Si tarda o es veu malament en el telèfon, pots perdre la visita abans "
            "que llija res. Ho expliquem en " + a('/blog/val/velocitat-de-la-web-i-posicionament', 'velocitat i posicionament')
            + '.',
            "<strong>Horaris que no coincidixen.</strong> Si la teua fitxa diu una cosa i el teu lloc web una altra, ningú sap "
            "quina creure."]},
        img('elementos-web-profesional-muestras-maquette-val', "Exemple de web d'interiorisme en un portàtil i un mòbil: Estudi "
            "Niu, amb una interiorista organitzant mostres de materials."),
        {'p': "Per a repassar un per un l'imprescindible, llig " + a('/blog/val/elements-imprescindibles-d-una-web',
                                                                   'els set elements que no poden faltar')
              + ' i, si vols veure-ho aplicat al teu ofici, ' + a('/pide-tu-demo', 'demana la teua demo') + '.'},
    ]},
]}

# ───────────────────────── 3. composant de l'application ─────────────────────────
MARQUE_DEBUT = '/* guide-accueil:debut */'
MARQUE_FIN = '/* guide-accueil:fin */'
COMPOSANT = MARQUE_DEBUT + (
    '// Guide section (translations.es.guide, translations.val.guide), posee par _tools/patch_home_es_20261015.py\n'
    'const GuideSection=()=>{const{t}=useLanguage();const g=t.guide;if(!g||!g.sections)return null;const h=React.createElement;'
    'const raw=x=>({__html:x});'
    'const item=(it,k)=>{'
    'if(it.p)return h("p",{key:k,className:"text-gray-700 text-lg leading-relaxed mb-4",dangerouslySetInnerHTML:raw(it.p)});'
    'if(it.h3)return h("h3",{key:k,className:"text-xl md:text-2xl font-bold text-gray-800 mt-10 mb-3"},it.h3);'
    'if(it.ul)return h("ul",{key:k,className:"list-disc pl-6 space-y-2 text-gray-700 text-lg leading-relaxed mb-6"},'
    'it.ul.map((x,i)=>h("li",{key:i,dangerouslySetInnerHTML:raw(x)})));'
    'if(it.img){const b="/assets/"+it.img.file,v="?v="+it.img.v;return h("figure",{key:k,className:"my-8"},h("picture",null,'
    'h("source",{type:"image/webp",srcSet:b+"-800.webp"+v+" 800w, "+b+".webp"+v+" "+it.img.width+"w",'
    'sizes:"(max-width: 800px) calc(100vw - 32px), 768px"}),'
    'h("img",{src:b+".jpg"+v,alt:it.img.alt,width:it.img.width,height:it.img.height,loading:"lazy",decoding:"async",'
    'className:"w-full h-auto rounded-2xl shadow-sm"})));}'
    'if(it.table){const tb=it.table;return h("div",{key:k,className:"overflow-x-auto my-8 rounded-2xl border border-gray-200 bg-white"},'
    'h("table",{className:"w-full min-w-[640px] text-left text-base"},'
    'h("thead",{className:"bg-gray-100"},h("tr",null,tb.head.map((x,i)=>h("th",{key:i,scope:"col",className:"p-4 font-bold text-gray-800"},x)))),'
    'h("tbody",null,tb.rows.map((r,i)=>h("tr",{key:i,className:"border-t border-gray-200"+(i===tb.highlight?" bg-green-50":"")},'
    'r.map((x,j)=>j?h("td",{key:j,className:"p-4 text-gray-700 align-top",dangerouslySetInnerHTML:raw(x)})'
    ':h("th",{key:j,scope:"row",className:"p-4 font-semibold text-gray-800 align-top",dangerouslySetInnerHTML:raw(x)})))))));}'
    'return null;};'
    'return h("section",{id:"guia",className:"py-20 bg-gray-50"},h("div",{className:"max-w-3xl mx-auto px-4"},'
    'g.sections.map((s,i)=>h("div",{key:s.id,id:s.id,className:(i?"mt-16 ":"")+"scroll-mt-24"},'
    'h("h2",{className:"text-3xl md:text-4xl font-bold text-gray-800 mb-6"},s.title),s.items.map(item)))));};\n'
) + MARQUE_FIN + '\n'
ANCRE_COMPOSANT = 'const FAQSection='
ACCUEIL = ('React.createElement(TestimonialsSection,null),/*#__PURE__*/React.createElement(FAQSection,null)',
           'React.createElement(TestimonialsSection,null),/*#__PURE__*/React.createElement(GuideSection,null),'
           '/*#__PURE__*/React.createElement(FAQSection,null)')


# ───────────────────────── outils ─────────────────────────
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


def litteral(v):
    """Littéral JavaScript (clés sans guillemets, chaînes en JSON)."""
    if isinstance(v, dict):
        return '{' + ','.join('%s:%s' % (k, litteral(x)) for k, x in v.items()) + '}'
    if isinstance(v, list):
        return '[' + ','.join(litteral(x) for x in v) + ']'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    return js(v)


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


def ea(x):
    return html.escape(x, quote=True)


def repli_guide(g):
    """Le guide dans le repli statique : mêmes éléments, même ordre que GuideSection."""
    L = []
    for sec in g['sections']:
        L += ['', '    <h2>%s</h2>' % e(sec['title'])]
        for it in sec['items']:
            if 'p' in it:
                L.append('    <p>%s</p>' % it['p'])
            elif 'h3' in it:
                L.append('    <h3>%s</h3>' % e(it['h3']))
            elif 'ul' in it:
                L += ['    <ul>'] + ['      <li>%s</li>' % x for x in it['ul']] + ['    </ul>']
            elif 'img' in it:
                m = it['img']
                b, v = '/assets/' + m['file'], '?v=' + m['v']
                L += ['    <figure>', '      <picture>',
                      '        <source type="image/webp" srcset="%s-800.webp%s 800w, %s.webp%s %sw" sizes="(max-width: 800px) '
                      'calc(100vw - 32px), 768px">' % (b, v, b, v, m['width']),
                      '        <img src="%s.jpg%s" alt="%s" width="%s" height="%s" loading="lazy" decoding="async">' % (
                          b, v, ea(m['alt']), m['width'], m['height']),
                      '      </picture>', '    </figure>']
            elif 'table' in it:
                tb = it['table']
                L += ['    <table>', '      <thead><tr>%s</tr></thead>' % ''.join('<th scope="col">%s</th>' % e(x) for x in tb['head']),
                      '      <tbody>']
                L += ['        <tr><th scope="row">%s</th>%s</tr>' % (r[0], ''.join('<td>%s</td>' % x for x in r[1:])) for r in tb['rows']]
                L += ['      </tbody>', '    </table>']
    return L


def repli(t):
    """Repli statique (patch_prix_iva_accueil_20261007.py), plus le guide entre les avis et la FAQ."""
    h, hw, b, c, f, p, u, ts, fq, ct = (t['hero'], t['howItWorks'], t['benefits'], t['comparison'], t['forWho'],
                                         t['pricing'], t['upsells'], t['testimonials'], t['faq'], t['cta'])
    L = ['<div id="fallback">',
         '    <h1>%s %s</h1>' % (e(h['title']), e(h['titleHighlight'])),
         '    <p>%s</p>' % e(h['subtitle']), '    <p>%s</p>' % e(h['trusted']), '',
         '    <h2>%s</h2>' % e(b['title']), '    <ul>']
    L += ['      <li><strong>%s</strong> — %s</li>' % (e(b['benefit%d' % i]), e(b['benefit%dDesc' % i])) for i in (1, 2, 3, 4)]
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
    if t.get('guide'):
        L += repli_guide(t['guide'])
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
    a_ = s.index('<div id="fallback">')
    return a_, s.index('    <ul>\n      <li><a href="/precios">', a_)


def faq_du_head(s):
    m = None
    for x in re.finditer(r'(?s)(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)', s[:s.index('<body')]):
        if '"FAQPage"' in x.group(2):
            m = x
    if not m:
        sys.exit('FAQPage introuvable dans le <head>')
    return m


def bornes_bloc(s, lang):
    """(début, fin) du bloc de la langue dans translations (accolades comprises)."""
    i0 = s.index('const translations=') + len('const translations=')
    ies = s.index('es:{', i0) + 3
    fes = fin_bloc(s, ies)
    if lang == 'es':
        return ies, fes
    if not s.startswith(',val:{', fes + 1):
        sys.exit('le bloc val ne suit pas le bloc es')
    return fes + 6, fin_bloc(s, fes + 6)


def poser_guide(s, lang, guide):
    """Ajoute (ou remplace) la clé guide du bloc de la langue, juste avant sa FAQ."""
    deb, fin = bornes_bloc(s, lang)
    bloc = s[deb:fin + 1]
    nouveau = 'guide:' + litteral(guide)
    if bloc.count(',guide:{') > 1:
        sys.exit('plusieurs clés guide dans le bloc %s' % lang)
    if ',guide:{' in bloc:
        i = bloc.index(',guide:{') + 1
        j = fin_bloc(bloc, i + 6)
        bloc = bloc[:i] + nouveau + bloc[j + 1:]
    else:
        ancre = 'faq:{title:'
        if bloc.count(ancre) != 1:
            sys.exit('ancre de la FAQ trouvée %d fois dans le bloc %s' % (bloc.count(ancre), lang))
        bloc = bloc.replace(ancre, nouveau + ',' + ancre)
    return s[:deb] + bloc + s[fin + 1:]


def verifier_guide(guide, lang):
    """Images présentes dans assets/ (jpg, webp, webp 800) et liens internes vers des pages qui existent."""
    redir = set()
    for l in open(os.path.join(ROOT, '_redirects'), encoding='utf-8'):
        p_ = l.split()
        if len(p_) >= 2 and p_[0].startswith('/'):
            redir.add(p_[0])
    for sec in guide['sections']:
        for it in sec['items']:
            if 'img' in it:
                for suffixe in ('.jpg', '.webp', '-800.webp'):
                    if not os.path.isfile(os.path.join(ROOT, 'assets', it['img']['file'] + suffixe)):
                        sys.exit('image absente (%s) : assets/%s%s' % (lang, it['img']['file'], suffixe))
            textes = [it.get('p', '')] + it.get('ul', []) + [x for r in it.get('table', {}).get('rows', []) for x in r]
            for t_ in textes:
                for href in re.findall(r'href="(/[^"#?]*)"', t_):
                    f_ = href.strip('/')
                    if href in redir or not any(os.path.isfile(os.path.join(ROOT, c)) for c in (f_, f_ + '.html', f_ + '/index.html')):
                        sys.exit('lien interne absent ou redirigé (%s) : %s' % (lang, href))


# ───────────────────────── traitement ─────────────────────────
s = open(SRC, encoding='utf-8').read()
avant = s

# 0. Les générateurs reproduisent-ils le repli et la FAQPage en place ?
t0 = lire_translations(s)['es']
a0, b0 = bornes_repli(s)
if repli(t0) + '\n' != s[a0:b0]:
    sys.exit('le repli en place diffère de celui que régénère ce script : rien n\'est écrit')
if faqpage(t0['faq']['items']) != faq_du_head(s).group(2):
    sys.exit('la FAQPage en place diffère de celle que régénère ce script : rien n\'est écrit')
verifier_guide(GUIDE_ES, 'es')
verifier_guide(GUIDE_VAL, 'val')

# 1. reformulations du bloc es
deb, fin = bornes_bloc(s, 'es')
bloc = s[deb:fin + 1]
faits, deja = 0, 0
for ancien, nouveau in REMPLACEMENTS:
    if bloc.count(nouveau) == 1 and bloc.count(ancien) == 0:
        deja += 1
        continue
    if bloc.count(ancien) != 1:
        sys.exit('ancre trouvée %d fois dans le bloc es : %s' % (bloc.count(ancien), ancien[:90]))
    bloc = bloc.replace(ancien, nouveau)
    faits += 1
s = s[:deb] + bloc + s[fin + 1:]

# 2. guide es et val
s = poser_guide(s, 'es', GUIDE_ES)
s = poser_guide(s, 'val', GUIDE_VAL)

# 3. composant et place dans l'accueil
if s.count(MARQUE_DEBUT) == 1 and s.count(MARQUE_FIN) == 1:
    i, j = s.index(MARQUE_DEBUT), s.index(MARQUE_FIN) + len(MARQUE_FIN) + 1
    s = s[:i] + COMPOSANT + s[j:]
elif s.count(MARQUE_DEBUT) == 0 and s.count(ANCRE_COMPOSANT) == 1:
    s = s.replace(ANCRE_COMPOSANT, COMPOSANT + ANCRE_COMPOSANT)
else:
    sys.exit('marqueurs du composant ou ancre « const FAQSection= » introuvables ou ambigus')
if s.count(ACCUEIL[1]) == 0:
    if s.count(ACCUEIL[0]) != 1:
        sys.exit('assemblage de l\'accueil (avis puis FAQ) trouvé %d fois' % s.count(ACCUEIL[0]))
    s = s.replace(ACCUEIL[0], ACCUEIL[1])
elif s.count(ACCUEIL[1]) != 1:
    sys.exit('GuideSection placé plusieurs fois dans l\'accueil')

# 4. repli statique et JSON-LD FAQPage du <head>
t = lire_translations(s)
if 'guide' in t['en'] or 'guide' in t['fr']:
    sys.exit('les blocs en et fr ne doivent pas avoir de guide')
t = t['es']
a0, b0 = bornes_repli(s)
s = s[:a0] + repli(t) + '\n' + s[b0:]
m = faq_du_head(s)
s = s[:m.start(2)] + faqpage(t['faq']['items']) + s[m.end(2):]

if s == avant and SORTIE == SRC:
    print('déjà appliqué : rien à changer (%d reformulations déjà en place)' % deja)
    sys.exit(0)
open(SORTIE, 'w', encoding='utf-8').write(s)
print('ok : %d reformulations (%d déjà en place), guide es et val (%d sections), composant GuideSection, repli %d mots, '
      'FAQPage %d questions (%s)' % (faits, deja, len(GUIDE_ES['sections']),
                                      len(re.sub(r'<[^>]+>', ' ', repli(t)).split()), len(t['faq']['items']), SORTIE))
