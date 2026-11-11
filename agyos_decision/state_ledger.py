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
from decimal import Decimal
from fractions import Fraction
import math
import time
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
        if task_id in self.tasks:
            raise HierarchyCapError(f"Duplicate task id: {task_id}")
        if isinstance(depth, bool) or not isinstance(depth, int) or depth < 0:
            raise HierarchyCapError("Task depth must be a nonnegative integer")
        if len(self.tasks) >= self.max_tasks:
            raise HierarchyCapError(f"DAG exceeds maximum allowed {self.max_tasks} tasks (current: {len(self.tasks)})")

        if depth > self.max_depth:
            raise HierarchyCapError(f"Task depth {depth} exceeds maximum hierarchy depth {self.max_depth} (max 3 levels: 0, 1, 2)")

        deps = list(dependencies or [])
        if len(set(deps)) != len(deps):
            raise HierarchyCapError("Duplicate dependencies are not allowed")
        for dep in deps:
            children = self.children_map.get(dep, [])
            if len(children) >= self.max_children:
                raise HierarchyCapError(f"Parent node '{dep}' exceeds maximum allowed {self.max_children} children")

        task = {
            "task_id": task_id,
            "depth": depth,
            "dependencies": deps,
            "status": "pending",
        }
        # Forward references remain valid; publish only after all checks succeed.
        self.children_map = {
            **self.children_map,
            **{dep: [*self.children_map.get(dep, []), task_id] for dep in deps},
        }
        self.tasks = {**self.tasks, task_id: task}

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


def _budget_count(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _budget_decimal(value: float, name: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f"{name} must be a finite nonnegative number")
    number = Decimal(str(value))
    if not number.is_finite() or number < 0:
        raise ValueError(f"{name} must be a finite nonnegative number")
    return number


class RunBudgetTracker:
    """Single-owner accounting; callers must check before dispatching each tool.

    Exact rational USD accumulation preserves decimal charges independently of
    the caller's decimal context. Deadlines are checked on
    consumption; this class cannot cancel a running tool or authenticate callers.
    """

    def __init__(
        self,
        total_tokens: int = 30000,
        total_usd: float = 1.50,
        total_seconds: int = 600,
        total_tool_calls: int = 40,
        reserve_ratio: float = 0.20,
        *,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.total_tokens = _budget_count(total_tokens, "total_tokens")
        self._total_usd = Fraction(_budget_decimal(total_usd, "total_usd"))
        self.total_usd = float(self._total_usd)
        self.total_seconds = _budget_count(total_seconds, "total_seconds")
        self.total_tool_calls = _budget_count(total_tool_calls, "total_tool_calls")
        ratio = Fraction(_budget_decimal(reserve_ratio, "reserve_ratio"))
        if ratio >= 1:
            raise ValueError("reserve_ratio must be less than one")
        self.reserve_ratio = float(ratio)

        self.reserved_tokens = int(self.total_tokens * ratio)
        self._reserved_usd = self._total_usd * ratio
        self.reserved_usd = float(self._reserved_usd)
        self.available_execution_tokens = self.total_tokens - self.reserved_tokens
        self._execution_usd = self._total_usd - self._reserved_usd
        self.available_execution_usd = float(self._execution_usd)
        self.reserved_tool_calls = int(self.total_tool_calls * ratio)
        self.available_execution_tool_calls = self.total_tool_calls - self.reserved_tool_calls
        self.available_execution_seconds = float(self.total_seconds * (1 - ratio))
        self._clock = clock
        self._started = clock()
        if not math.isfinite(self._started):
            raise ValueError("Budget clock must be finite")

        self.used_tokens = 0
        self._used_usd = Fraction(0)
        self.used_tool_calls = 0

    @property
    def used_usd(self) -> float:
        """Numeric compatibility view; comparisons use the exact rational ledger."""
        return float(self._used_usd)

    def consume(self, tokens: int = 0, usd: float = 0.0, tool_calls: int = 0) -> None:
        """Consume execution budget. Rejects if exceeding available non-reserved envelope."""
        self._consume(tokens, usd, tool_calls, reserve=False)

    def consume_reserve(self, tokens: int = 0, usd: float = 0.0,
                        purpose: str = "verification", *, tool_calls: int = 0) -> None:
        """Access the total envelope for recovery; purpose is not authorization."""
        if purpose not in ("verification", "rollback"):
            raise ValueError("Reserve purpose must be verification or rollback")
        self._consume(tokens, usd, tool_calls, reserve=True)

    def _consume(self, tokens: int, usd: float, tool_calls: int, *, reserve: bool) -> None:
        new_tokens = self.used_tokens + _budget_count(tokens, "tokens")
        new_usd = self._used_usd + Fraction(_budget_decimal(usd, "usd"))
        new_calls = self.used_tool_calls + _budget_count(tool_calls, "tool_calls")
        token_limit = self.total_tokens if reserve else self.available_execution_tokens
        usd_limit = self._total_usd if reserve else self._execution_usd
        call_limit = self.total_tool_calls if reserve else self.available_execution_tool_calls
        time_limit = self.total_seconds if reserve else self.available_execution_seconds
        elapsed = self._clock() - self._started
        if not math.isfinite(elapsed) or elapsed < 0 or elapsed >= time_limit:
            raise ValueError("Elapsed time exceeds budget or budget clock is invalid")
        if new_tokens > token_limit:
            raise ValueError(f"Token consumption {new_tokens} exceeds budget {token_limit}")
        if new_usd > usd_limit:
            raise ValueError(f"USD spend {new_usd} exceeds budget {usd_limit}")
        if new_calls > call_limit:
            raise ValueError(f"Tool calls {new_calls} exceed budget {call_limit}")
        # No accounting changes occur on a rejected multi-resource charge.
        self.used_tokens = new_tokens
        self._used_usd = new_usd
        self.used_tool_calls = new_calls


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
