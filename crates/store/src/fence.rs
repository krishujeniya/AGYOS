//! Fencing Token to Prevent Stale Split-Brain Writers.
//!
//! Complies with Principle P10 (Leases with Fencing).

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize, Default)]
pub struct FenceToken(u64);

impl FenceToken {
    pub fn new(epoch: u64) -> Self {
        Self(epoch)
    }

    pub fn epoch(&self) -> u64 {
        self.0
    }

    pub fn next(&self) -> Self {
        Self(self.0 + 1)
    }
}
