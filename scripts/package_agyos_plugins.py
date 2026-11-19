#!/usr/bin/env python3
"""
Package AGYOS Plugins into .agents/plugins/
Adheres strictly to the Antigravity CLI Plugin specification with logos and clean scoped rules.
"""

import subprocess
import json
import shutil
from pathlib import Path
from agyos_decision.toon_config import dump_toon_config

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
    },
    {
        "id": "agyos-council",
        "name": "AGYOS Multi-Model Deliberation Council",
        "description": "Multi-agent CLI deliberation panel running isolated subprocesses for architectural consensus.",
    },
    {
        "id": "agyos-core",
        "name": "AGYOS Core SDLC Standards & Role Agents",
        "description": "Complete software development lifecycle automation with specialized expert role agents and quality guardrails.",
    },
    {
        "id": "agyos-polyglot",
        "name": "AGYOS Polyglot Language & Framework Engineering",
        "description": "Enterprise coding capabilities for Rust, Go, Python, TypeScript, React, Vue, Django, and modern backend stacks.",
    },
    {
        "id": "agyos-verification",
        "name": "AGYOS Machine Verification & Testing",
        "description": "Test-driven development (TDD), Playwright E2E runners, property testing, and test coverage ratchets.",
    },
    {
        "id": "agyos-security",
        "name": "AGYOS Security & Defense Guardrails",
        "description": "OWASP Top 10 auditing, secret detection, open-source sanitization, and dependency safety reviews.",
    },
    {
        "id": "agyos-seo",
        "name": "AGYOS Technical SEO & Generative Optimization",
        "description": "Technical SEO audits, Schema JSON-LD, sitemaps, E-E-A-T, and AI search answer citations.",
    },
    {
        "id": "agyos-business-creative",
        "name": "AGYOS UI/UX Design Engineering & Motion",
        "description": "Design engineering, micro-interactions, animation standards, and responsive accessible components.",
    }
]

def build_plugins():
    subprocess.run(["node", "scripts/materialize-documents.mjs"], cwd=REPO_ROOT, check=True)
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
        dump_toon_config(manifest, p_dir / "plugin.toon")
        
        # 3. Optional mcp_config.json / mcp_config.toon
        if "mcp_config" in p:
            (p_dir / "mcp_config.json").write_text(json.dumps(p["mcp_config"], indent=2), encoding="utf-8")
            dump_toon_config(p["mcp_config"], p_dir / "mcp_config.toon")
                
    print(f"Successfully packaged {len(PLUGINS_SPEC)} pure AGYOS plugins with logos in {PLUGINS_DIR}")

if __name__ == "__main__":
    build_plugins()
