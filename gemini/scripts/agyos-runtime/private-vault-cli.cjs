#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vault = require('./lib/private-vault.cjs');
function run(argv) {
  const [action, ...flags] = argv;
  if (!action || action === 'help' || action === '--help') {
    console.log([
      'AGYOS encrypted local-memory vault management',
      '  bin/agyos secure vault-init --passphrase-fd 0 [--path ABSOLUTE_PATH]',
      '  bin/agyos secure vault-status [--path ABSOLUTE_PATH]',
      'MCP memory writes are encrypted only after vault-init.',
      'MCP unlock requires AGYOS_VAULT_PASSPHRASE_FD=3 with inherited private FD 3.',
      'The private vault lives outside the AGYOS Git repository.',
    ].join('\n'));
    return;
  }
  if (!['vault-init', 'vault-status'].includes(action)) throw new Error('Unsupported vault operation');
  const opts = {};
  for (let i = 0; i < flags.length; i += 2) {
    const flag = flags[i], value = flags[i + 1];
    if (!['--path', '--passphrase-fd'].includes(flag) || !value ||
        Object.hasOwn(opts, flag)) throw new Error('Invalid vault option');
    opts[flag] = value;
  }
  const file = vault.assertVaultPath(path.resolve(opts['--path'] || vault.vaultPath()));
  if (action === 'vault-status') {
    if (opts['--passphrase-fd']) throw new Error('vault-status does not accept passphrase');
    console.log(JSON.stringify({ initialized: vault.isInitialized(file), path: file }));
    return;
  }
  if (opts['--passphrase-fd'] !== '0') throw new Error('vault-init requires --passphrase-fd 0');
  const input = fs.readFileSync(0);
  if (input.length > 4096) throw new Error('Passphrase input exceeds 4096 bytes');
  const secret = input.toString('utf8').replace(/\r?\n$/, '');
  input.fill(0);
  vault.initializeVault(file, secret);
  console.log(JSON.stringify({ initialized: true, path: file }));
}
if (require.main === module) {
  try { run(process.argv.slice(2)); }
  catch (error) {
    console.error('AGYOS private vault: ' + error.message);
    process.exitCode = 1;
  }
}
module.exports = { run };
