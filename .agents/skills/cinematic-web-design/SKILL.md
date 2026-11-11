---
name: cinematic-web-design
description: >-
  Build world-class, cinematic, dark editorial one-page websites and high-end frontend experiences
  derived from the Webbzer 10 template architecture, Google Flow 188 design principles, 93-effect
  motion catalog, procedural Canvas 2D physics engines, and strict anti-slop copy law. Delivers
  self-contained, single-file zero-dependency index.html implementations with WCAG 2.2 AA accessibility.
metadata:
  version: 1.0.0
  tier: 1
  domain: ui_ux
  origin: Webbzer / Google Flow / Anti-Slop
---

# Cinematic Web Design Engineering Runbook

Guides the creation of cinematic, dark editorial one-page websites and interactive frontend experiences at the quality level of `flow.google` and `antigravity.google`. Synthesizes the 10 Webbzer engine specifications, the Google Flow design-principles audit (188 principles), the 93-effect motion catalog, and five anti-slop copy doctrines.

For exhaustive specifications, inspect the reference documents:
- [FLUX Master Specification](references/FLUX_MASTER_PROMPT.md)
- [93-Effect Motion & Interaction Catalog](references/MOTION_EFFECTS_CATALOG.md)
- [Anti-Slop Engineering & Writing Law](references/ANTI_SLOP_LAW.md)
- [Procedural Canvas 2D Physics & Hero Engines](references/PROCEDURAL_CANVAS_ENGINES.md)

---

## 0. Output Contract & Non-Negotiable Invariants

1. **Single-File Zero-Dependency Delivery**: Deliver exactly one self-contained `index.html` file. All styles reside in one `<style>`, all logic in one `<script>` (module format permitted). Zero external requests: no CDNs, external webfonts, raster images, remote videos, or third-party analytics.
2. **Deterministic Inline Visuals**: Every visual asset is rendered via CSS, inline SVG, or procedural Canvas 2D. Typography relies exclusively on intentional system font stacks:
   - Display Serif: `Iowan Old Style, Palatino Linotype, Palatino, Georgia, 'Times New Roman', serif`
   - UI Sans: `system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif`
   - Code Mono: `ui-monospace, 'SF Mono', Menlo, Monaco, Consolas, monospace`
3. **No Placeholders or Truncation**: Code must be 100% complete. Never output `TODO`, placeholders, truncated sections, or summarize remaining implementation in prose.
4. **Honest Fictional Framing**: All product claims and case studies are explicitly labeled as `EXAMPLE` or `ILLUSTRATIVE`. Never fabricate testimonials, metrics, certifications, or user counts.
5. **Accessible Progressive Enhancement**: Content must remain fully legible with JavaScript disabled. All hidden-reveal states are gated behind an `html.has-js` class injected by script at runtime.
6. **Strict Anti-Slop Compliance**: Every string in the file (copy, tooltips, dialogs, technical summaries) strictly adheres to the Anti-Slop Law (Section 5).

---

## 1. Design Tokens & Visual Grammar

Embed this token block in `:root` and construct all interface styles strictly from these tokens:

```css
:root {
  /* Surfaces & Color */
  --bg: #0a1011; --surface: #101919; --surface-2: #152120; --paper: #eff3eb; --muted: #a4b0ae;
  --accent: #cee5d3; --accent-dim: rgba(206, 229, 211, 0.35); --line: rgba(225, 239, 232, 0.15);
  --scrim: rgba(10, 16, 17, 0.72); --atmo-1: #29453d; --atmo-2: #263b33;
  --ink-inverse: #19251e; --muted-inverse: #596b60; --accent-inverse: #63796a;

  /* Typography Scales */
  --font-display: 'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, 'Times New Roman', serif;
  --font-ui: system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
  --text-hero: clamp(64px, 8vw, 132px); --text-h2: clamp(44px, 5.2vw, 82px);
  --text-h3: clamp(21px, 2vw, 25px); --text-body: 15px; --text-small: 13px;
  --text-nav: 12px; --text-label: 10px; --text-legal: 12px;

  /* Spacing & Geometry */
  --space-1: 4px; --space-2: 8px; --space-3: 16px; --space-4: 24px; --space-5: 36px;
  --space-6: 48px; --space-7: 60px; --space-8: 80px; --space-9: 88px; --space-10: 120px; --space-11: 180px;
  --r-sm: 4px; --r-md: 8px; --r-lg: 16px; --r-xl: 24px; --r-2xl: 36px; --r-pill: 9999px;
  --pad: clamp(24px, 5.5vw, 100px); --content-max: 1360px;

  /* Motion & Dynamics */
  --ease-primary: cubic-bezier(0.165, 0.84, 0.44, 1); --ease-expo: cubic-bezier(0.19, 1, 0.22, 1);
  --ease-playful: cubic-bezier(0.34, 1.85, 0.64, 1); --ease-reveal: cubic-bezier(0.22, 1, 0.36, 1);
  --dur-fast: 150ms; --dur-base: 250ms; --dur-slow: 450ms; --dur-scene: 700ms;
  --lift-hover: -2px; --lift-card: -4px; --press-scale: 0.98;

  /* Elevation & Focus */
  --z-header: 50; --z-dropdown: 60; --z-overlay: 80; --z-toast: 90;
  --focus-ring: 2px solid var(--accent); --focus-offset: 3px;
}
```

**Contrast Invariant**: Body text must maintain >= 4.5:1 contrast against background; display headlines must maintain >= 3:1 contrast, including over scrims and canvas overlays. Contrast overrides decorative opacity.

---

## 2. 10-Act Page Anatomy & Density Rhythm

Structure the document in this exact 10-act sequence:

| Act | Element (`id` / selector) | Pattern & Execution |
|---|---|---|
| **0** | **Banner** (`.banner`) | Slim disclaimer line: "Flux is a design concept — see what that means →" linking to `#faq`. |
| **1** | **Header** (`.site-header`) | Sticky 86–100px header, glass blur on scroll (`S12`), brand SVG wavy lines, navigation links with scrollspy indicator (`S11`), demo button, mobile drawer menu (`O1`). |
| **2** | **Hero** (`#top`) | 200svh scroll container with sticky 100svh inner viewport. Right-weighted procedural Canvas 2D particle river. Oversized display serif headline, subcopy, and primary CTA visible without scroll. Two-phase scroll journey swapping to "Less friction. More flow." with counter bar (`01—02`). |
| **3** | **Manifesto** (`#manifesto`) | Editorial pause: eyebrow label, centered display thesis, floating chips drifting on sine trajectory (`A5`), framed SVG orbit arcs (`R15`). |
| **4** | **Platform** (`#platform`) | Bento grid: wide CONNECT card (constellation art), UNDERSTAND card (decision rings), full-width MOVE card (momentum arcs) with pointer-tracked magnetic borders (`P4`). |
| **5** | **Workflow** (`#workflow`) | Segmented tabs (**Research / Operations / Creative**). Tab panel: input stack -> bridge -> output card. All content marked `EXAMPLE`. Keyboard navigation via Arrow keys with roving `tabindex`. Stable reserved height (`CLS = 0`). |
| **6** | **Showcase** (`#showcase`) | Scroll-snap rail carousel with 4 illustrative output frames (`C1`–`C5`). Category filter chips with FLIP animation (`R5`). Blur-up card reveal (`M5`). Edge-fade gradient masks (`C3`). |
| **7** | **Principles** (`#principles`) | Inverted light chapter: paper background (`#eff3eb`), dark ink text (`#19251e`), three numbered intentional principles. |
| **8** | **Plans** (`#plans`) | 3 aligned concept plan cards (Concept $0 / Studio / Team). Explicitly labeled `EXAMPLE PLAN — NOT REAL PRICING`. Staggered entrance (`C12`). |
| **9** | **FAQ** (`#faq`) | Accordion (`C13`) using native buttons, `aria-expanded`, and CSS `grid-template-rows: 0fr -> 1fr` transitions. First item explains the fictional concept. |
| **10** | **Contact & Footer** (`#contact`) | Scroll-reactive concentric SVG arcs (`S7`, `S8`, `R15`), "Find your forward" headline. Footer includes SVG copy tool (`R16`), Motion On/Off toggle (`R11`), auto-updated year, and `#faq` link. |
| **—** | **Demo Dialog** (`#demo-dialog`) | Native `<dialog>` modal (`O3`). Backdrop `blur(24px)` with dark scrim. Staged status simulation (`T5`) with Replay control (`R14`). Full focus management: trapped within dialog, Escape closes, focus restored to opener. |

**Density Rhythm**: Cinematic (Hero) -> Spare (Manifesto) -> Feature-Rich (Platform/Workflow) -> Editorial (Principles) -> Utilitarian (Plans/FAQ) -> Spare (Contact).

---

## 3. Signature Procedural Hero Engines (Canvas 2D)

### The Folded Particle River Engine
- **Field**: Canvas positioned absolute inside hero (`z-index: -2`), DPR capped at 1.75 desktop / 1.5 mobile.
- **Layers**:
  1. *Static Dust*: 650 background dots pre-rendered once to an offscreen canvas (opacity ~0.38).
  2. *Dynamic Particles*: Exactly 88 desktop / 44 mobile. Mix of shapes (circles, capsules, rounded squares).
- **Ribbon Math**: Particles gravitate to folded parametric ribbon:
  `x = cx + Math.sin(u * 7.0 - 0.8) * spread + across * width * Math.cos(foldPhase)`
  `y = u * span - offset`, with fold phase drifting via `Math.sin(time * 0.13)`.
- **Physics**: Delta-time normalized (`dt`), negative upward gravity (−0.06 to −0.12), velocity damping 0.95, pointer repulsion within 120px desktop (bypassed on touch to preserve native scroll).
- **Scroll Morph**: `progress = clamp(-heroRect.top / (heroHeight - stickyHeight))`. As progress advances, field lerps from unconstrained drift into an orderly ribbon; roughness halves; layer rotates `−0.13 * progress`. Reverses continuously on scroll up.
- **Resilience & Fallbacks**:
  - `IntersectionObserver` and `document.hidden` pause execution offscreen.
  - Frame time > 35ms triggers adaptive throttling: DPR x0.75 -> particle count −25% -> static fallback.
  - CSS Fallback (`.engine-failed`): Layered blurred ellipses guarantee zero layout disruption.
  - `prefers-reduced-motion`: Renders single static frame at `progress = 0`.
  - Pause Control: Accessible hero button toggles animation loop.

### 10 Webbzer Scene Variants
When requested, swap the scene function behind the identical `update({ time, deltaTime, progress, pointer, isMobile })` interface:
1. **River**: Folded particle sheet (Charcoal + Mint) — AI platforms
2. **Field**: Undulating orbital particle lattice (Obsidian + Cobalt) — Research labs
3. **Contours**: Topographic frequency curves (Onyx + Orange/Magenta) — Audio tech
4. **Terrain**: Terracotta contour bands (Umber + Sand) — Data infrastructure
5. **Vortex**: Fluid spiraling streamlines (Midnight + Aqua) — Climate tech
6. **Grids**: Shearing coordinate grids (Navy + Ultramarine) — Design tooling
7. **Cubes**: Instanced isometric cubes (Graphite + Coral) — Cloud platforms
8. **Folds**: Translucent organza planes (Espresso + Peach/Lilac) — Health/wellbeing
9. **Braid**: Intertwined spectral filaments (Jet + Gold) — Luxury editorial
10. **Isosurface**: Evaluated 2D scalar field metaballs (Pitch + Emerald) — Biotech

---

## 4. Motion System & 93-Effect Implementation

- **Identity**: "Diffusion to clarity" — reveals resolve from soft/diffuse (`blur(16px)` + opacity 0 + transform) to sharp and clear.
- **Timing Standards**: Hover/focus: 90–220ms; Nav transitions: 180–250ms; Standard UI: 200–300ms; Dialogs: 200–350ms; Panel swaps: 250–500ms; Text reveals: 500–850ms.
- **Reveals**: Trigger once via `IntersectionObserver` at 80–85% viewport.
- **Typography Split**: Short editorial headings use `Intl.Segmenter` for per-character stagger (`L1`/`T1`) with `aria-label` on parent and `aria-hidden` on spans. Section H2s use whole-line mask reveals (`S3`/`T2`). Never split body copy.
- **Tally**: Maintain exact coverage of all 93 effects (59 Build, 11 Adapt, 23 Skip with explicit rationale). See [Catalog](references/MOTION_EFFECTS_CATALOG.md).

---

## 5. Anti-Slop Writing & Voice Law

Strictly enforce authentic human engineering prose:
1. **Voice Stance**: Lead with the point, trust the reader, take a technical stance, use concrete verbs (*build, cut, test, ship*), plain words (*is, has*), and high information density.
2. **Banned Words & Phrases**: Never use *delve, testament, tapestry, landscape, pivotal, in conclusion, crucial, embark, game-changer, foster, leverage, robust, streamline, seamless, moreover, unleash, elevate, beacon, "not X but Y", throat-clearing preambles, emphasis crutches ("Full stop."), artificial one-line staccato, or forced triads*.
3. **Punctuation & Formatting**: Zero em-dashes by default (never more than one per document); no decorative bold listicles; sentence case headings; no emojis in headings or copy; typographic curly apostrophes.
4. **Hallmark Tiers**: Floor violations (failing contrast, broken focus, broken reduced motion, invented facts) fail the build. Allowed reflex overrules (eyebrows, tracked micro-labels, single accent word) must be stamped in the CSS comment.
5. **Rubric**: Score copy against the 8-criteria rubric (target >= 32/40 with no score below 3). See [Anti-Slop Law](references/ANTI_SLOP_LAW.md).

---

## 6. Component State Matrix & Interaction Details

Every interactive element must explicitly implement:
- **Default**: Styled strictly from tokens.
- **Hover**: Fine pointers only (`@media (hover: hover) and (pointer: fine)`). Lift translateY −2px, border brighten.
- **Focus-Visible**: 2px solid accent ring with 3px offset. Never suppress or hide focus rings.
- **Active / Pressed**: Tactile scale compression (`transform: scale(0.98)`), 90ms.
- **Selected / Current**: Explicit aria attributes (`aria-selected="true"`, `aria-current="page"`).
- **Disabled**: Dimmed opacity (0.4), `cursor: not-allowed`, pointer events suppressed.
- **Content States**: Explicit handling for empty and illustrative outputs. No simulated loading spinners.

---

## 7. WCAG 2.2 AA Accessibility & Responsive Calibration

- **Semantic Landmarks**: `<header>`, `<main>`, `<section>`, `<nav>`, `<footer>`, `<dialog>`. Visible skip link (`Skip to content`) as first focusable element.
- **Keyboard Traversal**:
  - Full tab stop sequence.
  - Workflow tabs: Arrow keys with roving `tabindex`.
  - Carousel: Arrow keys and buttons.
  - Dialog: Focus trapped within modal, Escape key dismisses, focus restored to opener.
- **Screen Reader Announcements**: Status changes announced via `aria-live="polite"` (toasts, mode swaps, staged dialog text). All decorative canvases, SVG art, and particles flagged `aria-hidden="true"`.
- **Live Reduced Motion**: Immediate response to `prefers-reduced-motion: reduce`. Canvas freezes into static frame; reveals become instant; hero scroll pinning releases; scroll progress bar hides.
- **Touch Ergonomics**: All interactive touch targets >= 44x44px.
- **Responsive Widths**: Calibrated across 8 test viewports:
  - `320px` / `360px` / `390px`: Single column, zero horizontal overflow, H1/sub/CTA visible on first screen, particle count reduced to 44.
  - `768px`: Stacked tablet layout, swipeable carousels.
  - `1024px` / `1280px` / `1440px` / `1920px`: 12-column grid, fluid clamp scales, maximum content width 1360px.

---

## 8. Build Order & Verification Protocol

### Step-by-Step Build Order
1. **Skeleton**: HTML5 doctype, meta tags, favicon data URI, design tokens in `:root`, reset, base a11y, `.has-js` gating.
2. **Header & Navigation**: Sticky header, glass transition, mobile menu drawer, scrollspy.
3. **Hero Structure & Engine**: Two-phase hero markup, counter, Canvas 2D engine class, fallback CSS, pause control.
4. **Sections 3–10**: Manifesto, Platform bento, Workflow tabs, Showcase carousel, Principles, Plans, FAQ, Contact & Footer.
5. **Overlays & Dialog**: Native `<dialog>` modal, toast manager, SVG copy utility, motion toggle.
6. **Effects Pass**: Implement catalog effects L -> A -> P -> S -> C -> O -> M -> T -> R.
7. **Anti-Slop Edit Pass**: Audit all strings against banned list, calculate rubric score (>=32/40), stamp decision header comment in `<style>`.
8. **Verification Pass**: Run the self-verification checklist.

### Self-Verification Checklist
- [ ] Opens directly in browser with zero console errors and zero external requests.
- [ ] Complete keyboard operability (skip link, nav, tabs, carousel, accordion, modal).
- [ ] Two-phase hero scroll advances and reverses continuously without jumps or flashes.
- [ ] Reduced motion, JavaScript disabled, and engine failure states render gracefully.
- [ ] Zero horizontal overflow at 320px, 390px, and 1440px viewports.
- [ ] All 93 catalog effects accounted for (59 built, 11 adapted, 23 skipped with rationale).
- [ ] Zero banned AI words or constructions in any copy or report prose.
- [ ] Final report appended per Section 16 format.
