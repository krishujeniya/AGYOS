#!/usr/bin/env python3
"""AGY On-Demand MCP and Plugin Manager.

Maintains all MCP servers and plugins disabled at startup to preserve memory
and reduce startup latency. Activates servers and plugins dynamically on-demand
when they are called or requested.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

USER_HOME = Path.home()
GEMINI_DIR = USER_HOME / ".gemini"
GLOBAL_MCP_CONFIG = GEMINI_DIR / "config" / "mcp_config.json"
GLOBAL_CONFIG = GEMINI_DIR / "config" / "config.json"
GLOBAL_SETTINGS = GEMINI_DIR / "settings.json"
PLUGINS_DIR = GEMINI_DIR / "config" / "plugins"

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_MCP_CONFIG = WORKSPACE_ROOT / ".mcp.json"

PLUGIN_SKILL_MAP: Dict[str, List[str]] = {
    "agyos-aegis": ["aegis"],
    "agyos-anchor": [
        "anchor",
        "anchor-draft-commit",
        "anchor-graph",
        "anchor-orchestrator",
        "anchor-preflight",
        "anchor-scope",
        "anchor-scout",
        "anchor-verify",
    ],
    "agyos-business-creative": [
        "animate",
        "animation-performance",
        "apple-design",
        "emil-design-eng",
        "freelancer-client-acquisition",
        "freelancer-identity",
        "freelancer-operations",
        "freelancer-project-delivery",
        "freelancer-sales-closing",
        "review-animations",
        "scrollheart",
    ],
    "agyos-council": [
        "agent-council-nudge",
        "council",
        "council-list",
        "council-nudge",
        "council-outcome",
        "council-replay",
        "council-revisit",
    ],
    "agyos-polyglot": [
        "backend-patterns",
        "django-patterns",
        "frontend-patterns",
        "golang-patterns",
        "postgres-patterns",
        "python-patterns",
        "rust-patterns",
        "typescript-patterns",
    ],
    "agyos-security": ["security-review"],
    "agyos-seo": ["seo"],
    "agyos-verification": [
        "diagnosing-bugs",
        "e2e-testing",
        "python-testing",
        "rust-testing",
        "verification-loop",
    ],
    "modern-web-guidance": ["chrome-extensions", "modern-web-guidance"],
}

MCP_TOOL_PREFIXES: Dict[str, str] = {
    "deepnote_": "deepnote-mcp",
    "flow_": "google-flow",
    "op_": "1password-mcp",
    "travis_": "travis-mcp",
    "obscura_": "obscura",
    "agyos_": "anchor",
    "notebooklm_": "gemini-notebook",
    "gemini_notebook_": "gemini-notebook",
    "nlm_": "gemini-notebook",
}


def read_json(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read().strip()
            return json.loads(content) if content else {}
    except (json.JSONDecodeError, OSError):
        return {}


def write_json(path: Path, data: Dict[str, Any]) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(f".tmp.{os.getpid()}")
        with open(tmp_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
        tmp_path.replace(path)
        return True
    except OSError as err:
        sys.stderr.write(f"[agy-ondemand] Failed to write {path}: {err}\n")
        return False


def get_installed_plugins() -> List[str]:
    plugins = []
    if PLUGINS_DIR.is_dir():
        for entry in os.scandir(PLUGINS_DIR):
            if entry.is_dir() and not entry.name.startswith("."):
                plugins.append(entry.name)
    workspace_plugins = WORKSPACE_ROOT / ".agents" / "plugins"
    if workspace_plugins.is_dir():
        for entry in os.scandir(workspace_plugins):
            if entry.is_dir() and not entry.name.startswith(".") and entry.name not in plugins:
                plugins.append(entry.name)
    return sorted(plugins)


def disable_all_mcps() -> int:
    count = 0
    if GLOBAL_MCP_CONFIG.is_file():
        cfg = read_json(GLOBAL_MCP_CONFIG)
        servers = cfg.get("mcpServers", {})
        for name, spec in servers.items():
            if isinstance(spec, dict) and not spec.get("disabled", False):
                spec["disabled"] = True
                count += 1
        write_json(GLOBAL_MCP_CONFIG, cfg)

    if WORKSPACE_MCP_CONFIG.is_file():
        w_cfg = read_json(WORKSPACE_MCP_CONFIG)
        w_servers = w_cfg.get("mcpServers", {})
        for name, spec in w_servers.items():
            if isinstance(spec, dict) and not spec.get("disabled", False):
                spec["disabled"] = True
                count += 1
        write_json(WORKSPACE_MCP_CONFIG, w_cfg)

    return count


def disable_all_plugins() -> int:
    installed = get_installed_plugins()
    cfg = read_json(GLOBAL_CONFIG)
    plugins_cfg = cfg.setdefault("plugins", {})
    count = 0
    for name in installed:
        entry = plugins_cfg.setdefault(name, {})
        if entry.get("enabled", True):
            entry["enabled"] = False
            count += 1
    write_json(GLOBAL_CONFIG, cfg)
    return count


def enable_mcp_server(name: str) -> bool:
    updated = False
    if GLOBAL_MCP_CONFIG.is_file():
        cfg = read_json(GLOBAL_MCP_CONFIG)
        if name in cfg.get("mcpServers", {}):
            cfg["mcpServers"][name]["disabled"] = False
            write_json(GLOBAL_MCP_CONFIG, cfg)
            updated = True

    if WORKSPACE_MCP_CONFIG.is_file():
        w_cfg = read_json(WORKSPACE_MCP_CONFIG)
        if name in w_cfg.get("mcpServers", {}):
            w_cfg["mcpServers"][name]["disabled"] = False
            write_json(WORKSPACE_MCP_CONFIG, w_cfg)
            updated = True

    return updated


def enable_plugin_bundle(name: str) -> bool:
    cfg = read_json(GLOBAL_CONFIG)
    plugins_cfg = cfg.setdefault("plugins", {})
    plugins_cfg[name] = {"enabled": True}
    return write_json(GLOBAL_CONFIG, cfg)


def resolve_target(query: str) -> Tuple[Optional[str], Optional[str]]:
    norm = query.strip().lower()

    global_mcp = read_json(GLOBAL_MCP_CONFIG).get("mcpServers", {})
    work_mcp = read_json(WORKSPACE_MCP_CONFIG).get("mcpServers", {})
    all_mcps = set(global_mcp.keys()) | set(work_mcp.keys())

    for m in all_mcps:
        if norm in (m.lower(), m.replace("-mcp", "").lower(), m.replace("mcp-", "").lower()):
            return ("mcp", m)

    installed_plugins = get_installed_plugins()
    for p in installed_plugins:
        if norm in (p.lower(), p.replace("agyos-", "").lower()):
            return ("plugin", p)

    for prefix, server_name in MCP_TOOL_PREFIXES.items():
        if norm.startswith(prefix):
            return ("mcp", server_name)

    for plugin_name, skills in PLUGIN_SKILL_MAP.items():
        if norm in [s.lower() for s in skills]:
            return ("plugin", plugin_name)

    return (None, None)


def activate_target(target: str) -> bool:
    target_type, resolved_name = resolve_target(target)
    if not target_type or not resolved_name:
        sys.stderr.write(f"[agy-ondemand] Unrecognized MCP server or plugin: {target}\n")
        return False

    if target_type == "mcp":
        ok = enable_mcp_server(resolved_name)
        if ok:
            print(f"Activated MCP server: {resolved_name}")
            return True
        sys.stderr.write(f"[agy-ondemand] Failed to activate MCP server: {resolved_name}\n")
        return False

    if target_type == "plugin":
        ok = enable_plugin_bundle(resolved_name)
        if ok:
            print(f"Activated plugin: {resolved_name}")
            return True
        sys.stderr.write(f"[agy-ondemand] Failed to activate plugin: {resolved_name}\n")
        return False

    return False


def get_status() -> Dict[str, Any]:
    global_mcp = read_json(GLOBAL_MCP_CONFIG).get("mcpServers", {})
    work_mcp = read_json(WORKSPACE_MCP_CONFIG).get("mcpServers", {})
    cfg_plugins = read_json(GLOBAL_CONFIG).get("plugins", {})
    all_plugins = get_installed_plugins()

    mcp_status = {}
    for k, v in global_mcp.items():
        mcp_status[k] = "disabled" if v.get("disabled", False) else "enabled"
    for k, v in work_mcp.items():
        if k not in mcp_status:
            mcp_status[k] = "disabled" if v.get("disabled", False) else "enabled"

    plugin_status = {}
    for p in all_plugins:
        enabled = cfg_plugins.get(p, {}).get("enabled", True)
        plugin_status[p] = "enabled" if enabled else "disabled"

    return {"mcps": mcp_status, "plugins": plugin_status}


def print_status_table() -> None:
    status = get_status()
    print("=== MCP Servers ===")
    for name, st in sorted(status["mcps"].items()):
        marker = "✓" if st == "enabled" else "○"
        print(f"  [{marker}] {name:<24} : {st}")

    print("\n=== Plugins ===")
    for name, st in sorted(status["plugins"].items()):
        marker = "✓" if st == "enabled" else "○"
        print(f"  [{marker}] {name:<24} : {st}")


def startup_guard() -> None:
    disabled_mcps = disable_all_mcps()
    disabled_plugins = disable_all_plugins()
    print(
        f"[agy-ondemand] Startup initialized: {disabled_mcps} MCPs and {disabled_plugins} plugins set to disabled."
    )


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd in ("startup", "init", "disable-all", "reset", "stop"):
        startup_guard()
    elif cmd in ("status", "list"):
        print_status_table()
    elif cmd in ("activate", "enable", "use"):
        if len(sys.argv) < 3:
            sys.stderr.write("Usage: agy-ondemand activate <mcp-or-plugin-name>\n")
            sys.exit(1)
        target = sys.argv[2]
        success = activate_target(target)
        sys.exit(0 if success else 1)
    elif cmd == "activate-mcp":
        if len(sys.argv) < 3:
            sys.stderr.write("Usage: agy-ondemand activate-mcp <server-name>\n")
            sys.exit(1)
        ok = enable_mcp_server(sys.argv[2])
        if ok:
            print(f"Activated MCP server: {sys.argv[2]}")
        sys.exit(0 if ok else 1)
    elif cmd == "activate-plugin":
        if len(sys.argv) < 3:
            sys.stderr.write("Usage: agy-ondemand activate-plugin <plugin-name>\n")
            sys.exit(1)
        ok = enable_plugin_bundle(sys.argv[2])
        if ok:
            print(f"Activated plugin: {sys.argv[2]}")
        sys.exit(0 if ok else 1)
    else:
        sys.stderr.write(f"Unknown action: {cmd}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
