---
name: vibe-to-production
description: Transform high-level vibe coding prompts and non-technical ideas into production-grade, FAANG-level software with automated PRD synthesis, TDD, threat modeling, and design engineering.
---

# Vibe to Production Engineering Engine

The definitive bridge between high-level, natural language "vibe coding" prompts and FAANG-grade, enterprise-ready software systems.

## Purpose

When non-technical founders, general operators, or rapid "vibe coders" express an ambitious product idea ("Build me an analytics dashboard with Stripe subscriptions and Google auth"), standard LLMs frequently produce fragile prototypes: monolithic 1,200-line files, hardcoded credentials, missing database indices, race conditions, and zero test coverage.

This skill equips AGYOS to act as a virtual FAANG engineering department, autonomously promoting rapid vibe prototypes into robust, hardened, production-grade applications.

---

## The 5-Phase Vibe-to-FAANG Operational Process

```
[Vibe Prompt] ➔ [1. SHAPE SPEC] ➔ [2. CONTRACTS & ADR] ➔ [3. TDD MAKER] ➔ [4. VIBE AUDIT] ➔ [5. VERIFY]
```

### Phase 1: Intent & Spec Shaping (Staff PM)
Convert loose, conversational intent into a structured Task List with unambiguous acceptance criteria:
1. **Core User Story**: Who is the user and what is the exact outcome?
2. **Acceptance Criteria**: Verifiable statements of done (e.g. "Returns HTTP 200 with JWT token on valid credentials").
3. **Declared Scope Boundary**: Explicitly document what is **in-scope** vs **out-of-scope** to prevent feature creep.
4. **Complexity Scoring**: Call `bin/agyos decide "<task>"` to obtain the calibrated complexity score (1–5).

### Phase 2: Contracts & Architecture (Principal Architect)
Before writing application logic:
1. **Schema-First Data Contracts**: Define typed data models (Pydantic in Python, Zod in TypeScript, Serde in Rust) with boundary validation.
2. **Database Invariants**: Ensure every queried foreign key has an index; enforce idempotency keys on write endpoints.
3. **Architecture Decision Record (ADR)**: If introducing a new library or structural change, record the decision in `docs/adr/`.
4. **Blast Radius Containment**: Isolate failures so that external service timeouts do not crash the primary application.

### Phase 3: Autonomous Maker Implementation (Staff Software Engineer)
Execute autonomous Test-Driven Development (TDD):
1. **Write Failing Test (RED)**: Author an Arrange-Act-Assert (AAA) test capturing the required behavior.
2. **Minimal Implementation (GREEN)**: Write the minimal clean code to make the test pass.
3. **Refactor & Polyglot Discipline (IMPROVE)**:
   - Functions under 50 lines with single responsibility.
   - Files under the 800-line maintainability ceiling.
   - Immutability: return new copies; never mutate arguments or state in-place.
   - Maximum 4 levels of indentation; early guard returns.

### Phase 4: Vibe Code Audit & Security Hardening (Checker Squad)
Audit the implementation against the 7 production dimensions:
1. **Hidden Debt**: Remove dead code, unused imports, or speculative abstractions.
2. **Error Handling**: Replace any bare `except:` or `catch (e) {}` with explicit typed handlers and structured error logs.
3. **Security Invariants**: Verify no credentials or API keys exist in code. Verify parameterized queries (no SQL injection).
4. **Design Engineering Standards**: If UI is created, enforce Emil Kowalski invariants:
   - Nested radii formula: $R_{\text{inner}} = R_{\text{outer}} - \text{padding}$.
   - Compositor-only motion: animate only `transform` and `opacity`.
   - Tactile feedback: `active:scale-[0.98]` on interactive buttons.

### Phase 5: Machine Verification (Adversarial Verifier)
Never mark a task complete without executing and printing fresh machine evidence:
1. Run full typechecker, linter, and unit/integration test suites.
2. Verify total assertions monotonically increased (Test Ratchet invariant).
3. Execute `bash scripts/agyos-verify.sh`.
4. Present verified walkthrough artifact with concrete command output to the operator.

---

## Quick Reference Commands

```bash
# 1. Decide optimal skills and gate complexity
bin/agyos decide "Implement user profile editing with avatar upload"

# 2. Run adversarial verification suite
bin/agyos verify

# 3. Compact conversation context when approaching limits
bin/agyos compact
```
