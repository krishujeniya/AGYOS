# Gate 1: UNDERSTAND — Full Protocol

> Load this reference JIT when entering Gate 1. Do NOT preload into context.

## Objective
Transform a vague idea into clear, documented requirements with user confirmation.

## Step-by-Step Protocol

### Step 1: Invoke Brainstorming Skill
```
Skill: brainstorming
Purpose: Explore user intent, requirements, and design before implementation
```

**HARD-GATE**: Do NOT proceed to Gate 2 without user design approval.

Key questions to explore:
1. **Who** is the end user? (Persona definition)
2. **What** problem does this solve? (Problem statement)
3. **Why** now? (Business justification)
4. **What** does success look like? (Success criteria)
5. **What** are the constraints? (Time, budget, tech, team)

### Step 2: Domain Research (Optional)
```
Skill: notebooklm-researcher (if available)
Skill: openspec-explore
```

Investigate:
- Existing solutions in the market
- Technical feasibility of proposed approaches
- Relevant APIs, libraries, frameworks
- Regulatory or compliance requirements

### Step 3: Document Requirements
Create `.sovereign/requirements.md`:

```markdown
# Requirements: [Project Name]

## Problem Statement
[What problem are we solving?]

## Target User
[Who is the primary user? Describe persona.]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Scope
### In Scope
- Feature A
- Feature B

### Out of Scope
- Feature X (future)
- Feature Y (not applicable)

## Constraints
- Timeline: [deadline]
- Budget: [if applicable]
- Tech stack: [preferences or requirements]
- Team: [who is available]

## Open Questions
- [ ] Question 1
- [ ] Question 2
```

### Step 4: HITL Approval Gate
Present requirements to user with:
```
✅ Requirements documented. Please review:
- Problem: [one-liner]
- Scope: [N features in, M features out]
- Constraints: [key constraints]

Approve to proceed to Gate 2: ANALYZE?
```

**WAIT for explicit user confirmation before proceeding.**

## State Update
After approval:
```json
{
  "current_gate": 2,
  "hitl_approvals": {
    "gate_1": "[timestamp]"
  }
}
```

## Quality Checklist
- [ ] Problem statement is specific (not vague)
- [ ] Target user is defined (not "everyone")
- [ ] Success criteria are measurable
- [ ] Scope has clear boundaries
- [ ] Constraints are documented
- [ ] User has explicitly approved
