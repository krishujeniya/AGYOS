#!/usr/bin/env bash
# Safe AGYOS rollback: read-only by default, explicit forward revert only.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
usage() {
  cat <<'EOF'
Usage: bin/agyos rollback [--plan]
       bin/agyos rollback --apply --commit HEAD
Safe revert creates an inverse commit on main. It never hard-resets, cleans
untracked work, creates a branch, or automatically undoes external actions.
EOF
}
if [[ $# -eq 0 || "${1:-}" == "--plan" || "${1:-}" == "--help" ]]; then
  usage
  echo "No changes made."
  exit 0
fi
if [[ $# -ne 3 || "$1" != "--apply" || "$2" != "--commit" || "$3" != "HEAD" ]]; then
  echo "ERROR: explicit --apply --commit HEAD required." >&2
  exit 2
fi
if [[ "$(git -C "$ROOT" branch --show-current)" != "main" ]]; then
  echo "ERROR: rollback is restricted to main." >&2
  exit 2
fi
if [[ -n "$(git -C "$ROOT" status --porcelain=v1 --untracked-files=all)" ]]; then
  echo "ERROR: working tree is not clean; preserve your changes." >&2
  exit 2
fi
HEAD_SHA="$(git -C "$ROOT" rev-parse --verify 'HEAD^{commit}')"
if ! git -C "$ROOT" rev-parse --verify "$HEAD_SHA^" >/dev/null 2>&1; then
  echo "ERROR: root commit cannot be automatically reverted." >&2
  exit 2
fi
if [[ "$(git -C "$ROOT" rev-list --parents -n 1 HEAD | wc -w)" -ne 2 ]]; then
  echo "ERROR: merge commits require deliberate manual revert." >&2
  exit 2
fi
git -C "$ROOT" revert --no-edit "$HEAD_SHA"
echo "Created a non-destructive revert commit on main."
