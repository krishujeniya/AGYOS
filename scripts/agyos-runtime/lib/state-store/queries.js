'use strict';

const crypto = require('crypto');
const { assertValidEntity } = require('./schema');

const ACTIVE_SESSION_STATES = ['active', 'running', 'idle'];
const SUCCESS_OUTCOMES = new Set(['success', 'succeeded', 'passed']);
const FAILURE_OUTCOMES = new Set(['failure', 'failed', 'error']);
const CLOSED_WORK_ITEM_STATUSES = new Set(['done', 'closed', 'resolved', 'merged', 'cancelled']);
const ATTENTION_WORK_ITEM_STATUSES = new Set(['blocked', 'needs-review', 'failed', 'stalled']);

function normalizeLimit(value, fallback) {
  if (value === undefined || value === null) {
    return fallback;
  }

  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    throw new Error(`Invalid limit: ${value}`);
  }

  return parsed;
}

function parseJsonColumn(value, fallback) {
  if (value === null || value === undefined || value === '') {
    return fallback;
  }

  return JSON.parse(value);
}

function stringifyJson(value, label) {
  try {
    return JSON.stringify(value);
  } catch (error) {
    throw new Error(`Failed to serialize ${label}: ${error.message}`);
  }
}

function mapSessionRow(row) {
  const snapshot = parseJsonColumn(row.snapshot, {});
  return {
    id: row.id,
    adapterId: row.adapter_id,
    harness: row.harness,
    state: row.state,
    repoRoot: row.repo_root,
    startedAt: row.started_at,
    endedAt: row.ended_at,
    snapshot,
    workerCount: Array.isArray(snapshot && snapshot.workers) ? snapshot.workers.length : 0,
  };
}

function mapSkillRunRow(row) {
  return {
    id: row.id,
    skillId: row.skill_id,
    skillVersion: row.skill_version,
    sessionId: row.session_id,
    taskDescription: row.task_description,
    outcome: row.outcome,
    failureReason: row.failure_reason,
    tokensUsed: row.tokens_used,
    durationMs: row.duration_ms,
    userFeedback: row.user_feedback,
    createdAt: row.created_at,
  };
}

function mapSkillVersionRow(row) {
  return {
    skillId: row.skill_id,
    version: row.version,
    contentHash: row.content_hash,
    amendmentReason: row.amendment_reason,
    promotedAt: row.promoted_at,
    rolledBackAt: row.rolled_back_at,
  };
}

function mapDecisionRow(row) {
  return {
    id: row.id,
    sessionId: row.session_id,
    title: row.title,
    rationale: row.rationale,
    alternatives: parseJsonColumn(row.alternatives, []),
    supersedes: row.supersedes,
    status: row.status,
    createdAt: row.created_at,
  };
}

function mapInstallStateRow(row) {
  const modules = parseJsonColumn(row.modules, []);
  const operations = parseJsonColumn(row.operations, []);
  const status = row.source_version && row.installed_at ? 'healthy' : 'warning';

  return {
    targetId: row.target_id,
    targetRoot: row.target_root,
    profile: row.profile,
    modules,
    operations,
    installedAt: row.installed_at,
    sourceVersion: row.source_version,
    moduleCount: Array.isArray(modules) ? modules.length : 0,
    operationCount: Array.isArray(operations) ? operations.length : 0,
    status,
  };
}

function mapGovernanceEventRow(row) {
  return {
    id: row.id,
    sessionId: row.session_id,
    eventType: row.event_type,
    payload: parseJsonColumn(row.payload, null),
    resolvedAt: row.resolved_at,
    resolution: row.resolution,
    createdAt: row.created_at,
  };
}

function mapWorkItemRow(row) {
  return {
    id: row.id,
    source: row.source,
    sourceId: row.source_id,
    title: row.title,
    status: row.status,
    priority: row.priority,
    url: row.url,
    owner: row.owner,
    repoRoot: row.repo_root,
    sessionId: row.session_id,
    metadata: parseJsonColumn(row.metadata, null),
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function mapWorkspaceMilestoneRow(row) {
  if (!row) return null;
  return {
    id: row.id,
    currentGate: row.current_gate,
    revision: row.revision,
    complexityScore: row.complexity_score,
    fastPath: Boolean(row.fast_path),
    metadata: parseJsonColumn(row.metadata, {}),
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function mapWorkspaceOperationRow(row) {
  if (!row) return null;
  return {
    operationId: row.operation_id,
    milestoneId: row.milestone_id,
    revision: row.revision,
    fromGate: row.from_gate,
    toGate: row.to_gate,
    mode: row.mode,
    inputHash: row.input_hash,
    payload: parseJsonColumn(row.payload, {}),
    committedAt: row.committed_at,
  };
}

function classifyOutcome(outcome) {
  const normalized = String(outcome || '').toLowerCase();
  if (SUCCESS_OUTCOMES.has(normalized)) {
    return 'success';
  }

  if (FAILURE_OUTCOMES.has(normalized)) {
    return 'failure';
  }

  return 'unknown';
}

function classifyWorkItemStatus(status) {
  const normalized = String(status || '').toLowerCase();
  if (CLOSED_WORK_ITEM_STATUSES.has(normalized)) {
    return 'closed';
  }

  if (ATTENTION_WORK_ITEM_STATUSES.has(normalized)) {
    return 'attention';
  }

  return 'open';
}

function toPercent(numerator, denominator) {
  if (denominator === 0) {
    return null;
  }

  return Number(((numerator / denominator) * 100).toFixed(1));
}

function summarizeSkillRuns(skillRuns) {
  const summary = {
    totalCount: skillRuns.length,
    knownCount: 0,
    successCount: 0,
    failureCount: 0,
    unknownCount: 0,
    successRate: null,
    failureRate: null,
  };

  for (const skillRun of skillRuns) {
    const classification = classifyOutcome(skillRun.outcome);
    if (classification === 'success') {
      summary.successCount += 1;
      summary.knownCount += 1;
    } else if (classification === 'failure') {
      summary.failureCount += 1;
      summary.knownCount += 1;
    } else {
      summary.unknownCount += 1;
    }
  }

  summary.successRate = toPercent(summary.successCount, summary.knownCount);
  summary.failureRate = toPercent(summary.failureCount, summary.knownCount);
  return summary;
}

function summarizeInstallHealth(installations) {
  if (installations.length === 0) {
    return {
      status: 'missing',
      totalCount: 0,
      healthyCount: 0,
      warningCount: 0,
      installations: [],
    };
  }

  const summary = installations.reduce((result, installation) => {
    if (installation.status === 'healthy') {
      result.healthyCount += 1;
    } else {
      result.warningCount += 1;
    }
    return result;
  }, {
    totalCount: installations.length,
    healthyCount: 0,
    warningCount: 0,
  });

  return {
    status: summary.warningCount > 0 ? 'warning' : 'healthy',
    ...summary,
    installations,
  };
}

function summarizeWorkItems(workItems) {
  const summary = {
    totalCount: workItems.length,
    openCount: 0,
    blockedCount: 0,
    closedCount: 0,
    items: workItems,
  };

  for (const workItem of workItems) {
    const classification = classifyWorkItemStatus(workItem.status);
    if (classification === 'closed') {
      summary.closedCount += 1;
    } else if (classification === 'attention') {
      summary.openCount += 1;
      summary.blockedCount += 1;
    } else {
      summary.openCount += 1;
    }
  }

  return summary;
}

function summarizeReadiness({ activeSessionCount, skillRuns, installHealth, pendingGovernanceCount, workItems }) {
  const failedSkillRuns = skillRuns.summary.failureCount;
  const warningInstallations = installHealth.warningCount;
  const pendingGovernanceEvents = pendingGovernanceCount;
  const blockedWorkItems = workItems.blockedCount;
  const attentionCount = failedSkillRuns + warningInstallations + pendingGovernanceEvents + blockedWorkItems;

  return {
    status: attentionCount > 0 ? 'attention' : 'ok',
    attentionCount,
    activeSessions: activeSessionCount,
    failedSkillRuns,
    warningInstallations,
    pendingGovernanceEvents,
    blockedWorkItems,
  };
}

function normalizeSessionInput(session) {
  return {
    id: session.id,
    adapterId: session.adapterId,
    harness: session.harness,
    state: session.state,
    repoRoot: session.repoRoot ?? null,
    startedAt: session.startedAt ?? null,
    endedAt: session.endedAt ?? null,
    snapshot: session.snapshot ?? {},
  };
}

function normalizeSkillRunInput(skillRun) {
  return {
    id: skillRun.id,
    skillId: skillRun.skillId,
    skillVersion: skillRun.skillVersion,
    sessionId: skillRun.sessionId,
    taskDescription: skillRun.taskDescription,
    outcome: skillRun.outcome,
    failureReason: skillRun.failureReason ?? null,
    tokensUsed: skillRun.tokensUsed ?? null,
    durationMs: skillRun.durationMs ?? null,
    userFeedback: skillRun.userFeedback ?? null,
    createdAt: skillRun.createdAt || new Date().toISOString(),
  };
}

function normalizeSkillVersionInput(skillVersion) {
  return {
    skillId: skillVersion.skillId,
    version: skillVersion.version,
    contentHash: skillVersion.contentHash,
    amendmentReason: skillVersion.amendmentReason ?? null,
    promotedAt: skillVersion.promotedAt ?? null,
    rolledBackAt: skillVersion.rolledBackAt ?? null,
  };
}

function normalizeDecisionInput(decision) {
  return {
    id: decision.id,
    sessionId: decision.sessionId,
    title: decision.title,
    rationale: decision.rationale,
    alternatives: decision.alternatives === undefined || decision.alternatives === null
      ? []
      : decision.alternatives,
    supersedes: decision.supersedes ?? null,
    status: decision.status,
    createdAt: decision.createdAt || new Date().toISOString(),
  };
}

function normalizeInstallStateInput(installState) {
  return {
    targetId: installState.targetId,
    targetRoot: installState.targetRoot,
    profile: installState.profile ?? null,
    modules: installState.modules === undefined || installState.modules === null
      ? []
      : installState.modules,
    operations: installState.operations === undefined || installState.operations === null
      ? []
      : installState.operations,
    installedAt: installState.installedAt || new Date().toISOString(),
    sourceVersion: installState.sourceVersion ?? null,
  };
}

function normalizeInstallStateIdentity(identity) {
  if (!identity || typeof identity !== 'object') {
    throw new Error('Invalid installState identity: expected targetId and targetRoot');
  }

  const targetId = identity.targetId;
  const targetRoot = identity.targetRoot;
  if (typeof targetId !== 'string' || targetId.length === 0) {
    throw new Error('Invalid installState identity: targetId must be a non-empty string');
  }
  if (typeof targetRoot !== 'string' || targetRoot.length === 0) {
    throw new Error('Invalid installState identity: targetRoot must be a non-empty string');
  }

  return { targetId, targetRoot };
}

function normalizeGovernanceEventInput(governanceEvent) {
  return {
    id: governanceEvent.id,
    sessionId: governanceEvent.sessionId ?? null,
    eventType: governanceEvent.eventType,
    payload: governanceEvent.payload ?? null,
    resolvedAt: governanceEvent.resolvedAt ?? null,
    resolution: governanceEvent.resolution ?? null,
    createdAt: governanceEvent.createdAt || new Date().toISOString(),
  };
}

function normalizeWorkItemInput(workItem) {
  const now = new Date().toISOString();
  return {
    id: workItem.id,
    source: workItem.source,
    sourceId: workItem.sourceId ?? null,
    title: workItem.title,
    status: workItem.status,
    priority: workItem.priority ?? null,
    url: workItem.url ?? null,
    owner: workItem.owner ?? null,
    repoRoot: workItem.repoRoot ?? null,
    sessionId: workItem.sessionId ?? null,
    metadata: workItem.metadata ?? null,
    createdAt: workItem.createdAt || now,
    updatedAt: workItem.updatedAt || now,
  };
}

function createQueryApi(db, { prepareRead = sql => db.prepare(sql) } = {}) {
  // Only these fixed SELECTs qualify for snapshot reuse; generic SQL stays conservative.
  const listRecentSessionsStatement = prepareRead(`
    SELECT *
    FROM sessions
    ORDER BY COALESCE(started_at, ended_at, '') DESC, id DESC
    LIMIT ?
  `);
  const countSessionsStatement = prepareRead(`
    SELECT COUNT(*) AS total_count
    FROM sessions
  `);
  const getSessionStatement = prepareRead(`
    SELECT *
    FROM sessions
    WHERE id = ?
  `);
  const getSessionSkillRunsStatement = prepareRead(`
    SELECT *
    FROM skill_runs
    WHERE session_id = ?
    ORDER BY created_at DESC, id DESC
  `);
  const getSessionDecisionsStatement = prepareRead(`
    SELECT *
    FROM decisions
    WHERE session_id = ?
    ORDER BY created_at DESC, id DESC
  `);
  const listActiveSessionsStatement = prepareRead(`
    SELECT *
    FROM sessions
    WHERE ended_at IS NULL
      AND state IN ('active', 'running', 'idle')
    ORDER BY COALESCE(started_at, ended_at, '') DESC, id DESC
    LIMIT ?
  `);
  const countActiveSessionsStatement = prepareRead(`
    SELECT COUNT(*) AS total_count
    FROM sessions
    WHERE ended_at IS NULL
      AND state IN ('active', 'running', 'idle')
  `);
  const listRecentSkillRunsStatement = prepareRead(`
    SELECT *
    FROM skill_runs
    ORDER BY created_at DESC, id DESC
    LIMIT ?
  `);
  const listInstallStateStatement = prepareRead(`
    SELECT *
    FROM install_state
    ORDER BY installed_at DESC, target_id ASC
  `);
  const getInstallStateStatement = prepareRead(`
    SELECT target_id
    FROM install_state
    WHERE target_id = ? AND target_root = ?
  `);
  const countPendingGovernanceStatement = prepareRead(`
    SELECT COUNT(*) AS total_count
    FROM governance_events
    WHERE resolved_at IS NULL
  `);
  const listPendingGovernanceStatement = prepareRead(`
    SELECT *
    FROM governance_events
    WHERE resolved_at IS NULL
    ORDER BY created_at DESC, id DESC
    LIMIT ?
  `);
  const listWorkItemsStatement = prepareRead(`
    SELECT *
    FROM work_items
    ORDER BY updated_at DESC, id DESC
    LIMIT ?
  `);
  const countWorkItemsStatement = prepareRead(`
    SELECT COUNT(*) AS total_count
    FROM work_items
  `);
  const listAllWorkItemsStatement = prepareRead(`
    SELECT *
    FROM work_items
    ORDER BY updated_at DESC, id DESC
  `);
  // Read the entire native READY set in SQL instead of truncating to the
  // 100 most recently updated items before checking their eligibility.
  const nextClaimableWorkItemStatement = prepareRead(`
    SELECT *
    FROM work_items
    WHERE (owner IS NULL OR owner = '')
      AND LOWER(TRIM(COALESCE(status, ''))) IN ('open', 'ready')
    ORDER BY CASE LOWER(COALESCE(priority, ''))
      WHEN 'critical' THEN 0
      WHEN 'high' THEN 1
      WHEN 'urgent' THEN 1
      WHEN 'low' THEN 3
      ELSE 2
    END ASC, updated_at DESC, id DESC
    LIMIT 1
  `);
  const getWorkItemStatement = prepareRead(`
    SELECT *
    FROM work_items
    WHERE id = ?
  `);
  const getSkillVersionStatement = prepareRead(`
    SELECT *
    FROM skill_versions
    WHERE skill_id = ? AND version = ?
  `);

  const upsertSessionStatement = db.prepare(`
    INSERT INTO sessions (
      id,
      adapter_id,
      harness,
      state,
      repo_root,
      started_at,
      ended_at,
      snapshot
    ) VALUES (
      @id,
      @adapter_id,
      @harness,
      @state,
      @repo_root,
      @started_at,
      @ended_at,
      @snapshot
    )
    ON CONFLICT(id) DO UPDATE SET
      adapter_id = excluded.adapter_id,
      harness = excluded.harness,
      state = excluded.state,
      repo_root = excluded.repo_root,
      started_at = excluded.started_at,
      ended_at = excluded.ended_at,
      snapshot = excluded.snapshot
  `);

  const insertSkillRunStatement = db.prepare(`
    INSERT INTO skill_runs (
      id,
      skill_id,
      skill_version,
      session_id,
      task_description,
      outcome,
      failure_reason,
      tokens_used,
      duration_ms,
      user_feedback,
      created_at
    ) VALUES (
      @id,
      @skill_id,
      @skill_version,
      @session_id,
      @task_description,
      @outcome,
      @failure_reason,
      @tokens_used,
      @duration_ms,
      @user_feedback,
      @created_at
    )
    ON CONFLICT(id) DO UPDATE SET
      skill_id = excluded.skill_id,
      skill_version = excluded.skill_version,
      session_id = excluded.session_id,
      task_description = excluded.task_description,
      outcome = excluded.outcome,
      failure_reason = excluded.failure_reason,
      tokens_used = excluded.tokens_used,
      duration_ms = excluded.duration_ms,
      user_feedback = excluded.user_feedback,
      created_at = excluded.created_at
  `);

  const upsertSkillVersionStatement = db.prepare(`
    INSERT INTO skill_versions (
      skill_id,
      version,
      content_hash,
      amendment_reason,
      promoted_at,
      rolled_back_at
    ) VALUES (
      @skill_id,
      @version,
      @content_hash,
      @amendment_reason,
      @promoted_at,
      @rolled_back_at
    )
    ON CONFLICT(skill_id, version) DO UPDATE SET
      content_hash = excluded.content_hash,
      amendment_reason = excluded.amendment_reason,
      promoted_at = excluded.promoted_at,
      rolled_back_at = excluded.rolled_back_at
  `);

  const insertDecisionStatement = db.prepare(`
    INSERT INTO decisions (
      id,
      session_id,
      title,
      rationale,
      alternatives,
      supersedes,
      status,
      created_at
    ) VALUES (
      @id,
      @session_id,
      @title,
      @rationale,
      @alternatives,
      @supersedes,
      @status,
      @created_at
    )
    ON CONFLICT(id) DO UPDATE SET
      session_id = excluded.session_id,
      title = excluded.title,
      rationale = excluded.rationale,
      alternatives = excluded.alternatives,
      supersedes = excluded.supersedes,
      status = excluded.status,
      created_at = excluded.created_at
  `);

  const upsertInstallStateStatement = db.prepare(`
    INSERT INTO install_state (
      target_id,
      target_root,
      profile,
      modules,
      operations,
      installed_at,
      source_version
    ) VALUES (
      @target_id,
      @target_root,
      @profile,
      @modules,
      @operations,
      @installed_at,
      @source_version
    )
    ON CONFLICT(target_id, target_root) DO UPDATE SET
      profile = excluded.profile,
      modules = excluded.modules,
      operations = excluded.operations,
      installed_at = excluded.installed_at,
      source_version = excluded.source_version
  `);
  const deleteInstallStateStatement = db.prepare(`
    DELETE FROM install_state
    WHERE target_id = @target_id AND target_root = @target_root
  `);

  const insertGovernanceEventStatement = db.prepare(`
    INSERT INTO governance_events (
      id,
      session_id,
      event_type,
      payload,
      resolved_at,
      resolution,
      created_at
    ) VALUES (
      @id,
      @session_id,
      @event_type,
      @payload,
      @resolved_at,
      @resolution,
      @created_at
    )
    ON CONFLICT(id) DO UPDATE SET
      session_id = excluded.session_id,
      event_type = excluded.event_type,
      payload = excluded.payload,
      resolved_at = excluded.resolved_at,
      resolution = excluded.resolution,
      created_at = excluded.created_at
  `);

  const upsertWorkItemStatement = db.prepare(`
    INSERT INTO work_items (
      id,
      source,
      source_id,
      title,
      status,
      priority,
      url,
      owner,
      repo_root,
      session_id,
      metadata,
      created_at,
      updated_at
    ) VALUES (
      @id,
      @source,
      @source_id,
      @title,
      @status,
      @priority,
      @url,
      @owner,
      @repo_root,
      @session_id,
      @metadata,
      @created_at,
      @updated_at
    )
    ON CONFLICT(id) DO UPDATE SET
      source = excluded.source,
      source_id = excluded.source_id,
      title = excluded.title,
      status = excluded.status,
      priority = excluded.priority,
      url = excluded.url,
      owner = excluded.owner,
      repo_root = excluded.repo_root,
      session_id = excluded.session_id,
      metadata = excluded.metadata,
      updated_at = excluded.updated_at
  `);

  const getWorkspaceMilestoneStatement = prepareRead(`
    SELECT id, current_gate, revision, complexity_score, fast_path, metadata, created_at, updated_at
    FROM workspace_milestones
    WHERE id = ?
  `);

  const listWorkspaceMilestonesStatement = prepareRead(`
    SELECT id, current_gate, revision, complexity_score, fast_path, metadata, created_at, updated_at
    FROM workspace_milestones
    ORDER BY updated_at DESC
  `);

  const getWorkspaceOperationStatement = prepareRead(`
    SELECT operation_id, milestone_id, revision, from_gate, to_gate, mode, input_hash, payload, committed_at
    FROM workspace_operations
    WHERE operation_id = ?
  `);

  const getWorkspaceOperationsForMilestoneStatement = prepareRead(`
    SELECT operation_id, milestone_id, revision, from_gate, to_gate, mode, input_hash, payload, committed_at
    FROM workspace_operations
    WHERE milestone_id = ?
    ORDER BY revision ASC
  `);

  const upsertWorkspaceMilestoneStatement = db.prepare(`
    INSERT INTO workspace_milestones (
      id, current_gate, revision, complexity_score, fast_path, metadata, created_at, updated_at
    ) VALUES (
      @id, @current_gate, @revision, @complexity_score, @fast_path, @metadata, @created_at, @updated_at
    )
    ON CONFLICT (id) DO UPDATE SET
      current_gate = excluded.current_gate,
      revision = excluded.revision,
      complexity_score = excluded.complexity_score,
      fast_path = excluded.fast_path,
      metadata = excluded.metadata,
      updated_at = excluded.updated_at
  `);

  const insertWorkspaceOperationStatement = db.prepare(`
    INSERT INTO workspace_operations (
      operation_id, milestone_id, revision, from_gate, to_gate, mode, input_hash, payload, committed_at
    ) VALUES (
      @operation_id, @milestone_id, @revision, @from_gate, @to_gate, @mode, @input_hash, @payload, @committed_at
    )
  `);

  function getSessionById(id) {
    const row = getSessionStatement.get(id);
    return row ? mapSessionRow(row) : null;
  }

  function getWorkItemById(id) {
    const row = getWorkItemStatement.get(id);
    return row ? mapWorkItemRow(row) : null;
  }

  function listRecentSessions(options = {}) {
    const limit = normalizeLimit(options.limit, 10);
    return {
      totalCount: countSessionsStatement.get().total_count,
      sessions: listRecentSessionsStatement.all(limit).map(mapSessionRow),
    };
  }

  function getSessionDetail(id) {
    const session = getSessionById(id);
    if (!session) {
      return null;
    }

    const workers = Array.isArray(session.snapshot && session.snapshot.workers)
      ? session.snapshot.workers.map(worker => ({ ...worker }))
      : [];

    return {
      session,
      workers,
      skillRuns: getSessionSkillRunsStatement.all(id).map(mapSkillRunRow),
      decisions: getSessionDecisionsStatement.all(id).map(mapDecisionRow),
    };
  }

  function listWorkItems(options = {}) {
    const limit = normalizeLimit(options.limit, 20);
    return {
      totalCount: countWorkItemsStatement.get().total_count,
      items: listWorkItemsStatement.all(limit).map(mapWorkItemRow),
    };
  }

  function getNextClaimableWorkItem() {
    const row = nextClaimableWorkItemStatement.get();
    return row ? mapWorkItemRow(row) : null;
  }

  function getStatus(options = {}) {
    const activeLimit = normalizeLimit(options.activeLimit, 5);
    const recentSkillRunLimit = normalizeLimit(options.recentSkillRunLimit, 20);
    const pendingLimit = normalizeLimit(options.pendingLimit, 5);
    const workItemLimit = normalizeLimit(options.workItemLimit, 10);

    const activeSessions = listActiveSessionsStatement.all(activeLimit).map(mapSessionRow);
    const activeSessionCount = countActiveSessionsStatement.get().total_count;
    const recentSkillRuns = listRecentSkillRunsStatement.all(recentSkillRunLimit).map(mapSkillRunRow);
    const installations = listInstallStateStatement.all().map(mapInstallStateRow);
    const pendingGovernanceEvents = listPendingGovernanceStatement.all(pendingLimit).map(mapGovernanceEventRow);
    const workItems = summarizeWorkItems(listAllWorkItemsStatement.all().map(mapWorkItemRow));
    workItems.items = listWorkItemsStatement.all(workItemLimit).map(mapWorkItemRow);
    const skillRuns = {
      windowSize: recentSkillRunLimit,
      summary: summarizeSkillRuns(recentSkillRuns),
      recent: recentSkillRuns,
    };
    const installHealth = summarizeInstallHealth(installations);
    const pendingGovernanceCount = countPendingGovernanceStatement.get().total_count;

    return {
      generatedAt: new Date().toISOString(),
      readiness: summarizeReadiness({
        activeSessionCount,
        skillRuns,
        installHealth,
        pendingGovernanceCount,
        workItems,
      }),
      activeSessions: {
        activeCount: activeSessionCount,
        sessions: activeSessions,
      },
      skillRuns,
      installHealth,
      governance: {
        pendingCount: pendingGovernanceCount,
        events: pendingGovernanceEvents,
      },
      workItems,
    };
  }

  return {
    deleteInstallState(identity) {
      const normalized = normalizeInstallStateIdentity(identity);
      const existing = getInstallStateStatement.get(normalized.targetId, normalized.targetRoot);
      if (!existing) {
        return false;
      }
      deleteInstallStateStatement.run({
        target_id: normalized.targetId,
        target_root: normalized.targetRoot,
      });
      return true;
    },
    getSessionById,
    getSessionDetail,
    getWorkItemById,
    getStatus,
    insertDecision(decision) {
      const normalized = normalizeDecisionInput(decision);
      assertValidEntity('decision', normalized);
      insertDecisionStatement.run({
        id: normalized.id,
        session_id: normalized.sessionId,
        title: normalized.title,
        rationale: normalized.rationale,
        alternatives: stringifyJson(normalized.alternatives, 'decision.alternatives'),
        supersedes: normalized.supersedes,
        status: normalized.status,
        created_at: normalized.createdAt,
      });
      return normalized;
    },
    insertGovernanceEvent(governanceEvent) {
      const normalized = normalizeGovernanceEventInput(governanceEvent);
      assertValidEntity('governanceEvent', normalized);
      insertGovernanceEventStatement.run({
        id: normalized.id,
        session_id: normalized.sessionId,
        event_type: normalized.eventType,
        payload: stringifyJson(normalized.payload, 'governanceEvent.payload'),
        resolved_at: normalized.resolvedAt,
        resolution: normalized.resolution,
        created_at: normalized.createdAt,
      });
      return normalized;
    },
    insertSkillRun(skillRun) {
      const normalized = normalizeSkillRunInput(skillRun);
      assertValidEntity('skillRun', normalized);
      insertSkillRunStatement.run({
        id: normalized.id,
        skill_id: normalized.skillId,
        skill_version: normalized.skillVersion,
        session_id: normalized.sessionId,
        task_description: normalized.taskDescription,
        outcome: normalized.outcome,
        failure_reason: normalized.failureReason,
        tokens_used: normalized.tokensUsed,
        duration_ms: normalized.durationMs,
        user_feedback: normalized.userFeedback,
        created_at: normalized.createdAt,
      });
      return normalized;
    },
    listRecentSessions,
    listWorkItems,
    getNextClaimableWorkItem,
    upsertInstallState(installState) {
      const normalized = normalizeInstallStateInput(installState);
      assertValidEntity('installState', normalized);
      upsertInstallStateStatement.run({
        target_id: normalized.targetId,
        target_root: normalized.targetRoot,
        profile: normalized.profile,
        modules: stringifyJson(normalized.modules, 'installState.modules'),
        operations: stringifyJson(normalized.operations, 'installState.operations'),
        installed_at: normalized.installedAt,
        source_version: normalized.sourceVersion,
      });
      return normalized;
    },
    upsertWorkItem(workItem) {
      const normalized = normalizeWorkItemInput(workItem);
      assertValidEntity('workItem', normalized);
      upsertWorkItemStatement.run({
        id: normalized.id,
        source: normalized.source,
        source_id: normalized.sourceId,
        title: normalized.title,
        status: normalized.status,
        priority: normalized.priority,
        url: normalized.url,
        owner: normalized.owner,
        repo_root: normalized.repoRoot,
        session_id: normalized.sessionId,
        metadata: stringifyJson(normalized.metadata, 'workItem.metadata'),
        created_at: normalized.createdAt,
        updated_at: normalized.updatedAt,
      });
      const row = getWorkItemStatement.get(normalized.id);
      return row ? mapWorkItemRow(row) : null;
    },
    upsertSession(session) {
      const normalized = normalizeSessionInput(session);
      assertValidEntity('session', normalized);
      upsertSessionStatement.run({
        id: normalized.id,
        adapter_id: normalized.adapterId,
        harness: normalized.harness,
        state: normalized.state,
        repo_root: normalized.repoRoot,
        started_at: normalized.startedAt,
        ended_at: normalized.endedAt,
        snapshot: stringifyJson(normalized.snapshot, 'session.snapshot'),
      });
      return getSessionById(normalized.id);
    },
    upsertSkillVersion(skillVersion) {
      const normalized = normalizeSkillVersionInput(skillVersion);
      assertValidEntity('skillVersion', normalized);
      upsertSkillVersionStatement.run({
        skill_id: normalized.skillId,
        version: normalized.version,
        content_hash: normalized.contentHash,
        amendment_reason: normalized.amendmentReason,
        promoted_at: normalized.promotedAt,
        rolled_back_at: normalized.rolledBackAt,
      });
      const row = getSkillVersionStatement.get(normalized.skillId, normalized.version);
      return row ? mapSkillVersionRow(row) : null;
    },
    getWorkspaceMilestone(id) {
      const row = getWorkspaceMilestoneStatement.get(id);
      return mapWorkspaceMilestoneRow(row);
    },
    listWorkspaceMilestones() {
      return listWorkspaceMilestonesStatement.all().map(mapWorkspaceMilestoneRow);
    },
    getWorkspaceOperation(operationId) {
      const row = getWorkspaceOperationStatement.get(operationId);
      return mapWorkspaceOperationRow(row);
    },
    getWorkspaceOperationsForMilestone(milestoneId) {
      return getWorkspaceOperationsForMilestoneStatement.all(milestoneId).map(mapWorkspaceOperationRow);
    },
    transactWorkspaceGate({
      milestoneId,
      expectedRevision = null,
      operationId,
      targetGate,
      mode = 'normal',
      complexityScore = null,
      payload = {},
    }) {
      if (!milestoneId || typeof milestoneId !== 'string') {
        throw new Error('milestoneId must be a non-empty string');
      }
      if (!operationId || typeof operationId !== 'string') {
        throw new Error('operationId must be a non-empty string');
      }
      const validGates = ['IDLE', 'UNDERSTAND', 'ANALYZE', 'PLAN', 'IMPLEMENT', 'VERIFY'];
      if (!validGates.includes(targetGate)) {
        throw new Error(`Invalid target gate: '${targetGate}'`);
      }

      const inputSignature = `${milestoneId}:${targetGate}:${mode}:${JSON.stringify(payload || {})}`;
      const inputHash = crypto.createHash('sha256').update(inputSignature).digest('hex');

      const existingOpRow = getWorkspaceOperationStatement.get(operationId);
      if (existingOpRow) {
        if (existingOpRow.input_hash === inputHash && existingOpRow.to_gate === targetGate) {
          return {
            status: 'REPLAY',
            milestoneId: existingOpRow.milestone_id,
            revision: existingOpRow.revision,
            currentGate: existingOpRow.to_gate,
            operationId: existingOpRow.operation_id,
            committedAt: existingOpRow.committed_at,
          };
        }
        throw new Error(`CONFLICT: Operation ID '${operationId}' previously committed with conflicting parameters.`);
      }

      const milestoneRow = getWorkspaceMilestoneStatement.get(milestoneId);
      let currentGate = 'IDLE';
      let currentRevision = 0;
      let complexity = complexityScore !== null && complexityScore !== undefined ? complexityScore : 3;
      let fastPath = mode === 'fast' ? 1 : 0;
      let createdAt = new Date().toISOString();
      let metadata = {};

      if (!milestoneRow) {
        if (targetGate !== 'UNDERSTAND') {
          throw new Error(`INVALID_TRANSITION: New milestone '${milestoneId}' must start at UNDERSTAND (requested '${targetGate}')`);
        }
      } else {
        const milestone = mapWorkspaceMilestoneRow(milestoneRow);
        if (expectedRevision !== null && expectedRevision !== undefined && milestone.revision !== expectedRevision) {
          throw new Error(`CONFLICT: Expected revision ${expectedRevision} but found ${milestone.revision} for milestone '${milestoneId}'`);
        }
        currentGate = milestone.currentGate;
        currentRevision = milestone.revision;
        complexity = complexityScore !== null && complexityScore !== undefined ? complexityScore : milestone.complexityScore;
        fastPath = mode === 'fast' ? 1 : (milestone.fastPath ? 1 : 0);
        createdAt = milestone.createdAt;
        metadata = milestone.metadata || {};
      }

      let allowed = false;
      const transitionKey = `${currentGate}:${targetGate}:${mode}`;
      const normalAllowed = [
        'IDLE:UNDERSTAND:normal',
        'UNDERSTAND:ANALYZE:normal',
        'ANALYZE:PLAN:normal',
        'PLAN:IMPLEMENT:normal',
        'IMPLEMENT:VERIFY:normal',
        'VERIFY:IDLE:normal',
      ];
      if (normalAllowed.includes(transitionKey)) {
        allowed = true;
      } else if (transitionKey === 'ANALYZE:IMPLEMENT:fast') {
        if (typeof complexity === 'number' && complexity >= 1 && complexity <= 2) {
          allowed = true;
        } else {
          throw new Error(`INVALID_TRANSITION: Fast-path requires complexity 1 or 2 (found ${complexity})`);
        }
      }

      if (!allowed) {
        throw new Error(`INVALID_TRANSITION: Transition ${currentGate} -> ${targetGate} (${mode}) is not permitted`);
      }

      const newRevision = currentRevision + 1;
      const now = new Date().toISOString();
      const updatedMetadata = { ...metadata, ...(payload || {}), lastTransition: { from: currentGate, to: targetGate, at: now } };

      upsertWorkspaceMilestoneStatement.run({
        id: milestoneId,
        current_gate: targetGate,
        revision: newRevision,
        complexity_score: complexity,
        fast_path: fastPath,
        metadata: stringifyJson(updatedMetadata, 'workspaceMilestone.metadata'),
        created_at: createdAt,
        updated_at: now,
      });

      insertWorkspaceOperationStatement.run({
        operation_id: operationId,
        milestone_id: milestoneId,
        revision: newRevision,
        from_gate: currentGate,
        to_gate: targetGate,
        mode: mode,
        input_hash: inputHash,
        payload: stringifyJson(payload || {}, 'workspaceOperation.payload'),
        committed_at: now,
      });

      return {
        status: 'ACCEPTED',
        milestoneId,
        revision: newRevision,
        fromGate: currentGate,
        currentGate: targetGate,
        operationId,
        committedAt: now,
      };
    },
    restoreWorkspaceMilestoneRevision(milestoneId, targetRevision) {
      const ops = getWorkspaceOperationsForMilestoneStatement.all(milestoneId).map(mapWorkspaceOperationRow);
      const targetOp = ops.find(op => op.revision === targetRevision);
      if (!targetOp) {
        throw new Error(`Revision ${targetRevision} not found for milestone '${milestoneId}'`);
      }
      const now = new Date().toISOString();
      upsertWorkspaceMilestoneStatement.run({
        id: milestoneId,
        current_gate: targetOp.toGate,
        revision: targetOp.revision,
        complexity_score: 3,
        fast_path: targetOp.mode === 'fast' ? 1 : 0,
        metadata: stringifyJson({ restoredFromRevision: targetRevision, restoredAt: now }, 'metadata'),
        created_at: targetOp.committedAt,
        updated_at: now,
      });
      return mapWorkspaceMilestoneRow(getWorkspaceMilestoneStatement.get(milestoneId));
    },
  };
}

module.exports = {
  ACTIVE_SESSION_STATES,
  FAILURE_OUTCOMES,
  SUCCESS_OUTCOMES,
  createQueryApi,
};
