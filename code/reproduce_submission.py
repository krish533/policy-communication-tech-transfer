"""One-command publication replication for the revised manuscript.

This runner executes the publication-facing 34-event/29-event inference, diagnostics,
figures, and explicit stacked-dataset exports in the same order used by CI.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = [
    "final_expanded_inference.py",
    "expanded34_diagnostics.py",
    "build_expanded_manuscript_figures.py",
    "export_final_stacked_datasets.py",
]
EXPECTED = [
    ROOT / "results" / "expanded_manual_sample_results.csv",
    ROOT / "results" / "expanded34_event_list.csv",
    ROOT / "results" / "strict29_event_list.csv",
    ROOT / "results" / "expanded34_balance.csv",
    ROOT / "results" / "expanded34_stack_composition.csv",
    ROOT / "results" / "expanded34_leave_one_out.csv",
    ROOT / "data" / "derived" / "final_stacked_event_dataset_expanded34.csv",
    ROOT / "data" / "derived" / "final_stacked_event_dataset_strict29.csv",
]


def main() -> None:
    for script in STEPS:
        print(f"\n=== Running {script} ===", flush=True)
        subprocess.run([sys.executable, str(ROOT / "code" / script)], cwd=ROOT, check=True)

    missing = [str(path.relative_to(ROOT)) for path in EXPECTED if not path.exists()]
    if missing:
        raise FileNotFoundError("Replication completed but expected outputs are missing: " + ", ".join(missing))

    print("\nSubmission replication completed successfully.")
    print("Preferred design: 34 events (8 upward / 26 downward).")
    print("Strict sensitivity: 29 events (7 upward / 22 downward).")
    print("Publication-facing permutation draws: 100,000 per outcome.")


if __name__ == "__main__":
    main()
