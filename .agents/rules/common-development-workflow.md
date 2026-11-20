---
trigger: always_on
---
# Development Workflow

> This file extends [common/git-workflow.md](common-git-workflow.md) with the full feature development process that happens before git operations.

The Feature Implementation Workflow describes the development pipeline: research, planning, TDD, code review, and then committing to git.

## Feature Implementation Workflow

0. **Skill Discovery & Research First (Mandatory Before Any Work)**
   - **Discover best skills first:** Automatically query `agyos_find_skill` or `.agents/skills` to retrieve the exact domain specialist instructions. Ingest them silently before taking action.
   - **Codebase and documentation research:** Use `research`, `code-explorer`, AST/grep scans, and official vendor docs to confirm current system structure, interfaces, and dependencies before modifying any file.
   - **Check existing patterns & registries:** Search local implementations and trusted registries. Prefer adopting proven patterns over writing speculative logic.
   - **Human language and minimal components:** Communicate in natural, direct human prose. Reject AI buzzwords, robotic filler, and unneeded wrapper components.

1. **Plan First**
   - Use **planner** agent to create implementation plan
   - Generate planning docs before coding: PRD, architecture, system_design, tech_doc, task_list
   - Identify dependencies and risks
   - Break down into phases

2. **TDD Approach**
   - Use **tdd-guide** agent
   - Write tests first (RED)
   - Implement to pass tests (GREEN)
   - Refactor (IMPROVE)
   - Verify 80%+ coverage

3. **Code Review**
   - Use **code-reviewer** agent immediately after writing code
   - Address CRITICAL and HIGH issues
   - Fix MEDIUM issues when possible

4. **Commit & Push**
   - Detailed commit messages
   - Follow conventional commits format
   - See [git-workflow.md](common-git-workflow.md) for commit message format and PR process

5. **Pre-Review Checks**
   - Verify all automated checks (CI/CD) are passing
   - Resolve any merge conflicts
   - Ensure branch is up to date with target branch
   - Only request review after these checks pass
