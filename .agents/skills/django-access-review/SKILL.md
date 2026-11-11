---
name: django-access-review
description: Use when reviewing Django or DRF code for IDOR, object-level authorization, or user-to-user data access gaps.
risk: unknown
source: community
---
# Django Access Control & IDOR Review

Use when reviewing Django or DRF code for IDOR, object-level authorization, or user-to-user data access gaps.

## Workflow

1. Confirm the request fits this skill and identify the required inputs and output constraints.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.
4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.
5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.
6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.
