"""Structured logging subsystem for Roxx.

Configurable via environment variables:
- ``ROXX_LOG_FORMAT``: "text" (default) or "json"
- ``ROXX_LOG_LEVEL``: "DEBUG", "INFO", "WARNING" (default), "ERROR", "CRITICAL"

Pure Python standard library; zero external dependencies.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time
from typing import Any, Dict, Optional

_INITIALIZED = False
_DEFAULT_LOGGER_NAME = "roxx"


class JsonFormatter(logging.Formatter):
    """Format log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt or "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        # Include extra structured fields if passed via extra={"extra_fields": {...}}
        extra = getattr(record, "extra_fields", None)
        if isinstance(extra, dict):
            for k, v in extra.items():
                if k not in payload:
                    payload[k] = v
        return json.dumps(payload, ensure_ascii=False)


class RoxxTextFormatter(logging.Formatter):
    """Format log records as clean prefixed text."""

    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()
        extra = getattr(record, "extra_fields", None)
        if isinstance(extra, dict) and extra:
            extra_str = " " + " ".join(f"{k}={v}" for k, v in extra.items())
            msg = f"{msg}{extra_str}"
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                msg = f"{msg}\n{record.exc_text}"
        return f"[{record.name}] {record.levelname}: {msg}"


def _get_configured_level() -> int:
    raw = os.environ.get("ROXX_LOG_LEVEL", "WARNING").strip().upper()
    return getattr(logging, raw, logging.WARNING)


def configure_logging(
    level: Optional[int] = None,
    log_format: Optional[str] = None,
    stream: Optional[Any] = None,
) -> None:
    """Configure root roxx logger formatting and level."""
    global _INITIALIZED
    logger = logging.getLogger(_DEFAULT_LOGGER_NAME)

    if level is None:
        level = _get_configured_level()
    logger.setLevel(level)

    if log_format is None:
        log_format = os.environ.get("ROXX_LOG_FORMAT", "text").strip().lower()

    if stream is None:
        stream = sys.stderr

    # Avoid duplicate handlers on re-configuration
    for h in list(logger.handlers):
        logger.removeHandler(h)

    handler = logging.StreamHandler(stream)
    handler.setLevel(level)

    if log_format == "json":
        formatter = JsonFormatter()
    else:
        formatter = RoxxTextFormatter()

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    _INITIALIZED = True


def get_logger(name: str = _DEFAULT_LOGGER_NAME) -> logging.Logger:
    """Return a logger child of the roxx namespace, auto-configured on first call."""
    global _INITIALIZED
    if not _INITIALIZED:
        configure_logging()
    if name == _DEFAULT_LOGGER_NAME or name.startswith(_DEFAULT_LOGGER_NAME + "."):
        return logging.getLogger(name)
    return logging.getLogger(f"{_DEFAULT_LOGGER_NAME}.{name}")


def log_event(
    logger: logging.Logger,
    level: int,
    message: str,
    *,
    trace_id: Optional[str] = None,
    model: Optional[str] = None,
    elapsed_ms: Optional[float] = None,
    **kwargs: Any,
) -> None:
    """Emit a log record with structured attributes."""
    extra: Dict[str, Any] = {}
    if trace_id is not None:
        extra["trace_id"] = trace_id
    if model is not None:
        extra["model"] = model
    if elapsed_ms is not None:
        extra["elapsed_ms"] = round(elapsed_ms, 2)
    extra.update(kwargs)

    logger.log(level, message, extra={"extra_fields": extra})
