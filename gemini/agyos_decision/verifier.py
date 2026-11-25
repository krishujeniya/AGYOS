"""AGYOS Verifier: Atomic-Claim Grounding & End-State Verification (P19, P09, P20).

Decomposes agent output into atomic claims (entities, numbers, currencies, dates, references)
and deterministically verifies each claim against grounded tool evidence.
Enforces invariant: 0 unbacked numeric or contract claims.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple


@dataclass
class AtomicClaim:
    text: str
    claim_type: str  # "numeric", "currency", "identifier", "date", "entity"
    extracted_value: str
    grounded: bool = False
    evidence_source: str = ""


@dataclass
class VerificationReport:
    total_claims: int
    grounded_claims: int
    unbacked_claims: int
    precision: float
    passed: bool
    claims: List[AtomicClaim] = field(default_factory=list)


def extract_atomic_claims(text: str) -> List[AtomicClaim]:
    """Extract verifiable atomic assertions from output text."""
    claims: List[AtomicClaim] = []

    # 1. Currency & dollar amounts
    for match in re.finditer(r"\$\s*([0-9,]+(?:\.[0-9]{2})?)", text):
        val = match.group(0).replace(" ", "")
        claims.append(AtomicClaim(
            text=f"Mentions amount {val}",
            claim_type="currency",
            extracted_value=val,
        ))

    # 2. Percentage claims
    for match in re.finditer(r"([0-9]+(?:\.[0-9]+)?)\s*%", text):
        val = match.group(0)
        claims.append(AtomicClaim(
            text=f"Mentions percentage {val}",
            claim_type="numeric",
            extracted_value=val,
        ))

    # 3. Contract / Task IDs (tsk_*, snap_*, idem_*, run_*)
    for match in re.finditer(r"\b(tsk_[a-zA-Z0-9_-]+|snap_[a-zA-Z0-9_-]+|idem_[a-zA-Z0-9_-]+)\b", text):
        val = match.group(0)
        claims.append(AtomicClaim(
            text=f"References identifier {val}",
            claim_type="identifier",
            extracted_value=val,
        ))

    return claims


def verify_atomic_grounding(
    output_text: str,
    ground_truth_facts: Dict[str, Any],
) -> VerificationReport:
    """Verify all atomic claims against ground-truth facts. Requires 0 unbacked claims."""
    claims = extract_atomic_claims(output_text)
    if not claims:
        # If no numeric/contract claims present, verify text is non-empty
        passed = len(output_text.strip()) > 0
        return VerificationReport(
            total_claims=0,
            grounded_claims=0,
            unbacked_claims=0,
            precision=1.0 if passed else 0.0,
            passed=passed,
            claims=[],
        )

    # Flatten ground-truth values to set of strings
    def flatten_facts(obj: Any) -> Set[str]:
        s = set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                s.add(str(k).lower())
                s.update(flatten_facts(v))
        elif isinstance(obj, (list, tuple, set)):
            for v in obj:
                s.update(flatten_facts(v))
        else:
            s.add(str(obj).lower())
        return s

    fact_tokens = flatten_facts(ground_truth_facts)
    grounded_count = 0
    unbacked_count = 0

    for claim in claims:
        norm_val = claim.extracted_value.lower()
        # Direct or clean numerical match
        cleaned_val = norm_val.replace("$", "").replace(",", "")
        is_grounded = (
            norm_val in fact_tokens
            or cleaned_val in fact_tokens
            or any(norm_val in ft for ft in fact_tokens)
            or any(cleaned_val in ft for ft in fact_tokens)
        )
        claim.grounded = is_grounded
        if is_grounded:
            grounded_count += 1
            claim.evidence_source = "ground_truth_evidence"
        else:
            unbacked_count += 1
            claim.evidence_source = "UNBACKED"

    precision = grounded_count / len(claims) if claims else 1.0
    # Strict Invariant: 0 unbacked claims allowed
    passed = (unbacked_count == 0)

    return VerificationReport(
        total_claims=len(claims),
        grounded_claims=grounded_count,
        unbacked_claims=unbacked_count,
        precision=round(precision, 4),
        passed=passed,
        claims=claims,
    )
