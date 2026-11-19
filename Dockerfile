# syntax=docker/dockerfile:1.4
FROM node:22-bookworm-slim AS documents
WORKDIR /app
COPY scripts/materialize-documents.mjs scripts/
COPY README.md.toon SECURITY.md.toon ./
COPY docs/ docs/
COPY site/ site/
RUN node scripts/materialize-documents.mjs

FROM python:3.12.9-slim-bookworm AS builder

WORKDIR /app
RUN python -m pip install --no-cache-dir 'mistune==3.2.1'
COPY scripts/build_docs_site.py scripts/
COPY --from=documents /app/README.md /app/SECURITY.md ./
COPY --from=documents /app/docs/ docs/
COPY --from=documents /app/site/ site/
RUN python scripts/build_docs_site.py --out /public --base /

FROM python:3.12.9-slim-bookworm AS runner

RUN groupadd -r agyos -g 1001 && \
    useradd -r -u 1001 -g agyos -d /nonexistent -s /usr/sbin/nologin agyos

WORKDIR /app/site
COPY --from=builder /public/ ./
USER agyos

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["python3", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:8080/', timeout=2).close()"]
CMD ["python3", "-m", "http.server", "8080", "--bind", "0.0.0.0"]
