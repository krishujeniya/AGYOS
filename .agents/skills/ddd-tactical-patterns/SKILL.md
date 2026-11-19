---
name: ddd-tactical-patterns
description: "Apply DDD tactical patterns in code using entities, value objects, aggregates, repositories, and domain events with explicit invariants."
risk: safe
source: self
tags: "[ddd, tactical, aggregates, value-objects, domain-events]"
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "ddd-tactical-patterns"
sections[7]:
  - "\n"
  - "# DDD Tactical Patterns\n\n"
  - "## Use this skill when\n\n- Translating domain rules into code structures.\n- Designing aggregate boundaries and invariants.\n- Refactoring an anemic model into behavior-rich domain objects.\n- Defining repository contracts and domain event boundaries.\n\n"
  - "## Do not use this skill when\n\n- You are still defining strategic boundaries.\n- The task is only API documentation or UI layout.\n- Full DDD complexity is not justified.\n\n"
  - "## Instructions\n\n1. Identify invariants first and design aggregates around them.\n2. Model immutable value objects for validated concepts.\n3. Keep domain behavior in domain objects, not controllers.\n4. Emit domain events for meaningful state transitions.\n5. Keep repositories at aggregate root boundaries.\n\nIf detailed checklists are needed, open `references/tactical-checklist.md`.\n\n"
  - "## Example\n\n```typescript\nclass Order {\n  private status: \"draft\" | \"submitted\" = \"draft\";\n\n  submit(itemsCount: number): void {\n    if (itemsCount === 0) throw new Error(\"Order cannot be submitted empty\");\n    if (this.status !== \"draft\") throw new Error(\"Order already submitted\");\n    this.status = \"submitted\";\n  }\n}\n```\n\n"
  - "## Limitations\n\n- This skill does not define deployment architecture.\n- It does not choose databases or transport protocols.\n- It should be paired with testing patterns for invariant coverage.\n"
