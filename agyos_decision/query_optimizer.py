"""AGYOS Query Optimization Engine — Unified Intent, Role, Skill & Context Synthesis.

Translates any natural language prompt into a fully-optimized execution plan:
1. Matches optimal FAANG role from the 104-role enterprise matrix aligned with the pod.
2. Selects specialist skills from the 2,247 catalog and maps DAG relations.
3. Applies Amazon Working Backwards EVPI clarification and safe default assumptions.
4. Generates KV-cache aligned Tri-Format prompt envelopes (static prefix + dynamic suffix).
5. Routes to the optimal model (Gemini 3.8 Flash / Claude 3.5 Sonnet) with token budgeting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import re
from typing import Any, Dict, List, Optional
from xml.sax.saxutils import escape as xml_escape

from .contracts import TaskContract
from .intent_compiler import compile_intent
from .evpi_clarify import evaluate_evpi
from .roles import get_role, classify_role_for_task, list_roles, CompanyRole, POD_DEFAULT_ROLES
from .skills_router import decide_skill
from .model_router import route_model, DataSensitivity
from .graph import get_role_subgraph
from .xml_compiler import compile_cached_prompt, minify_xml


@dataclass(frozen=True)
class OptimizedQueryPlan:
    query: str
    role_id: str
    role_title: str
    department: str
    seniority: str
    governing_pod: str
    risk: str
    complexity: int
    complexity_reason: str
    primary_skill: str
    candidate_skills: List[str]
    evpi_should_ask: bool
    evpi_question: Optional[str]
    assumptions: List[str]
    model_id: str
    model_provider: str
    thinking_level: Optional[str]
    token_budget: int
    cost_ceiling_usd: float
    static_prefix_xml: str
    dynamic_suffix_xml: str
    full_prompt_xml: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "role": {
                "role_id": self.role_id,
                "title": self.role_title,
                "department": self.department,
                "seniority": self.seniority,
                "governing_pod": self.governing_pod,
            },
            "routing": {
                "risk": self.risk,
                "complexity": self.complexity,
                "complexity_reason": self.complexity_reason,
                "primary_skill": self.primary_skill,
                "candidate_skills": self.candidate_skills,
            },
            "evpi": {
                "should_ask_question": self.evpi_should_ask,
                "question": self.evpi_question,
                "assumptions": self.assumptions,
            },
            "model_economics": {
                "recommended_model": self.model_id,
                "provider": self.model_provider,
                "thinking_level": self.thinking_level,
                "token_budget": self.token_budget,
                "cost_ceiling_usd": self.cost_ceiling_usd,
            },
            "prompt_cache": {
                "static_prefix_length": len(self.static_prefix_xml),
                "dynamic_suffix_length": len(self.dynamic_suffix_xml),
                "full_prompt_length": len(self.full_prompt_xml),
            },
        }

    def to_xml(self, compact: bool = False) -> str:
        """Render the complete optimized execution plan as a FAANG XML envelope."""
        xml_lines = [
            f'<agyos_optimized_query risk="{self.risk}" pod="{self.governing_pod}" model="{self.model_id}">',
            f'  <assignment>',
            f'    <role id="{self.role_id}" seniority="{self.seniority}" department="{self.department}">{xml_escape(self.role_title)}</role>',
            f'    <primary_skill>{self.primary_skill}</primary_skill>',
            f'    <candidate_skills count="{len(self.candidate_skills)}">{",".join(self.candidate_skills)}</candidate_skills>',
            f'  </assignment>',
            f'  <clarification should_ask="{str(self.evpi_should_ask).lower()}">',
        ]
        if self.evpi_question:
            xml_lines.append(f'    <question>{xml_escape(self.evpi_question)}</question>')
        xml_lines.append(f'    <assumptions count="{len(self.assumptions)}">')
        for a in self.assumptions:
            xml_lines.append(f'      <assumption>{xml_escape(a)}</assumption>')
        xml_lines.append(f'    </assumptions>')
        xml_lines.append(f'  </clarification>')
        xml_lines.append(f'  <prompt_envelope format="xml_toon">')
        xml_lines.append(f'    <static_prefix format="xml_kv_cache">')
        xml_lines.append(f'{self.static_prefix_xml}')
        xml_lines.append(f'    </static_prefix>')
        xml_lines.append(f'    <dynamic_suffix format="xml_task">')
        xml_lines.append(f'{self.dynamic_suffix_xml}')
        xml_lines.append(f'    </dynamic_suffix>')
        xml_lines.append(f'  </prompt_envelope>')
        xml_lines.append(f'</agyos_optimized_query>')

        raw_xml = "\n".join(xml_lines)
        return minify_xml(raw_xml) if compact else raw_xml


def optimize_query(
    query: str,
    *,
    compact: bool = False,
    depth: int = 1,
    sensitivity: DataSensitivity = DataSensitivity.INTERNAL,
) -> OptimizedQueryPlan:
    """Optimize any user query into an end-to-end FAANG execution plan."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("A non-empty query string is required")

    clean_query = query.strip()

    # 1. Intent Compilation & Risk Classification
    contract = compile_intent(clean_query)
    risk = contract.risk
    governing_pod = contract.pod

    # 2. Role Resolution (ensuring alignment with the assigned pod)
    matched_role = get_role(contract.role_id) if contract.role_id else None
    if not matched_role or matched_role.governing_pod != governing_pod:
        matched_role = classify_role_for_task(clean_query, pod=governing_pod)

    if matched_role.governing_pod != governing_pod:
        default_role_id = POD_DEFAULT_ROLES.get(governing_pod, "role-swe")
        matched_role = get_role(default_role_id) or matched_role

    role_id = matched_role.role_id
    role_title = matched_role.title
    department = matched_role.department
    seniority = matched_role.seniority

    # 3. Specialist Skill Discovery
    skill_result = decide_skill(clean_query)
    primary_skill = skill_result.get("primary_skill", "clean-code")
    candidates_raw = skill_result.get("candidates", [])
    candidate_skills = [c["name"] for c in candidates_raw if c.get("name") != primary_skill][:4]

    classification = skill_result.get("classification", {})
    complexity = classification.get("complexity_score", 2)
    complexity_reason = classification.get("workflow_guidance", "Standard workflow")

    # 4. Amazon Working Backwards & EVPI Clarification
    evpi_decision = evaluate_evpi(clean_query, contract)
    evpi_should_ask = evpi_decision.should_ask_question
    evpi_question = evpi_decision.question if evpi_should_ask else None
    assumptions = list(evpi_decision.assumptions_applied) or list(contract.assumptions)

    # 5. Model Routing & Token Economics
    model_decision = route_model(clean_query, complexity=complexity, sensitivity=sensitivity)
    model_id = model_decision.model_id
    model_provider = model_decision.provider.value
    thinking_level = model_decision.thinking_level

    token_budget = contract.budget.tokens
    cost_ceiling_usd = contract.budget.usd

    # 6. Active Skills & KV-Cache Prompt Assembly
    active_skills = [primary_skill] + candidate_skills[:2]
    # Re-package contract with resolved role and skills
    enriched_contract = TaskContract(
        task_id=contract.task_id,
        run_id=contract.run_id,
        parent_task_id=contract.parent_task_id,
        tenant_id=contract.tenant_id,
        requester_id=contract.requester_id,
        depth=contract.depth,
        pod=governing_pod,
        objective=contract.objective,
        risk=risk,
        assumptions=assumptions,
        inputs=contract.inputs,
        dependencies=contract.dependencies,
        allowed_actions=contract.allowed_actions,
        forbidden_actions=contract.forbidden_actions,
        capability_allowlist=contract.capability_allowlist,
        approval=contract.approval,
        acceptance=contract.acceptance,
        budget=contract.budget,
        idempotency_key=contract.idempotency_key,
        preconditions=contract.preconditions,
        postconditions=contract.postconditions,
        compensation=contract.compensation,
        result=contract.result,
        role_id=role_id,
        department=department,
        seniority=seniority,
    )
    # Attach active skills dynamically for XML compiler
    object.__setattr__(enriched_contract, "active_skills", active_skills)

    prompt_parts = compile_cached_prompt(enriched_contract, compact=compact)
    static_prefix = prompt_parts["static_prefix"]
    dynamic_suffix = prompt_parts["dynamic_suffix"]
    full_prompt = prompt_parts["full_prompt"]

    return OptimizedQueryPlan(
        query=clean_query,
        role_id=role_id,
        role_title=role_title,
        department=department,
        seniority=seniority,
        governing_pod=governing_pod,
        risk=risk,
        complexity=complexity,
        complexity_reason=complexity_reason,
        primary_skill=primary_skill,
        candidate_skills=candidate_skills,
        evpi_should_ask=evpi_should_ask,
        evpi_question=evpi_question,
        assumptions=assumptions,
        model_id=model_id,
        model_provider=model_provider,
        thinking_level=thinking_level,
        token_budget=token_budget,
        cost_ceiling_usd=cost_ceiling_usd,
        static_prefix_xml=static_prefix,
        dynamic_suffix_xml=dynamic_suffix,
        full_prompt_xml=full_prompt,
    )
