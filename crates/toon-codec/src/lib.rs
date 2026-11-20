//! TOON (Token-Oriented Object Notation) Codec Library.
//!
//! Provides high-performance, bounded serialization and deserialization between
//! JSON/Rust data structures and token-efficient TOON format for LLM prompting,
//! configuration, and persistent memory.

pub mod decode;
pub mod encode;
pub mod error;
pub mod legacy;
pub mod model;

pub use decode::{decode_document, decode_records, parse_scalar, split_csv_line};
pub use encode::{encode, encode_json_array, encode_records, format_scalar};
pub use error::ToonError;
pub use legacy::{unpack_legacy_envelope, LegacyEnvelope};
pub use model::ToonValue;

/// Minify TOON text by stripping empty lines and trailing whitespace.
pub fn minify_toon(input: &str) -> String {
    let mut out = String::with_capacity(input.len());
    for line in input.lines() {
        let trimmed = line.trim_end();
        if !trimmed.trim().is_empty() {
            out.push_str(trimmed);
            out.push('\n');
        }
    }
    if out.ends_with('\n') {
        out.pop();
    }
    out
}
