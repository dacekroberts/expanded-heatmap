"""Pittsburgh step 1: the T's stations in the city, and its three lines as
GeoJSON.

    python pipeline/pittsburgh/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Rail from OpenStreetMap route-relation membership (the osm-rail skill), on
Minneapolis's pattern: a whitelist on network + ref + route, every other
relation in the box named in config.NOT_DRAWN or the step exits. Stations are
the kept relations' `stop` members, collapsed by name - across lines too,
which makes the shared trunk (Allegheny to South Hills Junction) one station
each. A line may have more than two relations (Red's two services); each
needs at least two. Gate 3 counts the whole lines; the city scope comes after
it: a station outside TIGER's place polygon goes to excluded_stations.csv
with the county subdivision it is in (the Los Angeles rule), because the
city's register stops at the city line. Each line is drawn whole, from its
longest direction's TRACK ways only.
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
from pipeline.pittsburgh import config  # noqa: E402


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/pittsburgh/fetch_sources.py")
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
        return (t.get("network") == config.NETWORK and t.get("ref") in config.LINE_REFS
                and t.get("route") == "light_rail")

    print("  route relations in the box:")
    keep, rows = {}, []
    for r in sorted(rels, key=lambda r: r["id"]):
        t = r["tags"]
        ok = kept(t)
        print(f"    {'KEEP' if ok else 'drop':4} {r['id']:>9} {t.get('route', ''):10} "
              f"ref {t.get('ref', '-'):<4} {t.get('name', '')}")
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
            rows.append({"node": n["id"], "raw_name": nm,
                         "stop_name": config.STATION_NAME_ALIASES.get(nm.strip(), nm.strip()),
                         "line": t["ref"], "latitude": n["lat"], "longitude": n["lon"]})
    for ref in config.LINE_REFS:
        if len(keep.get(ref, [])) < 2:
            sys.exit(f"Line {ref}: {len(keep.get(ref, []))} relations, not at least the two directions")

    q = pd.DataFrame(rows).drop_duplicates(["node", "line"])
    print("\n  name folds:", sorted({(a, b) for a, b in zip(q.raw_name, q.stop_name) if a != b}))
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
    print(f"  shared by both lines: {sorted(shared.stop_name)}")

    print()
    station_gates.verify_stations(
        city="Pittsburgh", platforms=pos, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={config.LINE_NAMES[k]: int(v) for k, v in per_line.items()})
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    # --- The city scope: TIGER's place polygon ---------------------------------
    city = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    area = city.to_crs(config.CRS_PROJECTED).area.sum() / 1e6
    print(f"\n  city boundary: {len(city)} feature(s), {area:.1f} km2")
    lo, hi = config.CITY_AREA_KM2
    if not lo <= area <= hi:
        sys.exit(f"the place polygon is {area:.1f} km2, outside {lo}-{hi}")
    shape = city.geometry.union_all()
    pts = gpd.GeoDataFrame(by_name, geometry=gpd.points_from_xy(by_name.longitude,
                                                                by_name.latitude),
                           crs=config.CRS_GEOGRAPHIC)
    inside = pts.within(shape).values
    cousub = gpd.read_file(config.COUSUB_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    out = gpd.sjoin(pts[~inside], cousub[["NAME", "geometry"]], how="left",
                    predicate="within")
    if out["NAME"].isna().any():
        sys.exit(f"stations in no county subdivision: {sorted(out[out.NAME.isna()].stop_name)}")
    if out.index.duplicated().any():
        sys.exit("a station in two county subdivisions")
    if (out["NAME"] == "Pittsburgh city").any():
        sys.exit("a station outside the place polygon but inside the Pittsburgh subdivision")
    # TIGER legal names, as a reader says them.
    # Pennsylvania's: "Bethel Park municipality" -> "Bethel Park",
    # "Castle Shannon borough" -> "Castle Shannon Borough".
    place = (out["NAME"].str.replace(r" (city|municipality)$", "", regex=True)
             .str.replace(r" borough$", " Borough", regex=True)
             .str.replace(r" township$", " Township", regex=True))
    excluded = pd.DataFrame({
        "station": out["stop_name"],
        "lines": out["lines"].map(lambda s: ";".join(config.LINE_NAMES[k] for k in s.split(";"))),
        "reason": "Outside the City of Pittsburgh: " + place,
        "latitude": out["latitude"].round(6), "longitude": out["longitude"].round(6),
    }).sort_values(["reason", "station"])
    excluded.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  outside the city: {len(excluded)} -> "
          f"{config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    print("   ", excluded["reason"].str.replace("Outside the City of Pittsburgh: ", "")
          .value_counts().to_dict())
    scoped = by_name[inside]
    for ref in config.LINE_REFS:
        n_in = int(scoped["lines"].str.contains(ref).sum())
        print(f"    {config.LINE_NAMES[ref]}: {n_in} of {int(per_line[ref])} in the city")
        emit(f"stations_in_city_{ref}", n_in)

    nn = gpd.GeoSeries(gpd.points_from_xy(scoped.longitude, scoped.latitude),
                       crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"  in-scope spacing (m): min {d.min():,.0f}  median {d.median():,.0f}  "
          f"max {d.max():,.0f}")
    if d.median() < config.SPACING_MIN_M:
        sys.exit("median under the spacing floor: the standard rings were chosen above it")

    kept_out = scoped.rename(columns={"stop_name": "station"})[
        ["station", "lines", "latitude", "longitude"]].sort_values("station")
    kept_out.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(kept_out)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")

    features = []
    for ref in config.LINE_REFS:
        best = max(keep[ref], key=lambda r: (sum(len(m["geometry"]) for m in track(r)), -r["id"]))
        merged = linemerge(MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                            for m in track(best)]))
        parts = list(getattr(merged, "geoms", [merged]))
        length = gpd.GeoSeries(parts, crs=config.CRS_GEOGRAPHIC).to_crs(
            config.CRS_PROJECTED).length.sum() / 1000
        print(f"  {config.LINE_NAMES[ref]}: relation {best['id']}, {len(parts)} piece(s), "
              f"{length:.1f} km")
        features.append({"type": "Feature", "properties": {"line": ref},
                         "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection",
                                                "features": features}), encoding="utf-8")

    emit("stop_positions", len(pos))
    emit("stations_outside_city", len(excluded))
    emit("stations_in_scope", len(kept_out))


if __name__ == "__main__":
    main()
