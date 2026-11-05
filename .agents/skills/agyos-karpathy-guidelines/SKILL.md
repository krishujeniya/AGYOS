---
name: agyos-karpathy-guidelines
description: Behavioral guidelines to eliminate LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
---

# AGYOS Karpathy Behavioral Guidelines

Behavioral engineering guidelines for AGYOS agents and operators, derived from Andrej Karpathy's findings on large language model coding failure modes.

Tradeoff: These rules prioritize correctness and precision over rapid generation. For trivial one-line edits, apply pragmatic judgment.

## 1. Think Before Coding

Surface assumptions, state uncertainties, and evaluate tradeoffs prior to mutation.

Before writing code:
- State technical assumptions explicitly in the implementation plan. When requirements admit multiple valid interpretations, list each option with its tradeoff rather than silently choosing one.
- If a simpler design exists, present it directly. Push back against unnecessary abstractions or requirements that conflict with simplicity.
- When an instruction is ambiguous, pause. Formulate one specific clarifying question rather than guessing.

## 2. Simplicity First

Deliver the minimal complete solution that directly satisfies the requirement.

Implementation rules:
- Build only the requested capabilities. Reject speculative extensions or hypothetical future requirements.
- Never introduce helper classes, abstraction layers, or design patterns for single-use code.
- Avoid artificial configurability or parameter sprawl that was not specified.
- Keep functions under 50 lines with a single responsibility.
- Keep source files under the 800-line maintainability ceiling.
- If an implementation spans 200 lines where 50 lines suffice, refactor to the simpler 50-line implementation.

## 3. Surgical Changes

Confine file mutations strictly to the task boundary.

Editing rules:
- Do not modify adjacent, unrelated code, comments, or formatting styles during a bug fix or feature addition.
- Preserve working production code even if alternative syntax is preferred.
- Match existing repository conventions, indentation, and architectural patterns.
- If unrelated dead code is observed, report it in the summary rather than deleting it unprompted.
- When new code makes an import, variable, or helper obsolete, remove that specific orphan immediately.

Validation check: Every modified line in `git diff` must map directly to the active milestone requirement.

## 4. Goal-Driven Execution

Convert every engineering task into an executable, verifiable criterion.

Execution rules:
- Transform loose tasks into concrete validation assertions:
  - Feature addition: Write failing unit test first (RED), implement minimal logic (GREEN), refactor cleanly (IMPROVE).
  - Bug remediation: Write a reproduction test that fails, apply minimal fix, verify test passes.
  - Performance optimization: Record deterministic baseline latency, apply optimization, remeasure.
- Structure multi-step work into phased checkpoints with exact verification commands:
  1. Step definition -> verification command -> expected exit code / assertion.
  2. Repeat sequentially through full verification.
- Always demand machine evidence from compiler, linter, or test runner before declaring completion.
