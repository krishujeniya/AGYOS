---
name: diagnostics-trace
description: "Add or troubleshoot error tracking, structured logs, and alerts. Use when instrumenting observability or tracing production failures to their source."
risk: safe
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "diagnostics-trace"
sections[10]:
  - "\n"
  - "# Error Tracking and Monitoring\n\nAdd or troubleshoot error tracking, structured logs, and alerts. Use when instrumenting observability or tracing production failures to their source.\n\n"
  - "## Use this skill when\n\n- Working on error tracking and monitoring tasks or workflows\n- Needing guidance, best practices, or checklists for error tracking and monitoring\n\n"
  - "## Do not use this skill when\n\n- The task is unrelated to error tracking and monitoring\n- You need a different domain or tool outside this scope\n\n"
  - "## Context\nThe user needs to implement or improve error tracking and monitoring. Focus on real-time error detection, meaningful alerts, error grouping, performance monitoring, and integration with popular error tracking services.\n\n"
  - "## Requirements\n$ARGUMENTS\n\n"
  - "## Instructions\n\n- Clarify goals, constraints, and required inputs.\n- Apply relevant best practices and validate outcomes.\n- Provide actionable steps and verification.\n- If detailed examples are required, open `resources/implementation-playbook.md`.\n\n"
  - "## Output Format\n\n1. **Error Tracking Analysis**: Current error handling assessment\n2. **Integration Configuration**: Setup for error tracking services\n3. **Logging Implementation**: Structured logging setup\n4. **Alert Rules**: Intelligent alerting configuration\n5. **Error Grouping**: Deduplication and grouping logic\n6. **Recovery Strategies**: Automatic error recovery implementation\n7. **Dashboard Setup**: Real-time error monitoring dashboard\n8. **Documentation**: Implementation and troubleshooting guide\n\nFocus on providing comprehensive error visibility, intelligent alerting, and quick error resolution capabilities.\n\n"
  - "## Resources\n\n- `resources/implementation-playbook.md` for detailed patterns and examples.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
