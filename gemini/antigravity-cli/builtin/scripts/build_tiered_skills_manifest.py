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
from agyos_decision.toon_config import dump_toon_manifest
SKILLS_DIR = ROOT / "skills"
OUT_MANIFEST = ROOT.parent / "skills-manifest.json"
OUT_MANIFEST_TOON = ROOT / "skills-manifest.toon"
OUT_TIER1 = ROOT / "tier1-skills.json"
OUT_TIER1_TOON = ROOT / "tier1-skills.toon"

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
    "playwright-skill", "sast-configuration", "threat-modeling-expert", "cinematic-web-design",
    "faceless-shorts-engine", "modern-web-guidance", "chrome-extensions", "turn-ideas-into-reality",
    "3b1b-manim", "vertical-video-psychology", "video-production-orchestrator",
    "penetration-testing-with-strix", "managed-pentesting-with-strix", "ci-security-scanning-with-strix",
    "fix-security-vulnerabilities-with-strix", "application-security-testing", "web-app-penetration-testing",
    "owasp-top-10-testing", "find-security-vulnerabilities-in-code", "strix-api-security-testing",
    "gemini-notebook"
}

def extract_frontmatter(skill_md: Path):
    """Use the same strict metadata parser as the runtime and docs index."""
    metadata = read_metadata(skill_md)
    return metadata["name"], metadata["description"].strip()

def build_manifest():
    skills = []
    tier1_count = 0

    for role_dir in sorted(SKILLS_DIR.iterdir()):
        if not role_dir.is_dir() or role_dir.name.startswith("."):
            continue
        for item in sorted(role_dir.iterdir()):
            if not item.is_dir() or item.name.startswith("."):
                continue
            skill_file = item / "SKILL.toon" if (item / "SKILL.toon").is_file() else item / "SKILL.md"
            if not skill_file.is_file():
                continue

            _, desc = extract_frontmatter(skill_file)
            is_tier1 = (
                item.name in TIER1_EXACT or
                item.name.startswith(TIER1_CORE_PREFIXES) or
                any(k in desc.lower() for k in ["architecture", "tdd", "security review", "emil kowalski", "5-gate", "testing", "code review"])
            )
            if is_tier1:
                tier1_count += 1

            skills.append({
                "name": item.name,
                "role": role_dir.name,
                "tier": 1 if is_tier1 else 2,
                "description": desc or f"{item.name} skill",
                "path": f"skills/{role_dir.name}/{item.name}",
            })

    print(f"Total skills scanned: {len(skills)}")
    print(f"Tier 1 (Core Engineering & UI/UX): {tier1_count}")
    print(f"Tier 2 (Domain & Specialized Extensions): {len(skills) - tier1_count}")

    manifest_data = {
        "version": "3.1.0",
        "total_skills": len(skills),
        "tier1_count": tier1_count,
        "tier2_count": len(skills) - tier1_count,
        "skills": skills,
    }

    OUT_MANIFEST.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    print(f"Successfully wrote {OUT_MANIFEST}")

if __name__ == "__main__":
    build_manifest()
