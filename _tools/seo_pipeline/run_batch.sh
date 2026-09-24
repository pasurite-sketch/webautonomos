#!/usr/bin/env bash
# Traite les N prochaines pages (par priorité). Pour cron.
# Usage : N=3 bash _tools/seo_pipeline/run_batch.sh
set -uo pipefail
REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$REPO"
P="_tools/seo_pipeline"
mkdir -p "$P/runs"
exec 9>"$P/runs/.lock"
flock -n 9 || { echo "déjà en cours"; exit 0; }
N="${N:-3}"
for slug in $(python3 "$P/pipeline.py" next --n "$N"); do
  bash "$P/run_page.sh" "$slug" || echo "$slug : non publié (voir $P/runs/$slug/run.log)"
done
python3 "$P/pipeline.py" status
