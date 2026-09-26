# Full 127-Revision Audit

This note documents the systematic audit of the complete baseline revision universe for the September 25, 2026 manuscript. The purpose is to make the path from the 127 detected policy changes to the 25 strict event-study revisions transparent and reproducible.

## Baseline revision universe

Using the pinned Paper 1 observed-document sequence and the manuscript threshold `|ΔPCSI| > 0.03`, the linked universe contains 127 revisions at 78 institutions: 47 upward and 80 downward. The 25 manuscript events remain the strict hand-reviewed main sample: 6 upward and 19 downward.

The manuscript states that 45 document pairs were hand-reviewed and 82 were rule-coded, but the current public replication materials preserve row-level manual C/P/N and A/B/C labels only for the final 25 main events. Missing documentary labels are therefore not imputed in this audit.

## Revision-by-revision mechanical screen

`code/all_revision_analysis.py` evaluates all 127 revisions using the observed successor-document year as a screening date. For each revision it records whether another qualifying revision occurs in the `[-4,+5]` window and whether the linked AUTM panel contains pre- and post-event outcome information.

Under this observed-document-year screen:

- 62 revisions pass the no-overlap and core-outcome-coverage screen;
- 25 are the existing main events;
- 37 additional non-main revisions remain potentially usable and merit documentary review;
- 65 of the 102 non-main revisions fail at least one mechanical screen under observed-document-year timing.

The 37 priority candidates contain 12 upward and 25 downward revisions.

This is a screening exercise, not a final documentary classification. For non-main events a documented adoption/effective date may differ from the observed document year, which can change overlap or outcome-window eligibility.

## Documentary source recovery

For the 37 mechanically viable non-main candidates, `code/extract_candidate_policy_text.py` reconstructs the relevant predecessor and successor source text from the pinned Paper 1 raw sentence corpus. The extraction recovers 21,068 sentence rows, 71 predecessor/successor document-year keys, and 33 institutions, including original source filenames plus cleaned sentence text.

This makes a new documentary review feasible without inferring missing historical manual labels from the outcomes. It also reveals several obvious source-composition problems (for example royalty-only pages, whole policy manuals, handbooks, or non-policy reports paired with governing IP policies) and several strong same-policy successor pairs with explicit revision dates. Those judgments should be coded in a separate review file before any expanded preferred event sample is estimated.

## Influence and weighting robustness for the main 25

### Leave-one-revision-out

The independently reconstructed full-sample licensing gap is 0.6213 log points. Dropping each of the 25 events one at a time yields gaps from 0.5565, when Stevens Institute of Technology 2014 (upward) is omitted, to 0.6928, when Albert Einstein/Yeshiva 2015 (upward) is omitted. Thus no single event generates the sign or broad magnitude of the licensing result.

### Equal-event weighting

A transparent event-level calculation gives every revision one scalar pre/post difference-in-differences contribution rather than allowing larger stacks to receive more observational weight. The upward-minus-downward gap is 0.5641 log points, with exact direction-assignment permutation p = 0.00453 (803 of 177,100 assignments at least as extreme as observed). This supports the conclusion that the main pattern is not an artifact of unequal stack sizes.

## Continuous revision magnitude

The actual signed change in PCSI contains more information than a binary upward/downward label, so the audit estimates continuous-magnitude specifications as diagnostics.

At the event level, the licensing effect rises by about 0.221 log points per +0.1 PCSI change; a 100,000-shuffle permutation gives p approximately 0.0498. The rank correlation is positive but not conventionally significant.

In the stacked specification, the average post coefficient is about 0.331 per +0.1 PCSI (clustered SE approximately 0.083). However, the joint pre-trend test rejects at conventional levels (p approximately 0.0257). Consequently the continuous-magnitude specification should be treated as an exploratory/robustness diagnostic, not as stronger causal-style evidence than the binary direction design.

## Threshold universe

| Threshold | Revisions | Institutions | Up | Down |
|---:|---:|---:|---:|---:|
| 0.020 | 156 | 87 | 60 | 96 |
| 0.025 | 139 | 84 | 52 | 87 |
| 0.030 | 127 | 78 | 47 | 80 |
| 0.040 | 103 | 67 | 38 | 65 |
| 0.050 | 83 | 55 | 31 | 52 |

These counts describe detected revisions in the full policy history; they are not counts of event-study-eligible revisions.

## Recommended empirical hierarchy

For the paper, the cleanest interpretation is:

1. **127 revisions** — the descriptive universe of meaningful communication changes;
2. **25 hand-reviewed revisions** — the strict preferred event-study sample;
3. **the manuscript's broader 59-event rule-coded sample** — an important robustness check showing that the result is not unique to the 25-event sample;
4. **leave-one-out and equal-event weighting** — influence and weighting checks;
5. **continuous ΔPCSI** — appendix diagnostic because its pre-trend is not flat.

This structure is stronger than subdividing the 25 main events into many small substantive categories.

## Generated files

`code/all_revision_analysis.py` generates the all-127 disposition table, leave-one-out results, equal-event effects, threshold counts, and a machine-readable summary. `code/extract_candidate_policy_text.py` generates the sentence-level documentary extract and metadata during CI. The large sentence extract is retained as a workflow artifact rather than committed to Git history.