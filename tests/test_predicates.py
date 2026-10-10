import pytest
from predicates.grounding import ground_predicates

def test_missing_predicates_default_zero():
    out = ground_predicates({"predicates": {"red_signal": 0.9}})
    assert out["red_signal"] == pytest.approx(0.9)
    assert out["at_stop_line"] == 0.0

def test_invalid_truth_rejected():
    with pytest.raises(ValueError):
        ground_predicates({"predicates": {"red_signal": 1.2}})
