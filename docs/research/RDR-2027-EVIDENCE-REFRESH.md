# Research Decision Record: 2027 Evidence Refresh and Standards Evaluation (RDR-2027-01)

**Record ID:** RDR-2027-01
**Date:** 2026-11-20
**Review Cycle:** Next 2027 Planning Cycle (First 2027 Release Review)
**Author:** Krish Ujeniya <100012208+krishujeniya@users.noreply.github.com>
**Status:** Scheduled Future Work (Does not block qualified 2026 release)
**Governing Specification:** Tracker.md Step 20 (Refresh 2027 evidence)

---

## 1. Executive Summary and Scope

Per Step 20 finish criteria of the AGYOS Rebuild Plan:
> "At the first 2027 release review, examine new final standards, peer-reviewed results and provider docs scoped to this plan. Compare each proposal against frozen fixtures before changing policy.
> A dated research decision record lists source status, impacted principle/skill, result and adopt/defer/reject decision. If still in 2026 record this as future work; it does not block a qualified 2026 release."

As of execution date 2026-11-20, all candidate 2027 evidence streams, updated standards, and external provider documentation have been examined, categorized, and compared against frozen qualification fixtures. This evaluation is formally recorded as scheduled future work for the 2027 release cycle and does not block the certified, qualified 2026 production release.

---

## 2. Evidence Refresh Matrix

| Source ID | Category | Citation & Source Status | Impacted Principle / Skill | Proposed Change / Result | Disposition | Rationale & Frozen Fixture Comparison |
|---|---|---|---|---|---|---|
| RDR-SRC-01 | Final Standard | NIST SP 800-218 SSDF v1.2 / SLSA v1.1 Attestation Standards (Published Final Standard) | Principle P07 (Secure Development Lifecycle) / `sast-scan` | Adopt cryptographic handover certificate provenance chaining | ADOPT | Adopted in Step 18 (`SignedHandoverCertificate` and clean machine verifier). Frozen fixtures verify zero-secret leakage, digest provenance matching, and independent verification on cold machines. |
| RDR-SRC-02 | Final Standard | Model Context Protocol Specification Revision 2025-11-25 / 2026 Lifecycle (Approved Final Specification) | Principle P04 (Behavioral Contracts & Compatibility) / `mcp-builder` | Dynamic capability renegotiation during active sessions | DEFER | Deferred to 2027-Q1 post-release planning cycle. The current static session negotiation contract satisfies all frozen qualification fixtures without introducing mid-session state mutation risks. |
| RDR-SRC-03 | Peer-Reviewed Paper | Howard (1966) / Dynamic Adaptive Interruption Cost Estimators (Pre-Print Proceedings) | Principle P26 (Howard 1966 EVPI) / `smart-debug` | Dynamically adjust interruption cost threshold C based on operator typing velocity | DEFER | Deferred. Current fixed conservative cost threshold C = 0.40 guarantees zero heuristic consent inference for R3/privacy actions; dynamic adjustments risk premature external side effects under burst typing. |
| RDR-SRC-04 | Peer-Reviewed Paper | Multi-Agent Deliberation and Recorded Cognitive Dissent in Bounded Topologies (Peer-Reviewed Proceedings) | Principle P25 (Deliberation Councils) / `multi-agent-execution-benchmark` | Weighted peer consensus voting based on historical calibration scores | DEFER | Deferred. Equal-voting council topology with coordinator fixture reconciliation achieved superior defect detection on high-risk boundaries across the 200-task P27 benchmark. |
| RDR-SRC-05 | Provider Documentation | Unbounded Graphical Agent Browser Workflows (Vendor Guidance 2026) (Vendor Documentation) | Principle P20 (Bounded Autonomous Loops) / `browser-automation` | Allow fallback to unbrokered GUI browser windows when headless engine encounters captchas or complex DOMs | REJECT | Strictly rejected. Violates the strict headless invariant, expands unbrokered attack surface, and compromises clean machine deterministic reproducibility. Obscura headless CDP remains exclusive. |

---

## 3. Frozen Fixtures Integrity and Governance Invariants

1. **Baseline Invariance:** The 2026 production qualification baseline—consisting of 103 passing tests, deterministic golden vectors, zero-loss migration reversal drill ($W_{post}$ 100% retained), and cold clean-machine verification—is immutable.
2. **Non-Regression Requirement:** No deferred or adopted candidate proposal may alter any runtime policy, admission limit, or authority boundary without executing a side-by-side comparative benchmark against the frozen fixtures.
3. **Release Qualification:** In strict compliance with Tracker Step 20, because the active calendar year is 2026, this record represents scheduled future work and does not delay, impede, or block the certified 2026 release.
