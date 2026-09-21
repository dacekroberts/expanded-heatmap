"""Step 1 - MTA rail station coordinates, filtered to stations within New York
City.

Input:  data/new_york/raw/gtfs.zip                 (MTA subway + SIR feed)
        data/new_york/raw/city_boundary.geojson    (the five borough polygons)
Output: data/new_york/processed/stations.csv
        outputs/new_york/excluded_stations.csv     (audit record)

A station is a GTFS parent station (location_type 1); the feed's platforms
(one per direction, suffixed N/S) each point to one. MTA gives some complexes
several parent stations a few hundred feet apart (Times Sq-42 St, and the
stations linked in transfers.txt); they are kept as MTA counts them, the same
choice Chicago's step 1 makes. Rings from two parents in one complex overlap,
but the map assigns each business to its single nearest station, so nothing is
double-counted.

Every NYC subway station is a full station - there are no street-running
offshoots as in San Francisco's Muni Metro - so every in-city station is kept
and the sub-transit-line filters do not apply. What New York needs instead is
a smaller ring, because the stations are so close together: see
RING_EDGES_MILES in config.py.

The `lines` column names the TRUNK each station is on, not the services. The
feed's 29 routes are service patterns over ~11 physical lines (the 4, 5, 6 and
6X all run on Lexington Avenue); config.ROUTE_TO_TRUNK groups them the way the
MTA's own route_color does. See config.py for why.

Run:  python pipeline/new_york/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.new_york.config import (  # noqa: E402
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_URL,
    GTFS_ZIP,
    LINE_NAMES,
    ROUTE_IDS,
    ROUTE_TO_TRUNK,
    RING_EDGES_MILES,
    METERS_PER_MILE,
    STATIONS_CSV,
)


def load_gtfs_table(zip_path, filename, **kwargs):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(filename) as f:
            return pd.read_csv(f, dtype=str, **kwargs)


def main():
    if not GTFS_ZIP.exists():
        sys.exit(f"No GTFS feed at {GTFS_ZIP}.\nDownload it from {GTFS_URL}\n"
                 "(or run: python pipeline/new_york/fetch_sources.py)")
    if not CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"No boundary file at {CITY_BOUNDARY_GEOJSON}; see config.py "
                 "for how to download it.")

    routes = load_gtfs_table(GTFS_ZIP, "routes.txt")
    print("Routes in this feed:")
    print(routes[["route_id", "route_short_name", "route_type", "route_color"]]
          .to_string(index=False))

    matched = routes[routes["route_id"].isin(ROUTE_IDS)]
    missing = set(ROUTE_IDS) - set(matched["route_id"])
    if missing:
        print(f"WARNING: expected route_ids not found in this feed: {sorted(missing)}")
    left_out = sorted(set(routes["route_id"]) - set(ROUTE_IDS))
    print(f"Left out on purpose: {left_out or 'nothing'} (see config.py)")

    # Every route must map to a trunk, or a station would silently lose a line.
    unmapped = sorted(set(matched["route_id"]) - set(ROUTE_TO_TRUNK))
    if unmapped:
        sys.exit(f"route_ids with no trunk in ROUTE_TO_TRUNK: {unmapped}")

    # Cross-check the trunk grouping against the feed's own colours: a trunk
    # whose services do not share one route_color means the feed regrouped and
    # config.py needs re-checking (the two deliberate departures are the L and
    # the shuttles, which share MTA's grey - see config.py).
    colors = matched.set_index("route_id")["route_color"]
    for trunk in sorted(set(ROUTE_TO_TRUNK.values())):
        members = [r for r, t in ROUTE_TO_TRUNK.items() if t == trunk and r in colors.index]
        distinct = sorted({colors[r] for r in members})
        if len(distinct) > 1:
            print(f"NOTE: trunk {trunk!r} spans route_colors {distinct} "
                  f"(routes {members})")

    trips = load_gtfs_table(GTFS_ZIP, "trips.txt")
    stop_times = load_gtfs_table(GTFS_ZIP, "stop_times.txt", usecols=["trip_id", "stop_id"])
    stops = load_gtfs_table(GTFS_ZIP, "stops.txt")

    # Every (trunk, platform stop) pair actually served by a trip.
    served = (
        trips[trips["route_id"].isin(matched["route_id"])][["trip_id", "route_id"]]
        .merge(stop_times, on="trip_id")
        .drop_duplicates(["route_id", "stop_id"])
        .merge(stops[["stop_id", "parent_station"]], on="stop_id")
    )
    served["trunk"] = served["route_id"].map(ROUTE_TO_TRUNK)
    served["line"] = served["trunk"].map(lambda t: LINE_NAMES[t][0])

    parents = stops[stops["location_type"] == "1"].set_index("stop_id")
    lines_by_parent = (
        served.groupby("parent_station")["line"]
        .apply(lambda s: " / ".join(sorted(set(s))))
    )
    stations = pd.DataFrame({
        "station": parents.loc[lines_by_parent.index, "stop_name"].values,
        "latitude": parents.loc[lines_by_parent.index, "stop_lat"].astype(float).values,
        "longitude": parents.loc[lines_by_parent.index, "stop_lon"].astype(float).values,
        "lines": lines_by_parent.values,
    })
    print(f"\n{len(stations)} distinct MTA rail stations (parent stations) in the feed.")

    # --- Spatial filter to New York City ------------------------------------
    # The subway is wholly within the city, so this is expected to exclude
    # nothing; it runs anyway, because "expected" is not "verified" and a feed
    # change would otherwise pass silently (add-city Step 0).
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = (boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None
                else boundary.to_crs(CRS_GEOGRAPHIC))
    city = boundary.geometry.union_all()
    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC,
    )
    inside = stations_gdf.geometry.within(city).values
    in_city = stations[inside].sort_values("station").reset_index(drop=True)
    excluded = stations[~inside].sort_values("station").reset_index(drop=True)
    excluded["located_in"] = "Outside New York City limits"

    print(f"{len(in_city)} of {len(stations)} stations fall within New York City.")
    if len(excluded):
        print(f"Excluded ({len(excluded)}): {excluded['station'].tolist()}")
    else:
        print("Excluded (0): none - the whole network is inside the city, as expected.")

    # Spacing, for the record: distance to the nearest other kept station.
    # This is the measurement behind the smaller ring edges (config.py).
    xy = gpd.GeoSeries(
        gpd.points_from_xy(in_city["longitude"], in_city["latitude"]),
        crs=CRS_GEOGRAPHIC,
    ).to_crs(CRS_PROJECTED)
    pts = np.column_stack([xy.x, xy.y])
    dist = np.sqrt(((pts[:, None] - pts[None]) ** 2).sum(-1))
    np.fill_diagonal(dist, np.inf)
    nearest = dist.min(axis=1)
    outer_m = RING_EDGES_MILES[-1] * METERS_PER_MILE
    print(f"Nearest-neighbour distance among kept stations: median {np.median(nearest):.0f} m, "
          f"10th percentile {np.percentile(nearest, 10):.0f} m, minimum {nearest.min():.0f} m "
          f"({(nearest < 250).sum()} stations within 250 m of another).")
    print(f"Stations closer together than the {RING_EDGES_MILES[-1]} mi outer ring "
          f"({outer_m:.0f} m): {(nearest < outer_m).sum()} of {len(in_city)} - "
          "their rings overlap, and each business is assigned to its nearest "
          "station only.")

    print("\nKept stations per trunk:")
    for trunk, (label, _color) in LINE_NAMES.items():
        n = in_city["lines"].str.contains(label, regex=False).sum()
        print(f"  {label}: {n}")

    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded.to_csv(EXCLUDED_STATIONS_CSV, index=False)
    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    in_city.to_csv(STATIONS_CSV, index=False)
    print(f"\nWrote {STATIONS_CSV}\nWrote {EXCLUDED_STATIONS_CSV}")


if __name__ == "__main__":
    main()
