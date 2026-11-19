---
name: pr-enhancer
description: "Prepare a pull request for review with a clear summary, scoped changes, test evidence, and reviewer context. Use when improving a PR before review."
risk: unknown
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "pr-enhancer"
sections[10]:
  - "\n"
  - "# Pull Request Enhancement\n\nPrepare a pull request for review with a clear summary, scoped changes, test evidence, and reviewer context. Use when improving a PR before review.\n\n"
  - "## Use this skill when\n\n- Working on pull request enhancement tasks or workflows\n- Needing guidance, best practices, or checklists for pull request enhancement\n\n"
  - "## Do not use this skill when\n\n- The task is unrelated to pull request enhancement\n- You need a different domain or tool outside this scope\n\n"
  - "## Context\nThe user needs to create or improve pull requests with detailed descriptions, proper documentation, test coverage analysis, and review facilitation. Focus on making PRs that are easy to review, well-documented, and include all necessary context.\n\n"
  - "## Requirements\n$ARGUMENTS\n\n"
  - "## Instructions\n\n- Clarify goals, constraints, and required inputs.\n- Apply relevant best practices and validate outcomes.\n- Provide actionable steps and verification.\n- If detailed examples are required, open `resources/implementation-playbook.md`.\n\n"
  - "## Output Format\n\n1. **PR Summary**: Executive summary with key metrics\n2. **Detailed Description**: Comprehensive PR description\n3. **Review Checklist**: Context-aware review items  \n4. **Risk Assessment**: Risk analysis with mitigation strategies\n5. **Test Coverage**: Before/after coverage comparison\n6. **Visual Aids**: Diagrams and visual diffs where applicable\n7. **Size Recommendations**: Suggestions for splitting large PRs\n8. **Review Automation**: Automated checks and findings\n\nFocus on creating PRs that are a pleasure to review, with all necessary context and documentation for efficient code review process.\n\n"
  - "## Resources\n\n- `resources/implementation-playbook.md` for detailed patterns and examples.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
