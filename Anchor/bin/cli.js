#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
const command = args[0];

if (command !== 'init') {
  console.log('Usage: npx anchor-agent init');
  process.exit(1);
}

const targetDir = process.cwd();
const packageDir = path.join(__dirname, '..');

console.log('⚓ Installing ANCHOR framework into current directory...');

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    const baseName = path.basename(src);
    if (baseName === 'eval_fixtures' || baseName === 'archive') {
      return;
    }
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

// Copy essential directories and files
const itemsToCopy = ['.agents', 'bin', 'dashboard', 'tests', 'AGENTS.md'];
itemsToCopy.forEach(item => {
  const src = path.join(packageDir, item);
  const dest = path.join(targetDir, item);
  if (fs.existsSync(src)) {
    copyRecursiveSync(src, dest);
    console.log(`  - Copied ${item}`);
  }
});

// Run init script
console.log('  - Running bin/init.sh...');
try {
  // Ensure scripts are executable
  execSync('chmod +x bin/*.sh', { stdio: 'inherit', cwd: targetDir });
  execSync('bash bin/init.sh', { stdio: 'inherit', cwd: targetDir });
} catch (error) {
  console.error('❌ Failed to run init.sh');
  process.exit(1);
}

console.log('✅ ANCHOR installation complete!');
