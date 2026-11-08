'use strict';

/* Local encrypted memory vault; independent of untrusted agent instructions.
 * Not end-to-end encrypted model inference. Node crypto only, no auto-unlock.
 */
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const LIMIT = 1024 * 1024;
const FORMAT = 'agyos.local-memory-vault';
const AAD = Buffer.from('agyos-local-memory-vault-v1', 'utf8');
const SCRYPT = Object.freeze({ N: 32768, r: 8, p: 1, maxmem: 64 * 1024 * 1024 });
const O_NOFOLLOW = fs.constants.O_NOFOLLOW || 0;

function vaultPath(env = process.env) {
  return path.resolve(env.AGYOS_VAULT_PATH ||
    path.join(env.XDG_STATE_HOME || path.join(os.homedir(), '.local', 'state'),
      'agyos', 'private-memory.vault.json'));
}
function assertPrivateDirectory(directory, create = false) {
  if (create) fs.mkdirSync(directory, { recursive: true, mode: 0o700 });
  const st = fs.lstatSync(directory);
  if (!st.isDirectory() || st.isSymbolicLink() || (st.mode & 0o077) !== 0 ||
      (process.getuid && st.uid !== process.getuid()))
    throw new Error('Vault directory must be owned by current user and mode 0700');
}
function assertVaultPath(file) {
  const resolved = path.resolve(file);
  // Never put secrets under checkout even when the caller sets an override.
  const repo = path.resolve(__dirname, '..', '..', '..');
  if (resolved === repo || resolved.startsWith(repo + path.sep))
    throw new Error('Encrypted vault must be located outside AGYOS repository');
  return resolved;
}
function readPrivateFile(file) {
  const st = fs.lstatSync(file);
  if (!st.isFile() || st.isSymbolicLink() || (st.mode & 0o077) !== 0 ||
      (process.getuid && st.uid !== process.getuid()) || st.size > LIMIT * 2)
    throw new Error('Unsafe vault file type, size, owner, or permissions');
  const fd = fs.openSync(file, fs.constants.O_RDONLY | O_NOFOLLOW);
  try {
    const actual = fs.fstatSync(fd);
    if (!actual.isFile() || actual.ino !== st.ino || actual.size > LIMIT * 2)
      throw new Error('Vault file changed during read');
    return fs.readFileSync(fd, { encoding: 'utf8' });
  } finally { fs.closeSync(fd); }
}
function passphraseFromFd(raw) {
  if (!/^[3-9]$/.test(String(raw)))
    throw new Error('AGYOS_VAULT_PASSPHRASE_FD must be a private descriptor 3-9');
  const fd = Number(raw);
  const chunks = [];
  let size = 0, length = 0;
  do {
    const buffer = Buffer.alloc(512);
    length = fs.readSync(fd, buffer, 0, buffer.length, null);
    size += length;
    chunks.push(buffer.subarray(0, length));
    if (size > 4096) throw new Error('Passphrase input exceeds 4096 bytes');
  } while (length !== 0);
  const secret = Buffer.concat(chunks).toString('utf8').replace(/\r?\n$/, '');
  for (const chunk of chunks) chunk.fill(0);
  if (Buffer.byteLength(secret, 'utf8') < 16)
    throw new Error('Vault passphrase must contain at least 16 bytes');
  return secret;
}
function getPassphrase(env = process.env) {
  const fd = env.AGYOS_VAULT_PASSPHRASE_FD;
  if (fd === undefined) throw new Error('Secure vault locked: passphrase FD not configured');
  return passphraseFromFd(fd);
}
function checkRecord(obj) {
  if (!obj || typeof obj !== 'object' || Array.isArray(obj) ||
      Object.keys(obj).sort().join(',') !== 'ciphertext,format,kdf,nonce,salt,tag,version' ||
      obj.format !== FORMAT || obj.version !== 1 || obj.kdf !== 'scrypt-N32768-r8-p1')
    throw new Error('Invalid or unsupported vault file');
  for (const field of ['salt', 'nonce', 'tag', 'ciphertext']) {
    if (typeof obj[field] !== 'string' || obj[field].length > LIMIT * 2 ||
        !/^[a-zA-Z0-9+/]*={0,2}$/.test(obj[field]))
      throw new Error('Invalid vault encoding');
  }
  for (const [key, len] of [['salt', 32], ['nonce', 12], ['tag', 16]]) {
    if (Buffer.from(obj[key], 'base64').length !== len)
      throw new Error('Invalid vault cryptographic parameter length');
  }
}
function makeRecord(data, passphrase) {
  const plain = Buffer.from(JSON.stringify(data), 'utf8');
  if (plain.length > LIMIT) throw new Error('Encrypted memory exceeds 1 MiB limit');
  const salt = crypto.randomBytes(32), nonce = crypto.randomBytes(12);
  const key = crypto.scryptSync(passphrase, salt, 32, SCRYPT);
  let encrypted, tag;
  try {
    const cipher = crypto.createCipheriv('aes-256-gcm', key, nonce);
    cipher.setAAD(AAD);
    encrypted = Buffer.concat([cipher.update(plain), cipher.final()]);
    tag = cipher.getAuthTag();
  } finally { key.fill(0); plain.fill(0); }
  return { format: FORMAT, version: 1, kdf: 'scrypt-N32768-r8-p1',
    salt: salt.toString('base64'), nonce: nonce.toString('base64'),
    ciphertext: encrypted.toString('base64'), tag: tag.toString('base64') };
}
function openRecord(record, passphrase) {
  checkRecord(record);
  const key = crypto.scryptSync(passphrase, Buffer.from(record.salt, 'base64'), 32, SCRYPT);
  let decrypted;
  try {
    const decipher = crypto.createDecipheriv('aes-256-gcm', key,
      Buffer.from(record.nonce, 'base64'));
    decipher.setAAD(AAD);
    decipher.setAuthTag(Buffer.from(record.tag, 'base64'));
    decrypted = Buffer.concat([decipher.update(Buffer.from(record.ciphertext, 'base64')),
      decipher.final()]);
    if (decrypted.length > LIMIT) throw new Error('Decrypted vault exceeds size limit');
    const value = JSON.parse(decrypted.toString('utf8'));
    if (!value || typeof value !== 'object' || Array.isArray(value))
      throw new Error('Invalid decrypted memory structure');
    return value;
  } catch {
    throw new Error('Vault authentication failed (wrong secret or tampering)');
  } finally { key.fill(0); if (decrypted) decrypted.fill(0); }
}
function readVault(file, passphrase) {
  file = assertVaultPath(file);
  assertPrivateDirectory(path.dirname(file));
  return openRecord(JSON.parse(readPrivateFile(file)), passphrase);
}
function writeAtomic(file, contents, createOnly = false) {
  file = assertVaultPath(file);
  const parent = path.dirname(file);
  assertPrivateDirectory(parent, true);
  if (createOnly && fs.existsSync(file)) throw new Error('Vault already initialized');
  const lock = file + '.lock';
  const lockFd = fs.openSync(lock,
    fs.constants.O_CREAT | fs.constants.O_EXCL | fs.constants.O_WRONLY | O_NOFOLLOW, 0o600);
  const temp = path.join(parent, '.agyos-vault-' + crypto.randomBytes(12).toString('hex'));
  try {
    if (createOnly && fs.existsSync(file)) throw new Error('Vault already initialized');
    const fd = fs.openSync(temp,
      fs.constants.O_CREAT | fs.constants.O_EXCL | fs.constants.O_WRONLY | O_NOFOLLOW, 0o600);
    try { fs.writeFileSync(fd, contents); fs.fsyncSync(fd); }
    finally { fs.closeSync(fd); }
    if (fs.existsSync(file)) {
      readPrivateFile(file); // Reject symlink or unsafe preexisting file.
    }
    fs.renameSync(temp, file);
    const dirFd = fs.openSync(parent, fs.constants.O_RDONLY);
    try { fs.fsyncSync(dirFd); } finally { fs.closeSync(dirFd); }
  } finally {
    if (fs.existsSync(temp)) fs.unlinkSync(temp);
    fs.closeSync(lockFd);
    fs.unlinkSync(lock);
  }
}
function initializeVault(file, passphrase) {
  file = assertVaultPath(file);
  if (typeof passphrase !== 'string' || Buffer.byteLength(passphrase, 'utf8') < 16)
    throw new Error('Vault passphrase must be at least 16 bytes');
  writeAtomic(file, JSON.stringify(makeRecord({}, passphrase)) + '\n', true);
}
function updateVault(file, passphrase, mutate) {
  file = assertVaultPath(file);
  // Lock is acquired before reading to prevent concurrent lost updates.
  const dir = path.dirname(file);
  assertPrivateDirectory(dir);
  const lock = file + '.lock';
  const lockFd = fs.openSync(lock,
    fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | O_NOFOLLOW, 0o600);
  let temp;
  try {
    const data = readVault(file, passphrase);
    const updated = mutate(data);
    const record = JSON.stringify(makeRecord(updated, passphrase)) + '\n';
    temp = path.join(dir, '.agyos-vault-' + crypto.randomBytes(12).toString('hex'));
    const fd = fs.openSync(temp,
      fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | O_NOFOLLOW, 0o600);
    try { fs.writeFileSync(fd, record); fs.fsyncSync(fd); }
    finally { fs.closeSync(fd); }
    // Recheck target against symlink swap while holding only our cooperative lock.
    readPrivateFile(file);
    fs.renameSync(temp, file);
    temp = undefined;
    const dirFd = fs.openSync(dir, fs.constants.O_RDONLY);
    try { fs.fsyncSync(dirFd); } finally { fs.closeSync(dirFd); }
  } finally {
    if (temp && fs.existsSync(temp)) fs.unlinkSync(temp);
    fs.closeSync(lockFd);
    fs.unlinkSync(lock);
  }
}
function isInitialized(file = vaultPath()) {
  return fs.existsSync(assertVaultPath(file));
}
module.exports = { vaultPath, getPassphrase, passphraseFromFd, initializeVault,
  readVault, updateVault, isInitialized, makeRecord, openRecord, assertVaultPath };
