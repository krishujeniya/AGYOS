//! Effect Provider Contract.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum EffectOutcome {
    Confirmed,
    ExplicitUnknown,
    Failed,
}

pub trait EffectProvider {
    fn dispatch(&mut self, effect_id: &str, payload: &str) -> EffectOutcome;
    fn compensate(&mut self, effect_id: &str) -> bool;
}
