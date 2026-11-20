#!/usr/bin/env python3
"""AGYOS 7-Step Autonomous Cycle CLI Entrypoint.

Executes autonomous development lifecycles across the 7 stages:
Think → Plan → Build → Review → Test → Ship → Reflect
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agyos_decision.cycle import (
    AutonomousCycleStage,
    CycleContext,
    run_autonomous_cycle,
    validate_goal,
)


def format_text_report(ctx: CycleContext) -> str:
    """Format clean, grounded human-readable summary of the autonomous cycle."""
    lines = [
        "============================================================",
        "AGYOS 7-Step Autonomous Lifecycle Execution",
        "============================================================",
        f"Goal:              {ctx.goal}",
        f"Milestone ID:      {ctx.milestone_id or 'Pending'}",
        f"Assigned Role:     {ctx.role_title} ({ctx.role_id})",
        f"Governing Pod:     {ctx.pod} (Risk: {ctx.risk}, Complexity: {ctx.complexity}/5)",
        f"Primary Skill:     {ctx.skill_name}",
        f"Target Model:      {ctx.model_id} [Thinking: {ctx.thinking_level}]",
        "------------------------------------------------------------",
        "Stage Progression:",
    ]

    for stage in AutonomousCycleStage:
        status = ctx.stage_statuses.get(stage.value, "PENDING")
        marker = f"[{status}]"
        detail = ""
        if stage == AutonomousCycleStage.THINK:
            detail = f"Role: {ctx.role_id}, Skill: {ctx.skill_name}"
        elif stage == AutonomousCycleStage.PLAN:
            detail = f"{len(ctx.tasks)} tasks planned, checkpoint created"
        elif stage == AutonomousCycleStage.BUILD:
            detail = f"{len(ctx.build_files)} files tracked, invariants verified"
        elif stage == AutonomousCycleStage.REVIEW:
            detail = f"Verdict: {ctx.review_verdict} ({len(ctx.review_findings)} findings)"
        elif stage == AutonomousCycleStage.TEST:
            detail = f"Verdict: {ctx.test_verdict} ({len(ctx.test_errors)} errors)"
        elif stage == AutonomousCycleStage.SHIP:
            detail = f"{ctx.delivery_status} (Commit: {ctx.commit_sha or 'none'})"
        elif stage == AutonomousCycleStage.REFLECT:
            detail = f"Milestone complete, AI_HANDOFF updated"
        lines.append(f"  {stage.value:<8} {marker:<9} {detail}")

    lines.extend([
        "------------------------------------------------------------",
        f"Delivery Status:   {ctx.delivery_status}",
        f"Handoff Logged:    {'Yes' if ctx.handoff_entry else 'No'}",
        "============================================================",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="agyos-cycle",
        description="AGYOS 7-Step Autonomous Cycle Engine (Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect)",
    )
    parser.add_argument("goal", help="Natural language objective or feature requirement")
    parser.add_argument(
        "--step",
        "--stage",
        dest="stage",
        choices=["think", "plan", "build", "review", "test", "ship", "reflect"],
        default=None,
        help="Execute up to a specific stage (default: execute all 7 stages)",
    )
    parser.add_argument(
        "--auto-push",
        action="store_true",
        help="Automatically push commit to origin main when static verification passes",
    )
    parser.add_argument(
        "--commit-msg",
        default=None,
        help="Optional custom conventional commit message",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output full execution context in JSON format",
    )
    args = parser.parse_args()

    try:
        clean_goal = validate_goal(args.goal)
        ctx = run_autonomous_cycle(
            goal=clean_goal,
            root_dir=ROOT,
            auto_push=args.auto_push,
            stop_at_stage=args.stage,
            commit_msg=args.commit_msg,
        )

        if args.json:
            print(json.dumps(ctx.to_dict(), indent=2))
        else:
            print(format_text_report(ctx))

    except Exception as exc:
        err_dict = {"status": "FAILED", "error": str(exc)}
        if args.json:
            print(json.dumps(err_dict, indent=2))
        else:
            print(f"Error during autonomous cycle: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
