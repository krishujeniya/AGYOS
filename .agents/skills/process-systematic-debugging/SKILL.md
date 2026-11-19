---
name: process-systematic-debugging
description: "Master rule for debugging and fixing issues. Enforces the 4-phase root cause analysis process, backward tracing, defense-in-depth validation, and condition-based waiting for flaky tests. Prevents guessing and 'quick fixes'."
category: process
risk: safe
tags: "[debugging, bugfix, root cause, testing, process, flaky tests]"
version: "1.0.0"
prompt-source: prompt.toon
---
skill: "process-systematic-debugging"
sections[10]:
  - "\n"
  - "# Process: Systematic Debugging\n\n"
  - "## The Iron Law\n**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**\nRandom fixes waste time and create new bugs. Quick patches mask underlying issues. You must complete the 4 phases below before writing any fix.\n\n"
  - "## The 4-Phase Debugging Protocol\n\n"
  - "### Phase 1: Investigation & Evidence (DO THIS FIRST)\n1. **Read Errors:** Read the complete stack trace and error message.\n2. **Reproduce:** Find exact steps to reproduce consistently.\n3. **Trace Backward (Root Cause Tracing):** \n   - Observe the symptom (e.g., `git init failed`).\n   - Find the immediate cause in the code.\n   - Ask: What called this? Keep tracing up the call stack.\n   - Find where the bad data *originated*, not where it merely crashed.\n4. **Gather Evidence:** In multi-layered systems, add logging at boundaries to see exactly where data state diverges from expectations.\n\n"
  - "### Phase 2: Pattern Analysis\n- Look for working variants of the failing behavior in the codebase.\n- Identify the exact differences between the broken implementation and the reference.\n\n"
  - "### Phase 3: Hypothesis & Testing\n- Form a single, testable hypothesis (`I think X is the root cause because Y`).\n- Test minimally. Change one variable at a time.\n\n"
  - "### Phase 4: Implementation & Defense\n1. **Failing Test First:** Write a test that proves the bug exists (and fails).\n2. **Implement Fix at Source:** Fix the original trigger identified in Phase 1.\n3. **Defense-in-Depth:** A bug fixed in one place can be bypassed. Add structural validation at all layers:\n   - *Layer 1:* Entry Point Validation (e.g., Zod schemas)\n   - *Layer 2:* Business Logic Validation\n   - *Layer 3:* Environment Guards (e.g., refuse destructive actions in test ENVs)\n4. **Verify Fix:** Ensure the failing test now passes.\n\n"
  - "## Red Flags (STOP and return to Phase 1)\n- *\"Just try changing X and see if it works\"*\n- *\"Add multiple changes, run tests\"*\n- *\"I'll write the test after fixing it\"*\n- **You have tried 3+ fixes and it still fails.** (This indicates an architectural problem. Stop and discuss with the user).\n\n"
  - "## Specialized Technique: Condition-Based Waiting (Flaky Tests)\nNever use arbitrary timeouts (`setTimeout(r, 1000)`, `sleep()`) to wait for async state, as this causes flaky tests under CI load. \n\n**Rule:** Polling Condition > Arbitrary Timeout.\n```typescript\n// ❌ WRONG\nawait new Promise(r => setTimeout(r, 1000));\nexpect(system.ready).toBe(true);\n\n// ✅ RIGHT\nawait waitFor(() => system.ready === true, \"System to become ready\", 5000);\n```\nOnly use arbitrary timeouts if you are explicitly testing timing behavior (e.g., debouncing), and document the reasoning.\n"
