<p align="center">
  <img src="assets/agyos-logo.svg" alt="AGYOS" width="180" />
</p>

<h1 align="center">AGYOS</h1>

<p align="center">
  <strong>Autonomous Cognitive Operating System and Bounded Multi-Agent Kernel</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-blue.svg" alt="Apache 2.0 license" /></a>
  <a href="https://github.com/krishujeniya/AGYOS/actions/workflows/remote-builder.yml"><img src="https://github.com/krishujeniya/AGYOS/actions/workflows/remote-builder.yml/badge.svg" alt="Remote Builder CI" /></a>
  <a href="https://krishujeniya.github.io/AGYOS/"><img src="https://img.shields.io/badge/Docs-GitHub_Pages-blue.svg" alt="Documentation site" /></a>
</p>

AGYOS (Antigravity Operating System) is an autonomous cognitive operating system and bounded multi-agent kernel designed for solopreneurs, independent engineers, and autonomous agent fleets. It combines a 15-crate native Rust kernel, a 104-role virtual corporate organization across 12 departments and 5 governing operational pods, a 2,289-skill catalog with on-demand physical runbook retrieval, a tri-format semantic compilation engine (TOON, XML, and typed JSON), and a 7-step autonomous cycle (`Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect`).

The runtime is qualified across local production (2 vCPU / 2 GiB reference hardware) and heavy production hosted profiles, with strict boundary enforcement, Howard 1966 EVPI intent clarification, zero-loss crash recovery, and monotonic remote CI verification.

---

## Architecture Overview

```text
Prompt / Task Intent
         │
         ▼
[ Intent Compilation & Howard 1966 EVPI Clarification ]
         │
         ▼
[ 104-Role Virtual Matrix & 5 Operational Pods ]
         │
         ▼
[ Progressive Retrieval & 2,289-Skill Catalog ]
         │
         ▼
[ 7-Step Autonomous Engineering Cycle ]
  Think ──► Plan ──► Build ──► Review ──► Test ──► Ship ──► Reflect
         │
         ▼
[ 15-Crate Native Rust Kernel & ACID Storage Engine ]
  • Event Revisions & Outbox Log (RPO = 0)
  • Deduplication & Monotonic Fence Tokens
  • Encrypted Backups & 100% Retained Reversal Drill
         │
         ▼
[ Remote Builder CI & Gated Release Certification ]
```

---

## Core Capabilities

### 1. 15-Crate Native Rust Kernel
- **High-Performance Memory Ceiling:** Bounded working set <= 256 MiB steady RSS; sub-35ms p99 routing latency.
- **Transactional State Engine (`crates/store`):** Append-only event store, transactional outbox with monotonic fence tokens (`FenceToken`), deduplication tables, and crash recovery with RPO = 0.
- **TOON Codec (`crates/toon-codec`):** Deterministic parser, serializer, and minifier implementing Token-Oriented Object Notation invariants.
- **Domain & Balance Ledger (`crates/domain`):** Typed `TaskContract`, exact micro-currency accounting (1,000 charges of $0.001 sum to $1.000), and R0 (read-only) through R3 (external irreversible) risk tiers.
- **Fair Admission & Worker Pool (`apps/worker`):** Round-robin fair queue admission, hot-tenant throttling (40% ceiling under contention), 6-worker pool lease management (432 concurrent slots), and AES-256-GCM encrypted backup envelopes.
- **State Migration & Shadow Reconciler (`crates/migration`):** Deterministic imports, signed difference ledgers, and zero-loss cutover roll-forward and reversal drills ($W_{post}$ 100% retained).
- **Release Certification & Cutover Guard (`crates/release`):** Exact-SHA verification, provenance digest matching, clean-machine verification, and separate operator approvals for publication and production release.
- **Retirement & Maintenance (`crates/maintenance`):** 14-day canary observation evaluation, vendor-independent export/restore, and maintenance risk register.

### 2. 104-Role Virtual Enterprise Matrix
AGYOS models a full-scale corporate organization partitioned into 12 functional departments and governed by 5 operational pods:
- **`pod-build`**: Engineering, Architecture, Systems Design, DevOps, QA, and Infrastructure.
- **`pod-customer`**: Customer Success, Support Operations, Client Onboarding, and Account Management.
- **`pod-growth`**: Marketing Strategy, Conversion Rate Optimization, Paid Acquisition, Content Creation, and Sales Pipeline.
- **`pod-gna`**: Finance, Treasury, Legal Compliance, Risk Management, Corporate Governance, and Executive Operations.
- **`pod-people`**: Talent Acquisition, Human Resources, Operational Compliance, and Learning & Development.

### 3. 7-Step Autonomous Cycle Standard
AGYOS executes complex engineering workflows autonomously without requiring manual slash commands:
1. **Think:** Ingests natural prompt, compiles intent, evaluates Howard 1966 EVPI, aligns role and pod, and selects specialist skill runbooks.
2. **Plan:** Generates architectural blueprints, acceptance criteria, concrete task breakdowns, and structured milestone checkpoints.
3. **Build:** Executes Maker TDD (RED -> GREEN -> REFACTOR) complying with 6 FAANG production invariants.
4. **Review:** Independent Checker audit for code quality, secret leakage, OWASP Top 10 vulnerabilities, and git hygiene.
5. **Test:** Monotonic remote static and integration verification strictly via GitHub Actions.
6. **Ship:** Delivery strictly to single `main` branch under verified author identity.
7. **Reflect:** Prepend structured handoffs to `AI_HANDOFF.toon`, update state checkpoints, and record durable memory.

### 4. Six FAANG-Grade Production Invariants
- **Strict Boundary Input Validation:** Schema-first validation at all system boundaries before processing.
- **Zero Silent Exception Swallowing:** Explicit, typed error handling; zero bare `except:` or `catch (e) {}` blocks.
- **Safe & Idempotent Operations:** Parameterized queries, idempotent deduplication keys, and transactional outboxes.
- **Immutability & Size Ceilings:** Functions < 50 lines, files < 800 lines, maximum 4 nesting levels, immutable data transformations.
- **Zero Plaintext Secrets:** Zero hardcoded tokens; environment-variable injection with strict startup redaction.
- **Monotonic Machine Evidence:** Zero speculative completion claims; verification strictly backed by passing remote CI runs.

---

## 20-Step Qualified Rebuild Plan (Tracker.md)

AGYOS has achieved certified completion across all 20 steps of the architectural rebuild specification:

| Step | Milestone | Delivered Components | Verification Status |
|:---|:---|:---|:---|
| **01** | Audit baseline & fix references | Pinned dependencies, pruned dead forwarders, canonical workspace tree | PASS (commit `75249539`) |
| **02** | Lock schema & profile | Canonical TOON schema rules, envelope headers, invariant attributes | PASS (commit `75249539`) |
| **03** | Define first slice | Onboarding proposal fixture with work cap reduction (20h -> 12h) | PASS (commit `75249539`) |
| **04** | Bootstrap remote builder | Rust `bootstrap.rs`, locked toolchain, remote Actions trigger | PASS (commit `e3573e04`) |
| **05** | Qualify TOON codec | `crates/toon-codec` (parser, encoder, round-trip tests, size ceilings) | PASS (CI run `44716773379`) |
| **06** | Build domain & policy | `crates/domain` (TaskContracts, R0-R3 risk tiers, exact balance ledger) | PASS (CI run `44717789498`) |
| **07** | Transactional recovery | `crates/store` (event log, outbox, dedup table, fence tokens, snapshots) | PASS (CI run `44718501229`) |
| **08** | AGY CLI integration | `crates/broker` (isolated AGY workspace projection, broker confinement) | PASS (CI run `44719232352`) |
| **09** | First internal slice | Client proposal drafting, checker review, crash recovery survival | PASS (CI run `44719888802`) |
| **10** | Reconcile catalogs | `crates/catalog` (reconciled 2,549 source paths, 4,620 aliases, 104 roles) | PASS (CI run `44720797333`) |
| **11** | Place & qualify skills | 153 skills across 27 homes with 12 department end-to-end fixtures | PASS (CI run `44723974439`) |
| **12** | Routing & councils | `crates/runtime` (progressive retrieval, EVPI, context budgets, 4-arm P27 benchmark) | PASS (CI run `44726623050`) |
| **13** | Business effects | `crates/adapters` (8 domain adapters, SSRF defense, W3C PROV receipts) | PASS (CI run `44727853460`) |
| **14** | Operator control | `crates/runtime/src/pilot.rs` (12-operator pilot in English & Gujarati) | PASS (CI run `44728657584`) |
| **15** | Local production | `crates/telemetry` (redacted metrics, 2 vCPU / 2 GiB load/fault/restore profiles) | PASS (CI run `44730651359`) |
| **16** | Heavy production | `apps/worker` (fair queue admission, 6 worker leases, spending limits, AES-256-GCM) | PASS (CI run `44732412969`) |
| **17** | State migration | `crates/migration` (deterministic import, shadow reader, zero-loss reversal drill) | PASS (CI run `44733737010`) |
| **18** | Certified release | `crates/release` (release gate engine, live cutover guard, clean machine drill) | PASS (CI run `44734422860`) |
| **19** | Retire & maintain | `crates/maintenance` (14-day canary observation, vendor-free export/restore, risk ledger) | PASS (CI run `44735206249`) |
| **20** | Refresh 2027 evidence | `crates/maintenance/src/research_decision.rs` & `docs/research/RDR-2027-EVIDENCE-REFRESH.toon` | PASS (CI run `44736184705`) |

---

## Repository Structure

```text
.
├── bootstrap.rs                 # Rust workspace orchestrator & compilation driver
├── build/                       # Build profiles & locked workspace declarations (workspace.toon)
├── crates/                      # Core Rust workspace crates
│   ├── toon-codec/              # Pure TOON format encoder, decoder & conformance tests
│   ├── domain/                  # Contracts, R0-R3 risk boundaries, balance ledger
│   ├── store/                   # Event log, transactional outbox, deduplication, fence tokens
│   ├── broker/                  # AGY CLI boundary projection & tool broker confinement
│   ├── catalog/                 # 104-role registry, 153 canonical skills, phrase router
│   ├── runtime/                 # Progressive retrieval, Howard EVPI, context budget, councils, pilot
│   ├── adapters/                # 8 domain adapters (CRM, billing, legal, hiring, Git, models, web)
│   ├── telemetry/               # Redacted metrics, local production profiles, backup/restore
│   ├── migration/               # Shadow reader, signed difference ledger, reversal drill
│   ├── release/                 # Release gates, live cutover guard, discovery-to-handover engine
│   └── maintenance/             # Canary observation, vendor-free export/restore, 2027 RDR engine
├── apps/                        # Production applications
│   └── worker/                  # Heavy hosted worker pool, fair queue admission, AES-256-GCM
├── .agents/                     # Autonomous agent definitions, workflows, rules, and skills
│   ├── agents/                  # 104 role agent profiles in TOON/XML format
│   ├── rules/                   # Operational and engineering policies
│   ├── skills/                  # 2,289 skill runbooks and reference materials
│   ├── state/                   # Active operational state (CURRENT.toon, state.json, checkpoints/)
│   └── workflows/               # Autonomous execution cycle workflows
├── bin/                         # Developer CLI binaries (bin/agyos, bin/state.sh)
├── docs/                        # Specifications, architecture models, research decision records
└── knowledge/                   # Canonical skill runbooks (knowledge/skills/), aliases, unavailable catalog
```

---

## Quickstart & CLI Usage

### 1. Skill Discovery & Selection
```bash
# Rank skills and print optimal runbook
bin/agyos decide "debug concurrent async Rust actor" --json --runbook

# Search catalog across 2,289 capabilities
bin/agyos find "database migration reversal"

# Render specific physical runbook
bin/agyos skill software-architecture
```

### 2. Autonomous Cycle Dispatch
```bash
# Execute end-to-end 7-step autonomous cycle
bin/agyos cycle --task "Implement tenant isolation adapter with W3C PROV receipt"

# Read active operational state and current gate
bin/agyos state
```

### 3. TOON Codec Fast-Path
```bash
# Encode or minify TOON documents
bin/agyos toon encode --input sample.json --output sample.toon
bin/agyos toon minify --input sample.toon
```

---

## CI/CD & Engineering Invariants

- **Single Main Branch Invariant:** All development lands strictly on `main`. No feature branches or divergent worktrees are permitted.
- **Identity Enforcement:** All commits are authored and committed under the verified GitHub identity:
  `Krish Ujeniya <100012208+krishujeniya@users.noreply.github.com>`.
- **Zero Local Execution Invariant:** Unit tests, integration suites, compilers, and linters execute strictly in GitHub Actions runners via `.github/workflows/remote-builder.yml`. Local operations are strictly read-only static inspection and `git diff --check`.
- **Skills in TOON Invariant:** All skill definitions and runbooks are strictly authored and maintained in Token-Oriented Object Notation (`.toon`). Repository-level documentation and research are maintained in clean GitHub Markdown.
- **Python Management:** All Python scripts, environments, and tools execute strictly via `uv` (`uv run`, `uv pip`, `uv tool`). Raw invocation of `python` or `pip` is forbidden.

---

## License & Provenance

This project is licensed under the Apache License 2.0. See [`LICENSE`](LICENSE) for terms. All third-party tools, vendor specifications, and reference materials retain their respective licenses and attribution notices.

Security disclosures and vulnerability reporting guidelines are detailed in [`SECURITY.toon`](SECURITY.toon).
