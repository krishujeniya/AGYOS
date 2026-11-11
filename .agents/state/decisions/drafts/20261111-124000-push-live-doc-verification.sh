#!/usr/bin/env bash
# Publish the corrected live-page verification record and archive this execution.
# The operator authorized the catalog documentation updates and GitHub publication.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$REPO_ROOT"

DRAFT_REL=".agents/state/decisions/drafts/20261111-124000-push-live-doc-verification.sh"
EXECUTED_REL=".agents/state/decisions/executed/20261111-124000-push-live-doc-verification.sh"
CHECKPOINT=".agents/state/checkpoints/M1-skill-catalog-quality.md"

if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "Refusing to publish: current branch is not main." >&2
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Refusing to publish: working tree is not clean." >&2
  exit 1
fi

git fetch origin
git merge-base --is-ancestor origin/main main
PUSH_OUTPUT="$(git push origin main 2>&1 | sed 's/[[:blank:]]*$//')"
printf '%s\n' "$PUSH_OUTPUT"

{
  printf '\n\n## Live-verification docs push execution · %s\n\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '%s\n' '- Script: `.agents/state/decisions/executed/20261111-124000-push-live-doc-verification.sh`'
  printf '%s\n' '- Command: `git push origin main`'
  printf '%s\n' '- Result: successful exit; archived only after the documentation commit was pushed.'
  printf '\n```text\n%s\n```\n' "$PUSH_OUTPUT"
} >> "$CHECKPOINT"

git mv "$DRAFT_REL" "$EXECUTED_REL"
git add -- "$CHECKPOINT"
git diff --cached --check
bash bin/state-validate.sh
bash bin/gate-check.sh
git commit -m "chore(audit): record live documentation verification"

git fetch origin
git merge-base --is-ancestor origin/main main
ARCHIVE_PUSH_OUTPUT="$(git push origin main 2>&1 | sed 's/[[:blank:]]*$//')"
printf '%s\n' "$ARCHIVE_PUSH_OUTPUT"

LOCAL_SHA="$(git rev-parse HEAD)"
REMOTE_SHA="$(git ls-remote origin refs/heads/main | awk '{print $1}')"
if [[ "$LOCAL_SHA" != "$REMOTE_SHA" ]]; then
  echo "Refusing success: origin/main ($REMOTE_SHA) does not match HEAD ($LOCAL_SHA)." >&2
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Refusing success: working tree is not clean after publication." >&2
  exit 1
fi
printf 'Verified origin/main=%s; working tree clean.\n' "$LOCAL_SHA"
