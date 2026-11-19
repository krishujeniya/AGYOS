---
name: dbt-transformation-patterns
description: "Production-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing."
risk: none
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "dbt-transformation-patterns"
sections[7]:
  - "\n"
  - "# dbt Transformation Patterns\n\nProduction-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing.\n\n"
  - "## Use this skill when\n\n- Building data transformation pipelines with dbt\n- Organizing models into staging, intermediate, and marts layers\n- Implementing data quality tests and documentation\n- Creating incremental models for large datasets\n- Setting up dbt project structure and conventions\n\n"
  - "## Do not use this skill when\n\n- The project is not using dbt or a warehouse-backed workflow\n- You only need ad-hoc SQL queries\n- There is no access to source data or schemas\n\n"
  - "## Instructions\n\n- Define model layers, naming, and ownership.\n- Implement tests, documentation, and freshness checks.\n- Choose materializations and incremental strategies.\n- Optimize runs with selectors and CI workflows.\n- If detailed patterns are required, open `resources/implementation-playbook.md`.\n\n"
  - "## Resources\n\n- `resources/implementation-playbook.md` for detailed dbt patterns and examples.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
