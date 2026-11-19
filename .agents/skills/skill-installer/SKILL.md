---
name: skill-installer
description: Instala, valida, registra e verifica novas skills no ecossistema. 10 checks de seguranca, copia, registro no orchestrator e verificacao pos-instalacao.
risk: safe
source: community
date_added: '2026-03-06'
author: "Krish Ujeniya"
tags:
- skill-management
- deployment
- validation
- installation
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
prompt-source: prompt.toon
---
skill: "skill-installer"
sections[2]:
  - "# Skill Installer v3.0\n\nInstala, valida, registra e verifica novas skills no ecossistema. 10 checks de seguranca, copia, registro no orchestrator e verificacao pos-instalacao.\n\n"
  - "## Workflow\n\n1. Confirm the request fits this skill and identify the required inputs and output constraints.\n2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).\n3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.\n4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.\n5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.\n6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.\n"
