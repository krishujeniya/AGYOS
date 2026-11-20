---
trigger: model_decision
description: "Cross-role SDLC handoff contract specifying envelope fields, evidence links, and status lifecycle."
---

# AGYOS Handoff Contract

## Envelope

Every cross-role handoff is one TOON file at `.agents/handoffs/<handoff_id>.toon` with the fields: handoff_id, from_role, to_role, phase, gate, artifacts[], evidence[], created_at, expires_at, status, response_note.

## Lifecycle

- status moves open -> accepted | rejected; rejected requires response_note; expired handoffs do not satisfy any gate.
- An accepted handoff without evidence[] pointers is a defect: acceptance is evidence-linked.

## Placement

- Phase-scoped handoffs cite exactly one SDLC phase; continuous duties use phase: standing.
- Gates consume handoffs; a gate rule (see agyos-gate-legal-clearance.toon) names the handoff type and the artifact keys it checks.
