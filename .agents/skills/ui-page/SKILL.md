---
name: ui-page
description: "Scaffold a new mobile-first page using StyleSeed Toss layout patterns, section rhythm, and existing shell components."
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: "Krish Ujeniya"
tags: [ui, page-design, mobile, layout, styleseed]
tools: [claude, cursor, codex, gemini]
prompt-source: prompt.toon
---
skill: "ui-page"
sections[15]:
  - "\n"
  - "# UI Page\n\n"
  - "## Overview\n\nPart of [StyleSeed](https://github.com/bitjaru/styleseed), this skill scaffolds a complete page or screen using the Toss seed's mobile-first composition rules. It keeps page structure consistent by building on the existing shell, top bar, bottom navigation, and card rhythm instead of producing disconnected sections.\n\n"
  - "## When to Use\n- Use when you need a new page in a Toss-seed app\n- Use when you want a consistent page shell, spacing, and navigation structure\n- Use when you are adding a new product flow and need a solid starting layout\n- Use when you want to stay mobile-first even if the project later expands to larger breakpoints\n\n"
  - "## How It Works\n\n"
  - "### Step 1: Inspect the Existing Shell\n\nRead the current page scaffolding patterns first, especially:\n- page shell\n- top bar\n- bottom navigation\n- representative pages using the same route family\n\n"
  - "### Step 2: Define the Page Purpose\n\nClarify:\n- the page name\n- the primary user question the screen answers\n- the top one or two actions the user should take\n\nEvery screen should have one dominant purpose.\n\n"
  - "### Step 3: Use the Information Pyramid\n\nLay out the page from highest importance to lowest:\n1. Hero or top summary\n2. KPI or key actions\n3. detail cards or supporting modules\n4. lists, history, or secondary content\n\nAvoid repeating the same section type mechanically from top to bottom.\n\n"
  - "### Step 4: Apply the Toss Layout Rules\n\nDefault layout choices:\n- mobile viewport width around `max-w-[430px]`\n- page background on `bg-background`\n- horizontal padding around `px-6`\n- section rhythm with `space-y-6`\n- generous bottom padding if a bottom nav is present\n- cards using semantic surface tokens, rounded corners, and light shadows\n\n"
  - "### Step 5: Compose Instead of Rebuilding\n\nUse existing `ui/` and `patterns/` components wherever possible. New pages should primarily orchestrate existing building blocks, not recreate them.\n\n"
  - "### Step 6: Account for Real Device Constraints\n\n- handle safe-area insets\n- avoid horizontal overflow\n- keep interactive clusters thumb-friendly\n- ensure long content scrolls cleanly without clipping the bottom navigation\n\n"
  - "## Output\n\nReturn:\n1. The page scaffold\n2. The chosen section structure\n3. Reused components and any newly required components\n4. Empty, loading, and error states that the page will need next\n\n"
  - "## Best Practices\n\n- Keep the first version structurally correct before adding decoration\n- Use one strong hero instead of multiple competing highlights\n- Preserve navigation consistency across sibling screens\n- Prefer reusable section components when the page will likely repeat\n\n"
  - "## Additional Resources\n\n- [StyleSeed repository](https://github.com/bitjaru/styleseed)\n- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-page/SKILL.md)\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
