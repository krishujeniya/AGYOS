# AGYOS Engineering Quality Audit — 2026-11-08

Scope: the main branch, with evidence from selected high-risk source files and CI. This is not a complete manual audit of every file.

## Defects corrected

| Priority | Problem found | Source | Fix |
| --- | --- | --- | --- |
| Critical | Caller-supplied authorized flags/outbox tokens could override payment and other R3 restrictions | scripts/hooks/authorizer.py | Refuse such flags; pending trusted approval proof, block R3 |
| High | Pre-write snapshots could include unrelated paths and symlinks, and private file permissions were not guaranteed | scripts/hooks/authorizer.py | Limit to bounded regular repo files, no symlinks, unique filenames, private permissions and fail-closed errors |
| High | OS safety hook treated malformed events and unexpected errors as allowed tool calls | scripts/hooks/agy_os_hook.py | Reject malformed, non-object, oversized, incorrectly typed requests and unexpected pretool exceptions |
| High | Malformed MCP JSON was silently dropped or could dereference absent arguments | mcp/state-server.cjs, mcp/agyos-state-server.cjs | JSON-RPC validation, input bounds, explicit errors |
| High | MCP exception details could disclose local paths and secret-related errors | MCP state servers | Generic external tool errors and no raw stack traces |
| Medium | MCP root detection assumed a .git checkout and could traverse toward the filesystem root | MCP state servers | Resolve root relative to the installed server module |
| Low | Sysinfo returned a hardcoded obsolete skill count | MCP state servers | Derive count from current indexed catalog |
| Medium | Unit tests lacked negative cases for approval spoofing and protocol errors | scripts/tests | Add security, malformed input and snapshot regression tests |

## Important unresolved problems

| Priority | Finding | Status and necessary engineering |
| --- | --- | --- |
| P0 | There is no trusted end-to-end outbox approval verifier; R3 operations must not accept model-controlled metadata | **Blocked safely** until independent authenticated approval exists |
| P0 | AGYOS is not entirely end-to-end encrypted; workflow state, logs, checkpoints, ECC memory, cloud tools and hosted model prompts remain outside encrypted exchange | **Open**; requires per-boundary migration, threat modeling and host verification |
| P0 | External inference services need readable prompts | **Trust boundary**; use approved local inference or independently attested confidential execution where applicable |
| P1 | Encrypted message files lack ratcheting, replay defense, identity discovery and independent security audit | **Open**; review protocol design before high-assurance use |
| P1 | Old publicly committed state cannot be protected retroactively | **Open**; assess historical secret exposure and rotate credentials if needed |
| P1 | Encrypted private memory requires local vault initialization/key FD at startup | **Open deployment step**, intentionally not auto-initialized with predictable secrets |
| P1 | Cross-harness ECC memory is a separate storage format | **Open**; compatibility-preserving migration and rollback needed |
| P1 | Existing heuristic keyword checks do not substitute for trusted tool-capability enforcement | **Open**; implement least-privilege host tool grants and verified task contracts |
| P1 | Thousands of discovered skills cannot all be assumed trusted or compatible | **Partial**; review provenance, isolate executable skills, test selective activation |
| P2 | CI cannot validate the user's installed agy host, optional network tools, Bun Agent Council, cloud or IoT operations | **Open**; run host-specific acceptance tests with disposable fixtures |
| P2 | Duplicated MCP server modules can drift | **Partially mitigated** by synchronized patches; future consolidation needs compatibility tests |
| P2 | README and TRACKER include historical skill counts and test-pass claims | **Open**; publish dated generated capability counts instead of undated assertions |
| P2 | No end-to-end functional benchmark proves user task completion from natural-language requests | **Open**; add routing, execution and independent verification receipts |
| P2 | Memory/performance behavior on 4GB Ubuntu is unmeasured | **Open**; measure RSS, startup time, indexing and execution before optimization |

## Verification standards

CI: .github/workflows/ci.yml. Checks: Python syntax, generated catalog drift, scripts/tests Python regressions and Node encrypted-exchange/vault/MCP tests. These tests do **not** prove entire-OS encryption or live tool integration.

Only claim verified changes once CI passes on the exact latest main commit. Never claim every defect in 9,000+ tracked objects has been inspected.

## Follow-up implementation criteria

1. All external irreversible actions require a separate trusted approval, not a JSON flag or text token supplied in an agent tool request.
2. Encrypt state/checkpoint/telemetry consumers without breaking rollback or governance; do not silently migrate old files.
3. Run the live agy CLI, MCP server, plugin checks, Bun council tests, and full smoke workflows on the actual Ubuntu installation.
4. Add a security review of cryptographic key lifecycle, group identity, replay resistance and incident recovery.
5. Keep source citations and reproducible tests for each finding.

The present audit is a verified bounded hardening pass, not a comprehensive certification.
