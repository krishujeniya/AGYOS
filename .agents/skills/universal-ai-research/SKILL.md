---
name: universal-ai-research
description: >-
  Universal autonomous research pipeline and scientific methodology engine based on 214 principles
  across 8 research domains (GPT Researcher, Research Paper Writing, Paper Agent, K-Dense Scientific
  Skills, Paper Review, Academic Research Agent, AI Research Skills, and Humanizer). Produces 6 core
  artifacts: topic survey, top-5 ranking, selected topic, literature corpus, 11-section synthesis report,
  and run log with noncompensatory novelty and feasibility gates.
metadata:
  version: 3.0.0
  license: MIT
---

# Universal Autonomous AI Research Pipeline (Reference & Operating Runbook v3.0)

A platform-neutral, model-neutral, and tool-adaptive research pipeline for autonomous research agents, coding assistants, and human scholars. Translates ambiguous research fields into defensible research questions, evidence-grounded literature corpora, falsifiable study protocols, and publication-grade synthesis reports.

---

## 1. Operating Invariants & Epistemic Boundaries

### A. Responsible Autonomy & Human Claim Ownership
1. **Direction Ownership**: The human researcher retains permanent ownership of the research direction, scientific claims, ethics compliance, data governance, and publication decisions.
2. **Provisional Recommendations**: Agent-selected topics and study plans are provisional recommendations until explicitly approved by the human researcher.
3. **Execution Guardrails**: The agent must never initiate paid API calls, execute unauthorized full-scale experiments, submit manuscripts, or access private participant data without explicit written consent.

### B. Epistemic Separation of Claims
Every statement and data point must be classified into one of four explicit evidentiary classes:
- `INSPECTED EVIDENCE`: Directly read and verified from primary published text, dataset files, or experimental logs.
- `AGENT INFERENCE`: Logical conclusions, synthesis patterns, or interpretations derived by the agent.
- `PROPOSED HYPOTHESIS`: Unverified conjectures, candidate explanations, or suggested future experiments.
- `USER-REPORTED`: Background assertions, constraints, or prior results provided by the user.

### C. Falsifiability & Noncompensatory Gates
- A high score in impact or feasibility can never compensate for a failed novelty gate or unverified competitor baseline.
- If mandatory claim conditions fail, the agent must **STOP, DROP, or NARROW** the proposal.

---

## 2. Host Capability Discovery & 4 Execution Modes

Before initiating research, detect the host environment and select the matching execution mode:

| Host Mode | Environment Characteristics | Deliverable Strategy |
|---|---|---|
| **Mode A: Research + Files** | Web search / scholarly APIs available; writable local file system. | Full online retrieval; generate 6 physical Markdown files in `runs/<RUN_ID>/`. |
| **Mode B: Research + Chat** | Online retrieval available; no writable local file system. | Full online retrieval; output 6 clearly demarcated inline sections matching artifact names. |
| **Mode C: Offline + Files** | No network retrieval; local file uploads and writable disk present. | Inspect provided documents; generate 6 physical files marked `OFFLINE / EXTERNAL VERIFICATION PENDING`. |
| **Mode D: Offline + Chat** | No network retrieval; no writable local file system. | Structured analysis of user-supplied text; output 6 inline sections detailing research designs and query plans. |

---

## 3. The 6-Stage Research Lifecycle & Mandatory Deliverables

```
[STAGE 1: TOPIC DISCOVERY] ────────► 01_topic_survey.md (15–20 Candidates, 11 Fields)
        │
        ▼
[STAGE 2: EVIDENCE-GATED RANKING] ──► 02_top5_ranking.md & 03_selected_topic.md (Gates & Falsifiers)
        │
        ▼
[STAGE 3: LITERATURE CORPUS] ──────► 04_literature_dataset.md (15–30 Verified Papers, 13 Fields, Verify-or-Drop)
        │
        ▼
[STAGE 4: CROSS-STUDY SYNTHESIS] ──► 05_synthesis_report.md (Exactly 11 Required Sections)
        │
        ▼
[STAGE 5: STUDY PROTOCOL] ─────────► Bounded Protocol in 03_selected_topic.md (Causal & Power Controls)
        │
        ▼
[STAGE 6: REVIEW & HUMANIZATION] ──► 06_run_log.md (Audit, Decisions, 26 Anti-Slop Patterns, Principle Coverage)
```

### Stage 1: Topic Discovery & Frontier Mapping (`01_topic_survey.md`)
Generate 15–20 candidate research topics in the specified field. For every topic, supply all 11 mandatory fields:
1. `Research Topic`: Clear title defining scope.
2. `Specific Research Question`: Focused, testable question.
3. `Why This Topic Matters`: Practical and theoretical significance.
4. `Existing Research Status`: Current state of scholarly knowledge.
5. `What Has Already Been Studied`: Established empirical findings.
6. `What Is Still Unknown`: Unresolved tensions and missing evidence.
7. `The Specific Research Gap`: Precise methodological, population, or theoretical void.
8. `Why the Topic May Be Novel`: Comparison against dated literature searches.
9. `Target Population / Context`: Exact experimental unit or observational domain.
10. `Suggested Methodology`: Qualitative, quantitative, experimental, or mixed-methods with justification.
11. `Literature Search Keywords`: 5–10 targeted search strings.

**Coverage Classification**: Assign each topic one provisional category:
- `Class A`: Apparently unexplored within checked boundary.
- `Class B`: Under-researched with early exploratory literature.
- `Class C`: Active domain with important specific gaps remaining.
- `Class D`: Saturated; exclude unless a distinct orthogonal angle is demonstrated.

### Stage 2: Evidence-Gated Topic Ranking (`02_top5_ranking.md` & `03_selected_topic.md`)
Score each candidate from 0 to 5 across 5 core axes:
1. `Gap Strength`: Significance of the identified void.
2. `Novelty`: Distinctness from existing literature.
3. `Feasibility`: Access to data, compute, experimental units, and methods.
4. `Potential Impact`: Scientific or practical consequence.
5. `Evidence Freshness`: Alignment with recent five-year developments.

**Noncompensatory Critical Gates**:
- `NOVELTY Gate`: `NOT_ASSESSED | PASS | REVISE | FAIL`. Must discriminate against the closest published competitor.
- `FEASIBILITY Gate`: `BLOCK | FEASIBILITY_PILOT_ONLY | EXECUTION_READY | FULL_RUN_READY`. Audits data access, population constraints, ethics, and cost ceilings.
- `Falsifier Chain`: Define minimum claim, closest competitor, and the cheapest decisive falsification test.

### Stage 3: Verified Literature Corpus & Evidence Ledger (`04_literature_dataset.md`)
Assemble a target corpus of 15–30 verified scholarly works. Enforce the **Verify-or-Drop** standard: every included entry must resolve to an authoritative DOI registry, scholarly repository, or peer-reviewed index. Unverified web links must be excluded or separated into a distinct unverified ledger.

For every retained paper, record all 13 mandatory fields:
1. Full Title
2. Authors
3. Publication Year
4. Journal / Conference / Preprint Repository
5. DOI or persistent identifier
6. Direct Verified URL
7. Research Objective
8. Research Methodology & Design
9. Sample Size & Population
10. Key Empirical Findings
11. Acknowledged Limitations
12. Direct Relevance to Research Topic
13. Explicit Author-Identified Gap (distinguished from agent inference)

**Corpus Categorization**: Group papers into:
- `Group A`: Foundational Research
- `Group B`: Recent Research (last 5 years)
- `Group C`: Systematic Reviews & Meta-Analyses
- `Group D`: Studies with Contradictory Findings
- `Group E`: Explicit Gap-Identifying Papers
- `Group F`: Closest Competitor Works

Conclude with a prioritized 5–10 paper **Read First** list with specific justifications.

### Stage 4: Cross-Study Synthesis (`05_synthesis_report.md`)
Synthesize evidence across studies rather than summarizing papers sequentially. The report must contain **exactly these 11 top-level headings**:
1. `## 1. Executive Summary`: Corpus-level overview and evidence confidence.
2. `## 2. State of the Research`: Established knowledge, broad consensus, and boundary uncertainties.
3. `## 3. Key Findings Across Studies`: Cross-study patterns with direct `P###` citations.
4. `## 4. Contradictory Findings`: Empirical disagreements and hypothesized methodological causes.
5. `## 5. Methodologies Used`: Analysis of designs, samples, metrics, and systemic weaknesses.
6. `## 6. Research Gaps`: Specific unanswered questions mapped directly to supporting papers.
7. `## 7. Limitations of Existing Research`: Threats to internal, external, and construct validity.
8. `## 8. Emerging Trends`: Genuine theoretical, technological, and methodological shifts.
9. `## 9. Potential Research Opportunities`: 5–10 structured proposals addressing identified gaps.
10. `## 10. Key Papers to Prioritize`: Final ranked reading order based on relevance.
11. `## 11. Final Takeaway`: Definitive synthesis of what is known, unknown, and next actions.

### Stage 5: Study Design & Safeguards (Included in `03_selected_topic.md`)
Develop a bounded study plan:
- Explicit unit of analysis, controls, and comparison groups.
- Causal identification assumptions vs. associational bounds.
- Statistical power planning and effect size estimates (rejecting p-value reliance alone).
- Predeclared stopping rules and kill conditions.

### Stage 6: Paper Quality Writing & Humanization (`06_run_log.md`)
Review synthesis prose against the **26 Humanizer Anti-Slop Rules**:
1. Remove formulaic "not X but Y" dichotomies.
2. Eliminate dramatic one-line repetition closers.
3. Replace vague philosophical maxims with concrete assertions.
4. Delete staged introductory warm-ups.
5. Remove rebuttals to non-existent imaginary critics.
6. Discard forced rule-of-three groupings.
7. Vary repetitive sentence beginnings.
8. Stop using em dashes as universal thought connectors.
9. Eliminate stacked redundant adverbs and qualifiers.
10. Cut hyphenated buzzword pairs.
11. Prefer direct active agents over passive evasion.
12. Replace generic stock AI vocabulary with ordinary technical precision.
13. Avoid inflating modest findings into world-changing milestones.
14. Replace vague associations with concrete mechanisms.
15. Strip weak participial endings that simulate depth without facts.
16. Delete commercial marketing rhetoric from scientific text.
17. Never cite unnamed "experts" or unreferenced "consensus".
18. Prefer direct verbs over heavy nominalizations.
19. Use bold text solely for functional legibility.
20. Remove decorative, empty headings.
21. Adhere to consistent punctuation conventions.
22. Delete conversational chatbot residue ("Here is the summary").
23. Remove unrequested knowledge-cutoff disclaimers.
24. Avoid repeating section titles in opening sentences.
25. Focus on the scientific subject rather than narrating document activity.
26. Avoid explaining basic domain concepts already known to the intended reader.

---

## 4. Quality Gates Checklist (Q1–Q10)

Before marking any research run complete, audit against these 10 noncompensatory quality gates:
- **Q1 (Source Authenticity)**: All paper IDs resolve to verified scholarly records.
- **Q2 (Claim Grounding)**: Every factual statement maps to directly inspected source content.
- **Q3 (Novelty Discrimination)**: Minimum contribution is differentiated from closest competitors.
- **Q4 (Methodological Validity)**: Causal claims are restricted to designs that isolate causality.
- **Q5 (Feasibility & Ethics)**: Resource, data access, and consent boundaries are respected.
- **Q6 (Structural Coherence)**: Synthesis report contains all 11 required section headings.
- **Q7 (Humanization Compliance)**: All 26 anti-slop patterns audited and corrected.
- **Q8 (Output Completeness)**: 6 artifacts generated with 11 topic fields and 13 paper fields.
- **Q9 (Principle Coverage)**: Applicable principles across R1–R8 documented in `06_run_log.md`.
- **Q10 (Epistemic Integrity)**: Unexamined claims marked unverified; zero fabricated findings.

---

## 5. Principle Routing Register (R1–R8: 214 Principles)

The 214 principles from the research literature are grouped into 8 operational domains:
- **R1 (14 Principles) — GPT Researcher Architecture**: Modular components, provider abstractions, centralized configurations, retriever registries, and event streaming.
- **R2 (22 Principles) — Research Paper Writing**: One core message per paragraph, early topic sentences, reverse outlines, claim-to-evidence alignment, and limitation transparency.
- **R3 (22 Principles) — Paper Agent Production**: Evidence IDs, line-level tracing, no outcome fabrication, structured rebuttal decomposition, and problem-to-evidence slide architecture.
- **R4 (44 Principles) — Scientific Method & Rigor**: Causal estimands, rival hypothesis generation, power simulation, blocking, pseudoreplication avoidance, and risk-of-bias audits.
- **R5 (18 Principles) — Critical Peer Review**: Manuscript-type calibration, derived statistical verification, figure-to-text consistency, and prioritized validity triage.
- **R6 (28 Principles) — Academic Research Agent**: Human claim ownership, cheapest decisive falsifier, freeze baselines, explicit gate states, and cost ceilings.
- **R7 (40 Principles) — AI & ML Research Rigor**: Abstraction ladders, mechanism transfer, one-sentence contribution, ablation completeness, random seed reporting, and compute transparency.
- **R8 (26 Principles) — Humanizer Anti-Slop Standards**: The 26 explicit writing patterns eliminating synthetic chatbot mannerisms and inflated prose.

---

## 6. Execution Command & Automated Scaffolding

To scaffold, initialize, or validate a research run workspace:

```bash
# Initialize a new research workspace for a specified field
python3 scripts/universal_research_runner.py init "DeepSeek-V3 Multi-Token Prediction" -d runs/mtp-research

# Validate completed research artifacts against schema and quality gates
python3 scripts/universal_research_runner.py validate runs/mtp-research
```
