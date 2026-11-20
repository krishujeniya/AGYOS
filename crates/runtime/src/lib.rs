//! AGYOS Autonomous Runtime, Progressive Routing, and Council Deliberation Engine.
//!
//! Complies with Step 12: Implement routing and councils, and Principles:
//! - P15 (Tail Amplification & Latency Bounds)
//! - P16 (Admission Control & Graceful Degradation)
//! - P22 (Measured Context Retrieval - Liu et al., TACL 2024)
//! - P24 (Calibrated Reliance)
//! - P25 (Selective Cognitive Forcing - Buçinca et al., 2021)
//! - P26 (Universal Accessibility - Single Question at a Time)
//! - P27 (Empirically Justified Councils - Vaccaro et al., 2024)
//! - P28 (Decision Value Under Uncertainty - Howard, 1966)
//! - P29 (Progressive Disclosure)
//! - P30 (Authority and Reversibility as Human Choices)
//! - P32 (Operator-Owned Budgets & Verification Reserves)

pub mod benchmark;
pub mod budget;
pub mod council;
pub mod evpi;
pub mod model_policy;
pub mod routing;

pub use benchmark::{ArmMetricResult, P27Arm, P27BenchmarkRunner, PairedComparisonResult};
pub use budget::{ContextBudget, TokenSavingsEvaluator};
pub use council::{BlindReviewCriterion, CouncilDeliberationOutcome, CouncilEngine};
pub use evpi::{ActionDecision, EvpiEngine, EvpiParameters};
pub use model_policy::{AdmissionController, ExecutionMode, ModelPolicyRouter, ModelTier};
pub use routing::{CandidateSkillMatch, ProgressiveRetriever, RetrievalResult};
