"""Glasgow step 1: the Subway - one 15-station loop - from OpenStreetMap's two
route relations (SPT publishes no GTFS for it).

    python pipeline/glasgow/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

LINES. The Outer and Inner Circle are the loop's two directions, in twin
tunnels metres apart. London's branch rule keeps the longest relation and adds
another only where it brings real new track, so the loop is drawn ONCE, as
one line in SPT orange (the brief). Written to config.LINES_GEOJSON for step 3.

STATIONS. Route-relation stop members of EVERY stop role (the loop starts and
ends at Govan, a `stop_entry_only` / `stop_exit_only` member), names
normalised, collapsed by name within config.STATION_CLUSTER_M; gate 3 against
the operator's 15.
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
from pipeline.glasgow import config  # noqa: E402

BRANCH_NEAR_M = 300
BRANCH_MIN_NEW_M = 1000


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/glasgow/fetch_sources.py")
    return path


def write_lines(rels, city):
    geoms = {}
    for r in rels:
        ways = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                for m in r.get("members", [])
                if m.get("type") == "way" and len(m.get("geometry") or []) >= 2]
        geoms[r["id"]] = gpd.GeoSeries([unary_union(ways).intersection(city)],
                                       crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).iloc[0]
    chosen, covered = [], None
    for rid in sorted(geoms, key=lambda i: -geoms[i].length):
        g = geoms[rid]
        new = g if covered is None else g.difference(covered.buffer(BRANCH_NEAR_M))
        if new.length >= BRANCH_MIN_NEW_M:
            chosen.append(rid)
            covered = g if covered is None else covered.union(new)
    merged = linemerge(covered) if covered.geom_type == "MultiLineString" else covered
    merged = gpd.GeoSeries([merged], crs=config.CRS_PROJECTED).to_crs(config.CRS_GEOGRAPHIC).iloc[0]
    parts = [p for p in getattr(merged, "geoms", [merged]) if p.length > 0]
    names = {r["id"]: r["tags"].get("name") for r in rels}
    colours = sorted({r["tags"].get("colour", "") for r in rels if r["id"] in chosen})
    print(f"  Subway: {[names[i] for i in chosen]} of {len(rels)} relations -> {len(parts)} part(s), "
          f"{covered.length / 1000:.1f} km, colour {colours}")
    feats = [{"type": "Feature",
              "properties": {"line": "Subway", "osm_relations": chosen, "osm_colour": colours},
              "geometry": mapping(MultiLineString(parts))}]
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")
    print(f"  1 line -> {config.LINES_GEOJSON.relative_to(config.ROOT)}")


def station_name(raw):
    name = raw.strip().replace("’", "'")
    name = re.sub(r"\s+(subway\s+)?(station|Station)$", "", name).strip()
    return config.STATION_NAME_ALIASES.get(name, name)


def write_stations(rels, city):
    stops = {e["id"]: e for e in json.loads(config.OSM_STOPS_JSON.read_text(encoding="utf-8"))["elements"]}
    members = set()
    for r in rels:
        mine = {m["ref"] for m in r.get("members", [])
                if m.get("type") == "node" and m.get("role", "").startswith("stop") and m["ref"] in stops}
        n = len({station_name(stops[i]["tags"].get("name", "")) for i in mine})
        if n != config.EXPECTED_STATIONS_PER_RELATION:
            sys.exit(f"{r['tags'].get('name')}: {n} distinct stop names, expected "
                     f"{config.EXPECTED_STATIONS_PER_RELATION} - OSM changed; read it first")
        members |= mine
    to_m = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
    by_name = {}
    for nid in members:
        s = stops[nid]
        by_name.setdefault(station_name(s["tags"].get("name", "")), []).append(s)
    unused = sorted(set(config.STATION_NAME_ALIASES) - {s["tags"].get("name") for s in stops.values()})
    if unused:
        print(f"  NOTE: config.STATION_NAME_ALIASES no longer needed for {unused} - retire it")
    rows = []
    for name, ss in by_name.items():
        xy = [to_m.transform(s["lon"], s["lat"]) for s in ss]
        far = max(math.dist(a, b) for a in xy for b in xy)
        if far > config.STATION_CLUSTER_M:
            sys.exit(f"{name!r}: its stop nodes are {far:.0f} m apart - two places under one name?")
        rows.append({"station": name, "lines": "Subway",
                     "latitude": sum(s["lat"] for s in ss) / len(ss),
                     "longitude": sum(s["lon"] for s in ss) / len(ss)})
    st = pd.DataFrame(rows)
    print(f"  {len(members)} stop nodes -> {len(st)} stations")
    g = gpd.GeoDataFrame(st, geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                         crs=config.CRS_GEOGRAPHIC)
    inside = g.within(city)
    print(f"  Glasgow City: {int(inside.sum())} inside, {int((~inside).sum())} outside")
    station_gates.verify_stations(
        city="Glasgow",
        platforms=pd.DataFrame([{"latitude": stops[n]["lat"], "longitude": stops[n]["lon"]} for n in members]),
        stations=st[inside.values].reset_index(drop=True), crs_projected=config.CRS_PROJECTED,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line={"Subway": len(st)})
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")
    out = (st[~inside.values].assign(reason="outside Glasgow City")
           [["station", "lines", "reason", "latitude", "longitude"]].sort_values("station"))
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = st[inside.values].sort_values("station").reset_index(drop=True)
    keep.insert(0, "stop_id", keep["station"])
    keep[["stop_id", "station", "lines", "latitude", "longitude"]].to_csv(
        config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}; "
          f"{len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")


def main():
    need(config.OSM_ROUTES_JSON, "the OSM route relations")
    need(config.OSM_STOPS_JSON, "the OSM stop nodes")
    need(config.CITY_BOUNDARY_GEOJSON, "the Glasgow City boundary")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    rels = [e for e in json.loads(config.OSM_ROUTES_JSON.read_text(encoding="utf-8"))["elements"]
            if e.get("type") == "relation"]
    if len(rels) != config.EXPECTED_RELATIONS:
        sys.exit(f"{len(rels)} Subway relations, expected {config.EXPECTED_RELATIONS} - read OSM first")
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC).union_all()
    write_lines(rels, city)
    write_stations(rels, city)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
