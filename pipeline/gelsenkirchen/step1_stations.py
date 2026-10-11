"""Gelsenkirchen step 1: every stop of trams 301, 302 and 107 and Stadtbahn
U11 inside the City of Gelsenkirchen.

    python pipeline/gelsenkirchen/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Geneva's step 1 on the shared `pipeline/osm_tram.py`: stations are the stop
members of the kept route relations, collapsed by name within
config.MAX_SPREAD_M. Gate 3 counts each WHOLE line against the operators'
timetables before the scope split, and stops the step on a mismatch. Then
the cut at the city line (owner, 2026-10-05, call 3; Berlin's precedent):
302's stops in Bochum and 107's and U11's in Essen are drawn with their
lines, never ringed, and listed with the city each lies in. No stop is
thinned.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.gelsenkirchen import config  # noqa: E402
from pipeline.gelsenkirchen.boundary import place_polygons  # noqa: E402


def per_line(st, refs):
    return {ref: int(st["lines"].str.split("/").apply(lambda ls: ref in ls).sum())
            for ref in refs}


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    places = place_polygons()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", config.FETCH)
    kept = osm_tram.select_relations(els, routes=config.ROUTES, refs=config.LINE_REFS,
                                     operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                                     verbose=False)
    # The route type OSM gives each drawn line decides nothing on its own:
    # `mode` stays tram whatever U11 is typed (owner, 2026-10-05, call 4).
    print("\n  OSM route type per drawn line: " + ", ".join(
        f"{ref} {'/'.join(sorted({r['tags']['route'] for r in rs}))} ({len(rs)} relation(s))"
        for ref, rs in kept.items()))
    q = osm_tram.stop_rows(els, routes=config.ROUTES, refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD, name_aliases=config.NAME_ALIASES)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED,
                                      max_spread_m=config.MAX_SPREAD_M)
    print()
    whole = per_line(st, config.LINE_REFS)
    res = station_gates.verify_stations(
        city="Gelsenkirchen", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=whole)
    # Gate 3 stops a tram step 1 (the tram-city skill).
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with the operators' own stop counts - " + "; ".join(
            f"{ref}: build {b}, operator {o}" for ref, (b, o) in res["per_line_mismatches"].items()))

    inside, outside = osm_tram.split_by_places(st, places, keep={config.CITY_AGS})
    print(f"\n  {len(st)} stops -> {len(inside)} in {config.NAME}, {len(outside)} elsewhere")
    if (config.EXPECTED_IN_SCOPE is not None
            and (len(inside), len(outside)) != (config.EXPECTED_IN_SCOPE, config.EXPECTED_OUTSIDE)):
        sys.exit(f"expected {config.EXPECTED_IN_SCOPE} inside and {config.EXPECTED_OUTSIDE} "
                 f"outside (the build of 2026-10-07) - re-read OSM")
    in_line, out_line = per_line(inside, config.LINE_REFS), per_line(outside, config.LINE_REFS)
    print("  per line (whole / inside / outside), and the stops inside that the line alone serves:")
    for ref in config.LINE_REFS:
        alone = inside[inside["lines"] == ref]
        print(f"    {config.LINE_NAMES[ref]:<9} {whole[ref]:>3} / {in_line[ref]:>3} / "
              f"{out_line[ref]:>3}   alone {len(alone)}")
    print("  outside, by city: " + ", ".join(
        f"{n} {c}" for c, n in outside["name"].value_counts().items()))

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-scope spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    if config.MEDIAN_GAP_BOUNDS_M is None:
        sys.exit("config.MEDIAN_GAP_BOUNDS_M is unset: take the ring decision on the "
                 "median above first")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the in-scope median gap is {d.median():.0f} m, outside {lo:.0f}-{hi:.0f} - "
                 f"re-take the ring decision")
    emit("median_gap_m", round(float(d.median())))

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": [f"in {n}, outside the City of {config.NAME}"
                                   for n in outside["name"]],
                        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV, index=False,
                                                  encoding="utf-8", lineterminator="\n")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")

    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
