# Local security toolkits

These are source packages used by AGYOS security and penetration testing runbooks. The skills reside in `.agents/skills/`; the core agent engines, tools, sandbox specifications, and test suites reside here so the skill catalog does not duplicate tool code.

| Toolkit | Purpose | Runbook |
| --- | --- | --- |
| [`strix/`](strix/README.md) | Autonomous penetration testing tool for web apps, APIs, codebases, and infrastructure. Validates findings with working proofs of concept. | [penetration-testing-with-strix](../../.agents/skills/penetration-testing-with-strix/SKILL.md) |

Use the toolkit's own README and configuration files as the source of truth for runtime dependencies, sandbox image setup, and flags.

Testing, builds, dependency installation, and compiler tasks for this repository run in GitHub Actions CI. Local checks are limited to static inspection and git diff validation.

## Provenance and licensing

Strix is developed by usestrix and licensed under Apache-2.0. The bundled package retains its original LICENSE, NOTICE, documentation, and metadata files under `tools/security/strix/`.
