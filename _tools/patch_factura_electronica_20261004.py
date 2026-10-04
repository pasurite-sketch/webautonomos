# -*- coding: utf-8 -*-
"""Article « facturación electrónica obligatoria » (ES, VAL, EN ; pages statiques et données du blog de
index.html) : affirmations fausses ou interdites corrigées (demande d'Angelino du 04/10/2026). Idempotent.

Corrigé : obligation Crea y Crece limitée aux factures entre entreprises et professionnels ; calendrier
(« ya obligadas desde julio de 2025 », « 12 meses », « a partir de 2027 ») remplacé par les étapes, sans date,
avec renvoi à l'Agence fiscale ; Verifactu présenté comme un « formato », un « sistema homologado » ou une
« solución gratis de la AEAT » ; signature électronique avancée obligatoire seulement via FACe ; sanctions
« entre 150 y 6.000 euros » sans source ; éditeurs de logiciels cités ; « la mayoría de autónomos » (VERITE §8) ;
« el error más común » ; « por qué es obligatoria » (titre) devient « será ». Seules les pages statiques reçoivent
le lien vers l'article Verifactu.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {'es': 'blog/es/facturacion-electronica-autonomos-obligatoria.html',
     'val': 'blog/val/facturacio-electronica-obligatoria.html',
     'en': 'blog/en/mandatory-e-invoicing-for-freelancers.html'}
DATA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patch_factura_electronica_20261004.json'),
                      encoding='utf-8'))


def esc(t):
    return html.escape(t, quote=True)


def remplacer(s, ancien, nouveau, etiquette, compte):
    n = s.count(ancien)
    if n:
        compte[etiquette] = compte.get(etiquette, 0) + n
        return s.replace(ancien, nouveau)
    return s


idx_path = os.path.join(ROOT, 'index.html')
idx = open(idx_path, encoding='utf-8').read()
for lang, d in DATA.items():
    p = os.path.join(ROOT, F[lang])
    s = open(p, encoding='utf-8').read()
    c, ci = {}, {}
    # titres de section (sommaire + H2 statiques ; blocs « heading » du blog de index.html)
    for ancien, nouveau in d['h2']:
        s = remplacer(s, esc(ancien), esc(nouveau), 'h2', c)
        idx = remplacer(idx, '"' + ancien + '"', '"' + nouveau + '"', 'h2', ci)
    # paragraphes
    for i, (ancien, nouveau) in enumerate(d['paras']):
        statique = esc(nouveau)
        lien = d.get('liens', {}).get(str(i + 1))
        if lien:
            statique = statique.replace(esc(lien[0]), lien[1])
        s = remplacer(s, esc(ancien) if lang != 'es' else ancien, statique, 'p', c)
        idx = remplacer(idx, ancien, nouveau, 'p', ci)
    # FAQ : réponse visible (échappée), JSON-LD (brute), données du blog (brute)
    for ancien, nouveau in d['faq']:
        s = remplacer(s, esc(ancien) if lang != 'es' else ancien, esc(nouveau), 'faq', c)
        s = remplacer(s, json.dumps(ancien, ensure_ascii=False)[1:-1], json.dumps(nouveau, ensure_ascii=False)[1:-1], 'faq-ld', c)
        idx = remplacer(idx, ancien, nouveau, 'faq', ci)
    s, n1 = re.subn(r'("dateModified":\s*")[^"]*(")', r'\g<1>2026-10-04T12:00:00+02:00\2', s)
    s, n2 = re.subn(r'(<meta property="article:modified_time" content=")[^"]*(">)', r'\g<1>2026-10-04T12:00:00+02:00\2', s)
    open(p, 'w', encoding='utf-8').write(s)
    print('%-4s page : %s | index.html : %s | dates : %d+%d' % (lang, c, ci, n1, n2))
open(idx_path, 'w', encoding='utf-8').write(idx)
