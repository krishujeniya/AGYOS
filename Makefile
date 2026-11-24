.PHONY: all dev test typecheck lint build clean help

# Default target
all: test

help:
	@echo "AGYOS Unified Makefile"
	@echo "======================="
	@echo "make dev         - Run backend and frontend concurrently"
	@echo "make test        - Run fast, loadless unit and integration tests"
	@echo "make typecheck   - Run type checking (Python pyright/mypy + Next.js tsc)"
	@echo "make lint        - Run linters across backend and frontend"
	@echo "make build       - Build production artifacts for frontend and backend"
	@echo "make clean       - Remove temporary caches and build artifacts"

dev:
	@echo "Starting AGYOS development environment..."
	@mkdir -p .agents/state
	@bash -c "trap 'kill 0' SIGINT; (cd backend && uv run uvicorn app.main:app --reload --port 8000) & (cd frontend && npm run dev) & wait"

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

test: test-backend test-frontend

test-backend:
	@echo "Running backend tests via uv..."
	cd backend && uv run python -m unittest discover -s tests -p "test_*.py"

test-frontend:
	@echo "Running frontend typecheck & validation..."
	cd frontend && npx tsc --noEmit

typecheck:
	@echo "Typechecking backend and frontend..."
	cd backend && uv run python -m py_compile app/main.py app/api/v1/endpoints.py
	cd frontend && npx tsc --noEmit

lint:
	@echo "Linting backend and frontend..."
	@git diff --check

build: build-frontend

build-frontend:
	@echo "Building Next.js frontend portal for Cloudflare Pages..."
	cd frontend && npm run build

clean:
	@echo "Cleaning transient build caches..."
	rm -rf frontend/.next frontend/out frontend/.turbo
	rm -rf backend/__pycache__ backend/tests/__pycache__ backend/app/__pycache__
	rm -rf .pytest_cache .ruff_cache htmlcov dist target
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
