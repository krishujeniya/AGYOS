# Gate 4: IMPLEMENT — Full Protocol

> Load this reference JIT when entering Gate 4. Do NOT preload into context.

## Objective
Execute the implementation plan autonomously using expert agents with TDD discipline.

## Step-by-Step Protocol

### Step 1: Complexity Assessment
```
Skill: expert-orchestrator
```

Score the overall implementation:
- If score 6-9: Single agent execution
- If score 10-14: Small swarm (2-3 experts)
- If score 15+: Full swarm with parallel dispatch

### Step 2: Environment Setup
```
Skill: using-git-worktrees
Skill: expert-devops
```

1. Create feature branch: `git checkout -b feature/[project-name]`
2. If complex: Use git worktree for isolation
3. Set up development environment (Docker, deps, etc.)

### Step 3: Execute Tasks from task_plan.md

For each unchecked task `- [ ]` in `task_plan.md`:

#### 3a. TDD Cycle
```
Skill: test-driven-development
```

1. **RED**: Write failing test first
2. **Verify RED**: Run test, confirm it fails for the right reason
3. **GREEN**: Write minimal code to pass
4. **Verify GREEN**: Run test, confirm it passes
5. **REFACTOR**: Clean up while keeping tests green

#### 3b. Implementation
```
Skill: expert-dev
```

- Follow SOLID principles
- Keep functions < 20 lines
- Use meaningful names
- Handle errors gracefully
- No TODOs without context

#### 3c. Update State

After completing each task:
```bash
# Mark task complete in task_plan.md
sed -i 's/- \[ \] Task N/- [x] Task N/' .sovereign/task_plan.md

# Update state.json
# current_task += 1
```

Log progress in `progress.md`:
```markdown
## Task N: [Title] ✅
- Completed: [timestamp]
- Files modified: [list]
- Tests: [N] passing
- Notes: [any observations]
```

#### 3d. Parallel Dispatch (if applicable)
```
Skill: subagent-driven-development
Skill: dispatching-parallel-agents
```

For independent tasks, fan-out to parallel agents:
- Each agent gets isolated context
- Clear deliverables per agent
- Orchestrator integrates results

### Step 4: Debugging (when tests fail)
```
Skill: systematic-debugging
```

1. **Phase 1**: Root cause investigation (read errors, reproduce, check changes)
2. **Phase 2**: Pattern analysis (find working examples, compare)
3. **Phase 3**: Hypothesis and testing (single hypothesis, minimal change)
4. **Phase 4**: Implementation (fix root cause, not symptom)

**If 3+ fixes fail**: Stop, question architecture, discuss with user.

### Step 5: Continuous Quality Rules

All 11 engine rules are enforced during implementation:
- `testing.md`: No code without tests
- `security.md`: Security-first always
- `error-handling.md`: No silent fails
- `git-workflow.md`: Clean commits
- `logging.md`: Structured logging
- `performance.md`: Performance is a requirement

### HITL During Implementation
- **NOT required** for code, tests, git operations, debugging
- **REQUIRED** if: security-critical decisions, external API keys needed, production data access

## State Update
After all tasks complete:
- Set `current_gate: 5`
- All tasks in `task_plan.md` should be `- [x]`
