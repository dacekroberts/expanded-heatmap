"""Step 1 - MBTA rapid-transit stations in Boston, with the Green Line thinned.

Input:  data/boston/raw/gtfs.zip                  (MBTA GTFS)
        data/boston/raw/ma_municipalities.geojson (MassGIS town polygons)
Output: data/boston/processed/stations.csv
        outputs/boston/excluded_stations.csv      (two kinds of exclusion)

TWO STATION RULES AT ONCE, as in Philadelphia:

  Red, Orange, Blue and Mattapan keep EVERY in-city station. Red/Orange/Blue
  are grade-separated heavy rail on their own right-of-way. Mattapan is a
  street-running trolley and the obvious guess was that it needed thinning,
  but its stops sit a median 518 m apart - comparable to New York's 482 m and
  nowhere near San Francisco's 134 m - so it is left whole on the measurement
  rather than on the label. See config.THINNED_GROUPS.

  The Green Line is a central subway plus four street-running surface
  branches, which is San Francisco's exact shape, so it takes the four
  sub-transit-line filters (docs/sub_transit_line_filters.md).

The excluded-stations record therefore carries TWO reasons, and names which:
stations in another municipality (the network is regional - it reaches
Brookline, Cambridge, Somerville, Newton, Medford, Malden, Quincy, Revere and
Milton) and Green Line surface stops dropped by the spacing filter.

Run:  python pipeline/boston/step1_stations.py
"""

import io
import math
import re
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.boston.config import (  # noqa: E402
    BOUNDARY_TOWN_FIELD,
    CITY_BOUNDARY_NAME,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_ZIP,
    LINE_NAMES,
    LINE_SHAPES,
    ROUTE_GROUPS,
    STATION_NAME_ALIASES,
    STATION_SPACING_MILES,
    STATION_SUFFIX_PATTERN,
    STATIONS_CSV,
    SUBWAY_STATION_NAMES,
    THINNED_GROUPS,
    TOWN_BOUNDARIES_GEOJSON,
)

_SUFFIX = re.compile(STATION_SUFFIX_PATTERN)
NEAR_DUPLICATE_M = 150.0


def canonical_name(stop_name: str) -> str:
    raw = str(stop_name).strip()
    prev = None
    while prev != raw:
        prev = raw
        raw = _SUFFIX.sub("", raw).strip()
    return STATION_NAME_ALIASES.get(raw, raw)


def haversine_miles(lat1, lon1, lat2, lon2):
    r = 3958.7613
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def load(zip_path, filename, usecols=None):
    with zipfile.ZipFile(zip_path) as z, z.open(filename) as f:
        return pd.read_csv(io.BytesIO(f.read()), dtype=str, low_memory=False,
                           usecols=usecols)


def ordered_stop_sequence(shape_id, trips, stop_times, stops, parent_of, name_of):
    """One line's real, in-order stop sequence for a representative shape."""
    match = trips[trips["shape_id"] == shape_id]
    if match.empty:
        sys.exit(f"shape_id {shape_id!r} is not in this feed. MBTA renumbers "
                 f"shapes between feed versions - re-check config.LINE_SHAPES "
                 f"against trips.txt.")
    trip_id = match["trip_id"].iloc[0]
    seq = stop_times[stop_times["trip_id"] == trip_id].copy()
    seq["stop_sequence"] = seq["stop_sequence"].astype(int)
    seq = seq.sort_values("stop_sequence")
    rows = []
    for stop_id in seq["stop_id"]:
        parent = parent_of.get(stop_id)
        key = parent if isinstance(parent, str) and parent else stop_id
        lat, lon = name_of[key][1], name_of[key][2]
        rows.append({"canonical": canonical_name(name_of[key][0]),
                     "latitude": lat, "longitude": lon})
    out = pd.DataFrame(rows)
    # A shape can revisit a station (the Green Line's shared subway); keep the
    # first occurrence so the sequence stays a path.
    return out.drop_duplicates(subset="canonical").reset_index(drop=True)


def select_line_stations(group, ordered, interchange_names):
    """The four filters, applied to one line's ordered sequence."""
    n = len(ordered)
    kept = [False] * n
    last_kept_name = [None] * n

    # Filter 1: central-subway stations are never thinned.
    for i in range(n):
        if ordered.iloc[i]["canonical"] in SUBWAY_STATION_NAMES:
            kept[i] = True
    # Filter 2: this line's own two terminals.
    kept[0] = True
    kept[n - 1] = True

    # Filter 3: ~1 per STATION_SPACING_MILES along the real path, counted
    # fresh from whichever stop was most recently kept by ANY filter.
    cur_lat, cur_lon = ordered.iloc[0]["latitude"], ordered.iloc[0]["longitude"]
    since = 0.0
    most_recent = ordered.iloc[0]["canonical"]
    at_exclusion = {}
    for i in range(1, n - 1):
        row = ordered.iloc[i]
        since += haversine_miles(cur_lat, cur_lon, row["latitude"], row["longitude"])
        cur_lat, cur_lon = row["latitude"], row["longitude"]
        if kept[i]:
            since = 0.0
            most_recent = row["canonical"]
            continue
        if since >= STATION_SPACING_MILES:
            kept[i] = True
            since = 0.0
            most_recent = row["canonical"]
        else:
            last_kept_name[i] = most_recent
            at_exclusion[row["canonical"]] = since

    # Filter 4: a stop shared by 2+ line GROUPS is force-kept.
    for i in range(n):
        if ordered.iloc[i]["canonical"] in interchange_names:
            kept[i] = True

    keep_df = ordered[kept].drop_duplicates(subset="canonical")
    excluded = [{
        "station": ordered.iloc[i]["canonical"],
        "line": LINE_NAMES[group][0],
        "latitude": ordered.iloc[i]["latitude"],
        "longitude": ordered.iloc[i]["longitude"],
        "reason": f"Green Line spacing filter (surface stop, under "
                  f"{STATION_SPACING_MILES} mi since the nearest kept stop)",
        "located_in": "",
        "nearest_kept_station": last_kept_name[i],
        "miles_since_nearest_kept": round(at_exclusion.get(
            ordered.iloc[i]["canonical"], float("nan")), 3),
    } for i in range(n) if not kept[i]]
    return keep_df, pd.DataFrame(excluded)


def report_near_duplicates(stations):
    """Two distinct names within NEAR_DUPLICATE_M are almost certainly one
    physical station under inconsistent naming - the check San Francisco's
    build needed four hand-curated aliases to satisfy."""
    if stations.empty:
        return
    g = gpd.GeoSeries(
        gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    names = list(stations["station"])
    flagged = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            d = g.iloc[i].distance(g.iloc[j])
            if d < NEAR_DUPLICATE_M:
                flagged.append((names[i], names[j], round(d, 1)))
    if flagged:
        print(f"\n  NEAR-DUPLICATE CHECK: {len(flagged)} pair(s) within "
              f"{NEAR_DUPLICATE_M:.0f} m - add an alias to "
              f"config.STATION_NAME_ALIASES if these are one station:")
        for a, b, d in flagged:
            print(f"    {d:>6.1f} m  {a!r}  vs  {b!r}")
    else:
        print(f"\n  Near-duplicate check: no two stations within "
              f"{NEAR_DUPLICATE_M:.0f} m - no missing aliases.")


def main():
    for path in (GTFS_ZIP, TOWN_BOUNDARIES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run pipeline/boston/fetch_sources.py first.")

    routes = load(GTFS_ZIP, "routes.txt", usecols=["route_id", "route_type"])
    wanted = {r for ids in ROUTE_GROUPS.values() for r in ids}
    missing = wanted - set(routes["route_id"])
    if missing:
        sys.exit(f"route_id(s) {sorted(missing)} not in this feed - check "
                 f"config.ROUTE_GROUPS against routes.txt.")
    print(f"{len(wanted)} rapid-transit route_ids in "
          f"{len(ROUTE_GROUPS)} line groups; the 14 CR-* Regional Rail routes "
          f"and the ferries are deliberately not included.\n")

    trips = load(GTFS_ZIP, "trips.txt",
                 usecols=["route_id", "trip_id", "shape_id"])
    stop_times = load(GTFS_ZIP, "stop_times.txt",
                      usecols=["trip_id", "stop_id", "stop_sequence"])
    stops = load(GTFS_ZIP, "stops.txt",
                 usecols=["stop_id", "stop_name", "parent_station",
                          "stop_lat", "stop_lon"])
    parent_of = dict(zip(stops["stop_id"], stops["parent_station"]))
    name_of = {r.stop_id: (r.stop_name, float(r.stop_lat), float(r.stop_lon))
               for r in stops.itertuples()}

    # Assert the configured subway list is real. A typo here silently thins a
    # central-subway station as if it were a surface stop, which is how
    # "North Station" was found being truncated to "North".
    green_names = set()
    for rid in ROUTE_GROUPS["Green"]:
        ids = set(stop_times[stop_times["trip_id"].isin(
            set(trips[trips["route_id"] == rid]["trip_id"]))]["stop_id"])
        for s in ids:
            p = parent_of.get(s)
            key = p if isinstance(p, str) and p else s
            green_names.add(canonical_name(name_of[key][0]))
    absent = sorted(SUBWAY_STATION_NAMES - green_names)
    if absent:
        sys.exit(f"config.SUBWAY_STATION_NAMES lists {absent}, which the feed "
                 f"does not contain on any Green Line branch. Filter 1 would "
                 f"silently thin them. Fix the names or the suffix pattern.")
    print(f"All {len(SUBWAY_STATION_NAMES)} configured central-subway stations "
          f"are present in the feed.\n")

    # Which groups serve each station, for the group-level interchange test.
    # GROUP level, not route level: two branches of one trunk are not an
    # interchange, and treating them as one defeated Philadelphia's thinning.
    sequences, name_to_groups = {}, {}
    for group, rids in ROUTE_GROUPS.items():
        group_trips = trips[trips["route_id"].isin(rids)]
        for shape_id in LINE_SHAPES[group]:
            seq = ordered_stop_sequence(shape_id, group_trips, stop_times,
                                        stops, parent_of, name_of)
            sequences[(group, shape_id)] = seq
            for nm in seq["canonical"]:
                name_to_groups.setdefault(nm, set()).add(group)
    interchange = {n for n, gs in name_to_groups.items() if len(gs) >= 2}
    print(f"{len(interchange)} interchange station(s) served by 2+ line "
          f"groups:\n  {', '.join(sorted(interchange))}\n")

    kept_frames, excluded_frames = [], []
    for (group, shape_id), seq in sequences.items():
        if group in THINNED_GROUPS:
            keep, excl = select_line_stations(group, seq, interchange)
            print(f"  {LINE_NAMES[group][0]:<18} {shape_id:<12} "
                  f"{len(seq):>3} stops -> {len(keep):>3} kept "
                  f"({len(excl)} thinned)")
            excluded_frames.append(excl)
        else:
            keep = seq
            print(f"  {LINE_NAMES[group][0]:<18} {shape_id:<12} "
                  f"{len(seq):>3} stops -> {len(keep):>3} kept (not thinned)")
        kept_frames.append(keep.assign(line=LINE_NAMES[group][0]))

    stations = (pd.concat(kept_frames, ignore_index=True)
                .rename(columns={"canonical": "station"}))
    stations = (stations.groupby("station", as_index=False)
                .agg(latitude=("latitude", "first"),
                     longitude=("longitude", "first"),
                     lines=("line", lambda s: ", ".join(sorted(set(s))))))
    print(f"\n{len(stations)} distinct stations after thinning, before the "
          f"municipal filter")

    # --- Which municipality is each station in? ---------------------------
    towns = gpd.read_file(TOWN_BOUNDARIES_GEOJSON)
    towns = (towns.set_crs(CRS_GEOGRAPHIC) if towns.crs is None
             else towns.to_crs(CRS_GEOGRAPHIC))
    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC)
    located = gpd.sjoin(gdf, towns[[BOUNDARY_TOWN_FIELD, "geometry"]],
                        predicate="within", how="left")
    if located.index.duplicated().any():
        located = located[~located.index.duplicated()]
    located = located.drop(columns=["index_right", "geometry"])
    located["located_in"] = (located[BOUNDARY_TOWN_FIELD]
                             .fillna("(outside every town polygon)"))
    located = located.drop(columns=[BOUNDARY_TOWN_FIELD])

    in_city = located[located["located_in"] == CITY_BOUNDARY_NAME].copy()
    out_city = located[located["located_in"] != CITY_BOUNDARY_NAME].copy()

    print(f"\n{len(in_city)} of {len(located)} stations are in "
          f"{CITY_BOUNDARY_NAME}. Excluded, by the town they are in:")
    print("  " + out_city["located_in"].value_counts()
          .to_string().replace("\n", "\n  "))

    out_city = out_city.assign(
        line=out_city["lines"],
        reason="outside the City of Boston (the network is regional)",
        nearest_kept_station="", miles_since_nearest_kept="")

    cols = ["station", "line", "latitude", "longitude", "reason", "located_in",
            "nearest_kept_station", "miles_since_nearest_kept"]
    excluded = pd.concat(
        [f for f in excluded_frames if not f.empty] + [out_city[cols]],
        ignore_index=True)
    # A Green Line stop can be thinned AND out of town; report it once, as
    # out-of-town, because that is the stronger reason.
    excluded = excluded.drop_duplicates(subset=["station"], keep="last")

    report_near_duplicates(in_city)

    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded[cols].sort_values(["reason", "station"]).to_csv(
        EXCLUDED_STATIONS_CSV, index=False)
    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    in_city.sort_values("station")[["station", "latitude", "longitude"]].to_csv(
        STATIONS_CSV, index=False)

    print(f"\nWrote {len(in_city)} stations to {STATIONS_CSV}")
    print(f"Wrote {len(excluded)} excluded station(s) to "
          f"{EXCLUDED_STATIONS_CSV}, with the reason for each")


if __name__ == "__main__":
    main()
