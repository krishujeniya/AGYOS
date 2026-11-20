//! TOON Error Types and Invariant Diagnostics.
//!
//! Complies with Principle P13 (Bounded Parsing and Stable Error Diagnostics).

use std::fmt;

/// Maximum payload size allowed for inline parsing: 256 KiB.
pub const MAX_PAYLOAD_BYTES: usize = 262_144;

/// Maximum allowed nesting depth for hierarchical structures.
pub const MAX_NESTING_DEPTH: usize = 4;

/// Maximum length for a single string scalar: 65,536 characters.
pub const MAX_STRING_LENGTH: usize = 65_536;

/// Maximum number of array elements in a single collection.
pub const MAX_ARRAY_ELEMENTS: usize = 1_024;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ToonError {
    SizeCeilingExceeded { limit: usize, actual: usize },
    MaxDepthExceeded { limit: usize, actual: usize },
    StringLengthExceeded { limit: usize, actual: usize },
    ArrayElementsExceeded { limit: usize, actual: usize },
    InvalidEscapeSequence(String),
    LoneSurrogate(String),
    DuplicateKey(String),
    PathTraversalDetected(String),
    NumericOverflow(String),
    UnexpectedEof,
    SyntaxError(String),
}

impl fmt::Display for ToonError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ToonError::SizeCeilingExceeded { limit, actual } => {
                write!(f, "Payload size ceiling exceeded: limit {} bytes, actual {} bytes", limit, actual)
            }
            ToonError::MaxDepthExceeded { limit, actual } => {
                write!(f, "Maximum nesting depth exceeded: limit {}, actual {}", limit, actual)
            }
            ToonError::StringLengthExceeded { limit, actual } => {
                write!(f, "String length ceiling exceeded: limit {}, actual {}", limit, actual)
            }
            ToonError::ArrayElementsExceeded { limit, actual } => {
                write!(f, "Array element count ceiling exceeded: limit {}, actual {}", limit, actual)
            }
            ToonError::InvalidEscapeSequence(msg) => write!(f, "Invalid escape sequence: {}", msg),
            ToonError::LoneSurrogate(seq) => {
                write!(
                    f,
                    "Invalid escape sequence: {} is a lone surrogate. Supplementary code points MUST appear as literal UTF-8",
                    seq
                )
            }
            ToonError::DuplicateKey(k) => write!(f, "Duplicate key in TOON document: {}", k),
            ToonError::PathTraversalDetected(p) => write!(f, "Path traversal sequence detected in target reference: {}", p),
            ToonError::NumericOverflow(s) => write!(f, "Numeric value outside valid range: {}", s),
            ToonError::UnexpectedEof => write!(f, "Unexpected end of input while parsing TOON document"),
            ToonError::SyntaxError(msg) => write!(f, "TOON syntax error: {}", msg),
        }
    }
}

impl std::error::Error for ToonError {}
