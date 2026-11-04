#!/usr/bin/env python3
"""AGYOS Fail-Closed Authorizer Hook.

Enforces:
1. R3 Irreversible Action Blocking (payments, refunds, wire transfers, mass broadcasts, production drops)
   unless explicit outbox authorization token is present.
2. Capability Allowlist Enforcement: blocks tool invocations outside the assigned task contract allowlist.
3. Pre-Write Snapshots: creates automatic backups before write_file/edit_file operations.
4. Fail-Closed Resilience: denies high-impact actions when evaluation encounters unknown or corrupted state.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import sys
import time

R3_BLOCKED_PATTERNS = [
    r"api\.stripe\.com",
    r"\b(refund|charge|disburse)\b",
    r"\bwire\s+money\b",
    r"\btransfer\b.*\$",
    r"\b(drop\s+database|drop\s+table)\b",
    r"\bdelete\s+from\b.*\b(all|users|accounts)\b",
    r"\b(blast|broadcast)\b.*\b(all|entire)\b.*\b(list|contacts|leads)\b",
]

HIGH_IMPACT_KEYWORDS = [
    "wire", "refund", "pay", "charge", "stripe", "transfer",
    "drop", "delete", "broadcast", "disburse", "sign",
]

ROOT_DIR = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = ROOT_DIR / ".agents" / "state" / "snapshots"


def ensure_snapshot_dir() -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    return SNAPSHOT_DIR


def extract_tool_info(data: dict) -> tuple[str, dict]:
    tool_call = data.get("toolCall")
    if isinstance(tool_call, dict):
        name = tool_call.get("name", "")
        args = tool_call.get("args", {})
        return name, args if isinstance(args, dict) else {}
    legacy_input = data.get("tool_input", {})
    if isinstance(legacy_input, dict):
        name = data.get("tool_name", "")
        return name, legacy_input
    return "", {}


def is_high_impact_command(cmd: str) -> bool:
    lower = cmd.lower()
    return any(re.search(pat, lower) for pat in R3_BLOCKED_PATTERNS) or any(kw in lower for kw in HIGH_IMPACT_KEYWORDS)


def backup_pre_write(path_str: str) -> str:
    """Take transactional snapshot of file before mutation."""
    try:
        p = Path(path_str)
        if not p.is_absolute():
            p = ROOT_DIR / p
        if p.is_file():
            snap_dir = ensure_snapshot_dir()
            timestamp = int(time.time() * 1000)
            backup_path = snap_dir / f"{p.name}.{timestamp}.bak"
            shutil.copy2(p, backup_path)
            return str(backup_path)
    except Exception:
        pass
    return ""


def main(event: str) -> None:
    if event != "PreToolUse":
        print(json.dumps({"decision": "allow"} if event == "Stop" else {}))
        return

    raw_input = sys.stdin.read()
    try:
        data = json.loads(raw_input) if raw_input.strip() else {}
    except Exception as e:
        # If raw input has high-impact markers, fail closed
        if any(kw in raw_input.lower() for kw in HIGH_IMPACT_KEYWORDS):
            print(json.dumps({
                "decision": "deny",
                "reason": f"High-impact authorizer error (fail-closed on malformed payload): {e}"
            }))
            return
        data = {}

    tool_name, tool_args = extract_tool_info(data)

    # 1. Capability Allowlist Enforcement
    contract = data.get("taskContract")
    if isinstance(contract, dict):
        allowlist = contract.get("capability_allowlist")
        if isinstance(allowlist, list) and allowlist:
            if tool_name and tool_name not in allowlist:
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"Tool '{tool_name}' blocked: not permitted in task capability allowlist {allowlist}"
                }))
                return

    # 2. R3 Irreversible Action Blocking
    cmd = tool_args.get("CommandLine") or tool_args.get("command", "")
    if isinstance(cmd, str) and cmd:
        for pat in R3_BLOCKED_PATTERNS:
            if re.search(pat, cmd, re.IGNORECASE):
                # Check for explicit outbox authorization token
                if not data.get("authorized", False) and not tool_args.get("outbox_token"):
                    print(json.dumps({
                        "decision": "deny",
                        "reason": f"R3 irreversible action blocked: requires operator authorization in outbox (matched {pat})"
                    }))
                    return

    # 3. Pre-Write Snapshot
    if tool_name in ("edit_file", "write_file", "write_to_file", "replace_file_content"):
        target_path = tool_args.get("Path") or tool_args.get("file_path") or tool_args.get("target_file")
        if isinstance(target_path, str) and target_path:
            backup_pre_write(target_path)

    # Default Allow
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    event = sys.argv[1] if len(sys.argv) > 1 else "PreToolUse"
    try:
        main(event)
    except Exception as exc:
        print(json.dumps({
            "decision": "deny",
            "reason": f"Authorizer execution exception (fail-closed): {exc}"
        }))
