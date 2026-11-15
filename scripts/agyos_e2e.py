#!/usr/bin/env python3
"""AGYOS End-to-End Autonomous Pipeline Engine.

Executes autonomous development lifecycles without manual command input:
1. Ingests natural language prompt and compiles typed TaskContract.
2. Evaluates EVPI clarification decision and records explicit assumptions.
3. Decides specialist skill, assesses complexity score (1-5), and routes model tier.
4. Manages milestone lifecycle gates (Fast-path <= 2 vs 5-Gate >= 3).
5. Executes static sanity checks and transitions gate to VERIFY.
6. Delivers milestone to origin main under locked Krish Ujeniya identity.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agyos_decision.contracts import TaskContract
from agyos_decision.evpi_clarify import ClarificationDecision, evaluate_evpi
from agyos_decision.intent_compiler import compile_intent
from agyos_decision.model_router import DataSensitivity, ModelRouter
from agyos_decision.skills_router import assess_complexity, decide_skill


def validate_prompt(prompt: str) -> str:
    """Validate task prompt boundary conditions."""
    if not isinstance(prompt, str):
        raise ValueError("Prompt must be a string")
    cleaned = prompt.strip()
    if len(cleaned) < 3:
        raise ValueError("Prompt must be at least 3 characters long")
    if len(cleaned) > 3000:
        raise ValueError("Prompt exceeds 3000 character maintainability boundary")
    return cleaned


def slugify_task(prompt: str) -> str:
    """Generate a clean URL/filename-safe slug from a task prompt."""
    tokens = [w for w in re.findall(r"[a-zA-Z0-9]+", prompt.lower()) if len(w) > 2]
    keywords = tokens[:4] if tokens else ["task"]
    return "-".join(keywords)


def get_next_milestone_id(root_dir: Path, slug: str) -> str:
    """Determine the next milestone identifier based on existing checkpoints."""
    checkpoints_dir = root_dir / ".agents" / "state" / "checkpoints"
    max_num = 1
    if checkpoints_dir.exists():
        for p in checkpoints_dir.glob("M*-*.md"):
            match = re.match(r"^M(\d+)-", p.name)
            if match:
                max_num = max(max_num, int(match.group(1)) + 1)
    return f"M{max_num}-{slug}"


def read_state_file(state_file: Path) -> Dict[str, Any]:
    """Read the current state JSON safely."""
    if not state_file.exists():
        return {"project": "AGYOS", "current_gate": "IDLE", "current_milestone": None}
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except Exception:
        return {"project": "AGYOS", "current_gate": "IDLE", "current_milestone": None}


def write_state_file(state_file: Path, data: Dict[str, Any]) -> None:
    """Write the state JSON atomically."""
    tmp = state_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(state_file)


def run_state_gate(target_gate: str, root_dir: Path, mode: str = "normal") -> bool:
    """Transition state gate using the safe state abstraction."""
    cmd = ["bash", "bin/agyos", "gate", target_gate]
    if mode == "fast":
        cmd = ["bash", "bin/agyos", "fast"]
    res = subprocess.run(cmd, cwd=root_dir, capture_output=True, text=True)
    return res.returncode == 0


def plan_task(prompt: str, root_dir: Path = ROOT) -> Dict[str, Any]:
    """Compile task intent, EVPI clarification, skill, complexity, and model routing."""
    clean_prompt = validate_prompt(prompt)
    contract: TaskContract = compile_intent(clean_prompt)
    evpi: ClarificationDecision = evaluate_evpi(clean_prompt, contract)
    skill_decision = decide_skill(clean_prompt)
    complexity, complexity_reason = assess_complexity(clean_prompt)
    model_decision = ModelRouter().route(
        task=clean_prompt,
        complexity=complexity,
        sensitivity=DataSensitivity.INTERNAL,
    )
    slug = slugify_task(clean_prompt)
    milestone_id = get_next_milestone_id(root_dir, slug)

    return {
        "prompt": clean_prompt,
        "milestone_id": milestone_id,
        "task_id": contract.task_id,
        "pod": contract.pod,
        "risk": contract.risk,
        "complexity_score": complexity,
        "complexity_reason": complexity_reason,
        "fast_path": bool(complexity <= 2),
        "skill": {
            "name": skill_decision.get("primary_skill", "unknown"),
            "path": skill_decision.get("primary_path", ""),
            "confidence": round(float(skill_decision.get("confidence", 0.0)), 3),
            "runbook_path": skill_decision.get("runbook_path", ""),
            "execution_invariant": skill_decision.get("execution_invariant", ""),
        },
        "model": {
            "model_id": model_decision.model_id,
            "provider": model_decision.provider.value,
            "thinking_level": model_decision.thinking_level,
            "privacy_boundary": model_decision.privacy_boundary,
        },
        "evpi": {
            "should_ask_question": evpi.should_ask_question,
            "question": evpi.question,
            "assumptions_applied": evpi.assumptions_applied,
            "proceed_immediately": evpi.proceed_immediately,
            "outbox_status": evpi.outbox_status,
        },
        "contract": contract.to_dict(),
    }


def write_checkpoint_header(
    checkpoint_path: Path, milestone_id: str, plan: Dict[str, Any], state: Dict[str, Any]
) -> None:
    """Create or overwrite initial milestone checkpoint header."""
    now = datetime.now(timezone.utc).isoformat()
    skill_versions = json.dumps(state.get("skill_versions", {}), indent=2)
    content = (
        f"# Checkpoint: {milestone_id}\n\n"
        f"Created: {now}\n"
        f"Goal: {plan['prompt']}\n"
        f"Pod: {plan['pod']} | Risk: {plan['risk']} | Complexity: {plan['complexity_score']}\n"
        f"Skill: {plan['skill']['name']} | Model: {plan['model']['model_id']}\n\n"
        f"## Skill-Versions\n```json\n{skill_versions}\n```\n\n"
        f"## Contract\n```json\n{json.dumps(plan['contract'], indent=2)}\n```\n\n"
        f"## Lifecycle History\n"
    )
    checkpoint_path.write_text(content, encoding="utf-8")


def append_checkpoint_entry(checkpoint_path: Path, entry: str) -> None:
    """Append a lifecycle block to the milestone checkpoint."""
    if not checkpoint_path.exists():
        return
    with open(checkpoint_path, "a", encoding="utf-8") as f:
        f.write(f"\n{entry}\n")


def update_current_summary(
    root_dir: Path, milestone_id: str, gate: str, plan: Dict[str, Any]
) -> None:
    """Update CURRENT.md session summary."""
    current_file = root_dir / ".agents" / "state" / "CURRENT.md"
    content = (
        f"# CURRENT (Structured Handoff)\n\n"
        f"## 1. Goal\n\n{plan['prompt']}\n\n"
        f"## 2. Active Milestone\n\n"
        f"- Identifier: `{milestone_id}`\n"
        f"- Active Gate: `{gate}`\n"
        f"- Assigned Pod: `{plan['pod']}` (Risk: `{plan['risk']}`)\n"
        f"- Complexity: `{plan['complexity_score']}` (Fast-path: `{plan['fast_path']}`)\n"
        f"- Primary Specialist Skill: `{plan['skill']['name']}`\n\n"
        f"## 3. Assumptions and Invariants\n\n"
        f"{', '.join(plan['evpi']['assumptions_applied']) if plan['evpi']['assumptions_applied'] else 'No special assumptions.'}\n"
    )
    current_file.write_text(content, encoding="utf-8")


def init_milestone(plan: Dict[str, Any], root_dir: Path = ROOT) -> Dict[str, Any]:
    """Initialize milestone, advance gate sequence, and record checkpoint."""
    state_file = root_dir / ".agents" / "state" / "state.json"
    state = read_state_file(state_file)
    milestone_id = plan["milestone_id"]

    if state.get("current_gate") == "VERIFY":
        run_state_gate("IDLE", root_dir)
        state = read_state_file(state_file)

    if state.get("current_gate") != "IDLE":
        run_state_gate("IDLE", root_dir)

    run_state_gate("UNDERSTAND", root_dir)
    run_state_gate("ANALYZE", root_dir)

    state = read_state_file(state_file)
    state["current_milestone"] = milestone_id
    state["complexity_score"] = plan["complexity_score"]
    state["iteration"] = 1
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    write_state_file(state_file, state)

    if plan["fast_path"]:
        run_state_gate("IMPLEMENT", root_dir, mode="fast")
    else:
        run_state_gate("PLAN", root_dir)
        run_state_gate("IMPLEMENT", root_dir)

    checkpoint_file = root_dir / ".agents" / "state" / "checkpoints" / f"{milestone_id}.md"
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    write_checkpoint_header(checkpoint_file, milestone_id, plan, state)
    append_checkpoint_entry(
        checkpoint_file,
        f"- Gate UNDERSTAND -> ANALYZE -> IMPLEMENT (fast={plan['fast_path']}) initialized.",
    )
    update_current_summary(root_dir, milestone_id, "IMPLEMENT", plan)

    final_state = read_state_file(state_file)
    return {
        "status": "INITIALIZED",
        "milestone_id": milestone_id,
        "current_gate": final_state.get("current_gate"),
        "complexity_score": final_state.get("complexity_score"),
    }


def execute_static_verification(root_dir: Path) -> Tuple[bool, List[str]]:
    """Execute read-only static code and syntax sanity verification."""
    errors = []
    py_res = subprocess.run(
        ["python3", "-m", "compileall", "agyos_decision", "scripts"],
        cwd=root_dir,
        capture_output=True,
        text=True,
    )
    if py_res.returncode != 0:
        errors.append(f"Python compile error: {py_res.stderr.strip()}")

    sh_res = subprocess.run(
        ["bash", "-n", "bin/agyos", "bin/state.sh", "bin/state-validate.sh"],
        cwd=root_dir,
        capture_output=True,
        text=True,
    )
    if sh_res.returncode != 0:
        errors.append(f"Shell syntax error: {sh_res.stderr.strip()}")

    diff_res = subprocess.run(
        ["git", "diff", "--check"],
        cwd=root_dir,
        capture_output=True,
        text=True,
    )
    if diff_res.returncode != 0:
        errors.append(f"Git diff whitespace error: {diff_res.stdout.strip()}")

    return (len(errors) == 0, errors)


def verify_milestone(
    milestone_id: str, plan: Dict[str, Any], root_dir: Path = ROOT
) -> Dict[str, Any]:
    """Transition gate to VERIFY and record deterministic machine verification."""
    state_file = root_dir / ".agents" / "state" / "state.json"
    state = read_state_file(state_file)

    if state.get("current_gate") == "IMPLEMENT":
        run_state_gate("VERIFY", root_dir)

    passed, errors = execute_static_verification(root_dir)
    verdict = "PASS" if passed else "FAIL"

    state = read_state_file(state_file)
    now = datetime.now(timezone.utc).isoformat()
    state["verification"] = {
        "status": verdict,
        "timestamp": now,
        "errors": errors,
        "static_checks": "compileall, bash -n, git diff --check",
    }
    state["last_updated"] = now
    write_state_file(state_file, state)

    checkpoint_file = root_dir / ".agents" / "state" / "checkpoints" / f"{milestone_id}.md"
    append_checkpoint_entry(
        checkpoint_file,
        f"- Gate VERIFY: status={verdict}, timestamp={now}, error_count={len(errors)}",
    )
    update_current_summary(root_dir, milestone_id, "VERIFY", plan)

    return {
        "status": verdict,
        "milestone_id": milestone_id,
        "errors": errors,
    }


def check_git_invariants(root_dir: Path) -> Tuple[bool, str]:
    """Verify single main branch and Krish Ujeniya git identity lock."""
    branch_res = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=root_dir,
        capture_output=True,
        text=True,
    )
    branch = branch_res.stdout.strip()
    if branch != "main":
        return False, f"Branch invariant violation: active branch is '{branch}', must be 'main'"

    name_res = subprocess.run(
        ["git", "config", "user.name"],
        cwd=root_dir,
        capture_output=True,
        text=True,
    )
    user_name = name_res.stdout.strip()
    if user_name != "Krish Ujeniya":
        return False, f"Identity invariant violation: user.name is '{user_name}', must be 'Krish Ujeniya'"

    email_res = subprocess.run(
        ["git", "config", "user.email"],
        cwd=root_dir,
        capture_output=True,
        text=True,
    )
    user_email = email_res.stdout.strip()
    if "krishujeniya" not in user_email:
        return False, f"Identity invariant violation: user.email is '{user_email}'"

    return True, "Git invariants verified"


def deliver_milestone(
    milestone_id: str,
    plan: Dict[str, Any],
    commit_msg: Optional[str] = None,
    auto_push: bool = False,
    watch_ci: bool = False,
    root_dir: Path = ROOT,
) -> Dict[str, Any]:
    """Commit verified changes, push to origin main, and transition gate to IDLE."""
    git_ok, git_reason = check_git_invariants(root_dir)
    if not git_ok:
        return {"status": "BLOCKED", "reason": git_reason}

    status_res = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root_dir,
        capture_output=True,
        text=True,
    )
    has_changes = bool(status_res.stdout.strip())
    committed_sha = None

    if has_changes:
        subprocess.run(["git", "add", "-A"], cwd=root_dir, check=True)
        default_msg = f"feat({milestone_id}): implement {plan['prompt']}"
        final_msg = commit_msg or default_msg
        commit_res = subprocess.run(
            ["git", "commit", "-m", final_msg],
            cwd=root_dir,
            capture_output=True,
            text=True,
        )
        if commit_res.returncode == 0:
            rev_res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root_dir,
                capture_output=True,
                text=True,
            )
            committed_sha = rev_res.stdout.strip()

    pushed = False
    if auto_push and committed_sha:
        push_res = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=root_dir,
            capture_output=True,
            text=True,
        )
        pushed = push_res.returncode == 0

    ci_run_id = None
    if watch_ci and pushed:
        list_res = subprocess.run(
            ["gh", "run", "list", "--limit", "1", "--json", "databaseId,status,conclusion"],
            cwd=root_dir,
            capture_output=True,
            text=True,
        )
        if list_res.returncode == 0:
            try:
                runs = json.loads(list_res.stdout)
                if runs:
                    ci_run_id = runs[0].get("databaseId")
            except Exception:
                pass

    run_state_gate("IDLE", root_dir)
    state_file = root_dir / ".agents" / "state" / "state.json"
    state = read_state_file(state_file)
    state["current_milestone"] = milestone_id
    if committed_sha:
        state["last_known_commit"] = committed_sha
    write_state_file(state_file, state)

    checkpoint_file = root_dir / ".agents" / "state" / "checkpoints" / f"{milestone_id}.md"
    append_checkpoint_entry(
        checkpoint_file,
        f"- Gate IDLE: milestone completed. Commit: {committed_sha or 'none'}, Pushed: {pushed}",
    )
    update_current_summary(root_dir, milestone_id, "IDLE", plan)

    return {
        "status": "DELIVERED",
        "milestone_id": milestone_id,
        "committed_sha": committed_sha,
        "pushed": pushed,
        "ci_run_id": ci_run_id,
        "current_gate": "IDLE",
    }


def run_full_pipeline(
    prompt: str,
    auto_push: bool = False,
    watch_ci: bool = False,
    root_dir: Path = ROOT,
) -> Dict[str, Any]:
    """Execute complete autonomous end-to-end milestone lifecycle."""
    plan = plan_task(prompt, root_dir)
    init_res = init_milestone(plan, root_dir)
    verify_res = verify_milestone(plan["milestone_id"], plan, root_dir)
    deliver_res = deliver_milestone(
        milestone_id=plan["milestone_id"],
        plan=plan,
        auto_push=auto_push,
        watch_ci=watch_ci,
        root_dir=root_dir,
    )
    return {
        "pipeline": "SUCCESS" if verify_res["status"] == "PASS" else "FAILED_VERIFICATION",
        "plan": plan,
        "init": init_res,
        "verify": verify_res,
        "deliver": deliver_res,
    }


def main() -> None:
    """CLI Entrypoint for AGYOS End-to-End Orchestrator."""
    parser = argparse.ArgumentParser(
        prog="agyos-e2e",
        description="AGYOS End-to-End Autonomous Pipeline Engine",
    )
    parser.add_argument("prompt", help="Natural language objective or feature requirement")
    parser.add_argument(
        "--action",
        choices=["plan", "init", "verify", "deliver", "full"],
        default="plan",
        help="Lifecycle action to execute (default: plan)",
    )
    parser.add_argument("--auto-push", action="store_true", help="Push commit to origin main")
    parser.add_argument("--watch-ci", action="store_true", help="Inspect triggered CI run")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    try:
        if args.action == "plan":
            result = plan_task(args.prompt, ROOT)
        elif args.action == "init":
            plan = plan_task(args.prompt, ROOT)
            result = init_milestone(plan, ROOT)
        elif args.action == "verify":
            plan = plan_task(args.prompt, ROOT)
            result = verify_milestone(plan["milestone_id"], plan, ROOT)
        elif args.action == "deliver":
            plan = plan_task(args.prompt, ROOT)
            result = deliver_milestone(
                plan["milestone_id"],
                plan,
                auto_push=args.auto_push,
                watch_ci=args.watch_ci,
                root_dir=ROOT,
            )
        else:
            result = run_full_pipeline(
                args.prompt,
                auto_push=args.auto_push,
                watch_ci=args.watch_ci,
                root_dir=ROOT,
            )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"AGYOS End-to-End [{args.action.upper()}]:")
            print(json.dumps(result, indent=2))
    except Exception as exc:
        err_out = {"error": str(exc), "status": "FAILED"}
        if args.json:
            print(json.dumps(err_out, indent=2))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
