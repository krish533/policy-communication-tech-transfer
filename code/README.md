# Code

The repository keeps the publication-facing expanded documentary design separate from the frozen September 25 benchmark and the earlier annual-panel replication.

## One-command publication replication

Run `python code/reproduce_submission.py` from the repository root after installing the pinned root `requirements.txt`. This is the canonical submission runner used by CI. It rebuilds publication-facing inference, diagnostics, manuscript figures, and explicit stacked datasets in the required order.

## Publication-facing expanded design

The runner executes:

1. `final_expanded_inference.py` — canonical publication-facing inference for the preferred 34-event documentary sample and the strict 29-event support sensitivity. It uses 100,000 direction-label assignments per outcome and rewrites the publication-facing expanded result files.
2. `expanded34_diagnostics.py` — balance, stack-composition, pre-trend, and leave-one-event-out diagnostics used by the revised manuscript.
3. `build_expanded_manuscript_figures.py` — regenerates the revised manuscript figures from the publication-facing outputs.
4. `export_final_stacked_datasets.py` — exports explicit row-level stacked datasets for the preferred 34-event design and strict 29-event sensitivity.

`expanded_manual_revision_analysis.py` contains the shared sample-construction and Monte Carlo routines. Its 20,000-draw default is intended for development; `final_expanded_inference.py` is the publication-facing entry point and raises the draw count to 100,000.

The preferred documentary sample contains 34 independently classified revision events (8 upward, 26 downward). The strict sensitivity contains 29 events (7 upward, 22 downward) after requiring at least two observed treated core-outcome panel years in event times 0..+5.

## Frozen September 25 benchmark

- `revision_replication.py` reproduces the hand-reviewed 25-event September 25 benchmark and exact direction-label permutation inference.
- `revision_event_study.py` contains lower-level panel, revision-universe, stacking, fixed-effect absorption, and clustered-inference functions. The expanded analysis reuses these tested utilities, but the 25-event sample is now a benchmark/sensitivity rather than the preferred revised-manuscript specification.
- `sept25_diagnostics.py` audits the benchmark data lineage, institution harmonization, revision counts, hand-reviewed transitions, and FY2023 licensing-series correction.
- `spec_search.py` is a development diagnostic retained for provenance and is not part of production CI.

## Legacy annual-panel benchmark

`replication.py` and `run_all.py` are the verified earlier Paper 2 programs. They operate on `data/merged_autm.csv` and are retained for provenance. Do not silently modify them to stand in for the revised documentary design.

## Environment

Use Python 3.11 and install only from the pinned root `requirements.txt`. The GitHub Actions workflows use the same environment. Randomization seeds are fixed in code so reruns are deterministic apart from platform-level numerical tolerance.
