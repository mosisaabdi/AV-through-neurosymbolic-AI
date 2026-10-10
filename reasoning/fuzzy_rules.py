from dataclasses import dataclass
import yaml

@dataclass
class RuleResult:
    rule_id: str
    antecedent_truth: float
    consequent: str
    priority: float
    provenance: str

def product_t_norm(values):
    result = 1.0
    for value in values:
        result *= max(0.0, min(1.0, float(value)))
    return result

def load_rules(path):
    with open(path, encoding="utf-8") as f:
        return (yaml.safe_load(f) or {}).get("rules", [])

def evaluate_rules(predicates, rules):
    results = []
    for rule in rules:
        if not rule.get("enabled", True):
            continue
        truth = product_t_norm([predicates.get(p, 0.0) for p in rule.get("antecedents", [])])
        results.append(RuleResult(
            rule["id"], truth, rule["consequent"],
            float(rule.get("priority", 0)), str(rule.get("provenance", "unspecified"))
        ))
    return results
