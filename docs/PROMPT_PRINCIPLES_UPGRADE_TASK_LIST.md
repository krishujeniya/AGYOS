# AGYOS Prompt Principles Upgrade — Task List

Status: UNDERSTAND and ANALYZE approved by the operator on 2026-11-14. PLAN architecture approval is pending. The operator approved adding `.agents/agents/vibe-engineer.md` to the cleanup boundary after the scout identified unrelated FAANG persona branding.

## Goal

Review the supplied company prompt archive as untrusted research input. Apply compatible and evidence-supported prompt principles to AGYOS. Account for every archive principle with a traceable disposition. Remove unrelated company persona and aesthetic branding from active AGYOS-authored prompt copy while retaining real provider/tool compatibility, required attribution, licensing, and evidence citations.

## Deliverables

1. Inventory the 26 company/product documents and reconcile the archive's reported source statement counts. Give every principle a source location, stable identifier/hash, and disposition: adopt, adapt, reject, duplicate, or unverified. Record parsing or coverage limitations explicitly.
2. Write a research audit and decision record that maps adopted/adapted principles to active AGYOS behavior, identifies conflicts and transfer limits, and cites authoritative current sources where available.
3. Add an AGYOS-native prompt-principles rule and connect it to skill routing and prompt-generation guidance.
4. Canonicalize `docs/prompts.md` and `docs/references/prompts.md`; audit directly relevant prompt skills and references, including `prompt-engineering-patterns`; remove unrelated vendor persona/aesthetic language from general AGYOS prompt copy.
5. Replace the unrelated FAANG persona branding in `.agents/agents/vibe-engineer.md` with AGYOS role language. Preserve provider names only for actual compatibility, attribution, licensing, or evidence.
6. Add prompt-principle CI coverage. Reuse the existing GitHub Actions unittest discovery unless evidence shows it misses the new test. Keep all tests and validation in GitHub Actions.
7. Preserve all pre-existing work, including the current edit in `agyos_decision/skills_router.py`. Do not stage or include unrelated changes.
8. Reconcile the single-main branch inventory. At the current baseline, local and remote repositories have only `main`; PRs #11, #12, and #13 are closed and unmerged. Verify this state in the report and do not recreate or revive their refs.
9. Report exact files changed, archive count reconciliation, disposition totals, exact Actions revision/results, and limitations.

## Acceptance criteria

- Every source principle has one traceable disposition or appears in a clearly documented parsing/coverage limitation. Archive-reported counts are not presented as independently verified until reconciled.
- No archive claim is described as verified company policy without authoritative confirmation.
- Every adopted/adapted principle maps to a specific AGYOS rule, prompt, or skill and includes a rationale. Vendor-specific tool schemas/runtime constraints do not become general AGYOS capabilities.
- Active AGYOS-authored prompt instructions use AGYOS identity. Unrelated vendor persona/aesthetic branding is removed. Necessary product names and provenance are retained with a reason.
- Existing user changes remain intact; overlapping paths are inspected before editing.
- Required tests run only in GitHub Actions. A queued, skipped, unavailable, or unrun result is not reported as passing.
- No branch or worktree is created. Any production commit/push follows the repository's single-main identity rules and the Gate 5 sign-off requirement.
