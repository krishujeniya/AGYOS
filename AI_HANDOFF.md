# AGYOS handoff

## Task and revision

Skill consolidation, work-based renaming, and unbranded MCP unification. Branch `main`.

## Summary of Executed Changes

### 1. Unified Flat Skills Catalog
- Consolidated all skills into a single flat directory: `.agents/skills/` (1,837 skills).
- Removed all 8 plugin skill subdirectories (`.agents/plugins/*/skills/`).
- Removed stray duplicate `.agents/skills/SKILL.md` from catalog root.
- Removed duplicate skills (`agent-council`, `agent-council-nudge`).

### 2. Work-Based & Unbranded Skill Renaming (277 Skills Total)
- Renamed 156 skills in Pass 1 to strip branding prefixes (`aegis-`, `agyos-`, `baoyu-`, `agent-`, `claude-`, `stitch-`, `ejentum-`, `nerdzao-`, `ralphinho-`, `nanoclaw-`, `nasiko-`) and simplify compound prefixes.
- Renamed 121 skills in Pass 2 to replace persona/founder names (`andrej-karpathy`, `bill-gates`, `elon-musk`, `geoffrey-hinton`, `ilya-sutskever`, `sam-altman`, `steve-jobs`, `warren-buffett`, `yann-lecun*`, `uncle-bob-craft`, `emil-design-eng`), non-English names (`advogado-*`, `leiloeiro-*`, `junta-*`), cryptic codes (`adhx`, `design-md`, `agents-md`, `yes-md`), single-word generics (`accessibility`, `architecture`, `build`, `commit`, `database`, `debugger`, `development`, `documentation`), and `-skill` suffixes with explicit task names enabling zero-shot AI discovery.
- Updated `name:` frontmatter across all renamed `SKILL.md` files.

### 3. Flat Unbranded MCP Architecture
- Renamed `mcp/agyos-state-server.cjs` -> `mcp/state-server.cjs` (zero branding).
- Created backward-compatibility symlink `mcp/agyos-state-server.cjs -> state-server.cjs`.
- Removed nested example subdirectories (`mcp/examples/`).
- Updated `mcp/README.md` to document the flat, unbranded structure.
- Updated MCP invocations in `bin/agyos`, `scripts/agyos-verify.sh`, `scripts/agyos-init.sh`, `scripts/package_agyos_plugins.py`, `.agents/plugins/agyos-anchor/mcp_config.json`, `README.md`, and documentation.

### 4. Manifest and Reference Alignment
- Rebuilt `.agents/skills-manifest.json` from scratch with 1,837 verified skills.
- Corrected path mapping in `.agents/tier1-skills.json` and `docs/skills-data.json`.
- Removed unnecessary temporary files: `.agents/ecc-install-state.json` (405KB), stray `SKILL.md`, and all `__pycache__` directories.

## Checks Actually Run

- `bash scripts/agyos-verify.sh`: **34 PASSED, 0 FAILED** (complete verification suite passed).
- JSON-RPC stdio daemon tools query: `tools/list` and `tools/call (agyos_find_skill)` verified with 0 error codes.
- Broken path verification in tier 1 skills manifest: **0 broken paths**.
- Hardlink integrity check across `.agents/skills/` and `skills/`: verified synchronized.

## Exact next command

```bash
bash scripts/agyos-verify.sh
```
