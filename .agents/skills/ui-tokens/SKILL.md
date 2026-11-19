---
name: ui-tokens
description: "List, add, and update StyleSeed design tokens while keeping JSON sources, CSS variables, and dark-mode values in sync."
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: "Krish Ujeniya"
tags: [ui, tokens, design-system, theming, styleseed]
tools: [claude, cursor, codex, gemini]
prompt-source: prompt.toon
---
skill: "ui-tokens"
sections[12]:
  - "\n"
  - "# UI Tokens\n\n"
  - "## Overview\n\nPart of [StyleSeed](https://github.com/bitjaru/styleseed), this skill manages design tokens without letting the source-of-truth files drift apart. It is meant for teams using the Toss seed's JSON token files and CSS implementation together.\n\n"
  - "## When to Use\n- Use when you need to inspect the current token set\n- Use when you want to add a new color, shadow, radius, spacing, or typography token\n- Use when you need to update a token and propagate the change safely\n- Use when the project has both JSON token files and CSS variables that must stay aligned\n\n"
  - "## How It Works\n\n"
  - "### Supported Actions\n\n- `list`: show the current tokens in a human-readable form\n- `add`: introduce a new token and wire it through the implementation\n- `update`: change an existing token value and audit the downstream usage\n\n"
  - "### Typical Source-of-Truth Split\n\nFor the Toss seed:\n- JSON under `tokens/`\n- CSS variables and theme wiring under `css/theme.css`\n- typography support in the font and base CSS files\n\n"
  - "### Rules\n\n- keep JSON and CSS in sync\n- prefer semantic names over descriptive names\n- provide dark-mode support where relevant\n- update the token implementation, not just the source manifest\n- check for direct component usage that might now be stale\n\n"
  - "## Output\n\nReturn:\n1. The requested token inventory or change summary\n2. Every file touched\n3. Any affected components or utilities that should be reviewed\n4. Follow-up actions if the new token requires broader adoption\n\n"
  - "## Best Practices\n\n- Add semantic intent, not one-off brand shades\n- Avoid token sprawl by extending existing scales first\n- Keep naming consistent with the rest of the system\n- Review contrast and accessibility when introducing new colors\n\n"
  - "## Additional Resources\n\n- [StyleSeed repository](https://github.com/bitjaru/styleseed)\n- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-tokens/SKILL.md)\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
