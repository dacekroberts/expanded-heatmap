"""Step 1 - Philadelphia SEPTA Metro station selection.

Input:  data/philadelphia/raw/gtfs.zip              (SEPTA's google_bus feed)
        data/philadelphia/raw/city_boundary.geojson (OpenDataPhilly City Limits)
Output: data/philadelphia/processed/stations.csv
        outputs/philadelphia/excluded_stations.csv

SEPTA Metro is TWO shapes of system at once, so this step applies two
different rules rather than one:

  L (Market-Frankford) and B (Broad Street + Ridge Spur) are grade-separated
  with stations a median 711 m and 681 m apart - sparse and meaningful, so
  every in-city station is kept, exactly like San Diego's Trolley.

  T (the five subway-surface trolley branches) and G (Girard Avenue) are
  street-running with stops a median 134-137 m apart, a 10th percentile of
  17-19 m. That is San Francisco's Muni Metro shape, so they get the
  four-filter thinning in docs/sub_transit_line_filters.md - without it 261
  trolley stops would swamp 47 real stations and every ring would overlap its
  neighbours, making "distance from a station" meaningless.

Routes M1 (Norristown High Speed Line) and D1/D2 (routes 101/102) are in the
feed but have zero stops inside Philadelphia - both begin at 69th Street in
Upper Darby - so they are not in config.ROUTE_GROUPS at all. Regional Rail is
a separate feed and out of scope (see config.py).

Run:  python pipeline/philadelphia/step1_stations.py
"""

import math
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.philadelphia.config import (  # noqa: E402
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_URL,
    GTFS_ZIP,
    LINE_NAMES,
    ROUTE_GROUPS,
    STATION_NAME_ALIASES,
    STATION_SPACING_MILES,
    STATION_SUFFIX_PATTERN,
    STATIONS_CSV,
    SUBWAY_STATION_NAMES,
    THINNED_GROUPS,
)

SUFFIX_RE = re.compile(STATION_SUFFIX_PATTERN)

# Two distinct names closer together than this are the same physical station
# under inconsistent raw naming - the check San Francisco's build needed, run
# here rather than assumed (docs/sub_transit_line_filters.md).
SAME_STATION_METRES = 60.0


def canonical_name(stop_name: str) -> str:
    stripped = SUFFIX_RE.sub("", stop_name).strip()
    return STATION_NAME_ALIASES.get(stripped, stripped)


def haversine_miles(lat1, lon1, lat2, lon2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def load_gtfs_table(zip_path, filename, usecols=None):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(filename) as f:
            return pd.read_csv(f, dtype=str, usecols=usecols)


def ordered_stop_sequence(route_id, trips, stop_times, stops):
    """One route's real, in-order stop sequence, taken from its single
    most-used trip shape (the mode over trips per shape_id - one direction is
    enough to get the line's real path; see san_diego/step1_stations.py)."""
    route_trips = trips[trips["route_id"] == route_id]
    if route_trips.empty:
        raise SystemExit(f"Route {route_id!r} has no trips in {GTFS_ZIP.name}. "
                         "SEPTA may have renumbered its routes; check "
                         "config.ROUTE_GROUPS against routes.txt.")
    shape_id = Counter(route_trips["shape_id"].dropna()).most_common(1)[0][0]
    trip_id = route_trips[route_trips["shape_id"] == shape_id].iloc[0]["trip_id"]

    seq = stop_times[stop_times["trip_id"] == trip_id].copy()
    seq["stop_sequence"] = seq["stop_sequence"].astype(int)
    seq = seq.sort_values("stop_sequence").merge(stops, on="stop_id")
    seq["latitude"] = seq["stop_lat"].astype(float)
    seq["longitude"] = seq["stop_lon"].astype(float)
    seq["canonical"] = seq["stop_name"].apply(canonical_name)
    # A stop repeated within one trip (a loop terminal) would confuse the
    # sequential spacing walk below.
    seq = seq.drop_duplicates(subset="canonical", keep="first")
    return seq[["canonical", "latitude", "longitude"]].reset_index(drop=True)


def select_line_stations(route_id, ordered, interchange_names):
    """The four filters, applied to one street-running route's ordered stops.

    Returns (kept, excluded); excluded carries enough to document every cut
    stop - which route, why, and what it was nearest to instead.
    """
    n = len(ordered)
    kept_mask = [False] * n
    last_kept_name = [None] * n

    # Filter 1: central-corridor (tunnel) stations - always kept, never
    # thinned. Never fires on G, which has no tunnel.
    for i in range(n):
        if ordered.iloc[i]["canonical"] in SUBWAY_STATION_NAMES:
            kept_mask[i] = True

    # Filter 2: this route's own two terminals.
    kept_mask[0] = True
    kept_mask[n - 1] = True

    # Filter 3: ~1 per STATION_SPACING_MILES along the route's real
    # stop-to-stop path, counted fresh from whichever stop was most recently
    # kept by ANY filter - not from the route's start.
    cursor_lat = ordered.iloc[0]["latitude"]
    cursor_lon = ordered.iloc[0]["longitude"]
    since_last_kept = 0.0
    most_recent_kept = ordered.iloc[0]["canonical"]
    exclusion_distance = {}
    for i in range(1, n - 1):
        row = ordered.iloc[i]
        since_last_kept += haversine_miles(cursor_lat, cursor_lon,
                                           row["latitude"], row["longitude"])
        cursor_lat, cursor_lon = row["latitude"], row["longitude"]
        if kept_mask[i]:
            since_last_kept = 0.0
            most_recent_kept = row["canonical"]
            continue
        if since_last_kept >= STATION_SPACING_MILES:
            kept_mask[i] = True
            since_last_kept = 0.0
            most_recent_kept = row["canonical"]
        else:
            last_kept_name[i] = most_recent_kept
            exclusion_distance[row["canonical"]] = since_last_kept

    # Filter 4: force-keep real transfer points (a stop 2+ routes share) even
    # where filter 3's spacing alone would have dropped them.
    for i in range(n):
        if ordered.iloc[i]["canonical"] in interchange_names:
            kept_mask[i] = True

    kept = ordered[kept_mask].drop_duplicates(subset="canonical")

    excluded_rows = []
    for i in range(n):
        if kept_mask[i]:
            continue
        name = ordered.iloc[i]["canonical"]
        excluded_rows.append({
            "station": name,
            "line": route_id,
            "latitude": ordered.iloc[i]["latitude"],
            "longitude": ordered.iloc[i]["longitude"],
            "reason": f"spacing filter (street-running stop, < "
                      f"{STATION_SPACING_MILES}mi since nearest kept stop)",
            "nearest_kept_station": last_kept_name[i],
            "miles_since_nearest_kept": round(
                exclusion_distance.get(name, float("nan")), 3),
        })
    excluded = pd.DataFrame(excluded_rows)
    if not excluded.empty:
        excluded = excluded.drop_duplicates(subset=["station", "line"])
    return kept, excluded


def report_near_duplicates(stations):
    """Any two distinct station names within SAME_STATION_METRES are almost
    certainly one physical station under inconsistent raw naming. Report them
    for STATION_NAME_ALIASES rather than merging silently."""
    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC,
    ).to_crs(CRS_PROJECTED)
    xy = list(zip(gdf.geometry.x, gdf.geometry.y, stations["station"]))
    pairs = []
    for i in range(len(xy)):
        for j in range(i + 1, len(xy)):
            d = math.dist(xy[i][:2], xy[j][:2])
            if d < SAME_STATION_METRES:
                pairs.append((xy[i][2], xy[j][2], round(d, 1)))
    if pairs:
        print(f"\n{len(pairs)} pair(s) of distinct names within "
              f"{SAME_STATION_METRES:.0f} m - candidates for "
              f"STATION_NAME_ALIASES:")
        for a, b, d in sorted(pairs, key=lambda p: p[2]):
            print(f"  {d:>6} m  {a!r} <-> {b!r}")
    else:
        print(f"\nNo two distinct station names sit within "
              f"{SAME_STATION_METRES:.0f} m of each other - the suffix pattern "
              f"and the {len(STATION_NAME_ALIASES)} configured alias(es) "
              f"resolved every duplicate this feed has.")


def main():
    if not GTFS_ZIP.exists():
        sys.exit(f"No GTFS feed at {GTFS_ZIP}.\n"
                 f"Run: python pipeline/philadelphia/fetch_sources.py\n"
                 f"(it downloads {GTFS_URL} and extracts the inner feed).")
    if not CITY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"No boundary file at {CITY_BOUNDARY_GEOJSON}. "
                 "Run pipeline/philadelphia/fetch_sources.py.")

    trips = load_gtfs_table(GTFS_ZIP, "trips.txt",
                            usecols=["route_id", "trip_id", "shape_id"])
    stop_times = load_gtfs_table(GTFS_ZIP, "stop_times.txt",
                                 usecols=["trip_id", "stop_id", "stop_sequence"])
    stops = load_gtfs_table(GTFS_ZIP, "stops.txt",
                            usecols=["stop_id", "stop_name", "stop_lat", "stop_lon"])

    sequences = {}
    for group, route_ids in ROUTE_GROUPS.items():
        for route_id in route_ids:
            sequences[(group, route_id)] = ordered_stop_sequence(
                route_id, trips, stop_times, stops)

    # Real transfer points: a canonical station served by 2+ LINE GROUPS.
    #
    # Group-level, not route-level, and that distinction matters here in a way
    # it did not in San Francisco (where every route was its own line). All
    # five T branches share the Center City tunnel, and T4 and T5 additionally
    # share the whole Woodland Avenue segment - counting those as transfer
    # points force-kept five consecutive stops inside 400 m and quietly
    # defeated the thinning. Two branches of one trunk are not an interchange;
    # the tunnel stations they share are kept by filter 1 regardless.
    name_to_groups = {}
    for (group, _), seq in sequences.items():
        for name in seq["canonical"].unique():
            name_to_groups.setdefault(name, set()).add(group)
    interchange_names = {n for n, gs in name_to_groups.items() if len(gs) >= 2}
    print(f"{len(interchange_names)} interchange station(s) served by 2+ line "
          f"groups:\n  {', '.join(sorted(interchange_names))}\n")

    kept_frames = []
    excluded_frames = []
    for (group, route_id), seq in sequences.items():
        name, _ = LINE_NAMES[group]
        if group in THINNED_GROUPS:
            selected, excluded = select_line_stations(route_id, seq,
                                                      interchange_names)
            excluded_frames.append(excluded)
            print(f"{group}/{route_id} ({name}): kept {len(selected)} of "
                  f"{len(seq)} stops - street-running, thinned to "
                  f"{STATION_SPACING_MILES} mi")
        else:
            selected = seq.drop_duplicates(subset="canonical")
            print(f"{group}/{route_id} ({name}): kept all {len(selected)} "
                  f"stations - grade-separated, not thinned")
        kept_frames.append(selected)

    all_selected = pd.concat(kept_frames, ignore_index=True)
    stations = (
        all_selected.groupby("canonical", as_index=False)
        .agg(latitude=("latitude", "mean"), longitude=("longitude", "mean"))
        .rename(columns={"canonical": "station"})
    )
    print(f"\n{len(stations)} distinct stations selected across "
          f"{len(sequences)} routes (before the city-boundary check).")

    # --- Spatial filter to Philadelphia --------------------------------------
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = (boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None
                else boundary.to_crs(CRS_GEOGRAPHIC)).dissolve()

    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC,
    )
    joined = gpd.sjoin(stations_gdf, boundary[["geometry"]],
                       predicate="within", how="left")
    in_city = joined[~joined["index_right"].isna()].drop(
        columns=["geometry", "index_right"])
    out_city = joined[joined["index_right"].isna()].drop(
        columns=["geometry", "index_right"])

    print(f"\nCity-limits filter: {len(stations)} -> {len(in_city)} stations "
          f"({len(out_city)} outside Philadelphia)")
    if len(out_city):
        for _, row in out_city.sort_values("station").iterrows():
            print(f"  excluded: {row['station']}")

    # Every cut station is documented - the thinned stops and the ones outside
    # the city alike. Written to outputs/ (committed) rather than
    # data/processed/ (gitignored): it is a citable record of a design
    # decision, not scratch output.
    out_city_rows = out_city.assign(
        line="", reason="outside Philadelphia city limits",
        nearest_kept_station="", miles_since_nearest_kept=float("nan"),
    )[["station", "line", "latitude", "longitude", "reason",
       "nearest_kept_station", "miles_since_nearest_kept"]]

    excluded_frames = [f for f in excluded_frames if not f.empty]
    excluded = pd.concat(excluded_frames + [out_city_rows], ignore_index=True)
    # A stop thinned on one branch but kept on another is not excluded at all.
    excluded = excluded[~excluded["station"].isin(set(in_city["station"]))]
    excluded = excluded.drop_duplicates(subset=["station", "line"]).sort_values(
        ["line", "station"])
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded.to_csv(EXCLUDED_STATIONS_CSV, index=False)
    print(f"\n{len(excluded)} excluded stop(s) documented in "
          f"{EXCLUDED_STATIONS_CSV}")

    in_city = in_city.sort_values("station").reset_index(drop=True)
    report_near_duplicates(in_city)

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    in_city.to_csv(STATIONS_CSV, index=False)
    print(f"\nWrote {len(in_city)} stations to {STATIONS_CSV}")


if __name__ == "__main__":
    main()
