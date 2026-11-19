---
name: ai-native-cli
description: "Design spec with 98 rules for building CLI tools that AI agents can safely use. Covers structured JSON output, error handling, input contracts, safety guardrails, exit codes, and agent self-description."
risk: safe
source: https://github.com/ChaosRealmsAI/agent-cli-spec
date_added: "2026-03-15"
prompt-source: prompt.toon
---
skill: "ai-native-cli"
sections[2]:
  - "# Agent-Friendly CLI Spec v0.1\n\nDesign spec with 98 rules for building CLI tools that AI agents can safely use. Covers structured JSON output, error handling, input contracts, safety guardrails, exit codes, and agent self-description.\n\n"
  - "## Workflow\n\n1. Confirm the request fits this skill and identify the required inputs and output constraints.\n2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).\n3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.\n4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.\n5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.\n6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.\n"
