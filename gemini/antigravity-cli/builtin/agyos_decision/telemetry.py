"""OpenTelemetry observability and tracing for Roxx.

Supports:
- Distributed tracing (W3C traceparent context propagation)
- GenAI semantic conventions (gen_ai.system, gen_ai.request.model, gen_ai.usage.input_tokens)
- Metrics (roxx.decisions, roxx.decision.latency_ms, roxx.tokens.input, roxx.errors)
- Seamless no-op fallback when OpenTelemetry is not installed or disabled.

Enable via:
    export ROXX_OTEL_ENABLED=1
or install ``opentelemetry-api`` and ``opentelemetry-sdk``.
"""
from __future__ import annotations

import os
import time
from contextlib import contextmanager
from typing import Any, Dict, Iterator, Optional

from .hooks import BaseHook, PredictContext
from .logging import get_logger, log_event

logger = get_logger("telemetry")

_OTEL_AVAILABLE = False
try:
    from opentelemetry import metrics as otel_metrics  # type: ignore[import-not-found]
    from opentelemetry import trace as otel_trace  # type: ignore[import-not-found]
    from opentelemetry.trace import Status, StatusCode  # type: ignore[import-not-found]
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator  # type: ignore[import-not-found]

    _OTEL_AVAILABLE = True
except ImportError:
    otel_trace = None  # type: ignore[assignment]
    otel_metrics = None  # type: ignore[assignment]
    Status = None  # type: ignore[assignment]
    StatusCode = None  # type: ignore[assignment]
    TraceContextTextMapPropagator = None  # type: ignore[assignment]


def is_otel_enabled() -> bool:
    """Return True if OpenTelemetry is installed and not explicitly disabled."""
    if not _OTEL_AVAILABLE:
        return False
    v = os.environ.get("ROXX_OTEL_ENABLED", "").strip().lower()
    if v in ("0", "false", "no", "off"):
        return False
    # If explicitly enabled, or if an otel TracerProvider has been configured by the caller
    if v in ("1", "true", "yes", "on"):
        return True
    try:
        # Check if a non-proxy tracer provider is registered
        provider = otel_trace.get_tracer_provider()
        return provider.__class__.__name__ != "ProxyTracerProvider"
    except Exception:
        return False


class _NoOpSpan:
    """Zero-overhead fallback span when OTEL is disabled or unavailable."""

    def set_attribute(self, key: str, value: Any) -> None:
        pass

    def set_attributes(self, attributes: Dict[str, Any]) -> None:
        pass

    def record_exception(self, exception: BaseException) -> None:
        pass

    def set_status(self, status: Any, description: Optional[str] = None) -> None:
        pass

    def end(self) -> None:
        pass

    def is_recording(self) -> bool:
        return False


class _NoOpTracer:
    @contextmanager
    def start_as_current_span(
        self,
        name: str,
        context: Optional[Any] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Iterator[_NoOpSpan]:
        yield _NoOpSpan()


class _NoOpCounter:
    def add(self, amount: int | float, attributes: Optional[Dict[str, Any]] = None) -> None:
        pass


class _NoOpHistogram:
    def record(self, amount: int | float, attributes: Optional[Dict[str, Any]] = None) -> None:
        pass


class _NoOpMeter:
    def create_counter(self, name: str, unit: str = "", description: str = "") -> _NoOpCounter:
        return _NoOpCounter()

    def create_histogram(self, name: str, unit: str = "", description: str = "") -> _NoOpHistogram:
        return _NoOpHistogram()


def get_tracer(name: str = "roxx") -> Any:
    """Return an OpenTelemetry tracer if enabled, otherwise a no-op tracer."""
    if is_otel_enabled():
        return otel_trace.get_tracer(name)
    return _NoOpTracer()


def get_meter(name: str = "roxx") -> Any:
    """Return an OpenTelemetry meter if enabled, otherwise a no-op meter."""
    if is_otel_enabled():
        return otel_metrics.get_meter(name)
    return _NoOpMeter()


# Metrics registry (created once per meter)
_METRICS: Dict[str, Any] = {}


def _get_metric_instruments() -> Dict[str, Any]:
    global _METRICS
    if _METRICS:
        return _METRICS
    meter = get_meter("roxx")
    _METRICS["decisions"] = meter.create_counter(
        "roxx.decisions",
        unit="1",
        description="Total number of System-1 decisions made",
    )
    _METRICS["latency"] = meter.create_histogram(
        "roxx.decision.latency_ms",
        unit="ms",
        description="Latency of System-1 decision inference in milliseconds",
    )
    _METRICS["input_tokens"] = meter.create_counter(
        "roxx.tokens.input",
        unit="1",
        description="Total number of input tokens processed across questions",
    )
    _METRICS["errors"] = meter.create_counter(
        "roxx.errors",
        unit="1",
        description="Total number of prediction or routing errors",
    )
    return _METRICS


def extract_trace_context(headers: Dict[str, str]) -> Optional[Any]:
    """Extract W3C trace context from request headers if available."""
    if not is_otel_enabled() or TraceContextTextMapPropagator is None:
        return None
    try:
        # Standardize header keys to lower case for W3C carrier
        carrier = {k.lower(): v for k, v in headers.items()}
        return TraceContextTextMapPropagator().extract(carrier=carrier)
    except Exception:
        return None


def inject_trace_context(carrier: Dict[str, str]) -> Dict[str, str]:
    """Inject current W3C trace context into carrier dict if available."""
    if not is_otel_enabled() or TraceContextTextMapPropagator is None:
        return carrier
    try:
        TraceContextTextMapPropagator().inject(carrier=carrier)
    except Exception:
        pass
    return carrier


class TelemetryHook(BaseHook):
    """Lifecycle hook for OpenTelemetry tracing, metrics, and structured logging.

    Attach to any Agent or Router:
        agent = roxx.load("krishujeniya/roxx", hooks=[TelemetryHook()])
    """

    def __init__(self, service_name: str = "roxx"):
        self.tracer = get_tracer(service_name)
        self.instruments = _get_metric_instruments()
        self._spans: Dict[str, Any] = {}

    def on_predict_start(self, ctx: PredictContext) -> None:
        if is_otel_enabled():
            span = self.tracer.start_span(
                "roxx.decision",
                attributes={
                    "gen_ai.system": "roxx",
                    "roxx.run_id": ctx.run_id,
                    "roxx.questions_count": len(ctx.questions) if ctx.questions else 0,
                },
            )
            self._spans[ctx.run_id] = span

    def on_route(self, ctx: PredictContext) -> None:
        span = self._spans.get(ctx.run_id)
        if span is not None:
            model = ctx.model or (ctx.decision.get("model") if ctx.decision else None)
            if model:
                span.set_attribute("gen_ai.request.model", model)
                span.set_attribute("roxx.checkpoint", model)
            if ctx.decision:
                reason = ctx.decision.get("reason")
                if reason:
                    span.set_attribute("roxx.route.reason", reason)

    def on_predict_end(self, ctx: PredictContext) -> None:
        model = ctx.model or "unknown"
        elapsed_ms = ctx.elapsed_ms if ctx.elapsed_ms is not None else (
            (time.perf_counter() - ctx.started_at) * 1000.0
        )
        input_tokens = ctx.usage.get("input_tokens", 0) if ctx.usage else 0

        # Record metrics
        instruments = _get_metric_instruments()
        instruments["decisions"].add(1, {"model": model})
        if elapsed_ms > 0:
            instruments["latency"].record(elapsed_ms, {"model": model})
        if input_tokens > 0:
            instruments["input_tokens"].add(input_tokens, {"model": model})

        # Structured log
        log_event(
            logger,
            20,  # logging.INFO
            f"Decision completed: model={model} questions={len(ctx.questions)} elapsed={elapsed_ms:.1f}ms",
            trace_id=ctx.run_id,
            model=model,
            elapsed_ms=elapsed_ms,
            input_tokens=input_tokens,
        )

        span = self._spans.pop(ctx.run_id, None)
        if span is not None:
            span.set_attribute("gen_ai.request.model", model)
            span.set_attribute("gen_ai.usage.input_tokens", input_tokens)
            span.set_attribute("gen_ai.usage.output_tokens", 0)
            span.set_attribute("roxx.elapsed_ms", elapsed_ms)
            if Status is not None and StatusCode is not None:
                span.set_status(Status(StatusCode.OK))
            span.end()

    def on_error(self, ctx: PredictContext) -> None:
        instruments = _get_metric_instruments()
        model = ctx.model or "unknown"
        err_type = type(ctx.error).__name__ if ctx.error else "UnknownError"
        instruments["errors"].add(1, {"model": model, "error_type": err_type})

        log_event(
            logger,
            40,  # logging.ERROR
            f"Decision failed: {ctx.error}",
            trace_id=ctx.run_id,
            model=model,
            error=str(ctx.error),
        )

        span = self._spans.pop(ctx.run_id, None)
        if span is not None:
            if ctx.error is not None:
                span.record_exception(ctx.error)
            if Status is not None and StatusCode is not None:
                span.set_status(Status(StatusCode.ERROR, str(ctx.error)))
            span.end()
