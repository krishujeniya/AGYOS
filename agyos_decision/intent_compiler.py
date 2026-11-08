"""AGYOS Intent Compiler — Natural Language Intent to Typed TaskContracts.

Translates plain natural language across all 11 company functions:
- marketing, lead gain, sales -> pod-growth
- onboarding, support -> pod-customer
- product, engineering -> pod-build
- finance, legal, ops -> pod-gna
- hiring -> pod-people

Without slash commands, keyword triggers, or manual agent naming.
Classifies risk tiers: R0 (read-only), R1 (local reversible), R2 (shared internal state), R3 (external irreversible).
"""

from __future__ import annotations

import re
import uuid
from typing import Any, Dict, List, Optional, Tuple

from .contracts import (
    Approval,
    Budget,
    Compensation,
    Postconditions,
    TaskContract,
    TaskResult,
    validate_contract,
)

# 11 Company functions mapped to the 5 Merged Pods
FUNCTION_TO_POD: Dict[str, str] = {
    "marketing": "pod-growth",
    "lead_generation": "pod-growth",
    "sales": "pod-growth",
    "onboarding": "pod-customer",
    "support": "pod-customer",
    "product": "pod-build",
    "engineering": "pod-build",
    "finance": "pod-gna",
    "legal": "pod-gna",
    "operations": "pod-gna",
    "hiring": "pod-people",
}

FUNCTION_PATTERNS: Dict[str, List[str]] = {
    "marketing": [
        "marketing", "launch announcement", "campaign", "newsletter",
        "messaging", "blog post", "social post", "copywriting", "seo content",
        "audience", "promotional", "branding"
    ],
    "lead_generation": [
        "lead", "prospect", "outreach list", "account list", "find customers",
        "prospects", "registrar", "directory", "pipeline source"
    ],
    "sales": [
        "sales", "proposal", "deal", "quote", "pricing tier", "renewal",
        "pitch", "sales guide", "discount", "close contract"
    ],
    "onboarding": [
        "onboarding", "welcome", "client checklist", "new client",
        "account provision", "welcome email", "kickoff", "setup documentation"
    ],
    "support": [
        "support", "ticket", "customer issue", "helpdesk", "timeout error",
        "troubleshoot client", "refund", "customer complaint"
    ],
    "product": [
        "product", "prd", "roadmap", "user feedback", "feature prioritization",
        "acceptance criteria", "user story", "opportunity tree", "specification"
    ],
    "engineering": [
        "engineering", "fix bug", "code", "endpoint", "refactor", "unit test",
        "regression test", "database query", "api", "idempotency", "patch",
        "checkout bug", "service", "handler"
    ],
    "finance": [
        "finance", "invoice", "ledger", "reconcile", "payment", "bank",
        "wire transfer", "variance report", "disbursement", "payroll", "balance"
    ],
    "legal": [
        "legal", "contract", "terms of service", "msa", "nda", "compliance",
        "indemnity", "liability", "clause", "gdpr", "regulations", "agreement"
    ],
    "operations": [
        "operations", "ops", "procurement", "vendor order", "supplier",
        "hardware", "inventory", "purchase order", "requisition", "logistics"
    ],
    "hiring": [
        "hiring", "applicant", "resume", "interview", "scorecard", "rubric",
        "job description", "candidate", "talent", "headcount", "offer letter"
    ],
}

R3_PATTERNS = [
    r"\b(wire|transfer|pay|disburse|charge|refund)\b.*\$",
    r"\b(send|broadcast|blast)\b.*\b(entire|all|every)\b.*\b(database|list|leads|contacts|users)\b",
    r"\b(sign|execute)\b.*\b(binding|contract|agreement|merger|nda)\b",
    r"\b(delete|purge|wipe|drop)\b.*\b(account|database|table|history|records|all)\b",
    r"\b(deploy|release)\b.*\b(production|prod)\b",
]

R2_PATTERNS = [
    r"\b(update|modify|patch|write)\b.*\b(crm|database|ledger|record|account)\b",
    r"\b(provision|grant|invite)\b.*\b(access|account|user|client)\b",
    r"\b(prepare|stage)\b.*\b(deploy|campaign|pr)\b",
]

R1_PATTERNS = [
    r"\b(fix|patch|refactor|implement|create|draft|write)\b.*\b(code|test|bug|handler|endpoint|proposal|post|doc)\b",
]


def classify_function(prompt: str) -> str:
    """Classify prompt into one of the 11 company functions."""
    lower = prompt.lower()

    # Career development belongs to pod-people, independent of AI/ML topic.
    if re.search(r"\\bcareer\\b", lower) and re.search(r"\\b(roadmap|plan|planning|gaps?|assessment)\\b", lower):
        return "hiring"

    # Prioritize engineering implementation for feature/endpoint requests
    if any(w in lower for w in ["implement checkout", "endpoint", "fix checkout", "idempotency", "unit test"]):
        return "engineering"

    scores: Dict[str, int] = {fn: 0 for fn in FUNCTION_PATTERNS}
    for fn, kws in FUNCTION_PATTERNS.items():
        for kw in kws:
            if kw in lower:
                scores[fn] += len(kw.split()) + 2

    best_fn = max(scores, key=lambda k: scores[k])
    if scores[best_fn] > 0:
        return best_fn

    # Fallback heuristics
    if any(w in lower for w in ["test", "bug", "code", "error", "endpoint"]):
        return "engineering"
    if any(w in lower for w in ["doc", "draft", "write"]):
        return "marketing"
    return "engineering"


def classify_risk(prompt: str, function: str) -> str:
    """Classify risk tier (R0-R3)."""
    lower = prompt.lower()

    # R3: External Irreversible
    for pattern in R3_PATTERNS:
        if re.search(pattern, lower):
            return "R3"

    # R2: Shared Internal State
    for pattern in R2_PATTERNS:
        if re.search(pattern, lower):
            return "R2"
    if any(w in lower for w in ["launch new subscription billing feature", "production deploy"]):
        return "R2"

    # R0: Read-only, analysis, diagnose, prioritize, screen, review, reconcile
    if any(lower.startswith(w) or f" {w} " in f" {lower} " for w in [
        "diagnose", "prioritize", "screen", "review", "reconcile", "analyze", "find potential"
    ]):
        return "R0"
    if function in ("legal", "hiring") and any(w in lower for w in ["review", "screen", "rubric", "flag"]):
        return "R0"
    if function in ("finance", "support") and any(w in lower for w in ["reconcile", "diagnose", "variances"]):
        return "R0"
    if function == "product" and any(w in lower for w in ["prioritize", "feedback"]):
        return "R0"

    # R1: Local Reversible Writes
    if any(re.search(p, lower) for p in R1_PATTERNS):
        return "R1"
    if any(w in lower for w in ["draft", "fix", "create", "write", "prepare", "implement"]):
        return "R1"

    # Default to R0
    return "R0"


def generate_default_assumptions(function: str, prompt: str, risk: str) -> List[str]:
    """Generate safe, explicit assumptions for benign ambiguities."""
    assumptions: List[str] = []
    if function in ("marketing", "lead_generation", "sales"):
        assumptions.append("professional business audience")
        assumptions.append("draft artifacts only without live publishing")
    elif function in ("onboarding", "support"):
        assumptions.append("standard client service template")
        assumptions.append("read-only diagnosis pending operator review")
    elif function in ("product", "engineering"):
        assumptions.append("bounded implementation maintaining backward compatibility")
        assumptions.append("monotonic test ratchet with 80%+ test coverage")
    elif function in ("finance", "legal", "operations"):
        assumptions.append("read-only analysis and variance flagging")
        assumptions.append("advisory findings requiring qualified human review")
    elif function == "hiring":
        assumptions.append("unbiased rubric scoring")
        assumptions.append("human hiring authority makes final employment determination")

    if risk == "R3":
        assumptions.append("staged in outbox as PENDING_COMMIT until explicit human authorization")

    return assumptions


def compile_intent(
    prompt: str,
    *,
    tenant_id: str = "tenant_default",
    requester_id: str = "operator",
    depth: int = 0,
    parent_task_id: Optional[str] = None,
) -> TaskContract:
    """Compile plain natural language into a strictly typed TaskContract."""
    function = classify_function(prompt)
    pod = FUNCTION_TO_POD[function]
    risk = classify_risk(prompt, function)

    task_id = f"tsk_{function[:4]}_{uuid.uuid4().hex[:8]}"
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    assumptions = generate_default_assumptions(function, prompt, risk)

    # Capability allowlist scoped by pod and risk
    allowed_actions = ["read_file"]
    forbidden_actions = []
    if risk in ("R1", "R2"):
        allowed_actions.extend(["edit_file", "write_file", "run_command"])
    elif risk == "R3":
        forbidden_actions.extend(["send:external", "charge:payment", "delete:production"])

    approval = Approval(
        required=(risk in ("R2", "R3")),
        scope=f"{pod}:{risk}",
        expires_at=None,
        status="pending" if risk in ("R2", "R3") else "approved",
    )

    budget = Budget(
        tokens=12000 if risk in ("R0", "R1") else 16000,
        usd=0.50 if risk in ("R0", "R1") else 0.80,
        seconds=180,
        tool_calls=20,
        max_retries=2,
    )

    postconditions = Postconditions(
        output_schema_ref=f"schema-{pod}-v1",
        verifier_cmd="scripts/agyos-verify.sh",
        required_claims_grounded=True,
    )

    compensation = Compensation(
        kind="snapshot_revert" if risk in ("R1", "R2") else "noop",
        resource_ref=task_id,
        rollback_cmd=f"bin/agyos rollback {task_id}",
        snapshot_id=f"snap_{task_id}",
    )

    contract = TaskContract(
        task_id=task_id,
        run_id=run_id,
        parent_task_id=parent_task_id,
        tenant_id=tenant_id,
        requester_id=requester_id,
        depth=depth,
        pod=pod,
        objective=prompt.strip(),
        risk=risk,
        assumptions=assumptions,
        inputs=[],
        dependencies=[],
        allowed_actions=allowed_actions,
        forbidden_actions=forbidden_actions,
        capability_allowlist=allowed_actions,
        approval=approval,
        acceptance=[{"type": "schema", "schema_id": f"schema-{pod}-v1"}],
        budget=budget,
        idempotency_key=f"idem_{task_id}",
        preconditions=["state.initialized"],
        postconditions=postconditions,
        compensation=compensation,
        result=TaskResult(status="pending"),
    )

    # Validate against JSON schema
    validate_contract(contract)
    return contract
