---
name: dependency-management-deps-audit
description: "Audit project dependencies for known vulnerabilities, license constraints, outdated packages, and supply-chain risks. Use when reviewing manifests or dependency changes."
risk: unknown
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "dependency-management-deps-audit"
sections[10]:
  - "\n"
  - "# Dependency Audit and Security Analysis\n\nAudit project dependencies for known vulnerabilities, license constraints, outdated packages, and supply-chain risks. Use when reviewing manifests or dependency changes.\n\n"
  - "## Use this skill when\n\n- Auditing dependencies for vulnerabilities\n- Checking license compliance or supply-chain risks\n- Identifying outdated packages and upgrade paths\n- Preparing security reports or remediation plans\n\n"
  - "## Do not use this skill when\n\n- The project has no dependency manifests\n- You cannot change or update dependencies\n- The task is unrelated to dependency management\n\n"
  - "## Context\nThe user needs comprehensive dependency analysis to identify security vulnerabilities, licensing conflicts, and maintenance risks in their project dependencies. Focus on actionable insights with automated fixes where possible.\n\n"
  - "## Requirements\n$ARGUMENTS\n\n"
  - "## Instructions\n\n- Inventory direct and transitive dependencies.\n- Run vulnerability and license scans.\n- Prioritize fixes by severity and exposure.\n- Propose upgrades with compatibility notes.\n- If detailed workflows are required, open `resources/implementation-playbook.md`.\n\n"
  - "## Safety\n\n- Do not publish sensitive vulnerability details to public channels.\n- Verify upgrades in staging before production rollout.\n\n"
  - "## Resources\n\n- `resources/implementation-playbook.md` for detailed tooling and templates.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
