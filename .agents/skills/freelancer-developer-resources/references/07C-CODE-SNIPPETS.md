---
title: "07C — Code Snippets"
description: "Copy-paste boilerplate for Docker, FastAPI, CI/CD, testing, and common ML/data engineering patterns."
version: "2026.05"
---

# 07C — CODE-SNIPPETS

> **Rule:** Never write infrastructure code from scratch. Copy, adapt, ship. These snippets are production-tested and follow 2026 best practices.

---

## Snippet 1: Docker — FastAPI + ML Model Serving

**File:** `Dockerfile`

```dockerfile
# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PATH=/root/.local/bin:$PATH

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY models/ ./models/
COPY config/ ./config/

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3     CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**File:** `.dockerignore`

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
notebooks/
data/raw/
*.csv
*.parquet
```

---

## Snippet 2: FastAPI — Production-Ready API Skeleton

**File:** `src/main.py`

```python
"""
Production-ready FastAPI application for ML model serving.
"""

import os
import time
from contextlib import asynccontextmanager
from typing import Any

import joblib
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# ---------- Prometheus Metrics ----------
PREDICTION_COUNTER = Counter("predictions_total", "Total predictions", ["model_version"])
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Prediction latency")
ERROR_COUNTER = Counter("errors_total", "Total errors", ["error_type"])

# ---------- Pydantic Models ----------
class PredictRequest(BaseModel):
    entity_id: str = Field(..., min_length=1, description="Unique entity identifier")
    context: dict[str, Any] = Field(default_factory=dict, description="Optional context")

class PredictResponse(BaseModel):
    entity_id: str
    score: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    timestamp: str
    explanation: dict[str, Any] | None = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

# ---------- Model Loading ----------
MODEL = None
MODEL_VERSION = os.getenv("MODEL_VERSION", "unknown")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global MODEL
    model_path = os.getenv("MODEL_PATH", "models/model.pkl")
    if not os.path.exists(model_path):
        raise RuntimeError(f"Model not found at {model_path}")
    MODEL = joblib.load(model_path)
    print(f"Loaded model version {MODEL_VERSION} from {model_path}")
    yield
    print("Shutting down...")

# ---------- App Initialization ----------
app = FastAPI(
    title="ML Prediction API",
    version=MODEL_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if os.getenv("ENV") != "prod" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGIN", "*")],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ---------- Middleware ----------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start)
    return response

# ---------- Endpoints ----------
@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    if MODEL is None:
        ERROR_COUNTER.labels(error_type="model_not_loaded").inc()
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        with PREDICTION_LATENCY.time():
            # Replace with actual feature extraction + prediction
            score = 0.5  # Placeholder

        PREDICTION_COUNTER.labels(model_version=MODEL_VERSION).inc()

        return PredictResponse(
            entity_id=request.entity_id,
            score=score,
            model_version=MODEL_VERSION,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            explanation={"top_features": ["feature_1", "feature_2"]},
        )
    except Exception as e:
        ERROR_COUNTER.labels(error_type="prediction_error").inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        version=MODEL_VERSION,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )

@app.get("/metrics")
async def metrics():
    return JSONResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )

# ---------- Global Exception Handler ----------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    ERROR_COUNTER.labels(error_type="unhandled").inc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "code": "INTERNAL_ERROR"},
    )
```

---

## Snippet 3: CI/CD — GitHub Actions Workflow

**File:** `.github/workflows/ci-cd.yml`

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install ruff mypy
      - run: ruff check src/
      - run: ruff format --check src/
      - run: mypy src/ --ignore-missing-imports

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=src --cov-report=xml --cov-report=term
      - uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      - uses: google-github-actions/setup-gcloud@v2
      - run: |
          gcloud auth configure-docker
          docker build -t gcr.io/${{ secrets.GCP_PROJECT }}/app:${{ github.sha }} .
          docker push gcr.io/${{ secrets.GCP_PROJECT }}/app:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      - uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: app
          image: gcr.io/${{ secrets.GCP_PROJECT }}/app:${{ github.sha }}
          region: us-central1
```

---

## Snippet 4: Testing — pytest Fixtures & Patterns

**File:** `tests/conftest.py`

```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_predict_payload():
    return {
        "entity_id": "550e8400-e29b-41d4-a716-446655440000",
        "context": {"device": "mobile", "country": "US"},
    }
```

**File:** `tests/test_api.py`

```python
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data

def test_predict_success(client, sample_predict_payload):
    response = client.post("/predict", json=sample_predict_payload)
    assert response.status_code == 200
    data = response.json()
    assert 0.0 <= data["score"] <= 1.0
    assert data["entity_id"] == sample_predict_payload["entity_id"]

def test_predict_missing_entity_id(client):
    response = client.post("/predict", json={"context": {}})
    assert response.status_code == 422

def test_predict_invalid_entity_id_format(client):
    response = client.post("/predict", json={"entity_id": "", "context": {}})
    assert response.status_code == 422

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "predictions_total" in response.text
```

---

## Snippet 5: ML Pipeline — ZenML + MLflow Skeleton

**File:** `pipelines/training_pipeline.py`

```python
"""
ZenML training pipeline with MLflow tracking.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score, precision_score, recall_score
import joblib

from zenml import pipeline, step
from zenml.client import Client
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri

# ---------- Steps ----------
@step
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Basic validation
    assert not df.empty, "Data is empty"
    assert "target" in df.columns, "Target column missing"
    return df

@step
def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    X = df.drop("target", axis=1)
    y = df["target"]
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

@step
def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> GradientBoostingClassifier:
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    return model

@step
def evaluate_model(model: GradientBoostingClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    preds = model.predict(X_test)
    metrics = {
        "f1": f1_score(y_test, preds, average="weighted"),
        "precision": precision_score(y_test, preds, average="weighted", zero_division=0),
        "recall": recall_score(y_test, preds, average="weighted", zero_division=0),
    }
    return metrics

@step
def save_model(model: GradientBoostingClassifier, metrics: dict) -> str:
    if metrics["f1"] < 0.7:
        raise ValueError(f"F1 score {metrics['f1']} below threshold")
    path = "models/model.pkl"
    joblib.dump(model, path)
    return path

# ---------- Pipeline ----------
@pipeline
def training_pipeline(data_path: str):
    df = load_data(data_path)
    X_train, X_test, y_train, y_test = split_data(df)
    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    model_path = save_model(model, metrics)
    return model_path, metrics

# ---------- Execution ----------
if __name__ == "__main__":
    client = Client()
    print(f"MLflow UI: {get_tracking_uri()}")

    model_path, metrics = training_pipeline(data_path="data/processed/train.csv")
    print(f"Model saved to: {model_path}")
    print(f"Metrics: {metrics}")
```

---

## Snippet 6: Data Validation — Great Expectations Lite

**File:** `src/data_validation.py`

```python
"""
Lightweight data validation without full Great Expectations overhead.
"""

import pandas as pd
from typing import Callable, Dict, List

class DataValidator:
    def __init__(self):
        self.rules: Dict[str, List[Callable]] = {}
        self.errors: List[str] = []

    def add_rule(self, column: str, check: Callable, description: str):
        if column not in self.rules:
            self.rules[column] = []
        self.rules[column].append((check, description))

    def validate(self, df: pd.DataFrame) -> bool:
        self.errors = []
        for column, checks in self.rules.items():
            if column not in df.columns:
                self.errors.append(f"Column '{column}' missing")
                continue
            for check, desc in checks:
                try:
                    result = check(df[column])
                    if not result:
                        self.errors.append(f"Column '{column}': {desc}")
                except Exception as e:
                    self.errors.append(f"Column '{column}': {desc} (exception: {e})")
        return len(self.errors) == 0

    def report(self) -> str:
        if not self.errors:
            return "All validations passed."
        return "\n".join([f"[FAIL] {e}" for e in self.errors])

# ---------- Usage ----------
def validate_customer_data(df: pd.DataFrame) -> bool:
    validator = DataValidator()

    validator.add_rule("customer_id", lambda s: s.notna().all(), "No null customer IDs")
    validator.add_rule("customer_id", lambda s: s.is_unique, "Customer IDs must be unique")
    validator.add_rule("age", lambda s: (s >= 18).all(), "Age must be >= 18")
    validator.add_rule("age", lambda s: (s <= 120).all(), "Age must be <= 120")
    validator.add_rule("signup_date", lambda s: pd.to_datetime(s, errors="coerce").notna().all(), "Valid dates required")
    validator.add_rule("country", lambda s: s.isin(["US", "CA", "UK", "DE", "FR", "IN"]).all(), "Country in allowed list")

    is_valid = validator.validate(df)
    print(validator.report())
    return is_valid
```

---

## Snippet 7: Environment Configuration — Pydantic Settings

**File:** `src/config.py`

```python
"""
Pydantic-based configuration with environment variable loading.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "ml-api"
    ENV: str = "dev"
    DEBUG: bool = False

    # Model
    MODEL_PATH: str = "models/model.pkl"
    MODEL_VERSION: str = "unknown"

    # API
    ALLOWED_ORIGIN: str = "*"
    API_KEY: str | None = None
    RATE_LIMIT_PER_MINUTE: int = 100

    # Database
    DATABASE_URL: str | None = None

    # Monitoring
    ENABLE_PROMETHEUS: bool = True
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

**File:** `.env.example`

```bash
# Copy to .env and fill in real values
APP_NAME=ml-api
ENV=dev
DEBUG=false
MODEL_PATH=models/model.pkl
MODEL_VERSION=v1.0.0
ALLOWED_ORIGIN=https://client-domain.com
API_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
ENABLE_PROMETHEUS=true
LOG_LEVEL=INFO
```

---

## Snippet 8: Makefile — Standard Commands

**File:** `Makefile`

```makefile
.PHONY: install lint test build run clean

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

lint:
	ruff check src/ tests/
	ruff format src/ tests/
	mypy src/ --ignore-missing-imports

test:
	pytest --cov=src --cov-report=term --cov-report=xml

build:
	docker build -t ml-api:latest .

run:
	docker run -p 8000:8000 --env-file .env ml-api:latest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/ .coverage htmlcov/
```

---

## Snippet 9: Pre-commit Hooks

**File:** `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ["--maxkb=1000"]
```

---

## Snippet 10: Requirements Files

**File:** `requirements.txt`

```
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
joblib>=1.4.0
scikit-learn>=1.5.0
pandas>=2.2.0
numpy>=1.26.0
prometheus-client>=0.20.0
python-multipart>=0.0.9
```

**File:** `requirements-dev.txt`

```
-r requirements.txt
pytest>=8.2.0
pytest-cov>=5.0.0
httpx>=0.27.0
ruff>=0.4.0
mypy>=1.10.0
pre-commit>=3.7.0
```

---

## Action Checklist

- [ ] Copy `Dockerfile` and `.dockerignore` into every new repo.
- [ ] Adapt `src/main.py` FastAPI skeleton to project needs.
- [ ] Set up GitHub Actions CI/CD before first commit.
- [ ] Run `make lint test` before every push.
- [ ] Install pre-commit hooks: `pre-commit install`.
- [ ] Use `DataValidator` class on every data ingestion point.
- [ ] Store secrets in `.env` (never commit); use `pydantic-settings`.

---

*Reference: Production code patterns synthesized from FastAPI docs, ZenML guides, and 2026 MLOps best practices.*
