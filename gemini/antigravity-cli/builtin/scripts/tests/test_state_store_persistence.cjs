'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { createStateStore } = require('../agyos-runtime/lib/state-store');

test('state store migrates a clean database and persists work items across reopen', async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'agyos-state-store-'));
  const dbPath = path.join(directory, 'state.db');
  try {
    const first = await createStateStore({ dbPath });
    assert.deepEqual(first.getAppliedMigrations().map(item => item.version), [1, 2, 3]);
    first.upsertWorkItem({
      id: 'task-persist-1',
      source: 'agyos-task',
      title: 'Persist task lifecycle state',
      status: 'ready',
      metadata: { lifecycleVersion: 1, attempt: 0 },
    });
    first.close();

    const reopened = await createStateStore({ dbPath });
    assert.deepEqual(reopened.getAppliedMigrations().map(item => item.version), [1, 2, 3]);
    assert.deepEqual(reopened.getWorkItemById('task-persist-1').metadata, {
      lifecycleVersion: 1,
      attempt: 0,
    });
    reopened.close();
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});
