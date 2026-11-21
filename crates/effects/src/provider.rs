//! Effect Provider Contract and Crash Simulation Fixture.

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

/// Mock failure modes for effect qualification test fixtures.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MockFailureMode {
    NormalSuccess,
    FailBeforeDispatch,
    CrashAfterDispatchBeforeReceipt,
}

/// Mock fixture provider for Step 13 effect broker qualification testing.
pub struct MockFixtureProvider {
    pub mode: MockFailureMode,
    pub dispatch_count: usize,
    pub compensate_count: usize,
}

impl MockFixtureProvider {
    pub fn new(mode: MockFailureMode) -> Self {
        Self {
            mode,
            dispatch_count: 0,
            compensate_count: 0,
        }
    }
}

impl EffectProvider for MockFixtureProvider {
    fn dispatch(&mut self, _effect_id: &str, _payload: &str) -> EffectOutcome {
        self.dispatch_count += 1;
        match self.mode {
            MockFailureMode::NormalSuccess => EffectOutcome::Confirmed,
            MockFailureMode::FailBeforeDispatch => EffectOutcome::Failed,
            MockFailureMode::CrashAfterDispatchBeforeReceipt => EffectOutcome::ExplicitUnknown,
        }
    }

    fn compensate(&mut self, _effect_id: &str) -> bool {
        self.compensate_count += 1;
        true
    }
}
