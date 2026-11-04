# Gate 5: VERIFY — Full Protocol

> Load this reference JIT when entering Gate 5. Do NOT preload into context.

## Objective
Verify all work with evidence, review code quality, and prepare for deployment.

## Step-by-Step Protocol

### Step 1: Verification (Evidence Before Claims)
```
Skill: verification-before-completion
```

**The Iron Law**: No completion claims without fresh verification evidence.

For EACH acceptance criterion:
1. IDENTIFY: What command proves this?
2. RUN: Execute the full command
3. READ: Full output, check exit code
4. VERIFY: Does output confirm the claim?
5. ONLY THEN: Make the claim

```bash
# Run full test suite
npm test  # or pytest, cargo test, go test ./...

# Run linter
npm run lint  # or ruff check, clippy

# Run type checker
npm run typecheck  # or mypy, tsc --noEmit

# Run build
npm run build
```

### Step 2: QA Gate Validation
```
Skill: expert-qa-engineer
```

Validate all QA gates defined in Gate 3:

#### Gate A: Unit Tests
- [ ] Coverage ≥ target (typically 80%)
- [ ] All unit tests passing
- [ ] No critical lint errors
- [ ] Type checking passes

#### Gate B: Integration Tests
- [ ] Integration tests passing
- [ ] API contracts validated
- [ ] DB migrations tested

#### Gate C: E2E Tests (if applicable)
- [ ] Critical user paths covered
- [ ] Cross-browser tested (if UI)
- [ ] Performance baseline met

### Step 3: Code Audit
```
Skill: vibe-code-auditor
```

Audit for:
- Structural flaws
- Technical debt
- Fragility
- Production risks
- Missing error handling
- Security vulnerabilities

### Step 4: Code Review
```
Skill: requesting-code-review
```

Generate review summary:
```markdown
## PR Summary
- Files changed: [N]
- Tests added: [N]
- Coverage: [X]%

## Changes
- [bullet list of changes]

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual verification: [steps]
```

### Step 5: Branch Completion
```
Skill: finishing-a-development-branch
```

Present options to user:
1. Merge back to main locally
2. Push and create Pull Request
3. Keep branch as-is
4. Discard work

### Step 6: HITL Deployment Approval
```
✅ All verification complete:
- Tests: [N/N] passing
- Coverage: [X]%
- Linter: Clean
- Build: Success
- Code audit: [summary]

Ready for deployment. Approve?
```

### Step 7: Archive (if using OpenSpec)
```
Skill: openspec-archive-change
```

## State Update
After deployment approval:
```json
{
  "current_gate": "COMPLETE",
  "completed_at": "[timestamp]",
  "verification": {
    "tests_passed": true,
    "coverage": "85%",
    "lint_clean": true,
    "build_success": true,
    "audit_passed": true
  }
}
```

## Verification Evidence Log

Create `.sovereign/verification.md`:
```markdown
# Verification Evidence: [Project Name]

## Test Results
[Paste actual test output here]

## Coverage Report
[Paste coverage output here]

## Lint Results
[Paste lint output here]

## Build Results
[Paste build output here]

## QA Gates
- [x] Gate A: Unit Tests — PASS
- [x] Gate B: Integration — PASS
- [x] Gate C: E2E — PASS

## Approved By
- User: [timestamp]
```
