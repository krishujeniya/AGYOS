#!/usr/bin/env python3
"""
Package AGYOS Plugins into .agents/plugins/
Adheres strictly to the Antigravity CLI Plugin specification with logos and clean scoped rules.
"""

import os
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / ".agents" / "plugins"
LOGO_SRC = REPO_ROOT / "assets" / "agyos-logo.svg"

PLUGINS_SPEC = [
    {
        "id": "agyos-anchor",
        "name": "Anchor Governance & Verification Spine",
        "description": "Deterministic 5-gate workflow governance, scope boundary enforcement, test ratchet, and FastMCP server.",
        "skills_src": [
            (".agents/skills/anchor-orchestrator", "anchor-orchestrator"),
            (".agents/skills/anchor-scout", "anchor-scout"),
            (".agents/skills/anchor-scope", "anchor-scope"),
            (".agents/skills/anchor-verify", "anchor-verify"),
            (".agents/skills/anchor-draft-commit", "anchor-draft-commit"),
            (".agents/skills/anchor-graph", "anchor-graph"),
            (".agents/skills/anchor-preflight", "anchor-preflight"),
        ],
        "mcp_config": {
            "mcpServers": {
                "anchor": {
                    "command": "node",
                    "args": [str(REPO_ROOT / "mcp/agyos-state-server.cjs")]
                }
            }
        },
        "rule": """# Anchor Governance Spine
- Enforce the 5-Gate Workflow: UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT -> VERIFY.
- Never write code on speculation; inspect manifests and existing files first.
- Strictly adhere to declared scope boundaries."""
    },
    {
        "id": "agyos-council",
        "name": "Agent Council Multi-Model Deliberation",
        "description": "Multi-agent CLI deliberation panel running Gemini, Claude, and Codex in parallel for architectural consensus.",
        "skills_src": [
            (".agents/skills/agent-council-nudge", "agent-council-nudge"),
            (".agents/skills/council-list", "council-list"),
            (".agents/skills/council-nudge", "council-nudge"),
            (".agents/skills/council-outcome", "council-outcome"),
            (".agents/skills/council-replay", "council-replay"),
            (".agents/skills/council-revisit", "council-revisit"),
        ],
        "rule": """# Multi-Model Deliberation Standard
- When evaluating architectural decisions, collect independent opinions and synthesize consensus.
- Reconcile divergent recommendations transparently based on trade-offs."""
    },
    {
        "id": "agyos-aegis",
        "name": "Aegis SDLC & 8 Expert Role Agents",
        "description": "Complete software development lifecycle automation with 8 expert role agents and 11 quality guardrails.",
        "skills_src": [
            (".agents/skills/aegis", "aegis"),
            (".agents/skills/architect", "architect"),
            (".agents/skills/code-architect", "code-architect"),
            (".agents/skills/code-explorer", "code-explorer"),
            (".agents/skills/planner", "planner"),
        ],
        "rule": """# Aegis SDLC Standards
- Follow contract-first API design and maintain specification documents before mutating code.
- Enforce clean separation of concerns and layered architecture."""
    },
    {
        "id": "agyos-ecc-polyglot",
        "name": "ECC Polyglot Language & Framework Engineering",
        "description": "Enterprise coding capabilities for Rust, Go, Python, TypeScript, React, Vue, Django, and modern backend stacks.",
        "skills_src": [
            (".agents/skills/rust-patterns", "rust-patterns"),
            (".agents/skills/golang-patterns", "golang-patterns"),
            (".agents/skills/python-patterns", "python-patterns"),
            (".agents/skills/typescript-patterns", "typescript-patterns"),
            (".agents/skills/frontend-patterns", "frontend-patterns"),
            (".agents/skills/backend-patterns", "backend-patterns"),
            (".agents/skills/django-patterns", "django-patterns"),
            (".agents/skills/postgres-patterns", "postgres-patterns"),
        ],
        "rule": """# Polyglot Engineering Standards
- Keep functions under 50 lines with a single responsibility.
- Keep source files under the 800-line maintainability ceiling.
- Enforce immutability: return new data structures; never mutate in-place."""
    },
    {
        "id": "agyos-verification",
        "name": "Adversarial Machine Verification & Testing",
        "description": "Test-driven development (TDD), Playwright E2E runners, property testing, and test coverage ratchets.",
        "skills_src": [
            (".agents/skills/verification-loop", "verification-loop"),
            (".agents/skills/e2e-testing", "e2e-testing"),
            (".agents/skills/python-testing", "python-testing"),
            (".agents/skills/rust-testing", "rust-testing"),
            (".agents/skills/diagnosing-bugs", "diagnosing-bugs"),
        ],
        "rule": """# Verification & Testing Invariants
- Minimum test coverage: 80% with Arrange-Act-Assert structure.
- Test Ratchet: Total assertions must never decrease without explicit written rationale.
- Always require machine evidence: clean compiler, linter, and test exit codes."""
    },
    {
        "id": "agyos-security",
        "name": "Security Hardening & Secret Defense",
        "description": "OWASP Top 10 auditing, secret detection, open-source sanitization, and dependency safety reviews.",
        "skills_src": [
            (".agents/skills/security-review", "security-review"),
            (".agents/skills/opensource-sanitizer", "opensource-sanitizer"),
            (".agents/skills/opensource-forker", "opensource-forker"),
            (".agents/skills/opensource-packager", "opensource-packager"),
        ],
        "rule": """# Security & Defense Invariants
- Never store API keys, tokens, or private credentials in repository files.
- Validate and sanitize all external inputs at the system boundary."""
    },
    {
        "id": "agyos-seo",
        "name": "Technical SEO & Generative Engine Optimization",
        "description": "25 SEO modules covering technical audits, Schema JSON-LD, sitemaps, E-E-A-T, and AI search answer citations.",
        "skills_src": [
            (".agents/skills/seo", "seo"),
        ],
        "rule": """# Technical SEO Standards
- Ensure valid semantic HTML, OpenGraph tags, and Schema.org JSON-LD markup.
- Verify indexability, crawlability, and accurate sitemap declarations."""
    },
    {
        "id": "agyos-business-creative",
        "name": "Freelance Operations, Emil Kowalski UI/UX & Motion",
        "description": "Freelance lifecycle, Emil Kowalski design engineering, Framer Motion, and GSAP ScrollTrigger cinematic experiences.",
        "skills_src": [
            (".agents/skills/freelancer-client-acquisition", "freelancer-client-acquisition"),
            (".agents/skills/freelancer-sales-closing", "freelancer-sales-closing"),
            (".agents/skills/freelancer-project-delivery", "freelancer-project-delivery"),
            (".agents/skills/freelancer-operations", "freelancer-operations"),
            (".agents/skills/freelancer-identity", "freelancer-identity"),
            (".agents/skills/scrollheart", "scrollheart"),
            (".agents/skills/emil-design-eng", "emil-design-eng"),
            (".agents/skills/animate", "animate"),
            (".agents/skills/review-animations", "review-animations"),
            (".agents/skills/animation-performance", "animation-performance"),
            (".agents/skills/apple-design", "apple-design"),
        ],
        "rule": """# Creative & UI/UX Design Engineering Standards
- Enforce Emil Kowalski's Design Engineering standards for all UI/UX, SaaS apps, and website generation.
- Concentric Border Radii: Nested child radii must satisfy R_inner = R_outer - padding.
- Animation Timing: Micro-interactions (150-200ms); modals (250-350ms); never animate keyboard actions.
- Compositor-Only: Animate transform and opacity only. No layout thrashing on height/width.
- Tactile Micro-Interactions: Active scale feedback (scale 0.98) on interactive controls.
- Use structured Before/After/Why markdown tables for UI code reviews.
- Build clean, accessible, responsive CSS, Tailwind, Framer Motion, and GSAP animations."""
    }
]

def build_plugins():
    PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
    
    for p in PLUGINS_SPEC:
        p_dir = PLUGINS_DIR / p["id"]
        p_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Assets and logo
        assets_dir = p_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        if LOGO_SRC.exists():
            shutil.copyfile(LOGO_SRC, assets_dir / "logo.svg")
        
        # 2. Manifest plugin.json
        manifest = {
            "name": p["id"],
            "description": p["description"],
            "version": "3.1.0",
            "author": "Krish Ujeniya",
            "logo": "assets/logo.svg",
            "repository": "https://github.com/krishujeniya/SKILL"
        }
        (p_dir / "plugin.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        
        # 3. Rules
        rules_dir = p_dir / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        (rules_dir / "AGENTS.md").write_text(p["rule"], encoding="utf-8")
        
        # 4. Optional mcp_config.json
        if "mcp_config" in p:
            (p_dir / "mcp_config.json").write_text(json.dumps(p["mcp_config"], indent=2), encoding="utf-8")
            
        # 5. Skills folder with symlinked skills
        skills_dir = p_dir / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)
        
        for rel_src, name in p["skills_src"]:
            src_path = REPO_ROOT / rel_src
            if src_path.exists():
                target_link = skills_dir / name
                if target_link.is_symlink() or target_link.exists():
                    target_link.unlink()
                target_link.symlink_to(src_path.resolve())
                
    print(f"Successfully packaged {len(PLUGINS_SPEC)} AGYOS plugins with logos in {PLUGINS_DIR}")

if __name__ == "__main__":
    build_plugins()
