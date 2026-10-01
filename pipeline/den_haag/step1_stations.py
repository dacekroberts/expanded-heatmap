"""Den Haag step 1: every stop of HTM's 14 tram lines in the Gemeente Den Haag.

    python pipeline/den_haag/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

On the shared `pipeline/osm_tram.py`: stations are the stop members of the
lines' route relations, collapsed by name. Eleven lines run on into a
neighbouring gemeente: their stops there are drawn with the line but not
ringed, and are listed with the gemeente each lies in (owner, call 26, for tram
1). No stop is thinned. OSM's colours are checked against config, so a recolour
upstream stops the build rather than drifting the map.
"""
import math
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.den_haag import config  # noqa: E402
from pipeline.den_haag.gemeenten import FETCH, gemeente_polygons  # noqa: E402


def check_colours(els):
    """OSM's `colour` per kept ref must still be what config recorded."""
    seen = {}
    for r in els:
        t = r.get("tags", {}) if r["type"] == "relation" else {}
        if t.get("route") == config.ROUTE and t.get("ref") in config.LINE_REFS:
            seen.setdefault(t["ref"], set()).add(t.get("colour"))
    for ref in config.LINE_REFS:
        want = config.OSM_COLOURS.get(ref)
        got = {c.lower() if c else None for c in seen.get(ref, set())}
        if got != {want}:
            sys.exit(f"line {ref}: OSM's colour is now {sorted(map(str, got))}, config "
                     f"recorded {want!r} - re-run the colour measurement")


def split_shared_names(q):
    """Label apart the stops HTM gives one name (config.SPLIT_LINK_M).

    A name's stop positions are grouped by single linkage in metres; a name in
    one group is untouched, and a name in several has each group labelled with
    the lines that serve it. Exits if two groups of a name are served by the
    same lines, since the label would not tell them apart."""
    pts = gpd.GeoSeries(gpd.points_from_xy(q["longitude"], q["latitude"]),
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    q = q.assign(_x=pts.x.values, _y=pts.y.values)
    order = list(config.LINE_REFS)
    renamed = {}
    for name, g in q.drop_duplicates("node").groupby("stop_name"):
        nodes = list(g["node"])
        xy = {n: (x, y) for n, x, y in zip(g["node"], g["_x"], g["_y"])}
        parent = {n: n for n in nodes}

        def find(n):
            while parent[n] != n:
                n = parent[n]
            return n
        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                if math.dist(xy[a], xy[b]) <= config.SPLIT_LINK_M:
                    parent[find(a)] = find(b)
        groups = {}
        for n in nodes:
            groups.setdefault(find(n), []).append(n)
        if len(groups) == 1:
            continue
        labels = []
        for members in groups.values():
            lines = sorted(set(q.loc[q["node"].isin(members), "line"]), key=order.index)
            label = f"{name} ({'line' if len(lines) == 1 else 'lines'} {'/'.join(lines)})"
            labels.append(label)
            for n in members:
                renamed[n] = label
        if len(set(labels)) != len(labels):
            sys.exit(f"{name!r}: two separate stops served by the same lines - "
                     f"{labels}; name them by place instead")
        print(f"    {name!r} is {len(groups)} stops: " + ", ".join(labels))
    q = q.drop(columns=["_x", "_y"])
    q["stop_name"] = [renamed.get(n, s) for n, s in zip(q["node"], q["stop_name"])]
    return q, len(set(renamed.values()))


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    gem = gemeente_polygons()
    els = osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH)
    check_colours(els)
    q = osm_tram.stop_rows(els, routes=(config.ROUTE,), refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD, name_aliases=config.NAME_ALIASES)
    print("\n  stop names HTM gives to more than one stop:")
    q, n_split = split_shared_names(q)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED,
                                      max_spread_m=config.COLLAPSE_MAX_SPREAD_M)
    print()
    res = station_gates.verify_stations(
        city="Den Haag", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={ref: int(st["lines"].str.split("/").apply(
            lambda ls: ref in ls).sum()) for ref in config.LINE_REFS})
    # Gate 3 stops a tram step 1 (the tram-city skill).
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with HTM's own stop counts - " + "; ".join(
            f"{ref}: build {b}, HTM {o}" for ref, (b, o) in res["per_line_mismatches"].items()))

    inside, outside = osm_tram.split_by_places(st, gem, keep={config.GEMEENTE_CODE})
    print(f"\n  {len(st)} tram stops -> {len(inside)} in the Gemeente Den Haag, "
          f"{len(outside)} elsewhere")

    # Per line: stops inside / all (the brief's stub figures).
    allq = q.drop_duplicates(["line", "stop_name"])
    ins = set(inside["stop_name"])
    print("\n  per line, stop names inside / all:")
    for ref in config.LINE_REFS:
        names = set(allq.loc[allq["line"] == ref, "stop_name"])
        k = len(names & ins)
        print(f"    {config.LINE_NAMES[ref]:<16} {k:>3} / {len(names):<3} ({k / len(names):.0%})")
        if k == 0:
            sys.exit(f"line {ref} has no stop in the gemeente - a stub question for the owner")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-gemeente spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    lo, hi = config.MEDIAN_GAP_BOUNDS_M
    if not lo <= d.median() <= hi:
        sys.exit(f"the in-gemeente median gap is {d.median():.0f} m; the halved rings were "
                 f"chosen at 335 m - re-take the ring decision")

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": [f"in {n} (gemeente {r}), outside the Gemeente Den Haag"
                                   for n, r in zip(outside["name"], outside["ref"])],
                        "latitude": outside["latitude"], "longitude": outside["longitude"]})
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV,
                                                  index=False, encoding="utf-8")
    print(f"\n  {len(out)} excluded station(s) -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    print("    by gemeente: " + ", ".join(f"{k} {v}" for k, v in
                                          outside["name"].value_counts().items()))

    keep = (inside.rename(columns={"stop_name": "station"})
            [["station", "lines", "latitude", "longitude"]].sort_values("station"))
    keep.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))
    emit("median_gap_m", round(float(d.median())))
    emit("shared_name_stops", n_split)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
