.PHONY: all dev test typecheck lint build clean help

# Default target
all: test

help:
	@echo "AGYOS Unified Makefile"
	@echo "======================="
	@echo "make dev         - Build static frontend and serve locally on port 8000"
	@echo "make test        - Run fast validation tests across scripts and frontend"
	@echo "make typecheck   - Run Python bytecode compile check and JS syntax check"
	@echo "make lint        - Run git hygiene and syntax checks"
	@echo "make build       - Build static frontend bundle into _site/"
	@echo "make clean       - Remove temporary caches and build artifacts"

dev: build
	@echo "Serving AGYOS static frontend from _site/ on http://127.0.0.1:8000..."
	uv run python -m http.server 8000 --directory _site

test:
	@echo "Running AGYOS tests..."
	cd gemini && uv run python -m unittest discover -s scripts/tests -v
	node --test gemini/scripts/tests/test_materialize_documents.mjs

typecheck:
	@echo "Checking Python and frontend syntax..."
	uv run python -m compileall gemini/agyos_decision gemini/scripts
	node --check frontend/site.js

lint:
	@echo "Linting repository hygiene..."
	@git diff --check
	node --check frontend/site.js

build:
	@echo "Building AGYOS static frontend into _site/..."
	uv run --with mistune python gemini/scripts/build_docs_site.py --out _site --base /

clean:
	@echo "Cleaning transient build caches..."
	rm -rf _site .pytest_cache .ruff_cache htmlcov dist
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
