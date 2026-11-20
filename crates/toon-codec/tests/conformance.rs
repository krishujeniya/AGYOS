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
    // Exceed 256 KiB
    let large_input = "a: \"x\"\n".repeat(35_000);
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
    // Depth > 4 must fail
    let input = "level1:\n  level2:\n    level3:\n      level4:\n        level5: \"overflow\"\n";
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
