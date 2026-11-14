# Task decomposition and answer checks

Complex tasks can benefit from explicit stages when the stages are part of the requested deliverable or reduce omissions. This is a task-structure choice, not a general guarantee of better reasoning. Model behavior varies; check current first-party guidance for a named integration.

## Write observable steps

For a multi-part analysis, describe the work product and checks rather than requesting private reasoning:

```text
Compare the two migration options using the supplied requirements.
Return a recommendation, the key trade-offs, supporting evidence, and unresolved assumptions.
Check that each stated requirement is addressed before returning the result.
```

For a numeric or logical task, ask for the result and a concise explanation or verification method when the user needs it. Do not ask for full hidden chain-of-thought or internal reasoning traces.

## When stages help

- The work has dependent outputs, such as inspect → compare → recommend.
- A required deliverable can be omitted unless called out.
- The answer needs a check against explicit criteria.

For a single clear task, a direct instruction may be enough. Avoid adding artificial stages or asking for visible reasoning when it does not help the user.

## Evidence

- [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Anthropic prompt engineering best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

These sources describe provider-specific guidance. Do not generalize their advice to every model or task.
