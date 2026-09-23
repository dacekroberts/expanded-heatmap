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
    analogue here is the railway=station whitelist below. The gate is not
    allowed to pass silently on a source that cannot answer it.
  * The operator's published count - gate 3 - is UNAVAILABLE, because the
    operator is the unreachable host. config.STATION_COUNT_GATE_3 is None and
    says why. This is disclosed on the city page.
  * OSM mixes PROPOSED infrastructure in with built, and misspells it. See
    OSM_EXCLUDE_RAILWAY.
"""

import json
import sys

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, shape
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent.parent))

from pipeline.stations import verify_stations
from pipeline.mexico_city.config import (
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    LINE_NAMES,
    OSM_BOUNDARY_JSON,
    OSM_EXCLUDE_RAILWAY,
    OSM_RAILWAY_KEEP,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OSM_STATION_NETWORKS,
    STATIONS_CSV,
    STATION_COUNT_GATE_3,
    STATION_COUNT_GATE_3_REASON,
)

# CDMX is 1,495 km2. A boundary that assembles wrong - the usual failure is a
# ring that does not close, leaving a sliver or the whole bbox - shows up here
# rather than as zero stations kept later. Surrey's boundary declared the wrong
# CRS and put every containment test at zero; Vancouver's was a MultiLineString
# that matched nothing. An area gate catches both shapes of that error.
BOUNDARY_AREA_KM2_MIN = 1_300.0
BOUNDARY_AREA_KM2_MAX = 1_700.0


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


def main():
    print("=== Step 1: Mexico City stations (OpenStreetMap) ===\n")

    print("Reading cached OSM:")
    st_data = read_cached(OSM_STATIONS_JSON, "stations")
    rt_data = read_cached(OSM_ROUTES_JSON, "routes")
    boundary = load_boundary()

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

    # --- COLLAPSE BY NAME, the fourth mechanism this project has met -------
    # OSM has one node per line at an interchange. Averaging the coordinates of
    # same-named nodes is right here and would be wrong in a feed with
    # platform-level nodes spread down a street; these are the same station box
    # entered from different lines, tens of metres apart at most.
    grouped = (platforms.groupby("name", as_index=False)
               .agg(latitude=("latitude", "mean"),
                    longitude=("longitude", "mean"),
                    nodes=("name", "size"),
                    networks=("network", lambda s: "; ".join(sorted(
                        {x for x in s if x})))))
    print(f"\nCollapsed {len(platforms):,} nodes -> {len(grouped):,} stations "
          f"by name")
    multi = grouped[grouped["nodes"] > 1]
    print(f"  names with more than one node (interchanges): {len(multi)}")
    for _, r in multi.sort_values("nodes", ascending=False).head(6).iterrows():
        print(f"      {r['name']:28s} {r['nodes']} nodes   {r['networks']}")

    # --- boundary filter --------------------------------------------------
    gdf = gpd.GeoDataFrame(
        grouped,
        geometry=gpd.points_from_xy(grouped["longitude"], grouped["latitude"]),
        crs=CRS_GEOGRAPHIC,
    )
    inside = gdf.within(boundary)
    kept = gdf[inside].drop(columns="geometry").copy()
    outside = gdf[~inside].copy()
    print(f"\nInside Ciudad de México: {len(kept):,}")
    print(f"Outside (Estado de México - Lines A and B): {len(outside):,}")

    if len(outside):
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
    rels = [e for e in rt_data["elements"] if e["type"] == "relation"]
    refs = sorted({r["tags"].get("ref") for r in rels if r["tags"].get("ref")})
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
