<p align="center">
  <img src="assets/logo.svg" alt="AGYOS Logo" width="220" />
</p>

<h1 align="center">AGYOS</h1>

<p align="center">
  <strong>Autonomous Cognitive Agent Operating System &amp; Monorepo of 1,849+ Engineering Skills</strong><br />
  <em>Engineered &amp; Authored by Krish Ujeniya</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache-2.0" /></a>
  <img src="https://img.shields.io/badge/Skills-1%2C849%20Skills-00F0FF.svg" alt="Skills Count" />
  <img src="https://img.shields.io/badge/Protocol-Model%20Context%20Protocol%20(MCP)-6366F1.svg" alt="MCP Daemon" />
  <img src="https://img.shields.io/badge/Verification-51%2F51_Passed-10B981.svg" alt="Verification" />
  <a href="https://krishujeniya.github.io/AGYOS/"><img src="https://img.shields.io/badge/Docs-GitHub%20Pages-A855F7.svg" alt="Documentation" /></a>
</p>

---

## Overview

**AGYOS** is an autonomous cognitive agent operating system and physical catalog of 1,849+ modular engineering skills, designed to give AI agents deterministic reliability, zero-speculation code generation, and multi-model consensus.

All skills reside in a single flat directory with zero subfolders, clear task-based naming, and zero external branding. Every skill encodes proven, actionable runbooks for software architecture, full-stack engineering, security testing, performance tuning, and technical operations.

AGYOS bridges natural-language, exploratory vibe coding with top-1% FAANG / Research Lab engineering rigor. Non-technical operators and high-velocity builders describe what they want to achieve, while AGYOS autonomously enforces strict boundary validation, immutability, zero-leak credential management, test-driven development, and deterministic machine verification.

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
                                    │ 1,849+ MODULAR RUNBOOK SKILLS  │
                                    │ (Frontend, Backend, Security)  │
                                    └────────────────────────────────┘
```

### 1. Unified Flat Skill Catalog
- **1,849 Physical Skills**: Every skill is stored directly under `.agents/skills/<name>/SKILL.md` (and mirrored at `skills/<name>/SKILL.md`).
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
  - `agyos_decision`: Classify task domain, assess gate complexity, and select optimal specialist skills.
  - `agyos_state`: Inspect active governance milestone and gate status.
  - `agyos_current`: Human-readable session overview from `CURRENT.md`.
  - `agyos_graph`: Dependency index and system invariant graph.
  - `agyos_checkpoint`: Append structured execution checkpoints.
  - `agyos_find_skill`: Fast sub-10ms keyword and semantic search over 1,849 skills.
  - `agyos_sys_info`: Comprehensive kernel health and subsystem status.
  - `agyos_memory`: Virtual multi-tier cross-session memory manager.

### 4. AGYOS Decision Engine (`agyos_decision` & `bin/agyos decide`)
- Fast, non-autoregressive System 1 decision engine and skill router.
- Automatically classifies incoming tasks across technical domains (`debugging`, `architecture`, `security`, `ui_ux`, `motion`, `database`, `performance`, `devops`, `seo`, `content`).
- Evaluates task complexity on a 1–5 scale:
  - **Complexity 1–2 (Fast-Path)**: Trivial or single-file edits bypass Gates 1–3 straight to `IMPLEMENT`.
  - **Complexity 3–5 (Standard / High-Impact)**: Multi-file features and architecture trigger the complete 5-gate lifecycle.
- Ranks candidate specialist skills from the 1,849 catalog with heuristic relevance scores and exact runbook paths.
- Accessible via CLI (`bin/agyos decide "<task>"`), MCP tool (`agyos_decision`), and Python API (`from agyos_decision import decide_skill`).

### 5. Zero-Slash Automation
No slash commands or manual mode switches required. The system automatically inspects user intent, discovers matching specialist runbooks via `agyos_decision`, and executes work with direct machine evidence.

---

## The Vibe-to-FAANG Autonomous Operating Model

The central challenge with AI-assisted software generation is the divergence between high-level prompt intent ("vibe coding") and production-grade engineering realities. Left ungoverned, AI assistants generate speculative code, swallow exceptions with bare `except: pass`, hardcode environment credentials, ignore database index constraints, and omit test verification.

AGYOS solves this by embedding a **Virtual FAANG Corporate Engineering Squad** directly into the agent runtime. Operators express ideas in natural human language, while AGYOS autonomously drives execution through Staff and Principal-level rigor.

```
                    ┌────────────────────────────────────────────────────────┐
                    │               NATURAL PROMPT / VIBE INTENT             │
                    │      "Build an AI video subscription app with auth"    │
                    └────────────────────────────────────────────────────────┘
                                                │
                                                ▼
                    ┌────────────────────────────────────────────────────────┐
                    │       AGYOS DECISION ENGINE (Domain & Complexity)      │
                    │        Selects: stripe, clerk-auth, nextjs, drizzle    │
                    └────────────────────────────────────────────────────────┘
                                                │
                                                ▼
        ┌────────────────────────────────────────────────────────────────────────────────┐
        │                 AUTONOMOUS 5-PHASE TRANSFORMATION PIPELINE                     │
        ├────────────────────────────────────────────────────────────────────────────────┤
        │  PHASE 1: SHAPE SPEC (Staff PM)                                                │
        │  • Clarifies requirements, scope boundaries, and core user flows.              │
        │                                                                                │
        │  PHASE 2: CONTRACTS & ADR (Principal Systems Architect)                       │
        │  • Authors Architecture Decision Records (`docs/adr/`).                        │
        │  • Generates explicit Pydantic / TypeScript schema contracts.                  │
        │                                                                                │
        │  PHASE 3: TDD MAKER (Senior Software Engineer)                                 │
        │  • Writes failing test suite first (RED).                                      │
        │  • Implements minimal immutable code to pass (GREEN).                          │
        │  • Enforces <50 line functions and clean separation of concerns.               │
        │                                                                                │
        │  PHASE 4: VIBE AUDIT & SECURITY (Principal Security & Vibe Auditor)            │
        │  • Audits against 6 Production Invariants (no swallowed errors, no leaks).     │
        │  • Scans secrets, validates SQL boundaries, verifies CSS compositor motion.   │
        │                                                                                │
        │  PHASE 5: MACHINE VERIFICATION (Staff QA & Verification Lead)                  │
        │  • Executes compiler, linter, unit, and integration suites (80%+ coverage).    │
        │  • Enforces Test Ratchet (monotonically non-decreasing test assertions).       │
        └────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
                    ┌────────────────────────────────────────────────────────┐
                    │            FAANG-GRADE PRODUCTION ARTIFACT             │
                    │        Clean tests, documented ADR, zero tech debt     │
                    └────────────────────────────────────────────────────────┘
```

### The 6 Production Invariants for Vibe Coders

Every piece of generated code must satisfy six non-negotiable invariants:

1. **Boundary Input Validation**: All external inputs (query parameters, body payloads, webhook signatures, file uploads) must be strictly validated using schema contracts (`Pydantic`, `Zod`, or `TypeSpec`) before touching business logic.
2. **Zero Silent Error Swallowing**: Catching bare `except:` or ignoring rejected promises is strictly blocked. Every error must be typed, logged with contextual telemetry, or propagated cleanly.
3. **Safe & Idempotent Data Layer**: Database mutations must use transactions and idempotency keys. Queries must specify column selection (no unbounded `SELECT *`) and respect indexed lookups.
4. **Immutability & Size Ceilings**: Functions must stay under 50 lines with a single responsibility. State must be treated as immutable, returning updated copies rather than mutating in place. Source files observe an 800-line maintainability ceiling.
5. **Zero-Secret Security Invariant**: API keys, webhook secrets, database connection strings, and private keys must never appear in source code or repositories. Environment variables or secure secret managers are mandatory.
6. **Deterministic Machine Evidence**: No feature or bugfix is marked complete without executing passing test and compiler output. Speculative completion claims are strictly forbidden.

### The 9 Autonomous Corporate Roles

AGYOS operationalizes the organizational divisions of FAANG research and engineering labs:

| Role | Operational Scope & Ownership |
|------|-------------------------------|
| **Product VP / Staff PM** | Translates informal user prompts into rigorous PRDs, user stories, and acceptance boundaries. |
| **Principal Systems Architect** | Establishes C4 container architecture, dataflow diagrams, and durable Architecture Decision Records. |
| **Staff Software Engineer (Maker)** | Writes clean, focused, functional code via Red-Green-Refactor TDD loops. |
| **Principal Security Engineer** | Performs STRIDE threat modeling, OWASP Top 10 boundary audits, and zero-leak credential audits. |
| **Staff QA & Verification Lead** | Generates regression tests, mutation suites, and enforces test ratchet monotonicity. |
| **Site Reliability Engineer (SRE)** | Validates operational readiness, health checks, graceful shutdown handling, and rollback plans. |
| **Principal ML / Data Engineer** | Enforces dataset contract integrity, training split boundaries, and latency benchmarks. |
| **Legal & Compliance Counsel** | Validates open-source license compatibility (Apache 2.0 / MIT vs GPL) and privacy boundaries (GDPR). |
| **BizOps & FinOps Director** | Optimizes inference routing economics across fast and high-capability model tiers. |

### Specialized Subagent Roster

AGYOS provides 81 specialized agents configured under `.agents/agents/` that can be directly dispatched by the orchestrator:
- `vibe-engineer`: Translates exploratory vibe coding into structured FAANG specifications, tests, and production code.
- `faang-architect`: Senior technical architect for system scalability, API contracts, ADRs, and failure domain containment.
- `code-reviewer`: Proactive reviewer for maintainability, idiomatic style, and polyglot quality standards.
- `security-reviewer`: Dedicated security analyst checking OWASP Top 10 vulnerabilities, input handling, and secrets.
- `qa-tdd-architect`: Specialist enforcing the Arrange-Act-Assert testing pattern and 80%+ test coverage.

---

## Repository Structure

```
├── .agents/
│   ├── agents/                 # 81 Specialized corporate role agent definitions
│   ├── plugins/                # Validated governance plugins (rules and config)
│   ├── rules/                  # 140 Modular governance, polyglot, and SDLC rules
│   ├── skills/                 # 1,849 Production skills (flat, 1 folder per skill)
│   ├── state/                  # 5-Gate runtime state and checkpoint journals
│   ├── workflows/              # 100 Multi-agent execution pipelines
│   ├── skills-manifest.json    # Complete index of 1,849 skills
│   └── tier1-skills.json       # Curated high-frequency skill registry
├── agyos_decision/             # Autonomous Decision Engine & skill routing package
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
│   ├── agyos-verify.sh         # Adversarial verification test suite (51 checks)
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

# Run comprehensive 51-point verification suite
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

The repository contains **1,849 skills** organized across major disciplines:

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
  note         = {Monorepo containing 1,849 modular skills, 5-gate lifecycle governance, and FastMCP daemon}
}
```

---

## License

Licensed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file for terms and conditions.

**Created & Maintained by Krish Ujeniya**  
*Website: [https://github.com/krishujeniya/AGYOS](https://github.com/krishujeniya/AGYOS)*
