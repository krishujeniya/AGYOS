---
trigger: always_on
---
# AGYOS OpenDots Coworker Architecture Standard

This standard incorporates the structural logics, design principles, and operational rules of CopilotKit OpenDots into AGYOS. It governs how autonomous agents, background workers, and project memory interact without introducing foreign dependencies or application code.

---

## 1. The Coworker ("Dot") Paradigm vs Transient Chatbots

Traditional agent frameworks treat AI as a transient request-and-response chatbot that terminates when a turn ends. The OpenDots architecture replaces this with persistent, always-on digital coworkers ("Dots"):

1. **Role and Domain Scoping**: Every Dot is instantiated with a defined operational scope, specific tools, and bounded responsibilities (e.g. Code Reviewer, Security Auditor, Research Specialist).
2. **Persistent State and Durable Memory**: A Dot retains its operational context across multiple sessions, reconciling previous checkpoints and task logs rather than starting from scratch.
3. **Autonomous Task Continuity**: Dots execute multi-step workflows asynchronously, reporting back upon completion rather than requiring step-by-step human babysitting.

---

## 2. Spaces and Pages Document Workspace Architecture

In the OpenDots pattern, agent deliverables must never be buried in transient chat logs. Work products are structured into living workspaces:

1. **Spaces (Project Domains)**: Top-level boundaries that isolate project state, operational rules, and access permissions.
2. **Pages (Living Artifacts)**: Structured, version-controlled markdown documents where deliverables, architectural designs, audit reports, and task boards reside.
3. **Collaborative Read/Write**: Both human operators and autonomous Dots share read and write access to pages, using them as the source of truth for ongoing work.

---

## 3. Sandboxed Per-Worker Compute & Headless Invariant

Autonomous coworkers executing external actions require isolated execution boundaries:

1. **Workspace Boundary Isolation**: Each Dot operates inside designated workspace paths or repository worktrees, preventing cross-task contamination.
2. **Headless Execution Only**: All browser interactions, web retrieval, and DOM evaluations strictly run in headless engines (such as Obscura headless CDP in AGYOS) without opening GUI windows.
3. **Zero Plaintext Secrets**: Environmental tokens, API keys, and credentials are never stored in working documents, pages, or commits; they are injected via server-side environment references.

---

## 4. Human-in-the-Loop Review Gates & Deny-by-Default

Autonomous capability requires predictable safety boundaries:

1. **Deny-by-Default on Destructive Actions**: Read-only inspection (grep, AST queries, file reading) may execute autonomously. Destructive operations (modifying critical branches, deploying, invoking paid APIs, credential changes) require an explicit review checkpoint.
2. **Interactive Review Checkpoints**: Before applying major mutations, the Dot presents a concise delta, rationale, and impact assessment for operator approval.
3. **Monotonic Audit Trail**: All tool calls, parameters, and outputs must be recorded in execution logs for auditability and post-incident review.

---

## 5. Model Context Protocol (MCP) Scoping

Tool access follows the principle of least privilege:

1. **Per-Dot Tool Allowlists**: Dots are granted access only to the specific MCP servers and tools required for their declared mandate.
2. **Strict Tool Schemas**: Interactions across the system boundary adhere strictly to JSON-RPC 2.0 schemas, rejecting untyped or speculative arguments.
3. **Decoupled Transport**: Communication between agents and tools remains transport-agnostic, supporting stdio, HTTP, and WebSocket connections without tight coupling.

---

## 6. Multi-Channel Asynchronous Coordination

Coworkers operate across multiple communication channels without losing state:

1. **Channel Agnosticism**: A Dot can receive instructions from CLI commands, webhook dispatches, CI triggers, or message boards, mapping all inputs into standard task specifications.
2. **Non-Blocking Execution**: Background jobs run asynchronously without tying up interactive turns, waking up the coordination spine only when results are ready.
3. **Unified Status Reporting**: Every channel receives concise, factual summaries containing exact diffs, test evidence, and next steps.
