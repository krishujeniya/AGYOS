# Phase 4A: Scene Templates

> The 5-scene narrative arc structure. Defines parallax layers, content rules, transition patterns, and audio-visual sync.
> Used alongside `05-code-generation-rules.md` during Phase 4.

---

## The 5-Scene Arc

Inspired by Joseph Campbell's micro-narrative and standard song structure (Intro → Verse → Chorus → Bridge → Outro).

| Scene | Name | Narrative Role | Song Parallel | Duration |
|---|---|---|---|---|
| 1 | The First Glance | Intro — set the mood | Intro | ~30s |
| 2 | The Silent Conversation | Verse — build context | Verse 1 | ~40s |
| 3 | The Climax | Chorus — emotional peak | Chorus | ~45s |
| 4 | Quiet Night | Bridge — shift perspective | Bridge | ~35s |
| 5 | Outro & CTA | Finish — resolve and close | Outro | ~20s |

**Total: 2–3 minutes of scroll content.**

---

## Parallax Layer Architecture

Each scene contains 4 layers with different scroll speeds, creating depth and emotional separation.

| Layer | CSS Class | Speed | z-index | Content | Emotional Role |
|---|---|---|---|---|---|
| Background | `.bg-layer` | 0.2x–0.3x | 1 | Abstract gradients, stars, bokeh | Shared memory, distant, nostalgic |
| Midground | `.mid-layer` | 0.5x–0.7x | 2 | Silhouettes, shapes, window lights | Current emotion, connection |
| Foreground | `.fg-layer` | 1.0x–1.5x | 3 | Floating particles, text bubbles, sparkles | Action, intention, movement |
| Text | `.text-layer` | 1.0x (pinned) | 4 | Story text, CTA | Inner voice, what he wants to say |

### Layer Rules:
- All layers are `position: absolute` within a `position: relative` section
- Background layers use CSS gradients and SVG shapes (no external images by default)
- Midground layers use CSS shapes, box-shadows, and SVG silhouettes
- Foreground layers use CSS-animated particles or GSAP-driven floating elements
- Text layers contain max 2 lines of text, centered, with entrance animations
- Apply `will-change: transform` on `.bg-layer`, `.mid-layer`, `.fg-layer`

---

## Scene-by-Scene Visual Direction

### Scene 1: The First Glance (Intro)

**Visual direction:** Dark night sky. Bokeh light circles in background. Silhouette shapes in midground. Subtle floating particles in foreground. Text fades in slowly.

**Motion direction:**
- Background: Very slow upward drift (`yPercent: -15`, speed 0.2x)
- Midground: Gentle horizontal drift (`xPercent: 5`, speed 0.5x)
- Foreground: Floating particles, random drift
- Text: Fade up from below (`y: 30 → 0`, `opacity: 0 → 1`, duration 1.5s)

**CSS implementation:**
- Background: `radial-gradient` circles of varying sizes and opacities
- Midground: Rounded rectangles with `box-shadow` for glow effect
- Foreground: Small circles with CSS `@keyframes` float animation
- Section height: `300svh` (forces slow scroll, calming entry)

**Mood:** Quiet anticipation. Like the moment before you say something important.

---

### Scene 2: The Silent Conversation (Verse)

**Visual direction:** Cozy atmosphere. Warm glowing windows in midground. Floating light particles like fireflies. Text drifts in from the side.

**Motion direction:**
- Background: Slow color temperature shift (cool → warm gradient transition)
- Midground: Glowing rectangles with pulsing `box-shadow` (window lights)
- Foreground: Floating orbs with gentle sine-wave motion
- Text: Horizontal drift entrance (`x: -50 → 0`, `opacity: 0 → 1`)

**CSS implementation:**
- Background: Linear gradient transitioning from midnight to deep warm
- Midground: Rounded rectangles with animated `box-shadow` glow
- Foreground: Circles with `transform: translateY()` using CSS animation
- Section height: `200svh`

**Mood:** Nostalgia. The memory of a quiet conversation that meant everything.

---

### Scene 3: The Climax (Chorus)

**Visual direction:** Warm gold center. The core message appears in large display font on a centered card. Radiating light particles. This is the emotional peak.

**Motion direction:**
- Background: Radial gradient expanding outward from center
- Midground: Light rays radiating from center (CSS transforms)
- Foreground: Particles accelerating outward, then settling
- Text: Scale up from small (`scale: 0.8 → 1`, `opacity: 0 → 1`), pinned for emphasis

**CSS implementation:**
- Background: Radial gradient with animated `background-size`
- Midground: Thin rectangles rotated at various angles, animating opacity
- Foreground: Particles with staggered entrance (`ScrollTrigger.batch`)
- Center card: Semi-transparent backdrop with `backdrop-filter: blur(10px)`
- Section height: `250svh` (longer dwell time for the key message)

**Mood:** Vulnerability. The moment the words are finally said.

---

### Scene 4: Quiet Night (Bridge)

**Visual direction:** Deep blue star field. Minimal motion. A moment of quiet after the climax. Stars drift slowly. Text appears gently.

**Motion direction:**
- Background: Dense star field, very slow drift (`yPercent: -5`)
- Midground: Larger star shapes at different depths, slow rotation
- Foreground: Occasional shooting star (GSAP timeline, not constant)
- Text: Simple fade in (`opacity: 0 → 1`, duration 2s, no spatial movement)

**CSS implementation:**
- Background: Dark navy with CSS dot pattern (stars)
- Midground: Larger circles with subtle `box-shadow` glow
- Foreground: A single animated line (shooting star) triggered once
- Section height: `150svh` (shorter — this is a breather)

**Mood:** Reflection. The space after a confession where both people process what was said.

---

### Scene 5: Outro & CTA (Finish)

**Visual direction:** Minimal motion. Fading to near-stillness. The CTA (replay button or gentle closing message) appears with a heartbeat-like pulse. Signature (if any) appears subtly.

**Motion direction:**
- Background: Static or nearly static, very subtle gradient shift
- Midground: Fade out most elements, leave only 1–2 soft shapes
- Foreground: Heartbeat pulse animation on CTA element (`scale: 1 → 1.05 → 1`, looping)
- Text: Final message fades in, signature fades in last

**CSS implementation:**
- Background: Solid dark with minimal gradient
- CTA button: Soft border, rounded, with pulsing `box-shadow`
- Signature: Small text, lower opacity, `letter-spacing: 0.2em`
- Section height: `100svh` (single viewport, no extended scroll)

**Mood:** Resolution. Peace. The story is told, and the rest is up to her.

---

## Scene Transition Patterns

Transitions between scenes should feel like memories surfacing, not digital page turns.

### Approved Transitions:
- **Soft color wash:** Background color smoothly transitions between scenes via ScrollTrigger scrub
- **Gaussian blur crossfade:** `backdrop-filter: blur()` animating from 0 → 20px → 0 between sections
- **Opacity crossfade:** Outgoing scene fades to 0 while incoming fades to 1
- **Vertical parallax offset:** Layers separate vertically, creating depth between scenes

### Forbidden Transitions:
- ❌ Hard cuts or instant visibility toggles
- ❌ Digital glitches or pixel effects
- ❌ Horizontal wipes or sliding panels
- ❌ Bouncing or elastic transitions between scenes
- ❌ Any transition that feels "techy" rather than emotional

---

## Audio-Visual Sync Points

If the user provides a song, map these sync points to the song's structure:

| Song Moment | Scene Transition | GSAP Event |
|---|---|---|
| Intro (first 15s) | Scene 1 entrance | Background layers begin parallax |
| First verse begins | Scene 1 → Scene 2 transition | Text entrance, color temperature shift |
| Tempo increase / drums enter | Scene 2 → Scene 3 transition | Particle acceleration, center card appears |
| Bridge / quiet section | Scene 3 → Scene 4 transition | Motion slows, stars appear |
| Final chorus / outro | Scene 4 → Scene 5 transition | Motion fades, CTA pulse begins |

**Important:** These are scroll-position-based, not time-based. The user controls the pacing. Audio sync is approximate — match the emotional arc, not exact timestamps.

---

## Content Examples by Relationship Stage

### Best Friends
| Scene | Line 1 | Line 2 |
|---|---|---|
| 1 | "Some people you meet, and you just know." | |
| 2 | "She laughs, and the whole room feels lighter." | |
| 3 | "I don't say it enough, but I'm glad you're here." | |
| 4 | "Quiet moments with you are my favorite kind." | |
| 5 | "This is for you. Replay it whenever you want." | — [signature] |

### Crush
| Scene | Line 1 | Line 2 |
|---|---|---|
| 1 | "There's something I've been meaning to say." | |
| 2 | "Every conversation with you feels like coming home." | |
| 3 | "You're the kind of person I want to know deeper." | |
| 4 | "I hope you see this the way I meant it." | |
| 5 | "I'd love to make more memories with you." | — [signature] |

### Early Dating
| Scene | Line 1 | Line 2 |
|---|---|---|
| 1 | "I keep finding new reasons to smile because of you." | |
| 2 | "The way you see the world makes me see it differently." | |
| 3 | "Every day with you feels like a story worth telling." | |
| 4 | "I didn't know I was missing this until I found you." | |
| 5 | "Here's to every chapter ahead." | — [signature] |

### Committed
| Scene | Line 1 | Line 2 |
|---|---|---|
| 1 | "You already know how I feel." | "But I wanted to build it anyway." |
| 2 | "You turned ordinary days into my favorite ones." | |
| 3 | "You're my favorite chapter in every story." | |
| 4 | "Even the quiet is better with you." | |
| 5 | "Always yours." | — [signature] |

---

## Breathing Room

Between scenes, maintain "emotional punctuation" — empty scroll space where nothing happens except gentle background motion. This lets the user process what they just read.

- **Minimum:** 50vh of empty scroll between text reveals within a scene
- **Between scenes:** The transition itself acts as breathing room (color wash duration)
- **Scene 3 → Scene 4:** Extra breathing room (100vh) — the user needs to sit with the climax before the bridge
