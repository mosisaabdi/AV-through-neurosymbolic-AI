import importlib.util
from pathlib import Path

MODULE = Path(__file__).parents[1] / "ontology" / "import_excel_rules.py"
spec = importlib.util.spec_from_file_location("import_excel_rules", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_common_excel_headers_are_detected():
    columns = mod.choose_columns(["Article No", "Traffic Rule Description", "Condition", "Required Action", "Legal Source"])
    assert columns["rule_id"] == "Article No"
    assert columns["rule_text"] == "Traffic Rule Description"
    assert columns["condition"] == "Condition"
    assert columns["action"] == "Required Action"
    assert columns["source"] == "Legal Source"

def test_unknown_headers_do_not_get_misrepresented_as_rules():
    columns = mod.choose_columns(["ColA", "ColB"])
    assert columns == {}
