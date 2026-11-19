---
name: secure-env-secrets-manager
description: "Handle project environment variables with secret-safe inspection and execution. Use when reviewing .env wiring or running commands that need credentials; never print secret values into the session."
risk: safe
source: https://github.com/wrsmith108/varlock-claude-skill
date_added: '2026-02-27'
prompt-source: prompt.toon
---
skill: "secure-env-secrets-manager"
sections[4]:
  - "\n"
  - "# Secret-safe environment handling\n\nUse this procedure when project commands need credentials or when checking environment configuration.\n\n"
  - "## Workflow\n\n1. Read project instructions and identify the existing secret manager and environment schema. Do not read or paste `.env` values into the conversation.\n2. Never use `cat .env`, `printenv`, shell tracing, or `echo` on secret values. Inspect a checked-in schema or example file that contains names and placeholders only.\n3. If Varlock is already installed and configured, follow its current project documentation. The upstream skill documents `varlock load --quiet` for quiet validation and `varlock run -- <command>` for a command that needs injected values.\n4. Do not install a CLI, alter a provider, or rotate credentials unless the user authorized that action. If the tool is missing, report the prerequisite and link the [Varlock skill source](https://github.com/wrsmith108/varlock-claude-skill).\n5. Before finishing, inspect the diff and logs for accidental secret values without printing or copying the values. Redact any evidence that could expose credentials.\n\nThis workflow reduces exposure risk; it cannot guarantee that secrets never appear in every host, shell, or external service.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
