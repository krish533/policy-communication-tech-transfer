"""Build publication-facing figures for the expanded 34-event manuscript.

Run after final_expanded_inference.py and expanded34_diagnostics.py.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGDIR = ROOT / "manuscript" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)


def main():
    p = pd.read_csv(RESULTS / "expanded_event_time_paths.csv")
    p = p[p["sample"].eq("expanded34")].copy()

    outcomes = [
        ("ln_licenses", "Log licenses and options", "(a) Licensing"),
        ("filing_margin", "Filing margin", "(b) Filing margin"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharex=True)
    for ax, (outcome, ylabel, title) in zip(axes, outcomes):
        d = p[p["outcome"].eq(outcome)].sort_values("event_time")
        ax.axhline(0, linewidth=0.8)
        ax.axvline(-1, linewidth=0.8, linestyle="--")
        ax.errorbar(
            d["event_time"], d["gap"],
            yerr=1.96 * d["se"], fmt="o-", capsize=2.5, linewidth=1.2,
        )
        ax.set_title(title)
        ax.set_xlabel("Years from policy revision")
        ax.set_ylabel(ylabel)
        ax.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
        ax.text(-0.95, ax.get_ylim()[0], "reference", rotation=90,
                va="bottom", ha="left", fontsize=7)

    fig.tight_layout()
    fig.savefig(FIGDIR / "fig1_event_study_expanded.pdf", bbox_inches="tight")
    fig.savefig(FIGDIR / "fig1_event_study_expanded.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    loo = pd.read_csv(RESULTS / "expanded34_leave_one_out.csv").copy()
    loo = loo.sort_values("gap").reset_index(drop=True)
    labels = loo["dropped_institution"].astype(str) + " (" + loo["dropped_year"].astype(int).astype(str) + ")"
    fig, ax = plt.subplots(figsize=(7.5, 8.2))
    ax.axvline(0.4949823607577816, linewidth=0.9, linestyle="--")
    ax.scatter(loo["gap"], range(len(loo)))
    ax.set_yticks(range(len(loo)))
    ax.set_yticklabels(labels, fontsize=6.5)
    ax.set_xlabel("Licensing gap after dropping one revision")
    ax.set_ylabel("")
    ax.set_title("Leave-one-event-out licensing estimates")
    fig.tight_layout()
    fig.savefig(FIGDIR / "figA1_leave_one_out_expanded.pdf", bbox_inches="tight")
    fig.savefig(FIGDIR / "figA1_leave_one_out_expanded.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote manuscript figures to {FIGDIR}")


if __name__ == "__main__":
    main()
