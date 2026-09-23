"""Step 1 - Barcelona Metro stations, from OpenStreetMap.

Spain's second city, and the one that shows what did NOT generalise from
Madrid. Madrid's rail came from CRTM's own ArcGIS feature layers, which are
maintained and which this project took in preference to CRTM's stale GTFS.
Barcelona's operator publishes GTFS behind a free account, so the equivalent
move is unavailable, and OSM is better than the alternative anyway: the agency
route needs FOUR feeds - TMB, FGC, TRAM and TRAM Besos - against one query.

THE STATION OBJECT IS DIFFERENT AGAIN. Three OSM cities, three answers:

    Mexico City   184  railway=station
    Guadalajara     1  railway=station   - its stations are railway=stop
    Barcelona     227  railway=station, 181 of them station=subway
                  ...and 501 railway=stop, which is what Guadalajara keys on

So Guadalajara's whitelist would have collected 501 per-direction stop
positions here. That is the meta-rule `osm-rail` exists for, hit a third time.

STATIONS ARE THE ROUTE RELATIONS' OWN MEMBER NODES, NOT NODES SELECTED BY TAG.
Two reasons, and the second was found the hard way:

  * Nine of the 181 `station=subway` nodes carry no `network` tag at all - Moli
    Nou, Gornal, Almeda, Cornella-Riera, Avinguda Carrilet among them, most
    being real L8 and L10 Sud stations - so any network filter drops them.
  * `railway=station` and the nodes a PTv2 route relation contains are
    DIFFERENT OBJECTS. A relation holds `stop_position` nodes (`railway=stop`);
    `railway=station` marks the station box and hangs off a `stop_area`
    relation instead. Measured here: 225 station nodes, 374 member nodes, **no
    overlap at all.** The first version of this step combined both filters and
    got an empty set.

It is also how FT's stations stay out without naming them: FT is not a drawn
line, so its nodes are not members of anything drawn.
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.osm_cache import load as osm_load
from pipeline.stations import verify_stations
from pipeline.barcelona.config import (
    BOUNDARY_AREA_KM2,
    BOUNDARY_AREA_TOLERANCE_KM2,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DRAWN_REFS,
    EXCLUDED_STATIONS_CSV,
    LINE_NAMES,
    OSM_BOUNDARY_JSON,
    OSM_EXCLUDE_RAILWAY,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    REF_ALIASES,
    STATIONS_CSV,
    STATION_ALIASES,
)

def canonical_ref(ref):
    """One key per line, whichever mirror answered.

    `overpass-api.de` says `L10N`; `overpass.kumi.systems` says `L10 Nord`.
    Both are current OSM as far as either host is concerned - they run
    different planet extracts - so the build normalises rather than trusting
    whichever host was up.
    """
    if not ref:
        return None
    key = " ".join(str(ref).split()).upper()
    return REF_ALIASES.get(key, key)


def _poly(rel):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer"
             and m.get("geometry")]
    if not lines:
        return None
    polys = list(polygonize(linemerge(MultiLineString(lines))))
    return unary_union(polys) if polys else None


def load_boundary():
    elements, host = osm_load(OSM_BOUNDARY_JSON, "the municipal boundary")
    print(f"  boundary: via {host}")
    rels = [e for e in elements if e["type"] == "relation"]
    polys = [g for g in (_poly(r) for r in rels) if g is not None]
    if not polys:
        raise SystemExit(
            "No usable Barcelona boundary polygon. Do NOT fall back to a "
            "bounding box - the whole point of the boundary is that the metro "
            "runs well past the municipality (L8 and L10 Sud reach Cornella "
            "and El Prat).")
    if len(polys) > 1:
        raise SystemExit(
            f"{len(polys)} boundary relations named Barcelona inside the bbox. "
            "Do not pick by size - that is what selected a Spanish province "
            "during the Guadalajara build. Inspect them and name the right one.")
    boundary = polys[0]
    area = (gpd.GeoSeries([boundary], crs=CRS_GEOGRAPHIC)
            .to_crs(CRS_PROJECTED).area.iloc[0] / 1e6)
    print(f"  boundary area: {area:,.1f} km2 "
          f"(expected {BOUNDARY_AREA_KM2} +/- {BOUNDARY_AREA_TOLERANCE_KM2})")
    if abs(area - BOUNDARY_AREA_KM2) > BOUNDARY_AREA_TOLERANCE_KM2:
        raise SystemExit(
            f"Boundary area {area:,.1f} km2 is not Barcelona's {BOUNDARY_AREA_KM2}. "
            "Either the wrong relation was selected or the rings did not close.")
    return boundary


def main():
    print("=== Step 1: Barcelona Metro stations (OpenStreetMap) ===\n")
    print("Reading cached OSM (fetch_sources.py downloads it):")
    route_els, route_host = osm_load(OSM_ROUTES_JSON, "route relations")
    print(f"  routes: via {route_host}, {len(route_els)} relations")
    station_els, station_host = osm_load(OSM_STATIONS_JSON, "their member nodes")
    print(f"  stations: via {station_host}, {len(station_els)} nodes")
    boundary = load_boundary()

    # --- the drawn lines ---------------------------------------------------
    rels = [e for e in route_els if e["type"] == "relation" and "tags" in e]
    seen_refs = {}
    for rel in rels:
        ref = canonical_ref(rel["tags"].get("ref"))
        if ref:
            seen_refs.setdefault(ref, []).append(rel)
    print(f"\nOSM route relations: {len(rels)} over {len(seen_refs)} refs")
    print(f"  {', '.join(sorted(seen_refs))}")

    drawn = {ref: seen_refs[ref] for ref in DRAWN_REFS if ref in seen_refs}
    missing = [r for r in DRAWN_REFS if r not in seen_refs]
    if missing:
        raise SystemExit(
            f"Drawn lines absent from OSM: {missing}. Every line in LINE_NAMES "
            "must exist, or the map would silently lose one - which is exactly "
            "what Guadalajara's rejected GTFS did to Linea 4.")
    not_drawn = sorted(set(seen_refs) - set(DRAWN_REFS))
    print(f"  drawn: {len(drawn)}   not drawn: {not_drawn or 'none'}")
    print("  (FT is the Tibidabo funfair funicular, operated by Barcelona de "
          "Serveis Municipals with no network tag; trams are their own "
          "networks. Both excluded by the operators' own tagging.)")

    # Node ids belonging to a drawn relation. This IS the station filter.
    drawn_node_ids = set()
    for rel_list in drawn.values():
        for rel in rel_list:
            for m in rel.get("members", ()):
                if m.get("type") == "node":
                    drawn_node_ids.add(m["ref"])
    print(f"  node members of drawn relations: {len(drawn_node_ids):,}")

    # --- stations ----------------------------------------------------------
    nodes = [e for e in station_els if e["type"] == "node" and "tags" in e]
    tagged = pd.DataFrame([{
        "id": e["id"],
        "name": (e["tags"].get("name") or "").strip(),
        "railway": e["tags"].get("railway"),
        "station": e["tags"].get("station"),
        "latitude": e["lat"],
        "longitude": e["lon"],
    } for e in nodes])
    print(f"\nMember nodes of subway/funicular relations: {len(tagged):,}")
    for bad in OSM_EXCLUDE_RAILWAY:
        n = int((tagged["railway"] == bad).sum())
        if n:
            print(f"  excluded railway={bad:20s} {n:5d}")

    platforms = tagged[tagged["id"].isin(drawn_node_ids)
                       & (tagged["name"] != "")].copy()
    print(f"  on a drawn line, with a name: {len(platforms):,}")
    if platforms.empty:
        raise SystemExit("No stations matched a drawn relation - a fetch "
                         "problem, not a fact about Barcelona.")

    # FGC's city-prefixed names folded onto TMB's. See STATION_ALIASES.
    hit = platforms["name"].isin(STATION_ALIASES)
    if hit.any():
        for old, new in STATION_ALIASES.items():
            n = int((platforms["name"] == old).sum())
            if n:
                print(f"  alias: {old!r} -> {new!r} ({n} node(s))")
        platforms["name"] = platforms["name"].replace(STATION_ALIASES)
    else:
        print("  NOTE: no STATION_ALIASES matched. Either OSM renamed them or "
              "the duplicate-interchange problem moved - check the "
              "nearest-neighbour minimum below before trusting the collapse.")

    grouped = (platforms.groupby("name", as_index=False)
               .agg(latitude=("latitude", "mean"),
                    longitude=("longitude", "mean"),
                    nodes=("name", "size")))
    per = grouped["nodes"].value_counts().to_dict()
    print(f"\nCollapsed {len(platforms):,} nodes -> {len(grouped):,} stations "
          f"by name")
    print(f"  nodes-per-name distribution: {per}")
    multi = grouped[grouped["nodes"] > 1]
    if len(multi):
        print(f"  {len(multi)} interchange names carry several nodes "
              f"(one per line calling there):")
        for _, r in multi.sort_values("nodes", ascending=False).head(8).iterrows():
            print(f"      {r['name']:34s} {r['nodes']} nodes")

    # --- boundary filter ----------------------------------------------------
    gdf = gpd.GeoDataFrame(
        grouped,
        geometry=gpd.points_from_xy(grouped["longitude"], grouped["latitude"]),
        crs=CRS_GEOGRAPHIC)
    inside = gdf.within(boundary)
    kept, outside = gdf[inside].copy(), gdf[~inside].copy()
    print(f"\nInside Barcelona: {len(kept):,}")
    print(f"Outside (L8/L10 Sud run to Cornella, El Prat and Sant Boi; "
          f"L1 to Hospitalet): {len(outside):,}")

    if len(outside):
        b_proj = (gpd.GeoSeries([boundary], crs=CRS_GEOGRAPHIC)
                  .to_crs(CRS_PROJECTED).iloc[0])
        dist = (outside.to_crs(CRS_PROJECTED).geometry
                .apply(lambda g: g.distance(b_proj)).round(0))
        EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
        (outside.drop(columns="geometry")
         .assign(distance_outside_m=dist.values, lines="Barcelona Metro")
         .rename(columns={"name": "station"})
         [["station", "latitude", "longitude", "lines", "distance_outside_m"]]
         .sort_values("distance_outside_m", ascending=False)
         .to_csv(EXCLUDED_STATIONS_CSV, index=False))
        print(f"  wrote {EXCLUDED_STATIONS_CSV.name} ({len(outside)} excluded)")

    # --- gates --------------------------------------------------------------
    print("\n--- station verification ---")
    actual = {}
    for ref, rel_list in drawn.items():
        best = max(rel_list, key=lambda x: sum(
            1 for m in x.get("members", ())
            if str(m.get("role", "")).startswith("stop")))
        actual[LINE_NAMES[ref]] = sum(
            1 for m in best.get("members", ())
            if str(m.get("role", "")).startswith("stop"))
    print("OSM stop-members per line:")
    for name, n in sorted(actual.items(), key=lambda kv: -kv[1]):
        print(f"    {name:26s} {n:3d}")

    # GATE 3 IS NOT RUN, AND THE GAP IS NAMED RATHER THAN FILLED. TMB publishes
    # a network-wide station figure but no per-line table that this build has
    # obtained, and FGC's four metro lines are a different operator again. A
    # partial gate with its gaps stated is worth more than a complete-looking
    # one assembled from memory - Guadalajara's precedent, where SITEUR
    # published counts for two lines of four and only those two were checked.
    print("\nGate 3 (operator's published per-line counts): NOT RUN.")
    print("  Barcelona's metro spans TWO operators - TMB (L1-L5, L9-L11, FM)")
    print("  and FGC (L6-L8, L12, FV) - and no per-line published table has")
    print("  been obtained from either. Recorded as a gap, not filled in.")

    st_out = kept.drop(columns="geometry").rename(columns={"name": "station"})
    verify_stations(
        city="Barcelona",
        platforms=platforms,
        stations=st_out,
        crs_projected=CRS_PROJECTED,
    )

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    (st_out.sort_values("station")[["station", "latitude", "longitude"]]
     .to_csv(STATIONS_CSV, index=False))
    print(f"\nWrote {len(st_out)} stations to {STATIONS_CSV}")


if __name__ == "__main__":
    main()
