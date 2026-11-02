# Phase 4B: Code Generation Rules

> The technical specification for generating ScrollHeart sites.
> Used alongside `04-scene-templates.md` during Phase 4.
> All code must be static, mobile-first, and GitHub Pages ready.

---

## File Structure

Generate exactly this structure:

```
scrollheart-story/
├── index.html          # 5 scenes, 4 layers each, semantic HTML
├── css/
│   └── style.css       # Mobile-first, design tokens, reduced-motion
├── js/
│   └── main.js         # GSAP timelines, ScrollTrigger, audio controller
├── assets/             # Optional: user-provided audio or images
│   └── (empty by default)
└── .nojekyll           # Bypass Jekyll on GitHub Pages
```

### AI Generation Workflow (CRITICAL)
- **Do not generate all files at once.** The CSS and JS files are large and will likely hit your output token limit if generated together.
- Generate `index.html` first. Ask the user for confirmation.
- Generate `css/style.css` next. Ask the user for confirmation.
- Generate `js/main.js` last.

### Asset Bloat Prevention
- If the user provides an audio file (`music.mp3`), explicitly instruct them to compress it to under **1MB** (e.g., 128kbps or lower) before adding it to the `assets/` folder. Large audio files will destroy mobile performance and scrolling smoothness.

---

## HTML Structure (`index.html`)

### Document Head

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <meta name="description" content="A story for you.">
  <title>A Story for You</title>

  <!-- Fonts (from design brief) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family={display_font}:wght@300;400;600&family={body_font}:wght@300;400;600&display=swap" rel="stylesheet">

  <!-- Styles -->
  <link rel="stylesheet" href="css/style.css">
</head>
```

**Head rules:**
- Always include `noindex, nofollow` meta
- NO social media meta tags (no `og:title`, no `twitter:card`)
- NO analytics scripts
- NO favicon link (keep it anonymous)
- Generic title — never include her name

### Document Body Structure

```html
<body>
  <!-- Audio Consent Overlay -->
  <div id="intro-overlay" class="overlay" role="dialog" aria-label="Begin the story">
    <div class="overlay-content">
      <p class="overlay-subtitle">I made something for you</p>
      <h1 class="overlay-title">A little story</h1>
      <button id="begin-btn" class="begin-button" aria-label="Begin the story">
        Begin
      </button>
      <p class="overlay-hint">🔊 Best with sound on</p>
    </div>
  </div>

  <!-- Audio Toast Notification -->
  <div id="audio-toast" class="audio-toast hidden" aria-live="polite">
    Audio blocked by browser — tap the 🔇 icon to try again.
  </div>

  <!-- Audio Element -->
  <audio id="bg-audio" preload="none" loop>
    <source src="assets/music.mp3" type="audio/mpeg">
  </audio>

  <!-- Audio Controls (visible after overlay dismissed) -->
  <div id="audio-controls" class="audio-controls" aria-label="Audio controls">
    <button id="audio-toggle" class="audio-btn" aria-label="Toggle audio">
      <span class="audio-icon">🔊</span>
    </button>
  </div>

  <!-- Main Content -->
  <main>
    <!-- Scene 1: The First Glance -->
    <section id="scene-1" class="scene" aria-label="Scene 1: The beginning">
      <div class="bg-layer"></div>
      <div class="mid-layer"></div>
      <div class="fg-layer"></div>
      <div class="text-layer">
        <h2 class="scene-text">{scene_1_text}</h2>
      </div>
    </section>

    <!-- Scene 2: The Silent Conversation -->
    <section id="scene-2" class="scene" aria-label="Scene 2: A memory">
      <div class="bg-layer"></div>
      <div class="mid-layer"></div>
      <div class="fg-layer"></div>
      <div class="text-layer">
        <p class="scene-text">{scene_2_text}</p>
      </div>
    </section>

    <!-- Scene 3: The Climax -->
    <section id="scene-3" class="scene" aria-label="Scene 3: The heart of the story">
      <div class="bg-layer"></div>
      <div class="mid-layer"></div>
      <div class="fg-layer"></div>
      <div class="text-layer">
        <div class="climax-card">
          <p class="scene-text scene-text--climax">{scene_3_text}</p>
        </div>
      </div>
    </section>

    <!-- Scene 4: Quiet Night -->
    <section id="scene-4" class="scene" aria-label="Scene 4: A quiet moment">
      <div class="bg-layer"></div>
      <div class="mid-layer"></div>
      <div class="fg-layer"></div>
      <div class="text-layer">
        <p class="scene-text">{scene_4_text}</p>
      </div>
    </section>

    <!-- Scene 5: Outro & CTA -->
    <section id="scene-5" class="scene scene--outro" aria-label="Scene 5: The end">
      <div class="bg-layer"></div>
      <div class="mid-layer"></div>
      <div class="fg-layer"></div>
      <div class="text-layer">
        <p class="scene-text">{scene_5_text}</p>
        <button id="replay-btn" class="replay-button" aria-label="Replay the story">
          ↻ Replay
        </button>
        <p class="signature">{signature}</p>
      </div>
    </section>
  </main>

  <!-- Scripts -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
```

**Body rules:**
- The overlay is the first thing the user sees — it gates audio playback
- Audio element has `preload="none"` — don't load until user clicks Begin
- Audio controls appear only AFTER the overlay is dismissed
- Each section has 4 layer divs in order: bg, mid, fg, text
- Scene 3 has a `.climax-card` wrapper for glassmorphism effect
- Scene 5 has the replay button and optional signature
- GSAP loaded from CDN at the bottom (not in head)
- NO jQuery, NO other libraries

---

## CSS Rules (`css/style.css`)

### Design Tokens (Custom Properties)

```css
:root {
  /* Colors from design brief */
  --color-primary: {primary};
  --color-background: {background};
  --color-accent: {accent};
  --color-text: {text};

  /* Typography */
  --font-display: '{display_font}', cursive;
  --font-body: '{body_font}', sans-serif;

  /* Spacing */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 4rem;
  --space-xl: 8rem;

  /* Scene Heights */
  --scene-height-intro: 300svh;
  --scene-height-verse: 200svh;
  --scene-height-chorus: 250svh;
  --scene-height-bridge: 150svh;
  --scene-height-outro: 100svh;
}
```

### Critical Global Styles

```css
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  overflow-x: clip;
  scroll-behavior: auto; /* NEVER use smooth — conflicts with GSAP */
}

body {
  overflow-x: clip;
  font-family: var(--font-body);
  color: var(--color-text);
  background-color: var(--color-background);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Section and Layer Styles

```css
.scene {
  position: relative;
  width: 100%;
  min-height: 100svh;
  overflow: hidden;
}

#scene-1 { height: var(--scene-height-intro); }
#scene-2 { height: var(--scene-height-verse); }
#scene-3 { height: var(--scene-height-chorus); }
#scene-4 { height: var(--scene-height-bridge); }
#scene-5 { height: var(--scene-height-outro); }

.bg-layer,
.mid-layer,
.fg-layer,
.text-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.bg-layer,
.mid-layer,
.fg-layer {
  will-change: transform;
  pointer-events: none;
}

.text-layer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-md);
  z-index: 4;
}
```

### Typography Styles

```css
.scene-text {
  font-family: var(--font-display);
  font-size: clamp(1.25rem, 5vw, 2.5rem);
  font-weight: 300;
  line-height: 1.4;
  text-align: center;
  max-width: min(90%, 600px);
  opacity: 0; /* Hidden until GSAP reveals */
}

.scene-text--climax {
  font-size: clamp(1.5rem, 6vw, 3rem);
  font-weight: 400;
}

.signature {
  font-family: var(--font-body);
  font-size: 0.875rem;
  letter-spacing: 0.2em;
  opacity: 0.6;
  margin-top: var(--space-lg);
}
```

### Overlay Styles

```css
.overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background);
  transition: opacity 0.8s ease, visibility 0.8s ease;
}

.overlay.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.overlay-content {
  text-align: center;
  padding: var(--space-md);
}

.overlay-subtitle {
  font-family: var(--font-body);
  font-size: 0.875rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  opacity: 0.6;
  margin-bottom: var(--space-sm);
}

.overlay-title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 8vw, 4rem);
  font-weight: 300;
  margin-bottom: var(--space-lg);
}

.begin-button {
  font-family: var(--font-body);
  font-size: 1rem;
  letter-spacing: 0.1em;
  padding: var(--space-sm) var(--space-lg);
  border: 1px solid var(--color-primary);
  border-radius: 50px;
  background: transparent;
  color: var(--color-primary);
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.begin-button:hover,
.begin-button:focus-visible {
  background-color: var(--color-primary);
  color: var(--color-background);
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.overlay-hint {
  font-size: 0.75rem;
  opacity: 0.4;
  margin-top: var(--space-md);
}
```

### Climax Card (Glassmorphism)

```css
.climax-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: var(--space-lg);
  max-width: min(90%, 500px);
}
```

### Audio Controls

```css
.audio-controls {
  position: fixed;
  bottom: var(--space-md);
  right: var(--space-md);
  z-index: 50;
  opacity: 0;
  transition: opacity 0.5s ease;
}

.audio-controls.visible {
  opacity: 1;
}

.audio-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  transition: border-color 0.3s ease;
  padding-bottom: env(safe-area-inset-bottom);
}

.audio-btn:hover {
  border-color: var(--color-primary);
}
```

### Replay Button

```css
.replay-button {
  font-family: var(--font-body);
  font-size: 0.875rem;
  letter-spacing: 0.15em;
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-primary);
  border-radius: 50px;
  background: transparent;
  color: var(--color-primary);
  cursor: pointer;
  margin-top: var(--space-lg);
  animation: heartbeat 2s ease-in-out infinite;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 rgba(222, 161, 147, 0); }
  50% { transform: scale(1.05); box-shadow: 0 0 20px rgba(222, 161, 147, 0.2); }
}
```

### Reduced Motion Fallback

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .bg-layer,
  .mid-layer,
  .fg-layer {
    will-change: auto;
    transform: none !important;
  }

  .scene-text {
    opacity: 1 !important;
    transform: none !important;
  }

  .scene {
    height: auto !important;
    min-height: 100svh;
  }
}
```

### Mobile-First Responsive

```css
/* Base: 320px+ (mobile first) */
/* Already defined above */

/* Tablet: 768px+ */
@media (min-width: 768px) {
  .scene-text {
    font-size: clamp(1.5rem, 4vw, 3rem);
  }

  .overlay-title {
    font-size: clamp(2.5rem, 6vw, 5rem);
  }

  .climax-card {
    padding: var(--space-xl);
  }
}

/* Safe area insets for notched phones */
@supports (padding: env(safe-area-inset-top)) {
  body {
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);
  }
}
```

---

## JavaScript Rules (`js/main.js`)

### Overall Structure

```javascript
// js/main.js

(function () {
  'use strict';

  // ============================================
  // 1. GSAP Setup
  // ============================================
  gsap.registerPlugin(ScrollTrigger);

  // ============================================
  // 2. Reduced Motion Check
  // ============================================
  const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
  ).matches;

  // ============================================
  // 3. Overlay & Audio Controller
  // ============================================
  // (see Audio Controller section below)

  // ============================================
  // 4. Scene Animations (skip if reduced motion)
  // ============================================
  if (!prefersReducedMotion) {
    initParallaxAnimations();
    initTextAnimations();
  } else {
    // Show all text immediately
    document.querySelectorAll('.scene-text').forEach(el => {
      el.style.opacity = '1';
    });
  }

  // ============================================
  // 5. Cleanup
  // ============================================
  window.addEventListener('beforeunload', () => {
    ScrollTrigger.getAll().forEach(t => t.kill());
  });

})();
```

### Audio Controller

```javascript
const overlay = document.getElementById('intro-overlay');
const beginBtn = document.getElementById('begin-btn');
const audio = document.getElementById('bg-audio');
const audioControls = document.getElementById('audio-controls');
const audioToggle = document.getElementById('audio-toggle');
const audioIcon = audioToggle.querySelector('.audio-icon');
let isPlaying = false;

// Begin button — gate for audio
beginBtn.addEventListener('click', () => {
  overlay.classList.add('hidden');
  audioControls.classList.add('visible');

  // Attempt to play audio
  audio.volume = 0.5;
  audio.play()
    .then(() => {
      isPlaying = true;
      audioIcon.textContent = '🔊';
    })
    .catch(() => {
      // Audio failed to load — degrade gracefully
      isPlaying = false;
      audioIcon.textContent = '🔇';
    });
});

// Audio toggle
audioToggle.addEventListener('click', () => {
  if (isPlaying) {
    audio.pause();
    isPlaying = false;
    audioIcon.textContent = '🔇';
  } else {
    audio.play()
      .then(() => {
        isPlaying = true;
        audioIcon.textContent = '🔊';
      })
      .catch(() => {
        audioIcon.textContent = '🔇';
      });
  }
});

// Replay button
const replayBtn = document.getElementById('replay-btn');
if (replayBtn) {
  replayBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    ScrollTrigger.refresh();
  });
}
```

### Parallax Animations

```javascript
function initParallaxAnimations() {
  // Use matchMedia for responsive breakpoints
  const mm = gsap.matchMedia();

  mm.add('(min-width: 1px)', () => {
    // Background layers — slowest
    gsap.utils.toArray('.bg-layer').forEach(layer => {
      gsap.to(layer, {
        yPercent: -15,
        ease: 'none',
        scrollTrigger: {
          trigger: layer.parentElement,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        },
      });
    });

    // Midground layers — moderate
    gsap.utils.toArray('.mid-layer').forEach(layer => {
      gsap.to(layer, {
        yPercent: -8,
        ease: 'none',
        scrollTrigger: {
          trigger: layer.parentElement,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        },
      });
    });

    // Foreground layers — fastest
    gsap.utils.toArray('.fg-layer').forEach(layer => {
      gsap.to(layer, {
        yPercent: 10,
        ease: 'none',
        scrollTrigger: {
          trigger: layer.parentElement,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        },
      });
    });
  });
}
```

### Text Animations

```javascript
function initTextAnimations() {
  gsap.utils.toArray('.scene-text').forEach(text => {
    gsap.from(text, {
      y: 30,
      opacity: 0,
      duration: 1.5,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: text,
        start: 'top 80%',
        end: 'top 50%',
        toggleActions: 'play none none reverse',
      },
    });
  });

  // Climax card special animation
  const climaxCard = document.querySelector('.climax-card');
  if (climaxCard) {
    gsap.from(climaxCard, {
      scale: 0.9,
      opacity: 0,
      duration: 1.8,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: climaxCard,
        start: 'top 75%',
        toggleActions: 'play none none reverse',
      },
    });
  }
}
```

### GSAP Best Practices Checklist

- ✅ Register ScrollTrigger plugin once at the top
- ✅ Create ScrollTriggers in DOM order (top to bottom)
- ✅ Use `scrub` for parallax, `toggleActions` for text reveals — never both on the same trigger
- ✅ Use `ease: "none"` for scrub-linked parallax
- ✅ No `markers: true` in production
- ✅ Kill all ScrollTriggers on `beforeunload`
- ✅ Check `prefers-reduced-motion` before creating any animations
- ✅ Use `gsap.matchMedia()` for responsive breakpoints
- ✅ Animate ONLY `transform` and `opacity` — never `width`, `height`, `top`, `left`
- ✅ Apply `will-change: transform` via CSS on animated layers
- ✅ Never use `scroll-behavior: smooth` in CSS

### Performance Rules

- Animate only `transform` (x, y, scale, rotation) and `opacity`
- Never animate `width`, `height`, `top`, `left`, `margin`, `padding`, `box-shadow` with ScrollTrigger
- Apply `will-change: transform` on `.bg-layer`, `.mid-layer`, `.fg-layer`
- Use `ScrollTrigger.batch()` for staggered particle reveals
- Target 60fps on mid-range Android (Snapdragon 6-series)
- Total payload under 2MB
- Inline critical CSS if needed for instant FCP

---

## `.nojekyll` File

Create an empty `.nojekyll` file in the root to bypass Jekyll processing on GitHub Pages:

```
(empty file)
```

This prevents GitHub from ignoring files that start with underscores.
