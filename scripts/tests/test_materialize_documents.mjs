import assert from 'node:assert/strict'
import { mkdtempSync, chmodSync, mkdirSync, readFileSync, readlinkSync, rmSync, statSync, symlinkSync, writeFileSync, existsSync } from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import test from 'node:test'
import { materialize } from '../materialize-documents.mjs'

function fixture(t) {
  const root = mkdtempSync(path.join(os.tmpdir(), 'agyos-documents-'))
  t.after(() => rmSync(root, { recursive: true, force: true }))
  return root
}

function record(file, key, value, mode = '100644') {
  writeFileSync(file + '.toon', 'mode: "' + mode + '"\n' + key + ': ' + JSON.stringify(value) + '\n')
}

test('preserves bytes, executable bit, skill metadata and the native policy link', t => {
  const root = fixture(t)
  const policy = path.join(root, 'AGENTS.md')
  const header = '---\r\nname: example\r\n---\r\n'
  const prompt = 'skill: example\n'
  record(policy, 'text', '\ufeffexample\r\nsecond line', '100755')
  record(path.join(root, 'GEMINI.md'), 'target', 'AGENTS.md', '120000')
  record(path.join(root, 'SKILL.md'), 'header', header)
  writeFileSync(path.join(root, 'prompt.toon'), prompt)
  record(path.join(root, 'archived.md'), 'archive', 'historical fixture')
  assert.deepEqual(materialize(root), { count: 3, changes: 3 })
  assert.equal(readFileSync(policy, 'utf8'), '\ufeffexample\r\nsecond line')
  assert.equal(statSync(policy).mode & 0o777, 0o755)
  assert.equal(readFileSync(path.join(root, 'SKILL.md'), 'utf8'), header + prompt)
  assert.equal(readlinkSync(path.join(root, 'GEMINI.md')), 'AGENTS.md')
  assert.equal(existsSync(path.join(root, 'archived.md')), false)
  assert.deepEqual(materialize(root), { count: 3, changes: 0 })
})

test('updates unchanged outputs and protects local edits and permissions', t => {
  const root = fixture(t)
  const file = path.join(root, 'README.md')
  record(file, 'text', 'one')
  materialize(root)
  record(file, 'text', 'two')
  materialize(root)
  assert.equal(readFileSync(file, 'utf8'), 'two')
  writeFileSync(file, 'local')
  assert.throws(() => materialize(root), /Preserve modified/)
  assert.equal(readFileSync(file, 'utf8'), 'local')
  writeFileSync(file, 'two')
  chmodSync(file, 0o755)
  assert.throws(() => materialize(root), /Preserve modified/)
  chmodSync(file, 0o644)
  rmSync(file + '.toon')
  materialize(root)
  assert.equal(existsSync(file), false)
})

test('rejects indirect prompt sources and existing output links', t => {
  const root = fixture(t)
  const other = fixture(t)
  const file = path.join(root, 'SKILL.md')
  writeFileSync(path.join(other, 'private'), 'sensitive')
  symlinkSync(path.join(other, 'private'), path.join(root, 'prompt.toon'))
  record(file, 'header', '---\nname: example\n---\n')
  assert.throws(() => materialize(root))
  assert.equal(existsSync(file), false)
  record(file, 'text', 'permitted')
  symlinkSync(path.join(other, 'private'), file)
  assert.throws(() => materialize(root), /Preserve modified/)
  assert.equal(readFileSync(path.join(other, 'private'), 'utf8'), 'sensitive')
  mkdirSync(path.join(root, 'other'))
  record(path.join(root, 'other', 'link.md'), 'target', '../../outside', '120000')
  assert.throws(() => materialize(root))
})
