"""Buffalo step 1: NFTA Metro Rail's stations, and its line as GeoJSON.

    python pipeline/buffalo/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Rail from OpenStreetMap route-relation membership (the osm-rail skill), on
the ground recorded in config: whitelist on network + ref + route, every
other relation in the box named in config.NOT_DRAWN or the step exits.
Stations are the kept relations' `stop` members, collapsed by name. The line
is written as GeoJSON from TRACK ways only - each relation also lists its
`platform` ways, which a whole-relation draw would add as stray outlines.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, mapping
from shapely.ops import linemerge

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.buffalo import config  # noqa: E402

COLLAPSE_MAX_SPREAD_M = 200
LINES_GEOJSON = config.LINES_GEOJSON


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/buffalo/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def track(rel):
    return [m for m in rel["members"] if m["type"] == "way" and m.get("geometry")
            and not m.get("role", "").startswith("platform")]


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    els = read_cached(config.OSM_ROUTES_JSON, "rail relations")["elements"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rels = [e for e in els if e["type"] == "relation"]

    def kept(t):
        return (t.get("network") == config.NETWORK and t.get("ref") == config.REF
                and t.get("route") == "light_rail")

    print("  route relations in the box:")
    keep, rows = [], []
    for r in sorted(rels, key=lambda r: r["id"]):
        t = r["tags"]
        ok = kept(t)
        print(f"    {'KEEP' if ok else 'drop':4} {r['id']:>9} {t.get('route', ''):10} "
              f"{t.get('network', '-'):<6} {t.get('name', '')}")
        if not ok:
            if r["id"] not in config.NOT_DRAWN:
                sys.exit(f"relation {r['id']} ({t.get('name')}) is neither kept nor named "
                         f"in config.NOT_DRAWN - a line this step cannot place")
            continue
        keep.append(r)
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            nt = (n or {}).get("tags", {})
            if not n or nt.get("public_transport") != "stop_position" or not nt.get("name"):
                sys.exit(f"stop member {m['ref']} is not a named stop_position")
            rows.append({"node": n["id"], "stop_name": nt["name"],
                         "latitude": n["lat"], "longitude": n["lon"]})
    if len(keep) != 2:
        sys.exit(f"{len(keep)} Metro Rail relations, not the two directions")

    q = pd.DataFrame(rows).drop_duplicates("node")
    q["stop_name"] = q["stop_name"].replace(config.STATION_NAME_ALIASES)
    by_name = q.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                         longitude=("longitude", "mean"),
                                         positions=("node", "nunique")).reset_index()
    g = gpd.GeoDataFrame(q, geometry=gpd.points_from_xy(q.longitude, q.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(q)} stop positions -> {len(by_name)} stations by name; widest "
          f"{spread.idxmax()} {spread.max():.0f} m")
    if (spread > COLLAPSE_MAX_SPREAD_M).any():
        sys.exit(f"names wider than {COLLAPSE_MAX_SPREAD_M} m: "
                 f"{spread[spread > COLLAPSE_MAX_SPREAD_M].round().to_dict()}")
    by_name["lines"] = config.LINE_KEY

    print()
    station_gates.verify_stations(
        city="Buffalo", platforms=q, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={config.LINE_NAMES[config.LINE_KEY]: len(by_name)})
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    area = city.to_crs(config.CRS_PROJECTED).area.sum() / 1e6
    print(f"\n  city boundary: {len(city)} feature(s), {area:.1f} km2")
    lo, hi = config.CITY_AREA_KM2
    if not lo <= area <= hi:
        sys.exit(f"the place polygon is {area:.1f} km2, outside {lo}-{hi}")
    shape = city.geometry.union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(by_name.longitude, by_name.latitude),
                        crs=config.CRS_GEOGRAPHIC)
    outside = by_name[~pts.within(shape).values]
    if len(outside):
        sys.exit(f"stations outside the City: {sorted(outside.stop_name)} - a scope "
                 f"question; name them in excluded_stations.csv with their municipality")
    # Written with a header and no rows (Calgary's precedent): every station is
    # in the City, and the file says so rather than being absent.
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")

    nn = pts.to_crs(config.CRS_PROJECTED)
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"  in-scope spacing (m): min {d.min():,.0f}  median {d.median():,.0f}  "
          f"max {d.max():,.0f}")
    if d.median() < 550:
        sys.exit("median under 550 m: the standard rings were chosen above it")

    out = by_name.rename(columns={"stop_name": "station"})[
        ["station", "lines", "latitude", "longitude"]].sort_values("station")
    out.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    # The line: the relation with the most track geometry, track ways only.
    best = max(keep, key=lambda r: (sum(len(m["geometry"]) for m in track(r)), -r["id"]))
    merged = linemerge(MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                        for m in track(best)]))
    parts = list(getattr(merged, "geoms", [merged]))
    length = gpd.GeoSeries(parts, crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).length.sum() / 1000
    print(f"  line: relation {best['id']}, {len(parts)} piece(s), {length:.1f} km")
    LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"line": config.LINE_KEY},
         "geometry": mapping(MultiLineString(parts))}]}), encoding="utf-8")

    emit("stop_positions", len(q))
    emit("stations_in_scope", len(out))


if __name__ == "__main__":
    main()
