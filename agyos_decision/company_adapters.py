"""AGYOS Company Adapters (Phase D: Dry-Run Company Operations).

Provides typed contracts and operational adapters across all 11 business functions:
- CRMAdapter: Marketing/Sales/Lead qualification with lawful provenance and non-binding quote drafts.
- HelpdeskAdapter: Customer ticket diagnosis, defect escalation to pod-build, and R3 refund staging.
- BillingFinanceAdapter: Invoice ledger variance reconciliation and R3 payment proposal staging.
- LegalAuditAdapter: Contract liability and indemnity risk analysis with advisory disclaimers.
- HiringScreenAdapter: Competency rubric screening with mandatory human hiring authority handoff.
"""

from __future__ import annotations

import re
import uuid
from typing import Any, Dict, List, Optional


class CRMAdapter:
    """Dry-run CRM adapter for pod-growth (Marketing, Leads, Sales)."""

    def qualify_lead(self, data: Dict[str, Any]) -> Dict[str, Any]:
        source = data.get("source", "").lower()
        consent = data.get("consent_basis", "").lower()

        if not consent or "unverified" in source:
            raise ValueError("Missing lawful provenance or consent basis: cannot qualify lead without consent metadata")

        return {
            "lead_id": f"lead_{uuid.uuid4().hex[:8]}",
            "name": data.get("name"),
            "email": data.get("email"),
            "source": source,
            "consent_basis": consent,
            "status": "QUALIFIED_DRAFT",
            "is_staged_only": True,
        }

    def create_quote(
        self,
        opportunity_id: str,
        list_price: float,
        discount_pct: float = 0.0,
    ) -> Dict[str, Any]:
        discount_amt = list_price * (discount_pct / 100.0)
        final_price = list_price - discount_amt
        requires_approval = (discount_pct > 20.0 or final_price > 10000.0)

        return {
            "quote_id": f"quote_{uuid.uuid4().hex[:8]}",
            "opportunity_id": opportunity_id,
            "list_price": list_price,
            "discount_pct": discount_pct,
            "final_price": round(final_price, 2),
            "requires_approval": requires_approval,
            "status": "DRAFT_PENDING_APPROVAL" if requires_approval else "DRAFT_READY",
            "is_binding": False,
        }


class HelpdeskAdapter:
    """Dry-run Support adapter for pod-customer (Onboarding, Support)."""

    def diagnose_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        error_log = ticket.get("error_log", "")
        ticket_id = ticket.get("ticket_id", "tkt_unknown")

        is_bug = any(term in error_log.lower() for term in ["500", "error", "exception", "null pointer", "timeout"])

        escalation_contract = None
        if is_bug:
            escalation_contract = {
                "contract_id": f"bug_{ticket_id}",
                "target_pod": "pod-build",
                "severity": "HIGH",
                "reproduction_evidence": error_log,
                "action": "isolate_root_cause_and_add_regression_test",
            }

        return {
            "ticket_id": ticket_id,
            "customer_id": ticket.get("customer_id"),
            "diagnosis_status": "REPRODUCIBLE_DEFECT" if is_bug else "POLICY_INQUIRY",
            "response_draft": f"Diagnosis completed for ticket {ticket_id}. Recommended resolution prepared.",
            "bug_escalation_contract": escalation_contract,
        }

    def request_refund(
        self,
        ticket_id: str,
        customer_id: str,
        amount: float,
    ) -> Dict[str, Any]:
        return {
            "refund_id": f"ref_{uuid.uuid4().hex[:8]}",
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "amount": round(amount, 2),
            "risk": "R3",
            "outbox_status": "PENDING_COMMIT",
            "disbursed": False,
            "requires_human_authorization": True,
        }


class BillingFinanceAdapter:
    """Dry-run Finance adapter for pod-gna (Finance, Legal, Operations)."""

    def reconcile(
        self,
        ledger: List[Dict[str, Any]],
        invoices: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        ledger_map = {item["invoice_id"]: item["amount"] for item in ledger}
        discrepancies: List[Dict[str, Any]] = []
        total_variance = 0.0

        for inv in invoices:
            inv_id = inv["invoice_id"]
            inv_amt = inv["amount"]
            ledger_amt = ledger_map.get(inv_id, 0.0)
            diff = abs(inv_amt - ledger_amt)
            if diff > 0.001:
                total_variance += diff
                discrepancies.append({
                    "invoice_id": inv_id,
                    "ledger_amount": ledger_amt,
                    "invoice_amount": inv_amt,
                    "variance": round(diff, 2),
                })

        return {
            "total_variance": round(total_variance, 2),
            "discrepancies": discrepancies,
            "audit_status": "VARIANCE_FLAGGED" if discrepancies else "RECONCILED_CLEAN",
            "mutated_balances": False,
        }

    def propose_payment(
        self,
        invoice_id: str,
        amount: float,
        vendor: str,
    ) -> Dict[str, Any]:
        return {
            "payment_proposal_id": f"pay_{uuid.uuid4().hex[:8]}",
            "invoice_id": invoice_id,
            "vendor": vendor,
            "amount": round(amount, 2),
            "risk": "R3",
            "outbox_status": "PENDING_COMMIT",
            "requires_fiduciary_authorization": True,
        }


class LegalAuditAdapter:
    """Dry-run Legal & Compliance adapter for pod-gna (Legal)."""

    def analyze_agreement(self, contract_text: str) -> Dict[str, Any]:
        flagged: List[Dict[str, str]] = []

        if re.search(r"liability\s+limitation|liability.*\$", contract_text, re.IGNORECASE):
            flagged.append({
                "clause": "Liability Limitation",
                "risk": "CAP_RESTRICTION",
                "finding": "Supplier liability capped; review against client standard risk threshold",
            })

        if re.search(r"indemnif", contract_text, re.IGNORECASE):
            flagged.append({
                "clause": "Indemnification",
                "risk": "INDEMNITY_EXPOSURE",
                "finding": "Customer indemnity obligation present; flag for mutual indemnity revision",
            })

        if re.search(r"governing\s+law", contract_text, re.IGNORECASE):
            flagged.append({
                "clause": "Governing Law",
                "risk": "JURISDICTION",
                "finding": "External jurisdiction specified; check compatibility with operating entity",
            })

        return {
            "flagged_clauses": flagged,
            "disclaimer": "Advisory only: does not constitute binding legal clearance. Formal execution requires human counsel.",
            "is_binding_clearance": False,
        }


class HiringScreenAdapter:
    """Dry-run Talent Screening adapter for pod-people (Hiring)."""

    def score_applicant(
        self,
        candidate_id: str,
        resume_text: str,
        rubric: List[str],
    ) -> Dict[str, Any]:
        lower_resume = resume_text.lower()
        matched_dims = [
            dim for dim in rubric
            if dim.lower() in lower_resume or dim.lower().replace("_", " ") in lower_resume
        ]
        match_score = len(matched_dims) / len(rubric) if rubric else 0.0

        return {
            "candidate_id": candidate_id,
            "rubric_total": len(rubric),
            "matched_competencies": matched_dims,
            "match_score": round(match_score, 2),
            "recommendation": "Human hiring manager interview determination required.",
            "is_automated_decision": False,
        }
