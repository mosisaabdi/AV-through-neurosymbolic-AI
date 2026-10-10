import yaml
from pathlib import Path
from reasoning.fuzzy_rules import load_rules

def test_config_parses():
    cfg = yaml.safe_load(Path("configs/full_model.yaml").read_text(encoding="utf-8"))
    assert "experiment" in cfg and "knowledge" in cfg

def test_rule_ids_unique():
    rules = load_rules("ontology/traffic_rules.yaml")
    ids = [r["id"] for r in rules]
    assert ids and len(ids) == len(set(ids))
