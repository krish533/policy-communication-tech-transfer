# September 25, 2026 manuscript baseline

This file records the authoritative empirical specification and manuscript state represented by the user-supplied PDF `sept25tt2.pdf`.

- PDF title: **When Universities Rewrite Their Intellectual-Property Policies: Policy Revisions, Policy Communication, and University Technology Transfer**
- Manuscript date: **September 2026**
- PDF SHA-256: `950c4cecbcdbc1b59c714d9554043da9c5528a632aa6bb65874f17b81ed2d6a3`
- PDF length: 30 pages

The PDF, rather than the earlier annual-PCSI draft, is the substantive baseline for further revisions in this repository.

## Abstract baseline

Universities regularly rewrite the intellectual-property policies that govern invention disclosure, ownership, and commercialization, yet little is known about what follows these ordinary revisions. The paper dates revisions in the observed policy histories of U.S. research universities, classifies their direction with the Policy Communication Stance Index (PCSI) developed in the companion measurement paper, and compares revising universities with contemporaneous non-revisers. Revisions toward more supportive language are followed by more licensing than revisions toward more restrictive language, with no difference beforehand, while invention disclosures do not respond. Annual panel estimates are consistent but imprecise. Because universities choose how to revise, the evidence documents where post-revision change concentrates rather than establishing causal effects.

Keywords: university technology transfer; intellectual-property policy; technology-transfer offices; licensing; policy revisions.

JEL: O31, O34, O38, I23, C23.

## Data baseline

Policy corpus:

- 519 IP and patent policy documents;
- 150 U.S. research universities;
- 1944–2025;
- 481 institution-year document records;
- 87,160 sentences.

Technology-transfer outcomes:

- AUTM Licensing Activity Survey, 1991–2023;
- 253 reporting identifiers harmonized to 149 institutions;
- 3,507 institution-year records;
- 2,564 annual observations with policy-in-force PCSI;
- 89.3% of annual PCSI values are carried forward;
- within-institution share of annual PCSI variance: 0.30.

Primary outcomes are licenses and options executed, invention disclosures, new U.S. patent applications, U.S. patents issued, and the filing margin

`log(1 + new patent applications) - log(1 + invention disclosures)`.

Startups are supplementary. Licensing income is excluded because reported units are inconsistent across survey years. For FY2023, the PDF uses licenses issued plus options issued because the survey total field no longer has the same definition as in prior years.

## Revision sample

Baseline revision threshold: `|ΔPCSI| > 0.03`.

At that threshold the linked policy history contains:

- 127 revisions at 78 AUTM-linked institutions;
- 45 hand-reviewed document pairs;
- 82 rule-coded-only pairs;
- 82 comparable or partially comparable pairs (C/P);
- 49 with documented timing (tier A/B);
- 25 revisions entering the main estimates;
- 6 upward and 19 downward revisions;
- revision years 1994–2021.

The 25 main events are committed separately in `data/revision_codes_manual.csv` exactly as listed in Appendix Table A1 of the PDF.

Comparability codes:

- `C`: same governing IP/patent policy before and after;
- `P`: partially comparable;
- `N`: not comparable.

Timing tiers:

- `A`: adoption date stated and no intervening version documented, or documents at most two years apart;
- `B`: adoption date stated but no revision history;
- `C`: intervening versions documented or no date stated.

The main sample uses C/P pairs in timing tiers A/B, requires no other revision by the same institution within the event window, and requires outcomes before and after the revision.

## Main empirical design

The principal design is a **stacked event study / stacked difference-in-differences**, not the legacy annual-PCSI TWFE regression.

For each event `e` at institution `i(e)` in documented revision year `E_e`, construct a stack containing the revising institution and institutions with no revision anywhere in `[E_e - 4, E_e + 5]`. Pool the stacks and estimate event-time effects with:

- stack × institution fixed effects;
- stack × year × research-size-tercile × public/private fixed effects;
- log research expenditure as a control;
- institution-clustered standard errors;
- year `-1` omitted.

Direction is coded `S_e = +1` for upward revisions and `S_e = -1` for downward revisions. The headline estimand is the average over event years 0–5 of the upward-minus-downward difference.

Preferred inference for the main sample is an exact permutation test on revision direction. With 25 events and 6 upward revisions there are exactly `C(25, 6) = 177,100` assignments. For larger alternative samples, the paper uses 20,000 random assignments preserving the number of upward events.

This design is deliberately described as observational. Revision direction is chosen by universities, so the design does not eliminate contemporaneous organizational changes that differ by direction.

## Headline results to reproduce

Main Table 3:

| Outcome | Up-minus-down gap | Clustered SE | Permutation p | BH q | Pre p | Upward vs controls | Downward vs controls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Log licenses and options | 0.619 | 0.136 | 0.015 | 0.075 | 0.62 | 0.289 | -0.330 |
| Filing margin | 0.374 | 0.168 | 0.155 | 0.388 | 0.63 | 0.166 | -0.207 |
| Log new patent applications | 0.262 | 0.182 | 0.243 | 0.405 | 0.50 | 0.151 | -0.111 |
| Log U.S. patents issued | 0.027 | 0.222 | 0.920 | 0.920 | 0.19 | 0.120 | 0.093 |
| Log invention disclosures | -0.112 | 0.105 | 0.507 | 0.634 | 0.37 | -0.015 | 0.096 |

The licensing result is the headline empirical pattern. The filing margin and new applications move in the same direction but are imprecise. Invention disclosures do not respond, which locates the post-revision pattern downstream of faculty entry into the TTO process.

## Revision-content result

Across all 127 threshold revisions, downward revisions add conflict-of-interest language in 32–33% of cases versus 13% of upward revisions (Fisher p = 0.019). In the 25-event main sample the corresponding comparison is 37% versus 0% (p = 0.137). These are keyword-presence comparisons and do not establish the legal content of provisions.

## Annual-panel supporting evidence

The annual harmonized-institution panel is supporting evidence only. The PDF reports:

- filing margin: lag 1 = 0.939 (SE 0.505; p = 0.065), lag 2 = 1.201 (SE 0.520; p = 0.023);
- licenses/options: lag 1 = 0.596 (SE 0.452);
- disclosures are negative at all lags shown;
- no lag-1 coefficient survives BH adjustment across the six outcomes (q = 0.345).

These estimates differ from the legacy Paper 2 benchmark because the September 25 paper harmonizes 253 AUTM reporting identifiers to 149 institutions and audits the outcome series.

## Robustness targets

Main licensing-gap robustness reported in the PDF:

- comparable pairs only: 0.510, permutation p = 0.078;
- timing tier A only: 0.457, p = 0.133;
- all revisions including rule-coded: 0.419, p = 0.006 (20,000-draw Monte Carlo);
- PCSI change recomputed without conflict-of-interest sentences: 0.653, p = 0.010;
- placebo dated six years early: 0.178, p = 0.488;
- dated one year early: 0.394, p = 0.060;
- dated one year late: 0.312, p = 0.289.

Threshold sensitivity for licensing:

- 0.020: 0.659, exact p = 0.012;
- 0.025: 0.647, exact p = 0.007;
- 0.030: 0.619, exact p = 0.015;
- 0.040: 0.650, exact p = 0.006;
- 0.050: 0.642, exact p = 0.038.

The leave-one-revision-out licensing gap ranges from 0.55 to 0.69.

## Identification language that must be preserved

Do **not** describe this paper as establishing causal effects. The manuscript's preferred interpretation is:

- the revision design provides a structured within-university comparison around documented policy changes;
- pre-revision paths are informative but low-powered;
- upward and downward revision direction is not randomly assigned;
- upward revisions start from substantially lower prior PCSI;
- contemporaneous leadership, staffing, budget, or organizational changes cannot be ruled out;
- the result is a robust post-revision empirical pattern concentrated at the licensing margin.

## Appendix map

- Appendix A: revision sample and coding procedure;
- Appendix B: threshold sensitivity;
- Appendix C: revision-direction balance and covariate interactions;
- Appendix D: leave-one-revision-out influence;
- Appendix E: annual panel and revision-timing checks;
- Appendix F: startup-series audit and supplementary estimates.

## Repository reconciliation rule

From this branch onward:

1. `data/revision_codes_manual.csv` is the canonical 25-event main sample unless documentary re-review changes it explicitly.
2. New main-paper code belongs in `code/revision_event_study.py` and related revision-design scripts.
3. `code/replication.py` remains the **legacy Paper 2 annual-panel benchmark** and should not be silently edited to stand in for the September 25 design.
4. Results generated for the September 25 design belong under `results/` and must be traceable to code.
5. Any difference between regenerated values and the PDF must be documented before changing manuscript claims.
