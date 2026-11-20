---
trigger: model_decision
description: "Release candidate merge gate requiring accepted license-clearance handoff and SBOM verification."
---

# Gate: Legal Clearance (license gate)

## Trigger

- Any release candidate whose merge set adds or upgrades a dependency, on every release train.

## Inputs

- SBOM artifact from scripts/generate_sbom.py in the validate job.
- gate-verdict.toon produced by the oss-license-risk-audit skill (PASS | PASS-WITH-REVIEW | BLOCK).

## Rule

- Merging requires an accepted license-clearance handoff from role-ip-patent-attorney with evidence pointing at the SBOM run and the verdict file.
- The council job fails when the release candidate lacks the handoff; the policy-guard hook blocks merge-class tool calls when the gate:legal-cleared label is absent.
- BLOCK verdicts clear only through a recorded exception in oss-policy.toon or a dependency change; never through silence.
