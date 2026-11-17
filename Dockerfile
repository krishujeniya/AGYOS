# syntax=docker/dockerfile:1.4
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /bin/uv

COPY requirements.txt ./
RUN uv pip install --system --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runner

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

RUN groupadd -r agyos -g 1001 && \
    useradd -r -u 1001 -g agyos -m -s /bin/bash agyos

COPY --from=builder /install /usr/local
COPY --chown=agyos:agyos . .

USER agyos

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8080/ || exit 1

WORKDIR /app/site
CMD ["python3", "-m", "http.server", "8080", "--bind", "0.0.0.0"]
