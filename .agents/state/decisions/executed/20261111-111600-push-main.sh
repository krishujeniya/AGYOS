#!/usr/bin/env bash
# Push the verified AGYOS skill-catalog update and already-ahead commits to origin/main.
# The operator explicitly authorized this GitHub push on 2026-11-11.
# Preconditions recorded for this revision:
# - focused catalog/router suite: 41 passed
# - host-skipped full suite: 155 passed, 1 host CLI test skipped
# - filtered AGYOS verifier: 51 checks passed; the same host test skipped inside its test suite
# - catalog and state validation, security scan, generated indexes, and diff checks passed
# - main is a fast-forward descendant of origin/main; no force push
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$REPO_ROOT"

if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "Refusing to push: current branch is not main." >&2
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Refusing to push: working tree is not clean." >&2
  exit 1
fi

git fetch origin
git merge-base --is-ancestor origin/main main
git push origin main
