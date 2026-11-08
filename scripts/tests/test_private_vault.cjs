'use strict';
const assert = require('node:assert/strict');
const test = require('node:test');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const vault = require('../agyos-runtime/lib/private-vault.cjs');
const PASSWORD = 'strong-local-only-test-password-29';
function temporary(fn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-private-vault-test-'));
  fs.chmodSync(dir, 0o700);
  try { return fn(dir); }
  finally { fs.rmSync(dir, { recursive: true, force: true }); }
}
test('vault ciphertext contains no plaintext and authenticated reads work', () => temporary(dir => {
  const file = path.join(dir, 'memory.vault.json');
  vault.initializeVault(file, PASSWORD);
  vault.updateVault(file, PASSWORD, data => ({
    ...data, tier1_recall_memory: { secret: 'CONFIDENTIAL-AGYOS-PROJECT-PLAN' }
  }));
  const stored = fs.readFileSync(file, 'utf8');
  assert.doesNotMatch(stored, /CONFIDENTIAL-AGYOS-PROJECT-PLAN/);
  assert.equal(vault.readVault(file, PASSWORD).tier1_recall_memory.secret,
    'CONFIDENTIAL-AGYOS-PROJECT-PLAN');
  assert.equal(fs.statSync(file).mode & 0o777, 0o600);
  assert.throws(() => vault.readVault(file, 'incorrect-but-long-password-abc'), /authentication failed/);
}));
test('vault tampering is detected, schema is verified, and repeated writes rotate nonce', () => temporary(dir => {
  const file = path.join(dir, 'vault.json');
  vault.initializeVault(file, PASSWORD);
  const one = JSON.parse(fs.readFileSync(file, 'utf8'));
  vault.updateVault(file, PASSWORD, data => ({ ...data, a: 1 }));
  const two = JSON.parse(fs.readFileSync(file, 'utf8'));
  assert.notEqual(one.nonce, two.nonce);
  two.tag = two.tag.replace(/^./, two.tag[0] === 'A' ? 'B' : 'A');
  fs.writeFileSync(file, JSON.stringify(two), { mode: 0o600 });
  assert.throws(() => vault.readVault(file, PASSWORD), /authentication failed/);
  assert.throws(() => vault.openRecord({ ...one, extra: 'malicious' }, PASSWORD), /Invalid or unsupported/);
}));
test('vault fails closed for unsafe file permissions, symlinks and repo paths', () => temporary(dir => {
  const file = path.join(dir, 'vault.json');
  vault.initializeVault(file, PASSWORD);
  assert.throws(() => vault.initializeVault(file, PASSWORD), /already initialized/);
  const alias = path.join(dir, 'alias.vault.json');
  fs.symlinkSync(file, alias);
  assert.throws(() => vault.readVault(alias, PASSWORD), /Unsafe/);
  fs.chmodSync(file, 0o644);
  assert.throws(() => vault.readVault(file, PASSWORD), /Unsafe/);
  assert.throws(() => vault.assertVaultPath(path.join(__dirname, '..', '..', 'private.vault.json')), /outside/);
}));
test('MCP memory writes never fall back to plaintext and encrypted state is fail-closed', () => temporary(dir => {
  const file = path.join(dir, 'memory.vault.json');
  const req = op => JSON.stringify({
    jsonrpc: '2.0', id: 1, method: 'tools/call',
    params: { name: 'agyos_memory', arguments: op },
  }) + '\n';
  const script = path.join(__dirname, '..', '..', 'mcp', 'state-server.cjs');
  const env = { ...process.env, AGYOS_VAULT_PATH: file };
  delete env.AGYOS_VAULT_PASSPHRASE_FD;
  const one = spawnSync(process.execPath, [script], {
    input: req({ action: 'write', tier: 'tier1', key: 'my_secret', value: 'should_not_write' }),
    encoding: 'utf8', env, timeout: 15000,
  });
  assert.equal(one.status, 0, one.stderr);
  assert.match(one.stdout, /AGYOS tool failed/);
  assert.equal(fs.existsSync(file), false);
  vault.initializeVault(file, PASSWORD);
  const locked = spawnSync(process.execPath, [script], {
    input: req({ action: 'read', tier: 'tier1', key: 'my_secret' }),
    encoding: 'utf8', env, timeout: 15000,
  });
  assert.equal(locked.status, 0);
  assert.match(locked.stdout, /AGYOS tool failed/);
  const passFile = path.join(dir, 'key.fd');
  fs.writeFileSync(passFile, PASSWORD, { mode: 0o600 });
  const configured = { ...env, AGYOS_VAULT_PASSPHRASE_FD: '3' };
  const withPassFd = request => {
    const fd = fs.openSync(passFile, 'r');
    try {
      return spawnSync(process.execPath, [script], {
        input: request, encoding: 'utf8', env: configured,
        stdio: ['pipe', 'pipe', 'pipe', fd], timeout: 15000,
      });
    } finally { fs.closeSync(fd); }
  };
  {
    const stored = withPassFd(req({ action: 'write', tier: 'tier1', key: 'my_secret', value: 'CONFIDENTIAL-AGYOS-PROTECTED' }));
    assert.equal(stored.status, 0, stored.stderr);
    assert.match(stored.stdout, /saved in encrypted/);
    assert.doesNotMatch(fs.readFileSync(file, 'utf8'), /CONFIDENTIAL-AGYOS-PROTECTED/);
    const reread = withPassFd(req({ action: 'read', tier: 'tier1', key: 'my_secret' }));
    assert.match(reread.stdout, /CONFIDENTIAL-AGYOS-PROTECTED/);
    const unsafe = withPassFd(req({ action: 'write', tier: 'tier1', key: '__proto__', value: 'hijack' }));
    assert.match(unsafe.stdout, /AGYOS tool failed/);
  }
}));
test('vault CLI initializes without secret appearing in stdout or on disk', () => temporary(dir => {
  const file = path.join(dir, 'vault.json');
  const script = path.join(__dirname, '..', 'agyos-runtime', 'private-vault-cli.cjs');
  const invoke = args => spawnSync(process.execPath, [script, ...args], {
    input: PASSWORD, encoding: 'utf8', timeout: 15000,
  });
  const init = invoke(['vault-init', '--path', file, '--passphrase-fd', '0']);
  assert.equal(init.status, 0, init.stderr);
  assert.doesNotMatch(init.stdout, /strong-local-only-test-password/);
  assert.equal(vault.isInitialized(file), true);
  const status = invoke(['vault-status', '--path', file]);
  assert.match(status.stdout, /"initialized":true/);
  assert.equal(invoke(['vault-init', '--path', file, '--passphrase-fd', '0']).status, 1);
}));
