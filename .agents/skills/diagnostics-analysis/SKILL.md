---
name: diagnostics-analysis
description: "Analyze errors and production incidents across distributed systems. Use when tracing failures across services or reviewing observability evidence."
risk: safe
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "diagnostics-analysis"
sections[10]:
  - "\n"
  - "# Error Analysis and Resolution\n\nAnalyze errors and production incidents across distributed systems. Use when tracing failures across services or reviewing observability evidence.\n\n"
  - "## Use this skill when\n\n- Investigating production incidents or recurring errors\n- Performing root-cause analysis across services\n- Designing observability and error handling improvements\n\n"
  - "## Do not use this skill when\n\n- The task is purely feature development\n- You cannot access error reports, logs, or traces\n- The issue is unrelated to system reliability\n\n"
  - "## Context\n\nThis tool provides systematic error analysis and resolution capabilities for modern applications. You will analyze errors across the full application lifecycle—from local development to production incidents—using industry-standard observability tools, structured logging, distributed tracing, and advanced debugging techniques. Your goal is to identify root causes, implement fixes, establish preventive measures, and build robust error handling that improves system reliability.\n\n"
  - "## Requirements\n\nAnalyze and resolve errors in: $ARGUMENTS\n\nThe analysis scope may include specific error messages, stack traces, log files, failing services, or general error patterns. Adapt your approach based on the provided context.\n\n"
  - "## Instructions\n\n- Gather error context, timestamps, and affected services.\n- Reproduce or narrow the issue with targeted experiments.\n- Identify root cause and validate with evidence.\n- Propose fixes, tests, and preventive measures.\n- If detailed playbooks are required, open `resources/implementation-playbook.md`.\n\n"
  - "## Safety\n\n- Avoid making changes in production without approval and rollback plans.\n- Redact secrets and PII from shared diagnostics.\n\n"
  - "## Resources\n\n- `resources/implementation-playbook.md` for detailed analysis frameworks and checklists.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
