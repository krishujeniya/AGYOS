# 🛡️ Aegis

<h2 align="center">Production-Grade Skill System for AI Coding Agents</h2>

<p align="center">
  <em>Created by <strong>Krish Ujeniya</strong></em>
</p>

<p align="center">
  <a href="#-the-5-gate-workflow">5-Gate Workflow</a> •
  <a href="#-skill-library">Skill Library</a> •
  <a href="#-expert-team">Expert Team</a> •
  <a href="#-quick-start">Quick Start</a>
</p>

---

## What is Aegis?

Aegis is a skills-only infrastructure that makes AI coding agents operate as a full development team — from CEO to DevOps engineer. No runtime. No installations. No frameworks. Just markdown skill files that any agent can load.

### Capabilities
- **1,600+ skills** covering the complete software development lifecycle
- **8 expert role agents** — PM, PO, Architect, Engineer, DevOps, QA Lead, QA Tester, Orchestrator
- **11 quality guardrails** enforced automatically
- **Filesystem-based state machine** for fault-tolerant, cross-session execution
- **Token-efficient codebase indexing** via pure-bash AST packer

---

## 🔄 The 5-Gate Workflow

```
IDEA → UNDERSTAND → ANALYZE → PLAN → IMPLEMENT → VERIFY → PRODUCTION
```

| Gate | Purpose | Expert Lead | Key Skills |
|------|---------|------------|------------|
| **UNDERSTAND** | Explore intent, gather requirements | 🎯 CEO | brainstorming, openspec-explore |
| **ANALYZE** | PRD, user stories, risk assessment | 📋 PM/PO | expert-product-manager, expert-product-owner |
| **PLAN** | Architecture, ADRs, task plan | 🏗️ Architect | expert-tech-architect, writing-plans |
| **IMPLEMENT** | TDD, clean code, parallel agents | 💻 Engineer | expert-dev, test-driven-development |
| **VERIFY** | Evidence-based verification, audit | 🧪 QA | verification-before-completion, vibe-code-auditor |

---

## 📚 Skill Library

```
library/
├── aegis/                # 🎯 Orchestrator Hub
│   ├── SKILL.md          # Master 5-Gate workflow controller
│   ├── references/       # JIT-loaded gate protocols
│   ├── templates/        # State machine templates
│   └── scripts/          # AST packer & utilities
│
├── experts/              # 🏭 Expert Role Skills
│   ├── skills/           # 50 role-specific agent skills
│   └── rules/            # 11 quality guardrails
│
├── core/                 # 📦 Foundational Skills
│   └── skills/           # 81 core workflow skills
│
├── community/            # 🌐 Community Skills
│   └── skills/           # 1,459 community-contributed skills
│
└── seo/                  # 🔍 SEO Optimization
    └── SKILL.md
```

| Category | Count |
|----------|-------|
| **Aegis Orchestrator** | 1 + 5 gate references |
| **Expert Roles** | 50 |
| **Quality Rules** | 11 |
| **Core Skills** | 81 |
| **Community Skills** | 1,459 |
| **Total** | **1,600+** |

---

## 👥 Expert Team

| Role | Skill | Expertise |
|------|-------|-----------|
| 🎯 **CEO/Orchestrator** | `expert-orchestrator` | Complexity scoring, swarm coordination |
| 📋 **Product Manager** | `expert-product-manager` | Vision, PRD, SaaS metrics |
| 📋 **Product Owner** | `expert-product-owner` | User stories, acceptance criteria |
| 🏗️ **Tech Architect** | `expert-tech-architect` | System design, ADRs, API/DB schema |
| 💻 **Engineer** | `expert-dev` | SOLID, clean code, debugging |
| 🚀 **DevOps** | `expert-devops` | CI/CD, Docker, K8s, Terraform |
| 🧪 **QA Lead** | `expert-qa-engineer` | Test pyramid, coverage, QA gates |
| 🧪 **QA Tester** | `expert-qa-test` | Playwright/Cypress, automation |

---

## ⚡ Quick Start

```bash
# Point any AI coding agent at the orchestrator:
# → library/aegis/SKILL.md

# Token-efficient codebase understanding:
./library/aegis/scripts/ast_packer.sh /path/to/project > .sovereign/ast_index.md
```

---

## 🔒 Human-in-the-Loop Policy

| Requires Human Approval | Fully Autonomous |
|------------------------|-----------------|
| ✅ Requirements confirmation | ❌ Code implementation |
| ✅ Scope & priority approval | ❌ Test writing & execution |
| ✅ Architecture decisions | ❌ Debugging & fixing |
| ✅ Production deployment | ❌ Git operations |
| ✅ Legal/financial/personal data | ❌ CI/CD configuration |

---

<p align="center">
  <strong>Aegis — by Krish Ujeniya</strong>
</p>
