//! Store Error Types and Diagnostics.

use std::fmt;
use domain::WorkspaceId;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum StoreError {
    WorkspaceNotFound(WorkspaceId),
    StaleFenceToken { current_fence: u64, submitted_fence: u64 },
    DuplicateOperationKey(String),
    IdempotencyConflict { operation_key: String, expected_payload_hash: String, actual_payload_hash: String },
    CrossWorkspaceAccess { expected: String, actual: String },
    CorruptedState(String),
    IoError(String),
    SerializationError(String),
}

impl fmt::Display for StoreError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            StoreError::WorkspaceNotFound(ws) => write!(f, "Workspace not found or deleted: {}", ws),
            StoreError::StaleFenceToken { current_fence, submitted_fence } => {
                write!(f, "Stale fence token: current epoch is {}, submitted epoch was {}", current_fence, submitted_fence)
            }
            StoreError::DuplicateOperationKey(k) => write!(f, "Duplicate operation key: {}", k),
            StoreError::IdempotencyConflict { operation_key, expected_payload_hash, actual_payload_hash } => {
                write!(f, "Idempotency conflict for key '{}': expected payload hash '{}', got '{}'", operation_key, expected_payload_hash, actual_payload_hash)
            }
            StoreError::CrossWorkspaceAccess { expected, actual } => {
                write!(f, "Cross-workspace access violation: expected containment in '{}', actual was '{}'", expected, actual)
            }
            StoreError::CorruptedState(msg) => write!(f, "Corrupted store state: {}", msg),
            StoreError::IoError(msg) => write!(f, "Store I/O error: {}", msg),
            StoreError::SerializationError(msg) => write!(f, "Serialization error: {}", msg),
        }
    }
}

impl std::error::Error for StoreError {}
