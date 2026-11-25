#!/usr/bin/env bash
# Push verified local main commit c20a29b to remote origin/main
# Preconditions:
# - Working tree clean
# - All 110 unit tests passing
# - Fast-forward on top of remote SHA 775c674
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../../.."
git push origin main
