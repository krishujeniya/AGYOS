//! Saga Coordinator for Transactional Compensation.

use store::{OutboxStatus, StoreError, TransactionalStore};
use crate::provider::EffectProvider;

pub struct SagaCoordinator;

impl SagaCoordinator {
    /// Rollback and compensate confirmed effects upon cancellation.
    pub fn compensate_effect(
        store: &mut TransactionalStore,
        provider: &mut dyn EffectProvider,
        effect_id: &str,
    ) -> Result<bool, StoreError> {
        let record = store.outbox().iter().find(|r| r.effect_id == effect_id);
        if let Some(r) = record {
            if r.status == OutboxStatus::Confirmed || r.status == OutboxStatus::ExplicitUnknown {
                let success = provider.compensate(effect_id);
                if success {
                    store.update_outbox_status(effect_id, OutboxStatus::Compensated)?;
                    return Ok(true);
                }
            }
        }
        Ok(false)
    }
}
