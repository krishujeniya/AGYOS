---
name: sop-gna
description: Standard Operating Procedure for General & Administrative Pod (Finance, Legal, and Operations). Governs invoice reconciliation, legal risk review, and procurement requisitions under strict fiduciary controls.
---

# SOP: G&A Operations (Finance, Legal, Operations)

This standard operating procedure governs financial audits, legal agreement reviews, and operational procurement workflows.

## Procedure Steps

1. **Intake & Fiduciary Classification**:
   - Classify analysis as R0 (read-only audit/review) or R1 (draft report).
   - Any external disbursements, banking mutations, or binding contract executions are strictly R3 and must be staged in the outbox as `PENDING_COMMIT`.

2. **Reconciliation & Analysis**:
   - Compare statements against general ledger accounts.
   - For legal reviews, extract indemnity, liability limits, and termination clauses with exact section references.
   - For procurement, compile vendor price/delivery matrix.

3. **Advisory Output Generation**:
   - Deliver findings clearly marked as internal drafts or advisory analyses.
   - Explicitly note that legal analysis does not constitute formal legal counsel.

4. **Approval Gate & Verification**:
   - Record snapshot of ledger and state before presenting changes to human operator.
