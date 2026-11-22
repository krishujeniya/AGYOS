<p align="center">
  <img src="assets/agyos-logo.svg" alt="AGYOS" width="180" />
</p>

<h1 align="center">AGYOS</h1>

<p align="center">
  <strong>Autonomous Cognitive Operating System for AGY CLI</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-blue.svg" alt="Apache 2.0 license" /></a>
  <a href="https://agyos.pages.dev"><img src="https://img.shields.io/badge/Cloudflare_Pages-Active-F38020?style=flat-square&logo=cloudflare" alt="Documentation site" /></a>
</p>

AGYOS is an autonomous operating system and multi-agent execution kernel for AGY CLI. It is built for solopreneurs, independent operators, and autonomous agent swarms to plan, build, review, test, and ship software under strict engineering invariants.

The system combines a 13-crate Rust engine and 2 applications with an enterprise organization of 104 operational roles across 12 departments, a 2,289-skill catalog with on-demand runbook retrieval, a Token-Oriented Object Notation (TOON) codec, and an automated 7-step cycle (`Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect`).

---

## Architecture

```mermaid
flowchart TD
    User(["Operator / User Request"]):::operator

    subgraph CognitiveLayer["1. Intent & Cognitive Governance"]
        Intent["Intent Compilation & EVPI<br/><code>TaskContract • Howard 1966 Decision</code>"]
        Pods["104-Role Virtual Organization<br/><code>12 Departments • 5 Governing Pods</code>"]
        Catalog["Skill Discovery & Retrieval<br/><code>2,289 Skills • On-Demand Runbooks</code>"]
    end

    subgraph AutonomousCycle["2. 7-Step Autonomous Engineering Cycle"]
        direction LR
        S1["1. Think<br/><code>Role & Skill Alignment</code>"] --> S2["2. Plan<br/><code>Checkpoints & Blueprint</code>"]
        S2 --> S3["3. Build<br/><code>Maker TDD Execution</code>"]
        S3 --> S4["4. Review<br/><code>Checker Audit & Diff Hygiene</code>"]
        S4 --> S5["5. Test<br/><code>Deterministic Static Gates</code>"]
        S5 --> S6["6. Ship<br/><code>Scoped Commit & Lock</code>"]
        S6 --> S7["7. Reflect<br/><code>AI_HANDOFF & Milestone Close</code>"]
    end

    subgraph StorageEngine["3. Rust ACID Storage Engine (crates/store)"]
        direction TB
        WAL[("Append-Only WAL<br/><code>Monotonic Event Revisions</code>")]
        Outbox["Transactional Outbox<br/><code>Zero-Loss Guarantee (RPO=0)</code>"]
        Dedup["Deduplication Table<br/><code>Idempotency Key + Payload Hash</code>"]
        Fence["Durable Disk Fence<br/><code>Writer Monotonic Fencing</code>"]
        WAL --- Outbox
        WAL --- Dedup
        WAL --- Fence
    end

    subgraph WorkerPool["4. Hosted Execution & Business Adapters"]
        Worker["Hosted Worker Pool (apps/worker)<br/><code>Fair Admission • Lease Management</code>"]
        Adapters["Domain Business Adapters (crates/adapters)<br/><code>Git • CRM • Billing • Legal • Hiring • Web</code>"]
        Codec["TOON Codec Engine (crates/toon-codec)<br/><code>Typed Parsing • Exact Encoding</code>"]
    end

    subgraph ReleaseGate["5. Gated Verification & Delivery"]
        CI["GitHub Actions Remote Builder<br/><code>Clean Rebuilds • Provenance Digests</code>"]
        MainBranch[("Protected Single main Branch<br/><code>Author: Krish Ujeniya</code>")]
    end

    %% Connections
    User -->|"Natural Language Prompt"| Intent
    Intent -->|"Assigns Lead Role"| Pods
    Pods -->|"Selects Specialist Skill"| Catalog
    Catalog -->|"Dispatches TaskContract"| AutonomousCycle

    S3 <-->|"Atomic Revisions & Snapshot"| StorageEngine
    S4 <-->|"Audits Evidence Receipts"| Adapters
    Worker <-->|"Executes Dispatched Jobs"| StorageEngine

    S5 -->|"Triggers Verification"| CI
    CI -->|"Verifies Artifacts & Digests"| S6
    S6 -->|"Fast-Forward Merge"| MainBranch

    %% Class Styles
    classDef operator fill:#2563eb,stroke:#1d4ed8,color:#ffffff,stroke-width:2px;
```

---

## Core Components

The repository is organized into a modular workspace containing 13 library crates and 2 application packages:

| Component | Path | Responsibility |
|:---|:---|:---|
| **Domain** | `crates/domain` | Typed `TaskContract`, R0-R3 risk boundaries, and exact micro-currency accounting |
| **TOON Codec** | `crates/toon-codec` | Deterministic Token-Oriented Object Notation encoder, decoder, and minifier |
| **Governance** | `crates/governance` | Policy engine and state transition invariants |
| **Store** | `crates/store` | Transactional append-only event store, outbox, deduplication, and fence tokens |
| **Effects** | `crates/effects` | Dispatched external effects and compensating sagas |
| **Catalog** | `crates/catalog` | 104-role registry, 2,289-skill catalog, and role alignment |
| **Runtime** | `crates/runtime` | Progressive retrieval, Howard 1966 EVPI decision engine, and Agent Councils |
| **AGY Bridge** | `crates/agy` | AGY CLI boundary projection, isolated workspaces, and broker confinement |
| **Adapters** | `crates/adapters` | 8 domain adapters (CRM, billing, legal, hiring, Git, web, helpdesk, models) |
| **Telemetry** | `crates/telemetry` | Redacted metrics, bounded telemetry ring buffers, and local backup/restore |
| **Migration** | `crates/migration` | Shadow reader reconciler and cutover roll-forward/reversal drills |
| **Release** | `crates/release` | Release verification gates, provenance matching, and handover receipts |
| **Maintenance** | `crates/maintenance` | 14-day canary observation evaluation and maintenance risk registers |
| **CLI App** | `apps/agyos` | Native CLI entry point and diagnostic kernel |
| **Worker App** | `apps/worker` | Hosted worker pool, fair round-robin queue admission, and authenticated backups |

---

## The 7-Step Autonomous Cycle

AGYOS executes engineering workflows autonomously through a 7-step cycle without requiring manual slash commands:

1. **Think:** Compiles natural language intent into a typed `TaskContract`, computes Howard 1966 EVPI for clarification, assigns the lead role, and identifies specialist skill runbooks.
2. **Plan:** Produces architectural blueprints, acceptance criteria, concrete task breakdowns, and structured milestone checkpoints.
3. **Build:** Executes Maker TDD (RED -> GREEN -> REFACTOR) complying with production invariants.
4. **Review:** Independent Checker audit for code quality, secret leakage, OWASP Top 10 vulnerabilities, and git hygiene.
5. **Test:** Monotonic remote static and integration verification strictly via GitHub Actions.
6. **Ship:** Delivery strictly to the single `main` branch under verified author identity after passing all gates.
7. **Reflect:** Logs structured handoffs to `AI_HANDOFF.md`, updates state checkpoints, and records durable memory.

---

## 104-Role Organization Matrix

AGYOS models an enterprise organization partitioned into 12 functional departments and governed by 5 operational pods:

- **`pod-build`** (43 roles): Engineering, Architecture, Systems Design, DevOps, QA, and Infrastructure.
- **`pod-growth`** (21 roles): Marketing Strategy, Conversion Rate Optimization, Content Creation, and Sales Pipeline.
- **`pod-customer`** (8 roles): Customer Success, Support Operations, Client Onboarding, and Account Management.
- **`pod-gna`** (27 roles): Finance, Treasury, Legal Compliance, Risk Management, and Corporate Governance.
- **`pod-people`** (5 roles): Talent Acquisition, Human Resources, Compliance, and Learning & Development.

---

## Engineering Invariants

- **Single `main` Branch Exclusive:** All development lands strictly on `main`. No feature branches, task branches, or divergent worktrees are permitted.
- **Identity Lock:** All commits must be authored and committed under the verified GitHub identity:
  `Krish Ujeniya <100012208+krishujeniya@users.noreply.github.com>`.
- **GitHub Actions Verification Mandatory:** Unit tests, integration suites, compilers, and linters execute strictly in GitHub Actions runners (`remote-builder.yml` and `ci.yml`). Local operations are limited to read-only static inspection and `git diff --check`.
- **Mandatory `uv` for Python:** All Python package management, virtual environments, and script executions strictly use `uv` (`uv run`, `uv pip`, `uv tool`). Raw invocation of `python` or `pip` is forbidden.
- **Bounded Working Sets:** Memory ceiling of <= 256 MiB steady RSS with bounded telemetry ring buffers.
- **Zero Plaintext Secrets:** Zero hardcoded tokens or secrets; environment variables use startup redaction.

---

## Quickstart & CLI Commands

### 1. Skill Discovery & Selection
```bash
# Select optimal skill and inspect instructions
bin/agyos decide "debug concurrent async Rust actor" --json --runbook

# Search catalog across 2,289 capabilities
bin/agyos find "database migration reversal"

# Display specific runbook
bin/agyos skill database-migrations
```

### 2. Autonomous Cycle Dispatch
```bash
# Execute end-to-end 7-step autonomous cycle
bin/agyos cycle "Implement tenant isolation adapter with W3C PROV receipt"

# Read active operational state and current gate
bin/agyos state
```

### 3. Role Matrix Inspection
```bash
# List enterprise roles
bin/agyos roles

# Inspect specific role profile
bin/agyos role role-solopreneur-operator
```

### 4. TOON Codec & Compilation
```bash
# Compile role definition into TOON
bin/agyos toon-agent role-swe --compact

# Compile skill runbook into compact TOON card
bin/agyos toon-skill software-architecture --compact

# Encode or minify TOON documents
bin/agyos toon encode --input sample.json --output sample.toon
bin/agyos toon minify --input sample.toon
```

---

## Repository Layout

```text
.
├── bootstrap.rs                 # Rust workspace orchestrator & compilation driver
├── build/                       # Build profiles & locked workspace declarations (workspace.toon)
├── crates/                      # 13 Library Crates
│   ├── domain/                  # Contracts, R0-R3 risk boundaries, balance ledger
│   ├── toon-codec/              # Pure TOON format encoder, decoder & conformance tests
│   ├── governance/              # Policy engine and state transition invariants
│   ├── store/                   # Event log, transactional outbox, deduplication, fence tokens
│   ├── effects/                 # Dispatched external effects & compensating sagas
│   ├── catalog/                 # 104-role registry, canonical skills, phrase router
│   ├── runtime/                 # Progressive retrieval, Howard EVPI, context budgets, councils
│   ├── agy/                     # AGY CLI boundary projection & broker confinement
│   ├── adapters/                # 8 domain adapters (CRM, billing, legal, hiring, Git, web)
│   ├── telemetry/               # Redacted metrics, local backup engine, incident runbooks
│   ├── migration/               # Shadow reader reconciler, signed difference ledgers
│   ├── release/                 # Release verification gates, clean machine verifier, cutover guard
│   └── maintenance/             # Canary evaluation, vendor-free export/restore, risk register
├── apps/                        # Production Applications
│   ├── agyos/                   # Native CLI application & diagnostic kernel
│   └── worker/                  # Hosted worker pool, fair queue admission, authenticated backups
├── .agents/                     # Agent definitions, workflows, rules, and skills
│   ├── agents/                  # 104 role agent profiles in TOON/XML format
│   ├── rules/                   # Operational and engineering policies
│   ├── skills/                  # 2,289 skill runbooks and reference materials
│   ├── state/                   # Active operational state (CURRENT.toon, state.json, checkpoints/)
│   └── workflows/               # Autonomous execution cycle workflows
├── bin/                         # Developer CLI binaries (bin/agyos, bin/state.sh)
├── docs/                        # Specifications, architecture models, research decision records
└── knowledge/                   # Canonical skill runbooks, aliases, unavailable catalog
```

---

## License & Security

This project is licensed under the Apache License 2.0. See [`LICENSE`](LICENSE) for details.

Security policies and vulnerability reporting procedures are documented in [`SECURITY.md`](SECURITY.md).
