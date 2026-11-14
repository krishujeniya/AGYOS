#!/usr/bin/env bash
# Commit only the reviewed parser fix, CI artifact-derived catalogs, and milestone evidence;
# push directly to main so GitHub Actions can verify the corrected exact revision.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

expected_head="dbb6f8df3c352384a8543c8908aab5a28082bc19"
[[ "$(git branch --show-current)" == "main" ]]
[[ "$(git rev-parse HEAD)" == "$expected_head" ]]
[[ "$(git remote get-url origin)" == "https://github.com/krishujeniya/AGYOS.git" ]]
[[ -z "$(git diff --cached --name-only)" ]]
[[ "$(git config user.name)" == "Krish Ujeniya" ]]
[[ "$(git config user.email)" == "100012208+krishujeniya@users.noreply.github.com" ]]

remote_main="$(git ls-remote origin refs/heads/main | cut -f1)"
[[ "$remote_main" == "$expected_head" ]]

git add -- \
  .agents/skills-manifest.json \
  .agents/state/CURRENT.md \
  .agents/state/checkpoints/M1-prompt-principles.md \
  .agents/state/state.json \
  docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md \
  docs/llms.txt \
  docs/research/PROMPT_PRINCIPLES_AUDIT.md \
  docs/skills-data.json \
  scripts/audit_prompt_principles.py \
  scripts/tests/test_prompt_principles.py

git diff --cached --check
git commit -m "fix(prompting): reconcile source audit counts and catalogs"
git push origin main

mkdir -p .agents/state/decisions/executed
mv "${BASH_SOURCE[0]}" .agents/state/decisions/executed/
