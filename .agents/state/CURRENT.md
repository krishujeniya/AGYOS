# CURRENT

- Task: research-led-optimization; operator requested research, one prompt, and local application.
- Branch/revision: main; baseline 190e8eac09cb17675442c3740a983b5f28b81ede; changes uncommitted.
- Gate: IDLE; PASS (operator approved and technical gates verified).
- Scope and acceptance: docs/research/OPTIMIZATION_PLAN.md.
- Deliverables: docs/research/OPTIMIZATION_RESEARCH.md, docs/OPTIMIZATION_PROMPT.md, docs/OPTIMIZATION_RESULTS.md, ADR 0002.
- Changes: exact budget accounting and deadline/reserve validation, atomic graph insertion, public routing JSON, regression isolation, host test fix (agy agents -> agy agent + 60s timeout).
- Evidence: Python 128/128 passed (50.7s); verification 51/51 passed; Bun 59/59 passed (134 expectations); line coverage ledger 95%, router 97%.
- Experiment: same routing rankings, 90 -> 0 serialization errors per 300 calls; no demonstrated latency gain; top-k variant rejected.
- Fix applied: test_agy_cli_lists_all_5_pods used `agy agents` (undocumented alias, variable timing) instead of `agy agent` (documented subcommand, ~4s). Changed to `agy agent` with 60s timeout.
- Limits: accounting is single-owner and requires trusted dispatch integration; no paid calls, commits, pushes, or deployment.
- Next: milestone verified; ready for commit and handoff.
