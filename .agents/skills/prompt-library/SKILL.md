---
name: prompt-library
description: "Reusable AGYOS prompt patterns for common tasks. Adapt them to the user's intent, context, and constraints; community provenance is recorded in the runbook."
risk: unknown
source: community
date_added: "2026-02-27"
---
# Prompt Library

Reusable prompt patterns for common tasks. Adapt each pattern to the user's intent and constraints; do not treat examples as universal instructions. Historical attribution is recorded in the runbook.

## Workflow

1. Identify the requested outcome, useful context, constraints, and output format.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Keep AGYOS as the default identity in AGYOS-authored prompt text. Retain third-party names only for compatibility, attribution, or evidence.
4. Add examples, output schemas, or ordered steps only when they solve a real task need. Never ask for hidden reasoning traces.
5. Do not treat a prompt template as permission to perform the actions it describes. Follow the current user's authorization and project rules.
6. Return the requested format and identify assumptions or limitations that materially affect use.
