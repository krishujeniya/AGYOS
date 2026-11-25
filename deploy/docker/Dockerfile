# syntax=docker/dockerfile:1.4
FROM python:3.12.9-slim-bookworm AS builder

WORKDIR /app
RUN python -m pip install --no-cache-dir 'mistune==3.2.1'
COPY gemini/scripts/build_docs_site.py gemini/scripts/
COPY README.md ./
COPY .github/SECURITY.md .github/SECURITY.md
COPY docs/ docs/
COPY assets/ assets/
COPY frontend/ frontend/
RUN python gemini/scripts/build_docs_site.py --out /public --base /

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
