#!/usr/bin/env node
'use strict';

/**
 * bin/workspace-state.cjs
 * AGYOS workspace state and gate transition transaction CLI.
 * Enforces transaction revision numbers, idempotency replay,
 * conflict rejection, and projection synchronization.
 */

const fs = require('fs');
const path = require('path');
const { createStateStore } = require('../builtin/scripts/agyos-runtime/lib/state-store');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const DEFAULT_DB_PATH = path.join(PROJECT_ROOT, 'state', 'workspace-state.db');
const DEFAULT_STATE_FILE = path.join(PROJECT_ROOT, 'state', 'state.json');
const DEFAULT_CURRENT_FILE = path.join(PROJECT_ROOT, 'state', 'CURRENT.md');

function parseArgs(args) {
  const parsed = {
    command: args[0] || 'status',
    db: DEFAULT_DB_PATH,
    stateFile: DEFAULT_STATE_FILE,
    currentFile: DEFAULT_CURRENT_FILE,
    milestoneId: null,
    gate: null,
    opId: null,
    revision: null,
    mode: 'normal',
    complexity: 3,
    project: false,
    json: false,
  };

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--db' && args[i + 1]) parsed.db = path.resolve(args[++i]);
    else if ((arg === '--state-file' || arg === '--out') && args[i + 1]) parsed.stateFile = path.resolve(args[++i]);
    else if (arg === '--current-file' && args[i + 1]) parsed.currentFile = path.resolve(args[++i]);
    else if ((arg === '--milestone' || arg === '--milestone-id') && args[i + 1]) parsed.milestoneId = args[++i];
    else if ((arg === '--gate' || arg === '--target-gate' || arg === '--transition') && args[i + 1]) {
      const g = args[++i];
      parsed.gate = g.includes('->') ? g.split('->')[1] : g;
    }
    else if ((arg === '--op' || arg === '--op-id' || arg === '--operation-id') && args[i + 1]) parsed.opId = args[++i];
    else if ((arg === '--revision' || arg === '--expected-revision') && args[i + 1]) parsed.revision = parseInt(args[++i], 10);
    else if (arg === '--mode' && args[i + 1]) parsed.mode = args[++i];
    else if (arg === '--complexity' && args[i + 1]) parsed.complexity = parseInt(args[++i], 10);
    else if (arg === '--project') parsed.project = true;
    else if (arg === '--json') parsed.json = true;
  }

  return parsed;
}

function projectWorkspaceState(milestone, stateFile, currentFile) {
  if (!milestone) return;
  fs.mkdirSync(path.dirname(stateFile), { recursive: true });

  const stateJson = {
    project: 'AGYOS',
    current_milestone: milestone.id,
    current_gate: milestone.currentGate,
    revision: milestone.revision,
    complexity_score: milestone.complexityScore,
    source_revision: milestone.revision,
    last_updated: milestone.updatedAt,
  };
  fs.writeFileSync(stateFile, JSON.stringify(stateJson, null, 2) + '\n');

  const currentMd = [
    `# AGYOS Current Status`,
    ``,
    `- **Active Milestone**: ${milestone.id}`,
    `- **Current Gate**: ${milestone.currentGate}`,
    `- **Revision**: ${milestone.revision}`,
    `- **Last Updated**: ${milestone.updatedAt}`,
    ``,
  ].join('\n');
  fs.writeFileSync(currentFile, currentMd);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const store = await createStateStore({ dbPath: options.db });

  try {
    switch (options.command) {
      case 'status': {
        const milestones = store.listWorkspaceMilestones();
        const active = milestones[0] || null;
        const result = {
          status: active ? 'ACTIVE' : 'UNINITIALIZED',
          dbPath: options.db,
          activeMilestone: active,
          totalMilestones: milestones.length,
        };
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case 'transact': {
        if (!options.milestoneId || !options.gate || !options.opId) {
          console.error('Error: transact requires --milestone, --gate, and --op');
          process.exit(1);
        }

        const result = store.transactWorkspaceGate({
          milestoneId: options.milestoneId,
          expectedRevision: options.revision,
          operationId: options.opId,
          targetGate: options.gate,
          mode: options.mode,
          complexityScore: options.complexity,
        });

        if (options.project) {
          const milestone = store.getWorkspaceMilestone(options.milestoneId);
          projectWorkspaceState(milestone, options.stateFile, options.currentFile);
        }

        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case 'import-legacy': {
        if (!fs.existsSync(options.stateFile)) {
          console.error(`Error: legacy state file not found at ${options.stateFile}`);
          process.exit(1);
        }
        const legacyData = JSON.parse(fs.readFileSync(options.stateFile, 'utf8'));
        const milestoneId = legacyData.current_milestone || 'M0-legacy';
        const currentGate = legacyData.current_gate || 'IDLE';

        // Check if already imported
        const existing = store.getWorkspaceMilestone(milestoneId);
        if (existing) {
          console.log(JSON.stringify({ status: 'ALREADY_EXISTS', milestone: existing }, null, 2));
          break;
        }

        const opId = `import-legacy-${Date.now()}`;
        // Bootstrap at UNDERSTAND, then advance to currentGate
        let milestone = null;
        if (currentGate === 'IDLE') {
          // Empty initial
          console.log(JSON.stringify({ status: 'IDLE_NOTHING_TO_IMPORT' }, null, 2));
          break;
        }

        store.transactWorkspaceGate({
          milestoneId,
          operationId: `${opId}-init`,
          targetGate: 'UNDERSTAND',
          complexityScore: legacyData.complexity_score || 3,
        });

        const intermediateGates = ['ANALYZE', 'PLAN', 'IMPLEMENT', 'VERIFY'];
        const targetIdx = intermediateGates.indexOf(currentGate);
        if (targetIdx >= 0) {
          for (let i = 0; i <= targetIdx; i++) {
            store.transactWorkspaceGate({
              milestoneId,
              operationId: `${opId}-${intermediateGates[i].toLowerCase()}`,
              targetGate: intermediateGates[i],
              complexityScore: legacyData.complexity_score || 3,
            });
          }
        }

        milestone = store.getWorkspaceMilestone(milestoneId);
        projectWorkspaceState(milestone, options.stateFile, options.currentFile);
        console.log(JSON.stringify({ status: 'IMPORTED', milestone }, null, 2));
        break;
      }

      case 'project': {
        let active = null;
        if (options.milestoneId) {
          active = store.getWorkspaceMilestone(options.milestoneId);
        } else {
          const milestones = store.listWorkspaceMilestones();
          active = milestones[0] || null;
        }
        if (active) {
          projectWorkspaceState(active, options.stateFile, options.currentFile);
          console.log(JSON.stringify({ status: 'PROJECTED', milestone: active }, null, 2));
        } else {
          console.log(JSON.stringify({ status: 'UNINITIALIZED' }, null, 2));
        }
        break;
      }

      case 'restore': {
        if (!options.milestoneId || options.revision === null) {
          console.error('Error: restore requires --milestone and --revision');
          process.exit(1);
        }
        const restored = store.restoreWorkspaceMilestoneRevision(options.milestoneId, options.revision);
        if (options.project) {
          projectWorkspaceState(restored, options.stateFile, options.currentFile);
        }
        console.log(JSON.stringify({ status: 'RESTORED', milestone: restored }, null, 2));
        break;
      }

      default:
        console.error(`Unknown command: ${options.command}`);
        process.exit(1);
    }
  } finally {
    store.close();
  }
}

if (require.main === module) {
  main().catch(err => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  });
}

module.exports = { parseArgs, projectWorkspaceState };
