<p align="center">
  <img src="assets/logo.svg" alt="AGYOS" width="180" />
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

The system combines a Python cognitive decision kernel (`gemini/antigravity-cli/builtin/agyos_decision/`), a static documentation and catalog frontend (`frontend/`), and a Node.js MCP state server (`gemini/antigravity-cli/mcp/`) with an enterprise organization of 104 operational roles across 12 departments, a TOON-native 2,289-skill catalog, a Token-Oriented Object Notation (TOON) codec, and an automated 7-step cycle (`Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect`).

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

    subgraph StorageEngine["3. Transactional State & Memory (gemini/antigravity-cli/mcp/ & gemini/antigravity-cli/builtin/agyos_decision/)"]
        direction TB
        SQLite[("ACID SQLite State<br/><code>Monotonic Revisions • CAS</code>")]
        Outbox["R3 Outbox & Snapshots<br/><code>state_ledger.py • Pre-Write Backup</code>"]
        Vault["Encrypted Private Vault<br/><code>AES-256-GCM • X25519 Envelopes</code>"]
        SQLite --- Outbox
        SQLite --- Vault
    end

    subgraph RuntimeLayer["4. Static Frontend, Docs & TOON Codec"]
        Frontend["Static Frontend & SEO (frontend/)<br/><code>index.html • catalog.html • sitemap.xml • llms.txt</code>"]
        SiteGen["Static Builder (gemini/antigravity-cli/builtin/scripts/build_docs_site.py)<br/><code>Allowlisted Docs • Search Index</code>"]
        Codec["TOON Codec Engine (gemini/antigravity-cli/builtin/agyos_decision/toon_codec.py)<br/><code>Typed Parsing • Exact Encoding</code>"]
    end

    subgraph ReleaseGate["5. Gated Verification & Delivery"]
        CI["GitHub Actions CI/CD<br/><code>ci.yml • Static & Integration Gates</code>"]
        MainBranch[("Protected Single main Branch<br/><code>Author: Krish Ujeniya</code>")]
    end

    %% Connections
    User -->|"Natural Language Prompt"| Intent
    Intent -->|"Assigns Lead Role"| Pods
    Pods -->|"Selects Specialist Skill"| Catalog
    Catalog -->|"Dispatches TaskContract"| AutonomousCycle

    S3 <-->|"Atomic Revisions & Snapshot"| StorageEngine
    S4 <-->|"Audits Evidence Receipts"| RuntimeLayer
    SiteGen <-->|"Reads Catalog & Docs"| Catalog

    S5 -->|"Triggers Verification"| CI
    CI -->|"Verifies Artifacts & Digests"| S6
    S6 -->|"Fast-Forward Merge"| MainBranch

    %% Class Styles
    classDef operator fill:#2563eb,stroke:#1d4ed8,color:#ffffff,stroke-width:2px;
```

---

## Core Components

The repository is organized into modular Python, Node.js, and static frontend subsystems:

| Component | Path | Responsibility |
|:---|:---|:---|
| **Decision Kernel** | `gemini/antigravity-cli/builtin/agyos_decision/` | Intent compilation, Howard 1966 EVPI, 104-role matrix, TOON codec/compiler, and 7-step cycle |
| **CLI Dispatcher** | `gemini/antigravity-cli/bin/agyos` | Unified CLI entry point across routing, TOON skills, verification, and lifecycle |
| **MCP Daemon** | `gemini/antigravity-cli/mcp/state-server.cjs` | Zero-dependency stdio JSON-RPC 2.0 server exposing state, memory, and TOON skill search |
| **Frontend Portal** | `frontend/` | Static documentation templates, skill catalog UI, and SEO files (`sitemap.xml`, `robots.txt`, `llms.txt`) |
| **Scripts & CI** | `gemini/antigravity-cli/builtin/scripts/` | Site/catalog builders, TOON validators, security scanners, benchmarks, and state-store tests |
| **Deployment** | `deploy/` | Docker and Cloudflare Pages deployment manifests |

---

## The 7-Step Autonomous Cycle

AGYOS executes engineering workflows autonomously through a 7-step cycle without requiring manual slash commands:

1. **Think:** Compiles natural language intent into a typed `TaskContract`, computes Howard 1966 EVPI for clarification, assigns the lead role, and identifies specialist skill runbooks.
2. **Plan:** Produces architectural blueprints, acceptance criteria, concrete task breakdowns, and structured milestone checkpoints.
3. **Build:** Executes Maker TDD (RED -> GREEN -> REFACTOR) complying with production invariants.
4. **Review:** Independent Checker audit for code quality, secret leakage, OWASP Top 10 vulnerabilities, and git hygiene.
5. **Test:** Monotonic remote static and integration verification strictly via GitHub Actions.
6. **Ship:** Delivery strictly to the single `main` branch under verified author identity after passing all gates.
7. **Reflect:** Logs structured handoffs, updates `gemini/antigravity-cli/builtin/state/CURRENT.md` and milestone checkpoints, and records durable memory.

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
- **GitHub Actions Verification Mandatory:** Unit tests, integration suites, compilers, and linters execute strictly in GitHub Actions runners (`ci.yml`). Local operations are limited to read-only static inspection and `git diff --check`.
- **Mandatory `uv` for Python:** All Python package management, virtual environments, and script executions strictly use `uv` (`uv run`, `uv pip`, `uv tool`). Raw invocation of `python` or `pip` is forbidden.
- **Bounded Working Sets:** Bounded telemetry ring buffers and pre-write snapshot caps (`16 MiB` max file snapshot size).
- **Zero Plaintext Secrets:** Zero hardcoded tokens or secrets; environment variables use startup redaction.

---

## One-Line Install (`~/.gemini`)

Replace or sync your local `~/.gemini` directory with `AGYOS/gemini/` (automatically creates a timestamped backup of `~/.gemini` first):

```bash
curl -fsSL https://raw.githubusercontent.com/krishujeniya/AGYOS/main/gemini/antigravity-cli/builtin/scripts/install.sh | bash
```

Or from a local clone:

```bash
git clone https://github.com/krishujeniya/AGYOS.git && cd AGYOS && make install
```

---

## Quickstart & CLI Commands

### 1. Skill Discovery & Selection
```bash
# Select optimal skill and inspect instructions
gemini/antigravity-cli/bin/agyos decide "debug concurrent async Rust actor" --json --runbook

# Search catalog across 2,289 capabilities
gemini/antigravity-cli/bin/agyos find "database migration reversal"

# Display specific runbook
gemini/antigravity-cli/bin/agyos skill database-migrations
```

### 2. Autonomous Cycle Dispatch
```bash
# Execute end-to-end 7-step autonomous cycle
gemini/antigravity-cli/bin/agyos cycle "Implement tenant isolation adapter with W3C PROV receipt"

# Read active operational state and current gate
gemini/antigravity-cli/bin/agyos state
```

### 3. Role Matrix Inspection
```bash
# List enterprise roles
gemini/antigravity-cli/bin/agyos roles

# Inspect specific role profile
gemini/antigravity-cli/bin/agyos role role-solopreneur-operator
```

### 4. TOON Codec & Compilation
```bash
# Compile role definition into TOON
gemini/antigravity-cli/bin/agyos toon-agent role-swe --compact

# Compile skill runbook into compact TOON card
gemini/antigravity-cli/bin/agyos toon-skill software-architecture --compact

# Encode or minify TOON documents
gemini/antigravity-cli/bin/agyos toon encode --input sample.json --output sample.toon
gemini/antigravity-cli/bin/agyos toon minify --input sample.toon
```

---

## Documentation

- [Developer Setup](docs/setup.md) — Prerequisites (`uv`, Node 22+), local loadless checks, and `Makefile` targets
- [System Architecture](docs/ARCHITECTURE.md) — 6-layer cognitive architecture, 5 pods, 104 roles, and EVPI/Saga controls
- [Skill Routing](docs/SKILL_ROUTING.md) — Discovery contract across the 2,289 TOON skills
- [Rules & Standards](docs/RULES.md) — Modular rule library (`gemini/antigravity-cli/builtin/rules/`) and precedence
- [Native Workflows](docs/NATIVE_WORKFLOWS.md) — Background multi-agent workflow scripts (`gemini/antigravity-cli/builtin/workflows/`)
- [Operations Runbook](docs/OPERATIONS_RUNBOOK.md) — SLOs, vault setup, compaction, and disaster recovery
- [Host Compatibility](docs/HOST_COMPATIBILITY.md) — Qualified interfaces and host verification limits
- [Deployment Guide](docs/deployment.md) — Cloudflare Pages (`agyos.pages.dev`) and Docker deployment

---

## Repository Layout

```text
AGYOS/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                     # Lint, typecheck, TOON/catalog validation & tests
│   │   ├── deploy.yml                 # Auto-deploy static portal on push to main (Cloudflare Pages)
│   │   ├── codeql.yml                 # Automated CodeQL security scanning
│   │   ├── security-toolkits.yml      # Strix security toolkit static checks
│   │   ├── strix-security.yml         # Strix security verification & scan
│   │   ├── video-toolkits.yml         # Video pipeline static checks & smoke render
│   │   └── docker-publish.yml         # Verified container publication to GHCR
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml             # Structured bug report form
│   │   ├── feature_request.yml        # Structured feature request form
│   │   └── config.yml                 # Disables blank issues / links to Discussions
│   ├── PULL_REQUEST_TEMPLATE.md       # Checklist for every PR
│   ├── PULL_REQUEST_TEMPLATE.toon     # TOON source for PR template
│   ├── CITATION.cff                   # Repository citation metadata
│   ├── CODEOWNERS                     # Auto-assigns reviewers per folder
│   ├── CODE_OF_CONDUCT.md             # Community standards
│   ├── CONTRIBUTING.md                # How to set up & contribute
│   ├── FUNDING.yml                    # Enables the GitHub Sponsor button
│   ├── SECURITY.md                    # Vulnerability reporting & E2EE/vault boundaries
│   ├── SUPPORT.md                     # Where to ask for help
│   ├── copilot-instructions.md        # Custom rules for coding assistants
│   ├── dependabot.yml                 # Auto-updates GitHub Actions
│   └── settings.yml                   # Declarative repository settings & main branch protection
├── assets/                            # Brand logos and raster/SVG icons
├── deploy/                            # docker/ (Dockerfile, compose)
├── docs/                              # Architecture, setup, deployment, runbooks & catalog JSON
├── frontend/                          # Static documentation portal, catalog UI, and SEO files
├── gemini/                            # Mirrors ~/.gemini/ (config/ + antigravity-cli/builtin/ with 2,289 role-based skills, 109 agents, 13 plugins, MCP, state)
├── .editorconfig                      # Consistent indentation/line-endings across IDEs
├── .gitignore                         # Combined Node, Python, Cloudflare, OS & agent hygiene rules
├── CHANGELOG.md                       # Version history & release notes
├── LICENSE                            # Apache 2.0 license
├── Makefile                           # Unified commands (make dev, make test, make typecheck, make lint, make build)
├── README.md                          # Project overview, badges, architecture, quickstart
└── wrangler.jsonc                     # Cloudflare Pages & edge bindings configuration
```

---

## License & Security

This project is licensed under the Apache License 2.0. See [`LICENSE`](LICENSE) for details.

Security policies and vulnerability reporting procedures are documented in [`.github/SECURITY.md`](.github/SECURITY.md).
