# API Reference

ANCHOR exposes several pure bash executables in the `bin/` directory.

## `bin/init.sh`
Initializes a new ANCHOR project, resets all state, generates IDE bridges, and installs the git pre-commit hook.

## `bin/gate-check.sh`
The core verification hook. Fails the commit if the `VERIFY` gate hasn't been completed for the current milestone.

## `bin/eval.sh`
The ANCHOR meta-verifier. Runs consistency checks against the state JSON, validates checkpoints, and runs adversarial behavioral checks.

## `bin/rollback.sh`
Safely stashes WIP changes to a rescue branch and hard resets to `last_known_commit`.

## `bin/dashboard.sh`
Launches the interactive local web UI for visualizing state.
