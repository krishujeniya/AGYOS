#!/usr/bin/env python3
"""
Generate Tiered Skill Manifest for AGYOS:
- Tier 1: Core Software Engineering, Architecture, Security, UI/UX (Emil Kowalski), TDD, Freelance, SEO (~380 skills)
- Tier 2: Domain Extensions, Specialized APIs, Research, Regional Legal, Custom Scrapers (~1,460 skills)
Prevents prompt context swamping while maintaining 100% searchability and JIT availability.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agyos_decision.catalog import read_metadata
SKILLS_DIR = ROOT / ".agents" / "skills"
OUT_MANIFEST = ROOT / ".agents" / "skills-manifest.json"
OUT_TIER1 = ROOT / ".agents" / "tier1-skills.json"

TIER1_CORE_PREFIXES = (
    "agyos-", "council-", "freelancer-", "emil-", "animate", "apple-design",
    "ask-sonner", "break-ui", "find-animation", "improve-animation", "mobile-native",
    "pick-ui", "prototype", "remove-animation", "review-animation", "write-swift",
    "scrollheart", "seo", "geo-", "tdd-", "test-", "debug", "python-", "rust-",
    "golang-", "go-", "typescript-", "react-", "vue-", "angular-", "django-",
    "fastapi-", "postgres-", "docker-", "k8s-", "git-", "security-", "c4-",
    "architecture-", "pentagi-"
)

TIER1_EXACT = {
    "systematic-debugging", "diagnosing-bugs", "code-reviewer", "security-review",
    "verification-loop", "e2e-testing", "benchmark-optimization-loop", "eval-harness",
    "clean-code", "refactoring-cleaner", "api-design", "microservices-patterns",
    "shadcn", "tailwind-patterns", "nextjs-best-practices", "bun-runtime", "uv-package-manager",
    "playwright-skill", "sast-configuration", "threat-modeling-expert"
}

def extract_frontmatter(skill_md: Path):
    """Use the same strict metadata parser as the runtime and docs index."""
    metadata = read_metadata(skill_md)
    return metadata["name"], metadata["description"].strip()

def build_manifest():
    skills = []
    tier1_list = []
    
    for item in sorted(SKILLS_DIR.iterdir()):
        if not item.is_dir():
            continue
        skill_md = item / "SKILL.md"
        if not skill_md.exists():
            continue
            
        _, desc = extract_frontmatter(skill_md)
        is_tier1 = (
            item.name in TIER1_EXACT or
            item.name.startswith(TIER1_CORE_PREFIXES) or
            any(k in desc.lower() for k in ["architecture", "tdd", "security review", "emil kowalski", "5-gate", "testing", "code review"])
        )
        
        entry = {
            "name": item.name,
            "tier": 1 if is_tier1 else 2,
            "description": desc or f"{item.name} skill",
            "path": f".agents/skills/{item.name}"
        }
        skills.append(entry)
        if is_tier1:
            tier1_list.append(entry)
            
    print(f"Total skills scanned: {len(skills)}")
    print(f"Tier 1 (Core Engineering & UI/UX): {len(tier1_list)}")
    print(f"Tier 2 (Domain & Specialized Extensions): {len(skills) - len(tier1_list)}")
    
    manifest_data = {
        "version": "3.1.0",
        "total_skills": len(skills),
        "tier1_count": len(tier1_list),
        "tier2_count": len(skills) - len(tier1_list),
        "skills": skills
    }
    
    OUT_MANIFEST.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    OUT_TIER1.write_text(json.dumps({"tier1_skills": tier1_list}, indent=2), encoding="utf-8")
    print(f"Successfully wrote {OUT_MANIFEST} and {OUT_TIER1}")

if __name__ == "__main__":
    build_manifest()
