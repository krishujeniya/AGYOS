//! Fixed-Point Currency and Atomic Budget Ledger.
//!
//! Complies with Principle P32 (Operator-Owned Budgets & Verification Reserves).
//!
//! Guarantees:
//! - Exact arithmetic with zero floating point drift (1 USD = 1,000,000 micro-dollars).
//! - A thousand USD 0.001 charges sum to USD 1.000000 exactly.
//! - 20% recovery reserve fund is strictly untouchable by standard task reservations.

use serde::{Deserialize, Serialize};
use std::ops::{Add, Sub};
use crate::error::DomainError;

/// Fixed-point money represented in micro-units ($0.000001 precision).
/// 1 USD = 1_000_000 micro-dollars.
/// 0.001 USD = 1_000 micro-dollars.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize, Default)]
pub struct FixedMoney(i64);

impl FixedMoney {
    pub const ZERO: FixedMoney = FixedMoney(0);
    pub const ONE_DOLLAR: FixedMoney = FixedMoney(1_000_000);
    pub const ONE_MILLI_DOLLAR: FixedMoney = FixedMoney(1_000); // $0.001

    pub fn from_micros(micros: i64) -> Self {
        Self(micros)
    }

    pub fn from_cents(cents: i64) -> Self {
        Self(cents * 10_000)
    }

    pub fn from_dollars(dollars: i64) -> Self {
        Self(dollars * 1_000_000)
    }

    pub fn as_micros(&self) -> i64 {
        self.0
    }

    pub fn as_f64(&self) -> f64 {
        self.0 as f64 / 1_000_000.0
    }
}

impl Add for FixedMoney {
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        Self(self.0 + rhs.0)
    }
}

impl Sub for FixedMoney {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self::Output {
        Self(self.0 - rhs.0)
    }
}

/// Atomic budget ledger tracking funds, active reservations, and mandatory 20% recovery reserve.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BudgetLedger {
    pub total_funds: FixedMoney,
    pub reserved_funds: FixedMoney,
    pub spent_funds: FixedMoney,
    pub recovery_reserve_basis_pts: u32, // Default 2,000 = 20.00%
}

impl BudgetLedger {
    pub fn new(total_funds: FixedMoney) -> Self {
        Self {
            total_funds,
            reserved_funds: FixedMoney::ZERO,
            spent_funds: FixedMoney::ZERO,
            recovery_reserve_basis_pts: 2_000, // 20%
        }
    }

    /// Calculate the untouchable recovery reserve (20% of total funds).
    pub fn recovery_reserve(&self) -> FixedMoney {
        let micros = (self.total_funds.as_micros() * self.recovery_reserve_basis_pts as i64) / 10_000;
        FixedMoney::from_micros(micros)
    }

    /// Calculate currently unreserved and unspent funds available for new allocation.
    pub fn available_spendable(&self) -> FixedMoney {
        let reserved_and_spent = self.reserved_funds + self.spent_funds + self.recovery_reserve();
        if self.total_funds >= reserved_and_spent {
            self.total_funds - reserved_and_spent
        } else {
            FixedMoney::ZERO
        }
    }

    /// Attempt to reserve funds for task execution.
    /// Fails immediately if the reservation would consume the 20% recovery reserve!
    pub fn reserve(&mut self, amount: FixedMoney) -> Result<(), DomainError> {
        let spendable = self.available_spendable();
        if amount > spendable {
            return Err(DomainError::RecoveryReserveViolation {
                requested: amount,
                available: spendable,
                recovery_reserve: self.recovery_reserve(),
            });
        }
        self.reserved_funds = self.reserved_funds + amount;
        Ok(())
    }

    /// Release reserved funds.
    pub fn release_reservation(&mut self, amount: FixedMoney) {
        if self.reserved_funds >= amount {
            self.reserved_funds = self.reserved_funds - amount;
        } else {
            self.reserved_funds = FixedMoney::ZERO;
        }
    }

    /// Settle spend against an existing reservation.
    pub fn commit_spend(&mut self, amount: FixedMoney) -> Result<(), DomainError> {
        if amount > self.reserved_funds {
            return Err(DomainError::BudgetExceeded {
                requested: amount,
                available: self.reserved_funds,
            });
        }
        self.reserved_funds = self.reserved_funds - amount;
        self.spent_funds = self.spent_funds + amount;
        Ok(())
    }
}
