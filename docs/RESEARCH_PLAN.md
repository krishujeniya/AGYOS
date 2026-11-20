# AGYOS Hierarchical Agent OS — Reconciled Research & Approval Plan

**Status:** PROPOSAL ONLY — no implementation changes authorized. Zero repository files have been modified.
**Prepared:** 2026-11-04.
**Repository:** https://github.com/krishujeniya/AGYOS
**Review baseline:** `main` at `22e8706c2be34f0d4bf87c01c01c1ee5b8741068`, content verified via the GitHub API on 2026-11-04. This supersedes the older baseline (`d418ff2…`) used in draft 2 of this plan; line anchors below were re-checked against the newer baseline where files were re-fetched, and must be re-derived with `git grep -n` at implementation time.
**Decision requested:** approve or reject this plan — NOT deployment, live customer actions, or any code change.

## How this document was produced (verification log)

Two draft plans were reconciled against the live repository, the official `agy` host documentation, and publisher records:

- **Draft 1** (7-part spec shape, strong on contracts/Sagas/EVPI/5-pod topology) was written without live repo access; its audit is superseded by the source-anchored audit below. Its useful machinery (typed contract schema, EVPI matrix, 5-pod merge topology, 3-regime sensitivity) is retained.
- **Draft 2** (evidence-led audit + principle catalog) supplied the verified audit spine and most of the catalog.
- **Every citation** in Section 2 was verified on 2026-11-04 against a publisher page, official proceedings page (PMLR/NeurIPS/ACL/USENIX/OpenReview), or DOI resolver. Where publishers blocked automated access (IEEE Computer Society, JSTOR, University of Chicago Press, ACM), verification was completed via publisher-linked bibliographic records (IEEE Computer Society issue pages, JSTOR issue TOCs, RePEc/EconPapers, USENIX Open Access) that quote the DOI verbatim. No claim in this plan rests on an unverified citation.
- **Correction to draft 1:** the claim that "NeurIPS/ICLR/ICML proceedings do not mint Crossref DOIs" is wrong for NeurIPS 2022+ (Curran Associates DOIs, e.g. `10.52202/…`, verified live). ICLR/ICML records are OpenReview/PMLR (no per-paper Crossref DOI); that is stated per entry.
- **arXiv-only work is quarantined** (Section 2.3) and forms no part of the evidence base.
- Where evidence is thin this document says **"I'm not sure"** rather than guessing. Every AGYOS claim carries a repository file path.

## 0. Executive decision

Build a **policy-constrained adaptive hierarchy**, not a permanent collection of concurrently operating personas. Plain-language requests pass through intent → policy → planning → optional native `agy` delegation → verification → memory/recovery. One agent is the default. Spawn specialist workers only when a typed dependency graph contains independently useful, bounded work and a measured single-agent baseline indicates benefit. External sends, spending, hiring decisions, production changes, contractual commitments and deletion require explicit authorization.

This proposal is **not evidence that AGYOS is currently an autonomous company OS**. Existing agent and workflow descriptions are mainly instructions; the current machine executor is a technical-domain keyword router plus state/skill MCP tools (`agyos_decision/skills_router.py`, `mcp/state-server.cjs`). The evidence base supports parts of the design, but **I'm not sure** that any published paper establishes a universal best hierarchy for real company-wide work. The architecture and thresholds below are hypotheses requiring AGYOS-specific experiments.

**Scope boundary:** this document only. Do not edit application code, prompt/rule files, hooks, runtime state, tests or deployment configuration until approval.

---

## 1. Audit

### 1.1 Methodology and status labels

**Source tiers:** (a) inspected executable source and explicit tests, (b) repository documentation and historical claims, (c) official `agy` host documentation, (d) peer-reviewed publisher record. A test file is evidence of coverage, **not** evidence that it passed now. Repository files were read remotely via the GitHub API; no fresh `agy`/Bun/Python integration suite was run in the target Ubuntu environment. Status labels: **Implemented and Tested** = implementation + explicit test assertion present (historical pass claims are *not* promoted to fresh pass); **Unverified** = implementation exists, runtime behavior not established; **Partial** = incomplete functionality; **Docs Only** = stated procedure lacks a matching executor; **Missing** = no implementation observed in inspected entrypoints. Absence findings are scoped to inspected paths.

### 1.2 Existing capabilities — source-anchored audit

Line anchors: `path:start-end` as recorded at the review baseline (`22e8706c`). Content of every file listed was re-confirmed at this baseline on 2026-11-04.

| Capability | Status | Repository path and line evidence | Assessment / next proof |
|---|---|---|---|
| Plain-language **skill matching** | Partial | `agyos_decision/skills_router.py:197-213,245-316,319-353`; `mcp/state-server.cjs:318-331` | Regex/token matching and heuristic fit exist; not proven semantic intent understanding or agent execution; measure paraphrase/OOD recall. |
| Domain taxonomy for whole company | Partial | `agyos_decision/skills_router.py:21-100,197-213`; `.agents/agents/marketing-agent.md:1-11` | Primarily engineering classification despite marketing agent file; sales/support/legal/HR operations need task ontology and policy constraints. |
| Complexity-based fast path | Partial | `agyos_decision/skills_router.py:216-242,342-347`; `bin/agyos:62-67` | Heuristic default complexity 2, and CLI `fast` mutates gate directly; no proven safe intent/risk gate. |
| Skills lookup over catalog | Implemented and Tested | `mcp/state-server.cjs:207-291`; `scripts/agyos-verify.sh:63-74` | Source and smoke assertions exist; <10 ms timing, precision, corpus count and full integrity not freshly benchmarked. |
| JSON-RPC stdio MCP tool interface | Implemented and Tested | `mcp/state-server.cjs:25-140,348-426`; `scripts/agyos-verify.sh:58-71` | Initialize, tool list and tool call implemented/tested by scripted greps; production MCP client interoperability unverified. |
| State/current/graph/checkpoint MCP tools | Partial | `mcp/state-server.cjs:294-317`; `.agents/state/context-graph.json:1` | Read functions exist, but checked-in dependency graph has empty nodes/edges/invariants. |
| Memory read/list/write | Unverified | `mcp/state-server.cjs:141-202,333-338`; `.agents/state/memory.json:1-34` | JSON KV tiers exist; no proven tenant ACL, retention, encryption, retrieval quality, race safety or provenance. |
| System health reporting | Partial | `mcp/state-server.cjs:143-170` | Health and plugin statuses are literal constants (including "100% Operational"), not probes. |
| Zero-command natural-language orchestration | Docs Only | `AGENTS.md:102-126`; `GEMINI.md` §7 (mirrors AGENTS.md); `bin/agyos:30-124` | Prompt prescriptions exist; CLI implementation dispatches named subcommands. No AGYOS-owned natural-language supervisor/stateful execution loop found in these entrypoints. |
| Five-stage governance policy | Partial | `AGENTS.md:28-56`; `bin/agyos:48-67`; `.agents/state/state.json:1-25` | Five stages documented and gate state writable; verified approval/transition rules across all actions not proven. |
| Maker/checker isolation | Docs Only | `AGENTS.md:60-65`; `.agents/rules/common-agents.md:53-61` | Explicit instructions, but no observed enforced independent attestations for each deliverable. |
| Native custom-role catalog | Unverified | `.agents/agents/marketing-agent.md:1-29`; `.agents/agents/faang-architect.md:1-11`; `.agents/rules/common-agents.md:6-28` | Role files exist. `agy` may discover them; actual availability/tool-name validity must be tested on pinned `agy`. |
| Marketing workflow | Partial | `.agents/workflows/marketing-campaign.md:1-24,81-94`; `.agents/agents/marketing-agent.md:22-45` | Detailed procedure, but slash entrypoint and legacy `.claude` output convention conflict with fully invisible routing. No live campaign execution proved. Also: legacy workflow indexing ended 2026-10-19 (§1.4). |
| Other workflow portability | Partial | `.agents/workflows/multi-workflow.md:1-23,38-93` | Explicit dependency on external `ccg-workflow` runtime (`npx ccg-workflow`, `~/.claude/bin/codeagent-wrapper`, Claude-style Bash/TaskOutput); not native `agy` end-to-end execution evidence. |
| Role/workflow completion contract | Docs Only | `.agents/rules/common-agents.md:53-61` | Correct anti-orphan instruction, not a scheduler with join/cancel/timeout enforcement. |
| Lifecycle hook loading/config | Unverified | `.agents/hooks.json:1-50`; `scripts/tests/test_startup.py:17-61` | Config references hard-coded `/home/ai/...` path. Loading in any other checkout is at risk; verify with `agy` hook inventory. |
| Dangerous shell-command hook filters | Implemented and Tested | `scripts/hooks/agy_os_hook.py:6-12,14-43`; `scripts/tests/test_startup.py:28-61` | Specific patterns tested. This is NOT comprehensive tool authorization, tenant isolation or prompt-injection prevention. |
| Hook fail-open on unknown/fault conditions | Partial | `scripts/hooks/agy_os_hook.py:28-52`; `docs/ARCHITECTURE.md:39-45` | Allows unspecified actions and exceptions. Availability-friendly, unsafe as sole control for irreversible/high-risk actions. |
| Startup contract regressions | Implemented and Tested | `scripts/tests/test_startup.py:64-105`; `scripts/agyos-verify.sh:42-55` | Tests for metadata/frontmatter/files and notification escaping exist; fresh suite not executed in this review. |
| Council engine/test command | Unverified | `scripts/council/package.json:1-14`; `bin/agyos:114-115`; `scripts/agyos-verify.sh:76-77` | External package (`cliagent-council` v0.4.0, repo `yogirk/agent-council`); Bun test command exists; current pass count, providers, model diversity and gains not verified. |
| Company-wide operations (CRM, invoices, hiring, legal commitments, customer messages) | Missing | `mcp/state-server.cjs:25-140,294-339`; `agyos_decision/skills_router.py:21-166`; marketing content only at `.agents/agents/marketing-agent.md:22-45` | No typed business data adapters, per-tenant action grants, end-state verifiers or approval receipts demonstrated in examined core. |
| Stable run ledger / retry / compensation executor | Missing | `.agents/state/state.json:1-25`; `mcp/state-server.cjs:294-339`; recovery instructions `.agents/agents/loop-operator.md:22-49` | State file and written retry advice exist, but no persisted transactional DAG executor or structured compensations observed. |
| Verification shell script | Implemented and Tested | `scripts/agyos-verify.sh:1-113` | Executable smoke-check definitions exist, but are not a measure of corporate task correctness; some checks invoke local `agy`/Bun. |
| Reproducible verification pass claim | Unverified | `README.md` badge "Verification-36/36" and tree label "agyos-verify.sh # Adversarial verification test suite (34 checks)"; `TRACKER.md:3-22` (33/33); `AI_HANDOFF.md:32-37` (34/34); `.agents/state/CURRENT.md:5-10` (34/34 with noted failures) | Counts vary across snapshots *within* the same baseline. Do not report a consolidated pass number without fresh command logs and commit SHA. |
| Memory as autonomous recall/reasoning | Docs Only | `docs/ARCHITECTURE.md:47-51,95-116`; `.agents/state/memory.json:4-32` | Tier labels and seed content present; memory quality and paging unproven. |
| Security and finance/legal guardrails | Docs Only | `.agents/rules/common-security.md:1-32`; `AGENTS.md:20-24` | Guidance exists, but no verified policy evaluation for tool APIs or cross-organization data. |

### 1.3 Contradictions that must be resolved before implementation

1. **Version/count drift** (all confirmed at baseline `22e8706c`): README headline/badge says **1,844+ skills / 36/36 verification / 76 agents / 140+ rules**, while the README tree label says the verify suite has **34 checks**; `TRACKER.md` says **1,838 skills / 33/33 / 74 agents / 162 rules**; `AI_HANDOFF.md` says **1,837 / 34/34**; `docs/ARCHITECTURE.md` Layer 2 says "1,842 skills" vs Layer 5 "1,844"; `GEMINI.md` §8 says "1,838+ skills"; `.agents/state/memory.json:27-33` seeds 1,838/162. Inventory from filesystem at a frozen SHA; never hardcode counts in diagnostics.
2. **Runtime references**: documented `mcp/agyos-state-server.cjs` vs primary `mcp/state-server.cjs` (`docs/ARCHITECTURE.md:53-62`; `AI_HANDOFF.md:20-25`; `bin/agyos:82-83`; also `GEMINI.md` §8). `AI_HANDOFF.md` claims a backward-compat symlink; confirm on Linux.
3. **Inconsistent gates**: `AGENTS.md:41-44` and `GEMINI.md` Gate 2 say "complexity score (1-5 skips to IMPLEMENT; 6-10 full flow)" while the code scores 1–5 (`agyos_decision/skills_router.py:216-242`). Fix specification and test safety before any automatic fast path.
4. **State disagreement**: `.agents/state/state.json:3-5` current gate `IDLE` vs `.agents/state/CURRENT.md:1-8` `VERIFY`. Treat CURRENT as commentary, not an authoritative ledger.
5. **Uncalibrated confidence**: `agyos_decision/skills_router.py:211-213,302-305` calls arithmetic hit scores "calibrated confidence"; these are NOT observed probabilities (see P13, Section 2).
6. **Unsafe permission default**: `scripts/hooks/agy_os_hook.py:34-52` handles only selected command strings and permits malformed/unknown input. Preserve tool availability with a separate **fail-closed** high-impact authorizer; do not pretend this hook establishes security.
7. **Agent host tool names**: `.agents/agents/faang-architect.md:4-9` requests `read_file`/`edit_file`/`write_file`; the official tool list names `view_file`/`write_to_file`/`replace_file_content` and warns unknown mappings may hang. Validate definitions on the actual `agy` version.
8. **Legacy workflow end-of-support**: the official migration notice states legacy `.agents/workflows/*.md` ceased to be indexed/executable after **2026-10-19** (§1.4). The catalog remains useful source material but must not be counted as callable host workflows; convert needed procedures to `.agents/skills/` after approval.
9. **Tests vs production capability**: grep-based smoke tests and historical pass claims (`scripts/agyos-verify.sh:58-83`) cannot establish multi-step business transaction correctness.
10. **MCP is not a delegation mechanism**: `mcp/state-server.cjs` exposes state/skill tools over stdio JSON-RPC. Nothing verified indicates MCP tools can spawn host subagents; delegation must use the host's native `invoke_subagent` (§1.4).

### 1.4 `agy` host contract (checked official docs, 2026-11-04)

Verified on `antigravity.google` docs pages:

- **Skills** (`/docs/skills`): CLI discovers `.agents/skills/<folder>/SKILL.md` (description required); autonomous natural-language selection is documented. A skill may also expose an optional slash alias, but users need no slash commands.
- **Custom subagents** (`/docs/subagents?tab=cli`): CLI discovers `.agents/agents/<name>.md` or nested `agent.md`; YAML metadata includes name/description/tools/subagent/model; native `invoke_subagent` is the worker mechanism; context is isolated.
- **Hooks** (`/docs/hooks?tab=cli`): CLI loads `.agents/hooks.json`; events: SessionStart, PreToolUse, PostToolUse, PreInvocation, PostInvocation, Stop; PreToolUse decisions include allow/auto_approve/deny/ask/force_ask/deny_unless_prior_grant; hooks in `settings.json` are not loaded.
- **Workflow migration** (`/docs/migration/workflows-to-skills`): legacy `.agents/workflows/*.md` ceased being indexed/executable on **2026-10-19**; skills replace them with automatic natural-language discovery.
- **CLI** (`/docs/cli/using`): `agy` launches a natural-language TUI.

**I'm not sure** (not found on the fetched official pages; treat as unconfirmed): a specific subagent nesting limit ("10" appears in community material), workspace modes named inherit/branch/share, and a headless `agy "prompt"` form. None changes this plan: the proposed depth is 3 levels, well under any plausible cap. Pin and probe `agy --version`, agent discovery, hooks and MCP before delivery — the globally installed CLI may differ from current docs.

---

## 2. Peer-reviewed principle catalog — publisher-verified

**Evidence levels:** **Direct** = measured on agent workflows closely related to the target operation; **Indirect** = empirical results on adjacent ML/HCI tasks; **Theoretical** = formal or analytic principle without AGYOS validation; **Hypothesis** = proposed AGYOS-specific mapping unsupported by a direct experiment. These labels describe **transfer to AGYOS**, not the paper's review status. "DOI not listed" means the venue assigns no per-paper Crossref DOI (ICLR/OpenReview, ICML/PMLR, USENIX); an arXiv DOI never substitutes. Every entry was verified on 2026-11-04 on the publisher, official proceedings, or OpenReview page.

### 2.1 Active evidence base

| ID, proposed principle | Authors; year; peer-reviewed venue; DOI / verified record | Finding; important limits | AGYOS target; level; one measurable experiment |
|---|---|---|---|
| P01 **Delegate conditionally; single agent first** | Yubin Kim, Ken Gu, Chanwoo Park, et al.; 2026, *Nature Machine Intelligence*; `10.1038/s42256-026-01268-y` | In matched-compute tests over six agentic benchmarks, extra agents sometimes worsened results; an in-domain architecture-selection model identified winners in ~87% of held-out configurations. The ~45% "saturation" figure is a dataset-dependent heuristic, not a universal threshold; poor cross-domain extrapolation. (Figures as reported by the authors; not independently re-computed.) | Adaptive supervisor; **Direct** for multi-agent architecture, **Hypothesis** for AGYOS; compare single/flat/hierarchical on identical business cases at matched cost and compute; report pass³ and dollars per success. |
| P02 **Ground actions in tool observations** | Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao; 2023, **ICLR**; DOI not listed; OpenReview `WE_vluYUL-X` | ReAct interleaves reasoning, action and observation, improving selected reasoning/interactive tasks (e.g. +34% success on ALFWorld one-shot vs imitation/RL baselines); not proof of reliable external action execution. | Planning/execution; **Direct**; compare dry-run tool-grounded action selection against single-shot recommendations on 60 cases; count unintended calls and final-state success. |
| P03 **Use explicit tool schemas and least-action interfaces** | Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, et al.; 2023, **NeurIPS**; `10.52202/075280-2997` | Toolformer trains a model to select APIs and use results; tasks and training differ from `agy` orchestration; tool correctness/authorization not established by this paper. | Tool adapter/contract schema; **Indirect**; measure malformed arguments and invalid/unauthorized tool calls before and after schema validation. |
| P04 **Plan a bounded dependency graph** | Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, Ee-Peng Lim; 2023, **ACL**; `10.18653/v1/2023.acl-long.147` | Plan-and-Solve reduced missed reasoning steps on static tasks; does not prove production DAG scheduler safety. | Planning/typed subtasks; **Indirect**; score omitted prerequisites, contract violations and plan edit count across 100 business tasks. |
| P05 **Search/backtrack only when worth its cost** | Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan; 2023, **NeurIPS**; `10.52202/075280-0517` | Tree of Thoughts boosts some planning/puzzle performance via candidate search, at multiplied token cost; not tested on general company operations. | Planner/recovery; **Indirect**; compare 1 vs 2 vs 4 plan candidates on dependency-heavy cases; report success per 1k tokens. |
| P06 **Use bounded feedback/reflection on failures** | Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao; 2023, **NeurIPS**; `10.52202/075280-0377` | Reflexion improved certain task retries using verbal feedback and short episodic memory; self-reflection can be inaccurate and is no substitute for independent test evidence. | Recovery/short-term memory; **Direct** for agents; A/B single retry with stored error signature vs blind same-prompt retry; measure recovery and waste. |
| P07 **Self-critique is useful but cannot certify correctness** | Aman Madaan, Niket Tandon, Prakhar Gupta, et al.; 2023, **NeurIPS**; `10.52202/075280-2019` | Self-Refine improved evaluated text/code tasks; feedback and maker can share one model and correlated errors. | Verification/revision; **Indirect**; compare self-critique, independent reviewer, executable assertions and hybrid on seeded defects; measure false acceptance. |
| P08 **Treat retrieved text as untrusted data** | Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner, Marc Fischer, Florian Tramèr; 2024, **NeurIPS Datasets & Benchmarks**; `10.52202/079017-2636` | AgentDojo shows agents are vulnerable to indirect prompt injection and fail even with no attack; defenses vary. | Policy/tool results/memory; **Direct**; run injection fixtures in fetched leads, tickets and documents; measure attack success and legitimate task retention. |
| P09 **Measure actual end state and repeated-run reliability** | Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan; 2025, **ICLR**; DOI not listed; OpenReview `roNSXZpUDN` | τ-bench evaluates customer-service agents against database end state and passᵏ; even top models solve <50% of tasks and are inconsistent (pasŝ⁸ < 25% in retail); simulated retail/airline tasks are not AGYOS business reality. | Verification/evals; **Direct**; 3 seeded trials per case, verify CRM/ticket/invoice state exactly, compute pass¹ and pass³. |
| P10 **Design the computer interface for agents** | John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press; 2024, **NeurIPS**; `10.52202/079017-1601` | SWE-agent showed tool/interface design improves coding-agent performance; results depend on specific tools/benchmarks. | Tool interfaces/test harness; **Direct** for engineering, **Indirect** for business; compare raw CLI vs typed, narrowly scoped tool API on identical repair tasks; count errors and time. |
| P11 **Retrieve selectively; do not dump context** | Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang; 2024, **TACL**; `10.1162/tacl_a_00638` | Relevant information buried mid-long-context was used less reliably by tested LMs; varies by model/context. | Memory/retrieval; **Indirect**; compare full history vs ranked provenance snippets; measure grounded answer success and tokens. |
| P12 **Model routing should optimize cost subject to quality** | Lingjiao Chen, Matei Zaharia, James Zou; 2024, **TMLR**; DOI not listed; OpenReview `cSimKw5p6R` (Featured Certification) | FrugalGPT used cost-aware model selection with strong savings on selected NLP datasets; effects are price/model/task dependent. | Budget/model selector; **Indirect**; compare static best model with measured route-by-task on 100 tasks; paired success/latency/$ with no degradation beyond a preregistered margin. |
| P13 **Calibrate uncertainty before using confidence thresholds** | Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger; 2017, **ICML**; DOI not listed; PMLR 70:1321-1330 | Modern neural network raw scores can be miscalibrated; temperature scaling helped evaluated classifiers; not guaranteed for LLM routes. | Intent and risk scoring; **Indirect**; on labeled AGYOS intents compute ECE, Brier, selective risk and abstention rate before/after calibration. |
| P14 **Escalate meaningfully to humans** | Saleema Amershi, Dan Weld, Mihaela Vorvoreanu, Adam Fourney, et al.; 2019, **ACM CHI**; `10.1145/3290605.3300233` | 18 human-AI design guidelines assessed with practitioners across products; not a measured one-question optimality theorem. | Clarification/approval UX; **Indirect**; test consequential vs inconsequential ambiguity; measure necessary-question recall and unnecessary-question rate. |
| P15 **Memory should be retrieved and reflected on, not simply accumulated** | Joon Sung Park, Joseph O'Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein; 2023, **ACM UIST**; `10.1145/3586183.3606763` | Generative-agents architecture used observation, retrieval, reflection and planning for believable simulation; not evidence of truthful customer/company memory. | Memory design; **Indirect**; test accurate retrieval, stale-fact rejection and deletion propagation on synthetic multi-session records. |
| P16 **Reasoning narratives are not verification evidence** | Miles Turpin, Julian Michael, Ethan Perez, Samuel Bowman; 2023, **NeurIPS**; `10.52202/075280-3275` | Step-by-step explanations can omit actual decision influences, including injected bias; agent self-report must not be sole evidence. | Verification/audit trail; **Direct** to the validation principle; compare narrative-only checks with deterministic postconditions on seeded adversarial cases. |
| P17 **Policy checks at every side-effect boundary** | Hao Li, Xiaogeng Liu, Chun Chiu, Dianqi Li, Ning Zhang, Chaowei Xiao; 2025, **NeurIPS**; `10.52202/085713-2791` | DRIFT introduces plan-aware validation and injection isolation on security benchmarks; bypass risk remains; AGYOS compatibility unknown. | Policy gate + untrusted memory; **Direct** for studied attack scenarios, **Hypothesis** for AGYOS production; simulate role-scope escalation and policy-changing tool results; measure authorized success and violations. |
| P18 **SOP-encoded structured artifact handoffs** | Sirui Hong, Mingchen Zhuge, Jonathan Chen, et al.; 2024, **ICLR** (oral); DOI not listed; OpenReview `VtmBAGCN7o` | MetaGPT encodes standard operating procedures and exchanges structured documents/schemas instead of free chat, curbing cascading hallucination in simulated software companies; rigid schemas can bottleneck novel creative work. | Delegation & workflow layers; **Direct** for multi-agent pipelines, **Hypothesis** for business functions; benchmark 3-hop cross-department chains with schema handoffs vs free text; measure required-field survival (target 100%). |
| P19 **Atomic-claim decomposition and verification** | Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer, Luke Zettlemoyer, Hannaneh Hajishirzi; 2023, **EMNLP**; `10.18653/v1/2023.emnlp-main.741` | FActScore: holistic judgments miss localized hallucinations; decomposing long-form outputs into atomic claims verified individually yields reliable factual precision metrics; adds latency. | Verification harness; **Direct** for long-form factuality; decompose generated proposals/reports/summaries into atomic claims checked against ground-truth tables; require 0 unbacked numeric/contract claims. |
| P20 **LLM-modulo: pair candidate generation with external verifiers** | Subbarao Kambhampati, Karthik Valmeekam, Lin Guan, Mudit Verma, Kaya Stechly, Siddhant Bhambri, Lucas Paul Saldyt, Anil B. Murthy; 2024, **ICML**; DOI not listed; PMLR 235:22895-22907 | Position paper: autoregressive LLMs cannot alone guarantee sound multi-step planning or self-verification; LLM + external deterministic verifiers within bounded backprompting achieves sound plans; requires engineering domain-specific checkers. | Planning & verification; **Theoretical** with supporting demonstrations; pair the DAG planner with a deterministic cycle/budget/precondition verifier; require 100% rejection of cyclic, over-budget or missing-precondition plans before execution. |
| P21 **Saga compensating transactions** | Hector Garcia-Molina, Kenneth Salem; 1987, **ACM SIGMOD Record** 16(3); `10.1145/38714.38742` | Long-lived distributed executions can't hold global locks; model as sub-transactions T₁…Tₙ with compensations C₁…Cₙ₋₁ for backward recovery to a semantically consistent state. External irreversible effects cannot be compensated locally and must be deferred to a commit boundary. | Memory & recovery; **Indirect** (DB theory → agent state machines); simulate mid-workflow crashes at step k ∈ {2,3,4} across 40 workflows; require 100% state restoration via reverse-order compensation. |
| P22 **Capability-based sandboxing** | Robert N. M. Watson, Jonathan Anderson, Ben Laurie, Kris Kennaway; 2010, **19th USENIX Security Symposium**, pp. 29-45; no Crossref DOI (USENIX record) | Capsicum replaces ambient authority with explicit delegable capability descriptors, enforcing least privilege and preventing confused-deputy escalation; requires enumerating capabilities in every contract; coarse sets reintroduce ambient risk. | Policy layer; **Indirect** (OS security → agent tool sandboxing); attempt 50 unauthorized cross-domain tool invocations; require 100% hard interception by the pre-tool authorizer. |
| P23 **Design by Contract** | Bertrand Meyer; 1992, *IEEE Computer* 25(10):40-51; `10.1109/2.161279` | Explicit preconditions (caller duty), postconditions (callee guarantee) and invariants isolate fault attribution to the exact boundary where a contract breaks; contracts must stay cheap to evaluate. | Delegation & verification; **Indirect** (software engineering → sub-agent handoff); wrap every L0→L1 and L1→L2 dispatch in executable pre/post-condition assertions; on 60 injected faults require 100% exact failing-node identification, zero silent corrupt handoffs. |
| P24 **Quota admission control and priority tiers** | Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, David Oppenheimer, Eric Tune, John Wilkes; 2015, **ACM EuroSys**; `10.1145/2741948.2741964` | Borg prevents runaway tasks from starving critical operations via quota admission control, resource envelopes and preemption; over-tight quotas cause false-positive preemptions without historical sizing. | Planning & budget layers; **Indirect** (cluster OS → agent budget management); inject runaway recursive sub-agent loops and token-exhaustion tasks; require halt at 100% of node budget with a 20% verification/rollback reserve preserved. |
| P25 **Bound depth and fan-out in decentralized trees** | Roy Radner; 1993, *Econometrica* 61(5):1109-1146; `10.2307/2951495` | For boundedly rational processors aggregating information under delay costs, hierarchical trees minimize latency/coordination overhead only when fan-out and depth are tightly bounded relative to item complexity; assumes near-decomposable aggregation. | Architecture & role topology; **Theoretical**; evaluate tree depths D ∈ {1,2,3,4,5} and fan-outs F ∈ {2,4,8} on 30 composite workflows; verify D ≤ 3, F ≤ 4 minimizes tokens × latency / success rate. |
| P26 **Knowledge hierarchies; management by exception** | Luis Garicano; 2000, *Journal of Political Economy* 108(5):874-904; `10.1086/317671` | Optimal hierarchies place low-cost specialized workers at the base for routine high-frequency problems and escalate only out-of-distribution exceptions upward, trading knowledge-acquisition cost against communication cost; fails if workers can't estimate their own competence boundary. | Delegation & recovery; **Theoretical**; route 100 mixed-difficulty requests through L1/L2 with explicit exception triggers (schema mismatch, confidence threshold, policy conflict); require ≥35% token savings vs routing everything through L0 with zero success-rate drop. |
| P27 **Expected Value of Perfect Information gate** | Ronald A. Howard; 1966, *IEEE Transactions on Systems Science and Cybernetics* 2(1):22-26; `10.1109/TSSC.1966.300074` | Gathering information before acting is rational iff EV(decision with information) − EV(under prior beliefs) exceeds inquiry cost; requires calibrated priors and loss estimates across action classes. | Intent & clarification policy; **Theoretical**; on 100 prompts (70 benignly underspecified R0-R2, 30 R3-critical) require ≤5% interruption rate on benign prompts and 100% single-question interception on R3 critical ambiguity. |
| P28 **Cognitive load; context slicing** | John Sweller; 1988, *Cognitive Science* 12(2):257-285; `10.1207/s15516709cog1202_4` | Problem-solving degrades when extraneous working-memory load consumes limited capacity; structuring inputs around minimal goal-relevant state preserves accuracy; over-pruning can strip cross-domain constraints. | Memory & delegation; **Indirect** (cognitive science → context management); compare full transcripts vs dependency-scoped slices (≤2,000 tokens per worker call) across 5-step workflows; require ≥45% token reduction with ≥10% instruction-adherence improvement. |
| P29 **Bounded multi-agent cross-critique** | Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, Igor Mordatch; 2024, **ICML**; DOI not listed; PMLR 235:11733-11763 | Multi-agent debate improved factuality and reasoning in tested settings; cost scales O(N × R) and similar agents can converge on shared mistakes (majority-yield behavior documented in later work). | Verification for R3 decisions; **Direct** with limits; restrict 2-round 2-agent review to R3 external/irreversible tasks; require ≥30% reduction in policy-violating approvals at <15% total token increase. |

### 2.2 Notes on the merged catalog

- P18 (MetaGPT) was excluded from draft 2's evidence base pending verification; it is now **verified as ICLR 2024 (oral)** and is legitimately included above. Its simulated software-company setting still limits transfer: level **Direct** for the structured-handoff mechanism, **Hypothesis** for business functions.
- P19-P29 supply the systems-theoretic spine (contracts, sagas, capabilities, quotas, hierarchies, EVPI, cognitive load) that draft 1 contributed; all DOIs/pages verified 2026-11-04.

### 2.3 Quarantined unreviewed (arXiv-only) work — excluded from the evidence base

Per the strict verification constraint, popular agent papers existing solely as arXiv preprints are **marked Unreviewed and excluded from the scored evidence base** (they may still motivate design ideas):

- *AutoGen* (Wu et al., arXiv:2308.08155) — Unreviewed (arXiv-only; excluded).
- *ChatDev* (Qian et al., arXiv:2307.07924 preprint) — Unreviewed (superseded here by P18, ICLR 2024).
- *Voyager* (Wang et al., arXiv:2305.16291) — Unreviewed (excluded).
- *AgentVerse* (Chen et al., arXiv:2308.10848) — Unreviewed (excluded).
- *MemGPT* (arXiv:2310.08560) — Unreviewed (excluded).

Skill counts, FAANG analogies and "zero hallucination" claims are not scientific evidence. No cited result proves fully autonomous legal advice, safe financial execution, or end-to-end company management.

---

## 3. Ranked design priorities and sensitivity

Scoring is a **provisional decision framework**, not results from AGYOS experiments. Six dimensions scored 0-5 (5 best): reliability **25**, task success **20**, empirical evidence strength/transferability **20**, cost-efficiency **15**, safety **10**, implementation feasibility **10**. Total = (25R + 20T + 20E + 15C + 10S + 10F) / 5, range 0-100. Ties are deliberate. Scores must be revised after pilot data.

| Rank | AGYOS principle (evidence) | R/T/E/C/S/F | Base /100 | Safety-heavy¹ | Cost-heavy² |
|---:|---|---|---:|---:|---:|
| 1 | Single-agent baseline; delegate only on measured advantage (P01) | 5/4/5/5/4/5 | **94** | 92 | 95 |
| 2= | Risk-based authorization before side effects (P08, P17, P22) | 5/5/5/3/5/4 | **92** | 96 | 86 |
| 2= | Tool-observed, machine-checked completion (P09, P16, P20) | 5/5/5/3/5/4 | **92** | 96 | 86 |
| 2= | Ask only consequential clarification (P14, P27) | 5/4/4/5/5/5 | **92** | 93 | 93 |
| 2= | Management-by-exception hierarchy (P26) | 5/4/5/5/4/4 | **92** | 90 | 93 |
| 6= | Typed task and handoff contracts (P23, P04, P18, P10) | 5/5/4/4/5/4 | **91** | 93 | 89 |
| 6= | Saga rollback and recovery (P21) | 5/4/5/4/5/4 | **91** | 94 | 88 |
| 8 | End-state evals with repeated-run reliability (P09) | 5/5/5/3/4/4 | **90** | 91 | 85 |
| 9 | Bounded retries, idempotency, no replay of side effects (P06, P09) | 5/4/4/4/5/5 | **89** | 92 | 87 |
| 10 | Observation-action execution loop (P02, P10) | 4/5/5/4/4/4 | **88** | 87 | 87 |
| 11 | Quota admission control with verification reserve (P24) | 5/4/5/4/4/3 | **87** | 87 | 85 |
| 12= | Prompt-injection boundary and data isolation (P08, P17) | 5/4/5/3/5/3 | **86** | 91 | 80 |
| 12= | Selective retrieved context with provenance (P11, P28) | 4/4/5/4/4/5 | **86** | 86 | 85 |
| 14 | Cost-aware model/role routing (P12) | 4/4/4/5/4/4 | **83** | 81 | 86 |

¹ Safety-heavy weights (25,15,20,5,25,10); ² cost-heavy weights (20,20,15,30,5,10); both sum to 100.

**Sensitivity result:** the top group is broadly stable. Under safety-heavy weights, risk-based authorization and machine-checked completion rise to 96 (top); under cost-heavy weights, single-agent-first stays #1 (95) and cheap clarification and exception hierarchies rise (93). Cost routing overtakes injection isolation under cost-heavy scoring, but **minimum safety requirements remain hard constraints, not tradable score points**. Under a capability-first regime (success 35, reliability 25), bounded search (P05) and debate (P29) rise but stay opt-in only — never default. Sensitivity is a prioritization exercise, not evidence that any 94-point principle works in AGYOS.

**Adoption rule:** P01/P08/P09/P14-derived constraints are prerequisites. Add costly DAG delegation only if paired trials improve end-state success by at least **5 percentage points** or cost-per-correct-task by **20%**, without a material increase in unauthorized actions. These thresholds are proposed engineering decisions, **not published constants**. Use bootstrap confidence intervals and explicitly report inconclusive results.

---

## 4. Architecture comparison and proposed layers

### 4.1 Paradigm comparison

| Dimension | Single agent + tools | Flat peer team | Adaptive hierarchy (proposed) |
|---|---|---|---|
| Communication | O(1) internal; context grows O(T) across all 11 domains | O(N²) chatter; loops and role confusion | O(N) tree edges, bounded depth 3, fan-out 4; no horizontal chatter without mediation |
| Working memory | Severe attention dilution: 50+ tools and 11 domain instructions in one prompt | Duplicated transcripts inflate tokens 3-8× | Scoped context slicing: each node receives only its typed contract + required state keys (≤2,000 tokens) |
| Fault isolation | Total: one injection has ambient authority over all tools | Peer persuasion propagates unverified assumptions | Capability descriptors scope each worker; local Saga compensation contains blast radius |
| Escalation | Over-allocates frontier tokens to trivial tasks | Peers debate routine steps with no termination rule | Management by exception: L1/L2 absorb routine SOPs; only exceptions reach L0 |
| Verification | Self-grading bias in one context | Consensus bias on plausible hallucinations | Parent + deterministic postconditions verify child outputs before state commit |
| Best use / evaluation | Default for drafting, short answers, bounded edits; baseline all tasks | Only independently verifiable parallel retrieval or draft candidates; matched token budget | Multi-department workflows with genuine dependencies and approvals; must beat baseline empirically |

### 4.2 Seven logical layers

Not necessarily seven separate model calls.

1. **Intent** — extract goal, company area, entities, requested outcome, dependencies, success criteria, ambiguity and evidence links from unrestricted natural language; no user-supplied agent name/keyword/slash required. Unknown intents route to a general scoped planner, not arbitrary tools. Learn from observed workflow examples rather than only keywords.
2. **Policy** — deterministic policy-as-code checks every proposed tool call *and* each data retrieval: tenant, actor, resource, permission, sensitivity, external side effect, irreversible effect, approval expiry. Deny unsupported actions; never trust retrieved web/email/doc text as authority (P08). High-impact checks **fail closed** even where availability-oriented hooks fail open (§1.3.6).
3. **Planning** — direct path for one-step tasks; otherwise an acyclic typed task graph with explicit acceptance tests, risk classification and critical path. Decomposition only where useful (P04, P25).
4. **Delegation** — `agy` parent invokes native subagents via `invoke_subagent` with scoped capabilities, contracts, tiny contexts and bounded runtime; isolate code changes in branch/worktree as needed. Never grant a worker broader permissions than its parent. **Do not fake host delegation through MCP tools** (§1.3.10).
5. **Verification** — validate typed output; run deterministic postconditions on workspace/database/API; independent checker only for high-impact/low-confidence tasks; record proof hashes and uncertainty (P09, P16, P19, P20). "Looks complete" is not success.
6. **Memory** — task-local working notes, versioned episodic ledger, retrieval index for reusable records; partitioned by tenant/company and user permissions; provenance, expiration, tombstones, deduplication. Never treat stored instructions as higher-priority commands (P08, P11, P15).
7. **Recovery** — persistent checkpoints, bounded retries with changed hypothesis, idempotency keys, compensating actions; stop and escalate if state cannot be proven (P06, P21). Never silently re-send email, re-charge a card or reissue an offer.

### 4.3 Typed task contract

Every delegated unit of work carries a versioned contract (JSON Schema / TypeScript equivalent). Required fields, reconciling both drafts:

```json
{
  "task_id": "tsk_onboarding_draft_01",
  "run_id": "uuid",
  "parent_task_id": null,
  "tenant_id": "tenant",
  "requester_id": "actor",
  "depth": 0,
  "department": "customer_success",
  "objective": "Create a draft onboarding sequence",
  "assumptions": ["professional tone", "enterprise tier defaults"],
  "inputs": [{"ref": "artifact-id", "trust": "untrusted", "version": "sha"}],
  "dependencies": [],
  "allowed_actions": ["read:crm", "write:draft"],
  "forbidden_actions": ["send:external", "charge:payment"],
  "capability_allowlist": ["read:crm", "write:draft"],
  "approval": {"required": false, "scope": null, "expires_at": null},
  "acceptance": [
    {"type": "schema", "schema_id": "onboarding-draft-v1"},
    {"type": "postcondition", "check": "draft_exists_and_valid"}
  ],
  "budget": {"tokens": 12000, "usd": 0.50, "seconds": 180, "tool_calls": 20, "max_retries": 2},
  "idempotency_key": "tenant-run-task-v1",
  "risk": "reversible_write",
  "preconditions": ["state.key:crm.account.exists"],
  "postconditions": {"output_schema_ref": "onboarding-draft-v1", "verifier_cmd": "scripts/agyos-verify.sh --task", "required_claims_grounded": true},
  "compensation": {"kind": "delete_draft", "resource_ref": "draft-id", "rollback_cmd": "state.revert(snap_id)", "snapshot_id": "snap_uuid"},
  "result": {"status": "pending", "artifacts": [], "proofs": [], "uncertainty": []}
}
```

Contract rules: all outputs carry **provenance, scope, assumptions and verifiable acceptance**; do not trust "confidence" numbers until calibrated (P13). Reject cycles, out-of-scope URLs/resources, missing approvals and budget violations **before** action. Workers return results to the parent; the parent is responsible for collection and final verification (mirrors the anti-orphan intent of `.agents/rules/common-agents.md:53-61`, which currently has no enforcement).

### 4.4 Proposed initial caps and approval matrix (reconciled)

Both drafts proposed caps; the values below take the more conservative of each pair, pending measurement:

- **Hierarchy depth**: 3 levels total (L0 supervisor → L1 pod coordinator → L2 bounded worker), i.e. **max 2 delegated levels**; an L2 attempt to spawn is deterministically rejected. (Host nesting limit unconfirmed — §1.4 — this design is conservative under any plausible cap.)
- **Fan-out and concurrency**: max **4 children per DAG node** (plan-time); max **3 concurrently active workers** per run (run-time); max **8 tasks** per DAG; no recursive self-spawning by default.
- **Budgets**: default exploration envelope **30k combined tokens, $1.50, 10 minutes, 40 tool calls** per run (R0/R1 single-domain slices default to 16k tokens); **20% of the root budget is reserved** for verification, reflection repair and rollback; per-task limits inside each contract; reject tasks whose cost estimate is unknown; higher budgets need operator override. These are trial defaults, not host limits.
- **Retries**: max **2** per failed task; no identical failing retry; timeout and backoff; no automated replay of externally visible side effects; evidence of idempotency before re-execution.
- **Approval matrix by risk tier**: **R0 read-only / R1 local reversible** — autonomous within least-privilege scope, explicit assumptions, checkpoints for R1. **R2 shared internal state** (CRM updates, onboarding invitations, vendor provisioning, production deploys, external campaigns) — prepare draft and proposed diff; approval before side effect. **R3 external/financial/legal/customer-irreversible** (payments, refunds, payroll, binding offers, contract terms, hiring decisions, account deletion, destructive edits) — exact-action human confirmation (actor, beneficiary, amount/terms, expiry); staged in an outbox as `PENDING_COMMIT` until all upstream R0-R2 gates pass; specialist agent advice never substitutes for qualified legal/financial review.
- **Rollback**: prefer preimage snapshot / new draft version; compensating actions for reversible systems (LIFO, per P21); for irreversible effects record an incident and route to human escalation — never claim rollback was possible.
- **Safety invariant**: a permissions mismatch is a stop, not an agent creativity problem.

### 4.5 Suggested implementation units after approval (do not execute now)

- **Phase A — baseline and contract hardening**: fix source-of-truth counts/status, absolute hook path assumptions (`.agents/hooks.json`), native role tool schemas (`.agents/agents/faang-architect.md` declares non-existent tool names); build eval dataset and single-agent baseline. Candidate files: `scripts/tests/`, `.agents/hooks.json`, `.agents/agents/`, `mcp/state-server.cjs`. Migrate essential legacy `.agents/workflows/` procedures to auto-discovered `.agents/skills/` after host validation — **new SOPs must be skills, not workflows** (§1.4).
- **Phase B — deterministic execution core**: schema validation and policy evaluator first, then append-only execution ledger, idempotency, approval receipts, side-effect interface and recovery. Candidate new `agyos_runtime/` package (or `agyos_decision/` modules: `intent_compiler`, `planner`, `delegator`, `clarify`, `contracts.schema.json`, `budget`) with focused tests; do **not** enlarge the MCP state server into a monolith.
- **Phase C — host adapter and optional delegation**: native subagent invocation via `invoke_subagent` (not MCP); handoff schema, join/cancel, parallel limit, isolated worktree; integrate entry instructions in `AGENTS.md`/`GEMINI.md` only after verifying host startup behavior.
- **Phase D — company adapters**: dry-run CRM/helpdesk/marketing/billing/HR/legal templates with granular permissions; no live sends or spending until evaluated.
- **Phase E — canary and launch gates**: paired A/B on single vs adaptive, shadow-run on scrubbed data, explicit operator approval, staged rollout, rollback.

---

## 5. Company-wide task-derived role map

Roles are **capabilities/tasks**, not 11-20 always-running agents. Reuse a shared general planner and verifier. Merge roles when their distinct model context, tools and measurable accuracy improvement do not justify extra cost (P25, P26). The existing marketing role is only a source template (`.agents/agents/marketing-agent.md:1-45`), not proof of an operational marketing department.

| Company function (example plain-language request) | Typed outputs and tools | Merged pod / owner | Boundary and measurable success |
|---|---|---|---|
| Marketing — "plan our launch" | audience evidence, approved positioning, content draft, experiments | **POD_GROWTH** (marketing + lead gain + sales) — `.agents/agents/pod-growth.md` | No invented testimonials; approval before publishing; sourced-claim rate, conversion uplift |
| Lead generation — "find potential customers" | deduped leads with lawful source/consent metadata, CRM draft | **POD_GROWTH** | No bulk unsolicited sends or protected-data scraping; precision, duplicate rate, lawful provenance |
| Sales — "prepare an offer" | opportunity stage, proposal, priced quote draft, next step | **POD_GROWTH**; pricing reviewer on high-value deals; non-standard terms escalate to POD_GNA | No binding promise/discount without approval; quote correctness, CRM end-state, win rate |
| Onboarding — "welcome this client" | checklist, account provision plan, training and email drafts | **POD_CUSTOMER** (onboarding + support) — `.agents/agents/pod-customer.md` | No invites/access creation without approval; setup completeness, time-to-value |
| Support — "resolve this ticket" | diagnosis, policy-correct reply, ticket state proposal | **POD_CUSTOMER**; escalation specialist for high risk; reproducible defects escalate to POD_BUILD via typed bug contract | Refund/account changes require approval; pass³, resolution rate, policy adherence |
| Product — "prioritize feedback" | opportunity tree, PRD, acceptance criteria, experiment | **POD_BUILD** (product + engineering) — `.agents/agents/pod-build.md` | Grounded user evidence, feasible spec, no fake research; measured outcome learning |
| Engineering — "fix checkout bug" | issue reproduction, PR patch, tests, rollback plan | **POD_BUILD**; L2 separation between `worker-coder` and `worker-verifier` | Tests, security and side-effect gates; verified regression pass, deployment incidents |
| Finance — "reconcile invoices" | reconciled records, variance report, payment proposal | **POD_GNA** (finance + legal + ops) — `.agents/agents/pod-gna.md` | No bank mutation/payment without exact approval; reconciliation accuracy, auditability |
| Legal/compliance — "review these terms" | issue list, risk flags, draft amendments, citations | **POD_GNA**; human counsel escalation | Advisory only; no legal clearance claims, no accepting terms; flagged issues verified |
| Operations/procurement — "prepare vendor order" | vendor comparison, inventory plan, PO draft | **POD_GNA** | External purchases blocked until approved; cost and delivery accuracy |
| Hiring/people — "screen applicants" | job rubric, interview packet, schedule draft | **POD_PEOPLE** (hiring) — `.agents/agents/pod-people.md` | Human hiring decisions; privacy/fairness review; rubric consistency, no automated rejection |
| Cross-functional — "launch new product and sell it" | shared DAG: PRD → engineering → launch → leads → sales → onboarding → support, with finance/legal approvals | One **Coordinator** supervising only the pods required by the DAG | Measured end-state across domains, joined workers, explicit approvals, no autonomous company commitments |

**Topology:** 1 L0 Coordinator (intent/planning) + 5 merged L1 pods (GROWTH, CUSTOMER, BUILD, GNA, PEOPLE) + ephemeral L2 workers only for parallelizable leaf tasks or adversarial verification. This covers all 11 requested company functions while reducing potential inter-role coordination edges from C(11,2) = 55 to 5 managed tree branches. **Minimum standing runtime roles:** Coordinator, Policy Guard (deterministic, not an LLM), Executor/Tool Adapter (deterministic), Verifier, Memory/Ledger. Only **one task agent** is initially active; functional expertise can be a runbook within the same agent. Spawn separate pod agents **only** when supported by host schemas and measured benchmark gains — no ceremonial management layers.

---

## 6. Clarification policy — one-question EVPI gate

Ask **one short, concrete question** (target <25 words, with a recommended default) only when different answers would materially change **correctness, safety, authorization or an irreversible action**. Otherwise use the safest reversible assumption, state it briefly and proceed.

**Decision function** (P27, P14):

1. Can a correct **read-only or draft** result be produced under an explicit assumption? If yes, do so without asking.
2. Would different interpretations change who/what is affected, money, an external send, access grants, compliance, data deletion, the correctness of a binding deliverable, or materially unsafe behavior? If yes, ask **one highest-information-gain question**, then wait; unanswered = draft/stop, not implied approval.
3. If uncertainty concerns an independent low-risk detail, choose a visible reversible default and include it in acceptance notes.
4. A question is **not** permission to skip deterministic policy checks; even clear intent may need approval for high-impact side effects.

| Scenario class | Risk tier | Critical ambiguity? | Action |
|---|---|---|---|
| Routine content, research, code, internal draft | R0/R1 | No | **Proceed immediately** with explicit assumptions header |
| Internal state update with reversible snapshot | R2 | No | **Proceed immediately**; snapshot ID logged |
| Missing hard numerical/legal/architectural invariant | R1-R3 | Yes — two incompatible outcomes | **Ask exactly 1 question** |
| Irreversible external side effect or destructive action | R3 | Yes — unconfirmed recipient/transfer/purge | **Stage in outbox** + ask 1 confirmation question with exact diff |

**Mandatory assumption header** when proceeding without asking (recorded in `TaskContract.assumptions` and prepended to the user-facing reply):

```markdown
> **Assumptions Applied:** (1) [default]; (2) [default]. *(Reply to override; snapshot `snap_<id>` makes this reversible.)*
```

Examples: "Write a welcome email" → draft, no question. "Send the welcome email to every lead" → ask which approved, consented list; do not send. "Refund the client" → ask which transaction and exact amount to prepare for approval; do not issue. "Fix a typo in this file" → bounded change with verification, no interview. "Sign the supplier contract" → prepare risks/draft; do not sign; require explicit human authorization.

---

## 7. Evaluation plan, acceptance gates and approval boundary

**Frozen fixture suite:** at least **120 cases** — 10+ in each of the 11 functions plus cross-functional flows, plus 30 adversarial policy/permission cases, 20 ambiguous natural-language paraphrases, 20 injected untrusted-document cases, 15 retry/idempotency cases, 15 memory/retention cases. Each scenario has a unique ID, typed pre-state, expected post-state, permitted calls, failure conditions and cost ceilings. Use synthetic or scrubbed records, never live credentials.

**Experiment:** randomize case order; pair identical fixture/host/model budgets across **single agent**, **flat parallel** and **adaptive hierarchy**; repeat each case ≥3 times; preserve raw outcomes; compare with bootstrap confidence intervals. Report pass¹, pass³ (all 3 succeed), forbidden-action rate, false-approval rate, extra-question rate, agent/tool count, p50/p95 duration, tokens, actual cost and cost per success. Segment by function, sensitivity and dependency degree. Publish negative results.

**Go/no-go (proposed, not proven):**

- **Zero** unauthorized irreversible actions or cross-tenant leakage in pre-launch red-team tests; any occurrence blocks launch.
- Correct post-state **≥95%** on read-only/draft cases, **≥90%** on reversible-write cases; 3-run reliability and uncertainty intervals reported.
- Clarification: **≥98% recall** on consequential-ambiguity fixtures; **≤10%** unnecessary questions on safe-default fixtures.
- Recovery: repeated side effects **0**; no task exceeds declared budget/agent count; orphaned workers **0**.
- Hierarchy ships only in slices with demonstrated paired advantage (§3); otherwise fall back to single agent. No cost/speed metric overrides a failed security threshold.
- Fresh test evidence required on target Ubuntu + pinned `agy` version; record git SHA, config, environment, logs, baseline and regression deltas. Historical counts (33/33, 34/34, 36/36 — §1.3.1) are claims, not evidence.

**Falsifiers:** hierarchy increases error amplification or cost at similar success → disable delegation for that slice; confidence routing remains uncalibrated → simple rules + abstain; hooks can bypass authorization → deny side effects at the adapter; memory retrieval uses stale/wrong-tenant facts → disable memory writes/retrieval until repaired; tasks require live actions with no permissions/integrations → deliver drafts rather than claim execution.

**Decision gates:** **Gate 0 (now)** — approve/reject this plan; the only authorized deliverable is this file on a research branch. **Gate 1** — pin `agy` version, record real machine baseline, audit agent frontmatter tool names/hooks/counts, write failing tests for known gaps. **Gate 2** — policy + contracts before delegation; end-state fixtures and budgets; single-agent default. **Gate 3** — optional native subagent delegation, constrained run ledger, recovery. **Gate 4** — company adapters one function at a time behind dry-run/approval; cross-functional experiments. **Gate 5** — independent threat review, economic study, staged release; freeze if safety prerequisites fail.

---

## 8. Final prompt for `agy` — use ONLY after approving the plan

```text
Read docs/RESEARCH_PLAN.md, README.md, AGENTS.md, GEMINI.md, TRACKER.md,
docs/ARCHITECTURE.md, .agents/agents/, .agents/rules/, .agents/skills/,
.agents/hooks.json, .agents/state/, agyos_decision/, mcp/state-server.cjs,
scripts/hooks/, scripts/agyos-verify.sh and tests. Confirm the actual agy
version and the official host tool, hook, subagent and skill contracts; treat
old pass counts (33/33, 34/34, 36/36) as claims, not evidence.

Implement the approved plan in small testable phases, starting with a
single-agent baseline, frozen business task fixtures and failing tests.

1. CONTRACTS & INTENT (agyos_decision/): create contracts.schema.json
   enforcing typed TaskContracts (task_id, parent, depth<=2, pod, risk tier
   R0-R3, assumptions, pre/postconditions, capability allowlist, budget,
   compensation). Implement intent compilation and EVPI clarification that
   route plain natural language across all 11 company functions (marketing,
   lead gain, sales, onboarding, support, product, engineering, finance,
   legal, ops, hiring) into the 5 merged pods (pod-growth, pod-customer,
   pod-build, pod-gna, pod-people) with zero slash commands, keywords or
   agent names. Ask at most ONE short question only when ambiguity changes
   correctness, safety or an irreversible action; otherwise record
   assumptions and proceed.

2. STATE, BUDGETS & RECOVERY: enforce hierarchy caps (3 levels, <=4 children
   per node, <=3 concurrent workers, <=8 DAG tasks, <=2 retries) and a run
   budget of 30k tokens/$1.50/10min/40 tool calls with 20% reserved for
   verification and rollback. Add transactional snapshots, an R3 outbox
   hold queue, reflection memory and LIFO Saga compensation. Keep the MCP
   state server a state store; never fake host delegation through MCP.

3. HOST ADAPTER & PODS: create the 5 pod definitions in .agents/agents/
   with valid host tool names and invoke_subagent-based delegation; express
   SOPs as .agents/skills/ (legacy .agents/workflows/ ceased host indexing
   on 2026-10-19). Wire hooks for capability allowlists, pre-write
   snapshots and R3 blocking; add a fail-closed authorizer for high-impact
   actions alongside the existing fail-open hook.

4. VERIFICATION: extend scripts/agyos-verify.sh and tests to validate
   contract schemas, DAG acyclicity, budget invariants, atomic-claim
   grounding and rollback restoration; run single/flat/adaptive A/B
   comparisons on identical fixtures, reporting pass^1/pass^3, forbidden
   actions, false approvals, cost and latency with confidence intervals.

5. SYNC DOCS: update docs/ARCHITECTURE.md and TRACKER.md with exact file
   paths, real test commands, outputs, failures, token/cost metrics and
   commit SHAs. Never invent capability, performance, paper results or
   test passes. Stop after each milestone for operator review; never
   perform live external actions without explicit, scoped approval.
```

---

**Review conclusion:** the most credible design is a **single-agent-first, policy-gated adaptive task hierarchy**, because peer-reviewed evidence supports tool grounding, machine-checked end-state verification, trust boundaries, contracts, rollback and conditional collaboration — but does **not** prove that a large standing agent workforce is optimal for AGYOS. Implementation remains unapproved until you approve this plan.
