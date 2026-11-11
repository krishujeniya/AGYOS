# Procedural Canvas 2D Physics & Hero Engines

Synthesized from the Webbzer engine specifications. Delivers dependency-free, high-performance Canvas 2D procedural background scenes with delta-time normalization, scroll-scrubbed camera paths, interactive pointer physics, and adaptive performance fallbacks.

---

## 1. Core Engine Architecture

Every procedural scene implements a unified lifecycle interface:
- `init(canvasElement, options)`: DPR configuration, offscreen sprite caches, event listener binding.
- `update({ time, deltaTime, progress, pointer, isMobile })`: Numerical physics step, spatial morphing, camera projection.
- `render(context)`: Batch draw operations, compositor blending.
- `dispose()`: Cancel `requestAnimationFrame`, disconnect observers, remove listeners, clear memory buffers.

---

## 2. The Folded Particle River (Flux Signature Engine)

### Canvas & Layer Composition
- **Resolution & DPR**: Device pixel ratio capped at 1.75 on desktop, 1.5 on mobile devices (`dpr = Math.min(window.devicePixelRatio || 1, isMobile ? 1.5 : 1.75)`).
- **Static Dust Layer**: 650 subtle background dust dots pre-rendered once to an offscreen canvas at opacity 0.38, composited with a single `drawImage` call per frame.
- **Dynamic Particle Count**: Exactly 88 particles on desktop, 44 on mobile viewports.
- **Particle State Tuple**:
  - `x, y`: Current coordinates.
  - `vx, vy`: Current velocity vector.
  - `homeX, homeY`: Calculated home coordinate along the ribbon path.
  - `depth`: Depth scale factor (0.4 to 1.2) controlling size, opacity, and blur simulation.
  - `size`: Base particle radius scaled by depth.
  - `rotation, vRot`: Current angle and angular velocity.
  - `color`: Mixed interpolation from paper-white (`#eff3eb`) to mint (`#cee5d3`).
  - `opacity`: Base alpha (0.3 to 0.9) modulated by depth and edge distance.
  - `seed`: Particle-specific deterministic hash controlling phase offsets.

### Ribbon Parametric Equations
Home positions trace a smooth, folded ribbon across normalized coordinate `u ∈ [0, 1]`:
```javascript
const foldPhase = Math.sin(time * 0.13);
const ribbonX = cx + Math.sin(u * 7.0 - 0.8) * spread + across * width * Math.cos(foldPhase);
const ribbonY = u * span - yOffset;
```
- **Strand Dispersion**: Approximately 8% of particles are offset outward as peripheral wisps (`seed.z > 0.92`).
- **Edge Attenuation**: Particle opacity attenuates at path endpoints using a smoothstep curve over `u`.
- **Traveling Filament**: A brightened localized highlight wave traverses the ribbon path continuously.

### Physics & Interaction Mechanics
- **Delta-Time Normalization**: All motion scales strictly by elapsed seconds (`dt`), preventing speed fluctuations across 60Hz, 120Hz, and 144Hz displays.
- **Organic Drift**: Harmonic oscillation calculated as `Math.sin(time * freq + phase)` per particle.
- **Negative Gravity**: Steady upward drift (−0.06 to −0.12 pixels per millisecond).
- **Velocity Damping**: Multiplicative velocity decay of 0.95 per physics tick.
- **Pointer Repulsion**:
  - Repel radius: 120px desktop, 90px mobile.
  - Force: Smooth inverse-distance repulsion applied passively.
  - Touch devices: Pointer repulsion is bypassed on touch to preserve native scrolling ergonomics.
- **Orbital Mode Transition**:
  - Spring tension: 0.06.
  - Friction: 0.82.
  - Smoothly re-targets particles from ribbon coordinates into concentric circular halo formations without visual discontinuity.

### Scroll Morphing & Reverse Continuity
- Scroll progress calculation:
  ```javascript
  const rawProgress = -heroRect.top / (heroHeight - stickyHeight);
  const progress = Math.min(Math.max(rawProgress, 0), 1);
  ```
- Progression smoothing: Exponential moving average via `progressSmoothed += (progress - progressSmoothed) * (1 - Math.exp(-dt * 8))`.
- As progress increases from 0.0 to 1.0:
  - Particles lerp toward structured ribbon targets (`0.65 * smoothstep(0.1, 0.95, progress)`).
  - Spatial turbulence roughness halves.
  - Layer coordinates rotate by `−0.13 * progress`.
- **Reversibility**: Upward scrolling perfectly unwinds the field back to its unconstrained drifting state.

### Sparkle Sprites
- 1.3% of particles are flagged as sparkles.
- Rendered using an offscreen pre-drawn radial gradient sprite.
- Composited with `ctx.globalCompositeOperation = 'lighter'` and gentle twinkle alpha modulation.

### Performance Guardrails & Failure Modes
- **Offscreen & Tab Visibility**: Pauses execution immediately via `document.hidden` listener and an `IntersectionObserver` on the hero element (rootMargin: 100px).
- **Adaptive Frame Rate Throttling**:
  - If frame render time exceeds 35ms across consecutive checks:
    1. Reduce DPR scale by 25% (minimum floor 1.0).
    2. Reduce particle count by 25% (minimum floor 40).
    3. If frame drops persist, pause engine and apply `.engine-failed` CSS fallback.
- **CSS Graceful Degradation (`.engine-failed`)**:
  - Three layered, rotated soft-bordered ellipses with blur and mint tinting.
  - Page layout, typography, and interactive controls remain fully functional.
- **Accessibility (`prefers-reduced-motion`)**:
  - Engine freezes loop immediately; renders a single static composition at `progress = 0`.
  - Removes pointer repulsion listeners.
  - Listens to live media query updates.
- **Autonomous Motion Pause Button**:
  - Visible control with `aria-pressed` state that freezes the canvas animation loop on demand.

---

## 3. The 10 Webbzer Signature Scene Variants

All Webbzer scenes adhere to the identical `update({ time, deltaTime, progress, pointer, isMobile })` interface:

| # | Variant | Visual Character | Color Palette | Target Domain |
|---|---|---|---|---|
| 1 | **River** *(Default)* | Folded particle sheet with smooth sine ribbons | Deep charcoal `#0a1011` + quiet mint `#cee5d3` | AI workflow platforms, executive tools |
| 2 | **Field** | Breathing, undulating particle lattice orbiting on scroll | Obsidian `#080c10` + electric cobalt `#2a69ff` | Deep research labs, scientific computing |
| 3 | **Contours** | Stacked topographic sound frequency curves that open in 3D | Onyx `#0d0d0d` + orange `#ff5a1f` / magenta `#d91a7a` | Audio synthesis, acoustic AI platforms |
| 4 | **Terrain** | Terracotta elevation lines separating into a central valley | Umber `#140f0d` + terracotta `#d96b43` / sand `#f2d6bd` | Geospatial intelligence, data infrastructure |
| 5 | **Vortex** | Fluid streamlines spiraling around an open eye | Midnight `#040d12` + aqua `#1dd1a1` / seafoam `#a8ffeb` | Climate tech, fluid mechanics, oceanics |
| 6 | **Grids** | Curved coordinate grids shearing into interference patterns | Navy `#060b18` + ultramarine `#3867d6` / white | Creative architecture, design tooling |
| 7 | **Cubes** | Instanced isometric cubes assembling into stepped planes | Graphite `#121214` + coral `#ff6b6b` / cream `#f7f1e3` | Developer infrastructure, cloud systems |
| 8 | **Folds** | Translucent organza-like planes breathing with slow phase | Espresso `#100b0d` + peach `#ffbe76` / lilac `#e056fd` | Wellbeing, restorative software, health tech |
| 9 | **Braid** | Intertwined spectral filaments opening into an infinity loop | Jet `#0a0a0a` + spectral dispersion / gold `#f6b93b` | High craft design studios, luxury editorial |
| 10 | **Isosurface** | Organic metaball contours evaluated across a 2D scalar field | Pitch `#050505` + phosphor emerald `#00d2d3` / pearl | Biotech, materials science, innovation labs |
