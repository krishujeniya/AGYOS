# Aegis

> Build commands, code standards, and project context for all AI coding agents.

**Author**: Krish Ujeniya

## Project Overview

Aegis is a production-grade skill system for AI coding agents. It provides 1,600+ skills organized across expert roles, core workflows, and community contributions — enabling any AI agent to operate as a full autonomous development team.

## Architecture

```
library/
├── aegis/                # 🎯 Orchestrator — 5-Gate workflow controller
│   ├── SKILL.md          # Master skill (read first)
│   ├── references/       # JIT-loaded gate protocols
│   ├── templates/        # State machine templates
│   └── scripts/          # AST packer utility
├── experts/              # 🏭 Expert team skills + quality rules
│   ├── skills/           # 50 role-specific skills
│   └── rules/            # 11 quality guardrails
├── core/                 # 📦 Foundational skills
│   └── skills/           # 81 core workflow skills
├── community/            # 🌐 Community-contributed skills
│   └── skills/           # 1,459 skills
└── seo/                  # 🔍 SEO optimization skill
```

## Build & Test

This is a skills-only project — no build step required. Point any AI agent at `library/aegis/SKILL.md` to activate.

## Codebase Understanding

```bash
./library/aegis/scripts/ast_packer.sh /path/to/project > .sovereign/ast_index.md
```

## Standards

- All skills follow the `SKILL.md` convention (YAML frontmatter + markdown body)
- Rules in `library/experts/rules/` are mandatory for all development
- State persists in `.sovereign/` at the target project root
