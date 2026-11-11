#!/usr/bin/env bash
# Push verified local main commit ae1275b to remote origin/main
# Preconditions:
# - Working tree clean
# - 128 unit tests passing (scripts/tests)
# - 51/51 adversarial verification checks passing (scripts/agyos-verify.sh)
# - Fast-forward on top of remote origin/main (190e8ea)
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../../.."
git push origin main
