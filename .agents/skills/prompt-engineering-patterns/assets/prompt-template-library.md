# Prompt patterns

Use these as adaptable AGYOS starting points. Keep only the fields that affect the task.

## Research

```text
Question: [specific question]
Scope: [time, region, population, or system]
Sources: [required source quality or allowed sources]
Return: findings, source links, uncertainty, and open questions.
Separate directly supported claims from inference.
```

## Code change

```text
Goal: [requested change]
Relevant paths: [known paths, if any]
Constraints: [compatibility, safety, scope]
Acceptance criteria: [observable behavior]
Verification: [project-approved checks]
Report: changed paths, actual check results, and remaining work.
```

## Data extraction

```text
Extract: [defined fields]
Output format: [schema]
Missing values: [representation]
Source record:
<record>
[input data]
</record>
```

## Editing

```text
Audience: [reader]
Purpose: [what the text should accomplish]
Keep: [meaning, terms, or facts to preserve]
Change: [specific editing request]
Return: [format]
Do not add unsupported claims.
```

These patterns do not override the user's request, repository rules, or permission boundaries.
