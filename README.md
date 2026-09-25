# Policy Communication and Technology Transfer

This repository is the active research and replication home for the updated paper on university intellectual-property policy communication and technology-transfer outcomes.

## Research design

The project links a text-based measure of communicative stance in U.S. university IP policies to longitudinal technology-transfer outcomes. The policy measure is inherited from the measurement pipeline in **Paper 1** and is merged to AUTM-style technology-transfer outcomes used in **Paper 2**.

This repository begins from a cross-repository verification completed on September 25, 2026. The purpose of the new repository is to keep the updated paper, its analysis code, and its verified data lineage together without changing the archived Paper 1 and Paper 2 repositories.

## Verified data lineage

Source repositories:

- Paper 1: `krish533/Tech-transfer-1`
- Paper 2: `krish533/tech-transfer-paper-2`

Pinned source commits:

- Paper 1: `25a9472b34334825b6d6c6a334f5b88eb00695b5`
- Paper 2: `88cf4a1c02540b136adb8beaa35e212625ac755e`

Cross-repository checks established that:

- the Paper 1 canonical panel contains 4,296 institution-year observations for 150 institutions;
- the Paper 1 primary 1944–2025 panel contains 4,277 observations for 150 institutions;
- 480 of those primary-panel observations are directly observed policy records;
- Paper 2 contains 2,564 rows carrying Paper 1 PCSI/NLP measures;
- all 2,564 rows match Paper 1 on standardized institution and calendar year;
- there are zero discrepancies in mean PCSI, median PCSI, Tone, Clarity, Legal Load, sentence count, word count, source year, and carry-forward status.

The independently re-estimated Paper 2 baseline is:

- lag-1 PCSI coefficient on `ln(1 + new patent applications)`: **0.615866**;
- institution-clustered standard error: **0.523368**;
- p-value: **0.240590**;
- N: **2,115**.

The complete Paper 2 replication output was also regenerated and matched the committed verified output byte-for-byte.

## Repository structure

```text
.
├── manuscript/                 # active updated-paper draft and paper notes
├── data/                       # verified analysis data and data documentation
├── code/                       # analysis and replication code
├── replication/                # frozen audit reports and provenance material
├── results/
│   ├── tables/                 # generated manuscript tables
│   └── figures/                # generated manuscript figures
└── .github/workflows/          # automated reproducibility checks
```

## Data files

The core updated-paper dataset is `data/verified_replication_dataset.csv`.

Expected properties:

- 3,507 rows;
- 46 analysis/provenance columns;
- SHA-256: `de5377b98c1261c5de9a5b4df21efb86af04bbdce28cb3676ec37c61456fcdf6`.

The original Paper 2 merged input is retained separately when needed for exact reproduction of the legacy Paper 2 analysis.

## Reproducibility scope

The released Paper 1 materials reproduce classifier inference, calibration, aggregation, policy-in-force panel construction, and manuscript-facing analyses. They do **not** reconstruct the original BERT fine-tuning from coder-level pre-adjudication records. This limitation should remain explicit in any reproducibility statement for the updated paper.

## Development convention

The updated paper should distinguish clearly between:

1. **verified descriptive/associational results** inherited from the audited data chain;
2. **new empirical extensions and robustness analyses** developed in this repository; and
3. **causal designs**, which should only be labeled causal when identification assumptions and diagnostics support that interpretation.

## Status

Repository initialized September 25, 2026. The archived source repositories remain unchanged and serve as provenance records.
