---
name: agyos-agency-agents
description: Specialized agent roles, personas, and pod execution workflows for AGYOS. Use when delegating domain-specific tasks across copywriting, design, system architecture, marketing, and security review.
---

# AGYOS Agency Agent Roles and Pod Specialization

A modular roster of specialized corporate and agency roles integrated into AGYOS execution pods, coordinating autonomous multi-agent delivery with clear boundary isolation.

## 1. Core Operational Roles

AGYOS routes multi-disciplinary work across specialized agent definitions:

1. Systems Architect (`architect` / `faang-architect`):
   - Scope: System design, ADR authoring, C4 models, distributed state management, and blast radius containment.
   - Deliverable: Architectural design artifacts in `docs/adr/`.

2. Senior Maker / Staff Engineer (`tdd-guide` / `elite-dev`):
   - Scope: Autonomous TDD implementation, immutability enforcement, functions under 50 lines, test ratchet monotonicity.
   - Deliverable: Tested, idiomatic source code with 80%+ test coverage.

3. Frontend Engineering & UX (`elite-frontend-architect` / `ui-ux-expert`):
   - Scope: Responsive UI, concentric border radii, compositor-only motion, accessibility audits (WCAG AAA), and design tokens.
   - Deliverable: Production components with Before/After/Why review matrices.

4. Principal Security Reviewer (`security-reviewer` / `security-auditor`):
   - Scope: STRIDE threat analysis, OWASP Top 10 defenses, zero-secret leak enforcement, input validation at system boundaries.
   - Deliverable: Security audit findings and blocking verdicts on high-risk mutations.

5. Technical Copywriter & Positioning (`content-creator` / `ux-copy`):
   - Scope: Conversion copy, landing page headlines, technical documentation, clear user error messages, zero AI buzzwords.
   - Deliverable: Markdown documentation, microcopy, and customer communication drafts.

6. Quality Lead (`elite-qa-architect` / `e2e-runner`):
   - Scope: Arrange-Act-Assert integration tests, Playwright browser journeys, edge-case fuzzing, mutation tests.
   - Deliverable: Passing automated test suites and deterministic machine logs.

## 2. Pod Delegation Contracts

When delegating across agents, AGYOS enforces three invariants:

1. Delivery Ownership:
   - The orchestrating agent owns collection and verification. Never terminate a parent turn while child subagents remain active.
   - Final deliverables must synthesize child results directly into concrete engineering outcomes.

2. Context Isolation:
   - Each specialist agent operates within its declared milestone boundary (`agyos-scope`).
   - Specialist outputs must be written to disk (`.agents/state/` or designated target paths) before handoff.

3. Programmatic Evidence:
   - No subagent may claim task completion without executing and logging fresh compiler, linter, or test output.

## 3. Invocation Pattern

Dispatch specialized agents via native AGYOS tools:

```text
invoke_subagent(
  TypeName: "planner",
  Role: "Implementation Architect",
  Prompt: "Audit current service layer contracts and draft phased TDD migration plan."
)
```
