---
name: agyos-academic-research
description: Systematic academic research and literature analysis. Identifies research gaps, evaluates empirical methodologies, synthesizes papers, manages citations, and builds defensible problem statements.
---

# AGYOS Academic Research & Literature Review

A disciplined methodology for conducting systematic academic literature reviews, identifying empirical research gaps, and structuring defensible research questions.

## 1. 4-Tier Topic Evaluation Framework

When evaluating candidate research topics or papers, categorize each area into one of four distinct tiers:

- Tier A (Completely Unexplored): Novel phenomenon or newly introduced architecture with zero published empirical baselines. Requires exploratory qualitative or benchmark studies.
- Tier B (Under-Researched): Emerging field with early conceptual papers but lacking rigorous empirical validation, diverse datasets, or real-world deployment data.
- Tier C (Active with Identifiable Gaps): Significant existing literature, but critical gaps remain (e.g., methodological limitations, unexamined edge cases, conflicting replication findings).
- Tier D (Highly Saturated): Extensively studied topics with established consensus. Exclude unless a novel, orthogonal evaluation angle is demonstrated.

## 2. Research Gap Identification

Isolate clear gaps before proposing research hypotheses:

1. Methodological Gaps: Previous studies relied solely on simulation or synthetic benchmarks; real-world deployment or adversarial testing is missing.
2. Contradictory Findings: Conflicting results between foundational studies indicating hidden confounders or differing experimental conditions.
3. Outdated Assumptions: Prior models assumed architectural constraints (e.g., fixed context windows, single-agent loops) that no longer hold.
4. Population / Domain Gaps: Algorithms verified in one domain (e.g., web NLP) have unmeasured transfer degradation in another (e.g., clinical records, code generation).

## 3. Systematic Literature Search & Synthesis

1. Query Structuring:
   - Combine MeSH terms, Boolean operators, and specific keywords across arXiv, Semantic Scholar, and PubMed.
   - Example: `("autonomous agents" OR "multi-agent") AND ("verification" OR "gate-check") AND ("hallucination" OR "grounding")`
2. Paper Synthesis Matrix:
   - For every reviewed paper, record: Title, Authors, Year, Core Claim, Methodology, Dataset/Sample Size, Key Findings, Limitations, and Threat to Validity.

## 4. Citation Integrity & Fact Grounding

- Verified DOIs: Always verify that cited papers exist with valid DOIs or arXiv identifiers. Never fabricate citations or author attributions.
- Primary Source Tracing: Trace claims to their original experimental paper rather than citing secondary review summaries.
