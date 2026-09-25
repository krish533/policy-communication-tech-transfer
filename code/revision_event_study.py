"""
September 25, 2026 revision-design replication.

Main design in the manuscript:
  * 25 hand-reviewed, dated revisions (6 upward, 19 downward)
  * clean controls with no |dPCSI| > .03 revision in [-4,+5]
  * stacked event study, event year -1 omitted
  * stack x institution FE
  * stack x year x research-size-tercile x public/private FE
  * log research expenditure control
  * institution-clustered standard errors

The script deliberately uses Institution_std (149 harmonized AUTM institutions)
for panel fixed effects. Institution_pci is only the sparse link from AUTM to
the 150-university policy corpus and must not be used as the panel identifier.
"""
from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "merged_autm.csv"
EVENTS = ROOT / "data" / "revision_codes_manual.csv"
RESULTS = ROOT / "results"
P1_COMMIT = "25a9472b34334825b6d6c6a334f5b88eb00695b5"
P1_URL = (
    "https://raw.githubusercontent.com/krish533/Tech-transfer-1/"
    f"{P1_COMMIT}/P1_replication_package/data/derived/"
    "policy_level_indices_institution_year.csv"
)
THRESHOLD = 0.03
EVENT_MIN = -4
EVENT_MAX = 5
OMITTED = -1
EVENT_TIMES = [k for k in range(EVENT_MIN, EVENT_MAX + 1) if k != OMITTED]
POST_TIMES = list(range(0, 6))
PRE_TIMES = [-4, -3, -2]


def norm(s: pd.Series) -> pd.Series:
    return (s.astype("string")
            .str.replace(r"\s+", " ", regex=True)
            .str.strip().str.casefold())


def num(s):
    return pd.to_numeric(s, errors="coerce")


def make_panel(raw: pd.DataFrame) -> pd.DataFrame:
    """Construct the September-25 harmonized AUTM panel."""
    x = pd.DataFrame(index=raw.index)
    x["institution"] = raw["Institution_std"].astype("string")
    x["year"] = num(raw["Year"])
    x["raw_id"] = raw["[ID]"].astype("string")
    x["private"] = num(raw["Private"]).fillna(0).astype(int)
    x["research_exp"] = num(raw["Tot Res Exp"])
    x["licensing_ftes"] = num(raw["Lic FTEs"])
    x["royalty_share"] = num(raw["Royalty Share"])

    x["disclosures"] = num(raw["Inv Dis Rec"])
    x["new_patent_apps"] = num(raw["New Pat App Fld"])
    x["total_patent_apps"] = num(raw["Tot Pat App Fld"])
    x["patents_issued"] = num(raw["Iss US Pat"])
    x["startups"] = num(raw["St-Ups Formed"])

    # The FY2023 total field changed definition. The manuscript uses Lic Iss + Opt Iss.
    lic_total = num(raw["Tot Lic/Opt Exe"])
    comp = num(raw["Lic Iss"]) + num(raw["Opt Iss"])
    x["licenses"] = lic_total
    x.loc[x["year"].eq(2023), "licenses"] = comp[x["year"].eq(2023)]

    for c in ["disclosures", "new_patent_apps", "total_patent_apps",
              "patents_issued", "licenses", "startups"]:
        x[f"ln_{c}"] = np.log1p(x[c])
    x["filing_margin"] = x["ln_new_patent_apps"] - x["ln_disclosures"]
    # Appendix balance values around 19 imply research expenditure is logged in dollars.
    x["ln_research_exp"] = np.where(x["research_exp"] > 0, np.log(x["research_exp"]), np.nan)
    x["ln_licensing_ftes"] = np.log1p(x["licensing_ftes"])

    # Research-size category c(i): time-invariant tercile of institution mean research spending.
    means = x.groupby("institution", observed=True)["research_exp"].mean()
    ranks = means.rank(method="first", pct=True)
    terc = pd.Series(np.minimum((ranks * 3).apply(np.ceil).astype(int) - 1, 2), index=means.index)
    x["size_tercile"] = x["institution"].map(terc).astype("Int64")

    if x["institution"].nunique() != 149:
        raise AssertionError(f"Expected 149 harmonized institutions, found {x['institution'].nunique()}")
    if x.duplicated(["institution", "year"]).any():
        raise AssertionError("Harmonized institution-year key is not unique")
    return x.sort_values(["institution", "year"]).reset_index(drop=True)


def load_p1_observed() -> pd.DataFrame:
    path = ROOT / "data" / "_p1_revision_tmp.csv"
    urllib.request.urlretrieve(P1_URL, path)
    p1 = pd.read_csv(path, low_memory=False)
    path.unlink(missing_ok=True)
    p1["Year"] = num(p1["Year"])
    p1["Mean_Tone_Score"] = num(p1["Mean_Tone_Score"])
    p1["Is_Carried_Forward"] = num(p1["Is_Carried_Forward"])
    obs = (p1[p1["Is_Carried_Forward"].eq(0)]
           .dropna(subset=["Institution", "Year", "Mean_Tone_Score"])
           .sort_values(["Institution", "Year"])
           .drop_duplicates(["Institution", "Year"], keep="last").copy())
    obs["prev_year"] = obs.groupby("Institution")["Year"].shift(1)
    obs["prev_pcsi"] = obs.groupby("Institution")["Mean_Tone_Score"].shift(1)
    obs["delta_pcsi"] = obs["Mean_Tone_Score"] - obs["prev_pcsi"]
    return obs


def revision_universe(raw: pd.DataFrame) -> pd.DataFrame:
    """Recover all 127 threshold revisions from the full P1 observed-document sequence."""
    obs = load_p1_observed()
    # Crosswalk from P1 corpus name to the 149-institution AUTM harmonization.
    cw = raw[["Institution_pci", "Institution_std"]].dropna().copy()
    cw["p1_norm"] = norm(cw["Institution_pci"])
    # A P1 name should map to one harmonized AUTM institution; mode is robust to repeated rows.
    cw = (cw.groupby("p1_norm", observed=True)["Institution_std"]
          .agg(lambda z: z.value_counts().index[0]).rename("institution").reset_index())
    obs["p1_norm"] = norm(obs["Institution"])
    z = obs.merge(cw, on="p1_norm", how="inner")
    rev = z[z["delta_pcsi"].abs() > THRESHOLD].copy()
    rev = rev.rename(columns={"Year": "revision_year"})
    rev["direction"] = np.where(rev["delta_pcsi"] > 0, "up", "down")
    out = rev[["institution", "Institution", "prev_year", "revision_year",
               "delta_pcsi", "direction"]].sort_values(["institution", "revision_year"])
    if len(out) != 127 or out["institution"].nunique() != 78:
        raise AssertionError(
            f"Expected 127 threshold revisions at 78 linked institutions; got {len(out)} / {out['institution'].nunique()}"
        )
    return out.reset_index(drop=True)


def load_main_events() -> pd.DataFrame:
    e = pd.read_csv(EVENTS)
    e = e[e["main_sample"].eq(1)].copy()
    e["event_id"] = np.arange(len(e))
    e["sign"] = np.where(e["direction"].eq("up"), 1.0, -1.0)
    if (len(e), int((e.sign > 0).sum()), int((e.sign < 0).sum())) != (25, 6, 19):
        raise AssertionError("Main event file must contain 25 events: 6 upward, 19 downward")
    return e


def make_stacks(panel: pd.DataFrame, universe: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    all_inst = set(panel["institution"].dropna().astype(str))
    rows = []
    for _, e in events.iterrows():
        E = int(e.revision_year)
        treated = str(e.institution)
        # Every Appendix-A1 name is the AUTM harmonized Institution_std name.
        if treated not in all_inst:
            raise AssertionError(f"Treated institution not in harmonized AUTM panel: {treated}")
        lo, hi = E + EVENT_MIN, E + EVENT_MAX
        bad = set(universe.loc[universe.revision_year.between(lo, hi), "institution"].astype(str))
        controls = all_inst - bad
        keep = controls | {treated}
        s = panel[panel["institution"].astype(str).isin(keep) & panel["year"].between(lo, hi)].copy()
        s["stack"] = int(e.event_id)
        s["event_year"] = E
        s["event_time"] = s["year"] - E
        s["treated"] = (s["institution"].astype(str) == treated).astype(int)
        s["event_sign"] = float(e.sign)
        s["direction"] = e.direction
        rows.append(s)
    return pd.concat(rows, ignore_index=True)


def _demean(arr: np.ndarray, groups: list[np.ndarray], max_iter=500, tol=1e-11) -> np.ndarray:
    """Alternating projection for multiple high-dimensional fixed effects."""
    out = arr.astype(float, copy=True)
    if out.ndim == 1:
        out = out[:, None]
    for _ in range(max_iter):
        old = out.copy()
        for codes in groups:
            ng = int(codes.max()) + 1
            counts = np.bincount(codes, minlength=ng).astype(float)
            for j in range(out.shape[1]):
                sums = np.bincount(codes, weights=out[:, j], minlength=ng)
                means = sums / counts
                out[:, j] -= means[codes]
        if np.nanmax(np.abs(out - old)) < tol:
            break
    return out


def _cluster_cov(X, resid, clusters):
    n, k = X.shape
    xtx_inv = np.linalg.pinv(X.T @ X)
    _, gcodes = np.unique(clusters, return_inverse=True)
    G = int(gcodes.max()) + 1
    meat = np.zeros((k, k))
    for g in range(G):
        idx = gcodes == g
        score = X[idx].T @ resid[idx]
        meat += np.outer(score, score)
    cov = xtx_inv @ meat @ xtx_inv
    if G > 1 and n > k:
        cov *= (G / (G - 1)) * ((n - 1) / (n - k))
    return cov


def fit_outcome(stacks: pd.DataFrame, outcome: str):
    df = stacks.copy()
    dcols, scols = [], []
    for k in EVENT_TIMES:
        tag = f"m{abs(k)}" if k < 0 else f"p{k}"
        d = f"D_{tag}"
        s = f"DS_{tag}"
        df[d] = ((df.treated == 1) & (df.event_time == k)).astype(float)
        df[s] = df[d] * df.event_sign
        dcols.append(d); scols.append(s)
    xcols = dcols + scols + ["ln_research_exp"]
    need = [outcome, "institution", "stack", "year", "size_tercile", "private"] + xcols
    q = df[need].dropna().copy()

    # Fixed effects are exactly those stated in the manuscript.
    fe1 = pd.factorize(q["stack"].astype(str) + "|" + q["institution"].astype(str))[0]
    fe2 = pd.factorize(q["stack"].astype(str) + "|" + q["year"].astype(str) + "|" +
                       q["size_tercile"].astype(str) + "|" + q["private"].astype(str))[0]
    y = q[outcome].to_numpy(float)
    X = q[xcols].to_numpy(float)
    Z = np.column_stack([y, X])
    rz = _demean(Z, [fe1, fe2])
    yr = rz[:, 0]
    Xr = rz[:, 1:]
    # Drop numerically empty columns only as a guard; all expected event cells should exist.
    keep = np.sqrt((Xr ** 2).sum(axis=0)) > 1e-10
    if not keep.all():
        bad = [c for c, ok in zip(xcols, keep) if not ok]
        raise AssertionError(f"Absorbed regressors have no residual variation: {bad}")
    beta = np.linalg.pinv(Xr.T @ Xr) @ (Xr.T @ yr)
    resid = yr - Xr @ beta
    cov = _cluster_cov(Xr, resid, q["institution"].astype(str).to_numpy())
    b = pd.Series(beta, index=xcols)

    # Linear-combination helper.
    def combo(weights):
        w = np.zeros(len(xcols))
        for name, val in weights.items():
            w[xcols.index(name)] = val
        est = float(w @ beta)
        se = float(np.sqrt(max(w @ cov @ w, 0)))
        return est, se

    post_gap_w = {}
    post_up_w = {}
    post_dn_w = {}
    for k in POST_TIMES:
        tag = f"p{k}"
        post_gap_w[f"DS_{tag}"] = 2 / len(POST_TIMES)
        post_up_w[f"D_{tag}"] = 1 / len(POST_TIMES)
        post_up_w[f"DS_{tag}"] = 1 / len(POST_TIMES)
        post_dn_w[f"D_{tag}"] = 1 / len(POST_TIMES)
        post_dn_w[f"DS_{tag}"] = -1 / len(POST_TIMES)
    gap, gap_se = combo(post_gap_w)
    up, up_se = combo(post_up_w)
    down, down_se = combo(post_dn_w)

    path = []
    for k in EVENT_TIMES:
        tag = f"m{abs(k)}" if k < 0 else f"p{k}"
        est, se = combo({f"DS_{tag}": 2.0})
        path.append({"event_time": k, "gap": est, "se": se})

    # Wald test of three pre-period direction interactions.
    idx = [xcols.index(f"DS_m{abs(k)}") for k in PRE_TIMES]
    bb = beta[idx]
    vv = cov[np.ix_(idx, idx)]
    stat = float(bb.T @ np.linalg.pinv(vv) @ bb)
    try:
        from scipy.stats import chi2
        pre_p = float(chi2.sf(stat, len(idx)))
    except Exception:
        pre_p = np.nan

    return {
        "outcome": outcome,
        "n": int(len(q)),
        "clusters": int(q["institution"].nunique()),
        "gap": gap, "gap_se": gap_se,
        "up": up, "up_se": up_se,
        "down": down, "down_se": down_se,
        "pre_p": pre_p,
        "path": path,
        "beta": b.to_dict(),
    }


def main(validate=False):
    raw = pd.read_csv(RAW, low_memory=False)
    panel = make_panel(raw)
    universe = revision_universe(raw)
    events = load_main_events()
    stacks = make_stacks(panel, universe, events)

    print("SEPT25 PANEL", len(panel), "rows", panel.institution.nunique(), "institutions")
    print("REVISION UNIVERSE", len(universe), "revisions", universe.institution.nunique(), "institutions")
    print("MAIN EVENTS", len(events), "up", int((events.sign > 0).sum()), "down", int((events.sign < 0).sum()))
    print("STACKED RAW ROWS", len(stacks))

    specs = [
        ("ln_licenses", 0.619, 0.136, 20181),
        ("filing_margin", 0.374, 0.168, 20277),
        ("ln_new_patent_apps", 0.262, 0.182, 20277),
        ("ln_patents_issued", 0.027, 0.222, 19821),
        ("ln_disclosures", -0.112, 0.105, 20277),
    ]
    out = []
    for y, target_b, target_se, target_n in specs:
        r = fit_outcome(stacks, y)
        out.append(r)
        print("RESULT", y,
              "gap", round(r["gap"], 6), "se", round(r["gap_se"], 6),
              "pre_p", round(r["pre_p"], 6),
              "up", round(r["up"], 6), "down", round(r["down"], 6),
              "N", r["n"], "clusters", r["clusters"],
              "TARGET", target_b, target_se, target_n)
        print("PATH", y, [(z["event_time"], round(z["gap"], 4)) for z in r["path"]])

    RESULTS.mkdir(parents=True, exist_ok=True)
    # JSON excludes full coefficient dictionaries to keep the diagnostic compact.
    compact = [{k: v for k, v in r.items() if k != "beta"} for r in out]
    (RESULTS / "sept25_eventstudy_diagnostic.json").write_text(
        json.dumps(compact, indent=2) + "\n", encoding="utf-8")

    if validate:
        assert len(panel) == 3507 and panel.institution.nunique() == 149
        assert len(universe) == 127 and universe.institution.nunique() == 78
        assert len(events) == 25 and (events.sign > 0).sum() == 6
        # Structural N checks are intentionally reported before they become hard assertions;
        # exact reproduction requires confirming the manuscript's size-tercile construction.


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()
    main(validate=args.validate)
