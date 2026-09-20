"""Step 1 - CTA 'L' station coordinates, filtered to stations actually within
the City of Chicago.

Input:  data/chicago/raw/gtfs.zip                 (CTA GTFS feed)
        data/chicago/raw/city_boundary.geojson    (City of Chicago boundary)
Output: data/chicago/processed/stations.csv
        outputs/chicago/excluded_stations.csv     (audit record)

The 'L' runs out of the city (Evanston, Skokie, Oak Park, Forest Park,
Cicero, Rosemont, ...), so "every L station" is not "every L station in
Chicago". Every excluded station is written to excluded_stations.csv. The
boundary layer holds Chicago only, so an excluded station is labelled as
outside city limits rather than with the suburb it is in.

A station is a GTFS parent station (location_type 1): the feed's platforms
(one per direction) each point to one. CTA gives the Red and Blue lines
separate parent stations at the same downtown street (Jackson, Monroe), a few
hundred feet apart; they are kept as CTA counts them (see config.py).

Stations are uniformly sparse inside the city (no street-running offshoots),
so every in-city station is kept; the sub-transit-line filters are not needed.

Run:  python pipeline/chicago/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.chicago.config import (  # noqa: E402
    GTFS_ZIP,
    CITY_BOUNDARY_GEOJSON,
    STATIONS_CSV,
    EXCLUDED_STATIONS_CSV,
    CTA_RAIL_ROUTE_IDS,
    CTA_LINE_NAMES,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
)


def load_gtfs_table(zip_path, filename, **kwargs):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(filename) as f:
            return pd.read_csv(f, dtype=str, **kwargs)


def main():
    if not GTFS_ZIP.exists():
        sys.exit(
            f"No GTFS feed at {GTFS_ZIP}.\n"
            "Download it from https://www.transitchicago.com/downloads/sch_data/google_transit.zip"
        )
    if not CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"No boundary file at {CITY_BOUNDARY_GEOJSON}; see config.py for how to download it.")

    routes = load_gtfs_table(GTFS_ZIP, "routes.txt")
    rail = routes[routes["route_type"] == "1"]
    print("Rail routes in this feed:")
    print(rail[["route_id", "route_long_name", "route_type"]].to_string(index=False))
    matched = rail[rail["route_id"].isin(CTA_RAIL_ROUTE_IDS)]
    missing = set(CTA_RAIL_ROUTE_IDS) - set(matched["route_id"])
    if missing:
        print(f"WARNING: expected CTA route_ids not found in this feed: {missing}")
    left_out = sorted(set(rail["route_id"]) - set(CTA_RAIL_ROUTE_IDS))
    print(f"Left out on purpose: {left_out} (see config.py)")

    trips = load_gtfs_table(GTFS_ZIP, "trips.txt")
    stop_times = load_gtfs_table(GTFS_ZIP, "stop_times.txt", usecols=["trip_id", "stop_id"])
    stops = load_gtfs_table(GTFS_ZIP, "stops.txt")

    # Every (line, platform stop) pair actually served by a trip.
    served = (
        trips[trips["route_id"].isin(matched["route_id"])][["trip_id", "route_id"]]
        .merge(stop_times, on="trip_id")
        .drop_duplicates(["route_id", "stop_id"])
        .merge(stops[["stop_id", "parent_station"]], on="stop_id")
    )
    served["line"] = served["route_id"].map(CTA_LINE_NAMES)
    parents = stops[stops["location_type"] == "1"].set_index("stop_id")

    lines_by_parent = served.groupby("parent_station")["line"].apply(lambda s: " / ".join(sorted(set(s))))
    stations = pd.DataFrame({
        "station": parents.loc[lines_by_parent.index, "stop_name"].values,
        "latitude": parents.loc[lines_by_parent.index, "stop_lat"].astype(float).values,
        "longitude": parents.loc[lines_by_parent.index, "stop_lon"].astype(float).values,
        "lines": lines_by_parent.values,
    })
    print(f"\n{len(stations)} distinct CTA 'L' stations (parent stations) across all cities.")

    # --- Spatial filter to the City of Chicago -------------------------------
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None else boundary.to_crs(CRS_GEOGRAPHIC)
    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC,
    )
    inside = stations_gdf.geometry.within(boundary.geometry.union_all())
    in_city = stations[inside.values].sort_values("station").reset_index(drop=True)
    excluded = stations[~inside.values].sort_values("station").reset_index(drop=True)
    excluded["located_in"] = "Outside Chicago city limits"

    print(f"{len(in_city)} of {len(stations)} stations fall within the City of Chicago.")
    print(f"Excluded ({len(excluded)}, suburban): {excluded['station'].tolist()}")

    # Spacing, for the record: distance to the nearest other kept station.
    xy = gpd.GeoSeries(gpd.points_from_xy(in_city["longitude"], in_city["latitude"]), crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    pts = np.column_stack([xy.x, xy.y])
    dist = np.sqrt(((pts[:, None] - pts[None]) ** 2).sum(-1))
    np.fill_diagonal(dist, np.inf)
    nearest = dist.min(axis=1)
    print(f"Nearest-neighbour distance among kept stations: median {np.median(nearest):.0f} m, "
          f"10th percentile {np.percentile(nearest, 10):.0f} m, minimum {nearest.min():.0f} m "
          f"({(nearest < 250).sum()} stations within 250 m of another).")

    print("\nKept stations per line:")
    for line in CTA_LINE_NAMES.values():
        print(f"  {line}: {in_city['lines'].str.contains(line).sum()}")

    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded.to_csv(EXCLUDED_STATIONS_CSV, index=False)
    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    in_city.to_csv(STATIONS_CSV, index=False)
    print(f"\nWrote {STATIONS_CSV}\nWrote {EXCLUDED_STATIONS_CSV}")


if __name__ == "__main__":
    main()
