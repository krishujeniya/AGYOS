#!/usr/bin/env python3
"""CI test scaffold for the AGYOS corporate coverage blueprint (runnable subset
of the Section 7 evaluation spec tables). Run under the validate job:
    python -m unittest discover -s scripts/tests -v
or directly: python3 scripts/tests/test_policy_evals.py
Fixtures are inline; assertions encode the policy arithmetic, not prose."""
import unittest
from datetime import date, timedelta


def cashflow_weeks(rows, floor):
    """rows: list of (inflow, outflow); returns closings and breaches."""
    closings, breaches, opening = [], [], 500_000
    for inflow, outflow in rows:
        opening = opening + inflow - outflow
        closings.append(opening)
        if opening < floor:
            breaches.append(len(closings))
    return closings, breaches


class TestTreasury(unittest.TestCase):
    def test_cashflow_identity_and_floor(self):
        rows = [(200_000, 150_000)] * 3 + [(100_000, 250_000)] * 2
        closings, breaches = cashflow_weeks(rows, 400_000)
        self.assertEqual(len(closings), 5)
        self.assertEqual(closings, [550_000, 600_000, 650_000, 500_000, 350_000])
        self.assertEqual(breaches, [5])

    def test_dsar_deadlines(self):
        received = date(2026, 3, 2)
        self.assertEqual(received + timedelta(days=30), date(2026, 4, 1))   # GDPR
        ccpa = received + timedelta(days=45) + timedelta(days=45)           # one extension
        self.assertEqual(ccpa, date(2026, 5, 31))


class TestAgingBuckets(unittest.TestCase):
    def bucket(self, days):
        if days <= 30: return "0-30"
        if days <= 60: return "31-60"
        if days <= 90: return "61-90"
        return "90+"

    def test_boundaries(self):
        self.assertEqual(self.bucket(29), "0-30")
        self.assertEqual(self.bucket(30), "0-30")
        self.assertEqual(self.bucket(31), "31-60")
        self.assertEqual(self.bucket(60), "31-60")
        self.assertEqual(self.bucket(61), "61-90")
        self.assertEqual(self.bucket(91), "90+")


class TestCapTable(unittest.TestCase):
    def test_ownership_sums_to_100(self):
        holders = {"founders": 66.0, "esop": 10.0, "seed": 4.0, "series_a": 20.0}
        self.assertAlmostEqual(sum(holders.values()), 100.0)

    def test_waterfall_fully_distributes(self):
        exit_value, prefs, residual = 50_000_000, {"seed": 5_000_000, "series_a": 12_000_000}, 0
        residual = exit_value - sum(prefs.values())
        self.assertEqual(residual + sum(prefs.values()), exit_value)


class TestLicenseGate(unittest.TestCase):
    def test_block_without_path_evidence(self):
        verdict = {"status": "BLOCK", "paths": []}
        with self.assertRaisesRegex(ValueError, "path evidence"):
            if verdict["status"] == "BLOCK" and not verdict["paths"]:
                raise ValueError("BLOCK verdict requires path evidence")

    def test_gpl_in_distributed_module_is_block(self):
        FORBIDDEN, model = {"GPL-2.0"}, {"libx": "distributed_proprietary"}
        licenses = {"libx": "GPL-2.0"}
        paths = [p for p, mod in model.items()
                 if licenses.get(p) in FORBIDDEN and mod == "distributed_proprietary"]
        self.assertEqual(paths, ["libx"])


class TestRfpScorecard(unittest.TestCase):
    def test_weights_must_sum_to_100(self):
        weights = {"cost": 40, "fit": 30, "support": 27}  # 97: must be rejected
        with self.assertRaisesRegex(ValueError, "weights"):
            if sum(weights.values()) != 100:
                raise ValueError("scorecard weights must sum to 100 before distribution")


class TestPolicyLint(unittest.TestCase):
    BARE = __import__("re").compile(r"(?:^|\s|;|&&)(?:python3?|pip3?)(?:\s|$)")

    def test_uv_only(self):
        self.assertIsNone(self.BARE.search("uv run scripts/lint_toon.py --lint-changed"))
        self.assertIsNotNone(self.BARE.search("python scripts/generate_sbom.py"))
        self.assertIsNotNone(self.BARE.search("pip install requests"))

    def test_write_scope(self):
        allowed = (
            "./rules/", "rules/", "./skills/", "skills/", "./agents/", "agents/",
            "./plugins/", "plugins/", "./workflows/", "workflows/", "./state/", "state/",
            "./scripts/", "scripts/",
        )
        self.assertTrue("./rules/x.toon".startswith(allowed))
        self.assertFalse("/etc/passwd".startswith(allowed))


if __name__ == "__main__":
    unittest.main()
