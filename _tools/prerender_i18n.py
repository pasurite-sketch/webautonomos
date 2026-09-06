# -*- coding: utf-8 -*-
"""Injecte le texte espagnol dans les balises data-t des pages i18n.

/visibilidad-ia/ et /diagnostico-automatizacion/ remplissent leurs balises par
JavaScript depuis un objet de traductions. Servies telles quelles, elles
montrent un h1 vide a un crawler sans JS : 229 et 311 caracteres de texte
visible pour 84 et 89 Ko de page (audit du 05/09/2026).

Ce script ecrit la version espagnole dans le HTML. Le script de la page
continue de la remplacer quand ?lang= demande une autre langue : le repli ne
gene pas l'i18n, il evite seulement la page vide.

    python3 _tools/prerender_i18n.py --check     # signale les ecarts, n'ecrit pas
    python3 _tools/prerender_i18n.py             # ecrit
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGES = [('visibilidad-ia/index.html', 'T'),
         ('diagnostico-automatizacion/index.html', 'T')]

EXTRACT = """
const fs=require('fs');
let src=fs.readFileSync(process.argv[2],'utf8');
let i=src.search(new RegExp('(?:var|const|let)\\\\s+%s\\\\s*=\\\\s*\\\\{'));
if(i<0){console.error('objet introuvable');process.exit(2);}
i=src.indexOf('{',i);
let d=0,j=i,q=null;
for(;j<src.length;j++){
  const c=src[j], pv=src[j-1];
  if(q){ if(c===q&&pv!=='\\\\')q=null; continue; }
  if(c==='"'||c==="'"||c==='`'){q=c;continue;}
  if(c==='/'&&src[j+1]==='/'){j=src.indexOf('\\n',j);continue;}
  if(c==='/'&&src[j+1]==='*'){j=src.indexOf('*/',j)+1;continue;}
  if(c==='{')d++; else if(c==='}'&&--d===0){j++;break;}
}
let obj; eval('obj='+src.slice(i,j));
fs.writeFileSync(process.argv[3], JSON.stringify(obj.es||obj.ES||{}));
"""


def textes(path, nom):
    """{cle: texte espagnol} extrait par Node, seul a savoir lire du JS."""
    with tempfile.TemporaryDirectory() as tmp:
        js = os.path.join(tmp, 'x.js')
        out = os.path.join(tmp, 'o.json')
        with open(js, 'w', encoding='utf-8') as fh:
            fh.write(EXTRACT % nom)
        r = subprocess.run(['node', js, path, out], capture_output=True, text=True)
        if r.returncode:
            sys.exit('%s : %s' % (nom, r.stderr.strip()))
        with open(out, encoding='utf-8') as fh:
            return json.load(fh)


def injecte(html, tr, stats):
    """Remplit <tag data-t="cle"></tag> ; laisse intact ce qui a deja du texte."""
    def sub(m):
        ouvre, cle, ferme = m.group(1), m.group(3), m.group(4)
        val = tr.get(cle)
        if val is None:
            stats['manquantes'].add(cle)
            return m.group(0)
        stats['remplies'] += 1
        return ouvre + val + ferme
    return re.sub(r'(<(\w+)[^>]*\bdata-t="([\w.]+)"[^>]*>)\s*(</\2>)', sub, html)


def main():
    check = '--check' in sys.argv
    total = 0
    for rel, nom in PAGES:
        path = os.path.join(ROOT, rel)
        tr = textes(path, nom)
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        vides = len(re.findall(r'<(\w+)[^>]*\bdata-t="[\w.]+"[^>]*>\s*</\1>', html))
        stats = {'remplies': 0, 'manquantes': set()}
        neuf = injecte(html, tr, stats)
        print('%-42s cles es %3d | balises vides %3d | remplies %3d'
              % (rel, len(tr), vides, stats['remplies']))
        if stats['manquantes']:
            print('   cles absentes de l\'objet : %s'
                  % ', '.join(sorted(stats['manquantes'])[:8]))
        if not check and neuf != html:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(neuf)
            total += stats['remplies']
    print('(--check : rien ecrit)' if check else 'Total injecte : %d' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
