"""AGYOS TaskContract implementation and schema validation.

Enforces:
- Depth <= 2 (L0 Coordinator -> L1 Pod -> L2 Worker)
- 5 Merged Pods: pod-growth, pod-customer, pod-build, pod-gna, pod-people
- Risk tiers: R0 (read-only), R1 (local reversible), R2 (shared internal state), R3 (external irreversible)
- Quota envelopes: <=30k tokens, <=$1.50, <=600s, <=40 tool calls, <=2 retries
- 20% budget reserve for verification and rollback
- Saga compensation specifications
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import jsonschema

SCHEMA_PATH = Path(__file__).resolve().parent / "contracts.schema.json"
_SCHEMA_CACHE: Optional[Dict[str, Any]] = None


def get_schema() -> Dict[str, Any]:
    global _SCHEMA_CACHE
    if _SCHEMA_CACHE is None:
        _SCHEMA_CACHE = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return _SCHEMA_CACHE


@dataclass
class Budget:
    tokens: int = 12000
    usd: float = 0.50
    seconds: int = 180
    tool_calls: int = 20
    max_retries: int = 2

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tokens": int(self.tokens),
            "usd": round(float(self.usd), 2),
            "seconds": int(self.seconds),
            "tool_calls": int(self.tool_calls),
            "max_retries": int(self.max_retries),
        }


@dataclass
class Postconditions:
    output_schema_ref: str
    verifier_cmd: str
    required_claims_grounded: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "output_schema_ref": self.output_schema_ref,
            "verifier_cmd": self.verifier_cmd,
            "required_claims_grounded": bool(self.required_claims_grounded),
        }


@dataclass
class Compensation:
    kind: str
    resource_ref: str
    rollback_cmd: str
    snapshot_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "resource_ref": self.resource_ref,
            "rollback_cmd": self.rollback_cmd,
            "snapshot_id": self.snapshot_id,
        }


@dataclass
class Approval:
    required: bool = False
    scope: Optional[str] = None
    expires_at: Optional[str] = None
    status: str = "approved"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "required": bool(self.required),
            "scope": self.scope,
            "expires_at": self.expires_at,
            "status": self.status,
        }


@dataclass
class TaskResult:
    status: str = "pending"
    artifacts: List[str] = field(default_factory=list)
    proofs: List[str] = field(default_factory=list)
    uncertainty: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "artifacts": list(self.artifacts),
            "proofs": list(self.proofs),
            "uncertainty": list(self.uncertainty),
        }


@dataclass
class TaskContract:
    task_id: str
    run_id: str
    parent_task_id: Optional[str]
    tenant_id: str
    requester_id: str
    depth: int
    pod: str
    objective: str
    risk: str
    assumptions: List[str] = field(default_factory=list)
    inputs: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    allowed_actions: List[str] = field(default_factory=list)
    forbidden_actions: List[str] = field(default_factory=list)
    capability_allowlist: List[str] = field(default_factory=list)
    approval: Approval = field(default_factory=Approval)
    acceptance: List[Dict[str, Any]] = field(default_factory=list)
    budget: Budget = field(default_factory=Budget)
    idempotency_key: str = ""
    preconditions: List[str] = field(default_factory=list)
    postconditions: Postconditions = field(
        default_factory=lambda: Postconditions("default-v1", "scripts/agyos-verify.sh", True)
    )
    compensation: Compensation = field(
        default_factory=lambda: Compensation("noop", "none", "true", "snap_0")
    )
    result: TaskResult = field(default_factory=TaskResult)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "run_id": self.run_id,
            "parent_task_id": self.parent_task_id,
            "tenant_id": self.tenant_id,
            "requester_id": self.requester_id,
            "depth": int(self.depth),
            "pod": self.pod,
            "objective": self.objective,
            "risk": self.risk,
            "assumptions": list(self.assumptions),
            "inputs": list(self.inputs),
            "dependencies": list(self.dependencies),
            "allowed_actions": list(self.allowed_actions),
            "forbidden_actions": list(self.forbidden_actions),
            "capability_allowlist": list(self.capability_allowlist),
            "approval": self.approval.to_dict() if isinstance(self.approval, Approval) else self.approval,
            "acceptance": list(self.acceptance),
            "budget": self.budget.to_dict() if isinstance(self.budget, Budget) else self.budget,
            "idempotency_key": self.idempotency_key,
            "preconditions": list(self.preconditions),
            "postconditions": (
                self.postconditions.to_dict()
                if isinstance(self.postconditions, Postconditions)
                else self.postconditions
            ),
            "compensation": (
                self.compensation.to_dict()
                if isinstance(self.compensation, Compensation)
                else self.compensation
            ),
            "result": self.result.to_dict() if isinstance(self.result, TaskResult) else self.result,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TaskContract:
        budget_data = data.get("budget", {})
        budget = (
            Budget(**budget_data)
            if isinstance(budget_data, dict)
            else budget_data
        )
        post_data = data.get("postconditions", {})
        postconditions = (
            Postconditions(**post_data)
            if isinstance(post_data, dict)
            else post_data
        )
        comp_data = data.get("compensation", {})
        compensation = (
            Compensation(**comp_data)
            if isinstance(comp_data, dict)
            else comp_data
        )
        app_data = data.get("approval", {})
        approval = (
            Approval(**app_data)
            if isinstance(app_data, dict)
            else app_data
        )
        res_data = data.get("result", {})
        result = (
            TaskResult(**res_data)
            if isinstance(res_data, dict)
            else res_data
        )

        return cls(
            task_id=data["task_id"],
            run_id=data["run_id"],
            parent_task_id=data.get("parent_task_id"),
            tenant_id=data["tenant_id"],
            requester_id=data["requester_id"],
            depth=int(data["depth"]),
            pod=data["pod"],
            objective=data["objective"],
            risk=data["risk"],
            assumptions=list(data.get("assumptions", [])),
            inputs=list(data.get("inputs", [])),
            dependencies=list(data.get("dependencies", [])),
            allowed_actions=list(data.get("allowed_actions", [])),
            forbidden_actions=list(data.get("forbidden_actions", [])),
            capability_allowlist=list(data.get("capability_allowlist", [])),
            approval=approval,
            acceptance=list(data.get("acceptance", [])),
            budget=budget,
            idempotency_key=data.get("idempotency_key", f"idem_{data['task_id']}"),
            preconditions=list(data.get("preconditions", [])),
            postconditions=postconditions,
            compensation=compensation,
            result=result,
        )


def validate_contract(contract: TaskContract | Dict[str, Any]) -> None:
    schema = get_schema()
    raw = contract.to_dict() if isinstance(contract, TaskContract) else contract
    jsonschema.validate(instance=raw, schema=schema)
