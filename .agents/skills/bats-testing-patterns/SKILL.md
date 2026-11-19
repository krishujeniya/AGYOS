---
name: bats-testing-patterns
description: "Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities."
risk: unknown
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "bats-testing-patterns"
sections[7]:
  - "\n"
  - "# Bats Testing Patterns\n\nComprehensive guidance for writing comprehensive unit tests for shell scripts using Bats (Bash Automated Testing System), including test patterns, fixtures, and best practices for production-grade shell testing.\n\n"
  - "## Use this skill when\n\n- Writing unit tests for shell scripts\n- Implementing TDD for scripts\n- Setting up automated testing in CI/CD pipelines\n- Testing edge cases and error conditions\n- Validating behavior across shell environments\n\n"
  - "## Do not use this skill when\n\n- The project does not use shell scripts\n- You need integration tests beyond shell behavior\n- The goal is only linting or formatting\n\n"
  - "## Instructions\n\n- Confirm shell dialects and supported environments.\n- Set up a test structure with helpers and fixtures.\n- Write tests for exit codes, output, and side effects.\n- Add setup/teardown and run tests in CI.\n- If detailed examples are required, open `resources/implementation-playbook.md`.\n\n"
  - "## Resources\n\n- `resources/implementation-playbook.md` for detailed patterns and examples.\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
