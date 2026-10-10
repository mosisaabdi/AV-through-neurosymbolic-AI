# Reproducibility checklist
- [ ] Record Git commit and dependency lockfile.
- [ ] Record YOLOP repository URL/commit and checkpoint SHA256.
- [ ] Document dataset version, license, and fixed split manifests.
- [ ] Record image preprocessing, thresholds, and NMS settings.
- [ ] Fit PCA only on training data; archive the fitted transformation.
- [ ] Publish verified predicate inventory and grounding implementation.
- [ ] Add rule source, jurisdiction, version, applicability, exceptions, provenance.
- [ ] Document exact LTN library, groundings, t-norm, implication, quantifiers, aggregation.
- [ ] Record optimizer, learning rate, batch size, epochs, seeds, hardware, selection criterion.
- [ ] Publish action scoring, conflict handling, and metric definitions.
- [ ] Ensure baseline/ablation configs correspond to reported runs.
- [ ] Link each reported metric to evaluation logs/configuration.
- [ ] Mark synthetic examples clearly; never report them as experiment results.

Suggested run manifest: run_id, git_commit, config_sha256, dataset_version,
split_manifest_sha256, checkpoint_sha256, ontology_version, seed, hardware,
start_time, end_time, metrics_file.

## Dataset-specific checks added for the assumed Kaggle sources
- [ ] Run `scripts/inventory_dataset.py` on the downloaded BDD100K-OIA directory and inspect annotation samples before writing a parser.
- [ ] Populate `configs/datasets.example.yaml` with real paths, annotation filenames, version/download date, and license notes.
- [ ] Import the local rules workbook with `ontology/import_excel_rules.py`; manually review every row in `rules_review.csv` and keep imported rules disabled until mapped to predicates/actions and verified against source.
- [ ] Extract Adama video frames only for qualitative review unless frame/event ground truth exists.
- [ ] Prevent adjacent-frame/video-sequence leakage across splits.
- [ ] Confirm whether reported explanation labels are human-annotated, rule-derived, or generated; report the source explicitly.
