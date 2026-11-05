---
name: agyos-swarm-prediction-engine
description: Multi-agent swarm intelligence and scenario prediction engine. Builds GraphRAG knowledge graphs from seed documents, provisions memory-backed synthetic agent populations, executes multi-round market and behavioral simulations, and compiles structured prediction reports.
---

# AGYOS Swarm Intelligence Prediction Engine

A structured operational framework for configuring, running, and analyzing multi-agent swarm simulations. It ingests seed documents, constructs an ontology and knowledge graph, initializes a population of synthetic agents with episodic memory, simulates multi-round behavioral interactions, and synthesizes empirical outcome reports.

## 1. System Architecture & Component Mapping

The simulation architecture operates across four distinct subsystems:

1. Interaction Frontend: Web interface (default port 3000) for uploading seed material, defining prediction hypotheses, tracking real-time agent dialogues, and reviewing compiled reports.
2. Simulation Backend: API server (default port 5001) managing document parsing, ontology generation, simulation state loops, and entity memory stores.
3. Language Model Inference: OpenAI-compatible LLM endpoint powering agent decision-making, dialogue generation, and final report synthesis.
4. Entity Memory & Knowledge Graph: GraphRAG knowledge store anchoring agent personas to verified ground truths extracted from uploaded source material.

## 2. Environment Configuration

Define the required parameters in `.env` before initiating simulations:

```bash
# Core LLM Inference
LLM_API_KEY="your-llm-api-key"
LLM_BASE_URL="https://api.deepseek.com/v1"
LLM_MODEL_NAME="deepseek-chat"

# Secondary Fast / Summarizer Model (Optional)
LLM_BOOST_API_KEY=""
LLM_BOOST_BASE_URL=""
LLM_BOOST_MODEL_NAME=""

# Graph Memory Provider
ZEP_API_KEY="your-zep-api-key"

# Simulation Bounds
OASIS_DEFAULT_MAX_ROUNDS=10

# Networking (Remote / Production Deployments)
VITE_API_BASE_URL="http://localhost:5001"
```

Security note: Never commit `.env` containing live API credentials to version control.

## 3. Deployment & Startup Paths

### Option A: Local Source Installation

Prerequisites: Node.js 18+, Python 3.11-3.12, `uv` package manager.

```bash
# 1. Install dependencies across frontend and backend
npm run setup:all

# 2. Launch concurrent development servers
npm run dev
```

### Option B: Containerized Deployment (Docker Compose)

```yaml
version: "3.8"
services:
  simulation-engine:
    image: agyos/swarm-engine:latest
    env_file: .env
    ports:
      - "3000:3000"
      - "5001:5001"
    volumes:
      - ./backend/uploads:/app/backend/uploads
    restart: unless-stopped
```

Launch with persistent upload storage:
```bash
docker compose up -d
docker compose logs -f
```

## 4. Simulation Execution Protocol

Follow this 5-stage procedure to maximize simulation signal:

1. Curate Seed Documents:
   - Provide concise, factual source documents (product specifications, pricing proposals, policy drafts, or competitor briefs).
   - Avoid uploading multi-megabyte unstructured dumps; concise inputs produce sharper graph ontologies and lower inference expenditure.

2. Frame Explicit Prediction Goals:
   - Formulate falsifiable, specific scenario prompts:
     - Good: "How will self-employed freelancers react to a 15% price increase with an added invoicing feature?"
     - Weak: "Predict the future of SaaS."

3. Construct Ontology & Graph:
   - The engine parses seed text, identifies key entities (users, competitors, institutions), and builds relational graph nodes in memory.

4. Execute Calibration Round:
   - Run a test pass capped at 5–10 rounds (`OASIS_DEFAULT_MAX_ROUNDS=10`).
   - Monitor token consumption and inspect agent dialogues to ensure personas adhere to their specified behavioral priors.

5. Report Interrogation & Entity Audits:
   - Review the synthesized scenario report.
   - Query individual synthetic agents directly through the interface to inspect the exact rationales, biases, and memory associations that shaped their simulated decisions.

## 5. Operational Troubleshooting

- Port Collision: If port 3000 or 5001 is already bound, modify the host mapping (e.g., `-p 8080:3000 -p 5002:5001`).
- Graph Generation Failure: Verify memory service API keys and confirm outbound network egress to the GraphRAG service endpoint.
- Missing Uploads Across Restarts: Confirm that the host directory `./backend/uploads` is mapped into `/app/backend/uploads` inside the container.
- Remote Cross-Origin Errors: Ensure `VITE_API_BASE_URL` matches the external IP or domain of the host machine rather than `localhost`.
