"""The control for `pipeline/countries/latvia_register.py`: Riga's output must
not move.

    python scripts/latvia_register_control.py

Builds Riga's storefront frame through the shared module (Riga's step 2's
`build()`, which now calls it) and compares it with Riga's
`businesses_clean.csv` as last written, and its emitted figures with
`outputs/riga/baseline.json`. WRITES NOTHING: `data/` is one junction shared
by every worktree, so a branch never re-runs another city's step into it.
Exits non-zero on any difference.
"""
import contextlib
import io
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.baseline import parse  # noqa: E402
from pipeline.countries.latvia_register import utf8_console  # noqa: E402
from pipeline.riga import config  # noqa: E402
from pipeline.riga.step2_clean_businesses import build  # noqa: E402


def main():
    utf8_console()
    if not config.BUSINESSES_CLEAN_CSV.exists():
        sys.exit(f"no {config.BUSINESSES_CLEAN_CSV} to compare against")
    want = pd.read_csv(config.BUSINESSES_CLEAN_CSV, dtype=str, keep_default_na=False)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        got = build()
    print(buf.getvalue())
    figures = parse(buf.getvalue())
    # Through a CSV round trip, as the step writes it, so the two frames are
    # compared exactly as they would land on disk.
    got = pd.read_csv(io.StringIO(got.to_csv(index=False)), dtype=str, keep_default_na=False)

    bad = []
    if list(got.columns) != list(want.columns):
        bad.append(f"columns {list(got.columns)} vs {list(want.columns)}")
    elif len(got) != len(want):
        bad.append(f"{len(got)} rows vs {len(want)}")
    else:
        diff = (got != want).any(axis=1)
        if diff.any():
            bad.append(f"{int(diff.sum())} rows differ, e.g. {got[diff].head(3).to_dict('records')}")
    base = json.loads((config.OUTPUTS / "baseline.json").read_text(encoding="utf-8"))
    for k, v in figures.items():
        if k in base and str(base[k]) != str(v):
            bad.append(f"figure {k}: {v} vs baseline {base[k]}")
    step2_keys = {"excise_rows", "food_premises", "food_placed_exact", "food_placed_unit_dropped",
                  "food_unplaced", "food_with_unit_number", "trade_premise_groups",
                  "shops_and_services_named", "shops_placed", "shops_in_degrading_buildings",
                  "storefronts"}
    if step2_keys - set(figures):
        bad.append(f"figures not emitted: {sorted(step2_keys - set(figures))}")
    if bad:
        sys.exit("latvia_register does NOT reproduce Riga:\n  " + "\n  ".join(bad))
    print(f"CONTROL PASSES: {len(got):,} rows identical to Riga's businesses_clean.csv, "
          f"and all {len(step2_keys)} step 2 figures match outputs/riga/baseline.json")


if __name__ == "__main__":
    main()
