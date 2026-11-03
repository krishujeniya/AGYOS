#!/usr/bin/env bash
# Draft: Clean up temporary execution scripts and internal audit notes
set -euo pipefail

cd "$(dirname "$0")/../../../.."

echo "Removing temporary execution scripts and internal audit notes..."
git rm -f .agents/state/decisions/executed/20260725-045100-rewrite-git-history-author.sh \
       .agents/state/decisions/executed/20260725-045500-rewrite-git-history-gmail.sh \
       .agents/state/decisions/executed/20260725-045700-rewrite-git-tags-author.sh \
       docs/Need.md

echo "✅ Unnecessary files removed!"
