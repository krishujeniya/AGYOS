---
trigger: always_on
---
# Skill discovery and execution

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

See `docs/SKILL_ROUTING.md` for maintenance checks and known limits.
