# Agentic Security Mandate

> **Enforcement Level**: CRITICAL
> **Applies To**: All Autonomous Agents (Gate 4 & Gate 5)

## The Mandate
No code shall be presented to the Human-In-The-Loop (HITL) for deployment approval unless it has been explicitly audited and cleared by the `adversarial-red-team` skill.

## Rules of Engagement
1. **Zero Trust**: Agents implementing code (Gate 4) must assume their code is flawed.
2. **Mandatory Red Teaming**: Upon entering Gate 5, the orchestrator MUST spawn a Red Team sub-agent to attack the implementation.
3. **No Criticals**: If a 🔴 VULNERABILITY is discovered, the workflow immediately halts and reverts to Gate 4 for remediation.
4. **Audit Trail**: The Red Team's findings must be appended to `.sovereign/verification.md` using the standard template schema.
