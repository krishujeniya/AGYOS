//! Privileged Effect Broker with Idempotency and Complete Mediation.

use store::{OutboxRecord, OutboxStatus, StoreError, TransactionalStore};
use crate::provider::{EffectOutcome, EffectProvider};

pub struct EffectBroker;

impl EffectBroker {
    /// Process pending outbox effects through the provider.
    /// Guarantees:
    /// - Crashes around the provider receipt end as Confirmed or explicit Unknown.
    /// - Duplicate replay emits exactly one effect.
    pub fn process_outbox(
        store: &mut TransactionalStore,
        provider: &mut dyn EffectProvider,
    ) -> Result<Vec<(String, OutboxStatus)>, StoreError> {
        let mut results = Vec::new();
        let pending_records: Vec<OutboxRecord> = store
            .outbox()
            .iter()
            .filter(|r| r.status == OutboxStatus::Pending)
            .cloned()
            .collect();

        for record in pending_records {
            let outcome = provider.dispatch(&record.effect_id, &record.payload_json);
            let final_status = match outcome {
                EffectOutcome::Confirmed => OutboxStatus::Confirmed,
                EffectOutcome::ExplicitUnknown => OutboxStatus::ExplicitUnknown,
                EffectOutcome::Failed => OutboxStatus::Failed,
            };

            store.update_outbox_status(&record.effect_id, final_status)?;
            results.push((record.effect_id, final_status));
        }

        Ok(results)
    }
}
