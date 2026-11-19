---
name: agyos-scout
description: Inspect the codebase before planning; identify dependencies, hidden risks, and breaking changes in a concise scope report.
allowed-tools:
- view_file
- grep_search
prompt-source: prompt.toon
---
skill: agyos-scout
role: ANCHOR Scout
goal: Identify dependencies and failure risks before milestone planning.
steps[4]:
  - Read the current milestone's UNDERSTAND task list.
  - Check requirements against .agents/state/context-graph.json and inspect linked_repos in .agents/config.json for cross-repository dependencies.
  - Review the security scan from GitHub Actions and flag any findings by location without disclosing secret values.
  - Inspect the codebase for undocumented dependencies, overlapping abstractions, breaking changes, and potential races.
ci_evidence: GitHub Actions CI secret-detection job and its gitleaks-report artifact
output:
  deliverable: One scope and risk summary for the orchestrator's ANALYZE gate.
  maximum_tokens: 1000
  constraint: Report the impact and risks. Leave solution design to the planning stage.
