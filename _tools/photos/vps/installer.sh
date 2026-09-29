#!/usr/bin/env bash
# Installation de l'automatisation « une photo par page » sur le VPS (utilisateur ubuntu).
# Chaque étape est rejouable sans risque.
#
#   bash installer.sh cle        # 1. clé de déploiement GitHub (à ajouter au dépôt, écriture autorisée)
#   bash installer.sh clone      # 2. clone dédié du robot : ~/photos/webautonomos
#   bash installer.sh env        # 3. ~/.config/photos/env (clé API du GPT générée ici)
#   bash installer.sh cloudflared  # 4. binaire cloudflared dans ~/.local/bin
#   bash installer.sh tunnel     # 5. après « cloudflared tunnel login » : tunnel + DNS photos.webautonomos.es
#   bash installer.sh services   # 6. services systemd utilisateur (API, tunnel, nuit)
#   bash installer.sh etat       # contrôle de l'ensemble
set -euo pipefail

DEPOT_URL="github-photos:pasurite-sketch/webautonomos.git"
CLONE="$HOME/photos/webautonomos"
CLE_SSH="$HOME/.ssh/photos_webautonomos"
ENVF="$HOME/.config/photos/env"
TUNNEL="photos-webautonomos"
HOTE="photos.webautonomos.es"
CF="$HOME/.local/bin/cloudflared"

etape_cle() {
  mkdir -p ~/.ssh && chmod 700 ~/.ssh
  [ -f "$CLE_SSH" ] || ssh-keygen -t ed25519 -N "" -C "photos-bot@vps" -f "$CLE_SSH" >/dev/null
  if ! grep -q "^Host github-photos" ~/.ssh/config 2>/dev/null; then
    printf '\nHost github-photos\n  HostName github.com\n  User git\n  IdentityFile %s\n  IdentitiesOnly yes\n' "$CLE_SSH" >> ~/.ssh/config
    chmod 600 ~/.ssh/config
  fi
  grep -q "^github.com " ~/.ssh/known_hosts 2>/dev/null || ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts 2>/dev/null
  echo "Clé publique à ajouter au dépôt (Deploy keys, écriture autorisée) :"
  cat "$CLE_SSH.pub"
}

etape_clone() {
  mkdir -p "$(dirname "$CLONE")"
  if [ ! -d "$CLONE/.git" ]; then
    git clone -q "$DEPOT_URL" "$CLONE"
  fi
  git -C "$CLONE" fetch -q origin && git -C "$CLONE" reset -q --hard origin/main
  echo "clone : $CLONE ($(git -C "$CLONE" log --oneline -1))"
}

etape_env() {
  mkdir -p "$(dirname "$ENVF")" "$HOME/.local/state/photos"
  if [ ! -f "$ENVF" ]; then
    umask 077
    printf 'PHOTOS_API_CLE=%s\nPHOTOS_ROBOT=1\nPHOTOS_PORT=8787\n' "$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')" > "$ENVF"
  fi
  chmod 600 "$ENVF"
  echo "fichier de configuration : $ENVF (clé API non affichée)"
}

etape_cloudflared() {
  mkdir -p "$HOME/.local/bin"
  if [ ! -x "$CF" ]; then
    curl -fsSL -o "$CF" https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    chmod +x "$CF"
  fi
  "$CF" --version
}

etape_tunnel() {
  [ -f "$HOME/.cloudflared/cert.pem" ] || { echo "Lancer d'abord : $CF tunnel login"; exit 1; }
  "$CF" tunnel list 2>/dev/null | grep -q " $TUNNEL " || "$CF" tunnel create "$TUNNEL"
  ID=$("$CF" tunnel list 2>/dev/null | awk -v t="$TUNNEL" '$2==t {print $1}')
  cat > "$HOME/.cloudflared/photos.yml" <<EOF
tunnel: $ID
credentials-file: $HOME/.cloudflared/$ID.json
ingress:
  - hostname: $HOTE
    service: http://127.0.0.1:8787
  - service: http_status:404
EOF
  "$CF" tunnel route dns "$TUNNEL" "$HOTE" || true
  echo "tunnel $TUNNEL ($ID) -> $HOTE"
}

etape_services() {
  mkdir -p "$HOME/.config/systemd/user" "$HOME/.local/state/photos"
  cp "$CLONE"/_tools/photos/vps/photos-*.service "$CLONE"/_tools/photos/vps/photos-*.timer "$HOME/.config/systemd/user/"
  systemctl --user daemon-reload
  systemctl --user enable --now photos-api.service photos-nuit.timer
  [ -f "$HOME/.cloudflared/photos.yml" ] && systemctl --user enable --now photos-tunnel.service
  loginctl show-user "$USER" -p Linger
}

etape_etat() {
  systemctl --user --no-pager --plain list-units 'photos-*' || true
  curl -s -m 5 http://127.0.0.1:8787/sante && echo
  [ -f "$HOME/.cloudflared/photos.yml" ] && curl -s -m 10 "https://$HOTE/sante" && echo
}

case "${1:-}" in
  cle) etape_cle ;; clone) etape_clone ;; env) etape_env ;; cloudflared) etape_cloudflared ;;
  tunnel) etape_tunnel ;; services) etape_services ;; etat) etape_etat ;;
  *) sed -n '2,13p' "$0" ;;
esac
