"""The control for `pipeline/osm_tram.py`: run it on Aarhus's cache and
reproduce Aarhus's `stations.csv` exactly.

    python scripts/osm_tram_control.py

Aarhus's step 1 is the module's origin and is not rewired, so its last output
is an independent answer. Reads the cache only, and writes nothing. Exits
non-zero on any difference: a station, its lines, its kommune, or a
coordinate beyond 1e-9 degrees.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline.aarhus import config  # noqa: E402
from pipeline.aarhus.kommuner import kommune_polygons  # noqa: E402


def main():
    if not config.STATIONS_CSV.exists():
        sys.exit(f"no {config.STATIONS_CSV} - run Aarhus's step 1 first")
    want = pd.read_csv(config.STATIONS_CSV, encoding="utf-8")

    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations",
                                 "pipeline/aarhus/fetch_sources.py")
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS,
                           operator=config.OPERATOR,
                           name_aliases=config.STATION_NAME_ALIASES)
    _, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                              crs_projected=config.CRS_PROJECTED)
    inside, _ = osm_tram.split_by_places(st, kommune_polygons(verbose=False),
                                         keep=config.KOMMUNER, place_col="kommune")
    got = (inside[inside["stop_name"].isin(config.NEW_TRAMWAY)]
           .rename(columns={"stop_name": "station"})
           [["station", "lines", "kommune", "latitude", "longitude"]]
           .sort_values("station").reset_index(drop=True))
    want = want.sort_values("station").reset_index(drop=True)

    print(f"\n  osm_tram: {len(got)} stations; Aarhus's stations.csv: {len(want)}")
    if list(got["station"]) != list(want["station"]):
        sys.exit(f"station names differ:\n  only osm_tram: "
                 f"{sorted(set(got['station']) - set(want['station']))}\n  only Aarhus: "
                 f"{sorted(set(want['station']) - set(got['station']))}")
    bad = []
    for col in ("lines", "kommune"):
        diff = got[col] != want[col]
        bad += [f"{s}: {col} {a!r} vs {b!r}" for s, a, b in
                zip(got.loc[diff, "station"], got.loc[diff, col], want.loc[diff, col])]
    for col in ("latitude", "longitude"):
        d = (got[col] - want[col]).abs()
        bad += [f"{s}: {col} off by {x:.2e}" for s, x in
                zip(got.loc[d > 1e-9, "station"], d[d > 1e-9])]
    if bad:
        sys.exit("osm_tram does NOT reproduce Aarhus:\n  " + "\n  ".join(bad))
    print("  CONTROL PASSES: osm_tram reproduces Aarhus's stations.csv exactly "
          "(names, lines, kommune, coordinates)")


if __name__ == "__main__":
    main()
