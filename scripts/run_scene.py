import argparse, json, yaml
from predicates.grounding import ground_predicates
from reasoning.fuzzy_rules import load_rules, evaluate_rules
from decision.action_scoring import score_actions
from decision.explanation import build_explanation

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scene", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--output")
    a = p.parse_args()
    with open(a.scene, encoding="utf-8") as f: scene = json.load(f)
    with open(a.config, encoding="utf-8") as f: cfg = yaml.safe_load(f)
    predicates = ground_predicates(scene)
    rules = load_rules(cfg["knowledge"]["ontology_file"])
    results = evaluate_rules(predicates, rules)
    action, scores, evidence = score_actions(
        results, cfg["decision"]["actions"], scene.get("action_confidence", {}),
        float(cfg["decision"].get("rule_weight", 1.0))
    )
    output = {
        "scene_id": scene.get("scene_id", "unknown"),
        "action": action, "scores": scores,
        "explanation": build_explanation(action, predicates, evidence, scores),
        "rule_results": [r.__dict__ for r in results],
        "mode": "transparent_fuzzy_rule_baseline_not_full_LTN"
    }
    serialized = json.dumps(output, indent=2)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f: f.write(serialized + "\n")
    print(serialized)

if __name__ == "__main__":
    main()
