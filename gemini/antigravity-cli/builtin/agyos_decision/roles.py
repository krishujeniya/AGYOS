"""AGYOS 104-Role Enterprise Matrix — Fully Autonomous FAANG/MANGO Vibe Company.

12 Departments, 5 Seniority Tiers (L4–L8), 104 operational roles.
Each role carries: mandate, psychology principles, skill roster, keyword triggers.

Split: role definitions are in roles_registry.py; this module exposes the
public API (classify_role_for_task, list_roles, get_role, get_skills_for_role).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Enums & constants
# ---------------------------------------------------------------------------

class SeniorityLevel(str, Enum):
    L8 = "L8"  # C-Suite / VP
    L7 = "L7"  # Director / Principal
    L6 = "L6"  # Senior Manager / Staff
    L5 = "L5"  # Manager / Senior Individual Contributor
    L4 = "L4"  # Individual Contributor / Specialist


class CompanyDepartment(str, Enum):
    EXECUTIVE        = "executive"
    PRODUCT          = "product"
    ENGINEERING      = "engineering"
    DATA_AI          = "data_ai"
    DESIGN           = "design"
    MARKETING        = "marketing"
    SALES_BD         = "sales_bd"
    CUSTOMER_SUCCESS = "customer_success"
    FINANCE          = "finance"
    LEGAL_COMPLIANCE = "legal_compliance"
    PEOPLE_OPS       = "people_ops"
    IT_INFRA         = "it_infra"


# ---------------------------------------------------------------------------
# CompanyRole dataclass
# ---------------------------------------------------------------------------

@dataclass
class CompanyRole:
    role_id: str
    title: str
    department: str                      # CompanyDepartment.value
    seniority: str                       # SeniorityLevel.value
    governing_pod: str                   # one of the 5 pods
    mandate: str
    psychology_principles: List[str] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list)
    default_risk: str = "R1"
    keywords: List[str] = field(default_factory=list)
    primary_skills: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Role registry — 104 roles across 12 departments
# ---------------------------------------------------------------------------

_REGISTRY: Dict[str, CompanyRole] = {}


def _r(role: CompanyRole) -> None:
    _REGISTRY[role.role_id] = role


# ── EXECUTIVE (8 roles) ────────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-ceo",
    title="Chief Executive Officer",
    department=CompanyDepartment.EXECUTIVE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-gna",
    mandate="Set vision, allocate capital, approve R3 actions, embody company identity.",
    psychology_principles=["authority", "unity", "social_proof", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R3",
    keywords=["ceo", "vision", "strategy", "company direction", "executive decision",
               "board", "investor", "fundraise", "pivot", "okr", "north star"],
    primary_skills=["financial-projections", "market-opportunity", "pitch-psychologist",
                    "startup-analyst", "product-manager-toolkit"],
))

_r(CompanyRole(
    role_id="role-cto",
    title="Chief Technology Officer",
    department=CompanyDepartment.EXECUTIVE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-build",
    mandate="Own engineering strategy, architecture decisions, technical debt policy, and AI platform.",
    psychology_principles=["authority", "commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["cto", "tech stack", "architecture decision", "platform strategy",
               "engineering culture", "adr", "technical direction", "build vs buy"],
    primary_skills=["senior-architect", "architecture-decision-records", "software-architecture",
                    "aws-cloud-architecture", "multi-cloud-architecture"],
))

_r(CompanyRole(
    role_id="role-coo",
    title="Chief Operating Officer",
    department=CompanyDepartment.EXECUTIVE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-gna",
    mandate="Run daily operations, enforce process discipline, OKR cadence, and cross-pod coordination.",
    psychology_principles=["commitment", "loss_aversion", "peak_end_rule"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["coo", "operations", "process improvement", "okr cadence", "ops review",
               "efficiency", "workflow", "cross-team", "coordination", "runbook"],
    primary_skills=["business-analyst", "freelancer-operations", "kpi-dashboard-design",
                    "incident-response", "project-flow-ops"],
))

_r(CompanyRole(
    role_id="role-cpo",
    title="Chief Product Officer",
    department=CompanyDepartment.EXECUTIVE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-build",
    mandate="Own product strategy, roadmap, pricing, and go-to-market alignment.",
    psychology_principles=["anchoring", "decoy_effect", "peak_end_rule", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["cpo", "product strategy", "product roadmap", "product vision",
               "monetization strategy", "pricing strategy", "go to market", "gtm"],
    primary_skills=["product-manager-toolkit", "market-opportunity", "pricing-strategy",
                    "feature-development-pipeline", "product-manager"],
))

_r(CompanyRole(
    role_id="role-cmo",
    title="Chief Marketing Officer",
    department=CompanyDepartment.EXECUTIVE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-growth",
    mandate="Lead brand, demand generation, content engine, and growth loops.",
    psychology_principles=["social_proof", "liking", "reciprocity", "scarcity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["cmo", "brand strategy", "demand generation", "marketing strategy",
               "content strategy", "growth", "brand identity", "market positioning",
               "marketing", "marketing campaign", "launch"],
    primary_skills=["content-strategy", "brand-guidelines", "market-opportunity",
                    "analytics-tracking", "seo-audit"],
))

_r(CompanyRole(
    role_id="role-cso",
    title="Chief Security Officer",
    department=CompanyDepartment.EXECUTIVE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-gna",
    mandate="Own security posture, compliance, incident response, and zero-trust policy.",
    psychology_principles=["loss_aversion", "authority", "commitment"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R2",
    keywords=["cso", "security strategy", "ciso", "zero trust", "security posture",
               "compliance program", "risk management", "gdpr", "hipaa", "soc2"],
    primary_skills=["security-auditor", "devsecops-guardrails", "privacy-by-design",
                    "sast-scan", "gdpr-data-handling"],
))

_r(CompanyRole(
    role_id="role-cfo",
    title="Chief Financial Officer",
    department=CompanyDepartment.EXECUTIVE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-gna",
    mandate="Financial health, treasury, R3 payment approvals, and investor reporting.",
    psychology_principles=["loss_aversion", "anchoring", "authority"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R3",
    keywords=["cfo", "financial plan", "cash flow", "burn rate", "runway",
               "fundraise", "investor report", "financial model", "treasury"],
    primary_skills=["financial-projections", "startup-financial-modeling",
                    "billing-automation", "analytics-tracking",
                    "cap-table-modeler", "runway-sensitivity-analysis",
                    "fundraising-data-room"],
))

_r(CompanyRole(
    role_id="role-vp-engineering",
    title="VP Engineering",
    department=CompanyDepartment.EXECUTIVE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-build",
    mandate="Engineering org health, hiring bar, delivery velocity, and incident command.",
    psychology_principles=["commitment", "loss_aversion", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["vp engineering", "engineering manager", "engineering org", "delivery",
               "incident command", "on call", "team health", "hiring bar", "tech interview"],
    primary_skills=["senior-architect", "architect-review", "incident-response",
                    "tech-interview-resume-prep", "engineering-blueprint-planner"],
))


# ── PRODUCT (8 roles) ──────────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-product-director",
    title="Product Director",
    department=CompanyDepartment.PRODUCT.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-build",
    mandate="Own product portfolio, PRD quality, and OKR alignment across squads.",
    psychology_principles=["commitment", "peak_end_rule", "anchoring"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["product director", "product portfolio", "product org", "product ops",
               "product ops director", "squad alignment", "product kpis"],
    primary_skills=["product-manager-toolkit", "feature-development-pipeline",
                    "analytics-product", "kpi-dashboard-design"],
))

_r(CompanyRole(
    role_id="role-senior-pm",
    title="Senior Product Manager",
    department=CompanyDepartment.PRODUCT.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-build",
    mandate="Drive feature discovery, write PRDs, run customer interviews, and prioritize backlog.",
    psychology_principles=["jobs_to_be_done", "peak_end_rule", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["product manager", "prd", "product spec", "user story", "backlog",
               "feature request", "customer interview", "discovery", "mvp", "roadmap"],
    primary_skills=["product-manager-toolkit", "product-manager", "feature-development-pipeline",
                    "concise-planning", "ask-questions-if-underspecified"],
))

_r(CompanyRole(
    role_id="role-pm",
    title="Product Manager",
    department=CompanyDepartment.PRODUCT.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Translate validated user needs into scoped, shippable specifications.",
    psychology_principles=["jobs_to_be_done", "hicks_law", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["pm", "product requirements", "acceptance criteria", "feature spec",
               "stakeholder alignment", "sprint planning", "product backlog"],
    primary_skills=["product-manager", "concise-planning", "pydantic-models-py",
                    "feature-development-pipeline"],
))

_r(CompanyRole(
    role_id="role-scrum-agile-coach",
    title="Scrum / Agile Coach",
    department=CompanyDepartment.PRODUCT.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Facilitate ceremonies, remove blockers, enforce definition of done.",
    psychology_principles=["commitment", "social_proof", "peak_end_rule"],
    allowed_tools=["read_file", "edit_file", "run_command", "search_web"],
    default_risk="R0",
    keywords=["scrum", "agile", "sprint", "retrospective", "daily standup",
               "velocity", "burndown", "kanban", "definition of done", "ceremony"],
    primary_skills=["kanban-agent-pipeline", "project-flow-ops", "developer-session-diary",
                    "conductor-status", "sprint-backlog-grooming",
                    "story-pointing-calibration", "retrospective-synthesis"],
))

_r(CompanyRole(
    role_id="role-ux-researcher",
    title="UX Researcher",
    department=CompanyDepartment.PRODUCT.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Run qualitative and quantitative research, synthesize insights, feed PRDs.",
    psychology_principles=["jobs_to_be_done", "peak_end_rule", "millers_law"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R0",
    keywords=["ux research", "user research", "usability test", "user interview",
               "persona", "journey map", "survey", "feedback synthesis", "insight"],
    primary_skills=["product-manager-toolkit", "data-storytelling", "analytics-tracking",
                    "ask-questions-if-underspecified"],
))

_r(CompanyRole(
    role_id="role-growth-pm",
    title="Growth Product Manager",
    department=CompanyDepartment.PRODUCT.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Own activation, retention, and monetization loops — experiment-driven.",
    psychology_principles=["reciprocity", "loss_aversion", "commitment", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["growth pm", "activation", "retention", "a/b test", "experiment",
               "funnel", "conversion", "north star metric", "growth loop", "campaign", "launch"],
    primary_skills=["ab-test-setup", "analytics-tracking", "page-cro", "posthog-automation",
                    "mixpanel-automation"],
))

_r(CompanyRole(
    role_id="role-product-analyst",
    title="Product Analyst",
    department=CompanyDepartment.PRODUCT.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-build",
    mandate="Instrument events, build dashboards, and surface product health metrics.",
    psychology_principles=["anchoring", "millers_law"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R0",
    keywords=["product analyst", "product metrics", "event tracking", "dashboard",
               "kpi", "data analysis", "product data", "funnel analysis"],
    primary_skills=["analytics-tracking", "kpi-dashboard-design", "data-storytelling",
                    "posthog-automation", "mixpanel-automation"],
))

_r(CompanyRole(
    role_id="role-technical-pm",
    title="Technical Product Manager",
    department=CompanyDepartment.PRODUCT.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-build",
    mandate="Bridge product and engineering; own API contracts, data models, and integration specs.",
    psychology_principles=["commitment", "authority"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["technical pm", "api spec", "openapi", "data model", "integration spec",
               "technical spec", "engineering liaison", "api design"],
    primary_skills=["api-design", "openapi-spec-generation", "pydantic-models-py",
                    "product-manager-toolkit", "feature-development-pipeline"],
))


# ── ENGINEERING (16 roles) ─────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-staff-engineer",
    title="Staff Software Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-build",
    mandate="Drive cross-team technical decisions, mentorship, and architecture reviews.",
    psychology_principles=["authority", "commitment", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["staff engineer", "principal engineer", "architecture review", "rfc",
               "tech design", "cross-team", "tech lead", "system design"],
    primary_skills=["senior-architect", "architecture-decision-records", "code-reviewer",
                    "architect-review", "differential-review"],
))

_r(CompanyRole(
    role_id="role-senior-swe",
    title="Senior Software Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-build",
    mandate="Implement complex features end-to-end, write tests, review peers.",
    psychology_principles=["commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["senior engineer", "feature implementation", "code review", "refactor",
               "backend", "api endpoint", "service", "pull request", "pr"],
    primary_skills=["elite-python-architect", "golang-pro", "rust-pro", "dotnet-backend",
                    "tdd-cycle", "code-reviewer"],
))

_r(CompanyRole(
    role_id="role-swe",
    title="Software Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Implement assigned features, fix bugs, write unit tests with 80%+ coverage.",
    psychology_principles=["commitment"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["software engineer", "bug fix", "implement", "code", "unit test",
               "feature", "handler", "function", "class", "module"],
    primary_skills=["vibe-to-production", "test-driven-development", "code-reviewer", "systematic-debugging",
                    "clean-architecture-craftsmanship"],
))

_r(CompanyRole(
    role_id="role-frontend-engineer",
    title="Frontend Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build responsive, accessible UI components and client-side data flows.",
    psychology_principles=["fitts_law", "hicks_law", "peak_end_rule"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["frontend", "react", "ui component", "typescript", "nextjs", "css",
               "tailwind", "animation", "accessibility", "web", "browser"],
    primary_skills=["react-best-practices", "nextjs-best-practices", "tailwind-patterns",
                    "typescript-expert", "frontend-a11y", "design-spells"],
))

_r(CompanyRole(
    role_id="role-backend-engineer",
    title="Backend Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build scalable APIs, data pipelines, and server-side logic.",
    psychology_principles=["commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["backend", "api", "rest", "graphql", "database", "orm", "migration",
               "fastapi", "django", "express", "grpc", "microservice"],
    primary_skills=["elite-python-architect", "fastapi-patterns", "django-patterns",
                    "golang-pro", "dotnet-backend", "database-architect"],
))

_r(CompanyRole(
    role_id="role-mobile-engineer",
    title="Mobile Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Ship iOS and Android apps with platform-native UX patterns.",
    psychology_principles=["fitts_law", "hicks_law"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["mobile", "ios", "android", "react native", "flutter", "swift",
               "kotlin", "expo", "app store", "push notification"],
    primary_skills=["flutter-expert", "react-native-architecture", "expo-deployment",
                    "swift-concurrency-expert", "kotlin-coroutines-expert"],
))

_r(CompanyRole(
    role_id="role-devops-engineer",
    title="DevOps / Platform Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Maintain CI/CD, cloud infra, container orchestration, and observability.",
    psychology_principles=["commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["devops", "ci/cd", "docker", "kubernetes", "terraform", "github actions",
               "deploy", "pipeline", "infrastructure", "helm", "k8s", "cloud"],
    primary_skills=["terraform-infrastructure-as-code", "gitlab-ci-patterns",
                    "kubernetes-deployment", "docker-patterns", "gitops-workflow"],
))

_r(CompanyRole(
    role_id="role-site-reliability-engineer",
    title="Site Reliability Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-build",
    mandate="Own SLO/SLI, error budget, incident response, and reliability automation.",
    psychology_principles=["loss_aversion", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["sre", "slo", "sli", "error budget", "reliability", "on-call",
               "incident", "postmortem", "chaos engineering", "observability"],
    primary_skills=["slo-setup", "incident-response", "distributed-tracing",
                    "grafana-dashboards", "prometheus-configuration"],
))

_r(CompanyRole(
    role_id="role-security-engineer",
    title="Security Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-gna",
    mandate="Threat modeling, SAST/DAST, penetration testing, secrets management.",
    psychology_principles=["loss_aversion", "authority"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R2",
    keywords=["security", "pentest", "vulnerability", "cve", "sast", "dast",
               "owasp", "injection", "xss", "csrf", "threat model", "appsec"],
    primary_skills=["security-auditor", "sast-scan", "devsecops-guardrails",
                    "red-team-tactics", "secrets-management"],
))

_r(CompanyRole(
    role_id="role-qa-engineer",
    title="QA / Test Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Design test strategies, write E2E suites, and enforce quality gates.",
    psychology_principles=["commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["qa", "test", "e2e", "playwright", "cypress", "selenium", "test case",
               "test plan", "regression", "smoke test", "integration test"],
    primary_skills=["elite-qa-architect", "test-driven-development", "playwright-browser-testing",
                    "pairwise-test-generator", "git-pr-review"],
))

_r(CompanyRole(
    role_id="role-web3-blockchain-eng",
    title="Web3 / Blockchain Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Smart contracts, DeFi protocols, NFT standards, and on-chain analytics.",
    psychology_principles=["authority", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["web3", "blockchain", "smart contract", "solidity", "nft", "defi",
               "ethereum", "evm", "token", "wallet", "on-chain"],
    primary_skills=["solidity-security", "nft-standards", "web3-testing",
                    "defi-amm-security", "defi-protocol-templates"],
))

_r(CompanyRole(
    role_id="role-desktop-app-eng",
    title="Desktop Application Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build cross-platform desktop apps with native OS integrations.",
    psychology_principles=["fitts_law", "hicks_law"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["desktop", "electron", "tauri", "macos app", "windows app", "native app",
               "menubar", "system tray", "swiftui mac", "winui"],
    primary_skills=["electron-development", "macos-menubar-tuist-app",
                    "macos-spm-app-packaging", "swift-concurrency-expert"],
))

_r(CompanyRole(
    role_id="role-network-infra-eng",
    title="Network Infrastructure Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Design, configure, and troubleshoot network routing, VLANs, VPNs, and DNS.",
    psychology_principles=["authority", "commitment"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R2",
    keywords=["network", "routing", "bgp", "vlan", "vpn", "dns", "firewall",
               "cisco", "switch", "load balancer", "cdn", "mtls"],
    primary_skills=["network-engineer", "cisco-ios-patterns", "mtls-configuration",
                    "homelab-network-setup", "homelab-wireguard-vpn"],
))

_r(CompanyRole(
    role_id="role-database-reliability-eng",
    title="Database Reliability Engineer",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-build",
    mandate="Schema design, query optimization, backup/restore, and DB SLOs.",
    psychology_principles=["loss_aversion", "commitment"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R2",
    keywords=["database", "dba", "postgres", "mysql", "mongodb", "schema", "index",
               "query plan", "vacuum", "replication", "backup", "migration"],
    primary_skills=["database-admin", "postgresql-optimization", "database-migrations",
                    "neon-postgres", "sql-optimization-patterns"],
))

_r(CompanyRole(
    role_id="role-incident-commander",
    title="Incident Commander",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-build",
    mandate="Lead live incident response, coordinate roles, drive postmortem action items.",
    psychology_principles=["authority", "loss_aversion", "commitment"],
    allowed_tools=["read_file", "edit_file", "run_command"],
    default_risk="R2",
    keywords=["incident", "outage", "p0", "p1", "incident commander", "postmortem",
               "runbook", "war room", "escalation", "on-call rotation"],
    primary_skills=["incident-response", "postmortem-writing", "incident-responder",
                    "slo-setup", "distributed-tracing"],
))

_r(CompanyRole(
    role_id="role-agentic-workflow-architect",
    title="Agentic Workflow Architect",
    department=CompanyDepartment.ENGINEERING.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-build",
    mandate="Design multi-agent systems, orchestration patterns, and tool permission frameworks.",
    psychology_principles=["authority", "commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["agent", "agentic", "multi-agent", "llm orchestration", "tool calling",
               "autonomous", "workflow", "mcp", "swarm", "orchestration", "agent loop"],
    primary_skills=["autonomous-agents", "autonomous-agent-patterns", "crewai",
                    "multi-agent-patterns", "agents-spec-generator"],
))


# ── DATA & AI (10 roles) ───────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-data-scientist",
    title="Data Scientist",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build predictive models, run experiments, and translate data into decisions.",
    psychology_principles=["authority", "anchoring"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["data science", "machine learning", "model", "prediction", "classification",
               "regression", "feature engineering", "experiment", "notebook", "python"],
    primary_skills=["ml-pipeline-setup", "ml-pipeline-workflow", "scikit-learn",
                    "matplotlib", "statsmodels"],
))

_r(CompanyRole(
    role_id="role-ml-engineer",
    title="ML Engineer",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Productionize ML models, build inference pipelines, and maintain model health.",
    psychology_principles=["commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["mlops", "ml engineer", "model serving", "inference", "hugging face",
               "pytorch", "training", "fine-tuning", "embedding", "vector"],
    primary_skills=["ml-pipeline-workflow", "hugging-face-model-trainer",
                    "embedding-strategies", "vector-database-engineer", "mlops-engineer"],
))

_r(CompanyRole(
    role_id="role-data-engineer",
    title="Data Engineer",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build ETL pipelines, data warehouses, and streaming infrastructure.",
    psychology_principles=["commitment"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["data pipeline", "etl", "dbt", "airflow", "spark", "warehouse",
               "snowflake", "bigquery", "kafka", "streaming", "data lake"],
    primary_skills=["data-engineer", "dbt-transformation-patterns", "spark-optimization",
                    "snowflake-development", "clickhouse-io"],
))

_r(CompanyRole(
    role_id="role-ai-product-engineer",
    title="AI Product Engineer",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build LLM-powered features, RAG pipelines, and prompt systems.",
    psychology_principles=["authority", "social_proof", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["ai feature", "llm", "chatbot", "rag", "retrieval", "prompt engineering",
               "openai", "gemini", "anthropic", "langchain", "vector search"],
    primary_skills=["gemini-api-dev", "rag-implementation", "langchain-architecture",
                    "prompt-engineer", "llm-app-patterns"],
))

_r(CompanyRole(
    role_id="role-data-analyst",
    title="Data Analyst",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-build",
    mandate="Build BI reports, SQL queries, and business dashboards for decisions.",
    psychology_principles=["anchoring", "millers_law"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R0",
    keywords=["data analyst", "sql", "bi", "dashboard", "report", "metrics",
               "looker", "tableau", "power bi", "query", "analysis"],
    primary_skills=["kpi-dashboard-design", "sql-pro", "d3js-visualization",
                    "data-storytelling", "analytics-tracking"],
))

_r(CompanyRole(
    role_id="role-research-scientist",
    title="Research Scientist",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-build",
    mandate="Advance foundational AI capabilities, publish papers, and advise engineering on SOTA.",
    psychology_principles=["authority", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["research", "paper", "arxiv", "model architecture", "training objective",
               "benchmark", "ablation", "neural network", "foundational model"],
    primary_skills=["hugging-face-papers", "scientific-research", "scientific-writing",
                    "neural-networks-foundations-advisor", "benchmark-methodology"],
))

_r(CompanyRole(
    role_id="role-privacy-engineer",
    title="Privacy Engineer",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-gna",
    mandate="PII discovery, anonymization, GDPR/CCPA compliance, and data governance.",
    psychology_principles=["loss_aversion", "authority"],
    allowed_tools=["read_file", "edit_file", "run_command", "search_web"],
    default_risk="R2",
    keywords=["privacy", "pii", "gdpr", "ccpa", "data retention", "anonymization",
               "data governance", "consent", "right to erasure", "dpa"],
    primary_skills=["gdpr-data-handling", "zeroize-audit", "privacy-by-design",
                    "healthcare-phi-compliance", "security-auditor",
                    "dsar-pipeline", "deidentification-benchmark", "crossborder-tia"],
))

_r(CompanyRole(
    role_id="role-computer-vision-eng",
    title="Computer Vision Engineer",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build image/video understanding models and real-time vision pipelines.",
    psychology_principles=["authority"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["computer vision", "image recognition", "object detection", "yolo",
               "opencv", "image classification", "segmentation", "video analysis"],
    primary_skills=["computer-vision-expert", "hugging-face-vision-trainer",
                    "ml-pipeline-workflow", "fal-generate", "fal-upscale"],
))

_r(CompanyRole(
    role_id="role-speech-audio-ai-eng",
    title="Speech & Audio AI Engineer",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build STT/TTS systems, voice agents, and audio analysis pipelines.",
    psychology_principles=["authority", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["speech", "audio", "tts", "stt", "voice", "whisper", "asr",
               "text to speech", "speech recognition", "voicebot", "audio model"],
    primary_skills=["audio-transcriber", "voice-agents", "fal-audio", "ai-voiceover",
                    "azure-ai-transcription-py", "voice-ai-development"],
))

_r(CompanyRole(
    role_id="role-mlops-engineer",
    title="MLOps Engineer",
    department=CompanyDepartment.DATA_AI.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Automate model training, experiment tracking, registry, and deployment.",
    psychology_principles=["commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["mlops", "model registry", "experiment tracking", "mlflow", "wandb",
               "model deployment", "model monitoring", "drift", "retraining pipeline"],
    primary_skills=["mlops-engineer", "ml-pipeline-workflow", "hugging-face-trackio",
                    "hugging-face-jobs", "monitoring-setup"],
))


# ── DESIGN (8 roles) ───────────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-design-director",
    title="Design Director",
    department=CompanyDepartment.DESIGN.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-build",
    mandate="Set visual direction, design system strategy, and cross-product consistency.",
    psychology_principles=["liking", "social_proof", "peak_end_rule"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["design director", "visual direction", "brand direction", "design system",
               "design strategy", "creative direction", "ui direction"],
    primary_skills=["design-system-architect", "brand-guidelines", "hig-foundations",
                    "ui-ux-expert", "design-taste-audit"],
))

_r(CompanyRole(
    role_id="role-ux-ui-designer",
    title="UX / UI Designer",
    department=CompanyDepartment.DESIGN.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Design user flows, wireframes, high-fidelity mockups, and design system components.",
    psychology_principles=["fitts_law", "hicks_law", "peak_end_rule", "millers_law"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["ux", "ui", "design", "figma", "wireframe", "mockup", "prototype",
               "user flow", "ui component", "design system", "layout", "spacing"],
    primary_skills=["ui-ux-designer", "mobile-design", "hig-components-layout",
                    "design-system-spec-generator", "ui-design-guidelines"],
))

_r(CompanyRole(
    role_id="role-product-designer",
    title="Product Designer",
    department=CompanyDepartment.DESIGN.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Design end-to-end product experiences, from discovery through shipped pixels.",
    psychology_principles=["fitts_law", "peak_end_rule", "liking"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["product design", "interaction design", "design thinking", "design sprint",
               "usability", "product experience", "end to end design"],
    primary_skills=["ui-ux-designer", "mobile-design", "hig-patterns",
                    "design-spells", "swiftui-ui-patterns"],
))

_r(CompanyRole(
    role_id="role-brand-designer",
    title="Brand Designer",
    department=CompanyDepartment.DESIGN.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Create visual identity, logo, typography, color systems, and brand assets.",
    psychology_principles=["liking", "social_proof", "unity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["brand design", "logo", "identity", "visual identity", "brand assets",
               "color palette", "typography", "brand guidelines", "style guide"],
    primary_skills=["brand-guidelines", "brand-design-system", "iconsax-library",
                    "image-gen-deprecated", "fal-generate"],
))

_r(CompanyRole(
    role_id="role-motion-designer",
    title="Motion Designer",
    department=CompanyDepartment.DESIGN.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Create UI animations, marketing videos, and motion design assets.",
    psychology_principles=["liking", "peak_end_rule"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["motion design", "animation", "lottie", "after effects", "video",
               "transition", "micro interaction", "motion graphic", "gsap"],
    primary_skills=["magic-animator", "animejs-animation", "animation-vocabulary",
                    "motion-foundations", "react-video-remotion",
                    "video-production-orchestrator", "chopify"],
))

_r(CompanyRole(
    role_id="role-3d-visual-designer",
    title="3D Visual Designer",
    department=CompanyDepartment.DESIGN.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Create 3D renders, WebGL experiences, and real-time 3D design assets.",
    psychology_principles=["liking", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["3d", "three.js", "webgl", "blender", "spline", "shader",
               "3d render", "3d model", "glsl", "real-time 3d"],
    primary_skills=["threejs-webgl-development", "threejs-shaders", "spline-3d-integration",
                    "shader-programming-glsl", "threejs-geometry"],
))

_r(CompanyRole(
    role_id="role-design-system-engineer",
    title="Design System Engineer",
    department=CompanyDepartment.DESIGN.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build and maintain the token-based design system, component library, and documentation.",
    psychology_principles=["commitment", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["design system", "component library", "tokens", "storybook",
               "ui kit", "shadcn", "radix", "tailwind system", "design tokens"],
    primary_skills=["design-system-spec-generator", "ui-tokens", "shadcn-ui-components",
                    "radix-ui-design-system", "tailwind-design-system"],
))

_r(CompanyRole(
    role_id="role-ux-copywriter",
    title="UX Copywriter",
    department=CompanyDepartment.DESIGN.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-build",
    mandate="Write UI strings, error messages, onboarding flows, and microcopy.",
    psychology_principles=["hicks_law", "peak_end_rule", "liking"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R1",
    keywords=["ux copy", "microcopy", "error message", "onboarding copy",
               "ui text", "tooltip", "button label", "placeholder text"],
    primary_skills=["ux-copy", "conversion-copywriting", "content-creator",
                    "avoid-ai-writing", "hook-writer",
                    "microcopy-pattern-library", "onboarding-tooltip-system",
                    "a11y-copy-audit"],
))


# ── MARKETING (10 roles) ───────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-content-strategist",
    title="Content Strategist",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Build content pillars, editorial calendar, and distribution playbook.",
    psychology_principles=["reciprocity", "social_proof", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["content strategy", "content pillars", "editorial", "content calendar",
               "blog", "article", "thought leadership", "content marketing",
               "launch announcement", "announcement"],
    primary_skills=["content-strategy", "content-creator", "seo-content-planner",
                    "data-storytelling", "batch-content-plan"],
))

_r(CompanyRole(
    role_id="role-seo-specialist",
    title="SEO Specialist",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-growth",
    mandate="Technical SEO, keyword research, backlink strategy, and ranking improvement.",
    psychology_principles=["authority", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["seo", "search engine", "keyword research", "backlink", "technical seo",
               "ranking", "serp", "on-page seo", "structured data", "schema"],
    primary_skills=["seo-audit", "seo-keyword-research", "seo-technical",
                    "schema-markup", "seo-content"],
))

_r(CompanyRole(
    role_id="role-performance-marketer",
    title="Performance Marketer",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Run paid acquisition channels, optimize ROAS, and manage ad spend.",
    psychology_principles=["scarcity", "social_proof", "loss_aversion", "anchoring"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R2",
    keywords=["paid ads", "google ads", "meta ads", "ppc", "roas", "cac",
               "ad spend", "performance marketing", "cpm", "ctr", "conversion"],
    primary_skills=["paid-ads", "marketing-campaign", "ad-creative",
                    "analytics-tracking", "ab-test-setup"],
))

_r(CompanyRole(
    role_id="role-social-media-manager",
    title="Social Media Manager",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-growth",
    mandate="Manage social presence, publish content, and grow organic following.",
    psychology_principles=["social_proof", "liking", "reciprocity", "unity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["social media", "instagram", "twitter", "linkedin", "tiktok",
               "post", "reel", "thread", "engagement", "followers", "social strategy"],
    primary_skills=["social-content", "social-strategy", "instagram-growth",
                    "linkedin-growth", "tiktok-growth"],
))

_r(CompanyRole(
    role_id="role-brand-copywriter",
    title="Brand Copywriter",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-growth",
    mandate="Write long-form and short-form brand copy across all channels.",
    psychology_principles=["liking", "social_proof", "reciprocity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["copywriting", "copy", "brand copy", "ad copy", "landing page copy",
               "headline", "value proposition", "tagline", "marketing copy",
               "social marketing", "marketing campaign", "campaign"],
    primary_skills=["conversion-copywriting", "content-creator", "hook-writer",
                    "avoid-ai-writing", "brand-voice"],
))

_r(CompanyRole(
    role_id="role-conversion-optimizer",
    title="Conversion Rate Optimizer",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Run CRO experiments, optimize funnel, and improve activation rates.",
    psychology_principles=["loss_aversion", "scarcity", "social_proof", "anchoring"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["cro", "conversion", "landing page", "a/b test", "funnel",
               "signup flow", "checkout", "bounce rate", "conversion rate"],
    primary_skills=["page-cro", "form-cro", "signup-flow-cro", "ab-test-setup",
                    "analytics-tracking"],
))

_r(CompanyRole(
    role_id="role-email-lifecycle-marketer",
    title="Email & Lifecycle Marketer",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Build drip sequences, re-engagement flows, and lifecycle triggers.",
    psychology_principles=["commitment", "reciprocity", "loss_aversion", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["email", "drip", "lifecycle", "automation", "sequence", "newsletter",
               "re-engagement", "welcome email", "nurture", "klaviyo", "mailchimp"],
    primary_skills=["email-sequence", "brevo-automation", "mailchimp-automation",
                    "klaviyo-automation", "email-ops"],
))

_r(CompanyRole(
    role_id="role-pr-comms-manager",
    title="PR & Communications Manager",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Manage press, company narrative, crisis comms, and analyst relations.",
    psychology_principles=["authority", "social_proof", "unity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["pr", "press release", "media", "journalist", "analyst",
               "crisis communication", "company narrative", "public relations"],
    primary_skills=["content-creator", "avoid-ai-writing", "brand-voice",
                    "internal-comms", "crisis-and-moderation"],
))

_r(CompanyRole(
    role_id="role-partnership-bd-manager",
    title="Partnership & BD Manager",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Identify, negotiate, and activate strategic partnerships and co-marketing deals.",
    psychology_principles=["reciprocity", "liking", "commitment", "unity"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R1",
    keywords=["partnership", "business development", "bd", "co-marketing",
               "integration partner", "affiliate", "ecosystem", "channel partner"],
    primary_skills=["collabs-and-cross-promotion", "market-opportunity",
                    "competitive-landscape", "content-creator",
                    "partner-ecosystem-mapping", "co-marketing-term-sheet-builder",
                    "affiliate-program-ops"],
))

_r(CompanyRole(
    role_id="role-community-manager",
    title="Community Manager",
    department=CompanyDepartment.MARKETING.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-customer",
    mandate="Nurture online communities, run events, and amplify advocates.",
    psychology_principles=["unity", "reciprocity", "social_proof", "liking"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R1",
    keywords=["community", "discord", "slack community", "forum", "user group",
               "advocate", "ambassador", "community event", "community growth"],
    primary_skills=["community-management", "discord-automation", "slack-automation",
                    "social-content", "engagement-routine",
                    "moderation-escalation-ladder", "community-sentiment-trends",
                    "ambassador-event-ops"],
))


# ── SALES & BD (8 roles) ───────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-vp-sales",
    title="VP Sales",
    department=CompanyDepartment.SALES_BD.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-growth",
    mandate="Set revenue targets, build sales motion, and close enterprise deals.",
    psychology_principles=["authority", "social_proof", "commitment", "scarcity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R2",
    keywords=["vp sales", "revenue", "sales leader", "sales strategy",
               "enterprise sales", "sales motion", "quota", "forecast"],
    primary_skills=["sales-automator", "sales-enablement", "market-opportunity",
                    "pitch-psychologist", "startup-analyst"],
))

_r(CompanyRole(
    role_id="role-account-executive",
    title="Account Executive",
    department=CompanyDepartment.SALES_BD.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Run full sales cycle from discovery to close for target accounts.",
    psychology_principles=["commitment", "social_proof", "liking", "scarcity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["account executive", "sales", "deal", "prospect", "demo",
               "proposal", "close", "contract", "pipeline", "account"],
    primary_skills=["sales-automator", "sales-enablement", "pitch-psychologist",
                    "hubspot-integration", "pipedrive-automation"],
))

_r(CompanyRole(
    role_id="role-sales-development-rep",
    title="Sales Development Representative",
    department=CompanyDepartment.SALES_BD.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-growth",
    mandate="Prospect, qualify leads, and book discovery calls for AEs.",
    psychology_principles=["reciprocity", "social_proof", "liking"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["sdr", "bdr", "outreach", "cold email", "cold call", "prospecting",
               "lead qualification", "discovery call", "sequence"],
    primary_skills=["cold-email", "apify-lead-generation", "sales-automator",
                    "linkedin-growth", "social-selling-and-dm"],
))

_r(CompanyRole(
    role_id="role-solutions-engineer",
    title="Solutions Engineer",
    department=CompanyDepartment.SALES_BD.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Technical pre-sales, solution design, POC builds, and RFP responses.",
    psychology_principles=["authority", "commitment", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["solutions engineer", "presales", "technical sales", "poc",
               "rfp", "demo", "technical evaluation", "integration proof"],
    primary_skills=["sales-enablement", "api-design", "product-manager-toolkit",
                    "content-creator", "pitch-psychologist"],
))

_r(CompanyRole(
    role_id="role-customer-success-manager",
    title="Customer Success Manager",
    department=CompanyDepartment.SALES_BD.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-customer",
    mandate="Drive product adoption, NPS, and expansion revenue within accounts.",
    psychology_principles=["commitment", "reciprocity", "social_proof", "liking"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["customer success", "csm", "adoption", "nps", "churn", "expansion",
               "renewal", "qbr", "account health", "upsell"],
    primary_skills=["sop-customer", "churn-prevention", "hubspot-integration",
                    "analytics-tracking", "email-sequence"],
))

_r(CompanyRole(
    role_id="role-revenue-operations",
    title="Revenue Operations Analyst",
    department=CompanyDepartment.SALES_BD.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="CRM hygiene, sales analytics, pipeline reporting, and territory management.",
    psychology_principles=["commitment", "anchoring"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R1",
    keywords=["revops", "revenue operations", "crm", "salesforce", "hubspot crm",
               "pipeline", "forecast", "territory", "sales reporting"],
    primary_skills=["revenue-operations-analytics", "hubspot-automation",
                    "salesforce-automation", "kpi-dashboard-design", "analytics-tracking"],
))

_r(CompanyRole(
    role_id="role-enterprise-ae",
    title="Enterprise Account Executive",
    department=CompanyDepartment.SALES_BD.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-growth",
    mandate="Navigate complex enterprise buying cycles, MSA negotiation, and champion development.",
    psychology_principles=["authority", "commitment", "social_proof", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R2",
    keywords=["enterprise", "enterprise sales", "msa", "procurement", "legal review",
               "champion", "executive sponsor", "security review", "soc2 request"],
    primary_skills=["sales-enablement", "legal-advisor", "pitch-psychologist",
                    "master-agreement-generator", "hubspot-integration"],
))

_r(CompanyRole(
    role_id="role-freelancer-sales",
    title="Freelancer Business Development",
    department=CompanyDepartment.SALES_BD.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-growth",
    mandate="Win freelance projects, write proposals, negotiate rates, and close clients.",
    psychology_principles=["reciprocity", "social_proof", "commitment", "liking"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["freelance", "proposal", "client acquisition", "rate negotiation",
               "project scope", "statement of work", "sow", "retainer", "upwork"],
    primary_skills=["freelancer-sales-closing", "freelancer-client-acquisition",
                    "freelancer-project-delivery", "pitch-psychologist", "content-creator"],
))


# ── CUSTOMER SUCCESS (6 roles) ─────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-support-engineer",
    title="Support Engineer",
    department=CompanyDepartment.CUSTOMER_SUCCESS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-customer",
    mandate="Diagnose and resolve technical customer issues, write runbooks.",
    psychology_principles=["empathy", "commitment", "peak_end_rule"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R1",
    keywords=["support", "ticket", "customer issue", "bug report", "helpdesk",
               "troubleshoot", "error log", "api error", "integration error"],
    primary_skills=["sop-customer", "systematic-debugging", "incident-response",
                    "customer-support", "postmortem-writing"],
))

_r(CompanyRole(
    role_id="role-onboarding-specialist",
    title="Onboarding Specialist",
    department=CompanyDepartment.CUSTOMER_SUCCESS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-customer",
    mandate="Guide new customers through activation milestones and first value moments.",
    psychology_principles=["commitment", "reciprocity", "liking", "peak_end_rule"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["onboarding", "new customer", "activation", "welcome", "kickoff",
               "setup guide", "first value", "time to value", "ttv"],
    primary_skills=["sop-customer", "email-sequence", "onboarding-cro",
                    "customer-support", "content-creator"],
))

_r(CompanyRole(
    role_id="role-implementation-consultant",
    title="Implementation Consultant",
    department=CompanyDepartment.CUSTOMER_SUCCESS.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-customer",
    mandate="Customize and deploy product for enterprise clients, manage project plan.",
    psychology_principles=["authority", "commitment", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["implementation", "professional services", "deployment", "configuration",
               "client customization", "enterprise deployment", "project plan"],
    primary_skills=["sop-customer", "project-flow-ops", "developer-session-diary",
                    "api-design", "content-creator"],
))

_r(CompanyRole(
    role_id="role-technical-account-manager",
    title="Technical Account Manager",
    department=CompanyDepartment.CUSTOMER_SUCCESS.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-customer",
    mandate="Serve as technical partner for strategic accounts, drive health and expansion.",
    psychology_principles=["commitment", "liking", "authority", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["tam", "technical account manager", "strategic account",
               "account health", "technical advisory", "roadmap preview"],
    primary_skills=["sop-customer", "api-design", "analytics-tracking",
                    "pitch-psychologist", "content-creator"],
))

_r(CompanyRole(
    role_id="role-churn-analyst",
    title="Churn & Retention Analyst",
    department=CompanyDepartment.CUSTOMER_SUCCESS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-customer",
    mandate="Model churn risk, trigger save plays, and report retention metrics.",
    psychology_principles=["loss_aversion", "commitment", "social_proof"],
    allowed_tools=["read_file", "edit_file", "run_command", "search_web"],
    default_risk="R0",
    keywords=["churn", "retention", "cancellation", "save play", "win-back",
               "churned customer", "logo retention", "nrr"],
    primary_skills=["churn-prevention", "analytics-tracking", "kpi-dashboard-design",
                    "email-sequence", "data-storytelling",
                    "cohort-retention-curves", "customer-health-score",
                    "nps-sentiment-root-cause"],
))

_r(CompanyRole(
    role_id="role-docs-technical-writer",
    title="Technical Writer",
    department=CompanyDepartment.CUSTOMER_SUCCESS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-customer",
    mandate="Write API docs, product guides, tutorials, and release notes.",
    psychology_principles=["authority", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["documentation", "technical writing", "api docs", "user guide",
               "tutorial", "readme", "release notes", "docs site"],
    primary_skills=["documentation-generation-doc-generate", "api-documenter",
                    "wiki-architect", "app-store-changelog", "git-pr-review"],
))


# ── FINANCE (8 roles) ──────────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-corporate-controller",
    title="Corporate Controller",
    department=CompanyDepartment.FINANCE.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-gna",
    mandate="Own financial close, general ledger, and GAAP compliance.",
    psychology_principles=["authority", "loss_aversion", "commitment"],
    allowed_tools=["read_file"],
    default_risk="R3",
    keywords=["controller", "general ledger", "financial close", "gaap",
               "accounts payable", "accounts receivable", "journal entry", "accrual"],
    primary_skills=["financial-projections", "billing-automation",
                    "startup-financial-modeling", "analytics-tracking"],
))

_r(CompanyRole(
    role_id="role-fp-and-a-analyst",
    title="FP&A Analyst",
    department=CompanyDepartment.FINANCE.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-gna",
    mandate="Financial planning, variance analysis, and board-ready models.",
    psychology_principles=["anchoring", "loss_aversion"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R0",
    keywords=["fp&a", "financial planning", "forecast", "variance", "budget",
               "headcount plan", "board deck", "financial model", "scenario analysis"],
    primary_skills=["financial-projections", "startup-financial-modeling",
                    "data-storytelling", "kpi-dashboard-design"],
))

_r(CompanyRole(
    role_id="role-tax-compliance-spec",
    title="Tax & Compliance Specialist",
    department=CompanyDepartment.FINANCE.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-gna",
    mandate="Tax filings, transfer pricing, VAT/GST, and regulatory compliance.",
    psychology_principles=["authority", "loss_aversion"],
    allowed_tools=["read_file"],
    default_risk="R2",
    keywords=["tax", "vat", "gst", "transfer pricing", "tax filing", "compliance",
               "irs", "customs", "international tax", "tax strategy"],
    primary_skills=["customs-trade-compliance", "legal-advisor",
                    "legal-compliance-consultant", "financial-projections"],
))

_r(CompanyRole(
    role_id="role-billing-payments-eng",
    title="Billing & Payments Engineer",
    department=CompanyDepartment.FINANCE.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-gna",
    mandate="Implement Stripe/payment flows, subscription logic, and dunning management.",
    psychology_principles=["commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["stripe", "billing", "subscription", "payment", "invoice",
               "dunning", "webhook", "charge", "refund", "payment gateway"],
    primary_skills=["stripe-integration", "stripe-automation", "payment-integration",
                    "billing-automation", "pci-compliance"],
))

_r(CompanyRole(
    role_id="role-treasury-banking-spec",
    title="Treasury & Banking Specialist",
    department=CompanyDepartment.FINANCE.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-gna",
    mandate="Manage cash, wire transfers, banking relationships, and FX exposure.",
    psychology_principles=["loss_aversion", "authority"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R3",
    keywords=["treasury", "wire transfer", "bank account", "fx", "forex",
               "cash management", "banking", "liquidity", "disbursement"],
    primary_skills=["financial-projections", "billing-automation",
                    "startup-financial-modeling", "customs-trade-compliance",
                    "daily-cashflow-forecast", "fx-hedging-advisor",
                    "settlement-reconciliation-audit"],
))

_r(CompanyRole(
    role_id="role-accounts-manager",
    title="Accounts Manager",
    department=CompanyDepartment.FINANCE.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-gna",
    mandate="Process invoices, AR/AP, reconciliations, and expense reports.",
    psychology_principles=["commitment", "authority"],
    allowed_tools=["read_file", "edit_file", "run_command", "search_web"],
    default_risk="R2",
    keywords=["accounts", "invoice", "ar", "ap", "reconcile", "expense",
               "receipt", "reimbursement", "purchase order", "vendor payment"],
    primary_skills=["billing-automation", "financial-projections",
                    "stripe-automation", "analytics-tracking",
                    "ap-ar-aging-schedules", "ledger-reconciliation",
                    "collections-dunning-automation"],
))

_r(CompanyRole(
    role_id="role-startup-cfo-advisor",
    title="Startup CFO Advisor",
    department=CompanyDepartment.FINANCE.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-gna",
    mandate="Fractional CFO advising on fundraise, cap table, and strategic finance.",
    psychology_principles=["authority", "anchoring", "loss_aversion"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R2",
    keywords=["fractional cfo", "cap table", "fundraise", "term sheet", "safe",
               "convertible note", "equity", "dilution", "investor"], 
    primary_skills=["financial-projections", "startup-financial-modeling",
                    "startup-analyst", "pitch-psychologist"],
))

_r(CompanyRole(
    role_id="role-cost-optimization-analyst",
    title="Cost Optimization Analyst",
    department=CompanyDepartment.FINANCE.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-gna",
    mandate="Identify and execute cost savings across cloud, vendors, and operations.",
    psychology_principles=["loss_aversion", "anchoring"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R1",
    keywords=["cost optimization", "cloud cost", "aws cost", "vendor cost",
               "cost reduction", "spend analysis", "savings", "efficiency"],
    primary_skills=["aws-cost-optimizer", "aws-cost-cleanup", "cost-optimization",
                    "analytics-tracking", "kpi-dashboard-design"],
))


# ── LEGAL & COMPLIANCE (6 roles) ───────────────────────────────────────────

_r(CompanyRole(
    role_id="role-general-counsel",
    title="General Counsel",
    department=CompanyDepartment.LEGAL_COMPLIANCE.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-gna",
    mandate="Legal strategy, contract approval, employment law, and regulatory posture.",
    psychology_principles=["authority", "loss_aversion", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R3",
    keywords=["general counsel", "legal strategy", "regulatory", "litigation",
               "employment law", "corporate governance", "legal risk"],
    primary_skills=["legal-advisor", "legal-compliance-consultant",
                    "legal-contract-truth-engine", "gdpr-data-handling",
                    "corporate-governance-resolutions", "litigation-regulatory-risk-scanner"],
))

_r(CompanyRole(
    role_id="role-ip-patent-attorney",
    title="IP & Patent Attorney",
    department=CompanyDepartment.LEGAL_COMPLIANCE.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-gna",
    mandate="IP strategy, patent filings, trademark, and open-source license compliance.",
    psychology_principles=["authority", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R2",
    keywords=["ip", "patent", "trademark", "copyright", "open source license",
               "mit license", "gpl", "ip strategy", "trade secret"],
    primary_skills=["legal-contract-truth-engine", "scientific-db-uspto-database",
                    "legal-advisor", "legal-compliance-consultant",
                    "prior-art-search", "patent-claim-drafter", "oss-license-risk-audit"],
))

_r(CompanyRole(
    role_id="role-contract-manager",
    title="Contract Manager",
    department=CompanyDepartment.LEGAL_COMPLIANCE.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-gna",
    mandate="Draft, review, and execute MSAs, NDAs, SOWs, and vendor agreements.",
    psychology_principles=["commitment", "loss_aversion", "authority"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R2",
    keywords=["contract", "msa", "nda", "sow", "agreement", "terms",
               "vendor contract", "client contract", "redline", "clause"],
    primary_skills=["legal-contract-truth-engine", "master-agreement-generator",
                    "employment-contract-templates", "legal-advisor",
                    "redline-diff-analyzer", "renewal-and-liability-watch"],
))

_r(CompanyRole(
    role_id="role-compliance-officer",
    title="Compliance Officer",
    department=CompanyDepartment.LEGAL_COMPLIANCE.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-gna",
    mandate="Regulatory mapping, compliance programs, audit readiness, and policy enforcement.",
    psychology_principles=["authority", "loss_aversion", "commitment"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R2",
    keywords=["compliance", "regulatory", "soc2", "iso 27001", "hipaa",
               "gdpr", "audit", "policy", "control", "risk framework"],
    primary_skills=["gdpr-data-handling", "healthcare-phi-compliance",
                    "pci-compliance", "security-auditor", "legal-compliance-consultant"],
))

_r(CompanyRole(
    role_id="role-data-protection-officer",
    title="Data Protection Officer",
    department=CompanyDepartment.LEGAL_COMPLIANCE.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-gna",
    mandate="Data governance, DPIA, breach notification, and DPA negotiations.",
    psychology_principles=["authority", "loss_aversion"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R2",
    keywords=["dpo", "data protection", "dpia", "breach notification", "data governance",
               "consent management", "privacy policy", "data transfer"],
    primary_skills=["gdpr-data-handling", "privacy-by-design", "zeroize-audit",
                    "legal-compliance-consultant", "healthcare-phi-compliance"],
))

_r(CompanyRole(
    role_id="role-risk-manager",
    title="Risk Manager",
    department=CompanyDepartment.LEGAL_COMPLIANCE.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-gna",
    mandate="Enterprise risk framework, risk register, insurance, and business continuity.",
    psychology_principles=["loss_aversion", "authority", "commitment"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R1",
    keywords=["risk", "risk register", "risk framework", "business continuity",
               "disaster recovery", "insurance", "risk assessment", "mitigation"],
    primary_skills=["security-auditor", "legal-compliance-consultant",
                    "incident-response", "financial-projections"],
))


# ── PEOPLE & OPS (10 roles) ────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-vp-people",
    title="VP People",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L8.value,
    governing_pod="pod-people",
    mandate="People strategy, culture, compensation, and talent planning.",
    psychology_principles=["unity", "commitment", "reciprocity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R2",
    keywords=["vp people", "hr strategy", "culture", "talent strategy", "compensation",
               "people ops", "org design", "hr leader", "people team"],
    primary_skills=["sop-people", "hr-pro", "employment-contract-templates",
                    "analytics-tracking", "financial-projections"],
))

_r(CompanyRole(
    role_id="role-recruiter",
    title="Talent Recruiter",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-people",
    mandate="Source, screen, and close candidates across engineering and business roles.",
    psychology_principles=["liking", "social_proof", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["recruiter", "hiring", "candidate", "resume", "screening",
               "job description", "interview", "offer", "talent acquisition"],
    primary_skills=["sop-people", "hr-pro", "tech-interview-resume-prep",
                    "apify-lead-generation", "linkedin-growth"],
))

_r(CompanyRole(
    role_id="role-hr-business-partner",
    title="HR Business Partner",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-people",
    mandate="Strategic HR advisory to business units on performance, culture, and org design.",
    psychology_principles=["unity", "commitment", "liking"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["hrbp", "hr partner", "performance review", "pip", "org design",
               "team health", "culture", "employee engagement", "l&d"],
    primary_skills=["sop-people", "hr-pro", "content-creator",
                    "analytics-tracking", "employment-contract-templates"],
))

_r(CompanyRole(
    role_id="role-hr-ops-specialist",
    title="HR Operations Specialist",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-people",
    mandate="HRIS administration, payroll coordination, benefits, and onboarding logistics.",
    psychology_principles=["commitment", "authority"],
    allowed_tools=["read_file", "edit_file", "run_command", "search_web"],
    default_risk="R2",
    keywords=["hr ops", "hris", "payroll", "benefits", "offer letter",
               "onboarding logistics", "offboarding", "hr admin"],
    primary_skills=["employment-contract-templates", "hr-pro",
                    "billing-automation", "analytics-tracking",
                    "payroll-cycle-ops", "benefits-leave-administration",
                    "workforce-compliance-tracker"],
))

_r(CompanyRole(
    role_id="role-learning-development",
    title="L&D Specialist",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-people",
    mandate="Design training programs, skill gap analysis, and career development paths.",
    psychology_principles=["commitment", "reciprocity", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["learning", "training", "development", "l&d", "skill gap",
               "career path", "mentorship", "onboarding program", "course"],
    primary_skills=["hr-pro", "content-creator", "data-storytelling",
                    "ai-engineering-toolkit", "educational-content-and-how-to"],
))

_r(CompanyRole(
    role_id="role-procurement-vendor-manager",
    title="Procurement & Vendor Manager",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-gna",
    mandate="Vendor evaluation, contract negotiation, purchase orders, and supplier management.",
    psychology_principles=["authority", "loss_aversion", "commitment"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command", "search_web"],
    default_risk="R2",
    keywords=["procurement", "vendor", "supplier", "purchase order", "rfp",
               "vendor evaluation", "contract negotiation", "sourcing"],
    primary_skills=["customs-trade-compliance", "inventory-demand-planning",
                    "legal-contract-truth-engine", "financial-projections",
                    "vendor-rfp-generator", "vendor-spend-consolidator",
                    "vendor-sla-breach-watch"],
))

_r(CompanyRole(
    role_id="role-office-facilities-manager",
    title="Office & Facilities Manager",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-gna",
    mandate="Physical workspace, equipment, travel, and office operations.",
    psychology_principles=["commitment", "liking"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R1",
    keywords=["office", "facilities", "workspace", "equipment", "travel",
               "remote work", "co-working", "office setup", "hardware"],
    primary_skills=["freelancer-operations", "file-organizer",
                    "analytics-tracking", "content-creator"],
))

_r(CompanyRole(
    role_id="role-executive-assistant",
    title="Executive Assistant",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-gna",
    mandate="Calendar management, meeting coordination, travel, and executive communications.",
    psychology_principles=["commitment", "liking", "reciprocity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["executive assistant", "ea", "calendar", "scheduling", "meeting",
               "travel booking", "inbox management", "executive support"],
    primary_skills=["google-calendar-automation", "gmail-automation",
                    "outlook-automation", "content-creator", "linear-automation"],
))

_r(CompanyRole(
    role_id="role-solopreneur-operator",
    title="Solopreneur Operator",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-gna",
    mandate="Run all operational functions as a solo founder using AI leverage.",
    psychology_principles=["commitment", "unity", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["solopreneur", "solo founder", "bootstrapped", "indie hacker",
               "one person company", "operator", "founder operator"],
    primary_skills=["freelancer-operations", "freelancer-identity", "file-organizer",
                    "developer-session-diary", "context-save"],
))

_r(CompanyRole(
    role_id="role-chief-of-staff",
    title="Chief of Staff",
    department=CompanyDepartment.PEOPLE_OPS.value,
    seniority=SeniorityLevel.L6.value,
    governing_pod="pod-gna",
    mandate="Strategic projects, executive leverage, cross-pod coordination, and OKR tracking.",
    psychology_principles=["commitment", "authority", "unity"],
    allowed_tools=["read_file", "edit_file", "write_file"],
    default_risk="R1",
    keywords=["chief of staff", "cos", "strategic project", "executive ops",
               "cross-functional", "okr", "board prep", "agenda"],
    primary_skills=["freelancer-operations", "kpi-dashboard-design",
                    "analytics-tracking", "content-creator", "linear-project-management"],
))


# ── IT & INFRA (6 roles) ───────────────────────────────────────────────────

_r(CompanyRole(
    role_id="role-it-systems-admin",
    title="IT Systems Administrator",
    department=CompanyDepartment.IT_INFRA.value,
    seniority=SeniorityLevel.L4.value,
    governing_pod="pod-build",
    mandate="Manage SaaS stack, device management, IAM, and IT helpdesk.",
    psychology_principles=["authority", "commitment"],
    allowed_tools=["read_file", "edit_file", "run_command"],
    default_risk="R2",
    keywords=["it admin", "sysadmin", "device management", "mdm", "iam", "sso",
               "okta", "active directory", "it support", "it helpdesk"],
    primary_skills=["win11-system-manager", "linux-troubleshooting",
                    "bash-scripting", "server-management", "it-manager-pro"],
))

_r(CompanyRole(
    role_id="role-cloud-architect",
    title="Cloud Architect",
    department=CompanyDepartment.IT_INFRA.value,
    seniority=SeniorityLevel.L7.value,
    governing_pod="pod-build",
    mandate="Design multi-cloud architecture, cost governance, and infra standards.",
    psychology_principles=["authority", "commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["cloud architect", "aws architecture", "azure architecture",
               "gcp", "multi-cloud", "infra design", "landing zone", "well-architected"],
    primary_skills=["aws-cloud-architecture", "multi-cloud-architecture",
                    "azure-ai-projects-py", "terraform-infrastructure-as-code",
                    "cost-optimization"],
))

_r(CompanyRole(
    role_id="role-platform-engineer",
    title="Platform Engineer",
    department=CompanyDepartment.IT_INFRA.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Build internal developer platforms, golden paths, and self-service infra.",
    psychology_principles=["commitment", "social_proof"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R2",
    keywords=["platform", "idp", "internal platform", "golden path", "developer experience",
               "dx", "self-service", "infra as code", "paved road"],
    primary_skills=["kubernetes-deployment", "terraform-infrastructure-as-code",
                    "gitops-workflow", "monitoring-setup", "distributed-tracing"],
))

_r(CompanyRole(
    role_id="role-cybersecurity-analyst",
    title="Cybersecurity Analyst",
    department=CompanyDepartment.IT_INFRA.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-gna",
    mandate="Monitor threats, run vulnerability assessments, and manage SIEM.",
    psychology_principles=["loss_aversion", "authority"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R2",
    keywords=["cybersecurity", "threat", "vulnerability", "siem", "soc",
               "incident detection", "malware", "phishing", "pentest"],
    primary_skills=["security-auditor", "red-team-tactics", "sast-scan",
                    "managed-pentesting-with-strix", "malware-analyst"],
))

_r(CompanyRole(
    role_id="role-observability-engineer",
    title="Observability Engineer",
    department=CompanyDepartment.IT_INFRA.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-build",
    mandate="Instrument services with distributed tracing, metrics, and log aggregation.",
    psychology_principles=["commitment", "loss_aversion"],
    allowed_tools=["read_file", "edit_file", "write_file", "run_command"],
    default_risk="R1",
    keywords=["observability", "tracing", "metrics", "logs", "otel", "opentelemetry",
               "prometheus", "grafana", "loki", "tempo", "datadog"],
    primary_skills=["distributed-tracing", "grafana-dashboards", "prometheus-configuration",
                    "monitoring-setup", "service-mesh-observability"],
))

_r(CompanyRole(
    role_id="role-finops-cloud-cost",
    title="FinOps / Cloud Cost Engineer",
    department=CompanyDepartment.IT_INFRA.value,
    seniority=SeniorityLevel.L5.value,
    governing_pod="pod-gna",
    mandate="Cloud cost visibility, rightsizing, reserved capacity, and FinOps culture.",
    psychology_principles=["loss_aversion", "anchoring"],
    allowed_tools=["read_file", "edit_file"],
    default_risk="R1",
    keywords=["finops", "cloud cost", "aws cost", "cost visibility", "rightsizing",
               "reserved instances", "savings plans", "cloud spend", "cost alert"],
    primary_skills=["aws-cost-optimizer", "aws-cost-cleanup", "cost-optimization",
                    "analytics-tracking", "kpi-dashboard-design"],
))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_role(role_id: str) -> Optional[CompanyRole]:
    """Return a role by its role_id, or None if not found."""
    return _REGISTRY.get(role_id)


def list_roles(
    department: Optional[str] = None,
    seniority: Optional[str] = None,
) -> List[CompanyRole]:
    """Return all roles, optionally filtered by department and/or seniority."""
    roles = list(_REGISTRY.values())
    if department:
        roles = [r for r in roles if r.department == department]
    if seniority:
        roles = [r for r in roles if r.seniority == seniority]
    return roles


_ROLES_SKILLS_MATRIX: Optional[Dict[str, Any]] = None


def _get_matrix() -> Dict[str, Any]:
    global _ROLES_SKILLS_MATRIX
    if _ROLES_SKILLS_MATRIX is None:
        parent_dir = Path(__file__).resolve().parent.parent / "skills"
        matrix_path_toon = parent_dir / "roles-skills-matrix.toon"
        matrix_path_json = parent_dir / "roles-skills-matrix.json"

        if matrix_path_toon.is_file():
            try:
                from .toon_codec import decode_toon
                records = decode_toon(matrix_path_toon.read_text(encoding="utf-8"))
                by_role: Dict[str, Any] = {}
                by_skill: Dict[str, Any] = {}
                for r in records:
                    r_id = r.get("role_id", "")
                    skills = [s for s in r.get("skills", "").split("|") if s]
                    primary = [s for s in r.get("primary_skills", "").split("|") if s]
                    by_role[r_id] = {
                        "role_id": r_id,
                        "title": r.get("title", ""),
                        "department": r.get("department", ""),
                        "seniority": r.get("seniority", ""),
                        "governing_pod": r.get("governing_pod", ""),
                        "primary_skills": primary,
                        "skills": skills,
                    }
                    for s in skills:
                        if s not in by_skill:
                            by_skill[s] = {"primary_role": r_id, "roles": [r_id]}
                        elif r_id not in by_skill[s]["roles"]:
                            by_skill[s]["roles"].append(r_id)
                _ROLES_SKILLS_MATRIX = {"by_role": by_role, "by_skill": by_skill}
            except Exception:
                _ROLES_SKILLS_MATRIX = {}
        elif matrix_path_json.is_file():
            try:
                with open(matrix_path_json, "r", encoding="utf-8") as f:
                    _ROLES_SKILLS_MATRIX = json.load(f)
            except Exception:
                _ROLES_SKILLS_MATRIX = {}
        else:
            _ROLES_SKILLS_MATRIX = {}
    return _ROLES_SKILLS_MATRIX


def get_skills_for_role(role_id: str, all_skills: bool = False) -> List[str]:
    """Return skill names for a given role_id.

    If all_skills is False (default), returns role.primary_skills.
    If all_skills is True, returns all skills mapped to this role in skills-by-role.
    """
    role = _REGISTRY.get(role_id)
    if role is None:
        return []
    if not all_skills:
        return list(role.primary_skills)

    matrix = _get_matrix()
    by_role = matrix.get("by_role", {})
    if role_id in by_role:
        return list(by_role[role_id].get("skills", role.primary_skills))
    return list(role.primary_skills)


def get_all_skills_for_role(role_id: str) -> List[str]:
    """Return the complete list of mapped skills (core + specialized) for a given role_id."""
    return get_skills_for_role(role_id, all_skills=True)


def get_role_for_skill(skill_name: str) -> Optional[Dict[str, Any]]:
    """Look up which role(s) own a given skill."""
    matrix = _get_matrix()
    by_skill = matrix.get("by_skill", {})
    return by_skill.get(skill_name)


def get_primary_role_for_skill(skill_name: str) -> Optional[str]:
    """Return the primary owning role_id for a skill."""
    info = get_role_for_skill(skill_name)
    if info and info.get("primary_role"):
        return info["primary_role"]
    skills_root = Path(__file__).resolve().parent.parent / "skills"
    for match in skills_root.glob(f"*/{skill_name}"):
        if match.is_dir():
            return match.parent.name
    return None


POD_DEFAULT_ROLES: Dict[str, str] = {
    "pod-build": "role-swe",
    "pod-growth": "role-growth-pm",
    "pod-customer": "role-support-engineer",
    "pod-gna": "role-coo",
    "pod-people": "role-recruiter",
}


def classify_role_for_task(query: str, pod: Optional[str] = None) -> CompanyRole:
    """Match a natural language query to the best-fit CompanyRole.

    Scoring: keyword match weight (phrase length bonus) with word-boundary enforcement.
    If pod is specified, filters candidate roles to those in that governing pod.
    Falls back to safe default role for that pod (or role-swe) when no keywords match.
    """
    lower = query.lower()
    best_role: Optional[CompanyRole] = None
    best_score = -1

    candidates = [r for r in _REGISTRY.values() if pod is None or r.governing_pod == pod]

    for role in candidates:
        score = 0
        for kw in role.keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", lower):
                score += len(kw.split()) * 3 + 2  # longer phrases score much higher
        if score > best_score:
            best_score = score
            best_role = role

    # Always return a role — use pod default or swe safe fallback
    if best_role is None or best_score == 0:
        fallback_id = POD_DEFAULT_ROLES.get(pod, "role-swe") if pod else "role-swe"
        return _REGISTRY.get(fallback_id, _REGISTRY["role-swe"])
    return best_role
