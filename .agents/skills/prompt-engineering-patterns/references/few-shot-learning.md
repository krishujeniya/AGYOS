# Few-shot examples

Examples can clarify a target format, label boundary, tone, or edge case when a written rule is ambiguous. They also consume context and can bias outputs toward incidental details. Use them only when they improve the task's stated behavior.

## Select examples

- Match the task and format the user needs.
- Include meaningful variation, including a boundary case when it affects the rule.
- Keep examples correct, representative, and free of irrelevant details.
- Do not assume a fixed number of examples is best. Test a smaller and larger set when example count materially affects the result.
- Protect private or sensitive data; use synthetic examples when real records are unnecessary.

## Evaluate

Compare prompts with and without examples on the same representative inputs. Define task-specific pass criteria first, inspect errors as well as successful cases, and report the scope of the evaluation. A small sample does not establish a universal performance gain.

## Example shape

```text
Input: [representative input]
Output: [correct output in the required format]

Input: [meaningful edge case]
Output: [correct handling of that edge case]

Now process this input using the same rule:
[new input]
```
