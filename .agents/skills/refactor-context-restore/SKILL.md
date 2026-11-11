---
name: refactor-context-restore
description: "Resume an approved refactoring task by reconciling its plan, changed files, decisions, dependencies, and next safe step. Use before continuing an interrupted refactor."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Restore refactoring context

Use this runbook only for an existing refactoring task with a plan or explicit acceptance criteria.

## Workflow

1. Read the approved refactoring plan, relevant architecture decisions, repository instructions, and latest checkpoint.
2. Confirm branch, revision, worktree status, and the full relevant diff. Mark which edits were pre-existing, completed, or unfinished; do not revert changes just because the old plan predates them.
3. Trace the target module's current callers, contracts, configuration, and tests. Recheck dependencies because code may have changed since the plan was written.
4. Compare current structure with the refactor's stated goal and acceptance criteria. List any plan drift, new coupling, missing tests, or unresolved design choice with file evidence.
5. Choose the smallest next change that stays within the approved boundary. If the code no longer matches the plan or the next step expands scope, pause dependent edits and request a plan update.
6. Run the narrowest relevant regression check after an authorized change; record the exact command and actual result.

## Resume note

Report the approved refactoring plan, current revision, files already changed, preserved worktree edits, verified checks, remaining risks, and exact next command. This skill does not provide or assume a `context-restore` CLI.
