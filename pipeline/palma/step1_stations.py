"""Palma step 1: Metro de Palma M1's stations, and its line as GeoJSON.

    python pipeline/palma/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Rail from OpenStreetMap route-relation membership (the osm-rail skill), on
Ottawa's and Kitchener–Waterloo's pattern: a whitelist on operator + ref +
route, every other relation in the box named in config.NOT_DRAWN (M2's two,
no longer a metro service) or the step exits. Stations are the kept
relations' `stop` members, collapsed by name; gate 3 against TIB's own stop
list. A station outside the municipality is named with the municipality it is
in, from OSM's municipal boundaries. The line is its longest direction's
TRACK ways only (not its platforms), drawn to its ends.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, mapping, shape
from shapely.ops import linemerge

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.palma import config  # noqa: E402


def polygon_from_relation(els, rel_id=None):
    """A municipality's polygon from its relation's `outer` ways (Glasgow's
    method); fetch_sources.py uses it too."""
    from shapely.geometry import LineString
    from shapely.ops import polygonize, unary_union
    lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
             for e in els if e.get("type") == "relation" and (rel_id is None or e["id"] == rel_id)
             for m in e.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer" and len(m.get("geometry") or []) >= 2]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/palma/fetch_sources.py")
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
        return (t.get("operator") == config.OPERATOR and t.get("ref") in config.LINE_REFS
                and t.get("route") == "light_rail")

    print("  route relations in the box:")
    keep, rows = {}, []
    for r in sorted(rels, key=lambda r: r["id"]):
        t = r["tags"]
        ok = kept(t)
        why = "" if ok else config.NOT_DRAWN.get(r["id"], "")
        print(f"    {'KEEP' if ok else 'drop':4} {r['id']:>9} {t.get('route', ''):10} "
              f"ref {t.get('ref', '-'):<3} {t.get('name', '')}  {why}")
        if not ok:
            if r["id"] not in config.NOT_DRAWN:
                sys.exit(f"relation {r['id']} ({t.get('name')}) is neither kept nor named "
                         f"in config.NOT_DRAWN - a line this step cannot place")
            continue
        keep.setdefault(t["ref"], []).append(r)
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes.get(m["ref"])
            nm = (n or {}).get("tags", {}).get("name")
            if not n or not nm:
                sys.exit(f"stop member {m['ref']} of relation {r['id']} has no name")
            name = config.STATION_NAME_ALIASES.get(nm.strip(), nm.strip())
            rows.append({"node": n["id"], "raw_name": nm, "stop_name": name,
                         "line": t["ref"], "latitude": n["lat"], "longitude": n["lon"]})
    for ref in config.LINE_REFS:
        if len(keep.get(ref, [])) != 2:
            sys.exit(f"{ref}: {len(keep.get(ref, []))} relations, not the two directions")

    q = pd.DataFrame(rows).drop_duplicates(["node", "line"])
    per_line = q.groupby("line")["stop_name"].nunique()
    pos = q.drop_duplicates("node")
    by_name = pos.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                           longitude=("longitude", "mean"),
                                           positions=("node", "nunique")).reset_index()
    by_name["lines"] = by_name["stop_name"].map(
        q.groupby("stop_name")["line"].agg(lambda s: ";".join(sorted(set(s)))))
    g = gpd.GeoDataFrame(pos, geometry=gpd.points_from_xy(pos.longitude, pos.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(pos)} stop positions -> {len(by_name)} stations by name; widest "
          f"{spread.idxmax()} {spread.max():.0f} m")
    if (spread > config.COLLAPSE_MAX_SPREAD_M).any():
        sys.exit(f"names wider than {config.COLLAPSE_MAX_SPREAD_M} m: "
                 f"{spread[spread > config.COLLAPSE_MAX_SPREAD_M].round().to_dict()}")

    print()
    station_gates.verify_stations(
        city="Palma", platforms=pos, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={config.LINE_NAMES[k]: int(v) for k, v in per_line.items()})
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    city = shape(read_cached(config.CITY_BOUNDARY_GEOJSON, "boundary")["geometry"])
    area = gpd.GeoSeries([city], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    print(f"\n  municipality: {area:.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"the boundary measures {area:.1f} km2, outside {lo}-{hi}")
    pts = gpd.GeoSeries(gpd.points_from_xy(by_name.longitude, by_name.latitude),
                        crs=config.CRS_GEOGRAPHIC)
    inside = pts.within(city).values
    muni = read_cached(config.NEIGHBOURS_OSM_CACHE, "municipalities")["elements"]
    polys = {e["tags"].get("name"): polygon_from_relation(muni, e["id"])
             for e in muni if e["type"] == "relation"}
    outside = by_name[~inside].copy()
    outside["municipality"] = [next((n for n, p in polys.items() if n != "Palma" and p.contains(pt)),
                                    "unknown") for pt in pts[~inside]]
    outside["reason"] = [f"outside the municipality ({m})" for m in outside["municipality"]]
    outside.rename(columns={"stop_name": "station"})[
        ["station", "lines", "reason", "latitude", "longitude"]].to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  stations outside Palma: {dict(zip(outside.stop_name, outside.municipality)) or 'none'}")
    ins = by_name[inside]

    nn = pts[inside].to_crs(config.CRS_PROJECTED).reset_index(drop=True)
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"  in-scope spacing (m): min {d.min():,.0f}  median {d.median():,.0f}  "
          f"max {d.max():,.0f}")
    if d.median() < config.SPACING_MIN_M:
        sys.exit("median under the spacing floor: the standard rings were chosen above it")

    out = ins.rename(columns={"stop_name": "station"})[
        ["station", "lines", "latitude", "longitude"]].sort_values("station")
    out.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    features = []
    for ref in config.LINE_REFS:
        best = max(keep[ref], key=lambda r: (sum(len(m["geometry"]) for m in track(r)), -r["id"]))
        merged = linemerge(MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                            for m in track(best)]))
        parts = list(getattr(merged, "geoms", [merged]))
        length = gpd.GeoSeries(parts, crs=config.CRS_GEOGRAPHIC).to_crs(
            config.CRS_PROJECTED).length.sum() / 1000
        print(f"  {ref}: relation {best['id']}, {len(parts)} piece(s), {length:.1f} km")
        features.append({"type": "Feature", "properties": {"line": ref},
                         "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection",
                                                "features": features}), encoding="utf-8")

    emit("stop_positions", len(pos))
    emit("stations_in_scope", len(out))
    emit("stations_outside", len(outside))


if __name__ == "__main__":
    main()
