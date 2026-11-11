"""Public routing must survive JSON transport and ranking optimization."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from agyos_decision import skills_router as router

ROOT = Path(__file__).resolve().parents[2]
INTEGRATION_TASK = 'Review code and find problems before release'


class RoutingContractTests(unittest.TestCase):
    def test_fallback_is_json_without_cached_metadata(self):
        decision = json.loads(json.dumps(router.decide_skill('hello')))
        self.assertEqual(decision['selection_status'], 'fallback')
        self.assertEqual(decision['primary_skill'], 'agyos-decision')
        self.assertFalse(any(k.startswith('_') for k in decision['candidates'][0]))

    def test_integration_decision_is_json_and_has_only_public_candidate_fields(self):
        decision = router.decide_skill(INTEGRATION_TASK)
        decoded = json.loads(json.dumps(decision))
        self.assertEqual(decoded['primary_skill'], 'code-reviewer')
        expected = {'rank', 'name', 'description', 'path', 'tier', 'score', 'confidence'}
        for candidate in decoded['candidates']:
            self.assertEqual(set(candidate), expected)
        decision['candidates'][0]['description'] = 'caller mutation'
        self.assertNotEqual(router.decide_skill(INTEGRATION_TASK)['candidates'][0]
                            ['description'], 'caller mutation')

    def test_integration_cli_json_round_trip(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/agyos-decision.py'),
             INTEGRATION_TASK, '--json', '--runbook'],
            text=True, capture_output=True, cwd='/tmp', timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload['primary_skill'], 'code-reviewer')
        self.assertEqual(payload['execution_status'], 'runbook_returned')

    def test_integration_mcp_json_round_trip(self):
        request = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {
            'name': 'agyos_decision', 'arguments': {'task': INTEGRATION_TASK}}}
        result = subprocess.run(
            ['node', str(ROOT / 'mcp/state-server.cjs')],
            input=json.dumps(request) + '\n', text=True, capture_output=True,
            check=True, timeout=30,
        )
        payload = json.loads(json.loads(result.stdout)['result']['content'][0]['text'])
        self.assertEqual(payload['primary_skill'], 'code-reviewer')
        self.assertEqual(payload['execution_status'], 'pending_runbook_read')

    def test_rankings_match_full_sort_including_ties_and_limits(self):
        catalog = [
            {'name': f'python-test-{i:03}', 'description': 'python testing',
             'path': f'.agents/skills/python-test-{i:03}', 'tier': 2}
            for i in reversed(range(100))
        ]
        for limit in (1, 5, 100, 150):
            query = 'python test'
            domain = router.classify_domain(query)[0]
            expected = sorted(catalog, key=lambda s: (
                -router.score_skill_fit(s, query, domain), s['name']))[:limit]
            actual = router.select_best_skills(query, catalog, limit)
            self.assertEqual([s['name'] for s in actual], [s['name'] for s in expected])
            self.assertEqual([s['rank'] for s in actual], list(range(1, len(actual) + 1)))


if __name__ == '__main__':
    unittest.main()
