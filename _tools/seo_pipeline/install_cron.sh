#!/usr/bin/env bash
# À lancer UNE fois, en tant qu'utilisateur seo, sur le VPS :
#   bash ~/webautonomos/_tools/seo_pipeline/install_cron.sh
# - active la fusion automatique des pages non santé (AUTO_MERGE=1, décision du 25/09/2026) ;
# - installe (ou remplace) la tâche de nuit : chaque jour à 3h17, run_nuit.sh (qui prend le
#   verrou AVANT de mettre le dépôt à jour).
# Idempotent : relancer ne crée pas de doublon.
set -euo pipefail
ENV="$HOME/.seo_pipeline.env"
[ -f "$ENV" ] || { echo "fichier $ENV introuvable"; exit 1; }
if grep -q '^AUTO_MERGE=' "$ENV"; then
  sed -i 's/^AUTO_MERGE=.*/AUTO_MERGE=1/' "$ENV"
else
  echo 'AUTO_MERGE=1' >> "$ENV"
fi
chmod 600 "$ENV"
LIGNE="17 3 * * * /bin/bash -lc 'cd \$HOME/webautonomos && bash _tools/seo_pipeline/run_nuit.sh >> \$HOME/nuit.log 2>&1'"
{ crontab -l 2>/dev/null | grep -v 'run_nuit.sh' | grep -v '# circuit SEO WebAutonomos' || true
  echo '# circuit SEO WebAutonomos (install_cron.sh) : passage de nuit'
  echo "$LIGNE"; } | crontab -
echo "AUTO_MERGE : $(grep '^AUTO_MERGE=' "$ENV")"
echo "tâche de nuit :"; crontab -l | grep -A0 'run_nuit.sh'
