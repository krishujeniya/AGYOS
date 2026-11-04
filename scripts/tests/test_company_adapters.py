"""Tests for AGYOS Company Adapters (Phase D: Dry-Run Company Operations).

Enforces:
1. CRMAdapter (pod-growth): lawful provenance, deduplication, non-binding quote drafts.
2. HelpdeskAdapter (pod-customer): ticket diagnosis, defect escalation contracts, R3 refund staging.
3. BillingFinanceAdapter (pod-gna): invoice variance reconciliation, payment proposal staging in outbox.
4. LegalAuditAdapter (pod-gna): liability and indemnity flagging, mandatory advisory disclaimer.
5. HiringScreenAdapter (pod-people): objective rubric scoring, zero automated rejections or offers.
"""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from agyos_decision.company_adapters import (
        BillingFinanceAdapter,
        CRMAdapter,
        HelpdeskAdapter,
        HiringScreenAdapter,
        LegalAuditAdapter,
    )
except ImportError:
    BillingFinanceAdapter = None
    CRMAdapter = None
    HelpdeskAdapter = None
    HiringScreenAdapter = None
    LegalAuditAdapter = None


class CRMAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(CRMAdapter, "CRMAdapter must be implemented")
        self.crm = CRMAdapter()

    def test_lead_requires_lawful_consent_metadata(self):
        # Missing consent/provenance must be rejected
        with self.assertRaises(ValueError) as ctx:
            self.crm.qualify_lead({"name": "John Doe", "email": "john@acme.com", "source": "unverified_list"})
        self.assertIn("provenance", str(ctx.exception).lower())

        # Valid lead with lawful consent succeeds
        lead = self.crm.qualify_lead({
            "name": "Jane Smith",
            "email": "jane@healthcorp.com",
            "source": "public_registrar",
            "consent_basis": "legitimate_interest_b2b",
        })
        self.assertEqual(lead["status"], "QUALIFIED_DRAFT")

    def test_sales_quote_high_discount_requires_approval(self):
        # Discount > 20% requires approval
        quote = self.crm.create_quote("opp_01", list_price=10000, discount_pct=25)
        self.assertTrue(quote["requires_approval"])
        self.assertEqual(quote["status"], "DRAFT_PENDING_APPROVAL")
        self.assertFalse(quote["is_binding"])


class HelpdeskAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(HelpdeskAdapter, "HelpdeskAdapter must be implemented")
        self.helpdesk = HelpdeskAdapter()

    def test_diagnose_ticket_and_escalate_bug(self):
        ticket = {
            "ticket_id": "tkt_842",
            "customer_id": "cust_10",
            "error_log": "500 Internal Server Error in POST /api/v1/checkout: null pointer in retry handler",
        }
        res = self.helpdesk.diagnose_ticket(ticket)
        self.assertEqual(res["diagnosis_status"], "REPRODUCIBLE_DEFECT")
        self.assertIsNotNone(res.get("bug_escalation_contract"))
        self.assertEqual(res["bug_escalation_contract"]["target_pod"], "pod-build")

    def test_refund_request_is_staged_in_outbox(self):
        res = self.helpdesk.request_refund(ticket_id="tkt_842", customer_id="cust_10", amount=500.0)
        self.assertEqual(res["risk"], "R3")
        self.assertEqual(res["outbox_status"], "PENDING_COMMIT")
        self.assertFalse(res["disbursed"])


class BillingFinanceAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BillingFinanceAdapter, "BillingFinanceAdapter must be implemented")
        self.finance = BillingFinanceAdapter()

    def test_reconcile_invoices_detects_variances(self):
        ledger = [{"invoice_id": "inv_01", "amount": 1000.0}, {"invoice_id": "inv_02", "amount": 2500.0}]
        invoices = [{"invoice_id": "inv_01", "amount": 1000.0}, {"invoice_id": "inv_02", "amount": 2650.0}]
        report = self.finance.reconcile(ledger, invoices)
        self.assertEqual(report["total_variance"], 150.0)
        self.assertEqual(len(report["discrepancies"]), 1)
        self.assertEqual(report["discrepancies"][0]["invoice_id"], "inv_02")

    def test_payment_proposal_staged_in_outbox(self):
        prop = self.finance.propose_payment(invoice_id="inv_01", amount=1000.0, vendor="Vendor Corp")
        self.assertEqual(prop["risk"], "R3")
        self.assertEqual(prop["outbox_status"], "PENDING_COMMIT")


class LegalAuditAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(LegalAuditAdapter, "LegalAuditAdapter must be implemented")
        self.legal = LegalAuditAdapter()

    def test_analyze_agreement_flags_clauses_and_includes_disclaimer(self):
        agreement_text = (
            "Section 8: Liability Limitation. In no event shall Supplier's liability exceed $10,000. "
            "Section 9: Indemnification. Customer shall fully indemnify Supplier against third party claims."
        )
        audit = self.legal.analyze_agreement(agreement_text)
        self.assertTrue(len(audit["flagged_clauses"]) >= 2)
        self.assertIn("advisory only", audit["disclaimer"].lower())
        self.assertFalse(audit["is_binding_clearance"])


class HiringScreenAdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(HiringScreenAdapter, "HiringScreenAdapter must be implemented")
        self.hiring = HiringScreenAdapter()

    def test_score_applicant_evaluates_rubric_without_automated_rejection(self):
        resume = "Senior Python engineer with 7 years experience in distributed systems, TDD, and asyncio."
        rubric = ["python", "distributed_systems", "tdd"]
        scorecard = self.hiring.score_applicant(candidate_id="cand_101", resume_text=resume, rubric=rubric)
        self.assertGreaterEqual(scorecard["match_score"], 0.8)
        self.assertIn("human hiring manager", scorecard["recommendation"].lower())
        self.assertFalse(scorecard["is_automated_decision"])


if __name__ == "__main__":
    unittest.main()
