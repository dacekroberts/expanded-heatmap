"""Tbilisi step 1: the metro's 23 stations, its two lines as GeoJSON, and the
city boundary.

    python pipeline/tbilisi/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Rail from OpenStreetMap route-relation membership (the osm-rail skill): the
subway relations in the box, two per line (one per direction), whitelisted on
`ref`; any other subway relation exits. Stations are the relations' `stop`
members, collapsed by name, checked against the `station=subway` nodes and
against the operator's count (gate 3). Each line is written from the
relation with the most track.

Every station is inside the city, so excluded_stations.csv is written with a
header and no rows (Calgary's precedent).
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, MultiLineString, Point, mapping
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.tbilisi import config  # noqa: E402

COLLAPSE_MAX_SPREAD_M = 200
STATION_NODE_MAX_M = 300


def track(rel, ways):
    """The relation's track ways as coordinate lists. The query outputs the
    relations as `out body` and the ways as `out geom` (the cheaper form), so
    geometry is joined by member ref."""
    return [[(p["lon"], p["lat"]) for p in ways[m["ref"]]["geometry"]]
            for m in rel["members"]
            if m["type"] == "way" and m["ref"] in ways
            and not m.get("role", "").startswith("platform")]


def boundary(rels):
    """The city of Tbilisi's administrative polygon, from its outer ways."""
    found = [r for r in rels if r.get("tags", {}).get("boundary") == "administrative"]
    if len(found) != 1:
        sys.exit(f"{len(found)} administrative relations named "
                 f"{config.OSM_BOUNDARY_NAME_EN!r}, not one")
    r = found[0]
    outer = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
             for m in r["members"]
             if m["type"] == "way" and m.get("role") == "outer" and m.get("geometry")]
    polys = list(polygonize(unary_union(outer)))
    if not polys:
        sys.exit(f"relation {r['id']}'s outer ways do not close")
    shape = unary_union(polys)
    print(f"  boundary: relation {r['id']} ({r['tags'].get('name')}, admin_level "
          f"{r['tags'].get('admin_level')}), {len(polys)} polygon(s)")
    return shape


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    if not config.OSM_JSON.exists():
        sys.exit(f"missing {config.OSM_JSON}\nRun: python pipeline/tbilisi/fetch_sources.py")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    els = json.loads(config.OSM_JSON.read_text(encoding="utf-8"))["elements"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    ways = {e["id"]: e for e in els if e["type"] == "way" and e.get("geometry")}
    rels = [e for e in els if e["type"] == "relation"]
    routes = [r for r in rels if r["tags"].get("type") == "route"]

    keep, rows = {}, []
    print("  subway route relations in the box:")
    for r in sorted(routes, key=lambda r: r["id"]):
        t = r["tags"]
        line = t.get("ref") if t.get("ref") in config.LINE_REFS else None
        print(f"    {'KEEP' if line else 'drop':4} {r['id']:>9} {t.get('ref', '-'):<4} "
              f"{t.get('colour', '-'):<8} {t.get('name:en') or t.get('name', '')}")
        if not line:
            sys.exit(f"relation {r['id']} is a subway route this step cannot place")
        keep.setdefault(line, []).append(r)
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            nt = (n or {}).get("tags", {})
            name = nt.get("name:en")
            if not n or not name:
                sys.exit(f"stop member {m['ref']} has no name:en")
            rows.append({"node": n["id"], "stop_name": name, "line": line,
                         "latitude": n["lat"], "longitude": n["lon"]})
    for line in config.LINE_REFS:
        if len(keep.get(line, [])) != 2:
            sys.exit(f"{len(keep.get(line, []))} relations for {config.LINE_REFS[line]}, "
                     f"not the two directions")

    q = pd.DataFrame(rows)
    fixed = sorted(set(q["stop_name"]) & set(config.STATION_NAME_FIXES))
    if fixed != sorted(config.STATION_NAME_FIXES):
        sys.exit(f"OSM no longer writes {sorted(set(config.STATION_NAME_FIXES) - set(fixed))}: "
                 f"remove it from config.STATION_NAME_FIXES")
    q["stop_name"] = q["stop_name"].replace(config.STATION_NAME_FIXES)
    print(f"  name fixed to the operator's spelling: {config.STATION_NAME_FIXES}")
    per_line = q.groupby("line")["stop_name"].nunique()
    positions = q.drop_duplicates("node")
    by_name = positions.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                                 longitude=("longitude", "mean")).reset_index()
    g = gpd.GeoDataFrame(positions, geometry=gpd.points_from_xy(positions.longitude,
                                                                positions.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"  {len(positions)} stop positions -> {len(by_name)} stations by name; widest "
          f"{spread.idxmax()} {spread.max():.0f} m")
    if (spread > COLLAPSE_MAX_SPREAD_M).any():
        sys.exit(f"names wider than {COLLAPSE_MAX_SPREAD_M} m: "
                 f"{spread[spread > COLLAPSE_MAX_SPREAD_M].round().to_dict()}")
    by_name["lines"] = by_name["stop_name"].map(
        q.groupby("stop_name")["line"].agg(lambda s: ";".join(sorted(set(s)))))

    # Every station=subway node lies within reach of one station, and each
    # station has one: the two OSM readings of the system agree.
    sn = [n for n in nodes.values() if n.get("tags", {}).get("station") == "subway"]
    sg = gpd.GeoSeries([Point(n["lon"], n["lat"]) for n in sn],
                       crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    st = gpd.GeoSeries(gpd.points_from_xy(by_name.longitude, by_name.latitude),
                       crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    far = [n.get("tags", {}).get("name:en") for n, p in zip(sn, sg)
           if st.distance(p).min() > STATION_NODE_MAX_M]
    if len(sn) != len(by_name) or far:
        sys.exit(f"{len(sn)} station=subway nodes against {len(by_name)} stations; "
                 f"unmatched: {far}")
    print(f"  {len(sn)} station=subway nodes, each within {STATION_NODE_MAX_M} m of a station")

    counts = {config.LINE_REFS[k]: int(per_line.get(k, 0)) for k in config.LINE_REFS}
    print()
    station_gates.verify_stations(
        city="Tbilisi", platforms=positions, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=counts)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")
    if len(by_name) != config.OPERATOR_STATION_TOTAL:
        sys.exit(f"{len(by_name)} stations, against the operator's {config.OPERATOR_STATION_TOTAL}")

    # --- The city: every station inside it ---------------------------------
    city = boundary(rels)
    outside = [s for s, p in zip(by_name.stop_name, gpd.points_from_xy(by_name.longitude,
                                                                       by_name.latitude))
               if not city.contains(p)]
    if outside:
        sys.exit(f"stations outside the city boundary: {outside}")
    gpd.GeoDataFrame({"name": ["Tbilisi"]}, geometry=[city], crs=config.CRS_GEOGRAPHIC).to_file(
        config.CITY_BOUNDARY_GEOJSON, driver="GeoJSON")
    area = gpd.GeoSeries([city], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area[0]
    print(f"  city area {area / 1e6:,.0f} km2; every station inside")
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")

    d = pd.Series([st.drop(i).distance(p).min() for i, p in st.items()])
    print(f"  spacing (m): min {d.min():,.0f}  median {d.median():,.0f}  max {d.max():,.0f}")
    if d.median() < 966:
        sys.exit("median under the 0.6 mi outer ring: the standard rings were chosen above it")

    out = by_name.rename(columns={"stop_name": "station"})[
        ["station", "lines", "latitude", "longitude"]].sort_values("station")
    out.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"  {len(out)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    # --- The lines: per line, the relation with the most track -------------
    feats = []
    for line, rs in keep.items():
        best = max(rs, key=lambda r: (sum(len(c) for c in track(r, ways)), -r["id"]))
        merged = linemerge(MultiLineString(track(best, ways)))
        parts = [p for p in getattr(merged, "geoms", [merged]) if not p.is_empty]
        if not parts:
            sys.exit(f"{config.LINE_REFS[line]}: relation {best['id']} has no track geometry")
        length = gpd.GeoSeries(parts, crs=config.CRS_GEOGRAPHIC).to_crs(
            config.CRS_PROJECTED).length.sum() / 1000
        print(f"  {config.LINE_REFS[line]}: relation {best['id']}, {len(parts)} piece(s), "
              f"{length:.1f} km")
        feats.append({"type": "Feature", "properties": {"line": line},
                      "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_bytes(json.dumps({"type": "FeatureCollection",
                                                 "features": feats}).encode("utf-8"))

    emit("stop_positions", len(positions))
    emit("stations_in_scope", len(out))
    for k, v in counts.items():
        emit(f"stations_{k.replace(' ', '_').replace('-', '_').lower()}", v)


if __name__ == "__main__":
    main()
