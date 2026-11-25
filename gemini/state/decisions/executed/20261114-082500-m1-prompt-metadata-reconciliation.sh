#!/usr/bin/env bash
# Commit only the reviewed keyword-metadata accounting correction and evidence;
# push directly to main so GitHub Actions can verify the exact revision.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

expected_head="99c26eb16b79a0ebefa41b98044bf973bbc53dd6"
expected_paths="$(cat <<'EOF'
.agents/state/CURRENT.md
.agents/state/checkpoints/M1-prompt-principles.md
.agents/state/state.json
docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md
docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md
docs/research/PROMPT_PRINCIPLES_AUDIT.md
scripts/audit_prompt_principles.py
scripts/tests/test_prompt_principles.py
EOF
)"

[[ "$(git branch --show-current)" == "main" ]]
[[ "$(git rev-parse HEAD)" == "$expected_head" ]]
[[ "$(git remote get-url origin)" == "https://github.com/krishujeniya/AGYOS.git" ]]
[[ -z "$(git diff --cached --name-only)" ]]
[[ "$(git config user.name)" == "Krish Ujeniya" ]]
[[ "$(git config user.email)" == "100012208+krishujeniya@users.noreply.github.com" ]]

remote_main="$(git ls-remote origin refs/heads/main | cut -f1)"
[[ "$remote_main" == "$expected_head" ]]
actual_paths="$(git diff --name-only | LC_ALL=C sort)"
[[ "$actual_paths" == "$expected_paths" ]]
git diff --check

git add -- \
  .agents/state/CURRENT.md \
  .agents/state/checkpoints/M1-prompt-principles.md \
  .agents/state/state.json \
  docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md \
  docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md \
  docs/research/PROMPT_PRINCIPLES_AUDIT.md \
  scripts/audit_prompt_principles.py \
  scripts/tests/test_prompt_principles.py

git diff --cached --check
git commit -m "fix(prompting): account for keyword metadata separately"
git push origin main

mkdir -p .agents/state/decisions/executed
mv "${BASH_SOURCE[0]}" .agents/state/decisions/executed/
