#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const secure = require('./lib/e2ee.cjs');
const HELP = [
  'AGYOS endpoint-side encrypted file exchange',
  'Commands:',
  '  bin/agyos secure keygen [--identity PATH] --passphrase-fd 0',
  '  bin/agyos secure public [--identity PATH] --out FILE',
  '  bin/agyos secure encrypt [--identity PATH] --recipient PUB --in FILE --out FILE --passphrase-fd 0',
  '  bin/agyos secure decrypt [--identity PATH] --sender PUB --in FILE --out FILE --passphrase-fd 0',
  'Passphrases must be supplied by a private file descriptor/pipe.',
  'Verify fingerprints outside the transfer channel. No remote model or memory E2EE is implied.',
].join('\n');
function parse(argv) {
  const [op, ...args] = argv;
  if (op === 'help' || op === '--help' || !op) return { op: 'help' };
  const allowed = {
    keygen: ['identity', 'passphrase-fd'],
    public: ['identity', 'out'],
    encrypt: ['identity', 'recipient', 'in', 'out', 'passphrase-fd'],
    decrypt: ['identity', 'sender', 'in', 'out', 'passphrase-fd'],
  };
  if (!allowed[op]) throw new Error('Unsupported secure operation');
  const flags = {};
  for (let i = 0; i < args.length; i += 2) {
    const flag = args[i];
    const key = typeof flag === 'string' && flag.startsWith('--') ? flag.slice(2) : '';
    if (!allowed[op].includes(key) || Object.hasOwn(flags, key) ||
        !args[i + 1] || args[i + 1].startsWith('--'))
      throw new Error('Invalid or duplicate secure option');
    flags[key] = args[i + 1];
  }
  if (op !== 'keygen' && !flags.out) throw new Error('--out is required');
  if (['encrypt', 'decrypt'].includes(op) &&
      (!flags.in || !(op === 'encrypt' ? flags.recipient : flags.sender)))
    throw new Error('An input and trusted public identity are required');
  if (op !== 'public' && !Object.hasOwn(flags, 'passphrase-fd'))
    throw new Error('--passphrase-fd is required');
  return { op, flags };
}
function passphrase(fdRaw) {
  if (!/^[0-9]$/.test(fdRaw)) throw new Error('Passphrase FD must be 0..9');
  const buf = fs.readFileSync(Number(fdRaw));
  if (buf.length > 4096) throw new Error('Passphrase input exceeds limit');
  const value = buf.toString('utf8').replace(/\r?\n$/, '');
  buf.fill(0);
  return value;
}
function run(argv) {
  const { op, flags } = parse(argv);
  if (op === 'help') return console.log(HELP);
  const identityPath = path.resolve(flags.identity || secure.defaultIdentityPath());
  const repo = path.resolve(__dirname, '..', '..');
  if (op === 'keygen') {
    if (identityPath === repo || identityPath.startsWith(repo + path.sep))
      throw new Error('Private keys must be outside the AGYOS repository');
    const pub = secure.createIdentityFile(identityPath, passphrase(flags['passphrase-fd']));
    return console.log(JSON.stringify({ status: 'created', fingerprint: pub.fingerprint }));
  }
  if (op === 'public') {
    const pub = secure.readIdentityFile(identityPath).public;
    secure.validatePublic(pub);
    secure.writeNewFile(path.resolve(flags.out), JSON.stringify(pub, null, 2) + '\n', 0o644);
    return console.log(JSON.stringify({ status: 'exported', fingerprint: pub.fingerprint }));
  }
  const identity = secure.unlockIdentity(secure.readIdentityFile(identityPath),
    passphrase(flags['passphrase-fd']));
  if (op === 'encrypt') {
    const recipient = secure.readPublicFile(path.resolve(flags.recipient));
    const plain = secure.readRegularFile(path.resolve(flags.in), secure.MAX_PLAINTEXT);
    const envelope = secure.encryptBytes(identity, recipient, plain);
    plain.fill(0);
    secure.writeNewFile(path.resolve(flags.out), JSON.stringify(envelope, null, 2) + '\n');
    return console.log(JSON.stringify({ status: 'encrypted', recipient: recipient.fingerprint }));
  }
  const sender = secure.readPublicFile(path.resolve(flags.sender));
  const envelope = JSON.parse(secure.readRegularFile(path.resolve(flags.in)).toString('utf8'));
  const plain = secure.decryptBytes(identity, sender, envelope);
  secure.writeNewFile(path.resolve(flags.out), plain);
  plain.fill(0);
  return console.log(JSON.stringify({ status: 'decrypted', sender: sender.fingerprint }));
}
if (require.main === module) {
  try { run(process.argv.slice(2)); }
  catch (error) {
    console.error('AGYOS secure: ' + error.message);
    process.exitCode = 1;
  }
}
module.exports = { run, parse };
