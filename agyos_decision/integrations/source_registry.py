"""Pinned external capability registry; never executes upstream instructions.

The native AGYOS catalog remains the only authoritative skill selector. Source
routing is a narrow, explainable enhancement for specific multi-concept intents.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "integrations" / "registry" / "sources.json"
VALID_DISPOSITIONS = {"REUSE", "ENHANCE", "IMPORT", "ADAPT", "REFERENCE", "QUARANTINE", "BLOCK"}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.casefold()))


def _contains(query: str, phrase: str) -> bool:
    tokenized = _normalize(phrase)
    return bool(tokenized) and f" {tokenized} " in f" {query} "


def load_registry(path: Path = REGISTRY, skills_dir: Path | None = None) -> list[dict]:
    """Validate untrusted JSON and physical destinations before using a route."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Unsupported source registry schema")
    entries = data.get("sources")
    if not isinstance(entries, list) or len(entries) != 8:
        raise ValueError("Expected eight explicitly reviewed source entries")
    root = skills_dir or ROOT / ".agents" / "skills"
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Malformed source")
        source_id = entry.get("id")
        if not isinstance(source_id, str) or not ID_PATTERN.fullmatch(source_id) or source_id in seen:
            raise ValueError("Duplicate or invalid source id")
        seen.add(source_id)
        if not isinstance(entry.get("repo"), str) or not REPO_PATTERN.fullmatch(entry["repo"]):
            raise ValueError("Invalid source repository")
        if not isinstance(entry.get("commit"), str) or not SHA_PATTERN.fullmatch(entry["commit"]):
            raise ValueError("Source must be pinned to a commit")
        if entry.get("disposition") not in VALID_DISPOSITIONS:
            raise ValueError("Unknown integration disposition")
        skill = entry.get("primary_skill")
        if not isinstance(skill, str) or not ID_PATTERN.fullmatch(skill):
            raise ValueError("Invalid skill identifier")
        skill_path = root / skill / "SKILL.md"
        if not skill_path.is_file() or not skill_path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Integration maps to missing or unsafe skill: {skill}")
        rules = entry.get("routes")
        if not isinstance(rules, list) or not rules:
            raise ValueError("Missing intent rules")
        for terms in rules:
            if (not isinstance(terms, list) or len(terms) < 2 or
                    any(not isinstance(t, str) or not t.strip() or len(t) > 90 for t in terms)):
                raise ValueError("Only multi-concept, bounded intent rules are allowed")
    return entries


def match_sources(query: str, entries: list[dict] | None = None) -> list[dict]:
    """Return ranked evidence for multi-concept matches; no implicit tool calls."""
    if not isinstance(query, str) or not query.strip():
        return []
    normalized = _normalize(query)
    if entries is None:
        entries = load_registry()
    matched = []
    for entry in entries:
        scores = [
            sum(3 + len(_normalize(term).split()) for term in terms)
            for terms in entry["routes"]
            if all(_contains(normalized, term) for term in terms)
        ]
        if scores:
            matched.append({
                "source_id": entry["id"],
                "source_repo": entry["repo"],
                "commit": entry["commit"],
                "primary_skill": entry["primary_skill"],
                "pod": entry["pod"],
                "status": entry["status"],
                "disposition": entry["disposition"],
                "score": max(scores),
            })
    return sorted(matched, key=lambda e: (-e["score"], e["source_id"]))
