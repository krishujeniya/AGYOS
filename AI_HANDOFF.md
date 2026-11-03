# AI Handoff — AGYOS

## Task
Rebrand AGYOS to a unified single branding, eliminate legacy `cc-`, `claude-`, and `ecc-` prefixes and duplicate skills, rebrand `agyos-ecc-polyglot` plugin to `agyos-polyglot`, implement the FastMCP `agyos_find_skill` semantic skill finder and `bin/agyos find` CLI command, enforce Gravitas Invariant 7 (Search-First Autonomous Skill Discovery) in `AGENTS.md`, recompile manifests and documentation catalogs across all 1,838 physical skills, and pass 27/27 adversarial verification checks.

## Branch / Revision
- Branch: `main`
- Target Runtime: Antigravity CLI (`agy`) v1.4.12+
- Operating System: Linux (Ubuntu)

## Changed Files & Directories
- `mcp/agyos-state-server.cjs`: Added `agyos_find_skill` (and `anchor_find_skill` alias) FastMCP tool for high-speed token/keyword scoring against `.agents/skills-manifest.json`.
- `bin/agyos`: Added `find <query>` / `search <query>` subcommand for rapid terminal skill discovery.
- `scripts/package_agyos_plugins.py`: Rebranded `agyos-ecc-polyglot` to `agyos-polyglot` with canonical AGYOS repository and author metadata.
- `.agents/plugins/agyos-polyglot`: Packaged and installed to `~/.gemini/config/plugins/agyos-polyglot`.
- `.agents/skills/`: Purged 7 legacy `cc-skill-*` duplicate folders, renamed and rebranded 6 skills (`agyos-project-guidelines-example`, `agyos-devfleet`, `configure-agyos`, `agyos-guide`, `agyos-recipes`, `agyos-tools-cost-audit`).
- `.agents/rules/common-agents.md`: Updated agent orchestration rule from legacy ECC syntax to native `invoke_subagent`.
- `AGENTS.md` & `GEMINI.md`: Upgraded to 7 Gravitas Invariants with Invariant 7 (Search-First Autonomous Discovery) and Section 7.0 autonomous skill ingestion instructions.
- `TRACKER.md`: Hardening Ledger Item 7 recorded, updated scale inventory (1,838 skills, 27/27 tests).
- `scripts/agyos-verify.sh`: Added checks for `agyos_find_skill` JSON-RPC tool and `bin/agyos find` CLI.

## Tests Actually Run & Results
- `bin/agyos verify`: **27 PASSED, 0 FAILED**
  - AGENTS.md size limit (<24,000 bytes): PASS
  - GEMINI.md exists and matches AGENTS.md: PASS
  - AGY CLI installed and responsive: PASS
  - Anchor MCP server registered in AGY: PASS
  - AGYOS Safety Hook blocks dangerous commands: PASS
  - AGYOS Safety Hook allows benign commands: PASS
  - Anchor MCP server JSON-RPC initialize: PASS
  - Anchor MCP server tools/list: PASS
  - Anchor MCP server tools/call (anchor_state): PASS
  - Anchor MCP server tools/call (agyos_find_skill): PASS
  - bin/agyos find skill search CLI: PASS
  - Agent Council Bun test suite (59 passing tests): PASS
  - 8 AGYOS Plugins validated (`agyos-aegis`, `agyos-anchor`, `agyos-business-creative`, `agyos-council`, `agyos-polyglot`, `agyos-security`, `agyos-seo`, `agyos-verification`): PASS
  - Anchor state validation script: PASS
  - Merged skills catalog (>400 skills in .agents/skills): PASS (1,838 skills)
  - Merged rules catalog (>120 rules in .agents/rules): PASS (162 rules)
  - AGYOS master logo exists in assets/agyos-logo.svg: PASS
  - bin/agyos executable exists and functional: PASS
  - Tiered skills manifest exists and valid: PASS
  - Fast-path state bypass functional: PASS
- `bin/gate-check.sh`: PASS (monotonicity preserved)
- `python3 scripts/build_tiered_skills_manifest.py`: PASS (1,838 skills, 399 Tier 1, 1,439 Tier 2)
- `python3 scripts/build_docs_data.py`: PASS (1,838 skills cataloged into docs data)

## Blockers
None. 100% operational under single AGYOS branding.

## One Exact Next Command
```bash
bin/agyos verify
```
