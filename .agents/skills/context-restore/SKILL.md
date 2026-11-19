---
name: context-restore
description: "Restore task context after a long or interrupted session by finding the active objective, decisions, artifacts, and next verified step. Use when resuming work."
risk: unknown
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "context-restore"
sections[4]:
  - "\n"
  - "# Restore task context\n\nUse this runbook to resume a task from project artifacts and the current worktree. Do not assume memory or a prior handoff matches the checkout.\n\n"
  - "## Workflow\n\n1. Read applicable `AGENTS.md` files and the project's `AI_HANDOFF.md`, `CURRENT.md`, task list, or tracker when present.\n2. Check the current branch, revision, and `git status --short`. Read the relevant diff and preserve changes that predate the resumed task.\n3. Compare the stated objective and approvals with the latest plan, checkpoint, and code. Distinguish completed steps from proposals and stale handoff text.\n4. Inspect the files and tests relevant to the first unfinished step. Verify that its assumptions still hold in the current tree.\n5. Write down the exact next step and command, its scope, and its acceptance evidence. If scope or approval materially conflicts, ask before taking dependent action.\n6. Resume the first unfinished authorized step. Continue independent read-only work while waiting on any missing decision.\n\n"
  - "## Report\n\nState the branch and revision, current objective, preserved pre-existing edits, evidence reviewed, completed work, unresolved questions, and one concrete next action. Do not claim that a previous command passed unless its current result is available.\n"
