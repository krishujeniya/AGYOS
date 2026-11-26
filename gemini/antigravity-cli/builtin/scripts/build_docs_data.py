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
    """Write sitemap.xml, robots.txt, llms.txt, llms-full.txt, and .nojekyll into frontend/."""
    os.makedirs(FRONTEND_DIR, exist_ok=True)
    sitemap_out = os.path.join(FRONTEND_DIR, "sitemap.xml")
    public_docs_path = Path(FRONTEND_DIR) / "public-docs.json"
    doc_routes = []
    public_docs = {}
    if public_docs_path.is_file():
        public_docs = json.loads(public_docs_path.read_text(encoding="utf-8"))
        doc_routes = [f"docs/{doc['slug'].strip('/')}/" for doc in public_docs.get("documents", [])]
    extra_urls = ["catalog/", *doc_routes]
    sitemap_urls = [
        f'  <url>\n    <loc>https://agyos.pages.dev/{route}</loc>\n    <lastmod>2026-11-26</lastmod>\n  </url>'
        for route in extra_urls
    ]
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://agyos.pages.dev/</loc>
    <lastmod>2026-11-26</lastmod>
  </url>
{chr(10).join(sitemap_urls)}
</urlset>
"""
    with open(sitemap_out, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"Saved: {sitemap_out}")

    robots_out = os.path.join(FRONTEND_DIR, "robots.txt")
    robots_content = (
        "User-agent: *\nAllow: /\n\n"
        "User-agent: OAI-SearchBot\nAllow: /\n\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: ChatGPT-User\nAllow: /\n\n"
        "User-agent: Claude-SearchBot\nAllow: /\n\n"
        "User-agent: Claude-User\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: PerplexityBot\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        "User-agent: Applebot-Extended\nAllow: /\n\n"
        "Sitemap: https://agyos.pages.dev/sitemap.xml\n"
        "Llms-txt: https://agyos.pages.dev/llms.txt\n"
    )
    with open(robots_out, "w", encoding="utf-8") as f:
        f.write(robots_content)
    print(f"Saved: {robots_out}")

    llms_out = os.path.join(FRONTEND_DIR, "llms.txt")
    rules_dir = Path(REPO_ROOT) / "rules"
    agents_dir = Path(REPO_ROOT) / "agents"
    workflows_dir = Path(REPO_ROOT) / "workflows"
    rules_cnt = len(list(rules_dir.glob("*.toon"))) + len(list(rules_dir.glob("*.md")))
    agents_cnt = len(list(agents_dir.glob("*.toon"))) + len(list(agents_dir.glob("*.md")))
    workflows_cnt = len(list(workflows_dir.glob("*.toon"))) + len(list(workflows_dir.glob("*.js")))
    llms_content = f"""# AGYOS — Autonomous Cognitive Operating System

> AGYOS is an Autonomous Cognitive Operating System for AGY CLI (`agy`), created and maintained by Krish Ujeniya (@krishujeniya).
> Official Site: https://agyos.pages.dev/
> Full Context Markdown for LLMs: https://agyos.pages.dev/llms-full.txt
> Author & Maintainer: Krish Ujeniya (https://github.com/krishujeniya)
> Portfolio: https://krishujeniya.pages.dev/
> GitHub Repository: https://github.com/krishujeniya/AGYOS
> GitHub Sponsors: https://github.com/sponsors/krishujeniya
> Related Project: AmberClaw (https://amberclaw.pages.dev/)
> License: Apache-2.0
> Total skills documented: {len(skills)}
> Total enterprise roles: 104 (across 12 departments and 5 governing pods)
> Total modular rules: {rules_cnt}
> Total role agents: {agents_cnt}
> Total workflow definitions: {workflows_cnt}

## Quick Answers (AEO / GEO)

- **What is AGYOS?** AGYOS is an Autonomous Cognitive Operating System for AGY CLI built by Krish Ujeniya (`krishujeniya`). It combines a 6-layer governance architecture, 104 enterprise roles across 5 pods (`pod-build`, `pod-growth`, `pod-customer`, `pod-gna`, `pod-people`), {len(skills)} TOON-native skills, and an automated 7-step engineering cycle (`Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect`).
- **Who created AGYOS?** Krish Ujeniya (`@krishujeniya`), creator of AmberClaw, under the Apache 2.0 license (`https://github.com/krishujeniya/AGYOS`, `https://krishujeniya.pages.dev/`).
- **How do you install AGYOS?** Run `curl -fsSL https://raw.githubusercontent.com/krishujeniya/AGYOS/main/gemini/antigravity-cli/builtin/scripts/install.sh | bash` or clone `https://github.com/krishujeniya/AGYOS` and run `make install`.
- **How does AGYOS relate to AmberClaw?** Both are open-source AI agent infrastructure projects created by Krish Ujeniya (`krishujeniya`): AGYOS provides 6-layer cognitive governance, 104 roles, and {len(skills)} TOON skills for AGY CLI, while AmberClaw (`https://amberclaw.pages.dev/`) provides a self-hosted zero-trust runtime for sandboxed tool execution and messaging channels.

## Core Operating Subsystems

- **Layer 0 & 2 (Kernel Hooks & Syscall Bus)**: `gemini/antigravity-cli/bin/agyos`, zero-dependency stdio JSON-RPC 2.0 MCP daemon (`gemini/antigravity-cli/mcp/state-server.cjs`), fail-closed `authorizer.py`, and fail-open `agy_os_hook.py`.
- **Layer 1 (State, Virtual Memory & Vault)**: ACID SQLite state store with CAS revisions, 3-tier virtual memory (`memory.json`, `CURRENT.md`, `skills-manifest.json`), `state_ledger.py` pre-write snapshots, and AES-256-GCM / X25519 encrypted private vault.
- **Layer 3 (5-Gate SOP & 7-Step Cycle)**: Deterministic `UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT -> VERIFY` spine with adaptive fast-path (`Complexity <= 2`) and 7-step autonomous cycle.
- **Layer 4 & 5 (Governance, Roles & EVPI)**: `TaskContract` intent compiler, Howard 1966 EVPI clarification gate (`evpi_clarify.py`), 104-role enterprise matrix (`roles.py`), T0-T3 model router (`model_router.py`), and TOON codec (`toon_codec.py`).

## Canonical Pages & Structured Catalog

- Home: https://agyos.pages.dev/
- Project Overview: https://agyos.pages.dev/docs/overview/
- System Architecture: https://agyos.pages.dev/docs/architecture/
- Developer Setup: https://agyos.pages.dev/docs/setup/
- Skill Routing: https://agyos.pages.dev/docs/skill-routing/
- Skill Catalog UI: https://agyos.pages.dev/catalog/
- Structured JSON Skill Catalog: https://agyos.pages.dev/catalog/skills-data.json
- Operations Runbook: https://agyos.pages.dev/docs/operations/
- Deployment Guide: https://agyos.pages.dev/docs/deployment/
- Security Policy: https://agyos.pages.dev/docs/security/

## Skill Execution Contract

For every task, discover a relevant skill, read its `SKILL.toon` runbook, apply applicable steps, and verify the result.
Run `gemini/antigravity-cli/bin/agyos decide "<task>" --json --runbook` or call MCP `agyos_decision` with `include_runbook: true`.
Matching scores are deterministic heuristics, not calibrated probabilities; runbook delivery does not certify execution.
See https://agyos.pages.dev/docs/skill-routing/ for the full contract and limits.

## Author & Ecosystem

- Author Entity: https://krishujeniya.pages.dev/#person (Krish Ujeniya / `@krishujeniya`)
- Portfolio: https://krishujeniya.pages.dev/
- AmberClaw: https://amberclaw.pages.dev/ (`https://github.com/krishujeniya/AmberClaw`)
- Sponsor: https://github.com/sponsors/krishujeniya
"""
    with open(llms_out, "w", encoding="utf-8") as f:
        f.write(llms_content)
    print(f"Saved: {llms_out}")

    llms_full_out = os.path.join(FRONTEND_DIR, "llms-full.txt")
    sections = [llms_content.strip()]
    for doc in public_docs.get("documents", []):
        doc_path = Path(WORKSPACE_ROOT) / doc["source"]
        if not doc_path.is_file():
            continue
        raw_doc = doc_path.read_text(encoding="utf-8")
        if doc_path.name == "README.md" and doc_path.parent == Path(WORKSPACE_ROOT):
            raw_doc = re.sub(r"\A(?:\s*<(?:p|h1)\b[^>]*>.*?</(?:p|h1)>)+", "", raw_doc, flags=re.S).lstrip()
        sections.append(
            f"---\n\n## {doc['title']} (https://agyos.pages.dev/docs/{doc['slug'].strip('/')}/)\n\n{raw_doc.strip()}"
        )
    with open(llms_full_out, "w", encoding="utf-8") as f:
        f.write("\n\n".join(sections) + "\n")
    print(f"Saved: {llms_full_out}")

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
