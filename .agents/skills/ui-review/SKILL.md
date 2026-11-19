---
name: ui-review
description: "Review UI code for StyleSeed design-system compliance, accessibility, mobile ergonomics, spacing discipline, and implementation quality."
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: "Krish Ujeniya"
tags: [ui, review, design-system, accessibility, styleseed]
tools: [claude, cursor, codex, gemini]
prompt-source: prompt.toon
---
skill: "ui-review"
sections[14]:
  - "\n"
  - "# UI Review\n\n"
  - "## Overview\n\nPart of [StyleSeed](https://github.com/bitjaru/styleseed), this skill audits UI code against the Toss seed's conventions instead of reviewing it as generic frontend work. It focuses on design-token discipline, component ergonomics, accessibility, mobile readiness, typography, and spacing consistency.\n\n"
  - "## When to Use\n- Use when a component or page should follow the StyleSeed Toss design language\n- Use when reviewing a UI-heavy PR for consistency and design-system violations\n- Use when the output looks \"mostly fine\" but feels off in subtle ways\n- Use when you need a structured review with concrete fixes\n\n"
  - "## Review Checklist\n\n"
  - "### Design Tokens\n\n- no hardcoded hex colors when semantic tokens exist\n- no improvised shadow values when tokenized shadows exist\n- no arbitrary radius choices outside the system scale\n- no random spacing values that break the seed rhythm\n\n"
  - "### Component Conventions\n\n- uses the project's class merge helper\n- supports `className` extension when appropriate\n- uses the agreed typing pattern\n- avoids wrapper components that only forward one class string\n- reuses existing primitives before inventing new ones\n\n"
  - "### Accessibility\n\n- touch targets large enough for mobile\n- visible keyboard focus states\n- labels and `aria-*` attributes where needed\n- adequate color contrast\n- reduced-motion respect for animation\n\n"
  - "### Mobile UX\n\n- no horizontal overflow\n- safe-area handling where relevant\n- readable text sizes\n- thumb-friendly interaction spacing\n- bottom nav or sticky actions do not obscure content\n\n"
  - "### Typography and Spacing\n\n- uses the system type hierarchy\n- display and headings are not overly loose\n- body text remains readable\n- spacing follows the seed grid instead of arbitrary values\n\n"
  - "## Output Format\n\nReturn:\n1. A verdict: Pass, Needs Improvement, or Fail\n2. A prioritized list of issues with file and line references when available\n3. Concrete fixes for each issue\n4. Any open questions where the design intent is ambiguous\n\n"
  - "## Best Practices\n\n- Review against the seed, not against personal taste\n- Separate stylistic drift from real usability or accessibility bugs\n- Prefer actionable diffs over abstract criticism\n- Call out duplication when an existing component already solves the problem\n\n"
  - "## Additional Resources\n\n- [StyleSeed repository](https://github.com/bitjaru/styleseed)\n- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-review/SKILL.md)\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
