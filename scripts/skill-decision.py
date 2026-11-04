#!/usr/bin/env python3
"""AGYOS Decision Engine CLI — Autonomous Skill Routing & Complexity Gate.

Usage:
  python3 scripts/agyos-decision.py "<task description>" [--json]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agyos_decision.skills_router import decide_skill


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print("Usage: agyos-decision.py \"<task description>\" [--json]", file=sys.stderr)
        return 1

    query = " ".join(args).strip()
    result = decide_skill(query)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
        return 0

    classification = result["classification"]
    domain = classification["domain"]
    confidence = classification["confidence"]
    complexity = classification["complexity_score"]
    guidance = classification["workflow_guidance"]
    fast_path = classification["fast_path_eligible"]

    print("============================================================")
    print("AGYOS Autonomous Decision Engine")
    print("============================================================")
    print(f"Task: {query}")
    print(f"Domain: {domain.upper()} (calibrated confidence: {confidence:.2f})")
    print(f"Complexity: {complexity}/5 — {guidance}")
    if fast_path:
        print("Gate Routing: Fast-path eligible (skip Gates 1-3 direct to IMPLEMENT)")
    else:
        print("Gate Routing: Full 5-Gate standard workflow (UNDERSTAND -> ANALYZE -> PLAN -> IMPLEMENT -> VERIFY)")

    print(f"\nRecommended Primary Skill:")
    print(f"  Name: {result['primary_skill']}")
    print(f"  Path: {result['primary_path']}")
    print(f"  Confidence: {result['confidence'] * 100:.1f}%")

    candidates = result.get("candidates", [])
    if len(candidates) > 1:
        print("\nCandidate Rankings:")
        for cand in candidates:
            star = "*" if cand["name"] == result["primary_skill"] else " "
            desc = cand.get("description", "")[:70]
            print(f"  {star} #{cand['rank']} {cand['name']:<30} (score: {cand['score']:>5.1f}, conf: {cand['confidence']*100:>4.1f}%) — {desc}...")

    print("\nNext Action: Ingest skill runbook before mutating code:")
    print(f"  cat {result['primary_path']}/SKILL.md")
    print("============================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
