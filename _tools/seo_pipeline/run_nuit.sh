#!/usr/bin/env bash
# Passage de nuit du circuit SEO (lancé par cron, voir install_cron.sh).
#  1. relit sur GitHub l'état des PR (fusionnées → pages publiées) ;
#  2. affinage : contrôle gratuit des scores SERPmantics des pages publiées, les moins
#     récemment contrôlées d'abord, et retouche de celles qui ne sont pas au vert
#     (au plus MAX_AFFINAGES retouches par nuit) ;
#  3. nouvelles pages : les N_NOUVELLES suivantes de pages.json.
# Coût : 0 € de plus (mesures SERPmantics gratuites, guides réutilisés ; Claude sur
# l'abonnement). Seule limite : le quota d'utilisation de l'abonnement Claude.
main() {
set -uo pipefail
REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
cd "$REPO"
P="_tools/seo_pipeline"
mkdir -p "$P/runs"
exec 9>"$P/runs/.lock"
flock -n 9 || { echo "déjà en cours"; exit 0; }
# Mise à jour APRÈS le verrou : jamais de git checkout pendant qu'un lot travaille (26/09 :
# le cron de 3h17 avait basculé le dépôt sur main au milieu d'un passage).
if [ -z "$(git status --porcelain --untracked-files=no)" ]; then
  git checkout -q main && git fetch -q origin main && git reset -q --hard origin/main
fi
[ -f "$HOME/.seo_pipeline.env" ] && set -a && . "$HOME/.seo_pipeline.env" && set +a
MAX_AFFINAGES="${MAX_AFFINAGES:-3}"
N_NOUVELLES="${N_NOUVELLES:-2}"
echo "===== nuit du $(date '+%F %T') ====="
python3 "$P/pipeline.py" sync || true
faits=0
for slug in $(python3 "$P/pipeline.py" a-affiner --n 50); do
  [ "$faits" -ge "$MAX_AFFINAGES" ] && break
  bash "$P/run_page.sh" "$slug" --affiner
  rc=$?
  case "$rc" in
    3) ;;                        # déjà au vert : rien à faire, page suivante
    2) echo "$slug : affinage impossible (voir $P/runs/$slug/run.log)" ;;
    *) faits=$((faits + 1)) ;;   # retouche faite (PR) ou À REVOIR
  esac
done
echo "affinages de la nuit : $faits"
for slug in $(python3 "$P/pipeline.py" next --n "$N_NOUVELLES"); do
  bash "$P/run_page.sh" "$slug" || echo "$slug : non publié (voir $P/runs/$slug/run.log)"
done
python3 "$P/pipeline.py" status
}
main "$@"
