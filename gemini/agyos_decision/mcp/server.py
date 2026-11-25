"""MCP stdio server exposing the Roxx typed-decision tools.

Part of the optional ``roxx[mcp]`` extra. Speaks MCP over stdio, so it can be
wired to any MCP client (OpenClaw, Claude Desktop, cursor, ...):

    roxx-mcp-server
    python -m roxx.mcp.server

Environment (same meaning as roxx.serve where it exists):
  ROXX_DEVICE   torch device for the checkpoints (value goes straight to torch)
  ROXX_PRELOAD  "0" to build the checkpoints lazily instead of at startup (default on)
  ROXX_MODELS   comma list to preload; MCP default is "english,multilingual" so
                typed-decisions stays lazy (in roxx.serve an empty value preloads all)
  ROXX_THREADS  cap torch intra-op threads (CPU inference); keep <= physical cores
"""

from __future__ import annotations

import json
import os
import sys
import threading
from importlib import metadata as _metadata
from typing import Any

try:
    from mcp.server.mcpserver import MCPServer
    from mcp.server.mcpserver.exceptions import ToolError as McpToolError
except ImportError as exc:  # mcp extra not installed
    raise ImportError(
        "the roxx[mcp] extra (mcp>=2.2.0) is required to run the MCP server: "
        "pip install 'roxx[mcp]'"
    ) from exc

# roxx.serve only imports os/typing at module level, so reusing its helpers
# keeps one meaning for ROXX_PRELOAD / ROXX_THREADS across the package.
from roxx.serve import _apply_thread_limit, _env_bool

from .device import env_device
from .tools import (
    ToolError,
    roxx_predict,
    roxx_preset,
    roxx_route,
    roxx_status,
)

try:
    _ROXX_VERSION = _metadata.version("roxx")
except Exception:  # running from a source checkout without install metadata
    import roxx as _roxx

    _ROXX_VERSION = getattr(_roxx, "__version__", "")

server = MCPServer("roxx", version=_ROXX_VERSION)

_ROUTER: Any = None
_ROUTER_LOCK = threading.Lock()

# MCP default preload list. roxx.serve preloads every checkpoint when ROXX_MODELS
# is empty; MCP keeps typed-decisions lazy on purpose (it is ~as big as the other
# two, and auto-routing never selects it).
_DEFAULT_MODELS = ("english", "multilingual")

# Shared usage guardrails for the three decision tools. roxx_status reports
# instead of deciding, so it does not carry them.
_GUARDRAILS = (
    "Use for structured decisions only: choice (finite labels), score (ordinal rubric), "
    "noul (calibrated P(true)). One forward pass ~33ms (GPU) / ~200ms (CPU). "
    "No text generation, so no hallucination. Do NOT use for open Q&A, summarization, "
    "rewriting, code, or multi-hop reasoning. Do NOT use for >20-option choice "
    "questions without shortlisting."
)


def _models_from_env() -> list[str]:
    """Preload list from ROXX_MODELS (roxx.serve contract: comma list of names).

    Unlike roxx.serve, an empty value falls back to english+multilingual instead
    of "every checkpoint"; see the module docstring.
    """
    raw = os.environ.get("ROXX_MODELS", "").strip()
    names = [m.strip() for m in raw.split(",") if m.strip()]
    return names or list(_DEFAULT_MODELS)


def _ensure_router() -> Any:
    """Build the Router from the environment, following the roxx.serve contract.

    ROXX_DEVICE / ROXX_PRELOAD / ROXX_THREADS keep the same meaning as in
    roxx.serve (the helpers are reused, not duplicated). ROXX_MODELS follows the
    serve comma-list but defaults to english+multilingual here, so
    typed-decisions stays lazy. The global is only set once the router is fully
    built, so a failed preload stays retriable on the next tool call, and
    construction errors surface as ToolError payloads instead of being swallowed.
    """
    global _ROUTER
    if _ROUTER is not None:
        return _ROUTER
    with _ROUTER_LOCK:
        if _ROUTER is not None:
            return _ROUTER
        try:
            from roxx import Router
        except Exception as exc:
            raise ToolError("internal_error", f"cannot import roxx: {exc}") from exc
        try:
            _apply_thread_limit()
            router = Router(device=env_device())
            if _env_bool("ROXX_PRELOAD", True):
                router.preload(_models_from_env())
        except Exception as exc:
            raise ToolError("internal_error", f"router construction failed: {exc}") from exc
        _ROUTER = router
        return router


def _dump(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _router_or_error() -> Any:
    """The resident Router, or an McpToolError carrying the ToolError payload."""
    try:
        return _ensure_router()
    except ToolError as exc:
        raise McpToolError(_dump({"error": exc.code, "message": exc.message})) from exc


def _preset_builder(attr_name: str) -> dict:
    import roxx

    builder = getattr(roxx, attr_name, None)
    if builder is None:
        raise ToolError("internal_error", f"roxx.{attr_name} is not available in this version")
    return builder()


def _wrap(fn, **kwargs) -> str:
    """Run fn; raise McpToolError so isError=true AND the JSON payload is preserved.

    mcp 2.x wraps any non-ToolError Exception as UnexpectedToolError("Error executing
    tool <name>") and redacts the original message. Only
    mcp.server.mcpserver.exceptions.ToolError keeps our JSON on the wire.
    """
    try:
        return _dump(fn(**kwargs))
    except ToolError as exc:
        raise McpToolError(_dump({"error": exc.code, "message": exc.message})) from exc
    except McpToolError:
        raise
    except Exception as exc:
        raise McpToolError(
            _dump({"error": "internal_error", "message": f"{type(exc).__name__}: {exc}"})
        ) from exc


@server.tool(name="roxx_status")
def roxx_status_tool() -> str:
    """Report the device actually in use per loaded checkpoint (or the configured preference, flagged as such, when nothing is loaded), torch CUDA availability, loaded checkpoints, and package versions."""
    return _wrap(roxx_status, router=_ROUTER, preload=_env_bool("ROXX_PRELOAD", True))


@server.tool(
    name="roxx_route",
    description=(
        "Decide which Roxx checkpoint would answer, without running a forward pass. "
        "Use this to explain routing (english vs multilingual vs typed-decisions) to the user. "
        + _GUARDRAILS
    ),
)
def roxx_route_tool(state: dict, questions: dict) -> str:
    """Decide which Roxx checkpoint would answer, without running a forward pass."""
    router = _router_or_error()
    return _wrap(roxx_route, state=state, questions=questions, router=router)


@server.tool(
    name="roxx_predict",
    description=(
        "Answer typed questions (choice/score/noul) over any state in one forward pass. "
        "questions: {name: {type: 'choice'|'score'|'noul', instructions: str, criteria?: object|array}}. "
        "Returns answers with confidence, routing metadata and, when it can be read, the real "
        "device of the checkpoint that answered. "
        + _GUARDRAILS
    ),
)
def roxx_predict_tool(state: dict, questions: dict, model: str = "auto") -> str:
    """Answer typed questions (choice/score/noul) over any state in one forward pass."""
    router = _router_or_error()
    return _wrap(
        roxx_predict,
        state=state,
        questions=questions,
        model=model,
        router=router,
    )


@server.tool(
    name="roxx_preset",
    description=(
        "Run a built-in workflow: 'guard' | 'moderation' | 'triage' | 'model_router'. "
        "Use when the task matches one of those presets instead of hand-writing questions. "
        + _GUARDRAILS
    ),
)
def roxx_preset_tool(preset: str, state: dict) -> str:
    """Run a built-in workflow: 'guard' | 'moderation' | 'triage' | 'model_router'."""
    router = _router_or_error()
    return _wrap(
        roxx_preset,
        preset=preset,
        state=state,
        router=router,
        preset_builder=_preset_builder,
    )


def main() -> None:
    # Windows without Developer Mode cannot create HF cache symlinks (WinError
    # 1314). On POSIX the cache uses symlinks by default and disabling them
    # would copy the files and double disk use, so the override is Windows-only.
    if os.name == "nt":
        os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")
        os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
    if _env_bool("ROXX_PRELOAD", True):
        try:
            _ensure_router()
        except Exception as exc:
            print(f"[roxx-mcp] preload failed (will retry on demand): {exc}", file=sys.stderr)
    server.run()


if __name__ == "__main__":
    main()
