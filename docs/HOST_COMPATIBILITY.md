# Host compatibility checkpoint

Status: **M0 incomplete; runtime mediation is unverified.** The operator approved the implementation plan, which requires separate authorization for paid model calls.

On 2026-11-05, `agy --version` returned **1.5.1**, newer than the 1.5.0 used for the research audit. `agy --help`, `agy agents --help`, and `agy mcp --help` ran successfully. These commands establish CLI availability and advertised command-line flags, not the model's tool schema, hook behavior, subagent inheritance, or cancellation.

The official [hooks reference](https://antigravity.google/docs/hooks), [custom-subagents reference](https://antigravity.google/docs/subagents), and [headless reference](https://antigravity.google/docs/cli/headless) describe candidate interfaces. Actual 1.5.1 behavior must be verified in a disposable workspace before treating the existing hook as an enforcement boundary. In particular, `scripts/hooks/authorizer.py` reads `taskContract`, which is not established as authenticated host authority. A subsequent local fix removed the bypass using a truthy `outbox_token` for matched command patterns. Its file-backup argument handling still does not include the documented `TargetFile` field.

An offline ACP `initialize` handshake using `agy acp --disable-telemetry` and temporary app-data and Gemini directories returned protocol version 1 and agent version 1.5.1. It advertised session and prompt capabilities but no tool inventory or hook enforcement evidence. No session prompt or paid call was made. Pending checks: capture the host's actual tool inventory and arguments; test harmless hook denial and failure behavior; test subagent permission inheritance and cancellation; verify whether all relevant effects are mediated. Any unsupported capability must remain disabled in an autonomous execution mode; that mode is not implemented or certified here.

Next: obtain a separately authorized spending ceiling and run the disposable host probe described in `docs/RESEARCH_PLAN.md` M0. Do not treat this record as an M0 pass.
