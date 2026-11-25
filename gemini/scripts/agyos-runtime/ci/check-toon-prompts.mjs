import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { existsSync, lstatSync, readFileSync, readlinkSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { decode, encode } from '@toon-format/toon'

// Reference spec revision 009074d934289553a61763d70c50ee5160e60110.
const geminiPrefix = existsSync('gemini/skills/agyos-scout') ? 'gemini/' : ''
const directory = `${geminiPrefix}skills/agyos-scout`
const source = readFileSync(directory + '/prompt.toon', 'utf8')
const manifest = decode(readFileSync(directory + '/SKILL.toon', 'utf8'), { strict: true })
const prompt = decode(source, { strict: true })
assert.equal(prompt.skill, 'agyos-scout')
assert.equal(prompt.steps.length, 4)
assert.equal(prompt.output.maximum_tokens, 1000)
assert.deepEqual(decode(encode(prompt)), prompt)
assert.ok(manifest.header.includes('\nprompt-source: prompt.toon\n'))
assert.equal(execFileSync('bash', [`${geminiPrefix}bin/agyos`, 'skill', prompt.skill], {encoding: 'utf8'}), source)

const toonManifests = execFileSync('git', ['ls-files', '-z', '--', `${geminiPrefix}skills/*/SKILL.toon`, `${geminiPrefix}skills/*/SKILL.md.toon`], { encoding: 'utf8', maxBuffer: 8 << 20 }).split('\0').filter(Boolean)
const sources = new Set(execFileSync('git', ['ls-files', '-z', '--', `${geminiPrefix}skills/*/prompt.toon`], { encoding: 'utf8' }).split('\0').filter(Boolean))
assert.equal(sources.size, toonManifests.length, 'Each manifest needs a tracked source')
let unavailable = 0
for (const file of toonManifests) {
  assert.equal(existsSync(file.replace(/SKILL(?:\.md)?\.toon$/, 'SKILL.md')), false, `Unexpected SKILL.md for ${file}`)
  const recordManifest = decode(readFileSync(file, 'utf8'), { strict: true })
  assert.ok(typeof recordManifest.header === 'string' && recordManifest.header.includes('\nprompt-source: prompt.toon'), file)
  const sourceFile = file.replace(/SKILL(?:\.md)?\.toon$/, 'prompt.toon')
  assert.ok(sources.has(sourceFile), file)
  const text = readFileSync(sourceFile, 'utf8')
  const record = decode(text, { strict: true })
  assert.equal(record.skill, file.split('/').at(-2), file)
  assert.deepEqual(decode(encode(record)), record, file)
  if (record.status === 'unavailable') {
    assert.deepEqual(Object.keys(record).sort(), ['instruction', 'skill', 'status'], file)
    assert.match(record.instruction, /no operational instructions or tools/, file)
    unavailable++
  } else {
    assert.ok(Object.values(record).some(value => Array.isArray(value) && value.length), file)
  }
}
console.log(`Validated ${toonManifests.length} TOON skill prompts, including ${unavailable} unavailable records.`)

const allToon = execFileSync('git', ['ls-files', '-z', '--', ':(icase)*.toon'], {
  encoding: 'utf8', maxBuffer: 8 << 20
}).split('\0').filter(Boolean)
const skillPrefixes = [
  'gemini/skills/', 'gemini/skill-sources/', 'gemini/agents/', 'gemini/rules/',
  'gemini/workflows/', 'gemini/plugins/', 'gemini/tools/video/', 'gemini/integrations/chopify/',
  'skills/', 'skill-sources/', 'agents/', 'rules/', 'workflows/', 'plugins/',
  'tools/video/', 'integrations/chopify/',
]
const documents = allToon.filter(doc => {
  if (skillPrefixes.some(prefix => doc.startsWith(prefix))) return false
  try {
    const head = readFileSync(doc, 'utf8').slice(0, 50)
    return /^mode: "(100644|100755|120000)"/.test(head)
  } catch {
    return false
  }
})
assert.ok(documents.length > 0, 'Expected tracked TOON document sources')
const counts = { text: 0, header: 0, target: 0, archive: 0 }
for (const document of documents) {
  const record = decode(readFileSync(document, 'utf8'), { strict: true })
  const fields = Object.keys(record).filter(field => field !== 'mode')
  assert.equal(fields.length, 1, document)
  const [kind] = fields
  assert.ok(Object.hasOwn(counts, kind), document)
  assert.equal(typeof record[kind], 'string', document)
  counts[kind]++
  const output = document.endsWith('.md.toon')
    ? document.slice(0, -'.toon'.length)
    : document.slice(0, -'.toon'.length) + '.md'
  if (kind === 'target') {
    assert.equal(record.mode, '120000', document)
    assert.equal(readlinkSync(output), record.target, document)
    continue
  }
  assert.ok(['100644', '100755'].includes(record.mode), document)
  if (kind === 'archive') {
    assert.equal(Buffer.from(record.archive, 'base64').toString('base64'), record.archive, document)
    continue
  }
  const expected = kind === 'header'
    ? record.header + readFileSync(join(dirname(output), 'prompt.toon'), 'utf8')
    : record.text
  const status = lstatSync(output)
  assert.ok(status.isFile(), document)
  assert.equal(status.mode & 0o111, record.mode === '100755' ? 0o111 : 0, document)
  assert.ok(readFileSync(output).equals(Buffer.from(expected)), document)
}
console.log(`Validated ${documents.length} non-skill tracked document sources: ${JSON.stringify(counts)}`)
