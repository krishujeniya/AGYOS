---
name: agyos-anti-ai-design
description: Diagnostic and design guide to eliminate AI-generated UI slop. Replaces generic purple gradients, Inter overuse, emoji icons, uniform 3-card grids, and synthetic floating blobs with production design.
---

# AGYOS Anti-AI UI/UX Design Engineering

Engineering guidelines for detecting and eliminating the common visual signatures of generic, automated AI web generation, elevating interfaces to production standards.

## 1. Palette: Eliminate Generic Purple Gradients

Signature Flaw:
- Overuse of violet-to-fuchsia or generic indigo gradients (`from-purple-600 to-indigo-600`) as fallback hero backgrounds and button accents.

Engineering Fix:
- Implement a disciplined color architecture using CSS variables or Tailwind tokens:
  - High-contrast monochrome: Crisp black/white (`#0a0a0a` / `#fafafa`) with a single deliberate accent (emerald, amber, electric blue, or terracotta).
  - Test contrast ratios against WCAG AAA standards (7:1 for normal text, 4.5:1 for large controls).
  - Use subtle radial gradients with low opacity (3-8%) anchored to structural elements rather than generic full-viewport washes.

## 2. Typography: Move Beyond Default Inter Everywhere

Signature Flaw:
- Defaulting to Inter or Roboto for all headers, labels, numbers, and body copy without typographic hierarchy.

Engineering Fix:
- Pair distinct display and body typefaces:
  - Technical / Modern: Geist Sans (body) + Geist Mono (data/code).
  - Architectural / Product: Plus Jakarta Sans or Cabinet Grotesk (display) + Inter/Public Sans (body).
  - Editorial / High-Trust: Instrument Serif or Playfair (display) + DM Sans (body).
- Enforce strict optical scaling: `text-xs` (12px), `text-sm` (14px), `text-base` (16px), `text-xl` (20px), `text-3xl` (30px), `text-5xl` (48px).

## 3. Iconography: Replace Inlined Emojis with Vector Icons

Signature Flaw:
- Using emoji characters (🚀, 💡, ⚡, 🛡️) inside production cards, buttons, and navigation headers.

Engineering Fix:
- Use consistent vector icon libraries: Lucide Icons, Phosphor Icons, or Radix Icons.
- Standardize stroke width (e.g., `stroke-width="1.75"` across all icons) and bounding box sizing (`16px`, `20px`, `24px`).
- Wrap icons in accessible semantic wrappers (`aria-hidden="true"` on decorative icons, explicit labels on standalone buttons).

## 4. Layout: Break the Uniform 3-Card Grid Pattern

Signature Flaw:
- Repetitive, identical 3-card horizontal rows (`grid-cols-1 md:grid-cols-3`) with identical padding, centered text, and decorative icons.

Engineering Fix:
- Adopt Bento grid patterns with varying cell weights (e.g., a 2:1 column split, full-width feature anchor, or layered interactive preview).
- Mix vertical alignments: left-align dense copy, display live code snippets or interactive components in key cards, and use asymmetric visual hierarchy.

## 5. Depth & Motion: Replace Fake 3D Blobs with Tactile Micro-Interactions

Signature Flaw:
- Blurred circular background blobs (`blur-3xl bg-pink-500/20`) floating aimlessly across the viewport.

Engineering Fix:
- Apply Emil Kowalski's 6 Design Engineering Invariants:
  1. Concentric Border Radii: Nested inner radius must equal outer radius minus padding ($R_{\text{inner}} = R_{\text{outer}} - \text{padding}$).
  2. Tactile Press Feedback: Interactive buttons require active press downscale (`active:scale-[0.98] transition-transform duration-100`).
  3. Compositor-Only Motion: Animate `transform` and `opacity` only; never animate `height` or `width` layout properties.
  4. Crisp Borders: Define crisp tokenized borders (`border border-neutral-200 dark:border-neutral-800`).
