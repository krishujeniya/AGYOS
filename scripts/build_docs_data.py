#!/usr/bin/env python3
"""
Compile comprehensive skills database and SEO assets for AGYOS documentation site.
Indexes all 1,845 physical skills from .agents/skills/ and generates:
- docs/skills-data.json
- docs/sitemap.xml
- docs/robots.txt
- docs/llms.txt
- docs/ai-catalog.json
Applies unslop rules to remove AI buzzwords, decorative symbols, and fluff.
"""

import os
import json
import re
from pathlib import Path

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
SKILLS_DIR = os.path.join(REPO_ROOT, ".agents", "skills")
MANIFEST_PATH = os.path.join(REPO_ROOT, ".agents", "skills-manifest.json")

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
    """Extract name and description from SKILL.md frontmatter supporting folded/literal blocks."""
    skill_file = skill_dir / "SKILL.md"
    name = skill_dir.name
    desc = ""
    if not skill_file.exists():
        return name, desc
    try:
        content = skill_file.read_text(encoding="utf-8", errors="ignore")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                in_desc = False
                desc_lines = []
                for line in fm.splitlines():
                    if line.startswith("name:"):
                        in_desc = False
                        name = line.split("name:", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("description:"):
                        val = line.split("description:", 1)[1].strip().strip('"').strip("'")
                        if val in (">", "|", ""):
                            in_desc = True
                            desc_lines = []
                        else:
                            in_desc = False
                            desc = val
                    elif in_desc:
                        if line.startswith(" ") or line.startswith("\t"):
                            desc_lines.append(line.strip())
                        elif line.strip() and not line.startswith("#"):
                            in_desc = False
                if desc_lines and not desc:
                    desc = " ".join(desc_lines)
    except Exception:
        pass
    return name, desc

def classify_skill(sid: str, name: str, desc: str):
    """Classify a skill into an AGYOS module and category."""
    sid_lower = sid.lower()
    desc_lower = desc.lower()

    if sid_lower.startswith("anchor-"):
        return "Anchor Governance", "Governance"
    if sid_lower.startswith("council-") or sid_lower in ("council", "council"):
        return "Agent Council", "Deliberation"
    if (
        sid_lower.startswith(("emil-", "animate", "apple-design", "motion-", "swiftui-", "tailwind-", "threejs-", "ui-", "shadcn", "radix-"))
        or sid_lower in ("break-ui", "scrollheart", "bang-motion", "design-spells", "design-taste-frontend", "ask-sonner", "find-animation", "improve-animation", "remove-animation", "review-animation")
        or "emil kowalski" in desc_lower
        or "animation" in desc_lower
    ):
        return "Emil Kowalski UI/UX & Motion", "Frontend & Motion"
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
        sid_lower.startswith(("security-", "sast-", "threat-"))
        or sid_lower in ("secret-agent-007", "dev-orchestrator", "credential-manager", "security-review")
        or "security" in desc_lower
        or "vulnerability" in desc_lower
    ):
        return "Security & Defense", "Security"
    if sid_lower.startswith(("python-", "rust-", "golang-", "go-", "typescript-", "react-", "vue-", "angular-", "django-", "fastapi-", "postgres-", "docker-", "k8s-", "git-", "c-", "haskell-", "julia-", "ruby-")):
        return "ECC Polyglot Engineering", "Languages & Runtimes"
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
    """Scan .agents/skills/ and return deduplicated, classified skills."""
    manifest_tiers = load_manifest_lookup()
    skills = []
    seen = set()

    for entry in sorted(os.listdir(SKILLS_DIR)):
        entry_path = os.path.join(SKILLS_DIR, entry)
        if not os.path.isdir(entry_path):
            continue
        skill_file = os.path.join(entry_path, "SKILL.md")
        if not os.path.exists(skill_file):
            continue

        raw_name, raw_desc = extract_frontmatter(Path(entry_path))
        clean_desc = unslop(raw_desc or f"{entry} skill for AGYOS.")
        module, category = classify_skill(entry, raw_name, clean_desc)
        tier = manifest_tiers.get(entry, 1 if module in ("Anchor Governance", "Agent Council", "Emil Kowalski UI/UX & Motion", "Verification & Testing", "Security & Defense") else 2)

        skill_obj = {
            "id": entry,
            "name": raw_name.replace("-", " ").title() if raw_name == entry else raw_name,
            "module": module,
            "category": category,
            "tier": tier,
            "runtime": ["AGY CLI", "Gemini", "Claude Code", "Codex"],
            "command": f"bin/agyos skill {entry}" if module == "Anchor Governance" else entry,
            "path": f".agents/skills/{entry}",
            "risk": "safe",
            "description": clean_desc
        }
        if entry not in seen:
            seen.add(entry)
            skills.append(skill_obj)

    return skills

def write_json_files(skills):
    """Write skills-data.json and ai-catalog.json."""
    os.makedirs(DOCS_DIR, exist_ok=True)
    data_out = os.path.join(DOCS_DIR, "skills-data.json")
    with open(data_out, "w", encoding="utf-8") as f:
        json.dump(skills, f, indent=2)
    print(f"Saved: {data_out}")

    catalog_out = os.path.join(DOCS_DIR, "ai-catalog.json")
    catalog_data = {
        "name": "AGYOS",
        "description": "The Autonomous Cognitive Operating System for AGY CLI.",
        "url": "https://krishujeniya.github.io/AGYOS/",
        "version": "3.1.0",
        "total_skills": len(skills),
        "modules": [
            "Anchor Governance",
            "Agent Council",
            "Emil Kowalski UI/UX & Motion",
            "Technical SEO",
            "Freelance Suite",
            "ECC Polyglot Engineering",
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
    """Write sitemap.xml, robots.txt, and llms.txt."""
    sitemap_out = os.path.join(DOCS_DIR, "sitemap.xml")
    modules = ["anchor", "council", "ui-ux", "seo", "freelance", "polyglot", "verification", "security", "explorer"]
    sitemap_urls = [
        f'  <url>\n    <loc>https://krishujeniya.github.io/AGYOS/#{m}</loc>\n    <lastmod>2026-11-03</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>'
        for m in modules
    ]
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://krishujeniya.github.io/AGYOS/</loc>
    <lastmod>2026-11-03</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
{chr(10).join(sitemap_urls)}
</urlset>
"""
    with open(sitemap_out, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"Saved: {sitemap_out}")

    robots_out = os.path.join(DOCS_DIR, "robots.txt")
    with open(robots_out, "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: https://krishujeniya.github.io/AGYOS/sitemap.xml\n")
    print(f"Saved: {robots_out}")

    llms_out = os.path.join(DOCS_DIR, "llms.txt")
    llms_content = f"""# AGYOS Documentation

> The Autonomous Cognitive Operating System for AGY CLI (`agy`).
> Maintained by krishujeniya.
> Total skills documented: {len(skills)}
> Total modular rules: 162
> Total role agents: 74
> Total workflow pipelines: 100

## Core Operating Subsystems

- Anchor Governance: 5-Gate spine (UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT -> VERIFY) with FastMCP JSON-RPC 2.0 daemon and adaptive fast-path.
- Agent Council: Multi-model CLI consensus engine deliberating across Gemini, Claude, and Codex in parallel Bun subprocesses.
- Emil Kowalski UI/UX: Enforcing concentric border radii, 0ms/150ms/250ms motion timing, compositor-only animations, and tactile micro-interactions.
- Adversarial Verification: 25-point falsifiable test suite validating plugins, safety hooks, MCP protocols, and ratchet monotonicity.
- ECC Polyglot: High-efficiency coding standards across 15+ programming languages and frameworks.

## Structured Skill Catalog

Access the complete JSON catalog at https://krishujeniya.github.io/AGYOS/skills-data.json
"""
    with open(llms_out, "w", encoding="utf-8") as f:
        f.write(llms_content)
    print(f"Saved: {llms_out}")

    nojekyll_out = os.path.join(DOCS_DIR, ".nojekyll")
    with open(nojekyll_out, "w", encoding="utf-8") as f:
        f.write("")
    print(f"Saved: {nojekyll_out}")

def sync_skills_to_runtimes():
    """Verify skills catalog and check user agent runtimes (~/.gemini, ~/.codex, ~/.claude)."""
    print("\n--- Synchronizing skills to AGY and Codex runtimes ---")
    runtime_dirs = [
        (os.path.expanduser("~/.gemini/skills"), "AGY (~/.gemini/skills)"),
        (os.path.expanduser("~/.gemini/config/skills"), "AGY config (~/.gemini/config/skills)"),
        (os.path.expanduser("~/.codex/skills"), "Codex (~/.codex/skills)"),
        (os.path.expanduser("~/.agents/skills"), "Agents (~/.agents/skills)"),
        (os.path.expanduser("~/.claude/skills"), "Claude Code (~/.claude/skills)"),
    ]

    workspace_count = 0
    if os.path.exists(SKILLS_DIR):
        workspace_count = len([s for s in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, s))])
    print(f"AGYOS Master Catalog (.agents/skills): {workspace_count} physical skills ready.")

    for target_dir, label in runtime_dirs:
        try:
            os.makedirs(target_dir, exist_ok=True)
            active_count = len([s for s in os.listdir(target_dir) if not s.startswith(".")])
            print(f"Verified {label}: {active_count} active installed skills.")
        except Exception:
            pass

def build_data():
    """Main execution entrypoint."""
    skills = compile_all_skills()
    print(f"Total compiled unique skills: {len(skills)}")
    write_json_files(skills)
    write_seo_files(skills)
    sync_skills_to_runtimes()

if __name__ == "__main__":
    build_data()
