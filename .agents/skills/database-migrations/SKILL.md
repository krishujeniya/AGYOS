---
name: database-migrations
description: "Safe, reversible database migration patterns: forward-only production changes, expand-contract zero-downtime renames, concurrent indexes, batched backfills, and per-tool workflows for PostgreSQL, Prisma, Drizzle, Kysely, Django, and golang-migrate. Use when writing a schema or data migration, adding a column or index to a large table, planning a rollback, or preparing a zero-downtime deploy."
metadata:
  origin: ECC
---
# Database Migration Patterns

Safe, reversible database migration patterns: forward-only production changes, expand-contract zero-downtime renames, concurrent indexes, batched backfills, and per-tool workflows for PostgreSQL, Prisma, Drizzle, Kysely, Django, and golang-migrate. Use when writing a schema or data migration, adding a column or index to a large table, planning a rollback, or preparing a zero-downtime deploy.

## Workflow

1. Confirm the request fits this skill and identify the required inputs and output constraints.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.
4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.
5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.
6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.
