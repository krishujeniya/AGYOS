'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {
  SESSION_END_ACTIONS,
  SESSION_SUMMARY_OUTCOMES,
  resolveSessionEndState,
} = require('../agyos-runtime/lib/session-end-state');

test('session end has explicit skip, create, and update actions', () => {
  assert.deepEqual(SESSION_END_ACTIONS, ['skip', 'create', 'update']);
  assert.deepEqual(SESSION_SUMMARY_OUTCOMES, ['empty', 'mechanical', 'llm']);
  assert.deepEqual(resolveSessionEndState({ internalSummarySubprocess: true }), {
    action: 'skip', summaryOutcome: 'empty'
  });
  assert.deepEqual(resolveSessionEndState({ sessionFileExists: false, summary: {} }), {
    action: 'create', summaryOutcome: 'mechanical'
  });
  assert.deepEqual(resolveSessionEndState({ sessionFileExists: true, summary: {}, llmSummary: 'summary' }), {
    action: 'update', summaryOutcome: 'llm'
  });
});
