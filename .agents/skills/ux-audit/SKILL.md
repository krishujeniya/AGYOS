---
name: ux-audit
description: "Audit screens against Nielsen's heuristics and mobile UX best practices using the StyleSeed Toss design language as the implementation context."
category: design
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: "Krish Ujeniya"
tags: [ux, audit, usability, mobile, styleseed]
tools: [claude, cursor, codex, gemini]
prompt-source: prompt.toon
---
skill: "ux-audit"
sections[9]:
  - "\n"
  - "# UX Audit\n\n"
  - "## Overview\n\nPart of [StyleSeed](https://github.com/bitjaru/styleseed), this skill audits usability rather than just visuals. It uses Nielsen's 10 heuristics plus modern mobile UX expectations to find issues in navigation, feedback, recovery, hierarchy, and cognitive load.\n\n"
  - "## When to Use\n- Use when a screen feels awkward even though the code and styling seem correct\n- Use when evaluating a flow before or after implementation\n- Use when reviewing a mobile-first product for usability regressions\n- Use when you want findings framed as user experience problems with remediation\n\n"
  - "## Audit Framework\n\nReview the target against:\n- visibility of system status\n- match between system and real-world language\n- user control and freedom\n- consistency and standards\n- error prevention\n- recognition rather than recall\n- flexibility and efficiency\n- aesthetic and minimalist design\n- recovery from errors\n- help, onboarding, and empty-state guidance\n\nAdd mobile-specific checks for reachability, touch ergonomics, input burden, and thumb-friendly action placement.\n\n"
  - "## Output\n\nReturn:\n1. A prioritized issue list\n2. The heuristic violated by each issue\n3. Why the issue matters to real users\n4. Specific remediation suggestions for the page, component, or flow\n\n"
  - "## Best Practices\n\n- Judge the experience from the user's point of view, not the implementer's\n- Separate high-severity flow blockers from minor polish issues\n- Include recovery and state-management guidance, not only layout comments\n- Tie recommendations back to concrete UI changes\n\n"
  - "## Additional Resources\n\n- [StyleSeed repository](https://github.com/bitjaru/styleseed)\n- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-audit/SKILL.md)\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
