# MASTER PROMPT — FLUX · a cinematic AI-platform website

**Tuned for:** Gemini 3.8 Flash (high reasoning) · **Output:** ONE self-contained `index.html`
**Synthesized from:** the 10 Webbzer template specs (Flux / Field / Signal / Strata / Tidal / Phase / Lattice / Aura / Prismatic / Bloom) · the Google Flow design-principles audit (188 principles) · the merged site master prompt (full motion catalog, style catalog, state matrix) · five anti-slop skills, principles only (blader/humanizer · theclaymethod/unslop · Nutlope/hallmark · conorbronsdon/avoid-ai-writing · hardikpandya/stop-slop).

**How to use:** paste everything below the horizontal rule into Gemini 3.8 Flash (high) as ONE message. To rebrand, edit §2 and the Copy Bank in §5 — nothing else needs touching. Appendix A is documentation, not work.

---

You are Gemini 3.8 Flash (high), acting as a world-class creative director and senior front-end engineer. Build **FLUX®**, a fictional AI-workflow platform presented as a cinematic, dark, editorial one-page website at the quality level of flow.google/about and antigravity.google. You take principles only and build an original identity: no Google marks, no copied media, no real companies.

## 0 · OUTPUT CONTRACT — non-negotiable

1. Deliver exactly **one file: `index.html`**, fully self-contained. All CSS in one `<style>`, all JS in one `<script>` (module OK). No frameworks, no imports, no build step.
2. **Zero external requests.** No CDN, no webfonts, no images, no video, no fetch, no analytics. Every visual is CSS, inline SVG, or Canvas 2D. Fonts are intentional system stacks (display serif: `Iowan Old Style, Palatino Linotype, Palatino, Georgia, 'Times New Roman', serif`; UI: system sans; mono for none). Glyph shapes may vary by OS — accepted.
3. The file must be **complete**: no placeholders, no `TODO`, no lorem ipsum, no truncated sections, no empty handlers, no summarizing remaining code in prose. If output is long, continue until finished.
4. First visible output = the complete file, then the Final Report (§16). Print no plans, options, or commentary.
5. Every fact is fictional-but-labeled: this is a design concept. Never invent clients, testimonials, user counts, metrics, awards, or security certifications. Simulated output is labeled `EXAMPLE` or `ILLUSTRATIVE`.
6. Nothing may be hidden by default and revealed by JS: gate every reveal state behind an `html.has-js` class added by script. Content must read perfectly with JavaScript disabled.
7. Every word you write obeys §5B (anti-slop law) — site copy, dialog, tooltips, and the Final Report prose alike. Never invent a fact to fill a sentence.

## 1 · PROTOCOL — how you work

1. Think silently. Decide nothing with the user: every choice is already made in this document.
2. Build in the exact order of §14.
3. Before answering, run every item of §15 and fix violations.
4. Obey §18 priority order when values conflict.

## 2 · THE BUILD — decisions already made

- **Brand:** Flux® — "a more considered kind of AI." Voice: quiet confidence, human-centred, honest. Tagline: *Human intent. Intelligent momentum.*
- **Theme:** dark cinematic, ONE coherent theme, no theme switch. **Hero:** particle-led — the folded luminous particle river (§6), scroll-scrubbed, pointer-reactive. Media-free build: no photos, no video — the field, type, and SVG art carry everything.
- **Palette (pinned):** deep charcoal `#0a1011` canvas · raised `#101919` / `#152120` · paper `#eff3eb` · muted `#a4b0ae` · one quiet mint `#cee5d3` · hairline `rgba(225,239,232,.15)` · scrim `rgba(10,16,17,.72)` · atmosphere glows `#29453d` / `#263b33` (green-charcoal, a few chapters only) · one inverted light chapter (§7 below) using paper bg, ink `#19251e`, accent `#63796a`. No neon, no bloom, no per-section gradients.
- **Page anatomy — 10 acts, in this order:**

| # | Section (id) | Content & pattern |
|---|---|---|
| 0 | Banner (`.banner`) | One slim honest line: "Flux is a design concept — see what that means →" → `#faq`. Entrance L5. |
| 1 | Header (`.site-header`) | Sticky, 86–100px, glass on scroll (S12). Brand SVG mark (three wavy lines) + wordmark. Links: Platform, Workflow, Showcase, Plans, FAQ. Primary pill "Let's talk →" opens demo dialog. Mobile menu (O1). Scrollspy indicator (S11). |
| 2 | Hero (`#top`) | 200svh scroll region (190svh ≤700px), sticky 100svh inner. Canvas particle river right-weighted; eyebrow, oversized serif H1, subcopy, primary CTA — all visible on first screen without scroll. Two-phase scroll journey → "Less friction. More flow." Counter `01—02` with progress bar. Scroll cue L7. |
| 3 | Manifesto (`#manifesto`) | Editorial pause: eyebrow "A DIFFERENT STARTING POINT", large centered statement, 3 floating chips on a sine drift (A5), framed concept composition (SVG orbit arcs, stroke-draw R15). |
| 4 | Platform (`#platform`) | Bento: wide CONNECT card (orbit constellation art), UNDERSTAND card (decision rings), full-width MOVE card (momentum arcs). CSS/SVG art only, magnetic border (P4). |
| 5 | Workflow (`#workflow`) | Segmented tabs **Research / Operations / Creative** (C7–C9). Panel: input stack → bridge → output card. All panel content is labeled `EXAMPLE`. Keyboard ARIA tabs with arrow keys. |
| 6 | Showcase (`#showcase`) | Rail carousel of 4 illustrative output frames (C1–C5): Research brief · Operations plan · Creative direction · A calmer inbox. Filter chips All/Research/Operations/Creative (R5 FLIP, R6 empty state). Frames get blur-up reveal (M5). Label: `ILLUSTRATIVE OUTPUT — NOT A PERFORMANCE CLAIM`. |
| 7 | Principles (`#principles`) | The inverted light chapter. Paper background, ink text: 01 Built around intention · 02 Clarity over complexity · 03 Your judgment. Amplified. |
| 8 | Plans (`#plans`) | Three aligned example plan cards (C12) — Concept $0 / Studio / Team — every card labeled `EXAMPLE PLAN — NOT REAL PRICING`, SVG checkmarks, footnote. |
| 9 | FAQ (`#faq`) | Accordion (C13), button + `aria-expanded` + `grid-template-rows` animation. First answer explains Flux is a fictional concept template. |
| 10 | Contact + footer (`#contact`) | Concentric arcs reacting to scroll (S7/S8, stroke-draw R15), "Find your forward." + "Start a conversation →" (demo dialog). Footer: brand, tagline, **Copy logo as SVG** (R16 + O5), **Motion: On/Off** toggle (R11), year via JS, "About this template" → `#faq`. |
| — | Demo dialog (`#demo-dialog`) | `<dialog>`: "Make it your own." Truthful copy: this is where a real booking/signup/contact flow would go; **no details are collected or sent**. Staged status line (T5) with Replay control (R14). Esc, ×, backdrop click all close; focus returns to opener. |

- **Density rhythm** across the page: cinematic → spare → feature-rich → editorial → utilitarian → spare. Pricing and FAQ come **after** proof, never before.

## 3 · DESIGN TOKENS — put this block in `:root` verbatim, then use only tokens

```css
:root{
  /* color */
  --bg:#0a1011; --surface:#101919; --surface-2:#152120; --paper:#eff3eb; --muted:#a4b0ae;
  --accent:#cee5d3; --accent-dim:rgba(206,229,211,.35); --line:rgba(225,239,232,.15);
  --scrim:rgba(10,16,17,.72); --atmo-1:#29453d; --atmo-2:#263b33;
  --ink-inverse:#19251e; --muted-inverse:#596b60; --accent-inverse:#63796a;
  /* type */
  --font-display:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif;
  --font-ui:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  --text-hero:clamp(64px,8vw,132px); --text-h2:clamp(44px,5.2vw,82px);
  --text-h3:clamp(21px,2vw,25px); --text-body:15px; --text-small:13px;
  --text-nav:12px; --text-label:10px; --text-legal:12px;
  /* space · radius · border */
  --space-1:4px; --space-2:8px; --space-3:16px; --space-4:24px; --space-5:36px;
  --space-6:48px; --space-7:60px; --space-8:80px; --space-9:88px; --space-10:120px; --space-11:180px;
  --r-sm:4px; --r-md:8px; --r-lg:16px; --r-xl:24px; --r-2xl:36px; --r-pill:9999px;
  --pad:clamp(24px,5.5vw,100px); --content-max:1360px;
  /* motion */
  --ease-primary:cubic-bezier(.165,.84,.44,1); --ease-expo:cubic-bezier(.19,1,.22,1);
  --ease-playful:cubic-bezier(.34,1.85,.64,1); --ease-reveal:cubic-bezier(.22,1,.36,1);
  --dur-fast:150ms; --dur-base:250ms; --dur-slow:450ms; --dur-scene:700ms;
  --stagger-step:70ms; --stagger-char:24ms;
  --blur-diffuse:16px; --blur-glass:16px; --blur-overlay:24px;
  --lift-hover:-2px; --lift-card:-4px; --press-scale:.98;
  /* layers · focus */
  --z-header:50; --z-dropdown:60; --z-overlay:80; --z-toast:90;
  --focus-ring:2px solid var(--accent); --focus-offset:3px;
}
```

Contrast is law: `--muted` on `--bg` ≈ 8.5:1; keep every body text ≥ 4.5:1 and large display ≥ 3:1, including over scrims. Contrast overrides decorative opacity.

## 4 · ART DIRECTION LAW

1. Near-black canvas; luminosity comes from the particle field and type — UI chrome stays quiet.
2. One dominant focal point per section; hierarchy by scale, contrast, placement.
3. Negative space is a feature: long quiet intervals around key messages.
4. Figure–ground: paper type on charcoal; muted text yields to headlines.
5. Pills signal action; cards signal content. 1px hairlines separate planes; shadows only on overlays (menu, dialog, toast).
6. Soft geometry (pills, 12–24px card radii) + organic geometry (orbits, halos, arcs, folded ribbons).
7. Editorial asymmetry; alternate alignment between workflow stages; oversized serif headlines are graphic shapes (`text-wrap:balance`).
8. 10px letter-spaced eyebrow labels (`.13em`) name each section; sparse, never paragraphs.
9. Centered type for intros/transitions; left-aligned for dense comparisons and directories.
10. Progressive concreteness: density rises as intent rises (hero poetic → plans/FAQ practical).
11. Outcome before tooling; evidence before explanation; capability before pricing.
12. Peeking neighbor cards + edge-fade masks signal continuation on every rail.
13. One visual grammar everywhere: same radius, border, spacing, and motion family across varied content.
14. Gestalt: proximity groups image+title+detail+CTA; similarity marks repeated actions; common region (borders, rounded cards) binds units; chunk the workflow into three memorable stages.
15. Scrim over any busy field behind copy; copy is never sacrificed to atmosphere.
16. Atmosphere: ONE glow family, concentrated in 2–3 chapters — never a gradient in every section.
17. Serial-position: strongest impression first, practical close last.
18. Recognition over recall; progressive disclosure; the bright primary CTA is the isolation effect in a dark field.

## 5 · TYPOGRAPHY & COPY

- Scales from tokens: hero `--text-hero`/1.0/`-.06em`; H2 `--text-h2`/1.05/`-.055em`; H3 `--text-h3`/1.3/`-.035em`; body `--text-body`/1.65, measure 60–80ch; nav `--text-nav`; eyebrows `--text-label`/`.13em`; legal ≥ `--text-legal`. Text hierarchy: strong headline → softer body → dim metadata.
- One H1 (`Intelligence in motion.`). Clean heading order. Action labels match intent: Explore, See how it works, Start a conversation, Copy logo.
- Voice shifts poetic → practical as the page descends. Benefits before features; features before proof; proof before plans.
- **Copy Bank (canonical — use these; refine phrasing, never inflate claims):**

| Slot | Copy |
|---|---|
| Eyebrow | A more considered kind of AI |
| H1 | Intelligence in *motion.* |
| Hero sub | Connect the dots. Clear the busywork. Make room for what comes next. |
| Hero CTA | Explore the platform → |
| Journey (phase 2) | FROM POSSIBILITY TO PURPOSE · Less friction. *More flow.* · A clear path from scattered information to your next meaningful move. |
| Platform intro | Your work has a rhythm. *Let's find it.* — Good ideas deserve better than another handoff. |
| Capabilities | 01 / CONNECT — Context, not another silo. · 02 / UNDERSTAND — Find the signal. · 03 / MOVE — Keep your momentum. |
| Workflow heading | From a loose end to *a clear next step.* |
| Workflow data | research: input "A world of information." → brief "The bigger picture. The important details." (structured summary · sources kept in context · questions worth exploring) \| operations: input "The moving pieces." → "A shared direction. A clearer handoff." (priorities in one view · clear next-step ownership · a checkpoint for your team) \| creative: input "The start of something." → "More room to explore. A place to begin." (themes worth developing · a first-pass creative brief · your perspective, still essential) |
| Principles | The future of work should feel *more human.* |
| FAQ | What is Flux? · Can I make this my own? · Does the experience work on mobile? · Is any of this connected to a real service? |
| Contact | MAKE ROOM FOR WHAT'S NEXT · Find your *forward.* · Start a conversation → |
| Footer | Human intent. Intelligent momentum. |

## 5B · ANTI-SLOP LAW — write like a person, lint like a machine

Merged and deduplicated from humanizer, unslop, hallmark, avoid-ai-writing, and stop-slop. Principles only, no tooling. **Scope:** every string in the file beyond the Copy Bank (section body copy, capability descriptions, workflow panel copy, showcase captions, FAQ answers, dialog, tooltips) and the Final Report prose. The Copy Bank above is fixed brand copy: its short display lines are a deliberate brand device and are exempt from the cadence bans below. This instruction document is not site copy.

**Voice law (stance):**
1. Lead with the point. No throat-clearing, no setup before the idea.
2. Trust the reader. No over-explaining, no "in other words", no hand-holding, no telling them what they already know.
3. Have a stance. A specific opinion beats balanced-to-a-fault framing. "You" beats "people"; no narrator-from-a-distance voice.
4. Be concrete. Verbs a reader can picture (build, cut, fix, send, write, ship) over abstract ones (leverage, utilize, facilitate, implement, optimize, navigate, unpack, foster). Active voice; a human subject does things. No inanimate agency ("the platform empowers", "the data tells a story", "the numbers speak for themselves").
5. Plain over impressive: is/has over "serves as / features / boasts"; specific over grand. If a sentence sounds like a pull-quote, rewrite it.
6. Density over filler: every word earns its place; if it can be cut without losing meaning, it is already gone.

**Banned constructions (hard list — none may appear in any string):** "not X but Y" and negative parallelism ("It's not just X, it's Y", "Not only… but also", "No prior. No nostalgia.") — state the point directly (genuine corrections like "Use pnpm, not npm." stay fine) · throat-clearing openers ("Here's the thing:", "Let me be clear", "It turns out", "Let's dive in", "Let's unpack", "In today's fast-paced…") · emphasis crutches ("Full stop.", "Let that sink in.", "Read that again.", "Make no mistake", "This cannot be overstated", "The struggle is real.") · one-line closers, cliffhanger fragments, dramatic staccato ("That's it. That's the thing.") · deep-sounding sayings ("At its core, what really matters is…") · staged run-ups ("Honestly?", "Let me explain") · arguing with no one ("I'm not saying X, but…", "A tempting approach would be…") · wh-opener self-Q&A ("Why does this matter? Because…") · forced triads: use the count the meaning needs; two items beat three · significance inflation ("stands as a testament to", "pivotal moment", "watershed", "enduring legacy", "rich tapestry", "cornerstone", "game-changing", "The future looks bright") — keep the fact, drop the significance · false agency and personification · vague attribution ("Experts believe", "Studies show") — name the source or cut · reader flattery ("Here's what's interesting", "worth your time", "Whether you're a seasoned pro or just starting out") · business and marketing jargon ("navigate challenges", "leverage synergies", "deep dive", "circle back", "move the needle", "low-hanging fruit", "robust", "seamless", "world-class", "state-of-the-art", "hidden gem", "nestled") · copula avoidance ("serves as", "features", "boasts", "showcases" → "is", "has") · superficial -ing riders ("…, symbolizing…, reflecting…") · formulaic challenge arcs ("Despite challenges… continues to thrive") — name the challenge and the response · chatbot residue and reasoning leaks ("Certainly!", "Great question!", "I hope this helps", "as an AI", "Let me think step by step") · meta-commentary ("The table below compares…", a heading repeated in its first sentence, "The rest of this…") · generic codas and summary sandwiches ("In conclusion…", "Ultimately, this reminds us that…") — end on the last concrete fact or the action · hedge stacks ("could potentially possibly", "(arguably…)", "While X is promising, Y remains a challenge") — uncertainty stated once, plainly, only where real · filler and inflation ("in order to"→"to", "due to the fact that"→"because", "utilize"→"use", "leverage"→"use", "commence"→"start") · synonym cycling — repeat the clear word · false ranges ("from X to Y" spanning everything) — list the actual items · paragraph-openers on connective scaffolds ("Moreover,", "Furthermore,") — restructure · knowledge-limit filler ("While details are limited…") — state what is known or cut.

**Mechanics:** em-dashes: zero by default, never two in one paragraph; commas, periods, colons, parentheses do that job · no decorative bold, no bold-label listicles ("**Speed:** Speed improved…") — write prose · headings in sentence case that name what the section holds; no emoji in headings; a heading never repeats its own first sentence · lists only when the meaning is a list; cut "7 reasons" to the 2–3 that matter · no runs of one-line staccato paragraphs (eyebrow labels excepted) · sentence length varies naturally (roughly 8–25 words); no three consecutive same-length sentences; paragraphs end differently — no punchy one-liner every time · proper typographic apostrophes in UI copy (Let's, you're).

**Structure & silhouette (document-level tells):** paragraphs open on their own claim, not a discourse cue · no recap loops: the ending never re-opens the intro's vocabulary · no intro-promises/body-repeats/conclusion-restates shape · no moralizing coda; every section and the page end on the action or the last concrete fact · no both-sidesism, templated redemption arcs, over-determined lists of benefits, or one uniform emotional register.

**Design tells (Hallmark's gate tiers, mapped to this build):**
- **Floor — never ships:** failing contrast, invisible focus, broken reduced motion, invented facts, broken phone layout. Any one of these fails the whole build (already enforced by §3, §11, §12, §13).
- **Reflex gates — default banned, overrulable only on the record:** eyebrow label above every heading, tracked-capital labels, one coloured word in a headline, pages of empty frames, pages that are nothing but photos, a hero that misses its screen, an email sign-up tacked onto the end, a form that says thanks without sending anything. **This build's recorded overrules (the only three):** eyebrow labels, tracked-capital micro-labels, and the single mint accent word are pinned Flow/Flux brand devices — allowed exactly as specified in §2/§5 and nowhere else. Every other gate stands: no empty frames (every card carries real content), no trailing newsletter, the hero fits its screen (§15), and no form fakes success (§13).
- **Built from the job:** the page ends on its action — here, the conversation CTA and the truthful dialog.
- **Review cold:** after the hero is built, re-read it with fresh eyes before building anything else; a fresh-context review gets the last word.
- **Decisions stamped:** the first CSS comment inside `<style>` lists the decisions taken, including the three recorded overrules.

**The edit pass (process law) — run before you finish:**
1. Write plainly first.
2. Findings pass: read every sentence; quote the smallest defective span; classify it against the banned lists above.
3. Repair pass: smallest repair per finding; never restructure writing that is already human; maximum two passes.
4. Preservation: facts, numbers, names, links, product claims, scope, and honest hedges survive untouched (never silently change an amount or a unit); the Copy Bank is never reworded.
5. Score the prose on 8 criteria, 1–5 each: directness, natural rhythm, concrete verbs, reader trust, human authenticity, density, fact preservation, template avoidance. Ship at ≥32/40 with no criterion below 3; revise below that.
6. Read it aloud (mentally). If it sounds like an announcement or a template, rewrite it.

**In one line:** state, don't perform; name, don't inflate; end on the fact or the action.

## 6 · SIGNATURE HERO — the folded particle river (Canvas 2D)

A luminous, folded river of particles flows down the right side of the hero, like light through silk. It is procedural — not a video, not a gradient, not a stock shape. Build one engine class, zero dependencies:

**Field.** Canvas fills the hero (`position:absolute; inset:0; z-index:-2`), DPR-aware (cap 1.75 desktop / 1.5 mobile ×quality). Two layers: (a) 650 static dust dots, pre-rendered once to an offscreen canvas, opacity ≈ .38; (b) **88 dynamic particles desktop / 44 mobile** — shapes: circle, rounded square, capsule, triangle, dot. Each particle stores position, velocity, home (a point on the ribbon), depth scale 0.4–1.2, size, rotation, rotation velocity, color (mix of paper-white → mint), opacity, seed. Depth drives size, opacity, blur, and apparent speed.

**Ribbon.** Home positions trace a folded band: `u∈[0,1]` along a path of sine folds (≈ `x = cx + sin(u*7−.8)*spread + across*width*cos(fold)`, `y = u*span − offset`, fold phase drifting with `sin(time*.13)`. Wisps and discrete strands: ~8% of particles offset outward (`seed.z>.92` analog). Edge fade via smoothstep at both ends of `u`; a moving filament brightens a traveling band.

**Physics.** Delta-time normalized. Organic oscillation: seeded `sin(time*f+phase)` per particle, never identical loops. Upward drift (negative gravity −0.06…−0.12), velocity damping 0.95, terminal-velocity cap, boundary wrap. **Pointer:** repel within 120px (90 mobile) with smooth inverse-distance force; recovery settles back to flow; passive listeners; touch does not repel (native scroll stays sacred). **Modes** (accessible toggle, R12): *Flow* — free drift; *Orbit* — ease into a ring/halo formation with spring tension 0.06, friction 0.82 and slow rotational flow; transition is fluid, never a cut.

**Scroll morph.** `progress = clamp(−heroRect.top / (heroHeight − stickyHeight))`, smoothed by `1−exp(−dt*8)`. As progress rises, the field reorganizes from free drift into an orderly flowing ribbon: lerp toward ribbon targets by `0.65 * smoothstep(.1,.95,progress)`, roughness halves, whole layer rotates `−0.13*progress`, slight camera-like drift/scale. **Reverse scroll reverses continuously. No scene cuts, no flashing boundaries.**

**Sparkles.** ~1.3% of seeds render larger with a glow sprite (pre-rendered radial gradient, `globalCompositeOperation:'lighter'`), gentle twinkle.

**Choreography (must match exactly).** Copy phase: eyebrow/H1/sub/CTA fade out and rise `−28px` across `smooth(.12,.39)` of progress, then become `visibility:hidden` + `inert`. Journey phase: "Less friction. More flow." arrives across `smooth(.43,.65)` with `+20px` settle; `aria-hidden` until ≥.5. Counter bar fills `scaleX(.05 + progress*.95)`. Scroll cue fades out past hero top (S13). At 0 progress everything returns exactly.

**Performance & resilience.** `requestAnimationFrame` with delta-time; no per-frame allocation; cached sprites via `drawImage`; pause when tab hidden AND when hero offscreen (`IntersectionObserver`, rootMargin 100px); adaptive quality: sustained frame time >35ms → DPR ×0.75 (floor 1), then −25% particles (floor 40), then static frame + `.engine-failed` class; `pagehide` → full dispose (cancel rAF, disconnect observers, remove listeners). On context loss or throw: `.engine-failed` shows the CSS fallback (three layered, rotated, soft-bordered ellipses, blurred, mint-tinted) — content and functionality are unaffected. **Reduced motion:** no loop, one static frame at `progress=0`, no pointer force; live-respond to media-query changes. **Pause control:** a visible hero control (`aria-pressed`, tooltip O6) freezes the field; that is the site's autonomous-motion pause/stop control.

## 7 · MOTION SYSTEM

**Identity — "diffusion to clarity."** Every reveal resolves from soft/diffuse to sharp/clear (blur ≤16px + opacity + transform only). Motion reveals relationships; continuity matters more than the number of effects. Ambient motion (field, glow, loops) is calm; user-triggered transitions are intentional and snappy. Use anticipation, follow-through and overshoot with restraint (`--ease-playful` on ≤3 delightful entrances).

**Easings:** `--ease-primary` ordinary · `--ease-expo` overlays & large reveals · `--ease-reveal` text entrances · `--ease-playful` rare overshoot · ease-in-out carousel travel · ease-in exits · spring physics in the field. **Timing:** hover/focus 90–220ms · nav 180–250ms · standard 200–300ms · modal 200–350ms · panels/tabs 250–500ms · carousel 400–650ms · card reveal 450–750ms · text 500–850ms · scene 500–900ms · char stagger 20–45ms (start 24) capped ~700ms total · ambient loops 5–8s. Reveals never delay interaction. **Reveal mechanics:** trigger once via `IntersectionObserver` at 80–85% viewport; `data-split-text` for short editorial headings only — split with `Intl.Segmenter` (emoji/scripts stay whole), `aria-label` on the parent + `aria-hidden` spans; from `opacity:0; translateY(28px) rotateX(-20deg)` to identity, with `perspective` on the parent. Whole-line variant for section H2s (S3/T2). Never split body copy.

## 8 · COMPLETE EFFECTS CATALOG — 93 IDs, every one decided

Rules: build every **B**; **A** = build the single-page/media-free adaptation shown; **S** = skip, and print the skip + reason verbatim in the Final Report. Zero silent omissions. All durations/easings from §3/§7; reduced-motion behavior per §7/§10 for every built row.

**Load & intro**

| ID | Effect & spec | D |
|---|---|---|
| L1 | Hero H1 entrance: per-char stagger (Intl.Segmenter), opacity 0→1, translateY 28px→0, rotateX −20°→0, 650ms `--ease-reveal`, 24ms/char, cap 700ms; AT hears it once | B |
| L2 | Subcopy + CTA follow-up: 450ms, 70ms step | B |
| L3 | Hero scene diffusion-in: canvas wrapper blur 16px→0, opacity 0→1, scale 1.04→1, 700ms expo on `.engine-ready` | B |
| L4 | Particle field fade-in after first paint, 700ms | B |
| L5 | Banner entrance: opacity + height, 250ms | B |
| L6 | Header reveal: opacity, translateY −8px, 250ms | B |
| L7 | Scroll-cue loop: translateY 0→6px + opacity, 1.8s ease-in-out infinite | B |

**Ambient & continuous**

| ID | Effect & spec | D |
|---|---|---|
| A1 | Particle drift with negative gravity while hero visible | B |
| A2 | Turbulence, oscillation, rotation jitter (seeded, non-looping) | B |
| A3 | Orbital formation flow on mode toggle (spring .06 / friction .82) | B |
| A4 | Halo/ring + arc + wave targets (Orbit mode formations) | B |
| A5 | Manifesto chips sine float: translateY ≤35px, 7s loop | B |
| A6 | Atmosphere glow breathing: opacity + scale 1→1.06, 8s ease-in-out | B |
| A7 | Ambient loop, media-free build → the field IS the loop; visible Pause control (§6) | A |
| A8 | Content-derived color: active showcase slide tints that section's glow hue, 450ms | A |

**Pointer & focus**

| ID | Effect & spec | D |
|---|---|---|
| P1 | Particle cursor repulsion + settle, damping .95, 120px radius | B |
| P2 | Custom cursor — OFF by design: cursor followers read cheap; native cursor everywhere | S |
| P3 | Magnetic pull on primary pills, ≤6px within 80px, 250ms | B |
| P4 | Magnetic border highlight on capability cards: pointer-tracked radial gradient border via `--mx/--my` | B |
| P5 | Button hover lift: translateY −2px + fill shift, 150–220ms | B |
| P6 | Press: scale .98, 90ms | B |
| P7 | Link underline reveal: scaleX 0→1 origin left, 200ms | B |
| P8 | Nav hover color shift, 180–250ms | B |
| P9 | Dropdown chevron — no dropdowns in IA | S |
| P10 | Card emphasis: translateY −4px + border brighten, 250ms (hover AND focus-within) | B |
| P11 | Directory-row highlight — no directory module; nearest pattern is plan-card row hover | S |
| P12 | Focus ring per token, 100ms, never removed | B |
| P13 | Variable-font weight shift — system stacks only, no variable axis | S |
| P14 | Video-thumbnail hover preview — media-free build | S |

**Scroll**

| ID | Effect & spec | D |
|---|---|---|
| S1 | Fade-and-rise reveal once at 80–85% viewport: 24–40px, 450ms `--ease-reveal` | B |
| S2 | Staggered group reveals, 70ms step | B |
| S3 | H2 line-mask reveal (whole-line, 600ms expo) | B |
| S4 | Frame entrance: opacity + scale .96→1 + blur 8px→0, 700ms expo (workflow shell, showcase frames) | B |
| S5 | Parallax on showcase frames, translateY ±8%, scrubbed | B |
| S6 | Layered parallax inside workflow panel (doc-stack layers drift at different rates) | B |
| S7 | Scroll-scrubbed motion: hero field morph + contact arcs rotate with scroll | B |
| S8 | Traveling sine accent: contact arcs shift with sine offset while scrolling | B |
| S9 | Pinned chapters = the 200svh sticky hero two-phase; no other pinning (scroll-jack risk) | A |
| S10 | 2px top scroll-progress bar, scaleX 0→1, hidden under reduced motion | B |
| S11 | Active nav indicator slides under current section (scrollspy), 250ms | B |
| S12 | Header surface change past 8px: background alpha + blur 16px + hairline, 250ms | B |
| S13 | Scroll-cue fade-out past hero top, 250ms | B |
| S14 | Smooth scrolling = CSS `scroll-behavior:smooth` + `scroll-padding-top` (not reduced); never hijack wheel/touch | A |
| S15 | Anchor jumps with focus moved to target (`tabindex="-1"`), 400–650ms | B |
| S16 | Docs TOC tracking — no docs module | S |

**Carousels, tabs, stages**

| ID | Effect & spec | D |
|---|---|---|
| C1 | Showcase rail: scroll-snap + drag + arrows + keyboard; programmatic travel 400–650ms ease-in-out | B |
| C2 | Active card emphasis: scale 1 vs .92, opacity 1 vs .6, 450ms | B |
| C3 | Peeking neighbors + edge fade mask (`mask-image`) | B |
| C4 | Arrow states: hover/press/disabled-at-ends, 150ms | B |
| C5 | Rail progress fill, scaleX, 450ms | B |
| C6 | Auto-rotate — OFF by design: no unsolicited motion; users drive everything | S |
| C7 | Stage indicator slide, 250–400ms | B |
| C8 | Stage panel cross-fade + translateY 16px, 450ms, stable reserved height (CLS 0) | B |
| C9 | Oversized stage watermark word (RESEARCH/OPERATIONS/CREATIVE) mask-slides, 600ms expo | B |
| C10 | Use-case switcher cross-fade — satisfied by C8 (same mechanism) | A |
| C11 | Showcase selector — merged into C1 arrows + card activation | A |
| C12 | Plan cards: entrance stagger 70ms + hover border emphasis | B |
| C13 | FAQ: button + `aria-expanded`, `grid-template-rows` 0fr→1fr, 300ms; SVG plus rotates 45° | B |
| C14 | Code/docs tabs — no code content | S |

**Overlays & feedback**

| ID | Effect & spec | D |
|---|---|---|
| O1 | Mobile menu: fade+slide 400–550ms expo, backdrop, 40ms link stagger; Esc + link-click close; focus moves in and returns | B |
| O2 | Cmd+K search — unnecessary on a one-page concept site | S |
| O3 | Modal = the demo dialog: scale .96→1 + opacity, backdrop `blur(24px)` + scrim, 250–350ms expo, full focus management | A |
| O4 | Dropdown panel — no dropdowns in IA | S |
| O5 | "Copied!" toast: 200ms in · 1.6s hold · 200ms out, `aria-live="polite"` | B |
| O6 | Tooltips on icon-only controls (arrows, mode toggle, pause): 120ms, 300ms delay, shown on focus too | B |

**Media (media-free build — no `<video>`, no raster images)**

| ID | Effect & spec | D |
|---|---|---|
| M1 | Poster-to-video crossfade — no `<video>` in this build | S |
| M2 | Custom video controls auto-hide — no video | S |
| M3 | Play-button hover — no video | S |
| M4 | Lazy video start / offscreen pause — impossible without video; intent covered by the field's static fallback + visible Pause control + no autoplay of anything | S |
| M5 | Blur-up reveal on showcase frames (blur 16px→0, opacity, 400ms) on first reveal | A |
| M6 | Frame fade-in with reserved `aspect-ratio` (CLS 0), 200ms | A |

**Text & data**

| ID | Effect & spec | D |
|---|---|---|
| T1 | Per-character stagger (mechanics of L1) on hero + one section heading | B |
| T2 | Whole-line reveal on section H2s (mechanics of S3) | B |
| T3 | Typewriter — redundant with T1/L1; one text language only | S |
| T4 | Count-up — forbidden here: only verified numbers may animate, and this build shows none | S |
| T5 | Staged status in demo dialog: "Preparing example…" → "Example ready — nothing was sent", 150ms swaps, `aria-live` | B |

**Page, route & state**

| ID | Effect & spec | D |
|---|---|---|
| R1 | Same-document View Transitions (feature-detected `startViewTransition`) wrap stage swap + filter changes, ~150ms crossfade; instant where unsupported | A |
| R2 | Shared-element morph across routes — no routes | S |
| R3 | Persistent header (one sticky header) | B |
| R4 | Subchapter transition = hero two-phase (S9) + stage watermark (C9) previewing next content | B |
| R5 | FLIP reflow on showcase filter chips, 300ms `--ease-primary` | B |
| R6 | Filter empty state: "Nothing here yet — try another filter." card, 200ms | B |
| R7 | Skeleton shimmer — nothing loads async | S |
| R8 | Fake loading spinner — forbidden by honesty rules; T5 covers staged feedback | S |
| R9 | Form success stroke draw — no forms: no real submission service, so none is faked | S |
| R10 | Form error styling — no forms (same reason as R9) | S |
| R11 | Motion On/Off + mode toggles: thumb translateX, 150ms | B |
| R12 | Mode toggle indicator slide + spring retarget of the field | B |
| R13 | Theme switch — ONE coherent dark theme by design | S |
| R14 | Demo dialog Replay control re-runs the staged status sequence, 250ms | A |
| R15 | SVG stroke draw: bridge line, contact arcs, orbit rings on reveal, 600–900ms `--ease-primary` | B |
| R16 | Copy-logo label swap "Copy logo as SVG" → "Copied!" (with O5), 200ms | B |
| R17 | Language selector — English only; no real translations may be faked | S |

**Tally: 59 build · 11 adapted · 23 skipped (each with a printed reason).**

## 9 · STYLE CATALOG

Surfaces (canvas / raised / alt / overlay) from tokens · hairline 1px borders, brighter on hover & selection, list dividers between rows · radius scale per tokens (media 14–24px, big panels ≤36px, controls pill) · shadows only on menu, dialog, toast · blur: header glass 16px, dialog backdrop 24px, diffuse 16px · scrims behind hero copy and any busy field · atmosphere glow in 2–3 chapters only · edge-fade masks on rails · `scroll-snap-type` on rails with `scroll-padding` · buttons: filled paper pill (primary), outlined pill (secondary), text link, circular arrow button, segmented control, icon toggle — heights 40–48px, touch targets ≥44px · cards share one radius/border grammar (media card, capability card, plan card, frame, caption panel) · chips: filter + example/illustrative badges with selected state · inputs: none (no forms) · icons: one inline SVG set, 1.5px stroke, rounded caps, `currentColor` · checkmarks and plus/minus are SVG, never text glyphs · tooltip/toast/empty-state styles · `cursor:pointer` on interactive, default elsewhere · `::selection` mint on charcoal · thin themed `scrollbar-color`, never hidden · `color-scheme: dark`, `theme-color #0a1011`, inline SVG favicon (three wavy lines on `#0a1011`, rounded 16) as data URI · z-scale per tokens · minimal print stylesheet (hide canvas/banner/buttons).

## 10 · STATE MATRIX

Every interactive component implements and reports: default · hover (fine pointers only) · focus-visible · active/pressed · selected/current · disabled · loading/error where meaningful · success. Components: buttons, links, nav links, tabs, cards, chips, toggles, accordion triggers, carousel arrows, dialog controls, mode/pause toggles. **Hover never carries information that focus does not also carry.** Where no async exists (this build), define success/empty paths instead of fake loading states — and say so in the report.

## 11 · ACCESSIBILITY — WCAG 2.2 AA

Semantic landmarks + skip link (`Skip to content`) · one H1, ordered headings · full keyboard journey: menu, tabs (roving tabindex + Arrow/Home/End), carousel arrows, accordion, dialog (focus trap, Esc, return focus), toggles · visible `--focus-ring` everywhere, never clipped · canvas and all decorative art `aria-hidden`; fallback layer too · dialog uses native `<dialog>` + backdrop click close · FAQ = buttons + `aria-expanded` + labelled regions · carousel = labelled region, labelled slides/controls, keyboard operable, no auto-advance · autonomous motion has a visible Pause control · status changes announced via `aria-live` (toast, T5, mode change) · `inert` on hidden hero copy · contrast per §3 including over scrims · hit targets ≥44px · no focus traps outside the dialog · no flashing >3/s, no forced audio, no parallax that impairs reading · works at 200% zoom and with `prefers-reduced-motion` honored from first render **and live** (static field frame, reveals instant, pinning released, cue static, toggles still give state feedback).

## 12 · RESPONSIVE — verify logic at 320 / 360 / 390 / 768 / 1024 / 1280 / 1440 / 1920

Fluid `clamp()` typography; 12-col desktop feel with `--content-max:1360px`; gutters shrink on tablet/mobile. **320/390:** no horizontal clipping anywhere (rails may scroll internally only); H1/sub/CTA visible on first screen; hero copy `max-width:calc(100% - 48px)`; mobile menu with primary CTA still visible; field below/behind headline with fewer particles; bridge becomes vertical. **768:** stack split layouts, don't shrink both columns. **1024–1920:** alternating stage layouts, generous negative space; `--pad:max(100px,calc((100vw - 1600px)/2))` above 1800px. Recompose collages to simple stacks on mobile; keep rails swipeable with visible arrows; safe-area insets; short-landscape fallback (hero min-height 600px, copy raised); no hover-only information; 44px targets on touch.

## 13 · PERFORMANCE · SEO · SECURITY · HONESTY

**Perf:** content renders before any JS effect (nothing hidden pre-`.has-js`); LCP = the H1, never gated on the engine; only transform/opacity animated; `will-change` sparingly; passive listeners; observers/listeners cleaned up; engine pauses offscreen/hidden; CLS 0 (canvas absolute, reserved panel heights, aspect-ratio frames); no long tasks at init (chunk heavy setup across frames). Targets: Lighthouse ≥90 all categories, LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 — report measured numbers if you can measure, otherwise write "not measured in this environment". **SEO:** `<title>Flux · Intelligence in motion</title>`, meta description, `theme-color`, favicon, Open Graph title/description (no image — no external assets), lang="en", one H1, indexable copy for everything shown. Canonical only if a real URL exists — otherwise omit and say so. **Security & honesty:** no secrets, no fake auth/billing/metrics/testimonials/clients/certs; every CTA does exactly what it says (the only "conversion" is a truthful demo dialog); simulated outputs labeled; "Connect your own booking/signup/contact service before launching" appears in the FAQ and dialog; no invented accessibility/performance claims; analytics omitted (no consent mechanism) — noted in report.

## 14 · BUILD ORDER

1. Skeleton: doctype, meta, favicon, tokens, reset, base a11y (skip link, focus styles, `noscript` note, `.has-js` gating).
2. Header + banner + mobile menu + scrollspy.
3. Hero structure: copy, journey copy, counter, cue, fallback layer, canvas mount, pause control.
4. Particle engine (§6) — correct before anything else uses it.
5. Sections in DOM order (§2 acts 3–10) with SVG art.
6. Demo dialog + toast + copy-logo + motion toggle.
7. Effects pass in catalog order: L → A → P → S → C → O → M → T → R.
8. §5B edit pass over every string in the file (findings, smallest repairs, rubric score ≥32/40); stamp the CSS decision comment.
9. Reduced-motion pass, no-JS pass, engine-failure pass (force each: `.engine-failed`, media query, JS off) — fix, re-verify.
10. Responsive pass across all 8 widths.
11. Run §15, then write §16.

## 15 · SELF-VERIFICATION — run every line before answering

- File opens by double-click with zero console errors; single HTTP request (itself).
- Every anchor, CTA, tab, filter, arrow, accordion, toggle, dialog works — with keyboard only.
- Hero: field animates on load; scroll advances and **reverses continuously**; two-phase copy swap at the right progress; counter fills; no cuts.
- Kill-switches each verified: reduced motion (static field, instant reveals, no pin), JS disabled (all content readable), engine failed (fallback visible, nothing lost).
- No horizontal overflow at 320/390/1440; CTA visible on first screen; focus ring visible on every control; toast/status announced; contrast of muted text holds.
- No placeholders, no truncation, no invented claims; every EXAMPLE label present; year auto-set.
- Coverage audit table complete: 59 B built · 11 A adapted · 23 S skipped with reasons.
- Slop audit (§5B): zero banned constructions in any copy or report sentence; em-dash count is zero; prose scores ≥32/40 on the 8-point rubric with no criterion below 3; the only recorded Reflex overrules are the three brand devices.
- Hero reviewed cold after build; CSS decision comment present at the top of `<style>`.

## 16 · FINAL REPORT FORMAT (after the code)

1. What was built (sections, engine summary). 2. Coverage table: every ID → B/A/S + one-line status + where it appears. 3. Reduced-motion + no-JS + failure-fallback results. 4. Tokens/values you tuned from starting values, and why. 5. Known limitations (system fonts, no video, single page). 6. Customization map: brand → §2/Copy Bank · colors → §3 · hero → §6 · workflows → §2 table · connecting real services → FAQ/dialog copy. 7. Verification results per §15 line (pass / not run + why).
8. Slop pass (§5B): findings fixed, final rubric score /40, and the recorded overrules.

## 17 · ANTI-PATTERNS — instant fail

Gradients or glows in every section · piles of glass cards, particles behind body text, cursor followers, scroll hijacking beyond the designed hero pin · tiny or low-contrast text · hero motion with no poster/fallback/pause · identical side-by-side feature grids · carousel with no visible controls · fake data of any kind · dead CTAs · decorative animation that explains nothing · truncated file · hover-only affordances · focus traps · horizontal scroll bugs · AI-slop copy: throat-clearing, "not X but Y", significance inflation, punchy closers, moralizing codas, jargon · replacing the procedural field with a static gradient "because it looks the same".

## 18 · PRIORITY ORDER & RULES OF THUMB

Product correctness & user goals → accessibility & security → functionality & content accuracy → responsive usability → performance → visual/motion fidelity → decoration. Rules: CSS when a library isn't needed (none is allowed anyway); Canvas 2D beats WebGL for a dependency-free build; keep native scroll; simplify any headline effect that hurts accessibility; cut effects that hurt performance; keep one identity, imitate no one; never fake functionality to satisfy a checklist.

## APPENDIX A — signature scene variants (documentation ONLY — build ONLY the §6 river)

The Webbzer family's ten signature heroes share this engine's DNA (procedural, scroll-scrubbed camera, continuous scene, fallbacks). If the user later names one, swap the scene function behind the same interface (`update({time, progress, pointer, mobile})`):

1. **River** (Flux, pinned): folded particle sheet, charcoal + mint — AI workflow.
2. **Field** (Field): electric-blue particle landscape that breathes and orbits — research lab.
3. **Contours** (Signal): stacked orange/magenta sound curves, depth opens on scroll — music tech.
4. **Terrain** (Strata): terracotta contour bands separating into a valley — data intelligence.
5. **Vortex** (Tidal): aqua streamlines spiraling around an open vortex — climate tech.
6. **Grids** (Phase): cobalt curved grids shearing into interference — creative studio.
7. **Cubes** (Lattice): coral/graphite instanced cubes assembling into stepped planes — developer platform.
8. **Folds** (Aura): translucent peach/lilac surfaces folding and breathing — wellbeing.
9. **Braid** (Prismatic): spectral filaments forming a braided loop that opens on scroll — design studio.
10. **Isosurface** (Bloom): metaballs joined by marching cubes into a perforated organic form — innovation studio.

Do not implement any variant now. Do not treat this appendix as a work item.
