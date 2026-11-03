---
trigger: glob
globs: "**/*.css,**/*.scss,**/*.tsx,**/*.jsx,**/*.vue,**/*.svelte,**/*.html"
---
# Emil Kowalski UI/UX & Motion Engineering Standard

This rule encodes Emil Kowalski's design engineering philosophy for UI polish, component design, animation decisions, and tactile micro-interactions.

## 1. Concentric Border Radii Formula
When nesting curved containers (e.g. cards with inner images or buttons):
$$\text{Radius}_{\text{inner}} = \text{Radius}_{\text{outer}} - \text{Padding}$$
- Never use the same border-radius for an outer card and an inner element.
- If padding is larger than outer radius, inner radius should be 0 or minimal.

## 2. The Animation Decision Framework
Before writing motion code, determine frequency of use:

| Frequency | Decision | Example |
| --- | --- | --- |
| 100+ times/day | **No animation ever (0ms)** | Command palette, shortcuts, search toggle |
| Tens of times/day | Fast micro-interaction (150-200ms) | Hover states, list item selection |
| Occasional | Standard animation (250-350ms) | Modals, drawers, toasts |
| Rare / First-time | Expressive delight (400-500ms) | Onboarding, success celebration |

**Rule**: Never animate keyboard-initiated actions. They must respond instantaneously.

## 3. Compositor-Only Animation Invariant
- Animate **ONLY** `transform` and `opacity`.
- **Never** animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`) directly.
- For dynamic resizing or layout morphing, use FLIP projection (e.g. Framer Motion `<motion.div layout />` with `layoutId`).

## 4. Easing & Curve Standards
- **Entering elements**: Use fast acceleration with smooth deceleration: `cubic-bezier(0.16, 1, 0.3, 1)` (expo out).
- **Exiting elements**: Fast and decisive: `cubic-bezier(0.7, 0, 0.84, 0)` or faster duration (~150ms).
- Avoid generic `linear` or default CSS `ease`.
- Popover `transform-origin` must match the trigger button position (modals remain centered).

## 5. Tactile Micro-Interactions
- **Active press state**: Every interactive button must have feedback: `active:scale-[0.98]` or `active:translate-y-[1px]`.
- **Hover guards**: Always wrap hover effects in `@media (hover: hover) and (pointer: fine)` to avoid sticky hover bugs on touch devices.
- **Tabular numbers**: Always use `font-variant-numeric: tabular-nums` (or `tabular-nums` in Tailwind) on counters, prices, timers, and data tables.

## 6. Review Format Requirement
When reviewing UI code, present issues in a structured Before / After / Why markdown table:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1)` | Specify exact property; avoid `all` layout thrash |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Physical objects do not appear from absolute zero |
| Missing `:active` | `active:scale-[0.98]` | Provides physical press feedback |
