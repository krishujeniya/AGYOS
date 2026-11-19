---
name: agyos-preflight
description: Inspect planned deliverables before implementation and report whether they are unbuilt, partial, or already built.
allowed-tools:
- view_file
- grep_search
prompt-source: prompt.toon
---
skill: "agyos-preflight"
sections[13]:
  - "\n"
  - "# agyos-preflight\n\nYou run this skill before IMPLEMENT begins on any milestone. Your job is to determine whether the planned work already exists, partially exists, or needs to be built from scratch. You return one of three verdicts: **UNBUILT**, **PARTIAL**, or **BUILT**.\n\n"
  - "## When to run\n\nAfter the PLAN gate is approved and before IMPLEMENT starts. The orchestrator calls you here.\n\n"
  - "## Inputs you need\n\n1. The **milestone goal** — what is being built (from the checkpoint or CURRENT.md).\n2. The **planned deliverables** — the specific files, functions, or components the plan says to create (from the Implementation Plan artifact).\n\n"
  - "## How to check\n\nFor each planned deliverable, run these checks in order:\n\n"
  - "### Step 0 — Check for out-of-band drift\n\n```bash\n# Has a human edited files since ANCHOR last ran?\nbash bin/drift-check.sh\n```\n\nIf drift is detected (script returns non-zero), you MUST read the drifted files to understand what changed before proceeding with your other checks. Do not ignore drift.\n\n"
  - "### Step 1 — Check state for prior completion\n\n```bash\n# Has this milestone already been completed?\ngrep -l \"COMPLETE\\|APPROVE\" .agents/state/checkpoints/<milestone-id>.md 2>/dev/null\n```\n\nIf the checkpoint shows a VERIFY APPROVE verdict, the milestone is already done.\n\n"
  - "### Step 2 — Check for existing files\n\nFor each file the plan says to create:\n\n```bash\n# Does the file already exist?\ntest -f <planned-file-path> && echo \"EXISTS: <planned-file-path>\" || echo \"MISSING: <planned-file-path>\"\n```\n\n"
  - "### Step 3 — Check for existing symbols\n\nFor each function, class, or component the plan says to create:\n\n```bash\n# Get linked repos\nLINKED=$(jq -r '.linked_repos[]?' .agents/config.json 2>/dev/null || echo \"\")\n\n# Does the symbol already exist in the codebase or linked repos?\ngrep -rn \"<symbol-name>\" --include=\"*.ts\" --include=\"*.js\" --include=\"*.py\" --include=\"*.md\" . $LINKED 2>/dev/null | grep -v node_modules | grep -v .git\n```\n\n"
  - "### Step 4 — Check for partial implementations\n\n```bash\n# Are there TODO/FIXME markers in relevant files?\ngrep -rn \"TODO\\|FIXME\\|PLACEHOLDER\\|NOT IMPLEMENTED\" <relevant-paths> 2>/dev/null\n```\n\n"
  - "## How to decide the verdict\n\n| Condition | Verdict |\n|-----------|---------|\n| All planned files exist AND checkpoint shows APPROVE | **BUILT** — halt, tell orchestrator the work is already done, surface the artifact location |\n| Some planned files exist OR symbols partially match | **PARTIAL** — tell orchestrator what exists, recommend revising the milestone to \"extend/complete X\" rather than \"build X from scratch\" |\n| No planned files exist, no matching symbols found | **UNBUILT** — tell orchestrator to proceed with IMPLEMENT as planned |\n\n"
  - "## Output format\n\nRecord your verdict in the checkpoint exactly like this:\n\n```\n- preflight: <VERDICT> — checked <N> planned deliverables\n  - <file-or-symbol>: EXISTS | MISSING | PARTIAL (reason)\n  - <file-or-symbol>: EXISTS | MISSING | PARTIAL (reason)\n```\n\n"
  - "## Rules\n\n1. **Never assume.** Always grep/test. \"I think this exists\" is not a preflight result.\n2. **Check the actual file, not just the path.** A file that exists but is empty or a stub is PARTIAL, not BUILT.\n3. **If you find the work is BUILT, do not proceed to IMPLEMENT.** Surface the existing artifact location to the human and the orchestrator. Rebuilding already-done work wastes tokens and risks regression.\n4. **Record every check you ran** in the checkpoint. An unrecorded check is an unrun check (AGENTS.md rule 1).\n"
