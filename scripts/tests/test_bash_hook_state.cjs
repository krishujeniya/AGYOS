'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { runHooks } = require('../agyos-runtime/hooks/bash-hook-dispatcher');
const { runHooks: runPostToolHooks } = require('../agyos-runtime/hooks/posttooluse-dispatcher');

const enabledEnv = { ECC_HOOKS_ENABLED: 'true', ECC_HOOK_PROFILE: 'standard' };

test('Bash hook dispatcher records skips and successful continuation', () => {
  const result = runHooks('input', [
    { id: 'hook:disabled', profiles: 'standard', run: () => 'unreachable' },
    { id: 'hook:run', profiles: 'standard', run: () => ({ stdout: 'changed' }) },
  ], { ...enabledEnv, ECC_DISABLED_HOOKS: 'hook:disabled' });
  assert.deepEqual(result.outcomes, [
    { id: 'hook:disabled', outcome: 'skipped' },
    { id: 'hook:run', outcome: 'continued' },
  ]);
  assert.equal(result.output, 'changed');
});

test('Bash hook dispatcher stops after an explicit nonzero hook result', () => {
  let laterHookRan = false;
  const result = runHooks('input', [
    { id: 'hook:block', profiles: 'standard', run: () => ({ exitCode: 2, stderr: 'blocked' }) },
    { id: 'hook:later', profiles: 'standard', run: () => { laterHookRan = true; return 'later'; } },
  ], enabledEnv);
  assert.equal(result.exitCode, 2);
  assert.equal(laterHookRan, false);
  assert.deepEqual(result.outcomes, [{ id: 'hook:block', outcome: 'stopped', exitCode: 2 }]);
});

test('Bash hook exceptions are recorded as fail-open and dispatch continues', () => {
  const result = runHooks('input', [
    { id: 'hook:error', profiles: 'standard', run: () => { throw new Error('fixture failure'); } },
    { id: 'hook:after', profiles: 'standard', run: () => 'ok' },
  ], enabledEnv);
  assert.deepEqual(result.outcomes, [
    { id: 'hook:error', outcome: 'failed', policy: 'continue' },
    { id: 'hook:after', outcome: 'continued' },
  ]);
  assert.match(result.stderr, /fixture failure/);
  assert.equal(result.output, 'ok');
});

test('PostToolUse dispatcher records skipped, failed, and continued outcomes', () => {
  let laterHookRan = false;
  const result = runPostToolHooks(JSON.stringify({ tool_name: 'Edit' }), [
    { id: 'post:skip', matcher: 'Write', profiles: 'standard', run: () => ({ stdout: 'skip' }) },
    { id: 'post:fail', matcher: 'Edit', profiles: 'standard', run: () => ({ exitCode: 3 }) },
    { id: 'post:continue', matcher: 'Edit', profiles: 'standard', run: () => { laterHookRan = true; return { stdout: 'ok' }; } },
  ], { env: enabledEnv, toolName: 'Edit' });
  assert.deepEqual(result.outcomes, [
    { id: 'post:skip', outcome: 'skipped' },
    { id: 'post:fail', outcome: 'failed', policy: 'continue', exitCode: 3 },
    { id: 'post:continue', outcome: 'continued' },
  ]);
  assert.equal(result.exitCode, 3);
  assert.equal(laterHookRan, true);
});
