# When Universities Rewrite Their Intellectual-Property Policies

**Policy Revisions, Policy Communication, and University Technology Transfer**

This repository is the active research, manuscript, and replication home for the university IP-policy revision paper. The September 25, 2026 25-event draft is preserved as a historical benchmark; the active manuscript now uses the fully re-reviewed **34-event documentary sample**.

## Current empirical design

The paper's main design is a **stacked revision event study**, not the older annual-PCSI regression. Each revising university is compared with contemporaneous universities that do not revise anywhere in the same `[-4,+5]` event window. The direction contrast compares revisions toward more supportive policy communication with revisions toward more restrictive communication.

The analysis remains observational. Universities choose whether and how to revise their policies, so the paper documents post-revision patterns rather than a causal effect of wording.

## Revision universe and sample construction

At the baseline `|ΔPCSI| > 0.03` threshold, the linked policy history contains **127 revisions at 78 institutions: 47 upward and 80 downward**.

The active sample-construction funnel is:

1. **127 detected revisions** — full descriptive universe;
2. **62 mechanically eligible revisions** — pass non-overlap and core-outcome-support screens;
3. **34 documentary-reviewed preferred events** — all 62 eligible pairs were reviewed under the same C/P/N comparability and A/B/C timing rules; 34 satisfy C/P plus A/B;
4. **29-event strict post-support sample** — requires at least one observed calendar year after the revision; used as a conservative sensitivity;
5. **25-event September-25 set** — retained as a historical/reproduction robustness specification;
6. **59-event rule-coded sample** — broad robustness only, not preferred because many pairs are not document-reviewed.

The preferred 34 events occur at **32 institutions: 8 upward and 26 downward**. The strict 29-event sample contains **7 upward and 22 downward**.

The complete 127-revision mechanical audit is documented in [`replication/all_127_revision_audit.md`](replication/all_127_revision_audit.md). The second-pass documentary review of the 37 mechanically eligible non-baseline candidates is documented in [`replication/manual_rereview37.md`](replication/manual_rereview37.md), with row-level coding in [`data/revision_codes_rereview37.csv`](data/revision_codes_rereview37.csv).

## Preferred headline result

For the 34-event documentary-reviewed sample, the average post-revision upward-minus-downward licensing gap is:

- **0.495 log points**
- clustered SE **0.140**
- 100,000-draw direction-label permutation **p = 0.032**
- joint pre-trend **p = 0.32**
- Benjamini-Hochberg adjustment across the five main outcomes **q = 0.159**

The contrast reflects movement in both directions: the post-period average relative to controls is **+0.279** after upward revisions and **-0.216** after downward revisions.

The stricter 29-event post-support sample gives a nearly identical licensing gap of **0.499** (SE 0.133; permutation `p = 0.026`; pre-trend `p = 0.52`; BH `q = 0.130`). Filing-margin and patent-application estimates move in the same direction but are less precise; invention disclosures do not increase.

Dropping each of the 34 preferred events one at a time leaves the licensing gap between **0.436 and 0.559**, so no single revision drives the expanded result.

## September-25 benchmark

The September 25 PDF reported 25 events (6 upward, 19 downward) and a licensing gap of 0.619 with permutation `p = 0.015`. The independently reconstructed 25-event specification is **0.6213 (SE 0.1360; exact permutation p = 0.00946)**. The small manuscript-versus-reconstruction difference is documented in [`replication/sept25_reconciliation.md`](replication/sept25_reconciliation.md) rather than tuned away.

The old 25-event specification is now a robustness benchmark, not the preferred sample.

## Why the sample was expanded

The earlier draft's main weakness was that only 25 revisions had been manually classified even though the full threshold universe contained 127 detected changes. We therefore screened all 127 mechanically and reviewed **every one of the 62 revisions that could actually enter the stacked design**. Among the 37 additional candidates, nine satisfy the same C/P comparability and A/B timing standards used by the original sample, producing the 34-event preferred set.

The 37-candidate text extract is reproducibly generated from the pinned Paper 1 sentence corpus: 21,068 sentence rows covering 71 predecessor/successor document-year keys at 33 institutions.

**Pre-submission safeguard:** the nine newly admitted second-pass documentary classifications should receive a blinded independent check by a human coauthor before journal submission. The code and manuscript contain this as a provenance safeguard; outcome estimates were not used to define documentary usability.

## Data lineage

The project combines the pinned Paper 1 measurement repository `krish533/Tech-transfer-1` at commit `25a9472b34334825b6d6c6a334f5b88eb00695b5` and the legacy Paper 2 outcome repository `krish533/tech-transfer-paper-2` at commit `88cf4a1c02540b136adb8beaa35e212625ac755e`.

The cross-repository audit established that all 2,564 rows carrying PCSI/NLP measures match the Paper 1 panel on the policy-link key, with zero mismatches in mean PCSI, median PCSI, Tone, Clarity, Legal Load, sentence count, word count, source year, and carry-forward status.

The legacy verified dataset remains [`data/verified_replication_dataset.csv`](data/verified_replication_dataset.csv) (3,507 rows × 46 columns; SHA-256 `de5377b98c1261c5de9a5b4df21efb86af04bbdce28cb3676ec37c61456fcdf6`). For the current paper, the panel fixed-effect identifier is the **149-institution `Institution_std` harmonization** in `data/merged_autm.csv`; the sparse 139-institution `Institution_pci` field is a policy-corpus matching key, not the panel identifier.

## Current code

- `code/revision_event_study.py` — panel construction, clean stacks, fixed effects, and clustered estimates.
- `code/revision_replication.py` — canonical September-25 25-event reconstruction and exact permutation benchmark.
- `code/all_revision_analysis.py` — 127-revision mechanical audit, leave-one-out/equal-event checks, continuous-magnitude diagnostics, and threshold counts.
- `code/extract_candidate_policy_text.py` — reproducible predecessor/successor text extraction for the 37 additional documentary candidates.
- `code/expanded_manual_revision_analysis.py` — constructs the 34-event and 29-event documentary samples.
- `code/final_expanded_inference.py` — publication-facing 100,000-draw permutation inference and BH adjustments.
- `code/expanded34_diagnostics.py` — event-time paths, balance, stack composition, and leave-one-out diagnostics for the preferred 34-event sample.
- `code/build_expanded_manuscript_figures.py` — manuscript figures from regenerated expanded-sample outputs.
- `code/sept25_diagnostics.py` — source-lineage and September-25 reconciliation checks.
- `code/replication.py` and `code/run_all.py` — frozen legacy annual-panel Paper 2 benchmark programs.

Annual continuous-PCSI models remain supporting evidence; they are not the main design.

## Manuscript

`manuscript/main.tex` is the active manuscript driver. The revised paper is modularized under `manuscript/updated34/`:

```text
manuscript/
├── main.tex
├── sept25_baseline.md
├── paper2_verified_starting_point.tex
└── updated34/
    ├── 00_frontmatter.tex
    ├── 01_introduction.tex
    ├── 02_related_literature.tex
    ├── 03_data.tex
    ├── 04_empirical_strategy.tex
    ├── 05_results.tex
    ├── 06_discussion_conclusion.tex
    ├── 07_references.tex
    ├── 08_appendix.tex
    └── appendix/
```

The `Build expanded manuscript` GitHub Action regenerates the preferred and strict-sample estimates, rebuilds manuscript figures, compiles the LaTeX paper, and uploads the PDF/source bundle as a workflow artifact.

## Reproducibility standard

A result is described as reproduced only when the repository regenerates it from code and data. Documentary classifications are stored separately from outcome analysis. The manuscript does not infer C/P/N or A/B/C labels from word counts merely to enlarge the preferred sample.

The Paper 1 release reproduces classifier inference, calibration, aggregation, policy-in-force panel construction, and manuscript-facing analyses. It does not reconstruct the original BERT fine-tuning from coder-level pre-adjudication records; that limitation remains part of the provenance statement.

## Interpretation rule

Keep four categories separate:

1. **34-event preferred documentary results** — active manuscript;
2. **29-event strict post-support results** — conservative sensitivity;
3. **25-event September-25 and legacy annual-panel results** — provenance/supporting evidence;
4. **causal claims** — only if a future design provides defensible identification beyond the observational revision comparison.
