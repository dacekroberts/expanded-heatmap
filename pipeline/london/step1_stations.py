"""London step 1: the Underground, DLR, Elizabeth line and Overground inside
Greater London - line geometry and stations from OpenStreetMap's route
relations (TfL publishes no GTFS, and its API draws straight lines).

STATIONS. Route-relation stop members, names normalised and collapsed, split
where a name's stops are far apart, eight stations OSM's relations omit added
from their station nodes; gate 3 against the published per-line counts.

    python pipeline/london/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

LINES. Every relation of a line (both directions, every branch) is merged into
one MultiLineString and clipped to Greater London: the Northern's two branches,
the District's and the DLR's five routes are one labelled line each, as TfL
presents them. Written to config.LINES_GEOJSON for step 3
(`load_geojson_line_shapes`, Tokyo's and Berlin's contract).
"""
import json
import math
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, mapping
from shapely.ops import linemerge, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.london import config  # noqa: E402


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/london/fetch_sources.py")
    return path


def write_lines(rels, city):
    by_ref = {}
    for r in rels:
        by_ref.setdefault(r["tags"].get("ref"), []).append(r)
    wanted = {ref for refs in config.LINE_OSM_REFS.values() for ref in refs}
    extra = sorted(set(by_ref) - wanted, key=str)
    if extra:
        sys.exit(f"the OSM query returned refs no line claims: {extra} - a scope question")
    feats = []
    print("  lines (every relation merged, clipped to Greater London):")
    for key, refs in config.LINE_OSM_REFS.items():
        mine = [r for ref in refs for r in by_ref.get(ref, [])]
        if not mine:
            sys.exit(f"{key}: no relation with ref(s) {refs} - OSM changed; read it first")
        # One direction per branch: the longest relation first, then only those
        # adding real new track - a line's two directions often run on parallel
        # tracks metres apart, and merging both doubled Central to 127 km in
        # 89 fragments (2026-09-28), which the label solver anchors badly.
        geoms = {}
        for r in mine:
            ways = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                    for m in r.get("members", [])
                    if m.get("type") == "way" and len(m.get("geometry") or []) >= 2]
            if ways:
                geoms[r["id"]] = gpd.GeoSeries([unary_union(ways).intersection(city)],
                                               crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).iloc[0]
        chosen, covered = [], None
        for rid in sorted(geoms, key=lambda i: -geoms[i].length):
            g = geoms[rid]
            new = g if covered is None else g.difference(covered.buffer(config.BRANCH_NEAR_M))
            if new.length >= config.BRANCH_MIN_NEW_M:
                chosen.append(rid)
                # Only the NEW part: the relation's shared stretch runs on
                # parallel tracks metres away and would draw the core twice.
                covered = g if covered is None else covered.union(new)
        merged = linemerge(covered) if covered.geom_type == "MultiLineString" else covered
        merged = gpd.GeoSeries([merged], crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC).iloc[0]
        parts = list(getattr(merged, "geoms", [merged]))
        colours = sorted({r["tags"].get("colour", "") for r in mine})
        km = covered.length / 1000
        print(f"    {key:<20} {len(chosen):>2} of {len(mine):>2} relations -> {len(parts):>3} parts, "
              f"{km:6.1f} km  colour {colours}")
        feats.append({"type": "Feature",
                      "properties": {"line": key, "osm_refs": list(refs), "osm_colour": colours},
                      "geometry": mapping(MultiLineString([p for p in parts if p.length > 0]))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")
    print(f"  {len(feats)} lines -> {config.LINES_GEOJSON.relative_to(config.ROOT)}")


def station_name(raw):
    """"Beckton Platform 1", "South Acton (Platform 1)" and "Canary Wharf
    Platforms 1 & 2" -> the station; "Blackhorse Road station" -> "Blackhorse
    Road"; then config.STATION_NAME_ALIASES (one station, two names)."""
    name = raw.strip().replace("’", "'")
    name = re.sub(r"\s*\(?\bPlatforms?\s+[\w/&\s-]+\)?$", "", name)
    name = re.sub(r"\s+(station|Station)$", "", name).strip()
    return config.STATION_NAME_ALIASES.get(name, name)


def clusters(xy, radius):
    """Single-linkage groups of points within `radius` metres."""
    n, group = len(xy), list(range(len(xy)))

    def find(i):
        while group[i] != i:
            group[i] = group[group[i]]
            i = group[i]
        return i
    for i in range(n):
        for j in range(i + 1, n):
            if math.dist(xy[i], xy[j]) <= radius:
                group[find(i)] = find(j)
    out = {}
    for i in range(n):
        out.setdefault(find(i), []).append(i)
    return list(out.values())


def write_stations(rels, city):
    """Stations from ROUTE-RELATION MEMBERSHIP (osm-rail's rule), collapsed by
    normalised name and split where same-named stops are more than
    config.STATION_CLUSTER_M apart - Hammersmith is two Underground stations,
    Bethnal Green an Underground and an Overground one ~600 m apart."""
    stops = {e["id"]: e for e in json.loads(config.OSM_STOPS_JSON.read_text(encoding="utf-8"))["elements"]}
    line_of_ref = {ref: key for key, refs in config.LINE_OSM_REFS.items() for ref in refs}
    lines_at = {}
    for r in rels:
        key = line_of_ref[r["tags"]["ref"]]
        for m in r.get("members", []):
            if m.get("type") == "node" and m.get("role", "").startswith("stop") and m["ref"] in stops:
                lines_at.setdefault(m["ref"], set()).add(key)
    to_m = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
    rows = []
    by_name = {}
    for nid, lines in lines_at.items():
        s = stops[nid]
        by_name.setdefault(station_name(s["tags"].get("name", "")), []).append((nid, s, lines))
    carried = sorted(n for n in config.STATION_ADDITIONS if n in by_name)
    if carried:
        sys.exit(f"OSM's relations now carry {carried}: take them out of "
                 f"config.STATION_ADDITIONS and re-run")
    extra = json.loads(config.OSM_ADDITIONS_JSON.read_text(encoding="utf-8"))["elements"]
    for name, line in config.STATION_ADDITIONS.items():
        nodes = [e for e in extra if e["tags"].get("name") == name]
        if not nodes:
            sys.exit(f"no OSM station node named {name!r} in {config.OSM_ADDITIONS_JSON.name}")
        by_name[name] = [(n["id"], n, {line}) for n in nodes]
    print(f"  added by config.STATION_ADDITIONS: {', '.join(config.STATION_ADDITIONS)}")
    split = []
    for name, members in by_name.items():
        xy = [to_m.transform(s["lon"], s["lat"]) for _, s, _ in members]
        groups = clusters(xy, config.STATION_CLUSTER_M)
        if len(groups) > 1:
            split.append((name, len(groups)))
        for g in groups:
            ms = [members[i] for i in g]
            rows.append({"station": name,
                         "lines": "/".join(sorted(set().union(*(m[2] for m in ms)),
                                                  key=list(config.LINE_OSM_REFS).index)),
                         "latitude": sum(m[1]["lat"] for m in ms) / len(ms),
                         "longitude": sum(m[1]["lon"] for m in ms) / len(ms),
                         "platforms": len(ms)})
    st = pd.DataFrame(rows)
    print(f"\n  {len(lines_at)} stop nodes -> {len(by_name)} names -> {len(st)} stations; "
          f"names that are more than one place: {sorted(split)}")
    g = gpd.GeoDataFrame(st, geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                         crs=config.CRS_GEOGRAPHIC)
    inside = g.within(city)
    print(f"  Greater London: {int(inside.sum())} inside, {int((~inside).sum())} outside")
    per_line = {k: (int(sum(k in v.split("/") for v in st["lines"][inside])),
                    int(sum(k in v.split("/") for v in st["lines"])))
                for k in config.LINE_OSM_REFS}
    print("  per line, inside of all: " + ", ".join(f"{k} {a}/{b}" for k, (a, b) in per_line.items()))
    actual = {k: b for k, (_, b) in per_line.items() if k in config.OPERATOR_STATION_COUNTS}
    actual["Overground (network)"] = int(st["lines"].map(
        lambda v: bool(set(v.split("/")) & set(config.OVERGROUND_LINES))).sum())
    station_gates.verify_stations(city="London", platforms=pd.DataFrame(
        [{"latitude": s["lat"], "longitude": s["lon"]} for s in (stops[n] for n in lines_at)]),
        stations=st[inside.values].reset_index(drop=True), crs_projected=config.CRS_PROJECTED,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")
    out = (st[~inside.values].assign(reason="outside Greater London (the FSA's London region)")
           [["station", "lines", "reason", "latitude", "longitude"]].sort_values("station"))
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = st[inside.values].sort_values(["station", "latitude"]).reset_index(drop=True)
    keep.insert(0, "stop_id", [f"{r.station}|{r.latitude:.4f}" for r in keep.itertuples()])
    keep[["stop_id", "station", "lines", "latitude", "longitude"]].to_csv(
        config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}; "
          f"{len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")


def main():
    need(config.OSM_ROUTES_JSON, "the OSM route relations")
    need(config.CITY_BOUNDARY_GEOJSON, "the Greater London boundary")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    rels = [e for e in json.loads(config.OSM_ROUTES_JSON.read_text(encoding="utf-8"))["elements"]
            if e.get("type") == "relation"]
    skipped = [r for r in rels if r["tags"].get("name", "").startswith(config.RELATION_NAMES_SKIPPED)]
    if len(skipped) == 0 and config.RELATION_NAMES_SKIPPED:
        print(f"  NOTE: no relation matches config.RELATION_NAMES_SKIPPED any more - retire it")
    rels = [r for r in rels if r not in skipped]
    print(f"  {len(rels)} relations ({len(skipped)} skipped by name)")
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC).union_all()
    write_lines(rels, city)
    write_stations(rels, city)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
