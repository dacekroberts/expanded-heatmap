"""Step 1 - Mexico City's rail stations, from OpenStreetMap.

THE FIRST STEP 1 IN THIS PROJECT THAT IS NOT GTFS. Every `*.cdmx.gob.mx` host
is unreachable (see config.py's docstring), so the geometry comes from OSM as a
documented per-city exception approved 2026-09-22.

What that changes, concretely, because "it's just a different source" is not
true:

  * NO parent_station, so the collapse is BY NAME. OSM carries one station node
    per line at an interchange - Pantitlan, La Raza, Jamaica, Oceania - which
    is a fourth collapse mechanism after Edmonton's parent_station, Calgary's
    direction prefix and Toronto's three naming conventions.
  * NO stop_times, so pipeline/stations.py's BOARDABILITY gate cannot run. Its
    analogue here is the railway=station whitelist below, plus the named stop
    members of the drawn route relations, which carry nine stations the
    whitelist cannot see (2026-10-04). The gate is not allowed to pass
    silently on a source that cannot answer it.
  * The operator's published count - gate 3 - is UNAVAILABLE, because the
    operator is the unreachable host. config.STATION_COUNT_GATE_3 is None and
    says why. This is disclosed on the city page.
  * OSM mixes PROPOSED infrastructure in with built, and misspells it. See
    OSM_EXCLUDE_RAILWAY.
"""

import json
import math
import sys

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, shape
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent.parent))

from pipeline.stations import (
    check_operator_counts,
    check_route_stops_covered,
    projected_xy,
    route_stop_members,
    station_name_key,
    strip_line_designator,
    verify_stations,
)
from pipeline.mexico_city.config import (
    CABLE_ATTACH_MAX_M,
    CABLE_LINES,
    CABLE_STATION_ALIASES,
    OSM_AERIALWAY_JSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    LINE_NAMES,
    MUNICIPIOS,
    MUNIDS,
    OSM_BOUNDARY_JSON,
    OSM_EXCLUDE_RAILWAY,
    OSM_MUNICIPIOS_JSON,
    OSM_RAILWAY_KEEP,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OSM_STATION_NETWORKS,
    REGIONAL,
    REGIONAL_STATE_CODE,
    STATIONS_CSV,
    STATION_COUNT_GATE_3,
    STATION_COUNT_GATE_3_REASON,
    STATIONS_PER_MUNICIPIO,
)

# CDMX is 1,495 km2. A boundary that assembles wrong - the usual failure is a
# ring that does not close, leaving a sliver or the whole bbox - shows up here
# rather than as zero stations kept later. Surrey's boundary declared the wrong
# CRS and put every containment test at zero; Vancouver's was a MultiLineString
# that matched nothing. An area gate catches both shapes of that error.
BOUNDARY_AREA_KM2_MIN = 1_300.0
BOUNDARY_AREA_KM2_MAX = 1_700.0

# Mexico City (Regional): the four State of México municipios together,
# measured 414.0 km2 in EPSG:32614 on 2026-10-07 (Ecatepec 156.1, Naucalpan
# 157.9, Nezahualcóyotl 62.6, La Paz 37.3; relations 5605754, 5606080,
# 5606086, 5605964). The band is wide enough for OSM edits and narrow enough
# to catch a ring that did not close or a municipio that went missing (the
# smallest, La Paz, is 37 km2: losing it leaves 377, inside the band, which
# is why each MUNID is also required by name below).
MUNICIPIOS_AREA_KM2_MIN = 330.0
MUNICIPIOS_AREA_KM2_MAX = 520.0


def read_cached(path, label):
    """Read a raw input that `fetch_sources.py` has already downloaded.

    This step does NOT fetch. It used to - `overpass()` lived here and pulled
    on a cache miss - which made `drift_check.py` reach the network on any
    checkout without `data/mexico_city/raw/`, and turned "does the committed
    code still produce the committed output" into "does the current upstream".
    See pipeline/mexico_city/fetch_sources.py for the whole argument.
    """
    if not path.exists():
        raise SystemExit(
            f"Missing {path.name} ({label}). "
            f"Run pipeline/mexico_city/fetch_sources.py first."
        )
    print(f"  {label}: {path.name} ({path.stat().st_size:,} bytes)")
    return json.loads(path.read_text(encoding="utf-8"))


def load_boundary():
    """Assemble CDMX's admin_level=4 polygon from the relation's member ways."""
    data = read_cached(OSM_BOUNDARY_JSON, "boundary")
    rels = [e for e in data["elements"] if e["type"] == "relation"]
    if len(rels) != 1:
        raise SystemExit(
            f"Expected exactly one admin_level=4 relation named "
            f"'Ciudad de México', got {len(rels)}. Two layers with the same "
            "name is a real hazard here (Calgary published two 'City "
            "Boundary' layers, one of them 184 bytes of useless GeoJSON)."
        )
    lines = [
        [(p["lon"], p["lat"]) for p in m["geometry"]]
        for m in rels[0].get("members", [])
        if m.get("type") == "way" and m.get("role") == "outer" and m.get("geometry")
    ]
    if not lines:
        raise SystemExit("boundary relation carried no outer way geometry")
    polys = list(polygonize(linemerge(MultiLineString(lines))))
    if not polys:
        raise SystemExit(
            "outer ways did not close into a polygon - the rings did not "
            "assemble, which is the usual Overpass boundary failure"
        )
    geom = unary_union(polys)
    area_km2 = (gpd.GeoSeries([geom], crs=CRS_GEOGRAPHIC)
                .to_crs(CRS_PROJECTED).area.iloc[0] / 1e6)
    print(f"  boundary: {len(polys)} polygon(s), {area_km2:,.0f} km2")
    if not BOUNDARY_AREA_KM2_MIN <= area_km2 <= BOUNDARY_AREA_KM2_MAX:
        raise SystemExit(
            f"CDMX boundary area {area_km2:,.0f} km2 is outside "
            f"{BOUNDARY_AREA_KM2_MIN:,.0f}-{BOUNDARY_AREA_KM2_MAX:,.0f}. "
            "Either the rings assembled wrong or this is not CDMX."
        )
    return geom


def _outer_polygon(rel):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer"
             and m.get("geometry")]
    if not lines:
        return None
    polys = list(polygonize(linemerge(MultiLineString(lines))))
    return unary_union(polys) if polys else None


def load_municipios():
    """Mexico City (Regional): one polygon per State of México municipio,
    keyed by INEGI:MUNID (Monterrey's join key, pipeline/monterrey/
    step1_stations.py), plus their union. Steps 2 and 3 read this too, so all
    three steps agree on where the region is."""
    data = read_cached(OSM_MUNICIPIOS_JSON, "municipio boundaries")
    by_code = {}
    for rel in (e for e in data["elements"] if e["type"] == "relation"):
        munid = rel.get("tags", {}).get("INEGI:MUNID")
        if munid not in MUNIDS:
            continue
        if munid in by_code:
            raise SystemExit(f"Two boundary relations carry INEGI:MUNID {munid}. "
                             "Inspect them; never pick by size.")
        geom = _outer_polygon(rel)
        if geom is None:
            raise SystemExit(f"INEGI:MUNID {munid} ({rel['tags'].get('name')}) "
                             "did not assemble into a polygon.")
        by_code[munid] = geom
    missing = [m for m in MUNIDS if m not in by_code]
    if missing:
        raise SystemExit(f"No boundary for {missing}. All four are required: a "
                         "missing municipio would silently drop its stations.")
    areas = (gpd.GeoSeries(list(by_code.values()), index=list(by_code),
                           crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).area / 1e6)
    for munid, a in areas.items():
        print(f"      {munid} {MUNICIPIOS[munid[len(REGIONAL_STATE_CODE):]]:22s} "
              f"{a:7,.1f} km2")
    union = unary_union(list(by_code.values()))
    area = (gpd.GeoSeries([union], crs=CRS_GEOGRAPHIC)
            .to_crs(CRS_PROJECTED).area.iloc[0] / 1e6)
    print(f"  municipios: {len(by_code)}, union {area:,.1f} km2")
    if not MUNICIPIOS_AREA_KM2_MIN <= area <= MUNICIPIOS_AREA_KM2_MAX:
        raise SystemExit(f"municipio union {area:,.0f} km2 outside "
                         f"{MUNICIPIOS_AREA_KM2_MIN:,.0f}-"
                         f"{MUNICIPIOS_AREA_KM2_MAX:,.0f}.")
    return by_code, union


def load_scope():
    """The polygon the map covers: CDMX alone, or CDMX plus the four
    municipios when REGIONAL is on. Returns (scope, cdmx, municipios by code)."""
    cdmx = load_boundary()
    if not REGIONAL:
        return cdmx, cdmx, {}
    by_code, union = load_municipios()
    return unary_union([cdmx, union]), cdmx, by_code


def _centre(element):
    """(lat, lon) of a cached OSM object: a node's own point, or the centre
    of a way's or relation's bounds (`out body geom` gives both)."""
    if element["type"] == "node":
        return element["lat"], element["lon"]
    b = element["bounds"]
    return (b["minlat"] + b["maxlat"]) / 2, (b["minlon"] + b["maxlon"]) / 2


def load_cable_stations(grouped):
    """The cable cars' stations (Cablebús and Mexicable), for the lines in
    config.CABLE_LINES.

    A line's stations are the aerialway=station NODE MEMBERS of its route
    relation, plus the objects config names under `extra` (Cablebús Línea 3,
    whose stations are not members). Gate 3 runs here per line against the
    operator's count, and RAISES on a mismatch.

    A cable station whose name key matches a station already in `grouped` is
    the same interchange and ATTACHES to it: no row is added and the existing
    station keeps its position. Averaging it in, as the Metro collapse does,
    would move three Metro stations by up to 170 m.

    Returns (new stations, every cable station point, attached rows)."""
    data = read_cached(OSM_AERIALWAY_JSON, "cable cars")
    by_id = {(e["type"], e["id"]): e for e in data["elements"]}
    rows = []
    for key, spec in CABLE_LINES.items():
        rel = by_id.get(("relation", spec["relation"]))
        if rel is None or rel.get("tags", {}).get("route") != "aerialway":
            raise SystemExit(f"{spec['name']}: relation {spec['relation']} is "
                             f"not a route=aerialway relation in "
                             f"{OSM_AERIALWAY_JSON.name}.")
        members = [("node", m["ref"]) for m in rel.get("members", [])
                   if m.get("type") == "node"]
        for ident in members + list(spec["extra"]):
            element = by_id.get(ident)
            tags = (element or {}).get("tags") or {}
            if tags.get("aerialway") != "station":
                if ident in spec["extra"]:
                    raise SystemExit(f"{spec['name']}: {ident} is listed as a "
                                     "station in config and is not one in the "
                                     "cache.")
                continue    # an untagged member node, never a station
            name = (tags.get("name") or "").strip()
            if not name:
                raise SystemExit(f"{spec['name']}: station {ident} has no name.")
            lat, lon = _centre(element)
            rows.append({"line": key,
                         "name": CABLE_STATION_ALIASES.get(name, name),
                         "latitude": lat, "longitude": lon,
                         "network": spec["network"]})
    cable = pd.DataFrame(rows)
    cable["key"] = cable["name"].map(station_name_key)

    # Gate 3, per line: the operator's count against the build's.
    actual = {CABLE_LINES[k]["name"]: int(n)
              for k, n in cable.groupby("line")["key"].nunique().items()}
    expected = {spec["name"]: spec["count"] for spec in CABLE_LINES.values()}
    print("\n  cable cars, gate 3:")
    mismatched = check_operator_counts(expected, actual)
    if mismatched:
        raise SystemExit(f"cable-car station counts disagree with the "
                         f"operators: {mismatched}")

    xy = projected_xy(cable.index, cable["longitude"], cable["latitude"],
                      CRS_PROJECTED)
    have = {station_name_key(n): i for i, n in grouped["name"].items()}
    have_xy = projected_xy(grouped.index, grouped["longitude"],
                           grouped["latitude"], CRS_PROJECTED)
    new, attached = [], []
    for key, g in cable.groupby("key", sort=True):
        lines = ", ".join(CABLE_LINES[k]["name"] for k in sorted(set(g["line"])))
        if key in have:
            i = have[key]
            far = max(math.dist(xy[j], have_xy[i]) for j in g.index)
            if far > CABLE_ATTACH_MAX_M:
                raise SystemExit(
                    f"{g['name'].iloc[0]} ({lines}) is {far:,.0f} m from the "
                    f"station of the same name, over {CABLE_ATTACH_MAX_M:.0f} "
                    "m: two places under one name, not an interchange.")
            attached.append({"index": i, "name": grouped.at[i, "name"],
                             "lines": lines, "metres": round(far),
                             "networks": sorted(set(g["network"]))})
            continue
        spread = max(math.dist(xy[a], xy[b]) for a in g.index for b in g.index)
        if spread > CABLE_ATTACH_MAX_M:
            raise SystemExit(f"{g['name'].iloc[0]} ({lines}): same-named cable "
                             f"stations {spread:,.0f} m apart.")
        new.append({"name": g["name"].iloc[0],
                    "latitude": g["latitude"].mean(),
                    "longitude": g["longitude"].mean(),
                    "nodes": len(g),
                    "networks": "; ".join(sorted(set(g["network"])))})
    print(f"  cable cars: {len(cable)} station points on {len(CABLE_LINES)} "
          f"lines -> {len(new)} new stations, {len(attached)} attached to a "
          "station already on the map (not moved):")
    for a in attached:
        print(f"      {a['name']:24s} {a['metres']:4d} m   {a['lines']}")
    return pd.DataFrame(new), cable, attached


def main():
    print("=== Step 1: Mexico City stations (OpenStreetMap) ===\n")

    print("Reading cached OSM:")
    st_data = read_cached(OSM_STATIONS_JSON, "stations")
    rt_data = read_cached(OSM_ROUTES_JSON, "routes")
    boundary, cdmx, municipios = load_scope()

    nodes = [e for e in st_data["elements"]
             if e["type"] == "node" and "tags" in e]
    print(f"\nRaw railway=* nodes in bbox: {len(nodes):,}")

    tagged = pd.DataFrame([
        {
            "name": (e["tags"].get("name") or "").strip(),
            "railway": e["tags"].get("railway"),
            "station": e["tags"].get("station"),
            "subway": e["tags"].get("subway"),
            "network": (e["tags"].get("network") or "").strip(),
            "latitude": e["lat"],
            "longitude": e["lon"],
        }
        for e in nodes
    ])

    # --- the whitelist, and what it removes -------------------------------
    for bad in OSM_EXCLUDE_RAILWAY:
        n = int((tagged["railway"] == bad).sum())
        if n:
            print(f"  excluded railway={bad:18s} {n:5d}")
    platforms = tagged[tagged["railway"].isin(OSM_RAILWAY_KEEP)].copy()
    print(f"  railway=station kept: {len(platforms):,}")

    # MATCH ON THE MODE, NEVER ON THE NETWORK LABEL ALONE. Seven real stations
    # (Tlahuac, Atlalilco, La Raza, Pantitlan x2, Huipulco, Estadio Azteca)
    # carry no network tag, so network alone is too narrow - but it is also too
    # WIDE: OSM tags Lecheria `network=STC Metro` with no station or subway tag
    # at all, and Lecheria is a Ferrocarril Suburbano station, not Metro. A
    # network-only match admitted it into the published excluded-stations
    # record as a Metro station. What a node IS (its mode) is evidence; what a
    # label claims about its operator is not.
    is_rail = (
        platforms["station"].isin(("subway", "light_rail"))
        | (platforms["subway"] == "yes")
    )
    platforms = platforms[is_rail & (platforms["name"] != "")].copy()
    print(f"  metro/light-rail with a name: {len(platforms):,}")
    for net, n in platforms["network"].value_counts().items():
        print(f"      network={net or '(none)':24s} {n:5d}")

    # --- ROUTE-RELATION MEMBERSHIP: the stations the whitelist cannot see ---
    # Nine Metro stations exist only as `railway=stop` positions on their
    # line's route relation (Talismán's station node has no mode tag), four
    # termini among them; the whitelist alone dropped all nine until
    # 2026-10-04 (DECISIONS.md). A named stop
    # whose key matches no whitelisted node becomes a station here. Station
    # nodes keep precedence wherever they exist, so no kept station moves.
    rels = [e for e in rt_data["elements"] if e["type"] == "relation"]
    nodes_by_id = {e["id"]: e for e in st_data["elements"] if e["type"] == "node"}
    route_stops = route_stop_members(rels, nodes_by_id, refs=LINE_NAMES)
    have = set(platforms["name"].map(station_name_key))
    named = route_stops[route_stops["name"] != ""]
    added = named[~named["name"].map(station_name_key).isin(have)]
    print(f"\nRoute stop members: {len(route_stops):,} "
          f"({len(named):,} named); stations only a stop member gives: "
          f"{added['name'].nunique()}")
    for name, g in added.groupby("name"):
        print(f"      {name:28s} line(s) {', '.join(sorted(set(g['line'])))}")
    platforms = pd.concat([
        platforms,
        added.drop_duplicates("node")
             .assign(railway="stop")[["name", "railway", "network",
                                      "latitude", "longitude"]],
    ], ignore_index=True)

    # --- COLLAPSE BY NAME KEY, the fourth mechanism this project has met ---
    # OSM has one node per line at an interchange. Averaging the coordinates of
    # same-named nodes is right here and would be wrong in a feed with
    # platform-level nodes spread down a street; these are the same station box
    # entered from different lines. The key, not the raw name, because OSM
    # also names an interchange per line: "Consulado" / "Consulado L4" (330 m)
    # and "Candelaria L1" / "Candelaria L4" (180 m) were each kept twice
    # until 2026-10-04. The shown name drops the line designator.
    platforms["key"] = platforms["name"].map(station_name_key)

    def shown_name(names):
        counts = names.map(strip_line_designator).value_counts()
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]

    grouped = (platforms.groupby("key", as_index=False)
               .agg(name=("name", shown_name),
                    latitude=("latitude", "mean"),
                    longitude=("longitude", "mean"),
                    nodes=("name", "size"),
                    networks=("network", lambda s: "; ".join(sorted(
                        {x for x in s if x}))))
               .drop(columns="key"))
    print(f"\nCollapsed {len(platforms):,} nodes -> {len(grouped):,} stations "
          f"by name key")
    spelled = platforms.groupby("key")["name"].nunique()
    for key in spelled[spelled > 1].index:
        print(f"      one station, several names: "
              f"{sorted(set(platforms.loc[platforms['key'] == key, 'name']))}")
    multi = grouped[grouped["nodes"] > 1]
    print(f"  names with more than one node (interchanges): {len(multi)}")
    for _, r in multi.sort_values("nodes", ascending=False).head(6).iterrows():
        print(f"      {r['name']:28s} {r['nodes']} nodes   {r['networks']}")

    # Every stop of every drawn line has a station, in scope or not. Raises.
    station_of = check_route_stops_covered(
        city="Mexico City", route_stops=route_stops, stations=grouped,
        crs_projected=CRS_PROJECTED, name_col="name")
    per_line = {LINE_NAMES[ref]: n for ref, n in
                station_of.groupby(route_stops["line"]).nunique().items()}
    print("  stations per line, from route membership (not gate 3):")
    for ref in LINE_NAMES:
        print(f"      {LINE_NAMES[ref]:12s} {per_line.get(LINE_NAMES[ref], 0):4d}")

    # --- the cable cars: added AFTER the Metro collapse, so none moves -----
    before = grouped[["latitude", "longitude"]].copy()
    cable_new, cable_points, attached = load_cable_stations(grouped)
    for a in attached:
        nets = set(filter(None, grouped.at[a["index"], "networks"].split("; ")))
        grouped.at[a["index"], "networks"] = "; ".join(
            sorted(nets | set(a["networks"])))
    assert before.equals(grouped[["latitude", "longitude"]]), (
        "a Metro or Tren Ligero station moved while the cable cars were added")
    grouped = pd.concat([grouped, cable_new], ignore_index=True)
    platforms = pd.concat([
        platforms,
        cable_points.assign(railway="aerialway")[
            ["name", "railway", "network", "latitude", "longitude", "key"]],
    ], ignore_index=True)

    # --- boundary filter --------------------------------------------------
    gdf = gpd.GeoDataFrame(
        grouped,
        geometry=gpd.points_from_xy(grouped["longitude"], grouped["latitude"]),
        crs=CRS_GEOGRAPHIC,
    )
    inside = gdf.within(boundary)
    kept = gdf[inside].drop(columns="geometry").copy()
    outside = gdf[~inside].copy()
    if not REGIONAL:
        print(f"\nInside Ciudad de México: {len(kept):,}")
        print(f"Outside (Estado de México - Lines 2, A and B): {len(outside):,}")
    else:
        # Each kept station's municipio by point in polygon on INEGI:MUNID,
        # asserted against the brief's count per municipio, so a boundary
        # edit that moves a station across a line fails here.
        in_cdmx = gdf[inside].within(cdmx)
        print(f"\nInside the scope (CDMX and four municipios): {len(kept):,}"
              f"   CDMX {int(in_cdmx.sum()):,}   outside: {len(outside):,}")
        per_muni = {}
        for _, r in gdf[inside][~in_cdmx].iterrows():
            hits = [k for k, g in municipios.items() if r.geometry.within(g)]
            if len(hits) != 1:
                raise SystemExit(f"{r['name']}: in {len(hits)} municipio "
                                 "polygons, expected exactly one.")
            per_muni.setdefault(hits[0], []).append(r["name"])
        for munid in MUNIDS:
            names = sorted(per_muni.get(munid, []))
            code = munid[len(REGIONAL_STATE_CODE):]
            print(f"    {munid} {MUNICIPIOS[code]:22s} {len(names):2d}  "
                  f"{', '.join(names)}")
        got = {m[len(REGIONAL_STATE_CODE):]: len(v) for m, v in per_muni.items()}
        if got != STATIONS_PER_MUNICIPIO:
            raise SystemExit(f"stations per municipio {got} != "
                             f"{STATIONS_PER_MUNICIPIO} (the brief's count).")

    # Written even when empty (header only), so a regional build that keeps
    # every station never leaves the city-alone list behind.
    if len(outside) or REGIONAL:
        b_proj = gpd.GeoSeries([boundary], crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).iloc[0]
        dist = (outside.to_crs(CRS_PROJECTED).geometry
                .apply(lambda g: g.distance(b_proj)).round(0))
        EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
        (outside.drop(columns="geometry")
         .assign(distance_outside_m=dist.values,
                 lines=outside["networks"].values)
         .rename(columns={"name": "station"})
         [["station", "latitude", "longitude", "lines", "distance_outside_m"]]
         .sort_values("distance_outside_m", ascending=False)
         .to_csv(EXCLUDED_STATIONS_CSV, index=False))
        print(f"  wrote {EXCLUDED_STATIONS_CSV.name}")
        for _, r in (outside.assign(d=dist.values)
                     .sort_values("d", ascending=False).head(5).iterrows()):
            print(f"      {r['name']:28s} {r['d']:8,.0f} m outside")

    # --- the gates --------------------------------------------------------
    print("\n--- station verification ---")
    refs =sorted({r["tags"].get("ref") for r in rels if r["tags"].get("ref")})
    print(f"Route relations: {len(rels)} over {len(refs)} refs: {', '.join(refs)}")
    # EVERY CHECK BELOW IS VACUOUS ON AN EMPTY SET, so assert non-empty first.
    # An empty Overpass result once made this function print "every ref has
    # exactly 2 direction relations" over zero relations.
    if len(rels) < 2 * len(LINE_NAMES):
        raise SystemExit(
            f"Only {len(rels)} route relations for {len(LINE_NAMES)} configured "
            f"lines; expected 2 per line (both directions). An empty or partial "
            "Overpass result must fail here rather than pass silently."
        )
    missing = [r for r in refs if r not in LINE_NAMES]
    if missing:
        raise SystemExit(
            f"OSM refs with no name in config.LINE_NAMES: {missing}. Every "
            "drawn line needs its real public name (project invariant)."
        )
    # Cross-direction agreement: each line should have exactly two relations.
    per_ref = pd.Series([r["tags"].get("ref") for r in rels]).value_counts()
    odd = per_ref[per_ref != 2]
    if len(odd):
        print(f"  NOTE refs without exactly 2 direction relations:\n{odd}")
    else:
        print(f"  every ref has exactly 2 direction relations (both ways)")

    print(f"\nGATE 3 (operator's published count): UNAVAILABLE")
    print(f"  {STATION_COUNT_GATE_3_REASON}")
    assert STATION_COUNT_GATE_3 is None, (
        "If a published count becomes available, set STATION_COUNT_GATE_3 and "
        "pass it to verify_stations as expected_per_line."
    )

    verify_stations(
        city="Mexico City",
        platforms=platforms,
        stations=kept,
        crs_projected=CRS_PROJECTED,
        expected_per_line=None,     # gate 3 unavailable - see above
    )

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    (kept.rename(columns={"name": "station"})
     .sort_values("station")[["station", "latitude", "longitude"]]
     .to_csv(STATIONS_CSV, index=False))
    print(f"\nWrote {len(kept)} stations to {STATIONS_CSV}")


if __name__ == "__main__":
    main()
