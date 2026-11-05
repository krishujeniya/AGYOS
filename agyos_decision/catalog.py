"""Shared, strict skill discovery metadata for runtime and generated indexes."""

from pathlib import Path
import re
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agents" / "skills"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|$)", re.DOTALL)


def read_metadata(skill_file: Path) -> dict[str, Any]:
    """Read metadata without accepting a body or a path as a skill identity."""
    match = FRONTMATTER.match(skill_file.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {skill_file}")
    try:
        metadata = yaml.safe_load(match[1])
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML frontmatter: {skill_file}") from exc
    if not isinstance(metadata, dict) or metadata.get("name") != skill_file.parent.name:
        raise ValueError(f"Skill name must match its directory: {skill_file}")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"Missing skill description: {skill_file}")
    return metadata


def physical_catalog() -> list[dict[str, Any]]:
    """Index every physical runbook; invalid metadata is an actionable error."""
    entries = []
    for file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        metadata = read_metadata(file)
        entries.append({
            "name": file.parent.name,
            "description": metadata["description"].strip(),
            "path": f".agents/skills/{file.parent.name}",
            "tier": 2,
        })
    return entries


def canonical_entry(entry: Any) -> dict[str, Any] | None:
    """Constrain index references to physical runbooks under this checkout."""
    if not isinstance(entry, dict):
        return None
    name = entry.get("id") or entry.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", name):
        return None
    file = SKILLS_DIR / name / "SKILL.md"
    if not file.is_file() or not file.resolve().is_relative_to(SKILLS_DIR.resolve()):
        return None
    description = entry.get("description", "")
    category = entry.get("category") or entry.get("module") or ""
    if not isinstance(description, str) or not description.strip() or not isinstance(category, str):
        return None
    return {
        "name": name,
        "description": description,
        "path": f".agents/skills/{name}",
        "tier": entry.get("tier", 2),
        "category": category.lower(),
    }
