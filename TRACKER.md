## Current update: prompt principles upgrade and source audit reconciliation — 2026-11-14

- Audited 26 company and product prompt archive documents against AGYOS prompt principles; reconciled 14,888 principle rows plus 1 separately classified metadata row, accounting for the publisher's 14,889 source rows with zero count mismatches.
- Removed vendor-specific persona and aesthetic branding from active AGYOS-authored prompt surfaces; integrated AGYOS prompt-principles rule in `.agents/rules/agyos-prompt-principles.md` and updated skill routing.
- Added GitHub Actions prompt principles audit step and artifact upload with bounded retention; refreshed generated skill catalog outputs from CI artifacts.
- Milestone `M1-prompt-principles` closed at Gate 5 with full independent review and operator sign-off; GitHub Actions CI run `43585495536` and Pages deployment `43585495534` passed on `main`.
- Full evidence and records: [docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md](docs/PROMPT_PRINCIPLES_UPGRADE_PLAN.md), [docs/research/PROMPT_PRINCIPLES_AUDIT.md](docs/research/PROMPT_PRINCIPLES_AUDIT.md), and [AI_HANDOFF.md](AI_HANDOFF.md).

---

## Historical update: skill catalog quality and OpenWhispr — 2026-11-11

- Audited the 1,982-skill baseline and added the source-backed `openwhispr` skill; the current physical catalog and generated indexes contain 1,983 skills.
- The catalog scanner reports zero structural findings, duplicate descriptions, or exact duplicate-body groups. All primary entrypoints are below 300 lines.
- Moved 613 long runbooks into linked references without unexplained content loss; repaired confirmed links and metadata, improved ten imported placeholders, and resolved eight duplicate-body candidate groups while preserving legacy IDs and local assets.
- Current indexes contain 1,983 skills (390 Tier 1, 1,593 Tier 2). The generators cover all eight catalog/documentation artifacts deterministically.
- Focused catalog/router tests: 41 passed. The host-skipped full suite ran 156 tests: 155 passed and the `agy` CLI integration case was skipped. The filtered AGYOS wrapper passed 51/51 with that same host test skipped; the unfiltered suite recorded three errors. Full evidence is in the audit report.
- OpenWhispr v1.0.2 documents per-activity local/cloud paths, System Audio versus optional Screen Recording, and distinct OAuth consent/API-key scope behavior; its frozen routing case selects `openwhispr`.
- Independent review closed the migration, OpenWhispr, and legacy pointer findings. 309 long-description heuristics and 7,657 freshness-keyword matches remain review candidates; they are not verified defects.
- Full evidence and limits: [catalog audit report](docs/SKILL_CATALOG_AUDIT_REPORT.md). Catalog commit `20947c2d244a16a2b86bf88e0d56102a269ca736` was pushed to `origin/main`; CI and the documentation deployment workflows succeeded for that commit.

---

## Engineering update — 2026-11-08

- Added safe, single-branch Git revert rollback with regression tests; removed destructive reset/clean behavior and automatic rescue branch creation.
- Hardened verification with an isolated state fixture, private temporary logs, timeouts and actual AGENTS.md / GEMINI.md content comparison.
- Added opt-in private-only MCP memory view and read-only privacy coverage diagnostics.
- Bounded external Python subprocess arguments and execution time in the MCP routing services.
- Full-system end-to-end encryption, trustworthy external R3 approval, and live Ubuntu AGY runtime verification remain **open**; see [docs/ENGINEERING_AUDIT_2026-11-08.md](docs/ENGINEERING_AUDIT_2026-11-08.md).
- Older version numbers, verification counts and operational claims below are **historical records**, not current proof.

---

## Historical update: skill routing consistency (2026-11-05)

- Shared discovery/read/apply/verify policy covers all 1,862 skills and 141 rules.
- Catalog metadata, routing, CLI/MCP runbook delivery, generators, and README/docs updated; existing specialist bodies and attribution retained.
- Validation: 75 Python tests, 59 council tests, 51 host verification checks; strict metadata/rule validation; generated assets reproduced; independent Gate 5 review passed.
- Contract and limitations: [docs/SKILL_ROUTING.md](docs/SKILL_ROUTING.md).
- GitHub push requested by the user; remote revision verification follows commit.
- Earlier counts and execution evidence below are historical snapshots.

---

# AGYOS Master Engineering & Capability Tracker

> **System**: AGYOS v3.1 — Unified Cognitive Operating System for Antigravity CLI (`agy`)  
> **Repository Root**: `/home/ai/Documents/projects/Freelance/AGYOS`  
> **Historical status (2026-11-05)**: 51/51 Adversarial Verification Checks, 56/56 Unit Tests, 59/59 Bun Tests; **current live-host status unverified**  
> **Target Runtime**: Google Antigravity CLI (`agy`) v1.5.0 (verified)  
> **Commit SHA**: `ea98092` (Baseline: `22e8706c2be34f0d4bf87c01c01c1ee5b8741068`)  
> **Consolidated Ecosystems**: AGYOS Core (SDLC), AGYOS Governance (5-Gate), Agent Council (Consensus), Adaptive Pod Hierarchy (5 Pods), Company Adapters (11 Functions), Canary Launch Gate, Fail-Closed Authorizer, LIFO Saga Recovery

---

## 1. Historical System Inventory Snapshot (2026-11-05)

The figures below are historical. See the 2026-11-11 update above for the current skill and verification summary.

```
+---------------------------------------------------------------------------------+
|                                 AGYOS CAPACITY                                  |
+---------------------+-------------------+------------------+--------------------+
|  PHYSICAL SKILLS    |  MODULAR RULES    |  ROLE AGENTS     |  CORE PLUGINS      |
|  1,862 Standalone   |  140 Rules (<24K) |  81 Specialized  |  8 Validated (`agy`)|
+---------------------+-------------------+------------------+--------------------+
|  OPERATIONAL PODS   |  MCP SERVERS      |  TOTAL SCRIPTS    |  TEST VERIFICATION |
|  5 Merged Pods      |  1 FastMCP Daemon |  402 Scripts     |  51 / 51 Passed    |
+---------------------+-------------------+------------------+--------------------+
```

---

## 2. Hardening Ledger: Disadvantages Eliminated (ECC vs AGYOS)

| Known Disadvantage / Tradeoff | Root Cause in Legacy AGYOS | Hardened Solution in AGYOS v3.1 | Status |
| :--- | :--- | :--- | :---: |
| **1. Prompt Context Swamping** | 1,846 skills in a flat list overwhelmed the model's system prompt budget. | **2-Tier Progressive Disclosure System**: 399 Tier 1 core software & UI/UX skills load on prompt; 1,439 Tier 2 domain extensions load JIT via `.agents/skills-manifest.json`. | **RESOLVED** |
| **2. Ceremony / Bureaucracy on Tiny Edits** | 5-Gate AGYOS process was too rigid for 1-line typo fixes or small tweaks. | **Adaptive Fast-Path Router**: `bin/agyos fast` bypasses Gates 1–3 for complexity $\le 2$, leaping directly to IMPLEMENT with zero ceremony. | **RESOLVED** |
| **3. Pre-Tool Hook Deadlock Risk** | Missing hook paths or python errors caused exit status 2, halting all tools. | **Fail-Open Fallback Guard**: `scripts/hooks/agy_os_hook.py` catches all unhandled exceptions, defaults safely to `{"decision": "allow"}` without freezing. | **RESOLVED** |
| **4. External Submodule Clutter** | 5 cloned git repos  added 200MB+ bloat & broken symlinks. | **100% Self-Contained Consolidation**: All skills physically copied to `.agents/skills/`; redundant repos & web dashboards deleted. | **RESOLVED** |
| **5. Multi-Runtime Brittleness** | Council required Bun in arbitrary paths. | **Dedicated Council Subsystem**: Streamlined TypeScript engine housed in `scripts/council/` (59 Bun tests green, 0ms latency). | **RESOLVED** |
| **6. Stale Docs Compiler & Web Explorer** | Legacy compiler searched deleted submodules, indexing only 73 skills. | **Unified Dynamic Ingestion Engine**: `scripts/build_docs_data.py` indexes all 1,838 skills directly from `.agents/skills/`, compiles full JSON data & sitemaps, and applies Emil Kowalski UI/UX standards. | **RESOLVED** |
| **7. Brand Fragmentation & Passive Blindness** | Mixed legacy prefixes (`cc-`, `ecc-`, `claude-`) and no automated skill discovery mechanism. | **100% Single Brand + Autonomous Search-First**: Standardized all skills/plugins under pure AGYOS (`agyos-polyglot`), built FastMCP `agyos_find_skill` tool, `bin/agyos find` CLI, and Invariant 7. | **RESOLVED** |
| **8. Flat vs Hierarchical AI OS Architecture** | Lack of explicit hierarchical subsystem mapping and persistent tiered memory model compared to AIOS and MemGPT. | **6-Layer Hierarchical Architecture & 3-Tier Virtual Memory**: Synthesized AIOS, MemGPT, and MetaGPT into Layer 0-5 stack, 3-tier memory paging (`.agents/state/memory.json`), `agyos_sys_info`, `agyos_memory`, and 10 Core Operating Principles (`docs/ARCHITECTURE.md`). | **RESOLVED** |

---

## 3. The 7 Non-Negotiable Gravitas Invariants

1. **Search-First Autonomous Skill Discovery (TOP PRIORITY)**: Whenever given ANY task, problem, or objective, automatically call `agyos_find_skill` or query the catalog FIRST to discover the best matching specialist skill(s), silently ingest the runbook, and use it directly for that work. Never perform blind or speculative work.
2. **Mandatory Deep Research (TOP PRIORITY)**: ALWAYS research using research skills (`research`, `code-explorer`, `deep-research`, codebase AST/grep scans, vendor doc lookups) BEFORE writing code or making modifications. Inspect existing files, dependencies, contracts, and tests first. Never write code on speculation or ungrounded assumptions.
3. **Pure Human Language & Zero AI Slop (TOP PRIORITY)**:
   - **Authentic Engineering Prose**: Use authentic, natural human engineering language. Direct, technical, grounded, and concise.
   - **Banned AI Words & Buzzwords**: Never use words like "delve", "testament", "tapestry", "landscape", "pivotal", "in conclusion", "crucial", "embark", "game-changer", "foster", "leverage", "robust", "streamline", "seamless", "moreover", "unleash", "elevate", "beacon".
   - **Banned Templated & Robotic Phrasing**: No formulaic chatbot intros ("Certainly!", "I'd be happy to help", "As an AI..."), generic rule-of-three, hollow intensifiers, or fake conversational fluff.
   - **Banned AI Symbols**: No decorative emoji spam (🚀, 🛡️, ✨, ⚡, etc.) in system responses, code comments, or commits unless specifically requested.
   - **No Unnecessary Components**: Reject speculative wrappers, premature abstractions, unnecessary utility layers, and boilerplate components. Build only what is needed with clean, minimal implementation.
4. **Stay in Declared Scope**: Confine all file mutations strictly to the active milestone path boundary (`agyos-scope`). Never touch unapproved, cross-module files out of band.
5. **Require Machine Evidence**: Never claim a task, gate, or milestone is complete without executing and printing fresh compiler, linter, or test output.
6. **Avoid Identical Retries**: If a command or test fails twice with the same signature, alter the underlying hypothesis or halt. Never loop blindly.
7. **Satisfy Contract Gates**: Every phase transition must satisfy strict programmatic gate criteria recorded in `.agents/state/state.json`.

---

## 4. The AGYOS 5-Gate Lifecycle Engine

```
[GATE 1: UNDERSTAND] ➔ [GATE 2: ANALYZE] ➔ [GATE 3: PLAN] ➔ [GATE 4: IMPLEMENT] ➔ [GATE 5: VERIFY]
                                 │
                         (Complexity <= 2)
                                 │
                                 └───► [FAST-PATH: IMPLEMENT ➔ VERIFY]
```

- **Gate 1 (UNDERSTAND)**: Intent clarification, acceptance criteria, Task List artifact. HITL approval required.
- **Gate 2 (ANALYZE)**: Read-only AST dependency mapping (`agyos-scout`), blast radius containment, complexity scoring.
- **Gate 3 (PLAN)**: Architecture Decision Records (ADR), C4 models, data contracts, and compact context (`compact.sh`).
- **Gate 4 (IMPLEMENT)**: Autonomous TDD Red-Green-Refactor loop. Functions $<50$ lines, files $<800$ lines, immutability strictly enforced.
- **Gate 5 (VERIFY)**: Full adversarial verification (`bin/agyos verify`), test ratchet monotonicity enforcement, Quiz-Me review.

---

## 5. Emil Kowalski UI/UX & Motion Engineering Standards

Enforced across all frontend, website, and SaaS generation workflows:

1. **Concentric Border Radii Formula**:
   $$\text{Radius}_{\text{inner}} = \text{Radius}_{\text{outer}} - \text{Padding}$$
   Nested elements must mathematically honor this curve to eliminate mismatched optical corners.
2. **The Animation Decision Framework**:
   - **100+ times/day** (shortcuts, command palette, toggles): **0ms (Never animate)**.
   - **Tens of times/day** (hover states, dropdown menus): **150ms – 200ms**.
   - **Occasional** (modals, drawers, sheets): **250ms – 350ms**.
   - **Never animate keyboard-initiated actions**: Immediate response is mandatory.
3. **Compositor-Only Invariant**:
   - Animate **ONLY** `transform` and `opacity`.
   - Never animate layout properties (`width`, `height`, `top`, `margin`, `padding`) without FLIP projection (`<motion.div layout />`).
4. **Tactile Micro-Interactions**:
   - Buttons must provide tactile press feedback: `active:scale-[0.98]`.
   - Hover effects must be wrapped in `@media (hover: hover) and (pointer: fine)` to protect touch users.
5. **Popover Transform Origins**:
   - Scale from the trigger button coordinates, never from the screen center.
6. **Review Format Requirement**:
   - All UI reviews must present issues in a structured Before / After / Why table:
     ```markdown
     | Before | After | Why |
     | --- | --- | --- |
     | transition: all 300ms | transition: transform 180ms ease-out | Prevents layout thrashing |
     | transform: scale(0) | transform: scale(0.95); opacity: 0 | Real objects do not scale from 0 |
     ```

---

## 6. Directory Layout & Subsystems

```text
/home/ai/Documents/projects/Freelance/AGYOS/
├── .agents/                          # Core AGYOS Cognitive Runtime
│   ├── skills/                       # 1,838 physical standalone skills
│   ├── rules/                        # 162 modular governance rules (<24KB)
│   ├── workflows/                    # 100 autonomous execution pipelines
│   ├── agents/                       # 74 corporate role agents
│   ├── plugins/                      # 8 validated AGYOS plugins
│   ├── state/                        # State engine (CURRENT.md, state.json)
│   ├── skills-manifest.json          # Tiered catalog index (Tier 1 vs Tier 2)
│   ├── tier1-skills.json             # Fast-path core skills lookup table
│   └── hooks.json                    # Real-time lifecycle bus
│
├── skills/                           # Direct visible shortcut to all 1,838 skills
├── rules/                            # Direct visible shortcut to all 162 rules
├── workflows/                        # Direct visible shortcut to all 100 workflows
│
├── bin/                              # Kernel binaries & verification scripts
│   ├── agyos                         # Central CLI (init, verify, find, skill, state, gate, fast, council)
│   ├── gate-check.sh                 # Pre-commit test ratchet monotonicity validator
│   ├── state.sh                      # Atomic 5-gate state access layer
│   ├── state-validate.sh             # Self-healing state validator
│   ├── compact.sh                    # Context compaction utility
│   └── rollback.sh                   # Milestone rollback utility
│
├── mcp/                              # FastMCP device drivers
│   └── agyos-state-server.cjs        # FastMCP JSON-RPC 2.0 daemon for AGY CLI (with agyos_find_skill)
│
├── scripts/                          # System automation & hooks
│   ├── hooks/agy_os_hook.py          # Real-time lifecycle interceptor (fail-open)
│   ├── agyos-verify.sh               # 27-point adversarial test runner
│   ├── package_agyos_plugins.py      # Dynamic plugin packager
│   ├── build_tiered_skills_manifest.py # Tier 1 / Tier 2 catalog indexer
│   ├── build_docs_data.py            # Dynamic docs and skills compiler
│   └── council/                      # Multi-model consensus engine (59 Bun tests green)
│
├── assets/                           # Vector branding (agyos-logo.svg)
├── docs/                             # Documentation reference guides & interactive explorer
├── AGENTS.md                         # Constitution, 7 Gravitas Invariants, Emil Kowalski rules
├── GEMINI.md -> AGENTS.md            # Dual-discovery link for Antigravity CLI
├── README.md                         # System documentation
├── AI_HANDOFF.md                     # Milestone handoff & audit trail
├── TRACKER.md                        # This living ledger & engineering tracker
└── skills-lock.json                  # Lockfile tracking installed skills
```

---

## 7. Hierarchical AI OS Architecture & Virtual Memory Model

AGYOS synthesizes the structural patterns of modern AI OS research:
- **AIOS (`agiresearch/AIOS`)**: Kernel abstraction, unified syscall bus via FastMCP stdio daemon, tool/scheduler isolation.
- **MemGPT / Letta (`letta-ai/letta`)**: 3-Tier Virtual Memory Paging (`tier0_core_memory`, `tier1_recall_memory`, `tier2_archival_index`) in `.agents/state/memory.json`.
- **MetaGPT (`geekan/MetaGPT`)**: Multi-agent Standard Operating Procedures (`Code = SOP(Team)`), deterministic artifact handoffs, 5-gate lifecycle.

Full architecture documentation and the 10 Core Operating Principles are codified in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 8. Adversarial Verification Suite: 51 / 51 Passing

```text
============================================================
AGYOS Adversarial Verification Suite
============================================================
• Checking AGENTS.md size limit (<24,000 bytes)... PASS
• Checking GEMINI.md exists and matches AGENTS.md... PASS
• Checking AGY CLI installed and responsive... PASS
• Checking AGYOS MCP server registered in AGY... PASS
• Checking AGYOS Safety Hook blocks dangerous commands... PASS
• Checking AGYOS Safety Hook allows benign commands... PASS
• Checking AGY startup metadata and hook contract regressions... PASS
• Checking AGYOS MCP server JSON-RPC initialize... PASS
• Checking AGYOS MCP server tools/list... PASS
• Checking AGYOS MCP server tools/call (agyos_state)... PASS
• Checking AGYOS MCP server tools/call (agyos_find_skill)... PASS
• Checking AGYOS MCP server tools/call (agyos_sys_info)... PASS
• Checking AGYOS MCP server tools/call (agyos_memory)... PASS
• Checking AGYOS MCP server tools/call (agyos_decision)... PASS
• Checking bin/agyos find skill search CLI... PASS
• Checking bin/agyos decide CLI decision engine... PASS
• Checking bin/agyos sysinfo CLI command... PASS
• Checking bin/agyos mem virtual memory CLI... PASS
• Checking Agent Council Bun test suite (59 passing tests)... PASS
• Checking Plugin validation for agyos-business-creative... PASS
• Checking Plugin validation for agyos-core... PASS
• Checking Plugin validation for agyos-council... PASS
• Checking Plugin validation for agyos-governance... PASS
• Checking Plugin validation for agyos-polyglot... PASS
• Checking Plugin validation for agyos-security... PASS
• Checking Plugin validation for agyos-seo... PASS
• Checking Plugin validation for agyos-verification... PASS
• Checking AGYOS state validation script... PASS
• Checking Merged skills catalog (>400 skills in .agents/skills)... PASS
• Checking Merged rules catalog (>120 rules in .agents/rules)... PASS
• Checking AGYOS master logo exists in assets/agyos-logo.svg... PASS
• Checking bin/agyos executable exists and functional... PASS
• Checking Tiered skills manifest exists and valid... PASS
• Checking Fast-path state bypass functional... PASS
• Checking Hierarchical architecture specification exists... PASS
• Checking Virtual memory state storage exists and valid... PASS
• Checking TaskContract JSON schema validity (Draft 2020-12)... PASS
• Checking Intent compiler maps 11 company functions to 5 pods... PASS
• Checking EVPI clarification asks <= 1 question on critical ambiguity... PASS
• Checking DAG task graph enforces depth<=2, fanout<=4, tasks<=8, workers<=3... PASS
• Checking Run budget tracker reserves 20% for verification and rollback... PASS
• Checking Transactional snapshot rollback restoration... PASS
• Checking LIFO Saga compensation reverse-order execution... PASS
• Checking 5 Pod agent definitions exist in .agents/agents/... PASS
• Checking 5 SOP skills exist in .agents/skills/... PASS
• Checking Fail-Closed Authorizer hook blocks unauthorized R3 payments... PASS
• Checking Fail-Closed Authorizer enforces capability allowlist... PASS
• Checking Atomic-claim verifier enforces 0 unbacked claims... PASS
• Checking Company adapters dry-run operational validation... PASS
• Checking Architecture A/B benchmark execution (pass^1/pass^3 & CI)... PASS
• Checking Canary launch gate & go/no-go audit pass... PASS
============================================================
Verification Summary: 51 PASSED, 0 FAILED
============================================================
```

### 8.1 Empirical A/B Benchmark Results (Single vs Flat vs Adaptive)

Executed on 14 frozen business fixtures (`scripts/tests/fixtures/business_tasks.json`) across 3 trials ($N = 3$, 42 total executions per architecture):

| Architecture | Pass^1 (95% CI) | Pass^3 | Forbidden Actions | False Approvals (R3) | Avg Tokens | Avg USD | Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Single Agent Baseline** | 0.80 [0.69 – 0.91] | 0.80 | 9 | 9 | 21,108 | $0.950 | 193ms |
| **Flat Peer Team** | 0.00 [0.00 – 0.00] | 0.00 | 5 | 9 | 40,160 | $2.008 | 529ms |
| **Adaptive Hierarchy (AGYOS)** | **1.00 [1.00 – 1.00]** | **1.00** | **0** | **0** | **13,066** | **$0.580** | **113ms** |

```bash
# Run the benchmark suite directly
python3 scripts/ab_compare_benchmark.py
```

---

## 9. CLI Quick Reference

```bash
# Verify system integrity across all 33 proof gates
bin/agyos verify

# Query kernel diagnostics, loaded skills, gate, and memory tiers
bin/agyos sysinfo

# Read or write 3-tier virtual memory paging (tier0, tier1, tier2)
bin/agyos mem tier0
bin/agyos mem tier1
bin/agyos mem tier2
bin/agyos mem write <tier> <key> <value>

# Search 1,838+ skills in AGYOS catalog for the best matching specialist
bin/agyos find <query>

# Inspect runbook instructions for a specific skill
bin/agyos skill <name>

# Fast-path for complexity 1-2 tasks after ANALYZE (transitions to IMPLEMENT)
bin/agyos fast

# Inspect active milestone, gate, and session state
bin/agyos state
bin/agyos state --json

# Manually transition AGYOS gate
bin/agyos gate UNDERSTAND
bin/agyos gate ANALYZE
bin/agyos gate PLAN
bin/agyos gate IMPLEMENT
bin/agyos gate VERIFY
bin/agyos gate IDLE

# Convene Agent Council multi-model deliberation
bin/agyos council

# Compact context window and archive current state
bin/agyos compact

# Safely rollback active milestone
bin/agyos rollback
```
