# Production Code Audit

Use this procedure to review a repository for production-readiness risks. An audit is read-only unless the user explicitly asks for implementation. Keep findings within the requested paths and state the evidence and coverage limits.

## 1. Establish scope and baseline

1. Restate the target repository, requested outcome, excluded paths, and constraints. Resolve material ambiguity before making changes.
2. Read applicable `AGENTS.md`, project handoff notes, and relevant skill instructions. Inspect the current branch, revision, worktree status, and relevant diff so pre-existing edits are preserved.
3. Read project manifests, CI configuration, entry points, and tests that define the target behavior. Use repository search and targeted file reads; do not claim to have read every file unless that was actually done and recorded.
4. Define the areas and paths covered by this audit. If the request is broad, inventory the repository first, then report any paths or file types excluded from detailed review.

## 2. Inspect and collect evidence

Review only the requested scope. Follow relevant execution paths and contracts instead of relying on filenames or generic checklists. Look for issues in the areas that apply:

- Correctness and error handling
- Authentication, authorization, input handling, secrets, and data exposure
- Dependencies and deployment configuration
- Performance bottlenecks supported by a reproducible baseline
- Maintainability, complexity, and duplication
- Tests, observability, recovery, and operational readiness

For each finding, record the file and line or other reproducible evidence, the affected behavior, impact, confidence, and a practical next step. Distinguish confirmed defects from risks, heuristics, and questions that require runtime, owner, or external-source verification. A keyword match or checklist item alone is not proof of a defect.

Use the repository's existing checks where applicable. Check version-sensitive technical claims against current primary documentation. Do not claim coverage beyond the files, commands, environments, and behaviors actually examined.

## 3. Prioritize recommendations

Order findings by demonstrated impact and likelihood. Separate required fixes from optional improvements. Avoid assigning compliance status, a letter grade, a coverage percentage, or a production-ready verdict unless the user supplied measurable criteria and the audit collected evidence that satisfies them.

For performance work, record the baseline command, dataset or workload, environment, repeated measurements, and variance. Compare the same workload after a change. If comparable measurements are unavailable, report the bottleneck as unmeasured and do not state an improvement percentage.

## 4. Make changes only when authorized

The default audit is read-only. If the user explicitly requests fixes, change only the authorized files and behavior. Prefer one focused change at a time, add or update a regression check for each confirmed defect, and preserve unrelated worktree edits. Do not add infrastructure, refactor adjacent modules, install packages, contact external services, or perform destructive actions unless that action is authorized and needed for the stated scope.

Before a broad or irreversible change, stop at the relevant approval boundary. Do not infer permission from a request to inspect, audit, or recommend.

## 5. Verify and report

Run the narrowest relevant checks first, followed by applicable project checks. Report commands and their actual results. If a check could not run, label it as not run and give the reason. A passing test suite does not establish security, performance, or deployment readiness by itself.

Use this report structure:

```markdown
# Production Code Audit

## Scope
- Repository and revision:
- Paths and behaviors examined:
- Exclusions and limits:

## Findings
For each finding: severity, confidence, evidence, impact, and recommended action.

## Checks
- Command — result
- Not run — reason

## Open questions
- Claims or behaviors needing runtime, owner, or primary-source verification.
```

## Finding confidence

- **Confirmed:** directly reproduced or supported by a specific code path, test, configuration, or authoritative source.
- **Likely:** supported by evidence but missing a runtime or environmental check.
- **Candidate:** surfaced by a heuristic or checklist and needs investigation.

Do not turn a candidate into a confirmed finding without additional evidence.

## Useful review areas

Apply only the areas relevant to the repository and request:

- Security: trust boundaries, authorization decisions, validation, secret handling, and sensitive output.
- Reliability: timeouts, retries, idempotency, failure handling, data integrity, and recovery.
- Performance: measured hot paths, query behavior, memory use, and asset sizes.
- Quality: module boundaries, complexity, duplicated behavior, and maintainable tests.
- Operations: configuration, logs, health signals, deployment steps, and rollback procedures.

These are review prompts, not a claim that every repository requires every control.

## Related skills

- `ai-code-review` — focused source review.
- `api-security-best-practices` — API security design guidance.
- `app-perf-optimizer` — performance investigation and optimization.
- `systematic-debugging` — tracing a reproduced failure to its cause.

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Engineering Practices](https://google.github.io/eng-practices/)
