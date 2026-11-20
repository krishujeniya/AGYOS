# AGYOS Project Context & Master System Architecture

> **Repository**: [krishujeniya/AGYOS](https://github.com/krishujeniya)
> **Author & System Owner**: Krish Ujeniya (`100012208+krishujeniya@users.noreply.github.com`)
> **Target Runtime**: Antigravity CLI (`agy`) v1.4.12+
> **Architecture**: Autonomous Solopreneur Enterprise Operating System
> **Document Status**: Canonical Project Ground Truth (`context.md`)

---

## 1. Executive Summary & Core Mission

AGYOS is an autonomous Cognitive Operating System built for the Antigravity CLI (`agy`). Its primary objective is to turn a single solo operator (freelancer, independent builder, or technical founder) into a self-directed, 104-role virtual software enterprise capable of designing, building, securing, and shipping production-grade applications without manual step-by-step guidance.

### The Problem It Solves
Traditional AI developer tools operate as ephemeral, reactive chatbots that require continuous human prompting, lose context across long tasks, consume excessive tokens through repetitive Markdown/JSON payloads, and lack enterprise discipline.

AGYOS eliminates these bottlenecks by introducing:
1. **Autonomous Operation**: Execution moves through a 7-step autonomous cycle (`Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect`) without requiring manual slash commands.
2. **Virtual Corporate Matrix**: A 104-role organizational structure across 12 departments and 5 operational pods, translating high-level prompts into end-to-end SDLC execution.
3. **Token-Oriented Object Notation (TOON)**: A tabular compression format reducing context consumption by 40% to 60% compared to JSON/Markdown on lightweight models like Google Gemini Flash.
4. **FAANG/MANGO Production Discipline**: Strict boundaries, monotonic test ratchets, schema-first input validation, zero-secret enforcement, and immutable state updates.
5. **Zero Local Overhead**: Complete offloading of builds, tests, linters, and heavy operations to GitHub Actions CI/CD, keeping local low-spec workstations clean and fast.

---

## 2. System Architecture & The 6-Layer Engine

AGYOS models the cognitive lifecycle as a layered operating system, defined in [docs/ARCHITECTURE.md](file:///home/ai/Documents/projects/Freelance/AGYOS/docs/ARCHITECTURE.md):

```
┌────────────────────────────────────────────────────────┐
│ User Objective / Autonomous Intent                     │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Layer 0: Kernel & Safety Interceptor                   │
│ - scripts/hooks/authorizer.py, agy_os_hook.py          │
│ - Principle of least privilege, fail-open resilience   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Layer 1: 3-Tier Hierarchical Virtual Memory            │
│ - Tier 0 (Core Working): .agents/state/memory.json     │
│ - Tier 1 (Recall Cache): Checkpoints & CURRENT.md      │
│ - Tier 2 (Archival Deep): 2,289 Skills & Runbooks      │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Layer 2: FastMCP Syscall & Driver Bus                  │
│ - mcp/state-server.cjs (FastMCP JSON-RPC stdio)        │
│ - Discrete tool permission boundary                    │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Layer 3: 5-Gate Governance & SRE State Machine         │
│ - IDLE -> UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT   │
│ - Verification monotonic test ratchet                  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Layer 4: Multi-Agent Corporate Role Hierarchy          │
│ - 104 roles, 12 departments, 5 operational pods        │
│ - Client Working Backwards SDLC Pipeline               │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Layer 5: Extensibility & Capability Catalog            │
│ - 2,289 Skills (.agents/skills/)                       │
│ - 185 Agents, 147 Rules, 99 Workflows                  │
│ - Tri-format codec (TOON + XML + JSON)                 │
└────────────────────────────────────────────────────────┘
```

---

## 3. The 104-Role Virtual Corporate Matrix

AGYOS structures operational capability into 104 specialized roles registered in `agyos_decision/roles.py`, organized across 12 departments and 5 governing pods:

### 12 Corporate Departments
1. **Executive (8 roles, L8)**: CEO, CTO, COO, CPO, CMO, CSO, CFO, VP Engineering.
2. **Product (8 roles, L4-L7)**: Product Director, Senior PM, PM, Scrum/Agile Coach, UX Researcher, Growth PM, Product Analyst, Technical PM.
3. **Engineering (16 roles, L5-L7)**: Staff SWE, Senior SWE, SWE, Frontend Engineer, Backend Engineer, Mobile Engineer, DevOps/Platform Engineer, Site Reliability Engineer, Security Engineer, QA/Test Engineer, Web3/Blockchain Engineer, Desktop App Engineer, Network Infra Engineer, DB Reliability Engineer, Incident Commander, Agentic Workflow Architect.
4. **Data & AI (10 roles, L4-L7)**: Data Scientist, ML Engineer, Data Engineer, AI Product Engineer, Data Analyst, Research Scientist, Privacy Engineer, Computer Vision Engineer, Speech & Audio AI Engineer, MLOps Engineer.
5. **Design (8 roles, L4-L7)**: Design Director, UX/UI Designer, Product Designer, Brand Designer, Motion Designer, 3D Visual Designer, Design System Engineer, UX Copywriter.
6. **Marketing (10 roles, L4-L5)**: Content Strategist, SEO Specialist, Performance Marketer, Social Media Manager, Brand Copywriter, Conversion Rate Optimizer, Email & Lifecycle Marketer, PR & Comms Manager, Partnership & BD Manager, Community Manager.
7. **Sales & BD (8 roles, L4-L8)**: VP Sales, Account Executive, Sales Development Rep, Solutions Engineer, Customer Success Manager, Revenue Operations Analyst, Enterprise AE, Freelancer BD.
8. **Customer Success (6 roles, L4-L6)**: Support Engineer, Onboarding Specialist, Implementation Consultant, Technical Account Manager, Churn Analyst, Technical Writer.
9. **Finance (8 roles, L4-L7)**: Corporate Controller, FP&A Analyst, Tax Specialist, Billing & Payments Engineer, Treasury Specialist, Accounts Manager, Startup CFO Advisor, Cost Optimization Analyst.
10. **Legal & Compliance (6 roles, L5-L8)**: General Counsel, IP & Patent Attorney, Contract Manager, Compliance Officer, Data Protection Officer, Risk Manager.
11. **People & Ops (10 roles, L4-L8)**: VP People, Talent Recruiter, HR Business Partner, HR Ops Specialist, L&D Specialist, Procurement & Vendor Manager, Facilities Manager, Executive Assistant, Solopreneur Operator, Chief of Staff.
12. **IT & Platform (6 roles, L4-L7)**: IT Systems Administrator, Cloud Architect, Platform Engineer, Cybersecurity Analyst, Observability Engineer, FinOps Engineer.

### 5 Operational Pods
- **Pod Build**: Core system engineering, compilers, runtime CLI, and system architecture.
- **Pod Customer**: Support engineering, onboarding workflows, technical documentation, and customer success.
- **Pod People**: Talent acquisition, HR operations, compliance policies, and organizational structure.
- **Pod Growth**: Performance marketing, content strategy, brand acquisition, and revenue operations.
- **Pod GNA**: General & Administrative, legal contracts, corporate finance, accounting, and risk management.

---

## 4. The 7-Step Autonomous Cycle Engine

Implemented in `agyos_decision/cycle.py` and detailed in [.agents/rules/agyos-autonomous-cycle.md](file:///home/ai/Documents/projects/Freelance/AGYOS/.agents/rules/agyos-autonomous-cycle.md), the system automatically advances through 7 stages:

```
Think ──> Plan ──> Build ──> Review ──> Test ──> Ship ──> Reflect
```

1. **Think (Intent Synthesis)**: Compiles the user's prompt into a typed `TaskContract`, computes Expected Value of Perfect Information (EVPI), matches the optimal role from the 104-role matrix, and identifies required skills via `decide_skill`.
2. **Plan (Architectural Blueprint)**: Breaks work into atomic tasks with explicit acceptance criteria (Given/When/Then), establishes milestone identifiers, and writes checkpoints to `.agents/state/checkpoints/<milestone_id>.md`.
3. **Build (TDD Implementation)**: Applies Test-Driven Development (RED -> GREEN -> IMPROVE) with boundary input validation, explicit error handling, immutability, and function sizes under 50 lines.
4. **Review (Checker Audit)**: Executes independent AST verification, regex security scans for credentials or shell escapes, and `git diff --check` validation.
5. **Test (Static Verification Proof)**: Executes deterministic static checks (`python3 -m compileall`, `bash -n bin/*`) and delegates heavy verification to GitHub Actions CI/CD workflows.
6. **Ship (Single Main Delivery)**: Stages verified changes, validates author identity (`Krish Ujeniya`), creates conventional commits, and merges cleanly into `origin main`.
7. **Reflect (Knowledge Preservation)**: Updates `AI_HANDOFF.toon` / `AI_HANDOFF.md`, marks milestone checkpoints complete, resets state gates to `IDLE`, and updates long-term memory.

### 3-Strike Recovery Policy
- **Strike 1**: Fix syntax, lint, or logic failure directly. Re-verify.
- **Strike 2**: Re-read runbook and code. Apply alternative pattern.
- **Strike 3**: Stop mutation immediately, document root cause in milestone checkpoint, and report blocker to operator.

---

## 5. The Tri-Format Semantic Engine & TOON Standard

AGYOS relies on a hybrid semantic architecture tailored for high-speed LLM context windows:

| Format | Purpose | Advantages |
|---|---|---|
| **TOON** (`.toon`) | Tabular context injection, skill catalogs, handoffs, and manifests | 40%–60% token reduction over JSON/XML; eliminates repetitive keys and syntax tokens |
| **XML** | System prompts, task execution envelopes, guardrails, and role prompts | High LLM attention bias, clear CDATA boundaries, and zero prompt-injection leakage |
| **JSON** | FastMCP JSON-RPC 2.0 communication, tool schemas, and disk state ledgers | Universal programmatic compatibility, strict schema validation, and API standard |

### Native Rust Engine (`crates/toon-codec/`)
A dedicated high-performance Rust crate located at [crates/toon-codec](file:///home/ai/Documents/projects/Freelance/AGYOS/crates/toon-codec) provides sub-millisecond serialization and parsing for TOON documents, establishing the foundation for compiled runtime execution.

---

## 6. Strict Non-Negotiable Operational Invariants

AGYOS enforces strict project policies that apply to every agent and task:

1. **Single Main Branch Exclusive**:
   - The repository operates exclusively on the `main` branch.
   - Creating feature branches, task branches, or divergent worktrees is strictly prohibited.
   - Any secondary branches are merged into `main` and deleted immediately.
2. **Identity Lock (Krish Ujeniya)**:
   - All commits must strictly be authored and committed under:
     `git config user.name "Krish Ujeniya"`
     `git config user.email "100012208+krishujeniya@users.noreply.github.com"`
   - Commits link directly to verified GitHub attribution.
3. **Zero Local Builds / Heavy Execution**:
   - Compilers, unit test suites, integration tests, type checkers, linters, dependency installers, and media rendering must never execute on the local workstation.
   - All heavy execution runs strictly in GitHub Actions CI/CD workflows (`.github/workflows/ci.yml`).
   - Allowed local operations are strictly read-only static inspection (grep, AST read, file inspection) and `git diff --check`.
4. **Mandatory UV Exclusively for Python**:
   - Raw `python`, `pip`, `poetry`, or `virtualenv` invocations are strictly forbidden.
   - All Python commands, scripts, package management, and virtual environments must run via `uv` (`uv run`, `uv pip`, `uv venv`, `uv add`).
5. **Headless Browser Exclusively (Obscura)**:
   - All browser automation, testing, and scraping run headlessly via Obscura (`bin/obscura`). Graphical Chrome/Chromium windows are prohibited.
6. **Direct Zero-API Security Scanning (Strix)**:
   - The embedded security suite (`scripts/strix_runner.py` and `scripts/agy_security_scanner.py`) executes directly via AGY CLI without external paid LLM API keys.
7. **Pure Human Language & Zero AI Slop**:
   - Responses, documentation, and commits use direct, technical, grounded human prose.
   - Strictly banned AI buzzwords: *delve*, *testament*, *tapestry*, *landscape*, *pivotal*, *in conclusion*, *crucial*, *embark*, *game-changer*, *foster*, *leverage*, *robust*, *streamline*, *seamless*, *moreover*, *unleash*, *elevate*, *beacon*.
   - Strictly banned decorative emoji markers (e.g., rocket, shield, spark icons) in system output and commits.

---

## 7. Catalog & Artifact Inventory

The repository contains a fully indexed inventory verified against the live filesystem:

- **Skills**: 2,289 runbooks in `.agents/skills/` mapped by role in `.agents/skills-by-role/`.
- **Agents**: 185 role and specialist agent specifications in `.agents/agents/`.
- **Rules**: 147 operational and governance rules in `.agents/rules/`.
- **Workflows**: 99 multi-agent execution workflows in `.agents/workflows/`.
- **Command Line Entry**: [bin/agyos](file:///home/ai/Documents/projects/Freelance/AGYOS/bin/agyos), providing `decide`, `intent`, `cycle`, `strix`, `skill`, `gate`, and `verify`.
- **Core Documentation**:
  - [README.md](file:///home/ai/Documents/projects/Freelance/AGYOS/README.md) & [README.toon](file:///home/ai/Documents/projects/Freelance/AGYOS/README.toon)
  - [AGENTS.md](file:///home/ai/Documents/projects/Freelance/AGYOS/AGENTS.md) & [AGENTS.toon](file:///home/ai/Documents/projects/Freelance/AGYOS/AGENTS.toon)
  - [AI_HANDOFF.md](file:///home/ai/Documents/projects/Freelance/AGYOS/AI_HANDOFF.md) & [AI_HANDOFF.toon](file:///home/ai/Documents/projects/Freelance/AGYOS/AI_HANDOFF.toon)
  - [TRACKER.md](file:///home/ai/Documents/projects/Freelance/AGYOS/TRACKER.md) & [TRACKER.toon](file:///home/ai/Documents/projects/Freelance/AGYOS/TRACKER.toon)
  - [docs/ARCHITECTURE.md](file:///home/ai/Documents/projects/Freelance/AGYOS/docs/ARCHITECTURE.md)
  - [docs/OPERATIONS_RUNBOOK.md](file:///home/ai/Documents/projects/Freelance/AGYOS/docs/OPERATIONS_RUNBOOK.md)

---

## 8. Historical Evolution Across Sessions

Across 18 recorded operational sessions, the system has undergone a deliberate evolution:

1. **Phase 1: Foundation & Skill Catalog Harvesting**: Consolidated over 2,200 developer, operations, and domain runbooks from diverse ecosystems into structured skill packs under `.agents/skills/`.
2. **Phase 2: Corporate Matrix & Solopreneur Model**: Shifted from generic prompt helpers into a 104-role FAANG/MANGO enterprise matrix spanning 12 departments and 5 operational pods, with Amazon Working Backwards SDLC pipelines.
3. **Phase 3: TOON Token Compression Cutover**: Converted thousands of loose Markdown files into native TOON specifications, pruning key redundancy and achieving 40-60% token savings for fast Gemini Flash execution.
4. **Phase 4: Junk Pruning & Repository Hygiene**: Removed redundant scripts, unused Docker/IDE artifacts, legacy build caches, and unneeded dependencies, establishing strict single-source-of-truth hygiene.
5. **Phase 5: Native Rust Engine**: Introduced `crates/toon-codec/` for native compilation, memory safety, and high-performance serialization.
6. **Phase 6: Direct Zero-API Security Engine**: Integrated Strix penetration testing into `bin/agyos strix` with direct CLI AST/OWASP analysis, eliminating external API dependencies.
7. **Phase 7: 7-Step Autonomous Operational Engine**: Implemented `agyos_decision/cycle.py` and `scripts/agyos_cycle.py`, establishing autonomous `Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect` execution without manual slash commands.

---

## 9. Current Operational State & Strategic Roadmap

### Current Operational State
- **Branch**: `main` (clean, synchronized with `origin/main`).
- **Identity**: Confirmed as `Krish Ujeniya`.
- **Runtime**: Tested and functional under Antigravity CLI (`agy`) and `uv run`.
- **Verification Engine**: GitHub Actions CI (`.github/workflows/ci.yml`) passing cleanly.
- **Local Workstation**: Free of build artifacts, temporary caches, or local dependency bloat.

### Immediate Strategic Focus
1. **End-to-End Client Working Backwards Validation**: Run autonomous projects through the full discovery-to-delivery lifecycle using the 7-step autonomous engine.
2. **Rust Engine Integration**: Expand `crates/toon-codec` into a complete runtime daemon capable of executing state machine transitions with zero Python interpreter overhead.
3. **Autonomous Project Portfolio Delivery**: Use AGYOS as the governing OS to build, test, and ship client products, Cloudflare/GitHub Pages portfolios, and micro-SaaS applications autonomously under Krish Ujeniya's single-operator leadership.
