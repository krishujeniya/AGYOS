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
