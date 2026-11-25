#!/usr/bin/env bash
# Commit only the reviewed final PASS state for the prompt-principles milestone;
# push it to main for exact-revision GitHub Actions verification.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

expected_head="31b4018d38cfe68cae669f5df689c257ccc8b069"
expected_paths="$(cat <<'EOF'
.agents/state/CURRENT.md
.agents/state/checkpoints/M1-prompt-principles.md
.agents/state/state.json
docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md
docs/research/PROMPT_PRINCIPLES_AUDIT.md
EOF
)"

[[ "$(git branch --show-current)" == "main" ]]
[[ "$(git branch --format='%(refname:short)' | LC_ALL=C sort)" == "main" ]]
[[ "$(git rev-parse HEAD)" == "$expected_head" ]]
[[ "$(git remote get-url origin)" == "https://github.com/krishujeniya/AGYOS.git" ]]
[[ -z "$(git diff --cached --name-only)" ]]
[[ "$(git config user.name)" == "Krish Ujeniya" ]]
[[ "$(git config user.email)" == "100012208+krishujeniya@users.noreply.github.com" ]]

remote_branches="$(git ls-remote --heads origin | awk '{print $2}' | LC_ALL=C sort)"
[[ "$remote_branches" == "refs/heads/main" ]]
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

[[ "$(git diff --cached --name-only | LC_ALL=C sort)" == "$expected_paths" ]]
git diff --cached --check
git commit -m "docs(prompting): close verified milestone state"
git push origin main

mkdir -p .agents/state/decisions/executed
mv "${BASH_SOURCE[0]}" .agents/state/decisions/executed/
