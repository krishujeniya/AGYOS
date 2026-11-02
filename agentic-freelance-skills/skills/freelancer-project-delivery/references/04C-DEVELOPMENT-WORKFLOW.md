---
module: "04-PROJECT-DELIVERY"
part: "C"
title: "Development Workflow"
version: "2026.05"
status: "Production-Ready"
---

# 04C: Development Workflow

> **Core Principle:** Clean code, clean commits, clean process. Your future self (and your client) will thank you for every hour you spend on discipline today.
>
> *"Code quality signals: You write maintainable code. You think about others using your code. You understand software engineering basics."* — Ayush Singh

---

## Table of Contents

1. [Git Branching Strategy](#1-git-branching-strategy)
2. [Commit Standards](#2-commit-standards)
3. [Code Quality](#3-code-quality)
4. [CI/CD Pipeline](#4-cicd-pipeline)
5. [Documentation Standards](#5-documentation-standards)
6. [AI Prompts](#6-ai-prompts)
7. [Action Checklist](#7-action-checklist)

---

## 1. Git Branching Strategy

### The Freelancer Git Flow

```
main (production-ready)
  ↑
dev (integration)
  ↑
feature/data-pipeline
feature/model-training
feature/api-endpoints
feature/frontend-dashboard
```

### Branch Rules

| Branch | Purpose | Protection | Merge Requirement |
|--------|---------|------------|-------------------|
| **main** | Production code | Protected | PR + review + tests pass |
| **dev** | Integration branch | Protected | PR + tests pass |
| **feature/*** | New features | None | PR to dev |
| **hotfix/*** | Production fixes | None | PR to main + dev |
| **release/*** | Release prep | None | PR to main |

### Commit Workflow

```bash
# 1. Create feature branch
git checkout -b feature/data-ingestion

# 2. Make changes, commit often
git add .
git commit -m "feat: add Apache Airflow data ingestion pipeline"

# 3. Push to remote
git push origin feature/data-ingestion

# 4. Create Pull Request (self-review or peer)
# 5. Run CI checks
# 6. Merge to dev
# 7. Delete feature branch
```

---

## 2. Commit Standards

### Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

| Type | Use When | Example |
|------|----------|---------|
| **feat** | New feature | `feat(model): add XGBoost churn predictor` |
| **fix** | Bug fix | `fix(api): handle missing feature edge case` |
| **docs** | Documentation | `docs(readme): add deployment instructions` |
| **style** | Formatting | `style(black): reformat data pipeline` |
| **refactor** | Code restructuring | `refactor(pipeline): separate ETL stages` |
| **test** | Adding tests | `test(model): add robustness tests` |
| **chore** | Maintenance | `chore(deps): update requirements.txt` |

### Commit Best Practices

| Rule | Example |
|------|---------|
| **Atomic commits** | One logical change per commit |
| **Meaningful messages** | `feat: add drift detection` not `update` |
| **Reference issues** | `feat: add monitoring (#12)` |
| **No secrets** | Scan with `git-secrets` before push |
| **Small, frequent** | Commit every 30-60 minutes |

---

## 3. Code Quality

### Python Standards

| Tool | Purpose | Config |
|------|---------|--------|
| **black** | Code formatting | `line-length = 88` |
| **isort** | Import sorting | `profile = black` |
| **flake8** | Linting | `max-line-length = 88` |
| **mypy** | Type checking | `strict = true` |
| **pylint** | Code analysis | Default config |

### Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

### Code Review Checklist (Self-Review)

- [ ] Code follows style guide (black, PEP 8)
- [ ] Functions are <50 lines
- [ ] No hardcoded values (use config/env vars)
- [ ] Error handling for all external calls
- [ ] Logging for debugging (not print statements)
- [ ] Type hints on all functions
- [ ] Docstrings for public APIs
- [ ] No secrets in code
- [ ] Tests cover new code

---

## 4. CI/CD Pipeline

### GitHub Actions CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run linters
        run: |
          black --check .
          isort --check-only .
          flake8 .

      - name: Run type checker
        run: mypy src/

      - name: Run tests
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Deployment Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t $IMAGE_NAME:$GITHUB_SHA .

      - name: Push to registry
        run: |
          echo $GCP_SA_KEY | docker login -u _json_key --password-stdin https://gcr.io
          docker push $IMAGE_NAME:$GITHUB_SHA

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy $SERVICE_NAME \
            --image $IMAGE_NAME:$GITHUB_SHA \
            --region us-central1 \
            --platform managed
```

---

## 5. Documentation Standards

### README Structure

```markdown
# Project Name

## Overview
One sentence: What this does and why it matters.

## Problem Statement
What pain point does this solve?

## Solution
How does this solve it?

## Results
Quantified impact.

## Tech Stack
| Category | Tools |
|----------|-------|
| ML | Python, XGBoost, Scikit-Learn |
| API | FastAPI, Docker |
| Cloud | GCP Cloud Run |

## Quick Start
```bash
git clone [repo]
cd project
pip install -r requirements.txt
python -m src.app
```

## Project Structure
```
src/
├── data/          # Data pipelines
├── features/      # Feature engineering
├── models/        # Model training
├── api/           # FastAPI app
└── monitoring/    # Drift detection
```

## API Documentation
[Swagger UI link]

## Monitoring
[Dashboard link]

## License
[Your license]
```

### API Documentation (FastAPI + Swagger)

FastAPI auto-generates OpenAPI docs. Access at `/docs` endpoint.

Key practices:
- Use Pydantic models for request/response schemas
- Add docstrings to every endpoint
- Include example values
- Document error responses
- Version your API (`/v1/predict`)

---

## 6. AI Prompts

### Prompt 1: Code Review Assistant

```
Act as a senior code reviewer.

Review this code:
[PASTE CODE]

Check for:
1. Style compliance (PEP 8, black formatting)
2. Error handling (try/except, input validation)
3. Type hints (missing or incorrect)
4. Docstrings (missing or incomplete)
5. Hardcoded values (should be config)
6. Security (secrets, SQL injection, XSS)
7. Performance (inefficient loops, memory leaks)
8. Test coverage (missing tests)

Provide specific line-by-line feedback.
Suggest refactors where needed.
```

### Prompt 2: CI/CD Generator

```
Act as a DevOps engineer.

Project details:
- Language: [Python/Node.js/etc]
- Framework: [FastAPI/Flask/React/etc]
- Cloud: [GCP/AWS/Azure]
- Deployment: [Docker/Kubernetes/Serverless]

Generate:
1. GitHub Actions CI workflow (lint, test, type-check)
2. GitHub Actions CD workflow (build, push, deploy)
3. Dockerfile
4. docker-compose.yml (for local dev)
5. .pre-commit-config.yaml

Use best practices for [language] and [cloud].
Include health checks and rollback strategy.
```

### Prompt 3: Documentation Writer

```
Act as a technical writer.

Project details:
- Name: [PROJECT]
- What it does: [DESCRIPTION]
- Tech stack: [TOOLS]
- Key results: [METRICS]

Write:
1. README.md (comprehensive, GitHub-ready)
2. API documentation (OpenAPI/Swagger style)
3. Deployment guide (step-by-step)
4. Troubleshooting section (5 common issues)

Target audience: Technical but not expert.
Include code examples and screenshots placeholders.
```

---

## 7. Action Checklist

### Project Setup

- [ ] Initialize Git repo with README
- [ ] Set up branch protection rules
- [ ] Configure pre-commit hooks
- [ ] Set up GitHub Actions CI
- [ ] Create requirements.txt and requirements-dev.txt
- [ ] Set up virtual environment
- [ ] Configure IDE (VS Code settings, extensions)

### Development

- [ ] Follow conventional commits
- [ ] Run pre-commit hooks before every push
- [ ] Self-review code before PR
- [ ] Write tests for new features
- [ ] Update documentation with changes
- [ ] Keep commits atomic and meaningful

### Deployment

- [ ] Set up CD pipeline
- [ ] Configure environment variables
- [ ] Set up monitoring and alerts
- [ ] Test rollback procedure
- [ ] Document deployment process

---

> **Next:** [04D: MLOps Pipeline →](04D-ML-OPS-PIPELINE.md)
>
> *"Your code is your resume. Make it readable."*

---

*Module 04C | Development Workflow | Version 2026.05*
