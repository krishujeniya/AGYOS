'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const server = path.join(__dirname, '..', '..', 'mcp', 'state-server.cjs');

function rpc(input, entrypoint = server) {
  const result = spawnSync(process.execPath, [entrypoint], {
    input: typeof input === 'string' ? input : JSON.stringify(input) + '\n',
    encoding: 'utf8', timeout: 20000,
  });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout.split('\n').filter(Boolean).map(line => JSON.parse(line));
}

test('MCP parse errors have bounded, structured responses', () => {
  const out = rpc('{not-json}\n');
  assert.equal(out.length, 1);
  assert.equal(out[0].error.code, -32700);
  const oversized = rpc('{"jsonrpc":"2.0","method":"ping","id":1,"pad":"' +
    'A'.repeat(1024 * 1024 + 128) + '"}\n');
  assert.equal(oversized[0].error.code, -32600);
});

test('invalid tool inputs cannot crash or enumerate internal errors', () => {
  const requests = [
    { jsonrpc: '2.0', method: 'tools/call', id: 1 },
    { jsonrpc: '2.0', method: 'tools/call', id: 2, params: [] },
    { jsonrpc: '2.0', method: 'tools/call', id: 3, params: { name: 'agyos_memory', arguments: [] } },
    { jsonrpc: '2.0', method: 'tools/call', id: 4, params: { name: 'agyos_memory', arguments: {} } },
    { jsonrpc: '2.0', method: 'tools/call', id: 5, params: { name: 'nonexistent', arguments: {} } },
  ];
  for (const req of requests) {
    const response = rpc(req)[0];
    assert.equal(response.id, req.id);
    assert.equal(response.error.code, -32602);
  }
});

test('malformed envelopes and private memory errors do not expose file paths', () => {
  const response = rpc({
    jsonrpc: '2.0', method: 'tools/call', id: 11,
    params: {
      name: 'agyos_memory',
      arguments: { action: 'write', tier: 'tier1', key: 'secret', value: 'private' }
    }
  })[0];
  assert.equal(response.id, 11);
  assert.equal(response.result.isError, true);
  assert.match(response.result.content[0].text, /AGYOS tool failed/);
  assert.doesNotMatch(JSON.stringify(response), /node:internal|stack trace|\/home\/runner|\.agents\/state\/memory\.json/);
});

test('normal MCP initialization and tool listing remain compatible', () => {
  const init = rpc({ jsonrpc: '2.0', method: 'initialize', id: 1, params: {
    protocolVersion: '2024-11-05',
  } })[0];
  assert.equal(init.result.capabilities.tools.constructor, Object);
  const list = rpc({ jsonrpc: '2.0', method: 'tools/list', id: 2 })[0];
  assert.ok(list.result.tools.some(t => t.name === 'agyos_decision'));
  assert.ok(list.result.tools.some(t => t.name === 'agyos_memory'));
  assert.ok(list.result.tools.some(t => t.name === 'agyos_pipeline'));
  const ping = rpc({ jsonrpc: '2.0', method: 'ping', id: 'ok' })[0];
  assert.equal(ping.id, 'ok');
});

test('notification does not receive JSON-RPC response', () => {
  assert.deepEqual(rpc({ jsonrpc: '2.0', method: 'notifications/initialized' }), []);
});


test('search, decision, and pipeline reject oversized tasks without spawning Python', () => {
  for (const [name, args] of [
    ['agyos_find_skill', { query: 'x'.repeat(600) }],
    ['agyos_decision', { task: 'x'.repeat(3100) }],
    ['agyos_pipeline', { prompt: 'x'.repeat(3100) }],
  ]) {
    const result = rpc({
      jsonrpc: '2.0', method: 'tools/call', id: 77,
      params: { name, arguments: args },
    })[0];
    assert.equal(result.id, 77);
    assert.equal(result.result.isError, true);
  }
});

test('agyos_pipeline returns valid plan from MCP invocation', () => {
  const result = rpc({
    jsonrpc: '2.0', method: 'tools/call', id: 88,
    params: { name: 'agyos_pipeline', arguments: { prompt: 'optimize postgres database queries', action: 'plan' } },
  })[0];
  assert.equal(result.id, 88);
  assert.equal(result.result.isError, undefined);
  const parsed = JSON.parse(result.result.content[0].text);
  assert.equal(parsed.pod, 'pod-build');
  assert.ok(parsed.skill.name.includes('postgres') || parsed.skill.name.includes('database'));
});

const obscuraServer = path.join(__dirname, '..', '..', 'mcp', 'obscura-server.cjs');

function rpcObscura(input) {
  const result = spawnSync(process.execPath, [obscuraServer], {
    input: typeof input === 'string' ? input : JSON.stringify(input) + '\n',
    encoding: 'utf8', timeout: 20000,
  });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout.split('\n').filter(Boolean).map(line => JSON.parse(line));
}

test('Obscura MCP initialization and tool listing meet spec', () => {
  const init = rpcObscura({ jsonrpc: '2.0', method: 'initialize', id: 1, params: {
    protocolVersion: '2024-11-05',
  } })[0];
  assert.equal(init.result.serverInfo.name, 'obscura');
  const list = rpcObscura({ jsonrpc: '2.0', method: 'tools/list', id: 2 })[0];
  assert.ok(list.result.tools.some(t => t.name === 'browser_navigate'));
  assert.ok(list.result.tools.some(t => t.name === 'browser_snapshot'));
  assert.ok(list.result.tools.some(t => t.name === 'browser_click'));
  assert.ok(list.result.tools.some(t => t.name === 'browser_cdp_endpoint'));
  assert.ok(list.result.tools.some(t => t.name === 'browser_evaluate'));
  const ping = rpcObscura({ jsonrpc: '2.0', method: 'ping', id: 3 })[0];
  assert.equal(ping.id, 3);
});

test('Obscura tools handle execution headlessly and safely', () => {
  const cdp = rpcObscura({
    jsonrpc: '2.0', method: 'tools/call', id: 4,
    params: { name: 'browser_cdp_endpoint', arguments: {} }
  })[0];
  assert.equal(cdp.id, 4);
  const parsed = JSON.parse(cdp.result.content[0].text);
  assert.equal(parsed.headless, true);
  assert.equal(parsed.gui_disabled, true);
  assert.ok(parsed.endpoint_url.includes('9222'));

  const evalRes = rpcObscura({
    jsonrpc: '2.0', method: 'tools/call', id: 5,
    params: { name: 'browser_evaluate', arguments: { script: '1 + 1' } }
  })[0];
  assert.equal(evalRes.id, 5);
  const evalJson = JSON.parse(evalRes.result.content[0].text);
  assert.equal(evalJson.result, 2);
});

test('both state server entry points expose the same tools and state', () => {
  const legacy = path.join(path.dirname(server), 'agyos-state-server.cjs');
  for (const request of [
    { jsonrpc: '2.0', method: 'tools/list', id: 1 },
    { jsonrpc: '2.0', method: 'tools/call', id: 2, params: { name: 'agyos_state' } },
  ]) {
    assert.deepEqual(rpc(request, legacy), rpc(request));
  }
});
