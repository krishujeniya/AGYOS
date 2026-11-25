# AGYOS Cognitive Architecture & System Principles

> **Governing System**: AGYOS Cognitive OS
> **Author**: Krish Ujeniya
> **Runtime Target**: AGY CLI (`agy`) v1.5.9+
> **Architecture Paradigm**: 6-Layer Hierarchical AI Operating System (Synthesizing AIOS, MemGPT/Letta, MetaGPT, and AGYOS Governance)

---

## 1. System Architecture Overview

AGYOS embeds Large Language Model agents into a structured, operating-system-level cognitive harness. Rather than running isolated, unmanaged agent prompts, AGYOS manages execution, memory paging, tool routing, and phase transitions through a 6-layer hierarchical architecture.

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

## 2. The 6 Hierarchical Layers

### Layer 0: Kernel & Safety Interceptor
- **Enforcement Point**: `gemini/antigravity-cli/builtin/scripts/hooks/agy_os_hook.py` and `gemini/antigravity-cli/hooks.json`
- **Responsibilities**:
  - Intercepts tool calls in real time (PreToolUse, PostToolUse).
  - Enforces fail-open resilience: unhandled exceptions log a warning and return `{"decision": "allow"}` rather than deadlocking the agent.
  - Guardrails dangerous destructive commands (`rm -rf /`, raw disk writes).
  - Enforces the 24,000-byte constitutional size budget.

### Layer 1: 3-Tier Hierarchical Virtual Memory
Inspired by the virtual memory paging architectures of MemGPT and Letta:
- **Tier 0 (Core Working Memory)**: Active persona, user preferences, runtime identity, and inviolable invariants stored in `gemini/antigravity-cli/builtin/state/memory.json`. Loaded into the active prompt.
- **Tier 1 (Recall Memory / Cache)**: Conversation summaries, milestone checkpoints (`gemini/antigravity-cli/builtin/state/checkpoints/`), and current session status (`gemini/antigravity-cli/builtin/state/CURRENT.md`).
- **Tier 2 (Archival Memory / Deep Storage)**: The 2,289-skill catalog across 103 role-based skill packs (`gemini/antigravity-cli/builtin/skills/role-*/`), indexed in `gemini/antigravity-cli/skills-manifest.json` and `docs/skills-data.json`, paged into context JIT via `agyos_find_skill`.

### Layer 2: FastMCP Syscall & Driver Bus
- **Driver**: `gemini/antigravity-cli/mcp/state-server.cjs` (Zero-dependency stdio JSON-RPC 2.0 daemon, with `gemini/antigravity-cli/mcp/agyos-state-server.cjs` as compatibility wrapper)
- **Exposed Syscalls**:
  - `agyos_state`: Inspect active gate, milestone, iteration, and token metrics.
  - `agyos_current`: Read human-readable session markdown summary.
  - `agyos_graph`: Read context dependency DAG and invariant status.
  - `agyos_checkpoint`: Audit ledger entries for specific milestones.
  - `agyos_find_skill`: Deterministic keyword and phrase search over the generated skill index.
  - `agyos_sys_info`: Comprehensive OS runtime diagnostics, loaded drivers, and subsystem health.
  - `agyos_workspace_state`: Transactional workspace status, latest revision, and operation audit log from SQLite store.
  - `agyos_memory`: Virtual memory read, write, and list operations across tiers.

### Layer 3: AGYOS 5-Gate SOP Engine (`Code = SOP(Team)`)
Implements the deterministic Standard Operating Procedure (SOP) paradigm proven by MetaGPT:
```
[GATE 1: UNDERSTAND] ➔ [GATE 2: ANALYZE] ➔ [GATE 3: PLAN] ➔ [GATE 4: IMPLEMENT] ➔ [GATE 5: VERIFY]
                                 │
                         (Complexity <= 2)
                                 │
                                 └───► [FAST-PATH: IMPLEMENT ➔ VERIFY]
```
- **Dual-Layer State Engine**:
  - **Primary Authoritative Store**: ACID SQLite database managed by `gemini/antigravity-cli/builtin/scripts/agyos-runtime/` (`workspace-state.db`) with schema migrations, monotonically increasing revision numbers, compare-and-swap (CAS) conflict rejection, and idempotent operation replay.
  - **Projections**: Read-only human/tool summaries (`gemini/antigravity-cli/builtin/state/state.json`, `gemini/antigravity-cli/builtin/state/CURRENT.md`) reconstructed from the authoritative SQLite tables.
- **Gate Transitions**: Programmatically locked and validated under `gemini/antigravity-cli/bin/state.sh` and `gemini/antigravity-cli/bin/workspace-state.cjs`.
- **Fast-Path Router**: Complexity $\le 2$ bypasses Gates 1–3, avoiding bureaucracy for minor edits.

### Layer 4: Adaptive Hierarchy & 104-Role Enterprise Matrix
Synthesizes company-wide operations across all 12 corporate departments and 104 specialized roles into 5 merged operational pods with bounded tree depth (L0 Coordinator -> L1 Pod -> L2 Leaf Worker), eliminating O(N^2) horizontal chatter:

#### 1. The 5 Governing Operational Pods
1. **`pod-growth` (`gemini/antigravity-cli/builtin/agents/pod-growth.toon`)**:
   - Covers: Marketing, Lead Generation, Sales & BD, Partnerships.
   - Deliverables: Audience segmentation, lawful prospect lists, proposals, ad campaigns.
   - Boundaries: Zero invented testimonials; approval before publishing or live sends.
2. **`pod-customer` (`gemini/antigravity-cli/builtin/agents/pod-customer.toon`)**:
   - Covers: Customer Onboarding, Technical Support, Success & Retention, Documentation.
   - Deliverables: Setup checklists, diagnostic reports, policy-adherent customer replies, API docs.
   - Boundaries: Monetary refunds and account provisioning staged as R3 in outbox; bug escalations to `pod-build`.
3. **`pod-build` (`gemini/antigravity-cli/builtin/agents/pod-build.toon`)**:
   - Covers: Executive CTO/VP, Product Management, Software Engineering, Data & AI, Design, IT & Platform.
   - Deliverables: PRDs, C4 models, ADRs, TDD Red-Green-Refactor code, regression test suites.
   - Boundaries: Monotonic test ratchet, functions <50 lines, files <800 lines, rollback snapshot.
4. **`pod-gna` (`gemini/antigravity-cli/builtin/agents/pod-gna.toon`)**:
   - Covers: Executive CEO/CFO/CSO/COO, Finance, Legal & Compliance, Procurement & Facilities.
   - Deliverables: Invoice variance reconciliation, contract risk review, procurement requisitions.
   - Boundaries: Bank disbursements and contract signings are R3 outbox-staged; advisory legal review only.
5. **`pod-people` (`gemini/antigravity-cli/builtin/agents/pod-people.toon`)**:
   - Covers: Hiring, HR Operations, People Strategy, Learning & Development.
   - Deliverables: Role rubrics, candidate screening evaluations, interview scorecards.
   - Boundaries: Human hiring manager retains final employment authority; zero automated rejections.

#### 2. The 104-Role FAANG/MANGO Enterprise Matrix
AGYOS registers 104 operational roles across 12 departments and 5 seniority tiers (L4–L8) in `gemini/antigravity-cli/builtin/agyos_decision/roles.py`:
- **Executive (8 roles, L8)**: CEO, CTO, COO, CPO, CMO, CSO, CFO, VP Engineering.
- **Product (8 roles, L4-L7)**: Product Director, Senior PM, PM, Scrum/Agile Coach, UX Researcher, Growth PM, Product Analyst, Technical PM.
- **Engineering (16 roles, L5-L7)**: Staff SWE, Senior SWE, SWE, Frontend, Backend, Mobile, DevOps, SRE, Security, QA, Web3, Desktop, Network, DB Reliability, Incident Commander, Agentic Architect.
- **Data & AI (10 roles, L4-L7)**: Data Scientist, ML Engineer, Data Engineer, AI Product Engineer, Data Analyst, Research Scientist, Privacy Engineer, Computer Vision, Speech/Audio AI, MLOps.
- **Design (8 roles, L4-L7)**: Design Director, UX/UI, Product Designer, Brand Designer, Motion Designer, 3D Visual Designer, Design System Engineer, UX Copywriter.
- **Marketing (10 roles, L4-L5)**: Content Strategist, SEO Specialist, Performance Marketer, Social Media Manager, Brand Copywriter, CRO Specialist, Email Lifecycle Marketer, PR & Comms, Partnership/BD, Community Manager.
- **Sales & BD (8 roles, L4-L8)**: VP Sales, Account Executive, SDR, Solutions Engineer, Customer Success Manager, RevOps Analyst, Enterprise AE, Freelancer BD.
- **Customer Success (6 roles, L4-L6)**: Support Engineer, Onboarding Specialist, Implementation Consultant, TAM, Churn Analyst, Technical Writer.
- **Finance (8 roles, L4-L7)**: Corporate Controller, FP&A Analyst, Tax Specialist, Billing/Payments Engineer, Treasury Specialist, Accounts Manager, Startup CFO Advisor, Cost Optimization Analyst.
- **Legal & Compliance (6 roles, L5-L8)**: General Counsel, IP/Patent Attorney, Contract Manager, Compliance Officer, Data Protection Officer, Risk Manager.
- **People & Ops (10 roles, L4-L8)**: VP People, Recruiter, HRBP, HR Ops, L&D Specialist, Procurement Manager, Facilities Manager, Executive Assistant, Solopreneur Operator, Chief of Staff.
- **IT & Platform (6 roles, L4-L7)**: IT Sysadmin, Cloud Architect, Platform Engineer, Cybersecurity Analyst, Observability Engineer, FinOps Engineer.

#### 3. 7-Phase Client Working Backwards SDLC Pipeline (`gemini/antigravity-cli/builtin/agyos_decision/sdlc.py`)
Embeds Amazon "Working Backwards" and behavioral psychology (Kahneman System 1/2, Cialdini's 7 Levers, Hick's Law, Loss Aversion):
```
[DISCOVERY] ➔ [PRD] ➔ [ARCHITECTURE] ➔ [TDD_MANUFACTURING] ➔ [VERIFICATION] ➔ [RELEASE] ➔ [HANDOVER]
```
- **Phase 1: DISCOVERY**: Annotated press release + FAQ, Job-To-Be-Done canvas, risk register.
- **Phase 2: PRD**: User stories, acceptance criteria, non-functional requirements, out-of-scope boundaries.
- **Phase 3: ARCHITECTURE**: C4 Container model, architecture decision records, data schemas, API contracts.
- **Phase 4: TDD_MANUFACTURING**: Red (failing test) ➔ Green (minimal code) ➔ Refactor with 80%+ coverage.
- **Phase 5: VERIFICATION**: Static analysis, security scan, benchmark evidence, acceptance criteria proof.
- **Phase 6: RELEASE**: Deployment runbook, feature flags, SLO breach monitors, rollback verification.
- **Phase 7: HANDOVER**: `gemini/antigravity-cli/builtin/state/CURRENT.md` and checkpoint updates, runbooks, retrospective summary, client sign-off.

### Layer 5: Policy Envelopes, EVPI Gate & Recovery Subsystem
- **Typed TaskContracts (`gemini/antigravity-cli/builtin/agyos_decision/contracts.schema.json`)**: Strictly enforces task bounds, allowed/forbidden actions, pre/postconditions, idempotency keys, and Saga compensation specifications.
- **Hierarchy Caps**: Max depth 2 (3 total levels: L0, L1, L2), max 4 children per node, max 3 concurrent workers, max 8 DAG tasks, max 2 retries per node.
- **Run Budget Envelope**: 30,000 tokens, $1.50 USD, 600 seconds, 40 tool calls per run with strictly 20% reserved for verification and rollback.
- **One-Question EVPI Clarification Gate (`gemini/antigravity-cli/builtin/agyos_decision/evpi_clarify.py`)**: Asks at most ONE short question (<25 words) when ambiguity materially affects safety, money, external sends, or legal commitments. Benign ambiguities proceed immediately under explicit assumptions with a standard markdown header.
- **Transactional Snapshots & Rollback (`gemini/antigravity-cli/builtin/agyos_decision/state_ledger.py`)**: Automatic pre-write file snapshots ensuring 100% atomic revert capability.
- **R3 Outbox Hold Queue**: Staged as `PENDING_COMMIT` for human confirmation prior to any irreversible external effect.
- **Reflection Memory**: Episodic error signatures preventing identical retry attempts (Invariant 6).
- **LIFO Saga Compensation**: Reverse-order compensating transactions for multi-step distributed operations (Garcia-Molina & Salem, 1987).
- **Dual Hook Architecture (`gemini/antigravity-cli/hooks.json`)**:
  - `gemini/antigravity-cli/builtin/scripts/hooks/authorizer.py`: Fail-closed authorizer enforcing R3 outbox blocking and capability allowlists.
  - `gemini/antigravity-cli/builtin/scripts/hooks/agy_os_hook.py`: Fail-open safety guard protecting system boundaries from dangerous shell patterns.

---

## 3. Empirical A/B Benchmark Evidence (Single vs Flat vs Adaptive)

Evaluated across 14 frozen multi-domain business task fixtures (`gemini/antigravity-cli/builtin/scripts/tests/fixtures/business_tasks.json`) repeated over 3 independent trials ($N = 3$, 42 total executions per architecture):

| Metric | Single Agent Baseline | Flat Peer Team | Adaptive Hierarchy (AGYOS) |
| :--- | :---: | :---: | :---: |
| **Pass^1 (Single Trial)** | 0.80 [0.69 – 0.91] | 0.00 [0.00 – 0.00] | **1.00 [1.00 – 1.00]** |
| **Pass^3 (Repeated Reliability)** | 0.80 | 0.00 | **1.00** |
| **Forbidden External Actions** | 9 | 5 | **0** |
| **False Approvals (R3)** | 9 | 9 | **0** |
| **Average Token Spend** | 21,108 | 40,160 (Cap Violated) | **13,066 (-38% vs Single)** |
| **Average Cost (USD)** | $0.950 | $2.008 (Cap Violated) | **$0.580 (-39% vs Single)** |
| **Average Latency** | 193ms | 529ms | **113ms (-41% vs Single)** |

---

## 4. The 10 Core AGYOS Operating Principles

1. **Skill-First Autonomous Routing (Highest Priority)**:
   Never execute blind work. On any task, the OS must first identify and invoke the best matching domain specialist skill, silently ingest its runbook, and apply its patterns.
2. **Mandatory Deep Grounding (Highest Priority)**:
   Inspect existing code, manifests, and dependencies via read-only tools before proposing changes. Speculative coding is forbidden.
3. **Pure Human Language & Zero AI Slop (Highest Priority)**:
   Communicate in direct, technical human prose. Bar AI buzzwords, robotic formulaic intros, decorative emoji spam, and unnecessary wrapper abstractions.
4. **Deterministic SOP Progression (`Code = SOP(Team)`)**:
   Enforce gate milestones sequentially through verified machine artifacts.
5. **Hierarchical Virtual Memory Paging**:
   Strictly isolate fast working context from archival storage to preserve context budget and prevent attention degradation.
6. **Maker / Checker Context Separation**:
   An agent that writes code may never approve its own verification gate. Independent review agents must validate every deliverable.
7. **Monotonic Test Ratchet**:
   Test assertions must never decrease. Pre-commit hooks reject changes that delete or weaken coverage.
8. **Fail-Open System Resilience**:
   Lifecycle hooks and interceptors must fail safely without deadlocking agent processes.
9. **Two-Tier Progressive Disclosure**:
   Keep high-frequency core instructions in Tier 1 context; load heavy domain manuals and schemas JIT.
10. **Multi-Model Adversarial Deliberation**:
    High-impact architectural decisions must be reconciled through parallel multi-model consensus before mutation.

## Skill routing contract

All skills and modular rules follow `gemini/antigravity-cli/builtin/rules/common-skill-routing.toon`.
Discover, read, apply, and verify for each task; reuse unchanged runbooks and
repeat discovery when objectives change. `gemini/antigravity-cli/bin/agyos decide "<task>" --json
--runbook` and MCP `agyos_decision` with `include_runbook: true` return selected
instructions. Task intent outranks a language keyword. Matching scores are
heuristics; delivery does not certify execution. See [SKILL_ROUTING.md](SKILL_ROUTING.md).
