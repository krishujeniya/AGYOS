# Creative & UI/UX Design Engineering Standards
- Enforce Design Engineering standards for all UI/UX, SaaS apps, and website generation.
- Concentric Border Radii: Nested child radii must satisfy R_inner = R_outer - padding.
- Animation Timing: Micro-interactions (150-200ms); modals (250-350ms); never animate keyboard actions.
- Compositor-Only: Animate transform and opacity only. No layout thrashing on height/width.
- Tactile Micro-Interactions: Active scale feedback (scale 0.98) on interactive controls.
- Use structured Before/After/Why markdown tables for UI code reviews.
- Build clean, accessible, responsive CSS, Tailwind, Framer Motion, and GSAP animations.