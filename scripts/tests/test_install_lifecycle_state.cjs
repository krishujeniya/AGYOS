'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {
  INSTALL_LIFECYCLE_STATUSES,
  assertLifecycleResultStatuses,
} = require('../agyos-runtime/lib/install-lifecycle');
const {
  AUTO_UPDATE_STATUSES,
  assertAutoUpdateResultStatuses,
} = require('../agyos-runtime/auto-update');

test('repair lifecycle result states are declared and checked', () => {
  assert.deepEqual(INSTALL_LIFECYCLE_STATUSES.repair, ['planned', 'repaired', 'ok', 'error']);
  assert.equal(assertLifecycleResultStatuses([{ status: 'planned' }, { status: 'repaired' }], 'repair').length, 2);
  assert.throws(
    () => assertLifecycleResultStatuses([{ status: 'uninstalled' }], 'repair'),
    /Invalid repair result status/,
  );
});

test('uninstall lifecycle keeps partial cleanup distinct from success', () => {
  assert.equal(INSTALL_LIFECYCLE_STATUSES.uninstall.includes('partial'), true);
  assert.equal(INSTALL_LIFECYCLE_STATUSES.uninstall.includes('uninstalled'), true);
  assert.throws(
    () => assertLifecycleResultStatuses([{ status: 'repaired' }], 'uninstall'),
    /Invalid uninstall result status/,
  );
});

test('auto-update result states distinguish dry-run, update, and failure', () => {
  assert.deepEqual(AUTO_UPDATE_STATUSES, ['planned', 'updated', 'error']);
  assert.equal(assertAutoUpdateResultStatuses([{ status: 'planned' }, { status: 'updated' }]).length, 2);
  assert.throws(
    () => assertAutoUpdateResultStatuses([{ status: 'repaired' }]),
    /Invalid auto-update result status/,
  );
});
