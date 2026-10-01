"""Zurich step 1: every stop of the drawn VBZ trams in the Stadt Zürich.

    python pipeline/zurich/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: stations are the stop members of the
kept tram relations, collapsed by name. Trams 2 and 10 run on past the Stadt
(Schlieren; Opfikon and Kloten): their stops there are drawn with the line but
not ringed, and are listed with the Gemeinde each lies in. Trams 12 and 20 and
the Forchbahn are judged and left out (config.NOT_DRAWN). No stop is thinned.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.zurich import config  # noqa: E402
from pipeline.zurich.gemeinden import FETCH, gemeinde_polygons  # noqa: E402


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    gem = gemeinde_polygons()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=config.ROUTES, refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD, name_aliases=config.NAME_ALIASES)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED,
                                      max_spread_m=config.MAX_SPREAD_M)
    print()
    station_gates.verify_stations(
        city="Zurich", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M)

    inside, outside = osm_tram.split_by_places(st, gem, keep={config.BFS_ZURICH})
    print(f"\n  {len(st)} tram stops -> {len(inside)} in the Stadt Zürich, "
          f"{len(outside)} elsewhere")
    if (config.EXPECTED_IN_CITY is not None
            and (len(inside), len(outside)) != (config.EXPECTED_IN_CITY, config.EXPECTED_OUTSIDE)):
        sys.exit(f"expected {config.EXPECTED_IN_CITY} inside and {config.EXPECTED_OUTSIDE} "
                 f"outside (the build of 2026-09-30) - re-read OSM")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-city spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the in-city median gap is {d.median():.0f} m; the halved rings were "
                 f"chosen at 283 m - re-take the ring decision")

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": [f"in {n} (BFS {r}), outside the Stadt Zürich"
                                   for n, r in zip(outside["name"], outside["ref"])],
                        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV,
                                                  index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for s, r, ln in zip(out["station"], out["reason"], out["lines"]):
        print(f"    {s:<32} {ln:<8} {r}")

    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")
    per_line = {ref: int(keep["lines"].str.split("/").apply(lambda x: ref in x).sum())
                for ref in config.LINE_REFS}
    print(f"  stations per line in the Stadt: {per_line}")

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
