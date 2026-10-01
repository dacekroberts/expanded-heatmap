"""Step 1 - Métro and REM stations inside the agglomeration of Montréal.

Input:  data/montreal/raw/gtfs.zip              (STM's own GTFS Static)
        data/montreal/raw/rem_gtfs.zip          (the REM's own feed, 2026-09-27)
        data/montreal/raw/agglomeration.geojson (34 features, dissolved)

THE REM JOINED ON 2026-09-27 (the tram rescope). Its stations come from its
own feed, collapse into the Métro's by name where the two meet
(Édouard-Montpetit, McGill), and are cut by the same boundary: the South Shore
and Laval / Deux-Montagnes ends fall outside, with the line drawn to them.
Everything below about the Métro predates it and still holds.
Output: data/montreal/processed/stations.csv
        outputs/montreal/excluded_stations.csv

THE STATION SCOPE IS ALMOST ALL IN, WHICH IS UNUSUAL HERE. 64 of 68 stations
are on the island; the other 4 are in Laval and Longueuil, whose own business
data would have to be sourced separately. Compare San Diego (16 of 63 out),
Los Angeles (54 of 110) and D.C. (58 of 98) - the Métro barely leaves its
city, which is part of why this city ranks well.

THREE THINGS WORTH KNOWING BEFORE CHANGING ANYTHING HERE.

  **The off-island cut is spatial, and it is CROSS-CHECKED against a
  structural marker.** The boundary polygon decides, per the project
  invariant - never a name list. But STM also appends " -Zone B" (its fare
  zone) to exactly the off-island stations, so this step asserts the two
  agree. If they ever diverge, one of them has changed and the run stops
  rather than quietly keeping or dropping four stations.

  **Display names come from the CHILD stops, not the parents.** Children are
  mixed case ("Station Angrignon"); parents are upper case ("STATION
  ANGRIGNON"), which on a map reads as shouting. Only the LEADING "Station "
  is stripped - a trailing-token rule is what turned Boston's "North Station"
  into "North", and this feed has "Square-Victoria-OACI" and
  "Université-de-Montréal" to lose.

  **No thinning.** The Métro is entirely underground and grade-separated, so
  this is D.C.'s and SkyTrain's shape. The spacing is MEASURED and printed
  rather than asserted, and it is tighter than Vancouver's - if that ever
  stops being acceptable the numbers will say so.

Run:  python pipeline/montreal/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.montreal.config import (  # noqa: E402
    BOUNDARY_AREA_KM2_MIN,
    BOUNDARY_FEATURES_EXPECTED,
    BOUNDARY_NAME_FIELD,
    BOUNDARY_TYPE_FIELD,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_ZIP,
    IN_CITY_STATIONS_EXPECTED,
    LINE_NAMES,
    INTERCHANGE_MAX_SPREAD_M,
    OFF_ISLAND_FARE_ZONE_SUFFIX,
    OPERATOR_STATION_COUNTS,
    REM_GTFS_ZIP,
    REM_ISLAND_ZONE,
    REM_LINE_KEY,
    REM_LINE_NAME,
    REM_ROUTE_IDS,
    REM_STATION_NAME_STRIP_PREFIX,
    RING_EDGES_METERS,
    ROUTE_IDS,
    STATION_NAME_STRIP_PREFIX,
    STATIONS_CSV,
    THINNED_GROUPS,
)
from pipeline.stations import check_operator_counts  # noqa: E402


def load(zip_path, filename, **kw):
    with zipfile.ZipFile(zip_path) as z, z.open(filename) as f:
        return pd.read_csv(f, dtype=str, **kw)


def rem_stations():
    """The REM's parent stations, from the operator's own feed.

    Parents (location_type 1) are already mixed case ("Station Du Ruisseau"),
    so unlike STM's they name themselves; the children carry " - Quai 1".
    `zone` is kept for the fare-zone cross-check in main().
    """
    routes = load(REM_GTFS_ZIP, "routes.txt")
    missing = sorted(set(REM_ROUTE_IDS) - set(routes["route_id"]))
    if missing:
        sys.exit(f"REM route_id(s) {missing} are not in its feed - the "
                 f"operator has renumbered; re-read routes.txt.")
    trips = load(REM_GTFS_ZIP, "trips.txt")
    trips = trips[trips["route_id"].isin(REM_ROUTE_IDS)]
    stop_times = load(REM_GTFS_ZIP, "stop_times.txt", usecols=["trip_id", "stop_id"])
    stops = load(REM_GTFS_ZIP, "stops.txt")
    served = set(stop_times.loc[stop_times["trip_id"].isin(set(trips["trip_id"])),
                                "stop_id"])
    children = stops[stops["stop_id"].isin(served)]
    if children["parent_station"].isna().any():
        sys.exit("a served REM platform has no parent_station.")
    p = stops[stops["stop_id"].isin(set(children["parent_station"]))].copy()
    p["station"] = (p["stop_name"].str.strip()
                    .str.replace(f"^{REM_STATION_NAME_STRIP_PREFIX}", "", regex=True)
                    .str.strip())
    p["latitude"] = p["stop_lat"].astype(float)
    p["longitude"] = p["stop_lon"].astype(float)
    p["lines"] = REM_LINE_NAME
    p["feed"] = "REM"
    p["zone"] = p["zone_id"]
    print(f"\nREM: {len(children)} served platforms -> {len(p)} stations "
          f"(routes {', '.join(REM_ROUTE_IDS)})")
    return p[["stop_id", "station", "latitude", "longitude", "lines", "feed", "zone"]]


def collapse_interchanges(metro, rem):
    """One station per interchange, by NAME (Copenhagen's rule).

    A REM station named like a Métro station is the same interchange: the
    two collapse to the Métro's point, the lines are joined, and the spread
    is printed so a merge of two different places cannot pass silently. A
    spread past config.INTERCHANGE_MAX_SPREAD_M stops the run. The Métro's
    point is kept so the 62 Métro-only stations and the two interchanges keep
    the rings they were published with.
    """
    shared = sorted(set(metro["station"]) & set(rem["station"]))
    print(f"\nInterchanges collapsed by name ({len(shared)}):")
    for name in shared:
        m = metro[metro["station"] == name].iloc[0]
        r = rem[rem["station"] == name].iloc[0]
        pts = gpd.GeoSeries(gpd.points_from_xy([m.longitude, r.longitude],
                                               [m.latitude, r.latitude]),
                            crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
        spread = pts.iloc[0].distance(pts.iloc[1])
        print(f"  {name:<24} spread {spread:>5.0f} m")
        if spread > INTERCHANGE_MAX_SPREAD_M:
            sys.exit(f"  {name}: the Métro and REM stations are {spread:.0f} m "
                     f"apart, past the {INTERCHANGE_MAX_SPREAD_M:.0f} m limit. "
                     f"Same name, different place? Decide before collapsing.")
        metro.loc[metro["station"] == name, "lines"] = f"{m.lines}, {r.lines}"
        metro.loc[metro["station"] == name, "feed"] = "STM+REM"
    rem = rem[~rem["station"].isin(shared)]
    return pd.concat([metro, rem], ignore_index=True)


def main():
    for path in (GTFS_ZIP, REM_GTFS_ZIP, CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/montreal/fetch_sources.py first.")
    if THINNED_GROUPS:
        sys.exit(f"config.THINNED_GROUPS is {set(THINNED_GROUPS)} but this step "
                 f"implements no thinning. The Métro is grade-separated "
                 f"throughout; port Boston's filters rather than leaving the "
                 f"setting inert.")

    # --- routes -------------------------------------------------------------
    routes = load(GTFS_ZIP, "routes.txt")
    matched = routes[routes["route_id"].isin(ROUTE_IDS)]
    missing = sorted(set(ROUTE_IDS) - set(matched["route_id"]))
    if missing:
        sys.exit(f"route_id(s) {missing} are not in this feed - check "
                 f"routes.txt.")
    non_rail = matched[matched["route_type"] != "1"]
    if len(non_rail):
        sys.exit(f"route_type != 1 on {list(non_rail['route_id'])}. The STM "
                 f"runs the Métro and buses only, so this should not happen.")
    print("Routes drawn (exact route_id match):")
    for r in matched.sort_values("route_id").itertuples():
        print(f"  {r.route_id:<4} {LINE_NAMES[r.route_id]:<18} "
              f"route_type={r.route_type}  official route_color=#{r.route_color}")

    # --- platforms -> parent stations ---------------------------------------
    trips = load(GTFS_ZIP, "trips.txt")
    stop_times = load(GTFS_ZIP, "stop_times.txt",
                      usecols=["trip_id", "stop_id"])
    stops = load(GTFS_ZIP, "stops.txt")

    keep_trips = trips[trips["route_id"].isin(ROUTE_IDS)]
    served = stop_times[stop_times["trip_id"].isin(set(keep_trips["trip_id"]))]
    children = stops[stops["stop_id"].isin(set(served["stop_id"]))].copy()
    if children["parent_station"].isna().any():
        sys.exit("a served platform has no parent_station; the collapse below "
                 "would invent stations. Vancouver's suffix-stripping approach "
                 "is the fallback if STM ever stops publishing them.")

    # Mixed-case display name, from the child, leading prefix only.
    children["display"] = (children["stop_name"].str.strip()
                           .str.replace(f"^{STATION_NAME_STRIP_PREFIX}", "",
                                        regex=True).str.strip())
    blank = children["display"].eq("")
    if blank.any():
        sys.exit(f"{int(blank.sum())} platform name(s) stripped to nothing.")

    name_of = children.groupby("parent_station")["display"].first()
    parents = stops[stops["stop_id"].isin(set(children["parent_station"]))].copy()
    parents["station"] = parents["stop_id"].map(name_of)
    parents["latitude"] = parents["stop_lat"].astype(float)
    parents["longitude"] = parents["stop_lon"].astype(float)
    print(f"\n{len(children)} served platforms -> {len(parents)} parent stations")
    dupes = parents["station"][parents["station"].duplicated()].tolist()
    if dupes:
        sys.exit(f"two parent stations share a display name: {dupes}.")

    # --- which lines serve each station -------------------------------------
    trip_to_route = dict(zip(keep_trips["trip_id"], keep_trips["route_id"]))
    parent_of = dict(zip(children["stop_id"], children["parent_station"]))
    st = served.assign(parent=served["stop_id"].map(parent_of),
                       line=served["trip_id"].map(trip_to_route).map(LINE_NAMES))
    parents["lines"] = parents["stop_id"].map(
        st.groupby("parent")["line"].apply(lambda s: ", ".join(sorted(set(s.dropna())))))
    parents["feed"] = "STM"

    parents = collapse_interchanges(parents, rem_stations())

    # --- the boundary -------------------------------------------------------
    b = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    x0, y0, _, _ = b.total_bounds
    if not (-180 <= x0 <= 180 and -90 <= y0 <= 90):
        sys.exit(f"boundary bounds {b.total_bounds} are not degrees - the "
                 f"NAD83/MTM resource was downloaded instead of the WGS 84 one.")
    if len(b) != BOUNDARY_FEATURES_EXPECTED:
        print(f"  NOTE: boundary has {len(b)} features, expected "
              f"{BOUNDARY_FEATURES_EXPECTED}")
    types = b[BOUNDARY_TYPE_FIELD].value_counts().to_dict()
    print(f"\nBoundary: {len(b)} features {types}")
    geom = b.to_crs(CRS_PROJECTED).union_all()
    area = geom.area / 1e6
    print(f"  dissolved to {geom.geom_type}, {area:.1f} km2 "
          f"(the agglomeration's LAND area is ~499; this layer follows the "
          f"river channel, so a tight check is not possible here)")
    if area < BOUNDARY_AREA_KM2_MIN:
        sys.exit(f"  dissolved area {area:.1f} km2 is below the "
                 f"{BOUNDARY_AREA_KM2_MIN} floor - features are missing.")

    gdf = gpd.GeoDataFrame(
        parents,
        geometry=gpd.points_from_xy(parents["longitude"], parents["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    inside = gdf.geometry.within(geom)

    # The cross-checks: the spatial cut must agree with each feed's own fare
    # zone - STM's suffix on the Métro, ARTM's zone_id on the REM.
    stm = gdf["feed"].ne("REM")
    zone_b = gdf["station"].str.endswith(OFF_ISLAND_FARE_ZONE_SUFFIX)
    if set(gdf.loc[stm & ~inside, "station"]) != set(gdf.loc[stm & zone_b, "station"]):
        sys.exit(
            "THE SPATIAL CUT AND STM'S FARE ZONE DISAGREE.\n"
            f"  outside the boundary: {sorted(gdf.loc[stm & ~inside, 'station'])}\n"
            f"  marked '{OFF_ISLAND_FARE_ZONE_SUFFIX.strip()}': "
            f"{sorted(gdf.loc[stm & zone_b, 'station'])}\n"
            "  One of them has changed. Decide which is right rather than "
            "letting four stations in or out silently."
        )
    print(f"  spatial cut agrees with STM's '{OFF_ISLAND_FARE_ZONE_SUFFIX.strip()}' "
          f"marking on all {int(stm.sum())} STM stations")
    rem = gdf["feed"].eq("REM")
    zoned = rem & gdf["zone"].notna()
    island = gdf["zone"].eq(REM_ISLAND_ZONE)
    if not (inside[zoned] == island[zoned]).all():
        bad = gdf.loc[zoned & (inside != island), "station"].tolist()
        sys.exit(f"THE SPATIAL CUT AND THE REM'S zone_id DISAGREE on {bad}. "
                 f"Zone {REM_ISLAND_ZONE} is ARTM's zone A, the island.")
    print(f"  spatial cut agrees with the REM's zone_id on {int(zoned.sum())} "
          f"zoned REM stations; no zone in this feed (checked spatially only): "
          f"{sorted(gdf.loc[rem & ~zoned, 'station'])}")

    gdf["distance_outside_m"] = [
        0.0 if ins else round(p.distance(geom), 1)
        for ins, p in zip(inside, gdf.geometry)]

    kept = gdf[inside].drop(columns="geometry").copy()
    excluded = gdf[~inside].drop(columns="geometry").copy()
    # The fare-zone suffix is a data artefact, not part of a station's name.
    excluded["station"] = excluded["station"].str.replace(
        OFF_ISLAND_FARE_ZONE_SUFFIX, "", regex=False)
    print(f"\n{len(kept)} of {len(gdf)} stations are in the agglomeration "
          f"({len(kept) / len(gdf):.1%}); {len(excluded)} are not.")
    if len(kept) != IN_CITY_STATIONS_EXPECTED:
        print(f"  NOTE: expected {IN_CITY_STATIONS_EXPECTED} in-city stations "
              f"and got {len(kept)} - the network has changed.")
    print("\nExcluded (off the island), with how far outside:")
    for r in excluded.sort_values("distance_outside_m").itertuples():
        print(f"  {r.station:<38} {r.distance_outside_m:>8.0f} m   {r.lines}")

    print("\nIn-scope stations per line (no line drops out of the map):")
    for name in [*LINE_NAMES.values(), REM_LINE_NAME]:
        n = int(kept["lines"].fillna("").str.contains(name, regex=False).sum())
        total = int(gdf["lines"].fillna("").str.contains(name, regex=False).sum())
        print(f"  {name:<18}{n:>4} of {total:>3}")

    # --- gate 3: whole lines, before the island cut, against the operators ---
    print("\nGate 3 - whole lines (before the island cut):")
    line_names = {**LINE_NAMES, REM_LINE_KEY: REM_LINE_NAME}
    actual_per_line = {
        key: int(gdf["lines"].fillna("").str.contains(name, regex=False).sum())
        for key, name in line_names.items()}
    check_operator_counts(OPERATOR_STATION_COUNTS, actual_per_line)

    # --- spacing, measured against the outer ring ---------------------------
    outer = RING_EDGES_METERS[-1]
    pts = gpd.GeoSeries(
        gpd.points_from_xy(kept["longitude"], kept["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).reset_index(drop=True)
    nn = np.array([pts.drop(index=i).distance(pts.iloc[i]).min()
                   for i in range(len(pts))])
    kept["nearest_station_m"] = np.round(nn, 1)
    print(f"\nStation spacing vs the {outer:.0f} m outer ring (the thinning test):")
    print(f"  n={len(kept)}  median {np.median(nn):.0f} m  min {nn.min():.0f} m  "
          f"max {nn.max():.0f} m")
    print(f"  closer than the outer ring: {int((nn < outer).sum())}/{len(kept)} - "
          f"their rings overlap, and each business is assigned to its nearest "
          f"station so nothing is double-counted.")
    print(f"  Tighter than Vancouver (median 841 m) and D.C. (962 m), both "
          f"unthinned; far looser than San Francisco's street-running 134 m, "
          f"which was thinned.")
    print("  tightest: " + ", ".join(
        f"{r.station} ({r.nearest_station_m:.0f} m)"
        for r in kept.nsmallest(4, "nearest_station_m").itertuples()))

    # --- outputs ------------------------------------------------------------
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded.sort_values("station")[
        ["station", "latitude", "longitude", "lines", "distance_outside_m"]
    ].to_csv(EXCLUDED_STATIONS_CSV, index=False)
    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    kept.sort_values("station")[["station", "latitude", "longitude"]].to_csv(
        STATIONS_CSV, index=False)
    print(f"\nWrote {len(kept)} stations to {STATIONS_CSV}")
    print(f"Wrote {EXCLUDED_STATIONS_CSV} ({len(excluded)} off-island stations)")


if __name__ == "__main__":
    main()
