---
name: enhance-prompt
description: Prepares UI requests as structured prompts for Google's Stitch interface, using the project's available design system and stated requirements.
allowed-tools:
  - "Read"
  - "Write"
risk: unknown
source: community
prompt-source: prompt.toon
---
skill: "enhance-prompt"
sections[4]:
  - "\n"
  - "# Enhance a prompt for Stitch\n\nUse this skill only when the user wants a prompt prepared for Google's Stitch interface. AGYOS remains the authoring identity; Stitch is named only as the target integration.\n\nBefore drafting version-sensitive instructions, check the [official Stitch prompting guide](https://stitch.withgoogle.com/docs/learn/prompting/).\n\n"
  - "## Workflow\n\n1. Identify the page or interface, intended users, platform, required content, interactions, and constraints already supplied.\n2. Inspect the project's design-system documentation when available. Preserve its tokens and component patterns; do not invent a replacement system.\n3. Ask only when a missing detail would materially change the page or interaction. Otherwise mark a low-risk assumption.\n4. Describe the page structure, component behavior, visual direction, and content hierarchy in concrete terms.\n5. Include exact color or type tokens only when supplied or verified. Keep accessibility needs such as contrast, focus, responsive behavior, and reduced motion explicit when relevant.\n6. Return a concise prompt for Stitch. Do not claim that a prompt guarantees a particular generated result.\n\n"
  - "## Output shape\n\n```text\nCreate [page/interface] for [audience and purpose].\nPlatform: [web/mobile/desktop, if known]\nStructure: [required sections and content]\nInteractions: [states and actions]\nVisual direction: [user-provided or repository-backed design guidance]\nConstraints: [accessibility, responsive, technical, and brand requirements]\n```\n\nOmit fields the task does not need. Use the project's own brand and design system. Do not borrow another company's identity, style, logo, or signature layout.\n"
