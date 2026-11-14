'use strict';

const SESSION_END_ACTIONS = Object.freeze(['skip', 'create', 'update']);
const SESSION_SUMMARY_OUTCOMES = Object.freeze(['empty', 'mechanical', 'llm']);

function resolveSessionEndState({ internalSummarySubprocess = false, sessionFileExists = false, summary = null, llmSummary = null } = {}) {
  const action = internalSummarySubprocess ? 'skip' : sessionFileExists ? 'update' : 'create';
  const summaryOutcome = llmSummary ? 'llm' : summary ? 'mechanical' : 'empty';
  return { action, summaryOutcome };
}

module.exports = {
  SESSION_END_ACTIONS,
  SESSION_SUMMARY_OUTCOMES,
  resolveSessionEndState,
};
