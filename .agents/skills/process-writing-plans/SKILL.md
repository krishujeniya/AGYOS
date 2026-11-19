---
name: process-writing-plans
description: "Master of creating detailed, bite-sized implementation plans. Enforces TDD, specific file paths, and strict task granularity. Use before touching code when solving complex problems or implementing new features."
category: process
risk: safe
tags: "[planning, tdd, implementation, architecture, steps, tasks, process]"
version: "1.0.0"
prompt-source: prompt.toon
---
skill: "process-writing-plans"
sections[9]:
  - "\n"
  - "# Process: Writing Plans\n\n"
  - "## Purpose\nThis skill governs how implementation plans are constructed. Jumping straight into code for complex features leads to regressions and messy architecture. This skill forces you to break down the goal into incredibly small, actionable, TDD-driven tasks before execution begins.\n\n"
  - "## When to Use\n- **Gate 3 (PLAN):** When writing the `implementation_plan.md` and `task.md`.\n- **Anytime** a feature requires touching more than one component or introduces new logic.\n- **Complex Orchestrations:** When delegating tasks to subagents or managing multi-step workflows.\n\n"
  - "## File-Based Planning Integration\nIn alignment with the `planning-with-files.md` skill, complex problem-solving should utilize persistent planning artifacts in the root directory:\n- `task_plan.md`: The single source of truth for ordered sub-tasks.\n- `progress.md`: Current execution state and execution logs for the current phase.\n- `findings.md`: Persistent knowledge, API schemas, and test discoveries.\nAlways ensure your implementation plan generates or updates these files before acting.\n\n"
  - "## The Bite-Sized Doctrine\n\nAssume the executing agent (which could be yourself in the next step) needs absolute clarity. Document EXACTLY which files to touch, which tests to write, and how to verify them.\n\n**Each task must represent 2-5 minutes of work.**\n\n"
  - "### Strict Task Structure\nEvery task in your plan MUST follow this rhythm:\n1. **RED:** Write the failing test.\n2. **VERIFY RED:** Run the test. Watch it fail for the right reason.\n3. **GREEN:** Write the minimal implementation code.\n4. **VERIFY GREEN:** Run the test. Watch it pass.\n5. **COMMIT / CHECKPOINT:** Mark the task as done.\n\n"
  - "## Plan Document Template\nWhen creating an `implementation_plan.md`, use this structure:\n\n```markdown\n# [Feature Name] Implementation Plan\n\n**Goal:** [One sentence describing what this builds]\n\n**Architecture:** [2-3 sentences about approach, referencing relevant architecture skills like architecture-python-backend.md or architecture-react-nextjs.md]\n\n---\n\n### Task 1: [Component/Function Name]\n\n**Files:**\n- Create: `exact/path/to/file.py`\n- Modify: `exact/path/to/existing.py:123-145`\n- Test: `tests/exact/path/to/test.py`\n\n**Step 1: Write failing test**\n[Code snippet of the exact test]\n\n**Step 2: Verify RED**\nCommand: `pytest tests/path/test.py::test_name`\nExpected: FAIL (\"function not defined\")\n\n**Step 3: Implementation**\n[Code snippet of minimal implementation]\n\n**Step 4: Verify GREEN**\nCommand: `pytest tests/path/test.py::test_name`\nExpected: PASS\n```\n\n"
  - "## Operator Checklist (PRE-ACT)\n- [ ] Is the plan broken down into bite-sized (2-5 min) tasks?\n- [ ] Are `task_plan.md`, `progress.md`, and `findings.md` initialized or updated to guide execution?\n- [ ] Does every logic task start with a failing test (TDD)?\n- [ ] Are exact file paths and test commands provided?\n- [ ] Are architecture rules (e.g., DFII, BFRI) respected in the plan?\n"
