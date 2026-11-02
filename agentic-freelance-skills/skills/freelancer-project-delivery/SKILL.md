---
name: freelancer-project-delivery
description: Use when onboarding clients, setting up git repositories, designing MLOps pipelines (ZenML, MLflow, DVC), structuring tests/QA for ML, and managing project milestones or delivery handoffs.
---

# Freelancer Project Delivery System

Deliver production-grade work that exceeds client expectations, maintains quality standards, and creates natural upsell opportunities through systematic project management and MLOps excellence.

---

## Skill Architecture

To utilize this skill's core workflows, configuration patterns, or checklists, read the corresponding document in the `references/` directory:

| File | Focus | Purpose |
|------|-------|---------|
| [04A-KICKOFF-SYSTEM.md](references/04A-KICKOFF-SYSTEM.md) | Kickoff System | Client onboarding checklist, technical access protocol, communication bounds, project portal configuration |
| [04B-PROJECT-MANAGEMENT.md](references/04B-PROJECT-MANAGEMENT.md) | Project Management | Agile sprint structures, milestone definitions, async weekly status templates |
| [04C-DEVELOPMENT-WORKFLOW.md](references/04C-DEVELOPMENT-WORKFLOW.md) | Development Workflow | Git branch architecture, pull request templates, linter and formatter settings |
| [04D-ML-OPS-PIPELINE.md](references/04D-ML-OPS-PIPELINE.md) | MLOps Pipeline | Production ML pipelines (ZenML, MLflow, DVC), model registration, drift detection (Evidently AI) |
| [04E-TESTING-QA.md](references/04E-TESTING-QA.md) | Testing & QA | unit testing, integration tests, robustness testing, CI pipelines |
| [04F-DELIVERY-HANDOFF.md](references/04F-DELIVERY-HANDOFF.md) | Delivery & Handoff | Production handoff checklists, demo video creation guide, live training scripts |

---

## Agent Guidelines & Workflows

### 1. Onboarding & Kickoff
When initiating a new client contract:
- Reference [04A-KICKOFF-SYSTEM.md](references/04A-KICKOFF-SYSTEM.md) to set up the client's **Project Portal** (Slack/Notion/Linear) and request infrastructure/data access.
- Execute the kickoff checklist to define communication boundaries (no unscheduled calls, weekly async reports).

### 2. Agile Project Management
When managing timelines and writing client updates:
- Reference [04B-PROJECT-MANAGEMENT.md](references/04B-PROJECT-MANAGEMENT.md) to run **2-week development sprints** featuring clean milestone tracking.
- Draft professional weekly status updates detailing what was done, what is planned next, and blockages/risks.

### 3. Engineering & Development Workflows
When setting up codebases or code review pipelines:
- Reference [04C-DEVELOPMENT-WORKFLOW.md](references/04C-DEVELOPMENT-WORKFLOW.md) to establish clean git workflows (`main` $\rightarrow$ `dev` $\rightarrow$ `feature/*`).
- Configure automated code formatting (Black, Ruff) and apply standardized pull request templates.

### 4. MLOps System Design
When designing, building, or configuring machine learning pipelines:
- Reference [04D-ML-OPS-PIPELINE.md](references/04D-ML-OPS-PIPELINE.md) to structure model runs with ZenML, version data with DVC, track parameters/metrics with MLflow, and registry/deploy models.
- Set up automated data and concept drift detection using Evidently AI.

### 5. ML-Specific Testing and Quality Assurance
When writing testing pipelines for data or models:
- Reference [04E-TESTING-QA.md](references/04E-TESTING-QA.md) to establish a test suite containing: python unit tests, data schema validation (Pydantic), model performance assertion checks, and robustness/bias verification.

### 6. Client Handoff and Demos
When completing the project and transferring ownership:
- Reference [04F-DELIVERY-HANDOFF.md](references/04F-DELIVERY-HANDOFF.md) to record high-impact 2-minute demo videos, package documentation, and run live training sessions.

---

## Quick Reference Summary

| Concept | File | Section | One-Line Summary |
|---------|------|---------|------------------|
| Project Portal | [04A](references/04A-KICKOFF-SYSTEM.md) | 3 | Establish a shared workspace as the single source of truth for communication |
| 2-Week Sprints | [04B](references/04B-PROJECT-MANAGEMENT.md) | 2 | Structure projects into bi-weekly sprints with concrete, demoable deliverables |
| Git Branch Flow | [04C](references/04C-DEVELOPMENT-WORKFLOW.md) | 2 | Protect production branch: branch from `dev`, require PR verification and linting |
| Production ML Pipeline | [04D](references/04D-ML-OPS-PIPELINE.md) | 2 | Maintain reproducible pipelines: Data Validation $\rightarrow$ Feature Prep $\rightarrow$ Model Registry |
| Drift Dashboards | [04D](references/04D-ML-OPS-PIPELINE.md) | 5 | Implement data drift alerts to flag performance decay in production |
| Testing Pyramid | [04E](references/04E-TESTING-QA.md) | 2 | Structure test suite: 70% Unit tests, 20% Integration tests, 10% End-to-End checks |
| 2-Minute Demo | [04F](references/04F-DELIVERY-HANDOFF.md) | 2 | Record a concise, problem-to-solution video demo of the working system |

---

> **Previous Skill:** [freelancer-sales-closing ←](../freelancer-sales-closing/SKILL.md)
> **Next Skill:** [freelancer-post-delivery →](../freelancer-post-delivery/SKILL.md)
