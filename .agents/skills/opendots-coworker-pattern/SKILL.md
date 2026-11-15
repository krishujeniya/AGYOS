---
name: opendots-coworker-pattern
description: Architect and orchestrate persistent AI coworkers (Dots), document workspaces (Spaces & Pages), isolated sandboxes, and human-in-the-loop review gates following OpenDots principles without adding application code.
---

# OpenDots Coworker Pattern

This skill applies the architectural principles and operational logics of CopilotKit OpenDots to AGYOS workflows. It instructs agents how to behave as persistent, role-scoped coworkers operating over structured document workspaces with review checkpoints, without introducing foreign application code or dependencies.

---

## When to Use This Skill

Use this skill when:
- Designing or operating multi-agent systems where agents must maintain durable identity, context, and background task continuity.
- Structuring deliverables into living documents (Spaces and Pages) rather than dumping transient responses into chat logs.
- Enforcing human-in-the-loop review gates for high-risk operations (file writes, database operations, external API calls).
- Defining isolated compute sandboxes and granular Model Context Protocol (MCP) tool permissions per specialist.

---

## Core Principles

1. **Persistent Coworkers over Ephemeral Chatbots**: An agent ("Dot") is assigned a clear job role, system instructions, and tool bounds. It retains state across task iterations instead of starting fresh each turn.
2. **Spaces and Pages Architecture**:
   - **Space**: The bounded problem or repository domain.
   - **Page**: The living document (specifications, architecture designs, audit ledgers, test plans) where deliverables are drafted, refined, and maintained collaboratively.
3. **Per-Worker Isolated Execution**:
   - Every worker executes within defined sandbox boundaries (dedicated directories, worktrees, or headless browser sessions).
   - Browser interactions use headless engines (such as Obscura headless CDP) without spawning GUI windows.
4. **Deny-by-Default Review Gates**:
   - Safe operations (read, query, inspect) run autonomously.
   - Modifying actions (file writes, deletions, remote pushes, external API calls) pause at explicit review checkpoints presenting the diff, rationale, and rollback path.
5. **Least-Privilege MCP Tool Allowlists**:
   - Only attach tools explicitly needed for the worker's role.
   - Reject arbitrary tool access to minimize blast radius.

---

## Operational Workflow

### Step 1: Define the Coworker ("Dot") Profile
Before assigning work, establish the worker's operational specification:
- **Role Title**: Concise job title (e.g. `Security Auditor`, `Performance Optimizer`).
- **Scope Boundary**: Files and modules the worker is permitted to inspect or touch.
- **Allowed Tools**: Explicit list of read/write tools or MCP actions permitted.
- **Execution Mode**: Autonomous for read/analysis; checkpoint-gated for writes.

### Step 2: Establish the Space and Living Page
Create or designate the living artifact where the worker's output will be preserved:
- Place the document in the appropriate documentation or artifact path (e.g. `docs/`, `brain/<id>/`).
- Define the page structure: Objective, Current State, Detailed Findings / Specifications, Decision Records, and Action Items.
- Ensure the page serves as the persistent source of truth for both human engineers and subsequent agent passes.

### Step 3: Sandboxed Execution
When the worker carries out tasks:
- Confine file system operations to the designated project directory.
- Direct web research and DOM evaluation through headless interfaces (Obscura headless CDP).
- Never write credentials, API keys, or session tokens into pages or transcripts.

### Step 4: Interactive Review Checkpoint
Before applying any non-read-only changes:
- Formulate a structured review summary:
  1. Exact files to be created or modified.
  2. Concise rationale for the modification.
  3. Risk assessment and test verification plan.
- Require operator sign-off before committing changes to shared resources.

### Step 5: Deliverable Persistence and Checkpoint Log
Upon completing the task:
- Update the living page with the verified results and evidence.
- Record an audit entry summarizing the actions executed, tools invoked, and output artifacts.
- Leave the workspace clean and ready for the next coworker or inspection.

---

## Anti-Patterns to Avoid

- **Chat Log Dumping**: Producing large multi-page reports solely inside chat messages instead of recording them in a structured page.
- **Speculative Over-Tooling**: Granting an agent full write or execution tools when it only needs read or analysis capabilities.
- **Silent Tool Failures**: Continuing execution when an underlying tool or command fails without surfacing the diagnostic context.
- **Unbounded Multi-Agent Cascades**: Spawning unmonitored agent chains without an explicit completion contract and owner.
