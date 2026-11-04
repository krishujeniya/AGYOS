<p align="center">
  <img src="assets/logo.svg" alt="AGYOS Logo" width="220" />
</p>

<h1 align="center">AGYOS</h1>

<p align="center">
  <strong>Autonomous Cognitive Agent Operating System &amp; Monorepo of 1,842+ Engineering Skills</strong><br />
  <em>Engineered &amp; Authored by Krish Ujeniya</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache-2.0" /></a>
  <img src="https://img.shields.io/badge/Skills-1%2C842%20Skills-00F0FF.svg" alt="Skills Count" />
  <img src="https://img.shields.io/badge/Protocol-Model%20Context%20Protocol%20(MCP)-6366F1.svg" alt="MCP Daemon" />
  <img src="https://img.shields.io/badge/Verification-34%2F34_Passed-10B981.svg" alt="Verification" />
  <a href="https://krishujeniya.github.io/AGYOS/"><img src="https://img.shields.io/badge/Docs-GitHub%20Pages-A855F7.svg" alt="Documentation" /></a>
</p>

---

## Overview

**AGYOS** is an autonomous cognitive agent operating system and physical catalog of 1,842+ modular engineering skills, designed to give AI agents deterministic reliability, zero-speculation code generation, and multi-model consensus.

All skills reside in a single flat directory with zero subfolders, clear task-based naming, and zero external branding. Every skill encodes proven, actionable runbooks for software architecture, full-stack engineering, security testing, performance tuning, and technical operations.

---

## Core Pillars

```
                                    ┌────────────────────────────────┐
                                    │    NATURAL LANGUAGE PROMPT     │
                                    └────────────────────────────────┘
                                                    │
                                                    ▼
                     ┌─────────────────────────────────────────────────────────────┐
                     │          SEARCH-FIRST AUTONOMOUS SKILL DISCOVERY             │
                     │  (Zero-Slash Ingestion: Finds exact runbook in <10ms)       │
                     └─────────────────────────────────────────────────────────────┘
                                                    │
        ┌───────────────────────────────────────────┼───────────────────────────────────────────┐
        ▼                                           ▼                                           ▼
┌───────────────┐                           ┌───────────────┐                           ┌───────────────┐
│ 5-GATE ENGINE │                           │  FASTMCP STDO │                           │ AGENT COUNCIL │
│  Governance   │                           │ State Daemon  │                           │  Deliberation │
└───────────────┘                           └───────────────┘                           └───────────────┘
        │                                           │                                           │
        └───────────────────────────────────────────┼───────────────────────────────────────────┘
                                                    ▼
                                    ┌────────────────────────────────┐
                                    │ 1,842+ MODULAR RUNBOOK SKILLS  │
                                    │ (Frontend, Backend, Security)  │
                                    └────────────────────────────────┘
```

### 1. Unified Flat Skill Catalog
- **1,842 Physical Skills**: Every skill is stored directly under `.agents/skills/<name>/SKILL.md` (and mirrored at `skills/<name>/SKILL.md`).
- **Work-Based Naming**: Skills use explicit task names (e.g. `deep-learning-architecture-advisor`, `wcag-accessibility-compliance`, `pentagi-orchestrator`, `clean-architecture-craftsmanship`) for instant zero-shot discovery.
- **Zero Third-Party Branding**: Pure engineering terminology and clear responsibilities.

### 2. 5-Gate Lifecycle Governance
Every non-trivial engineering workflow progresses through five deterministic gates:
1. **UNDERSTAND**: Task specification, scope boundaries, and acceptance criteria.
2. **ANALYZE**: Read-only codebase inspection, dependency mapping, and risk analysis.
3. **PLAN**: Architecture Decision Records (ADR), interface contracts, and test strategy.
4. **IMPLEMENT**: Test-Driven Development (TDD) red-green-refactor loop with 80%+ test coverage.
5. **VERIFY**: Adversarial proof, machine evidence, zero linter warnings, and passing test suites.

### 3. FastMCP State Daemon (`mcp/state-server.cjs`)
- Zero external dependencies; vanilla JSON-RPC 2.0 over standard I/O (`stdio`).
- Implements Model Context Protocol (MCP) tools:
  - `agyos_state`: Inspect active governance milestone and gate status.
  - `agyos_current`: Human-readable session overview from `CURRENT.md`.
  - `agyos_graph`: Dependency index and system invariant graph.
  - `agyos_checkpoint`: Append structured execution checkpoints.
  - `agyos_find_skill`: Fast sub-10ms keyword and semantic search over 1,842 skills.
  - `agyos_sys_info`: Comprehensive kernel health and subsystem status.
  - `agyos_memory`: Virtual multi-tier cross-session memory manager.

### 4. Zero-Slash Automation
No slash commands or manual mode switches required. The system automatically inspects user intent, discovers matching specialist runbooks via `agyos_find_skill`, and executes work with direct machine evidence.

---

## Repository Structure

```
├── .agents/
│   ├── agents/                 # 74 Specialized corporate role agent definitions
│   ├── plugins/                # Validated governance plugins (rules and config)
│   ├── rules/                  # 161 Modular governance, polyglot, and SDLC rules
│   ├── skills/                 # 1,842 Production skills (flat, 1 folder per skill)
│   ├── state/                  # 5-Gate runtime state and checkpoint journals
│   ├── workflows/              # 100 Multi-agent execution pipelines
│   ├── skills-manifest.json    # Complete index of 1,842 skills
│   └── tier1-skills.json       # Curated high-frequency skill registry
├── assets/
│   ├── logo.svg                # Master project vector logo
│   └── README.md
├── bin/
│   ├── agyos                   # Kernel CLI (init, state, gate, verify, council, skill)
│   ├── compact.sh              # Context compaction utility
│   ├── gate-check.sh           # Pre-commit test ratchet enforcer
│   └── state.sh                # Programmatic gate transitions
├── docs/                       # Static documentation website (GitHub Pages ready)
│   ├── index.html              # Interactive skill catalog explorer and search
│   ├── docs.css                # Polished responsive styling
│   ├── docs.js                 # Client-side instantaneous search
│   └── skills-data.json        # Pre-indexed search data
├── mcp/
│   ├── state-server.cjs        # FastMCP zero-dependency stdio JSON-RPC daemon
│   └── README.md
├── scripts/
│   ├── agyos-verify.sh         # Adversarial verification test suite (34 checks)
│   ├── agyos-init.sh           # Environment bootstrapper and self-repair
│   └── hooks/                  # Real-time tool lifecycle interceptors
├── skills/                     # Direct link to .agents/skills/
├── rules/                      # Direct link to .agents/rules/
├── workflows/                  # Direct link to .agents/workflows/
├── CITATION.cff                # Academic and professional citation metadata
├── LICENSE                     # Apache 2.0 open-source license
└── README.md                   # Primary project documentation
```

---

## Quickstart & CLI Usage

### 1. Initialize and Validate Environment
```bash
# Bootstrap repository permissions and state daemon
bash scripts/agyos-init.sh

# Run comprehensive 34-point verification suite
bash scripts/agyos-verify.sh
```

### 2. Query the Skills Catalog via CLI
```bash
# Search for skills by domain or task
bin/agyos find "react animation"
bin/agyos find "pentagi penetration testing"
bin/agyos find "clean architecture"

# View full skill runbook
bin/agyos skill wcag-accessibility-compliance
bin/agyos skill pentagi-orchestrator
```

### 3. Inspect Governance State
```bash
# View active gate, milestone, and invariant status
bin/agyos state

# Advance governance gate
bin/agyos gate UNDERSTAND
bin/agyos gate ANALYZE
bin/agyos gate PLAN
bin/agyos gate IMPLEMENT
bin/agyos gate VERIFY
```

### 4. Query FastMCP State Daemon Directly
```bash
# Discover tools via stdio JSON-RPC
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | node mcp/state-server.cjs

# Search skills via JSON-RPC
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"agyos_find_skill","arguments":{"query":"ssrf testing"}}}' | node mcp/state-server.cjs
```

---

## Skills Catalog Highlights

The repository contains **1,842 skills** organized across major disciplines:

| Domain | Key Skills |
|--------|------------|
| **Architecture & Systems** | `architecture-decision-framework`, `clean-architecture-craftsmanship`, `c4-architecture`, `hexagonal-architecture`, `microservices-patterns`, `event-sourcing-architect` |
| **Security & Pentesting** | `pentagi-orchestrator`, `ssrf-oob-interaction-testing`, `xxe-xml-injection-testing`, `cve-vulnerability-intelligence`, `security-sandbox-runner`, `metasploit-framework`, `sqlmap-database-pentesting` |
| **Frontend & UI/UX** | `ui-design-engineering-standards`, `wcag-accessibility-compliance`, `shadcn-ui-components`, `web-animation-design`, `threejs-webgl-development`, `tailwind-patterns` |
| **Backend & Databases** | `database-schema-modeling`, `postgres-patterns`, `fastapi-pro`, `rust-patterns`, `golang-patterns`, `redis-patterns`, `graphql-architect` |
| **AI, ML & Agents** | `deep-learning-architecture-advisor`, `self-supervised-learning-jepa`, `ai-agent-discovery`, `multi-agent-execution-benchmark`, `kanban-agent-pipeline`, `eval-harness` |
| **DevOps & Infrastructure** | `aws-cloud-architecture`, `terraform-infrastructure-as-code`, `kubernetes-architect`, `docker-expert`, `decentralized-cluster-management`, `prometheus-configuration` |

---

## Interactive Documentation (GitHub Pages)

The complete interactive documentation and live skill search explorer is available at:
**[https://krishujeniya.github.io/AGYOS/](https://krishujeniya.github.io/AGYOS/)**

The documentation site is 100% static, client-side, zero-dependency, and automatically deployed via GitHub Actions on every commit to `main`.

---

## Citation & Authorship

If you utilize this cognitive architecture, skill catalog, or governance framework in your research, agents, or production deployments, please cite:

```bibtex
@software{ujeniya2026agentskills,
  author       = {Krish Ujeniya},
  title        = {AGYOS: Autonomous AI Agent Frameworks, Workflow Orchestrators & Engineering Skills Monorepo},
  year         = {2026},
  url          = {https://github.com/krishujeniya/AGYOS},
  note         = {Monorepo containing 1,842 modular skills, 5-gate lifecycle governance, and FastMCP daemon}
}
```

---

## License

Licensed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file for terms and conditions.

**Created & Maintained by Krish Ujeniya**  
*Website: [https://github.com/krishujeniya/AGYOS](https://github.com/krishujeniya/AGYOS)*
