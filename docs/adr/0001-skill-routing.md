# Decision: shared skill discovery metadata and explicit runbook delivery

Status: accepted for local routing, 2026-11-05.

Multiple parsers had diverged: malformed YAML became placeholder descriptions,
documentation could outrank the runtime manifest, and language keywords displaced
task specialists. Returning a skill name did not establish that it was read.

Use one strict YAML parser for discovery metadata. Prefer a complete runtime
manifest, recover through documentation data or a physical scan, and constrain
paths to existing runbooks. Rank explicit skill IDs first, then task intent and
catalog evidence, with language keywords as supporting evidence. Unknown scope
uses the standard workflow; only explicit bounded low-risk work takes a fast path.

CLI and MCP may return the selected runbook, with delivery recorded separately
from execution. A shared rule governs all catalog entries. Generated indexes are
checked for drift in CI.

This keeps selection local and reproducible without model calls. The tradeoff is
keyword-based matching rather than semantic understanding. Scores are not
probabilities; an assistant must assess fit and apply relevant instructions.
Host invocation and permission enforcement remain separate responsibilities.
