//! Golden and Differential Test Suite for TOON Codec.
//! Principles: P04, P09, P13

use toon_codec::{
    decode_document, decode_records, encode_records, unpack_legacy_envelope, ToonValue,
};

#[test]
fn test_golden_tabular_stream() {
    let input = "skills[2]{name, tier}:\n  - \"skill-a\", 1\n  - \"skill-b\", 2\n";
    let records = decode_records(input).expect("Should decode tabular stream");
    assert_eq!(records.len(), 2);
    assert_eq!(records[0]["name"], "skill-a");
    assert_eq!(records[0]["tier"], 1);
    assert_eq!(records[1]["name"], "skill-b");
    assert_eq!(records[1]["tier"], 2);

    let re_encoded = encode_records(&records, "skills", true);
    assert!(re_encoded.starts_with("skills[2]{name, tier}:"));
}

#[test]
fn test_golden_legacy_envelope_unpack() {
    let input = "target: \"artifacts/proposals/client.md\"\ntext: \"Proposal content body\"\n";
    let val = decode_document(input).expect("Should decode legacy envelope");
    let envelope = unpack_legacy_envelope(&val).expect("Should unpack envelope");
    assert_eq!(envelope.target.as_deref(), Some("artifacts/proposals/client.md"));
    assert_eq!(envelope.text_body.as_deref(), Some("Proposal content body"));
}

#[test]
fn test_golden_numeric_boundaries() {
    let input = "max_i64: 9223372036854775807\nmin_i64: -9223372036854775808\nfloat_val: 3.14159\n";
    let val = decode_document(input).expect("Numeric boundary parse should succeed");
    if let ToonValue::Map(entries) = val {
        assert_eq!(entries[0].1, ToonValue::Int(i64::MAX));
        assert_eq!(entries[1].1, ToonValue::Int(i64::MIN));
        assert_eq!(entries[2].1, ToonValue::Float(3.14159));
    } else {
        panic!("Expected map");
    }
}
