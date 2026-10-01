"""Stable entry point for expanded-34 manuscript diagnostics.

This wrapper reuses the diagnostic functions in expanded34_diagnostics.py while
avoiding pandas attribute-name ambiguity for the `sample` column in the final
summary block.
"""
from __future__ import annotations

import json
import numpy as np
import pandas as pd

import expanded34_diagnostics as d
import expanded_manual_revision_analysis as exp
import revision_event_study as core
import revision_replication as canon


def main():
    raw = pd.read_csv(core.RAW, low_memory=False)
    panel = canon.median_size_panel(raw)
    universe = core.revision_universe(raw)
    e34, e29 = exp.load_expanded_events(raw)

    p34, s34 = d.event_paths(panel, universe, e34, "expanded34")
    p29, s29 = d.event_paths(panel, universe, e29, "strict29")
    pd.concat([p34, p29], ignore_index=True).to_csv(
        d.RESULTS / "expanded_event_time_paths.csv", index=False)

    res = pd.read_csv(d.RESULTS / "expanded_manual_sample_results.csv")
    res["bh_q"] = np.nan
    for sample_name, idx in res.groupby("sample").groups.items():
        res.loc[idx, "bh_q"] = d.bh_adjust(res.loc[idx, "permutation_p"].to_numpy())
    res.to_csv(d.RESULTS / "expanded_manual_sample_results.csv", index=False)

    evbal, bal = d.event_balance(panel, raw, e34)
    evbal.to_csv(d.RESULTS / "expanded34_event_level_balance_data.csv", index=False)
    bal.to_csv(d.RESULTS / "expanded34_balance.csv", index=False)

    stacks = d.stack_composition(s34, e34)
    stacks.to_csv(d.RESULTS / "expanded34_stack_composition.csv", index=False)

    loo, loo_summary = d.leave_one_out(panel, universe, e34)
    loo.to_csv(d.RESULTS / "expanded34_leave_one_out.csv", index=False)

    summary = {
        "expanded34_bh_q": res.loc[res["sample"].eq("expanded34")]
            .set_index("outcome")["bh_q"].to_dict(),
        "strict29_bh_q": res.loc[res["sample"].eq("strict29")]
            .set_index("outcome")["bh_q"].to_dict(),
        "expanded34_leave_one_out": loo_summary,
        "balance_draws": 50000,
    }
    (d.RESULTS / "expanded34_diagnostics_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n")
    print("EXPANDED34 DIAGNOSTICS", json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
