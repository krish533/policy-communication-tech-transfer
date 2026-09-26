# September 25 manuscript reconciliation

This note records the independent reconstruction of the September 25, 2026 manuscript from the repository data and the pinned Paper 1 policy history. The manuscript PDF remains the authoritative source for reported values; regenerated values below are shown explicitly so small differences are not hidden.

## Structural checks reproduced exactly

The reconstruction verifies all of the following:

- AUTM panel: **3,507 institution-years**.
- Raw AUTM reporting identifiers: **253**.
- Harmonized AUTM institutions: **149**, using `Institution_std` as the institution key.
- Full Paper 1 policy-in-force panel: **4,296 rows / 150 institutions**.
- Directly observed policy-document institution-years: **481**.
- At `|ΔPCSI| > 0.03`, AUTM-linked policy histories contain **127 revisions at 78 institutions**, of which **47 are upward and 80 downward**.
- All **25 Appendix A1 main-sample revisions** match the pinned Paper 1 document sequence on institution, previous-document year, revision year, direction, and PCSI change (within the PDF's displayed rounding).
- Main event sample: **25 revisions, 6 upward and 19 downward**.
- Stacked event-study row counts reproduce the manuscript exactly: **20,181** for licenses/options, **20,277** for the filing margin, new patent applications and invention disclosures, and **19,821** for patents issued.
- FY2023 licensing audit reproduces the manuscript: median `Tot Lic/Opt Exe` = **6**, while median `Lic Iss + Opt Iss` = **29**; the reconstructed current-paper outcome therefore uses the component sum in 2023.

A separate specification audit found that the manuscript's reported event path, clustered standard error, and pre-trend test are closely reproduced when the research-size strata are terciles of each institution's **median research expenditure over the AUTM panel**. That definition is used in `code/revision_replication.py`.

## Main Table 3: PDF versus independent regeneration

| Outcome | PDF gap | Regenerated gap | PDF SE | Regenerated SE | PDF permutation p | Regenerated exact p | PDF N | Regenerated N |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Log licenses and options | 0.619 | 0.621275 | 0.136 | 0.136012 | 0.015 | 0.009458 | 20,181 | 20,181 |
| Filing margin | 0.374 | 0.380218 | 0.168 | 0.169965 | 0.155 | 0.153196 | 20,277 | 20,277 |
| Log new patent applications | 0.262 | 0.266925 | 0.182 | 0.183855 | 0.243 | 0.236025 | 20,277 | 20,277 |
| Log U.S. patents issued | 0.027 | 0.018688 | 0.222 | 0.225719 | 0.920 | 0.943970 | 19,821 | 19,821 |
| Log invention disclosures | -0.112 | -0.113293 | 0.105 | 0.105119 | 0.507 | 0.498972 | 20,277 | 20,277 |

The regenerated Benjamini-Hochberg q-values from these exact permutation p-values are approximately **0.0473, 0.3830, 0.3934, 0.9440, and 0.6237** in the corresponding outcome family. These are not substituted into the manuscript because the PDF reports a different exact-permutation count, most visibly for licensing (`p = 0.015`, BH `q = 0.075`).

## Licensing event path

With median-research-expenditure terciles, the independently regenerated upward-minus-downward path is:

- year -4: **0.197**
- year -3: **0.000**
- year -2: **0.029**
- year 0: **0.384**
- year +1: **0.543**
- year +2: **0.331**
- year +3: **0.674**
- year +4: **0.891**
- year +5: **0.905**

The regenerated joint pre-trend p-value is **0.621**, and the average post-revision comparison decomposes into **+0.287** for upward revisions relative to controls and **-0.334** for downward revisions relative to controls. These line up closely with the PDF's displayed values (pre-period approximately 0.21, 0.01, 0.03; year 0 = 0.38; years 3–5 about 0.68–0.90; pre p = 0.62; upward = 0.289; downward = -0.330).

## What remains unreconciled

The reconstruction is **near-exact but not byte-for-byte identical** to the PDF's main Table 3. Because sample sizes, the 127-revision universe, all 25 hand-reviewed transitions, the FY2023 outcome correction, and the main licensing standard error/pre-trend path reproduce, the remaining difference is small and appears to arise from a manuscript-generation detail not preserved in the earlier public replication materials. Possible locations include the exact construction of research-size strata at boundary cases, documentary timing/control exclusions for non-main revisions, or the exact permutation implementation used for the PDF.

Until the original September 25 analysis script or complete hand-coded 127-revision timing file is recovered, the repository keeps **both** values visible:

1. the PDF-reported manuscript targets in `manuscript/sept25_baseline.md`; and
2. the independently regenerated values produced by `code/revision_replication.py`.

No manuscript claim should be silently changed from 0.619 / p = 0.015 to the regenerated 0.621 / p = 0.009 without resolving that provenance gap or making a deliberate new-version decision.

## Identification

Nothing in this reconciliation strengthens the design from observational to causal. Revision direction is chosen by universities, and contemporaneous direction-specific organizational changes cannot be excluded. The appropriate interpretation remains a robust post-revision empirical pattern concentrated at the licensing margin.
