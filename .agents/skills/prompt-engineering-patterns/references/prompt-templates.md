# Prompt templates

Templates help when a task repeats and its variable fields are known. Keep only fields that change the requested result. A direct prompt is preferable when a template adds no value.

## General task template

```text
Goal: [requested result]
Context: [relevant facts or source material]
Constraints: [requirements and boundaries]
Output: [format, audience, and required fields]
```

Omit any line that is unnecessary. If a field contains quoted or retrieved text, label it as input data and preserve its source when relevant.

## Structured extraction

```text
Extract these fields from the supplied record: [field names and definitions].
Return [format or schema]. Use null or the stated missing-value marker when a field is absent.
Record:
<record>
[input data]
</record>
```

## Evidence-based summary

```text
Summarize the supplied material for [audience] in [requested format].
Separate source claims from verified facts and identify material gaps.
Material:
<source>
[input data]
</source>
```

## Reusable implementation request

```text
Goal: [specific change]
Repository context: [paths or constraints already known]
Acceptance criteria: [observable outcomes]
Verification: [approved commands or CI workflow]
Report: [changed paths, actual results, and remaining checks]
```

These are field examples, not mandatory sections or a named universal framework.
