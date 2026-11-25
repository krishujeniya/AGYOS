"""Tests for AGYOS Unified Query Optimization Engine.

Validates:
1. End-to-end query translation across multiple company domains (engineering, growth, finance, legal).
2. Proper role assignment from 104-role matrix and skill selection from 2,247 catalog.
3. Amazon Working Backwards EVPI clarification and safe default assumptions.
4. Tri-Format KV-cache prompt envelope structure (static prefix + dynamic suffix).
5. XML serialization and compact minification validity.
6. Validation of input boundaries and exception safety.
"""

from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agyos_decision.query_optimizer import optimize_query, OptimizedQueryPlan
from agyos_decision.toon_codec import decode_toon


class TestQueryOptimizer(unittest.TestCase):
    def test_engineering_query_optimization(self):
        query = "Fix database connection pooling and deadlock in FastAPI service"
        plan = optimize_query(query)

        self.assertIsInstance(plan, OptimizedQueryPlan)
        self.assertEqual(plan.governing_pod, "pod-build")
        self.assertIn(plan.role_id, ("role-backend-engineer", "role-database-reliability-eng", "role-swe", "role-senior-swe"))
        self.assertIsNotNone(plan.primary_skill)
        self.assertIn(plan.model_provider, ("google", "anthropic"))
        self.assertGreater(plan.token_budget, 0)
        self.assertGreater(plan.cost_ceiling_usd, 0.0)

        # Prompt cache prefix must be non-empty and valid XML
        agent_root = ET.fromstring(plan.static_prefix_xml)
        self.assertEqual(agent_root.tag, "agyos_agent")
        task_root = ET.fromstring(plan.dynamic_suffix_xml)
        self.assertEqual(task_root.tag, "agyos_task")

    def test_growth_marketing_query_optimization(self):
        query = "Draft launch announcement and social marketing campaign for new SaaS feature"
        plan = optimize_query(query)

        self.assertEqual(plan.governing_pod, "pod-growth")
        self.assertIn(plan.role_id, ("role-growth-pm", "role-cmo", "role-content-strategist", "role-brand-copywriter", "role-performance-marketer"))
        self.assertFalse(plan.evpi_should_ask)
        self.assertGreater(len(plan.assumptions), 0)

    def test_finance_query_optimization(self):
        query = "Analyze quarterly budget variance and reconcile stripe payment fees"
        plan = optimize_query(query)

        self.assertEqual(plan.governing_pod, "pod-gna")
        self.assertIn(plan.role_id, ("role-fp-and-a-analyst", "role-corporate-controller", "role-cfo", "role-accounts-manager"))
        self.assertEqual(plan.risk, "R0")

    def test_legal_query_optimization(self):
        query = "Review mutual non-disclosure agreement and flag liability clauses"
        plan = optimize_query(query)

        self.assertEqual(plan.governing_pod, "pod-gna")
        self.assertIn(plan.role_id, ("role-contract-manager", "role-general-counsel", "role-compliance-officer"))
        self.assertEqual(plan.risk, "R0")

    def test_xml_output_and_compact_minification(self):
        query = "Implement robust user authentication endpoint with rate limiting"
        plan = optimize_query(query, compact=False)
        xml_pretty = plan.to_xml(compact=False)
        xml_compact = plan.to_xml(compact=True)

        self.assertLess(len(xml_compact), len(xml_pretty))

        # Both must parse cleanly as XML
        root_pretty = ET.fromstring(xml_pretty)
        root_compact = ET.fromstring(xml_compact)
        self.assertEqual(root_pretty.tag, "agyos_optimized_query")
        self.assertEqual(root_compact.tag, "agyos_optimized_query")

        # Verify envelope structure
        self.assertIsNotNone(root_pretty.find("assignment"))
        self.assertIsNotNone(root_pretty.find("clarification"))
        self.assertIsNotNone(root_pretty.find("prompt_envelope"))

    def test_to_dict_serialization(self):
        query = "Design architecture for scalable multi-tenant SaaS"
        plan = optimize_query(query)
        data = plan.to_dict()

        self.assertIn("query", data)
        self.assertIn("role", data)
        self.assertIn("routing", data)
        self.assertIn("evpi", data)
        self.assertIn("model_economics", data)
        self.assertIn("prompt_cache", data)
        self.assertEqual(data["query"], query)

    def test_empty_query_raises_value_error(self):
        with self.assertRaises(ValueError):
            optimize_query("")
        with self.assertRaises(ValueError):
            optimize_query("   ")


if __name__ == "__main__":
    unittest.main()
