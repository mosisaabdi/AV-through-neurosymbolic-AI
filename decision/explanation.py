def build_explanation(action, predicates, evidence_by_action, scores):
    return {
        "selected_action": action,
        "score": round(float(scores.get(action, 0.0)), 6),
        "grounded_predicates": {k: round(float(v), 6) for k, v in predicates.items()},
        "supporting_rules": evidence_by_action.get(action, []),
        "warning": "Explanation reflects configured rules and supplied predicate evidence."
    }
