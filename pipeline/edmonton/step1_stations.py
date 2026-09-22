"""Step 1 - ETS LRT stations, all of which are inside Edmonton.

Input:  data/edmonton/raw/gtfs.zip              (ETS's own feed)
        data/edmonton/raw/city_boundary.geojson (qqvh-dp5m, the current one)
Output: data/edmonton/processed/stations.csv
        outputs/edmonton/excluded_stations.csv   (EMPTY - nothing is outside)
        outputs/edmonton/non_revenue_stops.csv   (3 rows - see below)

THREE OF EDMONTON'S 33 "STATIONS" ARE NOT STATIONS, AND THIS IS A NEW ERROR FOR
THIS PROJECT. Toronto's and Calgary's station counts were wrong because
PLATFORMS had been counted as stations; Edmonton's is wrong for a different
reason, and the platform check passes here cleanly. `parent_station` is
populated on all 65 served stops and collapses them to 33 with a healthy 632 m
nearest-neighbour median. But every rail trip also touches two garage access
points and a tail track, and at those three NOBODY CAN BOARD:

    Q7020  Andrews Garage Platform   1,947 stop_times, 0 boardable
    Q7019  DL Macdonald Platform     1,947 stop_times, 0 boardable
    QHTT   Health Sciences Tail      1,430 stop_times, 0 boardable

`pickup_type` and `drop_off_type` are both 1 on every one of their stop_times.
Every other station has thousands of boardable ones, so the split is not a
judgment call. Keeping them inflated the published Canada ranking figure -
2,520 storefronts / 33 = 76 per station, against the real 2,445 / 30 = **82**.

**Every city in this project should have had this check and none of them did.**
A stop a revenue trip touches is not automatically a place a passenger can use,
and "it is in stop_times for a rail trip" is the assumption that hid it. The
generalisation is in the `add-city` skill: a station count needs BOTH the
spacing diagnostic (are these platforms?) and the boardability filter (are
these stations?).

TWO MORE THINGS WORTH KNOWING BEFORE CHANGING ANYTHING HERE.

  **`route_id` IS safe to pin here, unlike Calgary's.** Edmonton's ids are
  stable and self-describing (`021R`, `022R`, `023R`) where Calgary embeds a
  feed version (`201-20780` vs `201-20786`). The short names are checked too,
  because they are what the legend shows.

  **No thinning.** The measured spacing settles it, as it did for Calgary: the
  Valley Line is street-running and its stops sit at normal spacing, not the
  every-block spacing that forced San Francisco's thinning. What the spacing
  DOES show is three genuine interchange pairs 84-328 m apart, where a Valley
  Line surface stop sits beside a Capital Line underground station. Those are
  different places with different platforms and are correctly not merged.

Run:  python pipeline/edmonton/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.edmonton.config import (  # noqa: E402
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_ZIP,
    IN_CITY_STATIONS_EXPECTED,
    LINE_NAMES,
    NON_REVENUE_STOPS_CSV,
    NON_REVENUE_STOPS_EXPECTED,
    PARENT_STATIONS_EXPECTED,
    PLATFORM_SPACING_MEDIAN_M_MAX,
    PLATFORMS_EXPECTED,
    RING_EDGES_METERS,
    ROUTE_IDS,
    ROUTE_SHORT_NAMES,
    STATION_SPACING_MEDIAN_M_MIN,
    STATIONS_CSV,
)


def load(zip_path, filename, **kw):
    with zipfile.ZipFile(zip_path) as z, z.open(filename) as f:
        return pd.read_csv(f, dtype=str, **kw)


def nn_metres(lon, lat):
    """Nearest-neighbour distance per point, in the city's projected CRS."""
    pts = gpd.GeoSeries(gpd.points_from_xy(lon, lat),
                        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    pts = pts.reset_index(drop=True)
    return np.array([pts.drop(index=i).distance(pts.iloc[i]).min()
                     for i in range(len(pts))])


def main():
    for path in (GTFS_ZIP, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/edmonton/fetch_sources.py first.")

    # --- routes -------------------------------------------------------------
    routes = load(GTFS_ZIP, "routes.txt")
    matched = routes[routes["route_id"].isin(ROUTE_IDS)]
    missing = sorted(set(ROUTE_IDS) - set(matched["route_id"]))
    if missing:
        sys.exit(f"route_id(s) {missing} are not in this feed. Edmonton's ids "
                 f"are stable (unlike Calgary's versioned ones), so this means "
                 f"the network changed, not that the pin is wrong.")
    non_rail = matched[~matched["route_type"].isin({"0", "1"})]
    if len(non_rail):
        sys.exit(f"route_type {list(non_rail['route_type'])} on "
                 f"{list(non_rail['route_id'])} - the LRT is route_type 0; a "
                 f"bus route has been matched.")
    got_short = sorted(matched["route_short_name"].dropna())
    if got_short != sorted(ROUTE_SHORT_NAMES):
        print(f"  NOTE: short names are {got_short}, config expects "
              f"{sorted(ROUTE_SHORT_NAMES)} - the legend uses these.")
    print("Routes drawn (matched on route_id, which is stable here):")
    for r in matched.sort_values("route_id").itertuples():
        print(f"  {r.route_id:<6} {LINE_NAMES[r.route_id]:<14} "
              f"short={r.route_short_name:<8} route_type={r.route_type}")

    # --- shape candidates, so LINE_SHAPES can be filled from evidence ------
    trips = load(GTFS_ZIP, "trips.txt")
    keep_trips = trips[trips["route_id"].isin(set(matched["route_id"]))]
    print("\nTrips per shape, per line (the mode is the line's primary "
          "alignment):")
    for rid in ROUTE_IDS:
        tt = keep_trips[keep_trips["route_id"] == rid]
        vc = tt["shape_id"].value_counts()
        print(f"  {LINE_NAMES[rid]} ({rid}): {len(tt):,} trips, "
              f"{len(vc)} shapes")
        for sid, n in vc.head(4).items():
            print(f"      {sid:<20} {n:>5} trips")

    # --- served stops = PLATFORMS -------------------------------------------
    stop_times = load(GTFS_ZIP, "stop_times.txt",
                      usecols=["trip_id", "stop_id", "pickup_type",
                               "drop_off_type"])
    stops = load(GTFS_ZIP, "stops.txt")
    served = stop_times[stop_times["trip_id"].isin(set(keep_trips["trip_id"]))]
    rs = stops[stops["stop_id"].isin(set(served["stop_id"]))].copy()
    rs["latitude"] = rs["stop_lat"].astype(float)
    rs["longitude"] = rs["stop_lon"].astype(float)
    print(f"\n{len(rs)} served stops - these are PLATFORMS, not stations")
    if len(rs) != PLATFORMS_EXPECTED:
        print(f"  NOTE: expected {PLATFORMS_EXPECTED}")

    if rs["parent_station"].isna().any():
        sys.exit(f"parent_station is blank on "
                 f"{int(rs['parent_station'].isna().sum())} served stop(s). It "
                 f"was populated on all {PLATFORMS_EXPECTED} on 2026-09-21, "
                 f"and it is the first and best of this project's four "
                 f"collapse mechanisms - do not fall back to name munging "
                 f"without measuring the spacing afterwards.")

    # --- THE BOARDABILITY FILTER: which served stops are stations at all ----
    sv = served.copy()
    sv["boardable"] = ((sv["pickup_type"].fillna("0") == "0")
                       | (sv["drop_off_type"].fillna("0") == "0"))
    by_stop = sv.groupby("stop_id")["boardable"].agg(["any", "size", "sum"])
    rs = rs.join(by_stop, on="stop_id")
    revenue = rs["any"].fillna(False).astype(bool)
    non_rev = rs[~revenue].copy()
    print(f"\nBoardability (pickup_type/drop_off_type on every stop_time):")
    print(f"  {int(revenue.sum())} of {len(rs)} served stops are boardable")
    if len(non_rev):
        print(f"  {len(non_rev)} are NOT - a trip stops there but no passenger "
              f"can use it:")
        for r in non_rev.sort_values("stop_name").itertuples():
            print(f"      {r.parent_station:<8} {r.stop_name:<34} "
                  f"{int(r.size):>5} stop_times, 0 boardable")
    rs = rs[revenue].copy()

    # --- collapse platforms -> stations -------------------------------------
    stations = rs.groupby("parent_station").agg(
        station=("stop_name", "first"),
        latitude=("latitude", "mean"),
        longitude=("longitude", "mean"),
        platforms=("stop_id", "size")).reset_index()
    per = stations["platforms"].value_counts().sort_index()
    print(f"\n{len(rs)} boardable platforms -> {len(stations)} stations "
          f"({', '.join(f'{n} with {k}' for k, n in per.items())})")

    non_rev_parents = set(non_rev["parent_station"]) - set(stations["parent_station"])
    if len(non_rev_parents) != NON_REVENUE_STOPS_EXPECTED:
        print(f"  NOTE: {len(non_rev_parents)} non-revenue stations dropped, "
              f"expected {NON_REVENUE_STOPS_EXPECTED}")
    if len(stations) + len(non_rev_parents) != PARENT_STATIONS_EXPECTED:
        print(f"  NOTE: {len(stations)} + {len(non_rev_parents)} does not make "
              f"the {PARENT_STATIONS_EXPECTED} parent_stations measured on "
              f"2026-09-21 - the network has changed.")

    # --- the spacing diagnostic, BOTH ways ----------------------------------
    # This is the check that caught Toronto and Calgary, and it is run on the
    # uncollapsed set too so that a regression shows up as a number rather than
    # as a plausible-looking station list.
    raw_nn = nn_metres(rs["longitude"], rs["latitude"])
    st_nn = nn_metres(stations["longitude"], stations["latitude"])
    stations["nearest_station_m"] = np.round(st_nn, 1)
    print("\nNearest-neighbour spacing (the platform-vs-station diagnostic):")
    print(f"  {len(rs)} platforms : median {np.median(raw_nn):>6.0f} m  "
          f"min {raw_nn.min():>5.0f}  -> must look like platforms")
    print(f"  {len(stations)} stations  : median {np.median(st_nn):>6.0f} m  "
          f"min {st_nn.min():>5.0f}  -> must not")
    if np.median(raw_nn) > PLATFORM_SPACING_MEDIAN_M_MAX:
        sys.exit(f"  uncollapsed median {np.median(raw_nn):.0f} m is too WIDE "
                 f"for platforms. Either the feed stopped publishing separate "
                 f"platforms, or the wrong stops were selected.")
    if np.median(st_nn) < STATION_SPACING_MEDIAN_M_MIN:
        sys.exit(f"  collapsed median {np.median(st_nn):.0f} m is too TIGHT for "
                 f"stations - these are still platforms. This is exactly what "
                 f"went wrong in Toronto (234 'stations') and Calgary (83).")
    outer = RING_EDGES_METERS[-1]
    print(f"  closer than the {outer:.0f} m outer ring: "
          f"{int((st_nn < outer).sum())}/{len(stations)}")
    print(f"  San Francisco's street-running median was 134 m and WAS thinned; "
          f"Calgary 632 m, Montréal 728 m, Vancouver 841 m, none thinned.")
    print("  tightest (these are interchange pairs, not duplicates): "
          + ", ".join(f"{r.station} ({r.nearest_station_m:.0f} m)"
                      for r in stations.nsmallest(4,
                                                  "nearest_station_m").itertuples()))

    # --- which lines serve each station -------------------------------------
    trip_to_route = dict(zip(keep_trips["trip_id"], keep_trips["route_id"]))
    stop_to_parent = dict(zip(rs["stop_id"], rs["parent_station"]))
    sl = served.assign(parent=served["stop_id"].map(stop_to_parent),
                       line=served["trip_id"].map(trip_to_route).map(LINE_NAMES))
    stations["lines"] = stations["parent_station"].map(
        sl.dropna(subset=["parent"]).groupby("parent")["line"].apply(
            lambda s: ", ".join(sorted(set(s.dropna())))))

    print("\nStations per line:")
    for rid, name in LINE_NAMES.items():
        n = int(stations["lines"].fillna("").str.contains(name,
                                                          regex=False).sum())
        print(f"  {name:<14}{n:>4}")
    shared = int(stations["lines"].fillna("").str.contains(",").sum())
    print(f"  served by more than one: {shared}")

    # --- the boundary: a CHECK, since nothing should be outside -------------
    b = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    if len(b) == 0 or b.geometry.isna().all():
        sys.exit("boundary has no geometry.")
    geom = b.to_crs(CRS_PROJECTED).union_all()
    area = geom.area / 1e6
    print(f"\nBoundary: {len(b)} feature(s), {geom.geom_type}, {area:.1f} km2 "
          f"(Edmonton is ~765 km2 of land; 783.1 is the post-2019 polygon)")

    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    inside = gdf.geometry.within(geom)
    outside = gdf[~inside]
    print(f"  inside Edmonton: {int(inside.sum())} of {len(gdf)}")
    if len(outside):
        print(f"  {len(outside)} OUTSIDE, which contradicts the recorded scope "
              f"(the LRT does not leave Edmonton):")
        for r in outside.itertuples():
            print(f"      {r.station:<34} {round(r.geometry.distance(geom)):>7} m")
    kept = gdf[inside].drop(columns="geometry").copy()
    if len(kept) != IN_CITY_STATIONS_EXPECTED:
        print(f"  NOTE: expected {IN_CITY_STATIONS_EXPECTED} stations and got "
              f"{len(kept)} - the network has changed. The Valley Line is "
              f"actively extending, so this is the likely direction.")

    # --- outputs ------------------------------------------------------------
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    # Written even when empty: the file is part of every city's output
    # contract, and an empty one says "nothing was excluded" where a missing
    # one says nothing at all.
    outside.drop(columns="geometry").assign(
        distance_outside_m=[round(r.distance(geom), 1) for r in outside.geometry]
        if len(outside) else pd.Series(dtype=float)
    )[["station", "latitude", "longitude", "lines", "distance_outside_m"]] \
        .to_csv(EXCLUDED_STATIONS_CSV, index=False)

    # The non-revenue stops get the same treatment, for the same reason: this
    # is the first city where they were found, and a silent drop of three
    # "stations" is indistinguishable from a bug.
    non_rev.assign(stop_times=non_rev["size"].astype(int))[
        ["parent_station", "stop_id", "stop_name", "latitude", "longitude",
         "stop_times"]].sort_values("stop_name").to_csv(
        NON_REVENUE_STOPS_CSV, index=False)

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    kept.sort_values("station")[["station", "latitude", "longitude"]].to_csv(
        STATIONS_CSV, index=False)
    print(f"\nWrote {len(kept)} stations to {STATIONS_CSV}")
    print(f"Wrote {EXCLUDED_STATIONS_CSV} ({len(outside)} excluded)")
    print(f"Wrote {NON_REVENUE_STOPS_CSV} ({len(non_rev)} platforms across "
          f"{len(non_rev_parents)} non-revenue stops)")


if __name__ == "__main__":
    main()
