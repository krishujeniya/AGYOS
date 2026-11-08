'use strict';
// Endpoint-side AGYOS sealed envelopes: no remote key custody or network calls.
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const MAX_PLAINTEXT = 8 * 1024 * 1024;
const MAX_ENVELOPE = 12 * 1024 * 1024;
const SUITE = 'X25519-HKDF-SHA256-AES256GCM-ED25519';
const CTX = Buffer.from('AGYOS-E2EE-V1\0', 'utf8');
const SCRYPT_OPTIONS = Object.freeze({ N: 32768, r: 8, p: 1, maxmem: 64 * 1024 * 1024 });
const FILE_NOFOLLOW = fs.constants.O_NOFOLLOW || 0;

function assertShape(obj, keys) {
  if (!obj || typeof obj !== 'object' || Array.isArray(obj)) throw new Error('Invalid object');
  const actual = Object.keys(obj).sort();
  if (actual.length !== keys.length || keys.slice().sort().some((k, i) => actual[i] !== k))
    throw new Error('Unexpected or missing fields');
}
function decB64(s, length) {
  if (typeof s !== 'string' || s.length > MAX_ENVELOPE * 2 ||
      !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(s))
    throw new Error('Invalid base64 encoding');
  const b = Buffer.from(s, 'base64');
  if (b.toString('base64') !== s || (length !== undefined && b.length !== length))
    throw new Error('Invalid encoded length');
  return b;
}
function b64(buf) { return Buffer.from(buf).toString('base64'); }
function derPublic(key) { return key.export({ format: 'der', type: 'spki' }); }
function derPrivate(key) { return key.export({ format: 'der', type: 'pkcs8' }); }
function fingerprint(agreement, signing) {
  return crypto.createHash('sha256').update('agyos/public-identity/v1\0')
    .update(decB64(agreement)).update(decB64(signing)).digest('hex');
}
function validatePublic(pub) {
  assertShape(pub, ['kind', 'version', 'agreement', 'signing', 'fingerprint']);
  if (pub.kind !== 'agyos.public-identity' || pub.version !== 1)
    throw new Error('Unsupported public identity');
  const a = crypto.createPublicKey({ key: decB64(pub.agreement), format: 'der', type: 'spki' });
  const s = crypto.createPublicKey({ key: decB64(pub.signing), format: 'der', type: 'spki' });
  if (a.asymmetricKeyType !== 'x25519' || s.asymmetricKeyType !== 'ed25519')
    throw new Error('Unsupported public key algorithms');
  if (fingerprint(pub.agreement, pub.signing) !== pub.fingerprint)
    throw new Error('Public key fingerprint mismatch');
  return pub;
}
function makePublic(agreement, signing) {
  const a = b64(derPublic(agreement)), s = b64(derPublic(signing));
  return { kind: 'agyos.public-identity', version: 1, agreement: a,
    signing: s, fingerprint: fingerprint(a, s) };
}
function requirePassphrase(passphrase) {
  if (typeof passphrase !== 'string' || passphrase.length < 12 || passphrase.length > 4096)
    throw new Error('Passphrase must contain 12-4096 characters');
}
function derive(passphrase, salt) {
  return crypto.scryptSync(Buffer.from(passphrase, 'utf8'), salt, 32, SCRYPT_OPTIONS);
}
function newIdentity(passphrase) {
  requirePassphrase(passphrase);
  const agreement = crypto.generateKeyPairSync('x25519');
  const signing = crypto.generateKeyPairSync('ed25519');
  const publicIdentity = makePublic(agreement.publicKey, signing.publicKey);
  const secretMaterial = Buffer.from(JSON.stringify({
    agreement: b64(derPrivate(agreement.privateKey)),
    signing: b64(derPrivate(signing.privateKey)),
  }), 'utf8');
  const salt = crypto.randomBytes(32), nonce = crypto.randomBytes(12);
  const key = derive(passphrase, salt);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, nonce);
  cipher.setAAD(CTX);
  const ciphertext = Buffer.concat([cipher.update(secretMaterial), cipher.final()]);
  const tag = cipher.getAuthTag();
  secretMaterial.fill(0);
  key.fill(0);
  return { kind: 'agyos.private-identity', version: 1, public: publicIdentity,
    secret: { kdf: 'scrypt-N32768-r8-p1', salt: b64(salt), nonce: b64(nonce),
      ciphertext: b64(ciphertext), tag: b64(tag) } };
}
function unlockIdentity(record, passphrase) {
  requirePassphrase(passphrase);
  assertShape(record, ['kind', 'version', 'public', 'secret']);
  if (record.kind !== 'agyos.private-identity' || record.version !== 1)
    throw new Error('Unsupported private identity');
  const pub = validatePublic(record.public);
  assertShape(record.secret, ['kdf', 'salt', 'nonce', 'ciphertext', 'tag']);
  if (record.secret.kdf !== 'scrypt-N32768-r8-p1')
    throw new Error('Unsupported identity key derivation');
  const key = derive(passphrase, decB64(record.secret.salt, 32));
  let plain;
  try {
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, decB64(record.secret.nonce, 12));
    decipher.setAAD(CTX);
    decipher.setAuthTag(decB64(record.secret.tag, 16));
    plain = Buffer.concat([decipher.update(decB64(record.secret.ciphertext)), decipher.final()]);
  } catch {
    throw new Error('Identity authentication failed');
  } finally {
    key.fill(0);
  }
  let material;
  try { material = JSON.parse(plain.toString('utf8')); }
  finally { plain.fill(0); }
  assertShape(material, ['agreement', 'signing']);
  const a = crypto.createPrivateKey({ key: decB64(material.agreement), format: 'der', type: 'pkcs8' });
  const s = crypto.createPrivateKey({ key: decB64(material.signing), format: 'der', type: 'pkcs8' });
  if (a.asymmetricKeyType !== 'x25519' || s.asymmetricKeyType !== 'ed25519')
    throw new Error('Invalid private key algorithms');
  const computed = makePublic(crypto.createPublicKey(a), crypto.createPublicKey(s));
  if (computed.fingerprint !== pub.fingerprint ||
      computed.agreement !== pub.agreement || computed.signing !== pub.signing)
    throw new Error('Identity private/public keys mismatch');
  return { public: pub, agreementPrivate: a, signingPrivate: s };
}
function canonicalHeader(h) {
  assertShape(h, ['version', 'kind', 'suite', 'to', 'from', 'sender', 'ephemeral', 'salt', 'nonce']);
  if (h.version !== 1 || h.kind !== 'agyos.e2ee-header' || h.suite !== SUITE)
    throw new Error('Unsupported envelope version or algorithms');
  return { version: h.version, kind: h.kind, suite: h.suite, to: h.to,
    from: h.from, sender: validatePublic(h.sender), ephemeral: h.ephemeral,
    salt: h.salt, nonce: h.nonce };
}
function signedBytes(header, ciphertext, tag) {
  return Buffer.concat([CTX, Buffer.from(JSON.stringify({
    header: canonicalHeader(header), ciphertext, tag,
  }), 'utf8')]);
}
function sealedKey(privateKey, publicKey, salt, header) {
  const secret = crypto.diffieHellman({ privateKey, publicKey });
  try {
    return Buffer.from(crypto.hkdfSync('sha256', secret, salt,
      Buffer.concat([CTX, Buffer.from(header.to + ':' + header.from, 'utf8')]), 32));
  } finally { secret.fill(0); }
}
function encryptBytes(sender, recipient, data) {
  recipient = validatePublic(recipient);
  if (!Buffer.isBuffer(data) || data.length > MAX_PLAINTEXT)
    throw new Error('Payload must be a buffer no larger than 8 MiB');
  const eph = crypto.generateKeyPairSync('x25519');
  const salt = crypto.randomBytes(32), nonce = crypto.randomBytes(12);
  const header = canonicalHeader({
    version: 1, kind: 'agyos.e2ee-header', suite: SUITE,
    to: recipient.fingerprint, from: sender.public.fingerprint,
    sender: sender.public, ephemeral: b64(derPublic(eph.publicKey)),
    salt: b64(salt), nonce: b64(nonce),
  });
  const recipientKey = crypto.createPublicKey({ key: decB64(recipient.agreement), format: 'der', type: 'spki' });
  const key = sealedKey(eph.privateKey, recipientKey, salt, header);
  let ciphertext, tag;
  try {
    const cipher = crypto.createCipheriv('aes-256-gcm', key, nonce);
    cipher.setAAD(Buffer.concat([CTX, Buffer.from(JSON.stringify(header))]));
    ciphertext = Buffer.concat([cipher.update(data), cipher.final()]);
    tag = cipher.getAuthTag();
  } finally { key.fill(0); }
  const body = { header, ciphertext: b64(ciphertext), tag: b64(tag) };
  return { kind: 'agyos.e2ee-envelope', version: 1, ...body,
    signature: b64(crypto.sign(null, signedBytes(header, body.ciphertext, body.tag), sender.signingPrivate)) };
}
function decryptBytes(recipient, trustedSender, envelope) {
  trustedSender = validatePublic(trustedSender);
  assertShape(envelope, ['kind', 'version', 'header', 'ciphertext', 'tag', 'signature']);
  if (envelope.kind !== 'agyos.e2ee-envelope' || envelope.version !== 1)
    throw new Error('Unsupported envelope');
  const h = canonicalHeader(envelope.header);
  if (h.to !== recipient.public.fingerprint) throw new Error('Envelope is not addressed to this recipient');
  if (h.from !== trustedSender.fingerprint ||
      h.sender.signing !== trustedSender.signing || h.sender.agreement !== trustedSender.agreement)
    throw new Error('Sender identity does not match trusted public key');
  const signer = crypto.createPublicKey({ key: decB64(trustedSender.signing), format: 'der', type: 'spki' });
  if (!crypto.verify(null, signedBytes(h, envelope.ciphertext, envelope.tag),
                     signer, decB64(envelope.signature, 64)))
    throw new Error('Envelope signature verification failed');
  const eph = crypto.createPublicKey({ key: decB64(h.ephemeral), format: 'der', type: 'spki' });
  if (eph.asymmetricKeyType !== 'x25519') throw new Error('Invalid ephemeral key');
  const key = sealedKey(recipient.agreementPrivate, eph, decB64(h.salt, 32), h);
  try {
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, decB64(h.nonce, 12));
    decipher.setAAD(Buffer.concat([CTX, Buffer.from(JSON.stringify(h))]));
    decipher.setAuthTag(decB64(envelope.tag, 16));
    const data = Buffer.concat([decipher.update(decB64(envelope.ciphertext)), decipher.final()]);
    if (data.length > MAX_PLAINTEXT) throw new Error('Decrypted payload too large');
    return data;
  } catch {
    throw new Error('Envelope authenticated decryption failed');
  } finally { key.fill(0); }
}
function defaultIdentityPath() {
  return path.join(process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'),
    'agyos', 'identity.json');
}
function readRegularFile(file, limit = MAX_ENVELOPE) {
  const stat = fs.lstatSync(file);
  if (!stat.isFile() || stat.isSymbolicLink() || stat.size > limit)
    throw new Error('Refusing symlink, non-regular or oversized file');
  const fd = fs.openSync(file, fs.constants.O_RDONLY | FILE_NOFOLLOW);
  try {
    const actual = fs.fstatSync(fd);
    if (!actual.isFile() || actual.size > limit) throw new Error('File changed during read');
    const contents = fs.readFileSync(fd);
    if (contents.length > limit) throw new Error('File exceeds size limit');
    return contents;
  } finally { fs.closeSync(fd); }
}
function writeNewFile(file, content, mode = 0o600) {
  const flags = fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | FILE_NOFOLLOW;
  const fd = fs.openSync(file, flags, mode);
  try {
    fs.writeFileSync(fd, content);
    fs.fsyncSync(fd);
  } catch (err) {
    fs.closeSync(fd);
    fs.unlinkSync(file);
    throw err;
  }
  fs.closeSync(fd);
}
function readIdentityFile(file) {
  const stat = fs.lstatSync(file);
  if ((stat.mode & 0o077) !== 0 || (process.getuid && stat.uid !== process.getuid()))
    throw new Error('Private identity permissions or ownership are unsafe');
  return JSON.parse(readRegularFile(file, 64 * 1024).toString('utf8'));
}
function createIdentityFile(file, passphrase) {
  const parent = path.dirname(path.resolve(file));
  fs.mkdirSync(parent, { recursive: true, mode: 0o700 });
  const stat = fs.lstatSync(parent);
  if (!stat.isDirectory() || (stat.mode & 0o077) !== 0)
    throw new Error('Private identity directory must be mode 0700');
  const identity = newIdentity(passphrase);
  writeNewFile(file, JSON.stringify(identity, null, 2) + '\n');
  return identity.public;
}
function readPublicFile(file) {
  return validatePublic(JSON.parse(readRegularFile(file, 64 * 1024).toString('utf8')));
}
module.exports = { MAX_PLAINTEXT, MAX_ENVELOPE, defaultIdentityPath, newIdentity,
  unlockIdentity, validatePublic, encryptBytes, decryptBytes, createIdentityFile,
  readIdentityFile, readPublicFile, readRegularFile, writeNewFile };
