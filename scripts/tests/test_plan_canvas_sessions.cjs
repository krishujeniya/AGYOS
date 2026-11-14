'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { createSessionStore } = require('../agyos-runtime/lib/plan-canvas/sessions');

test('Plan Canvas feedback moves open to feedback and drains back to open', t => {
  const stateDir = fs.mkdtempSync(path.join(os.tmpdir(), 'plan-canvas-state-'));
  t.after(() => fs.rmSync(stateDir, { recursive: true, force: true }));
  const store = createSessionStore({ stateDir });
  const { session } = store.open(path.join(stateDir, 'plan.md'));
  const queued = store.queueFeedback(session.key, [{ kind: 'chat', text: 'Clarify the risk.' }]);
  assert.equal(queued.session.status, 'feedback');
  assert.equal(store.takeFeedback(session.key).items.length, 1);
  assert.equal(store.get(session.key).status, 'open');
  assert.equal(store.get(session.key).pendingFeedback.length, 0);
});

test('user-ended sessions stay ended until explicit reopen and retain attribution', t => {
  const stateDir = fs.mkdtempSync(path.join(os.tmpdir(), 'plan-canvas-state-'));
  t.after(() => fs.rmSync(stateDir, { recursive: true, force: true }));
  const store = createSessionStore({ stateDir });
  const artifact = path.join(stateDir, 'plan.md');
  const { session } = store.open(artifact);
  store.end(session.key, 'user');
  store.end(session.key, 'agent');
  assert.equal(store.get(session.key).endedBy, 'user');
  assert.equal(store.addAgentReply(session.key, 'late agent reply'), null);
  assert.deepEqual(store.get(session.key).chat, []);
  assert.equal(store.open(artifact).refused, true);
  assert.equal(store.queueFeedback(session.key, [{ kind: 'chat', text: 'late' }]), null);
  const reopened = store.open(artifact, { reopen: true });
  assert.equal(reopened.refused, false);
  assert.equal(reopened.session.status, 'open');
  assert.equal(reopened.session.endedBy, undefined);
});

test('Plan Canvas session lifecycle survives a store restart', t => {
  const stateDir = fs.mkdtempSync(path.join(os.tmpdir(), 'plan-canvas-state-'));
  t.after(() => fs.rmSync(stateDir, { recursive: true, force: true }));
  const first = createSessionStore({ stateDir });
  const { session } = first.open(path.join(stateDir, 'plan.md'));
  first.queueFeedback(session.key, [{ kind: 'chat', text: 'Persist me.' }]);
  const restarted = createSessionStore({ stateDir });
  assert.equal(restarted.get(session.key).status, 'feedback');
  assert.equal(restarted.takeFeedback(session.key).items[0].text, 'Persist me.');
});
