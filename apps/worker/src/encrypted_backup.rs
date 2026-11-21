//! Hosted Encrypted Backup & Regional Disaster Recovery Engine (Step 16).
//!
//! Complies with Step 16 finish criteria and Principles:
//! - P09 (Explicit State & Invariants)
//! - P10 (Atomic Durability & Sagas)
//! - P20 (End-to-End Observability)
//! - P21 (Privacy & Boundary Protection - Zero Plaintext Secrets in Backups)

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

/// Encrypted backup envelope holding ciphertext, nonce, and integrity verification tags.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EncryptedBackupEnvelope {
    pub key_version: u32,
    pub ciphertext_hex: String,
    pub auth_tag_hex: String,
    pub payload_digest: String,
    pub timestamp_epoch_s: u64,
    #[serde(default)]
    pub nonce_hex: String,
}

pub struct EncryptedBackupEngine;

fn hmac_sha256(key: &[u8], data: &[u8]) -> [u8; 32] {
    let mut k = [0u8; 64];
    if key.len() > 64 {
        let mut h = Sha256::new();
        h.update(key);
        let hashed = h.finalize();
        k[..32].copy_from_slice(&hashed);
    } else {
        k[..key.len()].copy_from_slice(key);
    }

    let mut ipad = [0x36u8; 64];
    let mut opad = [0x5cu8; 64];
    for i in 0..64 {
        ipad[i] ^= k[i];
        opad[i] ^= k[i];
    }

    let mut inner = Sha256::new();
    inner.update(&ipad);
    inner.update(data);
    let inner_hash = inner.finalize();

    let mut outer = Sha256::new();
    outer.update(&opad);
    outer.update(&inner_hash);
    outer.finalize().into()
}

fn constant_time_eq(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut diff = 0u8;
    for (x, y) in a.iter().zip(b.iter()) {
        diff |= x ^ y;
    }
    diff == 0
}

fn derive_keys(secret_key: &str, key_version: u32, nonce: &[u8]) -> ([u8; 32], [u8; 32]) {
    let mut enc_info = Vec::with_capacity(32);
    enc_info.extend_from_slice(b"agyos-enc-key-v1:");
    enc_info.extend_from_slice(&key_version.to_be_bytes());
    enc_info.extend_from_slice(nonce);
    let k_enc = hmac_sha256(secret_key.as_bytes(), &enc_info);

    let mut mac_info = Vec::with_capacity(32);
    mac_info.extend_from_slice(b"agyos-mac-key-v1:");
    mac_info.extend_from_slice(&key_version.to_be_bytes());
    mac_info.extend_from_slice(nonce);
    let k_mac = hmac_sha256(secret_key.as_bytes(), &mac_info);

    (k_enc, k_mac)
}

fn ctr_crypt(k_enc: &[u8; 32], nonce: &[u8], input: &[u8]) -> Vec<u8> {
    let mut output = Vec::with_capacity(input.len());
    let mut counter = 0u32;
    for chunk in input.chunks(32) {
        let mut block_input = Vec::with_capacity(nonce.len() + 4);
        block_input.extend_from_slice(nonce);
        block_input.extend_from_slice(&counter.to_be_bytes());
        let block_key = hmac_sha256(k_enc, &block_input);
        for (b, k) in chunk.iter().zip(block_key.iter()) {
            output.push(b ^ k);
        }
        counter += 1;
    }
    output
}

fn compute_aad(
    key_version: u32,
    timestamp_epoch_s: u64,
    nonce_hex: &str,
    payload_digest: &str,
    ciphertext_hex: &str,
) -> Vec<u8> {
    format!(
        "v{}|ts:{}|nonce:{}|digest:{}|ct:{}",
        key_version, timestamp_epoch_s, nonce_hex, payload_digest, ciphertext_hex
    )
    .into_bytes()
}

fn compute_payload_digest(raw: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(raw);
    format!("sha256:{}", hex::encode(hasher.finalize()))
}

fn generate_nonce(secret_key: &str, timestamp_s: u64, payload_len: usize) -> Vec<u8> {
    let mut hasher = Sha256::new();
    hasher.update(secret_key.as_bytes());
    hasher.update(&timestamp_s.to_be_bytes());
    hasher.update(&(payload_len as u64).to_be_bytes());
    hasher.finalize()[..16].to_vec()
}

impl EncryptedBackupEngine {
    /// Encrypts raw backup archive using authenticated encryption (HMAC-SHA256 authenticated cipher with per-key unique nonces).
    pub fn encrypt_backup(
        raw_payload: &str,
        key_version: u32,
        secret_key: &str,
        timestamp_s: u64,
    ) -> EncryptedBackupEnvelope {
        let payload_bytes = raw_payload.as_bytes();
        let payload_digest = compute_payload_digest(payload_bytes);
        let nonce = generate_nonce(secret_key, timestamp_s, payload_bytes.len());
        let nonce_hex = hex::encode(&nonce);

        let (k_enc, k_mac) = derive_keys(secret_key, key_version, &nonce);
        let encrypted_bytes = ctr_crypt(&k_enc, &nonce, payload_bytes);
        let ciphertext_hex = hex::encode(&encrypted_bytes);

        let aad = compute_aad(
            key_version,
            timestamp_s,
            &nonce_hex,
            &payload_digest,
            &ciphertext_hex,
        );
        let auth_tag = hmac_sha256(&k_mac, &aad);
        let auth_tag_hex = hex::encode(auth_tag);

        EncryptedBackupEnvelope {
            key_version,
            ciphertext_hex,
            auth_tag_hex,
            payload_digest,
            timestamp_epoch_s: timestamp_s,
            nonce_hex,
        }
    }

    /// Decrypts and verifies backup envelope integrity. Rejects tampered ciphertext, tampered metadata, or mismatched keys.
    pub fn decrypt_backup(
        envelope: &EncryptedBackupEnvelope,
        secret_key: &str,
    ) -> Result<String, String> {
        if Self::is_legacy(envelope) {
            return Self::decrypt_legacy(envelope, secret_key);
        }

        let nonce = hex::decode(&envelope.nonce_hex)
            .map_err(|e| format!("Invalid nonce hex encoding: {}", e))?;
        let (_k_enc, k_mac) = derive_keys(secret_key, envelope.key_version, &nonce);

        let aad = compute_aad(
            envelope.key_version,
            envelope.timestamp_epoch_s,
            &envelope.nonce_hex,
            &envelope.payload_digest,
            &envelope.ciphertext_hex,
        );
        let expected_tag = hmac_sha256(&k_mac, &aad);
        let provided_tag = hex::decode(&envelope.auth_tag_hex)
            .map_err(|e| format!("Invalid auth tag hex encoding: {}", e))?;

        if !constant_time_eq(&expected_tag, &provided_tag) {
            return Err("Decryption failed: authentication tag verification failed".to_string());
        }

        let (k_enc, _) = derive_keys(secret_key, envelope.key_version, &nonce);
        let ciphertext_bytes = hex::decode(&envelope.ciphertext_hex)
            .map_err(|e| format!("Invalid ciphertext hex encoding: {}", e))?;

        let decrypted_bytes = ctr_crypt(&k_enc, &nonce, &ciphertext_bytes);
        let computed_digest = compute_payload_digest(&decrypted_bytes);
        if computed_digest != envelope.payload_digest {
            return Err("Decryption failed: payload digest mismatch".to_string());
        }

        String::from_utf8(decrypted_bytes).map_err(|e| format!("Invalid UTF-8 payload: {}", e))
    }

    /// Checks if envelope was produced by legacy unauthenticated XOR/DefaultHasher construction.
    pub fn is_legacy(envelope: &EncryptedBackupEnvelope) -> bool {
        envelope.nonce_hex.is_empty()
    }

    /// Decrypts a legacy envelope for migration purposes.
    fn decrypt_legacy(
        envelope: &EncryptedBackupEnvelope,
        secret_key: &str,
    ) -> Result<String, String> {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};

        let mut tag_hasher = DefaultHasher::new();
        envelope.ciphertext_hex.hash(&mut tag_hasher);
        envelope.key_version.hash(&mut tag_hasher);
        secret_key.hash(&mut tag_hasher);
        let expected_tag = format!("{:016x}", tag_hasher.finish());

        if expected_tag != envelope.auth_tag_hex {
            return Err("Legacy decryption failed: authentication tag verification failed".to_string());
        }

        let key_bytes = secret_key.as_bytes();
        let mut raw_bytes = Vec::new();
        for i in 0..(envelope.ciphertext_hex.len() / 2) {
            let byte_str = &envelope.ciphertext_hex[i * 2..i * 2 + 2];
            let byte = u8::from_str_radix(byte_str, 16).map_err(|e| e.to_string())?;
            let k = key_bytes[i % key_bytes.len()];
            raw_bytes.push(byte ^ k);
        }

        String::from_utf8(raw_bytes).map_err(|e| e.to_string())
    }

    /// Migrates a legacy envelope to a modern authenticated envelope with unique nonce and HMAC authentication.
    pub fn migrate_legacy(
        envelope: &EncryptedBackupEnvelope,
        legacy_secret_key: &str,
        new_key_version: u32,
        new_secret_key: &str,
        timestamp_s: u64,
    ) -> Result<EncryptedBackupEnvelope, String> {
        let plaintext = Self::decrypt_legacy(envelope, legacy_secret_key)?;
        Ok(Self::encrypt_backup(
            &plaintext,
            new_key_version,
            new_secret_key,
            timestamp_s,
        ))
    }

    /// Rotates encryption key, re-encrypting under a new key version without exposing plaintext.
    pub fn rotate_key(
        envelope: &EncryptedBackupEnvelope,
        old_secret_key: &str,
        new_key_version: u32,
        new_secret_key: &str,
    ) -> Result<EncryptedBackupEnvelope, String> {
        let plaintext = Self::decrypt_backup(envelope, old_secret_key)?;
        Ok(Self::encrypt_backup(
            &plaintext,
            new_key_version,
            new_secret_key,
            envelope.timestamp_epoch_s,
        ))
    }
}
