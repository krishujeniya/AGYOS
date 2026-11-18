# Quickstart

The root [README](https://github.com/krishujeniya/AGYOS#readme) is the canonical project overview and command guide. It combines the current architecture summary, CLI examples, security boundaries, CI policy, and links to detailed references.

Clone the repository and inspect the available commands:

```bash
git clone https://github.com/krishujeniya/AGYOS.git
cd AGYOS
bin/agyos help
```

To find a relevant runbook and read it:

```bash
bin/agyos decide "fix a Python error" --json --runbook
bin/agyos skill technical-documentation-writer
```

To inspect workflow state, workspace revisions, or export diagnostics:

```bash
# Check current gate and recommended next safe action
bin/agyos state

# Inspect transactional workspace milestones in SQLite store
bin/agyos workspace status

# Preview redacted system diagnostics
bin/agyos diagnostics --preview
```

Read the repository's [`AGENTS.md`](https://github.com/krishujeniya/AGYOS/blob/main/AGENTS.md) before making changes. Tests, builds, linters, type checks, dependency resolution, setup, and media renders for this repository run in GitHub Actions; see the [CI workflows](https://github.com/krishujeniya/AGYOS/tree/main/.github/workflows).
