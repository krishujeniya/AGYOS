---
title: "07D — Monitoring Playbooks"
description: "Production monitoring setup for ML systems: Prometheus metrics, Grafana dashboards, drift detection, alerting rules, and incident response runbooks."
version: "2026.05"
---

# 07D — MONITORING-PLAYBOOKS

> **Rule:** If you cannot measure it, you cannot improve it. If you do not monitor it, it will break. Deploy monitoring BEFORE going live.

---

## Playbook 1: Prometheus + Grafana Stack Setup

### 1.1 Prometheus Configuration

**File:** `monitoring/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: "ml-api"
    static_configs:
      - targets: ["api:8000"]
    metrics_path: "/metrics"
    scrape_interval: 10s

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]

  - job_name: "postgres-exporter"
    static_configs:
      - targets: ["postgres-exporter:9187"]
```

### 1.2 Alert Rules

**File:** `monitoring/alert_rules.yml`

```yaml
groups:
  - name: ml_api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(errors_total[5m]) > 0.01
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec for {{ $labels.instance }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(prediction_latency_seconds_bucket[5m])) > 0.2
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "High prediction latency"
          description: "p99 latency is {{ $value }}s"

      - alert: ModelNotLoaded
        expr: up{job="ml-api"} == 1 and predictions_total == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Model may not be loaded"
          description: "API is up but no predictions served in 5 minutes"

      - alert: FeatureDriftDetected
        expr: feature_drift_score > 0.1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Feature drift detected"
          description: "KS test score {{ $value }} exceeds threshold"

      - alert: PredictionDistributionShift
        expr: abs(avg_over_time(prediction_mean[1h]) - prediction_mean_baseline) > 0.05
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Prediction distribution shifted"
          description: "Mean prediction drifted by {{ $value }} from baseline"

      - alert: DataFreshnessStale
        expr: time() - max(feature_timestamp) > 3600
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Features are stale"
          description: "No fresh features in over 1 hour"

      - alert: InfrastructureCostSpike
        expr: daily_infrastructure_cost > 50
        for: 1h
        labels:
          severity: info
        annotations:
          summary: "Cost spike detected"
          description: "Daily cost is ${{ $value }}"
```

### 1.3 Docker Compose for Monitoring Stack

**File:** `docker-compose.monitoring.yml`

```yaml
version: "3.8"

services:
  prometheus:
    image: prom/prometheus:v2.51.0
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./monitoring/alert_rules.yml:/etc/prometheus/alert_rules.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"

  grafana:
    image: grafana/grafana:10.4.0
    volumes:
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  alertmanager:
    image: prom/alertmanager:v0.27.0
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"

volumes:
  prometheus_data:
  grafana_data:
```

---

## Playbook 2: Grafana Dashboard JSON

**File:** `monitoring/grafana/dashboards/ml-system.json`

```json
{
  "dashboard": {
    "title": "ML System Monitoring",
    "tags": ["ml", "production"],
    "timezone": "utc",
    "panels": [
      {
        "title": "Request Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(predictions_total[5m])",
            "legendFormat": "{{ model_version }}"
          }
        ],
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 0}
      },
      {
        "title": "Error Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(errors_total[5m])",
            "legendFormat": "{{ error_type }}"
          }
        ],
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 0}
      },
      {
        "title": "Latency (p50/p95/p99)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(prediction_latency_seconds_bucket[5m]))",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, rate(prediction_latency_seconds_bucket[5m]))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, rate(prediction_latency_seconds_bucket[5m]))",
            "legendFormat": "p99"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      },
      {
        "title": "Feature Drift Over Time",
        "type": "graph",
        "targets": [
          {
            "expr": "feature_drift_score",
            "legendFormat": "{{ feature_name }}"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {"params": [0.1], "type": "gt"},
              "query": {"model": {"expr": "feature_drift_score"}}
            }
          ]
        },
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4}
      },
      {
        "title": "Prediction Distribution",
        "type": "graph",
        "targets": [
          {
            "expr": "avg_over_time(prediction_mean[1h])",
            "legendFormat": "Current Mean"
          },
          {
            "expr": "prediction_mean_baseline",
            "legendFormat": "Baseline Mean"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
      },
      {
        "title": "Model Version Distribution",
        "type": "piechart",
        "targets": [
          {
            "expr": "sum by (model_version) (predictions_total)",
            "legendFormat": "{{ model_version }}"
          }
        ],
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 12}
      },
      {
        "title": "Infrastructure Cost",
        "type": "stat",
        "targets": [
          {
            "expr": "daily_infrastructure_cost",
            "legendFormat": "Daily $"
          }
        ],
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 12}
      }
    ]
  }
}
```

---

## Playbook 3: Drift Detection Implementation

**File:** `src/drift_detection.py`

```python
"""
Drift detection using statistical tests and Prometheus metrics.
Reference: Prometheus + Grafana drift detection patterns (2025)
"""

import numpy as np
import pandas as pd
from scipy import stats
from prometheus_client import Gauge
import joblib

# Prometheus metrics for drift
FEATURE_DRIFT = Gauge("feature_drift_score", "Drift score per feature", ["feature_name"])
PREDICTION_MEAN = Gauge("prediction_mean", "Current prediction mean")
PREDICTION_MEAN_BASELINE = Gauge("prediction_mean_baseline", "Baseline prediction mean")
ERROR_DRIFT = Gauge("error_drift_score", "Error drift score")

class DriftDetector:
    def __init__(self, reference_data: pd.DataFrame, reference_predictions: np.ndarray):
        self.reference_data = reference_data
        self.reference_predictions = reference_predictions
        self.reference_stats = self._compute_stats(reference_data)

        # Set baseline metrics
        PREDICTION_MEAN_BASELINE.set(np.mean(reference_predictions))

    def _compute_stats(self, df: pd.DataFrame) -> dict:
        stats_dict = {}
        for col in df.select_dtypes(include=[np.number]).columns:
            stats_dict[col] = {
                "mean": df[col].mean(),
                "std": df[col].std(),
                "min": df[col].min(),
                "max": df[col].max(),
            }
        return stats_dict

    def detect_feature_drift(self, current_data: pd.DataFrame) -> dict:
        drift_scores = {}
        for col in self.reference_stats.keys():
            if col not in current_data.columns:
                continue

            ref = self.reference_data[col].dropna()
            cur = current_data[col].dropna()

            # KS test for continuous features
            ks_stat, p_value = stats.ks_2samp(ref, cur)
            drift_scores[col] = {
                "ks_statistic": float(ks_stat),
                "p_value": float(p_value),
                "drift_detected": p_value < 0.05,
            }

            # Update Prometheus metric
            FEATURE_DRIFT.labels(feature_name=col).set(float(ks_stat))

        return drift_scores

    def detect_prediction_drift(self, current_predictions: np.ndarray) -> dict:
        current_mean = np.mean(current_predictions)
        baseline_mean = np.mean(self.reference_predictions)

        PREDICTION_MEAN.set(current_mean)

        shift = abs(current_mean - baseline_mean)
        relative_shift = shift / baseline_mean if baseline_mean != 0 else 0

        return {
            "current_mean": float(current_mean),
            "baseline_mean": float(baseline_mean),
            "absolute_shift": float(shift),
            "relative_shift": float(relative_shift),
            "drift_detected": relative_shift > 0.05,
        }

    def detect_error_drift(self, current_errors: np.ndarray) -> dict:
        baseline_errors = np.abs(self.reference_predictions - self.reference_data.get("target", 0))

        ks_stat, p_value = stats.ks_2samp(baseline_errors, current_errors)
        ERROR_DRIFT.set(float(ks_stat))

        return {
            "ks_statistic": float(ks_stat),
            "p_value": float(p_value),
            "drift_detected": p_value < 0.05,
        }

    def full_report(self, current_data: pd.DataFrame, current_predictions: np.ndarray) -> dict:
        return {
            "feature_drift": self.detect_feature_drift(current_data),
            "prediction_drift": self.detect_prediction_drift(current_predictions),
            "timestamp": pd.Timestamp.now().isoformat(),
            "overall_drift": any(
                d["drift_detected"] for d in self.detect_feature_drift(current_data).values()
            ) or self.detect_prediction_drift(current_predictions)["drift_detected"],
        }
```

---

## Playbook 4: Incident Response Runbook

**File:** `docs/runbooks/incident-response.md`

```markdown
# Incident Response Runbook

## Severity Levels

| Level | Criteria | Response Time | Escalation |
|-------|----------|---------------|------------|
| SEV-1 | System down, no predictions, revenue impact | 15 min | Immediate client call |
| SEV-2 | Degraded performance, drift detected, accuracy drop | 1 hour | Slack alert + email |
| SEV-3 | Cost spike, non-critical alert | 4 hours | Email digest |
| SEV-4 | Informational, planned maintenance | 24 hours | Weekly report |

## Response Procedures

### SEV-1: System Down
1. **Acknowledge** alert in PagerDuty/Slack
2. **Check** Cloud Run / Kubernetes pod status: `gcloud run services list`
3. **Check** logs: `gcloud logging read "resource.type=cloud_run_revision"`
4. **If** pod crash → Rollback to last known good revision
5. **If** dependency failure → Check database / API status
6. **Communicate** to client within 15 minutes with ETA
7. **Post-mortem** within 24 hours

### SEV-2: Model Degradation
1. **Verify** drift detection report
2. **Check** feature pipeline freshness
3. **If** data issue → Fix pipeline, backfill if needed
4. **If** model issue → Trigger emergency retraining
5. **If** retraining takes >2 hours → Deploy previous model version
6. **Document** root cause in incident log

### SEV-3: Cost Spike
1. **Identify** cost driver in GCP Billing dashboard
2. **Check** if traffic spike is legitimate or attack
3. **If** attack → Enable rate limiting, block IPs
4. **If** legitimate → Scale up resources, optimize caching
5. **Notify** client if cost exceeds agreed budget

## Communication Templates

### Client Notification (SEV-1)
```
Subject: [URGENT] Service Disruption — [Project Name]

Hi [Client Name],

We have detected a service disruption affecting [specific feature].
Impact: [Brief description of business impact].
Status: Investigating root cause.
ETA for resolution: [X] minutes.

We will update you every 30 minutes until resolved.

-[Your Name]
```

### Post-Mortem Template
```markdown
# Post-Mortem: [Incident Title]
Date: [YYYY-MM-DD]
Severity: SEV-[1-4]
Duration: [X] minutes

## Summary
One-paragraph description of what happened.

## Timeline
- 12:00 — Alert fired
- 12:05 — Investigation started
- 12:15 — Root cause identified
- 12:30 — Fix deployed
- 12:45 — Service fully recovered

## Root Cause
What actually caused the incident.

## Impact
- Users affected: [X]
- Predictions missed: [X]
- Revenue impact: $[X]

## Resolution
How the incident was fixed.

## Prevention
What changes prevent recurrence:
- [ ] Monitoring improvement
- [ ] Code fix
- [ ] Process change
- [ ] Documentation update

## Lessons Learned
What we learned and what we will do differently.
```
```

---

## Playbook 5: Evidently AI Integration (Lightweight)

**File:** `src/evidently_monitoring.py`

```python
"""
Lightweight monitoring using Evidently AI reports.
For projects where full Prometheus setup is overkill.
"""

import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, RegressionPreset
from datetime import datetime
import json

class EvidentlyMonitor:
    def __init__(self, reference_data: pd.DataFrame, target_col: str | None = None):
        self.reference = reference_data
        self.target_col = target_col
        self.column_mapping = ColumnMapping(target=target_col) if target_col else None

    def generate_drift_report(self, current_data: pd.DataFrame) -> dict:
        report = Report(metrics=[DataDriftPreset()])
        report.run(
            reference_data=self.reference,
            current_data=current_data,
            column_mapping=self.column_mapping,
        )

        # Extract key metrics
        result = json.loads(report.json())
        drift_share = result["metrics"][0]["result"]["dataset_drift"]

        return {
            "drift_detected": drift_share,
            "report_path": self._save_report(report, "drift"),
            "timestamp": datetime.now().isoformat(),
        }

    def generate_performance_report(self, current_data: pd.DataFrame) -> dict:
        if not self.target_col:
            raise ValueError("Target column required for performance report")

        report = Report(metrics=[RegressionPreset()])
        report.run(
            reference_data=self.reference,
            current_data=current_data,
            column_mapping=self.column_mapping,
        )

        return {
            "report_path": self._save_report(report, "performance"),
            "timestamp": datetime.now().isoformat(),
        }

    def _save_report(self, report: Report, report_type: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"reports/{report_type}_{timestamp}.html"
        report.save_html(path)
        return path
```

---

## Action Checklist

- [ ] Deploy Prometheus + Grafana before first production deployment.
- [ ] Configure all alert rules with appropriate thresholds for your data.
- [ ] Set up Alertmanager routing to Slack and email.
- [ ] Implement `DriftDetector` class and expose metrics via `/metrics` endpoint.
- [ ] Create Grafana dashboard with layered views (strategic → granular).
- [ ] Write incident response runbook and share with client.
- [ ] Run a fire drill: manually trigger an alert and practice response.
- [ ] Schedule weekly review of monitoring dashboards.

---

*Reference: Prometheus + Grafana drift detection patterns, Evidently AI documentation, and 2026 MLOps monitoring standards.*
