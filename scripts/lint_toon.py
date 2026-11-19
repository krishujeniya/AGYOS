#!/usr/bin/env python3
"""Static TOON envelope linter for AGYOS (no heavy execution; CI-safe).

Checks .toon files against the repo's blob-envelope and prompt formats:
  - blob files: mode line present, text is a single quoted string
  - prompt files: skill line, sections[N] header, count equals list length
Also provides the hook subcommands (--check-path, --check-command, --lint-changed, --summary).
"""
import re
import subprocess
import sys
from pathlib import Path

BLOB_RE = re.compile(r'^mode: "100644"\ntext: "(?:[^"\\]|\\.)*"\n$', re.S)
HEADER_BLOB_RE = re.compile(r'^mode: "100644"\nheader: "(?:[^"\\]|\\.)*"\n$', re.S)


def lint_file(path: Path):
    problems = []
    text = path.read_text(encoding="utf-8")
    if text.startswith('mode: "100644"'):
        if text.startswith('mode: "100644"\nheader: "'):
            if not HEADER_BLOB_RE.match(text):
                problems.append("header blob malformed (unescaped quote/newline or missing trailing newline)")
        elif not BLOB_RE.match(text):
            problems.append("blob envelope malformed (unescaped quote/newline or missing trailing newline)")
        return problems
    if text.startswith('skill: "'):
        m = re.search(r"^sections\[(\d+)\]:$", text, re.M)
        if not m:
            problems.append("sections header missing")
            return problems
        declared = int(m.group(1))
        actual = len(re.findall(r'^  - "', text, re.M))
        if declared != actual:
            problems.append(f"sections[{declared}] but {actual} list entries")
        return problems
    if text.startswith("skill_name:"):
        m = re.search(r"^evals\[(\d+)\]:$", text, re.M)
        if not m:
            problems.append("evals header missing")
            return problems
        declared = int(m.group(1))
        actual = len(re.findall(r"^  - \d+, ", text, re.M))
        if declared != actual:
            problems.append(f"evals[{declared}] but {actual} entries")
        return problems
    if text.startswith('name: "') or text.startswith("mcpServers:") or text.startswith('version: "'):
        return problems  # flat manifest (plugin.toon, mcp_config.toon, matrix): key: value lines
    problems.append("unrecognized .toon envelope (no mode/text, sections or evals header)")
    return problems


BARE_PY = re.compile(r"(?:^|\s|;|&&)(?:python3?|pip3?)(?:\s|$)")


def check_command(cmd: str) -> int:
    if BARE_PY.search(cmd):
        print("BLOCK: bare python/pip invocation; use uv run", file=sys.stderr)
        return 1
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--lint-changed",):
        root = Path(".")
        fail = False
        for p in sorted(root.rglob("*.toon")):
            problems = lint_file(p)
            for pr in problems:
                print(f"FAIL {p}: {pr}")
                fail = True
        sys.exit(1 if fail else 0)
    if args[0] == "--check-command":
        sys.exit(check_command(args[1] if len(args) > 1 else ""))
    if args[0] == "--check-path":
        # hook passes the target path; writes must stay under .agents/ or scripts/
        target = args[1] if len(args) > 1 else ""
        allowed = ("./.agents/", ".agents/", "./scripts/", "scripts/")
        if not target.startswith(allowed):
            print(f"BLOCK: write outside .agents/ and scripts/: {target}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)
    if args[0] == "--summary":
        files = list(Path(".").rglob("*.toon"))
        bad = [p for p in files if lint_file(p)]
        print(f"static verification: {len(files)} .toon files, {len(bad)} with defects; git diff --check follows")
        subprocess.run(["git", "diff", "--check"], check=False)
        sys.exit(0)
    print("unknown flag", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
