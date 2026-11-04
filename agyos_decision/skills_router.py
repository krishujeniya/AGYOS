"""AGYOS Decision Engine — Autonomous Skill Routing & Selection.

Evaluates task intent, technical domains, and complexity against AGYOS's 1,842+
skills catalog to decide the optimal specialist skill and workflow gate.
Zero external dependencies; pure Python standard library.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DATA = REPO_ROOT / "docs" / "skills-data.json"
MANIFEST_DATA = REPO_ROOT / ".agents" / "skills-manifest.json"

# Domain taxonomy with domain keywords and curated specialist fallbacks
DOMAIN_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "debugging": {
        "keywords": [
            "bug", "error", "exception", "crash", "failure", "fail", "broken",
            "fix", "diagnose", "leak", "reproduce", "traceback", "stacktrace",
            "regression", "flaky", "segfault", "panic", "hang", "freeze"
        ],
        "primary": "diagnosing-bugs",
        "alternatives": ["systematic-debugging", "find-bugs", "smart-debug", "debug-toolkit"],
    },
    "architecture": {
        "keywords": [
            "architecture", "design", "adr", "c4", "system", "modular",
            "boundary", "refactor", "monorepo", "microservices", "domain",
            "ddd", "clean", "hexagonal", "separation", "scaffold"
        ],
        "primary": "architecture-decision-records",
        "alternatives": ["senior-architect", "c4-architecture", "hexagonal-architecture", "api-design"],
    },
    "ui_ux": {
        "keywords": [
            "ui", "ux", "frontend", "interface", "layout", "css", "tailwind",
            "shadcn", "component", "styling", "responsive", "design", "modal",
            "button", "navbar", "dropdown", "theme", "dark mode", "accessibility", "a11y"
        ],
        "primary": "frontend-design-direction",
        "alternatives": ["apple-design", "break-ui", "design-spells", "tailwind-patterns", "shadcn-ui-components"],
    },
    "motion": {
        "keywords": [
            "animation", "motion", "transition", "micro-interaction", "spring",
            "keyframes", "gsap", "framer", "threejs", "canvas", "svg", "tween"
        ],
        "primary": "animate",
        "alternatives": ["review-animation", "animation-performance", "motion-patterns", "threejs-animation"],
    },
    "security": {
        "keywords": [
            "security", "audit", "vulnerability", "cve", "auth", "token", "jwt",
            "secret", "key", "owasp", "xss", "csrf", "sqli", "injection", "sast",
            "pentest", "permission", "rbac", "threat", "sandbox", "pentagi"
        ],
        "primary": "security-review",
        "alternatives": ["pentagi-orchestrator", "cve-vulnerability-intelligence", "sast-scan", "threat-modeling-expert"],
    },
    "verification": {
        "keywords": [
            "test", "testing", "verify", "verification", "tdd", "unit", "e2e",
            "integration", "jest", "pytest", "playwright", "assert", "coverage",
            "ratchet", "gate", "falsifiable", "proof", "mock", "stub"
        ],
        "primary": "verification-loop",
        "alternatives": ["test-driven-development", "tdd-cycle", "e2e-testing", "code-reviewer", "eval-harness"],
    },
    "database": {
        "keywords": [
            "database", "db", "sql", "postgres", "postgresql", "mysql", "sqlite",
            "redis", "prisma", "drizzle", "migration", "schema", "query", "index",
            "orm", "table", "foreign key", "relation"
        ],
        "primary": "database-design",
        "alternatives": ["postgres-best-practices", "database-migrations", "database-schema-modeling", "architecture-database-design"],
    },
    "performance": {
        "keywords": [
            "performance", "perf", "latency", "benchmark", "optimize", "speed",
            "throughput", "bottleneck", "profile", "profiling", "slow", "cache",
            "memory usage", "cpu", "overhead"
        ],
        "primary": "benchmark-optimization-loop",
        "alternatives": ["performance-engineer", "performance-profiling", "web-performance-optimization"],
    },
    "devops": {
        "keywords": [
            "devops", "docker", "container", "kubernetes", "k8s", "deploy", "ci",
            "cd", "pipeline", "git", "github actions", "gitlab", "infra", "release",
            "terraform", "cloud", "aws", "gcp", "azure"
        ],
        "primary": "gitops-workflow",
        "alternatives": ["docker-patterns", "kubernetes-patterns", "cicd-workflow", "github-workflow-automation"],
    },
    "seo": {
        "keywords": [
            "seo", "search", "ranking", "crawl", "index", "sitemap", "meta",
            "schema.org", "json-ld", "opengraph", "canonical", "robots.txt", "keywords"
        ],
        "primary": "seo-audit",
        "alternatives": ["programmatic-seo", "schema-markup", "geo-fundamentals", "seo-technical"],
    },
    "governance": {
        "keywords": [
            "governance", "5-gate", "milestone", "compact", "workflow", "state",
            "understand", "analyze", "plan", "implement", "verify", "gate"
        ],
        "primary": "agyos-orchestrator",
        "alternatives": ["agyos-scout", "agyos-verify", "agyos-scope", "agyos-draft-commit"],
    },
    "council": {
        "keywords": [
            "council", "deliberation", "consensus", "multi-model", "compare",
            "tradeoff", "differing", "second opinion", "panel"
        ],
        "primary": "agent-council",
        "alternatives": ["council-multi-model", "council-revisit"],
    },
    "content": {
        "keywords": [
            "doc", "docs", "documentation", "readme", "write", "content",
            "changelog", "article", "guide", "tutorial", "spec", "copy"
        ],
        "primary": "technical-documentation-writer",
        "alternatives": ["project-readme-generator", "content-engine", "doc-generator"],
    },
    "freelance": {
        "keywords": [
            "freelance", "client", "proposal", "sow", "invoice", "hourly",
            "contract", "delivery", "rate", "pitch", "consulting"
        ],
        "primary": "agentic-freelance-skills",
        "alternatives": ["freelancer-client-acquisition", "freelancer-project-delivery", "freelancer-operations"],
    },
}

LANGUAGE_FRAMEWORK_MAP = {
    "python": "python-patterns",
    "fastapi": "fastapi-patterns",
    "django": "django-patterns",
    "rust": "rust-patterns",
    "golang": "golang-patterns",
    "go": "golang-patterns",
    "typescript": "typescript-patterns",
    "react": "react-patterns",
    "nextjs": "nextjs-best-practices",
    "next": "nextjs-best-practices",
    "vue": "vue-patterns",
    "angular": "angular-patterns",
    "docker": "docker-patterns",
    "k8s": "kubernetes-patterns",
    "kubernetes": "kubernetes-patterns",
    "postgres": "postgres-best-practices",
    "bun": "bun-development",
    "tailwind": "tailwind-patterns",
    "expo": "expo-api-routes",
    "swift": "swiftui-patterns",
}


def load_catalog() -> List[Dict[str, Any]]:
    """Load skill catalog from docs data or manifest."""
    if DOCS_DATA.exists():
        try:
            raw = json.loads(DOCS_DATA.read_text(encoding="utf-8"))
            return [
                {
                    "name": s.get("id") or s.get("name"),
                    "tier": s.get("tier", 1),
                    "description": s.get("description", ""),
                    "path": s.get("path") or f".agents/skills/{s.get('id')}",
                    "category": (s.get("category") or s.get("module") or "").lower(),
                }
                for s in raw
                if s.get("id") or s.get("name")
            ]
        except Exception:
            pass

    if MANIFEST_DATA.exists():
        try:
            raw = json.loads(MANIFEST_DATA.read_text(encoding="utf-8"))
            return raw.get("skills", [])
        except Exception:
            pass

    return []


def classify_domain(query: str) -> Tuple[str, float]:
    """Classify the technical domain with calibrated confidence."""
    tokens = set(re.findall(r"\w+", query.lower()))
    scores: Dict[str, int] = {}

    for domain, data in DOMAIN_TAXONOMY.items():
        kws = data["keywords"]
        hits = sum(1 for kw in kws if kw in tokens or any(kw in t for t in tokens))
        if hits > 0:
            scores[domain] = hits

    if not scores:
        return "general", 0.50

    best_domain = max(scores, key=lambda k: scores[k])
    confidence = min(0.98, 0.55 + (scores[best_domain] * 0.12))
    return best_domain, confidence


def assess_complexity(query: str) -> Tuple[int, str]:
    """Assess task complexity on a 1-5 scale to route gate progression."""
    lower = query.lower()
    words = re.findall(r"\w+", lower)
    length = len(words)

    # Complexity 1: single-line typo, string tweak, log deletion
    if length <= 6 and any(w in lower for w in ["typo", "rename", "fix link", "remove log", "comment", "spelling"]):
        return 1, "trivial single-line edit (fast-path bypass)"

    # Complexity 5: cross-system architectural overhaul, protocol change, breaking schema migration
    if any(w in lower for w in [
        "redesign architecture", "protocol change", "breaking change",
        "distributed transaction", "monorepo migration", "security audit full"
    ]):
        return 5, "cross-module architectural overhaul (full 5-gate workflow + council deliberation)"

    # Complexity 4: multi-file refactoring, major migration, security reviews
    if any(w in lower for w in ["refactor", "migrate", "rewrite", "threat model", "vulnerability", "auth flow"]):
        return 4, "multi-file structural change (full 5-gate workflow + ADR)"

    # Complexity 3: standard feature development, bug fix with regression check
    if any(w in lower for w in ["add", "implement", "create", "test", "feature", "endpoint", "service", "fix bug"]):
        return 3, "standard feature development (5-gate workflow)"

    # Complexity 2: bounded single-function or single-file fix
    return 2, "bounded single-file modification (fast-path bypass)"


def score_skill_fit(skill: Dict[str, Any], query: str, domain: str) -> float:
    """Calculate calibrated relevance score for a skill."""
    name = skill.get("name", "").lower()
    desc = skill.get("description", "").lower()
    tokens = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
    score = 0.0

    # Exact skill name match
    clean_query = query.lower().strip()
    if clean_query == name or clean_query.replace("-", " ") == name.replace("-", " "):
        score += 250.0

    # Framework exact mapping
    for fw, sk in LANGUAGE_FRAMEWORK_MAP.items():
        if fw in tokens and name == sk:
            score += 120.0

    # Domain primary and alternative alignment
    if domain in DOMAIN_TAXONOMY:
        domain_info = DOMAIN_TAXONOMY[domain]
        if domain_info["primary"] == name:
            score += 90.0
        elif name in domain_info.get("alternatives", []):
            score += 50.0

    # Token-level matching
    for token in tokens:
        if token == name:
            score += 50.0
        elif token in name:
            score += 25.0
        if token in desc:
            score += 8.0

    # Tier 1 priority boost
    if skill.get("tier") == 1:
        score += 15.0

    return score


def select_best_skills(query: str, catalog: Optional[List[Dict[str, Any]]] = None, limit: int = 5) -> List[Dict[str, Any]]:
    """Rank catalog skills against the query and domain."""
    if catalog is None:
        catalog = load_catalog()

    domain, _ = classify_domain(query)
    scored: List[Tuple[float, Dict[str, Any]]] = []

    for s in catalog:
        fit = score_skill_fit(s, query, domain)
        if fit > 0:
            scored.append((fit, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = []

    top_score = scored[0][0] if scored else 1.0

    for rank, (score, skill) in enumerate(scored[:limit], start=1):
        rel_confidence = min(0.99, max(0.40, score / (top_score + 10.0)))
        results.append({
            "rank": rank,
            "name": skill["name"],
            "score": round(score, 1),
            "confidence": round(rel_confidence, 2),
            "tier": skill.get("tier", 1),
            "description": skill.get("description", ""),
            "path": skill.get("path", f".agents/skills/{skill['name']}"),
        })

    return results


def decide_skill(query: str) -> Dict[str, Any]:
    """Execute complete decision pipeline for a task."""
    catalog = load_catalog()
    domain, domain_conf = classify_domain(query)
    complexity, complexity_reason = assess_complexity(query)
    candidates = select_best_skills(query, catalog, limit=5)

    if candidates:
        primary = candidates[0]
    else:
        fallback_name = DOMAIN_TAXONOMY.get(domain, {}).get("primary", "codebase-onboarding")
        primary = {
            "rank": 1,
            "name": fallback_name,
            "score": 50.0,
            "confidence": 0.60,
            "tier": 1,
            "description": "Default specialist for domain",
            "path": f".agents/skills/{fallback_name}",
        }

    return {
        "task": query,
        "classification": {
            "domain": domain,
            "confidence": domain_conf,
            "complexity_score": complexity,
            "workflow_guidance": complexity_reason,
            "fast_path_eligible": complexity <= 2,
        },
        "primary_skill": primary["name"],
        "primary_path": primary.get("path", ""),
        "confidence": primary.get("confidence", 0.70),
        "candidates": candidates,
    }
