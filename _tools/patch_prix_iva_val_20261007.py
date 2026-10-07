# -*- coding: utf-8 -*-
"""Accueil valencien (bloc val de l'objet translations d'index.html), 07/10/2026 : « + IVA » après les prix et
fin de « El preu que veus és el preu que pagues », comme pour l'espagnol le même jour
(patch_prix_iva_accueil_20261007.py). Demande d'Angelino du 07/10/2026.

- Carte tarifaire : « 15€ /mes + IVA » et « 349€ + IVA », avec « Pagament únic · Mateixos serveis » dessous (au
  lieu de « Una sola quota · … »), espace insécable entre « + » et « IVA » sur la carte et le héros.
- « + IVA » aussi dans le sous-titre du héros, la comparaison, l'étape 3, les services additionnels et trois
  réponses de la FAQ ; « Al preu que veus només s'hi suma l'IVA » dans la réponse sur les coûts cachés.
- La tuile « 15€/mes » du formulaire de contact lit déjà t.pricing.period depuis le correctif espagnol.

Le repli <noscript> et la FAQPage du <head> sont espagnols : rien à régénérer. Les blocs es, en et fr ne changent
pas. Chaque remplacement vérifie qu'il trouve sa chaîne une seule fois dans le bloc val. Non rejouable : si une
ancre manque (correctif déjà appliqué), le script s'arrête sans rien écrire. À lancer depuis la racine du dépôt :
  python3 _tools/patch_prix_iva_val_20261007.py [--sortie FICHIER]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
SORTIE = sys.argv[sys.argv.index('--sortie') + 1] if '--sortie' in sys.argv else SRC

# Espace insécable sous la forme d'échappement JavaScript  , écrit avec chr()
INSEC = chr(92) + 'u00a0'
AP = "'"

REMPLACEMENTS = [
    ('subtitle:"Només 15€/mes · Sense alta · Sense permanència"', 'subtitle:"Només 15€/mes +' + INSEC + 'IVA · Sense alta · Sense permanència"'),
    ('"<strong>Preu fix i clar:</strong> 15€/mes, tot inclòs.', '"<strong>Preu fix i clar:</strong> 15€/mes + IVA, tot inclòs.'),
    ('step3Desc:"Acceptes, pagues 15€/mes i la teua web', 'step3Desc:"Acceptes, pagues 15€/mes + IVA i la teua web'),
    # Carte tarifaire
    ('price:"15",period:"/mes",', 'price:"15",period:"/mes +' + INSEC + 'IVA",'),
    ('oneShotPeriod:"pagament únic",oneShotTerms:"Una sola quota · Mateixos serveis"',
     'oneShotPeriod:"+' + INSEC + 'IVA",oneShotTerms:"Pagament únic · Mateixos serveis"'),
    # Services additionnels
    ('seo:{title:"SEO Local",price:"15€/mes",', 'seo:{title:"SEO Local",price:"15€/mes + IVA",'),
    ('gmb:{title:"Google My Business",price:"29€/mes",', 'gmb:{title:"Google My Business",price:"29€/mes + IVA",'),
    ('"Creació de fitxa: 49€ (pagament únic)"', '"Creació de fitxa: 49€ + IVA (pagament únic)"'),
    # FAQ
    ('ni costos d' + AP + 'activació. El preu que veus és el preu que pagues, sense sorpreses."',
     'ni costos d' + AP + 'activació. Al preu que veus només s' + AP + 'hi suma l' + AP + 'IVA, sense sorpreses."'),
    ('El SEO Local (+15€/mes) és el que fa', 'El SEO Local (15€/mes + IVA) és el que fa'),
    ('Amb Google My Business (+29€/mes) ens encarreguem', 'Amb Google My Business (29€/mes + IVA) ens encarreguem'),
    ('la creem i verifiquem per 49€ (pagament únic).', 'la creem i verifiquem per 49€ + IVA (pagament únic).'),
]


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
s = s[:ival] + bloc + s[fval + 1:]
open(SORTIE, 'w', encoding='utf-8').write(s)
print('ok : %d remplacements dans translations.val (%s)' % (len(REMPLACEMENTS), SORTIE))
