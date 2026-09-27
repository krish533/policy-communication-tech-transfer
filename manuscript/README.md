# Manuscript

`main.tex` is now the active manuscript driver for the **expanded 34-event documentary specification** of *When Universities Rewrite Their Intellectual-Property Policies: Policy Revisions, Policy Communication, and University Technology Transfer*.

The September 25, 2026 25-event paper is preserved as a historical empirical benchmark in `sept25_baseline.md`; it is no longer the preferred sample. `paper2_verified_starting_point.tex` remains the frozen legacy annual-panel manuscript.

## Active manuscript structure

The active paper is modularized under `updated34/`:

- `00_frontmatter.tex` — revised abstract and keywords;
- `01_introduction.tex` — 127 → 62 → 34 → 29 sample-construction framing and updated headline result;
- `02_related_literature.tex` — literature and conceptual motivation;
- `03_data.tex` — AUTM/policy data and complete documentary-screening procedure;
- `04_empirical_strategy.tex` — stacked event study and permutation inference;
- `05_results.tex` — preferred 34-event estimates, strict 29-event sensitivity, historical 25-event benchmark, annual supporting evidence;
- `06_discussion_conclusion.tex` — interpretation, limitations, and conclusion;
- `07_references.tex` — references;
- `08_appendix.tex` — appendix wrapper;
- `appendix/` — preferred event list, stack composition, event-time paths, strict sample, balance, leave-one-out estimates, annual/outcome audits, and provision coding.

The preferred sample contains **34 documentary-reviewed revisions (8 upward / 26 downward)**. The stricter post-support sensitivity contains **29 events (7 upward / 22 downward)**. The reproduced September-25 25-event specification remains in the results as a robustness/provenance benchmark.

## Build

The `Build expanded manuscript` GitHub Action regenerates the expanded estimates, builds the event-study figures, compiles `main.tex`, and uploads the manuscript PDF plus source/results as a workflow artifact.

## Pre-submission safeguard

The nine newly admitted second-pass C/P/N and A/B/C documentary classifications should receive an independent blinded check by a human coauthor before journal submission. The row-level decisions and rationales are preserved in `../data/revision_codes_rereview37.csv`; outcome estimates were not used to decide documentary usability.
