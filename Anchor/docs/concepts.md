# ANCHOR Concepts

ANCHOR is built around three core concepts: **Gates**, **State**, and **Skills**.

## 1. Gates

The 5-Gate Workflow is the core routing mechanism of ANCHOR.

- **UNDERSTAND**: Gather requirements and clarify intent.
- **ANALYZE**: Evaluate feasibility, risk, and architecture.
- **PLAN**: Produce a step-by-step implementation plan.
- **IMPLEMENT**: Write the code autonomously.
- **VERIFY**: Deterministically prove the code works (tests, linters) without hallucination.

## 2. State

ANCHOR uses durable JSON and Markdown state that survives context resets. All state is kept in `.agents/state/`.

- `state.json`: The machine-readable state of the current session (budgets, active gate).
- `CURRENT.md`: The human-readable summary of the session.
- `checkpoints/`: The append-only audit trail of every gate transition.

## 3. Skills

Skills are isolated sets of instructions in `.agents/skills/` that execute specific steps of the workflow. The **Maker/Checker split** is enforced by having separate skills for building (`IMPLEMENT`) vs checking (`VERIFY`).
