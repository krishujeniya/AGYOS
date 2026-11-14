#!/usr/bin/env bash
# Stage only the approved M1 prompt-principles files, commit with the required identity,
# push directly to origin/main to trigger GitHub Actions, and archive this script after success.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

[[ "$(git branch --show-current)" == "main" ]]
[[ "$(git config user.name)" == "Krish Ujeniya" ]]
[[ "$(git config user.email)" == "100012208+krishujeniya@users.noreply.github.com" ]]

git add -- \
  .agents/agents/vibe-engineer.md \
  .agents/rules/agyos-prompt-principles.md \
  .agents/rules/common-skill-routing.md \
  .agents/skills/enhance-prompt/SKILL.md \
  .agents/skills/prompt-engineer/README.md \
  .agents/skills/prompt-engineer/SKILL.md \
  .agents/skills/prompt-engineering-patterns/SKILL.md \
  .agents/skills/prompt-engineering-patterns/assets/few-shot-examples.json \
  .agents/skills/prompt-engineering-patterns/assets/prompt-template-library.md \
  .agents/skills/prompt-engineering-patterns/references/chain-of-thought.md \
  .agents/skills/prompt-engineering-patterns/references/few-shot-learning.md \
  .agents/skills/prompt-engineering-patterns/references/prompt-optimization.md \
  .agents/skills/prompt-engineering-patterns/references/prompt-templates.md \
  .agents/skills/prompt-engineering-patterns/references/system-prompts.md \
  .agents/skills/prompt-engineering-patterns/scripts/optimize-prompt.py \
  .agents/skills/prompt-engineering/SKILL.md \
  .agents/skills/prompt-library/SKILL.md \
  .agents/skills/prompt-library/references/FULL_RUNBOOK.md \
  .agents/skills/prompt-optimizer/SKILL.md \
  .agents/skills/prompt-optimizer/references/FULL_RUNBOOK.md \
  .agents/state/CURRENT.md \
  .agents/state/checkpoints/M1-prompt-principles.md \
  .agents/state/context-graph.json \
  .agents/state/state.json \
  .github/workflows/ci.yml \
  docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md \
  docs/PROMPT_PRINCIPLES_UPGRADE_TASK_LIST.md \
  docs/prompts.md \
  docs/references/README.md \
  docs/references/prompts.md \
  docs/adr/0003-prompt-principles-integration.md \
  docs/research/PROMPT_PRINCIPLES_AUDIT.md \
  scripts/audit_prompt_principles.py \
  scripts/tests/test_prompt_principles.py

git diff --cached --check
git commit -m "feat(prompting): align AGYOS prompts with audited principles"
git push origin main

script_path="${BASH_SOURCE[0]}"
mkdir -p .agents/state/decisions/executed
mv "$script_path" .agents/state/decisions/executed/
