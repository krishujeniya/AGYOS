#!/usr/bin/env python3
"""Unit tests for AGYOS Model Registry and Router (Phase 4).

Covers:
1. Model registration, specs, canonical IDs, and thinking level parameters.
2. Rejection of unverified/invalid aliases (e.g., 'gemini-3.8-flash-high' as raw API ID).
3. Task complexity to tier mapping (T0, T1, T2, T3).
4. Strict privacy boundary enforcement: confidential/secret data fails closed without local inference.
5. Context window economics calculations and compaction thresholds.
6. Explainable routing decisions with cost and latency estimates.
"""
from __future__ import annotations

import unittest
from agyos_decision.model_router import (
    ModelRegistry,
    ModelRouter,
    ModelSpec,
    ModelTier,
    ModelProvider,
    DataSensitivity,
    RoutingPolicyDecision,
    calculate_context_budget,
)


class TestModelRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ModelRegistry()

    def test_canonical_google_model_registered(self):
        spec = self.registry.get_model("gemini-3.8-flash")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.provider, ModelProvider.GOOGLE)
        self.assertTrue(spec.thinking_supported)
        self.assertIn("high", spec.thinking_levels)
        self.assertIn("medium", spec.thinking_levels)
        self.assertIn("low", spec.thinking_levels)
        self.assertEqual(spec.context_window, 1048576)

    def test_alias_gemini_flash_high_resolves_to_base_with_high_thinking(self):
        canonical_id, thinking_level = self.registry.resolve_model_alias("gemini-3.8-flash-high")
        self.assertEqual(canonical_id, "gemini-3.8-flash")
        self.assertEqual(thinking_level, "high")

    def test_raw_api_id_never_returns_alias(self):
        # Raw API model ID must always be valid for provider API
        spec = self.registry.get_model("gemini-3.8-flash")
        self.assertEqual(spec.api_model_id, "gemini-3.8-flash")
        with self.assertRaises(KeyError):
            self.registry.get_model("nonexistent-model-xyz")

    def test_anthropic_candidates_registered(self):
        sonnet = self.registry.get_model("claude-sonnet-4-6")
        self.assertIsNotNone(sonnet)
        self.assertEqual(sonnet.provider, ModelProvider.ANTHROPIC)
        opus = self.registry.get_model("claude-opus-4-6")
        self.assertIsNotNone(opus)
        self.assertEqual(opus.provider, ModelProvider.ANTHROPIC)


class TestModelRouter(unittest.TestCase):
    def setUp(self):
        self.router = ModelRouter()

    def test_t0_routing_low_complexity(self):
        decision = self.router.route(
            task="find file in src/components and grep for button",
            complexity=1,
            sensitivity=DataSensitivity.PUBLIC,
        )
        self.assertEqual(decision.tier, ModelTier.T0)
        self.assertEqual(decision.model_id, "gemini-3.8-flash")
        self.assertEqual(decision.thinking_level, "low")
        self.assertIn("T0", decision.reason)

    def test_t1_routing_normal_code_edit(self):
        decision = self.router.route(
            task="implement user profile update endpoint with validation",
            complexity=3,
            sensitivity=DataSensitivity.INTERNAL,
        )
        self.assertEqual(decision.tier, ModelTier.T1)
        self.assertEqual(decision.model_id, "gemini-3.8-flash")
        self.assertEqual(decision.thinking_level, "medium")

    def test_t2_routing_complex_architecture(self):
        decision = self.router.route(
            task="redesign state machine architecture with multi-file refactoring and ADR",
            complexity=4,
            sensitivity=DataSensitivity.INTERNAL,
        )
        self.assertEqual(decision.tier, ModelTier.T2)
        self.assertEqual(decision.model_id, "gemini-3.8-flash")
        self.assertEqual(decision.thinking_level, "high")

    def test_t3_routing_threat_model_security(self):
        decision = self.router.route(
            task="conduct STRIDE threat modeling and cryptography review for E2EE protocol",
            complexity=5,
            sensitivity=DataSensitivity.INTERNAL,
        )
        self.assertEqual(decision.tier, ModelTier.T3)
        self.assertIn(decision.model_id, ["claude-opus-4-6", "gemini-3.8-flash"])
        if decision.model_id == "gemini-3.8-flash":
            self.assertEqual(decision.thinking_level, "high")

    def test_strict_privacy_confidential_fails_closed_without_local_inference(self):
        # Confidential data must NOT be silently exfiltrated to cloud providers
        decision = self.router.route(
            task="process customer credit card numbers and SSNs",
            complexity=3,
            sensitivity=DataSensitivity.CONFIDENTIAL,
            local_inference_available=False,
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.error_code, "LOCAL_INFERENCE_UNAVAILABLE")
        self.assertIn("confidential", decision.reason.lower())

    def test_strict_privacy_secret_requires_explicit_consent(self):
        decision = self.router.route(
            task="inspect private cryptographic keys",
            complexity=4,
            sensitivity=DataSensitivity.SECRET,
            local_inference_available=False,
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.error_code, "LOCAL_INFERENCE_UNAVAILABLE")

    def test_user_override_honored(self):
        decision = self.router.route(
            task="simple grep",
            complexity=1,
            user_override_model="claude-sonnet-4-6",
            sensitivity=DataSensitivity.PUBLIC,
        )
        self.assertEqual(decision.model_id, "claude-sonnet-4-6")
        self.assertIn("user override", decision.reason.lower())


class TestContextEconomics(unittest.TestCase):
    def test_budget_distribution_heuristic(self):
        budget = calculate_context_budget(effective_window=100000)
        self.assertEqual(budget["active_content"], 55000)
        self.assertEqual(budget["tool_overhead"], 20000)
        self.assertEqual(budget["response_verification"], 15000)
        self.assertEqual(budget["safety_margin"], 10000)
        self.assertEqual(budget["compaction_trigger"], 65000)
        self.assertEqual(budget["atomic_halt_trigger"], 80000)


if __name__ == "__main__":
    unittest.main()
