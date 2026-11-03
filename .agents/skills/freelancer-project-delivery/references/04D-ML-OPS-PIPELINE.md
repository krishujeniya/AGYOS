---
module: "04-PROJECT-DELIVERY"
part: "D"
title: "MLOps Pipeline"
version: "2026.05"
status: "Production-Ready"
---

# 04D: MLOps Pipeline

> **Core Principle:** Raw data is sacred. Never modify it. Pipeline stages: Raw → Validated → Processed → Features → Model-ready. Each stage is versioned, reproducible, and monitored.
>
> *"The difference between students and professionals: Students create random features, hope something works. Professionals create features based on hypotheses about the problem."* — Ayush Singh

---

## Table of Contents

1. [The MLOps Pipeline Architecture](#1-the-mlops-pipeline-architecture)
2. [Data Pipeline](#2-data-pipeline)
3. [Experiment Tracking](#3-experiment-tracking)
4. [Model Development](#4-model-development)
5. [Deployment](#5-deployment)
6. [Monitoring & Drift Detection](#6-monitoring--drift-detection)
7. [AI Prompts](#7-ai-prompts)
8. [Action Checklist](#8-action-checklist)

---

## 1. The MLOps Pipeline Architecture

### The 6-Stage Pipeline

```
Raw Data → Validated → Processed → Features → Model → Deployed → Monitored
    ↓           ↓           ↓          ↓        ↓         ↓          ↓
   DVC      Great Exp.   Pandas    Feature   MLflow   Docker   Evidently
            Expectations  Spark     Store    Registry  FastAPI   Grafana
```

### Stage Responsibilities

| Stage | Tool | Input | Output | Versioned |
|-------|------|-------|--------|-----------|
| **Raw** | DVC | External sources | Raw dataset | Yes |
| **Validated** | Great Expectations | Raw dataset | Validated dataset | Yes |
| **Processed** | Pandas/Spark | Validated dataset | Clean dataset | Yes |
| **Features** | Feast/Custom | Clean dataset | Feature vectors | Yes |
| **Model** | MLflow | Feature vectors | Trained model | Yes |
| **Deployed** | Docker/FastAPI | Trained model | API endpoint | Yes |
| **Monitored** | Evidently/Grafana | API traffic | Alerts | Yes |

---

## 2. Data Pipeline

### Data Versioning with DVC

```bash
# Initialize DVC
dvc init

# Track raw data
dvc add data/raw/dataset.csv

# Push to remote storage
dvc remote add -d myremote gdrive://[folder_id]
dvc push

# Checkout specific version
git checkout v1.0
dvc checkout
```

### Data Validation with Great Expectations

```python
import great_expectations as gx

context = gx.get_context()

datasource = context.sources.add_pandas("my_datasource")
data_asset = datasource.add_csv_asset("my_asset", filepath_or_buffer="data.csv")

batch_request = data_asset.build_batch_request()

# Define expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="my_suite"
)

validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_between("age", min_value=18, max_value=100)
validator.expect_column_values_to_be_in_set("churn", [0, 1])

validator.save_expectation_suite(discard_failed_expectations=False)

# Run checkpoint
checkpoint = context.add_or_update_checkpoint(
    name="my_checkpoint",
    validator=validator,
)
checkpoint_result = checkpoint.run()
```

### Data Quality Dimensions

| Dimension | Check | Tool |
|-----------|-------|------|
| **Completeness** | Missing values <5% | pandas.isnull() |
| **Validity** | Values in expected ranges | Great Expectations |
| **Accuracy** | Match source of truth | Cross-reference |
| **Consistency** | No contradictions | SQL checks |
| **Timeliness** | Data freshness | Airflow sensors |

---

## 3. Experiment Tracking

### MLflow Setup

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Set tracking URI
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("churn-prediction")

with mlflow.start_run(run_name="random-forest-baseline"):
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("random_state", 42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)

    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision_score(y_test, y_pred))
    mlflow.log_metric("recall", recall_score(y_test, y_pred))
    mlflow.log_metric("f1", f1_score(y_test, y_pred))

    # Log model
    mlflow.sklearn.log_model(model, "model")

    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("feature_importance.csv")
```

### Experiment Tracking Checklist

| Item | What to Track | Why |
|------|---------------|-----|
| **Code version** | Git commit hash | Reproducibility |
| **Data version** | DVC hash | Reproducibility |
| **Parameters** | All hyperparameters | Comparison |
| **Metrics** | All evaluation metrics | Performance |
| **Artifacts** | Models, plots, configs | Documentation |
| **Tags** | Model type, dataset, version | Organization |

---

## 4. Model Development

### The Baseline-First Approach

```python
# Step 1: Simple baseline
from sklearn.dummy import DummyClassifier

baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
baseline_score = baseline.score(X_test, y_test)
print(f"Baseline accuracy: {baseline_score:.3f}")

# Step 2: Simple ML baseline
from sklearn.linear_model import LogisticRegression

simple_model = LogisticRegression(max_iter=1000)
simple_model.fit(X_train, y_train)
simple_score = simple_model.score(X_test, y_test)
print(f"Simple model accuracy: {simple_score:.3f}")

# Step 3: Complex model (only if justified)
from sklearn.ensemble import GradientBoostingClassifier

complex_model = GradientBoostingClassifier(n_estimators=100)
complex_model.fit(X_train, y_train)
complex_score = complex_model.score(X_test, y_test)
print(f"Complex model accuracy: {complex_score:.3f}")

# Decision: Is the improvement worth the complexity?
improvement = (complex_score - simple_score) / simple_score
print(f"Improvement: {improvement:.1%}")
```

### Model Selection Criteria

| Criterion | Weight | How to Evaluate |
|-----------|--------|-----------------|
| **Performance** | High | Meets business threshold? |
| **Interpretability** | Medium | Can you explain predictions? |
| **Complexity** | Medium | Lines of code, dependencies |
| **Speed** | Medium | Training + inference time |
| **Robustness** | High | Handles edge cases? |
| **Maintainability** | High | Easy to update? |

### Model Registry

```python
# Register best model
mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="churn-prediction-model"
)

# Transition to staging
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="churn-prediction-model",
    version=1,
    stage="Staging"
)

# Transition to production
client.transition_model_version_stage(
    name="churn-prediction-model",
    version=1,
    stage="Production"
)
```

---

## 5. Deployment

### Docker Containerization

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY models/ ./models/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### FastAPI Serving

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import numpy as np

app = FastAPI(title="ML Prediction API", version="1.0.0")

# Load model on startup
model = mlflow.sklearn.load_model("models:/churn-model/Production")

class PredictRequest(BaseModel):
    features: list[float]

class PredictResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_version": "1.0.0"}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    try:
        features = np.array(request.features).reshape(1, -1)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].max()

        return PredictResponse(
            prediction=int(prediction),
            probability=float(probability),
            model_version="1.0.0"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Deployment Patterns

| Pattern | Latency | Use Case | Complexity |
|---------|---------|----------|------------|
| **Batch** | Hours | Daily reports, overnight processing | Low |
| **Real-time API** | <100ms | User-facing features, fraud detection | Medium |
| **Streaming** | Seconds | Real-time analytics, live recommendations | High |
| **Edge** | <10ms | Mobile apps, IoT, privacy-sensitive | High |

---

## 6. Monitoring & Drift Detection

### Evidently AI Setup

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset

# Create drift report
drift_report = Report(metrics=[
    DataDriftPreset(),
    DataQualityPreset()
])

drift_report.run(
    reference_data=reference_df,
    current_data=current_df
)

# Save report
drift_report.save_html("drift_report.html")

# Check if drift detected
drift_score = drift_report.as_dict()["metrics"][0]["result"]["dataset_drift"]
if drift_score:
    print("DRIFT DETECTED — Trigger retraining")
```

### Monitoring Dashboard Metrics

| Category | Metric | Threshold | Alert |
|----------|--------|-----------|-------|
| **Business** | Revenue impact | < baseline | Immediate |
| **Business** | Cost savings | < baseline | Immediate |
| **Model** | Accuracy | Drop >5% | Warning |
| **Model** | Precision/Recall | Drop >5% | Warning |
| **Data** | Missing values | >5% | Warning |
| **Data** | Feature drift | KS test p < 0.05 | Warning |
| **System** | Latency | >500ms | Critical |
| **System** | Error rate | >5% | Critical |
| **System** | Throughput | < baseline | Warning |

### Retraining Strategy

| Trigger | Action | Timeline |
|---------|--------|----------|
| **Scheduled** | Retrain monthly | Fixed date |
| **Drift detected** | Retrain immediately | Within 48 hours |
| **Performance drop** | Investigate + retrain | Within 1 week |
| **New data available** | Evaluate + retrain | Within 2 weeks |

---

## 7. AI Prompts

### Prompt 1: MLOps Architecture Designer

```
Act as an MLOps architect.

Project requirements:
- Problem: [PREDICTION TYPE]
- Data: [SOURCE, SIZE, FREQUENCY]
- Latency: [BATCH/REAL-TIME]
- Scale: [REQUESTS/DAY]
- Budget: [MONTHLY INFRASTRUCTURE]

Design a complete MLOps pipeline:
1. Data pipeline (ingestion, validation, versioning)
2. Feature engineering (store, transformations)
3. Training pipeline (experiment tracking, model registry)
4. Deployment (containerization, serving, scaling)
5. Monitoring (drift, performance, business metrics)
6. Retraining (triggers, automation, rollback)

Specify tools for each stage and justify choices.
Include cost estimates where possible.
```

### Prompt 2: Model Comparison Report

```
Act as an ML engineer.

I trained these models:
- Baseline: [MODEL] → [METRICS]
- Model A: [MODEL] → [METRICS]
- Model B: [MODEL] → [METRICS]

Create a comparison report:
1. Performance table (all metrics)
2. Complexity analysis (training time, inference time, model size)
3. Interpretability assessment
4. Robustness testing results
5. Recommendation with justification

Use professional, data-driven language.
Include confidence intervals where applicable.
```

### Prompt 3: Monitoring Setup Guide

```
Act as an MLOps engineer.

Production system:
- Model: [TYPE]
- Deployment: [DOCKER/CLOUD RUN/K8S]
- Data: [FEATURES]
- Business metric: [KPI]

Design a monitoring setup:
1. Metrics to track (business + model + system)
2. Tools to use (open source preferred)
3. Alert thresholds
4. Dashboard layout
5. Incident response playbook
6. Retraining triggers

Make it production-ready, not theoretical.
```

---

## 8. Action Checklist

### Week 1: Pipeline Setup

- [ ] Initialize DVC for data versioning
- [ ] Set up Great Expectations for data validation
- [ ] Configure MLflow tracking server
- [ ] Create experiment structure
- [ ] Set up feature store (or custom solution)

### Week 2: Model Development

- [ ] Establish baseline (simple model)
- [ ] Run experiments with tracking
- [ ] Compare models using MLflow
- [ ] Register best model to registry
- [ ] Document model selection rationale

### Week 3: Deployment

- [ ] Containerize with Docker
- [ ] Build FastAPI serving layer
- [ ] Deploy to staging environment
- [ ] Run load tests
- [ ] Set up CI/CD pipeline

### Week 4: Monitoring

- [ ] Configure Evidently AI drift detection
- [ ] Set up Grafana/Prometheus dashboards
- [ ] Define alert thresholds
- [ ] Test alert delivery
- [ ] Document incident response plan

---

> **Next:** [04E: Testing & QA →](04E-TESTING-QA.md)
>
> *"A model in production without monitoring is a ticking time bomb."*

---

*Module 04D | MLOps Pipeline | Version 2026.05*
