#!/usr/bin/env python3
"""Read-only AGYOS privacy coverage audit. Prints no file contents or secrets.

A successful audit run means the scan executed, NOT that the OS is end-to-end
encrypted. Full encryption is never asserted for hosted-model deployments.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PLAINTEXT_PATHS = (
    ".agents/state/state.json",
    ".agents/state/memory.json",
    ".agents/state/CURRENT.md",
    ".agents/state/context-graph.json",
)
PLAINTEXT_DIRECTORIES = (".agents/state/checkpoints", ".agents/state/decisions")


def tracked(relative: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", "--", relative],
        capture_output=True, text=True, check=False, timeout=10,
    )
    return result.returncode == 0


def status() -> dict:
    surfaces: list[dict] = []
    for relative in PLAINTEXT_PATHS:
        exists = (ROOT / relative).is_file()
        surfaces.append({
            "surface": relative, "exists": exists, "tracked": tracked(relative) if exists else False,
            "protection": "plaintext" if exists else "not_present",
        })
    for relative in PLAINTEXT_DIRECTORIES:
        exists = (ROOT / relative).is_dir()
        surfaces.append({
            "surface": relative, "exists": exists,
            "protection": "plaintext_storage_possible" if exists else "not_present",
        })

    vault_path = Path(os.environ.get(
        "AGYOS_VAULT_PATH",
        str(Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local/state")))
            / "agyos/private-memory.vault.json"),
    )).expanduser()
    try:
        st = vault_path.lstat()
        private_vault = bool(
            stat.S_ISREG(st.st_mode) and not vault_path.is_symlink()
            and st.st_mode & 0o077 == 0
            and vault_path.parent.stat().st_mode & 0o077 == 0
        )
    except OSError:
        private_vault = False

    return {
        "schema_version": 1,
        "full_e2ee": False,
        "scope": "read_only_metadata_scan",
        "memory_vault_present_and_private": private_vault,
        "memory_private_only_enabled": os.environ.get("AGYOS_MEMORY_PRIVATE_ONLY") == "1",
        "runtime": {
            "agy_available": shutil.which("agy") is not None,
            "bun_available": shutil.which("bun") is not None,
            "node_available": shutil.which("node") is not None,
        },
        "surfaces": surfaces,
        "unresolved": [
            "Hosted-model provider must see normal plaintext inference requests",
            "Workflow state/checkpoints, telemetry and independent ECC memory are not uniformly encrypted",
            "Key rotation, replay prevention and multi-device E2EE not independently audited",
            "Existing public Git history cannot be made private by encrypting future writes",
            "Installed AGY CLI and external platforms require host-specific testing",
        ],
        "conclusion": "PARTIAL_ENCRYPTION_NOT_SYSTEM_WIDE_E2EE",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only AGYOS privacy audit")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero unless fully E2EE (expected to fail for hosted models)")
    args = parser.parse_args()
    result = status()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if args.strict and not result["full_e2ee"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
