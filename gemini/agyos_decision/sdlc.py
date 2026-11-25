"""AGYOS SDLC Engine — 7-Phase Autonomous Client Working Backwards Pipeline.

Phases: DISCOVERY → PRD → ARCHITECTURE → TDD_MANUFACTURING → VERIFICATION → RELEASE → HANDOVER

Embeds:
- Amazon "Working Backwards" (press release + FAQ)
- Cialdini's 7 Principles (Reciprocity, Commitment, Social Proof, Authority,
  Liking, Scarcity, Unity)
- Kahneman System 1 vs System 2 routing
- Hick's Law, Fitts's Law, Peak-End Rule, Miller's Law
- Loss Aversion (2.5x pain multiplier), Anchoring, Decoy Effect
- Ray Dalio Idea Meritocracy
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .roles import CompanyRole, classify_role_for_task


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SDLCPhase(str, Enum):
    DISCOVERY          = "DISCOVERY"
    PRD                = "PRD"
    ARCHITECTURE       = "ARCHITECTURE"
    TDD_MANUFACTURING  = "TDD_MANUFACTURING"
    VERIFICATION       = "VERIFICATION"
    RELEASE            = "RELEASE"
    HANDOVER           = "HANDOVER"


# ---------------------------------------------------------------------------
# Phase metadata
# ---------------------------------------------------------------------------

@dataclass
class PhaseConfig:
    phase: SDLCPhase
    title: str
    deliverables: List[str]
    psychology_hooks: List[str]
    entry_gate: str         # condition that must be true to enter this phase
    exit_gate: str          # condition that must be true to exit this phase


PHASE_CONFIGS: List[PhaseConfig] = [
    PhaseConfig(
        phase=SDLCPhase.DISCOVERY,
        title="Client Working Backwards Discovery",
        deliverables=[
            "Annotated press release (what does success look like for the client?)",
            "FAQ — top 10 questions a skeptical investor / user would ask",
            "Job-To-Be-Done canvas: situation, motivation, outcome",
            "Risk register: assumptions that could invalidate the product",
        ],
        psychology_hooks=[
            "Reciprocity: give a free insight before asking any question",
            "Authority: cite relevant case studies or data points up front",
            "Liking: mirror client language, use their exact vocabulary",
            "Loss Aversion: surface what is at risk if problem is NOT solved",
        ],
        entry_gate="Client query received",
        exit_gate="Press release and FAQ approved by operator",
    ),
    PhaseConfig(
        phase=SDLCPhase.PRD,
        title="Product Requirements Document",
        deliverables=[
            "User stories (As a <role> I want <goal> so that <outcome>)",
            "Acceptance criteria (Given/When/Then)",
            "Non-functional requirements: performance, security, accessibility",
            "Out-of-scope boundary (explicit exclusions)",
            "Success metrics with baseline and target values",
        ],
        psychology_hooks=[
            "Commitment: get micro-agreements on each requirement section",
            "Anchoring: show high-effort estimate first, then scoped MVP",
            "Miller's Law: group requirements in 5-7 coherent chunks",
            "Hick's Law: minimize choices per screen/flow",
        ],
        entry_gate="Discovery phase approved",
        exit_gate="All acceptance criteria signed off",
    ),
    PhaseConfig(
        phase=SDLCPhase.ARCHITECTURE,
        title="System Architecture & Technical Design",
        deliverables=[
            "C4 Container diagram (System, Container, Component, Code levels)",
            "ADR: Architecture Decision Records for every key choice",
            "Data model ERD with indices and foreign key constraints",
            "API contract (OpenAPI 3.1 or gRPC proto)",
            "Security threat model (STRIDE)",
        ],
        psychology_hooks=[
            "Authority: present design options with evidence, not just preference",
            "Decoy Effect: offer 3 options — conservative, recommended, ambitious",
            "Social Proof: reference similar FAANG/MANGO patterns",
            "Loss Aversion: quantify cost of deferred technical debt",
        ],
        entry_gate="PRD approved",
        exit_gate="Architecture reviewed and ADRs committed to docs/adr/",
    ),
    PhaseConfig(
        phase=SDLCPhase.TDD_MANUFACTURING,
        title="TDD Manufacturing (Red → Green → Refactor)",
        deliverables=[
            "Failing tests written first (RED phase)",
            "Minimal implementation to pass tests (GREEN phase)",
            "Refactored clean code with 80%+ coverage (IMPROVE phase)",
            "Integration tests for all API contracts",
            "Security test for top-5 OWASP risks",
        ],
        psychology_hooks=[
            "Commitment: test ratchet is monotonic — coverage never decreases",
            "Loss Aversion: each uncovered line is a potential production incident",
            "Social Proof: show test suite badge / coverage report to client",
        ],
        entry_gate="Architecture approved",
        exit_gate="All tests green, coverage >= 80%, CI passing",
    ),
    PhaseConfig(
        phase=SDLCPhase.VERIFICATION,
        title="Verification & Quality Gate",
        deliverables=[
            "Static analysis report (Ruff / ESLint / Clippy)",
            "Security scan report (SAST, secrets grep, Gitleaks)",
            "Performance benchmark: p50/p95/p99 latencies",
            "Accessibility audit (WCAG 2.1 AA)",
            "Acceptance criteria evidence (automated + manual)",
        ],
        psychology_hooks=[
            "Authority: verified evidence builds client trust",
            "Peak-End Rule: strong finish — demo the best feature last",
            "Commitment: document exactly which checks ran and passed",
        ],
        entry_gate="TDD manufacturing complete",
        exit_gate="Zero CRITICAL findings, all acceptance criteria evidenced",
    ),
    PhaseConfig(
        phase=SDLCPhase.RELEASE,
        title="Production Release",
        deliverables=[
            "Deployment runbook",
            "Feature flags configured (gradual rollout)",
            "Monitoring alerts configured (SLO breach alerts)",
            "Rollback plan tested",
            "Changelog / release notes published",
        ],
        psychology_hooks=[
            "Scarcity: frame release as a moment — celebrate with client",
            "Social Proof: share early adoption data with client",
            "Peak-End Rule: memorable launch moment drives positive memory",
        ],
        entry_gate="Verification gate passed",
        exit_gate="Production deployment confirmed, monitors green",
    ),
    PhaseConfig(
        phase=SDLCPhase.HANDOVER,
        title="Knowledge Transfer & Handover",
        deliverables=[
            "AI_HANDOFF.md updated with final state",
            "Runbook and architecture docs updated",
            "Client retrospective and feedback captured",
            "Next milestone opportunity scoped",
        ],
        psychology_hooks=[
            "Reciprocity: give a free retrospective gift (insight report)",
            "Commitment: confirm next engagement date during handover",
            "Unity: position as ongoing partner, not transactional vendor",
        ],
        entry_gate="Release phase complete",
        exit_gate="AI_HANDOFF.md committed, client sign-off received",
    ),
]

PHASES_BY_ID: Dict[str, PhaseConfig] = {p.phase.value: p for p in PHASE_CONFIGS}


# ---------------------------------------------------------------------------
# Client Interview Session (Working Backwards engine)
# ---------------------------------------------------------------------------

@dataclass
class ClientInterviewSession:
    """Socratic discovery session using Amazon Working Backwards methodology.

    Usage:
        session = ClientInterviewSession.from_query("Build a SaaS billing system")
        for question in session.discovery_questions():
            print(question)
    """

    query: str
    role: CompanyRole
    answers: Dict[str, str] = field(default_factory=dict)
    phase: SDLCPhase = SDLCPhase.DISCOVERY

    @classmethod
    def from_query(cls, query: str) -> "ClientInterviewSession":
        role = classify_role_for_task(query)
        return cls(query=query, role=role)

    def discovery_questions(self) -> List[str]:
        """Generate Socratic discovery questions tailored to role and query."""
        return [
            # Working Backwards — press release framing
            "1. Imagine it is 12 months from now and this is a massive success. "
            "What headline would appear on TechCrunch describing what you built?",

            "2. Who is the single most important end-user? "
            "Describe their situation, frustration, and what winning looks like for them.",

            "3. What is the one metric that, if it moves, proves this delivered value? "
            "(Examples: revenue, activation rate, churn reduction, time saved per week)",

            # Problem depth — Kahneman System 2 probing
            "4. What have you already tried to solve this? "
            "What worked, what failed, and why did you stop?",

            "5. What is the most dangerous assumption in your plan right now? "
            "What would happen if that assumption is wrong?",

            # Scope boundary — Hick's Law / Miller's Law
            "6. If you could only ship ONE feature in the first version, what would it be? "
            "(Everything else is out of scope for v1)",

            # Risk framing — Loss Aversion (2.5x pain multiplier)
            "7. What is the worst outcome if this project ships late or fails? "
            "What does that cost you in revenue, trust, or opportunity?",

            # Cialdini hooks
            "8. Who else in your industry has solved a similar problem? "
            "What can we learn from their approach? (Social Proof)",

            "9. What constraints are non-negotiable? "
            "(Budget ceiling, compliance requirements, tech stack, timeline)",

            # Delivery model
            "10. How would you like to work together? "
            "Fixed scope + price, time & materials, or outcome-based retainer?",
        ]

    def press_release(self) -> str:
        """Generate a draft Amazon Working Backwards press release from answers."""
        headline = self.answers.get("1", "[Headline TBD — answer question 1 first]")
        user = self.answers.get("2", "[End-user TBD]")
        metric = self.answers.get("3", "[Success metric TBD]")
        feature = self.answers.get("6", "[Core feature TBD]")

        return textwrap.dedent(f"""\
            # PRESS RELEASE (INTERNAL WORKING BACKWARDS DRAFT)

            ## {headline}

            **FOR IMMEDIATE RELEASE**

            ---

            **Who it is for**: {user}

            **What it does**: {self.query}

            **Core capability in v1**: {feature}

            **How we know it worked**: {metric}

            ---

            *This press release was generated using Amazon Working Backwards methodology.
            It is an internal alignment tool — not a public announcement.*
        """)

    def phase_plan(self) -> str:
        """Return a formatted 7-phase delivery plan."""
        lines = ["# 7-Phase AGYOS Delivery Plan\n"]
        for cfg in PHASE_CONFIGS:
            lines.append(f"## Phase {cfg.phase.value}: {cfg.title}")
            lines.append(f"**Entry gate**: {cfg.entry_gate}")
            lines.append(f"**Exit gate**: {cfg.exit_gate}")
            lines.append("\n**Deliverables**:")
            for d in cfg.deliverables:
                lines.append(f"  - {d}")
            lines.append("\n**Psychology levers**:")
            for h in cfg.psychology_hooks:
                lines.append(f"  - {h}")
            lines.append("")
        return "\n".join(lines)

    def advance_phase(self) -> SDLCPhase:
        """Move to the next phase. Raises ValueError if already at HANDOVER."""
        phases = list(SDLCPhase)
        idx = phases.index(self.phase)
        if idx >= len(phases) - 1:
            raise ValueError("Already at final phase HANDOVER — no further phases.")
        self.phase = phases[idx + 1]
        return self.phase


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------

def get_phase(phase_id: str) -> Optional[PhaseConfig]:
    """Return a PhaseConfig by its string ID (e.g. 'DISCOVERY')."""
    return PHASES_BY_ID.get(phase_id.upper())


def list_phases() -> List[PhaseConfig]:
    """Return all phases in order."""
    return list(PHASE_CONFIGS)
