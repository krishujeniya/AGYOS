# AGYOS Prompt Principles Upgrade — Task List

Status: UNDERSTAND approved by the operator on 2026-11-14. ANALYZE scope approval is pending.

## Goal

Review the supplied 26-company prompt archive and improve AGYOS-authored prompt guidance using source-grounded, compatible principles. Remove unrelated company persona and aesthetic branding from AGYOS-authored prompt material while retaining technical identifiers, compatibility details, licenses, and source attribution.

## Deliverables

1. Inventory all 26 company documents and record each source principle with a source location and a disposition: adopt, adapt, reject, duplicate, or unverified. Include a short reason for each disposition. Do not represent community-extracted material as company-authored or officially verified.
2. Write a research and decision record that maps accepted/adapted principles to AGYOS behavior, identifies conflicts and transfer limits, and cites authoritative current sources where available.
3. Add an AGYOS-native prompt-principles rule and connect it to AGYOS skill discovery and prompt-generation guidance.
4. Audit and improve the prompt library and directly relevant prompt-engineering skills. Remove unrelated vendor persona/aesthetic branding from AGYOS-authored text; preserve provider names only where needed for compatibility, attribution, or accurate source discussion.
5. Add CI-only checks or evaluation fixtures for the prompt guidance and brand boundary. Preserve existing assertions and generated outputs.
6. Report exact files changed, source coverage, accepted and rejected principle counts, CI revision/results, and limitations. Keep uncommitted pre-existing work intact.

## Acceptance criteria

- All source documents in the supplied archive are inventoried; every counted source statement has a traceable disposition or an explicitly recorded parsing/coverage limitation.
- No archive claim is described as verified company policy without authoritative confirmation.
- Every adopted or adapted principle has a concrete AGYOS enforcement surface and rationale; vendor-specific tool schemas and runtime limitations are not treated as AGYOS capabilities.
- AGYOS-authored prompt instructions use AGYOS identity and voice. The audit preserves justified technical, licensing, and provenance references.
- Existing user changes remain intact; changes to already modified files are reconciled rather than overwritten.
- Required checks run only in GitHub Actions. A queued, skipped, unavailable, or unrun CI result is not reported as passing.
- No push, merge, release, or deployment occurs without separate authorization.
