"""Dublin step 1: Luas and DART stations, filtered to the four authorities.

Rail comes from the NTA's own GTFS, trimmed to three routes by
fetch_sources.py. OpenStreetMap is kept as a CROSS-CHECK and is not the source
- see config.ROUTES for why that order, and for the Madrid failure it avoids.

Reads the cache and NEVER fetches: a step that downloads turns every drift
check into a question about the current upstream instead of about the
committed code.

    python pipeline/dublin/step1_stations.py
"""
import csv
import io
import json
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, shape

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.baseline import emit
from pipeline.dublin import config
from pipeline.stations import verify_stations


def _read(zf, name):
    with zf.open(name) as fh:
        return list(csv.DictReader(io.TextIOWrapper(fh, "utf-8-sig")))


def load_gtfs():
    if not config.GTFS_ZIP.exists():
        sys.exit(f"missing {config.GTFS_ZIP}.\n"
                 f"Run: python pipeline/dublin/fetch_sources.py")
    with zipfile.ZipFile(config.GTFS_ZIP) as zf:
        return {n: _read(zf, n) for n in
                ("routes.txt", "trips.txt", "stop_times.txt", "stops.txt")}


def dissolved_boundary():
    """One polygon per authority, dissolved from a MULTIPART layer.

    Fingal ships 46 polygons and Dun Laoghaire-Rathdown 42, nearly all islands
    and coastal outcrops under 0.1 km2. Taking the first polygon per authority
    would test stations against Lambay Island.
    """
    if not config.BOUNDARY_GEOJSON.exists():
        sys.exit(f"missing {config.BOUNDARY_GEOJSON}.\n"
                 f"Run: python pipeline/dublin/fetch_sources.py")
    boundary = json.loads(config.BOUNDARY_GEOJSON.read_text(encoding="utf-8"))
    gdf = gpd.GeoDataFrame(
        [{"authority": f["properties"][config.BOUNDARY_NAME_FIELD],
          "geometry": shape(f["geometry"])} for f in boundary["features"]],
        crs=config.CRS_GEOGRAPHIC)
    print(f"Boundary: {len(gdf)} polygon parts across "
          f"{gdf['authority'].nunique()} authorities")
    dissolved = gdf.dissolve(by="authority").reset_index()
    proj = dissolved.to_crs(config.CRS_PROJECTED)
    for name, area in zip(proj["authority"], proj.geometry.area / 1e6):
        print(f"  {name:42s} {area:7.1f} km2")
    print(f"  {'REGION':42s} {proj.geometry.area.sum() / 1e6:7.1f} km2")
    return dissolved


def stops_per_route(gtfs):
    """stop_id -> the drawn routes it serves, via stop_times and trips."""
    trip_route = {t["trip_id"]: t["route_id"] for t in gtfs["trips.txt"]}
    per_route, stop_routes = {}, {}
    for st in gtfs["stop_times.txt"]:
        route = trip_route.get(st["trip_id"])
        if route not in config.ROUTES:
            continue
        per_route.setdefault(route, set()).add(st["stop_id"])
        stop_routes.setdefault(st["stop_id"], set()).add(route)

    print("\nRoutes drawn:")
    for route_id, (label, colour) in config.ROUTES.items():
        ids = per_route.get(route_id, set())
        if not ids:
            sys.exit(f"  {route_id!r} has no stops in the trimmed feed - "
                     f"re-read routes.txt rather than trusting this run.")
        print(f"  {route_id:20s} {label:18s} {colour}  "
              f"{len(ids):3d} stop_ids")
    return per_route, stop_routes


def collapse(gtfs, stop_routes):
    """Directional pairs -> one station per name.

    The NTA feed carries NO `parent_station` on any of these stops (measured:
    0 of 160), so the collapse is by name, which is Calgary's and Guadalajara's
    shape. The paired stops straddle the street, so the collapsed point is
    their mean rather than an arbitrary side.
    """
    rows = [s for s in gtfs["stops.txt"] if s["stop_id"] in stop_routes]
    platforms = pd.DataFrame([
        {"station": s["stop_name"],
         "latitude": float(s["stop_lat"]),
         "longitude": float(s["stop_lon"])} for s in rows])
    stations = (platforms.groupby("station", as_index=False)
                .agg(latitude=("latitude", "mean"),
                     longitude=("longitude", "mean")))
    print(f"\nStops: {len(platforms)} stop_ids -> {len(stations)} stations "
          f"by name")
    return platforms, stations


def osm_cross_check(stations):
    """A second opinion on the station count, per line.

    Madrid's three sources agreed on 13 lines and landed at 243 / 236 / 230
    stations, and the spread is what showed its GTFS feed undercounting. This
    prints rather than raises: a disagreement is a prompt to look, and OSM is
    not the authority here.
    """
    if not config.RAIL_OSM_JSON.exists():
        print("\nOSM cross-check: no cached file, skipped.")
        return
    els = json.loads(config.RAIL_OSM_JSON.read_text(encoding="utf-8"))["elements"]
    rels = {e["id"]: e for e in els if e.get("type") == "relation"}
    nodes = {e["id"]: e for e in els if e.get("type") == "node"}
    print("\nOSM cross-check (not the source - a second opinion):")
    osm_names = set()
    for ref in config.OSM_REFS:
        mine = [r for r in rels.values()
                if (r.get("tags") or {}).get("ref") == ref]
        names = set()
        for r in mine:
            for m in r.get("members", []):
                if m.get("type") != "node":
                    continue
                t = (nodes.get(m["ref"]) or {}).get("tags") or {}
                if t.get("name"):
                    names.add(t["name"])
        osm_names |= names
        print(f"  {ref:18s} OSM {len(names):3d} named stops")
    gtfs_names = set(stations["station"])
    only_gtfs = sorted(gtfs_names - osm_names)
    only_osm = sorted(osm_names - gtfs_names)
    print(f"  GTFS {len(gtfs_names)} names, OSM {len(osm_names)} names, "
          f"{len(gtfs_names & osm_names)} shared")
    if only_gtfs:
        print(f"  in GTFS only ({len(only_gtfs)}): {only_gtfs[:10]}")
    if only_osm:
        print(f"  in OSM only  ({len(only_osm)}): {only_osm[:10]}")
    print("  Name spelling differs between sources, so a name-only diff "
          "overstates disagreement; the counts are the signal.")


def main():
    gtfs = load_gtfs()
    region = dissolved_boundary()
    _per_route, stop_routes = stops_per_route(gtfs)
    platforms, stations = collapse(gtfs, stop_routes)

    # The shared gates. The spacing one RAISES if the collapse left platforms
    # behind, which is what Toronto and Calgary both shipped once.
    verify_stations(city="Dublin", platforms=platforms, stations=stations,
                    crs_projected=config.CRS_PROJECTED)
    osm_cross_check(stations)

    gdf = gpd.GeoDataFrame(
        stations,
        geometry=[Point(xy) for xy in zip(stations.longitude,
                                          stations.latitude)],
        crs=config.CRS_GEOGRAPHIC)
    joined = gpd.sjoin(gdf, region[["authority", "geometry"]],
                       how="left", predicate="within")
    joined = joined[~joined.index.duplicated(keep="first")]

    inside = joined[joined["authority"].notna()].copy()
    outside = joined[joined["authority"].isna()].copy()

    print(f"\nIn the four authorities: {len(inside)} of {len(joined)}")
    for name, n in inside["authority"].value_counts().items():
        print(f"  {name:42s} {n:3d}")
    print(f"\nExcluded (outside the region): {len(outside)}")
    for name in sorted(outside["station"]):
        print(f"  {name}")

    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)

    out = (inside[["station", "latitude", "longitude", "authority"]]
           .sort_values("station").reset_index(drop=True))
    out.to_csv(config.STATIONS_CSV, index=False)
    print(f"\nwrote {config.STATIONS_CSV.name}  {len(out)} stations")

    excl = outside[["station", "latitude", "longitude"]].copy()
    excl["reason"] = "outside the four Dublin local authorities"
    excl.sort_values("station").to_csv(config.EXCLUDED_STATIONS_CSV,
                                       index=False)
    print(f"wrote {config.EXCLUDED_STATIONS_CSV.name}  {len(excl)} stations")

    emit("gtfs_stop_ids", len(platforms))
    emit("stations_collapsed", len(stations))
    emit("stations_in_region", len(out))
    emit("stations_excluded", len(excl))


if __name__ == "__main__":
    main()
