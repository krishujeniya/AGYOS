# Contributing to ANCHOR

Thank you for your interest in making ANCHOR better! This document outlines how to develop, test, and contribute to the project.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/krishujeniya/Anchor.git
   cd Anchor
   ```

2. **Initialize your local environment:**
   ```bash
   bash bin/init.sh
   ```

3. **Install dependencies:**
   ANCHOR relies on standard Unix tools like `bash`, `jq`, and `grep`. For running tests and verification, ensure you have:
   - `bats` (Bash Automated Testing System)
   - `shellcheck`
   - `markdownlint-cli`

## Running Tests

ANCHOR enforces strict evidence over claims. Before submitting a PR, you must verify your changes locally using our test harnesses.

1. **Run the Evaluation Harness:**
   ```bash
   bash bin/eval.sh
   ```
   This will test current state integrity, historical checkpoint regressions, and behavioral security checks.

2. **Run bats tests:**
   ```bash
   bats tests/
   ```

## Pull Request Checklist

When submitting a PR, please ensure:
- [ ] You have run `bash bin/eval.sh` and it exits with `0` (PASS).
- [ ] You have run `shellcheck` on any modified `.sh` scripts.
- [ ] You have not weakened or removed any assertions without providing a valid `Override-Test-Ratchet` checkpoint note.
- [ ] All new functionality has an accompanying test or bats fixture.
- [ ] You have updated the `CHANGELOG.md` with your changes.

## Architecture Guidelines
- **Zero Dependencies:** ANCHOR's core spine must run with zero third-party packages installed on the host (relying purely on bash, jq, etc.).
- **Maker/Checker Separation:** Do not combine implementation skills and verification skills into the same agent context.
- **Durable State:** All state must be tracked via `.agents/state/state.json` or append-only Markdown artifacts.
