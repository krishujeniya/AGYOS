---
name: seo-dataforseo
description: "Use DataForSEO for live SERPs, keyword metrics, backlinks, competitor analysis, on-page checks, and AI visibility data. Trigger when the user needs real SEO data rather than static guidance."
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[command] [query]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
prompt-source: prompt.toon
---
skill: "seo-dataforseo"
sections[2]:
  - "# DataForSEO: Live SEO Data (Extension)\n\nUse DataForSEO for live SERPs, keyword metrics, backlinks, competitor analysis, on-page checks, and AI visibility data. Trigger when the user needs real SEO data rather than static guidance.\n\n"
  - "## Workflow\n\n1. Confirm the request fits this skill and identify the required inputs and output constraints.\n2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).\n3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.\n4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.\n5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.\n6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.\n"
