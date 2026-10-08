"""Thessaloniki step 1: Line 1 of the Thessaloniki Metro, from OpenStreetMap.

Gimhae's step 1 (osm-rail) with Thessaloniki's config. Stations come from
ROUTE-RELATION MEMBERSHIP, never a node tag filter: the stop nodes of the
metro relations, collapsed on pipeline.stations.station_name_key of their
Greek name. Relations are matched on route TYPE and ref, never on network,
and every downloaded relation must be placed (config.DRAWN_REFS) or the step
stops, so a line the query brings in cannot vanish.

Scope is the Municipality of Thessaloniki's OSM boundary (owner call 6): a
station inside it is kept; the Kalamaria branch's five are recorded in
excluded_stations.csv with the municipality each lies in, and the line is
CUT at the city line (owner call 4), so nothing outside the city is drawn.

Gate 3 (owner call 5): Elliniko Metro's 18 on the whole line and its
base line's 13 in the city, counted and then matched name by name; each
station's English label must be one of the operator's own names.

Writes processed/stations.csv, processed/rail_lines.json (one relation per
drawn line, the shape map_common.load_osm_line_shapes reads) and
outputs/thessaloniki/excluded_stations.csv. Reads the cache and NEVER fetches.

    python pipeline/thessaloniki/step1_stations.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import linemerge, polygonize, transform, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline import stations as station_gates  # noqa: E402
from pipeline.thessaloniki import config  # noqa: E402

TO_M = Transformer.from_crs(config.CRS_GEOGRAPHIC, config.CRS_PROJECTED, always_xy=True)
TO_LL = Transformer.from_crs(config.CRS_PROJECTED, config.CRS_GEOGRAPHIC, always_xy=True)
KEY = station_gates.station_name_key


def need(path, what):
    if not path.exists():
        sys.exit(f"missing {path} ({what}).\nRun: python pipeline/thessaloniki/fetch_sources.py")
    return path


def elements(path, what):
    return json.loads(need(path, what).read_text(encoding="utf-8"))["elements"]


def operator_key(name):
    k = KEY(name)
    return {KEY(a): KEY(b) for a, b in config.OPERATOR_NAME_ALIASES.items()}.get(k, k)


# --- boundaries -----------------------------------------------------------------

def relation_polygon(rel):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rel["members"]
             if m["type"] == "way" and m.get("role") == "outer" and m.get("geometry")]
    outer = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
    holes = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rel["members"]
             if m["type"] == "way" and m.get("role") == "inner" and m.get("geometry")]
    if holes:
        outer = outer.difference(unary_union(list(polygonize(linemerge(MultiLineString(holes))))))
    return outer


def area_km2(poly):
    return gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6


def municipalities():
    """{relation id: (name:en, polygon)} for every admin_level 7 relation."""
    out = {}
    for e in elements(config.BOUNDARY_OSM_JSON, "OSM boundaries"):
        t = e.get("tags", {})
        if t.get("admin_level") == config.BOUNDARY_ADMIN_LEVEL:
            out[e["id"]] = (t.get("name:en") or t.get("name"), t.get("name"), relation_polygon(e))
    return out


def boundary_polygon(verbose=True):
    """The Municipality of Thessaloniki, picked by its Greek name AND its admin
    level among the relations of the bounded query (never by size), area
    gated against the official 19.307 km2."""
    rels = [e for e in elements(config.BOUNDARY_OSM_JSON, "OSM boundaries")
            if e["type"] == "relation" and e.get("tags", {}).get("name") == config.BOUNDARY_NAME
            and e["tags"].get("admin_level") == config.BOUNDARY_ADMIN_LEVEL]
    if len(rels) != 1:
        sys.exit(f"expected one admin_level {config.BOUNDARY_ADMIN_LEVEL} relation named "
                 f"{config.BOUNDARY_NAME}, got {len(rels)}")
    rel = rels[0]
    if config.BOUNDARY_RELATION is not None and rel["id"] != config.BOUNDARY_RELATION:
        sys.exit(f"the boundary is relation {rel['id']}, not {config.BOUNDARY_RELATION}: "
                 f"re-read it before changing the config")
    poly = relation_polygon(rel)
    area = area_km2(poly)
    lo, hi = config.BOUNDARY_AREA_KM2
    if verbose:
        print(f"  boundary: relation {rel['id']} {rel['tags'].get('name')} "
              f"({rel['tags'].get('name:en')}), {area:,.2f} km2, {poly.geom_type}")
    if not lo <= area <= hi:
        sys.exit(f"boundary area {area:,.2f} km2 outside {lo}-{hi} - re-read the relation "
                 f"before changing the gate")
    return poly, rel["id"], area


# --- rail ---------------------------------------------------------------------------

def ways_of(rel):
    return [(m["ref"], [(p["lat"], p["lon"]) for p in m["geometry"]])
            for m in rel.get("members", []) if m["type"] == "way" and m.get("geometry")]


def to_m(latlon):
    return LineString([TO_M.transform(lo, la) for la, lo in latlon])


def line_geometry(rels):
    """The longest relation's ways, plus only the ways other relations add
    away from them (the branch), as projected LineStrings."""
    rels = sorted(rels, key=lambda r: sum(len(g) for _, g in ways_of(r)), reverse=True)
    drawn, seen, branch = [], set(), 0
    for i, r in enumerate(rels):
        for wid, g in ways_of(r):
            if wid in seen or len(g) < 2:
                continue
            ls = to_m(g)
            if i and unary_union(drawn).distance(ls.interpolate(0.5, normalized=True)) <= config.BRANCH_MIN_M:
                continue
            if i:
                branch += 1
            drawn.append(ls)
            seen.add(wid)
    return drawn, branch


def clip_to_city(lines_m, poly_ll):
    """The drawn track inside the city only (owner call 4), as (lat, lon) lists."""
    poly_m = transform(TO_M.transform, poly_ll)
    inside, before, after = [], 0.0, 0.0
    for ls in lines_m:
        before += ls.length
        part = ls.intersection(poly_m)
        for g in getattr(part, "geoms", [part]):
            if g.geom_type == "LineString" and g.length > 0:
                after += g.length
                inside.append([(la, lo) for lo, la in (TO_LL.transform(x, y) for x, y in g.coords)])
    return inside, before, after


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    els = elements(config.RAIL_OSM_JSON, "OSM rail relations")
    rels = [e for e in els if e["type"] == "relation"]
    nodes = {e["id"]: e for e in els if e["type"] == "node"}
    if not rels:
        sys.exit("the rail file holds no relations - an empty result is not an empty city")

    groups = {k: [] for k in config.LINES}
    unplaced = []
    for r in rels:
        t = r.get("tags", {})
        if t.get("route") not in config.LINES_ROUTE_TYPES or t.get("ref") not in config.DRAWN_REFS:
            unplaced.append(f"{r['id']} route={t.get('route')!r} ref={t.get('ref')!r}: {t.get('name')}")
            continue
        want = config.OSM_COLOUR.get(t["ref"])
        if want and (t.get("colour") or "").upper() != want.upper():
            sys.exit(f"relation {r['id']} (ref {t['ref']}): OSM colour {t.get('colour')} is not "
                     f"{want} - re-measure the line colour before changing the config")
        groups[config.DRAWN_REFS[t["ref"]]].append(r)
    if unplaced:
        sys.exit("relations with an unplaced ref or route type - place each in DRAWN_REFS:\n  "
                 + "\n  ".join(unplaced))
    print("Relations (ref on the RELATION):")
    for r in rels:
        t = r["tags"]
        print(f"  {r['id']:>9}  ref {t['ref']}  {t.get('name')}  -> {config.LINE_NAMES[config.DRAWN_REFS[t['ref']]]}")
    emit("relations", len(rels))

    # --- stations, from route membership ---------------------------------------
    stops = station_gates.route_stop_members(rels, nodes, refs=set(config.DRAWN_REFS))
    if (stops["name"] == "").any():
        sys.exit(f"{int((stops['name'] == '').sum())} unnamed stop members - name them rather "
                 f"than guess")
    stops["key"] = stops["name"].map(KEY)
    stops["name_en"] = [(nodes[n].get("tags", {}).get("name:en") or "").strip() for n in stops["node"]]
    stops["drawn"] = stops["line"].map(config.DRAWN_REFS)
    platforms = stops.drop_duplicates("node")
    print(f"\n  {len(stops)} stop members, {len(platforms)} distinct stop nodes, "
          f"{platforms.key.nunique()} names")

    objs = {}
    for e in elements(config.STATION_OSM_JSON, "OSM station objects"):
        t = e.get("tags", {})
        if t.get("station") == "subway" and t.get("name"):
            la, lo = (e["lat"], e["lon"]) if e["type"] == "node" else (e["center"]["lat"], e["center"]["lon"])
            objs.setdefault(KEY(t["name"]), []).append((t.get("name:en", "").strip(), *TO_M.transform(lo, la)))

    rows = []
    for key, g in platforms.groupby("key", sort=False):
        xy = np.array([TO_M.transform(lo, la) for la, lo in zip(g.latitude, g.longitude)])
        spread = float(max(np.hypot(*(xy - p).T).max() for p in xy))
        if spread > config.COLLAPSE_MAX_SPREAD_M:
            sys.exit(f"{g.name.iloc[0]}: its stop nodes spread {spread:,.0f} m - two stations "
                     f"under one name? Look before raising the limit")
        cx, cy = xy.mean(axis=0)
        near = [(np.hypot(ox - cx, oy - cy), en) for en, ox, oy in objs.get(key, [])
                if np.hypot(ox - cx, oy - cy) <= config.COLLAPSE_MAX_SPREAD_M and en]
        ens = sorted(set(e for e in g.name_en if e))
        en = min(near)[1] if near else (ens[0] if len(ens) == 1 else "")
        if not en:
            sys.exit(f"{g.name.iloc[0]}: no single English name (station object or stop nodes: {ens})")
        en = config.EN_NAME_OVERRIDES.get(en, en)
        lo, la = TO_LL.transform(cx, cy)
        rows.append({"station": en, "name_el": g.name.iloc[0], "key": key, "latitude": round(la, 7),
                     "longitude": round(lo, 7), "lines": " ".join(sorted(set(stops[stops.key == key].drawn))),
                     "nodes": len(g), "spread_m": round(spread)})
    st = pd.DataFrame(rows)
    print(f"  {len(st)} stations; stop nodes per station "
          f"{st.nodes.min()}-{st.nodes.max()}, widest spread {st.spread_m.max()} m")
    off = sorted(set(st.station) - set(config.OPERATOR_STATIONS_EN))
    if off:
        sys.exit(f"English names not in the operator's list: {off}")
    station_gates.check_route_stops_covered(
        city="Thessaloniki", route_stops=stops.assign(name=stops["name"]),
        stations=st.assign(station=st["name_el"]), crs_projected=config.CRS_PROJECTED)

    # --- the city ----------------------------------------------------------------
    poly, rel_id, area = boundary_polygon()
    st["in_city"] = [Point(lo, la).within(poly) for la, lo in zip(st.latitude, st.longitude)]
    poly_m = transform(TO_M.transform, poly)
    st["edge_m"] = [round(poly_m.exterior.distance(Point(TO_M.transform(lo, la))) if poly_m.geom_type == "Polygon"
                          else poly_m.boundary.distance(Point(TO_M.transform(lo, la))))
                    for la, lo in zip(st.latitude, st.longitude)]
    munis = municipalities()
    st["located_in"] = [next((en for _rid, (en, _el, p) in munis.items() if Point(lo, la).within(p)), "")
                        for la, lo in zip(st.latitude, st.longitude)]
    kept = st[st.in_city].copy()
    out = st[~st.in_city].copy()
    print(f"  in the city {len(kept)}, outside {len(out)}")
    for _, r in st.sort_values("in_city").iterrows():
        if r.edge_m < 400 or not r.in_city:
            print(f"    {'IN ' if r.in_city else 'OUT'} {r.station:<22} {r.edge_m:>5} m from the "
                  f"city line, in {r.located_in or '?'}")

    # Gate 3: the operator's counts, then its 13 names one by one.
    actual = {"Line 1": len(st), "Line 1 in Thessaloniki": len(kept)}
    gates = station_gates.verify_stations(
        city="Thessaloniki", platforms=platforms[platforms.key.isin(set(kept.key))],
        stations=kept, crs_projected=config.CRS_PROJECTED,
        expected_per_line=config.OPERATOR_STATION_COUNTS, actual_per_line=actual)
    if gates["per_line_mismatches"]:
        sys.exit(f"gate 3: {gates['per_line_mismatches']} against "
                 f"{config.OPERATOR_COUNTS_SOURCE}")
    want = {operator_key(n) for n in config.OPERATOR_IN_CITY_EL}
    got = {operator_key(n) for n in kept.name_el}
    if want != got:
        sys.exit(f"gate 3 by name: in the city but not on Elliniko Metro's base line "
                 f"{sorted(got - want)}; on it but not in the city {sorted(want - got)}")
    print(f"    by name: the {len(kept)} in the city are Elliniko Metro's base line, name for name")
    print(f"    source: {config.OPERATOR_COUNTS_SOURCE}")

    gaps = station_gates.nearest_neighbour_m(kept.longitude, kept.latitude, config.CRS_PROJECTED)
    med = float(np.median(gaps))
    print(f"  median nearest-station gap in the city: {med:.0f} m (min {gaps.min():.0f}, "
          f"max {gaps.max():.0f}); rings {config.RING_LABELS}")
    lo_, hi_ = config.MEDIAN_GAP_BOUNDS_M
    if not lo_ <= med <= hi_:
        sys.exit(f"median gap {med:.0f} m outside {lo_}-{hi_}: re-read the ring rule "
                 f"(docs/ring_rules.md) before changing the bounds")
    emit("stop_nodes", len(platforms))
    emit("stations_all", len(st))
    emit("stations_kept", len(kept))
    emit("stations_outside", len(out))

    out["lines"] = out["lines"].map(lambda ks: " ".join(config.LINE_NAMES[k] for k in ks.split()))
    # "outside" is the word app/station_scope.py reads.
    out["reason"] = [f"in {m}, outside the Municipality of Thessaloniki" for m in out.located_in]
    if (out.located_in == "").any():
        sys.exit(f"outside stations in no municipality of the query: {list(out.station[out.located_in == ''])}")
    out = out[["station", "lines", "reason", "latitude", "longitude"]]
    out.to_csv(config.EXCLUDED_STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"  {len(out)} stations outside the city -> {config.EXCLUDED_STATIONS_CSV.name}")

    kept = kept[["station", "name_el", "latitude", "longitude", "lines"]].sort_values("station")
    kept.to_csv(config.STATIONS_CSV, index=False, encoding="utf-8", lineterminator="\n")
    print(f"  wrote {config.STATIONS_CSV.name}: {len(kept)} stations")

    # --- the drawn line, cut at the city line -------------------------------
    rel_out = []
    for k, (ref, colour, name, _end) in config.LINES.items():
        lines_m, branch = line_geometry(groups[k])
        inside, before, after = clip_to_city(lines_m, poly)
        if not inside:
            sys.exit(f"{name}: no track inside the city")
        print(f"  {name}: {len(lines_m)} ways ({branch} branch), {before / 1000:.2f} km; inside the "
              f"city {len(inside)} pieces, {after / 1000:.2f} km")
        # The cut must keep the track at every kept station.
        track = unary_union([to_m(g) for g in inside])
        far = [(s, round(track.distance(Point(TO_M.transform(lo, la)))))
               for s, la, lo in zip(kept.station, kept.latitude, kept.longitude)]
        far = [f for f in far if f[1] > config.STATION_ON_TRACK_M]
        if far:
            sys.exit(f"{name}: kept stations off the cut track: {far}")
        rel_out.append({"type": "relation", "id": len(rel_out) + 1,
                        "tags": {"ref": ref, "name": name, "colour": colour},
                        "members": [{"type": "way", "geometry": [{"lat": la, "lon": lo} for la, lo in g]}
                                    for g in inside]})
        emit("track_km_in_city", round(after / 1000, 2))
    config.RAIL_LINES_JSON.write_bytes(json.dumps({"elements": rel_out}).encode("utf-8"))
    emit("lines_drawn", len(rel_out))


if __name__ == "__main__":
    main()
