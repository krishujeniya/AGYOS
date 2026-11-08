<p align="center">
  <img src="assets/logo.svg" alt="AGYOS Logo" width="220" />
</p>

<h1 align="center">AGYOS</h1>

<p align="center">
  <strong>Autonomous Cognitive Agent Operating System &amp; Monorepo of 1,862+ Engineering Skills</strong><br />
  <em>Engineered &amp; Authored by Krish Ujeniya</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-000000.svg" alt="License: Apache-2.0" /></a>
  <img src="https://img.shields.io/badge/Skills-1%2C862%20Skills-000000.svg" alt="Skills Count" />
  <img src="https://img.shields.io/badge/Protocol-FastMCP_2.0-000000.svg" alt="FastMCP Protocol" />
  <img src="https://img.shields.io/badge/Pods-5_Corporate_Pods-000000.svg" alt="Corporate Pods" />
  <img src="https://img.shields.io/badge/Verification-51%2F51_Passing-000000.svg" alt="Verification" />
  <a href="https://krishujeniya.github.io/AGYOS/"><img src="https://img.shields.io/badge/Docs-GitHub_Pages-000000.svg" alt="Documentation" /></a>
</p>

---

## Overview

**AGYOS** is an autonomous cognitive agent operating system and physical catalog of 1,862+ modular engineering skills, designed to give AI coding agents deterministic reliability, zero-speculation code generation, fail-closed safety, and multi-model consensus.

All skills reside in a single flat directory with zero nested subfolders, clear task-based naming, and zero external branding. Every skill encodes proven, actionable runbooks for software architecture, full-stack engineering, security testing, performance profiling, and operational workflows.

AGYOS bridges exploratory, natural-language "vibe coding" with top-1% FAANG and Research Lab engineering rigor. Non-technical operators and high-velocity builders describe what they want to achieve, while AGYOS autonomously enforces strict boundary input validation, immutability, zero-leak credential management, test-driven development (TDD), and deterministic machine verification.

---

## Autonomous Cognitive Architecture

```
                                    ┌────────────────────────────────┐
                                    │    NATURAL LANGUAGE PROMPT     │
                                    └────────────────────────────────┘
                                                    │
                                                    ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │          SEARCH-FIRST AUTONOMOUS SKILL DISCOVERY            │
                      │  (Zero-Slash Ingestion: Finds exact runbook in <10ms)       │
                      └─────────────────────────────────────────────────────────────┘
                                                    │
         ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
         ▼                                          ▼                                          ▼
┌─────────────────┐                        ┌─────────────────┐                        ┌─────────────────┐
│  5-GATE ENGINE  │                        │  FASTMCP STDIO  │                        │  AGENT COUNCIL  │
│ 5-Step Lifecycle│                        │  State Daemon   │                        │  Deliberation   │
└─────────────────┘                        └─────────────────┘                        └─────────────────┘
         │                                          │                                          │
         └──────────────────────────────────────────┼──────────────────────────────────────────┘
                                                    ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │           5 MERGED CORPORATE EXECUTION PODS                 │
                      │  (pod-growth, pod-customer, pod-build, pod-gna, pod-people) │
                      └─────────────────────────────────────────────────────────────┘
                                                    │
                                                    ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │             1,862+ PHYSICAL RUNBOOK SKILLS                  │
                      │  (Architecture, Fullstack, Pentesting, ML, Operations)      │
                      └─────────────────────────────────────────────────────────────┘
```

---

## Quickstart & One-Prompt Autonomous Setup

### 1. One-Prompt Agent Setup (For AI Assistants)

Paste this single prompt directly into your AI coding assistant (Google Antigravity `agy`, Claude Code, Cursor, Codex) to clone, configure, and verify AGYOS in one autonomous pass:

```text
Set up and initialize the AGYOS autonomous cognitive operating system in this workspace:
1. If not already in the repository, clone https://github.com/krishujeniya/AGYOS.git and navigate into AGYOS:
   git clone https://github.com/krishujeniya/AGYOS.git && cd AGYOS
2. Ensure executable permissions on all core binaries and scripts:
   chmod +x bin/agyos scripts/agyos-init.sh scripts/agyos-verify.sh mcp/state-server.cjs scripts/hooks/*.py
3. Run the zero-configuration bootstrapper to initialize state, validate plugins, register the FastMCP state daemon, and compile indices:
   bash scripts/agyos-init.sh
4. Execute the verification suite and unit tests to ensure all 51 automated checks pass:
   bash scripts/agyos-verify.sh
   python3 -m unittest discover -s scripts/tests -v
5. Confirm the intent compiler and 5-pod router are operational:
   bin/agyos intent "audit system security and summarize findings"
Confirm when all 51 checks pass and the workspace is fully initialized.
```

### 2. Terminal 1-Liner (For Human Operators)

```bash
git clone https://github.com/krishujeniya/AGYOS.git && cd AGYOS && bash scripts/agyos-init.sh && bash scripts/agyos-verify.sh
```

---

## Skill selection for every task

Discover a relevant skill, read its runbook, apply the steps needed for the task,
and verify the result. Repeat discovery when the objective changes; reuse an
unchanged runbook already read in the session. The shared
[routing rule](.agents/rules/common-skill-routing.md) covers all 1,862 skills and
141 modular rules without loading the entire catalog into each prompt.

```bash
# Select a skill and return its instructions
bin/agyos decide "fix python crash" --json --runbook

# Search alternatives or read a known runbook
bin/agyos find "database schema migration"
bin/agyos skill database-design

# Rebuild and validate the complete catalog after metadata changes
python3 scripts/build_tiered_skills_manifest.py
python3 scripts/build_docs_data.py
python3 -m unittest scripts.tests.test_skill_routing -v
```

MCP `agyos_decision` accepts `include_runbook: true`. Task intent takes priority
over language keywords; unclassified tasks fall back to objective inspection.
Scores are matching heuristics, not probabilities. Returning a runbook does not
prove an assistant applied it. See [the operating contract and limits](docs/SKILL_ROUTING.md).

---

## The 5 Merged Corporate Execution Pods

AGYOS compresses 11 traditional company departments into five autonomous, high-velocity corporate pods. Each pod is bound to explicit host tool contracts and standard operating procedures:

| Corporate Pod | Merged Departments | Standard Operating Procedure (SOP) | Host Tools | Safety Risk Policy |
|---------------|-------------------|-----------------------------------|------------|--------------------|
| **`pod-growth`** | Marketing, Growth, Sales, Outbound Business Development | `.agents/skills/sop-growth/SKILL.md` | `read_file`, `write_file`, `edit_file`, `search_web` | Drafts local campaigns; zero unsanctioned external transmissions. |
| **`pod-customer`** | Support, Client Onboarding, Customer Success, Retention | `.agents/skills/sop-customer/SKILL.md` | `read_file`, `write_file`, `edit_file` | Read-only reproduction; diagnostics prior to customer communications. |
| **`pod-build`** | Core Engineering, QA, Architecture, DevSecOps, SRE | `.agents/skills/sop-build/SKILL.md` | `read_file`, `write_file`, `edit_file`, `run_command` | Autonomous TDD Red-Green-Refactor with 80%+ test coverage. |
| **`pod-gna`** | Finance, Accounting, Legal, Compliance, Executive Ops | `.agents/skills/sop-gna/SKILL.md` | `read_file`, `write_file`, `edit_file` | 4-eyes review hold; external disbursements held in `PENDING_COMMIT` outbox. |
| **`pod-people`** | Recruiting, HR, Talent Ops, Team Onboarding | `.agents/skills/sop-people/SKILL.md` | `read_file`, `write_file`, `edit_file` | Blind rubric scoring; objective applicant evaluation. |

### Autonomous Intent Routing Matrix

Every natural language prompt can be compiled into a target pod, action class, and risk level:

```bash
# Test intent classification from the command line:
bin/agyos intent "Implement checkout endpoint with Stripe idempotency"
# -> pod-build (action: feature_implementation, risk: R1, confidence: 0.98)

bin/agyos intent "Draft outbound cold email sequence for Series B SaaS"
# -> pod-growth (action: marketing_campaign, risk: R1, confidence: 0.95)

bin/agyos intent "Diagnose client report of 500 error on CSV export"
# -> pod-customer (action: ticket_triage, risk: R0, confidence: 0.96)

bin/agyos intent "Disburse vendor payment of $12,500 via ACH"
# -> pod-gna (action: financial_disbursement, risk: R3, confidence: 0.99)
```

---

## 5-Gate Lifecycle Governance Spine

Every non-trivial engineering workflow progresses through five deterministic gates:

```
[GATE 1: UNDERSTAND] ➔ [GATE 2: ANALYZE] ➔ [GATE 3: PLAN] ➔ [GATE 4: IMPLEMENT] ➔ [GATE 5: VERIFY]
```

1. **UNDERSTAND**: Clarify intent, gather requirements, document deliverables in a structured Task List.
2. **ANALYZE**: Read-only codebase AST inspection (`agyos-scout`), blast radius containment, complexity scoring:
   - **Complexity 1–2 (Fast-Path)**: Single-file or trivial edits skip straight to `IMPLEMENT`.
   - **Complexity 3–5 (Standard / High-Impact)**: Multi-file features and architecture trigger the complete 5-gate lifecycle.
3. **PLAN**: Architecture Decision Records (ADR in `docs/adr/`), C4 models, test strategy, and context compaction (`bin/compact.sh`).
4. **IMPLEMENT**: Autonomous TDD Red-Green-Refactor loop. Functions &lt;50 lines, source files &lt;800 lines.
5. **VERIFY**: Adversarial proof execution (`bin/agyos verify`), test ratchet monotonicity enforcement.

---

## Security & Fail-Closed Tool Architecture

AGYOS enforces native tool binding strictly aligned with Google Antigravity (`agy`) v1.5.0 host tools:
- `read_file`: Inspect repository files and read-only resources.
- `write_file`: Create new files within declared scope.
- `edit_file`: Contiguous targeted modifications to existing files.
- `run_command`: Local build and test suite execution.
- `search_web`: Web documentation and API research.

### Dual-Hook Architecture (`.agents/hooks.json`)

1. **Fail-Closed Authorizer (`scripts/hooks/authorizer.py`)**:
   - Executes synchronously *before* every tool call.
   - Evaluates commands against R0–R3 risk tiers.
   - Blocks dangerous operations (`rm -rf /`, unsanctioned token exports, live payment calls).
2. **Session Lifecycle Guardian (`scripts/hooks/agy_os_hook.py`)**:
   - Tracks session state, prevents identical retries, and maintains working memory.

### Risk Classification Tiers

- **`R0` (Read-Only)**: `read_file`, `search_web`. Auto-authorized.
- **`R1` (Benign Write)**: `write_file`, `edit_file` inside declared scope.
- **`R2` (System Execution)**: Local tests, linters, compilers via `run_command`. Requires pre-write snapshot.
- **`R3` (Irreversible / External)**: Live payments, external emails, remote deletions. **BLOCKED**; held in `PENDING_COMMIT` outbox until signed by a human operator.

### State Ledger Invariants (`agyos_decision/state_ledger.py`)

- **Hierarchy Caps**: Subagent depth &le; 2, fanout &le; 4, workers &le; 3, total tasks &le; 8.
- **Kahn's Acyclicity**: Task dependency graphs must be strictly acyclic DAGs.
- **Budget Guard**: 30,000 tokens / $1.50 cap per task, with 20% reserved for verification.
- **Reflection Memory**: Identical retries with the same error signature are blocked.
- **LIFO Saga Compensation**: Rollback executes inverse actions in reverse order on failure.

---

## Emil Kowalski UI/UX & Motion Engineering Standards

All frontend, website, and SaaS generation workflows enforce Emil Kowalski's 6 Design Engineering Invariants:

1. **Concentric Border Radii Formula**: Nested child radii must satisfy $R_{\text{inner}} = R_{\text{outer}} - \text{padding}$ to eliminate optical corner clipping.
2. **Animation Decision Framework**: 100+ times/day = 0ms (no motion); tens of times/day = 150–200ms; modals/drawers = 250–350ms; never animate keyboard actions.
3. **Compositor-Only Animations**: Animate ONLY `transform` and `opacity`. Never animate layout reflow properties (`width`, `height`, `margin`, `padding`).
4. **Tactile Micro-Interactions**: Active scale press feedback (`active:scale-[0.98]`) on interactive controls. Wrap hover transitions in `@media (hover: hover) and (pointer: fine)` to prevent sticky hover on touch devices.
5. **Popover Transform Origins**: Set `transform-origin` to trigger button coordinates, never screen center.
6. **Before / After / Why Review Table**: Mandatory markdown table for all visual UI/UX code reviews:

| Before | After | Why |
|--------|-------|-----|
| `transition: all 0.3s` | `transition: transform 0.15s ease` | Prevents layout thrashing and geometric reflow spikes. |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Physical UI elements do not scale from a dimensionless point. |
| `.btn:hover { ... }` | `@media (hover: hover) { .btn:hover { ... } }` | Prevents sticky hovered states on touch and mobile devices. |

---

## The Vibe-to-FAANG Autonomous Operating Model

The central challenge with AI-assisted software generation is the divergence between high-level prompt intent ("vibe coding") and production-grade engineering realities. Left ungoverned, AI assistants generate speculative code, swallow exceptions with bare `except: pass`, hardcode environment credentials, ignore database index constraints, and omit test verification.

AGYOS solves this by embedding a **Virtual FAANG Corporate Engineering Squad** directly into the agent runtime. Operators express ideas in natural human language, while AGYOS autonomously drives execution through Staff and Principal-level rigor:

### The 6 Production Invariants for Vibe Coders

1. **Boundary Input Validation**: All external inputs (query parameters, body payloads, webhook signatures, file uploads) must be strictly validated using schema contracts (`Pydantic`, `Zod`, or `TypeSpec`) before touching business logic.
2. **Zero Silent Error Swallowing**: Catching bare `except:` or ignoring rejected promises is strictly blocked. Every error must be typed, logged with contextual telemetry, or propagated cleanly.
3. **Safe & Idempotent Data Layer**: Database mutations must use transactions and idempotency keys. Queries must specify column selection (no unbounded `SELECT *`) and respect indexed lookups.
4. **Immutability & Size Ceilings**: Functions must stay under 50 lines with a single responsibility. State must be treated as immutable, returning updated copies rather than mutating in place. Source files observe an 800-line maintainability ceiling.
5. **Zero-Secret Security Invariant**: API keys, webhook secrets, database connection strings, and private keys must never appear in source code or repositories. Environment variables or secure secret managers are mandatory.
6. **Deterministic Machine Evidence**: No feature or bugfix is marked complete without executing passing test and compiler output. Speculative completion claims are strictly forbidden.

---

## 5-Tier OS Filesystem Layout

```
AGYOS/
├── .agents/                   # Core Runtime: 1,862 skills, 141 rules, 81 agents, 8 plugins
│   ├── agents/                # 81 Corporate role agent definitions (5 merged pods)
│   ├── plugins/               # 8 Validated governance plugins (rules and config)
│   ├── rules/                 # 141 Modular governance, polyglot, and SDLC rules (<24KB)
│   ├── skills/                # 1,862 Physical standalone skills (1 folder per skill)
│   ├── state/                 # 5-Gate runtime state, snapshots, and outbox queue
│   ├── workflows/             # 100 Multi-agent execution pipelines
│   ├── skills-manifest.json   # Complete index of 1,862 skills
│   └── tier1-skills.json      # Curated high-frequency skill registry
├── agyos_decision/            # Autonomous Intent Compiler, Task Contracts & State Ledger
├── assets/                    # Master monochrome vector branding (logo.svg, agyos-logo.svg)
├── bin/
│   ├── agyos                  # Kernel CLI (init, state, gate, verify, council, skill, intent)
│   ├── compact.sh             # Context compaction utility
│   ├── gate-check.sh          # Pre-commit test ratchet enforcer
│   └── state.sh               # Programmatic gate transitions
├── docs/                      # Pure static documentation website (GitHub Pages ready)
│   ├── index.html             # Interactive skill catalog explorer and search
│   ├── docs.css               # Polished responsive styling (concentric radii & mobile ergonomics)
│   ├── docs.js                # Client-side instantaneous search across 1,862 skills
│   └── skills-data.json       # Pre-indexed search data
├── mcp/
│   ├── state-server.cjs       # FastMCP zero-dependency stdio JSON-RPC daemon
│   └── README.md
├── scripts/
│   ├── agyos-verify.sh        # Adversarial verification test suite (51 checks)
│   ├── agyos-init.sh          # Environment bootstrapper and self-repair
│   └── hooks/                 # Real-time fail-closed authorizer.py and agy_os_hook.py
├── skills/                    # Direct link to .agents/skills/
├── rules/                     # Direct link to .agents/rules/
├── workflows/                 # Direct link to .agents/workflows/
├── CITATION.cff               # Academic and professional citation metadata
├── LICENSE                    # Apache 2.0 open-source license
└── README.md                  # Primary project documentation
```

---

## CLI Reference (`bin/agyos`)

```bash
# Initialize or self-repair AGYOS
bin/agyos init

# Execute 51-point adversarial verification suite
bin/agyos verify

# Inspect active milestone, gate, and session state
bin/agyos state

# Compile intent into target pod, action class, and risk level
bin/agyos intent "Implement checkout endpoint with Stripe idempotency"

# Run autonomous System 1 skill discovery
bin/agyos decide "Design Postgres database schema with migrations"

# Fast-path bypass for minor edits (jumps directly to IMPLEMENT)
bin/agyos fast

# Convene multi-model consensus via Agent Council
bin/agyos council "Postgres vs SQLite for local cache?"

# Query skill runbook
bin/agyos skill postgres-best-practices
```

---

## Skills Catalog Discipline Highlights

The repository contains **1,862 skills** organized across major engineering disciplines:

| Discipline | Key Skills |
|------------|------------|
| **Architecture & Systems** | `architecture-decision-framework`, `clean-architecture-craftsmanship`, `c4-architecture`, `hexagonal-architecture`, `microservices-patterns`, `event-sourcing-architect` |
| **Security & Pentesting** | `pentagi-orchestrator`, `ssrf-oob-interaction-testing`, `xxe-xml-injection-testing`, `cve-vulnerability-intelligence`, `security-sandbox-runner`, `metasploit-framework`, `sqlmap-database-pentesting` |
| **Frontend & UI/UX** | `ui-design-engineering-standards`, `apple-design`, `wcag-accessibility-compliance`, `shadcn-ui-components`, `web-animation-design`, `threejs-webgl-development`, `tailwind-patterns` |
| **Backend & Databases** | `database-schema-modeling`, `postgres-patterns`, `fastapi-pro`, `rust-patterns`, `golang-patterns`, `redis-patterns`, `graphql-architect` |
| **AI, ML & Agents** | `deep-learning-architecture-advisor`, `self-supervised-learning-jepa`, `ai-agent-discovery`, `multi-agent-execution-benchmark`, `kanban-agent-pipeline`, `eval-harness` |
| **DevOps & Infrastructure** | `aws-cloud-architecture`, `terraform-infrastructure-as-code`, `kubernetes-architect`, `docker-expert`, `decentralized-cluster-management`, `prometheus-configuration` |

---

## Adversarial Verification Suite

Run the proof runner in your environment. The following output is illustrative; current results depend on installed dependencies and host access:

```bash
bash scripts/agyos-verify.sh
```

```text
• AGENTS.md size limit (<24,000 bytes): PASS
• GEMINI.md exists and matches AGENTS.md: PASS
• AGY CLI installed and responsive: PASS
• AGYOS MCP server registered in AGY: PASS
• AGYOS Safety Hook blocks dangerous commands: PASS
• AGYOS Safety Hook allows benign commands: PASS
• AGYOS MCP server JSON-RPC initialize: PASS
• AGYOS MCP server tools/list: PASS
• AGYOS MCP server tools/call (agyos_state): PASS
• AGYOS MCP server tools/call (agyos_decision): PASS
• bin/agyos decide CLI decision engine: PASS
• Agent Council Bun test suite (59 passing tests): PASS
• 8 AGYOS Plugins validated: PASS
• Merged skills catalog (>400 skills in .agents/skills): PASS (1,862 skills)
• Merged rules catalog (>120 rules in .agents/rules): PASS (141 rules)
• AGYOS master logo exists: PASS
• bin/agyos executable functional: PASS
• Tiered skills manifest exists and valid: PASS
• Fast-path state bypass functional: PASS
============================================================
Verification Summary: 51 PASSED, 0 FAILED
```

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
  note         = {Monorepo containing 1,862 modular skills, 5-gate lifecycle governance, 5 corporate pods, and FastMCP daemon}
}
```

---

## License

Licensed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file for terms and conditions.

**Created & Maintained by Krish Ujeniya**  
*GitHub: [https://github.com/krishujeniya/AGYOS](https://github.com/krishujeniya/AGYOS)*

## Pinned Third-Party Capability Integrations

AGYOS keeps its existing six-layer architecture, five gates, five corporate pods, skill catalog, and risk approvals. A reviewed eight-source integration registry lives in [`integrations/registry/sources.json`](integrations/registry/sources.json). The registry pins source commits and routes narrowly defined, multi-concept natural-language tasks to **existing** AGYOS skills; it does not load upstream instructions or grant new tool permissions.

The Python source matcher is `agyos_decision.integrations.source_registry`. A separate, optional `agent_reach_adapter` offers restricted read-only searches when the verified official CLI is present. Upstream skill catalogs, prompt archives and Azure infrastructure remain reference-only until each component passes licensing, dependency and security review. See [the integration report](docs/integrations/INTEGRATION_REPORT.md) for evidence and limitations.

## Optional Endpoint-Side Encrypted File Exchange

AGYOS provides a **separate, opt-in encrypted envelope** for sending files between two trusted endpoints. It uses X25519 key agreement with per-message ephemeral keys, HKDF-SHA256 key derivation, AES-256-GCM authenticated encryption, and Ed25519 sender signatures. Private identity keys are encrypted with scrypt and saved outside the Git repository. See [Encryption scope and usage](docs/security/END_TO_END_ENCRYPTION.md).

This is **not a claim that the whole AGYOS runtime is end-to-end encrypted**. Existing MCP memory, telemetry, prompts sent to model vendors and other third-party integrations are not covered. They require separate data-flow controls and provider agreements. The encrypted exchange does not enable itself or replace the existing AGYOS governance.


## Endpoint-to-endpoint encrypted exchange (opt-in)

AGYOS includes an independently keyed, authenticated **file exchange** using X25519, HKDF-SHA-256, AES-256-GCM, Ed25519 signatures, and passphrase-protected local private identities. See [E2EE limitations and setup](docs/security/E2EE.md). Invoke `bin/agyos secure help`. **This does not make all AGYOS traffic end-to-end encrypted**: model-provider requests, the existing MCP stdio tools, public skills, and plaintext memory/state are outside this encryption boundary. Do not place private keys or plaintext secrets in Git.
