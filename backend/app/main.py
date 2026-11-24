"""AGYOS Backend Application Entrypoint."""
from __future__ import annotations

import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import router as v1_router

app = FastAPI(
    title="AGYOS Cognitive API",
    description="High-performance autonomous operating system and multi-agent decision kernel.",
    version="3.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 router
app.include_router(v1_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    """Root endpoint providing service discovery."""
    return {
        "service": "AGYOS Autonomous Operating System API",
        "version": "3.2.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


@app.get("/health", tags=["Health"])
def health_probe() -> dict[str, str | float]:
    """Top-level health check probe."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "3.2.0",
    }
