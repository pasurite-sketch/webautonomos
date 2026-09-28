# -*- coding: utf-8 -*-
"""Section « Normativa » des pages métier espagnoles du bâtiment (28/09/2026).

Les pages FR et EN des mêmes métiers ont un tableau des règles vérifiées ; les pages
espagnoles, marché principal, n'en avaient pas. Ce script ajoute à /fontaneros/,
/electricistas/, /reformas/ et /carpinteros/ une section id="normativa" : tableau
des règles espagnoles, note, « lo que preparamos en tu web » et sources.

Contenu : traduction des tableaux des pages « in Spain » (build_metier_pages.py),
vérifiés sur les sources officielles le 24/09 (menuisiers) et le 28/09/2026
(plombiers, électriciens, builders) puis relus par une vérification indépendante.
La section est placée juste avant la FAQ. Le circuit SEO doit la garder telle
quelle (REGLES_REDACTEUR.md §2, notes de pages.json).

Pages santé (/psicologos/, /dentistas/, /fisioterapeutas/) ajoutées le même jour sur
décision d'Angelino (28/09/2026) : on garde les avis Google des patients affichés sur
ces pages (décision du 25/09) et le tableau ne contient pas de ligne sur les
testimonios de pacientes (RD 1907/1996, art. 4.7). Contenu traduit des pages « in
Spain » des mêmes métiers, vérifiées le 24/09/2026 puis relues.

    python3 _tools/patch_normativa_es_20260928.py            # essai
    python3 _tools/patch_normativa_es_20260928.py --apply    # écrit
Idempotent : une page qui contient déjà id="normativa" n'est pas modifiée.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
APPLY = '--apply' in sys.argv
E = lambda t: html.escape(t, quote=False)

CSS = """
  /* NORMATIVA (patch_normativa_es_20260928.py) */
  .nrm{padding:64px 6%;}
  .nrm.nrm-off{background:var(--off);}
  .nrm.nrm-line{border-top:1px solid var(--border);}
  .nrm-in{max-width:980px;margin:0 auto;}
  .nrm-ey{text-align:center;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--green-mid);margin-bottom:10px;}
  .nrm h2{text-align:center;}
  .nrm-lead{font-size:1.02rem;line-height:1.7;color:#334155;max-width:720px;margin:14px auto 30px;text-align:center;}
  .nrm-w{overflow-x:auto;border:1.5px solid var(--border);border-radius:16px;background:var(--white);}
  table.nrm-t{width:100%;border-collapse:collapse;font-size:.92rem;line-height:1.55;color:#334155;}
  table.nrm-t th,table.nrm-t td{padding:14px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border);}
  table.nrm-t thead th{font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--blue-dark);background:var(--off);}
  table.nrm-t tbody th{font-weight:700;color:var(--blue-dark);width:22%;}
  table.nrm-t td.ley{color:#64748b;font-size:.84rem;width:24%;}
  table.nrm-t tr:last-child th,table.nrm-t tr:last-child td{border-bottom:none;}
  .nrm-note{max-width:760px;margin:20px auto 0;background:#fffbeb;border:1.5px solid #fcd34d;border-radius:12px;padding:14px 18px;font-size:.9rem;line-height:1.6;color:#78350f;}
  .nrm-we{max-width:760px;margin:26px auto 0;}
  .nrm-we h3{font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:1.1rem;color:var(--blue-dark);margin-bottom:10px;text-align:center;}
  .nrm-we ul{list-style:none;margin:0;padding:0;}
  .nrm-we li{background:var(--white);border:1.5px solid var(--border);border-radius:12px;padding:10px 14px 10px 36px;margin-bottom:8px;position:relative;font-size:.93rem;line-height:1.5;color:#334155;}
  .nrm-we li::before{content:'✓';position:absolute;left:14px;top:10px;color:var(--green-mid);font-weight:700;}
  .nrm-src{max-width:760px;margin:18px auto 0;font-size:.8rem;line-height:1.6;color:#64748b;}
  .nrm-src a{color:#64748b;}
  @media (max-width:640px){
    table.nrm-t thead{display:none;}
    table.nrm-t tr{display:block;padding:14px 16px;border-bottom:1px solid var(--border);}
    table.nrm-t tr:last-child{border-bottom:none;}
    table.nrm-t tbody th,table.nrm-t td{display:block;padding:0;border:none;width:auto;}
    table.nrm-t td.ley{margin:4px 0 8px;font-size:.8rem;width:auto;}
  }
"""

# ─── Lignes communes ────────────────────────────────────────────────────────
PRESUPUESTO = ('Presupuesto por escrito',
               'Comunitat Valenciana: Decreto 11/1995; Madrid: Decreto 35/1995; Cataluña: Código de Consumo, art. 251-3',
               'En estas comunidades, el cliente tiene derecho a un presupuesto detallado por escrito antes de empezar '
               '(en Cataluña, cuando no puede calcular el precio por sí mismo), salvo que renuncie de su puño y letra y '
               'lo firme: una renuncia preimpresa no vale.')
PRESUPUESTO_MADRID = (PRESUPUESTO[0], PRESUPUESTO[1],
                      PRESUPUESTO[2] + ' La Comunidad de Madrid indica además que las empresas de reformas deben '
                      'ofrecer una hoja informativa de precios en su web.')
RECLAMACIONES = ('Reclamaciones', 'TRLGDCU, art. 21.3; normas autonómicas',
                 'Informa al cliente de dónde puede reclamarte: como mínimo, por el mismo medio por el que empezó la '
                 'relación contigo (WhatsApp o el formulario de tu web, por ejemplo), por correo postal, por teléfono y '
                 'por un medio electrónico. Desde el 28 de diciembre de 2025 debes responder en un plazo máximo de 15 '
                 'días (antes, un mes). Las hojas oficiales son autonómicas: en Andalucía, los negocios sin local deben '
                 'mostrar un cartel con código QR en presupuestos, facturas y web.')
URGENCIAS = ('Averías urgentes', 'TRLGDCU, art. 103.h',
             'No hay derecho de desistimiento de 14 días cuando el cliente te ha pedido que vayas para una reparación '
             'o un mantenimiento urgente. Sí lo hay para los servicios adicionales que prestes en esa visita y para los '
             'bienes que no sean las piezas de recambio necesarias.')
RESENAS = ('Reseñas de clientes', 'TRLGDCU, art. 20.4; Ley 3/1991, art. 27.7 y 27.8',
           'Indica si compruebas, y cómo, que las reseñas proceden de clientes reales. Desde el 28 de diciembre de '
           '2025 deben referirse a un servicio contratado o usado en los 30 días anteriores a la reseña, y las '
           'reseñas falsas están prohibidas expresamente desde el 28 de mayo de 2022.')
AVISO = ('Aviso legal', 'LSSI (Ley 34/2002), art. 10',
         'Tu nombre o razón social, tu dirección, tu correo electrónico y otro dato de contacto directo '
         '(normalmente, el teléfono), tu NIF, los datos del Registro Mercantil si eres una S.L. y, si muestras '
         'precios, si incluyen el IVA.')
REA = ('Subcontratación (REA)', 'Ley 32/2006, arts. 2 y 4',
       'Si te contratan o subcontratan en una obra de construcción en la que hay subcontratación, debes estar '
       'inscrito en el REA, salvo que seas autónomo sin trabajadores asalariados. No hace falta mostrar el número '
       'en tu web.')
IVA10 = ('IVA del 10 %', 'Ley 37/1992, art. 91.Uno.2.10.º',
         'Renovación o reparación de una vivienda con al menos dos años, para un particular que la usa (no alquilada) '
         'o para una comunidad de propietarios, siempre que el coste de los materiales que aportes no supere el '
         '40 % de la base imponible.')
WE_AVISO = 'Un aviso legal con tu nombre, tu NIF y tus datos de contacto, y los de tu sociedad si eres una S.L.'
WE_RECL = 'La información de reclamaciones que pide tu comunidad, como el cartel con código QR en Andalucía'
NOTA = ('Información general a septiembre de 2026, que no sustituye al asesoramiento jurídico. Tú nos das los datos de '
        'tu negocio y validas cada texto antes de publicarlo.')
SRC_CONSUMO = [('Ley General para la Defensa de los Consumidores (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-20555'),
               ('LSSI, art. 10 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758')]

PAGINAS = {
    'fontaneros': dict(
        titulo='Lo que tu empresa y tu web deben cumplir',
        lead='La fontanería en sí tiene poca regulación en España, pero la calefacción, el agua caliente, el gas y la '
             'climatización exigen una empresa habilitada, y la ley de consumo fija reglas para las urgencias, los '
             'presupuestos y las reclamaciones. Esto es lo esencial.',
        filas=[
            ('Calefacción, agua caliente y climatización', 'RITE (RD 1027/2007), arts. 19 y 36 a 42',
             'Las instalaciones térmicas fijas las ejecuta una empresa instaladora habilitada: presenta una declaración '
             'responsable ante la comunidad autónoma, tiene un seguro de responsabilidad civil de al menos 300.000 € y '
             'al menos una persona en plantilla con carné profesional de instalaciones térmicas de edificios.'),
            ('Gas', 'RD 919/2006, ITC-ICG 07 y 09',
             'Las instalaciones de gas las realiza una empresa instaladora de gas (categoría A, B o C), que emite el '
             'certificado de instalación. Las viviendas con gas canalizado pasan una inspección cada cinco años, por '
             'la distribuidora o por una empresa instaladora que elija el cliente.'),
            ('Gases fluorados', 'RD 115/2017, arts. 3 y 9',
             'Instalar un split o una bomba de calor con refrigerante fluorado exige personal con certificado de gases '
             'fluorados dentro de una empresa habilitada, y los equipos precargados no herméticamente sellados, como '
             'los split, solo se venden al usuario final con prueba de que los instalará una empresa habilitada.'),
            ('Instalaciones de agua', 'CTE DB HS4; normas autonómicas',
             'No hay un carné estatal de fontanería, pero algunas comunidades tienen reglas propias: en Madrid, '
             'registrar una instalación de agua exige el certificado de una empresa instaladora de fontanería. '
             'Consulta a la dirección general de industria de tu comunidad.'),
            URGENCIAS, PRESUPUESTO, RECLAMACIONES, RESENAS, AVISO,
        ],
        nota='Las normas sobre presupuestos, hojas de reclamaciones e instalaciones de agua son autonómicas: consulta '
             'a tu comunidad autónoma. ' + NOTA,
        we=[WE_AVISO,
            'Tus condiciones de desplazamiento y tus precios para particulares con el IVA incluido',
            'Las habilitaciones que tienes (RITE, gas, gases fluorados) descritas con exactitud, y ninguna más',
            WE_RECL,
            'Botón de llamada y WhatsApp siempre visibles en el móvil, para las urgencias'],
        fuentes=[('RITE, RD 1027/2007 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2007-15820'),
                 ('Reglamento de gas, RD 919/2006 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2006-15345'),
                 ('Gases fluorados, RD 115/2017 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2017-1679'),
                 ('Fraudes en revisiones de gas (Comunidad de Madrid)',
                  'https://www.comunidad.madrid/consumo/fraudes-inspecciones-revisiones-gas')] + SRC_CONSUMO,
    ),
    'electricistas': dict(
        titulo='Lo que tu empresa y tu web deben cumplir',
        lead='En España, las instalaciones eléctricas de baja tensión están reservadas a empresas instaladoras '
             'habilitadas, y solo '
             'ellas pueden firmar el certificado que permite conectar una instalación. La ley de consumo fija además '
             'las reglas de presupuestos, urgencias y reclamaciones. Esto es lo esencial.',
        filas=[
            ('Empresa instaladora', 'REBT (RD 842/2002), art. 22; ITC-BT-03',
             'Solo una empresa instaladora en baja tensión puede instalar, mantener o reparar instalaciones de baja '
             'tensión. Presentas una declaración responsable ante la comunidad autónoma donde te establezcas; vale en '
             'toda España '
             'y sin caducidad, y la comunidad te asigna un número y comunica tus datos al Registro Integrado '
             'Industrial.'),
            ('Requisitos', 'ITC-BT-03, apartados 3, 4 y 5.8 y apéndice I',
             'Al menos un instalador en baja tensión de tu categoría (básica o especialista), con cualquier tipo de '
             'contrato desde septiembre de 2025, y un seguro de responsabilidad civil de al menos 600.000 € por '
             'siniestro en la categoría básica o 900.000 € en la especialista.'),
            ('Certificado de instalación (boletín)', 'ITC-BT-04, apartados 5.4 y 5.5; ITC-BT-03, apartado 5.9',
             'Solo la empresa que hizo el trabajo emite el certificado, firmado por uno de sus instaladores, y la '
             'distribuidora no conecta sin él. Está prohibido facilitar certificados de instalaciones que la empresa '
             'no ha realizado.'),
            ('Trabajar sin habilitación', 'Ley 21/1992 de Industria, arts. 31 y 34; Cataluña: Ley 9/2014, art. 26.4.c',
             'Ejecutar instalaciones sin haber presentado la declaración responsable es una infracción grave según la '
             'Ley de Industria. Cataluña tiene su propio régimen, que la califica de muy grave.'),
            ('Puntos de recarga', 'ITC-BT-52 (RD 1053/2014); ITC-BT-03, apartado 3; Ley de Propiedad Horizontal, art. 17.5',
             'Cualquier empresa instaladora en baja tensión puede instalarlos: basta la categoría básica. En una '
             'comunidad, el propietario que instala un punto de recarga para uso privado en su plaza individual de '
             'garaje solo tiene que comunicarlo antes a la comunidad.'),
            ('Autoconsumo', 'RD 244/2019, art. 20.1; ITC-BT-03, apartado 3',
             'Debe instalarlo una empresa instaladora: categoría básica para generadores de menos de 10 kW, especialista '
             'desde 10 kW. En baja tensión y por debajo de 100 kW, la comunidad inscribe de oficio la instalación en '
             'el registro de autoconsumo una vez presentado el certificado.'),
            URGENCIAS, PRESUPUESTO, RECLAMACIONES, RESENAS, AVISO,
        ],
        nota='La habilitación se tramita en la dirección general de industria de tu comunidad, y las normas sobre '
             'presupuestos y hojas de reclamaciones también son autonómicas. ' + NOTA,
        we=[WE_AVISO,
            'Tu habilitación descrita con exactitud: empresa instaladora, categoría y solo los trabajos que cubre',
            'Tus condiciones de desplazamiento y tus precios para particulares con el IVA incluido',
            WE_RECL,
            'Botón de llamada y WhatsApp siempre visibles en el móvil, para las averías'],
        fuentes=[('REBT, RD 842/2002 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-18099'),
                 ('Ley 21/1992 de Industria (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-1992-17363'),
                 ('Registro Integrado Industrial (Ministerio de Industria)',
                  'https://industria.gob.es/registros-industriales/RII/Paginas/consultas-publicas.aspx'),
                 ('Autoconsumo, RD 244/2019 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2019-5089'),
                 ('Ley de Propiedad Horizontal (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-1960-10906')]
                + SRC_CONSUMO,
    ),
    'reformas': dict(
        titulo='Lo que tu empresa de reformas y tu web deben cumplir',
        lead='Las reformas no son una profesión regulada en sí, pero las licencias, la ley de consumo, el IVA y '
             'algunas normas concretas, como la del amianto, deciden qué puedes anunciar y cómo presupuestar. Esto es '
             'lo esencial.',
        filas=[
            ('Licencias de obra', 'TRLSRU (RDLeg 7/2015), art. 11.3; leyes urbanísticas autonómicas',
             'Según su alcance, una obra puede necesitar licencia, declaración responsable o comunicación previa ante '
             'el ayuntamiento. La presenta el propietario, como promotor, pero las leyes de la Comunidad de Madrid, la '
             'Comunitat Valenciana y Andalucía también sancionan al constructor y permiten paralizar la obra si se '
             'ejecuta sin ella.'),
            PRESUPUESTO_MADRID,
            ('Contratos firmados en casa del cliente o a distancia', 'TRLGDCU, arts. 93, 99.3, 102, 103 y 105',
             'El cliente tiene 14 días para desistir, o 30 si la visita no fue solicitada, y el plazo se amplía hasta '
             '12 meses si no le informas de ese derecho. Solo puedes empezar antes de que acaben esos 14 días si lo '
             'pide expresamente en un soporte duradero. No hay desistimiento para una reparación urgente que te pidió, '
             'y la transformación sustancial de un edificio queda excluida.'),
            ('Amianto (fibrocemento)', 'RD 396/2006, arts. 11, 12 y 17',
             'Solo las empresas inscritas en el RERA pueden retirar tejados o bajantes de fibrocemento (uralita), con un plan '
             'de trabajo aprobado por la autoridad laboral antes de cada obra (o un plan general para trabajos cortos '
             'e imprevistos). No anuncies la retirada de fibrocemento si no estás inscrito.'),
            ('Residuos de obra', 'RD 105/2008, arts. 2 y 5 y disp. adicional 1.ª; Ley 7/2022',
             'Quien ejecuta la obra es el poseedor de los residuos. Salvo en obras menores domiciliarias, que siguen '
             'las ordenanzas municipales, entrégalos a un gestor autorizado, separados por fracciones, y guarda la '
             'documentación cinco años.'),
            IVA10,
            ('Pagos en efectivo', 'Ley 7/2012, art. 7',
             'Un trabajo de 1.000 € o más no puede pagarse en efectivo, y los pagos fraccionados de una misma obra se '
             'suman. El límite es de 10.000 € para personas físicas que justifiquen no tener su domicilio fiscal en '
             'España y no actúen como empresarios.'),
            REA, RECLAMACIONES, RESENAS, AVISO,
        ],
        nota='Las licencias son municipales, y las normas sobre presupuestos y hojas de reclamaciones son '
             'autonómicas: consulta a tu ayuntamiento y a tu comunidad autónoma. ' + NOTA,
        we=[WE_AVISO,
            'Tus precios para particulares con el IVA incluido y tus servicios descritos con exactitud, incluida '
            'cualquier inscripción que necesiten',
            WE_RECL,
            'Un formulario para pedir presupuesto, un botón de WhatsApp y tu teléfono, para que el cliente te '
            'contacte directamente',
            'Las reseñas de clientes, con una nota que indica si se comprueban y cómo'],
        fuentes=[('TRLSRU, RDLeg 7/2015 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11723'),
                 ('Amianto, RD 396/2006 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2006-6474'),
                 ('Residuos de construcción, RD 105/2008 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2008-2486'),
                 ('IVA en obras de renovación (Agencia Tributaria)',
                  'https://sede.agenciatributaria.gob.es/Sede/iva/iva-operaciones-inmobiliarias/preguntas-frecuentes-sobre-obras-reparaciones-inmuebles.html'),
                 ('Reformas en el hogar (Comunidad de Madrid)', 'https://www.comunidad.madrid/consumo/reformas-hogar')]
                + SRC_CONSUMO,
    ),
    'carpinteros': dict(
        titulo='Lo que tu carpintería y tu web deben cumplir',
        lead='La carpintería no es una profesión regulada en España, pero en cuanto trabajas para particulares, la '
             'ley de consumo y las normas de tu comunidad deciden qué deben mostrar tu web, tus presupuestos y tus '
             'facturas. Esto es lo esencial.',
        filas=[
            AVISO,
            PRESUPUESTO_MADRID,
            ('Muebles a medida', 'TRLGDCU, arts. 102 y 103.c',
             'Un contrato firmado en casa del cliente le da 14 días para desistir, pero el suministro de bienes '
             'confeccionados según sus especificaciones o claramente personalizados, como un mueble a medida, está '
             'excluido del desistimiento.'),
            RECLAMACIONES,
            ('IVA del 10 %', 'Ley 37/1992, art. 91.Uno.2.10.º',
             'Renovación o reparación de una vivienda con al menos dos años, para un particular que la usa (no '
             'alquilada) o para una comunidad de propietarios, siempre que el coste de los materiales que aportes no '
             'supere el 40 % de la base imponible. En la instalación de doble acristalamiento, el coste de los '
             'materiales suele superar ese límite, y las puertas, ventanas o muebles de cocina entregados sin instalar '
             'tributan siempre al 21 %.'),
            RESENAS,
            REA,
        ],
        nota='Las normas sobre presupuestos y hojas de reclamaciones son autonómicas: consulta a la oficina de '
             'consumo de tu comunidad. ' + NOTA,
        we=[WE_AVISO,
            'Tus precios para particulares con el IVA incluido y una hoja informativa de precios (la que la Comunidad '
            'de Madrid pide a las empresas de reformas)',
            WE_RECL,
            'Las reseñas de clientes, con una nota que indica si se comprueban y cómo',
            'Un formulario para pedir presupuesto, un botón de WhatsApp y tu teléfono'],
        fuentes=[('IVA en obras de renovación (Agencia Tributaria)',
                  'https://sede.agenciatributaria.gob.es/Sede/iva/iva-operaciones-inmobiliarias/preguntas-frecuentes-sobre-obras-reparaciones-inmuebles.html'),
                 ('Reformas en el hogar (Comunidad de Madrid)', 'https://www.comunidad.madrid/consumo/reformas-hogar'),
                 ('Reclamaciones en Andalucía (Consumo Responde)',
                  'https://www.consumoresponde.es/art%C3%ADculos/obligaciones_de_las_empresas_en_materia_de_quejas_y_reclamaciones_en_andalucia'),
                 ('Ley 32/2006 de subcontratación (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2006-18205')]
                + SRC_CONSUMO,
    ),
}

AVISO_SANITARIO = ('Aviso legal', 'LSSI (Ley 34/2002), art. 10',
                   'Tu nombre o denominación social, tu dirección, tu correo electrónico y otro dato de contacto '
                   'directo (normalmente, el teléfono), tu NIF y, si muestras precios, si incluyen o no los impuestos '
                   'aplicables.')
NOTA_SANITARIA = ('Algunas comunidades, como la Región de Murcia, exigen además autorización previa de la publicidad '
                  'sanitaria, webs incluidas. Información general a septiembre de 2026, que no sustituye al '
                  'asesoramiento jurídico: consulta a tu colegio y a la consejería de sanidad de tu comunidad. Tú nos '
                  'das los datos de tu consulta y validas cada texto antes de publicarlo.')
PAGINAS_SANIDAD = {
    'psicologos': dict(
        titulo='Lo que tu consulta y tu web deben cumplir',
        lead='En España, lo que puedes decir en tu web depende de tu título: un psicólogo general sanitario es un '
             'profesional sanitario regulado, mientras que un terapeuta o un coach no lo es y no puede presentar su '
             'trabajo como atención sanitaria. Esto es lo esencial.',
        filas=[
            ('Psicólogo', 'Ley 43/1979, art. 2; LSSI (Ley 34/2002), art. 10',
             'La colegiación en un colegio oficial de psicólogos es obligatoria para ejercer. Tu web debe mostrar tu '
             'colegio y tu número de colegiado, tu titulación oficial, el país que la expidió y, en su caso, su '
             'reconocimiento en España, además de las normas profesionales que se te aplican (como el código '
             'deontológico de tu colegio) y dónde consultarlas.'),
            ('Psicólogo general sanitario', 'Ley 33/2011, disp. adicional 7.ª; RD 1277/2003, art. 6.2',
             'La actividad sanitaria exige el Máster en Psicología General Sanitaria (o el título de especialista en '
             'Psicología Clínica) y un centro autorizado por la consejería de sanidad de tu comunidad. Toda publicidad '
             'que sugiera una actividad sanitaria, tu web incluida, debe mostrar el número de registro que la '
             'comunidad asigna a tu centro.'),
            ('Título extranjero', 'RD 581/2017; RD 889/2022; Código Penal, art. 403',
             'Un título de la UE lo reconoce el Ministerio de Sanidad; uno de fuera de la UE, incluido el del Reino '
             'Unido a partir de 2021, debe homologarse al Máster en Psicología General Sanitaria ante el Ministerio de '
             'Ciencia, Innovación y Universidades (un grado por sí solo no puede homologarse). Ejercer como psicólogo '
             'sin un título reconocido en España es delito, y atribuirte públicamente esa condición lo agrava.'),
            ('Terapeutas, coaches e hipnoterapeutas', 'RD 1907/1996, arts. 4 y 5.3; RD 1277/2003, art. 6.2',
             'Estos títulos no están regulados, pero tu web no puede presentar tu trabajo como atención sanitaria: '
             'sin promesas de alivio o curación y sin afirmar que tratas una enfermedad. Estas prohibiciones se '
             'aplican a cualquiera que presente su trabajo como relacionado con la salud.'),
            ('Formularios de contacto', 'RGPD, arts. 5 y 9; LOPDGDD, art. 34',
             'El motivo por el que alguien quiere verte es un dato de salud: tu formulario debería pedir solo el '
             'nombre, los datos de contacto y el horario preferido. Si ejerces a título individual, no necesitas '
             'delegado de protección de datos.'),
            AVISO_SANITARIO,
        ],
        nota=NOTA_SANITARIA,
        we=['Tu colegio, tu número de colegiado, tu titulación y un enlace a tu código deontológico, además del '
            'número de registro de tu centro y los datos de la autorización sanitaria cuando correspondan',
            'Textos sin promesas de salud ni títulos que no tengas',
            'Un formulario de contacto sin campo de «motivo de consulta», con una nota que pide no compartir datos de '
            'salud',
            'Un enlace a tu herramienta de reservas, WhatsApp o teléfono, en lugar de recoger datos en la web',
            'Aviso legal, política de privacidad y de cookies con tus datos'],
        fuentes=[('Ley 43/1979 de colegios de psicólogos (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-1980-405'),
                 ('Ley 33/2011, disp. adicional 7.ª (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2011-15623'),
                 ('RD 1277/2003 de centros sanitarios (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-19572'),
                 ('RD 1907/1996 de publicidad sanitaria (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-1996-18085'),
                 ('Guía para profesionales del sector sanitario (AEPD)',
                  'https://www.aepd.es/guias/guia-profesionales-sector-sanitario.pdf'),
                 ('LSSI, art. 10 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758')],
    ),
    'fisioterapeutas': dict(
        titulo='Lo que tu consulta de fisioterapia y tu web deben cumplir',
        lead='La fisioterapia es una profesión sanitaria regulada en España, y eso marca lo que tu web debe mostrar '
             'y lo que puede decir. Esto es lo esencial.',
        filas=[
            ('Colegio y aviso legal', 'Ley 2/1974, art. 3; LSSI (Ley 34/2002), art. 10',
             'La colegiación en un colegio de fisioterapeutas es obligatoria para ejercer. Tu web debe mostrar tu '
             'colegio y tu número de colegiado, tu titulación, el país que la expidió y su reconocimiento en España '
             'si lo hay, las normas profesionales que se te aplican y tu NIF o NIE.'),
            ('Autorización del centro', 'RD 1277/2003, arts. 3 y 6.2',
             'Una consulta de fisioterapia (normalmente de tipo C.2.2, con la unidad de fisioterapia U.59) necesita '
             'autorización previa de la consejería de sanidad de tu comunidad. Toda publicidad que sugiera asistencia '
             'sanitaria, tu web incluida, debe mostrar el número de registro que te asigna la consejería. La '
             'Comunidad de Madrid exige también autorización para la fisioterapia exclusivamente a domicilio.'),
            ('Publicidad sanitaria', 'Ley 44/2003, art. 44; RD 1907/1996, art. 4',
             'La publicidad debe ser objetiva, prudente y veraz: sin garantías de alivio o curación y sin '
             'afirmaciones que no tengan respaldo científico.'),
            ('Código deontológico', 'Código Deontológico del Consejo General de Colegios de Fisioterapeutas, arts. 76 a 81',
             'Preséntate solo como «Fisioterapeuta»: añadir otra denominación, como «y osteópata», va contra el '
             'código. Muestra tu nombre, tu número de colegiado y tu colegio en tu publicidad, y no captes clientes '
             'con publicidad basada en el precio.'),
            ('Títulos extranjeros', 'RD 581/2017; RD 889/2022; RDL 38/2020, art. 4; Código Penal, art. 403',
             'Un título de la UE lo reconoce el Ministerio de Sanidad, previa solicitud; una nueva solicitud para un '
             'título del Reino Unido pasa por la homologación del Ministerio de Ciencia, Innovación y Universidades, '
             'con español de nivel B2. Ejercer sin un título reconocido en España es delito.'),
            ('Protección de datos', 'RGPD, art. 9; LOPDGDD, art. 34',
             'Los datos de salud de un formulario de contacto pertenecen a las categorías especiales de datos: pide '
             'solo lo necesario. Si ejerces a título individual, no necesitas delegado de protección de datos; una '
             'clínica, sí.'),
            ('IVA', 'Ley 37/1992, arts. 20.Uno.3.º y 90.Uno',
             'La fisioterapia está exenta de IVA cuando tiene por objeto el diagnóstico, la prevención o el '
             'tratamiento de una lesión o enfermedad; el masaje relajante o estético fuera de un tratamiento tributa '
             'al 21 %.'),
        ],
        nota=NOTA_SANITARIA,
        we=['Tu colegio, tu número de colegiado, tu titulación y un enlace al código deontológico, además de tu NIF '
            'o NIE',
            'El número de registro de tu centro allí donde la web presenta tus servicios',
            'Textos sin promesas de curación ni ofertas basadas en el precio',
            'Un enlace a tu herramienta de reservas, WhatsApp o teléfono, y un formulario que pide solo lo necesario',
            'Tu web en hasta 4 idiomas sin coste adicional'],
        fuentes=[('RD 1277/2003 de centros sanitarios (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-19572'),
                 ('RD 1907/1996 de publicidad sanitaria (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-1996-18085'),
                 ('Código deontológico (Consejo General de Colegios de Fisioterapeutas)',
                  'https://www.consejo-fisioterapia.org/descargas/codigo-deontologico-cgcfe.pdf'),
                 ('Preguntas frecuentes para profesionales sanitarios (AEPD)',
                  'https://www.aepd.es/preguntas-frecuentes/16-salud/2-profesionales-sanitarios'),
                 ('LSSI, art. 10 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758')],
    ),
    'dentistas': dict(
        titulo='Lo que tu clínica dental y tu web deben cumplir',
        lead='La odontología es una profesión sanitaria regulada en España, y su publicidad está especialmente '
             'vigilada. Esto es lo esencial para tu web.',
        filas=[
            ('Colegio y aviso legal', 'Ley 2/1974, art. 3; LSSI (Ley 34/2002), art. 10',
             'La colegiación en un colegio de odontólogos y estomatólogos es obligatoria. Tu web debe mostrar tu '
             'colegio y tu número de colegiado, tu titulación, el país que la expidió y su reconocimiento en España '
             'si lo hay, las normas profesionales aplicables, tu NIF y los datos de autorización de la clínica.'),
            ('Autorización de la clínica', 'RD 1277/2003, art. 6.2; RD 1594/1994, art. 3',
             'Una clínica dental (tipo C.2.5.1) necesita autorización autonómica, y su número de registro debe '
             'figurar en toda su publicidad, web incluida. Una consulta dental debe estar dirigida directa y '
             'personalmente por un dentista.'),
            ('Publicidad sanitaria', 'Ley 44/2003, art. 44; RD 1907/1996, art. 4',
             'La publicidad debe ser objetiva, prudente y veraz, sin garantías de resultados.'),
            ('Títulos', 'Ley 44/2003, disp. adicional 2.ª; código deontológico del Consejo General, art. 56',
             'En España no hay especialidades odontológicas oficiales, así que no puedes usar títulos como '
             '«especialista en implantes» o «especialista en ortodoncia». Usa solo los títulos que realmente tienes.'),
            ('Marcas y «gratis»', 'RD 1591/2009, art. 38.9; Ley 3/1991, art. 22.5',
             'Está prohibida la publicidad dirigida al público de productos sanitarios que aplica el dentista, como '
             'marcas de implantes o de alineadores. Llamar «gratis» a algo es engañoso si el paciente tiene que '
             'pagar cualquier cosa.'),
            ('Precios y financiación', 'TRLGDCU, art. 20.1.c; Ley 16/2011, art. 9',
             'Los precios anunciados deben ser el precio final completo. Todo anuncio que mencione el coste de una '
             'financiación debe incluir un ejemplo representativo con la TAE, y la financiación «al 0 %» gestionada '
             'a través de la clínica sigue siendo un crédito al consumo.'),
            ('Títulos extranjeros', 'RD 581/2017; RD 889/2022; RDL 38/2020, art. 4; Código Penal, art. 403',
             'Los títulos de Odontología de la UE tienen reconocimiento automático, pero debes solicitarlo igualmente '
             'al Ministerio de Sanidad; una nueva solicitud para un título del Reino Unido pasa por la homologación, '
             'con español de nivel B2. Ejercer sin un título reconocido es delito.'),
            ('Protección de datos', 'RGPD, art. 9; LOPDGDD, art. 34',
             'Las clínicas dentales deben designar un delegado de protección de datos; un dentista que ejerce solo, '
             'como persona física, no está obligado.'),
        ],
        nota='Las normas autonómicas añaden detalles: en Madrid, como explica el decálogo del Colegio de Dentistas '
             'de Madrid (COEM), la normativa de consumo exige el precio total de un tratamiento en lugar de «desde '
             'X €» y el precio anterior junto a cualquier descuento; el Colegio de Odontólogos y Estomatólogos de '
             'Cataluña (COEC) no admite la «primera visita gratis». '
             + NOTA_SANITARIA.replace('los datos de tu consulta', 'los datos de tu clínica'),
        we=['Tu colegio, tu número de colegiado, tu titulación y un enlace al código deontológico, además del número '
            'de registro y la autorización de la clínica',
            'Tratamientos descritos sin promesas de resultados, marcas ni títulos de «especialista»',
            'Precios finales completos y, si hay financiación, su ejemplo representativo',
            'Un enlace a tu herramienta de reservas, WhatsApp o teléfono, y un formulario que pide solo lo necesario',
            'Tu web en hasta 4 idiomas sin coste adicional'],
        fuentes=[('RD 1277/2003 de centros sanitarios (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2003-19572'),
                 ('RD 1907/1996 de publicidad sanitaria (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-1996-18085'),
                 ('Decálogo de publicidad dental (Colegio de Dentistas de Madrid)',
                  'https://coem.org.es/wp-content/uploads/2025/11/DECALOGO_PUBLICIDAD_COEM.pdf'),
                 ('Clínicas dentales: derechos de los consumidores (Comunidad de Madrid)',
                  'https://www.comunidad.madrid/consumo/clinicas-dentales-derechos-consumidores'),
                 ('LSSI, art. 10 (BOE)', 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758')],
    ),
}
PAGINAS.update(PAGINAS_SANIDAD)


def section(P, fond):
    filas = ''.join('<tr><th scope="row">%s</th><td class="ley">%s</td><td>%s</td></tr>' % (E(a), E(b), E(c))
                    for a, b, c in P['filas'])
    we = ''.join('<li>%s</li>' % E(t) for t in P['we'])
    src = ' · '.join('<a href="%s" rel="noopener" target="_blank">%s</a>' % (h, E(t)) for t, h in P['fuentes'])
    return ('<!-- NORMATIVA (patch_normativa_es_20260928.py) : règles vérifiées, à garder telles quelles -->\n'
            '<section class="nrm %s" id="normativa">\n'
            '  <div class="nrm-in">\n'
            '    <p class="nrm-ey">Normativa</p>\n'
            '    <h2>%s</h2>\n'
            '    <p class="nrm-lead">%s</p>\n'
            '    <div class="nrm-w"><table class="nrm-t">\n'
            '      <thead><tr><th scope="col">Tema</th><th scope="col">Norma</th><th scope="col">Qué significa para ti</th></tr></thead>\n'
            '      <tbody>%s</tbody>\n'
            '    </table></div>\n'
            '    <p class="nrm-note">%s</p>\n'
            '    <div class="nrm-we"><h3>Lo que preparamos en tu web</h3><ul>%s</ul></div>\n'
            '    <p class="nrm-src">Fuentes: %s</p>\n'
            '  </div>\n'
            '</section>\n\n') % (fond, E(P['titulo']), E(P['lead']), filas, E(P['nota']), we, src)


def main():
    for slug, P in PAGINAS.items():
        rel = slug + '/index.html'
        s = open(rel, encoding='utf-8').read()
        if 'id="normativa"' in s:
            print('  = %s : section déjà présente' % rel)
            continue
        ancre = '<!-- FAQ -->\n<section class="faq"'
        if s.count(ancre) != 1:
            sys.exit('ABANDON : %s : ancre FAQ trouvée %d fois' % (rel, s.count(ancre)))
        i = s.index(ancre)
        prev = list(re.finditer(r'<section[^>]*>', s[:i]))[-1].group(0)
        fond = 'nrm-line' if ('var(--off)' in prev or re.search(r'class="[^"]*\boff\b', prev)) else 'nrm-off'
        s2 = s.replace(ancre, section(P, fond) + ancre, 1)
        if s2.count('</style>') < 1:
            sys.exit('ABANDON : %s : </style> introuvable' % rel)
        s2 = s2.replace('</style>', CSS + '</style>', 1)
        for tag in ('section', 'table', 'tr', 'ul', 'li', 'p', 'div'):
            o = len(re.findall(r'<%s[\s>]' % tag, s2)) - len(re.findall(r'<%s[\s>]' % tag, s))
            f = s2.count('</%s>' % tag) - s.count('</%s>' % tag)
            if o != f:
                sys.exit('ABANDON : %s : <%s> déséquilibré (+%d / +%d)' % (rel, tag, o, f))
        print('  ✓ %s : section ajoutée avant la FAQ (%d lignes, fond %s)' % (rel, len(P['filas']), fond))
        if APPLY:
            open(rel, 'w', encoding='utf-8').write(s2)
    if not APPLY:
        print('Essai : rien n\'est écrit (ajouter --apply).')


if __name__ == '__main__':
    main()
