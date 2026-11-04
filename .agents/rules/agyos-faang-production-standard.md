---
trigger: always_on
---
# AGYOS FAANG-Grade Production Standards

## Purpose
Enforces Tier-1 FAANG (Meta, Apple, Amazon, Netflix, Google) and research laboratory software engineering standards across all AI-generated code, transforming loose, non-technical "vibe coding" prompts into enterprise-ready, maintainable, and battle-tested software.

---

## The 6 Production Invariants for Vibe Coders

Whenever implementing features from high-level, natural language, or vibe prompts, the system MUST enforce these invariants:

### 1. Strict Boundary Input Validation
- Validate all external inputs (HTTP payloads, CLI arguments, query parameters, webhook payloads, file inputs) at the system boundary before processing.
- Use schema-first validation (e.g., Pydantic in Python, Zod/TypeScript types in web, Serde in Rust).
- Reject malformed payloads immediately with structured HTTP 400/422 responses. Never trust unverified input.

### 2. Comprehensive Error Handling & Zero Silent Swallowing
- Never write bare `except:` or `catch (e) {}` blocks that silently swallow exceptions.
- Provide human-readable, safe error messages to UI clients; log detailed diagnostic context (stack traces, correlation IDs, offending IDs) on the server side.
- Implement explicit fallback states for degraded network or external service failures (circuit breaker pattern).

### 3. Safe & Idempotent Database Operations
- Use parameterized queries or typed ORM builders exclusively. String interpolation or concatenation in SQL statements is strictly forbidden.
- Always add database indices on foreign keys, unique columns, and high-frequency filter predicates.
- Enforce idempotent write operations (e.g., Stripe `idempotency_key`, database unique constraints with `ON CONFLICT DO NOTHING / UPDATE`).

### 4. Immutability & Modular Maintainability
- Return new copies of objects and data structures; never mutate state in place.
- Functions must remain under 50 lines focused on a single responsibility.
- Source files must remain under the 800-line maintainability ceiling. If logic exceeds 400 lines, extract cohesive sub-modules.
- Maximum 4 levels of indentation; prefer early guard returns over nested conditionals.

### 5. Zero-Secret & Defense-in-Depth Security
- Never store API keys, passwords, database credentials, or secret tokens in repository code, tests, or mock files.
- Load secrets strictly from validated environment variables with startup sanity checks.
- Enforce principle of least privilege on tool permissions, database users, and API tokens.
- Protect against OWASP Top 10: XSS, CSRF, SSRF, IDOR, and injection vulnerabilities.

### 6. Deterministic Machine Evidence & Test Ratchet
- Never declare a milestone or task complete based on speculative reasoning. Every completion claim requires executing and printing clean compiler, linter, and test suite output.
- Enforce the Arrange-Act-Assert (AAA) pattern with minimum 80% test coverage.
- The test ratchet is monotonic: total test assertions and coverage must never decrease without explicit rationale.

---

## Vibe-to-FAANG Operational Workflow

```
[Non-Tech Vibe Prompt]
        │
        ▼
1. Staff PM Synthesis ────────► Clarify requirements, user stories, acceptance criteria, boundaries
        │
        ▼
2. Decision & Complexity ─────► bin/agyos decide: Fast-path (<=2) or 5-Gate Workflow (>=3)
        │
        ▼
3. Principal Architecture ────► C4 system model, API contracts, ADRs in docs/adr/
        │
        ▼
4. Autonomous Maker TDD ──────► Write failing test (RED) -> Minimal code (GREEN) -> Refactor (IMPROVE)
        │
        ▼
5. Checker Verification ──────► Vibe Code Audit + Security Review + 80%+ Test Ratchet
        │
        ▼
[Production Deployment Ready]
```
