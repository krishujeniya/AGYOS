---
trigger: always_on
---
# Git Workflow
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

## Commit Message Format
```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, perf, ci

Note: ECC-managed installs set `"includeCoAuthoredBy": false` in `~/.claude/settings.json`, so commits carry no `Co-Authored-By` trailer by default. To keep Claude attribution, set `"includeCoAuthoredBy": true` or configure `attribution`; ECC never overwrites an explicit choice.

## Pull Request Workflow

When creating PRs:
1. Analyze full commit history (not just latest commit)
2. Use `git diff [base-branch]...HEAD` to see all changes
3. Draft comprehensive PR summary
4. Include test plan with TODOs
5. Push with `-u` flag if new branch

> For the full development process (planning, TDD, code review) before git operations,
> see [development-workflow.md](common-development-workflow.md).
