---
name: sop-customer
description: Standard Operating Procedure for Customer Pod (Onboarding and Support). Governs client onboarding checklists, ticket diagnosis, policy-adherent response drafting, and defect escalation.
---

# SOP: Customer Operations (Onboarding & Support)

This standard operating procedure governs client onboarding workflows and technical support ticket resolution.

## Procedure Steps

1. **Intake & Scope Definition**:
   - Extract customer ID, reported issue or onboarding tier, and requested outcome.
   - Default to R0 (read-only diagnosis) or R1 (draft guide).
   - If financial refunds or account access grants are requested, classify as R3 and stage in outbox.

2. **Diagnostics & Fact-Gathering**:
   - Inspect error logs and existing documentation via read-only tools.
   - Isolate root causes without making destructive changes to customer accounts.

3. **Deliverable Production**:
   - Provide clear, empathetic, and technically accurate resolution steps.
   - For reproducible engineering bugs, formulate a typed bug contract and escalate to `pod-build`.

4. **Verification & Completion**:
   - Confirm recommendations adhere to customer service SLAs and privacy guidelines.
