"""Step 1 - CTrain stations, all of which are inside Calgary.

Input:  data/calgary/raw/gtfs.zip              (Calgary Transit's own feed)
        data/calgary/raw/city_boundary.geojson (the `dataset` view)
Output: data/calgary/processed/stations.csv
        outputs/calgary/excluded_stations.csv

THE FEED PUBLISHES 83 PLATFORMS, NOT 83 STATIONS, AND THE WHOLE CANADA
RANKING RECORDED THE PLATFORM COUNT. Every stop name carries a direction
prefix and there is no `parent_station` column, so each name is unique and
nothing looks wrong. They collapse to 45 - the CTrain's real published count.
What caught it was the SPACING: an uncollapsed nearest-neighbour median of
17 m, minimum 8 m, which is impossible for rail stations. See the `add-city`
skill, "A STATION COUNT IS THE MOST ERROR-PRONE NUMBER IN THIS PROJECT".

THIS IS ALSO THE FIRST CITY IN THE PROJECT WHERE NOTHING IS EXCLUDED. The CTrain
does not leave Calgary, so all 45 stations are in scope and
`excluded_stations.csv` is written EMPTY rather than skipped - the file is part
of every city's output contract, and an empty one with a header is a stronger
statement than a missing file. Compare San Diego (16 of 63 dropped), Los
Angeles (54 of 110), D.C. (58 of 98) and SkyTrain (30 of 54).

THREE THINGS WORTH KNOWING BEFORE CHANGING ANYTHING HERE.

  **Routes match on `route_short_name`, NEVER on `route_id`.** Calgary embeds
  a feed version in the id: the Mobility Database mirror gives `201-20780` and
  the agency feed `201-20786`. A config pinning the id matches nothing after
  the next release, and matches it silently.

  **There is no feed validity window to check.** Neither Calgary feed carries
  `feed_info.txt`, so the `feed_end_date` guard written for D.C., Montréal and
  Vancouver cannot exist here. `fetch_sources.py` prints the Socrata
  `updatedAt` instead.

  **No thinning, but for a weaker reason than elsewhere.** The CTrain is
  grade-separated except along the downtown 7 Avenue transit mall, which IS
  street-running - so this is not D.C.'s or the Métro's clean case. What
  settles it is the measured spacing, printed below: the mall's stations sit at
  normal downtown spacing rather than the every-block spacing that forced San
  Francisco's thinning.

Run:  python pipeline/calgary/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.calgary.config import (  # noqa: E402
    CITY_BOUNDARY_GEOJSON,
    PLATFORMS_EXPECTED,
    SINGLE_PLATFORM_STATIONS_EXPECTED,
    STATION_DIRECTION_PREFIX,
    STATION_SUFFIX_PATTERNS,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_ZIP,
    IN_CITY_STATIONS_EXPECTED,
    LINE_NAMES,
    RING_EDGES_METERS,
    ROUTE_SHORT_NAMES,
    STATIONS_CSV,
    THINNED_GROUPS,
)


def load(zip_path, filename, **kw):
    with zipfile.ZipFile(zip_path) as z, z.open(filename) as f:
        return pd.read_csv(f, dtype=str, **kw)


def main():
    for path in (GTFS_ZIP, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/calgary/fetch_sources.py first.")
    if THINNED_GROUPS:
        sys.exit(f"config.THINNED_GROUPS is {set(THINNED_GROUPS)} but this "
                 f"step implements no thinning. Read the docstring first - the "
                 f"7 Avenue mall is street-running, so if thinning is ever "
                 f"wanted here it is a real decision, not an oversight.")

    # --- routes: short name, not id ----------------------------------------
    routes = load(GTFS_ZIP, "routes.txt")
    matched = routes[routes["route_short_name"].isin(ROUTE_SHORT_NAMES)]
    missing = sorted(set(ROUTE_SHORT_NAMES) - set(matched["route_short_name"]))
    if missing:
        sys.exit(f"route_short_name(s) {missing} are not in this feed. Note "
                 f"route_id is NOT usable here - it embeds a feed version "
                 f"(201-20780 in the mirror, 201-20786 in the agency feed).")
    non_rail = matched[~matched["route_type"].isin({"0", "1"})]
    if len(non_rail):
        sys.exit(f"route_type {list(non_rail['route_type'])} on "
                 f"{list(non_rail['route_short_name'])} - the CTrain is "
                 f"route_type 0 (LRT); a bus route has been matched.")
    print("Routes drawn (matched on route_short_name):")
    for r in matched.sort_values("route_short_name").itertuples():
        print(f"  {r.route_short_name:<5} {LINE_NAMES[r.route_short_name]:<11} "
              f"route_id={r.route_id:<12} (VERSIONED - do not pin) "
              f"route_type={r.route_type}")

    # --- shape candidates, so LINE_SHAPES can be filled from evidence ------
    trips = load(GTFS_ZIP, "trips.txt")
    keep_trips = trips[trips["route_id"].isin(set(matched["route_id"]))]
    print("\nTrips per shape, per line (the mode is the line's primary "
          "alignment):")
    id_to_short = dict(zip(matched["route_id"], matched["route_short_name"]))
    for short in ROUTE_SHORT_NAMES:
        ids = [k for k, v in id_to_short.items() if v == short]
        tt = keep_trips[keep_trips["route_id"].isin(ids)]
        vc = tt["shape_id"].value_counts()
        print(f"  {LINE_NAMES[short]} ({short}): {len(tt):,} trips, "
              f"{len(vc)} shapes")
        for sid, n in vc.head(4).items():
            print(f"      {sid:<16} {n:>5} trips")

    # --- stops -> stations --------------------------------------------------
    stop_times = load(GTFS_ZIP, "stop_times.txt",
                      usecols=["trip_id", "stop_id"])
    stops = load(GTFS_ZIP, "stops.txt")
    served = stop_times[stop_times["trip_id"].isin(set(keep_trips["trip_id"]))]
    rs = stops[stops["stop_id"].isin(set(served["stop_id"]))].copy()
    rs["latitude"] = rs["stop_lat"].astype(float)
    rs["longitude"] = rs["stop_lon"].astype(float)
    print(f"\n{len(rs)} served stops - these are PLATFORMS, not stations")
    if "parent_station" not in rs.columns:
        print("  no parent_station column, so nothing collapses them "
              "automatically and every name is unique (NB/SB/EB/WB prefix)")

    # Collapse: strip the direction prefix, then each suffix variant, then
    # normalise hyphens - the hyphen MOVES between one station's two
    # directions. See config for why each of these is necessary.
    name = rs["stop_name"].str.strip().str.replace(
        STATION_DIRECTION_PREFIX, "", regex=True)
    for pat in STATION_SUFFIX_PATTERNS:
        name = name.str.replace(pat, "", regex=True)
    rs["station"] = (name.str.replace("-", " ", regex=False)
                     .str.replace(r"\s+", " ", regex=True).str.strip())
    blank = rs["station"].eq("")
    if blank.any():
        sys.exit(f"{int(blank.sum())} stop name(s) normalised to nothing.")

    per_station = rs.groupby("station").size()
    stations = rs.groupby("station").agg(
        latitude=("latitude", "mean"),
        longitude=("longitude", "mean"),
        platforms=("stop_id", "size")).reset_index()
    singles = int((per_station == 1).sum())
    print(f"  -> {len(stations)} stations "
          f"({int((per_station == 2).sum())} with 2 platforms, {singles} with 1)")
    print(f"  the {singles} single-platform stations are 7 Avenue's ONE-WAY "
          f"COUPLET - EB 3 Street SW and WB 4 Street SW are different places, "
          f"so they are correctly NOT merged: "
          f"{', '.join(sorted(per_station[per_station == 1].index))}")

    # The collapse is only evidence if it agrees with the operator's own count.
    if len(stations) != IN_CITY_STATIONS_EXPECTED:
        sys.exit(
            f"collapsed to {len(stations)} stations, expected "
            f"{IN_CITY_STATIONS_EXPECTED} (the CTrain's published count). A "
            f"naive strip gets 47 or 49 here - the feed contains a typo "
            f"('CTrain Staion'), three different suffixes, and a hyphen that "
            f"moves between one station's two directions. Check "
            f"config.STATION_SUFFIX_PATTERNS against the printed name list "
            f"rather than adjusting this number."
        )
    if len(rs) != PLATFORMS_EXPECTED:
        print(f"  NOTE: {len(rs)} platforms, expected {PLATFORMS_EXPECTED}")
    if singles != SINGLE_PLATFORM_STATIONS_EXPECTED:
        print(f"  NOTE: {singles} single-platform stations, expected "
              f"{SINGLE_PLATFORM_STATIONS_EXPECTED}")

    # which lines serve each station
    trip_to_short = {t: id_to_short[r] for t, r in
                     zip(keep_trips["trip_id"], keep_trips["route_id"])}
    st = served.assign(station=served["stop_id"].map(
        dict(zip(rs["stop_id"], rs["station"]))),
        line=served["trip_id"].map(trip_to_short).map(LINE_NAMES))
    stations["lines"] = stations["station"].map(
        st.groupby("station")["line"].apply(
            lambda s: ", ".join(sorted(set(s.dropna())))))

    # --- the boundary: a CHECK, since nothing should be outside -------------
    b = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    if len(b) == 0 or b.geometry.isna().all():
        sys.exit("boundary has no geometry - this is the `map`-view trap. Use "
                 "the `dataset` view (erra-cqp9), not 7t9h-2z9s.")
    geom = b.to_crs(CRS_PROJECTED).union_all()
    area = geom.area / 1e6
    print(f"\nBoundary: {len(b)} feature(s), {geom.geom_type}, {area:.1f} km2 "
          f"(Calgary is ~825 km2 of land)")
    if not 600 < area < 1100:
        sys.exit(f"  dissolved area {area:.1f} km2 is implausible for Calgary.")

    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    inside = gdf.geometry.within(geom)
    outside = gdf[~inside]
    print(f"  inside Calgary: {int(inside.sum())} of {len(gdf)}")
    if len(outside):
        print(f"  {len(outside)} OUTSIDE, which contradicts the recorded scope "
              f"(the CTrain does not leave Calgary):")
        for r in outside.itertuples():
            print(f"      {r.station:<34} {round(r.geometry.distance(geom)):>7} m")
    kept = gdf[inside].drop(columns="geometry").copy()
    if len(kept) != IN_CITY_STATIONS_EXPECTED:
        print(f"  NOTE: expected {IN_CITY_STATIONS_EXPECTED} stations and got "
              f"{len(kept)} - the network has changed.")

    print("\nStations per line:")
    for short, name in LINE_NAMES.items():
        n = int(kept["lines"].fillna("").str.contains(name, regex=False).sum())
        print(f"  {name:<11}{n:>4}")
    shared = int(kept["lines"].fillna("").str.contains(",").sum())
    print(f"  served by both: {shared} (the 7 Avenue downtown trunk)")

    # --- spacing, measured: this is what settles the thinning question -----
    outer = RING_EDGES_METERS[-1]
    pts = gpd.GeoSeries(
        gpd.points_from_xy(kept["longitude"], kept["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).reset_index(drop=True)
    nn = np.array([pts.drop(index=i).distance(pts.iloc[i]).min()
                   for i in range(len(pts))])
    kept["nearest_station_m"] = np.round(nn, 1)
    print(f"\nStation spacing vs the {outer:.0f} m outer ring "
          f"(the thinning test):")
    print(f"  n={len(kept)}  median {np.median(nn):.0f} m  min {nn.min():.0f} m  "
          f"max {nn.max():.0f} m")
    print(f"  closer than the outer ring: {int((nn < outer).sum())}/{len(kept)}")
    print(f"  San Francisco's street-running median was 134 m and WAS thinned; "
          f"Montréal 728 m, Vancouver 841 m, D.C. 962 m, none thinned.")
    print("  tightest: " + ", ".join(
        f"{r.station} ({r.nearest_station_m:.0f} m)"
        for r in kept.nsmallest(5, "nearest_station_m").itertuples()))

    # --- outputs ------------------------------------------------------------
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    # Written even when empty: the file is part of the output contract, and an
    # empty one says "nothing was excluded" where a missing one says nothing.
    outside.drop(columns="geometry").assign(
        distance_outside_m=[round(r.distance(geom), 1) for r in outside.geometry]
        if len(outside) else pd.Series(dtype=float)
    )[["station", "latitude", "longitude", "lines", "distance_outside_m"]] \
        .to_csv(EXCLUDED_STATIONS_CSV, index=False)
    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    kept.sort_values("station")[["station", "latitude", "longitude"]].to_csv(
        STATIONS_CSV, index=False)
    print(f"\nWrote {len(kept)} stations to {STATIONS_CSV}")
    print(f"Wrote {EXCLUDED_STATIONS_CSV} ({len(outside)} excluded - the first "
          f"city in this project where that is zero)")


if __name__ == "__main__":
    main()
