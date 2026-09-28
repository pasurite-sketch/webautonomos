# -*- coding: utf-8 -*-
"""Web multilingüe sur les pages métier espagnoles (plan SEO FR-EN, 29/09/2026).

VERITE.md §3 : site multilingue sans supplément, jusqu'à 4 langues parmi castellano,
inglés, francés, catalán, valenciano, gallego, euskera ; WebAutonomos rédige chaque
version ; la modification mensuelle vaut pour toutes les langues.

/reformas/ et /dentistas/ en parlent déjà (section et FAQ). On ajoute une question
de FAQ aux cinq autres pages : dans la liste visible et, quand la page en a un,
dans le JSON-LD FAQPage.

Idempotent. Usage : python3 _tools/patch_idiomas_es_20260929.py [--check]
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHECK = '--check' in sys.argv

Q = "¿Puedo tener la web en varios idiomas?"
BASE_R = ("Sí. Tu web puede estar en hasta cuatro idiomas sin coste extra: castellano, inglés, francés, catalán, "
          "valenciano, gallego o euskera. Redactamos nosotros cada versión, y la modificación al mes incluida se "
          "aplica en todos los idiomas.")
PAGINAS = {
    'fontaneros': BASE_R + " Así también te encuentran los residentes extranjeros de tu zona y los clientes que "
                           "buscan en valenciano o en catalán.",
    'electricistas': BASE_R + " Así también te encuentran los residentes extranjeros de tu zona y los clientes que "
                              "buscan en valenciano o en catalán.",
    'carpinteros': BASE_R + " Así también te encuentran los residentes extranjeros de tu zona y los clientes que "
                            "buscan en valenciano o en catalán.",
    'psicologos': BASE_R + " Es útil si atiendes a pacientes en otro idioma, en consulta u online.",
    'fisioterapeutas': BASE_R + " Es útil si atiendes a pacientes extranjeros, residentes o de paso.",
}


def patch(rel, r):
    s = open(rel, encoding='utf-8').read()
    if Q in s:
        return s
    fl = s.find('class="faq-list"')
    fin = s.find('\n\n  </div>\n</section>', fl)
    if fl < 0 or fin < 0:
        sys.exit('ABANDON : %s : fin de la liste de FAQ introuvable. Rien écrit.' % rel)
    item = ('\n\n    <details class="faq-item">\n      <summary>%s</summary>\n      <p>%s</p>\n    </details>'
            % (html.escape(Q, quote=False), html.escape(r, quote=False)))
    s = s[:fin] + item + s[fin:]
    blocs = [m for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
             if '"FAQPage"' in m.group(1)]
    if len(blocs) > 1:
        sys.exit('ABANDON : %s : plusieurs FAQPage. Rien écrit.' % rel)
    if blocs:
        b = blocs[0]
        texte = b.group(1)
        k = texte.rfind('\n    }\n  ]\n}')
        if k < 0:
            sys.exit('ABANDON : %s : fin du FAQPage introuvable. Rien écrit.' % rel)
        q = json.dumps({"@type": "Question", "name": Q, "acceptedAnswer": {"@type": "Answer", "text": r}},
                       ensure_ascii=False, indent=2)
        q = '\n'.join('    ' + l for l in q.split('\n'))
        neuf = texte[:k] + '\n    },\n' + q + texte[k + len('\n    }'):]
        d = json.loads(neuf)
        if d['mainEntity'][-1]['name'] != Q:
            sys.exit('ABANDON : %s : insertion JSON-LD incorrecte. Rien écrit.' % rel)
        s = s[:b.start(1)] + neuf + s[b.end(1):]
    return s


def main():
    for p, r in PAGINAS.items():
        rel = '%s/index.html' % p
        avant = open(rel, encoding='utf-8').read()
        s = patch(rel, r)
        if s == avant:
            print('  = %s déjà à jour' % rel)
        elif CHECK:
            print('  ✓ %s à modifier — non écrit' % rel)
        else:
            open(rel, 'w', encoding='utf-8').write(s)
            print('  ✓ %s : question « varios idiomas » ajoutée' % rel)


if __name__ == '__main__':
    main()
