# -*- coding: utf-8 -*-
"""Mention « deux minutes » du diagnostic (07/10/2026) : deux minutes = quatre questions et le coût annuel ;
le verdict, la part récupérable et le délai de retour demandent six questions de plus (VERITE §5 bis)."""
import json, re, sys
L = [
 # EN
 ('blog/en/automate-without-coding.html', "puts numbers on a task in two minutes and tells you which side of that line yours falls on.", "puts a figure on a task's annual cost in about two minutes; six more questions tell you which side of that line yours falls on."),
 ('blog/en/costliest-automation-mistakes.html', "puts numbers on a task in two minutes — and, in doing so, puts you through the five-mistake test without even thinking about it.", "puts numbers on a task in two minutes."),
 ('blog/en/e-invoicing-deadlines-france-spain.html', "that works it out in two minutes: four questions, the result on screen, and it tells you whether automating that task is worth it or not.", "that works out a task's annual cost in about two minutes, with four questions and the result on screen; six more questions tell you whether automating it is worth it or not."),
 ('blog/en/hire-or-automate.html', "estimates yours in about two minutes.", "works out what the task costs you today in about two minutes; six more questions estimate what can be recovered and how long it takes to pay back."),
 ('blog/en/how-automating-a-process-works-step-by-step.html', "does it in about two minutes, with no commitment: four questions, a result on screen and a clear answer on whether automating it is worthwhile.", "works out its annual cost in about two minutes, with no commitment: four questions and a result on screen; six more questions give a clear answer on whether automating it is worthwhile."),
 ('blog/en/maintenance-the-hidden-cost-of-automation.html', "it puts a figure on a task in about two minutes, taking into account what it will cost to keep running, not just to build, with the result on screen and no commitment.", "it puts a figure on a task's annual cost in about two minutes, then six more questions work out the payback, taking into account what the automation will cost to keep running, not just to build, with the result on screen and no commitment."),
 ('blog/en/what-paperwork-really-costs-a-freelancer.html', "works it out in about two minutes: four questions about one task, the result on screen and no commitment, and it tells you whether automating that task is worth it.", "works out the annual cost of one task in about two minutes: four questions, the result on screen and no commitment; six more questions tell you whether automating that task is worth it."),
 # ES
 ('blog/es/automatizar-sin-saber-programar.html', "pone números a una tarea en dos minutos y te dice de qué lado de esa línea cae la tuya.", "pone cifra al coste anual de una tarea en unos dos minutos y, con seis preguntas más, te dice de qué lado de esa línea cae la tuya."),
 ('blog/es/como-es-automatizar-un-proceso-paso-a-paso.html', "lo hace en unos dos minutos, sin compromiso: cuatro preguntas, un resultado en pantalla y una respuesta clara sobre si compensa automatizarla.", "calcula su coste anual en unos dos minutos, sin compromiso: cuatro preguntas y un resultado en pantalla; con seis preguntas más, una respuesta clara sobre si compensa automatizarla."),
 ('blog/es/contratar-o-automatizar.html', "que cifra una tarea en dos minutos y te dice si automatizarla compensa o no.", "que cifra el coste anual de una tarea en unos dos minutos y, con seis preguntas más, te dice si automatizarla compensa o no."),
 ('blog/es/cuanto-cuesta-papeleo-autonomo.html', "que te lo calcula en dos minutos: cuatro preguntas, resultado en pantalla, y te dice si automatizar esa tarea compensa o no.", "que te lo calcula en unos dos minutos: cuatro preguntas y resultado en pantalla; con seis más, te dice si automatizar esa tarea compensa o no."),
 ('blog/es/factura-electronica-plazos-2026-2027.html', "que lo calcula en dos minutos, con el resultado en pantalla, y te dice si automatizar esa tarea compensa o no.", "que calcula su coste anual en unos dos minutos, con el resultado en pantalla, y, con seis preguntas más, te dice si automatizar esa tarea compensa o no."),
 ('blog/es/mantenimiento-coste-automatizacion.html', "cifra una tarea en dos minutos teniendo en cuenta lo que costará mantenerla viva, no solo montarla.", "cifra el coste anual de una tarea en unos dos minutos y, con seis preguntas más, el plazo de retorno teniendo en cuenta lo que costará mantener viva la automatización, no solo montarla."),
 ('blog/es/que-no-deberias-automatizar-nunca.html', "pone números a una tarea en dos minutos y te dice si merece automatizarse,", "pone cifra al coste anual de una tarea en unos dos minutos y, con seis preguntas más, te dice si merece automatizarse,"),
 # FR
 ('blog/fr/ce-que-la-paperasse-coute-vraiment.html', "en environ deux minutes et à partir d'une seule tâche, il affiche le résultat à l'écran, sans engagement, et vous dit s'il vaut la peine de la confier à un logiciel ou non.", "en environ deux minutes et à partir d'une seule tâche, il affiche son coût annuel à l'écran, sans engagement ; avec six questions de plus, il vous dit s'il vaut la peine de la confier à un logiciel ou non."),
 ('blog/fr/comment-se-passe-l-automatisation-etape-par-etape.html', ", en deux minutes et sans engagement : quatre questions, un résultat à l'écran, et une réponse honnête — oui, non, ou pas encore.", ", sans engagement : quatre questions et environ deux minutes pour le coût annuel, puis six questions de plus pour une réponse honnête — oui, non, ou pas encore."),
 ('blog/fr/comment-se-passe-l-automatisation-etape-par-etape.html', "vous aurez économisé bien plus que deux minutes.", "vous aurez économisé bien plus que quelques minutes."),
 ('blog/fr/comment-se-passe-l-automatisation-etape-par-etape.html', "le fait en deux minutes, sans engagement : quatre questions, un résultat à l'écran, et une réponse claire sur l'intérêt d'automatiser cette tâche précise.", "chiffre son coût annuel en environ deux minutes, sans engagement : quatre questions et un résultat à l'écran ; avec six questions de plus, une réponse claire sur l'intérêt d'automatiser cette tâche précise."),
 ('blog/fr/embaucher-ou-automatiser.html', "qui chiffre une tâche en deux minutes : quatre questions, résultat à l'écran, et il vous dit si l'automatiser vaut le coup ou non.", "qui chiffre le coût annuel d'une tâche en environ deux minutes : quatre questions, résultat à l'écran ; avec six de plus, il vous dit si l'automatiser vaut le coup ou non."),
 ('blog/fr/facture-electronique-1er-septembre-2026.html', "qui le calcule en deux minutes : quatre questions, résultat à l'écran, et il vous dit si automatiser cette tâche vaut le coup ou non.", "qui calcule son coût annuel en environ deux minutes : quatre questions, résultat à l'écran ; avec six de plus, il vous dit si automatiser cette tâche vaut le coup ou non."),
 ('blog/fr/maintenance-le-cout-cache-de-l-automatisation.html', "il chiffre une tâche en deux minutes en tenant compte de ce qu'elle coûtera à faire vivre, pas seulement à monter.", "il chiffre le coût annuel d'une tâche en environ deux minutes puis, avec six questions de plus, le délai de retour en tenant compte de ce que l'automatisation coûtera à faire vivre, pas seulement à monter."),
 # VAL
 ('blog/val/automatitzar-sense-saber-programar.html', "posa números a una tasca en dos minuts i et diu de quin costat d'eixa línia cau la teua.", "posa xifra al cost anual d'una tasca en uns dos minuts i, amb sis preguntes més, et diu de quin costat d'eixa línia cau la teua."),
 ('blog/val/com-es-automatitzar-un-proces-pas-a-pas.html', "ho fa en dos minuts, sense compromís: quatre preguntes, un resultat en pantalla, i una resposta clara sobre l'interés d'automatitzar eixa tasca concreta.", "calcula el seu cost anual en uns dos minuts, sense compromís: quatre preguntes i un resultat en pantalla; amb sis preguntes més, una resposta clara sobre l'interés d'automatitzar eixa tasca concreta."),
 ('blog/val/com-es-automatitzar-un-proces-pas-a-pas.html', "hauràs estalviat molt més que dos minuts.", "hauràs estalviat molt més que uns minuts."),
 ('blog/val/com-es-automatitzar-un-proces-pas-a-pas.html', ", en dos minuts i sense compromís: quatre preguntes, un resultat en pantalla, i una resposta honesta — sí, no, o encara no.", ", sense compromís: quatre preguntes i uns dos minuts per al cost anual, i sis preguntes més per a una resposta honesta — sí, no, o encara no."),
 ('blog/val/contractar-o-automatitzar.html', "xifra una tasca en dos minuts: quatre preguntes, resultat en pantalla, i et diu si automatitzar-la compensa o no.", "xifra el cost anual d'una tasca en uns dos minuts: quatre preguntes i resultat en pantalla; amb sis més, et diu si automatitzar-la compensa o no."),
 ('blog/val/errors-mes-cars-al-automatitzar.html', "posa números a una tasca en dos minuts — i, en fer-ho, et fa passar l'examen dels cinc errors sense ni tan sols pensar-ho.", "posa números a una tasca en dos minuts."),
 ('blog/val/factura-electronica-dues-normes.html', "ho calcula en dos minuts: quatre preguntes, resultat en pantalla, i et diu si automatitzar eixa tasca compensa o no.", "calcula el seu cost anual en uns dos minuts: quatre preguntes i resultat en pantalla; amb sis més, et diu si automatitzar eixa tasca compensa o no."),
 ('blog/val/la-paperassa-et-lleva-226-hores.html', "t'ho calcula en dos minuts: quatre preguntes, resultat en pantalla, i et diu si automatitzar eixa tasca compensa o no.", "t'ho calcula en uns dos minuts: quatre preguntes i resultat en pantalla; amb sis més, et diu si automatitzar eixa tasca compensa o no."),
 ('blog/val/manteniment-el-cost-amagat-de-l-automatitzacio.html', "xifra una tasca en dos minuts tenint en compte el que costarà mantindre viva, no sols muntar.", "xifra el cost anual d'una tasca en uns dos minuts i, amb sis preguntes més, el termini de retorn tenint en compte el que costarà mantindre viva l'automatització, no sols muntar-la."),
 ('blog/val/que-no-hauries-d-automatitzar-mai.html', "posa números a una tasca en dos minuts i et diu si mereix automatitzar-se", "posa xifra al cost anual d'una tasca en uns dos minuts i, amb sis preguntes més, et diu si mereix automatitzar-se"),
]
VAR = [("'", "'"), ("'", "&#x27;"), ("'", "’"), ("'", "\\u0027")]
dry = '--dry-run' in sys.argv
fichiers = {}
for f, old, new in L:
    s = fichiers.get(f) or open(f, encoding='utf-8').read()
    tot = 0
    for a, b in VAR:
        for dash in ['—', '&mdash;']:
            o = old.replace(a, b).replace('—', dash); n_ = new.replace(a, b).replace('—', dash)
            if (b != "'" or dash != '—') and o == old:
                continue
            c = s.count(o)
            if c:
                s = s.replace(o, n_); tot += c
    print(('OK ' if tot else '!! ') + '%d  %-58s %s' % (tot, f.split('/')[-1][:58], old[:50]))
    fichiers[f] = s
for f, s in fichiers.items():
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        json.loads(m.group(1))
    if not dry:
        open(f, 'w', encoding='utf-8').write(s)
print('fichiers :', len(fichiers), '(dry-run)' if dry else '')
