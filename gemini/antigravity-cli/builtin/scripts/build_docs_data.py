#!/usr/bin/env python3
"""
Compile comprehensive skills database and SEO assets for AGYOS documentation site.
Indexes all physical skills from gemini/skills/ and generates:
- docs/skills-data.json
- docs/ai-catalog.json
- frontend/sitemap.xml
- frontend/robots.txt
- frontend/llms.txt
- frontend/.nojekyll
Applies unslop rules to remove AI buzzwords, decorative symbols, and fluff.
"""

import os
import json
import re
import sys
from pathlib import Path

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(REPO_ROOT)))
sys.path.insert(0, REPO_ROOT)
from agyos_decision.catalog import read_metadata
from agyos_decision.toon_config import dump_toon_config, dump_toon_manifest
DOCS_DIR = os.path.join(WORKSPACE_ROOT, "docs")
FRONTEND_DIR = os.path.join(WORKSPACE_ROOT, "frontend")
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")
MANIFEST_PATH_TOON = os.path.join(os.path.dirname(REPO_ROOT), "skills-manifest.toon")
MANIFEST_PATH = os.path.join(os.path.dirname(REPO_ROOT), "skills-manifest.json")

AI_WORDS_MAP = {
    r"\bleverage\b": "use",
    r"\bleveraging\b": "using",
    r"\butilize\b": "use",
    r"\butilizing\b": "using",
    r"\bdelve\b": "explore",
    r"\bdelving\b": "exploring",
    r"\bseamless\b": "direct",
    r"\bseamlessly\b": "directly",
    r"\brobust\b": "reliable",
    r"\brobustness\b": "reliability",
    r"\bcrucial\b": "essential",
    r"\bparamount\b": "primary",
    r"\btestament\b": "proof",
    r"\btapestry\b": "collection",
    r"\bfoster\b": "support",
    r"\bfostering\b": "supporting",
    r"\belevate\b": "improve",
    r"\belevating\b": "improving",
    r"\bgame-changer\b": "major advance",
    r"\bgame changer\b": "major advance",
    r"\bdive deep\b": "inspect thoroughly",
    r"\bdive into\b": "inspect",
    r"\bmultifaceted\b": "broad",
    r"\bplethora\b": "wide range",
    r"\bfurthermore\b": "also",
    r"\bmoreover\b": "also",
    r"\bholistic\b": "complete",
    r"\bsynergy\b": "coordination",
    r"\bunleash\b": "enable",
    r"\bnavigating\b": "handling",
    r"\bintricate\b": "complex",
    r"\bvibrant\b": "active",
    r"\bpivotal\b": "critical",
    r"\benduring\b": "lasting",
    r"\bgroundbreaking\b": "practical",
    r"\btransformative\b": "effective",
    r"\brevolutionary\b": "novel"
}

def unslop(text: str) -> str:
    """Strip AI buzzwords, em dashes, and high-unicode emojis."""
    if not text:
        return ""
    clean = re.sub(r"[\U00010000-\U0010ffff]", "", text)
    clean = re.sub(r"[\u2600-\u27bf]", "", clean)
    clean = re.sub(r"[\u2300-\u23ff]", "", clean)
    clean = clean.replace("—", ", ").replace("–", "-")
    for pattern, replacement in AI_WORDS_MAP.items():
        clean = re.sub(pattern, replacement, clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

def extract_frontmatter(skill_dir: Path):
    """Use strict shared discovery metadata; do not hide invalid headers."""
    skill_file = skill_dir / "SKILL.toon" if (skill_dir / "SKILL.toon").is_file() else skill_dir / "SKILL.md"
    metadata = read_metadata(skill_file)
    return metadata["name"], metadata["description"].strip()

def classify_skill(sid: str, name: str, desc: str):
    """Classify a skill into an AGYOS module and category."""
    sid_lower = sid.lower()
    desc_lower = desc.lower()

    if sid_lower.startswith(("agyos-", "anchor-")):
        return "AGYOS Governance", "Governance"
    if sid_lower.startswith("council-") or sid_lower in ("council", "council"):
        return "Agent Council", "Deliberation"
    if (
        sid_lower.startswith(("emil-", "animate", "apple-design", "motion-", "swiftui-", "tailwind-", "threejs-", "ui-", "shadcn", "radix-", "chrome-extension"))
        or sid_lower in ("break-ui", "scrollheart", "bang-motion", "design-spells", "design-taste-frontend", "ask-sonner", "find-animation", "improve-animation", "remove-animation", "review-animation", "modern-web-guidance", "chrome-extensions")
        or "emil kowalski" in desc_lower
        or "animation" in desc_lower
        or "modern web" in desc_lower
    ):
        return "UI/UX & Motion", "Frontend & Motion"
    if sid_lower.startswith(("seo", "geo-")) or "seo" in sid_lower:
        return "Technical SEO", "SEO & Discovery"
    if sid_lower.startswith(("freelancer-", "freelance-")):
        return "Freelance Suite", "Client & Operations"
    if (
        sid_lower.startswith(("tdd-", "test-", "debug", "eval-", "benchmark-"))
        or sid_lower in ("systematic-debugging", "diagnosing-bugs", "verification-loop", "e2e-testing", "code-reviewer")
        or "tdd" in desc_lower
        or "verification" in desc_lower
    ):
        return "Verification & Testing", "QA & Testing"
    if (
        sid_lower.startswith(("security-", "sast-", "threat-", "pentagi-"))
        or sid_lower in ("secret-agent-007", "dev-orchestrator", "credential-manager", "security-review")
        or "security" in desc_lower
        or "vulnerability" in desc_lower
    ):
        return "Security & Defense", "Security"
    if sid_lower.startswith(("python-", "rust-", "golang-", "go-", "typescript-", "react-", "vue-", "angular-", "django-", "fastapi-", "postgres-", "docker-", "k8s-", "git-", "c-", "haskell-", "julia-", "ruby-")):
        return "AGYOS Polyglot Engineering", "Languages & Runtimes"
    return "Domain & Research Extensions", "Specialized"

def load_manifest_lookup():
    """Load existing manifest for tier lookup if available."""
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {item["name"]: item.get("tier", 2) for item in data.get("skills", [])}
        except Exception:
            pass
    return {}

def compile_all_skills():
    """Scan role-based builtin/skills/<role-id>/<skill>/ and return deduplicated, classified skills."""
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            manifest_skills = manifest.get("skills", [])
            physical_count = sum(
                1
                for role_dir in os.listdir(SKILLS_DIR)
                if os.path.isdir(os.path.join(SKILLS_DIR, role_dir))
                for e in os.listdir(os.path.join(SKILLS_DIR, role_dir))
                if os.path.isdir(os.path.join(SKILLS_DIR, role_dir, e))
                and (
                    os.path.exists(os.path.join(SKILLS_DIR, role_dir, e, "SKILL.toon"))
                    or os.path.exists(os.path.join(SKILLS_DIR, role_dir, e, "SKILL.md"))
                )
            )
            if len(manifest_skills) == physical_count:
                skills = []
                for m in manifest_skills:
                    entry = m["name"]
                    role_id = m.get("role", "role-swe")
                    clean_desc = unslop(m.get("description", "") or f"{entry} skill for AGYOS.")
                    module, category = classify_skill(entry, entry, clean_desc)
                    skills.append({
                        "id": entry,
                        "name": entry.replace("-", " ").title(),
                        "role": role_id,
                        "module": module,
                        "category": category,
                        "tier": m.get("tier", 2),
                        "runtime": ["AGY CLI", "Gemini", "Claude Code", "Codex"],
                        "command": f"bin/agyos skill {entry}",
                        "path": m.get("path", f"skills/{role_id}/{entry}"),
                        "risk": "assess_for_task",
                        "description": clean_desc
                    })
                return skills
        except Exception:
            pass

    manifest_tiers = load_manifest_lookup()
    skills = []
    seen = set()

    for role_id in sorted(os.listdir(SKILLS_DIR)):
        role_path = os.path.join(SKILLS_DIR, role_id)
        if not os.path.isdir(role_path):
            continue
        for entry in sorted(os.listdir(role_path)):
            entry_path = os.path.join(role_path, entry)
            if not os.path.isdir(entry_path) or entry in seen:
                continue
            skill_file = os.path.join(entry_path, "SKILL.md")
            if not os.path.exists(skill_file) and not os.path.exists(os.path.join(entry_path, "SKILL.toon")):
                continue

            raw_name, raw_desc = extract_frontmatter(Path(entry_path))
            clean_desc = unslop(raw_desc or f"{entry} skill for AGYOS.")
            module, category = classify_skill(entry, raw_name, clean_desc)
            tier = manifest_tiers.get(entry, 1 if module in ("AGYOS Governance", "Agent Council", "UI/UX & Motion", "Verification & Testing", "Security & Defense") else 2)

            skill_obj = {
                "id": entry,
                "name": raw_name.replace("-", " ").title() if raw_name == entry else raw_name,
                "role": role_id,
                "module": module,
                "category": category,
                "tier": tier,
                "runtime": ["AGY CLI", "Gemini", "Claude Code", "Codex"],
                "command": f"bin/agyos skill {entry}",
                "path": f"skills/{role_id}/{entry}",
                "risk": "assess_for_task",
                "description": clean_desc
            }
            seen.add(entry)
            skills.append(skill_obj)

    return skills

def write_json_files(skills):
    """Write skills-data.json and ai-catalog.json into docs/."""
    os.makedirs(DOCS_DIR, exist_ok=True)
    data_out = os.path.join(DOCS_DIR, "skills-data.json")
    with open(data_out, "w", encoding="utf-8") as f:
        json.dump(skills, f, indent=2)
    print(f"Saved: {data_out}")

    catalog_out = os.path.join(DOCS_DIR, "ai-catalog.json")
    catalog_data = {
        "name": "AGYOS",
        "description": "The Autonomous Cognitive Operating System for AGY CLI.",
        "url": "https://agyos.pages.dev/",
        "version": "3.1.0",
        "total_skills": len(skills),
        "modules": [
            "AGYOS Governance",
            "Agent Council",
            "UI/UX & Motion",
            "Technical SEO",
            "Freelance Suite",
            "AGYOS Polyglot Engineering",
            "Verification & Testing",
            "Security & Defense",
            "Domain & Research Extensions"
        ],
        "runtimes_supported": ["AGY CLI", "Gemini", "Claude Code", "Codex", "Bun"]
    }
    with open(catalog_out, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2)
    print(f"Saved: {catalog_out}")

def write_seo_files(skills):
    """Write sitemap.xml, robots.txt, llms.txt, and .nojekyll into frontend/."""
    os.makedirs(FRONTEND_DIR, exist_ok=True)
    sitemap_out = os.path.join(FRONTEND_DIR, "sitemap.xml")
    public_docs_path = Path(FRONTEND_DIR) / "public-docs.json"
    doc_routes = []
    if public_docs_path.is_file():
        public_docs = json.loads(public_docs_path.read_text(encoding="utf-8"))
        doc_routes = [f"docs/{doc['slug'].strip('/')}/" for doc in public_docs.get("documents", [])]
    extra_urls = ["catalog/", *doc_routes]
    sitemap_urls = [
        f'  <url>\n    <loc>https://agyos.pages.dev/{route}</loc>\n    <lastmod>2026-11-25</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>'
        for route in extra_urls
    ]
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://agyos.pages.dev/</loc>
    <lastmod>2026-11-25</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
{chr(10).join(sitemap_urls)}
</urlset>
"""
    with open(sitemap_out, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"Saved: {sitemap_out}")

    robots_out = os.path.join(FRONTEND_DIR, "robots.txt")
    with open(robots_out, "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: https://agyos.pages.dev/sitemap.xml\n")
    print(f"Saved: {robots_out}")

    llms_out = os.path.join(FRONTEND_DIR, "llms.txt")
    rules_cnt = len(list((Path(REPO_ROOT) / 'rules').glob('*.toon'))) or len(list((Path(REPO_ROOT) / 'rules').glob('*.md')))
    agents_cnt = len(list((Path(REPO_ROOT) / 'agents').glob('*.toon'))) or len(list((Path(REPO_ROOT) / 'agents').glob('*.md')))
    workflows_cnt = len(list((Path(REPO_ROOT) / 'workflows').glob('*.toon'))) or len(list((Path(REPO_ROOT) / 'workflows').glob('*.md')))
    llms_content = f"""# AGYOS Documentation

> The Autonomous Cognitive Operating System for AGY CLI (`agy`).
> Maintained By Krish Ujeniya (@krishujeniya).
> Total skills documented: {len(skills)}
> Total modular rules: {rules_cnt}
> Total role agents: {agents_cnt}
> Total workflow pipelines: {workflows_cnt}

## Core Operating Subsystems

- AGYOS Governance: 5-Gate spine (UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT -> VERIFY) with FastMCP JSON-RPC 2.0 daemon and adaptive fast-path.
- Model Registry & Router: 4-Tier task mapping (T0–T3), context economics (55/20/15/10), compaction trigger at 65% utilization, and strict fail-closed privacy gating (LOCAL_INFERENCE_UNAVAILABLE).
- Architecture Research & Standards Crosswalk: Empirical synthesis of 45 verified principles from 10 reference platforms (OpenHands, agent-zero, LangGraph, etc.) and 41 FAANG/SRE/DevOps public standards.
- Security & Cryptographic Architecture: STRIDE threat model, at-rest AES-256-GCM private memory vault, X25519 secure envelope exchange, dual hooks (agy_os_hook.py + authorizer.py), and transparent PARTIAL_ENCRYPTION_NOT_SYSTEM_WIDE_E2EE boundaries.
- Agent Council: Multi-model CLI consensus engine deliberating across models in parallel Bun subprocesses.
- UI/UX & Motion: Emil Kowalski design engineering invariants: concentric border radii, frequency-based timing, compositor-only animations, and tactile micro-interactions.
- Adversarial Verification: 51-point adversarial verification suite with monotonic test ratchets.
- AGYOS Polyglot: High-efficiency coding standards across 15+ programming languages and frameworks.

## Structured Skill Catalog

Access the complete JSON catalog at https://agyos.pages.dev/catalog/skills-data.json

## Skill Execution Contract

For every task, discover a relevant skill, read its runbook, apply applicable steps, and verify the result.
Run `gemini/bin/agyos decide "<task>" --json --runbook` to return the selected instructions.
MCP `agyos_decision` accepts `include_runbook: true`.
Matching scores are heuristics, not calibrated probabilities. Runbook delivery does not certify execution.
See https://github.com/krishujeniya/AGYOS/blob/main/docs/SKILL_ROUTING.md for the contract and limits.
"""
    with open(llms_out, "w", encoding="utf-8") as f:
        f.write(llms_content)
    print(f"Saved: {llms_out}")

    nojekyll_out = os.path.join(FRONTEND_DIR, ".nojekyll")
    with open(nojekyll_out, "w", encoding="utf-8") as f:
        f.write("")
    print(f"Saved: {nojekyll_out}")

def build_data():
    """Main execution entrypoint."""
    skills = compile_all_skills()
    print(f"Total compiled unique skills: {len(skills)}")
    write_json_files(skills)
    write_seo_files(skills)

if __name__ == "__main__":
    build_data()
