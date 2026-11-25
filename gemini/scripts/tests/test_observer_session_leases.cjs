'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');
const {
  getObserverPidFile,
  listSessionLeases,
  removeSessionLease,
  stopObserverForContext,
  writeSessionLease,
} = require('../agyos-runtime/lib/observer-sessions');

test('session leases are atomically replaced and removal is idempotent', t => {
  const projectDir = fs.mkdtempSync(path.join(os.tmpdir(), 'observer-leases-'));
  t.after(() => fs.rmSync(projectDir, { recursive: true, force: true }));
  const context = { projectDir };
  const leaseFile = writeSessionLease(context, 'session-1', { extra: 'value' });
  assert.equal(JSON.parse(fs.readFileSync(leaseFile, 'utf8')).extra, 'value');
  assert.equal(listSessionLeases(context).length, 1);
  assert.equal(removeSessionLease(context, 'session-1'), true);
  assert.equal(removeSessionLease(context, 'session-1'), true);
  assert.equal(listSessionLeases(context).length, 0);
  assert.deepEqual(fs.readdirSync(path.join(projectDir, '.observer-sessions')), []);
});

test('observer stop rechecks for active session leases', t => {
  const projectDir = fs.mkdtempSync(path.join(os.tmpdir(), 'observer-leases-'));
  t.after(() => fs.rmSync(projectDir, { recursive: true, force: true }));
  const context = { projectDir };
  fs.writeFileSync(getObserverPidFile(context), '99999999\n');
  writeSessionLease(context, 'session-active');
  assert.equal(stopObserverForContext(context), false);
  assert.equal(fs.existsSync(getObserverPidFile(context)), true);
  assert.equal(removeSessionLease(context, 'session-active'), true);
});

test('concurrent session starts retain every lease', async t => {
  const projectDir = fs.mkdtempSync(path.join(os.tmpdir(), 'observer-lock-'));
  t.after(() => fs.rmSync(projectDir, { recursive: true, force: true }));
  const modulePath = path.resolve(__dirname, '../agyos-runtime/lib/observer-sessions.js');
  const start = sessionId => new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ['-e',
      "require(process.argv[1]).writeSessionLease({ projectDir: process.argv[2] }, process.argv[3]);",
      modulePath, projectDir, sessionId,
    ], { stdio: 'ignore' });
    child.on('error', reject);
    child.on('exit', code => code === 0 ? resolve() : reject(new Error(`child exited ${code}`)));
  });
  await Promise.all([start('session-a'), start('session-b')]);
  const context = { projectDir };
  assert.equal(listSessionLeases(context).length, 2);
  assert.equal(stopObserverForContext(context), false);
  assert.equal(fs.existsSync(path.join(projectDir, '.observer-lifecycle.lock')), false);
});

test('a crashed observer lifecycle owner does not wedge later session starts', t => {
  const projectDir = fs.mkdtempSync(path.join(os.tmpdir(), 'observer-stale-lock-'));
  t.after(() => fs.rmSync(projectDir, { recursive: true, force: true }));
  const lockPath = path.join(projectDir, '.observer-lifecycle.lock');
  fs.writeFileSync(lockPath, JSON.stringify({ pid: 99999999, hostname: os.hostname(), token: 'stale' }));

  writeSessionLease({ projectDir }, 'session-after-crash');

  assert.equal(listSessionLeases({ projectDir }).length, 1);
  assert.equal(fs.existsSync(lockPath), false);
  assert.equal(fs.existsSync(`${lockPath}.reclaim`), false);
});
