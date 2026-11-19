import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { decode, encode } from '@toon-format/toon'

// Reference spec revision 009074d934289553a61763d70c50ee5160e60110.
const directory = '.agents/skills/agyos-scout'
const source = readFileSync(directory + '/prompt.toon', 'utf8')
const manifest = readFileSync(directory + '/SKILL.md', 'utf8')
const prompt = decode(source, { strict: true })
assert.equal(prompt.skill, 'agyos-scout')
assert.equal(prompt.steps.length, 4)
assert.equal(prompt.output.maximum_tokens, 1000)
assert.deepEqual(decode(encode(prompt)), prompt)
assert.equal(manifest.slice(manifest.indexOf('\n---\n', 4) + 5), source)
assert.equal(execFileSync('bash', ['bin/agyos', 'skill', prompt.skill], {encoding: 'utf8'}), source)

const files = execFileSync('git', ['ls-files', '-z', '--', '.agents/skills/*/SKILL.md'], { encoding: 'utf8', maxBuffer: 8 << 20 }).split('\0').filter(Boolean)
const sources = new Set(execFileSync('git', ['ls-files', '-z', '--', '.agents/skills/*/prompt.toon'], { encoding: 'utf8' }).split('\0').filter(Boolean))
assert.equal(sources.size, files.length, 'Each manifest needs a tracked source')
let unavailable = 0
for (const file of files) {
  const host = readFileSync(file, 'utf8')
  const end = host.indexOf('\n---\n', 4)
  assert.ok(end >= 0 && host.slice(0, end).includes('\nprompt-source: prompt.toon'), file)
  const sourceFile = file.replace(/SKILL\.md$/, 'prompt.toon')
  assert.ok(sources.has(sourceFile), file)
  const text = readFileSync(sourceFile, 'utf8')
  assert.equal(host.slice(end + 5), text, file)
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
console.log(`Validated ${files.length} skill prompts, including ${unavailable} unavailable records.`)
