---
trigger: always_on
---
# Skill discovery and execution
## STRICT GLOBAL INVARIANT: ZERO LOCAL BUILDS/TESTS (CI/CD ONLY VIA GITHUB ACTIONS)
- **Zero Local Execution for Heavy Verification**: NEVER run unit/integration/E2E test suites, compiler builds, linters, type checks, packaging, dependency installation, or media renders locally.
- **GitHub Actions Mandatory**: All testing, building, linting, and validation MUST run strictly in GitHub Actions CI/CD workflows. Trigger the workflow, push to branch, or dispatch via GitHub CLI (`gh workflow run`), then inspect the run results (`gh run watch` / `gh run view`).
- **Allowed Local Operations**: Only read-only static inspection (grep, AST read, file inspection) and `git diff --check` are permitted locally.
- **Prevent Pollution**: Keep temporary build caches, rendered artifacts, model checkpoints, virtual environments, and intermediate files completely off local disk and out of Git.

## STRICT REPOSITORY & DEPLOYMENT INVARIANT: SINGLE MAIN BRANCH & IDENTITY LOCK
- **Single `main` Branch Exclusive**: NEVER create feature branches, task branches, or divergent worktrees. The repository must maintain ONLY the `main` branch.
- **Auto-Prune & Branch Convergence**: If any other branch exists locally or on remote (e.g. `master`, feature branches, dependabot branches), immediately merge its valid changes into `main` and delete the secondary branch (`git branch -D <branch>`, `git push origin --delete <branch>`). Rename any legacy `master` branch to `main`.
- **Identity Enforcement (Krish Ujeniya)**:
  - All git commits MUST strictly be authored and committed under the verified GitHub identity:
    `git config user.name "Krish Ujeniya"`
    `git config user.email "100012208+krishujeniya@users.noreply.github.com"`
  - Commits must properly link to `https://github.com/krishujeniya` to display the verified account profile picture and attribution badge.
- **Auto-Deploy to GitHub**: Once a task or code change is complete and verified statically, automatically commit and push directly to `origin main` using the active authenticated `krishujeniya` GitHub account.

For every task, including follow-ups and small edits:

1. Discover a relevant skill using `agyos_decision`, `agyos_find_skill`,
   `bin/agyos decide "<task>" --json --runbook`, or inspect the local catalog
   when those tools are unavailable. Honor an explicitly requested skill.
2. Read the selected `SKILL.md` before specialist work. Reuse a runbook already
   read in this session when its contents and the task have not changed.
3. Apply relevant steps and load only the references needed for the objective.
   Select supporting skills when distinct parts of the task require them.
4. Re-run discovery when the objective changes or the first recommendation
   does not fit. A fallback is a prompt to inspect the objective, not proof of fit.
5. Verify with commands appropriate to the change. Report what ran, what failed,
   and what remains. Selection and returned runbooks do not prove execution.

This policy covers every skill and modular rule in the checkout. Apply common
rules and relevant language, workflow, and risk rules; do not load every skill
or force unrelated specialist steps into a simple task. Scores are matching
heuristics, never calibrated success probabilities.

Honor host permissions and explicit user constraints. Existing authorization
remains valid within scope. A runbook does not authorize external actions or
unsupported tools. Follow the host's actual tool schema rather than copying an
example invocation literally. Preserve upstream attribution and required notices.
In this repository, run tests, builds, linters, type checks, dependency
resolution, toolkit setup, and renders only through GitHub Actions. Local
verification is limited to read-only inspection and `git diff --check`.

See `docs/SKILL_ROUTING.md` for maintenance checks and known limits.
