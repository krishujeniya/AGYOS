#!/usr/bin/env python3
"""Read-only structural and freshness-candidate audit for AGYOS skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agyos_decision.catalog import read_metadata

SKILLS_DIR = ROOT / ".agents" / "skills"
SKILL_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FRONTMATTER = re.compile(r"\A---\n.*?\n---(?:\n|$)", re.DOTALL)
INLINE_LINK = re.compile(r"\!?\[[^\]]*\]\(\s*<?([^\s)>]+)>?(?:\s+[^)]*)?\s*\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$", re.MULTILINE)
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,}).*$")
FRESHNESS_TERMS = re.compile(
    r"\b(?:latest|current|currently|as of|pricing|price|version\s*\d|"
    r"regulation|regulatory|legal|law|clinical|medical|FDA|CVE-\d|CVSS|"
    r"GDPR|HIPAA|PCI(?:\s+DSS)?|YouTube|Runway|Twilio|Azure SDK)\b",
    re.IGNORECASE,
)
DESCRIPTION_TEMPLATE = re.compile(
    r"one sentence\s*[-–:]?\s*what this skill does and when to invoke it",
    re.IGNORECASE,
)
DESCRIPTION_JSON_FRAGMENT = re.compile(
    r"^\s*['\"]?[a-z][a-z0-9_-]*['\"]?\s*:\s*['\"](?:https?://|\{)",
    re.IGNORECASE,
)


def _finding(
    code: str,
    skill: str,
    path: Path,
    message: str,
    line: int | None = None,
    severity: str = "error",
) -> dict:
    item = {
        "code": code,
        "skill": skill,
        "path": path.as_posix(),
        "message": message,
        "severity": severity,
    }
    if line is not None:
        item["line"] = line
    return item


def _source_lines(text: str) -> list[str]:
    """Return Markdown source outside fences, comments, and inline code."""
    output = []
    fence_char = None
    fence_size = 0
    in_comment = False
    for line in text.splitlines():
        fence = FENCE.match(line)
        if fence:
            token = fence.group(1)
            char, size = token[0], len(token)
            if fence_char is None:
                fence_char, fence_size = char, size
            elif char == fence_char and size >= fence_size:
                fence_char = None
                fence_size = 0
            output.append("")
            continue
        if fence_char is not None:
            output.append("")
            continue
        clean = line
        if in_comment:
            close = clean.find("-->")
            if close == -1:
                output.append("")
                continue
            clean = clean[close + 3 :]
            in_comment = False
        while "<!--" in clean:
            start = clean.find("<!--")
            close = clean.find("-->", start + 4)
            if close == -1:
                clean = clean[:start]
                in_comment = True
                break
            clean = clean[:start] + clean[close + 3 :]
        output.append(re.sub(r"`+[^`]*`+", "", clean))
    return output


def _link_targets(lines: list[str]):
    for line_number, line in enumerate(lines, start=1):
        for match in INLINE_LINK.finditer(line):
            yield line_number, match.group(1)
        for match in REFERENCE_LINK.finditer(line):
            yield line_number, match.group(1)


def _check_links(
    source_dir: Path,
    allowed_root: Path,
    source_file: Path,
    text: str,
    skill: str,
) -> tuple[list[dict], list[dict]]:
    findings = []
    review_candidates = []
    for line_number, raw_target in _link_targets(_source_lines(text)):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith("#"):
            continue
        parsed = urlsplit(target)
        if parsed.scheme.lower() in {"http", "https", "mailto", "data", "ftp"}:
            continue
        if parsed.scheme.lower() == "file":
            findings.append(
                _finding("nonportable-file-link", skill, source_file, f"Use a skill-local relative link instead of {target!r}.", line_number)
            )
            continue
        local_path = unquote(parsed.path)
        if not local_path:
            continue
        if local_path.startswith("/"):
            review_candidates.append(
                _finding(
                    "root-relative-link",
                    skill,
                    source_file,
                    f"Confirm this root-relative target is an external documentation URL: {target!r}.",
                    line_number,
                    severity="review",
                )
            )
            continue
        if local_path.startswith("~"):
            findings.append(
                _finding("nonportable-file-link", skill, source_file, f"Use a skill-local relative link instead of {target!r}.", line_number)
            )
            continue
        resolved = (source_dir / local_path).resolve()
        if not resolved.is_relative_to(allowed_root.resolve()) or not resolved.exists():
            findings.append(
                _finding("broken-local-link", skill, source_file, f"Markdown target does not resolve: {target!r}.", line_number)
            )
    return findings, review_candidates


def _has_duplicate_frontmatter(text: str) -> int | None:
    first = FRONTMATTER.match(text)
    if not first:
        return None
    body_lines = _source_lines(text[first.end() :])
    for index, line in enumerate(body_lines[:30]):
        if line.strip() != "---" or index + 2 >= len(body_lines):
            continue
        if not body_lines[index + 1].lstrip().startswith("name:"):
            continue
        has_field = any(
            re.match(r"\s*(?:description|license|metadata):", candidate)
            for candidate in body_lines[index + 2 : index + 8]
        )
        has_close = "---" in body_lines[index + 1 : index + 10]
        if has_field and has_close:
            return len(text[: first.end()].splitlines()) + index + 1
    return None


def _normalized_body(text: str) -> str:
    match = FRONTMATTER.match(text)
    body = text[match.end() :] if match else text
    return re.sub(r"\s+", " ", body).strip().casefold()


def _groups(values: dict[str, list[str]]) -> list[list[str]]:
    return sorted(sorted(names) for names in values.values() if len(names) > 1)


def audit_catalog(skills_dir: Path = SKILLS_DIR) -> dict:
    """Audit direct skill folders and return deterministic findings and review groups."""
    skills_dir = Path(skills_dir).resolve()
    allowed_root = skills_dir.parent.parent if skills_dir.parent.name == ".agents" else skills_dir.parent
    folders = sorted((path for path in skills_dir.iterdir() if path.is_dir()), key=lambda p: p.name)
    findings = []
    review_candidates = []
    bodies: dict[str, list[str]] = defaultdict(list)
    descriptions: dict[str, list[str]] = defaultdict(list)
    freshness_candidates = []
    catalog_count = 0

    for skill_dir in folders:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            findings.append(_finding("missing-skill-file", skill_dir.name, skill_dir, "Direct skill directory has no SKILL.md."))
            continue
        catalog_count += 1
        relative_file = skill_file.relative_to(skills_dir.parent)
        skill = skill_dir.name
        if not SKILL_ID.fullmatch(skill):
            review_candidates.append(
                _finding(
                    "noncanonical-id",
                    skill,
                    relative_file,
                    "Existing public ID uses a non-kebab separator; assess compatibility before renaming.",
                    severity="review",
                )
            )

        try:
            metadata = read_metadata(skill_file)
        except (OSError, UnicodeError, ValueError) as exc:
            findings.append(_finding("invalid-frontmatter", skill, relative_file, str(exc)))
            continue

        description = re.sub(r"\s+", " ", metadata["description"]).strip()
        normalized_description = description.casefold()
        if (
            DESCRIPTION_TEMPLATE.search(description)
            or DESCRIPTION_JSON_FRAGMENT.search(description)
            or normalized_description in {skill.casefold(), "one sentence", "description"}
            or description.lstrip().startswith("{")
            or normalized_description == "[task description]"
        ):
            findings.append(
                _finding("placeholder-description", skill, relative_file, f"Description is not an actionable skill trigger: {description!r}.")
            )
        if len(description) > 300:
            review_candidates.append(
                _finding(
                    "long-description",
                    skill,
                    relative_file,
                    f"Discovery description has {len(description)} characters; review whether it can be shortened without losing task triggers.",
                    severity="review",
                )
            )
        descriptions[normalized_description].append(skill)

        text = skill_file.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        if line_count >= 300:
            findings.append(
                _finding("runbook-too-long", skill, relative_file, f"Primary runbook has {line_count} lines; limit is 299.")
            )
        second_header_line = _has_duplicate_frontmatter(text)
        if second_header_line:
            findings.append(
                _finding(
                    "duplicate-frontmatter",
                    skill,
                    relative_file,
                    "A second YAML skill header appears near the start of the runbook body.",
                    second_header_line,
                )
            )

        full_runbook = skill_dir / "references" / "FULL_RUNBOOK.md"
        body_source = full_runbook.read_text(encoding="utf-8") if full_runbook.is_file() else text
        bodies[_normalized_body(body_source)].append(skill)
        for source_file in sorted(skill_dir.rglob("*.md")):
            if any(part in {"node_modules", ".git", ".venv", "venv", "dist", "build"} for part in source_file.parts):
                continue
            source_relative = source_file.relative_to(skills_dir.parent)
            source_text = source_file.read_text(encoding="utf-8", errors="replace")
            link_findings, link_reviews = _check_links(
                source_file.parent,
                allowed_root,
                source_relative,
                source_text,
                skill,
            )
            findings.extend(link_findings)
            review_candidates.extend(link_reviews)
            for line_number, line in enumerate(source_text.splitlines(), start=1):
                if FRESHNESS_TERMS.search(line):
                    freshness_candidates.append(
                        {
                            "skill": skill,
                            "path": source_relative.as_posix(),
                            "line": line_number,
                            "excerpt": line.strip()[:220],
                        }
                    )

    findings.sort(key=lambda item: (item["skill"], item["code"], item.get("line", 0), item["path"]))
    review_candidates.sort(key=lambda item: (item["skill"], item["code"], item["path"]))
    description_groups = _groups(descriptions)
    body_groups = _groups(bodies)
    return {
        "skill_count": catalog_count,
        "directory_count": len(folders),
        "findings": findings,
        "review_candidates": review_candidates,
        "duplicate_description_groups": description_groups,
        "duplicate_body_groups": body_groups,
        "freshness_candidates": freshness_candidates,
    }


def _print_summary(report: dict) -> None:
    counts: dict[str, int] = defaultdict(int)
    for finding in report["findings"]:
        counts[finding["code"]] += 1
    print(f"Skills scanned: {report['skill_count']} / {report['directory_count']} direct directories")
    print(f"Structural findings: {len(report['findings'])}")
    print(f"Review candidates: {len(report['review_candidates'])}")
    for code, count in sorted(counts.items()):
        print(f"  {code}: {count}")
    print(f"Exact duplicate body groups for review: {len(report['duplicate_body_groups'])}")
    print(f"Exact duplicate description groups for review: {len(report['duplicate_description_groups'])}")
    print(f"Freshness candidates (keyword scan only): {len(report['freshness_candidates'])}")
    for item in report["findings"]:
        location = f"{item['path']}:{item['line']}" if "line" in item else item["path"]
        print(f"{item['code']}: {location}: {item['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=SKILLS_DIR, help="Direct skill root to scan")
    parser.add_argument("--json", action="store_true", help="Print the complete machine-readable report")
    args = parser.parse_args(argv)
    report = audit_catalog(args.skills_dir)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        _print_summary(report)
    return 1 if any(item["severity"] == "error" for item in report["findings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
