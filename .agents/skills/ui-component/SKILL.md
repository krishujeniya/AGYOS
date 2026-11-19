---
name: ui-component
description: "Generate a new UI component that follows StyleSeed Toss conventions for structure, tokens, accessibility, and component ergonomics."
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: "Krish Ujeniya"
tags: [ui, components, design-system, frontend, styleseed]
tools: [claude, cursor, codex, gemini]
prompt-source: prompt.toon
---
skill: "ui-component"
sections[15]:
  - "\n"
  - "# UI Component\n\n"
  - "## Overview\n\nPart of [StyleSeed](https://github.com/bitjaru/styleseed), this skill generates components that respect the Toss seed's design language instead of improvising ad hoc markup and styling. It emphasizes semantic tokens, predictable typing, reusable variants, and mobile-friendly accessibility defaults.\n\n"
  - "## When to Use\n- Use when you need a new UI primitive or composed component inside a StyleSeed-based project\n- Use when you want a component to match the existing Toss seed conventions\n- Use when a component should be reusable, typed, and design-token driven\n- Use when the AI might otherwise invent spacing, colors, or interaction patterns\n\n"
  - "## How It Works\n\n"
  - "### Step 1: Read the Local Design Context\n\nBefore generating code, inspect the seed's source of truth:\n- `CLAUDE.md` for conventions\n- `css/theme.css` for semantic tokens\n- at least one representative component from `components/ui/`\n\nIf the user already has a better local example, follow the local codebase over a generic template.\n\n"
  - "### Step 2: Choose the Correct Home\n\nPlace the output where it belongs:\n- `src/components/ui/` for primitives and low-level building blocks\n- `src/components/patterns/` for composed sections or multi-part patterns\n\nDo not create a new primitive if an existing one can be extended safely.\n\n"
  - "### Step 3: Follow the Structural Rules\n\nUse these defaults unless the host project strongly disagrees:\n- function declaration instead of a `const` component\n- `React.ComponentProps<>` or equivalent native prop typing\n- `className` passthrough support\n- `cn()` or the project's standard class merger\n- `data-slot` for component identification\n- CVA or equivalent only when variants are genuinely needed\n\n"
  - "### Step 4: Use Semantic Tokens Only\n\nDo not hardcode visual values if the design system has a token for them.\n\nPreferred examples:\n- `bg-card`\n- `text-foreground`\n- `text-muted-foreground`\n- `border-border`\n- `shadow-[var(--shadow-card)]`\n\n"
  - "### Step 5: Preserve StyleSeed Typography and Spacing\n\n- Use the scale already defined by the seed\n- Prefer multiples of 6px\n- Use logical spacing utilities where supported\n- Keep display and heading text tight, body text readable, captions restrained\n\n"
  - "### Step 6: Bake in Accessibility\n\n- Touch targets should be at least 44x44px for interactive elements\n- Keyboard focus must be visible\n- Pass through `aria-*` attributes where appropriate\n- Respect reduced-motion preferences for nonessential motion\n\n"
  - "## Output\n\nProvide:\n1. The generated component\n2. The target path\n3. Any required imports or dependencies\n4. Notes on variants, tokens, or follow-up integration work\n\n"
  - "## Best Practices\n\n- Compose from existing primitives before inventing new ones\n- Keep the component API small and predictable\n- Prefer semantic layout classes over arbitrary values\n- Export named components unless the host project uses another standard consistently\n\n"
  - "## Additional Resources\n\n- [StyleSeed repository](https://github.com/bitjaru/styleseed)\n- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-component/SKILL.md)\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
