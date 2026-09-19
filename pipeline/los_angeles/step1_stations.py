"""Step 1 - LA Metro Rail station coordinates, filtered to stations actually
within the City of Los Angeles.

Input:  data/los_angeles/raw/gtfs_rail.zip                      (Metro rail GTFS)
        data/los_angeles/raw/la_county_incorporated_cities.geojson
Output: data/los_angeles/processed/stations.csv
        outputs/los_angeles/excluded_stations.csv   (audit record)

Metro Rail (A, B, C, D, E, K Lines) runs through 23 other cities and
unincorporated areas besides Los Angeles (Long Beach, Pasadena, Santa
Monica, Inglewood, ... ), so "every Metro station" is not "every Metro
station in LA": of 110 stations, 54 lie outside the city. That is a
scoping decision rather than a config detail - covering them would need
those cities' own business data, sourced and verified separately - so every
excluded station is written to excluded_stations.csv with the city it is in.

Stations inside the city are spaced fairly evenly (median ~0.55 mi), unlike
San Francisco's street-running Muni Metro, so every one is kept; the
sub-transit-line filters are not needed.

Run:  python pipeline/los_angeles/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.los_angeles.config import (  # noqa: E402
    GTFS_ZIP,
    CITIES_BOUNDARY_GEOJSON,
    STATIONS_CSV,
    EXCLUDED_STATIONS_CSV,
    LA_METRO_ROUTE_IDS,
    LA_METRO_LINE_NAMES,
    GTFS_NAME_ALIASES,
    CITY_BOUNDARY_FIELD,
    CITY_BOUNDARY_NAME,
    CRS_GEOGRAPHIC,
)


def load_gtfs_table(zip_path, filename, **kwargs):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(filename) as f:
            return pd.read_csv(f, dtype=str, **kwargs)


def main():
    if not GTFS_ZIP.exists():
        sys.exit(
            f"No GTFS feed at {GTFS_ZIP}.\n"
            "Download it from https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip"
        )
    if not CITIES_BOUNDARY_GEOJSON.exists():
        sys.exit(f"No boundary file at {CITIES_BOUNDARY_GEOJSON}; see config.py for how to download it.")

    routes = load_gtfs_table(GTFS_ZIP, "routes.txt")
    print("Routes in this feed:")
    print(routes[["route_id", "route_long_name", "route_type"]].to_string(index=False))
    matched = routes[routes["route_id"].isin(LA_METRO_ROUTE_IDS)]
    missing = set(LA_METRO_ROUTE_IDS) - set(matched["route_id"])
    if missing:
        print(f"WARNING: expected LA Metro route_ids not found in this feed: {missing}")

    trips = load_gtfs_table(GTFS_ZIP, "trips.txt")
    stop_times = load_gtfs_table(GTFS_ZIP, "stop_times.txt", usecols=["trip_id", "stop_id"])
    stops = load_gtfs_table(GTFS_ZIP, "stops.txt")

    # Every (line, platform stop) pair actually served by a trip - the feed
    # also lists parent stations and entrances, which no trip calls at.
    served = (
        trips[trips["route_id"].isin(matched["route_id"])][["trip_id", "route_id"]]
        .merge(stop_times, on="trip_id")
        .drop_duplicates(["route_id", "stop_id"])
        .merge(stops, on="stop_id")
    )
    served["latitude"] = served["stop_lat"].astype(float)
    served["longitude"] = served["stop_lon"].astype(float)
    served["station"] = served["stop_name"].replace(GTFS_NAME_ALIASES)
    served["line"] = served["route_id"].map(LA_METRO_LINE_NAMES)

    # One row per physical station: average platform positions, and record
    # which lines call there.
    stations = (
        served.groupby("station", as_index=False)
        .agg(
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
            lines=("line", lambda s: " / ".join(sorted(set(s)))),
        )
    )
    print(f"\n{len(stations)} distinct Metro Rail stations across all cities "
          f"(after collapsing {len(GTFS_NAME_ALIASES)} per-line complex names).")

    # --- Spatial filter to the City of Los Angeles -------------------------
    cities = gpd.read_file(CITIES_BOUNDARY_GEOJSON)
    cities = cities.set_crs(CRS_GEOGRAPHIC) if cities.crs is None else cities.to_crs(CRS_GEOGRAPHIC)
    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC,
    )
    # Which city is each station in? (one join, used both to keep LA and to
    # label the excluded ones.)
    located = gpd.sjoin(
        stations_gdf, cities[[CITY_BOUNDARY_FIELD, "geometry"]], predicate="within", how="left"
    ).drop(columns=["index_right", "geometry"])
    located["city"] = located[CITY_BOUNDARY_FIELD].fillna("(unincorporated area)")
    located = located.drop(columns=[CITY_BOUNDARY_FIELD])

    in_city = located[located["city"] == CITY_BOUNDARY_NAME].drop(columns=["city"])
    excluded = located[located["city"] != CITY_BOUNDARY_NAME].sort_values(["city", "station"])

    print(f"{len(in_city)} of {len(stations)} stations fall within {CITY_BOUNDARY_NAME.title()}.")
    print("Excluded, by the city they are in:")
    print(excluded["city"].value_counts().to_string())

    in_city = in_city.sort_values("station").reset_index(drop=True)
    print(f"\nKept stations:\n{in_city.to_string(index=False)}")

    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded.rename(columns={"city": "located_in"}).to_csv(EXCLUDED_STATIONS_CSV, index=False)
    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    in_city.to_csv(STATIONS_CSV, index=False)
    print(f"\nWrote {STATIONS_CSV}\nWrote {EXCLUDED_STATIONS_CSV}")


if __name__ == "__main__":
    main()
