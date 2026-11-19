---
name: ddd-strategic-design
description: "Design DDD strategic artifacts including subdomains, bounded contexts, and ubiquitous language for complex business domains."
risk: safe
source: self
tags: "[ddd, strategic-design, bounded-context, ubiquitous-language]"
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "ddd-strategic-design"
sections[8]:
  - "\n"
  - "# DDD Strategic Design\n\n"
  - "## Use this skill when\n\n- Defining core, supporting, and generic subdomains.\n- Splitting a monolith or service landscape by domain boundaries.\n- Aligning teams and ownership with bounded contexts.\n- Building a shared ubiquitous language with domain experts.\n\n"
  - "## Do not use this skill when\n\n- The domain model is stable and already well bounded.\n- You need tactical code patterns only.\n- The task is purely infrastructure or UI oriented.\n\n"
  - "## Instructions\n\n1. Extract domain capabilities and classify subdomains.\n2. Define bounded contexts around consistency and ownership.\n3. Establish a ubiquitous language glossary and anti-terms.\n4. Capture context boundaries in ADRs before implementation.\n\nIf detailed templates are needed, open `references/strategic-design-template.md`.\n\n"
  - "## Required artifacts\n\n- Subdomain classification table\n- Bounded context catalog\n- Glossary with canonical terms\n- Boundary decisions with rationale\n\n"
  - "## Examples\n\n```text\nUse @ddd-strategic-design to map our commerce domain into bounded contexts,\nclassify subdomains, and propose team ownership.\n```\n\n"
  - "## Limitations\n\n- This skill does not produce executable code.\n- It cannot infer business truth without stakeholder input.\n- It should be followed by tactical design before implementation.\n"
