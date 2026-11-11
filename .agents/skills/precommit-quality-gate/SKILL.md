---
name: precommit-quality-gate
description: PreToolUse fact-forcing gate that denies the first Edit/Write/Bash (including MultiEdit and NotebookEdit) attempt until the agent presents concrete facts (importers, data schemas, verbatim user instruction), then allows retry; A/B-tested at +2.25 quality points. Use when enabling or configuring the GateGuard hook, exempting paths via env vars, or handling first-touch denials.
metadata:
  origin: community
---
# GateGuard — Fact-Forcing Pre-Action Gate

PreToolUse fact-forcing gate that denies the first Edit/Write/Bash (including MultiEdit and NotebookEdit) attempt until the agent presents concrete facts (importers, data schemas, verbatim user instruction), then allows retry; A/B-tested at +2.25 quality points. Use when enabling or configuring the GateGuard hook, exempting paths via env vars, or handling first-touch denials.

## Workflow

1. Confirm the request fits this skill and identify the required inputs and output constraints.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.
4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.
5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.
6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.
