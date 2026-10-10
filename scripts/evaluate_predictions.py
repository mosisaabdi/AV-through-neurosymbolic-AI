import argparse, json

def read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                try: rows.append(json.loads(line))
                except json.JSONDecodeError as e: raise ValueError(f"{path}:{n}: {e}") from e
    return rows

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--predictions", required=True)
    p.add_argument("--gold", required=True)
    a = p.parse_args()
    pred, gold = read_jsonl(a.predictions), read_jsonl(a.gold)
    if not pred or len(pred) != len(gold):
        raise SystemExit(f"Need equal non-empty files; got {len(pred)} predictions and {len(gold)} labels")
    acc = sum(x.get("action") == y.get("action") for x, y in zip(pred, gold)) / len(pred)
    print(f"n={len(pred)}")
    print(f"action_accuracy={acc:.6f}")
    pairs = [(x, y) for x, y in zip(pred, gold) if "explanation" in x and "explanation" in y]
    if pairs:
        score = sum(x["explanation"] == y["explanation"] for x, y in pairs) / len(pairs)
        print(f"explanation_exact_match={score:.6f} (n={len(pairs)})")
    print("These starter metrics are not substitutes for formally defined paper metrics.")

if __name__ == "__main__":
    main()
