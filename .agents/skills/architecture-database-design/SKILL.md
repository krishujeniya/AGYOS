---
name: architecture-database-design
description: "Master of PostgreSQL schema design, optimization, and safe migrations. Enforces strict conventions for IDs, indexes, JSONB, and transactional DDL. Use whenever modifying the data layer."
category: architecture
risk: safe
tags: "[postgres, database, sql, schema, migration, optimization, indexing]"
version: "1.0.0"
prompt-source: prompt.toon
---
skill: "architecture-database-design"
sections[10]:
  - "\n"
  - "# Architecture: Database Design\n\n"
  - "## Purpose\nThis skill establishes strict architectural and optimization guidelines for the PostgreSQL database. It complements the `database-asyncpg-qdrant` skill by enforcing robust schema design, proper indexing, safe migrations, and efficient data access patterns.\n\n"
  - "## When to Use\n- **Gate 3 (PLAN):** When designing table schemas or planning data migrations.\n- **Gate 4 (IMPLEMENT):** When writing complex SQL queries, creating indexes, or adding JSONB columns.\n\n"
  - "## Core Database Doctrine (Non-Negotiable)\n\n"
  - "### 1. Schema Design Conventions\n- **Identifiers:** Use `snake_case` strictly for tables and columns (unquoted).\n- **Primary Keys:** For reference tables (users, orders), prefer `BIGINT GENERATED ALWAYS AS IDENTITY`. Use `UUIDv7` ONLY when global uniqueness or opacity is strictly required. No `serial`.\n- **Foreign Keys:** PostgreSQL does NOT auto-index FK columns. You MUST add them manually.\n- **Nullability:** Add `NOT NULL` everywhere it’s semantically required.\n- **Timestamps:** ONLY use `TIMESTAMPTZ`. Never use `TIMESTAMP` without timezone.\n\n"
  - "### 2. Indexing Strategy\nCreate indexes for access paths you actually query:\n- B-tree: Default for equality/range queries (`=`, `<`, `>`, `ORDER BY`).\n- Partial Indexes: Excellent for hot subsets (`WHERE status = 'active'`).\n- Expression Indexes: Useful for case-insensitive searches (`LOWER(email)`).\n- GIN Indexes: Mandatory for JSONB containment (`@>`), existence (`?`), and Arrays.\n\n"
  - "### 3. JSONB Best Practices\n- Prefer `JSONB` over `JSON`. Focus on optional/variable attributes, keep core relations in regular columns.\n- Keep JSONB indexed with GIN: `CREATE INDEX ON tbl USING GIN (jsonb_col)`.\n- Use generated columns for frequently accessed JSONB scalar fields:\n  `price INT GENERATED ALWAYS AS ((jsonb_col->>'price')::INT) STORED`\n\n"
  - "### 4. Safe Schema Evolution (Migrations)\n- Always write reversible migrations (`up` and `down`).\n- Most operations can and should be wrapped in `BEGIN; ... COMMIT;`.\n- Avoid adding `NOT NULL` columns with volatile defaults (it rewrites the entire table).\n- For large tables, avoid table locks: Use `CREATE INDEX CONCURRENTLY`.\n\n"
  - "## Operator Checklist (PRE-ACT)\n- [ ] Is `snake_case` strictly used?\n- [ ] Are Foreign Keys manually indexed?\n- [ ] Is `TIMESTAMPTZ` used instead of `TIMESTAMP`?\n- [ ] Are JSONB columns supported by a GIN index?\n- [ ] Is the migration safely reversible?\n"
