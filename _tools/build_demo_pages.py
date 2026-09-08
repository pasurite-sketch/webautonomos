# -*- coding: utf-8 -*-
"""Génère les versions FRANÇAISE et ANGLAISE des pages de conversion,
à partir des sources espagnoles :

  pide-tu-demo.html   ->  demandez-votre-demo.html  (/demandez-votre-demo)
                      ->  get-your-demo.html        (/get-your-demo)
  gracias/index.html  ->  merci/index.html          (/merci/)
                      ->  thank-you/index.html      (/thank-you/)

Dans les deux langues : vidéo supprimée, témoignage remplacé par le carrousel des avis
Trustpilot, libellés du bandeau sur une seule ligne. CSS, JavaScript, webhook Make,
GA4 et Clarity conservés à l'identique. Les champs du formulaire gardent leurs noms :
la charge utile est inchangée, seul s'ajoute un champ caché `idioma`.

Remplace build_fr_demo.py (qui peut être supprimé).
À lancer depuis ~/webautonomos. Abandon total si une seule ancre ne correspond pas.
"""
import os, re, sys

SRC_DEMO="pide-tu-demo.html"
SRC_MERCI=os.path.join("gracias","index.html")

DEMO_FR=[
 # --- en-tête / métadonnées ---
 ('<html lang="es">', '<html lang="fr">', 1),
 ('<title>Tu Web Profesional Solo 15€/mes — Demo Gratis en 24h | WebAutonomos</title>',
  '<title>Votre site professionnel pour 15 €/mois — Démo gratuite en 24 h | WebAutonomos</title>', 1),
 ('<meta name="description" content="Página web profesional para autónomos por solo 15€/mes. Te enviamos tu demo personalizada en menos de 24 horas. Sin alta, sin permanencia.">',
  '<meta name="description" content="Site web professionnel pour indépendants à 15 €/mois. Nous vous envoyons votre démo personnalisée en moins de 24 heures. Sans frais d\'installation, sans engagement.">\n'
  '<link rel="canonical" href="https://webautonomos.es/demandez-votre-demo">\n'
  '<link rel="alternate" hreflang="es" href="https://webautonomos.es/pide-tu-demo">\n'
  '<link rel="alternate" hreflang="fr" href="https://webautonomos.es/demandez-votre-demo">\n'
  '<link rel="alternate" hreflang="x-default" href="https://webautonomos.es/pide-tu-demo">', 1),

 # --- navigation ---
 ('← Volver al inicio', "← Retour à l'accueil", 1),

 # --- hero ---
 ('Artesanos &amp; Profesionales', 'Artisans &amp; Professionnels', 1),
 ('<h1>Una web que convierte cada visita en <span class="ul">una llamada, una cita o un nuevo cliente.</span></h1>',
  '<h1>Un site qui transforme chaque visite en <span class="ul">un appel, un rendez-vous ou un nouveau client.</span></h1>', 1),
 ('Construimos tu sitio web profesional con tus fotos, tus servicios y tus reseñas de Google — y te lo enviamos en 24 horas, antes de que decidas nada.',
  'Nous construisons votre site professionnel avec vos photos, vos services et vos avis Google — et nous vous l\'envoyons en 24 heures, avant que vous ne décidiez quoi que ce soit.', 1),
 ('✓ Sin alta, sin permanencia', "✓ Sans frais d'installation, sans engagement", 1),
 ('✓ 15€/mes todo incluido', '✓ 15 €/mois tout compris', 1),
 ('✓ Demo gratuita en 24h', '✓ Démo gratuite en 24 h', 1),
 ('Quiero mi demo gratis →', 'Je veux ma démo gratuite →', 1),

 # --- étapes ---
 ('<p class="ey">El proceso</p>', '<p class="ey">Le déroulement</p>', 1),
 ('Tres pasos, sin complicaciones', 'Trois étapes, sans complications', 1),
 ('Sin contratos. Sin sorpresas. Sin tecnicismos.', 'Sans contrat. Sans surprise. Sans jargon technique.', 1),
 ('Rellenas los datos de tu negocio', 'Vous remplissez les infos de votre activité', 1),
 ('Tu empresa, tus servicios, tu zona. Son 2 minutos.', 'Votre entreprise, vos services, votre secteur. Cela prend 2 minutes.', 1),
 ('<div class="stit">Construimos tu sitio</div>', '<div class="stit">Nous construisons votre site</div>', 1),
 ('En menos de 24h tienes tu demo lista con tus fotos y reseñas reales de Google.',
  'En moins de 24 h, votre démo est prête avec vos photos et vos vrais avis Google.', 1),
 ('Te llamamos', 'Nous vous appelons', 1),
 ('Lo revisamos juntos. Si te gusta: 15€/mes. Si no: sin coste ni compromiso.',
  'Nous la regardons ensemble. Si elle vous plaît : 15 €/mois. Sinon : sans frais ni engagement.', 1),

 # --- secteurs ---
 ('<p class="ey">Para quién</p>', '<p class="ey">Pour qui</p>', 1),
 ('Todos los oficios, un solo precio', 'Tous les métiers, un seul prix', 1),
 ('Ya trabajamos con profesionales de toda España.', 'Nous travaillons déjà avec des professionnels indépendants.', 1),
 ('⚡ Electricistas','⚡ Électriciens',1), ('🔧 Fontaneros','🔧 Plombiers',1),
 ('🪵 Carpinteros','🪵 Menuisiers',1), ('🎨 Pintores','🎨 Peintres',1),
 ('🦷 Clínicas dentales','🦷 Cabinets dentaires',1), ('💆 Fisioterapeutas','💆 Kinésithérapeutes',1),
 ('🦶 Podólogos','🦶 Podologues',1), ('❄️ Climatización','❄️ Climatisation',1),
 ('🏗️ Reformas','🏗️ Rénovation',1), ('🔑 Cerrajeros','🔑 Serruriers',1),
 ('🪟 Aluminios y PVC','🪟 Aluminium et PVC',1), ('🎨 Tatuadores','🎨 Tatoueurs',1),
 ('➕ Tu oficio','➕ Votre métier',1),

 # --- preuve sociale ---
 ('<p class="ey">Resultados reales</p>', '<p class="ey">Résultats concrets</p>', 1),
 ('Profesionales que ya confían en nosotros', 'Des professionnels nous font déjà confiance', 1),
 ('Webs profesionales entregadas en toda España.', 'Des sites professionnels livrés en 24 heures.', 1),
 ('Tiempo medio de<br>entrega de la demo', 'délai moyen de<br>livraison de la démo', 1),

 # --- formulaire ---
 ('<p class="ey">Es gratis</p>', '<p class="ey">C\'est gratuit</p>', 1),
 ('Recibe tu demo personalizada', 'Recevez votre démo personnalisée', 1),
 ('Rellena los datos de tu negocio. Te enviamos el enlace a tu sitio en menos de 24 horas.',
  'Remplissez les informations de votre activité. Nous vous envoyons le lien vers votre site en moins de 24 heures.', 1),
 ('<label>Tu oficio <span class="star">*</span></label>', '<label>Votre métier <span class="star">*</span></label>', 1),
 ('<option value="" disabled selected>Elige tu sector…</option>',
  '<option value="" disabled selected>Choisissez votre secteur…</option>', 1),
 ('<optgroup label="Oficios">', '<optgroup label="Métiers">', 1),
 ('<optgroup label="Salud">', '<optgroup label="Santé">', 1),
 ('<optgroup label="Otros">', '<optgroup label="Autres">', 1),
 # valeurs espagnoles conservées (payload Make inchangé), libellés en français
 ('<option>Electricista</option>','<option value="Electricista">Électricien</option>',1),
 ('<option>Fontanero / Calefactor</option>','<option value="Fontanero / Calefactor">Plombier / Chauffagiste</option>',1),
 ('<option>Carpintero / Ebanista</option>','<option value="Carpintero / Ebanista">Menuisier / Ébéniste</option>',1),
 ('<option>Carpintería de aluminio / PVC</option>','<option value="Carpintería de aluminio / PVC">Menuiserie aluminium / PVC</option>',1),
 ('<option>Pintor / Decorador</option>','<option value="Pintor / Decorador">Peintre / Décorateur</option>',1),
 ('<option>Cerrajero</option>','<option value="Cerrajero">Serrurier</option>',1),
 ('<option>Climatización / Aire acondicionado</option>','<option value="Climatización / Aire acondicionado">Climatisation / Air conditionné</option>',1),
 ('<option>Reformas y construcción</option>','<option value="Reformas y construcción">Rénovation et construction</option>',1),
 ('<option>Instalador de suelos</option>','<option value="Instalador de suelos">Poseur de sols</option>',1),
 ('<option>Clínica dental / Dentista</option>','<option value="Clínica dental / Dentista">Cabinet dentaire / Dentiste</option>',1),
 ('<option>Fisioterapeuta / Osteópata</option>','<option value="Fisioterapeuta / Osteópata">Kinésithérapeute / Ostéopathe</option>',1),
 ('<option>Podólogo</option>','<option value="Podólogo">Podologue</option>',1),
 ('<option>Psicólogo</option>','<option value="Psicólogo">Psychologue</option>',1),
 ('<option>Médico / Especialista</option>','<option value="Médico / Especialista">Médecin / Spécialiste</option>',1),
 ('<option>Tatuadores</option>','<option value="Tatuadores">Tatoueurs</option>',1),
 ('<option>Otro oficio</option>','<option value="Otro oficio">Autre métier</option>',1),

 ('<label>Nombre de tu empresa <span class="star">*</span></label>',
  '<label>Nom de votre entreprise <span class="star">*</span></label>', 1),
 ('placeholder="Ej: Electricidad García"', 'placeholder="Ex : Électricité Martin"', 1),
 ('<label>Tu nombre <span class="star">*</span></label>', '<label>Votre nom <span class="star">*</span></label>', 1),
 ('placeholder="Nombre y apellido"', 'placeholder="Nom et prénom"', 1),
 ('<label>Ciudad principal <span class="star">*</span></label>', '<label>Ville principale <span class="star">*</span></label>', 1),
 ('placeholder="Ej: Alicante, Valencia…"', 'placeholder="Ex : Lyon, Bordeaux…"', 1),
 ('placeholder="+34 6XX XXX XXX"', 'placeholder="+33 6 XX XX XX XX"', 2),
 ('(opcional)', '(facultatif)', 1),
 ('placeholder="tu@email.es"', 'placeholder="vous@email.fr"', 2),
 ('<label>Repite tu WhatsApp <span class="star">*</span></label>',
  '<label>Confirmez votre WhatsApp <span class="star">*</span></label>', 1),
 ('<label>Repite tu email</label>', '<label>Confirmez votre e-mail</label>', 1),
 ('>Los números no coinciden.<', '>Les numéros ne correspondent pas.<', 1),
 ('>Los emails no coinciden.<', '>Les adresses e-mail ne correspondent pas.<', 1),

 ('<div class="sep"><span>Tu actividad</span></div>', '<div class="sep"><span>Votre activité</span></div>', 1),
 ('<label>Tus servicios principales <span class="star">*</span></label>',
  '<label>Vos principaux services <span class="star">*</span></label>', 1),
 ('placeholder="Ej: instalaciones, reparaciones, urgencias…"',
  'placeholder="Ex : installations, réparations, urgences…"', 1),
 ('<span>Recibir mi demo gratis en 24h</span>', '<span>Recevoir ma démo gratuite en 24 h</span>', 1),
 ('Sin alta &nbsp;·&nbsp; Sin permanencia &nbsp;·&nbsp; Cancela cuando quieras',
  "Sans frais d'installation &nbsp;·&nbsp; Sans engagement &nbsp;·&nbsp; Résiliez quand vous voulez", 1),
 ('<p>¿Prefieres escribirnos directamente?</p>', '<p>Vous préférez nous écrire directement ?</p>', 1),
 ('text=Hola%2C%20me%20interesa%20una%20web%20para%20mi%20negocio',
  'text=Bonjour%2C%20je%20suis%20int%C3%A9ress%C3%A9%20par%20un%20site%20pour%20mon%20activit%C3%A9', 2),

 # --- bandeau de réassurance ---
 ('<strong>Sin alta, sin permanencia</strong><span>Cancela cuando quieras</span>',
  "<strong>Sans frais d'installation</strong><span>Résiliez quand vous voulez</span>", 1),
 ('<strong>100% móvil</strong><span>Perfecto en smartphone</span>',
  '<strong>100 % mobile</strong><span>Parfait sur smartphone</span>', 1),
 ('<strong>Online en 24h</strong><span>Dominio .es incluido</span>',
  '<strong>En ligne en 24 h</strong><span>Domaine .fr inclus</span>', 1),
 ('<strong>Soporte WhatsApp</strong><span>Respuesta en el día</span>',
  '<strong>Assistance WhatsApp</strong><span>Réponse dans la journée</span>', 1),

 # --- pied de page ---
 ('>Aviso legal<', '>Mentions légales<', 1),
 ('>Privacidad<', '>Confidentialité<', 1),
 ('>Contacto<', '>Contact<', 1),

 # --- interface des mentions légales (textes légaux conservés en espagnol, cf. politique du site) ---
 ('aria-label="Contactar por WhatsApp"', 'aria-label="Nous contacter sur WhatsApp"', 1),
 ('>Cerrar</button>', '>Fermer</button>', 2),
 ('<h3>Aviso Legal</h3>\n        <p>Última actualización: Febrero 2026</p>',
  '<h3>Mentions légales</h3>\n        <p>Ce document n\'est disponible qu\'en espagnol.</p>', 1),
 ('<h3>Política de Privacidad</h3>',
  '<h3>Politique de confidentialité</h3>', 1),

 # --- JavaScript : bouton, redirection, message de secours ---
 ("btn.innerHTML = '<span>Enviando…</span>';", "btn.innerHTML = '<span>Envoi…</span>';", 1),
 ("window.location.href = '/gracias/';", "window.location.href = '/merci/';", 2),
 ("'🆕 LEAD (fallback)\\n\\n'+", "'🆕 LEAD FR (fallback)\\n\\n'+", 1),
]

MERCI_FR=[
 ('<html lang="es">', '<html lang="fr">', 1),
 ('<title>¡Tu demo está en camino! — WebAutonomos</title>',
  '<title>Votre démo est en route ! — WebAutonomos</title>', 1),
 ('<h1>¡Tu demo está<br>en camino!</h1>', '<h1>Votre démo est<br>en route !</h1>', 1),
 ('Ya tenemos tus datos. Esto es lo que va a pasar ahora:',
  'Nous avons bien reçu vos informations. Voici ce qui va se passer :', 1),
 ('Te enviamos tu demo por WhatsApp', 'Nous vous envoyons votre démo par WhatsApp', 1),
 ('Recibirás el enlace a tu sitio web personalizado en las próximas 24 horas.',
  'Vous recevrez le lien vers votre site personnalisé dans les 24 prochaines heures.', 1),
 ('Te llamamos para revisarlo juntos', 'Nous vous appelons pour la regarder ensemble', 1),
 ('Si te gusta: 15€/mes. Si no: sin coste ni compromiso.',
  'Si elle vous plaît : 15 €/mois. Sinon : sans frais ni engagement.', 1),
 ('Tu web online y funcionando', 'Votre site en ligne et opérationnel', 1),
 ('Con tus fotos, tus reseñas de Google y tu dominio .es incluido.',
  'Avec vos photos, vos avis Google et votre domaine .fr inclus.', 1),
 ('Escríbenos por WhatsApp', 'Écrivez-nous sur WhatsApp', 1),
 ('← Volver al inicio', "← Retour à l'accueil", 1),
 ('text=Hola%2C%20acabo%20de%20pedir%20mi%20demo',
  'text=Bonjour%2C%20je%20viens%20de%20demander%20ma%20d%C3%A9mo', 1),
]



DEMO_EN=[
 ('<html lang="es">', '<html lang="en">', 1),
 ('<title>Tu Web Profesional Solo 15€/mes — Demo Gratis en 24h | WebAutonomos</title>',
  '<title>Your professional website for just €15/month — Free demo in 24h | WebAutonomos</title>', 1),
 ('<meta name="description" content="Página web profesional para autónomos por solo 15€/mes. Te enviamos tu demo personalizada en menos de 24 horas. Sin alta, sin permanencia.">',
  '<meta name="description" content="A professional website for the self-employed from just €15/month. We send you your personalised demo in under 24 hours. No setup fee, no commitment.">\n'
  '<link rel="canonical" href="https://webautonomos.es/get-your-demo">\n'
  '<link rel="alternate" hreflang="es" href="https://webautonomos.es/pide-tu-demo">\n'
  '<link rel="alternate" hreflang="fr" href="https://webautonomos.es/demandez-votre-demo">\n'
  '<link rel="alternate" hreflang="en" href="https://webautonomos.es/get-your-demo">\n'
  '<link rel="alternate" hreflang="x-default" href="https://webautonomos.es/pide-tu-demo">', 1),

 ('← Volver al inicio', '← Back to home', 1),

 ('Artesanos &amp; Profesionales', 'Trades &amp; Professionals', 1),
 ('<h1>Una web que convierte cada visita en <span class="ul">una llamada, una cita o un nuevo cliente.</span></h1>',
  '<h1>A website that turns every visit into <span class="ul">a call, an appointment or a new client.</span></h1>', 1),
 ('Construimos tu sitio web profesional con tus fotos, tus servicios y tus reseñas de Google — y te lo enviamos en 24 horas, antes de que decidas nada.',
  'We build your professional website with your photos, your services and your Google reviews — and we send it to you within 24 hours, before you commit to anything.', 1),
 ('✓ Sin alta, sin permanencia', '✓ No setup fee, no commitment', 1),
 ('✓ 15€/mes todo incluido', '✓ €15/month, everything included', 1),
 ('✓ Demo gratuita en 24h', '✓ Free demo in 24h', 1),
 ('Quiero mi demo gratis →', 'I want my free demo →', 1),

 ('<p class="ey">El proceso</p>', '<p class="ey">The process</p>', 1),
 ('Tres pasos, sin complicaciones', 'Three steps, no complications', 1),
 ('Sin contratos. Sin sorpresas. Sin tecnicismos.', 'No contracts. No surprises. No technical jargon.', 1),
 ('Rellenas los datos de tu negocio', 'You fill in your business details', 1),
 ('Tu empresa, tus servicios, tu zona. Son 2 minutos.', 'Your company, your services, your area. It takes 2 minutes.', 1),
 ('<div class="stit">Construimos tu sitio</div>', '<div class="stit">We build your website</div>', 1),
 ('En menos de 24h tienes tu demo lista con tus fotos y reseñas reales de Google.',
  'In under 24 hours your demo is ready, with your photos and your real Google reviews.', 1),
 ('Te llamamos', 'We call you', 1),
 ('Lo revisamos juntos. Si te gusta: 15€/mes. Si no: sin coste ni compromiso.',
  'We go through it together. If you like it: €15/month. If not: no cost, no obligation.', 1),

 ('<p class="ey">Para quién</p>', '<p class="ey">Who it is for</p>', 1),
 ('Todos los oficios, un solo precio', 'Every trade, one single price', 1),
 ('Ya trabajamos con profesionales de toda España.', 'We already work with self-employed professionals across Spain.', 1),
 ('⚡ Electricistas','⚡ Electricians',1), ('🔧 Fontaneros','🔧 Plumbers',1),
 ('🪵 Carpinteros','🪵 Carpenters',1), ('🎨 Pintores','🎨 Painters',1),
 ('🦷 Clínicas dentales','🦷 Dental clinics',1), ('💆 Fisioterapeutas','💆 Physiotherapists',1),
 ('🦶 Podólogos','🦶 Podiatrists',1), ('❄️ Climatización','❄️ Air conditioning',1),
 ('🏗️ Reformas','🏗️ Renovations',1), ('🔑 Cerrajeros','🔑 Locksmiths',1),
 ('🪟 Aluminios y PVC','🪟 Aluminium and PVC',1), ('🎨 Tatuadores','🎨 Tattoo artists',1),
 ('➕ Tu oficio','➕ Your trade',1),

 ('<p class="ey">Resultados reales</p>', '<p class="ey">Real results</p>', 1),
 ('Profesionales que ya confían en nosotros', 'Professionals who already trust us', 1),
 ('Webs profesionales entregadas en toda España.', 'Professional websites delivered in 24 hours.', 1),
 ('Tiempo medio de<br>entrega de la demo', 'average time to<br>deliver your demo', 1),

 ("<p class=\"ey\">Es gratis</p>", '<p class="ey">It is free</p>', 1),
 ('Recibe tu demo personalizada', 'Get your personalised demo', 1),
 ('Rellena los datos de tu negocio. Te enviamos el enlace a tu sitio en menos de 24 horas.',
  'Fill in your business details. We send you the link to your website in under 24 hours.', 1),
 ('<label>Tu oficio <span class="star">*</span></label>', '<label>Your trade <span class="star">*</span></label>', 1),
 ('<option value="" disabled selected>Elige tu sector…</option>',
  '<option value="" disabled selected>Choose your sector…</option>', 1),
 ('<optgroup label="Oficios">', '<optgroup label="Trades">', 1),
 ('<optgroup label="Salud">', '<optgroup label="Health">', 1),
 ('<optgroup label="Otros">', '<optgroup label="Other">', 1),
 ('<option>Electricista</option>','<option value="Electricista">Electrician</option>',1),
 ('<option>Fontanero / Calefactor</option>','<option value="Fontanero / Calefactor">Plumber / Heating engineer</option>',1),
 ('<option>Carpintero / Ebanista</option>','<option value="Carpintero / Ebanista">Carpenter / Cabinetmaker</option>',1),
 ('<option>Carpintería de aluminio / PVC</option>','<option value="Carpintería de aluminio / PVC">Aluminium / PVC windows</option>',1),
 ('<option>Pintor / Decorador</option>','<option value="Pintor / Decorador">Painter / Decorator</option>',1),
 ('<option>Cerrajero</option>','<option value="Cerrajero">Locksmith</option>',1),
 ('<option>Climatización / Aire acondicionado</option>','<option value="Climatización / Aire acondicionado">Air conditioning</option>',1),
 ('<option>Reformas y construcción</option>','<option value="Reformas y construcción">Renovations and building</option>',1),
 ('<option>Instalador de suelos</option>','<option value="Instalador de suelos">Flooring installer</option>',1),
 ('<option>Clínica dental / Dentista</option>','<option value="Clínica dental / Dentista">Dental clinic / Dentist</option>',1),
 ('<option>Fisioterapeuta / Osteópata</option>','<option value="Fisioterapeuta / Osteópata">Physiotherapist / Osteopath</option>',1),
 ('<option>Podólogo</option>','<option value="Podólogo">Podiatrist</option>',1),
 ('<option>Psicólogo</option>','<option value="Psicólogo">Psychologist</option>',1),
 ('<option>Médico / Especialista</option>','<option value="Médico / Especialista">Doctor / Specialist</option>',1),
 ('<option>Tatuadores</option>','<option value="Tatuadores">Tattoo artist</option>',1),
 ('<option>Otro oficio</option>','<option value="Otro oficio">Another trade</option>',1),

 ('<label>Nombre de tu empresa <span class="star">*</span></label>',
  '<label>Your business name <span class="star">*</span></label>', 1),
 ('placeholder="Ej: Electricidad García"', 'placeholder="E.g. García Electrical"', 1),
 ('<label>Tu nombre <span class="star">*</span></label>', '<label>Your name <span class="star">*</span></label>', 1),
 ('placeholder="Nombre y apellido"', 'placeholder="First and last name"', 1),
 ('<label>Ciudad principal <span class="star">*</span></label>', '<label>Main town or city <span class="star">*</span></label>', 1),
 ('placeholder="Ej: Alicante, Valencia…"', 'placeholder="E.g. Alicante, Valencia…"', 1),
 ('placeholder="+34 6XX XXX XXX"', 'placeholder="+34 6XX XXX XXX"', 2),
 ('(opcional)', '(optional)', 1),
 ('placeholder="tu@email.es"', 'placeholder="you@email.com"', 2),
 ('<label>Repite tu WhatsApp <span class="star">*</span></label>',
  '<label>Confirm your WhatsApp <span class="star">*</span></label>', 1),
 ('<label>Repite tu email</label>', '<label>Confirm your email</label>', 1),
 ('>Los números no coinciden.<', '>The numbers do not match.<', 1),
 ('>Los emails no coinciden.<', '>The email addresses do not match.<', 1),
 ('<div class="sep"><span>Tu actividad</span></div>', '<div class="sep"><span>Your activity</span></div>', 1),
 ('<label>Tus servicios principales <span class="star">*</span></label>',
  '<label>Your main services <span class="star">*</span></label>', 1),
 ('placeholder="Ej: instalaciones, reparaciones, urgencias…"',
  'placeholder="E.g. installations, repairs, emergencies…"', 1),
 ('<span>Recibir mi demo gratis en 24h</span>', '<span>Get my free demo in 24h</span>', 1),
 ('Sin alta &nbsp;·&nbsp; Sin permanencia &nbsp;·&nbsp; Cancela cuando quieras',
  'No setup fee &nbsp;·&nbsp; No commitment &nbsp;·&nbsp; Cancel whenever you want', 1),
 ('<p>¿Prefieres escribirnos directamente?</p>', '<p>Prefer to message us directly?</p>', 1),
 ('text=Hola%2C%20me%20interesa%20una%20web%20para%20mi%20negocio',
  'text=Hello%2C%20I%27m%20interested%20in%20a%20website%20for%20my%20business', 2),

 ('<strong>Sin alta, sin permanencia</strong><span>Cancela cuando quieras</span>',
  '<strong>No setup fee</strong><span>Cancel whenever you want</span>', 1),
 ('<strong>100% móvil</strong><span>Perfecto en smartphone</span>',
  '<strong>100% mobile</strong><span>Perfect on smartphone</span>', 1),
 ('<strong>Online en 24h</strong><span>Dominio .es incluido</span>',
  '<strong>Online in 24h</strong><span>.es domain included</span>', 1),
 ('<strong>Soporte WhatsApp</strong><span>Respuesta en el día</span>',
  '<strong>WhatsApp support</strong><span>Same-day reply</span>', 1),

 ('>Aviso legal<', '>Legal notice<', 1),
 ('>Privacidad<', '>Privacy<', 1),
 ('>Contacto<', '>Contact<', 1),

 ('aria-label="Contactar por WhatsApp"', 'aria-label="Contact us on WhatsApp"', 1),
 ('>Cerrar</button>', '>Close</button>', 2),
 ('<h3>Aviso Legal</h3>\n        <p>Última actualización: Febrero 2026</p>',
  '<h3>Legal notice</h3>\n        <p>This document is only available in Spanish.</p>', 1),
 ('<h3>Política de Privacidad</h3>', '<h3>Privacy policy</h3>', 1),

 ("btn.innerHTML = '<span>Enviando…</span>';", "btn.innerHTML = '<span>Sending…</span>';", 1),
 ("window.location.href = '/gracias/';", "window.location.href = '/thank-you/';", 2),
 ("'🆕 LEAD (fallback)\\n\\n'+", "'🆕 LEAD EN (fallback)\\n\\n'+", 1),
]

MERCI_EN=[
 ('<html lang="es">', '<html lang="en">', 1),
 ('<title>¡Tu demo está en camino! — WebAutonomos</title>',
  '<title>Your demo is on its way! — WebAutonomos</title>', 1),
 ('<h1>¡Tu demo está<br>en camino!</h1>', '<h1>Your demo is<br>on its way!</h1>', 1),
 ('Ya tenemos tus datos. Esto es lo que va a pasar ahora:',
  'We have your details. Here is what happens next:', 1),
 ('Te enviamos tu demo por WhatsApp', 'We send you your demo on WhatsApp', 1),
 ('Recibirás el enlace a tu sitio web personalizado en las próximas 24 horas.',
  'You will receive the link to your personalised website within the next 24 hours.', 1),
 ('Te llamamos para revisarlo juntos', 'We call you to go through it together', 1),
 ('Si te gusta: 15€/mes. Si no: sin coste ni compromiso.',
  'If you like it: €15/month. If not: no cost, no obligation.', 1),
 ('Tu web online y funcionando', 'Your website online and running', 1),
 ('Con tus fotos, tus reseñas de Google y tu dominio .es incluido.',
  'With your photos, your Google reviews and your .es domain included.', 1),
 ('Escríbenos por WhatsApp', 'Message us on WhatsApp', 1),
 ('← Volver al inicio', '← Back to home', 1),
 ('text=Hola%2C%20acabo%20de%20pedir%20mi%20demo',
  'text=Hello%2C%20I%27ve%20just%20requested%20my%20demo', 1),
]

# Avis Trustpilot en anglais (versions de la page d'accueil ; Fabiana traduite depuis l'espagnol)
AVIS_EN=[
 ("Angelino built my website quickly and explains everything very well. When you have any questions they are always answered promptly. Anyone needing a website made I would highly recommend contacting Angelino.",
  "Lee Robinson", "Carpenter", ""),
 ("Extremely satisfied with WebAutonomos. Thank you for creating my wonderful website that represents me so well! Thank you for your responsiveness and professionalism. I recommend it without hesitation.",
  "Amelle B.", "", "translated from French"),
 ("I really liked Angelino's work on my website. He was patient, he knows how to listen and then make it happen. He offers a very good service.",
  "Fabiana", "", "translated from Spanish"),
 ("A very good professional, very attentive and always ready to help with whatever you need. He built my website exactly the way I wanted, with all the changes I needed and guiding me every step of the way.",
  "Ana Saiz", "Psychologist", "translated from Spanish"),
 ("Angelino's work on creating my new website comes highly recommended. Thank you for your patience and professionalism. The result is impeccable. I recommend him.",
  "Begoña Cid", "Hypnotherapist", "translated from Spanish"),
 ("After a lot of difficulty getting my website done, with WebAutonomos it was very easy and quick. Friendly and approachable service throughout. I recommend them!",
  "Analía Juan Guillén", "Psychologist", "translated from Spanish"),
]

LIB_EN = {
 "count": "Average rating from {n} verified Trustpilot reviews",
 "link": "See all reviews on Trustpilot →",
 "dot": "Review",
}

# ============================================================
#  Blocs partagés (FR et EN)
# ============================================================

# --- avis Trustpilot réels (versions françaises, cf. page d'accueil) ---
AVIS_FR=[
 ("Angelino a créé mon site rapidement et explique tout très bien. Quand on a une question, il répond toujours vite. Je recommande vivement de contacter Angelino à quiconque a besoin d'un site.",
  "Lee Robinson", "Menuisier", "traduit de l'anglais"),
 ("Extrêmement satisfaite de WebAutonomos. Merci pour la création de mon magnifique site qui me représente si bien ! Merci pour votre réactivité et votre professionnalisme. Je le recommande sans hésiter.",
  "Amelle B.", "", ""),
 ("J'ai beaucoup aimé le travail d'Angelino pour mon site web. Il a été patient, il sait écouter puis concrétiser. Il offre un très bon service.",
  "Fabiana", "", "traduit de l'espagnol"),
 ("Très bon professionnel, très attentif et toujours prêt à vous aider pour tout ce dont vous avez besoin. Il a créé mon site web exactement comme je le voulais, avec toutes les modifications nécessaires et en me guidant à chaque étape.",
  "Ana Saiz", "Psychologue", "traduit de l'espagnol"),
 ("Le travail d'Angelino pour la création de mon nouveau site web est vraiment recommandable. Merci pour ta patience et ton professionnalisme. Résultat impeccable. Je le recommande.",
  "Begoña Cid", "Hypnothérapeute", "traduit de l'espagnol"),
 ("Après beaucoup de difficultés pour avoir mon site, avec WebAutonomos cela a été très simple et rapide. Avec un accueil aimable et proche. Je le recommande !",
  "Analía Juan Guillén", "Psychologue", "traduit de l'espagnol"),
]
TRUSTPILOT_URL="https://es.trustpilot.com/review/webautonomos.es"



def carrousel(avis, lib):
    slides=[]
    for txt,who,job,tr in avis:
        ligne = who + (" — "+job if job else "")
        note = f'<span class="tp-tr">{tr}</span>' if tr else ""
        slides.append(
          '<div class="tp-slide"><div class="tp-card">'
          '<div class="tp-stars">\u2605\u2605\u2605\u2605\u2605</div>'
          f'<blockquote>\u00ab\u00a0{txt}\u00a0\u00bb</blockquote>'
          f'<div class="tp-who">\u2014 {ligne}{note}</div>'
          '</div></div>')
    dots="".join(
      f'<button class="tp-dot{" on" if i==0 else ""}" onclick="tpGo({i})" aria-label="{lib["dot"]} {i+1}"></button>'
      for i in range(len(avis)))
    return (
      '<div class="tp">\n'
      '  <div class="tp-head">'
      '<svg width="22" height="22" viewBox="0 0 24 24" fill="#00b67a" aria-hidden="true">'
      '<path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'
      '<span class="tp-score">4,2</span><span class="tp-of">/ 5</span>'
      f'<span class="tp-count">{lib["count"].format(n=len(avis))}</span></div>\n'
      f'  <div class="tp-view"><div class="tp-track" id="tpTrack">{"".join(slides)}</div></div>\n'
      f'  <div class="tp-dots" id="tpDots">{dots}</div>\n'
      f'  <a class="tp-link" href="{TRUSTPILOT_URL}" target="_blank" rel="noopener noreferrer">'
      f'{lib["link"]}</a>\n'
      '</div>')



def bloc_langue(h, avis, lib):
    """Supprime la vidéo et remplace le carrousel espagnol par sa version localisée."""
    def fin_div(txt, debut):
        i, prof = debut, 0
        while i < len(txt):
            if txt.startswith("<div", i): prof += 1; i += 4
            elif txt.startswith("</div>", i):
                prof -= 1; i += 6
                if prof == 0: return i
            else: i += 1
        return -1

    # 1. suppression de la section vidéo
    a=h.find('<!-- VIDEO -->'); b=h.find('<!-- STEPS -->')
    if a==-1 or b==-1 or b<=a: sys.exit("ABANDON : section vidéo introuvable.")
    h=h[:a]+h[b:]

    # 2. carrousel : la source espagnole en contient déjà un, on le remplace
    t0=h.find('<div class="tp">')
    if t0==-1: sys.exit("ABANDON : carrousel introuvable dans la source (lancer patch_es_reviews.py).")
    t1=fin_div(h, t0)
    if t1==-1: sys.exit("ABANDON : carrousel non refermé.")
    h=h[:t0]+carrousel(avis, lib)+h[t1:]

    # 3. bandeau de réassurance : libellés sur une seule ligne (textes plus longs qu'en espagnol)
    old_wrap = """  .ti-wrap {
    display:flex; flex-wrap:nowrap; justify-content:center;
    gap:36px; max-width:860px; margin:0 auto;
  }"""
    if h.count(old_wrap)!=1: sys.exit("ABANDON : CSS .ti-wrap introuvable.")
    h=h.replace(old_wrap, """  .ti-wrap {
    display:flex; flex-wrap:wrap; justify-content:center;
    gap:26px 22px; max-width:1080px; margin:0 auto;
  }""")
    old_strong = "  .ti strong { display:block; color:var(--text); font-weight:600; }"
    if h.count(old_strong)!=1: sys.exit("ABANDON : CSS .ti strong introuvable.")
    h=h.replace(old_strong, "  .ti strong { display:block; color:var(--text); font-weight:600; white-space:nowrap; }")
    return h


LIB_FR = {"count": "Note moyenne sur {n} avis vérifiés Trustpilot",
          "link": "Voir tous les avis sur Trustpilot →",
          "dot": "Avis"}

LANGUES = [
 ("fr", "française", "demandez-votre-demo.html", os.path.join("merci","index.html"),
        DEMO_FR, MERCI_FR, AVIS_FR, LIB_FR),
 ("en", "anglaise",  "get-your-demo.html",       os.path.join("thank-you","index.html"),
        DEMO_EN, MERCI_EN, AVIS_EN, LIB_EN),
]

def build(src, out, edits, label, code=None, avis=None, lib=None):
    if not os.path.exists(src):
        sys.exit(f"ABANDON : fichier source introuvable — {src}")
    h=open(src, encoding="utf-8").read()
    errs=[]
    for old,new,exp in edits:
        n=h.count(old)
        if n!=exp: errs.append(f"    {n}× (attendu {exp}) : {old[:70]}")
    if errs:
        print(f"ABANDON [{label}] — ancres non conformes, aucun fichier écrit :")
        print("\n".join(errs)); sys.exit(1)
    for old,new,exp in edits:
        h=h.replace(old,new)
    if code:
        anchor='<form id="pf" onsubmit="hs(event)" novalidate>'
        if h.count(anchor)!=1: sys.exit("ABANDON : balise <form> introuvable.")
        h=h.replace(anchor, anchor+f'\n        <input type="hidden" name="idioma" value="{code}">')
        h=bloc_langue(h, avis, lib)
    d=os.path.dirname(out)
    if d: os.makedirs(d, exist_ok=True)
    open(out,"w",encoding="utf-8").write(h)
    print(f"  ✓ {label} → {out} ({len(h)} caractères)")

print("Génération des pages de conversion :")
for code, nom, out_demo, out_merci, ed, em, avis, lib in LANGUES:
    build(SRC_DEMO,  out_demo,  ed, f"Demande de démo ({nom})",  code=code, avis=avis, lib=lib)
    build(SRC_MERCI, out_merci, em, f"Remerciement ({nom})")
print("\nOK — pages créées. Les sources espagnoles ne sont pas modifiées.")
