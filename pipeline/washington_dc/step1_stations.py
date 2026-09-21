"""Step 1 - WMATA Metrorail stations inside the District.

Input:  data/washington_dc/raw/gtfs.zip              (WMATA Rail GTFS Static)
        data/washington_dc/raw/city_boundary.geojson (DC Boundary, layer 10)
        data/washington_dc/raw/states.geojson        (Census TIGERweb states)
Output: data/washington_dc/processed/stations.csv
        outputs/washington_dc/excluded_stations.csv

THE BOUNDARY CUT IS THE BIG NUMBER HERE. Metrorail is 98 stations and reaches
deep into Maryland and Virginia, so most of the network is out of scope: the
District's business register covers the District only, and stations elsewhere
would need those jurisdictions' own registries, sourced and verified
separately. That is a new project, not a config change - except where the owner
has decided otherwise, as for Seattle.

So this step names the state each dropped station sits in rather than just
counting them, which is why a states layer is downloaded at all. San Diego's 16
and Los Angeles' 54 set that standard.

TWO THINGS THIS STEP DOES *NOT* DO, both deliberate:

  No thinning. Metrorail is grade-separated heavy rail end to end with no
  street-running segment, so it is San Diego's and New York's shape rather than
  San Francisco's. The spacing is MEASURED and printed below rather than
  asserted, so if that ever stops being true the number says so.

  No name surgery. `parent_station` is populated on all 125 platforms, so the
  98 stations collapse cleanly, and config.STATION_SUFFIX_PATTERN is None on
  purpose: "Union Station" and "Metro Center" are real station names, and
  Boston's bug was a pattern that stripped a trailing " Station" and turned
  "North Station" into "North".

Run:  python pipeline/washington_dc/step1_stations.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.washington_dc.config import (  # noqa: E402
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_ZIP,
    LINE_NAMES,
    RING_EDGES_METERS,
    ROUTE_GROUPS,
    STATES_GEOJSON,
    STATES_NAME_FIELD,
    STATIONS_CSV,
    STATION_NAME_ALIASES,
    STATION_SUFFIX_PATTERN,
    THINNED_GROUPS,
)

ROUTE_TO_GROUP = {r: g for g, routes in ROUTE_GROUPS.items() for r in routes}


def load(zip_path, filename):
    with zipfile.ZipFile(zip_path) as z, z.open(filename) as f:
        return pd.read_csv(f, dtype=str)


def canonical(stop_name: str) -> str:
    name = str(stop_name).strip()
    return STATION_NAME_ALIASES.get(name, name)


def main():
    for path in (GTFS_ZIP, CITY_BOUNDARY_GEOJSON, STATES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/washington_dc/fetch_sources.py first.")
    if STATION_SUFFIX_PATTERN is not None:
        sys.exit("config.STATION_SUFFIX_PATTERN is set. This feed needs no "
                 "suffix stripping, and stripping ' Station' would break "
                 "'Union Station' - see this file's docstring.")
    if THINNED_GROUPS:
        sys.exit(f"config.THINNED_GROUPS is {set(THINNED_GROUPS)}, but this "
                 f"step implements no thinning. Metrorail is grade-separated "
                 f"throughout; if that changed, port Boston's filters rather "
                 f"than leaving the setting inert.")

    routes = load(GTFS_ZIP, "routes.txt")
    matched = routes[routes["route_id"].isin(ROUTE_TO_GROUP)]
    missing = set(ROUTE_TO_GROUP) - set(matched["route_id"])
    if missing:
        sys.exit(f"route_id(s) {sorted(missing)} are not in this feed - check "
                 f"routes.txt. Note WMATA's feed is only valid for ten days, "
                 f"so re-fetch before assuming a route was withdrawn.")
    non_rail = matched[matched["route_type"] != "1"]
    if len(non_rail):
        sys.exit(f"route_type != 1 on {list(non_rail['route_id'])} - this is "
                 f"the Rail feed, so a non-rail route means the combined "
                 f"Rail & Bus operation was downloaded by mistake.")
    print("Routes drawn (exact route_id match):")
    for r in matched.sort_values("route_id").itertuples():
        print(f"  {r.route_id:<8} {LINE_NAMES[ROUTE_TO_GROUP[r.route_id]][0]:<14} "
              f"route_type={r.route_type}  official route_color=#{r.route_color}")

    trips = load(GTFS_ZIP, "trips.txt")
    stop_times = load(GTFS_ZIP, "stop_times.txt")
    stops = load(GTFS_ZIP, "stops.txt")

    # --- platforms -> parent stations ---------------------------------------
    keep_trips = trips[trips["route_id"].isin(ROUTE_TO_GROUP)]
    served = stop_times[stop_times["trip_id"].isin(set(keep_trips["trip_id"]))]
    platform_ids = set(served["stop_id"])
    platforms = stops[stops["stop_id"].isin(platform_ids)].copy()
    if platforms["parent_station"].isna().any() or \
            (platforms["parent_station"].fillna("") == "").any():
        sys.exit("a served platform has no parent_station; the collapse below "
                 "would silently invent stations.")

    parents = stops[stops["location_type"] == "1"].copy()
    parents["station"] = parents["stop_name"].map(canonical)
    parents["latitude"] = parents["stop_lat"].astype(float)
    parents["longitude"] = parents["stop_lon"].astype(float)
    served_parents = set(platforms["parent_station"])
    stations = parents[parents["stop_id"].isin(served_parents)].copy()
    print(f"\n{len(platforms)} served platforms -> {len(stations)} parent "
          f"stations")
    dupes = stations["station"][stations["station"].duplicated()].tolist()
    if dupes:
        sys.exit(f"two parent stations share a name: {dupes}. Add an alias "
                 f"rather than letting them merge.")

    # --- which lines serve each station -------------------------------------
    trip_to_group = {t: ROUTE_TO_GROUP[r] for t, r in
                     zip(keep_trips["trip_id"], keep_trips["route_id"])}
    parent_of = dict(zip(platforms["stop_id"], platforms["parent_station"]))
    st = served[["trip_id", "stop_id"]].assign(
        group=served["trip_id"].map(trip_to_group),
        parent=served["stop_id"].map(parent_of))
    groups_by_parent = st.groupby("parent")["group"].apply(
        lambda s: ", ".join(sorted({LINE_NAMES[g][0] for g in s})))
    stations["lines"] = stations["stop_id"].map(groups_by_parent)

    # --- inside the District? ----------------------------------------------
    dc = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    dc = dc.set_crs(CRS_GEOGRAPHIC) if dc.crs is None else dc.to_crs(CRS_GEOGRAPHIC)
    if len(dc) != 1:
        sys.exit(f"boundary has {len(dc)} features, expected 1.")
    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC)
    inside = gdf.within(dc.geometry.iloc[0])

    # How far outside is each dropped station? Step 0 found the closest at
    # ~40 m, so this is printed rather than trusted to a tolerance.
    dc_proj = dc.to_crs(CRS_PROJECTED).geometry.iloc[0]
    gdf["distance_outside_m"] = [
        0.0 if ins else round(p.distance(dc_proj), 1)
        for ins, p in zip(inside, gdf.to_crs(CRS_PROJECTED).geometry)]

    # Which state is each dropped station in? Naming beats measuring - the
    # Boston lesson.
    states = gpd.read_file(STATES_GEOJSON)
    states = (states.set_crs(CRS_GEOGRAPHIC) if states.crs is None
              else states.to_crs(CRS_GEOGRAPHIC))
    located = gpd.sjoin(gdf[["geometry"]], states[[STATES_NAME_FIELD, "geometry"]],
                        predicate="within", how="left")
    located = located[~located.index.duplicated()]
    gdf["state"] = located[STATES_NAME_FIELD].fillna("(unmatched)")

    kept = gdf[inside].drop(columns=["geometry"]).copy()
    excluded = gdf[~inside].drop(columns=["geometry"]).copy()
    print(f"\n{len(kept)} of {len(gdf)} stations are inside the District "
          f"({len(kept)/len(gdf):.1%}); {len(excluded)} are not.")
    print("\nExcluded stations by state:")
    print("  " + excluded["state"].value_counts().to_string().replace("\n", "\n  "))
    print("\nThe five closest exclusions (a tolerance would have to separate "
          "these, and does not need to - each is named):")
    for r in excluded.nsmallest(5, "distance_outside_m").itertuples():
        print(f"  {r.station:<26} {r.distance_outside_m:>8.1f} m outside, "
              f"in {r.state}")
    print("\nIn-District stations per line (none of the six drops out of the "
          "map):")
    for group, (name, _) in LINE_NAMES.items():
        n = int(kept["lines"].fillna("").str.contains(name, regex=False).sum())
        total = int(gdf["lines"].fillna("").str.contains(name, regex=False).sum())
        print(f"  {name:<14}{n:>4} of {total:>3}")

    # --- station spacing, measured against the outer ring -------------------
    outer = RING_EDGES_METERS[-1]
    pts = gpd.GeoSeries(
        gpd.points_from_xy(kept["longitude"], kept["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    nearest = []
    for i in range(len(pts)):
        d = pts.distance(pts.iloc[i])
        nearest.append(d[d.index != d.index[i]].min())
    kept["nearest_station_m"] = [round(v, 1) for v in nearest]
    closer = int((kept["nearest_station_m"] < outer).sum())
    print(f"\nStation spacing vs the {outer:.0f} m outer ring "
          f"(the thinning test):")
    print(f"  n={len(kept)}  median nearest "
          f"{kept['nearest_station_m'].median():.0f} m  "
          f"min {kept['nearest_station_m'].min():.0f} m  "
          f"max {kept['nearest_station_m'].max():.0f} m")
    print(f"  closer than the outer ring: {closer}/{len(kept)} - their rings "
          f"overlap, and each business is assigned to its nearest station so "
          f"nothing is double-counted.")
    print(f"  For comparison: San Francisco's street-running median was 134 m "
          f"(thinned), Boston's Mattapan 518 m and New York's 482 m (not "
          f"thinned).")
    tightest = kept.nsmallest(5, "nearest_station_m")
    print("  tightest pairs: " + ", ".join(
        f"{r.station} ({r.nearest_station_m:.0f} m)"
        for r in tightest.itertuples()))

    out_cols = ["station", "latitude", "longitude", "lines", "state",
                "distance_outside_m", "nearest_station_m"]
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded = excluded.assign(nearest_station_m="")
    excluded.sort_values(["state", "station"])[out_cols].to_csv(
        EXCLUDED_STATIONS_CSV, index=False)

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    kept.sort_values("station")[["station", "latitude", "longitude"]].to_csv(
        STATIONS_CSV, index=False)
    print(f"\nWrote {len(kept)} stations to {STATIONS_CSV}")
    print(f"Wrote {EXCLUDED_STATIONS_CSV} ({len(excluded)} stations outside "
          f"the District, each named with its state)")


if __name__ == "__main__":
    main()
