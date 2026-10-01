"""Göteborg step 1: every stop of trams 1-13 in Göteborgs Stad.

    python pipeline/goteborg/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: stations are the stop members of the
thirteen lines' relations, collapsed by name. Lines 4 and 12 run on into
Mölndal: their stops there are drawn with the line but not ringed, and are
listed with the kommun each lies in (owner, call 21) - provided each line keeps
at least half its stops in the city (the stub test, re-run here). No stop is
thinned. Each line's drawn colour is checked against the colours OSM records.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.goteborg import config  # noqa: E402
from pipeline.goteborg.kommuner import FETCH, kommun_polygons  # noqa: E402


def check_colours(els):
    """Each drawn colour must be one OSM records on that line's relations."""
    for ref in config.DRAWN_LINES:
        osm = {r["tags"].get("colour", "").lower() for r in els if r["type"] == "relation"
               and r["tags"].get("route") == config.ROUTE and r["tags"].get("ref") == ref}
        mine = config.LINE_COLOURS[ref].lower()
        if mine not in osm and config.LINE_COLOUR_SHIFTS.get(ref, ("",))[0].lower() not in osm:
            sys.exit(f"line {ref}: drawn colour {mine} is not one OSM records ({sorted(osm)}) "
                     f"- re-read OSM's colours")


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    kom = kommun_polygons()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    check_colours(els)
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD, name_aliases=config.NAME_ALIASES)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED)
    print()
    station_gates.verify_stations(
        city="Göteborg", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M)

    inside, outside = osm_tram.split_by_places(st, kom, keep={config.GOTEBORG_SCB})
    print(f"\n  {len(st)} tram stops -> {len(inside)} in Göteborgs Stad, "
          f"{len(outside)} elsewhere")

    # The stub test (owner, call 21): every line, and above all 4 and 12.
    in_names = set(inside["stop_name"])
    per_line = q.drop_duplicates(["line", "stop_name"]).groupby("line")["stop_name"]
    print("\n  stops per line inside the city:")
    for ref in config.LINE_REFS:
        names = set(per_line.get_group(ref))
        k = len(names & in_names)
        share = k / len(names)
        print(f"    {ref:>3}: {k:>3} of {len(names):>3} ({share:.0%})")
        if share < 1 and ref not in config.STUB_LINES:
            sys.exit(f"line {ref} now leaves the city - a scope question for the owner")
        if share < config.STUB_MIN_SHARE:
            sys.exit(f"line {ref} keeps {share:.0%} of its stops: a STUB under call 21's "
                     f"test - the call goes back to the owner")
    bad = sorted(set(outside["stop_name"]) - set(
        q[q["line"].isin(config.STUB_LINES)]["stop_name"]))
    if bad:
        sys.exit(f"stops outside the city on lines other than {config.STUB_LINES}: {bad}")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-city spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the in-city median gap is {d.median():.0f} m; the halved rings were "
                 f"chosen at 378 m - re-take the ring decision")

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": [f"in {n}, outside Göteborgs Stad" for n in outside["name"]],
                        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV,
                                                  index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for s, r in zip(out["station"], out["reason"]):
        print(f"    {s:<28} {r}")

    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
