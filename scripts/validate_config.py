import argparse, yaml

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()
    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    required = ["experiment", "data", "perception", "predicates", "knowledge", "reasoning", "decision"]
    missing = [key for key in required if key not in cfg]
    if missing:
        raise SystemExit(f"Missing sections: {missing}")
    print(f"Config structure valid: {args.config}")
    print("This does not verify placeholders, dataset paths, or checkpoint existence.")

if __name__ == "__main__":
    main()
