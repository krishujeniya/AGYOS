'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { parseDecisionRegister } = require('../agyos-runtime/release-approval-gate');

test('release decision register accepts only declared decision states', () => {
  const decisions = parseDecisionRegister([
    '| Decision | State | Evidence | Owner |',
    '| --- | --- | --- | --- |',
    '| Billing | approved | receipt | owner |',
    '| Preview | waiting-on-me | pending | owner |',
  ].join('\n'));
  assert.equal(decisions.get('billing'), 'approved');
  assert.equal(decisions.get('preview'), 'invalid:waiting-on-me');
});

test('conflicting duplicate release decisions fail closed', () => {
  const decisions = parseDecisionRegister([
    '| Decision | State | Evidence | Owner |',
    '| Billing | approved | receipt | owner |',
    '| Billing | blocked | reason | owner |',
  ].join('\n'));
  assert.equal(decisions.get('billing'), 'conflict:approved|blocked');
});
