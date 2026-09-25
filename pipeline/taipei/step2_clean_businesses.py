"""Taipei (Regional) step 2: the shared Taiwanese step 2 run once per city - Taipei
against its door plates, New Taipei against its own - and the two results
concatenated. Each city's figures are tagged in the baseline.

Reads the cache and NEVER fetches.

    python pipeline/taipei/step2_clean_businesses.py
"""
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.countries.taiwan_step2 import run  # noqa: E402
from pipeline.taipei import config  # noqa: E402


def city_config(prefixes, plates_csv, plates):
    shared = {k: getattr(config, k) for k in dir(config) if k.isupper()}
    shared.update(ADDRESS_PREFIXES=prefixes, DOORPLATE_CSV=plates_csv, PLATE_COLS=plates["cols"],
                  PLATE_DISTRICT_COL=plates["district"])
    return SimpleNamespace(**shared)


def main():
    parts = []
    for city, tag, csv_path, plates in (
            ("Taipei", "taipei_", config.TAIPEI_DOORPLATE_CSV, config.TAIPEI_PLATES),
            ("New Taipei", "new_taipei_", config.NEW_TAIPEI_DOORPLATE_CSV, config.NEW_TAIPEI_PLATES)):
        print(f"\n=== {city}")
        part = run(city_config(config.CITY_PREFIXES[city], csv_path, plates), city, "taipei",
                   tag=tag, write=False)
        parts.append(part.assign(city=city))
    out = pd.concat(parts, ignore_index=True)
    emit("storefronts", len(out))
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  wrote {config.BUSINESSES_CLEAN_CSV.name}: {len(out):,} storefronts "
          f"({out.city.value_counts().to_dict()})")


if __name__ == "__main__":
    main()
