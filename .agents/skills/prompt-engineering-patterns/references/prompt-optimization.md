# Prompt evaluation and revision

Treat prompt revisions as hypotheses. A wording change is useful only if it improves the result against the task's stated criteria without unacceptable trade-offs.

## Evaluation loop

1. Define the user-visible quality criteria and any hard constraints.
2. Select representative inputs, including known edge cases. Keep a separate set for confirming a change when the prompt is important or reused.
3. Record the baseline prompt, target model/version, settings, tools, and relevant input conditions.
4. Change one material instruction at a time where practical.
5. Compare outputs against the same rubric. Track errors, omissions, format compliance, latency, and cost only when relevant.
6. Keep a revision only when measured results support it; record limitations and conditions.

## Comparison record

```text
Prompt revision: [identifier]
Target and version: [if known]
Cases evaluated: [scope]
Criteria: [observable pass conditions]
Observed changes: [results]
Limitations: [unknowns and trade-offs]
Decision: [keep, revise, or revert]
```

Do not use a universal score threshold, claim a general accuracy gain from a narrow sample, or treat an LLM-generated score as ground truth without validation. Use CI for repository prompt checks when project rules require it.
