---
name: ddd-context-mapping
description: "Map relationships between bounded contexts and define integration contracts using DDD context mapping patterns."
risk: safe
source: self
tags: "[ddd, context-map, anti-corruption-layer, integration]"
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "ddd-context-mapping"
sections[8]:
  - "\n"
  - "# DDD Context Mapping\n\n"
  - "## Use this skill when\n\n- Defining integration patterns between bounded contexts.\n- Preventing domain leakage across service boundaries.\n- Planning anti-corruption layers during migration.\n- Clarifying upstream and downstream ownership for contracts.\n\n"
  - "## Do not use this skill when\n\n- You have a single-context system with no integrations.\n- You only need internal class design.\n- You are selecting cloud infrastructure tooling.\n\n"
  - "## Instructions\n\n1. List all context pairs and dependency direction.\n2. Choose relationship patterns per pair.\n3. Define translation rules and ownership boundaries.\n4. Add failure modes, fallback behavior, and versioning policy.\n\nIf detailed mapping structures are needed, open `references/context-map-patterns.md`.\n\n"
  - "## Output requirements\n\n- Relationship map for all context pairs\n- Contract ownership matrix\n- Translation and anti-corruption decisions\n- Known coupling risks and mitigation plan\n\n"
  - "## Examples\n\n```text\nUse @ddd-context-mapping to define how Checkout integrates with Billing,\nInventory, and Fraud contexts, including ACL and contract ownership.\n```\n\n"
  - "## Limitations\n\n- This skill does not replace API-level schema design.\n- It does not guarantee organizational alignment by itself.\n- It should be revisited when team ownership changes.\n"
