"""Kitchener–Waterloo step 1: ION's stations, and its line as GeoJSON.

    python pipeline/kitchener_waterloo/step1_stations.py

Reads the cache only; `fetch_sources.py` downloads.

Rail from OpenStreetMap route-relation membership (the osm-rail skill), on
Ottawa's pattern: a whitelist on operator + ref + route, every other relation
in the box named in config.NOT_DRAWN or the step exits. Stations are the kept
relations' `stop` members, collapsed by name. ION splits three stops by
direction through the two downtowns (Waterloo Public Square / Willis Way,
Frederick / Queen, Kitchener City Hall / Victoria Park): each direction's
relation has 16 stops, and the two together name 19 - which is how the
Region's own ION Stops layer counts them too (gate 3). A name whose stop
positions spread wider than config allows stops the step. The line is written
from its longest direction's TRACK ways only (not its platforms).
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, Point, mapping
from shapely.ops import linemerge

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import stations as station_gates  # noqa: E402
from pipeline.baseline import emit  # noqa: E402
from pipeline.kitchener_waterloo import config  # noqa: E402

# A way of the other direction further than this from the drawn one is a
# different street (a split), not the second track of the same corridor.
DIVERGE_M = 30


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\n"
                 "Run: python pipeline/kitchener_waterloo/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))


def track(rel):
    return [m for m in rel["members"] if m["type"] == "way" and m.get("geometry")
            and not m.get("role", "").startswith("platform")]


def region_ion_count():
    """Gate 3's figure from the Region's own ION Stops layer: stage 1's
    constructed LRT stops, by name."""
    rows = [f["attributes"] for f in read_cached(config.ION_STOPS_JSON, "ION stops")["features"]]
    names = {r["StopName"].strip() for r in rows
             if r.get("Stage1") == "LRT" and r.get("StopStatus") == "Constructed"}
    return len(names), names


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
            name = config.STATION_NAME_ALIASES.get(nm.strip(), nm.strip())
            rows.append({"node": n["id"], "raw_name": nm, "stop_name": name,
                         "line": t["ref"], "latitude": n["lat"], "longitude": n["lon"]})
    for ref in config.LINE_REFS:
        if len(keep.get(ref, [])) != 2:
            sys.exit(f"route {ref}: {len(keep.get(ref, []))} relations, not the two directions")

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

    n_region, region_names = region_ion_count()
    if n_region != config.OPERATOR_STATION_COUNTS["ION"]:
        sys.exit(f"the Region's ION Stops layer now names {n_region} stage-1 stops, "
                 f"config says {config.OPERATOR_STATION_COUNTS['ION']}")
    missing = sorted(set(by_name.stop_name) ^ region_names)
    print(f"  the Region's ION Stops layer: {n_region} stops; names differing from OSM's: "
          f"{missing or 'none'}")

    print()
    station_gates.verify_stations(
        city="Kitchener–Waterloo", platforms=pos, stations=by_name,
        crs_projected=config.CRS_PROJECTED, spacing_min=config.SPACING_MIN_M,
        expected_per_line=config.OPERATOR_STATION_COUNTS,
        actual_per_line={config.LINE_NAMES[k]: int(v) for k, v in per_line.items()})
    print(f"    gate 3 source: {config.OPERATOR_COUNTS_SOURCE}")

    cities = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_GEOGRAPHIC)
    if sorted(cities["PlaceName"]) != sorted(config.CITY_NAMES):
        sys.exit(f"boundary features {sorted(cities['PlaceName'])}, not {config.CITY_NAMES}")
    area = dict(zip(cities["PlaceName"], cities.to_crs(config.CRS_PROJECTED).area / 1e6))
    for name, (lo, hi) in config.CITY_AREA_KM2.items():
        print(f"  {name}: {area[name]:.1f} km2")
        if not lo <= area[name] <= hi:
            sys.exit(f"{name} measures {area[name]:.1f} km2, outside {lo}-{hi}")
    shape = cities.geometry.union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(by_name.longitude, by_name.latitude),
                        crs=config.CRS_GEOGRAPHIC)
    outside = by_name[~pts.within(shape).values]
    if len(outside):
        sys.exit(f"stations outside Kitchener and Waterloo: {sorted(outside.stop_name)} - a "
                 f"scope question; name them in excluded_stations.csv")
    for name in config.CITY_NAMES:
        poly = cities[cities["PlaceName"] == name].geometry.union_all()
        print(f"    stations in {name}: {int(pts.within(poly).sum())}")
    # Written with a header and no rows (Calgary's precedent): every station is
    # in the two cities, and the file says so rather than being absent.
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
        # The longest direction's track, plus the other direction's ways only
        # where it leaves it: the downtown splits run on parallel streets, so
        # one direction alone would leave a street without its line, while
        # both whole would draw every double-track stretch twice.
        best, other = sorted(keep[ref], key=lambda r: (
            -sum(len(m["geometry"]) for m in track(r)), r["id"]))
        ways = {m["ref"]: m for m in track(best)}

        def geom(ms):
            return gpd.GeoSeries([MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                                   for m in ms])],
                                 crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)[0]

        base = geom(ways.values())

        def farthest(m):
            # A way that leaves the corridor anywhere is added whole, so a
            # split's first way (which starts at the junction) is not lost.
            return max(Point(xy).distance(base) for xy in geom([m]).geoms[0].coords)

        split = [m for m in track(other) if m["ref"] not in ways and farthest(m) > DIVERGE_M]
        ways.update({m["ref"]: m for m in split})
        print(f"  route {ref}: relation {best['id']}, plus {len(split)} ways of {other['id']} "
              f"that leave it by more than {DIVERGE_M} m (the downtown splits)")
        merged = linemerge(MultiLineString([[(p["lon"], p["lat"]) for p in m["geometry"]]
                                            for m in ways.values()]))
        parts = list(getattr(merged, "geoms", [merged]))
        length = gpd.GeoSeries(parts, crs=config.CRS_GEOGRAPHIC).to_crs(
            config.CRS_PROJECTED).length.sum() / 1000
        print(f"  route {ref}: {len(ways)} ways, {len(parts)} piece(s), {length:.1f} km")
        features.append({"type": "Feature", "properties": {"line": ref},
                         "geometry": mapping(MultiLineString(parts))})
    config.LINES_GEOJSON.write_text(json.dumps({"type": "FeatureCollection",
                                                "features": features}), encoding="utf-8")

    emit("stop_positions", len(pos))
    emit("stations_in_scope", len(out))


if __name__ == "__main__":
    main()
