#!/usr/bin/env python3
"""AGYOS Strix Security & Penetration Testing Runner.

Coordinates autonomous penetration testing, OWASP Top 10 assessment, and
exploit verification using the Strix toolkit in tools/security/strix.

Usage:
  python3 scripts/strix_runner.py status [--json]
  python3 scripts/strix_runner.py skills [--json]
  python3 scripts/strix_runner.py test-inventory [--json]
  python3 scripts/strix_runner.py scan --target <path-or-url> [--mode quick|deep] [--budget <n>]
  python3 scripts/strix_runner.py cloud <subcommand> [args...]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
STRIX_ROOT = ROOT / "tools" / "security" / "strix"
SKILLS_DIR = ROOT / ".agents" / "skills"

STRIX_SKILLS = [
    "penetration-testing-with-strix",
    "managed-pentesting-with-strix",
    "ci-security-scanning-with-strix",
    "fix-security-vulnerabilities-with-strix",
    "application-security-testing",
    "web-app-penetration-testing",
    "owasp-top-10-testing",
    "find-security-vulnerabilities-in-code",
    "strix-api-security-testing",
]


def check_status() -> Dict[str, Any]:
    """Inspect environment, dependencies, and configuration for Strix."""
    docker_installed = shutil.which("docker") is not None
    uv_installed = shutil.which("uv") is not None
    obscura_bin = ROOT / "bin" / "obscura"

    strix_present = STRIX_ROOT.is_dir()
    pyproject_file = STRIX_ROOT / "pyproject.toml"

    installed_skills = []
    for skill_name in STRIX_SKILLS:
        skill_path = SKILLS_DIR / skill_name / "SKILL.md"
        if skill_path.is_file():
            installed_skills.append(skill_name)

    llm_configured = bool(os.environ.get("STRIX_LLM") and os.environ.get("LLM_API_KEY"))
    cloud_token_configured = bool(os.environ.get("STRIX_API_TOKEN"))

    return {
        "strix_toolkit_present": strix_present,
        "strix_path": str(STRIX_ROOT),
        "pyproject_found": pyproject_file.is_file(),
        "docker_available": docker_installed,
        "uv_available": uv_installed,
        "obscura_available": obscura_bin.is_file(),
        "llm_configured": llm_configured,
        "cloud_token_configured": cloud_token_configured,
        "strix_llm": os.environ.get("STRIX_LLM", "not set"),
        "installed_skills_count": len(installed_skills),
        "installed_skills": installed_skills,
    }


def list_skills() -> List[Dict[str, str]]:
    """List available Strix pentesting and security skills."""
    catalog = []
    for skill_name in STRIX_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        description = "Not installed"
        if skill_md.is_file():
            text = skill_md.read_text(encoding="utf-8")
            for line in text.splitlines():
                if line.startswith("description:"):
                    description = line.replace("description:", "").strip().strip('"').strip("'")
                    break
        catalog.append({
            "name": skill_name,
            "path": str(skill_md),
            "description": description,
        })
    return catalog


def test_inventory() -> Dict[str, Any]:
    """Inspect and inventory test modules in the Strix toolkit."""
    tests_dir = STRIX_ROOT / "tests"
    if not tests_dir.is_dir():
        return {"error": f"Tests directory not found at {tests_dir}", "test_files": []}

    test_files = sorted(tests_dir.glob("test_*.py"))
    inventory = []
    for tf in test_files:
        inventory.append({
            "name": tf.name,
            "size_bytes": tf.stat().st_size,
        })

    return {
        "tests_directory": str(tests_dir),
        "total_test_files": len(inventory),
        "test_files": inventory,
    }


def run_scan(target: str, mode: str = "quick", budget: float = 10.0, dry_run: bool = False) -> int:
    """Execute or prepare headless Strix pentest scan."""
    status = check_status()
    if not status["strix_toolkit_present"]:
        print(f"Error: Strix toolkit not found at {STRIX_ROOT}", file=sys.stderr)
        return 1

    cmd = [
        "python3", "-m", "strix.interface.main",
        "-n",
        "-t", target,
        "--scan-mode", mode,
        "--max-budget", str(budget),
    ]

    env = os.environ.copy()
    current_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{STRIX_ROOT}:{current_pp}" if current_pp else str(STRIX_ROOT)

    if dry_run:
        print("Dry run mode. Planned command:")
        print(" ".join(cmd))
        print("Environment PYTHONPATH:", env["PYTHONPATH"])
        return 0

    if not status["docker_available"] and not status["cloud_token_configured"]:
        print(
            "Notice: Local Docker engine is required for self-hosted sandbox execution. "
            "For managed cloud execution without Docker, configure STRIX_API_TOKEN.",
            file=sys.stderr,
        )

    import subprocess
    proc = subprocess.run(cmd, env=env, cwd=str(STRIX_ROOT))
    return proc.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AGYOS Strix Security & Pentest Runner")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to execute")

    status_parser = subparsers.add_parser("status", help="Inspect Strix environment and setup")
    status_parser.add_argument("--json", action="store_true", help="Output JSON format")

    skills_parser = subparsers.add_parser("skills", help="List registered Strix skills")
    skills_parser.add_argument("--json", action="store_true", help="Output JSON format")

    inv_parser = subparsers.add_parser("test-inventory", help="List test suite inventory")
    inv_parser.add_argument("--json", action="store_true", help="Output JSON format")

    scan_parser = subparsers.add_parser("scan", help="Run or plan a headless pentest scan")
    scan_parser.add_argument("--target", "-t", required=True, help="Target directory, URL, or API spec")
    scan_parser.add_argument("--mode", "-m", choices=["quick", "deep"], default="quick", help="Scan depth mode")
    scan_parser.add_argument("--budget", "-b", type=float, default=10.0, help="Maximum budget in USD")
    scan_parser.add_argument("--dry-run", action="store_true", help="Print command without executing")

    args, extra = parser.parse_known_args(argv)

    if args.subcommand == "status":
        st = check_status()
        if args.json:
            print(json.dumps(st, indent=2))
        else:
            print("=== AGYOS Strix Security Toolkit Status ===")
            print(f"Toolkit Present:       {st['strix_toolkit_present']}")
            print(f"Toolkit Path:          {st['strix_path']}")
            print(f"Pyproject Found:       {st['pyproject_found']}")
            print(f"Docker Available:      {st['docker_available']}")
            print(f"uv Available:          {st['uv_available']}")
            print(f"Obscura Headless:      {st['obscura_available']}")
            print(f"LLM Configured:        {st['llm_configured']} (model: {st['strix_llm']})")
            print(f"Cloud Token:           {st['cloud_token_configured']}")
            print(f"Installed Skills:      {st['installed_skills_count']} / {len(STRIX_SKILLS)}")
            for sk in st["installed_skills"]:
                print(f"  - {sk}")
        return 0

    if args.subcommand == "skills":
        sk_list = list_skills()
        if args.json:
            print(json.dumps(sk_list, indent=2))
        else:
            print("=== Registered Strix Pentest Skills ===")
            for item in sk_list:
                print(f"\n[{item['name']}]")
                print(f"  Path: {item['path']}")
                print(f"  Summary: {item['description'][:120]}...")
        return 0

    if args.subcommand == "test-inventory":
        inv = test_inventory()
        if args.json:
            print(json.dumps(inv, indent=2))
        else:
            print(f"=== Strix Test Suite Inventory ({inv.get('total_test_files', 0)} files) ===")
            print(f"Directory: {inv.get('tests_directory', '')}")
            for tf in inv.get("test_files", []):
                print(f"  - {tf['name']} ({tf['size_bytes']} bytes)")
        return 0

    if args.subcommand == "scan":
        return run_scan(target=args.target, mode=args.mode, budget=args.budget, dry_run=args.dry_run)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
