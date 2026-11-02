# 🛡️ Aegis

**Author**: Krish Ujeniya

## What is Aegis?

Aegis is an autonomous development skill system that makes AI coding agents operate like a full development team. Skills-only. No runtime. No dependencies.

## Directory Structure

```
library/
├── aegis/                # Orchestrator — 5-Gate workflow controller
├── experts/skills/       # 50 expert role skills (PM, Architect, Engineer, DevOps, QA)
├── experts/rules/        # 11 quality guardrails (security, testing, git, etc.)
├── core/skills/          # 81 foundational skills (brainstorming, TDD, debugging, etc.)
├── community/skills/     # 1,459 community-contributed skills
└── seo/                  # SEO optimization skill
```

## 5-Gate Workflow

1. **UNDERSTAND** — Brainstorm, explore intent, research domain
2. **ANALYZE** — PRD, user stories, risk assessment
3. **PLAN** — Architecture, ADRs, bite-sized task plan
4. **IMPLEMENT** — TDD, clean code, parallel agents
5. **VERIFY** — Evidence-based verification, code audit, review

## Rules

- Skills-first: every action invokes a specialized skill
- TDD mandatory: no production code without a failing test
- Verification iron law: no completion claims without fresh evidence
- State persistence: `.sovereign/` for filesystem state machine
- HITL: human approval for legal, financial, personal data, deployments only

## Skill Locations

| Purpose | Path |
|---------|------|
| Orchestrator | `library/aegis/SKILL.md` |
| Expert roles | `library/experts/skills/*/SKILL.md` |
| Core skills | `library/core/skills/*/SKILL.md` |
| Quality rules | `library/experts/rules/*.md` |
| Gate protocols | `library/aegis/references/gate-*.md` |
| AST packer | `library/aegis/scripts/ast_packer.sh` |
