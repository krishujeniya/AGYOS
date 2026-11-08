"""Restricted, opt-in Agent Reach CLI adapter (no installation or authentication).

Only read-only searches on default public channels and health queries are
allowed. This is not a bypass for platform access controls or AGYOS governance.
"""
from __future__ import annotations

import json
import shutil
import subprocess

PUBLIC_SEARCH_CHANNELS = frozenset({"github", "youtube", "web"})
HEALTH_OPERATIONS = frozenset({"version", "channels", "doctor"})
MAX_OUTPUT = 256 * 1024


def agent_reach_available() -> bool:
    return shutil.which("agent-reach") is not None


def invoke_read_only(operation: str, query: str | None = None, *, timeout: int = 25) -> dict:
    binary = shutil.which("agent-reach")
    if binary is None:
        return {"ok": False, "error": "NOT_INSTALLED", "hint": "Review pinned upstream docs/install.md; never install a similarly named PyPI package"}
    if operation in HEALTH_OPERATIONS and query is None:
        cmd = [binary, operation]
    elif operation in PUBLIC_SEARCH_CHANNELS and isinstance(query, str) and 0 < len(query.strip()) <= 500:
        cmd = [binary, operation, "search", query.strip()]
    else:
        return {"ok": False, "error": "UNAUTHORIZED_OPERATION", "hint": "Only version/channels/doctor or public read-only search is permitted"}
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return {"ok": False, "error": "UNAVAILABLE", "hint": "CLI missing, timed out, or not responsive"}
    if len(result.stdout) > MAX_OUTPUT:
        return {"ok": False, "error": "OUTPUT_LIMIT", "hint": "CLI response exceeded safe size limit"}
    try:
        parsed = json.loads(result.stdout)
    except (ValueError, TypeError):
        return {"ok": False, "error": "INVALID_RESPONSE", "hint": "Expected JSON from verified Agent Reach v1.6+"}
    if not isinstance(parsed, dict) or not isinstance(parsed.get("ok"), bool):
        return {"ok": False, "error": "INVALID_RESPONSE", "hint": "Invalid Agent Reach response envelope"}
    if result.returncode != 0:
        return {"ok": False, "error": "UPSTREAM_ERROR", "hint": "Inspect local Agent Reach channel health without logging credentials"}
    return {"ok": parsed["ok"], "result": parsed.get("result"), "source": "Agent Reach (untrusted external data)"}
