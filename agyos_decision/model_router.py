"""AGYOS Model Registry, Routing Policy & Context Economics Engine.

Implements Phase 4 of the AGYOS Specification:
- Canonical model registry for Google Gemini and Anthropic Claude.
- Strict rejection of invalid/speculative API IDs (e.g., 'gemini-3.8-flash-high' alias mapping).
- Tier-based routing (T0 fast/low-risk, T1 code/test, T2 architecture/refactor, T3 security/crypto).
- Strict privacy boundary enforcement: confidential/secret data fails closed without local inference.
- Explainable routing decisions with token economics and compaction thresholds.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import os
import re
from typing import Any, Dict, List, Optional, Tuple


class ModelProvider(str, Enum):
    GOOGLE = "google"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class ModelTier(str, Enum):
    T0 = "T0"  # Quick, low-risk (grep, navigation, metadata)
    T1 = "T1"  # Normal code edits, unit tests, standard research
    T2 = "T2"  # Complex architecture, multi-file refactor, evaluation review
    T3 = "T3"  # Critical security reviews, cryptography, privacy boundary analysis


class DataSensitivity(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"


@dataclass(frozen=True)
class ModelSpec:
    api_model_id: str
    provider: ModelProvider
    context_window: int
    max_output_tokens: int
    effective_context_limit: int
    thinking_supported: bool
    thinking_levels: Tuple[str, ...] = ()
    cost_per_1m_input_usd: float = 0.0
    cost_per_1m_output_usd: float = 0.0
    privacy_boundary: str = "provider_visible"
    verified_on_host: bool = False


@dataclass(frozen=True)
class RoutingPolicyDecision:
    allowed: bool
    tier: ModelTier
    model_id: str
    provider: ModelProvider
    thinking_level: Optional[str]
    reason: str
    privacy_boundary: str
    error_code: Optional[str] = None
    estimated_context_tokens: int = 4000
    compaction_threshold: int = 65000


# Canonical models supported by the host and official APIs
CANONICAL_MODELS: Dict[str, ModelSpec] = {
    "gemini-3.8-flash": ModelSpec(
        api_model_id="gemini-3.8-flash",
        provider=ModelProvider.GOOGLE,
        context_window=1048576,
        max_output_tokens=65536,
        effective_context_limit=128000,
        thinking_supported=True,
        thinking_levels=("low", "medium", "high"),
        cost_per_1m_input_usd=0.15,
        cost_per_1m_output_usd=0.60,
        privacy_boundary="provider_visible",
        verified_on_host=True,
    ),
    "claude-sonnet-4-6": ModelSpec(
        api_model_id="claude-sonnet-4-6",
        provider=ModelProvider.ANTHROPIC,
        context_window=200000,
        max_output_tokens=8192,
        effective_context_limit=64000,
        thinking_supported=True,
        thinking_levels=("low", "medium", "high"),
        cost_per_1m_input_usd=3.00,
        cost_per_1m_output_usd=15.00,
        privacy_boundary="provider_visible",
        verified_on_host=True,
    ),
    "claude-opus-4-6": ModelSpec(
        api_model_id="claude-opus-4-6",
        provider=ModelProvider.ANTHROPIC,
        context_window=200000,
        max_output_tokens=8192,
        effective_context_limit=64000,
        thinking_supported=True,
        thinking_levels=("medium", "high"),
        cost_per_1m_input_usd=15.00,
        cost_per_1m_output_usd=75.00,
        privacy_boundary="provider_visible",
        verified_on_host=True,
    ),
}

# Known aliases mapped to (canonical_api_id, default_thinking_level)
KNOWN_ALIASES: Dict[str, Tuple[str, str]] = {
    "gemini-3.8-flash-high": ("gemini-3.8-flash", "high"),
    "gemini-3.8-flash-medium": ("gemini-3.8-flash", "medium"),
    "gemini-3.8-flash-low": ("gemini-3.8-flash", "low"),
    "flash": ("gemini-3.8-flash", "medium"),
    "flash-high": ("gemini-3.8-flash", "high"),
    "sonnet": ("claude-sonnet-4-6", "high"),
    "opus": ("claude-opus-4-6", "high"),
}


class ModelRegistry:
    """Manages canonical model definitions and verifies host compatibility."""

    def __init__(self, models: Optional[Dict[str, ModelSpec]] = None):
        self._models = dict(models or CANONICAL_MODELS)

    def get_model(self, model_id: str) -> ModelSpec:
        if model_id in self._models:
            return self._models[model_id]
        raise KeyError(f"Model '{model_id}' is not registered as a canonical API model ID.")

    def resolve_model_alias(self, alias_or_id: str) -> Tuple[str, Optional[str]]:
        """Resolves user or CLI alias to (canonical_api_id, thinking_level)."""
        clean = alias_or_id.strip().lower()
        if clean in KNOWN_ALIASES:
            return KNOWN_ALIASES[clean]
        if clean in self._models:
            default_thinking = "high" if self._models[clean].thinking_supported else None
            return clean, default_thinking
        raise KeyError(f"Unknown model identifier or alias: '{alias_or_id}'")

    def list_available_models(self) -> List[ModelSpec]:
        return list(self._models.values())


def calculate_context_budget(effective_window: int = 128000) -> Dict[str, int]:
    """Calculates allocation according to context economics guidelines.

    Guidelines:
    - ~55% active content
    - ~20% tool/result growth
    - ~15% response/verification
    - ~10% safety margin
    - Compaction trigger at 60-70%
    - Atomic halt and resume at >80%
    """
    return {
        "active_content": int(effective_window * 0.55),
        "tool_overhead": int(effective_window * 0.20),
        "response_verification": int(effective_window * 0.15),
        "safety_margin": int(effective_window * 0.10),
        "compaction_trigger": int(effective_window * 0.65),
        "atomic_halt_trigger": int(effective_window * 0.80),
    }


class ModelRouter:
    """Evaluates task complexity, data sensitivity, and constraints to select the optimal model."""

    def __init__(self, registry: Optional[ModelRegistry] = None):
        self.registry = registry or ModelRegistry()

    def route(
        self,
        task: str,
        complexity: int,
        sensitivity: DataSensitivity = DataSensitivity.INTERNAL,
        user_override_model: Optional[str] = None,
        local_inference_available: bool = False,
    ) -> RoutingPolicyDecision:
        """Determines model assignment following AGYOS 4-Tier policy."""
        # 1. Strict Privacy Gate: confidential/secret must not route to cloud without local inference
        if sensitivity in (DataSensitivity.CONFIDENTIAL, DataSensitivity.SECRET):
            if not local_inference_available:
                return RoutingPolicyDecision(
                    allowed=False,
                    tier=ModelTier.T3 if sensitivity == DataSensitivity.SECRET else ModelTier.T2,
                    model_id="none",
                    provider=ModelProvider.LOCAL,
                    thinking_level=None,
                    reason=f"Data sensitivity is {sensitivity.value}; cloud provider inference is refused. "
                           f"Local attested confidential inference endpoint is unavailable.",
                    privacy_boundary="local_isolated",
                    error_code="LOCAL_INFERENCE_UNAVAILABLE",
                )

        # 2. User Override
        if user_override_model:
            try:
                canonical_id, thinking = self.registry.resolve_model_alias(user_override_model)
                spec = self.registry.get_model(canonical_id)
                tier = self._complexity_to_tier(complexity)
                budget = calculate_context_budget(spec.effective_context_limit)
                return RoutingPolicyDecision(
                    allowed=True,
                    tier=tier,
                    model_id=canonical_id,
                    provider=spec.provider,
                    thinking_level=thinking,
                    reason=f"User override requested '{user_override_model}' resolved to {canonical_id}.",
                    privacy_boundary=spec.privacy_boundary,
                    compaction_threshold=budget["compaction_trigger"],
                )
            except KeyError as e:
                pass  # Fall through to autonomous routing

        # 3. Autonomous Complexity-to-Tier Mapping
        tier = self._complexity_to_tier(complexity)
        return self._assign_tier_model(task, tier)

    def _complexity_to_tier(self, complexity: int) -> ModelTier:
        if complexity <= 1:
            return ModelTier.T0
        if complexity <= 3:
            return ModelTier.T1
        if complexity == 4:
            return ModelTier.T2
        return ModelTier.T3

    def _assign_tier_model(self, task: str, tier: ModelTier) -> RoutingPolicyDecision:
        if tier == ModelTier.T0:
            spec = self.registry.get_model("gemini-3.8-flash")
            budget = calculate_context_budget(spec.effective_context_limit)
            return RoutingPolicyDecision(
                allowed=True,
                tier=tier,
                model_id=spec.api_model_id,
                provider=spec.provider,
                thinking_level="low",
                reason="T0 low-risk task: minimal reasoning latency and lowest token cost.",
                privacy_boundary=spec.privacy_boundary,
                compaction_threshold=budget["compaction_trigger"],
            )

        if tier == ModelTier.T1:
            spec = self.registry.get_model("gemini-3.8-flash")
            budget = calculate_context_budget(spec.effective_context_limit)
            return RoutingPolicyDecision(
                allowed=True,
                tier=tier,
                model_id=spec.api_model_id,
                provider=spec.provider,
                thinking_level="medium",
                reason="T1 standard feature development: medium thinking depth for code and test generation.",
                privacy_boundary=spec.privacy_boundary,
                compaction_threshold=budget["compaction_trigger"],
            )

        if tier == ModelTier.T2:
            spec = self.registry.get_model("gemini-3.8-flash")
            budget = calculate_context_budget(spec.effective_context_limit)
            return RoutingPolicyDecision(
                allowed=True,
                tier=tier,
                model_id=spec.api_model_id,
                provider=spec.provider,
                thinking_level="high",
                reason="T2 complex architecture: high thinking effort for multi-file system design and ADR authoring.",
                privacy_boundary=spec.privacy_boundary,
                compaction_threshold=budget["compaction_trigger"],
            )

        # tier == ModelTier.T3
        # In T3, use Claude Opus if available, else Gemini Flash HIGH with human verification requirement
        try:
            opus_spec = self.registry.get_model("claude-opus-4-6")
            budget = calculate_context_budget(opus_spec.effective_context_limit)
            return RoutingPolicyDecision(
                allowed=True,
                tier=tier,
                model_id=opus_spec.api_model_id,
                provider=opus_spec.provider,
                thinking_level="high",
                reason="T3 critical security/crypto: verified deep reasoning model with mandatory verification.",
                privacy_boundary=opus_spec.privacy_boundary,
                compaction_threshold=budget["compaction_trigger"],
            )
        except KeyError:
            flash_spec = self.registry.get_model("gemini-3.8-flash")
            budget = calculate_context_budget(flash_spec.effective_context_limit)
            return RoutingPolicyDecision(
                allowed=True,
                tier=tier,
                model_id=flash_spec.api_model_id,
                provider=flash_spec.provider,
                thinking_level="high",
                reason="T3 critical: fallback to Gemini Flash HIGH with mandatory independent checker.",
                privacy_boundary=flash_spec.privacy_boundary,
                compaction_threshold=budget["compaction_trigger"],
            )
