"""Step 1 - Monterrey (Regional)'s Metrorrey stations, from OpenStreetMap.

Mexico's third city and its third station object. Mexico City's stations are
`railway=station` nodes and Guadalajara's are `railway=stop` pairs; here the
route relations list 37 `railway=station` nodes and 5 `railway=stop` positions
(Cuauhtémoc and General Anaya exist only as stops). So both types are accepted,
and only as MEMBERS of a Metrorrey route relation - never by tag, because 11
unbuilt Línea 4/6 monorail stations are already tagged `railway=station`.

Why not GTFS: Nuevo León publishes no Metrorrey data at all. See config.py.

Gate 3 runs in full: the operator's 2026-05-08 map names 19 / 13 / 9.
"""

import json
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.stations import verify_stations
from pipeline.monterrey.config import (
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DENUE_STATE_CODE,
    EXCLUDED_STATIONS_CSV,
    LINE_NAMES,
    MUNICIPIOS,
    MUNIDS,
    OSM_BOUNDARY_JSON,
    OSM_CONSTRUCTION_TAGS,
    OSM_ROUTES_JSON,
    OSM_STATIONS_JSON,
    OSM_STATION_RAILWAY,
    PUBLIC_NAME_FIXES,
    PUBLISHED_STATIONS_PER_LINE,
    STATIONS_CSV,
    STATION_MUNICIPIOS_CSV,
)

# The four municipios measured 650.7 km2 together in EPSG:32614 at the screen.
# A band wide enough for OSM edits, narrow enough to catch a ring that did not
# close or a municipio that went missing.
BOUNDARY_AREA_KM2_MIN = 550.0
BOUNDARY_AREA_KM2_MAX = 800.0


def read_cached(path, label):
    """Read a raw input fetch_sources.py downloaded. This step never fetches."""
    if not path.exists():
        raise SystemExit(f"Missing {path.name} ({label}). "
                         "Run pipeline/monterrey/fetch_sources.py first.")
    print(f"  {label}: {path.name} ({path.stat().st_size:,} bytes)")
    return json.loads(path.read_text(encoding="utf-8"))


def fold(name):
    """The collapse key: accents and case removed. OSM spells one station
    "Félix U. Gomez" on Línea 1 and "Félix U. Gómez" on Línea 3; without this
    the collapse finds 39 stations, not 38."""
    nfkd = unicodedata.normalize("NFKD", name)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).casefold().strip()


def display_name(variants):
    """Of a station's spellings, the one carrying the most accents - OSM's
    unaccented variants are the errors here, never the reverse - then the
    operator's spelling where OSM's is wrong outright."""
    best = max(sorted(variants), key=lambda v: sum(ord(c) > 127 for c in v))
    return PUBLIC_NAME_FIXES.get(best, best)


def _poly(rel):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer" and m.get("geometry")]
    if not lines:
        return None
    polys = list(polygonize(linemerge(MultiLineString(lines))))
    return unary_union(polys) if polys else None


def load_boundaries():
    """One polygon per municipio, keyed by INEGI code, plus their union.
    Step 2 (the storefronts' location test) and step 3 (label anchoring) read
    this too, so all three steps agree on where the region is."""
    data = read_cached(OSM_BOUNDARY_JSON, "boundaries")
    by_code = {}
    for rel in (e for e in data["elements"] if e["type"] == "relation"):
        munid = rel["tags"].get("INEGI:MUNID")
        if munid not in MUNIDS:
            continue
        if munid in by_code:
            raise SystemExit(f"Two boundary relations carry INEGI:MUNID {munid}. "
                             "Inspect them; never pick by size.")
        geom = _poly(rel)
        if geom is None:
            raise SystemExit(f"INEGI:MUNID {munid} ({rel['tags'].get('name')}) did "
                             "not assemble into a polygon.")
        by_code[munid] = geom
    missing = [m for m in MUNIDS if m not in by_code]
    if missing:
        raise SystemExit(f"No boundary for {missing}. All four are required: a "
                         "missing municipio would silently drop its stations.")
    union = unary_union(list(by_code.values()))
    area = gpd.GeoSeries([union], crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).area.iloc[0] / 1e6
    print(f"  boundaries: {len(by_code)} municipios, union {area:,.1f} km2")
    if not BOUNDARY_AREA_KM2_MIN <= area <= BOUNDARY_AREA_KM2_MAX:
        raise SystemExit(f"union area {area:,.0f} km2 outside "
                         f"{BOUNDARY_AREA_KM2_MIN:,.0f}-{BOUNDARY_AREA_KM2_MAX:,.0f}.")
    by_name = {MUNICIPIOS[k[len(DENUE_STATE_CODE):]]: g for k, g in by_code.items()}
    return by_name, union


def check_routes(rels):
    """Refuse to draw a network that is not the one the owner approved."""
    mono = [r for r in rels if r["tags"].get("route") == "monorail"]
    if mono:
        raise SystemExit(
            f"{len(mono)} Metrorrey MONORAIL route relation(s) now exist "
            f"({[r['tags'].get('ref') for r in mono]}). Línea 4 or 6 may have "
            "opened: check the operator before drawing or excluding it.")
    refs = sorted({r["tags"].get("ref") for r in rels})
    if refs != sorted(LINE_NAMES):
        raise SystemExit(f"route refs {refs} != {sorted(LINE_NAMES)}")
    for ref in refs:
        n = sum(1 for r in rels if r["tags"].get("ref") == ref)
        if n != 2:
            raise SystemExit(f"Línea {ref}: {n} route relations, expected 2 (one "
                             "per direction). A partial Overpass result fails here.")
    print(f"Route relations: {len(rels)} over refs {', '.join(refs)}; no monorail relation")


def main():
    print("=== Step 1: Monterrey (Regional) stations (OpenStreetMap) ===\n")
    print("Reading cached OSM:")
    st_data = read_cached(OSM_STATIONS_JSON, "stations")
    rt_data = read_cached(OSM_ROUTES_JSON, "routes")
    by_muni, boundary = load_boundaries()

    rels = [e for e in rt_data["elements"] if e["type"] == "relation"]
    check_routes(rels)

    nodes = {e["id"]: e for e in st_data["elements"] if e["type"] == "node"}
    print(f"\nRoute-member nodes: {len(nodes)}")
    building = [(i, e["tags"].get("name")) for i, e in nodes.items()
                if any(e.get("tags", {}).get(k) for k in OSM_CONSTRUCTION_TAGS)
                or e.get("tags", {}).get("railway") == "construction"]
    if building:
        raise SystemExit(f"Route members tagged as under construction: {building}. "
                         "Línea 4 or 6 may be joining a route: check before drawing.")

    rows = []
    for i, e in nodes.items():
        t = e.get("tags", {})
        rows.append({"id": i, "name": (t.get("name") or "").strip(),
                     "railway": t.get("railway"),
                     "latitude": e["lat"], "longitude": e["lon"]})
    members = pd.DataFrame(rows)
    print("  by railway tag:", members["railway"].value_counts(dropna=False).to_dict())
    platforms = members[members["railway"].isin(OSM_STATION_RAILWAY)
                        & (members["name"] != "")].copy()
    dropped = len(members) - len(platforms)
    if dropped:
        print(f"  NOT stations (other tags or unnamed): {dropped}")
    print(f"  stations and stops with a name: {len(platforms)}")

    # --- collapse by accent-folded name --------------------------------------
    platforms["key"] = platforms["name"].map(fold)
    grouped = (platforms.groupby("key")
               .agg(latitude=("latitude", "mean"), longitude=("longitude", "mean"),
                    nodes=("name", "size"), variants=("name", lambda s: sorted(set(s))))
               .reset_index())
    grouped["name"] = grouped["variants"].map(display_name)
    folded = grouped[grouped["variants"].map(len) > 1]
    for _, r in folded.iterrows():
        print(f"  accent-fold merged {r['variants']} -> {r['name']!r}")
    for bad, good in PUBLIC_NAME_FIXES.items():
        if bad in set(platforms["name"]):
            print(f"  public name fixed: {bad!r} -> {good!r}")
    platforms["name"] = platforms["key"].map(dict(zip(grouped["key"], grouped["name"])))
    print(f"\nCollapsed {len(platforms)} member nodes -> {len(grouped)} stations by name")
    print(f"  nodes-per-name: {grouped['nodes'].value_counts().to_dict()}")

    # --- boundary filter, and which municipio each station is in -------------
    gdf = gpd.GeoDataFrame(grouped, geometry=gpd.points_from_xy(grouped["longitude"],
                                                                grouped["latitude"]),
                           crs=CRS_GEOGRAPHIC)
    inside = gdf.within(boundary)
    kept, outside = gdf[inside].copy(), gdf[~inside].copy()
    print(f"\nInside the four municipios: {len(kept)}   outside: {len(outside)}")
    kept["municipio"] = [next((n for n, g in by_muni.items() if p.within(g)), "(edge)")
                         for p in kept.geometry]
    print("Stations per municipio (the regional-build record):")
    for m, n in kept["municipio"].value_counts().items():
        print(f"    {m:26s} {n:3d}")
    STATION_MUNICIPIOS_CSV.parent.mkdir(parents=True, exist_ok=True)
    (kept.drop(columns="geometry").rename(columns={"name": "station"})
     [["station", "municipio", "latitude", "longitude"]]
     .sort_values(["municipio", "station"])
     .to_csv(STATION_MUNICIPIOS_CSV, index=False))
    print(f"  wrote {STATION_MUNICIPIOS_CSV.name}")
    if len(outside):
        b_proj = gpd.GeoSeries([boundary], crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).iloc[0]
        dist = outside.to_crs(CRS_PROJECTED).geometry.apply(lambda g: g.distance(b_proj)).round(0)
        (outside.drop(columns="geometry").assign(distance_outside_m=dist.values, lines="Metrorrey")
         .rename(columns={"name": "station"})
         [["station", "latitude", "longitude", "lines", "distance_outside_m"]]
         .sort_values("distance_outside_m", ascending=False)
         .to_csv(EXCLUDED_STATIONS_CSV, index=False))
        print(f"  wrote {EXCLUDED_STATIONS_CSV.name} ({len(outside)} excluded)")

    # --- gate 3, in full -------------------------------------------------------
    print("\n--- station verification ---")
    actual = {}
    for ref, line in LINE_NAMES.items():
        mine = [r for r in rels if r["tags"].get("ref") == ref]
        best = max(mine, key=lambda x: sum(1 for m in x["members"]
                                           if str(m.get("role", "")).startswith("stop")))
        actual[line] = sum(1 for m in best["members"]
                           if str(m.get("role", "")).startswith("stop"))
    print(f"OSM stop-members per line : {actual}")
    print(f"Operator's published count: {PUBLISHED_STATIONS_PER_LINE}")

    st_out = kept.drop(columns="geometry").rename(columns={"name": "station"})
    verify_stations(
        city="Monterrey (Regional)",
        platforms=platforms[["name", "latitude", "longitude"]],
        stations=st_out,
        crs_projected=CRS_PROJECTED,
        expected_per_line=PUBLISHED_STATIONS_PER_LINE,
        actual_per_line=actual,
    )

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    (st_out.sort_values("station")[["station", "latitude", "longitude"]]
     .to_csv(STATIONS_CSV, index=False))
    print(f"\nWrote {len(st_out)} stations to {STATIONS_CSV}")


if __name__ == "__main__":
    main()
