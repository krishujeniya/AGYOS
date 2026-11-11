#!/usr/bin/env python3
"""Offline routing timings and fixed capability checks; never invokes an agent."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agyos_decision.skills_router import decide_skill, load_catalog

CASES = (
    ('fix python crash', 'diagnosing-bugs'),
    ('animate modal transition', 'motion-patterns'),
    ('write literature review', 'agyos-academic-research'),
    ('optimize slow Python code latency', 'benchmark-optimization-loop'),
    ('audit JWT security', 'security-review'),
    ('design database schema migration', 'database-design'),
    ('hello', 'agyos-decision'),
    ('use agyos-founder-guide', 'agyos-founder-guide'),
    ('Review code and find problems before release', 'code-reviewer'),
    ('Design an edge AI deployment architecture', 'ml-engineer'),
)


def summarize(samples):
    ordered = sorted(samples)
    return {'p50_ms': statistics.median(samples),
            'p95_ms': ordered[math.ceil(len(samples) * 0.95) - 1],
            'samples_ms': samples}


def measure(repeats):
    load_catalog.cache_clear()
    start = time.perf_counter()
    catalog = load_catalog()
    cold_ms = (time.perf_counter() - start) * 1000
    for query, _ in CASES:
        decide_skill(query)
    samples, errors, selected = [], [], []
    for iteration in range(repeats):
        for query, expected in CASES:
            start = time.perf_counter()
            decision = decide_skill(query)
            samples.append((time.perf_counter() - start) * 1000)
            if decision['primary_skill'] != expected:
                errors.append({'iteration': iteration, 'task': query,
                               'error': 'unexpected_primary'})
            try:
                json.dumps(decision)
            except (TypeError, ValueError):
                errors.append({'iteration': iteration, 'task': query,
                               'error': 'not_json_serializable'})
            if iteration == 0:
                selected.append({'task': query, 'primary': decision['primary_skill'],
                                 'ranking': [(c['name'], c['score'])
                                             for c in decision['candidates']]})
    return {'catalog_entries': len(catalog), 'catalog_load_ms': cold_ms,
            'warm_decision': summarize(samples), 'errors': errors,
            'selected': selected,
            'ranking_sha256': hashlib.sha256(json.dumps(selected, sort_keys=True).encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats', type=int, default=30)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.repeats <= 1000:
        parser.error('--repeats must be between 1 and 1000')
    result = measure(args.repeats)
    result.update({
        'schema_version': 1, 'kind': 'offline_routing_microbenchmark',
        'timestamp_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'python': platform.python_version(), 'platform': platform.platform(),
        'revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'router_sha256': hashlib.sha256((ROOT / 'agyos_decision/skills_router.py').read_bytes()).hexdigest(),
        'repeats_per_case': args.repeats, 'provider_calls': 0,
        'limits': 'Warm in-process decisions; excludes import, JSON serialization time, CLI/MCP transport and model latency. Fixed development cases, not a held-out task-success evaluation.',
    })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('catalog_entries', 'catalog_load_ms', 'ranking_sha256')}))
    print(f"p50={result['warm_decision']['p50_ms']:.3f}ms p95={result['warm_decision']['p95_ms']:.3f}ms errors={len(result['errors'])}")
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
