"""Step 1 - San Diego MTS Trolley station coordinates, filtered to stations
actually within San Diego city limits.

Input:  data/san_diego/raw/gtfs.zip                  (MTS GTFS feed)
        data/san_diego/raw/municipal_boundaries.geojson  (SANDAG regional
                                                           municipal boundaries)
Output: data/san_diego/processed/stations.csv

The Trolley (Blue/Orange/Green/Copper/Silver lines) runs through several
cities besides San Diego - El Cajon, La Mesa, Lemon Grove, Santee, National
City, Chula Vista - so "every Trolley stop" is not the same set as "every
Trolley stop in San Diego." This filters spatially against a real
city-boundary polygon rather than a hand-curated name list, since San
Diego's Trolley network is large enough, and its city border irregular
enough (Palm Avenue and Beyer Blvd are in San Diego near San Ysidro; 24th
Street and 8th Street look adjacent on the line but are actually in
National City), that eyeballing it risks getting individual stations
wrong.

Run:  python pipeline/san_diego/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.san_diego.config import (  # noqa: E402
    GTFS_ZIP,
    MUNICIPAL_BOUNDARIES_GEOJSON,
    STATIONS_CSV,
    TROLLEY_ROUTE_SHORT_NAMES,
    GTFS_NAME_ALIASES,
    CITY_BOUNDARY_NAME,
    CRS_GEOGRAPHIC,
)


def load_gtfs_table(zip_path, filename):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(filename) as f:
            return pd.read_csv(f, dtype=str)


def main():
    if not GTFS_ZIP.exists():
        sys.exit(
            f"No GTFS feed at {GTFS_ZIP}.\n"
            "Download it from https://www.sdmts.com/google_transit_files/google_transit.zip"
        )
    if not MUNICIPAL_BOUNDARIES_GEOJSON.exists():
        sys.exit(
            f"No boundary file at {MUNICIPAL_BOUNDARIES_GEOJSON}.\n"
            "Download it from "
            "https://geo.sandag.org/server/rest/directories/downloads/Municipal_Boundaries.geojson"
        )

    routes = load_gtfs_table(GTFS_ZIP, "routes.txt")

    # route_type "0" is tram/light rail in the GTFS spec - the Trolley
    # lines. Matched by route_short_name against a known list rather than
    # route_type alone, so a future feed update that adds some other
    # route_type-0 service (a streetcar pilot, say) doesn't silently get
    # swept in without a deliberate decision to include it.
    trolley_routes = routes[
        (routes["route_type"] == "0")
        & (routes["route_short_name"].isin(TROLLEY_ROUTE_SHORT_NAMES))
    ]
    print(f"Matched route_ids: {list(trolley_routes['route_id'])}\n")
    missing = set(TROLLEY_ROUTE_SHORT_NAMES) - set(trolley_routes["route_short_name"])
    if missing:
        print(f"WARNING: expected Trolley lines not found in this feed: {missing}")

    trips = load_gtfs_table(GTFS_ZIP, "trips.txt")
    stop_times = load_gtfs_table(GTFS_ZIP, "stop_times.txt")
    stops = load_gtfs_table(GTFS_ZIP, "stops.txt")

    trolley_trips = trips[trips["route_id"].isin(trolley_routes["route_id"])]
    trolley_stop_ids = stop_times[
        stop_times["trip_id"].isin(trolley_trips["trip_id"])
    ]["stop_id"].unique()

    trolley_stops = stops[stops["stop_id"].isin(trolley_stop_ids)].copy()
    trolley_stops["stop_lat"] = trolley_stops["stop_lat"].astype(float)
    trolley_stops["stop_lon"] = trolley_stops["stop_lon"].astype(float)
    trolley_stops["stop_name"] = trolley_stops["stop_name"].replace(GTFS_NAME_ALIASES)

    print(f"Found {trolley_stops['stop_name'].nunique()} distinct Trolley stop names "
          f"(all cities, before platform collapse):")
    print(sorted(trolley_stops["stop_name"].unique()))
    print()

    # Platforms sharing a name collapse to one row per station by
    # averaging.
    stations = (
        trolley_stops.groupby("stop_name", as_index=False)
        .agg(latitude=("stop_lat", "mean"), longitude=("stop_lon", "mean"))
        .rename(columns={"stop_name": "station"})
    )

    # --- Spatial filter to San Diego city limits ---------------------------
    boundary = gpd.read_file(MUNICIPAL_BOUNDARIES_GEOJSON)
    sd_boundary = boundary[boundary["Name"] == CITY_BOUNDARY_NAME].dissolve()
    if sd_boundary.crs is None:
        sd_boundary = sd_boundary.set_crs(CRS_GEOGRAPHIC)
    else:
        sd_boundary = sd_boundary.to_crs(CRS_GEOGRAPHIC)

    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC,
    )
    joined = gpd.sjoin(stations_gdf, sd_boundary[["geometry"]], predicate="within", how="left")
    in_city = joined[~joined["index_right"].isna()].drop(columns=["geometry", "index_right"])
    out_city = joined[joined["index_right"].isna()]

    print(f"\n{len(in_city)} of {len(stations)} Trolley stations fall within "
          f"{CITY_BOUNDARY_NAME} city limits.")
    print(f"Excluded (other cities the Trolley also serves): "
          f"{sorted(out_city['station'].tolist())}")

    in_city = in_city.sort_values("station").reset_index(drop=True)
    print(f"\nKept stations:\n{in_city.to_string(index=False)}")

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    in_city.to_csv(STATIONS_CSV, index=False)
    print(f"\nWrote {STATIONS_CSV}")


if __name__ == "__main__":
    main()
