---
name: search-engine-optimization
description: Inspect search visibility, metadata, crawlability, and eligible structured data using the rendered page and primary evidence.
prompt-source: prompt.toon
---
skill: "search-engine-optimization"
sections[3]:
  - "@context\": \"https://schema.org\",\n  \"@type\": \"Article\",\n  \"headline\": \"Page Title Here\",\n  \"author\": {\n    \"@type\": \"Person\",\n    \"name\": \"Author Name\"\n  },\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Brand Name\"\n  }\n}\n```\n\n### Audit output shape\n\n```text\n[HIGH] Duplicate title tags on product pages\nLocation: src/routes/products/[slug].tsx\nIssue: Dynamic titles collapse to the same default string, which weakens relevance and creates duplicate signals.\nFix: Generate a unique title per product using the product name and primary category.\n```\n\n"
  - "## Anti-Patterns\n\n| Anti-pattern | Fix |\n| --- | --- |\n| keyword stuffing | write for users first |\n| thin near-duplicate pages | consolidate or differentiate them |\n| schema for content that is not actually present | match schema to reality |\n| content advice without checking the actual page | read the real page first |\n| generic “improve SEO” outputs | tie every recommendation to a page or asset |\n\n"
  - "## Related Skills\n\n- `seo-specialist`\n- `frontend-patterns`\n- `brand-voice`\n- `market-research`\n"
