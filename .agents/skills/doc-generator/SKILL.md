---
name: doc-generator
description: "Generate or update API documentation, architecture diagrams, user guides, and technical references from an inspected codebase. Use when creating maintainable project documentation."
risk: safe
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "doc-generator"
sections[11]:
  - "\n"
  - "# Automated Documentation Generation\n\nGenerate or update API documentation, architecture diagrams, user guides, and technical references from an inspected codebase. Use when creating maintainable project documentation.\n\n"
  - "## Use this skill when\n\n- Generating API, architecture, or user documentation from code\n- Building documentation pipelines or automation\n- Standardizing docs across a repository\n\n"
  - "## Do not use this skill when\n\n- The project has no codebase or source of truth\n- You only need ad-hoc explanations\n- You cannot access code or requirements\n\n"
  - "## Context\nThe user needs automated documentation generation that extracts information from code, creates clear explanations, and maintains consistency across documentation types. Focus on creating living documentation that stays synchronized with code.\n\n"
  - "## Requirements\n$ARGUMENTS\n\n"
  - "## Instructions\n\n- Identify required doc types and target audiences.\n- Extract information from code, configs, and comments.\n- Generate docs with consistent terminology and structure.\n- Add automation (linting, CI) and validate accuracy.\n- If detailed examples are required, open `resources/implementation-playbook.md`.\n\n"
  - "## Safety\n\n- Avoid exposing secrets, internal URLs, or sensitive data in docs.\n\n"
  - "## Output Format\n\n- Documentation plan and artifacts to generate\n- File paths and tooling configuration\n- Assumptions, gaps, and follow-up tasks\n\n"
  - "## Resources\n\n- `resources/implementation-playbook.md` for detailed examples and templates.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
