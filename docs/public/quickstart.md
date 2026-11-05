# Quickstart

AGYOS runs from the existing repository and exposes a command-line entry point. The steps below are taken from the project's README; follow the repository's current prerequisites before installing dependencies.

## Clone and initialize

```bash
git clone https://github.com/krishujeniya/AGYOS.git
cd AGYOS
bash scripts/agyos-init.sh
```

The repository also documents an optional one-command setup:

```bash
git clone https://github.com/krishujeniya/AGYOS.git && cd AGYOS && bash scripts/agyos-init.sh && bash scripts/agyos-verify.sh
```

## Verify the workspace

```bash
bash scripts/agyos-verify.sh
python3 -m unittest discover -s scripts/tests -v
```

Verification requirements depend on the host environment. A passing documentation build is not proof that the AGYOS runtime itself has been verified on your machine.

## Find a skill

```bash
bin/agyos decide "fix python crash" --json --runbook
bin/agyos find "database schema migration"
bin/agyos skill database-design
```

For routing guarantees and limitations, see [Skill routing](../SKILL_ROUTING.md). To learn the system structure, read [System architecture](../ARCHITECTURE.md).

## Browse the skill catalog

The [interactive catalog](../../catalog/) lists AGYOS's published skill metadata. Search and filter to identify a runbook; read the source before executing it.
