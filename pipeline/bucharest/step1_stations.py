"""Bucharest step 1: Metrorex M1-M5 inside the municipality - line geometry
and stations from OpenStreetMap's route relations (osm-rail), copied from
Stockholm's step 1.

    python pipeline/stockholm/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

LINES. Every relation of a line (both directions, every branch) is merged into
one MultiLineString and clipped to the municipality, London's method: the longest
relation first, then only those adding real new track. A relation whose ref no
line claims stops the step, unless config.RELATIONS_SKIPPED names it. Written to config.LINES_GEOJSON for step 3.

STATIONS. Route-relation stop members of every stop role, names normalised and
collapsed, split where a name's stops are far apart; gate 3 against the
published per-line counts.
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
from pipeline.bucharest import config  # noqa: E402


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {what}: {path}\nRun: python pipeline/bucharest/fetch_sources.py")
    return path


def line_geoms(rels, city):
    geoms = {}
    for r in rels:
        ways = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                for m in r.get("members", [])
                if m.get("type") == "way" and len(m.get("geometry") or []) >= 2]
        if ways:
            geoms[r["id"]] = gpd.GeoSeries([unary_union(ways).intersection(city)],
                                           crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).iloc[0]
    return geoms


def write_lines(rels, city):
    by_ref = {}
    for r in rels:
        by_ref.setdefault(r["tags"].get("ref"), []).append(r)
    wanted = {ref for refs in config.LINE_OSM_REFS.values() for ref in refs}
    extra = sorted(set(by_ref) - wanted, key=str)
    if extra:
        sys.exit(f"the OSM query returned refs no line claims: {extra} - a scope question")
    feats = []
    print(f"  lines (every relation merged, clipped to {config.CITY_LABEL}):")
    for key, refs in config.LINE_OSM_REFS.items():
        mine = [r for ref in refs for r in by_ref.get(ref, [])]
        if not mine:
            sys.exit(f"{key}: no relation with ref(s) {refs} - OSM changed; read it first")
        geoms = line_geoms(mine, city)
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
        print(f"    {key:<8} {len(chosen):>2} of {len(mine):>2} relations -> {len(parts):>3} parts, "
              f"{covered.length / 1000:6.1f} km  colour {colours}  "
              f"{sorted({r['tags'].get('name', '') for r in mine})}")
        feats.append({"type": "Feature",
                      "properties": {"line": key, "osm_refs": list(refs), "osm_colour": colours},
                      "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")
    print(f"  {len(feats)} lines -> {config.LINES_GEOJSON.relative_to(config.ROOT)}")


def station_name(raw):
    """"T-Centralen, spår 1", "Slussen T-bana" -> the station; then
    config.STATION_NAME_ALIASES (one station, two names)."""
    name = raw.strip().replace("’", "'")
    name = re.sub(r",?\s*\(?\b(spår|plattform|platform)\s+[\w/&\s-]+\)?$", "", name, flags=re.I)
    name = re.sub(r"\s+(tunnelbanestation|t-banestation|t-bana|station)$", "", name, flags=re.I).strip()
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


def point(e):
    """A fetched member as {lat, lon, tags}: a node's own position, a way's or
    relation's centre."""
    c = e if "lat" in e else e.get("center", {})
    return {"lat": c["lat"], "lon": c["lon"], "tags": e.get("tags", {})}


def write_stations(rels, city):
    """Stations from ROUTE-RELATION MEMBERSHIP (osm-rail's rule): every stop
    role, plus every NAMED platform member - line 14 carries Tekniska
    högskolan only as a platform. A member the fetch lacks stops the step."""
    fetched = {(e["type"], e["id"]): e
               for e in json.loads(config.OSM_STOPS_JSON.read_text(encoding="utf-8"))["elements"]}
    lines_at, stops, missing, unnamed = {}, {}, [], 0
    for r in rels:
        key = r["tags"]["ref"]   # the ROUTE; rows name their lines below
        for m in r.get("members", []):
            role = m.get("role", "")
            if not (role.startswith("stop") or role.startswith("platform")):
                continue
            e = fetched.get((m["type"], m["ref"]))
            if e is None:
                missing.append((r["tags"]["ref"], m["type"], m["ref"]))
                continue
            name = e.get("tags", {}).get("name", "")
            if role.startswith("platform") and (not name or re.match(config.UNNAMED_PLATFORM, name)):
                unnamed += 1
                continue
            stops[(m["type"], m["ref"])] = point(e)
            lines_at.setdefault((m["type"], m["ref"]), set()).add(key)
    if missing:
        sys.exit(f"{len(missing)} stop/platform member(s) missing from {config.OSM_STOPS_JSON.name} - "
                 f"a mirror older than the relations? Re-fetch both from one host: {missing[:5]}")
    print(f"  {unnamed} unnamed platform members ignored (a stop member names their station)")
    raw_names = sorted({stops[n]["tags"].get("name", "") for n in lines_at})
    print(f"  {len(raw_names)} raw stop names: {raw_names}")
    unused = sorted(set(config.STATION_NAME_ALIASES) - {n.strip() for n in raw_names})
    if unused:
        print(f"  NOTE: config.STATION_NAME_ALIASES no longer needed for {unused} - retire it")
    to_m = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
    by_name = {}
    for nid, lines in lines_at.items():
        s = stops[nid]
        by_name.setdefault(station_name(s["tags"].get("name", "")), []).append((nid, s, lines))
    if "" in by_name:
        sys.exit(f"{len(by_name[''])} stop node(s) with no name - read OSM first")
    carried = sorted(n for n in config.STATION_ADDITIONS if n in by_name)
    if carried:
        sys.exit(f"OSM's relations now carry {carried}: take them out of "
                 f"config.STATION_ADDITIONS and re-run")
    extra = (json.loads(need(config.OSM_ADDITIONS_JSON, "the station additions").read_text(
        encoding="utf-8"))["elements"] if config.STATION_ADDITIONS else [])
    for name, ref in config.STATION_ADDITIONS.items():
        nodes = [e for e in extra if e["tags"].get("name") == name]
        if len(nodes) != 1:
            sys.exit(f"{len(nodes)} OSM station nodes named {name!r} in {config.OSM_ADDITIONS_JSON.name}")
        by_name[name] = [(("node", nodes[0]["id"]), point(nodes[0]), {ref})]
    if config.STATION_ADDITIONS:
        print(f"  added by config.STATION_ADDITIONS: {', '.join(config.STATION_ADDITIONS)}")
    line_of_ref = {ref: key for key, refs in config.LINE_OSM_REFS.items() for ref in refs}
    route_order = [ref for refs in config.LINE_OSM_REFS.values() for ref in refs]
    rows, split = [], []
    for name, members in by_name.items():
        xy = [to_m.transform(s["lon"], s["lat"]) for _, s, _ in members]
        groups = clusters(xy, config.STATION_CLUSTER_M)
        if len(groups) > 1:
            split.append((name, len(groups)))
        for g in groups:
            ms = [members[i] for i in g]
            refs = sorted(set().union(*(m[2] for m in ms)), key=route_order.index)
            rows.append({"station": name,
                         "lines": "/".join(sorted({line_of_ref[r] for r in refs},
                                                  key=list(config.LINE_OSM_REFS).index)),
                         "routes": "/".join(refs),
                         "latitude": sum(m[1]["lat"] for m in ms) / len(ms),
                         "longitude": sum(m[1]["lon"] for m in ms) / len(ms)})
    st = pd.DataFrame(rows)
    print(f"\n  {len(lines_at)} stop nodes -> {len(by_name)} names -> {len(st)} stations; "
          f"names that are more than one place: {sorted(split)}")
    g = gpd.GeoDataFrame(st, geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                         crs=config.CRS_GEOGRAPHIC)
    inside = g.within(city)
    print(f"  {config.CITY_LABEL}: {int(inside.sum())} inside, {int((~inside).sum())} outside: "
          f"{sorted(st['station'][~inside.values])}")
    per_route = {k: (int(sum(k in v.split("/") for v in st["routes"][inside.values])),
                     int(sum(k in v.split("/") for v in st["routes"])))
                 for k in route_order}
    print("  per route, inside of all: " + ", ".join(f"{k} {a}/{b}" for k, (a, b) in per_route.items()))
    actual = {k: b for k, (_, b) in per_route.items() if k in config.OPERATOR_STATION_COUNTS}
    actual["Metrorex (network)"] = len(st)
    station_gates.verify_stations(city="Bucharest", platforms=pd.DataFrame(
        [{"latitude": s["lat"], "longitude": s["lon"]} for s in (stops[n] for n in lines_at)]),
        stations=st[inside.values].reset_index(drop=True), crs_projected=config.CRS_PROJECTED,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")
    outside = g[~inside.values]
    if len(outside):
        places = gpd.read_file(need(config.NAMING_GEOJSON, "the naming layer"))
        named = gpd.sjoin(outside, places[["name", "geometry"]], how="left", predicate="within")
    else:
        named = outside.assign(name=pd.Series(dtype=str))
    if named["name"].isna().any():
        sys.exit(f"stations outside every place in {config.NAMING_GEOJSON.name}: "
                 f"{sorted(named['station'][named['name'].isna()])}")
    out = (named.assign(reason=f"outside {config.CITY_LABEL}, in " + named["name"])
           [["station", "lines", "reason", "latitude", "longitude"]].sort_values("station"))
    print("  excluded: " + ", ".join(f"{r.station} ({r.reason.split(', in ')[1]})" for r in out.itertuples()))
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    keep = st[inside.values].sort_values(["station", "latitude"]).reset_index(drop=True)
    keep.insert(0, "stop_id", keep["station"])
    if keep["stop_id"].duplicated().any():
        keep["stop_id"] = [f"{r.station}|{r.latitude:.4f}" for r in keep.itertuples()]
    # Every kept station must lie on a drawn line of its own: the branch rule
    # once dropped M5's Valea Ialomiței branch, leaving that terminus 519 m
    # from any track (2026-09-29).
    drawn = gpd.read_file(config.LINES_GEOJSON).to_crs(config.CRS_PROJECTED).set_index("line")
    kp = gpd.GeoSeries(gpd.points_from_xy(keep["longitude"], keep["latitude"]),
                       crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    off = [(r.station, round(min(drawn.loc[k].geometry.distance(p) for k in r.lines.split("/"))))
           for r, p in zip(keep.itertuples(), kp)]
    far = [(n, d) for n, d in off if d > config.STATION_OFF_LINE_MAX_M]
    if far:
        sys.exit(f"stations further than {config.STATION_OFF_LINE_MAX_M} m from their drawn line: {far}")
    print(f"  every station within {config.STATION_OFF_LINE_MAX_M} m of its line "
          f"(furthest {max(d for _, d in off)} m)")
    keep[["stop_id", "station", "lines", "latitude", "longitude"]].to_csv(
        config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(keep)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}; "
          f"{len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")


def main():
    need(config.OSM_ROUTES_JSON, "the OSM route relations")
    need(config.OSM_STOPS_JSON, "the OSM stop nodes")
    need(config.CITY_BOUNDARY_GEOJSON, "the municipality boundary")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    rels = [e for e in json.loads(config.OSM_ROUTES_JSON.read_text(encoding="utf-8"))["elements"]
            if e.get("type") == "relation"]
    skipped = [r for r in rels if r["id"] in config.RELATIONS_SKIPPED]
    for rid, why in config.RELATIONS_SKIPPED.items():
        if rid not in {r["id"] for r in skipped}:
            print(f"  NOTE: relation {rid} ({why}) is gone from OSM - retire config.RELATIONS_SKIPPED")
    rels = [r for r in rels if r["id"] not in config.RELATIONS_SKIPPED]
    print(f"  {len(rels)} relations ({len(skipped)} skipped: "
          f"{[config.RELATIONS_SKIPPED[r['id']] for r in skipped]})")
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC).union_all()
    write_lines(rels, city)
    write_stations(rels, city)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
