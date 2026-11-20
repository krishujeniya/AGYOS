---
description: "Autonomous 7-step software engineering cycle: Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect"
argument-hint: "<goal or feature requirement>"
---

# Autonomous 7-Step Cycle Workflow

Executes complete software delivery through the 7-step lifecycle without manual intervention.

## Sequence

```
[1. Think] ──> [2. Plan] ──> [3. Build] ──> [4. Review] ──> [5. Test] ──> [6. Ship] ──> [7. Reflect]
```

---

### Phase 1: Think

- Ingest natural language prompt into TaskContract (`compile_intent`).
- Evaluate EVPI clarification (`evaluate_evpi`). Proceed immediately with safe assumptions when benign.
- Select lead enterprise role (`classify_role_for_task`) and specialist skill (`decide_skill`).
- Assess complexity score (1-5) and route model tier (`ModelRouter`).

### Phase 2: Plan

- Generate milestone identifier (`M<n>-<slug>`).
- Define ordered task list with dependencies, target file paths, and done criteria.
- Advance state gate sequence (`UNDERSTAND` -> `ANALYZE` -> `PLAN`).
- Initialize milestone checkpoint in `.agents/state/checkpoints/<milestone>.md` and update `CURRENT.md`.

### Phase 3: Build

- Advance state gate to `IMPLEMENT`.
- Write minimal implementation adhering to the 6 FAANG Production Invariants.
- Apply strict boundary validation, explicit exception handling, and immutability.
- Keep functions < 50 lines and files < 800 lines.

### Phase 4: Review

- Execute independent Checker review.
- Run Python AST syntax inspection and shell syntax validation (`bash -n`).
- Scan for hardcoded credentials, secret patterns, and OWASP vulnerabilities.
- Verify `git diff --check` passes with zero whitespace or conflict errors.

### Phase 5: Test

- Advance state gate to `VERIFY`.
- Execute deterministic static verification (`compileall`, AST checks).
- Verify GitHub Actions CI/CD workflows configuration (`.github/workflows/ci.yml`).
- Enforce zero local heavy execution invariant.
- Record verification verdict in `.agents/state/state.json`.

### Phase 6: Ship

- Verify single `main` branch exclusive invariant.
- Verify author and committer identity lock (`Krish Ujeniya`).
- Stage changes and create conventional commit (`feat:`, `fix:`, `refactor:`).
- Push directly to `origin main` when auto-push is authorized.

### Phase 7: Reflect

- Prepend structured handoff entry to `AI_HANDOFF.toon` / `AI_HANDOFF.md`.
- Finalize milestone checkpoint status as `COMPLETED`.
- Reset state gate to `IDLE`.
- Store durable insights into recall memory tier.
