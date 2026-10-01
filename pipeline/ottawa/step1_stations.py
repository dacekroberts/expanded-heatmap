"""Ottawa step 1: the O-Train's stations, and its three lines as GeoJSON.

    python pipeline/ottawa/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Rail from OpenStreetMap route-relation membership (the osm-rail skill), on
Buffalo's pattern: a whitelist on operator + ref + route, every other
relation in the box named in config.NOT_DRAWN or the step exits. Stations are
the kept relations' `stop` members. OSM names a station's two platforms by
direction ("Blair O-Train West/Ouest", "Blair O-Train"), so the direction
suffix is stripped by rule, config's aliases fold Lyon A/B and Lac Dow, and
the stops collapse by name - across lines too, which is what makes Bayview
(Lines 1 and 2) and South Keys (Lines 2 and 4) one station each. A name whose
stop positions spread wider than config allows stops the step. Each line is
written from its longest direction's TRACK ways only (not its platforms).
"""
import json
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, mapping
from shapely.ops import linemerge

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.ottawa import config  # noqa: E402

DIRECTION_SUFFIX = re.compile(r"\s+O-Train(\s+(East/Est|West/Ouest))?$")


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/ottawa/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def track(rel):
    return [m for m in rel["members"] if m["type"] == "way" and m.get("geometry")
            and not m.get("role", "").startswith("platform")]


def station_name(raw):
    name = DIRECTION_SUFFIX.sub("", raw.strip())
    return config.STATION_NAME_ALIASES.get(name, name)


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
        print(f"    {'KEEP' if ok else 'drop':4} {r['id']:>9} {t.get('route', ''):10} "
              f"ref {t.get('ref', '-'):<3} {t.get('name', '')}")
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
            rows.append({"node": n["id"], "raw_name": nm, "stop_name": station_name(nm),
                         "line": t["ref"], "latitude": n["lat"], "longitude": n["lon"]})
    for ref in config.LINE_REFS:
        if len(keep.get(ref, [])) != 2:
            sys.exit(f"Line {ref}: {len(keep.get(ref, []))} relations, not the two directions")

    q = pd.DataFrame(rows).drop_duplicates(["node", "line"])
    print("\n  name folds:", sorted({(a, b) for a, b in zip(q.raw_name, q.stop_name) if a != b}
                                   - {(a, b) for a, b in zip(q.raw_name, q.stop_name)
                                      if DIRECTION_SUFFIX.search(a)}))
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
    shared = by_name[by_name["lines"].str.contains(";")]
    print(f"  interchanges: {dict(zip(shared.stop_name, shared.lines))}")

    print()
    station_gates.verify_stations(
        city="Ottawa", platforms=pos, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={config.LINE_NAMES[k]: int(v) for k, v in per_line.items()})
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    wards = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    area = wards.to_crs(config.CRS_PROJECTED).area.sum() / 1e6
    print(f"\n  city boundary: {len(wards)} wards, {area:.1f} km2")
    if len(wards) != config.WARD_COUNT:
        sys.exit(f"{len(wards)} ward features, not {config.WARD_COUNT}")
    lo, hi = config.CITY_AREA_KM2
    if not lo <= area <= hi:
        sys.exit(f"the dissolved wards are {area:.1f} km2, outside {lo}-{hi}")
    shape = wards.geometry.union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(by_name.longitude, by_name.latitude),
                        crs=config.CRS_GEOGRAPHIC)
    outside = by_name[~pts.within(shape).values]
    if len(outside):
        sys.exit(f"stations outside the City: {sorted(outside.stop_name)} - a scope "
                 f"question; name them in excluded_stations.csv")
    # Written with a header and no rows (Calgary's precedent): every station is
    # in the City, and the file says so rather than being absent.
    pd.DataFrame(columns=["station", "lines", "reason", "latitude", "longitude"]).to_csv(
        config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")

    nn = pts.to_crs(config.CRS_PROJECTED)
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"  in-scope spacing (m): min {d.min():,.0f}  median {d.median():,.0f}  "
          f"max {d.max():,.0f}")
    if d.median() < config.SPACING_MIN_M:
        sys.exit("median under the spacing floor: the standard rings were chosen above it")

    out = by_name.rename(columns={"stop_name": "station"})[
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
        print(f"  Line {ref}: relation {best['id']}, {len(parts)} piece(s), {length:.1f} km")
        features.append({"type": "Feature", "properties": {"line": ref},
                         "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection",
                                                "features": features}), encoding="utf-8")

    emit("stop_positions", len(pos))
    emit("stations_in_scope", len(out))


if __name__ == "__main__":
    main()
