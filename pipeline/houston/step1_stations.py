"""Houston step 1: METRORail's Red, Green and Purple Line stations in the City
of Houston, and their lines as GeoJSON.

    python pipeline/houston/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Rail from OpenStreetMap (owner, 2026-09-29), the osm-rail skill's shape:
whitelisted relations, stations from each relation's `stop` members, lines
drawn from track ways only (a `platform` way linemerges into a stray ring).
The Central Station couplet merges by config's explicit alias. Gate 3 runs
against METRO's own count, per line, after the merge.
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
from pipeline.houston import config  # noqa: E402

COLLAPSE_MAX_SPREAD_M = 250


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/houston/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def city_polygon():
    """The City of Houston as TIGER draws it (config explains why not OSM)."""
    if not config.CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"missing {config.CITY_BOUNDARY_GEOJSON}\n"
                 f"Run: python pipeline/houston/fetch_sources.py")
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    area = float(city.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.CITY_AREA_KM2
    print(f"  City of Houston (TIGER place 4835000): {area:,.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"the place polygon is {area:,.1f} km2, outside {lo:,}-{hi:,}")
    return city.geometry.union_all()


def track(rel):
    return [m for m in rel["members"] if m["type"] == "way" and m.get("geometry")
            and not m.get("role", "").startswith("platform")]


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    els = read_cached(config.OSM_ROUTES_JSON, "rail relations")["elements"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    rels = [e for e in els if e["type"] == "relation"]

    print("  route relations:")
    keep = []
    for r in sorted(rels, key=lambda r: (r["tags"].get("ref", ""), r["id"])):
        t = r["tags"]
        ref = t.get("ref")
        ok = (t.get("network") == config.OSM_NETWORK and t.get("route") == "light_rail"
              and ref in config.LINE_REFS)
        print(f"    {'KEEP' if ok else '????'} {r['id']:>8} {ref or '-':6} {t.get('name', '')}")
        if not ok:
            sys.exit(f"relation {r['id']} is not a whitelisted METRORail line: name it in config")
        keep.append(r)

    rows, per_rel = [], {}
    for r in keep:
        n_stops = 0
        for m in r["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes[m["ref"]]
            nt = n.get("tags", {})
            if nt.get("public_transport") != "stop_position":
                sys.exit(f"stop member {n['id']} is not a stop_position")
            if not nt.get("name"):
                sys.exit(f"stop {n['id']} on {r['tags']['ref']} has no name")
            rows.append({"node": n["id"], "stop_name": nt["name"], "line": r["tags"]["ref"],
                         "latitude": n["lat"], "longitude": n["lon"]})
            n_stops += 1
        per_rel[r["id"]] = n_stops
    q = pd.DataFrame(rows).drop_duplicates(["line", "node"])
    unused = set(config.STATION_NAME_ALIASES) - set(q["stop_name"])
    if unused:
        sys.exit(f"aliases for names OSM no longer carries: {sorted(unused)} - re-read the couplets")
    q["stop_name"] = q["stop_name"].replace(config.STATION_NAME_ALIASES)

    order = list(config.LINE_REFS)
    lines_by = q.groupby("stop_name")["line"].agg(lambda s: "/".join(sorted(set(s), key=order.index)))
    actual = {config.LINE_NAMES[ref]: int(q.loc[q["line"] == ref, "stop_name"].nunique())
              for ref in config.LINE_REFS}
    plat = q.drop_duplicates("node")
    by_name = plat.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                            longitude=("longitude", "mean"),
                                            positions=("node", "nunique")).reset_index()
    g = gpd.GeoDataFrame(plat, geometry=gpd.points_from_xy(plat.longitude, plat.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(plat)} stop positions -> {len(by_name)} stations; widest:")
    for nm in spread.sort_values(ascending=False).head(6).index:
        print(f"    {nm:<45} {spread[nm]:>5.0f} m")
    limit = pd.Series(COLLAPSE_MAX_SPREAD_M, index=spread.index, dtype=float)
    for nm, m in config.STAGGERED_PLATFORMS_M.items():
        if nm not in limit.index:
            sys.exit(f"config.STAGGERED_PLATFORMS_M names {nm!r}, which OSM no longer carries")
        limit[nm] = m
    if (spread > limit).any():
        sys.exit(f"names wider than their limit: {spread[spread > limit].round().to_dict()}")
    by_name["lines"] = by_name["stop_name"].map(lines_by)
    if len(by_name) != config.OPERATOR_TOTAL_STATIONS:
        sys.exit(f"{len(by_name)} stations, METRO counts {config.OPERATOR_TOTAL_STATIONS}")

    print()
    station_gates.verify_stations(
        city="Houston", platforms=plat, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    # --- The drawn lines: the longer direction's track ways per line --------
    feats = []
    for ref in config.LINE_REFS:
        rs = [r for r in keep if r["tags"]["ref"] == ref]
        best = max(rs, key=lambda r: (sum(len(m["geometry"]) for m in track(r)), -r["id"]))
        merged = linemerge(MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                            for m in track(best)]))
        parts = list(getattr(merged, "geoms", [merged]))
        km = gpd.GeoSeries(parts, crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).length.sum()
        print(f"  {config.LINE_NAMES[ref]}: relation {best['id']}, {len(parts)} piece(s), "
              f"{km / 1000:.1f} km")
        feats.append({"type": "Feature", "properties": {"line": ref},
                      "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")

    # --- Scope: inside the City of Houston -----------------------------------
    city = city_polygon()
    pts = gpd.GeoDataFrame(by_name, geometry=gpd.points_from_xy(by_name.longitude, by_name.latitude),
                           crs=config.CRS_GEOGRAPHIC)
    inside = pts[pts.within(city)].copy()
    outside = pts[~pts.within(city)].copy()
    outside["reason"] = "outside the City of Houston"
    print(f"\n  {len(pts)} stations -> {len(inside)} inside the city, {len(outside)} outside")

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"  in-scope spacing (m): min {d.min():,.0f}  median {d.median():,.0f}  "
          f"max {d.max():,.0f}")
    if d.median() < 550:
        sys.exit("median under 550 m: the standard rings were chosen above it")

    out = pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                        "reason": outside["reason"], "latitude": outside["latitude"],
                        "longitude": outside["longitude"]},
                       columns=["station", "lines", "reason", "latitude", "longitude"])
    out.sort_values("station").to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")

    keep_df = inside.rename(columns={"stop_name": "station"})[
        ["station", "lines", "latitude", "longitude"]].sort_values("station")
    keep_df.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(keep_df)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")
    emit("stop_positions", len(plat))
    emit("stations_in_scope", len(keep_df))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    main()
