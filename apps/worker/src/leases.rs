//! Worker Leases, Concurrency Bounds & Split-Brain Fencing (Step 16).
//!
//! Complies with Step 16 finish criteria and Principles:
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas - Fenced Leases)
//! - P11 (Idempotent Semantics)

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use store::FenceToken;

/// Unique worker instance identifier in the 6-worker pool.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct WorkerId(pub String);

/// Active task lease assigned to a worker.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkerLease {
    pub task_id: String,
    pub worker_id: WorkerId,
    pub fence_token: FenceToken,
    pub granted_epoch_s: u64,
    pub expires_epoch_s: u64,
}

/// Worker Pool and Fenced Lease Manager for Hosted Heavy Production.
pub struct WorkerPoolLeaseManager {
    worker_count: usize,
    slots_per_worker: usize,
    total_capacity: usize,
    lease_ttl_s: u64,
    active_leases: BTreeMap<String, WorkerLease>,
    worker_slot_usage: BTreeMap<WorkerId, usize>,
    current_fence_sequence: u64,
}

impl WorkerPoolLeaseManager {
    pub fn new() -> Self {
        let workers = 6;
        let slots = 72; // 6 workers * 72 slots = 432 concurrent slots
        let mut usage = BTreeMap::new();
        for i in 1..=workers {
            usage.insert(WorkerId(format!("worker-node-{:02}", i)), 0);
        }

        Self {
            worker_count: workers,
            slots_per_worker: slots,
            total_capacity: workers * slots,
            lease_ttl_s: 15, // 15-second lease heartbeat TTL
            active_leases: BTreeMap::new(),
            worker_slot_usage: usage,
            current_fence_sequence: 1,
        }
    }

    pub fn total_capacity(&self) -> usize {
        self.total_capacity
    }

    pub fn active_lease_count(&self) -> usize {
        self.active_leases.len()
    }

    /// Acquires a new lease for a task on an available worker.
    pub fn acquire_lease(
        &mut self,
        task_id: &str,
        current_epoch_s: u64,
    ) -> Result<WorkerLease, String> {
        // Prune expired leases first
        self.reclaim_expired_leases(current_epoch_s);

        // Find worker with least load
        let available_worker = self
            .worker_slot_usage
            .iter()
            .filter(|(_, &used)| used < self.slots_per_worker)
            .min_by_key(|(_, &used)| used)
            .map(|(w, _)| w.clone());

        let worker_id = match available_worker {
            Some(w) => w,
            None => return Err("All 432 worker call slots are saturated".to_string()),
        };

        self.current_fence_sequence += 1;
        let fence = FenceToken::new(self.current_fence_sequence);

        let lease = WorkerLease {
            task_id: task_id.to_string(),
            worker_id: worker_id.clone(),
            fence_token: fence,
            granted_epoch_s: current_epoch_s,
            expires_epoch_s: current_epoch_s + self.lease_ttl_s,
        };

        *self.worker_slot_usage.get_mut(&worker_id).unwrap() += 1;
        self.active_leases.insert(task_id.to_string(), lease.clone());

        Ok(lease)
    }

    /// Renews lease heartbeat, rejecting stale fences.
    pub fn renew_heartbeat(
        &mut self,
        task_id: &str,
        caller_fence: FenceToken,
        current_epoch_s: u64,
    ) -> Result<WorkerLease, String> {
        let lease = self
            .active_leases
            .get_mut(task_id)
            .ok_or_else(|| format!("No active lease for task {}", task_id))?;

        if caller_fence.epoch() < lease.fence_token.epoch() {
            return Err(format!(
                "Stale fence token {} rejected; active fence is {}",
                caller_fence.epoch(),
                lease.fence_token.epoch()
            ));
        }

        lease.expires_epoch_s = current_epoch_s + self.lease_ttl_s;
        Ok(lease.clone())
    }

    /// Releases a completed task lease.
    pub fn release_lease(&mut self, task_id: &str) -> bool {
        if let Some(lease) = self.active_leases.remove(task_id) {
            if let Some(used) = self.worker_slot_usage.get_mut(&lease.worker_id) {
                *used = used.saturating_sub(1);
            }
            true
        } else {
            false
        }
    }

    /// Reclaims expired leases when a worker node stalls or crashes.
    pub fn reclaim_expired_leases(&mut self, current_epoch_s: u64) -> Vec<String> {
        let mut expired_tasks = Vec::new();

        for (task_id, lease) in &self.active_leases {
            if current_epoch_s > lease.expires_epoch_s {
                expired_tasks.push(task_id.clone());
            }
        }

        for task_id in &expired_tasks {
            self.release_lease(task_id);
        }

        expired_tasks
    }
}
