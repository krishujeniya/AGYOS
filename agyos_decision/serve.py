"""HTTP server exposing Roxx over TypeSafe Jev's ``/v1/systemone`` wire protocol.

Roxx's ``predict()`` output is already schema-compatible with the Jev decision
API -- ``choice`` / ``score`` / ``noul`` answers and a ``{input_tokens,
output_tokens}`` usage block -- so a client written against Jev (for example the
`hs-jev` Haskell client) can point its ``baseUrl`` at this server and keep
working unchanged. All this module adds is the HTTP surface Roxx itself does not
ship: a ``POST /v1/systemone`` route, an optional bearer check, and a health
probe.

Configuration is entirely via environment variables so the same entry point
serves a laptop dev run and a systemd unit:

======================  ============================================  =========
env var                 meaning                                        default
======================  ============================================  =========
``ROXX_HOST``           bind address                                   0.0.0.0
``ROXX_PORT``           bind port                                      8000
``ROXX_DEVICE``         torch device for every checkpoint              (auto)
``ROXX_PRELOAD``        build the checkpoints at startup, not lazily   1
``ROXX_MODELS``         comma list to preload (english,multilingual,   (all)
                        typed-decisions); empty = every checkpoint
``ROXX_THREADS``        cap torch intra-op threads (CPU inference).    (torch
                        Keep <= physical cores; oversubscribing the     default)
                        logical/hyperthread count is a large regression.
``ROXX_AUTO_TASK``      auto-route to the typed-decisions checkpoint   0
``ROXX_API_KEY``        if set, require ``Authorization: Bearer <it>``  (none)
``ROXX_LOG_LEVEL``      uvicorn log level                              info
``ROXX_RATE_LIMIT``     sliding-window rate limit, e.g. "60/minute"    (none)
``ROXX_CORS_ENABLED``   enable CORS middleware                         0
``ROXX_CORS_ORIGINS``   comma list of allowed origins (e.g. "*")       *
``ROXX_SECURITY_HEADERS`` enable strict security headers (CSP, HSTS)  1
``ROXX_OTEL_ENABLED``   enable OpenTelemetry distributed tracing       (auto)
======================  ============================================  =========

Imports of heavy dependencies (fastapi, uvicorn, torch via Router) are all
deferred into the functions that need them, so ``import roxx.serve`` stays cheap
and touches no GPU -- which is what keeps the Nix ``pythonImportsCheck`` honest.
"""
import collections
import hmac
import json
import math
import os
import threading
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Tuple

from .logging import get_logger
from .telemetry import extract_trace_context, get_tracer, is_otel_enabled

logger = get_logger("serve")
_SERVER_START_TIME = time.monotonic()

# The three checkpoint names the router understands; used to decide whether a
# client's `model` field names a Roxx checkpoint (honour it) or is some other
# Jev model id (ignore it and let the router auto-select).
_KNOWN_MODELS = {"english", "multilingual", "typed-decisions"}

# Guardrails for unauthenticated remote input. The state is tokenized once per
# question and collated into one tensor, so an unbounded body can OOM the worker;
# the single-worker pool means one large request would also starve /health.
MAX_QUESTIONS = 64
MAX_STATE_CHARS = 50000
MAX_BODY_BYTES = 2 * 1024 * 1024
MAX_BATCH_ITEMS = 128
# Public Hugging Face ids, accepted so a client can name a checkpoint. The root bundle is
# deliberately absent: the documented ``krishujeniya/roxx`` value means
# "let the Router choose", rather than pinning the English checkpoint.
_PUBLISHED_MODEL_IDS = {
    "krishujeniya/roxx-multilingual": "multilingual",
    "krishujeniya/roxx-typed-decisions": "typed-decisions",
}


class RateLimiter:
    """Sliding-window in-memory rate limiter supporting 'N/second', 'N/minute', 'N/hour', 'N/day'."""

    def __init__(self, spec: str):
        parts = spec.strip().lower().split("/")
        if len(parts) != 2:
            raise ValueError(
                f"invalid rate limit {spec!r}: expected 'count/unit' (e.g. '60/minute', '10/s')"
            )
        try:
            self.limit = int(parts[0])
        except ValueError:
            raise ValueError(f"invalid rate limit count in {spec!r}: must be an integer") from None
        if self.limit <= 0:
            raise ValueError(f"invalid rate limit count in {spec!r}: must be > 0")

        unit = parts[1]
        if unit in ("s", "sec", "second", "seconds"):
            self.window_sec = 1.0
        elif unit in ("m", "min", "minute", "minutes"):
            self.window_sec = 60.0
        elif unit in ("h", "hr", "hour", "hours"):
            self.window_sec = 3600.0
        elif unit in ("d", "day", "days"):
            self.window_sec = 86400.0
        else:
            raise ValueError(f"unknown rate limit unit in {spec!r}: supported units are s, m, h, d")

        self._history: Dict[str, collections.deque] = collections.defaultdict(collections.deque)
        self._lock = threading.Lock()
        self._last_cleanup = time.monotonic()

    def check(self, key: str) -> Tuple[bool, int]:
        """Check if request for key is permitted. Returns (allowed, retry_after_seconds)."""
        now = time.monotonic()
        cutoff = now - self.window_sec
        with self._lock:
            if now - self._last_cleanup > 60.0:
                dead_keys = [k for k, q in self._history.items() if not q or q[-1] <= cutoff]
                for k in dead_keys:
                    del self._history[k]
                self._last_cleanup = now

            q = self._history[key]
            while q and q[0] <= cutoff:
                q.popleft()

            if len(q) >= self.limit:
                earliest = q[0]
                retry_after = max(1, math.ceil(earliest + self.window_sec - now))
                return False, retry_after

            q.append(now)
            return True, 0


def _env_bool(name: str, default: bool) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


def _resolve_model(model: Optional[str]) -> Optional[str]:
    """Map a client's `model` field onto a Roxx checkpoint, or None to auto-route."""
    if not model:
        return None
    published = _PUBLISHED_MODEL_IDS.get(str(model).strip().lower())
    if published is not None:
        return published
    from .router import normalise_name

    # normalise_name raises ValueError on anything that is not a known checkpoint
    # or alias. A Jev client's `model` field (e.g. "jev-1") is expected to miss;
    # treat that as "no explicit checkpoint" and let the router auto-select.
    try:
        key = normalise_name(model)
    except Exception:
        return None
    return key if key in _KNOWN_MODELS else None


def _resolve_port() -> int:
    """Port from ROXX_PORT, validated. Exits with a message instead of a traceback."""
    raw = os.environ.get("ROXX_PORT", "8000")
    try:
        port = int(str(raw).strip())
    except (TypeError, ValueError):
        raise SystemExit("invalid ROXX_PORT %r: must be an integer 1-65535" % (raw,))
    if not 1 <= port <= 65535:
        raise SystemExit("invalid ROXX_PORT %r: must be an integer 1-65535" % (raw,))
    return port


def _check_request_limits(state: Any, questions: Any) -> None:
    """Reject oversized inference requests before tokenization (413)."""
    from fastapi import HTTPException

    if not isinstance(questions, dict):
        raise HTTPException(status_code=400, detail="'questions' must be an object")
    if len(questions) > MAX_QUESTIONS:
        raise HTTPException(status_code=413,
                            detail="too many questions (%d > %d)" % (len(questions), MAX_QUESTIONS))
    try:
        state_len = len(state) if isinstance(state, str) else len(str(state))
    except Exception:
        state_len = MAX_STATE_CHARS + 1
    if state_len > MAX_STATE_CHARS:
        raise HTTPException(status_code=413,
                            detail="state too large (%d > %d chars)" % (state_len, MAX_STATE_CHARS))


async def _read_body_capped(request: Any) -> bytes:
    """Read the request body, refusing to buffer more than ``MAX_BODY_BYTES``.

    ``Content-Length`` cannot be the only gate. It is a value the client chooses,
    and under ``Transfer-Encoding: chunked`` it is absent altogether -- HTTP/2 and
    HTTP/3 have no such header at all -- so a request that simply omits it was
    read into memory in full, whatever its size. The body is streamed here and
    abandoned as soon as it exceeds the cap, so the limit holds for every framing
    rather than only for clients that announce their length honestly.
    """
    from fastapi import HTTPException

    total = 0
    chunks = []
    async for chunk in request.stream():
        if not chunk:
            continue
        total += len(chunk)
        if total > MAX_BODY_BYTES:
            # Stop reading rather than draining the rest: the peer is already over
            # the limit and nothing further can make the request acceptable.
            raise HTTPException(status_code=413, detail="request body too large")
        chunks.append(chunk)
    return b"".join(chunks)


def _apply_thread_limit():
    """Honour ROXX_THREADS by capping torch's intra-op thread count for CPU
    inference. Returns the value applied, or None if unset/invalid. torch is
    imported only when a limit is actually requested."""
    raw = os.environ.get("ROXX_THREADS")
    if not raw:
        return None
    try:
        n = int(raw)
    except ValueError:
        return None
    if n <= 0:
        return None
    import torch

    torch.set_num_threads(n)
    return n


def build_router():
    """Build a Router from the environment, preloading unless told otherwise."""
    from .router import Router

    _apply_thread_limit()
    device = os.environ.get("ROXX_DEVICE") or None
    models_env = os.environ.get("ROXX_MODELS", "").strip()
    preload_names = [m.strip() for m in models_env.split(",") if m.strip()] or None
    router = Router(device=device, auto_task_detection=_env_bool("ROXX_AUTO_TASK", False))
    if _env_bool("ROXX_PRELOAD", True):
        router.preload(preload_names)
    return router


def create_app(router: Optional[Any] = None):
    """Build the FastAPI app. Pass a Router to inject one (tests); otherwise one
    is built from the environment (and preloaded) at app-creation time."""
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    from fastapi import FastAPI, Header, HTTPException, Request

    if router is None:
        router = build_router()
    api_key = os.environ.get("ROXX_API_KEY") or None

    # Inference is synchronous torch, and a CPU call takes hundreds of milliseconds to
    # seconds, so it must not run on the event loop: one request would stall every
    # other client, `GET /health` included. One worker, because one forward pass at a
    # time is what a single CPU or GPU Agent wants (the Router already guards checkpoint
    # lifecycle, and leaves `Agent.system_one` unguarded deliberately so concurrent
    # predictions can share a checkpoint -- a GPU-shaped choice this endpoint does not
    # rely on). `loop.run_in_executor` is the API the issue asked for.
    pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="roxx-infer")
    # Created on first request, not here: an `asyncio.Lock` binds to the loop that is
    # running when it is first awaited, and `create_app` may be called before that loop
    # exists (module scope, TestClient startup, a preload script).
    gate: Optional[asyncio.Lock] = None

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        try:
            yield
        finally:
            # TestClient, embedded ASGI apps, and process supervisors all need
            # the executor to drain when the app stops.
            pool.shutdown(wait=True, cancel_futures=True)

    app = FastAPI(
        title="roxx-serve",
        summary="Roxx System-1 decisions over the TypeSafe Jev /v1/systemone protocol",
        lifespan=lifespan,
    )

    # CORS configuration
    cors_enabled = _env_bool("ROXX_CORS_ENABLED", False) or bool(os.environ.get("ROXX_CORS_ORIGINS"))
    if cors_enabled:
        from fastapi.middleware.cors import CORSMiddleware

        raw_origins = os.environ.get("ROXX_CORS_ORIGINS", "*").strip()
        origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins if origins else ["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Security headers middleware
    if _env_bool("ROXX_SECURITY_HEADERS", True):
        @app.middleware("http")
        async def security_headers_middleware(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
            return response

    # Rate limiting middleware
    rate_spec = os.environ.get("ROXX_RATE_LIMIT")
    limiter = RateLimiter(rate_spec) if rate_spec else None
    if limiter is not None:
        from fastapi.responses import JSONResponse

        @app.middleware("http")
        async def rate_limiting_middleware(request: Request, call_next):
            if request.url.path.startswith("/health"):
                return await call_next(request)
            client_key = request.headers.get("authorization") or (
                request.client.host if request.client else "unknown"
            )
            allowed, retry_after = limiter.check(client_key)
            if not allowed:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too Many Requests"},
                    headers={"Retry-After": str(retry_after)},
                )
            return await call_next(request)

    # Compared as bytes, not str. `hmac.compare_digest` raises TypeError when a str
    # operand holds a non-ASCII character, and Starlette decodes request headers as
    # latin-1 -- so `Authorization: Bearer s\xe9cret`, which is legal on the wire,
    # made the comparison itself raise. That surfaced as HTTP 500 plus a traceback
    # in the log, reachable by any unauthenticated client with one byte. Encoding
    # both sides first keeps the comparison constant-time and total: every header a
    # client can send now answers 401.
    expected_auth = ("Bearer " + api_key).encode("utf-8", "surrogateescape") if api_key else b""

    def _check_auth(authorization: Optional[str]) -> None:
        if api_key is None:
            return
        supplied = (authorization or "").encode("utf-8", "surrogateescape")
        if not hmac.compare_digest(supplied, expected_auth):
            raise HTTPException(status_code=401, detail="invalid or missing bearer token")

    @app.get("/health")
    def health() -> Dict[str, Any]:
        return {
            "status": "ok",
            "loaded": router.loaded,
            "device": os.environ.get("ROXX_DEVICE") or "auto",
        }

    @app.get("/health/live")
    def health_live() -> Dict[str, Any]:
        return {
            "status": "live",
            "uptime_seconds": round(time.monotonic() - _SERVER_START_TIME, 2),
        }

    @app.get("/health/ready")
    def health_ready() -> Dict[str, Any]:
        try:
            loaded = router.loaded
            return {
                "status": "ready",
                "loaded": loaded,
                "device": os.environ.get("ROXX_DEVICE") or "auto",
            }
        except Exception as e:
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=503,
                content={"status": "not_ready", "detail": str(e)},
            )

    @app.post("/v1/systemone")
    async def systemone(request: Request, authorization: Optional[str] = Header(default=None)):
        nonlocal gate
        _check_auth(authorization)
        # A declared length over the cap is rejected before anything is read; the
        # streaming cap below is what actually enforces it, for bodies that declare
        # no length or understate it.
        if request.headers.get("content-length"):
            try:
                if int(request.headers["content-length"]) > MAX_BODY_BYTES:
                    raise HTTPException(status_code=413, detail="request body too large")
            except ValueError:
                pass
        raw = await _read_body_capped(request)
        try:
            # Every parse failure a client can cause is a ValueError: JSONDecodeError for
            # malformed/empty/truncated bodies, UnicodeDecodeError for invalid UTF-8. A
            # broader catch would also swallow ClientDisconnect and Starlette's own
            # stream errors, reporting a transport or server fault as the client's.
            body = json.loads(raw)
        except ValueError:
            raise HTTPException(status_code=400, detail="request body must be valid JSON")
        if not isinstance(body, dict) or "questions" not in body:
            raise HTTPException(status_code=400, detail="request body must be an object with a 'questions' field")
        state = body.get("state")
        questions = body["questions"]
        _check_request_limits(state, questions)
        model = _resolve_model(body.get("model"))
        if gate is None:
            gate = asyncio.Lock()
        try:
            # Roxx's result is already Jev-shaped: {model, answers, usage, routing}.
            # hs-jev decodes `answers` and `usage` and ignores the rest.
            async with gate:
                loop = asyncio.get_running_loop()
                tracer = get_tracer("roxx.serve")
                trace_ctx = extract_trace_context(dict(request.headers))
                with tracer.start_as_current_span("roxx.serve.systemone", context=trace_ctx):
                    return await loop.run_in_executor(
                        pool, lambda: router.predict(state, questions, model=model))
        except HTTPException:
            raise
        except ValueError as e:
            # Question validation errors name the question and what to fix: safe for clients.
            raise HTTPException(status_code=422, detail=str(e))
        except Exception:  # noqa: BLE001 -- never leak paths/weights/OOM text to clients
            raise HTTPException(status_code=500, detail="inference failed")

    @app.post("/v1/systemone/batch")
    async def systemone_batch(request: Request, authorization: Optional[str] = Header(default=None)):
        nonlocal gate
        _check_auth(authorization)
        if request.headers.get("content-length"):
            try:
                if int(request.headers["content-length"]) > MAX_BODY_BYTES * 4:
                    raise HTTPException(status_code=413, detail="request body too large")
            except ValueError:
                pass
        raw = await _read_body_capped(request)
        try:
            body = json.loads(raw)
        except ValueError:
            raise HTTPException(status_code=400, detail="request body must be valid JSON")

        if isinstance(body, dict) and "items" in body:
            items = body["items"]
        elif isinstance(body, list):
            items = body
        else:
            raise HTTPException(status_code=400, detail="request body must contain an 'items' array or be a list")

        if not isinstance(items, list):
            raise HTTPException(status_code=400, detail="'items' must be a list")
        if len(items) > MAX_BATCH_ITEMS:
            raise HTTPException(status_code=413, detail=f"too many batch items ({len(items)} > {MAX_BATCH_ITEMS})")

        for idx, it in enumerate(items):
            if not isinstance(it, dict) or "questions" not in it:
                raise HTTPException(status_code=400, detail=f"item {idx} must be an object with 'questions'")
            _check_request_limits(it.get("state"), it["questions"])

        if gate is None:
            gate = asyncio.Lock()

        def _run_batch():
            results = []
            for it in items:
                m = _resolve_model(it.get("model"))
                results.append(router.predict(it.get("state"), it["questions"], model=m))
            return {"results": results}

        try:
            async with gate:
                loop = asyncio.get_running_loop()
                tracer = get_tracer("roxx.serve")
                trace_ctx = extract_trace_context(dict(request.headers))
                with tracer.start_as_current_span("roxx.serve.batch", context=trace_ctx):
                    return await loop.run_in_executor(pool, _run_batch)
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception:  # noqa: BLE001
            raise HTTPException(status_code=500, detail="batch inference failed")

    return app


def main() -> None:
    import uvicorn

    uvicorn.run(
        create_app(),
        host=os.environ.get("ROXX_HOST", "0.0.0.0"),
        port=_resolve_port(),
        log_level=os.environ.get("ROXX_LOG_LEVEL", "info"),
    )


if __name__ == "__main__":
    main()
