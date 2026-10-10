from collections import defaultdict

DEFAULT_ACTIONS = ["STOP", "YIELD", "SLOW", "KEEP_LANE", "CHANGE_LANE", "PROCEED"]

def score_actions(rule_results, actions=None, confidence_scores=None, rule_weight=1.0):
    actions = actions or DEFAULT_ACTIONS
    confidence_scores = confidence_scores or {}
    scores = {a: float(confidence_scores.get(a, 0.0)) for a in actions}
    evidence = defaultdict(list)
    for r in rule_results:
        if r.consequent in scores:
            scores[r.consequent] += rule_weight * r.antecedent_truth * (1 + r.priority / 100)
            evidence[r.consequent].append({
                "rule_id": r.rule_id,
                "truth": round(r.antecedent_truth, 6),
                "provenance": r.provenance
            })
    action = max(actions, key=lambda a: (scores[a], -actions.index(a)))
    return action, scores, dict(evidence)
