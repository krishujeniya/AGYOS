//! Upstream TOON Conformance Test Suite.
//! Reference Revision: 009074d934289553a61763d70c50ee5160e60110
//! Principles: P04 (Behavioral Contracts), P13 (Bounded Parsing)

use toon_codec::{
    decode_document, encode, unpack_legacy_envelope, ToonError, ToonValue,
};

#[test]
fn test_conformance_literal_utf8() {
    let input = "greeting: \"Hello World\"\nemoji: \"🚀 Antigravity 🦀\"\n";
    let decoded = decode_document(input).expect("Valid UTF-8 with emojis should succeed");
    if let ToonValue::Map(entries) = decoded {
        assert_eq!(entries.len(), 2);
        assert_eq!(entries[1].1, ToonValue::String("🚀 Antigravity 🦀".to_string()));
    } else {
        panic!("Expected map");
    }
}

#[test]
fn test_conformance_reject_lone_surrogates() {
    // Lone surrogate \ud83d must be rejected with stable error
    let input = "bad_surrogate: \"invalid \\ud83d sequence\"\n";
    let err = decode_document(input).expect_err("Lone surrogate should fail");
    match err {
        ToonError::LoneSurrogate(seq) => {
            assert!(seq.contains("d83d"), "Expected surrogate seq in error: {}", seq);
        }
        other => panic!("Expected LoneSurrogate error, got: {:?}", other),
    }
}

#[test]
fn test_conformance_reject_duplicate_keys() {
    let input = "task_id: \"task_01\"\ntask_id: \"task_02\"\n";
    let err = decode_document(input).expect_err("Duplicate key must fail");
    match err {
        ToonError::DuplicateKey(key) => assert_eq!(key, "task_id"),
        other => panic!("Expected DuplicateKey error, got: {:?}", other),
    }
}

#[test]
fn test_conformance_size_ceiling_enforcement() {
    // Payload > 256 KiB (262,144 bytes)
    let large_input = "key: \"".to_string() + &"x".repeat(270_000) + "\"\n";
    let err = decode_document(&large_input).expect_err("Payload > 256 KiB must fail");
    match err {
        ToonError::SizeCeilingExceeded { limit, actual } => {
            assert_eq!(limit, 262_144);
            assert!(actual > limit);
        }
        other => panic!("Expected SizeCeilingExceeded, got: {:?}", other),
    }
}

#[test]
fn test_conformance_max_depth_enforcement() {
    // Nesting depth > 4 must fail
    let input = "l1:\n  l2:\n    l3:\n      l4:\n        l5:\n          l6: \"overflow\"\n";
    let err = decode_document(input).expect_err("Nesting depth > 4 must fail");
    match err {
        ToonError::MaxDepthExceeded { limit, actual } => {
            assert_eq!(limit, 4);
            assert!(actual > limit);
        }
        other => panic!("Expected MaxDepthExceeded, got: {:?}", other),
    }
}

#[test]
fn test_conformance_path_traversal_rejection() {
    let doc = ToonValue::Map(vec![
        ("target".to_string(), ToonValue::String("../../../etc/shadow".to_string())),
        ("text".to_string(), ToonValue::String("payload".to_string())),
    ]);
    let err = unpack_legacy_envelope(&doc).expect_err("Path traversal must be rejected");
    match err {
        ToonError::PathTraversalDetected(path) => {
            assert!(path.contains("../"));
        }
        other => panic!("Expected PathTraversalDetected, got: {:?}", other),
    }
}

#[test]
fn test_conformance_canonical_roundtrip() {
    let doc = ToonValue::Map(vec![
        ("active".to_string(), ToonValue::Bool(true)),
        ("counter".to_string(), ToonValue::Int(42)),
        ("label".to_string(), ToonValue::String("production".to_string())),
    ]);

    let encoded = encode(&doc).expect("Encoding should succeed");
    let decoded = decode_document(&encoded).expect("Decoding should succeed");
    assert_eq!(doc, decoded);
}

#[test]
fn test_conformance_string_none_and_numeric_strings_roundtrip() {
    let doc = ToonValue::Map(vec![
        ("empty".to_string(), ToonValue::String(String::new())),
        ("exp_str".to_string(), ToonValue::String("1e5".to_string())),
        ("leading_zero".to_string(), ToonValue::String("0123".to_string())),
        ("none_str".to_string(), ToonValue::String("none".to_string())),
        ("null_val".to_string(), ToonValue::Null),
        ("plus_int".to_string(), ToonValue::String("+1".to_string())),
        ("raw_none".to_string(), ToonValue::Null),
        ("real_bool_str".to_string(), ToonValue::String("true".to_string())),
    ]);

    let encoded = encode(&doc).expect("Encoding should succeed");

    // "none" string must be quoted in the encoded TOON output
    assert!(
        encoded.contains("\"none\""),
        "String 'none' must be quoted: {}",
        encoded
    );
    assert!(
        encoded.contains("\"+1\""),
        "String '+1' must be quoted: {}",
        encoded
    );
    assert!(
        encoded.contains("\"0123\""),
        "String '0123' must be quoted: {}",
        encoded
    );
    assert!(
        encoded.contains("\"1e5\""),
        "String '1e5' must be quoted: {}",
        encoded
    );

    let decoded = decode_document(&encoded).expect("Decoding should succeed");
    assert_eq!(doc, decoded, "Roundtrip must preserve string values and types intact");
}

#[test]
fn test_conformance_unquoted_none_decodes_to_null() {
    let input = "task_status: none\n";
    let decoded = decode_document(input).expect("Decoding unquoted none should succeed");
    if let ToonValue::Map(entries) = decoded {
        assert_eq!(entries.len(), 1);
        assert_eq!(entries[0].1, ToonValue::Null);
    } else {
        panic!("Expected map");
    }

    let input_quoted = "task_status: \"none\"\n";
    let decoded_quoted = decode_document(input_quoted).expect("Decoding quoted \"none\" should succeed");
    if let ToonValue::Map(entries) = decoded_quoted {
        assert_eq!(entries.len(), 1);
        assert_eq!(entries[0].1, ToonValue::String("none".to_string()));
    } else {
        panic!("Expected map");
    }
}
