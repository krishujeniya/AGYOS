"""Token-Oriented Object Notation (TOON) Codec for AGYOS.

Provides 40%-60% token savings over JSON for uniform records
injected into LLM prompt contexts by declaring keys once in a
tabular layout.
"""

from __future__ import annotations

import csv
import io
import re
from typing import Any, Dict, List, Optional


def encode_toon(records: List[Dict[str, Any]], key_name: str = "items") -> str:
    """Encode a list of uniform dictionaries into TOON tabular format."""
    if not records:
        return f"{key_name}[0]:\n  - (empty)"

    keys = list(records[0].keys())
    output = [f"{key_name}[{len(records)}]:", "  - " + ", ".join(keys)]

    for r in records:
        row_vals = []
        for k in keys:
            v = r.get(k, "")
            if isinstance(v, list):
                val_str = "|".join(str(item) for item in v)
            else:
                val_str = str(v).replace("\n", " ").strip()
            # Quote if contains comma or special character
            if "," in val_str or '"' in val_str:
                escaped = val_str.replace('"', '""')
                val_str = f'"{escaped}"'
            row_vals.append(val_str)
        output.append("  - " + ", ".join(row_vals))

    return "\n".join(output)


def decode_toon(toon_text: str) -> List[Dict[str, Any]]:
    """Decode TOON formatted text back into a list of dictionaries."""
    lines = [line.strip() for line in toon_text.strip().splitlines() if line.strip()]
    if not lines or len(lines) < 2:
        return []

    # Parse header line (keys)
    header_line = lines[1]
    if header_line.startswith("-"):
        header_line = header_line.lstrip("- ").strip()
    reader = csv.reader([header_line], skipinitialspace=True)
    try:
        keys = next(reader)
    except StopIteration:
        return []

    records = []
    for line in lines[2:]:
        if not line.startswith("-"):
            continue
        row_line = line.lstrip("- ").strip()
        row_reader = csv.reader([row_line], skipinitialspace=True)
        try:
            vals = next(row_reader)
            record = {}
            for i, k in enumerate(keys):
                record[k] = vals[i] if i < len(vals) else ""
            records.append(record)
        except StopIteration:
            continue

    return records
