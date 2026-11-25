"""AGYOS EVPI Clarification Policy (Expected Value of Perfect Information).

Enforces:
- Ask at most ONE short, concrete question (<25 words) ONLY when ambiguity
  materially changes correctness, safety, authorization, or an irreversible action.
- For benign ambiguities (R0/R1 safe defaults): 0 questions asked, explicit assumptions
  recorded, proceed immediately with the standard markdown assumptions header.
- For R3 irreversible actions: stage in outbox hold queue as PENDING_COMMIT and ask 1 question.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .contracts import TaskContract


@dataclass
class ClarificationDecision:
    should_ask_question: bool
    question: Optional[str]
    assumptions_applied: List[str]
    proceed_immediately: bool
    outbox_status: str  # "NONE", "PENDING_COMMIT", "HELD"
    snapshot_id: str

    def format_assumptions_header(self) -> str:
        """Format the mandatory assumptions markdown header."""
        if not self.assumptions_applied:
            return ""
        items = "; ".join(f"({i+1}) {a}" for i, a in enumerate(self.assumptions_applied))
        return (
            f"> **Assumptions Applied:** {items}. "
            f"*(Reply to override; snapshot `{self.snapshot_id}` makes this reversible.)*"
        )


def evaluate_evpi(prompt: str, contract: TaskContract) -> ClarificationDecision:
    """Evaluate whether to ask a clarifying question or proceed immediately under explicit assumptions."""
    lower = prompt.lower()
    snapshot_id = contract.compensation.snapshot_id or f"snap_{contract.task_id}"

    # Scenario 1: Irreversible R3 actions (money transfer, bulk blast, deletion, binding signatures)
    if contract.risk == "R3":
        if any(w in lower for w in ["wire", "transfer", "pay", "disburse", "refund"]):
            question = "Confirm beneficiary account and exact amount to stage for human authorization?"
        elif any(w in lower for w in ["blast", "broadcast", "entire", "all leads", "all contacts"]):
            question = "Which approved, consented list of recipients should be targeted for this broadcast?"
        elif any(w in lower for w in ["delete", "purge", "wipe"]):
            question = "Confirm target resource identifier and permanent deletion authorization?"
        elif any(w in lower for w in ["sign", "execute", "binding"]):
            question = "Confirm authorized signatory and specific contract terms to stage for approval?"
        else:
            question = "Confirm authorized parameters for this irreversible external action?"

        return ClarificationDecision(
            should_ask_question=True,
            question=question,
            assumptions_applied=list(contract.assumptions),
            proceed_immediately=False,
            outbox_status="PENDING_COMMIT",
            snapshot_id=snapshot_id,
        )

    # Scenario 2: Consequential Ambiguity in R2 (unclear target environment or tenant)
    if contract.risk == "R2" and any(w in lower for w in ["prod", "production", "live"]):
        question = "Confirm target environment: staging or production deployment?"
        return ClarificationDecision(
            should_ask_question=True,
            question=question,
            assumptions_applied=list(contract.assumptions),
            proceed_immediately=False,
            outbox_status="HELD",
            snapshot_id=snapshot_id,
        )

    # Scenario 3: Benign Ambiguity in R0/R1 (drafts, analysis, local fixes)
    # Proceed immediately with explicit assumptions header and 0 questions asked.
    return ClarificationDecision(
        should_ask_question=False,
        question=None,
        assumptions_applied=list(contract.assumptions),
        proceed_immediately=True,
        outbox_status="NONE",
        snapshot_id=snapshot_id,
    )
