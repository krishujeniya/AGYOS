//! AGYOS Reconciled Skill and Role Catalog Engine.
//!
//! Complies with Step 10 acceptance criteria and Principles P03, P06, P09, P10, P12, P29.

pub mod index;
pub mod ledger;
pub mod reconcile;
pub mod role;
pub mod skill;

pub use index::ReconciledCatalogIndex;
pub use ledger::{MigrationLedger, SourcePathRecord};
pub use reconcile::{CatalogReconciler, ReconciledConflict};
pub use role::{Department, GoverningPod, RoleDefinition, RoleRegistry, SeniorityTier};
pub use skill::{SkillDefinition, SkillDisposition};
