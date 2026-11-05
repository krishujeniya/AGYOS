---
name: agyos-decision
description: Select relevant AGYOS skills for any task or follow-up, inspect their runbooks, and assess workflow complexity. Use when starting work, changing objectives, or maintaining skill routing and discovery metadata.
---
# Skill decision and execution

1. Inspect the request and honor explicit skill choices and constraints.
2. Run `bin/agyos decide "<task>" --json --runbook` from the checkout.
   MCP alternative: `agyos_decision` with `task` and `include_runbook: true`.
3. Read the returned runbook and assess its fit before specialist work. Without
   `--runbook`, read `runbook_path` or use `bin/agyos skill <primary_skill>`.
   A runbook already read in the session may be reused if it is unchanged.
4. Apply relevant steps and inspect linked resources only as needed. Re-run
   discovery if the objective changes or the recommendation is unsuitable.
5. Verify the actual changes and report executed evidence and remaining limits.

The decision covers the complete physical catalog through a tiered manifest.
Task intent takes priority over language keywords. Explicit skill IDs take
priority over heuristic ranking. Word boundaries and phrases prevent accidental
substring matches. Unclassified requests use this runbook for objective inspection.

`confidence` is a matching heuristic, not a probability. `selection_status` is
`matched` or `fallback`. `execution_status` starts at `pending_runbook_read` and
becomes `runbook_returned` when the CLI or MCP returns its contents. Neither
status certifies application, verification, or success.

Complexity 1-2 permits the fast path only for bounded low-risk work. Complexity
3-5 follows the full workflow; security, payments, migrations, and broad rule or
skill changes require broader inspection even when the request is short.

All rules and skills follow `.agents/rules/common-skill-routing.md`.
See `docs/SKILL_ROUTING.md` for maintenance commands and limitations.
