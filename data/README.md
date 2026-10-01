# Data

This directory contains frozen upstream inputs, documentary revision coding, and generated row-level analysis datasets. Do not manually edit generated or frozen analysis files.

## Current revised-paper inputs

### `merged_autm.csv`

Frozen annual institution-year technology-transfer panel used by the documentary event-study code to construct the analysis panel, controls, and outcomes.

SHA-256: `070f10179b34a0730d1f09ea3322d21e8f32e20d3036760df2adfef182aa2d4b`

### `revision_codes_manual.csv`

Hand-reviewed documentary coding underlying the frozen September 25 25-event benchmark.

### `revision_codes_rereview37.csv`

Second-pass documentary review of mechanically eligible non-main revisions. The nine usable additions in this file are combined with the frozen 25-event benchmark to form the preferred 34-event revised-paper sample.

## Verified cross-repository reference panel

### `verified_replication_dataset.csv`

The 3,507-row, 46-variable analysis-ready panel produced by the cross-repository Paper 1/Paper 2 verification. It is retained as a verified provenance/reference dataset. It is not the row-level stacked event-study dataset used directly by the preferred 34-event specification.

SHA-256: `de5377b98c1261c5de9a5b4df21efb86af04bbdce28cb3676ec37c61456fcdf6`

## Generated stacked datasets

`export_final_stacked_datasets.py` writes explicit row-level stacked datasets under `data/derived/`, including:

- `final_stacked_event_dataset_expanded34.csv` — preferred 34-event documentary design.
- `final_stacked_event_dataset_strict29.csv` — strict 29-event post-support sensitivity.

Because comparison institution-years can legitimately appear in multiple event-specific stacks, the number of stacked rows is not the number of independent policy events. The independent treated-event counts are 34 and 29, respectively.

For the exact execution order and analysis hierarchy, see `code/README.md` and the repository reproducibility documentation.
