# AI Handoff — AGYOS

## Task
Incorporate 3 top-priority core operating invariants into global configuration (`~/.gemini/config/AGENTS.md`), project constitution (`AGENTS.md` and `GEMINI.md`), and engineering rules (`common-coding-style.md`, `common-development-workflow.md`):
1. **Skill-First Autonomous Routing**: Automatically find and apply best skills first via FastMCP `agyos_find_skill` or `.agents/skills`.
2. **Mandatory Deep Research**: Always research files, manifests, and dependencies using research skills before proposing or modifying code.
3. **Pure Human Language & Zero AI Slop**: Strictly enforce natural human prose, ban 21+ AI buzzwords, eliminate robotic/templated conversational filler, ban decorative emoji spam, and reject unnecessary/speculative components.
Verified all 27 checks pass in `scripts/agyos-verify.sh`.

## Branch / Revision
- Branch: `main`
- Target Runtime: Antigravity CLI (`agy`) v1.4.12+
- Operating System: Linux (Ubuntu)

## Changed Files & Directories
- `~/.gemini/config/AGENTS.md`: Global operating policy updated with the 3 Core Operating Invariants as highest priority across all workspaces.
- `AGENTS.md` & `GEMINI.md`: Upgraded Section 1 Gravitas Invariants and Section 7.0 Autonomous Discovery to prioritize skill-first routing, mandatory research, and zero AI slop.
- `.agents/rules/common-coding-style.md`: Added "Pure Human Engineering & Zero AI Slop (CRITICAL)" section.
- `.agents/rules/common-development-workflow.md`: Re-anchored Step 0 to "Skill Discovery & Research First".
- `TRACKER.md`: Updated Section 3 Gravitas Invariants to align with the 3 top priorities.

## Tests Actually Run & Results
- `bin/agyos verify`: **27 PASSED, 0 FAILED**
- `bin/gate-check.sh`: **PASS** (monotonic assertions ratchet preserved)
- `python3 scripts/build_tiered_skills_manifest.py`: **PASS** (1,838 skills cataloged)
- `python3 scripts/build_docs_data.py`: **PASS** (all docs datasets compiled)

## Blockers
None. System is 100% operational with top-priority global human-engineering and skill-first invariants.

## One Exact Next Command
```bash
bin/agyos verify
```
