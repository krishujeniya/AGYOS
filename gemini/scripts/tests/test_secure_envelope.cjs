'use strict';
const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const secure = require('../agyos-runtime/lib/e2ee.cjs');
const PASS = 'integration-test-passphrase-123456789';
const user = () => secure.unlockIdentity(secure.newIdentity(PASS), PASS);
const clone = x => JSON.parse(JSON.stringify(x));

test('authenticated exchange decrypts for correct recipient and signer only', () => {
  const alice = user(), bob = user(), eve = user();
  const message = Buffer.from('private agent message');
  const envelope = secure.encryptBytes(alice, bob.public, message);
  assert.deepEqual(secure.decryptBytes(bob, alice.public, envelope), message);
  assert.equal(JSON.stringify(envelope).includes('private agent message'), false);
  assert.throws(() => secure.decryptBytes(eve, alice.public, envelope), /not addressed/);
  assert.throws(() => secure.decryptBytes(bob, eve.public, envelope), /Sender identity/);
});
test('tampered fields, forged identities and wrong passphrases fail closed', () => {
  const a = user(), b = user();
  const env = secure.encryptBytes(a, b.public, Buffer.from('secret'));
  for (const field of ['ciphertext', 'tag', 'signature']) {
    const modified = clone(env);
    modified[field] = modified[field].replace(/^./, modified[field][0] === 'A' ? 'B' : 'A');
    assert.throws(() => secure.decryptBytes(b, a.public, modified));
  }
  for (const field of ['nonce', 'salt', 'ephemeral']) {
    const modified = clone(env);
    modified.header[field] = modified.header[field].replace(/^./, modified.header[field][0] === 'A' ? 'B' : 'A');
    assert.throws(() => secure.decryptBytes(b, a.public, modified));
  }
  const pub = clone(a.public); pub.fingerprint = '0'.repeat(64);
  assert.throws(() => secure.validatePublic(pub), /fingerprint/);
  assert.throws(() => secure.unlockIdentity(secure.newIdentity(PASS), 'wrong-password-but-long-enough'), /authentication failed/);
  env.injection = 'untrusted';
  assert.throws(() => secure.decryptBytes(b, a.public, env), /Unexpected/);
});
test('every encryption uses new ephemeral keys and nonce', () => {
  const a = user(), b = user();
  const x = secure.encryptBytes(a, b.public, Buffer.from('same'));
  const y = secure.encryptBytes(a, b.public, Buffer.from('same'));
  assert.notEqual(x.header.ephemeral, y.header.ephemeral);
  assert.notEqual(x.header.nonce, y.header.nonce);
  assert.notEqual(x.ciphertext, y.ciphertext);
});
test('private identity file uses restrictive permissions and resists symlinks', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-secure-'));
  try {
    fs.chmodSync(dir, 0o700);
    const file = path.join(dir, 'identity.json');
    secure.createIdentityFile(file, PASS);
    assert.equal(fs.statSync(file).mode & 0o777, 0o600);
    assert.throws(() => secure.createIdentityFile(file, PASS), /EEXIST/);
    const alias = path.join(dir, 'alias');
    fs.symlinkSync(file, alias);
    assert.throws(() => secure.readIdentityFile(alias));
    fs.chmodSync(file, 0o644);
    assert.throws(() => secure.readIdentityFile(file), /permissions/);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
test('CLI round-trip and no-clobber checks', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-cli-'));
  const script = path.join(__dirname, '..', 'agyos-runtime', 'secure-envelope.cjs');
  const call = args => spawnSync(process.execPath, [script, ...args],
    { input: PASS, encoding: 'utf8', timeout: 20000 });
  try {
    fs.chmodSync(dir, 0o700);
    const alice = path.join(dir, 'alice.key.json');
    const bob = path.join(dir, 'bob.key.json');
    const aPub = path.join(dir, 'alice.pub.json');
    const bPub = path.join(dir, 'bob.pub.json');
    const input = path.join(dir, 'input.txt');
    const output = path.join(dir, 'ciphertext.json');
    const recovered = path.join(dir, 'recovered.txt');
    fs.writeFileSync(input, 'CONFIDENTIAL MESSAGE');
    for (const file of [alice, bob])
      assert.equal(call(['keygen', '--identity', file, '--passphrase-fd', '0']).status, 0);
    assert.equal(call(['public', '--identity', alice, '--out', aPub]).status, 0);
    assert.equal(call(['public', '--identity', bob, '--out', bPub]).status, 0);
    const result = call(['encrypt', '--identity', alice, '--recipient', bPub,
      '--in', input, '--out', output, '--passphrase-fd', '0']);
    assert.equal(result.status, 0, result.stderr);
    assert.equal(fs.readFileSync(output, 'utf8').includes('CONFIDENTIAL MESSAGE'), false);
    const decrypted = call(['decrypt', '--identity', bob, '--sender', aPub,
      '--in', output, '--out', recovered, '--passphrase-fd', '0']);
    assert.equal(decrypted.status, 0, decrypted.stderr);
    assert.equal(fs.readFileSync(recovered, 'utf8'), 'CONFIDENTIAL MESSAGE');
    assert.equal(call(['decrypt', '--identity', bob, '--sender', aPub,
      '--in', output, '--out', recovered, '--passphrase-fd', '0']).status, 1);
    assert.equal(call(['keygen', '--identity', path.join(__dirname, '..', '..', '.unsafe-secret'),
      '--passphrase-fd', '0']).status, 1);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});
