---
title: "07B — Architecture Templates"
description: "System design documents, API specification templates, and Architecture Decision Records (ADR) for production-grade freelance projects."
version: "2026.05"
---

# 07B — ARCHITECTURE-TEMPLATES

> **Rule:** Write the architecture document BEFORE writing code. Share it with the client for alignment. It prevents expensive redesigns and proves you think like a senior engineer.

---

## Template 1: System Design Document (SDD)

**Use for:** Any project with >2 components, external APIs, databases, or deployment infrastructure.

```markdown
# System Design Document: [Project Name]

## Metadata
- **Author:** [Your Name]
- **Client:** [Client Name]
- **Date:** [YYYY-MM-DD]
- **Status:** DRAFT / REVIEW / APPROVED
- **Version:** 1.0

---

## 1. Executive Summary

One-paragraph description of what this system does and why it exists.

**Business Goal:** [e.g., Reduce customer churn by 15% through automated risk scoring]
**Technical Goal:** [e.g., Deploy a real-time prediction API with <100ms latency]

---

## 2. Requirements

### 2.1 Functional Requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | System shall ingest user behavior events | Must |
| FR-02 | System shall generate churn risk scores | Must |
| FR-03 | System shall expose scores via REST API | Must |
| FR-04 | System shall send alerts to CRM | Should |

### 2.2 Non-Functional Requirements
| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | API latency (p99) | < 100ms |
| NFR-02 | Availability | 99.5% |
| NFR-03 | Daily prediction throughput | 100,000 |
| NFR-04 | Model retraining frequency | Weekly |
| NFR-05 | Data retention | 2 years |

### 2.3 Constraints
- Budget: $[X]/month infrastructure
- Timeline: [X] weeks
- Solo developer; no DevOps team
- Must run on GCP free tier or Cloud Run

---

## 3. Architecture Overview

### 3.1 High-Level Diagram
```text
[Data Source] → [Ingestion Service] → [Feature Store / DB]
                                    ↓
[Client App] → [API Gateway] → [Model Serving] → [Prediction Cache]
                                    ↓
                              [Monitoring & Alerting]
```

### 3.2 Component Descriptions
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| Ingestion | Python + Cloud Functions | Parse and validate events |
| Database | PostgreSQL / BigQuery | Store raw events and features |
| Feature Store | Feast / Custom | Serve consistent features |
| Model Serving | FastAPI + Docker | Host model, validate inputs |
| Cache | Redis | Cache frequent predictions |
| Monitoring | Prometheus + Grafana | Metrics, drift, alerts |

---

## 4. Data Design

### 4.1 Data Model
```sql
-- Core tables
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    created_at TIMESTAMP,
    segment VARCHAR(50)
);

CREATE TABLE events (
    event_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    event_type VARCHAR(50),
    timestamp TIMESTAMP,
    metadata JSONB
);

CREATE TABLE predictions (
    prediction_id UUID PRIMARY KEY,
    user_id UUID,
    score FLOAT,
    model_version VARCHAR(20),
    created_at TIMESTAMP
);
```

### 4.2 Data Flow
1. Events ingested via webhook → validated → written to `events`
2. ETL job (Airflow/ZenML) aggregates features → writes to `features`
3. Model serving reads from `features` → returns prediction
4. Predictions logged to `predictions` for monitoring

---

## 5. API Design

### 5.1 Endpoint Specification

#### POST /predict
**Request:**
```json
{
  "user_id": "uuid",
  "context": {
    "device": "mobile",
    "country": "US"
  }
}
```

**Response (200):**
```json
{
  "user_id": "uuid",
  "churn_probability": 0.73,
  "risk_tier": "high",
  "model_version": "v2.1.4",
  "timestamp": "2026-05-16T12:00:00Z",
  "explanation": {
    "top_features": ["days_since_login", "support_tickets"]
  }
}
```

**Response (400):**
```json
{
  "error": "Invalid user_id format",
  "code": "VALIDATION_ERROR"
}
```

**Response (500):**
```json
{
  "error": "Prediction service unavailable",
  "code": "INTERNAL_ERROR",
  "retry_after": 30
}
```

### 5.2 Authentication
- API Key via `X-API-Key` header
- Rate limit: 100 req/min per key
- CORS: Allow only `client-domain.com`

---

## 6. Deployment Architecture

### 6.1 Environment Strategy
| Env | Purpose | Trigger |
|-----|---------|---------|
| dev | Local development | Manual |
| staging | Pre-production testing | Push to `develop` branch |
| prod | Live traffic | Merge to `main` + manual approval |

### 6.2 CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t gcr.io/PROJECT/app:$GITHUB_SHA .
      - run: docker push gcr.io/PROJECT/app:$GITHUB_SHA
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: gcloud run deploy app --image gcr.io/PROJECT/app:$GITHUB_SHA
```

### 6.3 Rollback Plan
- Keep previous 3 Docker image tags in registry
- Cloud Run revision rollback: `gcloud run services update-traffic --to-revisions v2=0,v1=100`
- Database migrations: backward-compatible only; never drop columns in same deploy

---

## 7. Monitoring & Alerting

| Metric | Tool | Threshold | Alert |
|--------|------|-----------|-------|
| Request latency (p99) | Prometheus | > 200ms | PagerDuty/Slack |
| Error rate | Prometheus | > 1% | PagerDuty/Slack |
| Prediction drift | Evidently AI | KS test p < 0.05 | Email |
| Feature freshness | Custom | > 1 hour stale | Slack |
| Infrastructure cost | GCP Billing | > $X/day | Email |

---

## 8. Security Considerations

- Input validation via Pydantic models
- SQL injection prevention via ORM parameterized queries
- No secrets in code; use Secret Manager
- API key rotation every 90 days
- GDPR: Right to deletion implemented via `DELETE /users/{id}` cascade

---

## 9. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Model degradation | Medium | High | Automated retraining + drift alerts |
| API rate limit exceeded | Low | Medium | Caching + client backoff strategy |
| Data source outage | Low | High | Fallback to cached features + stale alert |
| Scope creep | High | Medium | Strict ADR process + change requests billed |

---

## 10. Appendix

- **Related ADRs:** ADR-001 (Model Selection), ADR-002 (Database Choice)
- **Change Log:**
  - v1.0 (2026-05-16): Initial draft
```

---

## Template 2: Architecture Decision Record (ADR)

**Use for:** Every significant technical choice (database, framework, deployment pattern, model type).

```markdown
# ADR-[NUMBER]: [Short Title]

## Status
- Proposed / Accepted / Deprecated / Superseded by ADR-XXX

## Context
What is the problem or opportunity? What forces are at play?

## Decision
What did we decide? Be specific.

## Consequences

### Positive
- [e.g., Faster inference due to compiled model format]
- [e.g., Reduced vendor lock-in with open-source stack]

### Negative
- [e.g., Steeper learning curve for client maintenance team]
- [e.g., Self-hosted = higher ops burden for solo freelancer]

### Risks
- [e.g., Community support may decline for chosen framework]

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| [Option A] | [Specific reason with data] |
| [Option B] | [Specific reason with data] |

## Related Decisions
- ADR-XXX (depends on this)
- ADR-YYY (informed by this)

## Date
YYYY-MM-DD

## Author
[Your Name]
```

**ADR Examples for Common Freelance Scenarios:**

| Decision | Context | Decision | Consequences |
|----------|---------|----------|--------------|
| ADR-1: Model Format | Need fast inference | ONNX Runtime | +2x speed, -slightly larger binary |
| ADR-2: Database | Client has no DBA | PostgreSQL on Cloud SQL | +managed backups, -$25/mo cost |
| ADR-3: Auth | No OAuth team | API Keys + JWT | +simple, -key rotation burden |
| ADR-4: Deployment | No Kubernetes team | Cloud Run | +serverless scaling, -cold start 2s |
| ADR-5: Frontend | Client needs internal tool | Streamlit | +fast build, -not consumer-grade UI |

---

## Template 3: API Specification (OpenAPI-Style)

**Use for:** Any REST API deliverable. Share with client before implementation.

```yaml
openapi: 3.0.0
info:
  title: [Project] Prediction API
  version: 1.0.0
  description: |
    [One-paragraph description]

    **Base URL:** `https://api.client-domain.com/v1`

    **Authentication:** API Key in `X-API-Key` header.

servers:
  - url: https://api.client-domain.com/v1
    description: Production
  - url: https://staging-api.client-domain.com/v1
    description: Staging

paths:
  /predict:
    post:
      summary: Generate prediction
      description: |
        Returns a risk score or classification for the given entity.

        **Rate Limit:** 100 req/min
        **Timeout:** 5s
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [entity_id]
              properties:
                entity_id:
                  type: string
                  format: uuid
                  example: "550e8400-e29b-41d4-a716-446655440000"
                context:
                  type: object
                  example: { "device": "mobile" }
      responses:
        "200":
          description: Successful prediction
          content:
            application/json:
              schema:
                type: object
                properties:
                  entity_id: { type: string }
                  score: { type: number, minimum: 0, maximum: 1 }
                  model_version: { type: string }
                  timestamp: { type: string, format: date-time }
        "400":
          description: Validation error
          content:
            application/json:
              schema:
                type: object
                properties:
                  error: { type: string }
                  code: { type: string }
        "429":
          description: Rate limit exceeded
          headers:
            Retry-After:
              schema:
                type: integer
              description: Seconds until retry
        "500":
          description: Internal error

  /health:
    get:
      summary: Health check
      responses:
        "200":
          description: Service healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: { type: string, example: "ok" }
                  version: { type: string }
                  timestamp: { type: string, format: date-time }

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - ApiKeyAuth: []
```

---

## Template 4: Decision Matrix

**Use for:** Justifying tool/framework selection to client or for your own records.

```markdown
# Decision Matrix: [Decision Topic]

## Criteria & Weights
| Criterion | Weight | Description |
|-----------|--------|-------------|
| Development Speed | 25% | Time to MVP |
| Maintenance Burden | 20% | Solo ops cost |
| Performance | 20% | Latency / throughput |
| Ecosystem | 15% | Libraries / community |
| Client Familiarity | 10% | Can client maintain? |
| Cost | 10% | Infrastructure spend |

## Options
| Criterion | Option A: [X] | Option B: [Y] | Option C: [Z] |
|-----------|---------------|---------------|---------------|
| Dev Speed | 9/10 | 7/10 | 6/10 |
| Maintenance | 7/10 | 8/10 | 5/10 |
| Performance | 8/10 | 9/10 | 7/10 |
| Ecosystem | 9/10 | 7/10 | 8/10 |
| Familiarity | 6/10 | 9/10 | 4/10 |
| Cost | 8/10 | 6/10 | 9/10 |
| **Weighted Score** | **8.05** | **7.65** | **6.55** |

## Winner: Option A
**Rationale:** Highest weighted score. Trade-off of lower client familiarity is acceptable because documentation and runbook will bridge the gap.
```

---

## Action Checklist

- [ ] Create `docs/architecture/` folder in every client repo.
- [ ] Write ADR within 24 hours of every major technical decision.
- [ ] Share SDD with client BEFORE Week 1 development begins.
- [ ] Export API spec to Swagger UI for client testing.
- [ ] Review all ADRs during project retrospectives.

---

*Reference: Technical spec templates and ADR best practices from 2026 engineering standards.*
