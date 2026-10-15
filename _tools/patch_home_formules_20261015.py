# -*- coding: utf-8 -*-
"""Corrige des formulations de l'objet `translations` de index.html (accueil ES, et ses
versions ?lang=val, en, fr) — 15/10/2026.

  - « desde / des de / from / à partir de » devant nos prix (règle du site : jamais) :
    Google My Business est à 29 €/mois, pas « à partir de » ; démo à 15 €/mois ;
  - délai de réponse : VERITE dit « respuesta en el día » (réponse dans la journée),
    pas « en menos de 24 horas ».

Chaque ancien texte doit apparaître exactement le nombre de fois prévu, uniquement dans
l'objet `translations` ; sinon le script s'arrête sans rien écrire. Idempotent.

Usage (depuis la racine du dépôt) :
    python3 _tools/patch_home_formules_20261015.py [--dry-run]
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')
DEBUT = 'const translations='

# (ancien, nouveau, nombre d'occurrences attendu)
REMPLACEMENTS = [
    ('Google My Business desde 29€/mes', 'Google My Business por 29€/mes', 1),
    ('Google My Business des de 29€/mes', 'Google My Business per 29€/mes', 1),
    ('Google My Business from €29/month', 'Google My Business for €29/month', 1),
    ('Google My Business à partir de 29 €/mois', 'Google My Business à 29 €/mois', 1),
    ('get yours from €15/month', 'get yours for just €15/month', 2),
    ('le vôtre à partir de 15 €/mois', 'le vôtre pour seulement 15 €/mois', 2),
    ('Respuesta en menos de 24 horas.', 'Respuesta en el día.', 1),
    ('Resposta en menys de 24 hores.', 'Resposta en el mateix dia.', 1),
    ('Response in less than 24 hours.', 'Same-day reply.', 1),
    ('Réponse en moins de 24 h.', 'Réponse dans la journée.', 1),
]


def fin_bloc(s, i):
    prof, q, esc, k = 0, None, False, i
    while k < len(s):
        c = s[k]
        if q:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == q:
                q = None
        elif c in '"\'`':
            q = c
        elif c in '{[':
            prof += 1
        elif c in '}]':
            prof -= 1
            if prof == 0:
                return k
        k += 1
    sys.exit('ABANDON : fin de l\'objet translations introuvable')


def valide(js):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 't.js')
        open(src, 'w', encoding='utf-8').write(js + ';\nprocess.stdout.write(String(Object.keys(translations).length));')
        r = subprocess.run(['node', src], capture_output=True, text=True)
        if r.returncode or r.stdout != '4':
            sys.exit('ABANDON : objet translations invalide après remplacement : ' + r.stderr[-300:])


def main():
    dry = '--dry-run' in sys.argv
    s = open(INDEX, encoding='utf-8').read()
    if s.count(DEBUT) != 1:
        sys.exit('ABANDON : `%s` absent ou en double' % DEBUT)
    i = s.find(DEBUT)
    f = fin_bloc(s, i + len(DEBUT))
    bloc = s[i:f + 1]
    if all(bloc.count(a) == 0 and bloc.count(b) >= n for a, b, n in REMPLACEMENTS):
        print('déjà appliqué : rien à changer')
        return
    for a, b, n in REMPLACEMENTS:
        if bloc.count(a) != n:
            sys.exit('ABANDON : « %s » trouvé %d fois dans translations, %d attendu(s)' % (a, bloc.count(a), n))
        if s.count(a) != n:
            sys.exit('ABANDON : « %s » présent aussi hors de translations' % a)
        bloc = bloc.replace(a, b)
    valide(bloc)
    nouveau = s[:i] + bloc + s[f + 1:]
    print('%d formulations corrigées' % sum(n for _, _, n in REMPLACEMENTS))
    if dry:
        print('--dry-run : rien écrit')
        return
    open(INDEX, 'w', encoding='utf-8').write(nouveau)
    print('index.html écrit')


if __name__ == '__main__':
    main()
