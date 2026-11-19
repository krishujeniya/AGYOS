---
name: qa-tdd-architect
description: "Master of Test-Driven Development (TDD), writing tests, Systematic Debugging, and fixing failing tests. Use this skill when asked to write tests, fix a bug, debug a complex issue, or ensure code quality via automated verification. Relevant keywords: qa, tdd, test-driven, testing, tests, bug, debugging, error, failure, systematic, root cause."
category: process
risk: moderate
tags: "[testing, qa, tdd, debugging, pytest, jest, playwright]"
version: "1.0.0"
prompt-source: prompt.toon
---
skill: "qa-tdd-architect"
sections[12]:
  - "\n"
  - "# QA & TDD Architect (Systematic Debugging)\n\n"
  - "## Purpose\nThis skill enforces strict Test-Driven Development (TDD) pipelines and Systematic Debugging. It mandates that no production code is written without a failing test first, and no bug is fixed without establishing the root cause.\n\n"
  - "## When to Use\n- Implementing a new feature (enforce RED-GREEN-REFACTOR).\n- Investigating a reported bug or error stack trace.\n- Fixing broken unit or integration tests.\n- Writing E2E tests for the frontend.\n\n"
  - "## Key Workflow: Test-Driven Development\n- **The Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.\n- [ ] **RED:** Write a failing test that clearly describes the desired behavior. Do not test implementations, test behavior. Wait and watch it fail to prove the test actually works. **GATE:** Do not proceed until the test fails with the expected error message.\n- [ ] **GREEN:** Write the absolute simplest minimal code necessary to make the test pass. Do not add future-proofing (\"YAGNI\"). If you can fake it to pass the test, fake it. **GATE:** All tests must pass before proceeding.\n- [ ] **REFACTOR:** Clean up the working code. Ensure all tests still pass. **Triggers:** Cyclomatic complexity > 10, function length > 20 lines, duplicate code blocks > 3 lines.\n\n"
  - "### AI-Augmented Multi-Agent TDD\nWhen building large features, you can orchestrate this cycle using subagents:\n- **Test Automator:** Writes the failing tests (RED).\n- **Backend Architect:** Implements minimal code to pass (GREEN).\n- **Code Reviewer:** Optimizes and cleans up the code (REFACTOR).\n\n"
  - "## Key Workflow: Systematic Debugging\n- **The Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.\n- [ ] **Phase 1: Root Cause.** Read the full stack trace. Reproduce consistently. Trace data flow backward from the symptom. Add diagnostic logs across layers if needed.\n- [ ] **Phase 2: Hypothesis.** Formulate a clear hypothesis (\"I think X failed because Y\").\n- [ ] **Phase 3: Implementation.** Create a FAILING TEST case that isolates the bug.\n- [ ] **Phase 4: Verify.** Apply the fix. Confirm the test passes. If 3 attempts fail, stop and question the architectural pattern.\n\n"
  - "## Patterns & Examples\n\n"
  - "### TDD: Red-Green-Refactor Flow\n```python\n# 1. RED (test_calculator.py)\ndef test_addition():\n    # Write this first. Watch it fail.\n    assert add(2, 2) == 4\n\n# 2. GREEN (calculator.py)\ndef add(a: int, b: int) -> int:\n    # Just enough to pass the test\n    return a + b\n```\n\n"
  - "### Fixing Failing Test Suites (Smart Error Grouping)\nIf you are tasked with fixing a broken test suite:\n1. Run the test suite and gather all failures.\n2. **Smart Error Grouping:** Group similar failures by error type (e.g., `ImportError`, `AssertionError`, `TypeError`) or common impacted files.\n3. Fix **Infrastructure First** (missing dependencies, import errors, missing DB tables).\n4. Fix **API contract changes** (renamed functions, signature mismatches).\n5. Fix **Logic errors** last.\n6. Fix one group at a time and verify the subset passes before moving to the next.\n\n"
  - "### Coverage & Validation Rules\n- **Minimum Thresholds:** 80% line coverage, 75% branch coverage, 100% critical path coverage.\n- If TDD discipline is broken, STOP immediately, identify which phase was violated, and rollback to the last valid state.\n\n"
  - "## Error Handling\n- Never comment out a failing test to \"fix\" the build unless explicitly authorized by the user due to deprecation.\n- If mocking is required, mock only external boundaries (HTTP calls, DB clients), never internal application logic.\n"
