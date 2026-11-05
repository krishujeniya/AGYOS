# Skill routing consistency

Baseline: main / 8e15b83; existing router edits retained.
Scope and acceptance: docs/SKILL_ROUTING.md. User requested implementation and push.

```json
{"iteration": 1, "gate": "IMPLEMENT", "red": {"command": "python3 -m unittest scripts.tests.test_skill_routing -q", "tests": 14, "failures": 122, "errors": 39}, "evidence": "/tmp/agyos-routing-red.log", "next": "repair catalog metadata and routing"}
```

```json
{"iteration": 1, "gate": "VERIFY", "status": "PASS", "python_tests": 73, "routing_catalog_tests": 17, "council_tests": 59, "host_checks": 51, "skill_headers": 1862, "rules": 141, "syntax": "PASS", "generated_reproducibility": "PASS", "independent_review": "PASS", "gitleaks": "outgoing history and tracked diff clean; staged scan precedes commit", "limitations": "Host invocation and specialist procedure quality are not guaranteed by routing checks"}
```

```json
{"iteration": 1, "gate": "VERIFY", "status": "PASS", "python_tests": 75, "routing_catalog_tests": 17, "council_tests": 59, "host_checks": 51, "skill_headers": 1862, "rules": 141, "syntax": "PASS", "generated_reproducibility": "PASS", "independent_review": "PASS", "gitleaks": "outgoing history and tracked diff clean; staged scan precedes commit", "limitations": "Host invocation and specialist procedure quality are not guaranteed by routing checks"}
```
