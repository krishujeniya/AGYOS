---
name: interactive-scroll-storySKILL.md")
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
