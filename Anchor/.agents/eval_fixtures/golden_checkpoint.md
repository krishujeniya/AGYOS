Goal: Provide a clean testing fixture for Phase 2 of eval.sh
# Milestone: M1-golden-test

Skill-Versions:
```json
{
  "anchor-draft-commit": "1.1.0",
  "anchor-verify": "1.1.0"
}
```

## Gate: PLAN
pass, human approved architecture

## Gate: COMPACT
pass, context compacted

## Gate: IMPLEMENT
## Iteration 1
What was done: Fixed tests.
Tokens used: 1500
```json
{
  "gate": "IMPLEMENT",
  "iteration": 1,
  "tdd_evidence": "Failing test output recorded here",
  "override_test_ratchet": false
}
```
Deterministic checks:
```bash
npm test
PASS
```

## Gate: VERIFY
pass, human approved deployment
```json
{
  "gate": "VERIFY",
  "status": "COMPLETE",
  "verified": "true"
}
```
