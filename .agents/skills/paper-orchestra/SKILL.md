---
name: paper-orchestra
description: "Automated AI research paper drafting and publication-ready LaTeX manuscript generation using Google Cloud AI Research's PaperOrchestra multi-agent architecture and PaperWritingBench methodology."
metadata:
  origin: google-research
  repository: "https://github.com/google-research/paper-orchestra"
---

# PaperOrchestra: Multi-Agent AI Research Paper Writing

Based on Google Cloud AI Research's PaperOrchestra framework (`google-research/paper-orchestra`), this skill decouples research execution from academic writing. It transforms unstructured, raw pre-writing materials—sparse idea notes, experimental logs, raw metric outputs, and code repositories—into submission-ready LaTeX manuscripts formatted to conference specifications (e.g., CVPR, ICLR, NeurIPS).

---

## 1. Core Architecture & Operating Principles

### A. Decoupled Writing Pipeline
Prior autonomous research systems tightly couple experiment execution with manuscript drafting. PaperOrchestra isolates the manuscript authoring process:
- Takes human-provided or agent-generated raw materials as read-only inputs.
- Parses numerical metrics directly from execution logs to prevent metric hallucination in tables.
- Applies a cooperative sequential multi-agent pipeline of specialized roles.

### B. Evidentiary Class Invariant
All text, data points, and citations in the generated manuscript must belong to one of three verified classes:
1. `EXPERIMENTAL EVIDENCE`: Directly parsed from execution logs, benchmark evaluation files, or table artifacts.
2. `GROUNDED CITATION`: Retrieved from verified APIs (arXiv, Semantic Scholar, CrossRef, PubMed) with confirmed DOIs or arXiv identifiers.
3. `METHODOLOGICAL PROSE`: Technical explanations grounded strictly in the declared problem formulation, algorithms, and architectures.

---

## 2. The 5-Agent Collaborative Pipeline

```
[Raw Pre-Writing Materials]
        │
        ▼
1. Outline Agent ─────────────► JSON Section Map + Conference Format (CVPR/ICLR)
        │
        ▼
2. Visual Asset Agent ────────► Matplotlib/Seaborn Plots + Architecture Diagrams
        │
        ▼
3. Literature Review Agent ───► API-Grounded Citation Retrieval (>=90% retention)
        │
        ▼
4. Section Writing Agent ─────► Full LaTeX Draft (Direct log metrics in tables)
        │
        ▼
5. Content Refinement Agent ──► AgentReview Peer Evaluation Loop (Score-guarded)
        │
        ▼
[Publication-Ready LaTeX Manuscript]
```

### Agent 1: Outline Agent
- **Responsibility**: Ingests unstructured notes, abstracts, and experimental conclusions.
- **Output**: A structured JSON outline detailing each section, subsection, target page budget, and narrative progression.
- **Layout Selection**: Enforces conference layout constraints (e.g., CVPR double-column 8-page format vs. ICLR single-column 9-page format).

### Agent 2: Visual Asset & Plotting Agent
- **Responsibility**: Inspects raw numerical outputs, evaluation curves, and architectural schemas.
- **Output**: Standalone Python plotting scripts (matplotlib, seaborn) generating publication-grade vector graphics (PDF/EPS) and TikZ/Mermaid architecture diagrams.
- **Formatting Standards**: Consistent font scaling matching document typography, distinct color palettes accessible for colorblind readers, and explicit error bounds / standard deviation bands.

### Agent 3: Literature Review Agent
- **Responsibility**: Formulates targeted literature queries based on the paper's core contributions and baseline competitors.
- **Output**: BibTeX citation database with verified keys, title, authors, year, and venue.
- **Retention Constraint**: Enforces a strict citation retention check (at least 90% of gathered relevant literature must be actively contextualized and cited in the Related Work or Introduction).

### Agent 4: Section Writing Agent
- **Responsibility**: Writes complete, cohesive technical sections in valid LaTeX:
  - Abstract & Introduction: Context, motivation, explicit research gap, and itemized contribution list.
  - Related Work: Thematic clustering of prior work with explicit contrasts.
  - Methodology: Mathematical problem formulation, equations with consistent notation, and algorithmic pseudocode.
  - Experiments: Benchmark setup, datasets, baseline configurations, quantitative ablation studies, and qualitative results.
  - Discussion & Conclusion: Practical implications, limitations, and future research vectors.
- **Zero Hallucination Constraint**: Every number in LaTeX tables (`\begin{tabular}`) must match the raw experimental logs verbatim.

### Agent 5: Content Refinement Agent (AgentReview)
- **Responsibility**: Simulates a rigorous peer-review panel grading the draft across standard conference criteria:
  - Clarity & Organization (1-10)
  - Methodological Rigor & Technical Soundness (1-10)
  - Empirical Completeness & Baseline Comparison (1-10)
  - Citation Depth & Academic Integrity (1-10)
- **Regression-Guarded Acceptance**: Iterative revisions are accepted only if the overall evaluation score improves or ties without negative drops across sub-axes; otherwise, the revision reverts to the previous state.

---

## 3. PaperWritingBench Evaluation Methodology

When evaluating manuscript drafts, apply the PaperWritingBench evaluation rubric derived from top-tier conference standards:

| Evaluation Axis | Target Standard | Failure Condition |
| :--- | :--- | :--- |
| **Literature Depth** | Comprehensive coverage of recent (last 2-3 years) and foundational prior art | Missing primary baseline models or fabricated reference entries |
| **Data Grounding** | Verifiable correspondence between log values and manuscript tables | Mismatched percentages, invented sample counts, or unsourced baselines |
| **Visual Cohesion** | Plots include clear axis legends, units, and referenced figure callouts | Floating unreferenced figures or rasterized low-resolution graphics |
| **LaTeX Integrity** | Clean compilation with zero unresolved cross-references (`??`) | Syntax errors, undefined packages, or overlapping text columns |

---

## 4. Operational Workflow for Agents

When requested to draft an academic paper using `paper-orchestra`:

1. **Step 1: Collect Pre-Writing Assets**:
   - Inspect user notes, code files, and benchmark log outputs.
   - Confirm target venue (e.g., CVPR, ICLR, NeurIPS, IEEE, ACM) to select the matching LaTeX template.

2. **Step 2: Generate Visual Assets & Tables**:
   - Extract raw metrics and write plotting scripts to generate clean PDF plots.
   - Format LaTeX tables using standard packages (`booktabs`, `array`).

3. **Step 3: Construct Grounded Bibliography**:
   - Query verified scholarly sources for relevant literature.
   - Build a verified `references.bib` file with exact DOIs and arXiv IDs.

4. **Step 4: Draft Section Manuscripts**:
   - Synthesize LaTeX chapters with consistent mathematical notation.
   - Insert cross-references (`\cref`, `\autoref`) for sections, figures, and tables.

5. **Step 5: Run Simulated Peer Review**:
   - Audit the draft for clarity, technical rigor, and unsupported claims.
   - Apply targeted refinements while preserving verified empirical findings.
