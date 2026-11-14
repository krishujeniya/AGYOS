'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {
  applyMultiHarnessPlan,
  GUIDED_INSTALL_STATUSES,
} = require('../agyos-runtime/lib/multi-harness-setup');

test('guided install distinguishes preview from applied work', async () => {
  const result = await applyMultiHarnessPlan({
    request: { dryRun: true, harnesses: ['claude', 'codex'] },
    harnesses: [],
  });
  assert.equal(result.status, 'preview');
  assert.deepEqual(result.retryHarnesses, ['claude', 'codex']);
  assert.equal(GUIDED_INSTALL_STATUSES.has(result.status), true);
});

test('guided install reports completed work and only retries unfinished harnesses', async () => {
  const result = await applyMultiHarnessPlan({
    request: { dryRun: false, harnesses: ['claude', 'codex', 'kimi'] },
    harnesses: [{ id: 'claude' }, { id: 'codex' }, { id: 'kimi' }],
  }, {
    applyClaude: async () => ({ configured: true }),
    applyCodex: async () => { throw new Error('fixture failure'); },
  });
  assert.equal(result.status, 'partial');
  assert.deepEqual(result.completed.map(item => item.id), ['claude']);
  assert.deepEqual(result.retryHarnesses, ['codex', 'kimi']);
  assert.equal(GUIDED_INSTALL_STATUSES.has(result.status), true);
});

test('guided install reports failure when the first operation fails', async () => {
  const result = await applyMultiHarnessPlan({
    request: { dryRun: false, harnesses: ['claude'] },
    harnesses: [{ id: 'claude' }],
  }, {
    applyClaude: async () => { throw new Error('fixture failure'); },
  });
  assert.equal(result.status, 'failed');
  assert.deepEqual(result.retryHarnesses, ['claude']);
});
