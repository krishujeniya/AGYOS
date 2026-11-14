'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { createHookContextScanner } = require('../agyos-runtime/hooks/hook-input-limits');
const { STATES, classifyWorktree } = require('../agyos-runtime/lib/worktree-lifecycle/lifecycle');
const {
  appendAcknowledgement,
  createShadowTrail,
  summarizeShadowTrail,
  verifyShadowTrail,
} = require('../agyos-runtime/lib/agent-proximity/shadow-trail');

test('hook input parser retains explicit top-level context across chunks', () => {
  const scanner = createHookContextScanner();
  scanner.push('{"hook_event_name":"PostTool');
  scanner.push('Use","tool_name":"Bash","stop_hook_active":true,"tool_input":{"tool_name":"ignored"}}');
  assert.deepEqual(scanner.context, {
    hookEventName: 'PostToolUse',
    toolName: 'Bash',
    stopHookActive: true,
  });
});

test('worktree classification protects dirty work and identifies stale unmerged work', () => {
  const common = { isMain: false, branch: 'feature', detached: false, aheadBehind: { ahead: 1, behind: 0 }, conflict: false, lastCommitMs: 1000 };
  assert.equal(classifyWorktree({ ...common, dirty: true }, { staleThresholdMs: 100, nowMs: 5000 }), STATES.DIRTY);
  assert.equal(classifyWorktree({ ...common, dirty: false }, { staleThresholdMs: 100, nowMs: 5000 }), STATES.STALE);
  assert.equal(classifyWorktree({ ...common, dirty: false, aheadBehind: { ahead: 0, behind: 0 } }, { staleThresholdMs: 100, nowMs: 5000 }), STATES.MERGED);
});

test('shadow trail enforces advisory acknowledgement transitions', () => {
  const at = '2026-11-12T00:00:01.000Z';
  const observation = agentId => ({
    agentId,
    taskId: 'task-1',
    repoId: 'repo-1',
    baseRevision: 'a'.repeat(40),
    scopeRevision: 1,
    footprint: 'complete',
    readPaths: [],
    writePaths: ['src/main.ts'],
    observedAt: '2026-11-12T00:00:00.000Z',
    expiresAt: '2026-11-12T01:00:00.000Z',
  });
  const trail = createShadowTrail({
    trailId: 'trail-1',
    at,
    observations: [observation('agent-a'), observation('agent-b')],
  });
  assert.equal(summarizeShadowTrail(trail).latestAdvisory.state, 'advisory');
  const acknowledged = appendAcknowledgement(trail, {
    id: 'ack-1', agentId: 'agent-a', scopeRevision: 1,
    at: '2026-11-12T00:00:02.000Z',
  });
  assert.equal(verifyShadowTrail(acknowledged), true);
  assert.deepEqual(summarizeShadowTrail(acknowledged).latestAdvisoryAcknowledgedBy, ['agent-a']);
  assert.throws(() => appendAcknowledgement(acknowledged, {
    id: 'ack-2', agentId: 'agent-a', scopeRevision: 1,
    at: '2026-11-12T00:00:03.000Z',
  }), /Invalid shadow coordination input/);
});
