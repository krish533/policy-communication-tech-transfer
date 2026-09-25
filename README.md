# When Universities Rewrite Their Intellectual-Property Policies

**Policy Revisions, Policy Communication, and University Technology Transfer**

This repository is the active research and replication home for the September 25, 2026 version of the paper on ordinary university IP-policy revisions and technology-transfer outcomes.

## Current paper baseline

The authoritative manuscript baseline is the 30-page September 25 PDF supplied by the authors:

> *When Universities Rewrite Their Intellectual-Property Policies: Policy Revisions, Policy Communication, and University Technology Transfer*

A structured record of that version, including its PDF SHA-256 and headline empirical benchmarks, is in [`manuscript/sept25_baseline.md`](manuscript/sept25_baseline.md).

The paper's **main design is a stacked revision event study**, not the older annual-PCSI regression. For each documented revision, the revising university is compared with contemporaneous universities that do not revise anywhere in the event window. Revision direction is classified using the Policy Communication Stance Index (PCSI) from the companion measurement paper.

### Main revision sample

The September 25 baseline uses:

- `|ΔPCSI| > 0.03` as the principal revision threshold;
- 25 hand-reviewed, documented policy revisions;
- 6 revisions toward more supportive language and 19 toward more restrictive language;
- event years 1994–2021;
- event window `[-4, +5]`, with year `-1` omitted;
- clean non-revising controls;
- stack × institution fixed effects;
- stack × year × research-size-tercile × public/private fixed effects;
- log research expenditure as a control;
- institution-clustered standard errors;
- exact permutation inference over all `C(25, 6) = 177,100` direction assignments for the main sample.

The 25 main events are recorded in [`data/revision_codes_manual.csv`](data/revision_codes_manual.csv).

### Headline manuscript result

The September 25 PDF reports an average post-revision upward-minus-downward licensing gap of **0.619 log points** (clustered SE 0.136; exact permutation `p = 0.015`; BH-adjusted `q = 0.075`). Relative to contemporaneous non-revisers, licensing rises after upward revisions and falls after downward revisions, while invention disclosures do not respond systematically.

The interpretation remains deliberately cautious: universities choose whether and how to revise their policies, so the design documents a robust post-revision pattern and where it appears in the technology-transfer pipeline; it does **not** establish a causal effect of policy wording.

## Independent reconstruction status

The repository now independently reconstructs the September 25 design from the audited AUTM merge, the pinned Paper 1 policy history, and the 25 hand-reviewed Appendix A1 events.

Structural quantities reproduce exactly: **3,507 institution-years, 149 harmonized institutions, 127 threshold revisions at 78 institutions, 25 main events (6/19), all 25 document transitions, and every Table 3 regression sample size**. The FY2023 licensing-series correction also reproduces exactly.

The independently regenerated Table 3 is extremely close but not byte-for-byte identical to the PDF. For licensing it gives **0.6213 (SE 0.1360; exact permutation p = 0.00946)** versus the PDF's **0.619 (SE 0.136; p = 0.015)**. The repository therefore preserves both the PDF targets and the regenerated values rather than silently replacing either one. See [`replication/sept25_reconciliation.md`](replication/sept25_reconciliation.md) and [`results/table3_reproduced.csv`](results/table3_reproduced.csv).

## Data lineage

The project combines two audited sources:

- Paper 1 measurement repository: `krish533/Tech-transfer-1`
- Legacy Paper 2 outcome repository: `krish533/tech-transfer-paper-2`

Pinned provenance commits:

- Paper 1: `25a9472b34334825b6d6c6a334f5b88eb00695b5`
- Paper 2: `88cf4a1c02540b136adb8beaa35e212625ac755e`

The cross-repository audit established that all 2,564 rows carrying PCSI/NLP measures match the Paper 1 panel on the policy-link key, with zero mismatches in mean PCSI, median PCSI, Tone, Clarity, Legal Load, sentence count, word count, source year, and carry-forward status.

The legacy verified dataset remains [`data/verified_replication_dataset.csv`](data/verified_replication_dataset.csv) (3,507 rows × 46 columns; SHA-256 `de5377b98c1261c5de9a5b4df21efb86af04bbdce28cb3676ec37c61456fcdf6`). For the current paper, the panel fixed-effect identifier is the **149-institution `Institution_std` harmonization** in `data/merged_autm.csv`; the sparse 139-institution `Institution_pci` field is a policy-corpus matching key, not the panel identifier.

## Current versus legacy code

- `code/revision_replication.py` — **canonical September 25 replication entry point**, including exact 177,100-assignment permutation inference.
- `code/revision_event_study.py` — lower-level panel, stacking, fixed-effect, and clustered-inference functions.
- `code/sept25_diagnostics.py` — lineage and sample-construction audit.
- `code/spec_search.py` — retained development diagnostic; not production CI.
- `code/replication.py` and `code/run_all.py` — frozen **legacy annual-panel Paper 2** benchmark programs.

Annual continuous-PCSI models remain supporting evidence in the September 25 paper; they are not the main design.

## Repository structure

```text
.
├── manuscript/
│   ├── sept25_baseline.md       # authoritative September 25 specification/results map
│   ├── main.tex                 # older editable LaTeX source; not yet line-for-line Sept. 25
│   └── paper2_verified_starting_point.tex  # frozen legacy manuscript
├── data/
│   ├── verified_replication_dataset.csv
│   ├── merged_autm.csv
│   └── revision_codes_manual.csv           # 25 hand-reviewed main events
├── code/
│   ├── revision_replication.py             # canonical September 25 replication
│   ├── revision_event_study.py             # lower-level revision-design functions
│   ├── sept25_diagnostics.py               # reconciliation checks
│   ├── spec_search.py                      # development diagnostic
│   ├── replication.py                      # frozen legacy Paper 2 benchmark
│   └── run_all.py
├── replication/
│   ├── sept25_reconciliation.md
│   └── cross-repository provenance files
├── results/
│   ├── table3_reproduced.csv
│   ├── table3_reproduced.json
│   ├── tables/
│   └── figures/
└── .github/workflows/           # reproducibility checks
```

## Reproducibility standard

A result is described as reproduced only when the repository regenerates it from code and data. If a PDF result depends on hand-reviewed documentary information not present in the legacy panel, that coding must be committed explicitly rather than inferred silently. Any remaining difference between the PDF and regenerated values is documented rather than tuned away.

The Paper 1 release reproduces classifier inference, calibration, aggregation, policy-in-force panel construction, and manuscript-facing analyses. It does not reconstruct the original BERT fine-tuning from coder-level pre-adjudication records; that limitation remains part of the provenance statement.

## Development rule

Keep three categories separate:

1. **September 25 revision-design results** — current paper;
2. **legacy annual-panel results** — provenance/supporting evidence;
3. **causal claims** — only if a future design provides defensible identification beyond the observational revision comparison.
