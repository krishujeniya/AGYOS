'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

test('concurrent processes serialize while recovering one stale lock', async t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'process-lock-state-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const lockPath = path.join(root, 'shared.lock');
  const logPath = path.join(root, 'events.log');
  const modulePath = path.resolve(__dirname, '../agyos-runtime/lib/process-lock.js');
  fs.writeFileSync(lockPath, JSON.stringify({
    pid: 99999999,
    hostname: os.hostname(),
    startedAt: '2020-01-01T00:00:00.000Z',
    token: 'stale',
  }));

  const workerSource = [
    "const fs=require('fs');",
    "const {acquireProcessLock}=require(process.argv[1]);",
    'const release=acquireProcessLock(process.argv[2],{timeoutMs:10000,label:"CI lock"});',
    'fs.appendFileSync(process.argv[3],`start:${process.pid}\\n`);',
    'Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,75);',
    'fs.appendFileSync(process.argv[3],`end:${process.pid}\\n`);',
    'release();',
  ].join('\n');
  const runWorker = () => new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ['-e', workerSource, modulePath, lockPath, logPath], { stdio: 'ignore' });
    child.on('error', reject);
    child.on('exit', code => code === 0 ? resolve() : reject(new Error(`worker exited ${code}`)));
  });

  await Promise.all(Array.from({ length: 5 }, runWorker));

  let active = 0;
  const events = fs.readFileSync(logPath, 'utf8').trim().split('\n');
  for (const event of events) {
    if (event.startsWith('start:')) {
      active += 1;
      assert.equal(active, 1, 'more than one process entered the critical section');
    } else {
      active -= 1;
      assert.equal(active, 0, 'a process exited without owning the critical section');
    }
  }
  assert.equal(events.length, 10);
  assert.equal(active, 0);
  assert.equal(fs.existsSync(lockPath), false);
  assert.equal(fs.existsSync(`${lockPath}.reclaim`), false);
});
