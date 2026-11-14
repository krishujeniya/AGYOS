#!/usr/bin/env bash
# Commit only the final CI artifact counts and milestone evidence;
# push directly to main to verify the evidence-only revision in GitHub Actions.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

expected_head="98486147dbab917deee345fd4c36498f5901bc01"
expected_paths="$(cat <<'EOF'
.agents/state/CURRENT.md
.agents/state/checkpoints/M1-prompt-principles.md
.agents/state/state.json
docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md
docs/research/PROMPT_PRINCIPLES_AUDIT.md
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
  docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md \
  docs/research/PROMPT_PRINCIPLES_AUDIT.md

git diff --cached --check
git commit -m "docs(prompting): record verified principles audit"
git push origin main

mkdir -p .agents/state/decisions/executed
mv "${BASH_SOURCE[0]}" .agents/state/decisions/executed/
