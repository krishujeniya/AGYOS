"""AGYOS Decision Engine: Fast, non-autoregressive System 1 decision engine with calibrated probabilities."""

__version__ = "3.1.0"

# Routing, language detection, email, contracts, and adapters are resolved lazily
# so that importing specific submodules (such as `skills_router`) does not pay
# the eager import cost of jsonschema, dataclasses, torch, or external frameworks.
_LAZY_ATTRS = {
    # Submodules
    "BillingFinanceAdapter": (".company_adapters", "BillingFinanceAdapter"),
    "CRMAdapter": (".company_adapters", "CRMAdapter"),
    "HelpdeskAdapter": (".company_adapters", "HelpdeskAdapter"),
    "HiringScreenAdapter": (".company_adapters", "HiringScreenAdapter"),
    "LegalAuditAdapter": (".company_adapters", "LegalAuditAdapter"),
    "Approval": (".contracts", "Approval"),
    "Budget": (".contracts", "Budget"),
    "Compensation": (".contracts", "Compensation"),
    "Postconditions": (".contracts", "Postconditions"),
    "TaskContract": (".contracts", "TaskContract"),
    "TaskResult": (".contracts", "TaskResult"),
    "validate_contract": (".contracts", "validate_contract"),
    "clean_email_body": (".email", "clean_email_body"),
    "email_state": (".email", "email_state"),
    "ClarificationDecision": (".evpi_clarify", "ClarificationDecision"),
    "evaluate_evpi": (".evpi_clarify", "evaluate_evpi"),
    "BaseHook": (".hooks", "BaseHook"),
    "Hook": (".hooks", "Hook"),
    "PredictContext": (".hooks", "PredictContext"),
    "PredictHook": (".hooks", "PredictHook"),
    "FUNCTION_TO_POD": (".intent_compiler", "FUNCTION_TO_POD"),
    "compile_intent": (".intent_compiler", "compile_intent"),
    "detect_language": (".lang", "analyse"),
    "detect_script": (".lang", "detect_script"),
    "is_english": (".lang", "is_english"),
    "email_questions": (".presets", "email_questions"),
    "guard_questions": (".presets", "guard_questions"),
    "moderation_questions": (".presets", "moderation_questions"),
    "router_questions": (".presets", "router_questions"),
    "triage_questions": (".presets", "triage_questions"),
    "DEFAULT_MODELS": (".router", "DEFAULT_MODELS"),
    "RouteDecision": (".router", "RouteDecision"),
    "Router": (".router", "Router"),
    "assess_complexity": (".skills_router", "assess_complexity"),
    "classify_domain": (".skills_router", "classify_domain"),
    "decide_skill": (".skills_router", "decide_skill"),
    "select_best_skills": (".skills_router", "select_best_skills"),
    "DAGTaskGraph": (".state_ledger", "DAGTaskGraph"),
    "HierarchyCapError": (".state_ledger", "HierarchyCapError"),
    "OutboxQueue": (".state_ledger", "OutboxQueue"),
    "ReflectionMemory": (".state_ledger", "ReflectionMemory"),
    "RunBudgetTracker": (".state_ledger", "RunBudgetTracker"),
    "SagaCoordinator": (".state_ledger", "SagaCoordinator"),
    "SnapshotManager": (".state_ledger", "SnapshotManager"),
    "DecisionResult": (".structured", "DecisionResult"),
    "decide": (".structured", "decide"),
    "Agent": (".agent", "Agent"),
    "RLAgent": (".agent", "RLAgent"),
    "load": (".agent", "load"),
    "proper_reward": (".common", "proper_reward"),
    "td_lambda_targets": (".common", "td_lambda_targets"),
    "ece_score": (".common", "ece_score"),
    "answer_confidence": (".common", "answer_confidence"),
    "confidence_from_probs": (".common", "confidence_from_probs"),
    "render_options": (".common", "render_options"),
    "QTYPES": (".common", "QTYPES"),
    "QTYPE_NAMES": (".common", "QTYPE_NAMES"),
    "shortlist_choice": (".shortlist", "shortlist_choice"),
    "predict_shortlist": (".shortlist", "predict_shortlist"),
    "embed_fn_from_agent": (".shortlist", "embed_fn_from_agent"),
    "RoxxRouter": (".integrations", "RoxxRouter"),
    "RoxxGuardrail": (".integrations", "RoxxGuardrail"),
    "RoxxGuardrailError": (".integrations", "RoxxGuardrailError"),
    "RoxxTriage": (".integrations", "RoxxTriage"),
    "RoxxEvaluator": (".integrations", "RoxxEvaluator"),
    "LayaRouter": (".integrations", "RoxxRouter"),
    "LayaGuardrail": (".integrations", "RoxxGuardrail"),
    "LayaGuardrailError": (".integrations", "RoxxGuardrailError"),
    "LayaTriage": (".integrations", "RoxxTriage"),
    "LayaEvaluator": (".integrations", "RoxxEvaluator"),
}


def __getattr__(name):
    try:
        module_name, attr = _LAZY_ATTRS[name]
    except KeyError:
        raise AttributeError("module %r has no attribute %r" % (__name__, name)) from None
    import importlib

    value = getattr(importlib.import_module(module_name, __name__), attr)
    globals()[name] = value      # cache: __getattr__ runs at most once per name
    return value


def __dir__():
    return sorted(list(globals()) + list(_LAZY_ATTRS))


__all__ = [
    "Agent",
    "RLAgent",
    "load",
    "Router",
    "RouteDecision",
    "DEFAULT_MODELS",
    "shortlist_choice",
    "predict_shortlist",
    "embed_fn_from_agent",
    "detect_language",
    "detect_script",
    "is_english",
    "clean_email_body",
    "email_questions",
    "email_state",
    "guard_questions",
    "moderation_questions",
    "router_questions",
    "triage_questions",
    "proper_reward",
    "td_lambda_targets",
    "ece_score",
    "answer_confidence",
    "confidence_from_probs",
    "render_options",
    "QTYPES",
    "QTYPE_NAMES",
    "RoxxRouter",
    "RoxxGuardrail",
    "RoxxGuardrailError",
    "RoxxTriage",
    "RoxxEvaluator",
    "LayaRouter",
    "LayaGuardrail",
    "LayaGuardrailError",
    "LayaTriage",
    "LayaEvaluator",
    "PredictContext",
    "PredictHook",
    "Hook",
    "BaseHook",
    "decide",
    "DecisionResult",
    "__version__",
]
