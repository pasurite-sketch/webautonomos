# -*- coding: utf-8 -*-
"""Article « facturación electrónica obligatoria » (ES, VAL, EN ; pages statiques et données du blog de
index.html) : l'application gratuite de facturation de l'AEAT est disponible dans sa sede, elle n'est plus
seulement « annoncée ». Elle répond à Verifactu ; sa page ne dit rien de la facture électronique entre
entreprises, d'où la réserve. Lien vers la page officielle dans les pages statiques seulement. Idempotent ;
à lancer après patch_factura_electronica_20261004.py.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = ('https://sede.agenciatributaria.gob.es/Sede/ayuda/consultas-informaticas/'
       'presentacion-declaraciones-ayuda-tecnica/aplicacion-gratuita-verifactu-aeat.html')
LIEN = '<a href="' + URL + '" style="color:#2563eb;" target="_blank" rel="noopener">%s</a>'

DATA = {
    'es': {
        'f': 'blog/es/facturacion-electronica-autonomos-obligatoria.html',
        'p': ["La Agencia Tributaria ha anunciado una aplicación de facturación gratuita para autónomos y pymes con pocas facturas: comprueba en su sede si ya está disponible y qué incluye.",
              "La Agencia Tributaria ofrece en su sede una aplicación gratuita de facturación, pensada para profesionales, autónomos y empresas con poca facturación: cumple con Verifactu, pero comprueba si te servirá también para la factura electrónica entre empresas antes de contar con ella.",
              "una aplicación gratuita de facturación"],
        'faq': ["Con poco volumen puede bastarte un programa con plan gratuito o la aplicación gratuita que ha anunciado la Agencia Tributaria, si ya está disponible.",
                "Con poco volumen puede bastarte un programa con plan gratuito o la aplicación gratuita de facturación de la Agencia Tributaria, pensada para Verifactu."],
    },
    'val': {
        'f': 'blog/val/facturacio-electronica-obligatoria.html',
        'p': ["L'Agència Tributària ha anunciat una aplicació de facturació gratuïta per a autònoms i pimes amb poques factures: comprova en la seua seu si ja està disponible i què inclou.",
              "L'Agència Tributària oferix en la seua seu una aplicació gratuïta de facturació, pensada per a professionals, autònoms i empreses amb poca facturació: complix amb Verifactu, però comprova si et servirà també per a la factura electrònica entre empreses abans de comptar-hi.",
              "una aplicació gratuïta de facturació"],
        'faq': ["Amb poc volum et pot bastar un programa amb pla gratuït o l'aplicació gratuïta que ha anunciat l'Agència Tributària, si ja està disponible.",
                "Amb poc volum et pot bastar un programa amb pla gratuït o l'aplicació gratuïta de facturació de l'Agència Tributària, pensada per a Verifactu."],
    },
    'en': {
        'f': 'blog/en/mandatory-e-invoicing-for-freelancers.html',
        'p': ["The Spanish Tax Agency has announced a free invoicing application for freelancers and small businesses with few invoices: check on its website whether it is already available and what it includes.",
              "The Spanish Tax Agency offers a free invoicing application on its website, designed for professionals, freelancers and companies with a low invoicing volume: it complies with Verifactu, but check whether it will also cover electronic invoicing between businesses before relying on it.",
              "a free invoicing application"],
        'faq': ["With a low volume, invoicing software with a free plan may be enough, or the free application announced by the Spanish Tax Agency, if it is already available.",
                "With a low volume, invoicing software with a free plan may be enough, or the free invoicing application of the Spanish Tax Agency, designed for Verifactu."],
    },
}


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
    p = os.path.join(ROOT, d['f'])
    s = open(p, encoding='utf-8').read()
    c, ci = {}, {}
    ancien, nouveau, ancre = d['p']
    s = remplacer(s, esc(ancien), esc(nouveau).replace(esc(ancre), LIEN % esc(ancre), 1), 'p', c)
    idx = remplacer(idx, ancien, nouveau, 'p', ci)
    ancien, nouveau = d['faq']
    # réponse visible (échappée), puis JSON-LD (brut) ; les deux formes ne diffèrent qu'en valencien
    s = remplacer(s, esc(ancien), esc(nouveau), 'faq', c)
    s = remplacer(s, json.dumps(ancien, ensure_ascii=False)[1:-1], json.dumps(nouveau, ensure_ascii=False)[1:-1], 'faq-ld', c)
    idx = remplacer(idx, ancien, nouveau, 'faq', ci)
    open(p, 'w', encoding='utf-8').write(s)
    print('%-4s page : %s | index.html : %s' % (lang, c, ci))
open(idx_path, 'w', encoding='utf-8').write(idx)
