//! TOON (Token-Oriented Object Notation) Codec Library.
//!
//! Provides ultra-fast serialization and deserialization between JSON/Rust data structures
//! and token-efficient TOON format for LLM prompting and configuration.

pub mod decode;
pub mod encode;

pub use decode::decode_records;
pub use encode::{encode_json_array, encode_records};

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

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn test_roundtrip() {
        let sample = json!([
            {"name": "skill-a", "tier": 1, "active": true},
            {"name": "skill-b", "tier": 2, "active": false}
        ]);
        let encoded = encode_json_array(sample.as_array().unwrap(), "skills").unwrap();
        assert!(encoded.starts_with("skills[2]:"));
        let decoded = decode_records(&encoded).unwrap();
        assert_eq!(decoded.len(), 2);
        assert_eq!(decoded[0].get("name").unwrap(), "skill-a");
        assert_eq!(decoded[0].get("tier").unwrap(), 1);
        assert_eq!(decoded[0].get("active").unwrap(), true);
    }
}
