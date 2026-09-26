"""Extract sentence-level source text for the 37 documentary-review candidates.

Downloads the pinned Paper 1 sentence corpus, then keeps only institution/document-year
pairs that form a mechanically viable non-main revision in the all-127 audit. The output
is used to review comparability and timing evidence without silently imputing those labels.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
AUDIT = RESULTS / "all_127_revision_disposition.csv"
P1_COMMIT = "25a9472b34334825b6d6c6a334f5b88eb00695b5"
RAW_URL = (
    "https://raw.githubusercontent.com/krish533/Tech-transfer-1/"
    f"{P1_COMMIT}/P1_replication_package/data/raw/"
    "policy_sentences_cleaned_combined.csv"
)


def norm(s: pd.Series) -> pd.Series:
    return (s.astype("string").str.replace(r"\s+", " ", regex=True)
            .str.strip().str.casefold())


def main():
    audit = pd.read_csv(AUDIT)
    cand = audit[audit["priority_for_full_manual_review"].eq(True)].copy()
    if len(cand) != 37:
        raise AssertionError(f"Expected 37 documentary-review candidates, got {len(cand)}")

    # P1 names are the correct names for matching the P1 sentence corpus.
    wanted = set()
    for _, r in cand.iterrows():
        for y in [r["prev_year"], r["revision_year"]]:
            if pd.notna(y):
                wanted.add((str(r["Institution"]).strip().casefold(), int(float(y))))

    tmp = RESULTS / "_policy_sentences_raw.csv"
    urllib.request.urlretrieve(RAW_URL, tmp)

    kept = []
    cols = None
    for chunk in pd.read_csv(tmp, low_memory=False, chunksize=25000):
        if cols is None:
            cols = list(chunk.columns)
        if "Institution" not in chunk.columns or "Year" not in chunk.columns:
            raise AssertionError(f"Unexpected P1 raw columns: {chunk.columns.tolist()}")
        inst = norm(chunk["Institution"])
        year = pd.to_numeric(chunk["Year"], errors="coerce")
        mask = pd.Series(False, index=chunk.index)
        # only 74 or fewer document keys, so this is inexpensive and transparent
        for n, y in wanted:
            mask |= inst.eq(n) & year.eq(y)
        if mask.any():
            kept.append(chunk.loc[mask].copy())
    tmp.unlink(missing_ok=True)
    out = pd.concat(kept, ignore_index=True) if kept else pd.DataFrame(columns=cols or [])

    # Preserve all source columns; this keeps any source filename/url/date metadata that exists.
    out.to_csv(RESULTS / "candidate_policy_sentence_extract.csv", index=False)

    obj_cols = [c for c in out.columns if str(out[c].dtype) in ("object", "string")]
    metadata = {
        "p1_source_commit": P1_COMMIT,
        "candidate_revisions": int(len(cand)),
        "wanted_document_keys": int(len(wanted)),
        "matched_sentence_rows": int(len(out)),
        "matched_institutions": int(out["Institution"].nunique()) if len(out) else 0,
        "matched_document_keys": int(out[["Institution", "Year"]].drop_duplicates().shape[0]) if len(out) else 0,
        "columns": list(out.columns),
        "object_columns": obj_cols,
        "unique_document_keys": (
            out[["Institution", "Year"]].drop_duplicates().sort_values(["Institution", "Year"])
            .astype(str).to_dict(orient="records") if len(out) else []
        ),
    }
    (RESULTS / "candidate_policy_sentence_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print("CANDIDATE TEXT METADATA", json.dumps(metadata, sort_keys=True))


if __name__ == "__main__":
    main()
