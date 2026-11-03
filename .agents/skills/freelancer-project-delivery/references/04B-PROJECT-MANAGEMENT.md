---
module: "04-PROJECT-DELIVERY"
part: "B"
title: "Project Management"
version: "2026.05"
status: "Production-Ready"
---

# 04B: Project Management

> **Core Principle:** The client doesn't care about your process. They care about their outcomes. Your job is to make the process invisible and the results visible.
>
> *"Sell results, not your service."* — Him Singh

---

## Table of Contents

1. [The Sprint Framework](#1-the-sprint-framework)
2. [Milestone Planning](#2-milestone-planning)
3. [Client Communication Rhythm](#3-client-communication-rhythm)
4. [Risk Management](#4-risk-management)
5. [Quality Gates](#5-quality-gates)
6. [AI Prompts](#6-ai-prompts)
7. [Action Checklist](#7-action-checklist)

---

## 1. The Sprint Framework

### The 2-Week Sprint Cycle

```
Week 1:
Monday    → Sprint Planning (1 hr) — What we'll build
Tue-Thu   → Development (deep work)
Friday    → Internal Demo + Review

Week 2:
Monday    → Client Demo (30 min) — What we built
Tue-Thu   → Development + Revisions
Friday    → Sprint Retrospective (15 min)
            → Next Sprint Planning (30 min)
```

### Sprint Planning Template

```markdown
# Sprint [Number] Planning — [Date Range]

## Sprint Goal
[One sentence: What does success look like?]

## Deliverables
| # | Task | Owner | Estimate | Priority |
|---|------|-------|----------|----------|
| 1 | [Task 1] | [You] | [Hours] | P0 |
| 2 | [Task 2] | [You] | [Hours] | P0 |
| 3 | [Task 3] | [You] | [Hours] | P1 |
| 4 | [Task 4] | [You] | [Hours] | P1 |

## Definition of Done
- [ ] Code reviewed (self or peer)
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Client demo prepared
- [ ] Deployed to staging

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Action] |
| [Risk 2] | Low/Med/High | Low/Med/High | [Action] |

## Client Demo Plan
- What to show: [Specific features]
- What to ask: [Feedback questions]
- What to avoid: [Unfinished work]
```

### The Demo Day Script

```
"Hi [Name], here's what we built this sprint:

[Feature 1] — [30-second demo]
• What it does: [One sentence]
• Why it matters: [Business impact]
• Try it yourself: [Link/credentials]

[Feature 2] — [30-second demo]
• What it does: [One sentence]
• Why it matters: [Business impact]

Questions or feedback?

Next sprint, we're building [Feature 3]. 
Anything you want us to prioritize or adjust?"
```

---

## 2. Milestone Planning

### The Milestone Map

| Milestone | Target Date | Deliverable | Client Action | Payment Trigger |
|-----------|-------------|-------------|---------------|-----------------|
| **Kickoff** | Week 0 | Project plan, access confirmed | Provide credentials | Deposit (50%) |
| **Discovery Complete** | Week 1 | Architecture doc, data audit | Review + approve | — |
| **MVP Ready** | Week 3 | Working model/API | Test + feedback | Milestone (25%) |
| **Production Deploy** | Week 4 | Live system, monitoring | Accept + sign off | — |
| **Handoff** | Week 5 | Documentation, training | Attend training | Final (25%) |

### The Milestone Review

At each milestone, answer:

| Question | Your Answer | Client Confirms |
|----------|-------------|-----------------|
| What was delivered? | [Specific items] | ☐ |
| Does it meet acceptance criteria? | [Yes/No + evidence] | ☐ |
| What's the quality level? | [Test results, metrics] | ☐ |
| Are there blockers for next phase? | [List or "None"] | ☐ |
| Is the timeline still valid? | [Yes/No + adjustments] | ☐ |

---

## 3. Client Communication Rhythm

### The Communication Calendar

| Day | Activity | Channel | Duration | Audience |
|-----|----------|---------|----------|----------|
| **Monday** | Sprint planning (internal) | Solo | 30 min | You |
| **Tuesday** | Deep work | — | 6-8 hrs | — |
| **Wednesday** | Async check-in | Slack/Email | 10 min | Client |
| **Thursday** | Deep work | — | 6-8 hrs | — |
| **Friday** | Weekly update + demo | Email + Call | 45 min | Client |

### The Async Check-In (Wednesday)

```
"Quick mid-week update:

✅ On track for Friday demo
🔄 Currently building [feature]
📅 No blockers, no help needed

See you Friday!"
```

### The Friday Ritual

| Time | Activity | Purpose |
|------|----------|---------|
| 9:00 AM | Write weekly update email | Document progress |
| 10:00 AM | Prepare demo environment | Ensure everything works |
| 2:00 PM | Client demo call (30 min) | Show + tell + gather feedback |
| 3:00 PM | Document feedback + action items | Clarity for next sprint |
| 4:00 PM | Sprint retrospective (15 min) | Personal improvement |
| 4:30 PM | Next sprint planning (30 min) | Ready for Monday |

---

## 4. Risk Management

### The Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|----|------|------------|--------|------------|-------|--------|
| R1 | Data quality issues | Medium | High | Data audit in Week 1 | You | Active |
| R2 | Client feedback delays | High | Medium | 48-hour SLA in SOW | Client | Monitoring |
| R3 | Scope creep | High | High | Change order process | Both | Active |
| R4 | Third-party API changes | Low | High | Abstraction layer | You | Monitoring |
| R5 | Deployment failures | Medium | High | Staging environment | You | Active |

### Escalation Protocol

| Level | Trigger | Action | Timeline |
|-------|---------|--------|----------|
| **Green** | On track, no issues | Normal updates | Weekly |
| **Yellow** | Minor delay or blocker | Notify client, propose solution | Within 24 hours |
| **Red** | Major delay, quality issue, or scope conflict | Emergency call, revised plan | Within 4 hours |
| **Black** | Project at risk of failure | Formal escalation, contract review | Immediate |

---

## 5. Quality Gates

### The Definition of Done

Before any deliverable is shown to the client:

| Gate | Check | Tool |
|------|-------|------|
| **Code Quality** | Linting passes, no warnings | flake8, black, pylint |
| **Tests** | Unit tests >80% coverage | pytest, coverage.py |
| **Documentation** | README updated, API docs generated | Sphinx, MkDocs |
| **Security** | No secrets in code, dependencies scanned | git-secrets, Snyk |
| **Performance** | Response time <200ms, memory <1GB | locust, memory_profiler |
| **Deployment** | Deployed to staging, health checks pass | Docker, Kubernetes |
| **Client-Ready** | Demo script prepared, edge cases handled | Manual review |

### The Pre-Demo Checklist

- [ ] Feature works on your machine
- [ ] Feature works on staging
- [ ] Feature works on client's environment (if possible)
- [ ] Edge cases handled (empty input, large input, invalid input)
- [ ] Error messages are user-friendly
- [ ] Demo data is realistic (not "test123")
- [ ] Backup plan if demo fails (screenshots, recorded video)
- [ ] You can explain every technical decision

---

## 6. AI Prompts

### Prompt 1: Sprint Planner

```
Act as an agile project manager.

Project details:
- Type: [AI/ML / Web / Data]
- Duration: [WEEKS]
- Current week: [X]
- Deliverables: [LIST]
- Blockers: [ANY]

Create a 2-week sprint plan:
1. Sprint goal (one sentence)
2. Task breakdown (5-8 tasks with estimates)
3. Definition of done
4. Demo plan (what to show, what to ask)
5. Risk assessment

Make it realistic — don't overcommit.
```

### Prompt 2: Risk Analyzer

```
Act as a project risk analyst.

Project context:
- Type: [TYPE]
- Client: [COMPANY TYPE]
- Timeline: [WEEKS]
- Team: [SOLO / WITH HELP]
- Tech stack: [TOOLS]

Identify 5 potential risks:
1. Technical risks
2. Client-related risks
3. Timeline risks
4. Scope risks
5. External risks

For each:
- Likelihood (Low/Med/High)
- Impact (Low/Med/High)
- Mitigation strategy
- Early warning signs

Format as a risk register table.
```

### Prompt 3: Demo Script Writer

```
Act as a technical demo specialist.

Feature to demo:
- Name: [FEATURE]
- What it does: [DESCRIPTION]
- Tech stack: [TOOLS]
- Client is: [TECHNICAL / NON-TECHNICAL]

Write a 5-minute demo script:
1. Hook (why this matters — 30 sec)
2. Setup (what we're looking at — 30 sec)
3. Demo (the feature in action — 2 min)
4. Results (metrics, impact — 1 min)
5. Q&A (what to ask the client — 1 min)

Include backup plan if live demo fails.
```

---

## 7. Action Checklist

### Week 1: Setup

- [ ] Create sprint planning template
- [ ] Set up project tracking (Notion/Trello/Linear)
- [ ] Define definition of done
- [ ] Create risk register
- [ ] Schedule recurring demo calls

### Every Sprint

- [ ] Sprint planning (Monday)
- [ ] Daily standup (solo, 5 min)
- [ ] Mid-week async check-in
- [ ] Client demo (Friday)
- [ ] Sprint retrospective
- [ ] Update project portal

### Every Milestone

- [ ] Run quality gates
- [ ] Prepare milestone review
- [ ] Send deliverables + summary
- [ ] Request client sign-off
- [ ] Invoice if payment triggered

---

> **Next:** [04C: Development Workflow →](04C-DEVELOPMENT-WORKFLOW.md)
>
> *"The best project management is invisible to the client and invaluable to you."*

---

*Module 04B | Project Management | Version 2026.05*
