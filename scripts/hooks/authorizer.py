#!/usr/bin/env python3
"""Fail-closed AGYOS tool authorizer.

Authorization flags inside model/tool payloads are untrusted. Irreversible
commands stay blocked until a separately verified human approval path exists.
Snapshots are local/private, not a backup system for secrets or external files.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import stat
import sys
import time

ROOT_DIR = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = ROOT_DIR / ".agents" / "state" / "snapshots"
MAX_HOOK_INPUT = 1024 * 1024
MAX_SNAPSHOT_BYTES = 16 * 1024 * 1024

R3_BLOCKED_PATTERNS = (
    r"api\.stripe\.com",
    r"\b(refund|charge|disburse)\b",
    r"\bwire\s+money\b",
    r"\btransfer\b.*\$",
    r"\b(drop\s+database|drop\s+table)\b",
    r"\bdelete\s+from\b.*\b(all|users|accounts)\b",
    r"\b(blast|broadcast)\b.*\b(all|entire)\b.*\b(list|contacts|leads)\b",
)
HIGH_IMPACT_RE = re.compile(
    r"\b(?:wire|refund|charge|stripe|transfer|drop|delete|broadcast|disburse)\b",
    re.IGNORECASE,
)
WRITE_TOOLS = frozenset(("edit_file", "write_file", "write_to_file", "replace_file_content"))


def ensure_snapshot_dir() -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, mode=0o700, exist_ok=True)
    if SNAPSHOT_DIR.is_symlink() or not SNAPSHOT_DIR.is_dir():
        raise ValueError("Unsafe snapshot directory")
    os.chmod(SNAPSHOT_DIR, 0o700)
    return SNAPSHOT_DIR


def extract_tool_info(data: dict) -> tuple[str, dict]:
    call = data.get("toolCall")
    if isinstance(call, dict):
        name, args = call.get("name", ""), call.get("args", {})
    else:
        name, args = data.get("tool_name", ""), data.get("tool_input", {})
    return name if isinstance(name, str) else "", args if isinstance(args, dict) else {}


def is_high_impact_command(cmd: str) -> bool:
    if not isinstance(cmd, str):
        return False
    return bool(HIGH_IMPACT_RE.search(cmd)) or any(
        re.search(pat, cmd, re.IGNORECASE) for pat in R3_BLOCKED_PATTERNS
    )


def backup_pre_write(path_str: str) -> str:
    """Back up regular AGYOS files with private permissions and no symlinks."""
    path = Path(path_str).expanduser()
    if not path.is_absolute():
        path = ROOT_DIR / path
    if path.is_symlink():
        raise ValueError("Refusing symlink source")
    resolved = path.resolve(strict=False)
    if not resolved.is_relative_to(ROOT_DIR):
        return ""  # Never copy files from unrelated projects into this repo.
    relative = resolved.relative_to(ROOT_DIR)
    if ".git" in relative.parts or (
        ".agents" in relative.parts and "state" in relative.parts
    ):
        return ""  # Do not duplicate sensitive state or git metadata.
    if resolved.name.startswith(".env") or resolved.suffix in (
        ".pem", ".key", ".cert", ".crt"
    ):
        return ""
    if not resolved.exists():
        return ""
    prior = resolved.lstat()
    if not stat.S_ISREG(prior.st_mode) or prior.st_size > MAX_SNAPSHOT_BYTES:
        raise ValueError("Existing file cannot be safely snapshotted")

    directory = ensure_snapshot_dir()
    digest = hashlib.sha256(str(relative).encode("utf-8")).hexdigest()[:12]
    name = f"{resolved.name}.{digest}.{time.time_ns()}.{secrets.token_hex(6)}.bak"
    dest = directory / name
    source_fd = os.open(resolved, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    target_fd = None
    try:
        current = os.fstat(source_fd)
        if not stat.S_ISREG(current.st_mode) or (
            current.st_ino, current.st_dev
        ) != (prior.st_ino, prior.st_dev):
            raise ValueError("Snapshot source changed during read")
        target_fd = os.open(
            dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
        with os.fdopen(source_fd, "rb", closefd=False) as src:
            with os.fdopen(target_fd, "wb", closefd=False) as dst:
                shutil.copyfileobj(src, dst, length=1024 * 1024)
                dst.flush()
                os.fsync(dst.fileno())
        return str(dest)
    except Exception:
        if dest.exists():
            dest.unlink()
        raise
    finally:
        os.close(source_fd)
        if target_fd is not None:
            os.close(target_fd)


def deny(reason: str) -> None:
    print(json.dumps({"decision": "deny", "reason": reason}))


def main(event: str) -> None:
    if event != "PreToolUse":
        print(json.dumps({"decision": "allow"} if event == "Stop" else {}))
        return

    raw_input = sys.stdin.read(MAX_HOOK_INPUT + 1)
    if len(raw_input) > MAX_HOOK_INPUT:
        deny("Hook payload exceeds 1 MiB limit")
        return
    try:
        data = json.loads(raw_input) if raw_input.strip() else {}
    except (ValueError, UnicodeError):
        if is_high_impact_command(raw_input):
            deny("Cannot authorize high-impact action with malformed input")
            return
        data = {}
    if not isinstance(data, dict):
        deny("Expected a JSON tool event object")
        return

    tool_name, tool_args = extract_tool_info(data)
    contract = data.get("taskContract")
    if isinstance(contract, dict):
        allowlist = contract.get("capability_allowlist")
        if isinstance(allowlist, list) and allowlist:
            if tool_name and tool_name not in allowlist:
                deny(f"Tool '{tool_name}' blocked by capability allowlist")
                return

    command = tool_args.get("CommandLine") or tool_args.get("command", "")
    if isinstance(command, str) and command:
        for pattern in R3_BLOCKED_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                # 'authorized' and 'outbox_token' are caller-controlled fields.
                # Until a trusted approval verifier is wired, R3 must remain denied.
                deny("R3 irreversible action blocked: trusted outbox approval verification unavailable")
                return

    if tool_name in WRITE_TOOLS:
        target = (
            tool_args.get("Path") or tool_args.get("file_path")
            or tool_args.get("target_file")
        )
        if isinstance(target, str) and target:
            try:
                backup_pre_write(target)
            except (OSError, ValueError) as exc:
                deny(f"Pre-write snapshot refused: {type(exc).__name__}")
                return
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    event = sys.argv[1] if len(sys.argv) > 1 else "PreToolUse"
    try:
        main(event)
    except Exception:
        deny("Authorizer failed safely; inspect local diagnostics")
