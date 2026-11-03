# Gate 2: ANALYZE — Full Protocol

> Load this reference JIT when entering Gate 2. Do NOT preload into context.

## Objective
Evaluate feasibility, define product scope, create user stories, and assess risks.

## Step-by-Step Protocol

### Step 1: Product Vision (PM Expert)
```
Skill: expert-product-manager
```

Generate:
1. **Product Vision Statement** — Concise elevator pitch
2. **PRD (Product Requirements Document)** — Problem, audience, scope
3. **Success Metrics** — What defines a successful launch
4. **SaaS Metrics** (if applicable) — MRR, churn, LTV, CAC

### Step 2: User Stories (PO Expert)
```
Skill: expert-product-owner
```

For each feature in scope:
1. Write INVEST-compliant user stories
2. Add Gherkin acceptance criteria (Given/When/Then)
3. Estimate story points (1/2/3/5/8/13)
4. Apply MoSCoW prioritization

### Step 3: Task-Model Fit Assessment
```
Skill: project-development
```

Evaluate each feature:
- Is it suited for LLM-assisted development?
- What's the estimated token cost?
- Single agent vs. multi-agent architecture needed?
- Pipeline architecture: acquire → prepare → process → parse → render

### Step 4: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 2] | ... | ... | ... |

### Step 5: Document Analysis
Create `.sovereign/analysis.md`:

```markdown
# Analysis: [Project Name]

## Product Vision
[One-liner vision statement]

## PRD Summary
- Problem: [...]
- Target Audience: [...]
- Key Features: [...]

## User Stories (Prioritized)
### Must Have (P0)
- US-001: As a [user], I want [feature] so that [benefit]
  - AC: Given [...] When [...] Then [...]

### Should Have (P1)
- US-002: ...

## Cost Estimation
- Estimated development: [time]
- Token budget: [estimate]
- Infrastructure: [requirements]

## Risk Register
[Risk table from Step 4]
```

### Step 6: HITL Approval Gate
Present to user:
```
✅ Analysis complete:
- [N] user stories defined ([X] Must, [Y] Should, [Z] Could)
- Estimated effort: [time]
- Key risks: [top 2-3 risks]

Approve scope to proceed to Gate 3: PLAN?
```

## State Update
After approval, update `state.json` with `current_gate: 3`.
