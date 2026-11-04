"""Tests for Atomic-Claim Grounding & Verifier (P19, P20).

Enforces:
1. Decomposes outputs into atomic claims.
2. Checks claims against grounded truth facts.
3. Invariant: 0 unbacked numeric or contract claims.
"""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agyos_decision.verifier import extract_atomic_claims, verify_atomic_grounding


class AtomicClaimVerifierTests(unittest.TestCase):
    def test_extract_claims_finds_amounts_percentages_and_identifiers(self):
        text = "Task tsk_onboarding_01 completed with 100% precision. Reconciled $45,000 for snap_99."
        claims = extract_atomic_claims(text)
        types = [c.claim_type for c in claims]
        values = [c.extracted_value for c in claims]
        self.assertIn("identifier", types)
        self.assertIn("numeric", types)
        self.assertIn("currency", types)
        self.assertIn("tsk_onboarding_01", values)
        self.assertIn("100%", values)
        self.assertIn("$45,000", values)

    def test_grounded_claims_pass_with_zero_unbacked(self):
        text = "Processed tsk_fin_01 with variance $120.50 and 95% confidence."
        facts = {
            "task_id": "tsk_fin_01",
            "variance": "120.50",
            "confidence": "95%",
        }
        report = verify_atomic_grounding(text, facts)
        self.assertTrue(report.passed)
        self.assertEqual(report.unbacked_claims, 0)
        self.assertEqual(report.precision, 1.0)

    def test_unbacked_currency_claim_is_rejected(self):
        text = "Wire $50,000 to vendor account."
        facts = {
            "approved_amount": "10,000",  # Grounded amount is only $10,000!
        }
        report = verify_atomic_grounding(text, facts)
        self.assertFalse(report.passed, "Unbacked claim of $50,000 must fail verification")
        self.assertEqual(report.unbacked_claims, 1)
        self.assertEqual(report.grounded_claims, 0)


if __name__ == "__main__":
    unittest.main()
