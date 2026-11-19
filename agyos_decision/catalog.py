"""Shared, strict skill discovery metadata for runtime and generated indexes."""

from pathlib import Path
import re
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agents" / "skills"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|$)", re.DOTALL)
YAML_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def read_metadata(skill_file: Path) -> dict[str, Any]:
    """Read metadata without accepting a body or a path as a skill identity."""
    raw_text = ""
    if skill_file.is_file():
        raw_text = skill_file.read_text(encoding="utf-8")
        if raw_text.startswith('mode: "'):
            m = re.search(r'^(?:header|text): ("(?:[^"\\]|\\.)*")', raw_text, re.M)
            if m:
                import json
                raw_text = json.loads(m.group(1))
    elif skill_file.name == "SKILL.md":
        toon_file = skill_file.with_name("SKILL.toon")
        if toon_file.is_file():
            raw_toon = toon_file.read_text(encoding="utf-8")
            if raw_toon.startswith('mode: "'):
                m = re.search(r'^(?:header|text): ("(?:[^"\\]|\\.)*")', raw_toon, re.M)
                if m:
                    import json
                    raw_text = json.loads(m.group(1))
    if not raw_text:
        match = None
    else:
        match = FRONTMATTER.match(raw_text)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {skill_file}")
    try:
        metadata = yaml.load(match[1], Loader=YAML_LOADER)
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
    for item in sorted(SKILLS_DIR.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        skill_file = item / "SKILL.md" if (item / "SKILL.md").is_file() else item / "SKILL.toon"
        if not skill_file.is_file():
            continue
        metadata = read_metadata(skill_file)
        entries.append({
            "name": item.name,
            "description": metadata["description"].strip(),
            "path": f".agents/skills/{item.name}",
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


def runbook_file(manifest: Path) -> Path:
    """Resolve an opted-in skill's delivery file and reject stale host content."""
    metadata = read_metadata(manifest)
    if "prompt-source" not in metadata:
        return manifest
    if metadata["prompt-source"] != "prompt.toon":
        raise ValueError(f"Unsupported prompt source: {manifest}")
    source = manifest.with_name("prompt.toon")
    content = manifest.read_text(encoding="utf-8")
    if source.read_text(encoding="utf-8") != content[FRONTMATTER.match(content).end():]:
        raise ValueError(f"Host manifest differs from {source}")
    return source
