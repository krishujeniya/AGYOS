---
trigger: always_on
description: "Enforces automatic execution through the 7-Step Autonomous Cycle: Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect across all AGYOS engineering and development tasks."
---

# AGYOS 7-Step Autonomous Cycle Standard

Whenever assigned an engineering, development, refactoring, bug fixing, or architectural task, AGYOS agents MUST automatically progress through this 7-step sequence:

```
Think ──> Plan ──> Build ──> Review ──> Test ──> Ship ──> Reflect
```

No slash commands are required from the operator. The lifecycle executes autonomously from initial prompt comprehension through verified production delivery and retrospective reflection.

---

## Step 1: THINK (Intent Synthesis & Grounding)

Before modifying code or planning architecture:
- **Intent Compilation**: Ingest natural language prompt into a typed TaskContract (`compile_intent`).
- **Socratic Analysis & EVPI**: Assess whether clarification is needed (`evaluate_evpi`). Apply safe default assumptions for non-destructive actions; ask at most 1 concise question if consequential.
- **Role & Pod Alignment**: Identify lead role from the 104-role matrix (`classify_role_for_task`) and governing pod.
- **Skill Discovery**: Query catalog (`decide_skill`) and silently ingest the specialist runbook.
- **Complexity Scoring**: Assess complexity (1-5). Complexity 1-2 qualifies for fast-path; 3-5 executes full governance.
- **Model & Thinking Routing**: Route optimal model provider and thinking level (`ModelRouter`).

---

## Step 2: PLAN (Architectural Blueprint & Milestone Checkpoint)

Translate thinking outputs into concrete execution units:
- **Milestone Identification**: Determine next milestone identifier (`M<n>-<slug>`).
- **Concrete Task Breakdown**: Define atomic tasks with target file paths, dependencies, and done criteria.
- **Acceptance Criteria**: Specify explicit Given/When/Then conditions.
- **Gate Advancement**: Transition state gate from `IDLE` -> `UNDERSTAND` -> `ANALYZE` -> `PLAN`.
- **Structured Checkpoint**: Initialize milestone checkpoint in `.agents/state/checkpoints/<milestone_id>.md` and update `.agents/state/CURRENT.md`.

---

## Step 3: BUILD (Maker TDD & FAANG Invariants)

Execute focused implementation with the 6 FAANG Production Invariants:
- **Gate Advancement**: Transition state gate to `IMPLEMENT`.
- **TDD Workflow**: Write tests first (RED) -> write minimal code (GREEN) -> refactor cleanly (IMPROVE).
- **Boundary Validation**: Validate all external inputs at the system boundary before processing.
- **Explicit Error Handling**: Zero bare `except:` or `catch (e) {}` blocks. Provide safe human-readable errors.
- **Immutability & Size Ceilings**: Functions < 50 lines, files < 800 lines, nesting <= 4 levels, immutable copies.
- **Zero Secrets**: Load credentials strictly from environment variables. Never hardcode tokens or keys.

---

## Step 4: REVIEW (Independent Checker Audit)

Enforce Maker/Checker separation with objective verification:
- **Code Quality Audit**: AST parse check across modified Python modules, shell syntax check (`bash -n`).
- **Security Audit**: Regex inspection for leaked credentials, unsafe subprocess execution, and OWASP Top 10 vulnerabilities.
- **Git Diff Hygiene**: Verify `git diff --check` passes with zero trailing whitespace or conflict markers.
- **Verdict Recording**: Append Review verdict (PASS/FAIL) and findings to the milestone checkpoint.

---

## Step 5: TEST (Deterministic Static Verification & CI/CD)

Ensure monotonic verification proof:
- **Gate Advancement**: Transition state gate to `VERIFY`.
- **Deterministic Static Proof**: Execute `python3 -m compileall`, `bash -n bin/*`, AST checks.
- **Zero Local Heavy Execution**: Never run local compilers, test runners, or heavy renders. Verification belongs strictly in GitHub Actions CI/CD (`.github/workflows/ci.yml`).
- **State Update**: Record verification status in `.agents/state/state.json` under `verification.status = PASS`.

---

## Step 6: SHIP (Single Main Branch Delivery)

Deliver the verified milestone safely:
- **Single Main Branch Invariant**: Verify active branch is `main`. Never create or maintain secondary branches.
- **Identity Lock**: Enforce author and committer identity strictly as `Krish Ujeniya` (`100012208+krishujeniya@users.noreply.github.com`).
- **Conventional Staging & Commit**: Stage modified files and create conventional commit (`feat:`, `fix:`, `refactor:`).
- **Delivery**: If auto-push is requested, push directly to `origin main`. Otherwise, verify staging and state exact push command.

---

## Step 7: REFLECT (Retrospective & Living Memory)

Close the operational loop and preserve knowledge:
- **Structured Handoff**: Prepend new handoff entry to `AI_HANDOFF.toon` (and `AI_HANDOFF.md`) detailing task, branch, delivered changes, evidence verified, and exact next command.
- **Milestone Finalization**: Mark checkpoint as `COMPLETED` and record completion timestamp.
- **Gate Reset**: Reset `.agents/state/state.json` gate to `IDLE`.
- **Session Memory**: Store durable lessons learned into recall memory tier.

---

## 3-Strike Failure Recovery Rule

1. **Strike 1**: Fix specific syntax, lint, or logic failure. Re-verify.
2. **Strike 2**: Re-read the source code and runbook. Adopt an alternative implementation pattern.
3. **Strike 3**: Stop immediately. Revert mutations, document root cause in checkpoint, and request operator direction.
