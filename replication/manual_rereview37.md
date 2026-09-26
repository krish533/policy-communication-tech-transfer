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

If these nine were appended to the existing hand-reviewed 25-event sample without any other change, the documentary sample would contain **34 events: 8 upward and 26 downward**. This expanded set should be treated as a robustness / re-review sample until its estimates and influence diagnostics are examined; it does not silently replace the September 25 25-event baseline.

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

The complete 37-row coding, including short source-based rationales and pre/post data support, is in `data/revision_codes_rereview37.csv`.

## Important late-event sensitivity

Yale and Washington State are dated in 2023, the final AUTM year. They satisfy the manuscript's stated C/P plus A/B documentary rule and have an event-year outcome, but they do **not** have a full calendar year after the revision in the AUTM panel. Thomas Jefferson and Ball State also have only one observed post-window panel year because of sparse AUTM reporting. For a stronger paper, estimates should therefore be shown both:

1. using the manuscript's original outcome-support rule; and
2. under a stricter sensitivity requiring at least one observed calendar year after the event.

The stricter rule is a sensitivity check, not a retroactive redefinition of the September 25 sample, because the existing main sample itself contains at least one event with only one observed post-window panel year.

## Why many apparently large PCSI changes are excluded

Several of the largest changes are document-composition changes rather than clean revisions to the same governing policy. Examples include an annual royalty audit followed by an IP policy, a royalty-sharing page followed by a full IP policy, and an IP policy followed by a university-wide manual. These are precisely the cases in which treating every observed-document PCSI jump as a policy revision would be misleading.

Other pairs are substantively comparable but cannot be cleanly dated. In several later documents, revision histories explicitly reveal intervening versions that are absent from the corpus. Those pairs are timing tier C even when their text is highly similar.

## Reproducibility

The documentary coding is intentionally stored separately from the outcome analysis. Outcome regressions should read this file rather than reconstructing C/P/N or A/B/C from word counts or filename heuristics. The policy text used for review can be regenerated by `code/extract_candidate_policy_text.py` from the pinned Paper 1 sentence corpus.
