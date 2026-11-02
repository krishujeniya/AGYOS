---
name: ScrollHeart
description: |
  Build her a story she can scroll through. ScrollHeart is a warm, gentle AI skill
  that helps a boy create a romantic, scroll-driven storytelling website for a girl
  he cares about. Generates static HTML/CSS/JS sites with GSAP ScrollTrigger,
  parallax layers, and optional background music — deployable free on GitHub Pages.
  Trigger on: romantic website, scroll story, gift for her, love page, surprise
  website, digital love letter, ScrollHeart, scrollheart.
version: 1.0.0
author: ScrollHeart
---

# ScrollHeart

> Build her a story she can scroll through.

This is the Antigravity IDE entry point. The full skill system lives at the workspace root.

**First**, read the complete skill workflow:

```
read_file("SKILL.md")
```

The root `SKILL.md` contains:
- Brand voice definition ("The Calm Bestie")
- The 5-phase workflow (Interview → Safety → Design Brief → Code → Post-Build)
- Hard rules (tech stack, safety, accessibility)
- 20-point slop-test gate

**All reference files** are at the workspace root:

| Phase | File to Load |
|---|---|
| Interview | `references/01-interview-flow.md` |
| Safety Check | `references/02-safety-checklist.md` |
| Design Brief | `references/03-design-brief-generator.md` |
| Code Generation | `references/04-scene-templates.md` + `references/05-code-generation-rules.md` |
| Post-Build | `references/06-deployment-guide.md` + `references/07-post-build-guide.md` |

**Resource files** for palette/font/song selection:

| Resource | File to Load |
|---|---|
| Color Palettes | `resources/color-palettes.json` |
| Font Pairings | `resources/font-pairings.json` |
| Song Suggestions | `resources/song-suggestions.json` |

**Example output** for quality reference:

| File | Purpose |
|---|---|
| `examples/good-output/index.html` | Reference HTML structure |
| `examples/good-output/css/style.css` | Reference CSS with design tokens |
| `examples/good-output/js/main.js` | Reference GSAP + audio controller |

## Quick Start

When triggered, begin with Phase 1 (Interview). Always start warm:

> "Hey! So there's someone special you want to make something for? I'm here to help you build her a little story she can scroll through. No pressure — we can take this one step at a time. Ready?"

Read `SKILL.md` at the workspace root for the full instructions.
