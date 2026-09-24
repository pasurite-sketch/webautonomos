# -*- coding: utf-8 -*-
"""Nettoyage du blog (24/09/2026) : faux cas clients et statistiques sans source.

Applique une table de remplacements à TOUTES les copies d'un texte : pages du
blog, données SPA de index.html, blog-spa-data.json, _tools/translations/*.json,
_tools/queue/published/*.json. Correspondance tolérante aux accents et aux
apostrophes (les copies SPA sont souvent sans accents).

    python3 _tools/nettoyage_blog.py            # essai : affiche les comptes
    python3 _tools/nettoyage_blog.py --apply    # écrit
"""
import glob, json, re, sys

APPLY = '--apply' in sys.argv
CLS = {'a': 'aáàâ', 'e': 'eéèêë', 'i': 'iíïî', 'o': 'oóòô', 'u': 'uúüù', 'n': 'nñ', 'c': 'cç'}


def fz(lit):
    out = []
    for ch in lit:
        lo = ch.lower()
        if ch in "'’":
            out.append(r"(?:'|’|&#x27;|&#39;|\\')")
        elif ch == '"':
            out.append(r'(?:&quot;|\\"|"|“|”)')
        elif ch == ' ':
            out.append(r'\s+')
        elif lo in CLS:
            k = CLS[lo]
            out.append('[' + k + k.upper() + ']')
        elif lo in 'áàâéèêëíïîóòôúüùñç':
            base = next(b for b, v in CLS.items() if lo in v)
            k = CLS[base]
            out.append('[' + k + k.upper() + ']')
        else:
            out.append(re.escape(ch))
    return ''.join(out)


# (fragment d'origine, remplacement) — le remplacement ne contient ni " ni \ (sûr en JSON et en JS)
T = [
 # ── Électriciens : intro, faux cas, 70 % ─────────────────────────────
 ("En 2026, el 92% de los consumidores busca servicios locales en internet antes de tomar una decisión. Las cifras no mienten: el 76% de las personas que buscan un servicio local en el móvil contactan con un negocio en las siguientes 24 horas.",
  "Hoy casi todo el mundo busca en internet antes de llamar a un electricista: en España, el 96,3% de las personas de 16 a 74 años usa internet (INE, 2025). Y quien necesita un electricista con urgencia suele llamar al primero que encuentra con un teléfono visible y buenas opiniones."),
 ("En 2026, el 92% dels consumidors busca serveis locals a internet abans de prendre una decisió. El 76% de les persones que busquen un servei local al mòbil contacten amb un negoci en les següents 24 hores.",
  "Hui quasi tothom busca a internet abans de telefonar a un electricista: a Espanya, el 96,3% de les persones de 16 a 74 anys usa internet (INE, 2025). I qui necessita un electricista amb urgència sol telefonar al primer que troba amb un telèfon visible i bones opinions."),
 ("In 2026, 92% of consumers search for local services online before making a decision. The numbers don't lie: 76% of people who search for a local service on their phone contact a business within the next 24 hours.",
  "Today almost everyone looks online before calling an electrician: in Spain, 96.3% of people aged 16 to 74 use the internet (INE, 2025). And someone who needs an electrician urgently tends to call the first one they find with a visible phone number and good reviews."),
 ("Mais en 2026, <strong>92 % des consommateurs cherchent un service de proximité sur internet</strong> avant de décider.",
  "Mais aujourd'hui, <strong>presque tout le monde cherche sur internet</strong> avant de décider."),
 ("Les chiffres ne mentent pas. D'après une étude de Google, <strong>76 % des personnes qui cherchent un service local depuis leur mobile contactent une entreprise dans les 24 heures</strong>.",
  "Et quand il y a urgence, <strong>le client appelle souvent le premier électricien qu'il trouve avec un numéro visible et de bons avis</strong>."),
 ("88 % des consommateurs accordent autant de crédit aux avis en ligne qu'aux recommandations de leurs proches.",
  "Un avis en ligne pèse souvent autant qu'une recommandation d'un proche."),
 ("Au-delà, 53 % des visiteurs l'abandonnent.",
  "Au-delà, selon Google (2016), 53 % des visites sur mobile sont abandonnées."),
 ("Un caso real: Miguel, electricista autónomo en Elche, creó su web profesional y en los primeros tres meses recibió 22 solicitudes de presupuesto desde internet. Hoy, el 40% de sus clientes nuevos llegan por la web.",
  "Cuanto más concreta sea tu web (servicios, zona, fotos de trabajos reales), más fácil es que un cliente que no te conoce se decida a llamarte."),
 ("Un cas real: Miquel, electricista autònom a Elx, va crear la seua web professional i en els primers tres mesos va rebre 22 sol·licituds de pressupost des d'internet. Hui, el 40% dels seus clients nous arriben per la web.",
  "Com més concreta siga la teua web (serveis, zona, fotos de treballs reals), més fàcil és que un client que no et coneix es decidisca a telefonar-te."),
 ("A real case: Miguel, a self-employed electrician in Elche, created his professional website and in the first three months received 22 quote requests from the internet. Today, 40% of his new clients come through his website.",
  "The more specific your website is (services, area, photos of real jobs), the easier it is for a client who does not know you to decide to call."),
 ("A real case: Miguel, a self-employed electrician in Elche, created his professional website and in the first three months received 22 quote requests from the internet.",
  "The more specific your website is (services, area, photos of real jobs), the easier it is for a client who does not know you to decide to call."),
 ("Un cas réel : Michel, électricien indépendant à Bruxelles, travaillait depuis 8 ans uniquement au bouche-à-oreille. En 2025, il a décidé de créer son site professionnel et d'optimiser sa fiche Google. En trois mois, il a reçu 22 demandes de devis venues d'internet. Aujourd'hui, 40 % de ses nouveaux clients arrivent par le site. Sans investir un euro en publicité.",
  "Plus votre site est concret (prestations, zone, photos de vos vrais chantiers), plus un client qui ne vous connaît pas se décide facilement à vous appeler."),
 ("En los primeros tres meses recibió 22 solicitudes de presupuesto desde internet.", ""),
 ("En els primers tres mesos va rebre 22 sol·licituds de pressupost des d'internet.", ""),
 ("In the first three months he received 22 quote requests through the internet.", ""),
 ("En trois mois, il a reçu 22 demandes de devis venues d'internet.", ""),
 ("El 70% de las búsquedas de servicios locales se hacen desde el teléfono", "Muchas búsquedas de servicios locales se hacen desde el teléfono"),
 ("El 70% de les cerques de serveis locals es fan des del telèfon", "Moltes cerques de serveis locals es fan des del telèfon"),
 ("El 70% de les cerques de servicis locals es fan des del telèfon", "Moltes cerques de servicis locals es fan des del telèfon"),
 ("70% of local service searches are done from phones", "Many local service searches are done from phones"),
 ("70% of searches for local services are done from the phone", "Many searches for local services are done from the phone"),
 ("70 % des recherches de services de proximité se font depuis un téléphone", "Une grande partie des recherches de services de proximité se fait depuis un téléphone"),
 ("El 70% de las búsquedas locales se hacen desde el teléfono", "Muchas búsquedas locales se hacen desde el teléfono"),
 ("El 70% de les cerques locals es fan des del telèfon", "Moltes cerques locals es fan des del telèfon"),
 ("70% of local searches are done from a mobile phone", "Many local searches are done from a mobile phone"),
 # ── Menuisiers / réformes ─────────────────────────────────────────────
 ("El sector de la carpintería y las reformas en España facturó más de 42.000 millones de euros en 2025, y la tendencia sigue al alza. Pero el 73% de los clientes que buscan una empresa de reformas empiezan por Google.",
  "Cada vez más clientes buscan en Google antes de encargar una reforma o un mueble a medida."),
 ("El sector de la fusteria i les reformes a Espanya va facturar més de 42.000 milions d'euros en 2025, i la tendència continua a l'alça. Però el 73% dels clients que busquen una empresa de reformes comencen per Google.",
  "Cada vegada més clients busquen a Google abans d'encarregar una reforma o un moble a mida."),
 ("The carpentry and renovation sector in Spain billed over 42 billion euros in 2025, and the trend keeps rising. But 73% of clients looking for a renovation company start with Google.",
  "More and more clients search on Google before hiring someone for a renovation or a piece of custom furniture."),
 ("Le secteur de la menuiserie et de la rénovation pèse des dizaines de milliards d'euros en Europe, et la tendance reste à la hausse. Mais voici le problème : <strong>73 % des clients qui cherchent une entreprise de rénovation commencent par Google</strong>.",
  "De plus en plus de clients cherchent sur Google avant de confier un chantier de rénovation ou un meuble sur mesure."),
 ("El 87% de los clientes potenciales de reformas afirman que las fotos de proyectos anteriores son el factor decisivo para pedir un presupuesto.",
  "Para muchos clientes, las fotos de proyectos anteriores son lo que les decide a pedir un presupuesto."),
 ("El 87% dels clients potencials de reformes afirmen que les fotos de projectes anteriors són el factor decisiu per a demanar un pressupost.",
  "Per a molts clients, les fotos de projectes anteriors són el que els decidix a demanar un pressupost."),
 ("87% of potential renovation clients say photos of previous projects are the decisive factor when requesting a quote.",
  "For many clients, photos of previous projects are what makes them request a quote."),
 ("87 % des clients potentiels en rénovation déclarent que les photos de chantiers antérieurs sont le facteur décisif pour demander un devis.",
  "Pour beaucoup de clients, les photos de chantiers antérieurs sont ce qui les décide à demander un devis."),
 ("El 87% de los clientes revisan trabajos anteriores antes de pedir presupuesto.", "Los clientes suelen mirar trabajos anteriores antes de pedir presupuesto."),
 ("El 87% dels clients revisen treballs anteriors antes de pedir pressupost.", "Els clients solen mirar treballs anteriors abans de demanar pressupost."),
 ("87% of customers look at previous work before requesting a quote.", "Customers usually look at previous work before requesting a quote."),
 ("87 % des clients examinent les chantiers antérieurs avant de demander un devis.", "Les clients regardent en général les chantiers antérieurs avant de demander un devis."),
 ("Casos reales: carpinteros y reformistas que triunfan con su web", "Qué cambia una web para un carpintero o una empresa de reformas"),
 ("Casos reals: fusters i reformistes que triomfen amb la seua web", "Què canvia una web per a un fuster o una empresa de reformes"),
 ("Real cases: carpenters and renovators thriving with their website", "What a website changes for a carpenter or a renovation company"),
 ("Cas réels : des artisans que leur site a fait décoller", "Ce qu'un site change pour un menuisier ou une entreprise de rénovation"),
 ("Antonio, carpintero en Elda, llevaba 15 años trabajando solo por recomendación. Cuando creó su web con una galería de muebles a medida, empezó a recibir consultas de clientes en Petrer, Novelda y Monóvar. En seis meses, su facturación creció un 35%. Reformas Martínez en Alicante pasó de 2-3 presupuestos al mes a 12-15 gracias a su portfolio de antes y después.",
  "Una web no hace milagros, pero cambia una cosa: los clientes que no te conocen pueden encontrarte, ver tus trabajos y contactarte sin depender de una recomendación. Para un carpintero en Elda o una empresa de reformas en Alicante, eso significa consultas de pueblos y barrios donde antes nadie sabía que existías, y clientes que llegan habiendo visto ya tu portfolio de antes y después."),
 ("Antonio, fuster a Elda, portava 15 anys treballant només per recomanació. Quan va crear la seua web amb una galeria de mobles a mida, va començar a rebre consultes de clients a Petrer, Novelda i Monòver. En sis mesos, la seua facturació va créixer un 35%. Reformes Martínez a Alacant va passar de 2-3 pressupostos al mes a 12-15 gràcies al seu portfoli d'abans i després.",
  "Una web no fa miracles, però canvia una cosa: els clients que no et coneixen poden trobar-te, veure els teus treballs i contactar amb tu sense dependre d'una recomanació. Per a un fuster a Elda o una empresa de reformes a Alacant, això significa consultes de pobles i barris on abans ningú sabia que existies, i clients que arriben havent vist ja el teu portfoli d'abans i després."),
 ("Antonio, a carpenter in Elda, spent 15 years working solely through referrals. When he created his website with a gallery of custom furniture, he started receiving enquiries from clients in Petrer, Novelda and Monovar. Within six months his turnover grew by 35%. Reformas Martinez in Alicante went from 2-3 quotes per month to 12-15 thanks to their before-and-after portfolio.",
  "A website does not work miracles, but it changes one thing: clients who do not know you can find you, see your work and contact you without depending on a referral. For a carpenter in Elda or a renovation company in Alicante, that means enquiries from towns and neighbourhoods where nobody knew you existed, from clients who have already seen your before-and-after portfolio."),
 ("La théorie, c'est bien, mais ce sont les résultats qui convainquent. Voici des exemples réels de la façon dont un <strong>site de menuiserie</strong> bien fait change une entreprise.",
  "Un <strong>site de menuiserie</strong> ne fait pas de miracles, mais il change une chose : les clients qui ne vous connaissent pas peuvent vous trouver, voir vos réalisations et vous contacter sans passer par une recommandation."),
 ("<strong>Antoine, menuisier à Renens :</strong> il travaillait depuis 15 ans uniquement sur recommandation. Quand il a créé son site avec une galerie de meubles sur mesure et de placards encastrés, il a commencé à recevoir des demandes de clients de Morges, Pully et Écublens qui ne l'auraient jamais trouvé. En six mois, son chiffre d'affaires a progressé de 35 %.",
  "<strong>Pour un menuisier :</strong> c'est l'occasion de montrer ses meubles sur mesure et ses placards encastrés à des clients des communes voisines qui n'auraient jamais entendu parler de lui."),
 ("<strong>Rénovations Martin, à Genève :</strong> cette entreprise familiale avait un compte Instagram de 800 abonnés, mais aucun site. Quand ils ont créé leur page avec un portfolio avant/après, un formulaire de devis et des témoignages, ils sont passés de 2 ou 3 devis par mois à 12 ou 15. Ce qui a le plus pesé, c'est la galerie de cuisines rénovées : 60 % des contacts cherchaient exactement cela.",
  "<strong>Pour une entreprise de rénovation :</strong> un portfolio avant/après, un formulaire de devis simple et des avis clients vérifiables en disent souvent plus qu'un compte Instagram, parce que le client y trouve en une minute ce qu'il cherche."),
 ("<strong>Charles, spécialiste de la rénovation de salles de bains à Lausanne :</strong> Charles a choisi de consacrer son site exclusivement aux salles de bains. Il a produit du contenu précis, comme « Rénover une salle de bains à Lausanne : prix, délais et options » ou « Remplacer une baignoire par une douche à Lausanne ». En quatre mois, il figurait en première page de Google sur ces recherches, face à des entreprises bien plus grandes que la sienne.",
  "<strong>Pour un spécialiste :</strong> un site consacré à un seul type de chantier, par exemple la salle de bains, avec des pages claires sur les prix, les délais et les options, a plus de chances d'apparaître sur les recherches correspondantes qu'un site qui annonce « nous faisons tout »."),
 ("Ces exemples confirment ce que nous expliquions", "Cela rejoint ce que nous expliquions"),
 ("porque el 70% de las búsquedas locales se hacen desde el teléfono", "porque muchos clientes te buscarán desde el teléfono"),
 ("perquè el 70% de les búsquedes locals es fan des del telèfon", "perquè molts clients et buscaran des del telèfon"),
 ("because 70% of local searches are made on a phone", "because many customers will look for you on their phone"),
 ("car 70 % des recherches de proximité se font depuis un téléphone", "car beaucoup de clients vous chercheront depuis leur téléphone"),
 ("70 % des recherches en rénovation se font depuis un mobile.", "Beaucoup de clients vous chercheront depuis leur téléphone."),
 ("El 70% de las búsquedas de reformas se hacen desde el móvil.", "Muchas búsquedas de reformas se hacen desde el móvil."),
 ("El 70% de les búsquedes de reformes es fan des del mòbil.", "Moltes cerques de reformes es fan des del mòbil."),
 ("70% of renovation searches are done on mobile.", "Many renovation searches are done on mobile."),
 # ── Autres « 70 % » ───────────────────────────────────────────────────
 ("Bonus: ahorra 70% del tiempo.", "Bonus: ahorra mucho tiempo."),
 ("Bonus: estalvia 70% del temps.", "Bonus: estalvia molt de temps."),
 ("Bonus: it saves 70% of the time.", "Bonus: it saves a lot of time."),
 ("This saves 70% of time.", "This saves a lot of time."),
 ("En prime, elle fait gagner 70 % du temps.", "En prime, elle fait gagner beaucoup de temps."),
 ("publicar sin imagen (70% menos de interacciones)", "publicar sin imagen (reciben menos interacciones)"),
 ("publicar sense imatge (70% menys d'interaccions)", "publicar sense imatge (reben menys interaccions)"),
 ("posting without an image (70% fewer interactions)", "posting without an image (fewer interactions)"),
 ("Los posts sin imagen reciben un 70% menos de interacciones.", "Los posts sin imagen reciben menos interacciones."),
 ("Els posts sense imatge reben un 70% menys d'interaccions.", "Els posts sense imatge reben menys interaccions."),
 ("Posts without images get 70% fewer interactions.", "Posts without images get fewer interactions."),
 ("les posts sans image reçoivent 70 % d'interactions en moins.", "les posts sans image reçoivent moins d'interactions."),
 ("Recuerda que más del 70% de las visitas a webs de autónomos locales llegan desde el teléfono.", "Recuerda que muchas visitas a webs de autónomos locales llegan desde el teléfono."),
 ("Recorda que més del 70% de les visites a webs d'autònoms locals arriben des del telèfon.", "Recorda que moltes visites a webs d'autònoms locals arriben des del telèfon."),
 ("Recuerda que más del 70% de las visitas llegan desde el móvil.", "Recuerda que muchas visitas llegarán desde el móvil."),
 ("Recorda que més del 70% de les visites arriben des del mòbil.", "Recorda que moltes visites arribaran des del mòbil."),
 ("Remember that over 70% of visits to local business websites come from mobile devices.", "Remember that many visits to local business websites come from mobile devices."),
 ("Remember that over 70% of visits to local freelancer websites come from phones.", "Remember that many visits to local freelancer websites come from phones."),
 ("Rappelez-vous que plus de 70 % des visites sur les sites d'indépendants locaux arrivent depuis un téléphone.", "Rappelez-vous qu'une grande partie des visites sur les sites d'indépendants locaux arrive depuis un téléphone."),
 ("Muchos autónomos en Valencia y Alicante nos dicen que el 60-70% de sus contactos desde la web llegan por WhatsApp, no por el formulario.", "Muchos contactos desde la web llegan por WhatsApp y no por el formulario."),
 ("Molts autònoms en València i Alacant mos diuen que el 60-70% dels seus contactes des de la web arriben per WhatsApp, no pel formulari.", "Molts contactes des de la web arriben per WhatsApp i no pel formulari."),
 ("Many freelancers in Valencia and Alicante tell us that 60 to 70% of the enquiries coming from their website arrive through WhatsApp, not through the form.", "Many enquiries from a website arrive through WhatsApp rather than the form."),
 ("Beaucoup d'indépendants nous rapportent que 60 à 70 % de leurs contacts issus du site arrivent par WhatsApp, et non par le formulaire.", "Une bonne partie des contacts issus d'un site arrive souvent par WhatsApp plutôt que par le formulaire."),
 ("Más del 70% de las búsquedas de salud se hacen desde el móvil.", "Muchas búsquedas de salud se hacen desde el móvil."),
 ("Més del 70% de les búsquedes de salut se fan des del mòbil.", "Moltes cerques de salut es fan des del mòbil."),
 ("Més del 70% de les cerques de salut es fan des del mòbil.", "Moltes cerques de salut es fan des del mòbil."),
 ("Over 70% of health-related searches are made from mobile devices.", "Many health-related searches are made from mobile devices."),
 ("Over 70% of healthcare searches are done from mobile.", "Many healthcare searches are done from mobile."),
 ("plus de 70 % des recherches de santé se font depuis un téléphone.", "une grande partie des recherches de santé se fait depuis un téléphone."),
 ("(en 2026, el 70% de visitas son móvil)", "(hoy muchas visitas llegan desde el móvil)"),
 ("(en 2026, el 70% de visites són mòbil)", "(hui moltes visites arriben des del mòbil)"),
 ("(in 2026, 70% of visits are mobile)", "(many visits now come from mobile)"),
 ("(70% of visits are mobile in 2026)", "(many visits now come from mobile)"),
 ("(en 2026, 70 % des visites viennent d'un téléphone)", "(aujourd'hui, beaucoup de visites viennent d'un téléphone)"),
]
T += [
 ("Un caso real: María, fisioterapeuta en Valencia, añadió los 7 elementos y sus solicitudes de cita se triplicaron en dos meses. No cambió nada de su servicio: solo mejoró su web.",
  "Piensa, por ejemplo, en una fisioterapeuta en Valencia: sin cambiar su servicio ni sus precios, completar estos 7 elementos hace que un paciente que no la conoce encuentre en su web todo lo que necesita para pedir cita."),
 ("Un cas real: Maria, fisioterapeuta a València, va afegir els 7 elements i les seues sol·licituds de cita es van triplicar en dos mesos. No va canviar res del seu servei: només va millorar la seua web.",
  "Pensa, per exemple, en una fisioterapeuta a València: sense canviar el seu servei ni els seus preus, completar estos 7 elements fa que un pacient que no la coneix trobe a la seua web tot el que necessita per a demanar cita."),
 ("A real case: Maria, a physiotherapist in Valencia, added the 7 elements and her appointment requests tripled in two months. She didn't change her service or prices -- she only improved her website.",
  "Take a physiotherapist in Valencia, for example: without changing her service or prices, completing these 7 elements means a patient who does not know her finds everything needed to book an appointment on her website."),
 ("Un cas réel : Marie, kinésithérapeute à Lyon, avait un site réduit à un bandeau générique et un numéro de téléphone. Après avoir ajouté les 7 éléments décrits ici, ses demandes de rendez-vous ont <strong>triplé en deux mois</strong>. Elle n'a changé ni sa prestation ni ses tarifs : seulement son site.",
  "Prenez l'exemple d'un kinésithérapeute dont le site se résume à un bandeau générique et un numéro de téléphone : sans changer ni sa prestation ni ses tarifs, ajouter les 7 éléments décrits ici permet à un patient qui ne le connaît pas de trouver <strong>tout ce qu'il faut pour prendre rendez-vous</strong>."),
 ("Un caso real: Antonio, cerrajero en Valencia, cambió de \"Servicio de cerraduras\" a \"Cerrajero\" y pasó de la posición 8 a la 3 en el Map Pack en solo tres semanas.",
  "Por ejemplo, un cerrajero que tiene «Servicio de cerraduras» como categoría principal compite peor en las búsquedas de «cerrajero» que uno que elige «Cerrajero»: la categoría principal debe coincidir con lo que escribe el cliente."),
 ("Un cas real: Antonio, manyoner a València, va canviar de \"Servei de panys\" a \"Manyoner\" i va passar de la posició 8 a la 3 en el Map Pack en només tres setmanes.",
  "Per exemple, un manyoner que té «Servei de panys» com a categoria principal competix pitjor en les cerques de «manyoner» que un que tria «Manyoner»: la categoria principal ha de coincidir amb el que escriu el client."),
 ("A real case: Antonio, a locksmith in Valencia, switched from \"Lock service\" to \"Locksmith\" and went from position 8 to position 3 in the Map Pack in just three weeks.",
  "For example, a locksmith whose primary category is “Lock service” competes less well on searches for “locksmith” than one who chooses “Locksmith”: the primary category should match what the customer types."),
 ("Un cas réel : Antoine, serrurier à Lyon, avait « Service de serrures » comme catégorie principale. Après avoir analysé ses concurrents et basculé sur « Serrurier », il est passé de la 8e à la 3e position du Map Pack pour « serrurier Lyon » en trois semaines seulement. Un seul changement, un effet considérable.",
  "Prenons un serrurier qui a « Service de serrures » comme catégorie principale : il se positionne moins bien sur « serrurier » qu'un concurrent qui a choisi « Serrurier ». La catégorie principale doit correspondre à ce que tape le client ; c'est un seul réglage, mais il compte."),
 ("Un cas réel : Pierre, menuisier à Lausanne, avait un site qui se contentait d'annoncer « menuiserie et rénovation ». Après avoir travaillé ses mots-clés, il a changé ses titres en « Menuisier à Lausanne : mobilier sur mesure et rénovation » et créé une page dédiée à « cuisines sur mesure Lausanne ». En trois mois, il est passé de 0 à 8 contacts mensuels depuis Google. Sans dépenser un euro en publicité.",
  "Prenons un menuisier dont le site se contente d'annoncer « menuiserie et rénovation ». En changeant ses titres en « Menuisier à Lausanne : mobilier sur mesure et rénovation » et en créant une page dédiée aux « cuisines sur mesure Lausanne », il donne enfin à Google de quoi le proposer sur les recherches de ses futurs clients, sans dépenser un euro en publicité."),
 ("Un cas réel : Marc, serrurier qui a déménagé d'un local du centre de Lyon vers la Croix-Rousse, avait son ancienne adresse dans 8 annuaires différents. Tant qu'il ne les a pas tous corrigés, son positionnement dans Google Maps n'a pas bougé.",
  "Prenons un artisan qui déménage et dont l'ancienne adresse reste dans plusieurs annuaires : il envoie à Google des informations contradictoires, et tant qu'elles ne sont pas toutes corrigées, sa fiche a du mal à progresser dans Google Maps."),
 ("<strong>Un cas réel :</strong> Jérôme, serrurier à Nantes, s'est mis à publier un Google Post chaque lundi avec la photo de son dernier chantier de la semaine. En deux mois seulement, les interactions avec sa fiche ont augmenté de 45 % et les appels directs depuis Google Maps sont passés de 8 à 14 par mois. « Ce sont 5 minutes chaque lundi qui me génèrent du travail pour toute la semaine », nous a-t-il raconté.",
  "<strong>Un exemple de routine :</strong> publier un Google Post chaque lundi avec la photo du dernier chantier de la semaine. Cela prend quelques minutes, montre que l'entreprise est active et donne aux clients une raison de plus d'appeler."),
 ("<strong>Un cas réel :</strong> Lucie, esthéticienne à Nantes, avait une fiche Google à moitié remplie et 4 avis. Après trois mois de cette stratégie, elle affichait 32 avis à 5 étoiles, un site optimisé et des publications hebdomadaires. Résultat : elle est apparue dans le Map Pack sur « esthéticienne Nantes » et est passée de 3 appels par mois depuis Google à 18. Sans dépenser un euro en publicité.",
  "<strong>En pratique :</strong> une fiche Google à moitié remplie avec quelques avis a peu de chances d'apparaître dans le Map Pack. Une fiche complète, des avis réguliers, un site optimisé et des publications hebdomadaires sont les leviers qui permettent d'y entrer, sans dépenser un euro en publicité."),
 ("Un cas réel positif : Laure, kinésithérapeute à Lyon, a obtenu en 6 mois seulement 8 backlinks locaux de qualité : le site de l'ordre professionnel des kinésithérapeutes, deux blogs santé locaux, le site du marathon de Lyon qu'elle a parrainé, un annuaire santé et trois sites de clients satisfaits l'ayant citée. Avec ces 8 liens seulement, elle est passée de la troisième page de Google à la première sur « kinésithérapeute Lyon ». La qualité l'emporte toujours sur la quantité.",
  "Pour un kinésithérapeute, par exemple, les bons liens locaux se trouvent naturellement : le site de l'ordre professionnel, des blogs santé de sa ville, un événement sportif local parrainé, un annuaire santé. Quelques liens de ce type valent mieux que des dizaines de liens sans rapport : la qualité l'emporte sur la quantité."),
 ("Un cas réel qui illustre la force de la mesure : Antoine, plombier à Lyon, a découvert grâce à la Search Console qu'il apparaissait en position 8 sur « plombier urgence Lyon » (la deuxième page de Google, que personne ne regarde). Il a optimisé le titre de sa page urgences, ajouté du contenu spécifique sur les interventions d'urgence et obtenu 3 avis mentionnant « urgence ». En 6 semaines, il est passé en position 3. Il est passé de 0 à 7 appels par mois pour des urgences.",
  "Un exemple de ce que permet la mesure : un plombier découvre dans la Search Console qu'il apparaît en position 8 sur « plombier urgence Lyon », en deuxième page, que presque personne ne regarde. En optimisant le titre de sa page urgences, en ajoutant du contenu précis sur ses interventions d'urgence et en obtenant des avis qui les mentionnent, il se donne les moyens de remonter en première page."),
 ("Un cas réel : Marie, coiffeuse dans le centre de Lyon, avait 12 avis pour une moyenne de 4,1. Elle a reçu un 1 étoile d'une cliente qui avait confondu son salon avec un autre. Elle a répondu professionnellement, et a lancé en parallèle son système de demande d'avis. En deux mois, elle a obtenu 30 avis supplémentaires, est montée à 4,6 de moyenne, et l'avis négatif s'est retrouvé noyé sous des dizaines de retours positifs. Elle reçoit aujourd'hui deux fois plus d'appels depuis Google Maps.",
  "Prenons une coiffeuse qui reçoit un avis 1 étoile d'une cliente qui l'a confondue avec un autre salon. Elle répond de façon professionnelle et lance en parallèle un système de demande d'avis : au fil des semaines, les nouveaux avis positifs replacent cet avis isolé dans son contexte."),
 ("Un cas réel : Raphaël, peintre à Bruxelles, a suivi ce plan à la lettre. En 6 mois, il est passé d'une dépendance totale au bouche-à-oreille à 12 contacts mensuels depuis Google et 3 à 4 depuis les réseaux sociaux. Le plus parlant : les contacts venus de Google se transformaient en clients dans 60 % des cas, contre 20 % seulement pour ceux venus des réseaux. De quoi lui confirmer où investir son temps.",
  "Suivre ce plan permet de mesurer, au bout de quelques mois, d'où viennent vraiment les contacts et lesquels deviennent des clients : c'est ce qui indique où investir son temps."),
 ("Un cas réel : Antoine, menuisier à Nantes, a installé un Schema de type « Carpenter » sur son site. Il y a mis son adresse exacte, ses horaires réels, sa zone d'intervention (Nantes, Saint-Herblain, Rezé) et le lien vers sa fiche Google. En six semaines, Google s'est mis à afficher son résultat avec les étoiles et les horaires sur les recherches « menuisier Nantes ». Ses clics depuis Google ont augmenté de 25 % sans rien changer d'autre.",
  "Prenons un menuisier qui installe un Schema de type « Carpenter » sur son site, avec son adresse exacte, ses horaires réels, sa zone d'intervention et le lien vers sa fiche Google : il donne à Google des informations claires et cohérentes, que le moteur peut ensuite reprendre dans ses résultats."),
 ("Un cas réel : le cabinet dentaire Les Tilleuls, à Bruxelles, n'avait qu'une page sur les réseaux sociaux depuis trois ans. Quand ils ont créé leur site professionnel, avec le détail des soins et la prise de rendez-vous, les demandes de première consultation ont augmenté de 40 % en deux mois. La raison ? Les patients qui cherchaient « dentiste Bruxelles » dans Google pouvaient enfin les trouver directement.",
  "Un cabinet dentaire qui n'a qu'une page sur les réseaux sociaux reste invisible pour les patients qui cherchent « dentiste » et le nom de leur ville sur Google. Un site professionnel, avec le détail des soins et la prise de rendez-vous, leur permet enfin de le trouver directement."),
 ("<strong>Un cas réel :</strong> Antoine, plombier à Lausanne avec 12 ans de métier, a monté son site avec nous en janvier. En 6 semaines, il a reçu 14 appels venus de Google, qui se sont traduits par 9 chantiers confirmés. « Avant, les clients ne venaient que par le bouche-à-oreille. Maintenant, des gens qui ne me connaissent pas m'appellent parce qu'ils voient mon site et qu'ils me font confiance », nous a-t-il raconté. Le tout pour 15 €/mois.",
  "<strong>Ce qui change avec un site :</strong> les clients ne viennent plus seulement par le bouche-à-oreille. Des gens qui ne vous connaissent pas vous appellent parce qu'ils ont vu votre site et vos réalisations. Chez WebAutonomos, ce site coûte 15 € HT par mois."),
 ("Un caso real: las cinco en un mismo proyecto", "Un caso típico: las cinco en un mismo proyecto"),
 ("Un cas real: els cinc en un mateix projecte", "Un cas típic: els cinc en un mateix projecte"),
 ("A real case: all five in one project", "A typical case: all five in one project"),
 ("Un cas réel : les cinq dans un même projet", "Un cas typique : les cinq dans un même projet"),
]
for a, b in T:
    assert '"' not in b and '\\' not in b, b

FICHIERS = (sorted(glob.glob('blog/*/*.html')) + ['index.html', 'blog-spa-data.json']
            + sorted(glob.glob('_tools/translations/*.json')) + sorted(glob.glob('_tools/queue/published/*.json')))

total = {}
for f in FICHIERS:
    try:
        s = open(f, encoding='utf-8').read()
    except FileNotFoundError:
        continue
    o = s
    for a, b in T:
        rx = re.compile(fz(a))
        s, n = rx.subn(lambda m: b, s)
        if n:
            total[a] = total.get(a, 0) + n
    if s != o:
        if f.endswith('.json'):
            json.loads(s)  # doit rester du JSON valide
        if APPLY:
            open(f, 'w', encoding='utf-8').write(s)
        print(('écrit ' if APPLY else 'à modifier ') + f)
print('--- fragments trouvés :')
for a, b in T:
    print(f'{total.get(a, 0):3}  {a[:90]}')
print('TOTAL', sum(total.values()), '| fragments jamais trouvés :', sum(1 for a, _ in T if not total.get(a)))
