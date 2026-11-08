# Integration Maintenance and Guardrails

## Source updates

Do **not** auto-follow `main` or `latest`. On a proposed upstream update, compare the pinned SHA with the candidate SHA. Read LICENSE changes, installer scripts, dependency locks, source code, authentication behavior, and upstream tests. Document the classification for each new component (REUSE, ENHANCE, IMPORT, ADAPT, REFERENCE, QUARANTINE, BLOCK). Keep duplicates and rejected items in a review artifact rather than overwriting AGYOS skill folders.

AAS Core or any upstream skill installation tool must **not** own routing. Prefer the existing AGYOS flat skill directory and regenerate the standard manifests **only after** an individually reviewed skill is added. Keep source references outside active skill directories.

## Tests

```bash
python3 -m unittest scripts.tests.test_external_sources -v
python3 -m unittest discover -s scripts/tests -v
python3 -m compileall agyos_decision scripts/tests
python3 scripts/build_tiered_skills_manifest.py
python3 scripts/build_docs_data.py
git diff --exit-code -- .agents/skills-manifest.json .agents/tier1-skills.json docs/skills-data.json docs/ai-catalog.json docs/llms.txt docs/sitemap.xml docs/robots.txt
bash scripts/agyos-verify.sh
bin/agyos decide "Review the code and find problems before release" --json --runbook
bin/agyos intent "Create a personalized AI engineering career roadmap"
```

The full `agyos-verify.sh` requires a working `agy`, Bun, MCP service, plugin validation, and local state. CI verifies an environment-specific subset; CI success alone does **not** certify local AGY CLI runtime compatibility.

## Security

- Every external link, search snippet, prompt, resume and model output is untrusted data.
- Only reviewed native AGYOS runbooks may be executed through the existing governor.
- The Agent Reach adapter uses subprocess argument vectors, disallows login/add/setup/update/write, caps query and output, and returns structured failures. It does **not** log subprocess stderr that could contain sensitive values. Install the official upstream binary separately and only after inspection; the PyPI `agent-reach` package is not the same project.
- Authenticated research platforms remain disabled. Do not fetch browser cookies automatically, circumvent access restrictions, or perform social engagement.
- Cloud and IoT deployment is always advisory until the user explicitly authorizes individual real-world actions.
- Before production review, run the independent checker and inspect GitHub Actions evidence.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| No source match | Multi-concept route not satisfied | Use normal AGYOS catalog; review matching patterns before expanding |
| Registry rejected | Invalid SHA, duplicate ID, missing native skill, or altered schema | Fix the registry and rerun Python tests; do not bypass validation |
| Agent Reach unavailable | Official CLI not installed or not responsive | Use AGYOS existing search providers; inspect upstream installation manually |
| Manifest drift | Generated docs or skills changed | Rebuild with AGYOS scripts and commit generated data |
| AI Engineering F2/F3/F4 unavailable | Upstream roadmap only | Preserve preview status; do not invent a skill |

## Rollback

This integration has no database migration. Revert its commits or close the draft PR to restore the old routing. If the optional Agent Reach CLI is installed in a local environment later, it is **not** installed or uninstalled by this repository and must be managed by that environment's operator.
