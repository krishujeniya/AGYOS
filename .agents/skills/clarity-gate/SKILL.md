---
# agentskills.io compliant frontmatter
name: clarity-gate
risk: unknown
source: community
version: 2.1.3
description: >
  Pre-ingestion verification for epistemic quality in RAG systems.
  Ensures documents are properly qualified before entering knowledge bases.
  Produces CGD (Clarity-Gated Documents) and validates SOT (Source of Truth) files.
author: "Krish Ujeniya"
license: CC-BY-4.0
repository: https://github.com/frmoretto/clarity-gate
triggers:
  - clarity gate
  - check for hallucination risks
  - can an LLM read this safely
  - review for equivocation
  - verify document clarity
  - pre-ingestion check
  - cgd verify
  - sot verify
capabilities:
  - document-verification
  - epistemic-quality
  - rag-preparation
  - cgd-generation
  - sot-validation
outputs:
  - type: cgd
    extension: .cgd.md
    spec: docs/CLARITY_GATE_FORMAT_SPEC.md
spec_version: "2.1"
prompt-source: prompt.toon
---
skill: "clarity-gate"
sections[2]:
  - "# Clarity Gate v2.1\n\nPre-ingestion verification for epistemic quality in RAG systems. Ensures documents are properly qualified before entering knowledge bases. Produces CGD (Clarity-Gated Documents) and validates SOT (Source of Truth) files.\n\n"
  - "## Workflow\n\n1. Confirm the request fits this skill and identify the required inputs and output constraints.\n2. Read the applicable sections in [the full runbook](references/FULL_RUNBOOK.md).\n3. Check version-sensitive instructions against authoritative current documentation; label claims that cannot be verified.\n4. Get any required approval before paid, destructive, external, or user-visible actions not already authorized.\n5. Follow the relevant procedure using the project’s existing tools and conventions. Ask for missing inputs instead of inventing values.\n6. Verify the result with available checks and report what ran, what passed, and any remaining uncertainty.\n"
