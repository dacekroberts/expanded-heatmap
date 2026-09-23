"""Step 1 - TTC rapid-transit stations: three subway lines and two LRT lines.

Input:  data/toronto/raw/gtfs.zip                     (the CITY's CKAN copy)
        data/toronto/raw/toronto_boundary_wgs84.zip
Output: data/toronto/processed/stations.csv
        outputs/toronto/excluded_stations.csv          (2 rows - see below)

THIS CITY IS WHY THE PROJECT DISTRUSTS STATION COUNTS, AND IT GOT THE NUMBER
WRONG TWICE.

`parent_station` is not populated on a single stop, so the best of this
project's four collapse mechanisms is unavailable and the names must be munged.
Every Toronto figure before 2026-09-21 rested on **234 "stations" that were
platforms**. The correction of that error then made a smaller one of the same
kind, because **three naming conventions live in this one feed**:

    subway HYPHENATES    "Finch Station - Southbound Platform"
    LRT DOES NOT         "Aga Khan Park & Museum Station Eastbound Platform"
    Union names its
    DESTINATION          "Union Station - Northbound Platform Towards Finch"
    and one bare form    "Finch West Station LRT Platform"

A pattern written for the subway leaves all 86 LRT platforms uncollapsed, which
gives 160 "stations" at a 70 m nearest-neighbour median - platform spacing. And
three stations appear TWICE, once plain and once suffixed `- Subway`
(`Kipling Station` against `Kipling Station - Subway`, 33 m apart).

**The collapse is checked by `pipeline/stations.py`, not here**, and that is
the actual lesson: this check was written five separate times for five Canadian
cities and was absent or wrong in four of them. Three gates - spacing,
boardability, and the operator's own published counts. All five of Toronto's
lines now match the TTC exactly (38/31/5/25/18); its old 77 and 118 matched
nothing published.

**Toronto also has NO non-revenue stops** - `pickup_type` and `drop_off_type`
are boardable on every rail stop_time. Checked, because Edmonton's feed hid two
garages and a tail track among its 33 stations, and a verified absence and an
unexamined one look identical afterwards.

STREETCARS ARE OUT OF SCOPE, and that is a decision: the TTC codes its 18
streetcar routes at `route_type 0` alongthe two LRT lines, and adding them
takes the network to 913 platforms / 706 names - San Francisco's shape, needing
`docs/sub_transit_line_filters.md`. `^Line \\d` separates LRT from streetcar,
which this brief once called a research problem and is a regex.

Run:  python pipeline/toronto/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.baseline import emit  # noqa: E402
from pipeline.stations import nearest_neighbour_m, verify_stations  # noqa: E402
from pipeline.toronto.config import (  # noqa: E402
    CITY_BOUNDARY_ZIP,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_ZIP,
    IN_CITY_STATIONS_EXPECTED,
    LINE_NAMES,
    LRT_NAME_REGEX,
    LRT_ROUTE_TYPE,
    NON_REVENUE_STOPS_EXPECTED,
    PLATFORM_SPACING_MEDIAN_M_MAX,
    PLATFORMS_EXPECTED,
    PUBLISHED_STATIONS_PER_LINE,
    RING_EDGES_METERS,
    ROUTE_IDS_EXPECTED,
    STATION_SPACING_MEDIAN_M_MIN,
    STATIONS_COLLAPSED_EXPECTED,
    STATION_STRIP_PATTERNS,
    STATIONS_CSV,
    SUBWAY_ONLY_STATIONS_EXPECTED,
    SUBWAY_ROUTE_TYPE,
)


def load(zip_path, filename, **kw):
    with zipfile.ZipFile(zip_path) as z, z.open(filename) as f:
        return pd.read_csv(f, dtype=str, **kw)


def collapse_names(names):
    """Strip every platform-naming convention this feed uses, in order."""
    s = names.str.strip()
    for pat in STATION_STRIP_PATTERNS:
        s = s.str.replace(pat, "", regex=True)
    return s.str.replace(r"\s+", " ", regex=True).str.strip()


def main():
    for path in (GTFS_ZIP, CITY_BOUNDARY_ZIP):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/toronto/fetch_sources.py first.")

    # --- routes: subway by type, LRT by NAME, streetcars excluded ----------
    routes = load(GTFS_ZIP, "routes.txt")
    by_type = routes["route_type"].value_counts().to_dict()
    print(f"Feed route_type counts: {by_type}")
    if by_type.get(SUBWAY_ROUTE_TYPE, 0) == 0:
        sys.exit(
            f"NO route_type {SUBWAY_ROUTE_TYPE} routes in this feed. That is "
            f"the Mobility Database mirror's signature failure - its copy of "
            f"this feed was three months expired and contained no subway at "
            f"all. Use the City's own CKAN package (config.GTFS_URL)."
        )
    subway = routes[routes["route_type"] == SUBWAY_ROUTE_TYPE]
    lrt = routes[(routes["route_type"] == LRT_ROUTE_TYPE)
                 & routes["route_long_name"].fillna("").str.match(LRT_NAME_REGEX)]
    streetcars = routes[(routes["route_type"] == LRT_ROUTE_TYPE)
                        & ~routes["route_long_name"].fillna("").str.match(LRT_NAME_REGEX)]
    rail = pd.concat([subway, lrt])
    print(f"\n{len(subway)} subway routes (route_type {SUBWAY_ROUTE_TYPE}) + "
          f"{len(lrt)} LRT (route_type {LRT_ROUTE_TYPE} matching "
          f"{LRT_NAME_REGEX!r}) = {len(rail)} drawn")
    print(f"  {len(streetcars)} streetcar routes EXCLUDED as out of scope: "
          f"{', '.join(sorted(streetcars['route_long_name'].fillna('?'))[:6])}...")
    for r in rail.sort_values("route_id").itertuples():
        name = LINE_NAMES.get(r.route_id, r.route_long_name)
        print(f"    {r.route_id:<3} {name:<26} route_type={r.route_type}")
    missing = sorted(set(LINE_NAMES) - set(rail["route_id"]))
    if missing:
        sys.exit(f"config.LINE_NAMES has route_id(s) {missing} that this feed "
                 f"does not carry.")
    if len(rail) != ROUTE_IDS_EXPECTED:
        print(f"  NOTE: {len(rail)} rail routes, expected {ROUTE_IDS_EXPECTED}")

    # --- shape candidates, so LINE_SHAPES can be filled from evidence ------
    trips = load(GTFS_ZIP, "trips.txt")
    keep = trips[trips["route_id"].isin(set(rail["route_id"]))]
    print("\nTrips per shape, per line (the mode is the primary alignment):")
    for rid in sorted(rail["route_id"]):
        tt = keep[keep["route_id"] == rid]
        vc = tt["shape_id"].value_counts()
        print(f"  {LINE_NAMES.get(rid, rid)} ({rid}): {len(tt):,} trips, "
              f"{len(vc)} shapes")
        for sid, n in vc.head(3).items():
            print(f"      {sid:<22} {n:>5} trips")

    # --- served stops = PLATFORMS ------------------------------------------
    st = load(GTFS_ZIP, "stop_times.txt",
              usecols=lambda c: c in {"trip_id", "stop_id", "pickup_type",
                                      "drop_off_type"})
    st = st[st["trip_id"].isin(set(keep["trip_id"]))]
    stops = load(GTFS_ZIP, "stops.txt")
    served = stops[stops["stop_id"].isin(set(st["stop_id"]))].copy()
    served["latitude"] = served["stop_lat"].astype(float)
    served["longitude"] = served["stop_lon"].astype(float)
    print(f"\n{len(served)} served stops - these are PLATFORMS, not stations")
    if len(served) != PLATFORMS_EXPECTED:
        print(f"  NOTE: expected {PLATFORMS_EXPECTED}")

    has_parent = ("parent_station" in served.columns
                  and served["parent_station"].notna().any())
    print(f"  parent_station populated: {has_parent}"
          + ("" if has_parent else " - so the NAMES must be collapsed, and two "
                                   "conventions live in this feed"))
    if has_parent:
        print("  NOTE: parent_station is now populated, which it was not on "
              "2026-09-21. Prefer it over the name patterns and re-check the "
              "spacing afterwards.")

    # --- boardability: Edmonton's lesson, applied as a check --------------
    if {"pickup_type", "drop_off_type"} <= set(st.columns):
        b = ((st["pickup_type"].fillna("0") == "0")
             | (st["drop_off_type"].fillna("0") == "0"))
        boardable = set(st.loc[b, "stop_id"])
        non_rev = served[~served["stop_id"].isin(boardable)]
    else:
        non_rev = served.iloc[0:0]
    print(f"  boardable: {len(served) - len(non_rev)} of {len(served)}")
    if len(non_rev) != NON_REVENUE_STOPS_EXPECTED:
        print(f"  {len(non_rev)} NON-REVENUE platforms, expected "
              f"{NON_REVENUE_STOPS_EXPECTED} - a trip stops there but nobody "
              f"can board:")
        for r in non_rev.itertuples():
            print(f"      {r.stop_name}")
    served = served[served["stop_id"].isin(boardable)].copy() if len(non_rev) else served

    # --- collapse, then CHECK the collapse two ways -----------------------
    served["station"] = collapse_names(served["stop_name"])
    blank = served["station"].eq("")
    if blank.any():
        sys.exit(f"{int(blank.sum())} stop name(s) normalised to nothing - a "
                 f"strip pattern is too greedy.")

    subway_only = served[served["stop_id"].isin(
        set(st[st["trip_id"].isin(set(keep[keep["route_id"].isin(
            set(subway["route_id"]))]["trip_id"]))]["stop_id"]))]
    n_subway = subway_only["station"].nunique()

    stations = served.groupby("station").agg(
        latitude=("latitude", "mean"),
        longitude=("longitude", "mean"),
        platforms=("stop_id", "size")).reset_index()
    print(f"\n{len(served)} platforms -> {len(stations)} stations")
    print(f"  subway only: {len(subway_only)} platforms -> {n_subway} stations "
          f"(the TTC publishes 38 + 31 + 5 less 3 interchanges = 71)")
    if n_subway != SUBWAY_ONLY_STATIONS_EXPECTED:
        print(f"  NOTE: subway-only expected {SUBWAY_ONLY_STATIONS_EXPECTED}")
    # `stations` here is the COLLAPSED set, before the boundary filter - 110,
    # not the 108 that survive it. This compared it against
    # IN_CITY_STATIONS_EXPECTED until 2026-09-22, so it printed a NOTE on every
    # single run and STATIONS_COLLAPSED_EXPECTED sat unused, which is how the
    # mis-wiring was found: a dead-constant sweep asked why nothing read it.
    if len(stations) != STATIONS_COLLAPSED_EXPECTED:
        print(f"  NOTE: expected {STATIONS_COLLAPSED_EXPECTED} stations. A "
              f"pattern written only for the subway's hyphenated names gives "
              f"160 here; check STATION_STRIP_PATTERNS against the spacing "
              f"below rather than adjusting this number.")

    # --- which lines serve each station, needed for gate 3 ----------------
    trip_to_route = dict(zip(keep["trip_id"], keep["route_id"]))
    stop_to_station = dict(zip(served["stop_id"], served["station"]))
    sl = st.assign(station=st["stop_id"].map(stop_to_station),
                   line=st["trip_id"].map(trip_to_route).map(LINE_NAMES))
    stations["lines"] = stations["station"].map(
        sl.dropna(subset=["station"]).groupby("station")["line"].apply(
            lambda s: ", ".join(sorted(set(s.dropna())))))
    print("\nStations per line:")
    for rid, name in LINE_NAMES.items():
        n = int(stations["lines"].fillna("").str.contains(name, regex=False).sum())
        print(f"  {name:<26}{n:>4}")
    print(f"  served by more than one: "
          f"{int(stations['lines'].fillna('').str.contains(',').sum())}")

    # --- the three shared gates -------------------------------------------
    # pipeline/stations.py rather than inline, because this check was written
    # five separate times for five Canadian cities and was absent or wrong in
    # four of them. The collapse above stays per-city - the feeds genuinely
    # differ - but the verification does not.
    actual_per_line = {
        name: int(stations["lines"].fillna("").str.contains(name,
                                                            regex=False).sum())
        for name in LINE_NAMES.values()
    }
    st_nn = nearest_neighbour_m(stations["longitude"], stations["latitude"],
                                CRS_PROJECTED)
    stations["nearest_station_m"] = np.round(st_nn, 1)
    print()
    verify_stations(
        city="Toronto", platforms=served, stations=stations,
        crs_projected=CRS_PROJECTED,
        expected_per_line=PUBLISHED_STATIONS_PER_LINE,
        actual_per_line=actual_per_line,
        non_revenue=len(non_rev),
        spacing_min=STATION_SPACING_MEDIAN_M_MIN,
        platform_max=PLATFORM_SPACING_MEDIAN_M_MAX,
    )
    outer = RING_EDGES_METERS[-1]
    print(f"    closer than the {outer:.0f} m outer ring: "
          f"{int((st_nn < outer).sum())}/{len(stations)}")
    print("    tightest: " + ", ".join(
        f"{r.station} ({r.nearest_station_m:.0f} m)"
        for r in stations.nsmallest(4, "nearest_station_m").itertuples()))

    # --- the boundary: a CHECK ---------------------------------------------
    b = gpd.read_file(CITY_BOUNDARY_ZIP)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    geom = b.to_crs(CRS_PROJECTED).union_all()
    print(f"\nBoundary: {len(b)} feature(s), {geom.area / 1e6:.1f} km2")
    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    inside = gdf.geometry.within(geom)
    outside = gdf[~inside]
    print(f"  inside Toronto: {int(inside.sum())} of {len(gdf)}")
    for r in outside.itertuples():
        print(f"      OUTSIDE: {r.station:<34} "
              f"{round(r.geometry.distance(geom)):>7} m")
    kept = gdf[inside].drop(columns="geometry").copy()
    if len(kept) != IN_CITY_STATIONS_EXPECTED:
        print(f"  NOTE: expected {IN_CITY_STATIONS_EXPECTED} in-city stations")

    # --- outputs ------------------------------------------------------------
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    outside.drop(columns="geometry").assign(
        distance_outside_m=[round(r.distance(geom), 1) for r in outside.geometry]
        if len(outside) else pd.Series(dtype=float)
    )[["station", "latitude", "longitude", "lines", "distance_outside_m"]] \
        .to_csv(EXCLUDED_STATIONS_CSV, index=False)
    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    kept.sort_values("station")[["station", "latitude", "longitude"]].to_csv(
        STATIONS_CSV, index=False)
    # Watched by drift_check against outputs/toronto/baseline.json - these are
    # the figures that can move while the rendered map still looks plausible.
    emit("platforms", len(served))
    emit("stations_collapsed", len(stations))
    emit("stations_in_city", len(kept))
    print(f"\nWrote {len(kept)} stations to {STATIONS_CSV}")
    print(f"Wrote {EXCLUDED_STATIONS_CSV} ({len(outside)} excluded)")


if __name__ == "__main__":
    main()
