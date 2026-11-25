"""Shared, strict skill discovery metadata for runtime and generated indexes."""

import base64
import json
from pathlib import Path
import re
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|$)", re.DOTALL)
YAML_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def decode_toon_document(path: Path) -> str:
    """Decode a two-field TOON document wrapper (text/header/archive) or return raw text."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith('mode: "'):
        return raw
    match = re.search(r'^(text|header|archive): ("(?:[^"\\]|\\.)*")', raw, re.M)
    if not match:
        return raw
    field, encoded = match.group(1), match.group(2)
    value = json.loads(encoded)
    if field == "archive":
        return base64.b64decode(value).decode("utf-8")
    if field == "header":
        prompt_file = path.with_name("prompt.toon")
        if prompt_file.is_file():
            return value + prompt_file.read_text(encoding="utf-8")
    return value


def read_runbook_text(manifest: Path) -> str:
    """Return the active runbook text for a TOON or legacy skill manifest."""
    source = runbook_file(manifest)
    if source.name == "prompt.toon":
        return source.read_text(encoding="utf-8")
    return decode_toon_document(source)


def read_metadata(skill_file: Path) -> dict[str, Any]:
    """Read metadata without accepting a body or a path as a skill identity."""
    raw_text = ""
    if skill_file.is_file():
        raw_text = decode_toon_document(skill_file)
    elif skill_file.name == "SKILL.md":
        toon_file = skill_file.with_name("SKILL.toon")
        if toon_file.is_file():
            raw_text = decode_toon_document(toon_file)
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


def resolve_skill_dir(name: str, skills_dir: Path | None = None) -> Path | None:
    """Resolve a skill directory under role-based builtin/skills/<role-id>/<name>/."""
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", name):
        return None
    root = (skills_dir or SKILLS_DIR).resolve()
    if skills_dir is None:
        from .roles import get_primary_role_for_skill
        role_id = get_primary_role_for_skill(name)
        if role_id:
            candidate = (root / role_id / name).resolve()
            if candidate.is_dir() and candidate.is_relative_to(root):
                return candidate
    for match in root.glob(f"*/{name}"):
        resolved = match.resolve()
        if resolved.is_dir() and resolved.is_relative_to(root):
            return resolved
    direct = (root / name).resolve()
    if direct.is_dir() and direct.is_relative_to(root):
        return direct
    return None


def physical_catalog() -> list[dict[str, Any]]:
    """Index every physical role-based runbook; invalid metadata is an actionable error."""
    entries = []
    for role_dir in sorted(SKILLS_DIR.iterdir()):
        if not role_dir.is_dir() or role_dir.name.startswith("."):
            continue
        for item in sorted(role_dir.iterdir()):
            if not item.is_dir() or item.name.startswith("."):
                continue
            skill_file = item / "SKILL.toon" if (item / "SKILL.toon").is_file() else item / "SKILL.md"
            if not skill_file.is_file():
                continue
            metadata = read_metadata(skill_file)
            entries.append({
                "name": item.name,
                "role": role_dir.name,
                "description": metadata["description"].strip(),
                "path": f"skills/{role_dir.name}/{item.name}",
                "tier": 2,
            })
    return entries


def canonical_entry(entry: Any) -> dict[str, Any] | None:
    """Constrain index references to physical runbooks under this checkout."""
    if not isinstance(entry, dict):
        return None
    name = entry.get("id") or entry.get("name")
    skill_dir = resolve_skill_dir(name) if isinstance(name, str) else None
    if skill_dir is None:
        return None
    file = skill_dir / "SKILL.toon" if (skill_dir / "SKILL.toon").is_file() else skill_dir / "SKILL.md"
    if not file.is_file():
        return None
    description = entry.get("description", "")
    category = entry.get("category") or entry.get("module") or ""
    if not isinstance(description, str) or not description.strip() or not isinstance(category, str):
        return None
    role_id = skill_dir.parent.name
    return {
        "name": name,
        "role": role_id,
        "description": description,
        "path": f"skills/{role_id}/{name}",
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
    if manifest.name == "SKILL.toon":
        return source
    content = manifest.read_text(encoding="utf-8")
    if source.read_text(encoding="utf-8") != content[FRONTMATTER.match(content).end():]:
        raise ValueError(f"Host manifest differs from {source}")
    return source
