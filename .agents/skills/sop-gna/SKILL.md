---
name: sop-gna
description: Standard Operating Procedure for General & Administrative Pod (Finance, Legal, and Operations). Governs invoice reconciliation, legal risk review, and procurement requisitions under strict fiduciary controls.
prompt-source: prompt.toon
---
skill: "sop-gna"
sections[3]:
  - "\n"
  - "# SOP: G&A Operations (Finance, Legal, Operations)\n\nThis standard operating procedure governs financial audits, legal agreement reviews, and operational procurement workflows.\n\n"
  - "## Procedure Steps\n\n1. **Intake & Fiduciary Classification**:\n   - Classify analysis as R0 (read-only audit/review) or R1 (draft report).\n   - Any external disbursements, banking mutations, or binding contract executions are strictly R3 and must be staged in the outbox as `PENDING_COMMIT`.\n\n2. **Reconciliation & Analysis**:\n   - Compare statements against general ledger accounts.\n   - For legal reviews, extract indemnity, liability limits, and termination clauses with exact section references.\n   - For procurement, compile vendor price/delivery matrix.\n\n3. **Advisory Output Generation**:\n   - Deliver findings clearly marked as internal drafts or advisory analyses.\n   - Explicitly note that legal analysis does not constitute formal legal counsel.\n\n4. **Approval Gate & Verification**:\n   - Record snapshot of ledger and state before presenting changes to human operator.\n"
