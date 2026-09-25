#!/usr/bin/env bash
# Traite une liste de pages, l'une après l'autre (même verrou que run_batch.sh).
# Usage : bash _tools/seo_pipeline/run_lot.sh <slug>[:--reparer|:--reprise] …
# Ex.   : bash _tools/seo_pipeline/run_lot.sh es-electricistas:--reparer en-carpenters
set -uo pipefail
REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$REPO"
P="_tools/seo_pipeline"
mkdir -p "$P/runs"
exec 9>"$P/runs/.lock"
flock -n 9 || { echo "déjà en cours"; exit 0; }
for item in "$@"; do
  slug="${item%%:*}"
  opt=""
  [ "$item" != "$slug" ] && opt="${item#*:}"
  # shellcheck disable=SC2086
  bash "$P/run_page.sh" "$slug" $opt || echo "$slug : non publié (voir $P/runs/$slug/run.log)"
done
python3 "$P/pipeline.py" status
