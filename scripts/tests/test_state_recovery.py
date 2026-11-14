"""Tests for AGYOS State, Budgets, Transactional Snapshots, Outbox, and Saga Recovery.

Enforces:
1. Hierarchy caps: 3 levels (depth <= 2), <= 4 children per node, <= 3 concurrent workers,
   <= 8 DAG tasks, <= 2 retries.
2. Run budget: 30k tokens, $1.50, 10 min, 40 tool calls with 20% reserved for verification and rollback.
3. Transactional snapshots and rollback restoration.
4. R3 Outbox hold queue with PENDING_COMMIT staging.
5. Reflection memory preventing identical failing retries.
6. LIFO Saga compensating transactions.
"""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from agyos_decision.contracts import Budget, TaskContract
    from agyos_decision.state_ledger import (
        DAGTaskGraph,
        HierarchyCapError,
        OutboxQueue,
        ReflectionMemory,
        RunBudgetTracker,
        SagaCoordinator,
        SnapshotManager,
    )
except ImportError as e:
    DAGTaskGraph = None
    HierarchyCapError = None
    OutboxQueue = None
    ReflectionMemory = None
    RunBudgetTracker = None
    SagaCoordinator = None
    SnapshotManager = None


class DAGHierarchyCapTests(unittest.TestCase):
    def test_rejected_insertion_preserves_both_graph_maps(self):
        import copy
        dag = DAGTaskGraph('atomic', max_children=1)
        dag.add_task('full-child', 1, ['full-parent'])
        before = copy.deepcopy((dag.tasks, dag.children_map))
        with self.assertRaises(HierarchyCapError):
            dag.add_task('rejected', 1, ['empty-parent', 'full-parent'])
        self.assertEqual((dag.tasks, dag.children_map), before)

    def test_duplicate_id_and_invalid_depth_do_not_overwrite_task(self):
        import copy
        dag = DAGTaskGraph('identity')
        dag.add_task('original', 0)
        before = copy.deepcopy((dag.tasks, dag.children_map))
        for task_id, depth in (('original', 1), ('new', -1), ('new', 0.5), ('new', True)):
            with self.subTest(task_id=task_id, depth=depth), self.assertRaises(ValueError):
                dag.add_task(task_id, depth)
            self.assertEqual((dag.tasks, dag.children_map), before)

    def setUp(self):
        self.assertIsNotNone(DAGTaskGraph, "DAGTaskGraph must be implemented")

    def test_dag_rejects_more_than_8_tasks(self):
        dag = DAGTaskGraph(run_id="run_cap_test")
        for i in range(8):
            dag.add_task(f"tsk_{i}", depth=1, dependencies=[])
        with self.assertRaises(HierarchyCapError) as ctx:
            dag.add_task("tsk_9", depth=1, dependencies=[])
        self.assertIn("8 tasks", str(ctx.exception))

    def test_dag_rejects_more_than_4_children_per_node(self):
        dag = DAGTaskGraph(run_id="run_fanout_test")
        dag.add_task("parent_0", depth=0, dependencies=[])
        for i in range(4):
            dag.add_task(f"child_{i}", depth=1, dependencies=["parent_0"])
        with self.assertRaises(HierarchyCapError) as ctx:
            dag.add_task("child_5", depth=1, dependencies=["parent_0"])
        self.assertIn("4 children", str(ctx.exception))

    def test_dag_rejects_depth_greater_than_2(self):
        dag = DAGTaskGraph(run_id="run_depth_test")
        dag.add_task("root", depth=0, dependencies=[])
        dag.add_task("l1", depth=1, dependencies=["root"])
        dag.add_task("l2", depth=2, dependencies=["l1"])
        with self.assertRaises(HierarchyCapError) as ctx:
            dag.add_task("l3", depth=3, dependencies=["l2"])
        self.assertIn("depth", str(ctx.exception).lower())

    def test_dag_rejects_cycles(self):
        dag = DAGTaskGraph(run_id="run_cycle_test")
        dag.add_task("a", depth=1, dependencies=["b"])
        dag.add_task("b", depth=1, dependencies=["a"])
        with self.assertRaises(ValueError) as ctx:
            dag.validate_acyclic()
        self.assertIn("cycle", str(ctx.exception).lower())

    def test_concurrent_worker_cap_max_3(self):
        dag = DAGTaskGraph(run_id="run_worker_test")
        dag.add_task("t1", depth=1, dependencies=[])
        dag.add_task("t2", depth=1, dependencies=[])
        dag.add_task("t3", depth=1, dependencies=[])
        dag.add_task("t4", depth=1, dependencies=[])
        self.assertEqual(dag.max_concurrent_workers, 3)
        active = dag.acquire_worker_slots(4)
        self.assertEqual(active, 3, "Concurrent worker execution must be capped at 3")


class RunBudgetEnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(RunBudgetTracker, "RunBudgetTracker must be implemented")

    def test_run_budget_envelope_caps(self):
        tracker = RunBudgetTracker(total_tokens=30000, total_usd=1.50, total_seconds=600, total_tool_calls=40)
        self.assertEqual(tracker.reserved_tokens, 6000)  # 20% reserved
        self.assertEqual(tracker.reserved_usd, 0.30)     # 20% reserved
        self.assertEqual(tracker.available_execution_tokens, 24000)
        self.assertEqual(tracker.available_execution_usd, 1.20)

    def test_exceeding_execution_budget_raises_error(self):
        tracker = RunBudgetTracker(total_tokens=30000, total_usd=1.50)
        tracker.consume(tokens=20000, usd=1.00, tool_calls=20)
        with self.assertRaises(ValueError) as ctx:
            # Consuming 5000 tokens exceeds available 24000 (reserving 6000 for verification/rollback)
            tracker.consume(tokens=5000, usd=0.30, tool_calls=15)
        self.assertIn("budget", str(ctx.exception).lower())


    def test_verification_reserve_is_accessible_only_for_verify_and_rollback(self):
        tracker = RunBudgetTracker(total_tokens=30000, total_usd=1.50)
        tracker.consume(tokens=24000, usd=1.20, tool_calls=30)
        # Regular task consumption fails
        with self.assertRaises(ValueError):
            tracker.consume(tokens=1000, usd=0.05, tool_calls=1)
        # Verification / rollback consumption succeeds using reserve
        tracker.consume_reserve(tokens=2000, usd=0.10, purpose="verification")
        self.assertEqual(tracker.used_tokens, 26000)


class TransactionalSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(SnapshotManager, "SnapshotManager must be implemented")

    def test_snapshot_capture_and_restore(self):
        mgr = SnapshotManager()
        state = {"balance": 1000, "status": "active", "files": ["doc1.md"]}
        snap_id = mgr.create_snapshot("snap_01", state)

        # Mutate state
        mutated_state = {"balance": 500, "status": "suspended", "files": ["doc1.md", "doc2.md"]}
        mgr.record_mutation(snap_id, mutated_state)

        # Restore
        restored = mgr.rollback(snap_id)
        self.assertEqual(restored["balance"], 1000)
        self.assertEqual(restored["status"], "active")
        self.assertEqual(restored["files"], ["doc1.md"])


class OutboxHoldQueueTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(OutboxQueue, "OutboxQueue must be implemented")

    def test_r3_action_staged_in_outbox(self):
        outbox = OutboxQueue()
        action = {
            "task_id": "tsk_wire_01",
            "action_type": "bank_transfer",
            "payload": {"amount": 50000, "recipient": "Vendor A"},
        }
        item_id = outbox.stage_action(action)
        self.assertEqual(outbox.get_status(item_id), "PENDING_COMMIT")
        self.assertFalse(outbox.is_committed(item_id))

        # Explicit human commit
        outbox.commit_action(item_id, authorized_by="operator")
        self.assertEqual(outbox.get_status(item_id), "COMMITTED")
        self.assertTrue(outbox.is_committed(item_id))

    def test_outbox_abort_cancels_action(self):
        outbox = OutboxQueue()
        action = {
            "task_id": "tsk_refund_01",
            "action_type": "refund",
            "payload": {"amount": 1200},
        }
        item_id = outbox.stage_action(action)
        outbox.abort_action(item_id, reason="operator rejected")
        self.assertEqual(outbox.get_status(item_id), "ABORTED")

    def test_terminal_outbox_states_cannot_be_overwritten(self):
        outbox = OutboxQueue()
        committed = outbox.stage_action({"action_type": "publish"})
        outbox.commit_action(committed, authorized_by="operator")
        with self.assertRaises(ValueError):
            outbox.abort_action(committed, reason="too late")
        self.assertEqual(outbox.get_status(committed), "COMMITTED")

        aborted = outbox.stage_action({"action_type": "transfer"})
        outbox.abort_action(aborted, reason="operator rejected")
        with self.assertRaises(ValueError):
            outbox.commit_action(aborted, authorized_by="operator")
        self.assertEqual(outbox.get_status(aborted), "ABORTED")

    def test_outbox_requires_authorization_identity_before_commit(self):
        outbox = OutboxQueue()
        item_id = outbox.stage_action({"action_type": "publish"})
        with self.assertRaises(ValueError):
            outbox.commit_action(item_id, authorized_by=" ")
        self.assertEqual(outbox.get_status(item_id), "PENDING_COMMIT")


class ReflectionMemoryTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(ReflectionMemory, "ReflectionMemory must be implemented")

    def test_reflection_prevents_identical_retry(self):
        memory = ReflectionMemory()
        error_sig = "TimeoutError: connection to db timed out after 30s"
        memory.record_attempt(task_id="tsk_db_01", hypothesis="increase pool size", error_signature=error_sig)

        # Attempting exact same hypothesis and error signature must be rejected
        is_duplicate = memory.is_identical_retry("tsk_db_01", hypothesis="increase pool size", error_signature=error_sig)
        self.assertTrue(is_duplicate, "Identical retry must be detected and blocked per Invariant 6")

        # Changed hypothesis is permitted
        is_diff = memory.is_identical_retry("tsk_db_01", hypothesis="check firewall routing", error_signature=error_sig)
        self.assertFalse(is_diff)

    def test_max_retries_capped_at_2(self):
        memory = ReflectionMemory()
        memory.record_attempt("tsk_01", "hypo 1", "err 1")
        memory.record_attempt("tsk_01", "hypo 2", "err 2")
        self.assertTrue(memory.can_retry("tsk_01"))  # 2 attempts recorded, max retries is 2
        memory.record_attempt("tsk_01", "hypo 3", "err 3")
        self.assertFalse(memory.can_retry("tsk_01"), "More than 2 retries must be blocked")


class LIFOSagaCompensationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(SagaCoordinator, "SagaCoordinator must be implemented")

    def test_saga_compensates_in_reverse_lifo_order(self):
        saga = SagaCoordinator(saga_id="saga_order_01")
        execution_order = []

        def comp1():
            execution_order.append("C1")

        def comp2():
            execution_order.append("C2")

        def comp3():
            execution_order.append("C3")

        saga.register_step("step1", comp1)
        saga.register_step("step2", comp2)
        saga.register_step("step3", comp3)

        # Trigger rollback
        saga.rollback()

        # Must execute LIFO: step3 compensation, then step2, then step1
        self.assertEqual(execution_order, ["C3", "C2", "C1"],
                         f"Saga compensation must be strictly LIFO, got {execution_order}")
        self.assertEqual(saga.status, "COMPENSATED")

    def test_saga_rejects_steps_and_repeated_rollback_after_completion(self):
        saga = SagaCoordinator(saga_id="saga_terminal_01")
        saga.register_step("step1", lambda: None)
        saga.rollback()
        with self.assertRaises(RuntimeError):
            saga.register_step("step2", lambda: None)
        with self.assertRaises(RuntimeError):
            saga.rollback()

    def test_failed_saga_compensation_is_terminal_and_not_replayed(self):
        saga = SagaCoordinator(saga_id="saga_retry_01")
        execution_order = []

        def compensate_step2():
            execution_order.append("step2")
            raise RuntimeError("compensation failure")

        saga.register_step("step1", lambda: execution_order.append("step1"))
        saga.register_step("step2", compensate_step2)
        with self.assertRaisesRegex(RuntimeError, "compensation failure"):
            saga.rollback()
        self.assertEqual(saga.status, "COMPENSATION_FAILED")
        with self.assertRaisesRegex(RuntimeError, "COMPENSATION_FAILED"):
            saga.rollback()
        self.assertEqual(execution_order, ["step2"])


if __name__ == "__main__":
    unittest.main()
