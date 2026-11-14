'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {
  claimWorkItem,
  moveWorkItem,
  validateWorkItemStatus,
} = require('../agyos-runtime/lib/control-pane/work-item-mutations');
const {
  buildUpsertPayload,
  closeStaleGithubItems,
  isGithubListingComplete,
  isLocallyManagedGithubItem,
  validateCloseStatus,
} = require('../agyos-runtime/work-items');

function fakeStore(item) {
  return {
    item: { ...item },
    writes: 0,
    getWorkItemById(id) {
      return this.item.id === id ? this.item : null;
    },
    getNextClaimableWorkItem() {
      return this.item;
    },
    upsertWorkItem(next) {
      this.writes += 1;
      this.item = { ...next };
      return this.item;
    },
  };
}

test('work-item statuses use the declared vocabulary', () => {
  assert.equal(validateWorkItemStatus(' NEEDS-REVIEW '), 'needs-review');
  assert.throws(() => validateWorkItemStatus('waiting-forever'), /Invalid work-item status/);
  assert.throws(
    () => buildUpsertPayload({ id: 'task-3', title: 'Task', status: 'waiting-forever' }),
    /Invalid work-item status/,
  );
});

test('claim only moves an eligible work item into an active lane', () => {
  const store = fakeStore({ id: 'task-1', status: 'open', owner: null, metadata: {} });
  assert.throws(
    () => claimWorkItem(store, { id: 'task-1', owner: 'agent-1', status: 'done' }),
    /must be an active status/,
  );
  assert.equal(store.writes, 0);

  const result = claimWorkItem(store, { id: 'task-1', owner: 'agent-1' });
  assert.equal(result.item.status, 'running');
  assert.equal(result.item.owner, 'agent-1');
});

test('terminal work items cannot be reopened through a lane move', () => {
  const store = fakeStore({ id: 'task-2', status: 'done', owner: null });
  assert.throws(() => moveWorkItem(store, { id: 'task-2', lane: 'ready' }), /is terminal/);
  assert.equal(store.writes, 0);
  assert.equal(store.item.status, 'done');
});

test('terminal work-item upserts reject active-status overrides', () => {
  const existing = { id: 'task-3', title: 'Finished task', status: 'done' };
  assert.throws(
    () => buildUpsertPayload({ id: 'task-3', title: 'Finished task', status: 'open' }, existing),
    /is terminal.*cannot return to active status/,
  );
  assert.throws(() => validateCloseStatus('open'), /close status 'open' must be terminal/);
  assert.equal(validateCloseStatus('closed'), 'closed');
  assert.equal(
    buildUpsertPayload({ id: 'task-3', title: 'Finished task', status: 'closed' }, existing).status,
    'closed',
  );
});

test('GitHub sync skips stale closure when an API listing may be truncated', () => {
  assert.equal(isGithubListingComplete([{}], [{}], 2), true);
  assert.equal(isGithubListingComplete([{}, {}], [{}], 2), false);
  assert.equal(isGithubListingComplete([{}], [{}, {}], 2), false);
});

test('stale GitHub sync closure preserves locally changed work items', () => {
  const syncState = {
    status: 'open', owner: null, sessionId: null, priority: 'normal', repoRoot: '/repo'
  };
  const remoteItem = {
    id: 'remote', status: 'open', owner: null, sessionId: null,
    priority: 'normal', repoRoot: '/repo',
    metadata: {
      repo: 'owner/repo', syncedBy: 'ecc-work-items-sync-github',
      githubSync: { state: { ...syncState }, managedLocally: false }
    }
  };
  const localItem = {
    ...remoteItem,
    id: 'local',
    status: 'blocked',
    metadata: { ...remoteItem.metadata, githubSync: { state: { ...syncState }, managedLocally: false } }
  };
  assert.equal(isLocallyManagedGithubItem(localItem), true);
  const store = {
    items: [remoteItem, localItem],
    listWorkItems() { return { items: this.items }; },
    upsertWorkItem(next) {
      const index = this.items.findIndex(item => item.id === next.id);
      this.items[index] = next;
      return next;
    }
  };
  const closed = closeStaleGithubItems(store, 'owner/repo', new Set());
  assert.deepEqual(closed.map(item => item.id), ['remote']);
  assert.equal(store.items.find(item => item.id === 'local').status, 'blocked');
});
