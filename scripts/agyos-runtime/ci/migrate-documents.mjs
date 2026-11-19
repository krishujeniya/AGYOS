// One-time conversion. The Actions artifact is published only after every
// candidate has been decoded with the pinned reference implementation.
import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, readFileSync, readlinkSync, writeFileSync } from 'node:fs'
import path from 'node:path'
import { decode } from '@toon-format/toon'

const ledger = []
const entries = execFileSync('git', ['ls-files', '--stage', '-z'], {encoding: 'utf8', maxBuffer: 64 << 20}).split('\0').filter(Boolean)
for (const entry of entries) {
  const [metadata, file] = entry.split('\t')
  if (!/\.md$/i.test(file)) continue
  const [mode, oid] = metadata.split(' ')
  const link = mode === '120000'
  const original = link ? Buffer.from(readlinkSync(file)) : readFileSync(file)
  const hash = createHash('sha1').update(`blob ${original.length}\0`).update(original).digest('hex')
  assert.equal(hash, oid, file)
  let key = link ? 'target' : 'text'
  let value = original.toString('utf8')
  assert.ok(Buffer.from(value).equals(original), file)
  const companion = path.join(path.dirname(file), 'prompt.toon')
  let body = ''
  if (path.basename(file) === 'SKILL.md' && existsSync(companion)) {
    body = readFileSync(companion, 'utf8')
    assert.ok(body.length && value.endsWith(body), file)
    key = 'header'
    value = value.slice(0, -body.length)
  } else if (/^tools\/(security|strix)\//.test(file) ||
      (/^\.agents\/skills\//.test(file) && file.split('/').length > 4 &&
       existsSync(`.agents/skills/${file.split('/')[2]}/prompt.toon`) &&
       /^status: unavailable$/m.test(readFileSync(`.agents/skills/${file.split('/')[2]}/prompt.toon`, 'utf8')))) {
    key = 'archive'
    value = original.toString('base64')
  }
  const destination = file + '.toon'
  assert.ok(!existsSync(destination), destination)
  const record = `mode: ${JSON.stringify(mode)}\n${key}: ${JSON.stringify(value)}\n`
  writeFileSync(destination, record, {flag: 'wx'})
  const parsed = decode(readFileSync(destination, 'utf8'), {strict: true})
  assert.equal(parsed.mode, mode)
  const recovered = key === 'archive' ? Buffer.from(parsed.archive, 'base64') : Buffer.from(parsed[key] + body)
  assert.ok(recovered.equals(original), file)
  ledger.push({file, destination, mode, oid, kind: key})
}
assert.ok(ledger.length > 0)
writeFileSync(process.env.RUNNER_TEMP + '/conversion.json', JSON.stringify(ledger, null, 2))
console.log(`Verified ${ledger.length} TOON documents against their original Git blobs and modes.`)
