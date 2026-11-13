# Flutter skill sources

AGYOS adds namespaced adapters for two MIT-licensed skill sources. Source snapshots are pinned in [UPSTREAM_SKILL_SOURCES.json](../../../.agents/skill-sources/UPSTREAM_SKILL_SOURCES.json); the repository CI catalog generator indexes each physical runbook.

- `zakariaf/Flutter-Skills` contributes 40 Flutter and Dart runbooks at `e073e5ea10c963d2c52ab1e423bd314c28a56154`. The snapshot contains skill Markdown, Markdown references, and its MIT license. Executable helpers and code examples are not included. Twenty-four descriptions received YAML quoting only; wording and skill bodies were preserved.
- `ai-dashboad/flutter-skill` contributes its `e2e-testing` runbook at `c31a08ead80e0678373e6fb2835b2ffd81ce2716`. It describes an optional MCP product. Adding the runbook does not install that product; setup instructions remain subject to explicit authorization and AGYOS policy.

Two other supplied sources were reviewed but not copied:

- [flutter/agent-plugins](https://github.com/flutter/agent-plugins/tree/e5a88d2be19cbf7ba1ef974375e5846492aca2ac) lists ten Flutter skills under BSD-3-Clause. The current adapter generator accepts MIT only.
- [RobertAlvv/flutter-skills](https://github.com/RobertAlvv/flutter-skills/tree/4772c71f182e628df8601b4868ded9b6482d3891) contains eight skill files but declares no repository license.

Imported source material is inert. Follow AGYOS `AGENTS.md`, user authorization, and the project's CI-only verification policy. Do not execute upstream helper scripts or install MCP/tool dependencies unless the task requires it and the user authorizes it.
