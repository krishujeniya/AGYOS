---
name: agyos-decision
description: Autonomous System 1 decision engine and skill router. Classifies task domains, assesses gate complexity (1-5), and selects optimal specialist skills from the catalog with calibrated confidence.
---

# AGYOS Decision Engine

Autonomous routing and selection of specialist skills from the AGYOS catalog (1,842+ skills) with calibrated confidence scoring and complexity-based gate routing.

## When to Use

Use this skill whenever:
1. Starting ANY non-trivial task or user request to identify the optimal specialist skill.
2. Determining whether a task needs a full 5-gate workflow (complexity >= 3) or a fast-path bypass (complexity <= 2).
3. Satisfying Invariant 1 (**Search-First Autonomous Skill Discovery**) before writing or modifying code.
4. Performing multi-class domain classification, ordinal scoring, or truth verification.

---

## 3-Step Decision Pipeline

```
[Incoming Work Objective]
           │
           ▼
1. Classify Domain (choice) ──────► debug | arch | ui_ux | motion | sec | verify | db | perf | devops | seo
           │
           ▼
2. Assess Complexity (score) ─────► 1-2: Fast-Path (direct to IMPLEMENT) | 3-5: Full 5-Gate Workflow
           │
           ▼
3. Rank & Select Skill (calibrated) ──► P(optimal_fit) >= 0.70 ──► Ingest SKILL.md & Execute
```

### Step 1: Domain Classification
Maps the objective across technical domains:
- `debugging`: Crashes, exceptions, stack traces, regressions (`diagnosing-bugs`).
- `architecture`: Interface contracts, ADRs, modular design (`architecture-decision-records`).
- `ui_ux`: Visual interfaces, layout systems, design tokens (`frontend-design-direction`).
- `motion`: Animation budgets, compositor-only motion, spring curves (`animate`).
- `security`: Authentication, CVE analysis, penetration testing (`security-review`, `pentagi-orchestrator`).
- `verification`: Unit/integration tests, test ratchets, TDD cycles (`verification-loop`).
- `database`: Schemas, migrations, indexing, query optimization (`database-design`, `postgres-best-practices`).
- `performance`: Latency baselines, single-variable hypotheses, benchmarks (`benchmark-optimization-loop`).
- `devops`: Pipelines, containerization, deployments (`gitops-workflow`).
- `seo`: Schema.org, indexing, crawlability, search engine optimization (`seo-audit`).
- `content`: Architecture documentation, technical guides (`technical-documentation-writer`).
- `freelance`: Client deliverables, SOWs, operational proposals (`agentic-freelance-skills`).
- `council`: Multi-model consensus and peer review (`agent-council`).
- `governance`: 5-gate milestone progression (`agyos-orchestrator`).

### Step 2: Complexity Gate Assessment (1–5)
- **Score 1–2 (Fast-Path Bypass)**: Trivial typos, string updates, bounded single-function or single-file fixes. Skips Gates 1–3 directly to `IMPLEMENT`.
- **Score 3 (Standard Development)**: Standard feature additions or bug fixes with regression tests. Runs standard 5-gate workflow.
- **Score 4–5 (High-Impact / Architectural)**: Cross-module refactoring, database migrations, security changes. Requires strict ADRs and council deliberation.

### Step 3: Invocation Methods

#### 1. Via CLI
```bash
# Formatted summary with domain, complexity, and recommendations
bin/agyos decide "Design Postgres database schema with migrations"

# Machine-readable JSON output
python3 scripts/agyos-decision.py "Add JWT authentication to FastAPI service" --json
```

#### 2. Via FastMCP Daemon
Call tool `agyos_decision` over stdio JSON-RPC:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "agyos_decision",
    "arguments": {
      "task": "Investigate memory leak in Node.js event listener"
    }
  }
}
```

#### 3. Via Python API
```python
from agyos_decision import decide_skill, select_best_skills

result = decide_skill("Optimize slow database query on billing table")
print(result["primary_skill"])       # postgres-best-practices
print(result["primary_path"])        # .agents/skills/postgres-best-practices
print(result["classification"])      # {'domain': 'database', 'complexity_score': 2, ...}
```

---

## Execution Flow Once Skill is Selected

1. Output recommended primary skill and calibrated confidence.
2. Silently read the skill runbook: `read_file(Path="<primary_path>/SKILL.md")`.
3. Apply domain specialist patterns directly to the implementation.
