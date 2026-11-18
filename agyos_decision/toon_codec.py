"""Token-Oriented Object Notation (TOON) Codec for AGYOS.

Provides 40%-60% token savings over JSON for uniform records
injected into LLM prompt contexts by declaring keys once in a
tabular layout.
"""

from __future__ import annotations

import csv
from typing import Any, Dict, List, Optional


def encode_toon(
    records: List[Dict[str, Any]],
    key_name: str = "items",
    compact: bool = False
) -> str:
    """Encode a list of uniform dictionaries into TOON tabular format."""
    if not records:
        return f"{key_name}[0]:\n  - (empty)" if not compact else f"{key_name}[0]:\n-(empty)"

    keys = list(records[0].keys())
    prefix = "- " if compact else "  - "
    output = [f"{key_name}[{len(records)}]:", f"{prefix}{', '.join(keys)}"]

    for r in records:
        row_vals = []
        for k in keys:
            v = r.get(k, "")
            if isinstance(v, list):
                val_str = "|".join(str(item) for item in v)
            else:
                val_str = str(v).replace("\n", " ").strip()
            # Quote if contains comma or double quote
            if "," in val_str or '"' in val_str:
                escaped = val_str.replace('"', '""')
                val_str = f'"{escaped}"'
            row_vals.append(val_str)
        output.append(f"{prefix}{', '.join(row_vals)}")

    return "\n".join(output)


def decode_toon(toon_text: str) -> List[Dict[str, Any]]:
    """Decode TOON formatted text back into a list of dictionaries with batch CSV reader."""
    lines = [line.strip() for line in toon_text.strip().splitlines() if line.strip()]
    if not lines or len(lines) < 2:
        return []

    # Fast row filter for tabular rows starting with '-'
    cleaned_rows = [line.lstrip("- ").strip() for line in lines[1:] if line.startswith("-")]
    if not cleaned_rows:
        return []

    # Single-pass C-level CSV parsing
    reader = csv.reader(cleaned_rows, skipinitialspace=True)
    try:
        keys = next(reader)
    except StopIteration:
        return []

    records = []
    for vals in reader:
        record = {k: (vals[i] if i < len(vals) else "") for i, k in enumerate(keys)}
        records.append(record)

    return records
