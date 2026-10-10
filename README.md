# Knowledge-Grounded Neuro-Symbolic Driving — Reproducibility Repository

This repository has been **updated using explicit assumptions** for the three resources identified by the project owner:

1. **BDD100K-OIA / Kaggle `abdimosisa/oia-lastframe`** — assumed to provide image/frame samples and some form of object/action labels. The exact file layout and schema have not been inspected, so the data tools inventory files and preserve raw annotations rather than assuming a fixed schema.
2. **Adama traffic-rules Excel / Kaggle `abdimosisa/adama-traffic-rules-updated2`** — assumed to contain tabular rule descriptions. The importer guesses common header names, exports a review CSV, and creates a *draft* YAML rule inventory. It cannot establish legal validity or infer missing logic safely; every imported rule must be reviewed.
3. **Adama test video / Kaggle `abdimosisa/adama-video`** — assumed to contain one or more common video files. A script extracts sampled frames for qualitative pipeline testing. Video frames are not quantitative ground truth unless independently annotated.

**Important scientific limitation:** this is a reproducibility scaffold and data-adaptation layer, not a verified reproduction of the paper's reported metrics. YOLOP inference and true LTN training/inference still require the exact implementation, checkpoint, and settings used in the experiments. Do not report synthetic/demo outputs as experimental results. The included example traffic rules are illustrative only.

## Suggested Kaggle workflow

Download the datasets from the project URLs into a local `data/` folder, or run the scripts in Kaggle with the dataset mounted under `/kaggle/input/`. Do not commit restricted data, model checkpoints, or personally identifying material to GitHub.

Example local structure (assumed; adjust to actual downloaded files):

```text
data/
  bdd100k_oia/        # images and annotations from oia-lastframe
  adama_rules/        # original .xlsx/.xls file
  adama_video/        # original video
  processed/
    video_frames/
    rule_import/
```

## Quick start

```bash
python -m venv .venv
# activate the environment
pip install -r requirements.txt
python -m pytest
python scripts/validate_config.py --config configs/full_model.yaml
python scripts/inventory_dataset.py --root data/bdd100k_oia --out data/processed/bdd_inventory.json
python ontology/import_excel_rules.py --input data/adama_rules/traffic_rules.xlsx --out-dir data/processed/rule_import
python scripts/extract_video_frames.py --input data/adama_video/test.mp4 --out data/processed/video_frames --every-seconds 1
python scripts/run_scene.py --scene examples/scene_red_signal.json --config configs/full_model.yaml
```

Replace example filenames with the actual files. The importer supports `.xlsx` and `.xls` when the needed engine is installed. It writes `rules_draft.yaml`, `rules_review.csv`, and `import_report.json`; these are draft outputs, not authoritative legal interpretations.

## What the updated tools do

- `scripts/inventory_dataset.py`: lists files, sizes, image dimensions, video metadata when OpenCV is installed, and JSON/JSONL/CSV annotation structure samples. It does not silently transform or relabel annotations.
- `ontology/import_excel_rules.py`: reads an Excel workbook, guesses likely columns (rule text, ID, condition, action/consequence, source/article), and exports a human-reviewable draft. Unknown columns are retained in the report/review CSV. When the source has only natural-language text, the importer does not pretend it can reliably convert that text into executable predicates.
- `scripts/extract_video_frames.py`: extracts frames at a configurable interval and writes a manifest. This supports qualitative tests only unless ground-truth labels are separately supplied.
- `configs/datasets.example.yaml`: documents assumed paths and the separation between development data, rule sources, and video evaluation.

## Assumptions and boundaries

- Annotation schemas are unknown. The repository does not assume BDD100K-OIA action labels equal traffic-rule-compliance labels or explanation ground truth.
- The rule importer uses conservative header matching; review its output and map each rule to predicates/actions manually before enabling it in experiments.
- PCA dimension and fusion settings in the example config are placeholders. Fit any transform on the training split only and save its fitted artifact.
- Jurisdiction-specific rules should be versioned and cited to their actual source documents. `ontology/traffic_rules.yaml` remains a software example until replaced by verified rules.
- Report separate metrics for perception, action prediction, rule compliance, and explanation quality. Document sample counts, splits, uncertainty, and evaluation code.

## Repository map

- `configs/`: experiment and dataset settings
- `perception/`: preprocessing and YOLOP adapter contract
- `fusion/`: feature fusion/PCA helper
- `predicates/`: predicate definitions and scene grounding
- `ontology/`: example rules, provenance, Excel importer
- `reasoning/`: transparent fuzzy baseline and LTN integration seam
- `decision/`: action scoring and evidence-linked explanations
- `scripts/`: dataset inventory, video frame extraction, config validation, demo, metrics
- `tests/`: unit tests for scaffold components
- `docs/`: reproducibility checklist and implementation report template

Before publication, pin dependencies, record dataset version/license and split manifests, add YOLOP repository/checkpoint hashes, verify all rules and citations, and ensure reported values are generated by committed code from documented ground truth.
