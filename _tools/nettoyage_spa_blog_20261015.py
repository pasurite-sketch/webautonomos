# -*- coding: utf-8 -*-
"""Vide le corps (content) et la FAQ (faq) des anciens articles du SPA dans index.html.

Contexte (15/10/2026) : l'objet `translations` de index.html contient encore, pour
chaque langue, les 57 anciens articles du blog (corps et FAQ, environ 1,46 Mo).
Ce texte n'est plus affiché : la navigation vers /blog est interceptée et renvoie
vers les pages statiques blog/{lang}/..., qui sont la seule source à jour. Il reste
lisible dans le code de l'accueil, avec des affirmations sans source (« Una agencia
tradicional te cobrará entre 1.500 y 5.000 euros ») et des formules interdites
(« desde 15 euros al mes »).

Le script :
  - remplace `content:[...]` et `faq:[...]` de chaque article par `[]` ;
  - garde toutes les autres clés (id, slug, title, excerpt, category, date...) dont
    se servent encore le routeur, le changement de langue et generate_sitemap.py ;
  - vérifie avec node que l'objet reste valide et que seules ces deux clés changent ;
  - remplace les formules « desde / des de / from 15€ » restantes par « por solo /
    per només / for just », comme sur le reste du site ;
  - est idempotent (un 2e passage ne change rien).

Usage (depuis la racine du dépôt) :
    python3 _tools/nettoyage_spa_blog_20261015.py           # écrit index.html
    python3 _tools/nettoyage_spa_blog_20261015.py --dry-run # vérifie sans écrire
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')
DEBUT = 'const translations='
# Formules interdites devant nos prix (règle du site : jamais « desde / des de / from »),
# remplacées comme sur le reste du site le 14/10/2026.
PRIX = [('Desde 15€/mes', 'Por solo 15 €/mes'), ('desde 15€/mes', 'por solo 15 €/mes'),
        ('Des de 15€/mes', 'Per només 15 €/mes'), ('des de 15€/mes', 'per només 15 €/mes'),
        ('from 15€/month', 'for just €15/month')]


def fin_bloc(s, i):
    """Position du caractère fermant le { ou [ ouvert en s[i], hors chaînes JS."""
    ouvrant = s[i]
    fermant = {'{': '}', '[': ']'}[ouvrant]
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
                if c != fermant:
                    sys.exit('ABANDON : accolades déséquilibrées à %d' % k)
                return k
        k += 1
    sys.exit('ABANDON : fin de bloc introuvable')


def elements(s, debut, fin):
    """Objets {..} de premier niveau du tableau s[debut:fin+1]."""
    k, out = debut + 1, []
    while k < fin:
        c = s[k]
        if c == '{':
            e = fin_bloc(s, k)
            out.append((k, e))
            k = e + 1
        else:
            k += 1
    return out


def cles_tableau(s, o_deb, o_fin, noms):
    """Spans [deb, fin] des valeurs tableau des clés `noms` au premier niveau de l'objet."""
    spans, k, q, esc, prof = [], o_deb + 1, None, False, 0
    while k < o_fin:
        c = s[k]
        if q:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == q:
                q = None
            k += 1
            continue
        if c in '"\'`':
            q = c
        elif c in '{[':
            prof += 1
        elif c in '}]':
            prof -= 1
        elif prof == 0 and s[k - 1] in '{,':
            for n in noms:
                for cle in (n + ':', '"%s":' % n):
                    if s.startswith(cle, k):
                        v = k + len(cle)
                        while s[v] in ' \n\t':
                            v += 1
                        if s[v] != '[':
                            sys.exit('ABANDON : %s n\'est pas un tableau à %d' % (n, v))
                        spans.append((v, fin_bloc(s, v)))
        k += 1
    return spans


def lire_objet(js):
    """Évalue `const translations={...}` avec node et renvoie l'objet Python."""
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 't.js')
        with open(src, 'w', encoding='utf-8') as fh:
            fh.write(js + ';\nprocess.stdout.write(JSON.stringify(translations));')
        r = subprocess.run(['node', src], capture_output=True, text=True)
        if r.returncode:
            sys.exit('ABANDON : objet translations invalide : ' + r.stderr[-400:])
        return json.loads(r.stdout)


def main():
    dry = '--dry-run' in sys.argv
    s = open(INDEX, encoding='utf-8').read()
    i = s.find(DEBUT)
    if i < 0 or s.count(DEBUT) != 1:
        sys.exit('ABANDON : `%s` absent ou en double' % DEBUT)
    o = i + len(DEBUT)
    o_fin = fin_bloc(s, o)
    avant = s[i:o_fin + 1]

    # tableaux articles:[...] (un par langue)
    arts, k = [], o
    while True:
        k = s.find('articles:[', k, o_fin)
        if k < 0:
            break
        deb = k + len('articles:')
        arts.append((deb, fin_bloc(s, deb)))
        k = deb
    if len(arts) != 4:
        sys.exit('ABANDON : %d tableaux articles trouvés, 4 attendus' % len(arts))

    spans = []
    for a_deb, a_fin in arts:
        for e_deb, e_fin in elements(s, a_deb, a_fin):
            spans += cles_tableau(s, e_deb, e_fin, ('content', 'faq'))
    a_vider = [(d, f) for d, f in spans if s[d:f + 1] != '[]']

    nouveau = s
    for d, f in sorted(a_vider, reverse=True):
        nouveau = nouveau[:d] + '[]' + nouveau[f + 1:]

    # 2e étape : formules de prix interdites (« desde / des de / from » devant nos prix)
    i2 = nouveau.find(DEBUT)
    f2 = fin_bloc(nouveau, i2 + len(DEBUT))
    bloc = nouveau[i2:f2 + 1]
    n_prix = 0
    for a, b in PRIX:
        n_prix += bloc.count(a)
        bloc = bloc.replace(a, b)
    nouveau = nouveau[:i2] + bloc + nouveau[f2 + 1:]

    if nouveau == s:
        print('déjà appliqué : rien à changer')
        return

    # contrôles : objet valide, seules content/faq des articles et les formules de prix changent
    apres = bloc
    t1, t2 = lire_objet(avant), lire_objet(apres)
    n_art = sum(len(t2[L]['blog']['articles']) for L in t2)

    def norm(x):
        if isinstance(x, str):
            for a, b in PRIX:
                x = x.replace(a, b)
            return x
        if isinstance(x, list):
            return [norm(v) for v in x]
        if isinstance(x, dict):
            return {k: norm(v) for k, v in x.items()}
        return x

    t1 = norm(t1)
    if list(t1) != list(t2):
        sys.exit('ABANDON : langues modifiées')
    for L in t1:
        b1, b2 = t1[L], t2[L]
        a1, a2 = b1['blog'].pop('articles'), b2['blog'].pop('articles')
        if b1 != b2:
            sys.exit('ABANDON : autre chose que les articles a changé en %s' % L)
        if len(a1) != len(a2):
            sys.exit('ABANDON : nombre d\'articles modifié en %s' % L)
        for x, y in zip(a1, a2):
            if y.get('content', []) != [] or y.get('faq', []) != []:
                sys.exit('ABANDON : article %s non vidé' % y.get('slug'))
            x.pop('content', None), x.pop('faq', None), y.pop('content', None), y.pop('faq', None)
            if x != y:
                sys.exit('ABANDON : métadonnées modifiées pour %s' % x.get('slug'))
    if s[:i] != nouveau[:i2] or s[o_fin + 1:] != nouveau[i2 + len(apres):]:
        sys.exit('ABANDON : le reste de index.html aurait changé')
    reste = [a for a, _ in PRIX if a in nouveau]
    if reste:
        sys.exit('ABANDON : formules restantes : %s' % reste)

    print('%d tableaux vidés (content et faq ; %d articles sur 4 langues), %d formules de prix corrigées ; %d → %d octets'
          % (len(a_vider), n_art, n_prix, len(s.encode('utf-8')), len(nouveau.encode('utf-8'))))
    if dry:
        print('--dry-run : rien écrit')
        return
    open(INDEX, 'w', encoding='utf-8').write(nouveau)
    print('index.html écrit')


if __name__ == '__main__':
    main()
