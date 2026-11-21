//! Hosted Fair Admission & Protected Control Capacity (Step 16).
//!
//! Complies with Step 16 finish criteria and Principles:
//! - P05 (Least Privilege & Complete Mediation)
//! - P15 (Tail Latency Amplification Bounds)
//! - P16 (Admission Control & Graceful Degradation)
//! - P20 (End-to-End Observability)
//! - P32 (Operator-Owned Budgets)

use domain::WorkspaceId;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, VecDeque};

/// Traffic class for hosted admission scheduling.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum HostedTrafficClass {
    /// Protected control operations: status queries and task cancellations (guaranteed >= 10% capacity).
    StatusOrCancel,
    /// Standard read-only route queries.
    RouteRead,
    /// Asynchronous durable submit tasks.
    DurableJob,
}

/// Queued job awaiting dispatch to a worker.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QueuedJob {
    pub job_id: String,
    pub workspace_id: WorkspaceId,
    pub traffic_class: HostedTrafficClass,
    pub payload_bytes: usize,
    pub enqueued_epoch_s: u64,
}

/// Admission decision outcome.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum AdmissionVerdict {
    Admitted { queue_position: usize },
    RejectedQueueFull { retry_after_s: u64 },
    RejectedTenantQuotaExceeded { workspace_id: String, retry_after_s: u64 },
    RejectedExpiredDeadline,
}

/// Fair Queue and Admission Controller for Hosted Heavy Production.
pub struct QueueAdmissionController {
    max_queue_entries: usize,
    max_queue_bytes: usize,
    max_queue_age_s: u64,
    protected_control_headroom_percent: u32,
    queues: BTreeMap<String, VecDeque<QueuedJob>>,
    tenant_order: VecDeque<String>,
    protected_queue: VecDeque<QueuedJob>,
    total_bytes: usize,
    total_entries: usize,
}

impl QueueAdmissionController {
    pub fn new() -> Self {
        Self {
            max_queue_entries: 100, // Hosted cap: 100 entries
            max_queue_bytes: 25 * 1024 * 1024, // 25 MiB total
            max_queue_age_s: 10, // 10s oldest-start deadline
            protected_control_headroom_percent: 10, // Guaranteed 10% control headroom
            queues: BTreeMap::new(),
            tenant_order: VecDeque::new(),
            protected_queue: VecDeque::new(),
            total_bytes: 0,
            total_entries: 0,
        }
    }

    pub fn total_entries(&self) -> usize {
        self.total_entries
    }

    pub fn total_bytes(&self) -> usize {
        self.total_bytes
    }

    /// Evaluates admission for a new job with fair tenant quota and protected control headroom.
    pub fn submit_job(&mut self, job: QueuedJob, current_epoch_s: u64) -> AdmissionVerdict {
        // Prune expired jobs older than 10s deadline
        self.prune_expired_jobs(current_epoch_s);

        // Protected status or cancel operations bypass standard queue limits up to guaranteed 10% headroom
        if job.traffic_class == HostedTrafficClass::StatusOrCancel {
            let protected_cap = (self.max_queue_entries * self.protected_control_headroom_percent as usize) / 100;
            if self.protected_queue.len() < protected_cap.max(10) {
                let pos = self.protected_queue.len();
                self.total_bytes += job.payload_bytes;
                self.protected_queue.push_back(job);
                self.total_entries += 1;
                return AdmissionVerdict::Admitted { queue_position: pos };
            }
        }

        // Global capacity checks (100 entries or 25 MiB)
        if self.total_entries >= self.max_queue_entries {
            return AdmissionVerdict::RejectedQueueFull { retry_after_s: 2 };
        }
        if self.total_bytes + job.payload_bytes > self.max_queue_bytes {
            return AdmissionVerdict::RejectedQueueFull { retry_after_s: 5 };
        }

        // Hot-tenant isolation: single tenant cannot exceed 40% of standard queue entries under contention
        let tenant_key = job.workspace_id.as_str().to_string();
        let max_per_tenant = (self.max_queue_entries * 40) / 100;
        if let Some(q) = self.queues.get(&tenant_key) {
            if q.len() >= max_per_tenant {
                return AdmissionVerdict::RejectedTenantQuotaExceeded {
                    workspace_id: tenant_key,
                    retry_after_s: 3,
                };
            }
        }

        if !self.tenant_order.contains(&tenant_key) {
            self.tenant_order.push_back(tenant_key.clone());
        }

        let tenant_queue = self.queues.entry(tenant_key).or_default();
        self.total_bytes += job.payload_bytes;
        self.total_entries += 1;
        let pos = tenant_queue.len();
        tenant_queue.push_back(job);

        AdmissionVerdict::Admitted { queue_position: pos }
    }

    /// Dispatches next job following round-robin fair dispatch across workspaces to prevent starvation.
    pub fn dispatch_next(&mut self) -> Option<QueuedJob> {
        // 1. High priority: Protected status/cancel jobs always dispatch first
        if let Some(job) = self.protected_queue.pop_front() {
            self.total_bytes = self.total_bytes.saturating_sub(job.payload_bytes);
            self.total_entries = self.total_entries.saturating_sub(1);
            return Some(job);
        }

        // 2. Round-robin fair dispatch across tenant queues
        let mut attempts = self.tenant_order.len();
        while attempts > 0 {
            attempts -= 1;
            let ws_str = match self.tenant_order.pop_front() {
                Some(ws) => ws,
                None => break,
            };

            let mut should_requeue_tenant = false;
            let mut selected_job = None;

            if let Some(q) = self.queues.get_mut(&ws_str) {
                if let Some(job) = q.pop_front() {
                    self.total_bytes = self.total_bytes.saturating_sub(job.payload_bytes);
                    self.total_entries = self.total_entries.saturating_sub(1);
                    selected_job = Some(job);
                }
                if !q.is_empty() {
                    should_requeue_tenant = true;
                }
            }

            if should_requeue_tenant {
                self.tenant_order.push_back(ws_str);
            } else {
                self.queues.remove(&ws_str);
            }

            if selected_job.is_some() {
                return selected_job;
            }
        }

        None
    }

    fn prune_expired_jobs(&mut self, current_epoch_s: u64) {
        let deadline = self.max_queue_age_s;

        self.protected_queue.retain(|job| {
            current_epoch_s.saturating_sub(job.enqueued_epoch_s) <= deadline
        });

        for q in self.queues.values_mut() {
            q.retain(|job| {
                current_epoch_s.saturating_sub(job.enqueued_epoch_s) <= deadline
            });
        }

        self.queues.retain(|_, q| !q.is_empty());
        self.tenant_order.retain(|ws| self.queues.contains_key(ws));

        self.total_entries = self.protected_queue.len()
            + self.queues.values().map(|q| q.len()).sum::<usize>();
        let standard_bytes: usize = self.queues.values().flat_map(|q| q.iter().map(|j| j.payload_bytes)).sum();
        let protected_bytes: usize = self.protected_queue.iter().map(|j| j.payload_bytes).sum();
        self.total_bytes = standard_bytes + protected_bytes;
    }
}
