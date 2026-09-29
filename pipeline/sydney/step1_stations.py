"""Sydney step 1: Sydney Trains' T1, T2, T3, T4, T8 and T9 and Sydney Metro's
M1 inside the City of Sydney - line geometry and stations from OpenStreetMap's
route relations (Transport for NSW's GTFS needs an API key, not needed here).

    python pipeline/sydney/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

LINES. Each line's relations (directions and branches) are merged by London's
branch rule - the longest first, another only where it adds real new track -
and clipped to the LGA, where the lines are drawn (written to
config.LINES_GEOJSON for step 3).

STATIONS. Route-relation stop members of every stop role, names normalised and
collapsed within config.STATION_CLUSTER_M; the lines run far beyond the LGA,
so most stations are outside it and listed in outputs/sydney/
excluded_stations.csv. Gate 3: the stations inside against the brief's 16.
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
from pipeline.sydney import config  # noqa: E402


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/sydney/fetch_sources.py")
    return path


def write_lines(rels, area):
    by_ref = {}
    for r in rels:
        by_ref.setdefault(r["tags"].get("ref"), []).append(r)
    wanted = {ref for refs in config.LINE_OSM_REFS.values() for ref in refs}
    extra = sorted(set(by_ref) - wanted, key=str)
    if extra:
        sys.exit(f"the OSM query returned refs no line claims: {extra} - a scope question")
    feats = []
    print("  lines (directions and branches merged, clipped to the City of Sydney):")
    for key, refs in config.LINE_OSM_REFS.items():
        mine = [r for ref in refs for r in by_ref.get(ref, [])]
        if not mine:
            sys.exit(f"{key}: no relation with ref(s) {refs} - OSM changed; read it first")
        geoms = {}
        for r in mine:
            ways = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                    for m in r.get("members", [])
                    if m.get("type") == "way" and len(m.get("geometry") or []) >= 2]
            if ways:
                geoms[r["id"]] = gpd.GeoSeries([unary_union(ways).intersection(area)],
                                               crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).iloc[0]
        chosen, covered = [], None
        for rid in sorted(geoms, key=lambda i: -geoms[i].length):
            g = geoms[rid]
            new = g if covered is None else g.difference(covered.buffer(config.BRANCH_NEAR_M))
            if new.length >= config.BRANCH_MIN_NEW_M:
                chosen.append(rid)
                covered = g if covered is None else covered.union(new)
        merged = linemerge(covered) if covered.geom_type == "MultiLineString" else covered
        merged = gpd.GeoSeries([merged], crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC).iloc[0]
        parts = [p for p in getattr(merged, "geoms", [merged]) if p.length > 0]
        colours = sorted({r["tags"].get("colour", "") for r in mine})
        print(f"    {key:<8} {len(chosen)} of {len(mine)} relations -> {len(parts):>3} parts, "
              f"{covered.length / 1000:6.1f} km  colour {colours}")
        feats.append({"type": "Feature",
                      "properties": {"line": key, "osm_refs": list(refs), "osm_colour": colours},
                      "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")
    print(f"  {len(feats)} lines -> {config.LINES_GEOJSON.relative_to(config.ROOT)}")


def station_name(raw):
    """OSM's Sydney stop names carry the platform three ways - "Central,
    Platform 16", "Campbelltown Platform 2" and "Gadigal 1" - and sometimes
    "Station": "Emu Plains Station, Platform 1" -> "Emu Plains"."""
    name = raw.strip().replace("’", "'")
    name = re.sub(r",?\s+[Pp]latforms?\s+[\w/&\s-]+$", "", name).strip()
    name = re.sub(r"\s+\d+[A-Za-z]?$", "", name).strip()
    name = re.sub(r"\s+(Metro\s+)?(station|Station)$", "", name).strip()
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


def write_stations(rels, area):
    stops = {e["id"]: e for e in json.loads(config.OSM_STOPS_JSON.read_text(encoding="utf-8"))["elements"]}
    line_of_ref = {ref: key for key, refs in config.LINE_OSM_REFS.items() for ref in refs}
    lines_at = {}
    for r in rels:
        key = line_of_ref[r["tags"]["ref"]]
        for m in r.get("members", []):
            if m.get("type") == "node" and m.get("role", "").startswith("stop") and m["ref"] in stops:
                lines_at.setdefault(m["ref"], set()).add(key)
    unused = sorted(set(config.STATION_NAME_ALIASES) - {s["tags"].get("name") for s in stops.values()})
    if unused:
        print(f"  NOTE: config.STATION_NAME_ALIASES no longer needed for {unused} - retire it")
    to_m = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
    by_name = {}
    for nid, lines in lines_at.items():
        s = stops[nid]
        by_name.setdefault(station_name(s["tags"].get("name", "")), []).append((nid, s, lines))
    rows, split = [], []
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
                         "longitude": sum(m[1]["lon"] for m in ms) / len(ms)})
    st = pd.DataFrame(rows)
    print(f"\n  {len(lines_at)} stop nodes -> {len(by_name)} names -> {len(st)} stations; "
          f"names that are more than one place: {sorted(split)}")
    g = gpd.GeoDataFrame(st, geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                         crs=config.CRS_GEOGRAPHIC)
    inside = g.within(area)
    print(f"  the City of Sydney: {int(inside.sum())} inside, {int((~inside).sum())} outside")
    ins = st[inside.values]
    per_line = {k: int(sum(k in v.split("/") for v in ins["lines"])) for k in config.LINE_OSM_REFS}
    print("  per line, inside: " + ", ".join(f"{k} {n}" for k, n in per_line.items()))
    names_in = set(ins["station"])
    missing, extra = config.EXPECTED_STATIONS - names_in, names_in - config.EXPECTED_STATIONS
    print(f"  gate 3: {len(names_in)} names inside, the brief lists {len(config.EXPECTED_STATIONS)}; "
          f"missing {sorted(missing)}, extra {sorted(extra)}")
    if missing or extra:
        sys.exit("  the stations inside the LGA disagree with the brief's list - read which before going on")
    station_gates.verify_stations(
        city="Sydney",
        platforms=pd.DataFrame([{"latitude": stops[n]["lat"], "longitude": stops[n]["lon"]} for n in lines_at]),
        stations=ins.reset_index(drop=True), crs_projected=config.CRS_PROJECTED)
    out = (st[~inside.values].assign(reason="outside the City of Sydney")
           [["station", "lines", "reason", "latitude", "longitude"]].sort_values("station"))
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = st[inside.values].sort_values(["station", "latitude"]).reset_index(drop=True)
    keep.insert(0, "stop_id", keep["station"])
    keep[["stop_id", "station", "lines", "latitude", "longitude"]].to_csv(
        config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}; "
          f"{len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")


def main():
    need(config.OSM_ROUTES_JSON, "the OSM route relations")
    need(config.OSM_STOPS_JSON, "the OSM stop nodes")
    need(config.CITY_BOUNDARY_GEOJSON, "the City of Sydney boundary")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    rels = [e for e in json.loads(config.OSM_ROUTES_JSON.read_text(encoding="utf-8"))["elements"]
            if e.get("type") == "relation"]
    print(f"  {len(rels)} relations")
    area = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC).union_all()
    write_lines(rels, area)
    write_stations(rels, area)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
