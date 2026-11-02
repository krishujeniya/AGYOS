---
name: freelancer-developer-resources
description: Use when requesting development prompts, system design/architecture templates (ADR, tech specs), docker/API boilerplates, CI/CD configs, Prometheus/Grafana monitoring scripts, or technical/behavioral interview preparation guides.
---

# Freelancer Developer Resources

Equip the solo AI/ML freelancer with copy-paste prompts, system design templates, reusable boilerplate code, production monitoring runbooks, and interview frameworks that match billion-dollar company engineering standards.

---

## Skill Architecture

To utilize this skill's prompts, system architectures, or code templates, read the corresponding document in the `references/` directory:

| File | Focus | Purpose |
|------|-------|---------|
| [07A-PROJECT-PROMPTS.md](references/07A-PROJECT-PROMPTS.md) | AI Prompts for Projects | XML-structured prompts for generating complete ML pipeline scripts, full-stack web applications, business automation services, or scrapers |
| [07B-ARCHITECTURE-TEMPLATES.md](references/07B-ARCHITECTURE-TEMPLATES.md) | System Design & ADR Docs | Architectural Decision Record (ADR) template, System Design Document blueprint, API Specification sheet |
| [07C-CODE-SNIPPETS.md](references/07C-CODE-SNIPPETS.md) | Boilerplate Snippets | Reusable Dockerfile configurations, FastAPI basic structures, GitHub Actions CI/CD workflows, pytest unit test scripts |
| [07D-MONITORING-PLAYBOOKS.md](references/07D-MONITORING-PLAYBOOKS.md) | Production Monitoring | Prometheus metric exports, Grafana monitoring dashboards, alert rules, runtime incident response playbooks |
| [07E-INTERVIEW-PREP.md](references/07E-INTERVIEW-PREP.md) | Freelancer Interview Prep | ML System Design framework, behavioral story builder, live technical coding review checklists |

---

## Agent Guidelines & Workflows

### 1. Generating Code with Prompts
When asked to write complex project scripts, pipelines, or web apps:
- Reference [07A-PROJECT-PROMPTS.md](references/07A-PROJECT-PROMPTS.md) to locate the relevant XML-structured promts.
- These prompts ensure AI models write complete, self-documenting code with error boundaries, logging, and unit tests (avoiding placeholders or shortened mock code).

### 2. Drafting System Architecture & ADRs
When asked to design a system, explain architecture choices, or document technical decisions:
- Reference [06B-LEGAL-CONTRACTS.md](../freelancer-operations/references/06B-LEGAL-CONTRACTS.md) for legal alignment, then use [07B-ARCHITECTURE-TEMPLATES.md](references/07B-ARCHITECTURE-TEMPLATES.md) to draft a System Design Document or ADR.
- Log architectural choices using the immutable ADR format detailing: Context, Alternatives Considered, Decision, Consequences, and Rollback Path.

### 3. Deploying Boilerplate Snippets
When setting up project scaffolds, containers, or test suites:
- Reference [07C-CODE-SNIPPETS.md](references/07C-CODE-SNIPPETS.md) to copy Dockerfile templates, modular FastAPI setups, and multi-stage CI/CD configuration files.

### 4. Setting Up Production Monitoring
When designing production release scripts or monitoring guides:
- Reference [07D-MONITORING-PLAYBOOKS.md](references/07D-MONITORING-PLAYBOOKS.md) to expose custom Prometheus metrics.
- Build Grafana panels tracking: system metrics (CPU, RAM, latency), database load, and model drift indicators.

### 5. Client Interviews and Screening prep
When assisting a freelancer with preparing for client screening calls or technical system design interviews:
- Reference [07E-INTERVIEW-PREP.md](references/07E-INTERVIEW-PREP.md) to draft behavioral stories using the STAR framework.
- Practice the 6-step Machine Learning System Design blueprint (Scope $\rightarrow$ Data $\rightarrow$ Features $\rightarrow$ Offline Training $\rightarrow$ Evaluation $\rightarrow$ Deployment/Monitoring).

---

## Quick Reference Summary

| Concept | File | Section | One-Line Summary |
|---------|------|---------|------------------|
| XML Prompts | [07A](references/07A-PROJECT-PROMPTS.md) | 2 | Structure instructions using `<context>` and `<requirements>` tags for precise generation |
| Tech Spec Blueprint | [07B](references/07B-ARCHITECTURE-TEMPLATES.md) | 1 | Define goals, non-goals, data schema, scale metrics, and failure scenarios before coding |
| ADR Format | [07B](references/07B-ARCHITECTURE-TEMPLATES.md) | 2 | Record decisions: title, context, options considered, selected decision, consequences |
| FastAPI Template | [07C](references/07C-CODE-SNIPPETS.md) | 2 | Deploy microservices with health-checks, global exception handlers, and dotenv setup |
| Prometheus metrics | [07D](references/07D-MONITORING-PLAYBOOKS.md) | 1 | Instrument endpoints with latency counters, failure triggers, and execution histograms |
| ML Design Steps | [07E](references/07E-INTERVIEW-PREP.md) | 1 | Answer system design queries: Problem $\rightarrow$ Data $\rightarrow$ Features $\rightarrow$ Model $\rightarrow$ Evaluation $\rightarrow$ Monitor |

---

> **Previous Skill:** [freelancer-operations ←](../freelancer-operations/SKILL.md)
> **Next Skill:** [freelancer-emergency-kit →](../freelancer-emergency-kit/SKILL.md)
