---
name: tech-debt-cleanup
description: "Compatibility ID for the technical-debt guide in codebase-tech-debt. Use when asked to find, assess, or prioritize technical debt."
risk: unknown
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "tech-debt-cleanup"
sections[2]:
  - "# Technical debt compatibility ID\n\nCompatibility ID for technical-debt requests. Use the canonical [codebase-tech-debt runbook](../codebase-tech-debt/SKILL.md) and its linked full reference for inventory, impact assessment, and prioritization.\n\n"
  - "## Workflow\n\n1. Confirm the request fits this skill and identify the required inputs and output constraints.\n2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).\n3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.\n4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.\n5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.\n6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.\n"
