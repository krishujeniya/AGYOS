"""Offline budget boundary cases; no provider calls or real clock sleeps."""

import unittest
from decimal import Decimal, localcontext

from agyos_decision.state_ledger import RunBudgetTracker


class BudgetHardeningTests(unittest.TestCase):
    def test_money_limits_ignore_ambient_decimal_precision(self):
        for precision in (4, 28):
            with self.subTest(precision=precision), localcontext() as context:
                context.prec = precision
                tracker = RunBudgetTracker(total_usd=1, reserve_ratio=0)
                tracker.consume(usd=1)
                with self.assertRaises(ValueError):
                    tracker.consume(usd=Decimal('0.00000000000000000000000000001'))
                self.assertEqual(tracker.used_usd, 1)

    def test_sub_float_precision_money_is_still_enforced(self):
        tracker = RunBudgetTracker(total_usd=Decimal('1.00000000000000000001'),
                                   reserve_ratio=0)
        tracker.consume(usd=1)
        tracker.consume(usd=Decimal('0.00000000000000000001'))
        with self.assertRaises(ValueError):
            tracker.consume(usd=Decimal('0.00000000000000000001'))

    def test_small_charges_accumulate_and_stop_at_execution_limit(self):
        tracker = RunBudgetTracker(total_usd=0.01)
        for _ in range(8):
            tracker.consume(usd=0.001)
        self.assertEqual(tracker.used_usd, 0.008)
        with self.assertRaises(ValueError):
            tracker.consume(usd=0.001)
        self.assertEqual(tracker.used_usd, 0.008)

    def test_decimal_boundary_is_not_binary_float_drift(self):
        tracker = RunBudgetTracker(total_usd=0.375)
        tracker.consume(usd=0.1)
        tracker.consume(usd=0.2)
        self.assertEqual(tracker.used_usd, 0.3)
        tracker.consume_reserve(usd=Decimal('0.075'))
        self.assertEqual(tracker.used_usd, 0.375)
        with self.assertRaises(ValueError):
            tracker.consume_reserve(usd=Decimal('0.000001'))

    def test_invalid_usage_is_rejected_without_changing_state(self):
        cases = (
            {'tokens': -1}, {'tokens': 1.5}, {'tokens': True},
            {'usd': -0.001}, {'usd': float('nan')},
            {'usd': float('inf')}, {'usd': '0.01'}, {'usd': True},
            {'tool_calls': -1}, {'tool_calls': 0.5}, {'tool_calls': True},
        )
        for method in ('consume', 'consume_reserve'):
            for kwargs in cases:
                with self.subTest(method=method, kwargs=kwargs):
                    tracker = RunBudgetTracker()
                    tracker.consume(tokens=10, usd=0.001, tool_calls=1)
                    with self.assertRaises(ValueError):
                        getattr(tracker, method)(**kwargs)
                    self.assertEqual((tracker.used_tokens, tracker.used_usd,
                                      tracker.used_tool_calls), (10, 0.001, 1))

    def test_invalid_configuration_is_rejected(self):
        cases = (
            {'total_tokens': -1}, {'total_tokens': 1.5},
            {'total_tool_calls': True}, {'total_seconds': -1},
            {'total_usd': float('nan')}, {'total_usd': float('inf')},
            {'total_usd': -0.1}, {'reserve_ratio': -0.1},
            {'reserve_ratio': 1}, {'reserve_ratio': float('nan')},
        )
        for kwargs in cases:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                RunBudgetTracker(**kwargs)

    def test_reserve_rejects_unrecognized_purpose(self):
        tracker = RunBudgetTracker()
        for purpose in ('execution', '', None, ['verification']):
            with self.subTest(purpose=purpose), self.assertRaises(ValueError):
                tracker.consume_reserve(tokens=1, purpose=purpose)
        self.assertEqual(tracker.used_tokens, 0)

    def test_tool_capacity_is_reserved_and_total_cap_is_enforced(self):
        tracker = RunBudgetTracker(total_tool_calls=5)
        tracker.consume(tool_calls=4)
        with self.assertRaises(ValueError):
            tracker.consume(tool_calls=1)
        tracker.consume_reserve(tool_calls=1, purpose='rollback')
        with self.assertRaises(ValueError):
            tracker.consume_reserve(tool_calls=1)
        self.assertEqual(tracker.used_tool_calls, 5)

    def test_elapsed_time_reserves_recovery_window(self):
        now = [100.0]
        tracker = RunBudgetTracker(total_seconds=10, clock=lambda: now[0])
        now[0] = 107.9
        tracker.consume(tokens=1)
        now[0] = 108.0
        with self.assertRaises(ValueError):
            tracker.consume(tokens=1)
        tracker.consume_reserve(tokens=1, purpose='rollback')
        now[0] = 110.0
        with self.assertRaises(ValueError):
            tracker.consume_reserve(tokens=1)
        self.assertEqual(tracker.used_tokens, 2)

    def test_invalid_clock_cannot_bypass_deadline(self):
        for value in (float('nan'), float('inf'), -1):
            now = [0.0]
            tracker = RunBudgetTracker(clock=lambda: now[0])
            now[0] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                tracker.consume(tokens=1)
            self.assertEqual(tracker.used_tokens, 0)

    def test_failed_multidimensional_charge_is_atomic(self):
        tracker = RunBudgetTracker()
        tracker.consume(tokens=1, usd=0.01, tool_calls=1)
        with self.assertRaises(ValueError):
            tracker.consume(tokens=1, usd=0.01, tool_calls=41)
        self.assertEqual((tracker.used_tokens, tracker.used_usd,
                          tracker.used_tool_calls), (1, 0.01, 1))


if __name__ == '__main__':
    unittest.main()
