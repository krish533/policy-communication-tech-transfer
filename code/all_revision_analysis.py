"""Audit the full 127-revision universe and stress-test the 25-event result.

This script deliberately separates facts we can reconstruct from the public data from
manual documentary classifications that are not preserved row-by-row in the current repo.
It produces:
  * a row-level disposition table for all 127 baseline revisions;
  * mechanical overlap/outcome-coverage diagnostics and a documentary-review queue;
  * leave-one-revision-out estimates for the 25 hand-reviewed events;
  * equal-event-weighted event-level effects with exact direction permutation inference;
  * a continuous signed-delta-PCSI stacked specification; and
  * threshold-universe counts at 0.02, 0.025, 0.03, 0.04, 0.05.

The 25 main events remain the manuscript's hand-reviewed sample. For the other 102
revisions, this script does NOT invent C/P/N or A/B/C documentary labels. Those labels
require the underlying policy documents / preserved manual coding.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, t as student_t, spearmanr

import revision_event_study as core
import revision_replication as canon

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def p1_observed_with_metadata() -> pd.DataFrame:
    p1 = core.load_p1_observed().copy()
    # Preserve the observed-document year separately from any hand-documented adoption year.
    p1 = p1.sort_values(["Institution", "Year"]).copy()
    # Bring forward document-level metadata when available.
    for col in ["n_words", "n_sentences", "Mean_Tone_Score"]:
        if col in p1.columns:
            p1[f"prev_{col}"] = p1.groupby("Institution", observed=True)[col].shift(1)
    return p1


def build_all_127(raw: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    universe = core.revision_universe(raw).copy()
    events = core.load_main_events().copy()
    p1 = p1_observed_with_metadata()

    # Crosswalk P1 names to harmonized AUTM institution names, same logic as core.revision_universe.
    cw = raw[["Institution_pci", "Institution_std"]].dropna().copy()
    cw["p1_norm"] = core.norm(cw["Institution_pci"])
    cw = (cw.groupby("p1_norm", observed=True)["Institution_std"]
          .agg(lambda z: z.value_counts().index[0]).rename("institution").reset_index())
    p1["p1_norm"] = core.norm(p1["Institution"])
    pm = p1.merge(cw, on="p1_norm", how="inner")
    pm = pm[pm["delta_pcsi"].abs() > core.THRESHOLD].copy()
    keep_cols = ["institution", "Institution", "prev_year", "Year", "delta_pcsi"]
    for c in ["n_words", "prev_n_words", "n_sentences", "prev_n_sentences",
              "Mean_Tone_Score", "prev_Mean_Tone_Score"]:
        if c in pm.columns:
            keep_cols.append(c)
    meta = pm[keep_cols].rename(columns={"Year": "revision_year"})

    z = universe.merge(meta, on=["institution", "Institution", "prev_year", "revision_year", "delta_pcsi"],
                       how="left", validate="one_to_one")
    z["observed_doc_year"] = z["revision_year"].astype(int)
    z["document_gap_years"] = z["revision_year"] - z["prev_year"]

    # Main-event match. In this manuscript all 25 Appendix A1 rows match the P1 sequence.
    main_keys = set((str(r.institution), int(r.revision_year), str(r.direction))
                    for _, r in events.iterrows())
    z["in_main25"] = [
        (str(r.institution), int(r.revision_year), str(r.direction)) in main_keys
        for _, r in z.iterrows()
    ]

    # Hand-reviewed labels that are actually preserved in the current repository (the 25 main rows).
    evcols = events[["institution", "revision_year", "prev_doc_year", "comparability",
                     "timing_tier", "direction"]].rename(columns={"revision_year": "main_event_year"})
    z = z.merge(evcols, on=["institution", "direction"], how="left", suffixes=("", "_manual"))
    # A few institutions can have multiple revisions of same direction; only accept exact year match.
    exact = z["main_event_year"].eq(z["revision_year"])
    for c in ["main_event_year", "prev_doc_year", "comparability", "timing_tier"]:
        z.loc[~exact, c] = np.nan
    z["manual_label_preserved"] = z["comparability"].notna() & z["timing_tier"].notna()

    # Document-length component of the manuscript's rule-based comparability screen.
    # The full rule also excludes manuals/bylaws/handbooks/copyright-only/royalty-only files;
    # those file-type labels are not preserved in the current derived panel.
    if "n_words" in z.columns and "prev_n_words" in z.columns:
        z["word_count_ratio"] = z["n_words"] / z["prev_n_words"].replace(0, np.nan)
        z["length_rule_pass"] = z["word_count_ratio"].between(0.5, 2.0)
    else:
        z["word_count_ratio"] = np.nan
        z["length_rule_pass"] = pd.NA

    # For non-main revisions, the only date reproducible from the public corpus is the observed
    # later-document year. This is a screening date, not a claim of documented adoption timing.
    z["screening_event_year"] = z["revision_year"].astype(int)

    # Mechanical overlap and outcome availability checks.
    rev_by_inst = {k: g["revision_year"].astype(int).tolist()
                   for k, g in universe.groupby("institution", observed=True)}
    panel_idx = {k: g.copy() for k, g in panel.groupby("institution", observed=True)}
    overlap = []
    pre_lic = []; post_lic = []; pre_any = []; post_any = []
    n_pre_years = []; n_post_years = []
    for _, r in z.iterrows():
        inst = r["institution"]; E = int(r["screening_event_year"])
        others = [y for y in rev_by_inst.get(inst, []) if y != int(r["revision_year"])]
        overlap.append(any(E + core.EVENT_MIN <= y <= E + core.EVENT_MAX for y in others))
        g = panel_idx.get(inst, pd.DataFrame())
        if g.empty:
            pre = post = g
        else:
            pre = g[g["year"].between(E + core.EVENT_MIN, E - 1)]
            post = g[g["year"].between(E, E + core.EVENT_MAX)]
        pre_lic.append(bool(pre.get("ln_licenses", pd.Series(dtype=float)).notna().any()))
        post_lic.append(bool(post.get("ln_licenses", pd.Series(dtype=float)).notna().any()))
        outcome_cols = [c for c in ["ln_licenses", "filing_margin", "ln_new_patent_apps",
                                    "ln_patents_issued", "ln_disclosures"] if c in g.columns]
        pre_any.append(bool(pre[outcome_cols].notna().any(axis=None)) if len(pre) and outcome_cols else False)
        post_any.append(bool(post[outcome_cols].notna().any(axis=None)) if len(post) and outcome_cols else False)
        n_pre_years.append(int(pre["year"].nunique()) if len(pre) else 0)
        n_post_years.append(int(post["year"].nunique()) if len(post) else 0)
    z["other_revision_in_window"] = overlap
    z["has_pre_license"] = pre_lic
    z["has_post_license"] = post_lic
    z["has_pre_any_core_outcome"] = pre_any
    z["has_post_any_core_outcome"] = post_any
    z["n_pre_panel_years"] = n_pre_years
    z["n_post_panel_years"] = n_post_years
    z["mechanical_window_pass"] = (~z["other_revision_in_window"] &
                                    z["has_pre_any_core_outcome"] & z["has_post_any_core_outcome"])

    # Do not pretend to know the documentary exclusion for rows not preserved in the manual file.
    def status(r):
        if r.in_main25:
            return "included_main25"
        reasons = []
        if r.other_revision_in_window:
            reasons.append("overlapping_revision_in_screening_window")
        if not r.has_pre_any_core_outcome:
            reasons.append("no_pre_core_outcome_at_observed_doc_year")
        if not r.has_post_any_core_outcome:
            reasons.append("no_post_core_outcome_at_observed_doc_year")
        if reasons:
            return ";".join(reasons)
        return "documentary_comparability_or_timing_review_required"
    z["current_disposition"] = z.apply(status, axis=1)
    z["priority_for_full_manual_review"] = (~z["in_main25"] & z["mechanical_window_pass"])

    # Stable ordering: main first, then candidates, then other exclusions; larger changes first within group.
    z["abs_delta_pcsi"] = z["delta_pcsi"].abs()
    z = z.sort_values(["in_main25", "priority_for_full_manual_review", "abs_delta_pcsi"],
                      ascending=[False, False, False]).reset_index(drop=True)
    z.insert(0, "revision_id", np.arange(1, len(z) + 1))
    return z


def leave_one_out(stacks_panel, universe, events):
    rows = []
    full_stacks = core.make_stacks(stacks_panel, universe, events)
    full = core.fit_outcome(full_stacks, "ln_licenses")
    for _, e in events.iterrows():
        sub = events[events["event_id"] != e.event_id].copy()
        s = core.make_stacks(stacks_panel, universe, sub)
        r = core.fit_outcome(s, "ln_licenses")
        rows.append({
            "dropped_institution": e.institution,
            "dropped_year": int(e.revision_year),
            "dropped_direction": e.direction,
            "gap": r["gap"], "cluster_se": r["gap_se"], "pre_p": r["pre_p"],
            "n": r["n"], "full_gap": full["gap"], "change_from_full": r["gap"] - full["gap"],
        })
    return pd.DataFrame(rows).sort_values("gap")


def event_level_effects(panel, universe, events):
    """Equal-event-weighted transparent DiD summaries for licensing.

    For each event, compare treated pre-to-post change with same-size-tercile/same-control clean
    controls in its stack. Each event contributes one scalar effect, so no large stack receives
    more weight simply because it contains more institution-years.
    """
    stacks = core.make_stacks(panel, universe, events)
    out = []
    for _, e in events.iterrows():
        s = stacks[stacks["stack"].eq(e.event_id)].copy()
        tr = s[s["treated"].eq(1)]
        if tr.empty:
            continue
        size = tr["size_tercile"].dropna().iloc[0]
        priv = tr["private"].dropna().iloc[0]
        ctrl = s[(s["treated"].eq(0)) & s["size_tercile"].eq(size) & s["private"].eq(priv)]
        pre_t = tr[tr.event_time.between(-4, -1)]["ln_licenses"].mean()
        post_t = tr[tr.event_time.between(0, 5)]["ln_licenses"].mean()
        # First average each control institution within pre/post, then average institutions,
        # preventing institutions with more observed years from dominating.
        def control_period_mean(q):
            if q.empty:
                return np.nan
            return q.groupby("institution", observed=True)["ln_licenses"].mean().mean()
        pre_c = control_period_mean(ctrl[ctrl.event_time.between(-4, -1)])
        post_c = control_period_mean(ctrl[ctrl.event_time.between(0, 5)])
        effect = (post_t - pre_t) - (post_c - pre_c)
        out.append({
            "event_id": int(e.event_id), "institution": e.institution,
            "revision_year": int(e.revision_year), "direction": e.direction,
            "delta_pcsi": float(e.delta_pcsi), "event_effect": effect,
            "treated_pre": pre_t, "treated_post": post_t,
            "control_pre": pre_c, "control_post": post_c,
            "n_same_stratum_controls": int(ctrl["institution"].nunique()),
        })
    return pd.DataFrame(out)


def exact_direction_permutation_event_level(eff: pd.DataFrame):
    e = eff.dropna(subset=["event_effect"]).reset_index(drop=True)
    n_up = int((e.direction == "up").sum())
    vals = e.event_effect.to_numpy(float)
    actual_up = np.where(e.direction.eq("up"))[0]
    obs = vals[actual_up].mean() - np.delete(vals, actual_up).mean()
    extreme = 0; total = 0
    for comb in itertools.combinations(range(len(e)), n_up):
        ix = np.array(comb, dtype=int)
        mask = np.ones(len(e), dtype=bool); mask[ix] = False
        stat = vals[ix].mean() - vals[mask].mean()
        total += 1
        extreme += int(abs(stat) >= abs(obs) - 1e-12)
    return {"n_events": int(len(e)), "n_up": n_up, "n_down": int(len(e)-n_up),
            "equal_event_gap": float(obs), "exact_permutation_p": extreme/total,
            "extreme_assignments": extreme, "total_assignments": total}


def continuous_delta_stacked(panel, universe, events, outcome="ln_licenses"):
    stacks = core.make_stacks(panel, universe, events).copy()
    delta_map = events.set_index("event_id")["delta_pcsi"].to_dict()
    stacks["delta_scaled"] = stacks["stack"].map(delta_map).astype(float) / 0.1
    dcols, zcols = [], []
    for k in core.EVENT_TIMES:
        tag = f"m{abs(k)}" if k < 0 else f"p{k}"
        d = f"D_{tag}"; z = f"DZ_{tag}"
        stacks[d] = ((stacks.treated == 1) & (stacks.event_time == k)).astype(float)
        stacks[z] = stacks[d] * stacks.delta_scaled
        dcols.append(d); zcols.append(z)
    xcols = dcols + zcols + ["ln_research_exp"]
    need = [outcome, "institution", "stack", "year", "size_tercile", "private"] + xcols
    q = stacks[need].dropna().copy()
    fe1 = pd.factorize(q["stack"].astype(str) + "|" + q["institution"].astype(str))[0]
    fe2 = pd.factorize(q["stack"].astype(str) + "|" + q["year"].astype(str) + "|" +
                       q["size_tercile"].astype(str) + "|" + q["private"].astype(str))[0]
    y = q[outcome].to_numpy(float); X = q[xcols].to_numpy(float)
    rz = core._demean(np.column_stack([y, X]), [fe1, fe2])
    yr, Xr = rz[:, 0], rz[:, 1:]
    beta = np.linalg.pinv(Xr.T @ Xr) @ (Xr.T @ yr)
    resid = yr - Xr @ beta
    cov = core._cluster_cov(Xr, resid, q["institution"].astype(str).to_numpy())
    def combo(names):
        w = np.zeros(len(xcols))
        for name, value in names.items(): w[xcols.index(name)] = value
        est = float(w @ beta); se = float(np.sqrt(max(w @ cov @ w, 0)))
        return est, se
    wpost = {f"DZ_p{k}": 1/6 for k in range(6)}
    slope, se = combo(wpost)
    df = max(int(q["institution"].nunique()) - 1, 1)
    p = float(2 * student_t.sf(abs(slope/se), df)) if se > 0 else np.nan
    idx = [xcols.index(f"DZ_m{j}") for j in [4,3,2]]
    bb = beta[idx]; vv = cov[np.ix_(idx, idx)]
    stat = float(bb.T @ np.linalg.pinv(vv) @ bb)
    pre_p = float(chi2.sf(stat, len(idx)))
    path = []
    for k in core.EVENT_TIMES:
        tag = f"m{abs(k)}" if k < 0 else f"p{k}"
        est, s = combo({f"DZ_{tag}": 1.0})
        path.append({"event_time": k, "effect_per_0_1_pcsi": est, "se": s})
    return {"outcome": outcome, "effect_per_0_1_pcsi": slope, "cluster_se": se,
            "cluster_p": p, "pretrend_p": pre_p, "n": int(len(q)),
            "clusters": int(q.institution.nunique()), "path": path}


def continuous_event_level(eff: pd.DataFrame, draws=100000, seed=20260926):
    e = eff.dropna(subset=["event_effect", "delta_pcsi"]).copy()
    x = e.delta_pcsi.to_numpy(float) / 0.1
    y = e.event_effect.to_numpy(float)
    X = np.column_stack([np.ones(len(x)), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    slope = float(b[1])
    rho, rho_p = spearmanr(x, y)
    rng = np.random.default_rng(seed)
    extreme = 0
    for _ in range(draws):
        xp = rng.permutation(x)
        bp = np.linalg.lstsq(np.column_stack([np.ones(len(xp)), xp]), y, rcond=None)[0][1]
        extreme += int(abs(bp) >= abs(slope) - 1e-12)
    return {"n_events": int(len(e)), "slope_per_0_1_pcsi": slope,
            "monte_carlo_permutation_p": (extreme + 1)/(draws + 1), "draws": draws,
            "spearman_rho": float(rho), "spearman_p": float(rho_p)}


def threshold_counts(raw):
    obs = core.load_p1_observed()
    cw = raw[["Institution_pci", "Institution_std"]].dropna().copy()
    cw["p1_norm"] = core.norm(cw["Institution_pci"])
    cw = (cw.groupby("p1_norm", observed=True)["Institution_std"]
          .agg(lambda z: z.value_counts().index[0]).rename("institution").reset_index())
    obs["p1_norm"] = core.norm(obs["Institution"])
    z = obs.merge(cw, on="p1_norm", how="inner")
    rows = []
    for th in [0.02, 0.025, 0.03, 0.04, 0.05]:
        r = z[z.delta_pcsi.abs() > th]
        rows.append({"threshold": th, "n_revisions": len(r), "n_institutions": r.institution.nunique(),
                     "up": int((r.delta_pcsi > 0).sum()), "down": int((r.delta_pcsi < 0).sum())})
    return pd.DataFrame(rows)


def main():
    raw = pd.read_csv(core.RAW, low_memory=False)
    panel = canon.median_size_panel(raw)
    universe = core.revision_universe(raw)
    events = core.load_main_events()

    audit = build_all_127(raw, panel)
    assert len(audit) == 127 and audit.institution.nunique() == 78
    assert int(audit.in_main25.sum()) == 25
    audit.to_csv(RESULTS / "all_127_revision_disposition.csv", index=False)

    loo = leave_one_out(panel, universe, events)
    loo.to_csv(RESULTS / "main25_leave_one_out.csv", index=False)

    eff = event_level_effects(panel, universe, events)
    eff.to_csv(RESULTS / "main25_equal_event_effects.csv", index=False)
    equal_inf = exact_direction_permutation_event_level(eff)
    cont_event = continuous_event_level(eff)
    cont_stack = continuous_delta_stacked(panel, universe, events)
    thresholds = threshold_counts(raw)
    thresholds.to_csv(RESULTS / "threshold_universe_counts.csv", index=False)

    disposition_counts = audit.current_disposition.value_counts().to_dict()
    summary = {
        "revision_universe": {"n": 127, "institutions": 78,
                              "up": int((audit.direction == "up").sum()),
                              "down": int((audit.direction == "down").sum())},
        "main25": {"n": 25, "up": int(((audit.direction == "up") & audit.in_main25).sum()),
                   "down": int(((audit.direction == "down") & audit.in_main25).sum())},
        "mechanical_screen": {
            "passes_overlap_and_core_outcome_screen": int(audit.mechanical_window_pass.sum()),
            "nonmain_priority_documentary_review": int(audit.priority_for_full_manual_review.sum()),
            "disposition_counts": {str(k): int(v) for k, v in disposition_counts.items()},
            "note": "Non-main C/P/N and A/B/C labels are not inferred because the public row-level manual file is incomplete."
        },
        "leave_one_out": {"min_gap": float(loo.gap.min()), "max_gap": float(loo.gap.max()),
                          "full_gap": float(loo.full_gap.iloc[0]),
                          "min_row": loo.iloc[0][["dropped_institution","dropped_year","dropped_direction","gap"]].to_dict(),
                          "max_row": loo.iloc[-1][["dropped_institution","dropped_year","dropped_direction","gap"]].to_dict()},
        "equal_event_weighted": equal_inf,
        "continuous_delta_event_level": cont_event,
        "continuous_delta_stacked": cont_stack,
        "threshold_universe_counts": thresholds.to_dict(orient="records"),
    }
    (RESULTS / "all_revision_analysis_summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")

    print("ALL127 SUMMARY", json.dumps(summary, sort_keys=True, default=str))
    print("LOO RANGE", loo.gap.min(), loo.gap.max())
    print("EQUAL EVENT", json.dumps(equal_inf, sort_keys=True))
    print("CONTINUOUS EVENT", json.dumps(cont_event, sort_keys=True))
    print("CONTINUOUS STACK", json.dumps({k:v for k,v in cont_stack.items() if k != 'path'}, sort_keys=True))
    print("THRESHOLDS", thresholds.to_dict(orient="records"))
    print("AUDIT COLUMNS", list(audit.columns))


if __name__ == "__main__":
    main()
