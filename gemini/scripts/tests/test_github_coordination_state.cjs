'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { applyClaim } = require('../agyos-runtime/lib/github-coordination/actions');
const {
  assertIssueClaimable,
  buildIssueStateFromAction,
  defaultCoordinationState,
} = require('../agyos-runtime/lib/github-coordination/state');

function fixture() {
  const issue = { number: 17, body: '', labels: [], author: { login: 'operator' } };
  return { issue, state: defaultCoordinationState(issue) };
}

test('coordination action accepts the declared publish transition', () => {
  const { issue, state } = fixture();
  const validated = {
    ...state,
    status: 'validated',
    validation: 'passed',
    review: 'approved',
    project: { state: 'ready', fields: {} },
  };
  const published = buildIssueStateFromAction(issue, validated, 'publish', {
    status: 'published',
    validation: 'passed',
    review: 'approved',
    projectState: 'done',
  });
  assert.equal(published.status, 'published');
  assert.equal(published.validation, 'passed');
  assert.equal(published.review, 'approved');
  assert.equal(published.project.state, 'done');
});

test('claiming requires an open, claimable issue and leaves dependency decisions explicit', () => {
  const { issue, state } = fixture();
  assert.doesNotThrow(() => assertIssueClaimable({ ...issue, state: 'open' }, state));
  for (const status of ['claimed', 'validated', 'blocked', 'published']) {
    assert.throws(
      () => assertIssueClaimable({ ...issue, state: 'open' }, { ...state, status }),
      /cannot be claimed from coordination status/,
    );
  }
  assert.throws(
    () => assertIssueClaimable({ ...issue, state: 'closed' }, state),
    /is not open/,
  );
  assert.throws(
    () => assertIssueClaimable({ ...issue, state: 'open' }, { ...state, validation: 'failed' }),
    /cannot be claimed while a coordination axis/,
  );
  assert.throws(
    () => assertIssueClaimable({ ...issue, state: 'open' }, { ...state, project: { ...state.project, state: 'blocked' } }),
    /cannot be claimed while a coordination axis/,
  );
});

test('review requests, approvals, and changes requested follow their matching lifecycle axes', () => {
  const { issue, state } = fixture();
  const claimed = { ...state, status: 'claimed', project: { state: 'in-progress', fields: {} } };
  const requested = buildIssueStateFromAction(issue, claimed, 'review', {
    status: 'claimed', review: 'requested', projectState: 'in-progress',
  });
  assert.equal(requested.review, 'requested');
  const approved = buildIssueStateFromAction(issue, claimed, 'review', {
    status: 'ready', review: 'approved', projectState: 'ready',
  });
  assert.equal(approved.status, 'ready');
  const changesRequested = buildIssueStateFromAction(issue, claimed, 'review', {
    status: 'blocked', review: 'changes-requested', projectState: 'blocked',
  });
  assert.equal(changesRequested.project.state, 'blocked');
  const stillBlocked = buildIssueStateFromAction(issue, {
    ...state, status: 'blocked', project: { state: 'blocked', fields: {} },
  }, 'validate', { status: 'blocked', validation: 'passed', projectState: 'ready' });
  assert.equal(stillBlocked.status, 'blocked');
});

test('claim action refuses open dependencies before writing to GitHub', t => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'github-claim-state-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const body = [
    '<!-- ecc-coordination:start -->',
    '```json',
    JSON.stringify({
      kind: 'epic', status: 'available', owner: 'operator', branch: null,
      validation: 'pending', review: 'not-requested',
      project: { state: 'backlog', fields: {} }, dependencies: [3], tasks: [], labels: [],
    }),
    '```',
    '<!-- ecc-coordination:end -->',
  ].join('\n');
  const issue = {
    number: 17, title: 'Epic', body, url: 'https://github.com/acme/app/issues/17', state: 'open',
    labels: [], author: { login: 'operator' }, assignees: [],
  };
  const logPath = path.join(root, 'gh.log');
  const shimPath = path.join(root, 'gh-shim.cjs');
  fs.writeFileSync(shimPath, [
    "const fs=require('fs');",
    'const args=process.argv.slice(2);',
    "fs.appendFileSync(process.env.GH_SHIM_LOG, args[0]+' '+args[1]+'\\n');",
    `if (args[0]==='issue' && args[1]==='view') process.stdout.write(${JSON.stringify(JSON.stringify(issue))});`,
    "else if (args[0]==='issue' && args[1]==='list') process.stdout.write('[{\"number\":3,\"state\":\"open\",\"labels\":[],\"body\":\"\"}]');",
    "else process.exit(0);",
  ].join('\n'));
  const oldShim = process.env.ECC_GH_SHIM;
  const oldLog = process.env.GH_SHIM_LOG;
  process.env.ECC_GH_SHIM = shimPath;
  process.env.GH_SHIM_LOG = logPath;
  t.after(() => {
    if (oldShim === undefined) delete process.env.ECC_GH_SHIM;
    else process.env.ECC_GH_SHIM = oldShim;
    if (oldLog === undefined) delete process.env.GH_SHIM_LOG;
    else process.env.GH_SHIM_LOG = oldLog;
  });

  assert.throws(
    () => applyClaim('acme/app', 17, {}, {
      rootDir: root,
      store: { dbPath: path.join(root, 'state.db') },
    }),
    /cannot be claimed until dependencies close: 3/,
  );
  const commands = fs.readFileSync(logPath, 'utf8');
  assert.match(commands, /issue view/);
  assert.match(commands, /issue list/);
  assert.doesNotMatch(commands, /issue edit|issue comment/);
  const digest = crypto.createHash('sha256').update('acme/app#17').digest('hex');
  assert.equal(fs.existsSync(`${path.join(root, 'state.db')}.claim-${digest}.lock`), false);
});

test('coordination actions reject unknown states and illegal status transitions', () => {
  const { issue, state } = fixture();
  assert.throws(
    () => buildIssueStateFromAction(issue, state, 'claim', { status: 'mystery' }),
    /Invalid coordination status/,
  );
  assert.throws(
    () => buildIssueStateFromAction(issue, state, 'sync', { status: 'published' }),
    /Invalid coordination status transition/,
  );
  assert.throws(
    () => buildIssueStateFromAction(issue, state, 'review', { review: 'maybe' }),
    /Invalid review state/,
  );
  assert.throws(
    () => buildIssueStateFromAction(issue, { ...state, status: 'blocked' }, 'claim', { status: 'claimed' }),
    /Invalid coordination status transition/,
  );
  assert.throws(
    () => buildIssueStateFromAction(issue, { ...state, status: 'blocked' }, 'decompose', { status: 'claimed' }),
    /Invalid coordination status transition/,
  );
  assert.throws(
    () => buildIssueStateFromAction(issue, state, 'publish', { status: 'published' }),
    /Invalid coordination status transition/,
  );
  assert.throws(
    () => buildIssueStateFromAction(issue, state, 'publish', {
      status: 'published', validation: 'passed', review: 'approved', projectState: 'done',
    }),
    /Invalid coordination status transition/,
  );
  assert.throws(
    () => buildIssueStateFromAction(issue, { ...state, status: 'blocked' }, 'review', {
      status: 'ready', review: 'approved', projectState: 'ready',
    }),
    /Invalid coordination status transition/,
  );
});

test('published coordination state cannot be reopened by a later action', () => {
  const { issue, state } = fixture();
  const publishedState = { ...state, status: 'published' };
  assert.throws(
    () => buildIssueStateFromAction(issue, publishedState, 'claim', { status: 'claimed' }),
    /Published epic state is terminal/,
  );
  assert.throws(
    () => buildIssueStateFromAction(issue, {
      ...publishedState, validation: 'passed', review: 'approved', project: { state: 'done', fields: {} },
    }, 'sync', { validation: 'failed' }),
    /status axes are terminal/,
  );
});
