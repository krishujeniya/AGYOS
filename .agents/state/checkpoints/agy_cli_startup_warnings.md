# AGY CLI startup warning repairs
Goal: Remove startup metadata and hook warnings while preserving command permissions.

## Gate: IMPLEMENT
Scope: Skill assets, planning frontmatter, 17 rule headers, two discovered READMEs, workspace config, JSON reference, hook responses, tests and handoff.
Authorization: Operator requested warning removal and clarified AGY CLI startup.

```json
{"gate":"IMPLEMENT","iteration":1,"status":"LOCAL_REPAIRS_VERIFIED","tdd_evidence":"Startup tests initially failed with 37 failures and 1 decoding error; notification injection test failed before its fix. Final: 12 passed.","verified":true,"main_checks_passed":34,"main_checks_failed":0,"structural_checks_passed":7,"python_sources_compiled":866,"python_compile_warnings":0}
```

## Gate: VERIFY
Independent checker startup_checker: twelve tests, shell syntax, diff hygiene and source review passed. No actionable regression remained. Native macOS execution was unavailable; subprocess construction was mocked.

Quiz:
1. Why does PostToolUse return {}? Its protobuf schema has no permission decision; PreToolUse has a separate decision schema.
2. Why allow rather than auto_approve? Allow delegates to existing permissions and other hooks.
3. How are titles kept out of executable AppleScript? A fixed script reads strings through argv.

Maker answers accepted by checker. Operator spot-check and host remediation remain pending; the overall gate is not marked complete.

No-prompt startup has no skill, rule, workflow or hook parsing warnings. Remaining: relative GeminiDir fallback, AppArmor sandbox restriction, account credit balance. Temporary directory override did not resolve the fallback. No security restriction was disabled; no model call was made.

Legacy eval failed two cases because its fixture directory is absent. Council type checking lacks bun-types. Neither check is marked passed.

Evidence and exact next command: AI_HANDOFF.md.
