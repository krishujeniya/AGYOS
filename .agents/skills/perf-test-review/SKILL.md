---
name: perf-test-review
description: "Review performance benchmarks and tests for valid, repeatable measurements. Use when checking a performance regression, optimization claim, benchmark setup, or timing-sensitive test."
risk: unknown
source: community
date_added: "2026-02-27"
prompt-source: prompt.toon
---
skill: "perf-test-review"
sections[4]:
  - "\n"
  - "# Performance test review\n\nReview the validity of the measurement before recommending an optimization.\n\n"
  - "## Workflow\n\n1. Identify the metric, workload, environment, and performance claim. Ask for missing inputs when they change the conclusion.\n2. Locate the benchmark command, fixture or dataset, setup and teardown, warm-up behavior, repetitions, and recorded raw results.\n3. Check whether the test measures the intended work. Look for shared-resource contention, network variance, cache state, noisy clocks, nondeterministic inputs, hidden setup work, and assertions tied to arbitrary timing thresholds.\n4. Establish comparable baseline measurements and rerun the same workload under the same environment. Report sample count and distribution; do not compare unrelated runs or invent a baseline.\n5. Separate correctness tests from performance measurements. Keep performance thresholds tied to a documented service objective or stable project baseline.\n6. If the measurement is invalid, propose the smallest test-harness correction. Change application code only when requested and when the measurements support the hypothesis.\n\n"
  - "## Output\n\nReport the claim, workload, environment, benchmark command, comparable baseline measurements, observed distribution, test validity issues, and confidence. State “unmeasured” when comparable evidence is unavailable; do not claim a speedup from a single timing.\n"
