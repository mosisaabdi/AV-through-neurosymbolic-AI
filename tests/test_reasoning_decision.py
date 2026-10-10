from reasoning.fuzzy_rules import evaluate_rules
from decision.action_scoring import score_actions

def test_red_signal_supports_stop():
    rules = [{"id":"R-SIG-RED","antecedents":["red_signal","at_stop_line"],
              "consequent":"STOP","priority":100,"enabled":True,"provenance":"test"}]
    results = evaluate_rules({"red_signal":0.9,"at_stop_line":0.8}, rules)
    assert abs(results[0].antecedent_truth - 0.72) < 1e-9
    action, scores, evidence = score_actions(results, actions=["STOP","PROCEED"])
    assert action == "STOP"
    assert evidence["STOP"][0]["rule_id"] == "R-SIG-RED"
