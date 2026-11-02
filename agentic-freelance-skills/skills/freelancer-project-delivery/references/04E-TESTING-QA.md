---
module: "04-PROJECT-DELIVERY"
part: "E"
title: "Testing & QA"
version: "2026.05"
status: "Production-Ready"
---

# 04E: Testing & QA

> **Core Principle:** Testing is not a phase. It is a continuous practice that starts before the first line of code and ends only when the system is decommissioned.
>
> *"Production deployment always reveals weaknesses you didn't test. The more you test before deployment, the fewer surprises after."* — Ayush Singh

---

## Table of Contents

1. [The Test Pyramid](#1-the-test-pyramid)
2. [Unit Testing](#2-unit-testing)
3. [Integration Testing](#3-integration-testing)
4. [Robustness Testing](#4-robustness-testing)
5. [Performance Testing](#5-performance-testing)
6. [AI Prompts](#6-ai-prompts)
7. [Action Checklist](#7-action-checklist)

---

## 1. The Test Pyramid

```
         /\
        /  \
       / E2E \      <- 10% of tests (slow, expensive)
      /--------\
     / Integration\  <- 20% of tests (medium speed)
    /--------------\
   /    Unit Tests   \ <- 70% of tests (fast, cheap)
  /--------------------\
```

### Test Distribution

| Level | % of Tests | Speed | Cost | Purpose |
|-------|-----------|-------|------|---------|
| **Unit** | 70% | <1 sec | Low | Test functions in isolation |
| **Integration** | 20% | 1-10 sec | Medium | Test component interactions |
| **E2E** | 10% | 10-60 sec | High | Test full user flows |

---

## 2. Unit Testing

### pytest Best Practices

```python
# tests/test_data_pipeline.py
import pytest
import pandas as pd
from src.data_pipeline import clean_data, validate_data

class TestDataPipeline:
    def test_clean_data_removes_nulls(self):
        # Arrange
        df = pd.DataFrame({
            'customer_id': [1, 2, None],
            'age': [25, 30, 35]
        })

        # Act
        result = clean_data(df)

        # Assert
        assert result['customer_id'].isnull().sum() == 0
        assert len(result) == 2

    def test_clean_data_handles_empty_df(self):
        df = pd.DataFrame()
        result = clean_data(df)
        assert len(result) == 0

    def test_validate_data_checks_ranges(self):
        df = pd.DataFrame({
            'age': [25, 150, 30]  # 150 is invalid
        })

        with pytest.raises(ValueError, match="age out of range"):
            validate_data(df)

    @pytest.mark.parametrize("input_age,expected", [
        (25, True),
        (17, False),
        (100, True),
        (101, False)
    ])
    def test_age_validation(self, input_age, expected):
        result = is_valid_age(input_age)
        assert result == expected
```

### Test Coverage Targets

| Component | Target Coverage | Minimum |
|-----------|----------------|---------|
| **Data pipeline** | 90% | 80% |
| **Feature engineering** | 85% | 75% |
| **Model training** | 80% | 70% |
| **API endpoints** | 95% | 85% |
| **Utilities** | 90% | 80% |

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_data_pipeline.py

# Run with verbose output
pytest -v

# Run failed tests only
pytest --lf

# Run in parallel
pytest -n auto
```

---

## 3. Integration Testing

### API Integration Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

class TestAPI:
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_predict_endpoint_valid_input(self):
        response = client.post("/predict", json={
            "features": [25.0, 100.0, 2.0, 0.0, 1.0]
        })
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "probability" in data
        assert 0 <= data["probability"] <= 1

    def test_predict_endpoint_invalid_input(self):
        response = client.post("/predict", json={
            "features": "not_a_list"
        })
        assert response.status_code == 422

    def test_predict_endpoint_missing_features(self):
        response = client.post("/predict", json={})
        assert response.status_code == 422

    def test_predict_endpoint_wrong_feature_count(self):
        response = client.post("/predict", json={
            "features": [1.0, 2.0]  # Too few features
        })
        assert response.status_code == 400
```

### Data Pipeline Integration Tests

```python
# tests/test_pipeline_integration.py
import pytest
from src.pipeline import run_pipeline

class TestPipelineIntegration:
    def test_full_pipeline_runs(self):
        result = run_pipeline(
            input_path="tests/data/sample.csv",
            output_path="tests/output/"
        )
        assert result["status"] == "success"
        assert result["rows_processed"] > 0
        assert result["model_accuracy"] > 0.7

    def test_pipeline_handles_corrupted_data(self):
        result = run_pipeline(
            input_path="tests/data/corrupted.csv"
        )
        assert result["status"] == "partial_success"
        assert result["rows_dropped"] > 0
```

---

## 4. Robustness Testing

### Missing Features Test

```python
def test_missing_features():
    # Test model performance when features are missing
    for feature in feature_names:
        X_test_missing = X_test.copy()
        X_test_missing[feature] = np.nan

        predictions = model.predict(X_test_missing)
        accuracy = accuracy_score(y_test, predictions)

        # Model should still work, maybe with reduced accuracy
        assert accuracy > baseline_accuracy * 0.8
```

### Distributional Shift Test

```python
def test_distributional_shift():
    # Test model on data from different time period
    X_new_period = load_data("different_time_period.csv")
    predictions = model.predict(X_new_period)

    # Distribution of predictions should be similar
    assert abs(predictions.mean() - training_predictions.mean()) < 0.1
```

### Adversarial Input Test

```python
def test_adversarial_inputs():
    # Test model with edge cases and boundary conditions
    edge_cases = [
        [0, 0, 0, 0, 0],      # All zeros
        [999999, 999999, 999, 999, 999],  # Very large values
        [-1, -1, -1, -1, -1],  # Negative values
    ]

    for case in edge_cases:
        try:
            result = model.predict([case])
            # Should not crash, may return default/error
        except Exception as e:
            # Should return meaningful error, not crash
            assert isinstance(e, ValueError)
```

### Data Quality Degradation Test

```python
def test_data_quality_degradation():
    # Test with noisy/corrupted data
    noise_levels = [0.01, 0.05, 0.1, 0.2]

    for noise in noise_levels:
        X_noisy = X_test + np.random.normal(0, noise, X_test.shape)
        predictions = model.predict(X_noisy)
        accuracy = accuracy_score(y_test, predictions)

        # Accuracy should degrade gracefully
        assert accuracy > baseline_accuracy * (1 - noise * 2)
```

---

## 5. Performance Testing

### Load Testing with locust

```python
# locustfile.py
from locust import HttpUser, task, between

class MLAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def predict(self):
        self.client.post("/predict", json={
            "features": [25.0, 100.0, 2.0, 0.0, 1.0]
        })

    @task(1)
    def health_check(self):
        self.client.get("/health")
```

### Performance Benchmarks

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| **API latency (p50)** | <100ms | >200ms |
| **API latency (p99)** | <500ms | >1000ms |
| **Throughput** | >100 req/sec | <50 req/sec |
| **Model load time** | <5 sec | >30 sec |
| **Memory usage** | <1GB | >2GB |
| **CPU usage** | <50% | >80% |

### Benchmark Script

```python
import time
import requests
import statistics

url = "http://localhost:8000/predict"
payload = {"features": [25.0, 100.0, 2.0, 0.0, 1.0]}

latencies = []
for _ in range(100):
    start = time.time()
    response = requests.post(url, json=payload)
    end = time.time()
    latencies.append((end - start) * 1000)

print(f"p50: {statistics.median(latencies):.1f}ms")
print(f"p95: {statistics.quantiles(latencies, n=20)[18]:.1f}ms")
print(f"p99: {statistics.quantiles(latencies, n=100)[98]:.1f}ms")
```

---

## 6. AI Prompts

### Prompt 1: Test Case Generator

```
Act as a QA engineer.

Function to test:
[PASTE FUNCTION CODE]

Generate:
1. 5 unit tests (happy path + edge cases)
2. 2 integration tests (with mock dependencies)
3. 1 robustness test (adversarial input)
4. 1 performance test (benchmark)

Use pytest. Include fixtures where appropriate.
Make tests independent and deterministic.
```

### Prompt 2: Test Coverage Analyzer

```
Act as a code quality analyst.

Current test coverage: [X]%
Untested files: [LIST]

Create a plan to reach 80%+ coverage:
1. Priority order for adding tests
2. Specific test cases for each untested file
3. Integration test scenarios
4. Mock/stub strategy for external dependencies
5. Estimated time to complete

Focus on high-impact tests first.
```

### Prompt 3: Load Test Designer

```
Act as a performance engineer.

API details:
- Endpoints: [LIST]
- Expected traffic: [REQUESTS/DAY]
- Peak traffic: [REQUESTS/SEC]
- SLA: [LATENCY TARGET]

Design load tests:
1. locustfile.py with realistic user behavior
2. Benchmark script for single-request latency
3. Stress test plan (how to find breaking point)
4. Performance regression test (compare to baseline)
5. Monitoring setup for load tests

Include expected results and pass/fail criteria.
```

---

## 7. Action Checklist

### Project Setup

- [ ] Install pytest and coverage tools
- [ ] Create tests/ directory structure
- [ ] Set up conftest.py with fixtures
- [ ] Configure CI to run tests on every push
- [ ] Set coverage target (80% minimum)

### Development

- [ ] Write unit tests for every new function
- [ ] Write integration tests for API endpoints
- [ ] Add robustness tests for model inputs
- [ ] Run tests before every commit
- [ ] Fix failing tests immediately

### Pre-Deployment

- [ ] Run full test suite (unit + integration)
- [ ] Run performance benchmarks
- [ ] Run load tests
- [ ] Check test coverage report
- [ ] Document any known test gaps

---

> **Next:** [04F: Delivery & Handoff →](04F-DELIVERY-HANDOFF.md)
>
> *"Untested code is broken code. Test everything, trust nothing."*

---

*Module 04E | Testing & QA | Version 2026.05*
