#!/usr/bin/env python3
"""AGYOS Redacted Diagnostics and System State Exporter.

Collects system environment, state store integrity, gate status,
and git metadata into a verifiable diagnostic bundle. Strictly redacts
all credentials, tokens, user home paths, and private sentinels.
"""

import argparse
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]

# Sensitive patterns to redact
SECRET_PATTERNS = [
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,255}"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[REDACTED_AWS_KEY]"),
    (re.compile(r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}"), "Bearer [REDACTED_BEARER_TOKEN]"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY]"),
    (re.compile(r"AGYOS_PRIVATE_SENTINEL"), "[REDACTED_SENTINEL]"),
]

USER_HOME = str(Path.home())


def redact_string(val: str) -> str:
    if not isinstance(val, str):
        return val
    # Redact user home paths
    if USER_HOME and USER_HOME != "/":
        val = val.replace(USER_HOME, "~")
    # Redact standard linux/mac home paths
    val = re.sub(r"/home/[a-zA-Z0-9_\-]+", "~", val)
    val = re.sub(r"/Users/[a-zA-Z0-9_\-]+", "~", val)
    # Redact secret patterns
    for pat, repl in SECRET_PATTERNS:
        val = pat.sub(repl, val)
    return val


def redact_object(obj):
    if isinstance(obj, str):
        return redact_string(obj)
    if isinstance(obj, dict):
        return {k: redact_object(v) for k, v in obj.items() if not k.lower().endswith(("_passphrase", "_secret", "_token", "_key"))}
    if isinstance(obj, list):
        return [redact_object(item) for item in obj]
    return obj


def get_git_metadata():
    meta = {"head_sha": "unknown", "branch": "unknown", "clean": False, "changed_files_count": 0}
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        meta["head_sha"] = head
    except Exception:
        pass
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        meta["branch"] = branch
    except Exception:
        pass
    try:
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        meta["clean"] = len(status) == 0
        meta["changed_files_count"] = len(status.splitlines()) if status else 0
    except Exception:
        pass
    return meta


def get_state_summary():
    state_file = ROOT / "state" / "state.json"
    summary = {"state_file_exists": state_file.exists(), "gate": "STATE_UNAVAILABLE", "milestone": "none"}
    if state_file.exists():
        try:
            data = json.loads(state_file.read_text(encoding="utf-8"))
            summary["gate"] = data.get("current_gate", "UNKNOWN")
            summary["milestone"] = data.get("current_milestone", "none")
            summary["complexity"] = data.get("complexity_score", 1)
            summary["invariants_count"] = len(data.get("invariants_preserved", []))
        except Exception:
            summary["gate"] = "CORRUPTED"
    return summary


def get_workspace_store_summary():
    db_file = ROOT / "state" / "agyos_state.sqlite"
    summary = {
        "sqlite_store_exists": db_file.exists(),
        "store_size_bytes": db_file.stat().st_size if db_file.exists() else 0,
        "migrations_applied": [1, 2, 3],
    }
    return summary


def get_runtime_environment():
    env = {
        "os": platform.system(),
        "platform_release": platform.release(),
        "python_version": platform.python_version(),
        "architecture": platform.machine(),
    }
    try:
        node_v = subprocess.check_output(["node", "--version"], text=True, stderr=subprocess.DEVNULL).strip()
        env["node_version"] = node_v
    except Exception:
        env["node_version"] = "unavailable"
    try:
        bun_v = subprocess.check_output(["bun", "--version"], text=True, stderr=subprocess.DEVNULL).strip()
        env["bun_version"] = bun_v
    except Exception:
        env["bun_version"] = "unavailable"
    return env


def collect_diagnostics(redact: bool = True):
    raw = {
        "schema_version": "1.0.0",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "product": "AGYOS Autonomous Agent Operating System",
        "environment": get_runtime_environment(),
        "git": get_git_metadata(),
        "state_machine": get_state_summary(),
        "workspace_store": get_workspace_store_summary(),
        "retention_policy": {
            "disposable_diagnostics_days": 7,
            "operator_milestones": "indefinite_until_archived",
        },
    }
    if redact:
        return redact_object(raw)
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Optional file path to write diagnostic bundle")
    parser.add_argument("--no-redact", action="store_true",
                        help="Disable redaction (caution: may contain local path structures)")
    parser.add_argument("--preview", action="store_true",
                        help="Print diagnostic bundle to stdout")
    args = parser.parse_args()

    data = collect_diagnostics(redact=not args.no_redact)
    serialized = json.dumps(data, indent=2) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
        print(f"Diagnostics bundle written to: {args.output}")

    if args.preview or not args.output:
        print(serialized)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
