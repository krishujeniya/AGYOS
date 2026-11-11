# Complete 93-Effect Motion & Interaction Catalog

Synthesized from the Webbzer engine specifications and the Google Flow design-principles audit (188 principles).

## Operating Rules
- **B (Build)**: Implement fully per specification.
- **A (Adapt)**: Implement the single-page, media-free adaptation described.
- **S (Skip)**: Explicitly omitted with rationale documented in the final report.
- **Motion Principle**: Diffusion to clarity. Every reveal resolves from diffuse (blur <=16px + opacity + transform) to sharp and clear.
- **Reduced Motion**: Honored on initial render and dynamically on media query changes.

---

## 1. Load & Intro (L1–L7)

| ID | Name & Specification | Decision |
|---|---|---|
| **L1** | **Hero H1 entrance**: Per-character stagger via `Intl.Segmenter`, opacity 0→1, translateY 28px→0, rotateX −20°→0, 650ms `--ease-reveal`, 24ms/char, capped at 700ms total. Accessible name on parent via `aria-label`, individual spans `aria-hidden`. | **B** |
| **L2** | **Subcopy & CTA follow-up**: 450ms, 70ms step delay after headline entrance settles. | **B** |
| **L3** | **Hero scene diffusion-in**: Canvas wrapper blur 16px→0, opacity 0→1, scale 1.04→1, 700ms `--ease-expo` triggered on `.engine-ready`. | **B** |
| **L4** | **Particle field fade-in**: Luminous particle field fades in after first paint, 700ms duration. | **B** |
| **L5** | **Banner entrance**: Height expansion + opacity reveal, 250ms duration. | **B** |
| **L6** | **Header reveal**: Opacity 0→1, translateY −8px→0, 250ms duration. | **B** |
| **L7** | **Scroll-cue loop**: Subtle vertical bobbing (translateY 0→6px) with breathing opacity, 1.8s ease-in-out infinite loop. Fades out as soon as hero scrolls. | **B** |

---

## 2. Ambient & Continuous (A1–A8)

| ID | Name & Specification | Decision |
|---|---|---|
| **A1** | **Particle drift with negative gravity**: Particles drift gently upward (negative gravity −0.06 to −0.12) while hero is in viewport. | **B** |
| **A2** | **Turbulence & oscillation**: Seeded harmonic sine oscillation (`sin(time * f + phase)`) per particle. No two particles share identical loops. | **B** |
| **A3** | **Orbital formation flow**: When user toggles Orbit mode, particles ease from river path into concentric ring/halo formations via spring physics (spring tension 0.06, friction 0.82). | **B** |
| **A4** | **Halo & ring targets**: Geometric targets for orbital states, calculating rotational coordinates dynamically. | **B** |
| **A5** | **Manifesto chips sine float**: Floating chips drift on a slow sine trajectory (translateY <= 35px, 7s cycle). | **B** |
| **A6** | **Atmosphere glow breathing**: Ambient background radial glow breathes in opacity and scale (1.0 to 1.06, 8s ease-in-out cycle). | **B** |
| **A7** | **Ambient media-free loop**: In a media-free build, the canvas particle field serves as the primary visual loop. A visible hero Pause control allows halting autonomous motion. | **A** |
| **A8** | **Content-derived color shift**: Activating showcase slide subtly adjusts the atmospheric glow hue over 450ms. | **A** |

---

## 3. Pointer & Focus (P1–P14)

| ID | Name & Specification | Decision |
|---|---|---|
| **P1** | **Particle cursor repulsion**: Cursor repels particles within a 120px radius (90px on touch devices) using smooth inverse-distance force with 0.95 damping. Touch scrolling remains unhindered. | **B** |
| **P2** | **Custom cursor**: Omitted by design. Custom cursor followers add latency and visual clutter. Native platform cursors are preserved everywhere. | **S** |
| **P3** | **Magnetic pull on primary pills**: Subtle pointer attraction (<=6px travel within 80px radius, 250ms `--ease-primary`). | **B** |
| **P4** | **Magnetic border highlight**: Pointer-tracked radial gradient on card borders updated via CSS custom properties `--mx` and `--my`. | **B** |
| **P5** | **Button hover lift**: translateY −2px + background fill shift, 150–220ms duration. Fine pointers only (`@media (hover: hover)`). | **B** |
| **P6** | **Active button press**: Tactile scale compression (`scale(0.98)`), 90ms duration. | **B** |
| **P7** | **Link underline reveal**: `scaleX(0)` to `scaleX(1)` with `transform-origin: left`, 200ms duration. | **B** |
| **P8** | **Nav hover shift**: Color transition over 180–250ms on desktop navigation links. | **B** |
| **P9** | **Dropdown chevron**: No nested dropdown menus in one-page editorial architecture. | **S** |
| **P10** | **Card emphasis**: translateY −4px + border brightness elevation on `:hover` and `:focus-within`, 250ms. | **B** |
| **P11** | **Directory-row highlight**: No dense table directory module. Covered by plan card row focus states. | **S** |
| **P12** | **Persistent focus ring**: 2px solid accent ring with 3px offset (`:focus-visible`), 100ms entrance. Never hidden or clipped. | **B** |
| **P13** | **Variable font weight shift**: System font stacks used for zero external requests; variable font axes not available. | **S** |
| **P14** | **Video thumbnail preview**: Media-free build without video assets. | **S** |

---

## 4. Scroll (S1–S16)

| ID | Name & Specification | Decision |
|---|---|---|
| **S1** | **Fade-and-rise reveal**: Triggered once via `IntersectionObserver` at 80–85% viewport. Elements rise 24–40px with opacity over 450ms `--ease-reveal`. | **B** |
| **S2** | **Staggered group reveals**: Multi-item grids and card groups reveal with a 70ms stagger step between siblings. | **B** |
| **S3** | **H2 line-mask reveal**: Section headings reveal using an overflow-hidden line mask with 600ms expo transition. | **B** |
| **S4** | **Frame entrance**: Scale 0.96→1, opacity 0→1, blur 8px→0 over 700ms expo for major cards and shells. | **B** |
| **S5** | **Showcase frame parallax**: Scrubbed vertical drift of translateY ±8% relative to viewport scroll progress. | **B** |
| **S6** | **Layered panel parallax**: Multi-layered workflow stack where background, bridge, and output layers drift at distinct rates. | **B** |
| **S7** | **Scroll-scrubbed canvas morph**: Hero river morphs from free particle drift into an orderly band as `progress` increases. Reverses seamlessly on upward scroll. | **B** |
| **S8** | **Traveling sine accent**: Contact section concentric arcs rotate and shift along a sine wave relative to scroll position. | **B** |
| **S9** | **Pinned chapter**: Pinned hero container across a 200svh scroll distance (190svh on mobile). No other sections are pinned to avoid scroll-jacking. | **A** |
| **S10** | **Top scroll progress bar**: 2px hairline fixed at viewport top, tracking overall document scroll with `scaleX(progress)`. Hidden when reduced motion is preferred. | **B** |
| **S11** | **Active nav indicator (Scrollspy)**: Sliding pill indicator under the navigation link corresponding to the active section in view, 250ms transition. | **B** |
| **S12** | **Header glass transition**: Past 8px of scroll, header transitions to semi-transparent surface with 16px blur and bottom hairline, 250ms duration. | **B** |
| **S13** | **Scroll cue fade-out**: Scroll indicator arrow and cue text fade out completely past the hero top threshold. | **B** |
| **S14** | **Native smooth scroll**: Native CSS `scroll-behavior: smooth` with `scroll-padding-top` matching sticky header height. Never hijack native touch or mousewheel physics. | **A** |
| **S15** | **Anchor navigation with focus transfer**: Internal anchor links shift keyboard focus directly to target section with `tabindex="-1"`. | **B** |
| **S16** | **Documentation TOC tracking**: No documentation manual sidebar present. | **S** |

---

## 5. Carousels, Tabs & Stages (C1–C14)

| ID | Name & Specification | Decision |
|---|---|---|
| **C1** | **Showcase rail**: Scroll-snap carousel with arrow buttons, keyboard arrow navigation, and touch drag support. Programmatic travel 400–650ms ease-in-out. | **B** |
| **C2** | **Active card emphasis**: Active centered card renders at scale 1.0 and opacity 1.0; inactive neighbor cards scale to 0.92 with opacity 0.6 over 450ms. | **B** |
| **C3** | **Edge fade masks**: Peeking sibling cards visible at viewport edges with CSS `mask-image: linear-gradient(...)` to indicate scrollable continuation. | **B** |
| **C4** | **Arrow control states**: Hover, active press, and disabled states at scroll boundaries with 150ms transitions. | **B** |
| **C5** | **Rail progress indicator**: Horizontal track fill bar scaling with current scroll position across the carousel rail. | **B** |
| **C6** | **Auto-rotate carousel**: Omitted by design. Unsolicited motion violates accessibility and user autonomy. All carousel navigation is user-driven. | **S** |
| **C7** | **Segmented stage indicator**: Sliding active background pill behind workflow tab controls, 250–400ms duration. | **B** |
| **C8** | **Stage panel cross-fade**: Tab panel transition combining opacity and translateY 16px over 450ms. Height is reserved to prevent layout shifts (CLS = 0). | **B** |
| **C9** | **Stage watermark reveal**: Large background watermark text (e.g. RESEARCH, OPERATIONS) slides in behind active panel with 600ms expo easing. | **B** |
| **C10** | **Use-case switcher**: Functionally identical to and satisfied by C8 stage panel transition mechanism. | **A** |
| **C11** | **Showcase slide selector**: Integrated directly into C1 rail controls and card click handlers. | **A** |
| **C12** | **Plan card entrance**: 70ms stagger entrance for pricing tiers with hover border glow. | **B** |
| **C13** | **FAQ accordion**: Native button triggers with `aria-expanded` and CSS `grid-template-rows: 0fr` to `1fr` transition over 300ms. Plus icon rotates 45 degrees. | **B** |
| **C14** | **Code tabs**: No code snippets in this editorial presentation. | **S** |

---

## 6. Overlays & Feedback (O1–O6)

| ID | Name & Specification | Decision |
|---|---|---|
| **O1** | **Mobile navigation menu**: Fullscreen or sheet slide-in over 400–550ms expo with backdrop blur. Staggered link entrance (40ms step). Escape key and link selection close menu. Focus trapped while open and restored to hamburger trigger upon close. | **B** |
| **O2** | **Command palette (Cmd+K)**: Omitted as unnecessary complexity for a single-page editorial showcase. | **S** |
| **O3** | **Demo modal dialog**: Native `<dialog>` element with backdrop `blur(24px)` and dark scrim. Scales 0.96→1.0 with opacity over 250–350ms expo. Full focus trap, Escape key handling, and backdrop click dismissal. | **A** |
| **O4** | **Dropdown menu**: No dropdowns in information architecture. | **S** |
| **O5** | **Copied toast notification**: Toast slides in over 200ms, holds for 1.6s, fades out over 200ms. Announced to screen readers via `aria-live="polite"`. | **B** |
| **O6** | **Icon-only control tooltips**: Floating tooltips appear after 300ms delay with 120ms fade for icon buttons. Visible on both hover and focus. | **B** |

---

## 7. Media & Placeholders (M1–M6)

| ID | Name & Specification | Decision |
|---|---|---|
| **M1** | **Poster-to-video crossfade**: Omitted because build is media-free without video tags. | **S** |
| **M2** | **Custom video controls**: Omitted because build has no video playback. | **S** |
| **M3** | **Play button hover**: Omitted because build has no video playback. | **S** |
| **M4** | **Lazy video playback**: Omitted because build has no video. Canvas engine handles offscreen pausing via `IntersectionObserver`. | **S** |
| **M5** | **Blur-up frame reveal**: Showcase illustrative panels reveal from `blur(16px)` to `blur(0)` with opacity over 400ms on first viewport intersection. | **A** |
| **M6** | **Reserved aspect ratio frames**: All showcase and card containers declare explicit `aspect-ratio` to guarantee zero Cumulative Layout Shift (CLS = 0). | **A** |

---

## 8. Text & Data (T1–T5)

| ID | Name & Specification | Decision |
|---|---|---|
| **T1** | **Per-character text stagger**: Applies L1 mechanics to hero headline and selected editorial headers. | **B** |
| **T2** | **Whole-line section reveal**: Applies S3 line-mask reveal to major section H2 titles. | **B** |
| **T3** | **Typewriter text effect**: Omitted. Character stagger (T1) provides superior editorial elegance without artificial cursor blinking. | **S** |
| **T4** | **Count-up metrics**: Strictly omitted by anti-slop rules. Only real, verified metrics may animate; fictional design concepts must never animate simulated counters. | **S** |
| **T5** | **Staged status line in demo dialog**: Text swaps sequentially ("Preparing example…" → "Example ready — nothing was sent") over 150ms, announced via `aria-live`. | **B** |

---

## 9. Page, Route & State (R1–R17)

| ID | Name & Specification | Decision |
|---|---|---|
| **R1** | **Same-document View Transitions**: `document.startViewTransition()` wraps stage tab swaps and filter transitions where supported; falls back instantly where unsupported. | **A** |
| **R2** | **Shared-element route transitions**: Omitted because application is a single-page document. | **S** |
| **R3** | **Persistent sticky header**: Single persistent header with scroll-reactive styling. | **B** |
| **R4** | **Subchapter transitions**: Two-phase hero scroll journey (S9) and stage watermark swaps (C9). | **B** |
| **R5** | **FLIP reflow on showcase filters**: Filter chips trigger FLIP (First, Last, Invert, Play) transition over 300ms `--ease-primary` to animate card repositioning. | **B** |
| **R6** | **Filter empty state**: Clean message card displayed when active filter yields zero results ("Nothing here yet — try another filter"). | **B** |
| **R7** | **Skeleton loading shimmer**: Omitted because all content is self-contained and pre-rendered without async network fetches. | **S** |
| **R8** | **Simulated loading spinners**: Strictly omitted. Fabricated spinners degrade user trust. | **S** |
| **R9** | **Form submission stroke draw**: Omitted. No real form submissions exist in static concept build. | **S** |
| **R10** | **Form error validation states**: Omitted for the same reason as R9. | **S** |
| **R11** | **Motion toggle control**: Accessible button in footer toggling motion on/off with 150ms sliding thumb transition. | **B** |
| **R12** | **Particle mode toggle**: Toggles field between Flow and Orbit modes with spring physics retargeting. | **B** |
| **R13** | **Theme switch**: Omitted by design. Presentation maintains one coherent, dark editorial aesthetic. | **S** |
| **R14** | **Demo dialog replay button**: Control in demo modal allowing users to replay staged status progression. | **A** |
| **R15** | **SVG stroke draw animations**: Inline SVG geometric lines (bridge line, contact arcs, orbit rings) draw their stroke on reveal (600–900ms `--ease-primary`). | **B** |
| **R16** | **Copy logo feedback**: "Copy logo as SVG" button temporarily swaps label to "Copied!" accompanied by toast notification. | **B** |
| **R17** | **Language switcher**: Omitted. Concept copy is English-only; synthetic translations are prohibited. | **S** |

---

## Catalog Tally Summary
- **59 Built (B)**
- **11 Adapted (A)**
- **23 Skipped with documented rationale (S)**
- **Total: 93 Effects Decided**
