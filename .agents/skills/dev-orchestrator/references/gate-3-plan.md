# Gate 3: PLAN — Full Protocol

> Load this reference JIT when entering Gate 3. Do NOT preload into context.

## Objective
Design the architecture, create a bite-sized implementation plan, and define quality gates.

## Step-by-Step Protocol

### Step 1: Architecture Design (Tech Architect)
```
Skill: expert-tech-architect
```

Create `design.md` with:
1. **System Architecture** — Component diagram (Mermaid)
2. **Technology Stack** — Framework/library decisions with rationale
3. **API Design** — Endpoints, contracts, versioning
4. **Database Schema** — Tables, relationships, indexes
5. **ADRs** — Architecture Decision Records for significant choices

### Step 2: Test Strategy (QA Engineer)
```
Skill: expert-qa-engineer
```

Define:
- Test pyramid distribution (70% unit / 20% integration / 10% E2E)
- Coverage goals per module
- QA gates (unit → integration → staging → production)
- Critical paths that MUST have E2E tests

### Step 3: Implementation Plan (Writing Plans)
```
Skill: writing-plans
Skill: planning-with-files
```

Create `task_plan.md` with bite-sized tasks:

```markdown
# Implementation Plan: [Project Name]

## Task 1: [Title]
**Files**: `path/to/file.ts`, `path/to/test.ts`
**Steps**:
- [ ] Step 1: Create file with interface
- [ ] Step 2: Write failing test
- [ ] Step 3: Implement minimal code
- [ ] Step 4: Verify tests pass

## Task 2: [Title]
...
```

**Task Granularity Rules** (from `writing-plans`):
- Each task modifies 1-3 files max
- Each step is a single action
- File paths are absolute, not relative
- Tests are written BEFORE implementation (TDD)
- Tasks are independent where possible (enable parallelization)

### Step 4: Tool Assessment
```
Skill: tool-design
```

Evaluate:
- Can we reduce tool count? (fewer tools = fewer agent errors)
- Are there primitive interfaces that cover multiple use cases?
- What's the minimum viable tool set?

### Step 5: HITL Architecture Approval
Present to user:
```
✅ Plan ready:
- Architecture: [pattern] with [tech stack]
- [N] implementation tasks defined
- Test strategy: [coverage goals]
- ADRs: [N] decisions documented

Approve architecture to proceed to Gate 4: IMPLEMENT?
```

## State Update
After approval:
- Set `current_gate: 4`, `current_task: 1`, `total_tasks: N`
- Initialize `progress.md` and `findings.md`
