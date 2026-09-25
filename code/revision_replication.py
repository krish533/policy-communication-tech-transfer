"""Final September 25 stacked-revision replication layer.

This module builds on revision_event_study.py but applies the research-size
stratification recovered from the manuscript benchmarks: terciles of each
institution's median research expenditure over the AUTM panel. It also
implements the paper's exact direction-label permutation inference over all
C(25,6)=177,100 assignments.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd

import revision_event_study as core

TARGETS = {
    "ln_licenses": {"gap": .619, "se": .136, "perm_p": .015, "pre_p": .62, "up": .289, "down": -.330, "n": 20181},
    "filing_margin": {"gap": .374, "se": .168, "perm_p": .155, "pre_p": .63, "up": .166, "down": -.207, "n": 20277},
    "ln_new_patent_apps": {"gap": .262, "se": .182, "perm_p": .243, "pre_p": .50, "up": .151, "down": -.111, "n": 20277},
    "ln_patents_issued": {"gap": .027, "se": .222, "perm_p": .920, "pre_p": .19, "up": .120, "down": .093, "n": 19821},
    "ln_disclosures": {"gap": -.112, "se": .105, "perm_p": .507, "pre_p": .37, "up": -.015, "down": .096, "n": 20277},
}


def median_size_panel(raw: pd.DataFrame) -> pd.DataFrame:
    p = core.make_panel(raw)
    med = p.groupby("institution", observed=True)["research_exp"].median()
    ranks = med.rank(method="average", pct=True)
    terc = np.minimum(np.ceil(ranks * 3).astype(int) - 1, 2)
    p["size_tercile"] = p["institution"].map(terc).astype("Int64")
    return p


def _design_frame(stacks: pd.DataFrame, outcome: str) -> tuple[pd.DataFrame, list[str]]:
    q = stacks.copy()
    dcols = []
    for k in core.EVENT_TIMES:
        tag = f"m{abs(k)}" if k < 0 else f"p{k}"
        col = f"D_{tag}"
        q[col] = ((q.treated == 1) & (q.event_time == k)).astype(float)
        dcols.append(col)
    need = [outcome, "institution", "stack", "year", "size_tercile", "private",
            "ln_research_exp"] + dcols
    return q[need].dropna().copy(), dcols


def _stack_sufficient_statistics(stacks: pd.DataFrame, outcome: str):
    """Normal-equation blocks for exact permutation inference.

    Because both absorbed fixed effects contain stack, all absorption is
    stack-separable. For stack e, a permuted direction label multiplies its
    event-time interaction block by s_e in {-1,+1}. The DS'DS block is
    therefore invariant to permutation, while D'DS, R'DS, and y'DS are
    linear in the signs. This makes exact enumeration fast and transparent.
    """
    q, dcols = _design_frame(stacks, outcome)
    stack_ids = sorted(q["stack"].unique())
    m = len(dcols)
    p0 = m + 1  # event-time main effects plus log research expenditure
    A = np.zeros((p0, p0))
    arhs = np.zeros(p0)
    C = np.zeros((m, m))
    B_parts = np.zeros((len(stack_ids), p0, m))
    c_parts = np.zeros((len(stack_ids), m))

    for pos, sid in enumerate(stack_ids):
        z = q[q["stack"].eq(sid)].copy()
        # Within a single stack the FEs reduce to institution and
        # year x size-tercile x private cells.
        fe1 = pd.factorize(z["institution"].astype(str))[0]
        fe2 = pd.factorize(z["year"].astype(str) + "|" +
                           z["size_tercile"].astype(str) + "|" +
                           z["private"].astype(str))[0]
        y = z[outcome].to_numpy(float)
        D = z[dcols].to_numpy(float)
        X0 = np.column_stack([D, z["ln_research_exp"].to_numpy(float)])
        # Z is the unsigned interaction basis. A direction permutation
        # simply multiplies all its columns in this stack by the stack sign.
        block = np.column_stack([y, X0, D])
        rr = core._demean(block, [fe1, fe2])
        yr = rr[:, 0]
        x0r = rr[:, 1:1+p0]
        zr = rr[:, 1+p0:]
        A += x0r.T @ x0r
        arhs += x0r.T @ yr
        C += zr.T @ zr
        B_parts[pos] = x0r.T @ zr
        c_parts[pos] = zr.T @ yr

    return q, dcols, stack_ids, A, arhs, C, B_parts, c_parts


def _solve_from_signs(signs, A, arhs, C, B_parts, c_parts):
    B = np.einsum("e,eij->ij", signs, B_parts, optimize=True)
    c = signs @ c_parts
    mat = np.block([[A, B], [B.T, C]])
    rhs = np.concatenate([arhs, c])
    beta = np.linalg.pinv(mat) @ rhs
    return beta


def exact_permutation(stacks: pd.DataFrame, events: pd.DataFrame, outcome: str, batch_size=4000):
    q, dcols, stack_ids, A, arhs, C, B_parts, c_parts = _stack_sufficient_statistics(stacks, outcome)
    if len(stack_ids) != 25:
        raise AssertionError(f"Expected 25 stacks, got {len(stack_ids)}")

    event_sign = events.set_index("event_id")["sign"].to_dict()
    obs_signs = np.array([event_sign[int(s)] for s in stack_ids], dtype=float)
    obs_beta = _solve_from_signs(obs_signs, A, arhs, C, B_parts, c_parts)
    m = len(dcols)
    post_idx = [dcols.index(f"D_p{k}") for k in core.POST_TIMES]
    # Interaction coefficients are the last m coefficients; manuscript gap = average 2 theta_k.
    obs_gap = float((2.0 / len(post_idx)) * obs_beta[m+1 + np.array(post_idx)].sum())

    # Confirm the normal-equation implementation agrees with the full stacked fit.
    point = core.fit_outcome(stacks, outcome)
    if abs(obs_gap - point["gap"]) > 1e-7:
        raise AssertionError(f"Permutation normal equations disagree with full fit: {obs_gap} vs {point['gap']}")

    total = 0
    extreme = 0
    buf = []

    def run_batch(combos):
        nonlocal total, extreme
        bsz = len(combos)
        S = -np.ones((bsz, 25), dtype=float)
        for i, comb in enumerate(combos):
            S[i, list(comb)] = 1.0
        # B(sign): batch x p0 x m; c(sign): batch x m.
        Bb = np.einsum("be,eij->bij", S, B_parts, optimize=True)
        cb = S @ c_parts
        p0 = A.shape[0]
        dim = p0 + m
        mats = np.empty((bsz, dim, dim), dtype=float)
        mats[:, :p0, :p0] = A
        mats[:, :p0, p0:] = Bb
        mats[:, p0:, :p0] = np.swapaxes(Bb, 1, 2)
        mats[:, p0:, p0:] = C
        rhs = np.empty((bsz, dim), dtype=float)
        rhs[:, :p0] = arhs
        rhs[:, p0:] = cb
        try:
            betas = np.linalg.solve(mats, rhs)
        except np.linalg.LinAlgError:
            betas = np.stack([np.linalg.pinv(mats[i]) @ rhs[i] for i in range(bsz)])
        gaps = (2.0 / len(post_idx)) * betas[:, p0 + np.array(post_idx)].sum(axis=1)
        total += bsz
        extreme += int((np.abs(gaps) >= abs(obs_gap) - 1e-12).sum())

    for comb in itertools.combinations(range(25), 6):
        buf.append(comb)
        if len(buf) >= batch_size:
            run_batch(buf); buf = []
    if buf:
        run_batch(buf)

    if total != 177100:
        raise AssertionError(f"Expected 177100 assignments, enumerated {total}")
    return {
        "observed_gap": obs_gap,
        "permutation_p": extreme / total,
        "extreme_assignments": extreme,
        "total_assignments": total,
        "n": int(len(q)),
    }


def bh_adjust(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    raw = [p * m / (i+1) for i, (_, p) in enumerate(items)]
    # monotonicity from largest rank backward
    adj = raw[:]
    for i in range(m-2, -1, -1):
        adj[i] = min(adj[i], adj[i+1])
    return {name: min(1.0, q) for (name, _), q in zip(items, adj)}


def main():
    raw = pd.read_csv(core.RAW, low_memory=False)
    panel = median_size_panel(raw)
    universe = core.revision_universe(raw)
    events = core.load_main_events()
    stacks = core.make_stacks(panel, universe, events)

    print("CANONICAL SEPT25 REPLICATION")
    print("panel", len(panel), "institutions", panel.institution.nunique())
    print("revision universe", len(universe), "institutions", universe.institution.nunique())
    print("events", len(events), "up", int((events.sign > 0).sum()), "down", int((events.sign < 0).sum()))
    print("stack rows", len(stacks))

    rows = []
    pvals = {}
    for outcome, target in TARGETS.items():
        point = core.fit_outcome(stacks, outcome)
        perm = exact_permutation(stacks, events, outcome)
        pvals[outcome] = perm["permutation_p"]
        row = {
            "outcome": outcome,
            "gap": point["gap"],
            "cluster_se": point["gap_se"],
            "perm_p": perm["permutation_p"],
            "pre_p": point["pre_p"],
            "upward": point["up"],
            "downward": point["down"],
            "n": point["n"],
            "extreme_assignments": perm["extreme_assignments"],
        }
        rows.append(row)
        print("CANONICAL RESULT", outcome, json.dumps(row, sort_keys=True))
        print("PDF TARGET", outcome, json.dumps(target, sort_keys=True))

    qvals = bh_adjust(pvals)
    for r in rows:
        r["bh_q"] = qvals[r["outcome"]]

    out = pd.DataFrame(rows)
    core.RESULTS.mkdir(parents=True, exist_ok=True)
    out.to_csv(core.RESULTS / "table3_reproduced.csv", index=False)
    (core.RESULTS / "table3_reproduced.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print("BH Q", qvals)

    # Hard structural checks; numerical differences from the PDF remain visible rather than hidden.
    assert len(panel) == 3507 and panel.institution.nunique() == 149
    assert len(universe) == 127 and universe.institution.nunique() == 78
    assert len(events) == 25 and int((events.sign > 0).sum()) == 6
    for r in rows:
        assert r["n"] == TARGETS[r["outcome"]]["n"]


if __name__ == "__main__":
    main()
