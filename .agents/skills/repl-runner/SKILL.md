---
name: repl-runner
description: Operate and extend NanoClaw, ECC's zero-dependency session-aware REPL, with persistent markdown-backed sessions and slash commands for model switching, skill loading, session branching, cross-session search, history compaction, and export. Use when running or extending scripts/claw.js, or when resuming, branching, compacting, searching, or exporting a NanoClaw session.
metadata:
  origin: ECC
prompt-source: prompt.toon
---
skill: "repl-runner"
sections[5]:
  - "\n"
  - "# NanoClaw REPL\n\nUse this skill when running or extending `scripts/claw.js`.\n\n"
  - "## Capabilities\n\n- persistent markdown-backed sessions\n- model switching with `/model`\n- dynamic skill loading with `/load`\n- session branching with `/branch`\n- cross-session search with `/search`\n- history compaction with `/compact`\n- export to md/json/txt with `/export`\n- session metrics with `/metrics`\n\n"
  - "## Operating Guidance\n\n1. Keep sessions task-focused.\n2. Branch before high-risk changes.\n3. Compact after major milestones.\n4. Export before sharing or archival.\n\n"
  - "## Extension Rules\n\n- keep zero external runtime dependencies\n- preserve markdown-as-database compatibility\n- keep command handlers deterministic and local\n"
