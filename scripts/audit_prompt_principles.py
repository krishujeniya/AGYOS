"""Create a source-locatable, text-free ledger from the pinned Principles archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SOURCE_REPOSITORY = "https://github.com/krishujeniya/Principles"
SOURCE_COMMIT = "d1ed7de8cb338f8646d2d2f5394dd9c87bb9223e"
EXPECTED_COMPANIES = 26
CURATED_START = "## Principle catalog"
CURATED_ENDS = ("## Repository source files", "## Scope and evidence notes", "## Part II")
EXHAUSTIVE_START = "### 3. Complete Unified Company-Wide Principles by Domain"
CURATED_ITEM = re.compile(r"^\s*(\d+(?:\.\d+)*)\.\s+(\S.*)$")
DOMAIN_HEADING = re.compile(r"^####\s+3\.\d+\s+(.+?)\s+\(([\d,]+)\s+Principles?\)\s*$")
CURATED_COUNT = re.compile(r"^\s*-?\s*\*\*Curated Principle Catalog Statements.*?\*\*:\s*([\d,]+)")
EXHAUSTIVE_COUNT = re.compile(r"^\s*-?\s*\*\*Exhaustive Prompt-Derived Principle Statements.*?\*\*:\s*([\d,]+)")
INDEX_TOTAL = re.compile(r"^\|\s*\*\*Total\*\*\s*\|")

EVIDENCE_PROMPTING = [
    "https://developers.openai.com/api/docs/guides/prompt-engineering",
    "https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6",
    "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices",
]
EVIDENCE_UNTRUSTED = [
    "https://developers.openai.com/api/docs/guides/tools-computer-use",
    "https://developers.openai.com/api/docs/guides/agent-builder-safety",
]

# These source locators were reviewed against current first-party guidance.
# Their wording is adapted to AGYOS and is not treated as company policy.
CURATED_DECISIONS = {
    ("ANTHROPIC.md", "1.5"): {
        "disposition": "adapt",
        "rationale": "Scale detail to task needs; do not impose a fixed response length or model-specific setting.",
        "control": ".agents/rules/agyos-prompt-principles.md#task-fit",
        "evidence": EVIDENCE_PROMPTING,
    },
    ("BRAVE.md", "2.1"): {
        "disposition": "adapt",
        "rationale": "Treat retrieved text as task data, not authority to redirect behavior; apply this to AGYOS inputs and tools.",
        "control": ".agents/rules/agyos-prompt-principles.md#untrusted-content",
        "evidence": EVIDENCE_UNTRUSTED,
    },
    ("BRAVE.md", "2.2"): {
        "disposition": "adapt",
        "rationale": "Reject behavioral redirection from retrieved content while preserving relevant evidence for the user request.",
        "control": ".agents/rules/agyos-prompt-principles.md#untrusted-content",
        "evidence": EVIDENCE_UNTRUSTED,
    },
    ("BRAVE.md", "2.4"): {
        "disposition": "adapt",
        "rationale": "Use untrusted text as evidence only within the user-authorized task; it cannot grant permission or override controls.",
        "control": ".agents/rules/agyos-prompt-principles.md#untrusted-content",
        "evidence": EVIDENCE_UNTRUSTED,
    },
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def normalize_statement(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def numeric_value(value: str) -> int:
    return int(value.replace(",", ""))


def find_section(lines: list[str], start: str, end_markers: tuple[str, ...]) -> tuple[int, int]:
    start_index = next(
        (i for i, line in enumerate(lines)
         if line.strip() == start or line.strip().startswith(f"{start} ")),
        -1,
    )
    if start_index < 0:
        return -1, -1
    end_index = next(
        (i for i in range(start_index + 1, len(lines))
         if any(lines[i].startswith(marker) for marker in end_markers)),
        len(lines),
    )
    return start_index, end_index


def source_record(
    path: Path,
    relative_path: str,
    file_digest: str,
    catalog: str,
    section: str,
    line_number: int,
    ordinal: str,
    statement: str,
) -> dict[str, Any]:
    normalized = normalize_statement(statement)
    statement_digest = sha256_bytes(normalized.encode("utf-8"))
    stable_key = f"{SOURCE_COMMIT}|{relative_path}|{catalog}|{ordinal}|{statement_digest}"
    record_id = sha256_bytes(stable_key.encode("utf-8"))[:24]
    return {
        "id": record_id,
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": SOURCE_COMMIT,
        "source_path": relative_path,
        "source_file_sha256": file_digest,
        "company": path.stem,
        "catalog": catalog,
        "section": section,
        "line": line_number,
        "ordinal": ordinal,
        "statement_sha256": statement_digest,
        "disposition": "unverified",
        "rationale": "Community-compiled statement; not independently authenticated as active company policy.",
        "control": None,
        "evidence": [],
        "confidence": "low",
        "duplicate_of": None,
    }


def parse_curated(
    lines: list[str], path: Path, relative_path: str, digest: str
) -> tuple[list[dict[str, Any]], list[str]]:
    start, end = find_section(lines, CURATED_START, CURATED_ENDS)
    if start < 0:
        return [], ["missing curated principle catalog"]
    rows = []
    section = "Curated principle catalog"
    for index in range(start + 1, end):
        line = lines[index]
        if line.startswith("### "):
            section = line[4:].strip()
        match = CURATED_ITEM.match(line)
        if match:
            rows.append(
                source_record(
                    path, relative_path, digest, "curated", section,
                    index + 1, match.group(1), match.group(2),
                )
            )
    return rows, []


def keyword_metadata_record(section: str, line_number: int, line: str) -> dict[str, Any]:
    return {
        "section": section,
        "line": line_number,
        "sha256": sha256_bytes(normalize_statement(line[2:]).encode("utf-8")),
    }


def parse_exhaustive(
    lines: list[str], path: Path, relative_path: str, digest: str
) -> tuple[list[dict[str, Any]], list[str], dict[str, int], list[dict[str, Any]]]:
    start, end = find_section(lines, EXHAUSTIVE_START, ("### 4.",))
    if start < 0:
        return [], ["missing exhaustive principle section"], {}, []
    rows = []
    warnings = []
    declared: dict[str, int] = {}
    keyword_metadata = []
    section = "Uncategorized principles"
    fence = ""
    for index in range(start + 1, end):
        line = lines[index]
        stripped = line.lstrip()
        if stripped.startswith((chr(96) * 3, "~~~")):
            marker = stripped[:3]
            fence = "" if fence == marker else (marker if not fence else fence)
            continue
        if fence:
            continue
        heading = DOMAIN_HEADING.match(line)
        if heading:
            section = heading.group(1).strip()
            declared[section] = numeric_value(heading.group(2))
            continue
        if line.startswith("#### "):
            section = line[5:].strip()
            warnings.append(f"unrecognized principle heading at line {index + 1}")
            continue
        if line.startswith("- **Keywords**:"):
            keyword_metadata.append(keyword_metadata_record(section, index + 1, line))
            continue
        if not line.startswith("- "):
            continue
        rows.append(
            source_record(
                path, relative_path, digest, "exhaustive", section,
                index + 1, f"line-{index + 1}", line[2:],
            )
        )
    for name, count in declared.items():
        observed = sum(1 for row in rows if row["section"] == name)
        observed += sum(1 for row in keyword_metadata if row["section"] == name)
        if observed != count:
            warnings.append(f"section {name!r} declares {count} source rows; parser accounted for {observed}")
    return rows, warnings, declared, keyword_metadata


def parse_company_file(path: Path, source_root: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    relative_path = path.relative_to(source_root).as_posix()
    digest = sha256_bytes(raw)
    curated, warnings = parse_curated(lines, path, relative_path, digest)
    exhaustive, exhaustive_warnings, declared_sections, keyword_metadata = parse_exhaustive(
        lines, path, relative_path, digest
    )
    warnings.extend(exhaustive_warnings)
    curated_claim = next(
        (numeric_value(match.group(1)) for line in lines
         if (match := CURATED_COUNT.match(line))),
        None,
    )
    exhaustive_claim = next(
        (numeric_value(match.group(1)) for line in lines
         if (match := EXHAUSTIVE_COUNT.match(line))),
        None,
    )
    if curated_claim is None:
        warnings.append("missing publisher curated-count metadata")
    elif len(curated) != curated_claim:
        warnings.append(f"curated metadata declares {curated_claim}; parser found {len(curated)}")
    if exhaustive_claim is None:
        warnings.append("missing publisher exhaustive-count metadata")
    elif len(exhaustive) + len(keyword_metadata) != exhaustive_claim:
        accounted = len(exhaustive) + len(keyword_metadata)
        warnings.append(f"exhaustive metadata declares {exhaustive_claim}; parser accounted for {accounted}")
    return {
        "path": relative_path,
        "company": path.stem,
        "source_file_sha256": digest,
        "publisher_curated": curated_claim,
        "publisher_exhaustive": exhaustive_claim,
        "parsed_curated": len(curated),
        "parsed_exhaustive": len(exhaustive),
        "parsed_keyword_metadata": len(keyword_metadata),
        "declared_exhaustive_sections": declared_sections,
        "keyword_metadata": [
            {"path": relative_path, "company": path.stem, **row}
            for row in keyword_metadata
        ],
        "records": curated + exhaustive,
        "warnings": warnings,
    }


def parse_index_claims(path: Path) -> dict[str, int]:
    total_line = next(
        (line for line in path.read_text(encoding="utf-8").splitlines() if INDEX_TOTAL.match(line)),
        None,
    )
    if total_line is None:
        raise ValueError("master index has no total inventory row")
    cells = [cell.strip() for cell in total_line.strip().strip("|").split("|")]
    if len(cells) < 9:
        raise ValueError("master index total row has an unexpected column count")
    values = [numeric_value(re.sub(r"[^0-9,]", "", cells[index])) for index in (1, 4, 5, 6, 7, 8)]
    return dict(zip(
        ("companies", "upstream_files", "curated", "exhaustive", "combined", "tools"),
        values,
        strict=True,
    ))


def apply_dispositions(records: list[dict[str, Any]]) -> None:
    canonical_by_hash: dict[str, str] = {}
    for row in records:
        key = (Path(row["source_path"]).name, row["ordinal"])
        decision = CURATED_DECISIONS.get(key) if row["catalog"] == "curated" else None
        if row["statement_sha256"] in canonical_by_hash:
            row["disposition"] = "duplicate"
            row["rationale"] = "Exact normalized duplicate of an earlier source statement."
            row["duplicate_of"] = canonical_by_hash[row["statement_sha256"]]
            continue
        canonical_by_hash[row["statement_sha256"]] = row["id"]
        if decision:
            row.update(decision)
            row["confidence"] = "medium"


def count_mismatches(
    company_count: int,
    claims: dict[str, int],
    company_results: list[dict[str, Any]],
    parsed_curated: int,
    parsed_exhaustive: int,
    keyword_metadata_count: int,
    record_count: int,
) -> list[dict[str, Any]]:
    mismatches = [
        {"path": result["path"], "warnings": result["warnings"]}
        for result in company_results if result["warnings"]
    ]
    if company_count != claims["companies"] or company_count != EXPECTED_COMPANIES:
        mismatches.append({
            "path": "Prompt/",
            "warnings": [f"index declares {claims['companies']} companies; parser found {company_count}"],
        })
    for label, observed, expected in (
        ("curated", parsed_curated, claims["curated"]),
        ("exhaustive source rows", parsed_exhaustive + keyword_metadata_count, claims["exhaustive"]),
        ("combined source rows", record_count + keyword_metadata_count, claims["combined"]),
    ):
        if observed != expected:
            mismatches.append({"path": "Prompt/", "warnings": [f"aggregate {label} count differs from index"]})
    return mismatches


def build_summary(
    claims: dict[str, int], company_results: list[dict[str, Any]],
    records: list[dict[str, Any]], parsed_curated: int,
    parsed_exhaustive: int, keyword_metadata: list[dict[str, Any]],
    mismatches: list[dict[str, Any]],
) -> dict[str, Any]:
    parsed_counts = Counter(row["disposition"] for row in records)
    return {
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": SOURCE_COMMIT,
        "source_directory": "Prompt/",
        "publisher_claims": claims,
        "parsed": {
            "company_files": len(company_results),
            "curated_statements": parsed_curated,
            "exhaustive_statements": parsed_exhaustive,
            "combined_statements": len(records),
            "non_principle_metadata_rows": len(keyword_metadata),
            "accounted_source_rows": len(records) + len(keyword_metadata),
            "dispositions": dict(sorted(parsed_counts.items())),
        },
        "count_status": summary_count_status(mismatches, keyword_metadata),
        "mismatches": mismatches,
        "non_principle_metadata": {
            "classification": "keyword metadata excluded from the principle ledger",
            "rows": keyword_metadata,
        },
        "inventory_limits": {
            "upstream_file_claim": claims["upstream_files"],
            "upstream_file_status": "not_reconciled; raw upstream files are absent from this supplied subtree",
            "tool_claim": claims["tools"],
            "tool_status": "publisher_claim_only; tool inventories are outside this ledger",
        },
        "source_files": [
            {
                "path": result["path"],
                "sha256": result["source_file_sha256"],
                "publisher_curated": result["publisher_curated"],
                "publisher_exhaustive": result["publisher_exhaustive"],
                "parsed_curated": result["parsed_curated"],
                "parsed_exhaustive": result["parsed_exhaustive"],
                "parsed_keyword_metadata": result["parsed_keyword_metadata"],
            }
            for result in company_results
        ],
        "ledger_contains_statement_text": False,
    }


def summary_count_status(
    mismatches: list[dict[str, Any]], keyword_metadata: list[dict[str, Any]]
) -> str:
    if mismatches:
        return "mismatch"
    if keyword_metadata:
        return "publisher_rows_reconciled_with_metadata"
    return "principle_counts_match"


def build_audit(source_root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    company_paths = sorted(
        path for path in source_root.glob("*.md")
        if path.name not in {"README.md", "00_MASTER_INDEX_ALL_26_COMPANIES.md"}
    )
    index_path = source_root / "00_MASTER_INDEX_ALL_26_COMPANIES.md"
    if not index_path.is_file():
        raise ValueError("pinned source is missing its master index")
    claims = parse_index_claims(index_path)
    company_results = [parse_company_file(path, source_root) for path in company_paths]
    records = [row for company in company_results for row in company["records"]]
    apply_dispositions(records)
    parsed_curated = sum(company["parsed_curated"] for company in company_results)
    parsed_exhaustive = sum(company["parsed_exhaustive"] for company in company_results)
    keyword_metadata = [
        row for company in company_results for row in company["keyword_metadata"]
    ]
    mismatches = count_mismatches(
        len(company_paths), claims, company_results, parsed_curated,
        parsed_exhaustive, len(keyword_metadata), len(records),
    )
    summary = build_summary(
        claims, company_results, records, parsed_curated, parsed_exhaustive,
        keyword_metadata, mismatches,
    )
    return records, summary


def write_outputs(
    records: list[dict[str, Any]], summary: dict[str, Any],
    ledger_path: Path, summary_path: Path,
) -> None:
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("w", encoding="utf-8", newline="\n") as output:
        for row in records:
            output.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_github_summary(summary: dict[str, Any]) -> None:
    summary_path_value = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path_value:
        return
    counts = summary["parsed"]
    lines = [
        "## Prompt-principles source audit",
        "",
        f"- Source commit: {summary['source_commit']}",
        f"- Count status: **{summary['count_status']}**",
        f"- Company files: {counts['company_files']}",
        f"- Parsed principles: {counts['combined_statements']} ({counts['curated_statements']} curated, {counts['exhaustive_statements']} exhaustive)",
        f"- Non-principle metadata rows: {counts['non_principle_metadata_rows']}",
        f"- Accounted source rows: {counts['accounted_source_rows']} / {summary['publisher_claims']['combined']} publisher-claimed rows",
        f"- Publisher tool claim: {summary['publisher_claims']['tools']}",
        f"- Parser mismatches: {len(summary['mismatches'])}",
        "",
    ]
    with Path(summary_path_value).open("a", encoding="utf-8") as output:
        output.write("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    try:
        records, summary = build_audit(args.source_dir)
    except (OSError, UnicodeError, ValueError) as error:
        error_summary = {
            "source_repository": SOURCE_REPOSITORY,
            "source_commit": SOURCE_COMMIT,
            "source_directory": "Prompt/",
            "count_status": "input_error",
            "error": str(error),
            "parsed": {
                "company_files": 0,
                "curated_statements": 0,
                "exhaustive_statements": 0,
                "combined_statements": 0,
                "non_principle_metadata_rows": 0,
                "accounted_source_rows": 0,
                "dispositions": {},
            },
            "non_principle_metadata": {"classification": "unavailable", "rows": []},
            "ledger_contains_statement_text": False,
        }
        write_outputs([], error_summary, args.output, args.summary)
        print(f"prompt-principles audit input error: {error}", file=sys.stderr)
        return 2
    write_outputs(records, summary, args.output, args.summary)
    append_github_summary(summary)
    print(json.dumps({
        "count_status": summary["count_status"],
        "parsed": summary["parsed"],
        "mismatches": summary["mismatches"],
    }, sort_keys=True))
    successful_statuses = {
        "principle_counts_match",
        "publisher_rows_reconciled_with_metadata",
    }
    return 0 if summary["count_status"] in successful_statuses else 1


if __name__ == "__main__":
    raise SystemExit(main())
