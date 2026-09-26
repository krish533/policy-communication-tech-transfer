# Code

The current September 25 paper and the legacy annual-panel paper are deliberately separated.

## Current paper

- `revision_replication.py` is the **canonical September 25 replication entry point**. It reconstructs the 149-institution AUTM panel, uses institution research-size terciles based on median research expenditure, rebuilds the 127-revision clean-control universe from the pinned Paper 1 policy history, estimates the 25-event stacked design, and enumerates all 177,100 assignments of six upward revision labels for exact permutation inference.
- `revision_event_study.py` contains the lower-level panel, revision-universe, stacking, fixed-effect absorption, and clustered-inference functions used by the canonical replication.
- `sept25_diagnostics.py` audits the data lineage, institution harmonization, full revision counts, the 25 hand-reviewed transitions, and the FY2023 licensing-series correction.
- `spec_search.py` is a development diagnostic retained to document how the research-size-stratification detail was reconciled against the September 25 manuscript. It is not part of production CI.

Generated current-paper Table 3 results are written to `results/table3_reproduced.csv` and `results/table3_reproduced.json`.

## Legacy annual-panel benchmark

`replication.py` and `run_all.py` are the verified earlier Paper 2 programs. They operate on `data/merged_autm.csv` and are retained for provenance. They should not be silently modified to stand in for the September 25 revision design.
