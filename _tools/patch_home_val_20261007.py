# -*- coding: utf-8 -*-
"""Accueil valencien (bloc val de l'objet translations d'index.html), 07/10/2026 : aligné sur l'accueil espagnol.
Demande d'Angelino du 07/10/2026 (« aligne-la sur la version espagnole »).

Le 06/10, patch_home_es_20261006.py avait mis l'accueil espagnol en conformité avec VERITE.md ; le valencien était
resté à la version Lovable. Ce script y reporte le même contenu, traduit :
- titre du héros (« Disseny de pàgines web per a autònoms que convertixen visites en clients »), premier avantage
  et étape 1 (textes écrits à partir de la fiche Google, pas une plantilla) ;
- carte tarifaire : « Enllaç al teu sistema de reserves » au lieu de « Calendari de cites online » (VERITE §2) ;
- services additionnels : contenu de VERITE §5 seulement ;
- comparaison : ni prix ni délais d'agences sans source ;
- FAQ : mêmes corrections que l'espagnol (ni « t'ho garantim », ni « en 24h », ni « recuperem la teua web en
  minuts », ni « per sempre »), question sur la fiche Google renommée, et les sept questions absentes du valencien
  (idiomes, puis les six ajoutées le 06/10), dans l'ordre de l'espagnol : 17 questions.

Les blocs es, en et fr ne changent pas ; le repli <noscript> et la FAQPage du <head> sont espagnols. Chaque
remplacement vérifie qu'il trouve sa chaîne une seule fois dans le bloc val. Non rejouable : si une ancre manque
(correctif déjà appliqué), le script s'arrête sans rien écrire. À lancer depuis la racine du dépôt :
  python3 _tools/patch_home_val_20261007.py [--sortie FICHIER]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
SORTIE = sys.argv[sys.argv.index('--sortie') + 1] if '--sortie' in sys.argv else SRC


def js(t):
    return json.dumps(t, ensure_ascii=False)


REMPLACEMENTS = [
    # Héros, avantages, étape 1
    ('title:' + js("Una web que convertix") + ',titleHighlight:' + js("visites en clients"),
     'title:' + js("Disseny de pàgines web per a autònoms") + ',titleHighlight:' + js("que convertixen visites en clients")),
    ('benefit1:' + js("Creació gratuïta") + ',benefit1Desc:' + js("Dissenyem la teua web abans que pagues res"),
     'benefit1:' + js("Textos i fotos inclosos") + ',benefit1Desc:' + js("No és una plantilla: escrivim i muntem la teua web per tu")),
    ('step1Desc:' + js("Dissenyem una web professional personalitzada per al teu negoci, gratis i sense compromís."),
     'step1Desc:' + js("Escrivim els textos amb les dades reals de la teua fitxa de Google, posem les fotos i el botó de WhatsApp. "
                       "No és una plantilla: tu no has de fer res.")),
    # Comparaison : ni prix ni délais d'agences sans source
    (js("<strong>Preus inflats:</strong> Et cobren 500€, 1.000€ o més per una web bàsica que no necessites."),
     js("<strong>Cada projecte, la seua factura:</strong> cada pàgina es pressuposta a banda, i el manteniment o els "
        "canvis poden cobrar-se després.")),
    (js("<strong>Setmanes d'espera:</strong> Et diuen 2 setmanes i acaben sent 2 mesos."),
     js("<strong>Pagar abans de veure:</strong> demanes pressupost, avances una part i esperes setmanes per a veure el disseny.")),
    (js("<strong>Lligat amb contracte:</strong> Permanències de 12 mesos, penalitzacions si cancel·les."),
     js("<strong>Contractes amb permanència:</strong> alguns serveis et lliguen durant mesos i penalitzen si cancel·les.")),
    # Carte tarifaire : pas d'agenda en ligne (VERITE §2), seulement un lien vers l'outil du client
    ('item9:' + js("Calendari de cites online"), 'item9:' + js("Enllaç al teu sistema de reserves")),
    # Services additionnels : contenu de VERITE §5 seulement
    ('features:' + js(["4 articles de blog al mes", "Optimització de paraules clau locals", "Meta títols i descripcions optimitzats",
                       "Estructura d'URLs amigable", "Velocitat de càrrega optimitzada", "Schema markup per a negocis locals",
                       "Informe mensual de posicionament"]).replace('", "', '","'),
     'features:' + js(["4 articles de blog al mes", "Paraules clau de la teua zona", "Informe mensual de posicionament"]).replace('", "', '","')),
    (',' + js("Gestió i resposta a ressenyes") + ',' + js("Informe mensual de rendiment") + ']',
     ',' + js("Gestió i resposta a ressenyes") + ']'),
    # FAQ
    ("Cap, t'ho garantim. Els 15€/mes inclouen absolutament tot el que necessites: disseny web professional i personalitzat, "
     "hosting d'alta velocitat,",
     "Cap. Els 15€/mes inclouen tot el necessari per a tindre la teua web en marxa: disseny web professional i personalitzat, "
     "hosting,"),
    ("i els fem en 24h. Quan aproves", "i els fem abans de publicar-la, sense límit d'ajustos. Quan aproves"),
    ("Tu només necessites dir-nos quins serveis oferixes, en quina zona treballes, i compartir-nos algunes fotos si les tens "
     "(si no, usem imatges professionals).",
     "Només has de dir-nos quins serveis oferixes, en quina zona treballes, i compartir-nos algunes fotos si les tens "
     "(si no, usem les de la teua fitxa de Google). No cal saber programació ni disseny gràfic, ni dedicar-hi temps."),
    ("Si en algun moment vols fer un canvi, ens escrius i ho fem nosaltres.",
     "Per a qualsevol canvi posterior, ens escrius i se n'encarrega el nostre equip: tens una modificació al mes inclosa."),
    ("còpies de seguretat automàtiques diàries (si alguna cosa falla, recuperem la teua web en minuts), monitorització 24/7 "
     "per a detectar caigudes i actuar immediatament, optimització de velocitat perquè la teua web carregue ràpid, renovació "
     "del certificat SSL, i suport tècnic per email i WhatsApp amb resposta en menys de 24h.",
     "còpies de seguretat automàtiques diàries (si alguna cosa falla, podem restaurar-la), monitorització 24/7 per a detectar "
     "caigudes, renovació del certificat SSL, i suport tècnic per email i WhatsApp amb resposta el mateix dia."),
    ("tens dret a una modificació al mes, per sempre: actualitzar textos i descripcions de serveis, canviar fotos i imatges, "
     "modificar horaris i dades de contacte, afegir nous serveis o eliminar els que ja no oferixes, ajustos de disseny "
     "(colors, tipografies, disposició), afegir noves seccions o pàgines, integrar el teu calendari de reserves, actualitzar "
     "preus... Tot el que necessites per a mantindre la teua web sempre actualitzada i rellevant. Ens escrius per WhatsApp o "
     "email, i en 24h tens els canvis fets.",
     "tens dret a una modificació al mes, sense límit de temps: actualitzar textos i descripcions de serveis, canviar fotos i "
     "imatges, modificar horaris i dades de contacte, afegir nous serveis o eliminar els que ja no oferixes, posar l'enllaç al "
     "teu sistema de reserves, actualitzar preus... Els canvis més grans, com un redisseny o una secció nova important, es fan "
     "amb pressupost tancat, sense sorpreses. Ens escrius per WhatsApp o email i ens n'ocupem."),
    ("El servei inclou: 4 articles de blog optimitzats al mes sobre temes del teu sector, investigació i optimització de "
     "paraules clau locals, meta títols i descripcions optimitzats per a cada pàgina, URLs amigables per a cercadors, "
     "optimització de velocitat de càrrega (factor clau per a Google), i un informe mensual on veus la teua evolució en el "
     "rànquing. És la diferència entre que et troben els clients de la teua zona o que troben a la teua competència.",
     "El servei inclou 4 articles de blog al mes sobre temes del teu sector, el treball de les paraules clau de la teua zona i "
     "un informe mensual on veus la teua evolució. Pots contractar-lo encara que la teua web no estiga feta amb nosaltres."),
    ('{q:' + js("Què inclou el servei de Google My Business?") + ',a:' + js(
        "Amb Google My Business (29€/mes + IVA) ens encarreguem de gestionar completament el teu perfil de Google perquè "
        "aparegues en Google Maps i en les cerques locals amb la millor imatge possible. Inclou: optimització completa de la "
        "teua fitxa (categories, descripció, horaris, atributs, fotos professionals), publicació de 4 posts al mes amb novetats "
        "i ofertes per a mantindre el teu perfil actiu, gestió i resposta professional a totes les ressenyes (positives i "
        "negatives), monitorització de la teua posició en el Local Pack, i un informe mensual detallat amb mètriques de "
        "rendiment (visualitzacions, clics, trucades, sol·licituds de ruta). Si encara no tens fitxa de Google, la creem i "
        "verifiquem per 49€ + IVA (pagament únic). És fonamental per a un negoci local: és el que apareix en Google Maps i en "
        "les cerques de la teua zona.") + '}',
     '{q:' + js("Què inclou la gestió de la teua fitxa de Google?") + ',a:' + js(
        "Amb la gestió de la teua fitxa de Google (29€/mes + IVA) ens encarreguem del teu perfil perquè aparegues en Google "
        "Maps i en les cerques locals amb la informació correcta. Inclou l'optimització de la teua fitxa (categories, "
        "descripció, horaris, atributs i fotos), la publicació de 4 posts al mes amb les teues novetats i la resposta a les "
        "ressenyes, positives i negatives. Si encara no tens fitxa de Google, la creem i verifiquem per 49€ + IVA (pagament "
        "únic). També pots contractar-la sense la web.") + '}'),
]

# Questions de l'espagnol absentes du valencien, insérées à la même place que dans l'espagnol
IDIOMES = [
    ("Puc tindre la meua pàgina web en diversos idiomes?",
     "Sí. En WebAutonomos, la teua pàgina web pot estar en fins a quatre idiomes sense cost extra: castellà, anglés, francés i "
     "qualsevol de les llengües cooficials d'Espanya (català, valencià, gallec o basc). Continua costant 15 €/mes + IVA, o "
     "349 € + IVA en pagament únic. Redactem nosaltres cada versió perquè els teus clients et troben en Google en el seu "
     "idioma. La modificació mensual inclosa s'aplica en tots els idiomes."),
]
ANCRE_IDIOMES = '{q:' + js("El domini és meu?")

NOUVELLES = [
    ("Què ha de tindre la pàgina web d'un autònom?",
     "Per a crear una pàgina que funcione, l'essencial és que els teus clients entenguen en poc temps què fas, on treballes i "
     "com contactar amb tu: els teus serveis explicats de forma clara, la teua zona de treball, fotos reals dels teus "
     "treballs, les teues opinions, un formulari de contacte, el botó de WhatsApp i els textos legals (avís legal, "
     "privacitat i cookies). Tot això ve en la teua pàgina de WebAutonomos, adaptat al teu sector i pensat per a veure's bé "
     "en el mòbil."),
    ("Necessite una pàgina web si ja estic en xarxes socials?",
     "Les xarxes socials com Instagram o Facebook servixen per a compartir contingut del teu dia a dia i mantindre el contacte "
     "amb els teus clients i la teua comunitat, però no les controles tu: l'abast depén de cada plataforma i les teues "
     "publicacions es perden amb el temps. El teu lloc web és teu, pot aparéixer en les cerques de Google i reunix en un sol "
     "lloc els teus serveis, el teu telèfon i la manera de contactar amb tu a través del formulari o de WhatsApp. L'ideal és "
     "usar les dues coses: incloem enllaços als teus perfils en xarxes socials sense cost extra."),
    ("És millor una plantilla, WordPress o una pàgina feta per vosaltres?",
     "Depén del temps que pugues dedicar-hi. Amb un creador de webs amb plantilles o amb WordPress pots crear la teua pàgina tu "
     "mateix, però hauràs de triar l'eina, preparar el contingut, configurar la plataforma i ocupar-te del manteniment. Una "
     "agència fa un projecte a mida, que es cobra per projecte. Amb WebAutonomos la preparem nosaltres a partir de la "
     "informació de la teua fitxa de Google, per 15 €/mes + IVA o 349 € + IVA en pagament únic, i els teus clients et troben "
     "sense que perdes temps en la part tècnica. Per a comparar opcions, tenim una comparativa dels 6 creadors de webs per a "
     "autònoms."),
    ("Puc vendre els meus productes en línia?",
     "Sí. Podem crear una botiga en línia amb catàleg de productes i pagament amb targeta, amb un pressupost a banda: el comerç "
     "electrònic no està inclòs en els 15 €/mes ni en els 349 €. Per a mostrar els teus productes i que un client te'ls demane "
     "amb un missatge, n'hi ha prou amb la teua pàgina i el seu formulari."),
    ("Quins textos legals necessita la meua pàgina?",
     "A Espanya, un lloc web professional ha d'identificar el seu titular (avís legal), explicar què fa amb les dades personals "
     "(política de privacitat) i informar sobre les cookies. Redactem eixos tres textos i els incloem en la teua pàgina. Si la "
     "teua activitat té normes pròpies, com les professions sanitàries, revisa també els seus requisits, com el número de "
     "col·legiat."),
    ("Com m'ajuda la meua pàgina a aconseguir més clients?",
     "Una pàgina no fa miracles, però treballa per tu a qualsevol hora: quan algú necessita el teu servei en la teua zona, pot "
     "trobar-te, veure el teu treball i les teues opinions, i escriure't a través de WhatsApp o del formulari. Per això cuidem "
     "el bàsic del posicionament: títols i textos amb el teu servei i la teua zona, i la mateixa informació que en la teua "
     "fitxa de Google. Per a anar més enllà, el SEO Local treballa la teua visibilitat cada mes."),
]
ANCRE_NOUVELLES = '{q:' + js("Què és el SEO Local i per què el necessite?")


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


def questions(liste):
    return ''.join('{q:%s,a:%s},' % (js(q), js(a)) for q, a in liste)


s = open(SRC, encoding='utf-8').read()
i0 = s.index('const translations=') + len('const translations=')
fes = fin_bloc(s, s.index('es:{', i0) + 3)
if not s.startswith(',val:{', fes + 1):
    sys.exit('le bloc val ne suit pas le bloc es')
ival = fes + 6  # accolade ouvrante du bloc val
fval = fin_bloc(s, ival)
bloc = s[ival:fval + 1]
for ancien, nouveau in REMPLACEMENTS:
    n = bloc.count(ancien)
    if n != 1:
        sys.exit('ancre trouvée %d fois dans le bloc val : %s' % (n, ancien[:90]))
    bloc = bloc.replace(ancien, nouveau)
for ancre, liste in ((ANCRE_IDIOMES, IDIOMES), (ANCRE_NOUVELLES, NOUVELLES)):
    if bloc.count(ancre) != 1:
        sys.exit('ancre d\'insertion introuvable ou ambiguë : %s' % ancre)
    bloc = bloc.replace(ancre, questions(liste) + ancre)
s = s[:ival] + bloc + s[fval + 1:]
open(SORTIE, 'w', encoding='utf-8').write(s)
print('ok : %d remplacements et %d questions ajoutées dans translations.val (%s)' % (
    len(REMPLACEMENTS), len(IDIOMES) + len(NOUVELLES), SORTIE))
