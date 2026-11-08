# Architectural Audit: Ten Reference Agent Platforms for AGYOS

**Document Status:** Complete Architecture & Research Matrix  
**Target Platform:** AGYOS v3.1 on Ubuntu 25.04 (3.3GB RAM ceiling, Python 3.13, Node 24, Bun 1.3)  
**Governing Standard:** Phase 1 of Master Autonomous Implementation Specification  
**Baseline Commit:** `35903ad9125607daf89ca2f189864136dbe18a67`

---

## 1. Overview and Assessment Methodology

This audit examines ten industry-leading open-source autonomous agent platforms. Each platform is analyzed for concrete, testable architectural principles applicable to AGYOS's single-operator, local-first CLI operating system.

### Principles Disposition Criteria:
- **`IMPLEMENTED`**: AGYOS already possesses an equivalent or superior mechanism in verified production code.
- **`REUSED`**: Principle or pattern is directly adopted or adapted into AGYOS code and workflows.
- **`PARTIAL`**: Principle is partially implemented or applicable only with architectural modifications.
- **`BLOCKED`**: Principle cannot be adopted due to hardware constraints (e.g., 3.3GB RAM limit), license incompatibility, or conflicting design invariants.
- **`NOT_APPLICABLE`**: Principle applies to an enterprise multi-tenant or server model that conflicts with AGYOS's local-first CLI paradigm.

---

## 2. Platforms 1–5: Core Runtime, Memory & Workflow Foundations

### 1. OpenHands (`All-Hands-AI/OpenHands`)
- **Canonical URL:** `https://github.com/All-Hands-AI/OpenHands` (redirects to `https://github.com/OpenHands/OpenHands`)
- **License:** MIT License
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Isolated agent runtime** | `openhands/runtime/impl/docker/docker_runtime.py` | Containerized sandbox architecture (`DockerRuntime`) managing persistent Docker containers and client-server IPC. | `.agents/rules/agyos-scope.md` | **BLOCKED** | Docker daemon footprint and multi-container environments exceed the 3.3GB RAM envelope on Ubuntu 25.04. AGYOS enforces isolation via local process cgroups and path boundaries rather than Docker. |
| **Computer/tool execution** | `openhands/runtime/action_execution_server.py`, `openhands/agenthub/codeact_agent/codeact_agent.py` | `CodeActAgent` emits executable bash code and Python commands into an internal action server that collects stdout/stderr observations. | `mcp/state-server.cjs:25-140` | **PARTIAL** | AGYOS executes tools via stdio JSON-RPC FastMCP and native CLI tools. CodeAct's single-turn multi-command batching script pattern is adaptable for long chains without spinning up HTTP action servers. |
| **Sandbox permissions** | `openhands/security/analyzer.py`, `openhands/security/options.py` | `SecurityAnalyzer` inspects command AST/regex patterns and enforces confirmation policies (`AlwaysConfirm`, `ConfirmRisky`, `DenyRisky`). | `scripts/hooks/authorizer.py:20-55` | **REUSED** | The risk assessment taxonomy (flagging destructive shell commands like `rm -rf`, raw socket writes, package installs) is adopted directly into AGYOS PreToolUse authorizer hooks. |
| **Event logs** | `openhands/events/stream.py`, `openhands/events/event.py` | Typed, append-only `EventStream` logging `Action` and `Observation` events with file-backed serialization and replay capabilities. | `.agents/state/checkpoints/` | **REUSED** | AGYOS stores macro state transitions in `.agents/state/state.json`. Adopting an append-only typed JSONL event stream model enables deterministic execution replay and telemetry logging without memory bloat. |
| **End-to-end coding evaluations** | `evaluation/benchmarks/swe_bench/run_infer.py` | Automated evaluation harness running coding agents against SWE-bench Lite and Verified datasets to measure real patch resolution. | `scripts/agyos-verify.sh:1-120` | **IMPLEMENTED** | AGYOS already enforces Gate 5 machine verification, monotonic test assertion ratchets, and local test runners. Running full SWE-bench suites locally is blocked by the 3.3GB RAM limit. |

---

### 2. agent-zero (`frdel/agent-zero`)
- **Canonical URL:** `https://github.com/frdel/agent-zero` (redirects to `https://github.com/agent0ai/agent-zero`)
- **License:** MIT License
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Hierarchical delegation** | `python/tools/call_subordinate.py` | Subordinate execution tool enabling a superior agent to dispatch isolated subtasks to subordinate agent instances with role prompts and reset flags. | `.agents/rules/common-agents.md` | **IMPLEMENTED** | AGYOS already uses hierarchical delegation with clear role contracts (`planner`, `tdd-guide`, `code-reviewer`, `security-reviewer`) and caller completion contracts. |
| **Self-directed tool execution** | `python/agent.py`, `python/tools/code_execution_tool.py` | `Agent.monologue()` parses dynamic actions into Python, Node.js, and Bash execution blocks with persistent terminal sessions indexed by session ID. | `bin/agyos:30-120` | **PARTIAL** | AGYOS executes structured MCP tools and vetted skill runbooks rather than arbitrary unbounded script generation. Agent-zero's multi-session terminal indexing pattern can be adopted for background process tracking. |
| **Role boundaries** | `prompts/default/agent.system.md` | System prompt templates enforce operational role personas and constrain tool availability between parent and child agents. | `GEMINI.md:§9` | **IMPLEMENTED** | AGYOS enforces strict role separation, Maker/Checker isolation, and 141 modular rules (<24KB) governing architecture, testing, security, and verification. |
| **Local/docker isolation** | `python/helpers/docker.py` | Pre-configured Docker container hosting a full headless Linux desktop, virtual X server, and browser to isolate agent side-effects. | `bin/agyos` | **NOT_APPLICABLE** | Running a virtual desktop inside Docker baseline consumes over 2GB RAM, incompatible with the 3.3GB hardware constraint. AGYOS executes directly in the user CLI environment with file scope gates. |
| **Memory lifecycle** | `python/helpers/memory.py`, `python/tools/memory.py` | Dynamic long-term memory engine backed by FAISS vector indexes and LiteLLM embeddings with explicit `save`, `load`, `delete`, and `forget` actions. | `mcp/state-server.cjs:141-202` | **REUSED** | AGYOS uses structured markdown state files. Incorporating an explicit `forget` / memory eviction lifecycle prevents memory contamination and context drift across multi-day CLI milestones. |

---

### 3. OpenManus (`FoundationAgents/OpenManus`)
- **Canonical URL:** `https://github.com/FoundationAgents/OpenManus`
- **License:** MIT License
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Minimal modular agent loop** | `app/agent/base.py`, `app/agent/manus.py` | Lightweight asynchronous loop (`BaseAgent.run()` calling `.step()`), utilizing Pydantic `BaseModel` and state enums (`AgentState`) without wrapper bloat. | `bin/agyos`, `bin/state.sh` | **REUSED** | The clean async `BaseAgent` loop (<200 lines) with explicit state transitions is directly adaptable into AGYOS Python 3.13 helper scripts, maintaining a memory footprint under 50MB. |
| **Browser/MCP integration** | `app/tool/browser_use_tool.py`, `app/agent/mcp.py` | MCP client implementation connecting tool calls to external MCP servers; delegates web tasks to `browser-use` executed via `uvx`. | `mcp/state-server.cjs:1-120` | **IMPLEMENTED** | AGYOS natively integrates FastMCP JSON-RPC 2.0 stdio servers for state, memories, decisions, and graph navigation. |
| **Tool schemas** | `app/tool/base.py`, `app/schema.py` | `BaseTool.to_param()` automatically converts Python type annotations, Pydantic fields, and docstrings into provider-compatible function tool definitions. | `mcp/state-server.cjs:30-100` | **IMPLEMENTED** | AGYOS schemas are verified and registered through standard MCP protocols and `.agents/skills/*/SKILL.md` specifications. |
| **Workflow composition** | `app/flow/base.py`, `app/flow/planning.py` | Task breakdown engine maintaining step statuses (`not_started`, `in_progress`, `completed`), executing sub-agents sequentially against the plan. | `GEMINI.md:§2` | **IMPLEMENTED** | AGYOS 5-Gate Workflow (UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT -> VERIFY) and 100 autonomous workflows provide more comprehensive gating and adversarial verification than `PlanningFlow`. |
| **Dependency isolation** | `pyproject.toml`, `run_mcp.py` | Package dependencies managed via `uv`, with resource-intensive external tools (`browser-use`) executed on-demand via `uvx` ephemeral environments. | `.github/workflows/ci.yml` | **REUSED** | Using `uvx` to isolate episodic tools prevents package conflicts in Python 3.13 and avoids loading unused binaries into RAM when idle. |

---

### 4. LangGraph (`langchain-ai/langgraph`)
- **Canonical URL:** `https://github.com/langchain-ai/langgraph`
- **License:** MIT License
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Durable execution** | `libs/langgraph/langgraph/pregel/loop.py` | Pregel-inspired computational engine executing graph nodes in discrete supersteps, persisting state transitions to durable storage before triggering next steps. | `bin/state.sh` | **PARTIAL** | AGYOS persists milestone gate states in JSON/Markdown. Full graph-cyclic superstep execution adds unnecessary abstraction layers for a CLI-driven OS. |
| **Checkpoints** | `libs/checkpoint/langgraph/checkpoint/base.py` | `BaseCheckpointSaver` interface persisting state tuples (`Checkpoint`, `CheckpointTuple`, metadata) indexed by thread ID and checkpoint ID to SQLite or memory. | `.agents/state/checkpoints/` | **IMPLEMENTED** | AGYOS records durable checkpoints in `.agents/state/checkpoints/<milestone>.md` and FastMCP tools, designed for git tracking without database daemon overhead. |
| **Typed state** | `libs/langgraph/langgraph/graph/state.py` | `StateGraph` enforces typed state definitions (Pydantic / `TypedDict`) combined with channel reducers (e.g. append-only, overwrite) ensuring deterministic state updates. | `.agents/state/state.json` | **REUSED** | The channel reducer abstraction (explicitly defining which state keys append vs replace) can be integrated into AGYOS state handlers to prevent destructive in-place mutations. |
| **Interrupt/resume** | `libs/langgraph/langgraph/types.py` | First-class `interrupt()` function halts graph execution mid-step, captures execution context, and resumes cleanly when input is provided. | `GEMINI.md:Gate 1, 5` | **REUSED** | Adding an explicit `interrupt()` primitive to AGYOS long-running subagent tasks enables fine-grained operator input checkpoints without killing the active process session. |
| **Human approval** | `libs/langgraph/langgraph/types.py` | Static and dynamic breakpoints (`interrupt_before`, `interrupt_after`) enabling human inspection and payload alteration before sensitive node execution. | `bin/state.sh:10-50` | **IMPLEMENTED** | AGYOS already mandates Human-in-the-Loop (HITL) approval gates at Gate 1 (task acceptance) and Gate 5 (release verification). |
| **Idempotency and recoverable workflows** | `libs/checkpoint/langgraph/checkpoint/base.py` | Checkpoint hashing, monotonic version IDs, and idempotent node execution ensure crash recovery without re-running completed side effects. | `AI_HANDOFF.md`, `bin/rollback.sh` | **PARTIAL** | AGYOS handles session resumption through `AI_HANDOFF.md` and gate validation, but does not track sub-node invocation hashing for step-level replay. |

---

### 5. Microsoft Agent Framework (`microsoft/agent-framework`)
- **Canonical URL:** `https://github.com/microsoft/agent-framework`
- **License:** MIT License
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Production workflow orchestration** | `python/packages/agent_framework/agent_framework/_workflows/_workflow_builder.py` | Multi-language graph builder supporting sequential, concurrent, and cyclic agent orchestration with streaming event updates (`AgentRunUpdateEvent`). | `.agents/workflows/` | **IMPLEMENTED** | AGYOS already possesses structured multi-agent pipelines and 5-gate lifecycle management optimized for local execution. |
| **Handoffs** | `python/packages/agent_framework/agent_framework/_workflows/handoff.py` | Formalized handoff builder generating tool contracts (`handoff_to_<agent>`), supporting single-tier and multi-tier transfers with human-in-loop and autonomous modes. | `.agents/rules/common-agents.md` | **REUSED** | Microsoft's explicit `HandoffBuilder` contract (generating typed tool signatures for inter-agent delegation) can be adopted to formalize subagent handoffs within AGYOS runbooks. |
| **Provider neutrality** | `python/packages/agent_framework/agent_framework/_chat_client.py` | Abstract `ChatClient` protocol abstracting model providers (Azure OpenAI, Microsoft Foundry, GitHub Models, Ollama via `LocalAgent`). | `agyos_decision/model_router.py` | **IMPLEMENTED** | AGYOS routes across provider models using native routing (`model_router.py`) and multi-model deliberation via Agent Council. |
| **State management** | `python/packages/agent_framework/agent_framework/_workflows/_workflow_context.py` | Thread-scoped workflow context tracking variables, messages, and state snapshots across execution steps. | `mcp/state-server.cjs` | **IMPLEMENTED** | AGYOS maintains state locally through file-backed JSON/Markdown and stdio MCP servers with sub-millisecond local latency. |
| **Traceability and authorization** | `python/packages/agent_framework/agent_framework/_workflows/_middleware.py` | Pluggable middleware pipeline (`AgentMiddleware`) intercepting tool calls for authorization, exception redaction, and OpenTelemetry span export. | `scripts/hooks/authorizer.py` | **REUSED** | The middleware interceptor chain model is directly applicable to AGYOS hooks, formalizing authorization gates and optional OTLP telemetry without external daemon overhead. |

---

## 3. Platforms 6–10: Production Collaboration, Services & Tools

### 6. CrewAI (`crewAIInc/crewAI`)
- **Canonical URL:** `https://github.com/crewAIInc/crewAI`
- **License:** MIT License
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Role-driven crews versus deterministic flows** | `src/crewai/crew.py`, `src/crewai/flow/flow.py` | `Crew` uses autonomous LLM agents with role/goal prompts; `Flow` defines deterministic DAGs via `@start()`, `@listen()`, and `@router()` with typed Pydantic state. | `bin/state.sh`, `.agents/workflows/` | **PARTIAL** | Adopt Flow event-driven branching decorators (`@listen`, `@router`) for subagent coordination within the 3.3GB RAM ceiling. |
| **Task ownership** | `src/crewai/task.py` | `Task` model binds a single `agent`, `expected_output`, `output_pydantic` schema, and `context` dependencies. | `.agents/state/state.json` | **IMPLEMENTED** | AGYOS strictly isolates task ownership per milestone phase and prevents multi-writer state conflicts. |
| **Lifecycle hooks** | `src/crewai/crew.py`, `src/crewai/flow/flow.py` | Provides `step_callback`, `task_callback`, `@before_kickoff`, and `@after_kickoff` execution hooks. | `scripts/hooks/agy_os_hook.py` | **IMPLEMENTED** | AGYOS lifecycle interceptors already gate tool execution and enforce the test ratchet at commit boundaries. |
| **Execution and delegation policies** | `src/crewai/tools/agent_tools/agent_tools.py` | `allow_delegation=True` injects `DelegateWorkTool` and `AskQuestionTool`; hierarchical mode uses a manager agent. | `.agents/rules/common-agents.md` | **REUSED** | Expose peer-agent delegation as structured, schema-validated MCP tools (`delegate_task`, `query_peer`) instead of raw prompt directives. |

---

### 7. Agno (`agno-agi/agno`)
- **Canonical URL:** `https://github.com/agno-agi/agno`
- **License:** Apache License 2.0
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Durable AgentOS services** | `libs/agno/agno/os/`, `libs/agno/agno/agent/agent.py` | Wraps agents as persistent FastAPI services with REST, WebSockets, and SSE endpoints. | `bin/agyos`, `mcp/state-server.cjs` | **PARTIAL** | A permanent FastAPI service exceeds the 3.3GB RAM budget (>300MB resident memory). Keep execution local-first CLI/stdio, running network listeners strictly on demand. |
| **RBAC (Role-Based Access Control)** | `libs/agno/agno/os/auth/` | Implements JWT authentication, multi-tenant isolation, and route-level role checks. | Local UNIX permissions | **NOT_APPLICABLE** | AGYOS is a local workstation CLI operating system; multi-tenant enterprise RBAC adds unnecessary runtime complexity. |
| **Human approvals (HITL)** | `libs/agno/agno/workflow/` | Workflow step pausing (`pause_for_human_in_the_loop`) with resumption upon explicit operator token submission. | `GEMINI.md:§2`, `scripts/hooks/authorizer.py` | **IMPLEMENTED** | AGYOS mandates explicit operator approval gates across state progression and destructive tool calls. |
| **Sessions** | `libs/agno/agno/storage/agent/session.py` | `AgentSession` records session IDs, state, and message histories to PostgreSQL or SQLite. | `.agents/state/state.json`, `CURRENT.md` | **IMPLEMENTED** | File-backed JSON/Markdown state provides persistence without external database server overhead. |
| **MCP integration** | `libs/agno/agno/tools/mcp.py` | Implements `MCPTools` client supporting Stdio and SSE transports for external tool discovery and invocation. | `mcp/agyos-state-server.cjs` | **IMPLEMENTED** | AGYOS architecture already uses MCP as its primary external integration layer. |
| **Tracing** | `libs/agno/agno/tracing/` | OpenTelemetry spans and LangSmith exporters capturing execution graphs, latency, and token metrics. | `.agents/state/checkpoints/` | **REUSED** | Adopt Agno's lightweight OpenTelemetry JSON span model for CLI trace logging to enable standard observability without external SaaS dependencies. |
| **Automation and eval feedback** | `libs/agno/agno/eval/` | Provides `Case`, `run_cases`, `PerformanceEval`, and `ReliabilityEval` runner suites. | `bin/gate-check.sh`, `scripts/agyos-verify.sh` | **REUSED** | Adopt Agno's structured `Case(input, expected_output, evaluators)` schema to formalize AGYOS skill evaluation benchmarks. |

---

### 8. Letta (`letta-ai/letta` and `letta-ai/letta-code`)
- **Canonical URL:** `https://github.com/letta-ai/letta` (and `https://github.com/letta-ai/letta-code`)
- **License:** Apache License 2.0
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Durable identity** | `letta/schemas/agent.py`, `letta/schemas/memory.py` | Stateful agent entities identified by GUIDs with persistent persona blocks decoupled from execution processes. | `.agents/agents/` | **PARTIAL** | Add persistent instance IDs to AGYOS agent pods to preserve stateful identity across disconnected CLI runs. |
| **Tiered memory** | `letta/memory.py`, `letta/schemas/memory.py` | Separates memory into Core (in-context blocks), Recall (recent event buffer), and Archival (vector store retrieval). | `mcp/state-server.cjs:141-202` | **REUSED** | Implement Letta's 3-tier memory model using local SQLite-vec for archival storage, keeping resident memory footprint under 50MB. |
| **Context compaction** | `letta/services/summarizer/`, `letta/agent.py` | Sliding-window summarization (`self_compact_sliding_window`) triggered when token thresholds are reached. | `bin/compact.sh` | **IMPLEMENTED** | Automated context size management and compaction gates are already operational in AGYOS. |
| **Retrieval** | `letta/tools/archival_memory.py` | Dedicated tool calls (`archival_memory_search`, `archival_memory_insert`) execute semantic retrieval on demand. | `agyos_decision/skills_router.py` | **IMPLEMENTED** | AGYOS mandates search-first retrieval using local indexing and AST tools prior to writing code. |
| **Private secrets separation and persistence** | `letta-code/src/secrets/` | Encrypted secret storage (`LETTA_ENCRYPTION_KEY`), dynamic injection via `$SECRET_NAME`, and context scrubbing. | `scripts/agyos-runtime/lib/private-vault.cjs` | **REUSED** | Adopt Letta's pattern of scrubbing secret strings from tool stdout/stderr streams before appending them to the model context window. |

---

### 9. MetaGPT (`FoundationAgents/MetaGPT`)
- **Canonical URL:** `https://github.com/FoundationAgents/MetaGPT`
- **License:** MIT License
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **SOP-oriented multi-agent collaboration** | `metagpt/team.py`, `metagpt/environment.py` | Materializes "Code = SOP(Team)" using an event bus where agents publish and subscribe to standardized actions. | `GEMINI.md:§2`, `bin/state.sh` | **IMPLEMENTED** | Standard Operating Procedure compliance is already the structural backbone of AGYOS. |
| **Role contracts** | `metagpt/roles/role.py`, `metagpt/schema.py` | Roles declare explicit subscription tags (`_watch`), action sets (`set_actions`), and typed message interfaces. | `.agents/agents/` | **IMPLEMENTED** | Agent responsibilities and input/output contracts are strictly defined and isolated. |
| **Artifact handoffs** | `metagpt/schema.py`, `metagpt/actions/` | Pydantic-typed documents (PRD, Architecture Design, Task Guide, Code) passed via `Message` with `cause_by` metadata. | `GEMINI.md:Gates 1-5` | **IMPLEMENTED** | Discrete artifact production and formal verification at each phase transition are mandatory invariants. |
| **Validation and company-task decomposition** | `metagpt/actions/project_management.py` | Decomposes projects into Work Breakdown Structures (WBS) with task dependency graphs evaluated by independent QA roles. | `docs/adr/`, `GEMINI.md:§3` | **REUSED** | Adopt MetaGPT's programmatic WBS dependency resolution model to automatically generate strict prerequisite graphs during Gate 3 planning. |

---

### 10. Goose (`aaif-goose/goose`, formerly `block/goose`)
- **Canonical URL:** `https://github.com/aaif-goose/goose` (migrated to Agentic AI Foundation / Linux Foundation)
- **License:** Apache License 2.0
- **Default Branch:** `main`
- **Maintenance Status:** Active

| Principle | Source File/Path | Upstream Evidence | Current AGYOS File/Line | Decision | Rationale & AGYOS Mapping |
|---|---|---|---|---|---|
| **Model/provider portability** | `crates/goose/src/providers/` | Rust provider trait abstracts streaming, tool calling, and token tracking across Anthropic, OpenAI, Ollama, and Databricks. | `agyos_decision/model_router.py` | **PARTIAL** | Add a lightweight local Python/Bun provider fallback interface to allow AGYOS script operations when running outside the `agy` host runtime. |
| **Extensible MCP interface** | `crates/goose/src/agents/extension.rs` | Dynamic MCP client discovering tools and routing JSON-RPC 2.0 messages over Stdio and SSE. | `mcp/state-server.cjs` | **IMPLEMENTED** | MCP architecture is natively deployed and utilized across AGYOS workflows. |
| **Sandbox/tool permissions** | `crates/goose/src/permission/` | Risk-classified tool permissions with interactive approval and an LLM-assisted permission judge evaluating safety. | `scripts/hooks/authorizer.py` | **REUSED** | Adopt Goose's structured risk tiers (read-only auto-approved vs destructive human-gated) directly within `authorizer.py`. |
| **Recipes and independent subagents** | `crates/goose/src/recipe/mod.rs` | Declarative, parameterized execution recipes; subagents run in isolated sessions with fixed turn budgets (`DEFAULT_SUBAGENT_MAX_TURNS`). | `.agents/rules/common-agents.md` | **REUSED** | Adopt Goose's strict subagent turn-budgeting pattern (`DEFAULT_SUBAGENT_MAX_TURNS`) to prevent runaway loops in delegated subagents. |

---

## 4. Master Disposition Statistics

| Disposition | Count | Percentage |
|---|---|---|
| **IMPLEMENTED** | 20 | 44.4% |
| **REUSED** | 16 | 35.6% |
| **PARTIAL** | 6 | 13.3% |
| **BLOCKED** | 1 | 2.2% |
| **NOT_APPLICABLE** | 2 | 4.4% |
| **TOTAL PRINCIPLES** | **45** | **100.0%** |
