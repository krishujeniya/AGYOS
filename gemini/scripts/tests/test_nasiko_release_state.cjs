'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { acquireLifecycleLock, digestBytes, installNasiko, uninstallNasiko } = require('../agyos-runtime/lib/nasiko-release');

test('Nasiko install dry-run plans without creating the destination', async t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'nasiko-state-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const installDir = path.join(root, 'bin');
  const plan = await installNasiko({ dryRun: true, installDir }, { platform: 'linux', arch: 'x64' });
  assert.equal(plan.dryRun, true);
  assert.equal(fs.existsSync(installDir), false);
});

test('Nasiko install requires consent before creating the destination', async t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'nasiko-state-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const installDir = path.join(root, 'bin');
  await assert.rejects(
    installNasiko({ installDir }, { platform: 'linux', arch: 'x64' }),
    /requires explicit --yes consent/,
  );
  assert.equal(fs.existsSync(installDir), false);
});

test('Nasiko uninstall dry-run and absent-install outcomes do not remove files', t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'nasiko-state-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const installDir = path.join(root, 'bin');
  const plan = uninstallNasiko({ dryRun: true, installDir }, { platform: 'linux', arch: 'x64' });
  assert.equal(plan.dryRun, true);
  const absent = uninstallNasiko({ yes: true, installDir }, { platform: 'linux', arch: 'x64' });
  assert.equal(absent.removed, false);
  assert.equal(fs.existsSync(installDir), false);
});

test('Nasiko lifecycle lock serializes operations and recovers a dead owner', t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'nasiko-lock-state-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const lockPath = path.join(root, '.ecc-nasiko-lifecycle.lock');
  const release = acquireLifecycleLock(root);
  assert.throws(() => acquireLifecycleLock(root, fs, { timeoutMs: 0 }), /Nasiko lifecycle is busy/);
  release();
  assert.equal(fs.existsSync(lockPath), false);

  fs.writeFileSync(lockPath, JSON.stringify({ pid: 99999999, startedAt: new Date().toISOString(), token: 'stale' }));
  const recoveredRelease = acquireLifecycleLock(root, fs, { isProcessAlive: () => false });
  recoveredRelease();
  assert.equal(fs.existsSync(lockPath), false);
});

test('Nasiko publication removes a partially written receipt and owned binary', async t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'nasiko-rollback-state-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const installDir = path.join(root, 'bin');
  const binary = Buffer.from('qualified-test-binary');
  const archive = Buffer.from('qualified-test-archive');
  const layerDigest = digestBytes(archive);
  const manifest = Buffer.from(JSON.stringify({
    schemaVersion: 2,
    layers: [{ mediaType: 'application/gzip', digest: layerDigest, size: archive.length }],
  }));
  const manifestDigest = digestBytes(manifest);
  const binaryDigest = digestBytes(binary);
  const dependencies = {
    platform: 'linux',
    arch: 'x64',
    releaseOverride: { manifestDigest, binaryDigest },
    fetchBytes: async url => url.includes('/manifests/') ? manifest : archive,
    extractBinary: () => binary,
    writeMetadata: (_metadataPath, _metadata, descriptor) => {
      fs.writeFileSync(descriptor, 'partial receipt');
      throw new Error('simulated receipt write failure');
    },
  };

  await assert.rejects(
    installNasiko({ yes: true, installDir }, dependencies),
    /simulated receipt write failure/,
  );

  assert.equal(fs.existsSync(path.join(installDir, 'nasiko')), false);
  assert.equal(fs.existsSync(path.join(installDir, '.ecc-nasiko-install.json')), false);
  assert.equal(fs.existsSync(path.join(installDir, '.ecc-nasiko-lifecycle.lock')), false);
});
