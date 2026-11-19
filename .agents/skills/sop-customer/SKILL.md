---
name: sop-customer
description: Standard Operating Procedure for Customer Pod (Onboarding and Support). Governs client onboarding checklists, ticket diagnosis, policy-adherent response drafting, and defect escalation.
prompt-source: prompt.toon
---
skill: "sop-customer"
sections[3]:
  - "\n"
  - "# SOP: Customer Operations (Onboarding & Support)\n\nThis standard operating procedure governs client onboarding workflows and technical support ticket resolution.\n\n"
  - "## Procedure Steps\n\n1. **Intake & Scope Definition**:\n   - Extract customer ID, reported issue or onboarding tier, and requested outcome.\n   - Default to R0 (read-only diagnosis) or R1 (draft guide).\n   - If financial refunds or account access grants are requested, classify as R3 and stage in outbox.\n\n2. **Diagnostics & Fact-Gathering**:\n   - Inspect error logs and existing documentation via read-only tools.\n   - Isolate root causes without making destructive changes to customer accounts.\n\n3. **Deliverable Production**:\n   - Provide clear, empathetic, and technically accurate resolution steps.\n   - For reproducible engineering bugs, formulate a typed bug contract and escalate to `pod-build`.\n\n4. **Verification & Completion**:\n   - Confirm recommendations adhere to customer service SLAs and privacy guidelines.\n"
