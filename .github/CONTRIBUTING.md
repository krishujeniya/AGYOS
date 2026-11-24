# Contributing to AGYOS

Thank you for your interest in contributing to AGYOS. We enforce strict engineering invariants to ensure stability and predictability.

## Development Lifecycle & Standards

1. **Single Branch Discipline**:
   All development lands directly on `main`. Do not create secondary branches.

2. **Author Attribution**:
   All commits must match the verified maintainer profile:
   - Name: `Krish Ujeniya`
   - Email: `100012208+krishujeniya@users.noreply.github.com`

3. **Python Execution via `uv`**:
   Execute all Python tasks through `uv` (`uv run`, `uv sync`). Direct usage of unmanaged `python` or `pip` is prohibited.

4. **Testing & Verification**:
   - Local validation is strictly lightweight (syntax checks, `git diff --check`, `tsc --noEmit`).
   - Heavy test suites and full builds execute remotely in GitHub Actions (`.github/workflows/ci.yml`).

## Workflow Steps

1. Review requirements and verify alignment with the 7-step autonomous cycle (`Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect`).
2. Run local syntax checks with `make test` or `make typecheck`.
3. Submit changes to `main` and monitor GitHub Actions CI until all jobs pass green.
