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
LOGO_SRC = REPO_ROOT / "assets" / "logo.svg"

PLUGINS_SPEC = [
    {
        "id": "agyos-governance",
        "name": "AGYOS Governance & Verification Spine",
        "description": "Deterministic 5-gate workflow governance, scope boundary enforcement, test ratchet, and FastMCP server.",
        "mcp_config": {
            "mcpServers": {
                "agyos": {
                    "command": "node",
                    "args": [str(REPO_ROOT / "mcp/agyos-state-server.cjs")]
                }
            }
        },
        "rule": """# AGYOS Governance Spine
- Enforce the 5-Gate Workflow: UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT -> VERIFY.
- Never write code on speculation; inspect manifests and existing files first.
- Strictly adhere to declared scope boundaries."""
    },
    {
        "id": "agyos-council",
        "name": "AGYOS Multi-Model Deliberation Council",
        "description": "Multi-agent CLI deliberation panel running isolated subprocesses for architectural consensus.",
        "rule": """# Multi-Model Deliberation Standard
- When evaluating architectural decisions, collect independent opinions and synthesize consensus.
- Reconcile divergent recommendations transparently based on trade-offs."""
    },
    {
        "id": "agyos-core",
        "name": "AGYOS Core SDLC Standards & Role Agents",
        "description": "Complete software development lifecycle automation with specialized expert role agents and quality guardrails.",
        "rule": """# AGYOS SDLC Standards
- Follow contract-first API design and maintain specification documents before mutating code.
- Enforce clean separation of concerns and layered architecture."""
    },
    {
        "id": "agyos-polyglot",
        "name": "AGYOS Polyglot Language & Framework Engineering",
        "description": "Enterprise coding capabilities for Rust, Go, Python, TypeScript, React, Vue, Django, and modern backend stacks.",
        "rule": """# Polyglot Engineering Standards
- Keep functions under 50 lines with a single responsibility.
- Keep source files under the 800-line maintainability ceiling.
- Enforce immutability: return new data structures; never mutate in-place."""
    },
    {
        "id": "agyos-verification",
        "name": "AGYOS Machine Verification & Testing",
        "description": "Test-driven development (TDD), Playwright E2E runners, property testing, and test coverage ratchets.",
        "rule": """# Verification & Testing Invariants
- Minimum test coverage: 80% with Arrange-Act-Assert structure.
- Test Ratchet: Total assertions must never decrease without explicit written rationale.
- Always require machine evidence: clean compiler, linter, and test exit codes."""
    },
    {
        "id": "agyos-security",
        "name": "AGYOS Security & Defense Guardrails",
        "description": "OWASP Top 10 auditing, secret detection, open-source sanitization, and dependency safety reviews.",
        "rule": """# Security & Defense Invariants
- Never store API keys, tokens, or private credentials in repository files.
- Validate and sanitize all external inputs at the system boundary."""
    },
    {
        "id": "agyos-seo",
        "name": "AGYOS Technical SEO & Generative Optimization",
        "description": "Technical SEO audits, Schema JSON-LD, sitemaps, E-E-A-T, and AI search answer citations.",
        "rule": """# Technical SEO Standards
- Ensure valid semantic HTML, OpenGraph tags, and Schema.org JSON-LD markup.
- Verify indexability, crawlability, and accurate sitemap declarations."""
    },
    {
        "id": "agyos-business-creative",
        "name": "AGYOS UI/UX Design Engineering & Motion",
        "description": "Design engineering, micro-interactions, animation standards, and responsive accessible components.",
        "rule": """# Creative & UI/UX Design Engineering Standards
- Enforce Design Engineering standards for all UI/UX, SaaS apps, and website generation.
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
            "repository": "https://github.com/krishujeniya/AGYOS"
        }
        (p_dir / "plugin.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        
        # 3. Rules
        rules_dir = p_dir / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        (rules_dir / "AGENTS.md").write_text(p["rule"], encoding="utf-8")
        
        # 4. Optional mcp_config.json
        if "mcp_config" in p:
            (p_dir / "mcp_config.json").write_text(json.dumps(p["mcp_config"], indent=2), encoding="utf-8")
                
    print(f"Successfully packaged {len(PLUGINS_SPEC)} pure AGYOS plugins with logos in {PLUGINS_DIR}")

if __name__ == "__main__":
    build_plugins()
