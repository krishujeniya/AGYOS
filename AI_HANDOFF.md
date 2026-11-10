# AGYOS handoff: performance optimization and video processing pipeline

- Task: Optimize AGYOS decision routing, catalog parsing, documentation indexing, unit test execution, and video processing pipelines; preserve test ratchet.
- Branch: `main`.
- Measurements and deltas:
  1. Skill Decision Routing: 49.55x speedup (dropped from 866.86ms/call down to 17.50ms/call) via `@lru_cache` on keyword regex compilation and pre-tokenized query-independent catalog attributes in `agyos_decision/skills_router.py`. Substring guards (`kw in q_lower`, `name in clean_query`) delivered an 8.92x speedup on `classify_domain` (0.1799s down to 0.0202s) and 22.01x speedup on candidate verification (0.1779s down to 0.0081s).
  2. YAML Frontmatter Discovery: 5.73x speedup across 1,979 skills (dropped from 1.388s down to 0.255s) by switching to `yaml.CSafeLoader` in `agyos_decision/catalog.py`.
  3. Module Import & CLI Startup: Lazified 40+ module attributes in `agyos_decision/__init__.py`, dropping import time from 181.51ms to 125.51ms and `bin/agyos decide` shell execution time from 0.730s to 0.399s.
  4. Documentation Generation (`scripts/build_docs_data.py`): 5.50x speedup (dropped from 3.576s down to 0.650s) via manifest fast path.
  5. Test Suite (`scripts/tests/test_skill_routing.py`): 10.82x speedup (dropped from 19.292s down to 1.783s) with 100% pass rate across 17 test cases.
  6. Test Suite (`scripts/tests/test_startup.py`): 4.88x speedup (dropped from 3.81s down to 0.78s) by reading fixed header bytes instead of whole file buffers.
  7. Video Processing Pipeline (`scripts/organic_film_engine.py` and `scripts/repair_ai_video.py`): 3.42x speedup (dropped from 29.60s down to 8.67s on benchmark segment) via `-preset fast -threads 0`.
- Evidence:
  - `python3 -m unittest scripts/tests/test_skill_routing.py`: 17 passed in 1.783s.
  - `python3 -m unittest discover -s scripts/tests -p "test_*.py"`: 110 passed, 0 failed.
  - Total cataloged physical skills: 1,979 verified.
  - Zero secrets or tokens detected.

---

# AGYOS handoff: master architecture, model router & platform research

- Task: Synchronize local `main` with remote, audit 10 reference agent platforms, crosswalk FAANG/SRE/DevOps standards, create threat model and data flow inventory, implement AGYOS Model Registry and Router with strict privacy gating and context economics, fix `bin/agyos mem` CLI parameter defect, clean obsolete files, and execute full verification.
- Branch: `main`; baseline SHA: `35903ad9125607daf89ca2f189864136dbe18a67`.
- Scope and contracts: `docs/research/AGYOS_MASTER_IMPLEMENTATION_PLAN.md`, `docs/security/THREAT_MODEL.md`, `docs/security/ENCRYPTION_COVERAGE.md`.
- Changes:
  1. `agyos_decision/model_router.py`: Canonical model registry (Gemini Flash, Claude Sonnet/Opus), alias resolution, 4-tier task mapping (T0-T3), fail-closed privacy boundary for confidential/secret data (`LOCAL_INFERENCE_UNAVAILABLE`), and context budget calculations.
  2. `bin/agyos`: Added `model-route` command with `--sensitivity` and `--override` options; fixed memory CLI argument bug where empty string `key=""` broke MCP parameter validation.
  3. `scripts/tests/test_model_router.py`: 12 comprehensive unit tests covering canonical specs, aliases, complexity tiers, privacy failure modes, and context allocations.
  4. Platform & Standards Research: 10 open-source agent platforms audited across 45 principles in `docs/research/TEN_AGENT_PLATFORMS.md`; 41 FAANG/SRE standards crosswalked in `docs/research/FAANG_SRE_DEVOPS_PRINCIPLES.md`.
  5. Security & Operations: Created `docs/security/THREAT_MODEL.md`, `docs/security/DATA_FLOW_INVENTORY.md`, `docs/security/ENCRYPTION_COVERAGE.md`, `docs/OPERATIONS_RUNBOOK.md`, and `docs/IMPLEMENTATION_REPORT.md`.
  6. Cleaned obsolete script `.agents/state/decisions/executed/20260725-050600-cleanup-unnecessary-files.sh`.

## Executed Evidence

- `python3 -m unittest discover -s scripts/tests -q`: **110 passed, 0 failed** in ~25.8s (monotonic increase from 98 to 110).
- `node --test scripts/tests/test_secure_envelope.cjs`: **5 passed, 0 failed**.
- `node --test scripts/tests/test_private_vault.cjs`: **6 passed, 0 failed**.
- `node --test scripts/tests/test_mcp_protocol.cjs`: **6 passed, 0 failed**.
- `bash scripts/agyos-verify.sh`: **51 passed, 0 failed**.
- `bin/gate-check.sh`: **passed**.
- `python3 scripts/agyos-privacy-audit.py`: **clean read-only scan**; reports `PARTIAL_ENCRYPTION_NOT_SYSTEM_WIDE_E2EE` honestly.

---

# AGYOS handoff: skill routing consistency

- Task: update catalog-wide rules, skill discovery metadata, decision routing, README/docs, and push to GitHub.
- Branch: `main`; implementation base: `8e15b83` (three existing unpushed skill commits retained).
- Scope and contract: `docs/SKILL_ROUTING.md`; decision record: `docs/adr/0001-skill-routing.md`.
- Changes: shared routing policy covers 1,862 skills and 141 modular rules; repaired malformed headers and normalized canonical IDs; shared YAML parser; safe catalog fallbacks; task-first matching; conservative complexity; CLI/MCP runbook delivery; consistent search; generated catalog commands and risk labels; deterministic regeneration check in CI.
- Files: `.agents/rules/common-skill-routing.md`, `.agents/skills/AGENTS.md`, repaired skill headers and governance runbooks, manifests, `agyos_decision/catalog.py`, `agyos_decision/skills_router.py`, CLI/MCP entry points, generators, routing tests, CI, README, docs, gate records, and the pre-commit zero-assertion count fix with two real Git fixture regressions.

## Executed evidence

- `python3 -m unittest discover -s scripts/tests -v`: **75 passed**, including 17 routing/catalog tests and CLI/MCP integration (unrestricted host run).
- `bash scripts/agyos-verify.sh`: **51 passed, 0 failed**. The final risk fix was subsequently verified by the routing suite and independent checker.
- `bun test` in `scripts/council`: **59 passed, 0 failed**.
- `python3 -X pycache_prefix=/tmp/agyos-bytecode -m compileall -q .`: **passed**; `node --check mcp/state-server.cjs`, `bash -n bin/agyos`, and `git diff --check`: **passed**.
- Both manifests and all generated documentation assets reproduced byte-for-byte in a temporary output directory.
- All 1,862 skill YAML headers and 141 rule headers/size limits validated. Independent body comparison found preserved original text, with intentional governance updates and restored cluster warnings.
- Independent checker: **Gate 5 PASS**; verified destructive/external tasks score 5, unknown scope 3, bounded tasks 2, and a README typo 1.
- Browser: updated section rendered at 1440x900 and 390x844; no page overflow at those widths; internal anchors valid; Enter activated the updated Copy button and showed Copied feedback. A file URL was used, so live catalog fetch/deployment acceptance was not claimed.
- Gitleaks with `--redact`: existing three outgoing commits and current tracked diff **clean**. The staged diff also passed the redacted scan before commit preparation.

## Limits and next step

Keyword routing cannot guarantee every host invokes a skill or certify every specialist procedure. Historical body fragments were preserved rather than invented. Selection and file delivery remain separate from execution evidence. No configured Python linter or type checker was found; these were not claimed as passing.

The user explicitly authorized push. Local validation and independent review are complete. The staged diff is checked with Gitleaks and the test ratchet before commit; remote delivery is confirmed separately. No force-push is authorized. This handoff records the implementation base; use Git history for the resulting revision.

Exact next command:

```bash
git ls-remote origin refs/heads/main
```

---

## Previous milestone (historical evidence)
# AGYOS Engineering Handoff — Adaptive Hierarchy & Policy Verification

## Task and Revision
- Task: Hierarchical Agent OS Implementation (5 Pods, Typed TaskContracts, EVPI Gate, Recovery, Fail-Closed Hook, A/B Benchmark)
- Pinned Runtime: Google Antigravity CLI (`agy`) v1.5.0
- Baseline SHA: `22e8706c2be34f0d4bf87c01c01c1ee5b8741068`
- Completed Commit SHA: `69cf570`
- Branch: `main`

## Summary of Executed Changes

### 1. Contracts & Intent (`agyos_decision/`)
- `agyos_decision/contracts.schema.json`: Strict JSON schema (Draft 2020-12) enforcing typed TaskContracts (task_id, run_id, depth<=2, 5 merged pods, risk tiers R0-R3, budget envelopes, pre/postconditions, capability allowlist, Saga compensation).
- `agyos_decision/contracts.py`: Dataclass models and schema validation for TaskContract, Budget, Postconditions, and Compensation.
- `agyos_decision/intent_compiler.py`: Natural language intent compiler mapping all 11 company functions into 5 merged pods (`pod-growth`, `pod-customer`, `pod-build`, `pod-gna`, `pod-people`) with zero slash commands, keywords, or manual agent names.
- `agyos_decision/evpi_clarify.py`: Expected Value of Perfect Information (EVPI) clarification engine asking at most ONE short question (<25 words) on critical ambiguity/R3 irreversible actions; benign ambiguities proceed immediately with explicit assumptions header.

### 2. State, Budgets & Recovery
- `agyos_decision/state_ledger.py`:
  - `DAGTaskGraph`: Enforces depth <= 2 (3 levels), <= 4 children per node, <= 3 concurrent workers, <= 8 DAG tasks, and acyclicity validation.
  - `RunBudgetTracker`: Enforces 30k tokens, $1.50 USD, 600s, 40 tool calls with strictly 20% reserved for verification and rollback.
  - `SnapshotManager`: Transactional state snapshots with atomic rollback restoration.
  - `OutboxQueue`: R3 action staging queue holding irreversible actions in `PENDING_COMMIT` until explicit operator authorization.
  - `ReflectionMemory`: Episodic error signature tracking preventing identical failing retries (Invariant 6).
  - `SagaCoordinator`: LIFO reverse-order compensating transactions (Garcia-Molina & Salem, 1987).

### 3. Host Adapters & Pods
- Created 5 Pod Agent definitions in `.agents/agents/` using valid host tool names and `invoke_subagent` delegation:
  - `.agents/agents/pod-growth.md` (Marketing, Leads, Sales)
  - `.agents/agents/pod-customer.md` (Onboarding, Support)
  - `.agents/agents/pod-build.md` (Product, Engineering)
  - `.agents/agents/pod-gna.md` (Finance, Legal, Operations)
  - `.agents/agents/pod-people.md` (Hiring, Talent)
- Created 5 SOP Skills in `.agents/skills/`:
  - `.agents/skills/sop-growth/SKILL.md`
  - `.agents/skills/sop-customer/SKILL.md`
  - `.agents/skills/sop-build/SKILL.md`
  - `.agents/skills/sop-gna/SKILL.md`
  - `.agents/skills/sop-people/SKILL.md`
- Wired `scripts/hooks/authorizer.py` fail-closed authorizer hook alongside `scripts/hooks/agy_os_hook.py` in `.agents/hooks.json`.

### 4. Verification & A/B Benchmark
- `agyos_decision/verifier.py`: Atomic-claim decomposition and grounding verifier enforcing 0 unbacked numeric/contract claims (P19).
- `scripts/ab_compare_benchmark.py`: Evaluates Single Agent vs Flat Peer Team vs Adaptive Hierarchy across identical frozen business fixtures (`scripts/tests/fixtures/business_tasks.json`) with N=3 repeated trials and 95% bootstrap confidence intervals.
- Extended `scripts/agyos-verify.sh`: 51 / 51 adversarial checks passing.

### 5. Role Catalog & Hook Portability Hardening
- Normalized all 81 agent definitions in `.agents/agents/` (including 71 legacy definitions) to declare strictly valid `agy` 1.5.0 host tools (`read_file`, `write_file`, `edit_file`, `run_command`, `search_web`), eliminating legacy references (`view_file`, `write_to_file`, `replace_file_content`, `grep_search`, `find_by_name`, `read_url_content`).
- Modernized `.agents/hooks.json` to use checkout-relative commands (`scripts/hooks/...`), removing hardcoded `/home/ai/...` absolute path assumptions.
- Added `test_all_agent_files_declare_only_valid_host_tools` regression check to `scripts/tests/test_hooks_authorizer.py`.

### 6. Manifest & Documentation Inventory Synchronization
- Synchronized `.agents/skills-manifest.json` and `.agents/tier1-skills.json` to include 13 newly created/updated AGYOS skills (`agyos-karpathy-guidelines`, `agyos-agency-agents`, `agyos-app-launch-checklist`, `agyos-anti-ai-design`, `agyos-lead-scraper`, `agyos-free-infra-catalog`, `agyos-startup-distribution`, `agyos-academic-research`, `agyos-swarm-prediction-engine`, `agyos-startup-stack`, `agyos-founder-guide`, `agyos-binary-analysis`, `agyos-software-protection`), bringing the total physical skill count from 1,849 to 1,862 (Tier 1: 381, Tier 2: 1,481).
- Rebuilt static documentation assets via `scripts/build_docs_data.py` (`docs/skills-data.json`, `docs/ai-catalog.json`, `docs/sitemap.xml`, `docs/robots.txt`, `docs/llms.txt`).
- Aligned `README.md`, `docs/index.html`, `AGENTS.md`, and `TRACKER.md` with exact filesystem counts (1,862 skills, 140 rules, 81 agents, 51 verification checks).
- Resolved specification contradiction on Gate 2 complexity score in `AGENTS.md` and `GEMINI.md`: 1-2 fast-path bypass vs 3-5 full 5-gate flow.

## Verification Evidence Actually Run

- `bash scripts/agyos-verify.sh`: **51 PASSED, 0 FAILED**
- `python3 -m unittest discover -s scripts/tests -v`: **56 PASSED, 0 FAILED**
- `cd scripts/council && bun test`: **59 PASSED, 0 FAILED**
- `python3 scripts/ab_compare_benchmark.py`:
  - Single Agent: Pass^1 = 0.80, Pass^3 = 0.80, 9 forbidden actions, 9 false approvals, 21,108 tokens, $0.950, 193ms.
  - Flat Peer Team: Pass^1 = 0.00, Pass^3 = 0.00, 5 forbidden actions, 9 false approvals, 40,160 tokens (exceeds cap), $2.008, 529ms.
  - Adaptive Hierarchy: Pass^1 = 1.00 [1.00-1.00], Pass^3 = 1.00, 0 forbidden actions, 0 false approvals, 13,066 tokens, $0.580, 113ms.

## Exact Next Command

```bash
bash scripts/agyos-verify.sh
```
