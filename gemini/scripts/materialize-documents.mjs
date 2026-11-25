// Restore AGY host files from the two-field TOON document format used by this repository.
import { createHash, randomUUID } from 'node:crypto'
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

const stateName = '.agyos-documents-state.json'
const excluded = new Set(['.git', 'OLD', 'node_modules', '.venv', '__pycache__'])
const sourcePattern = /\.toon$/i
const skillSourcePrefixes = [
  'gemini/skills/', 'gemini/skill-sources/', 'gemini/agents/', 'gemini/rules/',
  'gemini/workflows/', 'gemini/plugins/', 'gemini/tools/video/', 'gemini/integrations/chopify/',
  'skills/', 'skill-sources/', 'agents/', 'rules/', 'workflows/', 'plugins/',
  'tools/video/', 'integrations/chopify/', '.agents/',
]
const utf8 = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true })

export function targetRelative(source) {
  if (source.endsWith('.md.toon')) return source.slice(0, -'.toon'.length)
  if (source.endsWith('.toon')) return source.slice(0, -'.toon'.length) + '.md'
  return source
}

function isSkillSource(source) {
  const normalized = source.replace(/\\/g, '/')
  return skillSourcePrefixes.some(prefix => normalized.startsWith(prefix))
}

function sources(root) {
  if (fs.existsSync(path.join(root, '.git'))) {
    const names = execFileSync('git', ['ls-files', '-z'], { cwd: root, maxBuffer: 32 << 20 })
    return utf8.decode(names).split('\0').filter(name => sourcePattern.test(name) && !isSkillSource(name))
  }
  function walk(directory) {
    return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
      const filename = path.join(directory, entry.name)
      if (entry.isDirectory() && !excluded.has(entry.name)) return walk(filename)
      if (entry.isFile() && sourcePattern.test(entry.name)) {
        const rel = path.relative(root, filename)
        return isSkillSource(rel) ? [] : [rel]
      }
      return []
    })
  }
  return walk(root)
}

function safePath(root, relative) {
  const parts = relative.split(/[\\/]/)
  if (parts.some(p => !p || p === '.' || p === '..' || excluded.has(p)) || path.isAbsolute(relative)) {
    throw new Error(`Unsafe document path: ${relative}`)
  }
  const filename = path.join(root, relative)
  // Reject symlinked ancestors, including aliases that resolve back inside the tree.
  if (fs.realpathSync(path.dirname(filename)) !== path.dirname(filename)) {
    throw new Error(`Indirect document path: ${relative}`)
  }
  return filename
}

function readRegular(filename) {
  if (!fs.lstatSync(filename).isFile()) throw new Error(`Expected a regular file: ${filename}`)
  const fd = fs.openSync(filename, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0) | (fs.constants.O_NONBLOCK || 0))
  try {
    if (!fs.fstatSync(fd).isFile() || fs.lstatSync(filename).isSymbolicLink()) {
      throw new Error(`Expected a regular file: ${filename}`)
    }
    return fs.readFileSync(fd)
  } finally {
    fs.closeSync(fd)
  }
}

function document(root, source, relative) {
  const filename = safePath(root, source)
  const input = utf8.decode(readRegular(filename))
  const fields = /^mode: "(100644|100755|120000)"\r?\n(text|header|target|archive): ("[^\r\n]*")\r?\n?$/.exec(input)
  if (!fields || fields[0].length !== input.length) return null
  const [, mode, field, encoded] = fields
  const value = JSON.parse(encoded)
  if (field === 'archive') return null
  if ((mode === '120000') !== (field === 'target')) throw new Error(`Invalid target mode: ${source}`)
  if (field === 'target' && (path.basename(relative) !== 'GEMINI.md' || value !== 'AGENTS.md')) {
    throw new Error(`Unsupported document symlink: ${source}`)
  }
  let bytes = Buffer.from(value)
  if (field === 'header') {
    const base = path.basename(source)
    if ((base !== 'SKILL.toon' && base !== 'SKILL.md.toon') || !/^---\r?\n[\s\S]*?\r?\n---\r?\n$/.test(value)) {
      throw new Error(`Invalid discovery header: ${source}`)
    }
    bytes = Buffer.concat([bytes, readRegular(path.join(path.dirname(filename), 'prompt.toon'))])
  }
  return { mode, bytes }
}

function signature(mode, bytes) {
  return mode + ':' + createHash('sha256').update(bytes).digest('hex')
}

function current(filename) {
  const stat = fs.lstatSync(filename, { throwIfNoEntry: false })
  if (!stat) return null
  if (stat.isSymbolicLink()) return signature('120000', fs.readlinkSync(filename, { encoding: 'buffer' }))
  if (!stat.isFile()) throw new Error(`Expected a document: ${filename}`)
  return signature(stat.mode & 0o111 ? '100755' : '100644', readRegular(filename))
}

function replace(filename, mode, bytes, before) {
  const temporary = path.join(path.dirname(filename), '.agyos-document-' + randomUUID())
  try {
    if (mode === '120000') fs.symlinkSync(bytes.toString(), temporary)
    else {
      fs.writeFileSync(temporary, bytes, { flag: 'wx', mode: 0o600 })
      fs.chmodSync(temporary, mode === '100755' ? 0o755 : 0o644)
    }
    if (current(filename) !== before) throw new Error(`Document changed during installation: ${filename}`)
    if (before === null) fs.linkSync(temporary, filename)
    else fs.renameSync(temporary, filename)
  } finally {
    fs.rmSync(temporary, { force: true })
  }
}

export function materialize(root = process.cwd()) {
  root = fs.realpathSync(root)
  const statePath = path.join(root, stateName)
  const previousState = current(statePath)
  const previous = new Map(previousState === null ? [] : JSON.parse(readRegular(statePath)))
  const next = new Map()
  let changes = 0
  for (const source of sources(root).sort()) {
    const relative = targetRelative(source)
    const doc = document(root, source, relative)
    if (!doc) continue
    const filename = safePath(root, relative)
    const expected = signature(doc.mode, doc.bytes)
    const before = current(filename)
    // An unchanged source leaves local edits in place. Retain its original
    // digest so a later source update detects the three-way conflict.
    const locallyEdited = before !== null && !before.startsWith('120000:') &&
      doc.mode !== '120000' && previous.get(relative) === expected
    if (before !== expected && !locallyEdited) {
      if (before !== null && before !== previous.get(relative)) throw new Error(`Preserve modified document: ${relative}`)
      replace(filename, doc.mode, doc.bytes, before)
      changes++
    }
    next.set(relative, expected)
  }
  for (const [relative, digest] of previous) {
    if (next.has(relative)) continue
    if (!/\.md$/i.test(relative)) throw new Error(`Invalid state entry: ${relative}`)
    const filename = path.resolve(root, relative)
    if (!fs.existsSync(path.dirname(filename))) continue
    safePath(root, relative)
    const before = current(filename)
    if (before === null) continue
    if (before !== digest) throw new Error(`Preserve modified retired document: ${relative}`)
    fs.unlinkSync(filename)
    changes++
  }
  const state = Buffer.from(JSON.stringify([...next]) + '\n')
  if (previousState !== signature('100644', state)) replace(statePath, '100644', state, previousState)
  return { count: next.size, changes }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  try {
    const result = materialize()
    console.log(`Materialized ${result.count} documents (${result.changes} changed).`)
  } catch (error) {
    console.error(error.message)
    process.exitCode = 1
  }
}
