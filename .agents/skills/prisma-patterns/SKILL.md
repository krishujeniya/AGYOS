---
name: prisma-patterns
description: Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion. Use when writing a Prisma schema or query, or debugging transactions, migrations, or serverless connection limits.
metadata:
  origin: ECC
---
# Prisma Patterns

Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like updateMany returning count not records, $transaction timeouts, migrate dev resetting the DB, @updatedAt skipped on bulk writes, and serverless connection exhaustion. Use when writing a Prisma schema or query, or debugging transactions, migrations, or serverless connection limits.

## Workflow

1. Confirm the request fits this skill and identify the required inputs and output constraints.
2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).
3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.
4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.
5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.
6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.
