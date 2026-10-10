# Knowledge-Grounded Neuro-Symbolic Driving

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Status-Research%20Prototype-6A5ACD" alt="Status: Research Prototype" />
  <img src="https://img.shields.io/badge/License-Research%20Use-blue" alt="License" />
  <img src="https://img.shields.io/badge/Tests-Pytest-FFB000?logo=pytest&logoColor=black" alt="Pytest" />
</p>

A neuro-symbolic autonomous driving framework for interpretable scene understanding, rule-based driving logic, and evidence-grounded decision-making.

This repository implements a modular pipeline that combines perception outputs, symbolic predicate grounding, traffic-rule evaluation, and transparent action selection. The design is intended for research, reproducibility, and local adaptation to driving datasets and rule sources.

## Why this project

Modern autonomous driving systems often rely on opaque end-to-end models. This project takes a complementary perspective: a transparent stack in which

- perceptual inputs are processed into structured scene features,
- traffic situations are represented as predicates,
- symbolic constraints and traffic rules are evaluated explicitly,
- actions are scored with explainable evidence,
- decisions can be traced back to rule satisfaction and scene context.

The result is an interpretable decision layer designed to support reasoning, auditing, and qualitative evaluation.

## System overview

```mermaid
flowchart LR
    A[Scene / Video / Frames] --> B[Perception Preprocessing]
    B --> C[Predicate Grounding]
    C --> D[Rule Evaluation]
    D --> E[Action Scoring]
    E --> F[Explanation Generation]
    F --> G[Decision Output]
```

## Core capabilities

- Perception preprocessing and scene normalization
- YOLOP-compatible adapter contract for driving scene understanding
- Predicate grounding for traffic-state interpretation
- Knowledge-driven rule evaluation using symbolic logic
- Transparent fuzzy-rule baseline for decision support
- Explainable action selection with evidence mapping
- Dataset inventory and frame extraction tooling for reproducibility
- Excel-based traffic-rule import workflow for downstream review

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── configs/
│   ├── data_splits.example.json
│   ├── datasets.example.yaml
│   └── full_model.yaml
├── decision/
│   ├── __init__.py
│   ├── action_scoring.py
│   └── explanation.py
├── docs/
│   ├── IMPLEMENTATION_REPORT_TEMPLATE.md
│   └── REPRODUCIBILITY_CHECKLIST.md
├── examples/
│   └── scene_red_signal.json
├── fusion/
│   ├── __init__.py
│   └── feature_fusion_pca.py
├── ontology/
│   ├── __init__.py
│   ├── import_excel_rules.py
│   ├── rule_provenance.yaml
│   └── traffic_rules.yaml
├── perception/
│   ├── __init__.py
│   ├── preprocessing.py
│   └── yolop_adapter.py
├── predicates/
│   ├── __init__.py
│   └── predicate_definitions.yaml
├── reasoning/
│   ├── fuzzy_rules.py
│   └── ltn_model.py
├── scripts/
│   ├── evaluate_predictions.py
│   ├── extract_video_frames.py
│   ├── inventory_dataset.py
│   ├── run_scene.py
│   └── validate_config.py
├── tests/
│   ├── test_config_and_rules.py
│   ├── test_excel_importer.py
│   ├── test_predicates.py
│   └── test_reasoning_decision.py
└── data/    # local-only dataset directory (not committed to GitHub)
```

## Installation

### Requirements

- Python 3.10+
- pip
- Git

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- Windows:

```powershell
.venv\Scripts\activate
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Quick start

### 1) Validate the configuration

```bash
python scripts/validate_config.py --config configs/full_model.yaml
```

### 2) Run the demo scene

```bash
python scripts/run_scene.py --scene examples/scene_red_signal.json --config configs/full_model.yaml
```

This produces an output JSON with:

- selected action
- action scores
- rule evaluation details
- explanation text
- predicates used by the decision process

### 3) Inventory a dataset

```bash
python scripts/inventory_dataset.py --root data/bdd100k_oia --out data/processed/bdd_inventory.json
```

### 4) Extract frames from video input

```bash
python scripts/extract_video_frames.py --input data/adama_video/test.mp4 --out data/processed/video_frames --every-seconds 1
```

### 5) Import traffic rules from Excel

```bash
python ontology/import_excel_rules.py --input data/adama_rules/traffic_rules.xlsx --out-dir data/processed/rule_import
```

## Project configuration

The repository uses YAML configuration files under `configs/` to specify:

- dataset paths
- task splits
- knowledge ontology references
- action definitions
- rule weighting and decision parameters

Examples:

- `configs/full_model.yaml`
- `configs/datasets.example.yaml`
- `configs/data_splits.example.json`

## Data assumptions and usage

This project is designed to work with local research data and rule sources. A typical setup looks like:

```text
data/
  bdd100k_oia/
  adama_rules/
  adama_video/
  processed/
    video_frames/
    rule_import/
```

The repository does not commit raw datasets, checkpoints, or restricted media to GitHub. These artifacts should be stored locally or on a managed data platform according to the dataset license and institutional policy.

## Architecture

### Perception module

The `perception/` package contains preprocessing and an adapter layer for perception models. It is intended to support operations such as:

- image normalization
- scene preprocessing
- feature extraction compatible with driving scene understanding
- adaptation to YOLOP-style pipelines

### Predicate and knowledge layer

The `predicates/` and `ontology/` modules represent scene state, rule definitions, and regulatory knowledge. These components map raw observations into structured truth conditions such as:

- red light observed
- stop sign present
- mandatory yield state
- unsafe preceding vehicle context

### Reasoning and decision layer

The `reasoning/` package provides symbolic and fuzzy reasoning components for evaluating rule satisfaction and supporting action selection. The `decision/` package then aggregates evidence and produces ranked actions with explanations.

### Explainability

The decision pipeline explicitly records:

- rule activation
- predicate evidence
- action confidence
- explanation rationale

This is designed to support debugging, qualitative analysis, and human review of decisions.

## Testing

Run the project test suite with:

```bash
pytest
```

The repository currently includes tests for:

- configuration validation
- rule parsing and import behavior
- predicate definitions
- reasoning and decision logic

## Reproducibility and documentation

The project includes documentation templates for reproducibility and reporting:

- `docs/REPRODUCIBILITY_CHECKLIST.md`
- `docs/IMPLEMENTATION_REPORT_TEMPLATE.md`

These are designed to help document dataset versions, model assumptions, rule provenance, evaluation setup, and reporting details.

## Example workflow

1. Prepare or collect local driving data.
2. Inventory the dataset structure and metadata.
3. Validate configuration.
4. Run preprocessing and perception adapters.
5. Ground scene predicates.
6. Evaluate traffic rules and constraints.
7. Score candidate actions.
8. Produce explanation and output logs.
9. Record the exact setup for reproducibility.

## Notes on scientific use

This repository is structured as a transparent research implementation and reproducibility scaffold. It is intended for:

- pipeline prototyping
- local experiment adaptation
- explainable autonomous driving research
- rule-driven decision validation

It should be used responsibly in accordance with dataset licensing and domain-specific safety requirements.

## Contributing

Contributions are welcome in the following areas:

- robustness of rule import workflows
- improved perception-to-predicate mapping
- clearer explanation generation
- config validation and dataset documentation
- reproducibility tooling and benchmarking support

Please keep changes focused, documented, and validated with tests.

## License

This repository does not currently include a license file. If you plan to publish or distribute it publicly, add a license such as MIT or Apache-2.0 before release.

## Citation

If you use this repository in research, please cite the project appropriately and document the exact version, dataset sources, and rule provenance used in your work.

## Maintainer

Add your name, lab, or institutional affiliation here.

---

<p align="center">
  <strong>Transparent, knowledge-grounded decision-making for autonomous driving.</strong>
</p>
