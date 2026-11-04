---
name: sop-build
description: Standard Operating Procedure for Build Pod (Product and Engineering). Governs PRD authoring, Test-Driven Development (TDD) red-green-refactor loops, code quality, and regression verification.
---

# SOP: Build Operations (Product & Engineering)

This standard operating procedure enforces engineering rigor across product specification and software implementation.

## Procedure Steps

1. **Specification & PRD Synthesis (Gate 1-3)**:
   - Formulate clear problem statement, user stories, acceptance criteria, and failure boundary specs.
   - For complex features, author Architecture Decision Records (ADRs) and C4 component diagrams.

2. **Test-Driven Development Loop (Gate 4)**:
   - **RED**: Write failing automated tests covering core behavior and boundary cases.
   - **GREEN**: Write minimal, clean implementation to turn tests green.
   - **IMPROVE**: Refactor code for immutability, readability, functions <50 lines, and files <800 lines.

3. **Adversarial Verification (Gate 5)**:
   - Run typecheckers, linters, and full test suite with 80%+ coverage.
   - Enforce monotonic test ratchet: assertions must never decrease.

4. **Rollback & Commit**:
   - Provide clean git commit with conventional format and atomic rollback snapshot.
