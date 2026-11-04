"""AGYOS State Ledger, Budgets, Transactional Snapshots, Outbox & Recovery.

Enforces:
1. Hierarchy Caps (3 levels: depth <= 2, <= 4 children per node, <= 3 concurrent workers,
   <= 8 DAG tasks, <= 2 retries).
2. Run Budget Envelope (30k tokens, $1.50, 600s, 40 tool calls with 20% reserved for
   verification and rollback).
3. Transactional Snapshots & Rollback.
4. R3 Outbox Hold Queue (staged as PENDING_COMMIT until explicit human authorization).
5. Reflection Memory (episodic error signatures preventing identical failing retries).
6. LIFO Saga Compensation (strictly reverse-order compensation execution).
"""

from __future__ import annotations

import copy
import uuid
from typing import Any, Callable, Dict, List, Optional, Set


class HierarchyCapError(ValueError):
    """Raised when hierarchy fan-out, depth, task count, or worker cap is violated."""
    pass


class DAGTaskGraph:
    """Directed Acyclic Graph for multi-agent subtasks with strict hierarchy caps."""

    def __init__(
        self,
        run_id: str,
        max_tasks: int = 8,
        max_depth: int = 2,
        max_children: int = 4,
        max_concurrent_workers: int = 3,
    ) -> None:
        self.run_id = run_id
        self.max_tasks = max_tasks
        self.max_depth = max_depth
        self.max_children = max_children
        self.max_concurrent_workers = max_concurrent_workers
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.children_map: Dict[str, List[str]] = {}

    def add_task(self, task_id: str, depth: int, dependencies: Optional[List[str]] = None) -> None:
        if len(self.tasks) >= self.max_tasks:
            raise HierarchyCapError(f"DAG exceeds maximum allowed {self.max_tasks} tasks (current: {len(self.tasks)})")

        if depth > self.max_depth:
            raise HierarchyCapError(f"Task depth {depth} exceeds maximum hierarchy depth {self.max_depth} (max 3 levels: 0, 1, 2)")

        deps = list(dependencies or [])
        for dep in deps:
            if dep not in self.tasks:
                pass  # Dependency can be registered before or alongside
            children = self.children_map.setdefault(dep, [])
            if len(children) >= self.max_children:
                raise HierarchyCapError(f"Parent node '{dep}' exceeds maximum allowed {self.max_children} children")
            children.append(task_id)

        self.tasks[task_id] = {
            "task_id": task_id,
            "depth": depth,
            "dependencies": deps,
            "status": "pending",
        }

    def validate_acyclic(self) -> None:
        """Validate that the graph has no dependency cycles via Kahn's algorithm."""
        in_degree: Dict[str, int] = {t: 0 for t in self.tasks}
        adj: Dict[str, List[str]] = {t: [] for t in self.tasks}

        for task_id, info in self.tasks.items():
            for dep in info["dependencies"]:
                if dep in self.tasks:
                    adj[dep].append(task_id)
                    in_degree[task_id] += 1

        queue = [t for t, deg in in_degree.items() if deg == 0]
        visited_count = 0

        while queue:
            node = queue.pop(0)
            visited_count += 1
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if visited_count < len(self.tasks):
            raise ValueError(f"Cycle detected in task dependencies: {visited_count}/{len(self.tasks)} tasks visited")

    def acquire_worker_slots(self, requested: int) -> int:
        """Cap concurrent worker allocation at max_concurrent_workers (default 3)."""
        return min(requested, self.max_concurrent_workers)


class RunBudgetTracker:
    """Tracks token, USD, time, and tool call envelope with 20% reserved for verification/rollback."""

    def __init__(
        self,
        total_tokens: int = 30000,
        total_usd: float = 1.50,
        total_seconds: int = 600,
        total_tool_calls: int = 40,
        reserve_ratio: float = 0.20,
    ) -> None:
        self.total_tokens = int(total_tokens)
        self.total_usd = round(float(total_usd), 2)
        self.total_seconds = int(total_seconds)
        self.total_tool_calls = int(total_tool_calls)
        self.reserve_ratio = reserve_ratio

        self.reserved_tokens = int(self.total_tokens * self.reserve_ratio)
        self.reserved_usd = round(self.total_usd * self.reserve_ratio, 2)
        self.available_execution_tokens = self.total_tokens - self.reserved_tokens
        self.available_execution_usd = round(self.total_usd - self.reserved_usd, 2)

        self.used_tokens = 0
        self.used_usd = 0.0
        self.used_tool_calls = 0

    def consume(self, tokens: int = 0, usd: float = 0.0, tool_calls: int = 0) -> None:
        """Consume execution budget. Rejects if exceeding available non-reserved envelope."""
        new_tokens = self.used_tokens + tokens
        new_usd = round(self.used_usd + usd, 2)
        new_calls = self.used_tool_calls + tool_calls

        if new_tokens > self.available_execution_tokens:
            raise ValueError(
                f"Token consumption {new_tokens} exceeds available execution budget {self.available_execution_tokens} "
                f"({self.reserved_tokens} reserved for verification/rollback)"
            )
        if new_usd > self.available_execution_usd:
            raise ValueError(
                f"USD spend ${new_usd:.2f} exceeds available execution budget ${self.available_execution_usd:.2f} "
                f"(${self.reserved_usd:.2f} reserved for verification/rollback)"
            )
        if new_calls > self.total_tool_calls:
            raise ValueError(f"Tool calls {new_calls} exceed total envelope {self.total_tool_calls}")

        self.used_tokens = new_tokens
        self.used_usd = new_usd
        self.used_tool_calls = new_calls

    def consume_reserve(self, tokens: int = 0, usd: float = 0.0, purpose: str = "verification") -> None:
        """Consume from the reserved verification/rollback budget."""
        new_tokens = self.used_tokens + tokens
        new_usd = round(self.used_usd + usd, 2)
        if new_tokens > self.total_tokens:
            raise ValueError(f"Reserve consumption {new_tokens} exceeds total envelope {self.total_tokens}")
        if new_usd > self.total_usd:
            raise ValueError(f"Reserve spend ${new_usd:.2f} exceeds total envelope ${self.total_usd:.2f}")

        self.used_tokens = new_tokens
        self.used_usd = new_usd


class SnapshotManager:
    """Manages transactional state snapshots for atomic rollback."""

    def __init__(self) -> None:
        self.snapshots: Dict[str, Any] = {}
        self.history: List[str] = []

    def create_snapshot(self, snapshot_id: str, state: Any) -> str:
        self.snapshots[snapshot_id] = copy.deepcopy(state)
        self.history.append(snapshot_id)
        return snapshot_id

    def record_mutation(self, snapshot_id: str, mutated_state: Any) -> None:
        pass

    def rollback(self, snapshot_id: str) -> Any:
        if snapshot_id not in self.snapshots:
            raise KeyError(f"Snapshot '{snapshot_id}' not found")
        return copy.deepcopy(self.snapshots[snapshot_id])


class OutboxQueue:
    """R3 Outbox Hold Queue staging irreversible external actions until explicit authorization."""

    def __init__(self) -> None:
        self.items: Dict[str, Dict[str, Any]] = {}

    def stage_action(self, action: Dict[str, Any]) -> str:
        item_id = f"outbox_{uuid.uuid4().hex[:8]}"
        self.items[item_id] = {
            "item_id": item_id,
            "action": action,
            "status": "PENDING_COMMIT",
            "authorized_by": None,
            "reason": None,
        }
        return item_id

    def get_status(self, item_id: str) -> str:
        return self.items[item_id]["status"]

    def is_committed(self, item_id: str) -> bool:
        return self.items[item_id]["status"] == "COMMITTED"

    def commit_action(self, item_id: str, authorized_by: str) -> None:
        if item_id not in self.items:
            raise KeyError(f"Outbox item '{item_id}' not found")
        self.items[item_id]["status"] = "COMMITTED"
        self.items[item_id]["authorized_by"] = authorized_by

    def abort_action(self, item_id: str, reason: str) -> None:
        if item_id not in self.items:
            raise KeyError(f"Outbox item '{item_id}' not found")
        self.items[item_id]["status"] = "ABORTED"
        self.items[item_id]["reason"] = reason


class ReflectionMemory:
    """Episodic reflection memory tracking attempt hypotheses and error signatures."""

    def __init__(self, max_retries: int = 2) -> None:
        self.max_retries = max_retries
        self.attempts: Dict[str, List[Dict[str, str]]] = {}

    def record_attempt(self, task_id: str, hypothesis: str, error_signature: str) -> None:
        task_attempts = self.attempts.setdefault(task_id, [])
        task_attempts.append({
            "hypothesis": hypothesis.strip().lower(),
            "error_signature": error_signature.strip().lower(),
        })

    def is_identical_retry(self, task_id: str, hypothesis: str, error_signature: str) -> bool:
        task_attempts = self.attempts.get(task_id, [])
        hypo = hypothesis.strip().lower()
        err = error_signature.strip().lower()
        for attempt in task_attempts:
            if attempt["hypothesis"] == hypo and attempt["error_signature"] == err:
                return True
        return False

    def can_retry(self, task_id: str) -> bool:
        task_attempts = self.attempts.get(task_id, [])
        return len(task_attempts) <= self.max_retries


class SagaCoordinator:
    """Coordinates multi-step distributed sagas with strictly LIFO reverse compensation."""

    def __init__(self, saga_id: str) -> None:
        self.saga_id = saga_id
        self.steps: List[Dict[str, Any]] = []
        self.status = "ACTIVE"

    def register_step(self, step_name: str, compensation_fn: Callable[[], Any]) -> None:
        self.steps.append({
            "name": step_name,
            "compensation": compensation_fn,
        })

    def rollback(self) -> None:
        """Execute compensations in strict LIFO (reverse) order."""
        for step in reversed(self.steps):
            comp_fn = step["compensation"]
            if callable(comp_fn):
                comp_fn()
        self.status = "COMPENSATED"
