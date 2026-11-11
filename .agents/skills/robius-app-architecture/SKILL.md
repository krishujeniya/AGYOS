---
name: robius-app-architecture
description: |
  CRITICAL: Use for Robius app architecture patterns. Triggers on:
  Tokio, async, submit_async_request, 异步, 架构,
  SignalToUI, Cx::post_action, worker task,
  app structure, MatchEvent, handle_startup
risk: unknown
source: community
---
# Robius App Architecture Skill

CRITICAL: Use for Robius app architecture patterns. Triggers on:
Tokio, async, submit_async_request, 异步, 架构,
SignalToUI, Cx::post_action, worker task,
app structure, MatchEvent, handle_startup

## Workflow

1. Confirm the request fits this skill and identify the required inputs and output constraints.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.
4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.
5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.
6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.
