# -*- coding: utf-8 -*-
"""FAQ écrite dans le HTML des pages i18n (/visibilidad-ia/ et ses copies FR et EN).

Pourquoi (04/10/2026) : la liste #faq-list n'était remplie que par JavaScript, depuis
T[lang].faq. Un robot qui n'exécute pas les scripts, et la mesure SERPmantics, ne
voyaient aucune question. On écrit donc les questions dans le HTML, avec le balisage
exact de tr() : au chargement, tr() les réécrit à l'identique dans la langue active.

Utilisé par prerender_i18n.py (page espagnole) et build_i18n_pages.py (copies).
"""
import json
import re

SVG = ('<svg fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
       'stroke-linejoin="round" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 9l-7 7-7-7"></path></svg>')


def faq_html(faq):
    """Même balisage que la fonction tr() de la page."""
    return ''.join('<details><summary>%s%s</summary><div class="answer">%s</div></details>' % (q, SVG, r)
                   for q, r in faq)


def remplir_faq(html, faq):
    """Remplace le contenu de <div … id="faq-list"> par la FAQ ; (html, True) si la liste existe."""
    m = re.search(r'<div\b[^>]*\bid="faq-list"[^>]*>', html)
    if not m:
        return html, False
    d, fin = 1, None
    for t in re.finditer(r'<div\b|</div>', html[m.end():]):
        d += -1 if t.group(0) == '</div>' else 1
        if d == 0:
            fin = m.end() + t.start()
            break
    if fin is None:
        raise SystemExit('div#faq-list non refermée')
    return html[:m.end()] + faq_html(faq) + html[fin:], True


def faq_jsonld(html, faq, ld_id='faq-schema'):
    """Réécrit mainEntity du JSON-LD FAQPage depuis la FAQ (le contrôle d'intégrité les compare)."""
    mo = re.search(r'(<script type="application/ld\+json" id="%s">)(.*?)(</script>)' % ld_id, html, re.S)
    if not mo:
        return html
    g = json.loads(mo.group(2))
    g['mainEntity'] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}}
                       for q, r in faq]
    return html[:mo.start(2)] + '\n' + json.dumps(g, ensure_ascii=False, indent=2) + '\n' + html[mo.end(2):]
