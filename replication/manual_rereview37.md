# Manual documentary re-review of the 37 mechanically eligible revisions

This file records a second-pass documentary review of the 37 revisions that were **not** in the September 25 main sample but passed the mechanical screen for (i) no other threshold revision by the same institution inside the event window and (ii) observable core outcomes around the observed-document year.

The review applies the manuscript's definitions directly to the predecessor and successor policy text extracted from the pinned Paper 1 corpus (`25a9472b34334825b6d6c6a334f5b88eb00695b5`). It does not use AUTM outcomes to decide document usability.

## Coding rules

Comparability follows the September 25 manuscript:

- `C`: same governing IP or patent policy before and after;
- `P`: partially comparable, including excerpt/full-policy comparisons, campus/governing-board comparisons, or mixed but substantively overlapping IP-policy content;
- `N`: not comparable, including royalty-only pages, audit reports, general manuals, unrelated policies, or other documents that do not form a matched governing-policy pair.

Timing also follows the manuscript:

- `A`: adoption/revision date is stated and no intervening version is documented, or the two documents are at most two years apart;
- `B`: an adoption/effective/revision date is stated but the document provides no predecessor revision history;
- `C`: intervening versions are documented or no usable adoption/revision date is stated.

A pair is marked `usable_documentary_pair=True` only when comparability is `C/P` and timing is `A/B`. The earlier mechanical overlap/outcome screen has already been satisfied for all 37 rows.

## Result of the re-review

Of the 37 candidate pairs:

- **9** satisfy the manuscript's documentary rule (`C/P` plus timing `A/B`);
- **28** do not;
- 6 of the 9 new usable pairs are coded at high confidence and 3 at medium confidence;
- the 9 new usable pairs contain **2 upward and 7 downward** revisions.

Appending these nine to the existing 25-event sample gives an **expanded 34-event hand-reviewed sample: 8 upward and 26 downward**. The expanded set is treated as a robustness/re-review sample rather than silently replacing the frozen September 25 baseline.

| Institution | Prev. doc. | Revised | Direction | Comp. | Timing | Event year | Confidence |
| --- | ---: | ---: | --- | --- | --- | ---: | --- |
| Texas A&M University System | 2001 | 2006 | down | C | A | 2006 | high |
| Thomas Jefferson University | 1998 | 2000 | down | P | A | 2000 | medium |
| Ball State University | 2008 | 2013 | down | P | B | 2013 | medium |
| University of Pittsburgh | 2005 | 2021 | up | P | A | 2021 | high |
| University of Arkansas Fayetteville | 1986 | 2001 | down | C | A | 2001 | high |
| Yale University | 1998 | 2023 | down | C | B | 2023 | high |
| Washington State University (WSU) | 2016 | 2023 | up | P | B | 2023 | medium |
| Virginia Tech (Virginia Polytechnic Institute) | 2008 | 2013 | down | C | A | 2013 | high |
| Brown University | 2005 | 2021 | down | P | B | 2021 | medium |

The complete 37-row coding, including source-based rationales and pre/post data support, is in `data/revision_codes_rereview37.csv`.

## Expanded-sample estimates

The expanded 34-event sample was run through the same stacked specification as the canonical paper, using the median-research-expenditure tercile construction used by the independently reproduced September 25 specification. For these larger samples, direction inference uses 20,000 Monte Carlo assignments preserving the observed number of upward events, consistent with the manuscript's convention for larger alternative samples.

| Outcome | Up-minus-down gap | Clustered SE | Permutation p | Pre-trend p | Upward vs. controls | Downward vs. controls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Log licenses/options | **0.495** | 0.140 | **0.031** | 0.320 | 0.279 | -0.216 |
| Filing margin | 0.392 | 0.155 | 0.099 | 0.753 | 0.143 | -0.249 |
| Log new patent applications | 0.260 | 0.175 | 0.206 | 0.891 | 0.136 | -0.124 |
| Log patents issued | 0.137 | 0.190 | 0.538 | 0.470 | 0.171 | 0.034 |
| Log invention disclosures | -0.132 | 0.095 | 0.382 | 0.401 | -0.007 | 0.124 |

The central empirical pattern therefore survives the broader documentary review. Relative licensing remains higher after upward than downward revisions, the estimate remains concentrated at the licensing margin, and the joint pre-period test does not reject for licensing. The point estimate is smaller than in the 25-event baseline (roughly 0.50 rather than 0.62), which is a useful sign that expansion weakens rather than mechanically amplifies the headline result.

## Stricter post-outcome support sensitivity

Yale and Washington State are dated in 2023, the final AUTM year. They satisfy the manuscript's stated documentary rule but have no subsequent calendar-year AUTM observation. Thomas Jefferson and Ball State also have only one treated post-window observed panel year because of sparse AUTM reporting. The existing September 25 sample itself contains Brown University's 2005 event with only one treated post-window core-outcome year, so a stricter support rule should be applied uniformly rather than only to the new events.

We therefore also impose a uniform sensitivity requiring at least **two treated institution core-outcome panel years in event times 0 through +5**, guaranteeing at least one observed year beyond event year zero. This removes five events from the combined 34, including one original baseline event, and leaves **29 events: 7 upward and 22 downward**.

| Outcome | Up-minus-down gap | Clustered SE | Permutation p | Pre-trend p |
| --- | ---: | ---: | ---: | ---: |
| Log licenses/options | **0.499** | 0.133 | **0.027** | 0.517 |
| Filing margin | 0.361 | 0.158 | 0.123 | 0.676 |
| Log new patent applications | 0.167 | 0.177 | 0.394 | 0.858 |
| Log patents issued | 0.122 | 0.203 | 0.602 | 0.347 |
| Log invention disclosures | -0.194 | 0.098 | 0.204 | 0.491 |

The licensing pattern is essentially unchanged under this stricter support requirement.

Machine-readable results are stored in `results/expanded_manual_sample_results.csv`; the analysis is generated by `code/expanded_manual_revision_analysis.py`.

## Why many apparently large PCSI changes are excluded

Several of the largest changes are document-composition changes rather than clean revisions to the same governing policy. Examples include an annual royalty audit followed by an IP policy, a royalty-sharing page followed by a full IP policy, and an IP policy followed by a university-wide manual. These are precisely the cases in which treating every observed-document PCSI jump as a policy revision would be misleading.

Other pairs are substantively comparable but cannot be cleanly dated. In several later documents, revision histories explicitly reveal intervening versions that are absent from the corpus. Those pairs are timing tier C even when their text is highly similar.

## Interpretation

This re-review materially strengthens the sample-construction argument but does **not** convert the paper into a causal design. Universities choose both whether and how to revise their policies. The expanded-sample exercise is best presented as evidence that the licensing pattern is not an artifact of the original 25 hand-reviewed pairs or the six original upward events.

## Reproducibility

The documentary coding is intentionally stored separately from the outcome analysis. Outcome regressions read the review file rather than reconstructing C/P/N or A/B/C from word counts or filename heuristics. The policy text used for review can be regenerated by `code/extract_candidate_policy_text.py` from the pinned Paper 1 sentence corpus. GitHub Actions rerun the canonical 25-event benchmark, full 127-revision audit, document extraction, and the expanded hand-reviewed samples; the validation run completed successfully.
