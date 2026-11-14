---
name: enhance-prompt
description: Prepares UI requests as structured prompts for Google's Stitch interface, using the project's available design system and stated requirements.
allowed-tools:
  - "Read"
  - "Write"
risk: unknown
source: community
---

# Enhance a prompt for Stitch

Use this skill only when the user wants a prompt prepared for Google's Stitch interface. AGYOS remains the authoring identity; Stitch is named only as the target integration.

Before drafting version-sensitive instructions, check the [official Stitch prompting guide](https://stitch.withgoogle.com/docs/learn/prompting/).

## Workflow

1. Identify the page or interface, intended users, platform, required content, interactions, and constraints already supplied.
2. Inspect the project's design-system documentation when available. Preserve its tokens and component patterns; do not invent a replacement system.
3. Ask only when a missing detail would materially change the page or interaction. Otherwise mark a low-risk assumption.
4. Describe the page structure, component behavior, visual direction, and content hierarchy in concrete terms.
5. Include exact color or type tokens only when supplied or verified. Keep accessibility needs such as contrast, focus, responsive behavior, and reduced motion explicit when relevant.
6. Return a concise prompt for Stitch. Do not claim that a prompt guarantees a particular generated result.

## Output shape

```text
Create [page/interface] for [audience and purpose].
Platform: [web/mobile/desktop, if known]
Structure: [required sections and content]
Interactions: [states and actions]
Visual direction: [user-provided or repository-backed design guidance]
Constraints: [accessibility, responsive, technical, and brand requirements]
```

Omit fields the task does not need. Use the project's own brand and design system. Do not borrow another company's identity, style, logo, or signature layout.
