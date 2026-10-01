"""Odense step 1: every Odense Letbane station in service.

    python pipeline/odense/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

WHAT MAKES THIS CITY'S STEP 1 DIFFERENT:

  * **The first city on the shared `pipeline/osm_tram.py`** (the tram-city
    skill): stations are the stop members of the kept route relations,
    whitelisted on ref + route + operator, never a tag search.
  * **One station OSM's routes leave out**, SDU Syd/Hospital Nord, open since
    2023-08-25 and added by node id (config.STATION_ADD); **one tagged stop
    not yet open**, Hospital Syd, watched (check_not_yet_open), not ringed.
  * **The whole line is drawn** and every station lies inside the kommune, so
    step 3 draws OSM's relation whole (load_osm_line_shapes), unlike Aarhus's
    cut.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.odense import config  # noqa: E402
from pipeline.odense.kommuner import FETCH, kommune_polygons  # noqa: E402


def check_not_yet_open(els, st):
    """Each NOT_YET_OPEN stop is still a tagged tram stop on no kept route.

    Not a row in excluded_stations.csv: a stop not yet in service is not part
    of the network, and What Is Excluded has no category for it. It is a
    watch item, and this is the watch - the step stops when OSM puts the stop
    on a route (it has opened) or drops its tag."""
    for name, reason in config.NOT_YET_OPEN.items():
        if name in set(st["stop_name"]):
            sys.exit(f"{name!r} is now on a route relation - opened? Re-take the "
                     f"scope call rather than keep NOT_YET_OPEN")
        ns = [e for e in els if e["type"] == "node"
              and e.get("tags", {}).get("name") == name
              and e["tags"].get("railway") == "tram_stop"]
        if not ns:
            sys.exit(f"{name!r} is no longer a tagged tram stop in OSM - re-read it "
                     f"(opened, renamed or removed?)")
        print(f"    not yet open, not ringed: {name} - {reason}")


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    kom = kommune_polygons()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED)
    print()
    check_not_yet_open(els, st)
    station_gates.verify_stations(
        city="Odense", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={ref: int(st["lines"].str.split("/").apply(
            lambda ls: ref in ls).sum()) for ref in config.LINE_REFS})

    inside, outside = osm_tram.split_by_places(st, kom, keep=config.KOMMUNER,
                                               place_col="kommune")
    print(f"\n  {len(st)} Letbane stations -> {len(inside)} in Odense Kommune, "
          f"{len(outside)} elsewhere")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the in-scope median gap is {d.median():.0f} m; the halved rings were "
                 f"chosen at 441 m - re-take the ring decision")

    # Every in-service station is in the kommune today, so this is header-only;
    # it stays written so a stop that moves outside is recorded, not lost.
    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": [f"in {k} ({r}), outside Odense Kommune"
                                   for k, r in zip(outside["kommune"], outside["ref"])],
                        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV,
                                                  index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for s, r in zip(out["station"], out["reason"]):
        print(f"    {s:<28} {r}")

    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "kommune", "latitude", "longitude"]]
            .sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stop_positions_added", int((q["source"] == "added").sum()))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    main()
