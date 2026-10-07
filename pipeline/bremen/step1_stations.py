"""Bremen step 1: every stop of BSAG's eight tram lines in the City of Bremen.

    python pipeline/bremen/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Geneva's step 1 on the shared `pipeline/osm_tram.py`: stations are the stop
members of the kept tram relations, collapsed by name. Gate 3 compares the
whole lines with BSAG's own timetable index and stops on a mismatch. Line 4
runs on into Lilienthal (Lower Saxony): its stops there are drawn with the
line but not ringed, and are listed with the municipality each lies in
(owner, 2026-10-05, brief call 2; Florence's T1 and Göteborg's 4 and 12). No
stop is thinned.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm_tram  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.bremen import config  # noqa: E402
from pipeline.bremen.boundary import FETCH, place_polygons  # noqa: E402


def _is_named_stop(tags):
    return bool(tags.get("name")) and (tags.get("public_transport") == "stop_position"
                                       or tags.get("railway") == "tram_stop")


def drop_untagged_members(els):
    """Remove config.UNTAGGED_STOP_MEMBERS from the kept relations' member
    lists, in memory (config's comment), after checking each entry is still
    true. Returns the element list with the affected relations copied."""
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rels = [e for e in els if e["type"] == "relation"
            and e.get("tags", {}).get("route") in config.ROUTES
            and e["id"] not in config.NOT_DRAWN]
    out = {id(e): e for e in els}
    for node_id, name in config.UNTAGGED_STOP_MEMBERS.items():
        n = nodes.get(node_id)
        if n is None or n.get("tags"):
            sys.exit(f"UNTAGGED_STOP_MEMBERS {node_id} ({name}): OSM now has "
                     f"{(n or {}).get('tags', 'no such node')} - re-read it and remove the entry")
        users = [r for r in rels if any(m["type"] == "node" and m["ref"] == node_id
                                        and m.get("role", "").startswith("stop") for m in r["members"])]
        if not users:
            sys.exit(f"UNTAGGED_STOP_MEMBERS {node_id} ({name}) is no longer a stop member of a "
                     f"kept relation - remove the entry")
        named = [m for m in nodes.values() if m.get("tags", {}).get("name") == name
                 and _is_named_stop(m["tags"])]
        pts = gpd.GeoSeries(gpd.points_from_xy([n["lon"]] + [m["lon"] for m in named],
                                               [n["lat"]] + [m["lat"] for m in named]),
                            crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
        gap = float(pts.iloc[1:].distance(pts.iloc[0]).min()) if named else float("inf")
        if gap > config.UNTAGGED_MAX_M:
            sys.exit(f"UNTAGGED_STOP_MEMBERS {node_id}: the nearest stop named {name!r} is "
                     f"{gap:.0f} m away, over {config.UNTAGGED_MAX_M:.0f} m - re-read it")
        for r in users:
            ref = r["tags"].get("ref")
            others = {m["ref"] for s in rels if s["tags"].get("ref") == ref for m in s["members"]
                      if m["type"] == "node" and m.get("role", "").startswith("stop")
                      and m["ref"] != node_id}
            if not any(nodes.get(x, {}).get("tags", {}).get("name") == name for x in others):
                sys.exit(f"UNTAGGED_STOP_MEMBERS {node_id}: line {ref} has no other stop named "
                         f"{name!r}, so dropping it would lose the stop - re-read it")
            copy = dict(r, members=[m for m in r["members"] if m["ref"] != node_id
                                    or m["type"] != "node"])
            out[id(r)] = copy
        print(f"  untagged stop member {node_id} dropped from relation(s) "
              f"{[r['id'] for r in users]}: {gap:.0f} m from a named {name!r} stop")
    return [out[id(e)] for e in els]


def fold_names(q):
    """OSM's per-platform names to BSAG's one name per stop (config.NAME_FOLD),
    stopping on a listed name OSM no longer uses."""
    stale = sorted(set(config.NAME_FOLD) - set(q["stop_name"]))
    if stale:
        sys.exit(f"NAME_FOLD lists name(s) OSM no longer uses: {stale} - re-read OSM and "
                 f"update the list")
    hit = q["stop_name"].isin(config.NAME_FOLD)
    q = q.copy()
    q["stop_name"] = q["stop_name"].replace(config.NAME_FOLD)
    print(f"\n  {int(hit.sum())} stop position(s) renamed by the name fold, into "
          f"{sorted(set(config.NAME_FOLD.values()))}")
    return q


def per_line(frame):
    return {ref: int(frame["lines"].str.split("/").apply(lambda ls: ref in ls).sum())
            for ref in config.LINE_REFS}


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    print("Reading cached OSM:")
    places = place_polygons()
    els = drop_untagged_members(
        osm_tram.read_elements(config.OSM_ROUTES_JSON, "rail relations", FETCH))
    q = osm_tram.stop_rows(els, routes=config.ROUTES, refs=config.LINE_REFS,
                           operator=config.OPERATOR, not_drawn=config.NOT_DRAWN,
                           station_add=config.STATION_ADD, name_aliases=config.NAME_ALIASES)
    q = fold_names(q)
    platforms, st = osm_tram.collapse(q, refs=config.LINE_REFS,
                                      crs_projected=config.CRS_PROJECTED,
                                      max_spread_m=config.MAX_SPREAD_M)
    print()
    res = station_gates.verify_stations(
        city="Bremen", platforms=platforms, stations=st,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=per_line(st))
    # Gate 3 stops a tram step 1 (the tram-city skill).
    if res["per_line_mismatches"]:
        sys.exit("gate 3: the build disagrees with BSAG's own stop counts - " + "; ".join(
            f"{ref}: build {b}, BSAG {o}" for ref, (b, o) in res["per_line_mismatches"].items()))

    inside, outside = osm_tram.split_by_places(st, places, keep={config.CITY_AGS})
    print(f"\n  {len(st)} tram stops -> {len(inside)} in the City of Bremen, "
          f"{len(outside)} elsewhere")
    ins, outs = per_line(inside), per_line(outside)
    print("  per line, in / outside the city: " + ", ".join(
        f"{ref} {ins[ref]}/{outs[ref]}" for ref in config.LINE_REFS))
    if (config.EXPECTED_IN_SCOPE is not None
            and (len(inside), len(outside)) != (config.EXPECTED_IN_SCOPE, config.EXPECTED_OUTSIDE)):
        sys.exit(f"expected {config.EXPECTED_IN_SCOPE} inside and {config.EXPECTED_OUTSIDE} "
                 f"outside (the build of 2026-10-07) - re-read OSM")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"\n  in-city spacing (nearest neighbour, m): min {d.min():,.0f}  "
          f"median {d.median():,.0f}  mean {d.mean():,.0f}  max {d.max():,.0f}")
    if config.MEDIAN_GAP_BOUNDS_M is not None:
        lo, hi = config.MEDIAN_GAP_BOUNDS_M
        if not lo <= d.median() <= hi:
            sys.exit(f"the in-city median gap is {d.median():.0f} m, outside {lo:.0f}-{hi:.0f} - "
                     f"re-take the ring decision")
    emit("median_gap_m", round(float(d.median())))

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": [f"in {n}, Lower Saxony, outside the City of Bremen"
                                   for n in outside["name"]],
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

    emit("stop_positions", len(platforms))
    emit("stations_collapsed", len(st))
    emit("stations_in_scope", len(keep))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
