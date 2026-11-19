---
name: vibe-code-auditor
description: "Audit rapidly generated or AI-produced code for structural flaws, fragility, technical debt, and production risks. Automatically triggers before merging large features or concluding deep implementation loops to ensure the code is actually robust."
category: guardrail
risk: safe
tags: "[audit, security, technical-debt, review, architecture]"
version: "1.0.0"
prompt-source: prompt.toon
---
skill: "vibe-code-auditor"
sections[7]:
  - "\n"
  - "# Vibe Code Auditor\n\nA senior software architect persona focusing on evaluating prototype-quality and AI-generated code. Determines whether code that \"works\" is actually robust, maintainable, and production-ready.\n\n"
  - "## Purpose\nEven when tests pass and code visually works, it can contain hidden technical debt, monolithic functions, or security vulnerabilities (e.g., SQL injections, unsecured APIs). This skill forces a rigorous check against 7 key dimensions before complex code is shipped.\n\n"
  - "## When to Include\n- Code was generated rapidly (e.g., massive copy-paste or huge refactoring).\n- Subagent driven development just finished a massive module.\n- You are about to ask the user to merged a branch.\n- You suspect hidden technical debt.\n\n"
  - "## The 7 Audit Dimensions\n\n1. **Architecture & Design:** Separation of concerns. No business logic in UI routing. No god objects.\n2. **Consistency & Maintainability:** Consistent naming. Avoid copy-paste logic (dry).\n3. **Robustness & Error Handling:** Missing input validation. Bare `except` blocks swallowing errors. \n4. **Production Risks:** Hardcoded config values. Unbounded loops/N+1 queries. Missing logs.\n5. **Security & Safety:** Unsanitized inputs. Hardcoded tokens. Trust boundary violations.\n6. **Dead or Hallucinated Code:** Functions defined but never called. Imports unused. Contradictory comments.\n7. **Technical Debt Hotspots:** Deep nesting (>3 levels). Methods with 6+ parameters.\n\n"
  - "## Output Format (The Audit Report)\n\nWhen triggered to do an audit, DO NOT immediately rewrite the code. Output the following specific format.\n\n```markdown\n### Vibe Audit Report\n**Input:** [file name]\n\n#### Critical Issues (Must Fix Before Production)\n[CRITICAL] Short Title\nLocation: filename.py, line X\nDimension: Architecture\nProblem: Exactly what is wrong.\nFix: The minimum change required.\n\n#### High-Risk Issues\n[HIGH] ...\n\n#### Maintainability Problems\n[MEDIUM] ...\n\n#### Production Readiness Score\nScore: XX / 100\n(0-50 = High Risk, 51-85 = Target Fixes Needed, 86-100 = Production Ready)\n\n#### Refactoring Priorities\n1. [Priority] Fix title — estimated effort: S/M/L\n```\n\n"
  - "## Behavior Rules\n- **No inventions.** Ground every finding in the actual code provided. Do not speculate.\n- **Provide line numbers.**\n- **Do not flag cosmetic style preferences** unless they obscure logic.\n- **Do not recommend architectural rewrites** unless the current structure makes the system impossible to maintain safely. Provide targeted fixes.\n"
