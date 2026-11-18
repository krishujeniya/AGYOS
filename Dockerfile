# syntax=docker/dockerfile:1.4
FROM python:3.12-slim AS builder

WORKDIR /app
RUN python -m pip install --no-cache-dir 'mistune==3.2.1'
COPY scripts/build_docs_site.py scripts/
COPY README.md SECURITY.md ./
COPY docs/ docs/
COPY site/ site/
RUN python scripts/build_docs_site.py --out /public --base /

FROM python:3.12-slim AS runner

RUN groupadd -r agyos -g 1001 && \
    useradd -r -u 1001 -g agyos -d /nonexistent -s /usr/sbin/nologin agyos

WORKDIR /app/site
COPY --from=builder /public/ ./
USER agyos

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["python3", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:8080/', timeout=2).close()"]
CMD ["python3", "-m", "http.server", "8080", "--bind", "0.0.0.0"]
