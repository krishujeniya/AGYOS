---
name: issue-review
description: Review a GitHub issue the way /code-review reviews a PR. Fetches the issue with the gh CLI, checks the report against the current codebase, searches for duplicates and prior fixes, scores completeness, assigns severity, and writes a triage report plus a draft reply. Posting comments or labels is opt-in only. Use when the user asks to check, triage, validate, or review a GitHub issue.
metadata:
  origin: ECC
---
# Issue Review

Review a GitHub issue the way /code-review reviews a PR. Fetches the issue with the gh CLI, checks the report against the current codebase, searches for duplicates and prior fixes, scores completeness, assigns severity, and writes a triage report plus a draft reply. Posting comments or labels is opt-in only. Use when the user asks to check, triage, validate, or review a GitHub issue.

## Workflow

1. Confirm the request fits this skill and identify the required inputs and output constraints.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.
4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.
5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.
6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.
