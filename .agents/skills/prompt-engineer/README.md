# Prompt Engineer

This skill converts a user's intent into a prompt that is clear, scoped, and ready to use. It preserves the user's requirements and does not execute the prompt's requested task.

## Prompt fields

Use only the fields the task needs:

| Field | Include when it helps |
|---|---|
| Goal | The result the model should produce |
| Context | Facts or source material not otherwise available |
| Constraints | Boundaries that affect acceptable results |
| Process | Observable stages for dependent work |
| Output | Format, audience, and required fields |
| Examples | Representative cases that clarify a rule or format |

These fields are optional. A direct one-line request is enough for a simple task. No named framework guarantees a result.

## Drafting procedure

1. Read the full request and retain its intent, language, and stated requirements.
2. Identify material gaps. Ask only when a missing fact blocks a useful or safe prompt; otherwise make a low-risk assumption explicit.
3. Put the requested outcome first. Keep context separate from instructions when that reduces confusion.
4. Add roles, examples, ordered stages, schemas, or evaluation criteria only when they serve the task.
5. For multi-stage work, specify deliverables and completion checks. Ask for a concise answer or evidence where useful; never require hidden reasoning traces.
6. Review for invented facts, contradictory instructions, unnecessary wording, and names that do not serve compatibility, attribution, or evidence.
7. Return the prompt in the requested format and note material assumptions.

## Optional named structures

RTF, RISEN, RODES, RACE, RISE, STAR, SOAP, CLEAR, and GROW are labels some users may recognize for organizing roles, tasks, context, steps, audiences, or goals. They are optional. Select fields directly when a label adds no value. Chain-of-thought is not a request for private reasoning; ask for task steps or a concise verification summary instead.

## Evaluation

For prompts used repeatedly, compare a baseline and revised version on representative inputs. Define pass criteria before comparison, keep other conditions stable, and report only observed differences. Do not infer general accuracy or performance guarantees from a small sample.

## Related guidance

- [Prompt engineering skill](../prompt-engineering/SKILL.md)
- [AGYOS prompt principles](../../rules/agyos-prompt-principles.md)
- [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [OpenAI reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- [Anthropic prompt engineering](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
