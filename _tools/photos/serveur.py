#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API du GPT « Photos WebAutonomos » (VPS).

Écoute en local ; le tunnel Cloudflare la publie sur https://photos.webautonomos.es.
Les opérations sont décrites pour ChatGPT dans gpt/openapi.yaml :

    GET  /suivante   prochain sujet : URL, titre, prompt de la photo, langues des textes
    POST /photo      reçoit l'image générée (openaiFileIdRefs), la réduit, la pose, publie
    POST /passer     laisse un sujet de côté
    GET  /etat       avancement
    GET  /sante      sans clé : le service répond

Variables (fichier ~/.config/photos/env) :
    PHOTOS_API_CLE   clé partagée avec le GPT (en-tête Authorization: Bearer …)
    PHOTOS_ROBOT=1   autorise synchro (reset sur origin/main) et push : clone dédié
    PHOTOS_PORT      8787 par défaut
"""

import fcntl
import hmac
import ipaddress
import json
import logging
import logging.handlers
import os
import socket
import sys
import tempfile
import threading
import time
import traceback
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import photos as P  # noqa: E402
import photos_lib as L  # noqa: E402

ETAT = os.path.expanduser(os.environ.get('PHOTOS_ETAT', '~/.local/state/photos'))
os.makedirs(ETAT, exist_ok=True)
CLE = os.environ.get('PHOTOS_API_CLE', '')
PORT = int(os.environ.get('PHOTOS_PORT', '8787'))
RESERVATION_S = 20 * 60          # un sujet donné au GPT n'est pas redonné pendant 20 min
MAX_OCTETS = 25 * 1024 * 1024

log = logging.getLogger('photos')
_h = logging.handlers.RotatingFileHandler(os.path.join(ETAT, 'serveur.log'), maxBytes=2_000_000, backupCount=3)
_h.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
log.addHandler(_h)
log.setLevel(logging.INFO)

_verrou_threads = threading.Lock()
_reservations = {}


class Verrou:
    """Une seule opération à la fois sur le dépôt, y compris face au job de nuit."""

    def __enter__(self):
        _verrou_threads.acquire()
        self.fh = open(os.path.join(ETAT, 'verrou'), 'w')
        fcntl.flock(self.fh, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        fcntl.flock(self.fh, fcntl.LOCK_UN)
        self.fh.close()
        _verrou_threads.release()


# --------------------------------------------------------------------------
# Opérations
# --------------------------------------------------------------------------

def suivante():
    with Verrou():
        P.synchro()
        data = P.charger()
        now = time.time()
        prets = [s for s in data['sujets'] if s.get('statut') == 'pret' and P.a_des_pages_actives(s)]
        # Un seul utilisateur : la page en cours (donnée, ni envoyée ni passée)
        # revient, avec son prompt à jour, au lieu de sauter à la suivante.
        en_cours = [s for s in prets if now - _reservations.get(s['id'], 0) < RESERVATION_S]
        s = en_cours[0] if en_cours else (prets[0] if prets else None)
        if s is not None:
            _reservations[s['id']] = now
            log.info('suivante -> %s%s', s['id'], ' (page en cours)' if en_cours else '')
            return 200, P.charge_utile(s, len(prets))
    return 200, {'termine': True, 'restants': 0,
                 'message': 'Toutes les pages prévues ont leur photo. Rien à générer pour le moment.'}


def _telecharger(url):
    """Télécharge l'image depuis le lien signé d'OpenAI (valable 5 minutes)."""
    u = urllib.parse.urlparse(url)
    if u.scheme != 'https' or not u.hostname:
        raise L.PhotoErreur('lien de téléchargement invalide')
    for info in socket.getaddrinfo(u.hostname, 443):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise L.PhotoErreur('adresse de téléchargement refusée')
    req = urllib.request.Request(url, headers={'User-Agent': 'photos-webautonomos/1.0'})
    with urllib.request.urlopen(req, timeout=40) as r:
        type_ = r.headers.get('Content-Type', '')
        data = r.read(MAX_OCTETS + 1)
    if len(data) > MAX_OCTETS:
        raise L.PhotoErreur('image trop lourde')
    signature = data[:4] in (b'\x89PNG', b'RIFF') or data[:3] == b'\xff\xd8\xff'
    if not (type_.startswith('image/') or signature):
        raise L.PhotoErreur("le fichier reçu n'est pas une image (%s)" % type_)
    fd, chemin = tempfile.mkstemp(prefix='recue-', suffix='.img', dir=ETAT)
    with os.fdopen(fd, 'wb') as fh:
        fh.write(data)
    return chemin


def _premiere_image(refs):
    for r in refs or []:
        if isinstance(r, str):
            try:
                r = json.loads(r)
            except ValueError:
                r = {'download_link': r}
        if isinstance(r, dict) and r.get('download_link'):
            return r
    return None


def recevoir_photo(corps):
    sid = (corps.get('sujet_id') or '').strip()
    ref = _premiere_image(corps.get('openaiFileIdRefs'))
    if not sid:
        return 400, {'ok': False, 'erreur': 'sujet_id manquant.'}
    if not ref:
        return 400, {'ok': False, 'erreur': "Aucune image jointe : mets l'image générée dans openaiFileIdRefs."}
    # contrôles avant le téléchargement : le lien d'OpenAI n'est valable que 5 minutes
    s = P.trouver(P.charger(), sid)
    textes = P.normaliser_textes(corps.get('textes'))
    manque = [lg for lg in P.langues(s) if not textes.get(lg, {}).get('alt')]
    if manque:
        return 400, {'ok': False, 'erreur': 'Il manque le texte alternatif pour : %s. Renvoie la photo avec '
                                             'un alt pour chaque langue.' % ', '.join(manque)}
    chemin = _telecharger(ref['download_link'])
    try:
        refus = _controler(chemin, sid, ref)
        if refus:
            return 422, {'ok': False, 'erreur': refus}
        with Verrou():
            titre = s['titre']
            fichiers = P.en_boucle(lambda: P.appliquer(sid, chemin, textes),
                                   'Photo auto : %s' % titre[:80])
            s = P.trouver(P.charger(), sid)
            _reservations.pop(sid, None)
    finally:
        try:
            os.remove(chemin)
        except OSError:
            pass
    pages = [p['url'] for p in s['pages'] if L.active(p)]
    en_attente = [p['url'] for p in s['pages'] if not L.active(p)]
    apercu = 'https://webautonomos.es/assets/%s.jpg?v=%s' % (s['fichier'], s.get('v'))
    log.info('photo %s v%s -> %d fichiers', sid, s.get('v'), len(fichiers))
    msg = 'Photo posée sur %d page(s), en ligne dans 2 minutes environ.' % len(pages)
    if s.get('type') == 'file' and not s.get('publie'):
        msg = 'Photo prête : elle paraîtra avec l\'article le %s.' % s.get('publication')
    if en_attente:
        msg += ' %d page(s) gelée(s) la recevront automatiquement à la fin du gel.' % len(en_attente)
    return 200, {'ok': True, 'sujet_id': sid, 'version': s.get('v'), 'pages': pages,
                 'photo_publiee': apercu, 'message': msg + ' Photo reçue : ' + apercu}


def _controler(chemin, sid, ref):
    """Refuse une image déjà reçue ou qui contient du texte. Garde chaque image
    reçue (acceptée ou refusée) dans ~/.local/state/photos/recues/ pour contrôle."""
    import hashlib
    import shutil
    from PIL import Image
    data = open(chemin, 'rb').read()
    empreinte = hashlib.sha1(data).hexdigest()
    try:
        w, h = Image.open(chemin).size
    except Exception:  # noqa: BLE001
        w = h = 0
    log.info('reçue pour %s : name=%s id=%s mime=%s %d×%d %d octets sha1=%s', sid, ref.get('name'), ref.get('id'),
             ref.get('mime_type'), w, h, len(data), empreinte[:12])
    dossier = os.path.join(ETAT, 'recues')
    os.makedirs(os.path.join(dossier, 'refusees'), exist_ok=True)
    index_f = os.path.join(dossier, 'index.json')
    index = L.lire_json(index_f, {})
    ext = {'image/png': '.png', 'image/webp': '.webp', 'image/jpeg': '.jpg'}.get(ref.get('mime_type'), '.img')
    nom = '%s-%s%s' % (sid, time.strftime('%Y%m%d-%H%M%S'), ext)
    if empreinte in index:
        shutil.copy(chemin, os.path.join(dossier, 'refusees', nom))
        return ("Cette image a déjà été envoyée (pour %s). Génère une photo entièrement nouvelle pour ce sujet, "
                "puis renvoie-la." % index[empreinte]['sujet'])
    textes = L.textes_dans_image(chemin)
    if textes is None:
        log.warning('détecteur de texte absent : contrôle sauté')
    elif textes:
        shutil.copy(chemin, os.path.join(dossier, 'refusees', nom))
        log.warning('refusée (texte) pour %s : %s', sid, ' | '.join(textes[:5]))
        extrait = ', '.join('« %s »' % t[:40] for t in textes[:3])
        return ("L'image contient du texte lisible (%s). Les photos du site ne doivent contenir aucun texte, lettre, "
                "chiffre ni logo : génère une nouvelle photo réaliste sans aucun texte, montre-la, et attends « ok »."
                % extrait)
    shutil.copy(chemin, os.path.join(dossier, nom))
    index[empreinte] = {'sujet': sid, 'fichier': nom, 'le': time.strftime('%Y-%m-%d %H:%M:%S')}
    L.ecrire_json(index_f, index)
    return None


def passer(corps):
    sid = (corps.get('sujet_id') or '').strip()

    def operation():
        data = P.charger()
        s = P.trouver(data, sid)
        s['statut'] = 'saute'
        s['note'] = (corps.get('raison') or 'laissé de côté depuis le GPT')[:200]
        L.ecrire_json(L.SUJETS_JSON, data)
        return ['_tools/photos/sujets.json']

    with Verrou():
        P.en_boucle(operation, 'Photos auto : sujet %s laissé de côté' % sid)
        _reservations.pop(sid, None)
    log.info('passer %s', sid)
    return 200, {'ok': True, 'message': 'Sujet %s laissé de côté.' % sid}


def etat():
    data = P.charger()
    compte = {}
    for s in data['sujets']:
        compte[s.get('statut')] = compte.get(s.get('statut'), 0) + 1
    prochain = next((s for s in data['sujets'] if s.get('statut') == 'pret' and P.a_des_pages_actives(s)), None)
    return 200, {'photos_faites': compte.get('fait', 0), 'restantes': compte.get('pret', 0),
                 'laissees_de_cote': compte.get('saute', 0),
                 'pages_illustrees': len(L.images()),
                 'prochain': prochain and {'sujet_id': prochain['id'], 'titre': prochain['titre']}}


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

class Gestionnaire(BaseHTTPRequestHandler):
    server_version = 'photos-webautonomos/1.0'
    sys_version = ''

    def _repondre(self, code, obj):
        corps = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(corps)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(corps)

    def _autorise(self):
        recu = self.headers.get('Authorization', '')
        if CLE and hmac.compare_digest(recu.encode(), ('Bearer ' + CLE).encode()):
            return True
        self._repondre(401, {'ok': False, 'erreur': 'clé API invalide'})
        return False

    def _executer(self, fonction, *args):
        try:
            code, obj = fonction(*args)
        except L.PhotoErreur as e:
            log.warning('%s : %s', self.path, e)
            code, obj = 422, {'ok': False, 'erreur': str(e)}
        except Exception as e:  # noqa: BLE001 — le GPT doit recevoir une réponse lisible
            log.error('%s : %s\n%s', self.path, e, traceback.format_exc())
            code, obj = 500, {'ok': False, 'erreur': 'erreur du serveur : %s' % str(e)[:200]}
        self._repondre(code, obj)

    def do_GET(self):
        chemin = urllib.parse.urlparse(self.path).path
        if chemin == '/sante':
            return self._repondre(200, {'ok': True})
        if not self._autorise():
            return
        if chemin == '/suivante':
            return self._executer(suivante)
        if chemin == '/etat':
            return self._executer(etat)
        self._repondre(404, {'ok': False, 'erreur': 'adresse inconnue'})

    def do_POST(self):
        if not self._autorise():
            return
        n = int(self.headers.get('Content-Length') or 0)
        if n > 2_000_000:
            return self._repondre(413, {'ok': False, 'erreur': 'requête trop grosse'})
        try:
            corps = json.loads(self.rfile.read(n) or b'{}')
        except ValueError:
            return self._repondre(400, {'ok': False, 'erreur': 'JSON illisible'})
        chemin = urllib.parse.urlparse(self.path).path
        if chemin == '/photo':
            return self._executer(recevoir_photo, corps)
        if chemin == '/passer':
            return self._executer(passer, corps)
        self._repondre(404, {'ok': False, 'erreur': 'adresse inconnue'})

    def log_message(self, fmt, *args):
        log.info('%s %s', self.headers.get('Cf-Connecting-Ip', self.address_string()), fmt % args)


def main():
    if not CLE or len(CLE) < 24:
        sys.exit('PHOTOS_API_CLE absente ou trop courte (24 caractères minimum).')
    serveur = ThreadingHTTPServer(('127.0.0.1', PORT), Gestionnaire)
    log.info('écoute sur 127.0.0.1:%d (robot=%s)', PORT, P.robot())
    print('Photos WebAutonomos : écoute sur 127.0.0.1:%d' % PORT, flush=True)
    serveur.serve_forever()


if __name__ == '__main__':
    main()
