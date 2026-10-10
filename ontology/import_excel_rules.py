"""Conservative Excel-to-rule-draft importer; output requires human validation.

This tool does NOT convert arbitrary legal prose into executable logic. It preserves
source text and maps columns only when headers resemble common rule fields.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path
import yaml

ALIASES = {
    "rule_id": ["id", "rule id", "rule_id", "article", "article no", "number", "no"],
    "rule_text": ["rule", "rule text", "description", "traffic rule", "regulation", "content", "provision"],
    "condition": ["condition", "conditions", "if", "antecedent", "when", "trigger"],
    "action": ["action", "consequence", "then", "required action", "decision", "response"],
    "source": ["source", "reference", "legal source", "document", "law", "section", "article reference"],
}

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").strip().lower()).strip()

def choose_columns(columns):
    normalized = {c: norm(c) for c in columns}
    chosen = {}
    for field, aliases in ALIASES.items():
        alias_norms = [norm(a) for a in aliases]
        for col, ncol in normalized.items():
            if ncol in alias_norms or any(a and (ncol.startswith(a + " ") or a.startswith(ncol + " ")) for a in alias_norms):
                chosen[field] = col
                break
    return chosen

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="Path to .xlsx/.xls workbook")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--sheet", default=None, help="Optional worksheet name; default is first sheet")
    a = p.parse_args()
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Install pandas and openpyxl (for .xlsx) before importing Excel rules") from exc
    src = Path(a.input); out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    if not src.exists(): raise SystemExit(f"Input workbook not found: {src}")
    frame = pd.read_excel(src, sheet_name=a.sheet or 0, dtype=str).fillna("")
    columns = choose_columns(frame.columns)
    records = []
    for i, row in frame.iterrows():
        raw = {str(k): str(v).strip() for k, v in row.to_dict().items()}
        if not any(raw.values()): continue
        get = lambda key: str(row[columns[key]]).strip() if key in columns else ""
        rid = get("rule_id") or f"IMPORTED-{len(records)+1:04d}"
        text = get("rule_text")
        condition = get("condition")
        action = get("action")
        source = get("source")
        records.append({
            "id": rid,
            "description": text or "REVIEW REQUIRED: no rule-text column was confidently identified",
            "source_condition_text": condition,
            "source_action_text": action,
            "consequent": "REVIEW_REQUIRED",
            "antecedents": [],
            "priority": 0,
            "enabled": False,
            "provenance": source or f"Workbook: {src.name}; worksheet: {a.sheet or 'first sheet'}; row: {i+2}",
            "source_row": int(i + 2),
            "raw_columns": raw,
            "review_status": "needs_human_mapping",
        })
    rules_path = out / "rules_draft.yaml"
    with rules_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump({"notice": "Draft import only; validate legal meaning, predicates, exceptions, and provenance before use.", "source_workbook": str(src), "detected_columns": {k: str(v) for k,v in columns.items()}, "rules": records}, f, sort_keys=False, allow_unicode=True, width=110)
    csv_path = out / "rules_review.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        fields = ["id", "description", "source_condition_text", "source_action_text", "provenance", "source_row", "review_status", "raw_columns_json"]
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
        for r in records:
            writer.writerow({**{k:r.get(k, "") for k in fields if k != "raw_columns_json"}, "raw_columns_json": json.dumps(r["raw_columns"], ensure_ascii=False)})
    report = {"input": str(src), "sheet": a.sheet or "first sheet", "row_count_imported": len(records), "detected_columns": {k: str(v) for k,v in columns.items()}, "unmapped_columns": [str(c) for c in frame.columns if c not in columns.values()], "warning": "No imported rule is executable or enabled until manually reviewed."}
    (out / "import_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
if __name__ == "__main__": main()
