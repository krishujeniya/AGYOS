"""AGYOS Decision Engine — Autonomous Skill Routing & Selection.

Evaluates task intent, technical domains, and complexity against AGYOS's 1,862+
skills catalog to decide the optimal specialist skill and workflow gate.
Catalog metadata is validated with the repository's PyYAML dependency.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .catalog import canonical_entry, physical_catalog

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
            "animate", "animation", "motion", "transition", "micro-interaction", "spring",
            "keyframes", "gsap", "framer", "threejs", "canvas", "svg", "tween"
        ],
        "primary": "motion-patterns",
        "alternatives": ["motion-foundations", "review-animations", "animation-performance", "threejs-animation"],
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
            "tradeoff", "tradeoffs", "vs", "versus", "differing", "second opinion", "panel"
        ],
        "primary": "council",
        "alternatives": ["council-multi-model", "council-revisit", "council-outcome"],
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
        "primary": "freelancer-project-delivery",
        "alternatives": ["freelancer-client-acquisition", "freelancer-operations", "freelancer-sales-closing"],
    },
    "startup": {
        "keywords": [
            "startup", "founder", "stack", "bootstrap", "venture", "pre-seed",
            "seed", "fundraising", "pitch deck", "pitch", "mvp", "early stage"
        ],
        "primary": "agyos-startup-stack",
        "alternatives": ["agyos-founder-guide", "agyos-startup-distribution", "market-opportunity", "financial-projections"],
    },
    "reverse_engineering": {
        "keywords": [
            "binary", "disassembly", "decompile", "decompilation", "ghidra",
            "hopper", "ida", "frida", "hook", "assembly", "reversing",
            "reverse engineer", "elf", "protocol re"
        ],
        "primary": "agyos-binary-analysis",
        "alternatives": ["binary-analysis-patterns", "protocol-reverse-engineering", "anti-reversing-techniques"],
    },
    "software_protection": {
        "keywords": [
            "obfuscation", "control-flow flattening", "opaque predicate",
            "anti-debug", "anti-reversing", "tamper", "software protection",
            "binary hardening", "symbol stripping"
        ],
        "primary": "agyos-software-protection",
        "alternatives": ["security-hardening", "anti-reversing-techniques", "sast-scan"],
    },
    "simulation_prediction": {
        "keywords": [
            "swarm", "simulation", "prediction", "forecast", "synthetic population",
            "graphrag", "scenario simulation", "market prediction", "scenario"
        ],
        "primary": "agyos-swarm-prediction-engine",
        "alternatives": ["prediction-market-oracle-research", "multi-agent-patterns", "swot-pestel-market-analysis"],
    },
    "academic_research": {
        "keywords": [
            "academic", "literature review", "citation", "scholar", "paper",
            "arxiv", "systematic review", "peer-reviewed", "research gap"
        ],
        "primary": "agyos-academic-research",
        "alternatives": ["scientific-thinking-literature-review", "citation-management", "scientific-research"],
    },
    "coding_discipline": {
        "keywords": [
            "karpathy", "clean code", "surgical changes", "overcomplication",
            "simplification", "llm coding", "simplicity"
        ],
        "primary": "agyos-karpathy-guidelines",
        "alternatives": ["clean-code", "simplify-code", "code-simplifier"],
    },
    "agency_operations": {
        "keywords": [
            "agency", "creative agency", "pod dispatch", "agency agents",
            "account management", "deliverables"
        ],
        "primary": "agyos-agency-agents",
        "alternatives": ["team-agent-orchestration", "freelancer-operations", "dev-team"],
    },
    "lead_generation": {
        "keywords": [
            "lead", "leads", "prospect", "scraping", "lead scraper",
            "google maps scraper", "business directory", "outreach list"
        ],
        "primary": "agyos-lead-scraper",
        "alternatives": ["apify-lead-generation", "lead-intelligence", "data-scraper-agent"],
    },
    "app_launch": {
        "keywords": [
            "launch checklist", "app launch", "production checklist", "favicon",
            "opengraph", "meta tags", "pre-launch"
        ],
        "primary": "agyos-app-launch-checklist",
        "alternatives": ["app-manifest-generator", "seo-audit", "favicon-generator"],
    },
    "free_infrastructure": {
        "keywords": [
            "free tier", "free infra", "free cloud", "free host",
            "free database", "free compute", "free for dev"
        ],
        "primary": "agyos-free-infra-catalog",
        "alternatives": ["cost-optimization", "aws-cost-cleanup"],
    },
    "anti_ai_design": {
        "keywords": [
            "anti ai design", "purple gradient", "ai look", "banned font",
            "boring ui", "fresh design"
        ],
        "primary": "agyos-anti-ai-design",
        "alternatives": ["design-spells", "frontend-design-direction", "apple-design"],
    },
    "skill_routing": {
        "keywords": ["skill", "skills", "runbook", "runbooks", "skill routing", "decision engine"],
        "primary": "agyos-decision",
        "alternatives": ["skill-creator", "eval-harness", "verification-loop"],
    },
    "android_verification": {
        "keywords": ["android screen", "android emulator", "android ui", "adb", "screen visually"],
        "primary": "android_ui_verification",
        "alternatives": ["android-clean-architecture", "android-jetpack-compose-expert"],
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
    "angular": "angular-best-practices",
    "flutter": "flutter-expert",
    "svelte": "sveltekit",
    "docker": "docker-patterns",
    "k8s": "kubernetes-patterns",
    "kubernetes": "kubernetes-patterns",
    "postgres": "postgres-best-practices",
    "bun": "bun-development",
    "tailwind": "tailwind-patterns",
    "expo": "expo-api-routes",
    "swift": "swiftui-patterns",
    "solidity": "solidity-security",
}


def load_catalog() -> List[Dict[str, Any]]:
    """Prefer the runtime manifest; recover from stale or missing generated data."""
    for source in (MANIFEST_DATA, DOCS_DATA):
        try:
            raw = json.loads(source.read_text(encoding="utf-8"))
            entries = raw.get("skills", []) if isinstance(raw, dict) else raw
            if not isinstance(entries, list):
                continue
            valid = [item for entry in entries if (item := canonical_entry(entry))]
            physical_names = {p.parent.name for p in (REPO_ROOT / ".agents/skills").glob("*/SKILL.md")}
            if {s["name"] for s in valid} == physical_names and len(valid) == len(physical_names):
                return valid
        except (OSError, ValueError, TypeError):
            continue
    return physical_catalog()


def keyword_matches(keyword: str, query: str) -> bool:
    """Match complete words and phrases, never accidental substrings."""
    return bool(re.search(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", query, re.I))


def classify_domain(query: str) -> Tuple[str, float]:
    """Classify domain using bounded words and weighted phrases."""
    scores: Dict[str, int] = {}

    for domain, data in DOMAIN_TAXONOMY.items():
        kws = data["keywords"]
        hits = sum(len(kw.split()) + (2 if " " in kw else 0) for kw in kws if keyword_matches(kw, query))
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

    if any(keyword_matches(phrase, lower) for phrase in [
        "delete production", "drop database", "drop table", "wire money",
        "deploy to production", "production deployment", "send payment",
    ]):
        return 5, "high-impact external or destructive action (full workflow; authorization required)"

    # Complexity 5: cross-system architectural overhaul, protocol change, breaking schema migration
    if any(w in lower for w in [
        "redesign architecture", "protocol change", "breaking change",
        "distributed transaction", "monorepo migration", "security audit full"
    ]):
        return 5, "cross-module architectural overhaul (full 5-gate workflow + council deliberation)"

    # Complexity 4: multi-file refactoring, major migration, security reviews
    if any(keyword_matches(w, lower) for w in ["refactor", "migrate", "migration", "migrations", "rewrite", "threat model", "vulnerability", "security", "permissions", "jwt", "auth", "authentication", "payment", "payments", "all rules", "all skills"]):
        return 4, "multi-file structural change (full 5-gate workflow + ADR)"

    if length <= 6 and any(keyword_matches(w, lower) for w in ["typo", "rename", "fix link", "remove log", "comment", "spelling"]):
        return 1, "trivial single-line edit (fast-path bypass)"

    # Complexity 3: standard feature development, bug fix with regression check
    if any(w in lower for w in ["add", "implement", "create", "test", "feature", "endpoint", "service", "fix bug"]):
        return 3, "standard feature development (5-gate workflow)"

    if any(keyword_matches(phrase, lower) for phrase in ["single function", "single-file", "one file"]):
        return 2, "explicitly bounded modification (fast-path bypass)"
    return 3, "scope requires inspection (standard 5-gate workflow)"


def score_skill_fit(skill: Dict[str, Any], query: str, domain: str) -> float:
    """Calculate a deterministic relevance heuristic, not a probability."""
    name = skill.get("name", "").lower()
    desc = skill.get("description", "").lower()
    tokens = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
    score = 0.0

    # Exact skill name match
    clean_query = query.lower().strip()
    if keyword_matches(name, clean_query) or clean_query.replace("-", " ") == name.replace("-", " "):
        score += 1000.0

    # Framework exact mapping
    for fw, sk in LANGUAGE_FRAMEWORK_MAP.items():
        if fw in tokens and name == sk:
            score += 45.0

    # Domain primary and alternative alignment
    if domain in DOMAIN_TAXONOMY:
        domain_info = DOMAIN_TAXONOMY[domain]
        if domain_info["primary"] == name:
            score += 220.0
        elif name in domain_info.get("alternatives", []):
            score += 50.0

    # Token-level matching
    name_tokens = set(re.split(r"[-_]", name))
    for token in tokens:
        if token == name:
            score += 50.0
        elif token in name_tokens:
            score += 35.0
        elif token in name:
            score += 25.0
        if token in desc:
            score += 8.0

    # Tier 1 priority boost
    if score > 0 and skill.get("tier") == 1:
        score += 15.0

    return score


def select_best_skills(query: str, catalog: Optional[List[Dict[str, Any]]] = None, limit: int = 5) -> List[Dict[str, Any]]:
    """Rank catalog skills against the query and domain."""
    if limit <= 0:
        return []
    if catalog is None:
        catalog = load_catalog()

    domain, _ = classify_domain(query)
    scored: List[Tuple[float, Dict[str, Any]]] = []

    for s in catalog:
        fit = score_skill_fit(s, query, domain)
        if fit > 0:
            scored.append((fit, s))

    scored.sort(key=lambda x: (-x[0], x[1]["name"]))
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
    if not isinstance(query, str) or not query.strip():
        raise ValueError("A non-empty task description is required")
    catalog = load_catalog()
    if not catalog:
        raise ValueError("No valid skill catalog is available")
    domain, domain_conf = classify_domain(query)
    complexity, complexity_reason = assess_complexity(query)
    candidates = select_best_skills(query, catalog, limit=5)
    explicit = any(keyword_matches(s["name"], query) for s in catalog)
    technology = any(keyword_matches(name, query) for name in LANGUAGE_FRAMEWORK_MAP)
    ignored = {"please", "help", "use", "run", "check", "inspect", "review", "explain",
               "implement", "add", "create", "write", "show", "tell", "want", "need",
               "how", "can", "the", "with", "for", "this", "and", "from"}
    task_tokens = set(re.findall(r"\w+", query.lower())) - ignored
    catalog_match = any(
        len(token) > 2
        for candidate in candidates
        for token in task_tokens & set(re.split(r"[-_]", candidate["name"]))
    )
    fallback = domain == "general" and not explicit and not technology and not catalog_match

    if candidates and not fallback:
        primary = candidates[0]
    else:
        fallback_name = DOMAIN_TAXONOMY.get(domain, {}).get("primary", "agyos-decision")
        entry = next((s for s in catalog if s["name"] == fallback_name), None)
        if entry is None:
            raise ValueError(f"Required fallback skill missing from catalog: {fallback_name}")
        primary = {
            **entry,
            "rank": 1,
            "name": fallback_name,
            "score": 50.0,
            "confidence": 0.60,
            "tier": 1,
            "description": "Default specialist for domain",
            "path": f".agents/skills/{fallback_name}",
        }
        candidates = [primary]

    runbook_path = f"{primary.get('path', '')}/SKILL.md"
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
        "confidence_kind": "heuristic_not_probability",
        "selection_status": "fallback" if fallback else "matched",
        "execution_status": "pending_runbook_read",
        "runbook_path": runbook_path,
        "runbook_command": f"bin/agyos skill {primary['name']}",
        "read_tool_call": f"read_file(Path='{runbook_path}')",
        "execution_invariant": f"Autonomous Skill Invariant: Ingest runbook at {runbook_path} and adhere to domain rules before mutating code.",
        "candidates": candidates,
    }
