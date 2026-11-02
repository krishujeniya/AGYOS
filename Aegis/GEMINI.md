# 🛡️ Aegis — Gemini Configuration

**Author**: Krish Ujeniya

## For Gemini Agents

Aegis is a skills-only development infrastructure for autonomous AI coding agents.

## How to Use

1. **Start any task** by reading `library/aegis/SKILL.md` — the 5-Gate orchestrator
2. **Invoke expert skills** from `library/experts/skills/` for specialized roles
3. **Follow core skills** from `library/core/skills/` for workflows
4. **Persist state** in `.sovereign/` at the target project root
5. **Index codebases** with `library/aegis/scripts/ast_packer.sh`

## Skill Priority Order

1. `library/aegis/SKILL.md` — Master orchestrator (always read first)
2. `library/experts/skills/expert-orchestrator/` — Complexity assessment
3. Gate-specific protocols in `library/aegis/references/`
4. Role-specific experts in `library/experts/skills/`
5. Core skills in `library/core/skills/`

## Quality Enforcement

All 11 rules in `library/experts/rules/` are mandatory:
- `testing.md` — No code without tests
- `security.md` — Security-first development
- `development.md` — Clean code standards
- `git-workflow.md` — Clean commit history
- `error-handling.md` — No silent failures
- `continuity.md` — Cross-session state persistence
