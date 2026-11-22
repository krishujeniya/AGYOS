#!/usr/bin/env python3
"""
Package AGYOS Plugins into .agents/plugins/
Adheres strictly to the Antigravity CLI Plugin specification with logos and clean scoped rules.
"""

import subprocess
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agyos_decision.toon_config import dump_toon_config

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
    },
    {
        "id": "agyos-mcp-billing",
        "name": "AGYOS Financial & Payment Operations",
        "description": "Stripe read-only MCP integration with Least Privilege scopes for financial auditability.",
        "mcp_config": {
            "mcpServers": {
                "stripe": {
                    "type": "http",
                    "url": "https://mcp.stripe.com",
                    "env_ref": "AGY_STRIPE_MCP_KEY",
                    "tool_scope": [
                        "payouts:read",
                        "balance_transactions:read",
                        "disputes:read"
                    ],
                    "write_scope": "none",
                    "enabled": True
                }
            }
        },
    },
    {
        "id": "agyos-mcp-github",
        "name": "AGYOS GitHub Remote Collaboration",
        "description": "Scoped GitHub Copilot MCP client for PRs, issues, and security alerts.",
        "mcp_config": {
            "mcpServers": {
                "github-remote": {
                    "type": "http",
                    "url": "https://api.githubcopilot.com/mcp/",
                    "env_ref": "AGY_GITHUB_MCP_PAT",
                    "tool_scope": [
                        "pull_requests:read",
                        "issues:write",
                        "code_scanning:read",
                        "labels:write"
                    ],
                    "enabled": True
                }
            }
        },
    },
    {
        "id": "agyos-mcp-work",
        "name": "AGYOS Enterprise Work Tracking",
        "description": "Atlassian Jira MCP connector with read-only board and issue scoping.",
        "mcp_config": {
            "mcpServers": {
                "jira-remote": {
                    "type": "http",
                    "url": "https://api.atlassian.com/mcp/",
                    "env_ref": "AGY_JIRA_MCP_TOKEN",
                    "tool_scope": [
                        "boards:read",
                        "sprints:read",
                        "issues:read"
                    ],
                    "enabled": True
                }
            }
        },
    },
    {
        "id": "agyos-mcp-workspace",
        "name": "AGYOS Collaborative Artifact Publishing",
        "description": "Google Workspace MCP integration with folder isolation for AGYOS project deliverables.",
        "mcp_config": {
            "mcpServers": {
                "google-workspace": {
                    "type": "http",
                    "url": "https://googleworkspace.googleapis.com/mcp/",
                    "env_ref": "AGY_WORKSPACE_OAUTH_REF",
                    "tool_scope": [
                        "drive:read",
                        "drive:write",
                        "docs:export"
                    ],
                    "folder_scope": "AGYOS-artifacts",
                    "access_log": True,
                    "enabled": True
                }
            }
        },
    },
    {
        "id": "agyos-policy-guard",
        "name": "AGYOS Active Governance & Policy Guard",
        "description": "PreToolUse, PostToolUse, PreInvocation, and Stop lifecycle hooks enforcing FAANG invariants.",
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
        logo_dst = assets_dir / "logo.svg"
        if logo_dst.is_symlink():
            logo_dst.unlink()
        if LOGO_SRC.exists():
            shutil.copyfile(LOGO_SRC, logo_dst)
        
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
