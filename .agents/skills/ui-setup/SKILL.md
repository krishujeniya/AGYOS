---
name: ui-setup
description: "Interactive StyleSeed setup wizard for choosing app type, brand color, visual style, typography, and the first screen scaffold."
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: "Krish Ujeniya"
tags: [ui, design-system, setup, frontend, styleseed]
tools: [claude, cursor, codex, gemini]
prompt-source: prompt.toon
---
skill: "ui-setup"
sections[15]:
  - "\n"
  - "# UI Setup\n\n"
  - "## Overview\n\nPart of [StyleSeed](https://github.com/bitjaru/styleseed), this setup wizard turns a raw project into a design-system-guided workspace. It collects the minimum brand and product context needed to configure tokens, pick a visual direction, and generate an initial page without drifting into generic UI.\n\n"
  - "## When to Use\n- Use when you are starting a new app with the StyleSeed Toss seed\n- Use when you copied the seed into an existing project and need to personalize it\n- Use when you want the AI to ask one design decision at a time instead of guessing\n- Use when you need a first page scaffold after selecting colors, font, and app type\n\n"
  - "## How It Works\n\n"
  - "### Step 1: Ask One Question at a Time\n\nDo not front-load the full questionnaire. Ask a single question, wait for the answer, store it, then continue.\n\n"
  - "### Step 2: Capture the App Type\n\nIdentify the product shape before touching tokens or layout recipes.\n\nSuggested buckets:\n- SaaS dashboard\n- E-commerce\n- Fintech\n- Social or content\n- Productivity or internal tool\n- Other with a short freeform description\n\nUse the answer to choose the page composition pattern and the type of first screen to scaffold.\n\n"
  - "### Step 3: Choose the Brand Color\n\nOffer a few safe defaults plus a custom hex option. Once selected:\n- update the light theme brand token\n- update the dark theme brand token with a lighter accessible variant\n- keep all other colors semantic rather than hardcoding the brand everywhere\n\nIf the project uses the StyleSeed Toss seed, the main target is `css/theme.css`.\n\n"
  - "### Step 4: Offer an Optional Visual Reference\n\nAsk whether the user wants to borrow the feel of an established brand or design language. Good examples include Stripe, Linear, Vercel, Notion, Spotify, Supabase, and Airbnb.\n\nUse the reference to influence density, tone, and composition, not to clone assets or trademarks.\n\n"
  - "### Step 5: Pick Typography\n\nConfirm the font direction:\n- keep the default stack\n- swap to a preferred font if already installed or available\n- preserve hierarchy rules for display, heading, body, and caption text\n\nIf the seed is present, update the font-related files rather than scattering overrides across components.\n\n"
  - "### Step 6: Generate the First Screen\n\nAsk for:\n- app name\n- first page or screen name\n- a one-sentence purpose for that page\n\nThen scaffold the page using the seed's page shell, top bar, navigation, spacing scale, and card structure.\n\n"
  - "## Output\n\nReturn:\n1. The captured setup decisions\n2. The files or tokens updated\n3. The first page or scaffold created\n4. Any follow-up recommendations for components, patterns, accessibility, or copy\n\n"
  - "## Best Practices\n\n- Keep the interaction conversational, but deterministic\n- Make brand color changes through tokens, not component-by-component edits\n- Use an inspiration brand as a reference, not as a permission slip to copy\n- Prefer semantic tokens and reusable patterns over page-specific CSS\n\n"
  - "## Additional Resources\n\n- [StyleSeed repository](https://github.com/bitjaru/styleseed)\n- [StyleSeed Toss seed](https://github.com/bitjaru/styleseed/tree/main/seeds/toss)\n- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-setup/SKILL.md)\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
