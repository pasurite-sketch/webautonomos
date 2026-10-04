# -*- coding: utf-8 -*-
"""Chiffres sans source « entre 5 et 15 » retirés (demande d'Angelino du 04/10/2026). Idempotent.

VERITE.md §7 (aucun chiffre ni résultat sans source) et REGLES_REDACTEUR.md §2 bis (« la mayoría »,
« most », « la plupart » interdits comme faits) :
1. FAQ « combien puis-je économiser avec l'IA ? » (ES, VAL, EN, FR) : « entre 5 y 15 horas semanales »
   remplacé par une méthode pour mesurer soi-même le temps gagné.
2. Électriciens (EN, VAL, FR) : « entre 5 et 15 prises de contact par mois » retiré (FAQ, et corps FR).
3. Budget marketing (VAL, EN) : « entre 5 i 15 contactes mensuals » retiré.
Pages statiques (texte visible et JSON-LD) et données du blog de index.html.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

R = [
    # (fichiers, ancien, nouveau)
    # 1. IA
    (['blog/es/inteligencia-artificial-autonomos-herramientas.html', 'index.html'],
     'Depende de tu negocio, pero la mayoría de autónomos ahorran entre 5 y 15 horas semanales, que equivalen a cientos de euros en tiempo productivo.',
     'Depende de tu negocio y de las tareas que delegues. Mide el tiempo que dedicas hoy a tareas repetitivas, como redactar borradores, responder preguntas frecuentes o resumir documentos, compáralo al cabo de unas semanas usando IA y multiplica las horas recuperadas por lo que vale tu hora.'),
    (['blog/val/ia-per-a-autonoms-eines-concretes.html', 'index.html'],
     "Depén del teu negoci, però la majoria d'autònoms estalvien entre 5 i 15 hores setmanals, que equivalen a centenars d'euros en temps productiu.",
     'Depén del teu negoci i de les tasques que delegues. Mesura el temps que dediques hui a tasques repetitives, com redactar esborranys, respondre preguntes freqüents o resumir documents, compara-ho passades unes setmanes usant IA i multiplica les hores recuperades pel que val la teua hora.'),
    (['blog/val/ia-per-a-autonoms-eines-concretes.html'],  # texte visible : apostrophes échappées
     'Depén del teu negoci, però la majoria d&#x27;autònoms estalvien entre 5 i 15 hores setmanals, que equivalen a centenars d&#x27;euros en temps productiu.',
     'Depén del teu negoci i de les tasques que delegues. Mesura el temps que dediques hui a tasques repetitives, com redactar esborranys, respondre preguntes freqüents o resumir documents, compara-ho passades unes setmanes usant IA i multiplica les hores recuperades pel que val la teua hora.'),
    (['blog/en/ai-for-freelancers-practical-tools.html', 'index.html'],
     'It depends on your business, but most freelancers save between 5 and 15 hours a week, which is worth hundreds of euros in productive time.',
     'It depends on your business and the tasks you hand over. Measure the time you spend today on repetitive tasks, such as drafting texts, answering frequent questions or summarising documents, compare it after a few weeks of using AI and multiply the hours you get back by what your hour is worth.'),
    (['blog/fr/ia-pour-independants-outils-concrets.html'],
     "Cela dépend de votre activité, mais la plupart des indépendants économisent entre 5 et 15 heures par semaine, ce qui représente des centaines d'euros de temps productif.",
     "Cela dépend de votre activité et des tâches que vous confiez à l'IA. Mesurez le temps que vous consacrez aujourd'hui aux tâches répétitives, comme rédiger des brouillons, répondre aux questions fréquentes ou résumer des documents, comparez-le après quelques semaines d'utilisation et multipliez les heures récupérées par la valeur de votre heure."),
    # 2. Électriciens
    (['blog/en/website-for-electricians.html', 'index.html'],
     'An electrician with a site ranking for electrician in Valencia can receive between five and fifteen enquiries a month through Google without paying for advertising.',
     'An electrician whose site appears when people search for an electrician in Valencia can receive enquiries through Google without paying for advertising.'),
    (['blog/val/pagina-web-per-a-electricistes.html', 'index.html'],
     'pot rebre entre 5 i 15 contactes mensuals des de Google sense pagar publicitat.',
     'pot rebre peticions de clients des de Google sense pagar publicitat.'),
    (['blog/fr/site-web-pour-electriciens.html'],
     'peut recevoir de 5 à 15 prises de contact par mois depuis Google sans payer de publicité.',
     'peut recevoir des demandes de clients depuis Google sans payer de publicité.'),
    (['blog/fr/site-web-pour-electriciens.html'],
     'un site simple mais rapide et bien optimisé génère entre 5 et 15 prises de contact par mois.',
     'un site simple mais rapide et bien optimisé a plus de chances de faire sonner le téléphone.'),
    # 3. Budget marketing
    (['blog/val/pressupost-de-marketing-digital.html', 'index.html'],
     'Un autonom ben posicionat en una ciutat mitjana com Elda o Elx rep entre 5 i 15 contactes mensuals des de Google.',
     'Un autònom ben posicionat en una ciutat mitjana com Elda o Elx pot rebre peticions de clients des de Google cada mes.'),
    (['blog/en/digital-marketing-budget-for-freelancers.html', 'index.html'],
     'A well-positioned freelancer in a mid-sized city like Elda or Elche receives between 5 and 15 monthly contacts from Google.',
     'A well-positioned freelancer in a mid-sized city like Elda or Elche can receive enquiries from Google every month.'),
]

for fichiers, ancien, nouveau in R:
    n_total, deja = 0, 0
    for f in fichiers:
        p = os.path.join(ROOT, f)
        s = open(p, encoding='utf-8').read()
        n = s.count(ancien)
        if n:
            open(p, 'w', encoding='utf-8').write(s.replace(ancien, nouveau))
            n_total += n
        elif nouveau in s:
            deja += 1
    if not n_total and not deja:
        raise SystemExit('introuvable : ' + ancien[:70])
    print('%2d remplacement(s), %d fichier(s) déjà à jour : %s' % (n_total, deja, ancien[:62]))
