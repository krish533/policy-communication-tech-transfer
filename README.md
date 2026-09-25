# When Universities Rewrite Their Intellectual-Property Policies

**Policy Revisions, Policy Communication, and University Technology Transfer**

This repository is the active research and replication home for the September 25, 2026 version of the paper on ordinary university IP-policy revisions and technology-transfer outcomes.

## Current paper baseline

The authoritative manuscript baseline is the 30-page September 25 PDF supplied by the authors:

> *When Universities Rewrite Their Intellectual-Property Policies: Policy Revisions, Policy Communication, and University Technology Transfer*

A structured record of that version, including its PDF SHA-256 and every headline empirical benchmark, is in [`manuscript/sept25_baseline.md`](manuscript/sept25_baseline.md).

The paper's **main design is a stacked revision event study**, not the older annual-PCSI regression. For each documented revision, the revising university is compared with contemporaneous universities that do not revise anywhere in the event window. Revision direction is classified using the Policy Communication Stance Index (PCSI) from the companion measurement paper.

### Main revision sample

The September 25 baseline uses:

- `|ΔPCSI| > 0.03` as the principal revision threshold;
- 25 hand-reviewed, documented policy revisions;
- 6 revisions toward more supportive language;
- 19 revisions toward more restrictive language;
- event years 1994–2021;
- event window `[-4, +5]`, with year `-1` omitted;
- clean non-revising controls;
- stack × institution fixed effects;
- stack × year × research-size-tercile × public/private fixed effects;
- log research expenditure as a control;
- institution-clustered standard errors;
- exact permutation inference over all `C(25, 6) = 177,100` direction assignments for the main sample.

The 25 main events are recorded in [`data/revision_codes_manual.csv`](data/revision_codes_manual.csv).

### Headline result

For log licenses and options executed, the September 25 manuscript reports an average post-revision **upward-minus-downward gap of 0.619 log points** (clustered SE 0.136; exact permutation `p = 0.015`; BH-adjusted `q = 0.075`). Relative to contemporaneous non-revisers, licensing rises after upward revisions and falls after downward revisions. Invention disclosures do not respond systematically.

The interpretation remains deliberately cautious: universities choose whether and how to revise their policies, so the design documents a robust post-revision pattern and where it appears in the technology-transfer pipeline; it does **not** establish a causal effect of policy wording.

## Data lineage

The project combines two audited sources:

- Paper 1 measurement repository: `krish533/Tech-transfer-1`
- Legacy Paper 2 outcome repository: `krish533/tech-transfer-paper-2`

Pinned provenance commits:

- Paper 1: `25a9472b34334825b6d6c6a334f5b88eb00695b5`
- Paper 2: `88cf4a1c02540b136adb8beaa35e212625ac755e`

The September 25 cross-repository audit established that all 2,564 Paper 2 rows carrying PCSI/NLP measures match the Paper 1 panel on standardized institution and calendar year, with zero mismatches in mean PCSI, median PCSI, Tone, Clarity, Legal Load, sentence count, word count, source year, and carry-forward status.

The core verified analysis dataset is [`data/verified_replication_dataset.csv`](data/verified_replication_dataset.csv):

- 3,507 rows;
- 46 analysis/provenance columns;
- SHA-256 `de5377b98c1261c5de9a5b4df21efb86af04bbdce28cb3676ec37c61456fcdf6`.

The frozen original merged Paper 2 input remains in `data/merged_autm.csv` for exact legacy reproduction.

## Important distinction: current vs legacy code

`code/replication.py` and `code/run_all.py` reproduce the **legacy annual-panel Paper 2 benchmark**. They are retained as provenance and should not be interpreted as the main September 25 design.

The September 25 revision analysis is developed separately in `code/revision_event_study.py` and related scripts. This separation prevents the new revision design from silently overwriting the audited legacy benchmark.

Annual continuous-PCSI models remain supporting evidence in the September 25 paper. They are re-estimated on 149 harmonized institutions and are not the identifying design.

## Repository structure

```text
.
├── manuscript/
│   ├── sept25_baseline.md      # authoritative September 25 specification/results map
│   ├── main.tex                # editable manuscript source
│   └── paper2_verified_starting_point.tex  # frozen legacy manuscript
├── data/
│   ├── verified_replication_dataset.csv
│   ├── merged_autm.csv
│   └── revision_codes_manual.csv           # 25 hand-reviewed main events
├── code/
│   ├── revision_event_study.py             # September 25 main design
│   ├── sept25_diagnostics.py               # data reconciliation checks
│   ├── replication.py                      # frozen legacy Paper 2 benchmark
│   └── run_all.py
├── replication/                # cross-repository audit and frozen provenance
├── results/
│   ├── tables/
│   └── figures/
└── .github/workflows/          # reproducibility and revision-design checks
```

## Reproducibility standard

For the current paper, a result should be described as reproduced only when the repository regenerates the corresponding September 25 table/figure from code and data. If a PDF result depends on hand-reviewed documentary information not present in the legacy annual panel, that coding must be committed explicitly rather than inferred silently.

The Paper 1 release reproduces classifier inference, calibration, aggregation, policy-in-force panel construction, and manuscript-facing analyses. It does not reconstruct the original BERT fine-tuning from coder-level pre-adjudication records; that limitation remains part of the provenance statement.

## Development rule

Keep three categories separate:

1. **September 25 revision-design results** — current paper;
2. **legacy annual-panel results** — provenance/supporting evidence;
3. **causal claims** — only if a future design provides defensible identification beyond the observational revision comparison.
