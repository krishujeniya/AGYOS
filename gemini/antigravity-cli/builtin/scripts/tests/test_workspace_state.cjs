'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { createStateStore } = require('../agyos-runtime/lib/state-store');

test('workspace state: initializes clean schema with migration 3', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-ws-state-'));
  const dbPath = path.join(dir, 'workspace-state.db');
  try {
    const store = await createStateStore({ dbPath });
    assert.deepEqual(store.getAppliedMigrations().map(m => m.version), [1, 2, 3]);
    assert.deepEqual(store.listWorkspaceMilestones(), []);
    store.close();
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('workspace state: normal transition lifecycle advances revisions monotonically', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-ws-state-'));
  const dbPath = path.join(dir, 'workspace-state.db');
  try {
    const store = await createStateStore({ dbPath });
    const mId = 'M1-lifecycle-test';

    // 1. Init at UNDERSTAND (rev 1)
    const res1 = store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-init-1',
      targetGate: 'UNDERSTAND',
      complexityScore: 3,
    });
    assert.equal(res1.status, 'ACCEPTED');
    assert.equal(res1.revision, 1);
    assert.equal(res1.currentGate, 'UNDERSTAND');

    // 2. Advance to ANALYZE (rev 2)
    const res2 = store.transactWorkspaceGate({
      milestoneId: mId,
      expectedRevision: 1,
      operationId: 'op-analyze-2',
      targetGate: 'ANALYZE',
    });
    assert.equal(res2.status, 'ACCEPTED');
    assert.equal(res2.revision, 2);
    assert.equal(res2.currentGate, 'ANALYZE');

    // 3. Advance to PLAN (rev 3)
    const res3 = store.transactWorkspaceGate({
      milestoneId: mId,
      expectedRevision: 2,
      operationId: 'op-plan-3',
      targetGate: 'PLAN',
    });
    assert.equal(res3.status, 'ACCEPTED');
    assert.equal(res3.revision, 3);
    assert.equal(res3.currentGate, 'PLAN');

    // 4. Advance to IMPLEMENT (rev 4)
    const res4 = store.transactWorkspaceGate({
      milestoneId: mId,
      expectedRevision: 3,
      operationId: 'op-impl-4',
      targetGate: 'IMPLEMENT',
    });
    assert.equal(res4.status, 'ACCEPTED');
    assert.equal(res4.revision, 4);

    // 5. Advance to VERIFY (rev 5)
    const res5 = store.transactWorkspaceGate({
      milestoneId: mId,
      expectedRevision: 4,
      operationId: 'op-verify-5',
      targetGate: 'VERIFY',
    });
    assert.equal(res5.status, 'ACCEPTED');
    assert.equal(res5.revision, 5);

    // 6. Complete to IDLE (rev 6)
    const res6 = store.transactWorkspaceGate({
      milestoneId: mId,
      expectedRevision: 5,
      operationId: 'op-idle-6',
      targetGate: 'IDLE',
    });
    assert.equal(res6.status, 'ACCEPTED');
    assert.equal(res6.revision, 6);
    assert.equal(res6.currentGate, 'IDLE');

    store.close();
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('workspace state: idempotent replay returns recorded result and rejects conflicting reuse', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-ws-state-'));
  const dbPath = path.join(dir, 'workspace-state.db');
  try {
    const store = await createStateStore({ dbPath });
    const mId = 'M1-replay-test';

    store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-replay-1',
      targetGate: 'UNDERSTAND',
      complexityScore: 3,
    });

    // Idempotent replay: exact same op-id and target gate returns REPLAY
    const replay = store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-replay-1',
      targetGate: 'UNDERSTAND',
    });
    assert.equal(replay.status, 'REPLAY');
    assert.equal(replay.revision, 1);
    assert.equal(replay.currentGate, 'UNDERSTAND');

    // Conflicting reuse: same op-id with different target gate throws CONFLICT
    assert.throws(() => {
      store.transactWorkspaceGate({
        milestoneId: mId,
        operationId: 'op-replay-1',
        targetGate: 'ANALYZE',
      });
    }, /CONFLICT/);

    store.close();
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('workspace state: rejects revision mismatch (CAS check)', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-ws-state-'));
  const dbPath = path.join(dir, 'workspace-state.db');
  try {
    const store = await createStateStore({ dbPath });
    const mId = 'M1-conflict-test';

    store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-cas-1',
      targetGate: 'UNDERSTAND',
    });

    // Revision mismatch: expected 99, current is 1
    assert.throws(() => {
      store.transactWorkspaceGate({
        milestoneId: mId,
        expectedRevision: 99,
        operationId: 'op-cas-2',
        targetGate: 'ANALYZE',
      });
    }, /CONFLICT: Expected revision 99/);

    store.close();
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('workspace state: fast-path gate transition requires complexity 1 or 2', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-ws-state-'));
  const dbPath = path.join(dir, 'workspace-state.db');
  try {
    const store = await createStateStore({ dbPath });
    const mId = 'M1-fast-test';

    store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-fast-1',
      targetGate: 'UNDERSTAND',
      complexityScore: 2,
    });
    store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-fast-2',
      targetGate: 'ANALYZE',
      complexityScore: 2,
    });

    // Fast path from ANALYZE -> IMPLEMENT with complexity 2 succeeds
    const fastRes = store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-fast-3',
      targetGate: 'IMPLEMENT',
      mode: 'fast',
      complexityScore: 2,
    });
    assert.equal(fastRes.status, 'ACCEPTED');
    assert.equal(fastRes.currentGate, 'IMPLEMENT');

    // High complexity task (4) fast path fails
    const mId2 = 'M2-fast-fail';
    store.transactWorkspaceGate({
      milestoneId: mId2,
      operationId: 'op-fail-1',
      targetGate: 'UNDERSTAND',
      complexityScore: 4,
    });
    store.transactWorkspaceGate({
      milestoneId: mId2,
      operationId: 'op-fail-2',
      targetGate: 'ANALYZE',
      complexityScore: 4,
    });
    assert.throws(() => {
      store.transactWorkspaceGate({
        milestoneId: mId2,
        operationId: 'op-fail-3',
        targetGate: 'IMPLEMENT',
        mode: 'fast',
        complexityScore: 4,
      });
    }, /INVALID_TRANSITION: Fast-path requires complexity 1 or 2/);

    store.close();
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('workspace state: restore returns milestone to prior revision', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-ws-state-'));
  const dbPath = path.join(dir, 'workspace-state.db');
  try {
    const store = await createStateStore({ dbPath });
    const mId = 'M1-restore-test';

    store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-res-1',
      targetGate: 'UNDERSTAND',
    });
    store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-res-2',
      targetGate: 'ANALYZE',
    });
    store.transactWorkspaceGate({
      milestoneId: mId,
      operationId: 'op-res-3',
      targetGate: 'PLAN',
    });

    const active = store.getWorkspaceMilestone(mId);
    assert.equal(active.revision, 3);
    assert.equal(active.currentGate, 'PLAN');

    // Restore to revision 1 (UNDERSTAND)
    const restored = store.restoreWorkspaceMilestoneRevision(mId, 1);
    assert.equal(restored.revision, 1);
    assert.equal(restored.currentGate, 'UNDERSTAND');

    store.close();
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});
