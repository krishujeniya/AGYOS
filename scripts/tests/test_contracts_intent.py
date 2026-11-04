"""Tests for TaskContract schema, Intent Compilation, and EVPI Clarification.

Enforces:
1. Typed TaskContracts matching contracts.schema.json.
2. Natural language intent routing across all 11 company functions into 5 merged pods.
3. EVPI clarification (at most 1 short question when consequential, 0 when benign).
4. Hierarchy depth caps (depth <= 2) and budget envelopes (tokens <= 30k, usd <= $1.50).
5. Single-agent baseline execution contract.
"""

import json
from pathlib import Path
import sys
import unittest
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCHEMA_PATH = ROOT / "agyos_decision" / "contracts.schema.json"
FIXTURES_PATH = ROOT / "scripts" / "tests" / "fixtures" / "business_tasks.json"

# Import target modules
try:
    from agyos_decision.contracts import TaskContract, validate_contract
    from agyos_decision.intent_compiler import compile_intent
    from agyos_decision.evpi_clarify import evaluate_evpi
except ImportError as e:
    raise RuntimeError(f"Failed to import modules from ROOT={ROOT}: {e}")


class ContractSchemaTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCHEMA_PATH.exists(), f"Schema missing at {SCHEMA_PATH}")
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_schema_itself_is_valid_json_schema(self):
        jsonschema.Draft202012Validator.check_schema(self.schema)

    def test_valid_contract_passes_schema(self):
        valid_contract = {
            "task_id": "tsk_test_01",
            "run_id": "run_001",
            "parent_task_id": None,
            "tenant_id": "tenant_default",
            "requester_id": "user_operator",
            "depth": 0,
            "pod": "pod-growth",
            "objective": "Draft launch announcement for new feature",
            "assumptions": ["developer audience", "professional tone"],
            "inputs": [{"ref": "art_01", "trust": "untrusted", "version": "v1"}],
            "dependencies": [],
            "allowed_actions": ["read:crm", "write:draft"],
            "forbidden_actions": ["send:external", "charge:payment"],
            "capability_allowlist": ["read:crm", "write:draft"],
            "approval": {"required": False, "scope": None, "expires_at": None, "status": "approved"},
            "acceptance": [
                {"type": "schema", "schema_id": "launch-draft-v1"},
                {"type": "postcondition", "check": "draft_exists"}
            ],
            "budget": {
                "tokens": 12000,
                "usd": 0.50,
                "seconds": 180,
                "tool_calls": 20,
                "max_retries": 2
            },
            "idempotency_key": "idem_tsk_test_01",
            "risk": "R1",
            "preconditions": ["state.initialized"],
            "postconditions": {
                "output_schema_ref": "launch-draft-v1",
                "verifier_cmd": "scripts/agyos-verify.sh --task",
                "required_claims_grounded": True
            },
            "compensation": {
                "kind": "delete_draft",
                "resource_ref": "art_01",
                "rollback_cmd": "rm -f art_01",
                "snapshot_id": "snap_001"
            },
            "result": {
                "status": "pending",
                "artifacts": [],
                "proofs": [],
                "uncertainty": []
            }
        }
        jsonschema.validate(instance=valid_contract, schema=self.schema)

    def test_depth_greater_than_2_is_rejected(self):
        contract = {
            "task_id": "tsk_depth_3",
            "run_id": "run_001",
            "parent_task_id": "tsk_depth_2",
            "tenant_id": "t1",
            "requester_id": "r1",
            "depth": 3,  # Exceeds max 2 (3 total levels: 0, 1, 2)
            "pod": "pod-build",
            "objective": "Sub-sub-sub task",
            "assumptions": [],
            "inputs": [],
            "dependencies": [],
            "allowed_actions": ["read_file"],
            "forbidden_actions": [],
            "capability_allowlist": ["read_file"],
            "approval": {"required": False, "scope": None, "expires_at": None, "status": "approved"},
            "acceptance": [],
            "budget": {"tokens": 5000, "usd": 0.20, "seconds": 60, "tool_calls": 10, "max_retries": 1},
            "idempotency_key": "idem_d3",
            "risk": "R0",
            "preconditions": ["ready"],
            "postconditions": {"output_schema_ref": "any", "verifier_cmd": "echo", "required_claims_grounded": True},
            "compensation": {"kind": "noop", "resource_ref": "none", "rollback_cmd": "true", "snapshot_id": "snap_0"},
            "result": {"status": "pending", "artifacts": [], "proofs": [], "uncertainty": []}
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=contract, schema=self.schema)

    def test_budget_exceeding_run_cap_is_rejected(self):
        contract = {
            "task_id": "tsk_budget_violation",
            "run_id": "run_001",
            "parent_task_id": None,
            "tenant_id": "t1",
            "requester_id": "r1",
            "depth": 0,
            "pod": "pod-build",
            "objective": "Excessive budget task",
            "assumptions": [],
            "inputs": [],
            "dependencies": [],
            "allowed_actions": ["read_file"],
            "forbidden_actions": [],
            "capability_allowlist": ["read_file"],
            "approval": {"required": False, "scope": None, "expires_at": None, "status": "approved"},
            "acceptance": [],
            "budget": {
                "tokens": 40000,  # Cap is 30,000
                "usd": 2.50,      # Cap is $1.50
                "seconds": 700,   # Cap is 600s (10 min)
                "tool_calls": 50, # Cap is 40
                "max_retries": 3  # Cap is 2
            },
            "idempotency_key": "idem_bv",
            "risk": "R0",
            "preconditions": ["ready"],
            "postconditions": {"output_schema_ref": "any", "verifier_cmd": "echo", "required_claims_grounded": True},
            "compensation": {"kind": "noop", "resource_ref": "none", "rollback_cmd": "true", "snapshot_id": "snap_0"},
            "result": {"status": "pending", "artifacts": [], "proofs": [], "uncertainty": []}
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=contract, schema=self.schema)

    def test_invalid_pod_name_is_rejected(self):
        contract = {
            "task_id": "tsk_bad_pod",
            "run_id": "run_001",
            "parent_task_id": None,
            "tenant_id": "t1",
            "requester_id": "r1",
            "depth": 0,
            "pod": "pod-marketing-standalone",  # Must be one of the 5 merged pods
            "objective": "Task with unmerged pod",
            "assumptions": [],
            "inputs": [],
            "dependencies": [],
            "allowed_actions": ["read_file"],
            "forbidden_actions": [],
            "capability_allowlist": ["read_file"],
            "approval": {"required": False, "scope": None, "expires_at": None, "status": "approved"},
            "acceptance": [],
            "budget": {"tokens": 5000, "usd": 0.20, "seconds": 60, "tool_calls": 10, "max_retries": 1},
            "idempotency_key": "idem_bp",
            "risk": "R0",
            "preconditions": ["ready"],
            "postconditions": {"output_schema_ref": "any", "verifier_cmd": "echo", "required_claims_grounded": True},
            "compensation": {"kind": "noop", "resource_ref": "none", "rollback_cmd": "true", "snapshot_id": "snap_0"},
            "result": {"status": "pending", "artifacts": [], "proofs": [], "uncertainty": []}
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=contract, schema=self.schema)


class IntentCompilationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(compile_intent, "compile_intent must be implemented")
        fixtures_data = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
        self.fixtures = fixtures_data["tasks"]

    def test_all_11_company_functions_compile_to_correct_5_pods(self):
        for item in self.fixtures:
            with self.subTest(task_id=item["id"], function=item["function"]):
                contract = compile_intent(item["prompt"])
                self.assertIsInstance(contract, TaskContract)
                self.assertEqual(contract.pod, item["expected_pod"],
                                 f"Prompt '{item['prompt']}' mapped to {contract.pod}, expected {item['expected_pod']}")
                self.assertEqual(contract.risk, item["expected_risk"],
                                 f"Prompt '{item['prompt']}' risk {contract.risk}, expected {item['expected_risk']}")
                # Ensure the compiled contract validates against schema
                validate_contract(contract)

    def test_zero_slash_commands_or_agent_keywords_required(self):
        raw_prompt = "we need to analyze why client payments are delayed and prepare an invoice reconciliation sheet"
        contract = compile_intent(raw_prompt)
        self.assertEqual(contract.pod, "pod-gna")
        self.assertEqual(contract.risk, "R0")
        self.assertNotIn("/", raw_prompt)


class EVPIClarificationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(evaluate_evpi, "evaluate_evpi must be implemented")
        fixtures_data = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
        self.fixtures = fixtures_data["tasks"]

    def test_benign_ambiguity_asks_zero_questions_and_records_assumptions(self):
        benign_items = [f for f in self.fixtures if f["ambiguity_type"] == "benign"]
        for item in benign_items:
            with self.subTest(task_id=item["id"]):
                contract = compile_intent(item["prompt"])
                decision = evaluate_evpi(item["prompt"], contract)
                self.assertFalse(decision.should_ask_question,
                                 f"Task {item['id']} should not ask questions")
                self.assertIsNone(decision.question)
                self.assertTrue(len(contract.assumptions) > 0,
                                f"Task {item['id']} must record explicit assumptions")
                self.assertTrue(decision.proceed_immediately)
                header = decision.format_assumptions_header()
                self.assertIn("Assumptions Applied", header)

    def test_consequential_ambiguity_and_r3_asks_at_most_one_short_question(self):
        consequential_items = [f for f in self.fixtures if f["ambiguity_type"] == "consequential"]
        for item in consequential_items:
            with self.subTest(task_id=item["id"]):
                contract = compile_intent(item["prompt"])
                decision = evaluate_evpi(item["prompt"], contract)
                self.assertTrue(decision.should_ask_question,
                                f"Task {item['id']} must ask question for safety")
                self.assertIsNotNone(decision.question)
                # Word count strictly <= 25 words
                words = decision.question.split()
                self.assertLessEqual(len(words), 25,
                                     f"Question '{decision.question}' exceeds 25 words ({len(words)} words)")
                # Must be staged in outbox hold queue if R3
                if contract.risk == "R3":
                    self.assertEqual(decision.outbox_status, "PENDING_COMMIT")


if __name__ == "__main__":
    unittest.main()
