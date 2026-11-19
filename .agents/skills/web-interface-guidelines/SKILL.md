---
name: web-interface-guidelines
description: "Master of Web Interface Guidelines and high-craft Frontend Aesthetics. Enforces Vercel UI rules (Accessibility, Focus, Forms) and uncompromising, bold design directions (no generic AI aesthetics). Use when building, reviewing, or styling any React/Next.js/HTML UI."
category: frontend
risk: safe
tags: "[frontend, design, ui, ux, guidelines, aesthetics, vercel, a11y, styling]"
version: "1.0.0"
prompt-source: prompt.toon
---
skill: "web-interface-guidelines"
sections[12]:
  - "\n"
  - "# Web Interface Guidelines & Aesthetics\n\n"
  - "## Purpose\nThis skill ensures that all UI code generated for `project_game_pulse` strictly follows the highest standards of interaction design (adapted from Vercel Labs) AND possesses a bold, differentiated aesthetic character (avoiding \"AI slop\").\n\n"
  - "## When to Use\n- **Gate 3 (PLAN):** When conceptualizing the look and feel of a new page or component.\n- **Gate 4 (IMPLEMENT):** When writing interactive React/Next.js components, CSS, and animations.\n- **Gate 5 (VERIFY):** When auditing a UI for accessibility, usability, and design quality.\n\n---\n\n"
  - "## Part 1: High-Craft Aesthetics (The \"No Generic AI\" Mandate)\n\nBefore coding, commit to an intentional aesthetic direction:\n- **Bold Direction:** Choose a defined look (Minimalist, Brutalist, Retro, Luxury, etc.). Do not blend into a generic middle-ground.\n- **Typography:** Avoid generic default fonts (Arial, standard Inter) as the sole identity. Pair a characterful display font with a highly legible body font.\n- **Color & Theme:** Define strong, cohesive CSS palettes. Avoid default \"purple-gradient-on-white\" cliches unless strictly aligned with the brand.\n- **Layout & Space:** Embrace asymmetry, purposeful white space, or controlled density. Avoid predictable cookie-cutter \"card\" layouts if the context allows for more creative framing.\n- **Details:** Use textures (noise/grain), subtle borders, geometric patterns, or layered transparencies to build depth.\n\n---\n\n"
  - "## Part 2: Strict UI/UX Rules (Vercel Guidelines)\n\nThe code MUST comply with the following interaction and technical standards:\n\n"
  - "### 1. Interactive States\n- **Focus:** Every interactive element MUST have visible focus (`focus-visible:ring-*`). Never `outline-none` without replacement. Prefer `:focus-visible` over `:focus`.\n- **Hover:** Buttons/links need clear visual feedback (`hover:`).\n- **Disabled:** Provide clear disabled states with reduced opacity/cursor changes.\n\n"
  - "### 2. Forms & Inputs\n- **Autocomplete:** Inputs need `autocomplete` and meaningful `name` attributes.\n- **Types:** Use exact input types (`email`, `tel`, `url`, `number`) and `inputmode`.\n- **Labels:** ALWAYS use `htmlFor` or wrap the input. No unlabelled inputs.\n- **UX:** Never block paste (`onPaste` + `preventDefault`).\n- **Feedback:** Submit buttons stay enabled during requests but show a spinner. Errors must appear inline.\n\n"
  - "### 3. Motion & Animation\n- **Accessibility:** Honor `prefers-reduced-motion`.\n- **Performance:** ONLY animate `transform` and `opacity` for compositor-friendly animations.\n- **Explicit Transitions:** NEVER use `transition: all`. List properties explicitly.\n\n"
  - "### 4. Typography Content Handling\n- **Microcopy:** Use actual ellipses `…` not `...`. Use curly quotes `\"\"`.\n- **Data Rendering:** Use `font-variant-numeric: tabular-nums` for data columns.\n- **Overflow:** Handle long content safely (`truncate`, `line-clamp`, `break-words`, `min-w-0` on flex children).\n\n"
  - "### 5. Advanced Frontend Mechanisms\n- **Links vs Buttons:** Links use `<a>` (for Cmd+Click support). Actions use `<button>`. Never put `onClick` navigation on an anchor without proper routing techniques.\n- **Images:** Always set explicit `width` and `height` to prevent Cumulative Layout Shift (CLS). Use `loading=\"lazy\"` for below-fold.\n- **Hydration:** Avoid mismatch errors. Use `value` with `onChange` or `defaultValue` for uncontrolled inputs.\n- **System Theme:** Support dark mode correctly (`color-scheme: dark`).\n\n"
  - "## Operator Checklist (PRE-ACT)\n- [ ] Is the aesthetic direction bold and intentionally non-generic?\n- [ ] Are focus states (`focus-visible`) defined for all new interactive elements?\n- [ ] Are animations performant (transform/opacity only) and respectful of reduced motion?\n- [ ] Do all images have explicit dimensions?\n- [ ] Are form labels and appropriate input types used?\n"
