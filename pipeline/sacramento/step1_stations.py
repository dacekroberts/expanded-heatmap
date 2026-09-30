"""Sacramento step 1: SacRT's Blue and Gold Line stations in the City of
Sacramento, and their lines as GeoJSON.

    python pipeline/sacramento/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

What is its own here, each guarded rather than noted:
  * **The Green Line is suspended**, so it is not drawn (config) and its one
    Green-only station is recorded as closed for works.
  * **OSM lags SacRT twice on Blue**: two stop nodes carry no name (Morrison
    Creek, named from config) and Dos Rios, opened 2026-09-28, is not mapped
    at all (placed from Wikidata). Each entry STOPS the step once OSM catches
    up, so the workaround retires itself.
  * **Downtown couplets** merge by config's explicit aliases.
  * Gate 3 runs against SacRT's own timetables, per direction.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, Point, mapping
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.sacramento import config  # noqa: E402

COLLAPSE_MAX_SPREAD_M = 250


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/sacramento/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines))))) if lines else None


def boundaries():
    rows = []
    for rel in read_cached(config.OSM_BOUNDARIES_JSON, "boundaries")["elements"]:
        t = rel.get("tags", {})
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close")
        rows.append({"id": rel["id"], "name": t.get("name"), "level": t.get("admin_level"),
                     "geometry": outer.difference(inner) if inner is not None else outer})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    city = gdf[gdf["id"] == config.OSM_CITY_RELATION]
    area = float(city.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    print(f"  City of Sacramento (relation {config.OSM_CITY_RELATION}): {area:.1f} km2")
    if not 245 <= area <= 270:
        sys.exit(f"the city polygon is {area:.1f} km2, not ~257: assembled wrong")
    return gdf


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
    keep, green, rows = [], [], []
    for r in sorted(rels, key=lambda r: (r["tags"].get("ref", ""), r["id"])):
        t = r["tags"]
        ref = t.get("ref")
        sacrt = t.get("network") == "SacRT" and t.get("route") == "light_rail"
        state = ("KEEP" if sacrt and ref in config.LINE_REFS else
                 "susp" if sacrt and ref in config.NOT_DRAWN_REFS else "????")
        print(f"    {state} {r['id']:>8} {ref or '-':6} {t.get('name', '')}")
        if state == "????":
            sys.exit(f"relation {r['id']} is neither drawn nor named in config.NOT_DRAWN_REFS")
        (keep if state == "KEEP" else green).append(r)

    def stops(rel):
        out = []
        for m in rel["members"]:
            if m["type"] != "node" or not m.get("role", "").startswith("stop"):
                continue
            n = nodes[m["ref"]]
            nt = n.get("tags", {})
            if nt.get("public_transport") != "stop_position":
                sys.exit(f"stop member {n['id']} is not a stop_position")
            name = nt.get("name")
            if n["id"] in config.UNNAMED_STOP_NAMES:
                if name:
                    sys.exit(f"OSM now names stop {n['id']} {name!r}: retire its entry in "
                             f"config.UNNAMED_STOP_NAMES")
                name = config.UNNAMED_STOP_NAMES[n["id"]]
            if not name:
                sys.exit(f"stop {n['id']} on {rel['tags']['ref']} has no name and no config entry")
            out.append({"node": n["id"], "stop_name": name, "latitude": n["lat"],
                        "longitude": n["lon"]})
        return out

    per_rel = {}
    for r in keep:
        s = stops(r)
        per_rel[r["id"]] = len(s)
        rows += [dict(x, line=r["tags"]["ref"]) for x in s]
    names_on = {n for x in rows for n in [x["stop_name"]]}

    # Stations OSM has not mapped, placed from Wikidata by id.
    added = []
    for name, spec in config.ADDED_STATIONS.items():
        if name in names_on:
            sys.exit(f"OSM's relations now carry {name!r}: retire its config.ADDED_STATIONS "
                     f"entry and its Wikidata fetch")
        wd = read_cached(config.DATA_RAW / f"wikidata_{spec['wikidata']}.json", name)
        c = wd["entities"][spec["wikidata"]]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]
        added.append({"node": f"wikidata:{spec['wikidata']}", "stop_name": name, "line": spec["line"],
                      "latitude": c["latitude"], "longitude": c["longitude"]})
        print(f"\n  added from Wikidata {spec['wikidata']}: {name} "
              f"({c['latitude']:.5f}, {c['longitude']:.5f}) on {spec['line']}")
    q = pd.DataFrame(rows + added).drop_duplicates(["line", "node"])

    # Gate 3 per line: the fuller direction's stops, plus the added stations,
    # before the couplet merge - SacRT's timetables list one direction each.
    actual = {}
    for ref in config.LINE_REFS:
        best = max(per_rel[r["id"]] for r in keep if r["tags"]["ref"] == ref)
        actual[config.LINE_NAMES[ref]] = best + sum(1 for a in added if a["line"] == ref)

    q["stop_name"] = q["stop_name"].replace(config.STATION_NAME_ALIASES)
    order = list(config.LINE_REFS)
    lines_by = q.groupby("stop_name")["line"].agg(lambda s: "/".join(sorted(set(s), key=order.index)))
    plat = q.drop_duplicates("node")
    by_name = plat.groupby("stop_name").agg(latitude=("latitude", "mean"),
                                            longitude=("longitude", "mean"),
                                            positions=("node", "nunique")).reset_index()
    g = gpd.GeoDataFrame(plat, geometry=gpd.points_from_xy(plat.longitude, plat.latitude),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    spread = g.groupby("stop_name")["geometry"].agg(
        lambda s: max((a.distance(b) for a in s for b in s), default=0.0))
    print(f"\n  {len(plat)} stop positions -> {len(by_name)} stations; widest:")
    for nm in spread.sort_values(ascending=False).head(5).index:
        print(f"    {nm:<40} {spread[nm]:>5.0f} m")
    if (spread > COLLAPSE_MAX_SPREAD_M).any():
        sys.exit(f"names wider than {COLLAPSE_MAX_SPREAD_M} m: "
                 f"{spread[spread > COLLAPSE_MAX_SPREAD_M].round().to_dict()}")
    by_name["lines"] = by_name["stop_name"].map(lines_by)

    print()
    station_gates.verify_stations(
        city="Sacramento", platforms=plat, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    # --- The drawn lines, and the added stations checked against them -------
    feats, drawn = [], {}
    for ref in config.LINE_REFS:
        rs = [r for r in keep if r["tags"]["ref"] == ref]
        best = max(rs, key=lambda r: (sum(len(m["geometry"]) for m in track(r)), -r["id"]))
        merged = linemerge(MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                            for m in track(best)]))
        parts = list(getattr(merged, "geoms", [merged]))
        drawn[ref] = gpd.GeoSeries(parts, crs=config.CRS_GEOGRAPHIC).to_crs(
            config.CRS_PROJECTED).union_all()
        print(f"  {config.LINE_NAMES[ref]}: relation {best['id']}, {len(parts)} piece(s), "
              f"{drawn[ref].length / 1000:.1f} km")
        feats.append({"type": "Feature", "properties": {"line": ref},
                      "geometry": mapping(MultiLineString(parts))})
    for a in added:
        p = gpd.GeoSeries([Point(a["longitude"], a["latitude"])], crs=config.CRS_GEOGRAPHIC
                          ).to_crs(config.CRS_PROJECTED).iloc[0]
        d = p.distance(drawn[a["line"]])
        print(f"  {a['stop_name']}: {d:.0f} m from the drawn {config.LINE_NAMES[a['line']]}")
        if d > 80:
            sys.exit(f"{a['stop_name']} is {d:.0f} m from its line - the Wikidata point is wrong")
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats}),
                                    encoding="utf-8")

    # --- Scope: inside the City of Sacramento --------------------------------
    b = boundaries()
    pts = gpd.GeoDataFrame(by_name, geometry=gpd.points_from_xy(by_name.longitude, by_name.latitude),
                           crs=config.CRS_GEOGRAPHIC)
    city = b[b["id"] == config.OSM_CITY_RELATION].geometry.iloc[0]
    inside = pts[pts.within(city)].copy()
    outside = pts[~pts.within(city)].copy()

    def where(p):
        cities = b[(b["level"] == "8") & b.contains(p)]["name"].tolist()
        if cities:
            return f"in {cities[0]}, outside the City of Sacramento"
        county = b[(b["level"] == "6") & b.contains(p)]["name"].tolist()
        return (f"in unincorporated {county[0]}, outside the City of Sacramento" if county
                else "outside the City of Sacramento")

    outside["reason"] = outside.geometry.map(where)
    print(f"\n  {len(pts)} stations -> {len(inside)} inside the city, {len(outside)} outside")
    for ref in config.LINE_REFS:
        n_in = int(inside["lines"].str.split("/").map(lambda s: ref in s).sum())
        n_all = int(pts["lines"].str.split("/").map(lambda s: ref in s).sum())
        print(f"    {config.LINE_NAMES[ref]:<10} {n_in:>3} of {n_all:>3}")

    # --- Closed for works: the suspended Green Line's own station ------------
    closed = []
    for name, reason in config.CLOSED_FOR_WORKS.items():
        pos = [nodes[m["ref"]] for r in green for m in r["members"]
               if m["type"] == "node" and nodes[m["ref"]].get("tags", {}).get("name") == name]
        if not pos:
            sys.exit(f"{name!r} is not on OSM's Green relations - re-read the closure")
        if name in set(q["stop_name"]):
            sys.exit(f"{name!r} is on a drawn line now - it reopened; re-take the scope")
        closed.append({"station": name, "lines": "Green", "reason": reason,
                       "latitude": sum(n["lat"] for n in pos) / len(pos),
                       "longitude": sum(n["lon"] for n in pos) / len(pos)})

    nn = inside.to_crs(config.CRS_PROJECTED).geometry
    d = pd.Series([nn.drop(i).distance(p).min() for i, p in nn.items()])
    print(f"  in-scope spacing (m): min {d.min():,.0f}  median {d.median():,.0f}  "
          f"max {d.max():,.0f}")
    if d.median() < 550:
        sys.exit("median under 550 m: the standard rings were chosen above it")

    out = pd.concat([
        pd.DataFrame({"station": outside["stop_name"], "lines": outside["lines"],
                      "reason": outside["reason"], "latitude": outside["latitude"],
                      "longitude": outside["longitude"]}),
        pd.DataFrame(closed)])
    out.sort_values(["reason", "station"]).to_csv(config.EXCLUDED_STATIONS_CSV, index=False,
                                                  encoding="utf-8")
    print(f"  {len(out)} excluded -> {config.EXCLUDED_STATIONS_CSV.relative_to(config.ROOT)}")
    for k, n in out["reason"].str.replace(", outside the City of Sacramento", "") \
            .str.slice(0, 60).value_counts().items():
        print(f"    {k:<60} {n:>3}")

    keep_df = inside.rename(columns={"stop_name": "station"})[
        ["station", "lines", "latitude", "longitude"]].sort_values("station")
    keep_df.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8")
    print(f"  {len(keep_df)} stations -> {config.STATIONS_CSV.relative_to(config.ROOT)}")
    emit("stop_positions", len(plat))
    emit("stations_in_scope", len(keep_df))
    emit("stations_excluded", len(out))


if __name__ == "__main__":
    main()
