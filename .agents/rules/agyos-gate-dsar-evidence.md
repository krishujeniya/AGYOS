---
trigger: model_decision
description: "Architecture review gate requiring subject-data inventory paths and TIA recommendations for personal data."
---

# Gate: DSAR Evidence (architecture registration)

## Trigger

- Any ARCHITECTURE-phase diagram that adds a system, region or vendor touching personal data.

## Rule

- The architecture deliverable must declare, per new system, the subject-data inventory path that the dsar-pipeline skill reads; a system without an inventory path does not pass review.
- Cross-border flows additionally require a tia-report.toon recommendation (go, go-with-measures, no-go) referenced from the diagram's decision record.

## Why

- DSAR fulfillment is only as complete as the system-of-record map; registering inventory paths at architecture time is what keeps the pipeline runnable without quarterly archaeology.
