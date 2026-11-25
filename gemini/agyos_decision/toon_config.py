"""AGYOS TOON Configuration & Manifest Parser/Serializer.

Provides deterministic parsing and encoding of configuration files and tabular
manifests in Token-Oriented Object Notation (TOON) format.
Replaces JSON configuration storage with token-efficient, human-readable TOON.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .toon_codec import encode_toon, decode_toon


def _parse_scalar(val: str) -> Any:
    """Parse a scalar string into bool, int, float, or unquoted string."""
    val = val.strip()
    if not val:
        return ""
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.lower() in ("null", "none"):
        return None
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        try:
            return json.loads(val)
        except Exception:
            return val[1:-1]
    if re.fullmatch(r"-?\d+", val):
        return int(val)
    if re.fullmatch(r"-?\d+\.\d+", val):
        return float(val)
    return val


def _format_scalar_value(v: Any) -> str:
    """Format scalar python value into canonical TOON string representation."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        if (
            not v
            or any(c in v for c in (':', '"', '\n', '\r', '\t', '#', '[', ']', '{', '}'))
            or v.lower() in ('true', 'false', 'null')
            or re.fullmatch(r"-?\d+(\.\d+)?", v)
        ):
            return json.dumps(v, ensure_ascii=False)
        return v
    return json.dumps(v, ensure_ascii=False)


def _dump_toon_lines(data: Dict[str, Any], indent_level: int = 0) -> List[str]:
    """Recursively serialize nested dict/list structures to indented TOON lines."""
    lines: List[str] = []
    prefix = "  " * indent_level

    for k, v in data.items():
        if isinstance(v, dict):
            lines.append(f"{prefix}{k}:")
            lines.extend(_dump_toon_lines(v, indent_level + 1))
        elif isinstance(v, list):
            if not v:
                lines.append(f"{prefix}{k}[0]:\n{prefix}  - (empty)")
            elif isinstance(v[0], dict):
                tabular = encode_toon(v, key_name=k)
                for line in tabular.splitlines():
                    lines.append(f"{prefix}{line}")
            else:
                val_strs = [_format_scalar_value(item) for item in v]
                lines.append(f"{prefix}{k}[{len(v)}]: {', '.join(val_strs)}")
        else:
            lines.append(f"{prefix}{k}: {_format_scalar_value(v)}")
    return lines


def _parse_toon_lines(lines: List[str], idx: int = 0, base_indent: int = 0) -> tuple[Dict[str, Any], int]:
    """Recursively parse indented TOON lines into a Python dictionary."""
    result: Dict[str, Any] = {}
    num_lines = len(lines)

    while idx < num_lines:
        line = lines[idx]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            idx += 1
            continue

        indent = len(line) - len(line.lstrip(" "))
        if indent < base_indent:
            break

        # Check for tabular array header: name[count]: or name[count]{cols}:
        array_match = re.match(r"^([a-zA-Z0-9_\-\.]+)(?:\[(\d+)\])?(?:\{([^}]+)\})?:\s*(.*)$", stripped)
        if array_match and (
            array_match.group(2) is not None
            or array_match.group(3) is not None
            or (idx + 1 < num_lines and lines[idx + 1].strip().startswith("-"))
        ):
            key = array_match.group(1)
            inline_tail = array_match.group(4).strip() if array_match.group(4) else ""

            if inline_tail and not inline_tail.startswith("-"):
                items = [_parse_scalar(x.strip()) for x in inline_tail.split(",") if x.strip()]
                result[key] = items
                idx += 1
                continue

            array_lines = [stripped]
            idx += 1
            while idx < num_lines:
                nl = lines[idx]
                ns = nl.strip()
                if not ns:
                    idx += 1
                    continue
                n_indent = len(nl) - len(nl.lstrip(" "))
                if n_indent > indent or ns.startswith("-"):
                    array_lines.append(nl)
                    idx += 1
                else:
                    break

            tabular_text = "\n".join(array_lines)
            records = decode_toon(tabular_text)
            if records:
                result[key] = records
            else:
                bullet_items = []
                for al in array_lines[1:]:
                    al_strip = al.strip()
                    if al_strip.startswith("- "):
                        bullet_items.append(_parse_scalar(al_strip[2:]))
                result[key] = bullet_items
            continue

        if ":" in stripped:
            key, _, val_str = stripped.partition(":")
            key = key.strip()
            val_str = val_str.strip()

            if not val_str:
                # Nested block
                child_dict, next_idx = _parse_toon_lines(lines, idx + 1, base_indent=indent + 2)
                result[key] = child_dict
                idx = next_idx
                continue
            else:
                result[key] = _parse_scalar(val_str)
                idx += 1
                continue

        idx += 1

    return result, idx


def load_toon_config(path: Union[Path, str]) -> Any:
    """Parse a TOON key-value config or mixed schema file into a Python dictionary or list.

    Supports:
    - Key-value scalars: `key: value`
    - Tabular arrays with explicit counts: `items[N]:\n  - col1, col2\n  - val1, val2`
    - Simple lists: `items[N]: a, b, c` or `items[N]:\n  - a\n  - b`
    - Nested key-value blocks with 2-space indentation
    """
    file_path = Path(path)
    if not file_path.is_file():
        # Fallback to .json if .toon not found during migration
        json_fallback = file_path.with_suffix(".json")
        if json_fallback.is_file():
            return json.loads(json_fallback.read_text(encoding="utf-8"))
        raise FileNotFoundError(f"Config file not found: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    parsed, _ = _parse_toon_lines(lines, 0, 0)
    if not parsed and lines:
        records = decode_toon(text)
        if records:
            return records
    return parsed


def dump_toon_config(
    data: Union[Dict[str, Any], List[Any]],
    path: Union[Path, str],
    key_name: str = "items",
) -> None:
    """Serialize a Python dictionary or list to a TOON configuration file."""
    if isinstance(data, list):
        if not data:
            Path(path).write_text(f"{key_name}[0]:\n  - (empty)\n", encoding="utf-8")
            return
        if isinstance(data[0], dict):
            dump_toon_manifest(data, path, key_name=key_name)
            return
        val_strs = [_format_scalar_value(x) for x in data]
        Path(path).write_text(f"{key_name}[{len(data)}]: {', '.join(val_strs)}\n", encoding="utf-8")
        return

    lines = _dump_toon_lines(data, indent_level=0)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_toon_manifest(path: Union[Path, str]) -> List[Dict[str, Any]]:
    """Parse a TOON tabular manifest into a list of uniform record dictionaries."""
    file_path = Path(path)
    if not file_path.is_file():
        json_fallback = file_path.with_suffix(".json")
        if json_fallback.is_file():
            raw = json.loads(json_fallback.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                return raw
            if isinstance(raw, dict):
                for key in ("skills", "tier1_skills", "items", "entries"):
                    if key in raw and isinstance(raw[key], list):
                        return raw[key]
        raise FileNotFoundError(f"Manifest file not found: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    records = decode_toon(text)
    if records:
        return records

    # If decode_toon didn't match directly, parse with load_toon_config and extract main array
    cfg = load_toon_config(file_path)
    for key in ("skills", "tier1_skills", "items", "entries"):
        if key in cfg and isinstance(cfg[key], list):
            return cfg[key]
    return []


def dump_toon_manifest(
    records: List[Dict[str, Any]],
    path: Union[Path, str],
    key_name: str = "skills",
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Encode uniform records into a TOON manifest file with optional top-level header metadata."""
    lines: List[str] = []
    if metadata:
        for k, v in metadata.items():
            val_str = json.dumps(v, ensure_ascii=False) if isinstance(v, str) else str(v)
            lines.append(f"{k}: {val_str}")

    tabular = encode_toon(records, key_name=key_name)
    lines.append(tabular)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
