---
name: ui-design-guidelines
description: "Browse or apply design-engineering guidance from the UI Skills collection. Use when the task needs a specific interface-design guide; preserve the project's existing design system and accessibility requirements."
risk: safe
source: https://github.com/ibelick/ui-skills
date_added: '2026-02-27'
---

# UI design guidelines

Use this skill to find a focused design-engineering guide. It does not replace the product's existing visual system, framework-specific guidance, or accessibility review.

## Workflow

1. Read the project UI instructions and inspect the relevant screens, components, and design tokens.
2. Identify the requested area: layout, typography, motion, component behavior, or another documented category.
3. If the UI Skills CLI is already available, inspect its current help, list the relevant category, and retrieve only the matching guide. Do not run `npx` or install a package without authorization.
4. Compare retrieved guidance with the project's existing patterns and the user's explicit constraints. Resolve conflicts in favor of the project and user requirements.
5. Apply only the guidance needed for the requested change. Verify the affected UI at keyboard and mobile sizes when the task changes interactive or responsive behavior.

The upstream repository exposes commands to browse categories and fetch individual skills. Check its [current CLI documentation](https://github.com/ibelick/ui-skills) before relying on command names or guide contents.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
