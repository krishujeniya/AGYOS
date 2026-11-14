# Prompt library runbook

Use these patterns as starting points, not finished universal prompts. Adapt them to the user's goal, supplied context, constraints, and requested output. Follow `.agents/rules/agyos-prompt-principles.md`.

## Reusable task patterns

### Code review

```text
Review the supplied change for correctness, security, and maintainability.
Prioritize actionable findings. For each finding, give its location, evidence, impact, and a minimal fix.
Separate confirmed defects from suggestions. If no issue is confirmed, say so and list unverified areas.
Change:
<change>
[input]
</change>
```

### Debugging

```text
Diagnose the reported failure from the supplied evidence.
Return the observed symptom, likely cause with evidence, smallest appropriate fix, and a verification plan.
Do not infer runtime results that were not observed.
Failure and relevant context:
<context>
[input]
</context>
```

### Technical explanation

```text
Explain [topic] to [audience] for [purpose].
Use [requested level of detail and format]. Define necessary terms and distinguish established facts from uncertainty.
```

### Refactoring

```text
Refactor [code or module] to improve [specific quality].
Preserve observable behavior unless a behavior change is explicitly requested.
Return the change, relevant trade-offs, and results from the approved verification path.
```

### Test design

```text
Design tests for [behavior] using [project conventions]. Cover expected behavior and the boundary cases that affect the contract.
Do not weaken existing checks. Identify any behavior that cannot be verified from the available interface.
```

### Research summary

```text
Research [question] using [source constraints].
Return a concise answer with direct source links, publication dates where relevant, uncertainty, and open questions.
Label inference separately from source-supported facts.
```

## Technique choices

- Add examples when a stable format or ambiguous category needs demonstration. Use representative examples; do not set a universal count.
- Add output schemas when downstream use requires predictable fields.
- Name stages when the task has dependencies or explicit deliverables.
- Use a role only when it changes the perspective or expertise needed. AGYOS is the default identity for AGYOS-authored prompts.
- Do not ask for hidden chain-of-thought. Request the result, supporting evidence, assumptions, or a concise verification summary as needed.

## Attribution

Some historical patterns in this community skill were inspired by [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts). This attribution records provenance; it does not imply endorsement or current compatibility. The AGYOS patterns above are rewritten and should be checked against project rules and current target documentation.
