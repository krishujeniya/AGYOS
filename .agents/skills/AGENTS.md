# Instructions for the complete skill catalog

Every skill in this directory follows `../../AGENTS.md` and
`../rules/common-skill-routing.md`. Discover, read, apply, and verify for every
task. Reuse unchanged runbooks already read in the session; discover again when
the objective changes. Directory names are stable skill IDs and must match the
YAML `name`. Descriptions must state the capability and when it applies.

Use the host's supported tools. Local runbook examples do not override explicit
user scope, permissions, or existing authorization. Preserve licenses and
attribution. Run `python3 -m unittest scripts.tests.test_skill_routing -v` and
regenerate both catalogs after changing discovery metadata.
