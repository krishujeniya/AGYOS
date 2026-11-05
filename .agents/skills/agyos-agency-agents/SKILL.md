---
name: agyos-agency-agents
description: Specialized agent roles, personas, and pod execution workflows for AGYOS. Use when delegating domain-specific tasks across copywriting, design, system architecture, marketing, and security review.
---

# AGYOS Agency Agent Roles and Pod Specialization

A modular roster of specialized corporate and agency roles integrated into AGYOS execution pods, coordinating autonomous multi-agent delivery with clear boundary isolation.

## 1. Core Operational Roles & Divisions

AGYOS organizes agent capabilities into 12 functional divisions mapped to the 5 execution pods:

- Engineering (`pod-build`): Systems Architect, Frontend Wizard, Backend Specialist, API Builder, Refactoring Cleaner, Database Modeler.
- Testing & Quality (`pod-build`): QA Lead, Test Automator, E2E Browser Runner, Mutation Verifier.
- Security & Defense (`pod-build` / `pod-gna`): AppSec Auditor, Reverse Engineer, Cryptographic Reviewer, Anti-Decompilation Specialist.
- Product & Design (`pod-build`): UI/UX Designer, Design System Architect, Accessibility Specialist, Micro-Interaction Engineer.
- Strategy & Project Management (`pod-build` / `pod-growth`): Implementation Planner, Technical Program Manager, Reality Checker, Scrum Facilitator.
- Marketing & Growth (`pod-growth`): Content Strategist, Reddit Community Specialist, Copywriter, Programmatic SEO Architect.
- Paid Media (`pod-growth`): Ad Creative Engineer, Campaign Audience Profiler, Conversion Rate Optimizer.
- Sales & Distribution (`pod-growth`): Lead Intelligence Researcher, Sales Pipeline Specialist, Outreach Copywriter.
- Customer & Operations (`pod-customer`): Support Ticket Diagnostician, Customer Onboarding Lead, Documentation Author.
- Finance & Billing (`pod-gna`): Billing Operations Specialist, Revenue Analyst, Unit Economics Auditor.
- Legal & Compliance (`pod-gna`): Privacy/GDPR Auditor, Contract Analyzer, License Compatibility Reviewer.
- People & Talent (`pod-people`): Applicant Screener, Technical Interview Packager, Onboarding Coordinator.

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
