# Reproducibility and pre-submission checklist

This document defines the publication-facing replication path for the revised 34-event manuscript and separates automated checks from items that require human judgment.

## Canonical environment

- Python: 3.11
- Dependencies: install the pinned versions in `requirements.txt`
- Randomization: seeds are fixed in the analysis code
- Publication-facing permutation inference: 100,000 direction-label assignments per outcome

From a clean checkout:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python code/reproduce_submission.py
```

The event-study code reconstructs the 127-revision universe from the Paper 1 observed-policy history at pinned commit `25a9472b34334825b6d6c6a334f5b88eb00695b5`. That upstream file is retrieved from an immutable commit-specific GitHub URL, so a network connection to GitHub is required for that reconstruction step.

## Publication-facing hierarchy

1. **Preferred sample:** 34 documentary-reviewed revisions, 8 upward and 26 downward.
2. **Strict support sensitivity:** 29 revisions, 7 upward and 22 downward.
3. **Frozen September 25 benchmark:** 25 revisions, retained for provenance and robustness rather than treated as the preferred revised-manuscript specification.
4. **Legacy annual-panel analysis:** supporting/provenance evidence only.

The preferred row-level stacked dataset is generated at `data/derived/final_stacked_event_dataset_expanded34.csv`; the strict sensitivity is generated at `data/derived/final_stacked_event_dataset_strict29.csv`. Repeated comparison institution-years across stacks are intentional. The independent treated-event count is the number of policy revisions, not the number of stacked rows.

## Automated checks before merge/release

A release candidate should satisfy all of the following:

- `python code/reproduce_submission.py` completes without error.
- Preferred and strict event counts are 34 and 29, respectively.
- `results/expanded_manual_sample_results.csv` contains both `expanded34` and `strict29` publication-facing results.
- Manuscript figures rebuild from generated outputs.
- The LaTeX manuscript compiles in CI.
- Frozen verified data hashes match the values enforced by `Verify frozen research materials`.
- The empirical benchmark workflow passes.
- The full-package workflow passes and emits `PACKAGE_MANIFEST.txt`, `PACKAGE_SHA256SUMS.txt`, `PYTHON_VERSION.txt`, and `PIP_FREEZE.txt`.
- A main-branch push after merge triggers a fresh full-package build.

## Human checks that automation cannot complete

These should not be marked resolved by code or CI:

- Independent human/coauthor verification of the nine second-pass documentary classifications, performed without consulting outcome estimates.
- Final author list, author order, affiliations, and author-contribution statement.
- Funding statement.
- Competing-interest/conflict-of-interest statement.
- Journal-specific data/code availability wording and any repository DOI or archival link required at submission.
- Final visual inspection of the compiled PDF, tables, figures, appendix references, and cross-references.

## Release discipline

Do not manually edit generated result CSVs, derived stacked datasets, or manuscript figures. Change source data/coding only with an explicit documented reason, then rerun the canonical replication. Keep the frozen 25-event benchmark and verified cross-repository materials unchanged for provenance.
