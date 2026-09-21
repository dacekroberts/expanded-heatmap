"""Step 1 - SkyTrain stations inside Vancouver OR Surrey.

Input:  data/vancouver/raw/gtfs.zip                     (TransLink GTFS Static)
        data/vancouver/raw/vancouver_local_areas.geojson (22 local areas)
        data/vancouver/raw/surrey_city_boundaries.geojson (10 features, 1 city)
        data/vancouver/raw/bc_municipalities.geojson     (BC ABMS, for naming)
Output: data/vancouver/processed/stations.csv
        outputs/vancouver/excluded_stations.csv
        outputs/vancouver/station_municipalities.csv

THIS IS THE ONLY STEP 1 IN THE PROJECT THAT KEEPS STATIONS IN TWO CITIES.
A station is in scope if it falls inside EITHER boundary, and every kept
station is written out with the municipality it sits in - so a reader can see
the regional scope rather than infer it. Miami does the same for its six.

54 stations system-wide, 20 in Vancouver and 4 in Surrey, so 30 are dropped:
they lie in Burnaby, Richmond, New Westminster, Coquitlam and Port Moody, whose
own business registries would have to be sourced and verified separately. That
is a new project, not a config change.

FOUR THINGS WORTH KNOWING BEFORE CHANGING ANYTHING HERE.

  Routes match on route_id, NOT route_short_name, because `route_short_name` is
  EMPTY on all three rail routes in this feed. The public names live in
  `route_long_name`. A short-name match would find nothing and report no error.

  Names DO need surgery, unlike D.C. TransLink calls every rail stop
  "<Station> @ Platform N" (a few "@ <Line>"), two to four rows each. The
  pattern is perfectly regular, so no hand-curated alias dict is needed - but
  this step ASSERTS that every "@"-bearing name matched, so a new suffix form
  fails loudly instead of inventing stations.

  No thinning. SkyTrain is grade-separated end to end - elevated or in tunnel,
  with no street-running stops - so this is D.C.'s and San Diego's shape, not
  San Francisco's. The spacing is MEASURED and printed rather than asserted.

  The Vancouver boundary is checked by AREA, not just feature count. The 22
  local areas must dissolve to one Polygon of ~118.8 km2; a dissolve that
  silently dropped a local area would still return a valid Polygon, and only
  the km2 and the containment rate catch it.

Run:  python pipeline/vancouver/step1_stations.py
"""

import re
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.vancouver.config import (  # noqa: E402
    BOUNDARY_AREA_KM2_EXPECTED,
    BOUNDARY_AREA_TOLERANCE_KM2,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_ZIP,
    LINE_NAMES,
    MUNICIPALITIES_GEOJSON,
    MUNICIPALITIES_NAME_FIELD,
    RING_EDGES_METERS,
    ROUTE_IDS,
    STATION_MUNICIPALITIES_CSV,
    STATION_NAME_STRIP_SUFFIX,
    STATION_SUFFIX_PATTERN,
    STATIONS_CSV,
    SURREY_BOUNDARY_GEOJSON,
    SURREY_BOUNDARY_NAME_FIELD,
    SURREY_BOUNDARY_NAME_KEEP,
    THINNED_GROUPS,
)

SUFFIX = re.compile(STATION_SUFFIX_PATTERN, re.I)


def load(zip_path, filename, **kw):
    with zipfile.ZipFile(zip_path) as z, z.open(filename) as f:
        return pd.read_csv(f, dtype=str, **kw)


def read_degrees(path, label):
    """Read a boundary and REFUSE one whose coordinates are not degrees.

    Surrey's Hub FILE export declares EPSG:4326 and contains UTM 10N metres.
    This build reads the FeatureServer instead, which returns real degrees -
    but the assertion stays, so switching back to the file export fails loudly
    rather than matching nothing.
    """
    g = gpd.read_file(path)
    g = g.set_crs(CRS_GEOGRAPHIC) if g.crs is None else g.to_crs(CRS_GEOGRAPHIC)
    x0, y0, x1, y1 = g.total_bounds
    if not (-180 <= x0 <= 180 and -90 <= y0 <= 90 and abs(x1) <= 180):
        sys.exit(
            f"{label}: bounds {[round(v, 1) for v in (x0, y0, x1, y1)]} are not "
            f"degrees. This is the declared-4326-but-actually-UTM trap - use "
            f"set_crs(EPSG:26910, allow_override=True), never to_crs(). See "
            f"config.SURREY_SOURCE_XY_CRS."
        )
    return g


def main():
    for path in (GTFS_ZIP, CITY_BOUNDARY_GEOJSON, SURREY_BOUNDARY_GEOJSON,
                 MUNICIPALITIES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path.name}. Run "
                     f"pipeline/vancouver/fetch_sources.py first.")
    if THINNED_GROUPS:
        sys.exit(f"config.THINNED_GROUPS is {set(THINNED_GROUPS)}, but this "
                 f"step implements no thinning. SkyTrain is grade-separated "
                 f"throughout; if that changed, port Boston's filters rather "
                 f"than leaving the setting inert.")

    # --- routes -------------------------------------------------------------
    routes = load(GTFS_ZIP, "routes.txt")
    matched = routes[routes["route_id"].isin(ROUTE_IDS)]
    missing = sorted(set(ROUTE_IDS) - set(matched["route_id"]))
    if missing:
        sys.exit(f"route_id(s) {missing} are not in this feed. Check "
                 f"routes.txt - and note route_short_name is empty on the rail "
                 f"routes, so a short-name match would also find nothing.")
    non_rail = matched[matched["route_type"] != "1"]
    if len(non_rail):
        sys.exit(f"route_type != 1 on {list(non_rail['route_id'])}. The West "
                 f"Coast Express (route_type 2, commuter rail) and the SeaBus "
                 f"(route_type 4, a ferry) are both out of scope.")
    print("Routes drawn (exact route_id match; route_short_name is empty):")
    for r in matched.sort_values("route_id").itertuples():
        print(f"  {r.route_id:<8} {LINE_NAMES[r.route_id]:<16} "
              f"route_type={r.route_type}  official route_color=#{r.route_color}")

    # --- platforms -> stations ----------------------------------------------
    trips = load(GTFS_ZIP, "trips.txt")
    stop_times = load(GTFS_ZIP, "stop_times.txt",
                      usecols=["trip_id", "stop_id"])
    stops = load(GTFS_ZIP, "stops.txt")

    keep_trips = trips[trips["route_id"].isin(ROUTE_IDS)]
    served = stop_times[stop_times["trip_id"].isin(set(keep_trips["trip_id"]))]
    platforms = stops[stops["stop_id"].isin(set(served["stop_id"]))].copy()

    raw = platforms["stop_name"].str.strip()
    stripped = raw.str.replace(SUFFIX, "", regex=True)
    unmatched = raw[raw.str.contains("@") & (stripped == raw)]
    if len(unmatched):
        sys.exit(f"{len(unmatched)} platform name(s) contain '@' but did not "
                 f"match STATION_SUFFIX_PATTERN, e.g. "
                 f"{sorted(set(unmatched))[:4]}. Widen the pattern rather than "
                 f"letting these collapse into separate stations.")
    platforms["station"] = (stripped
                            .str.replace(f"{STATION_NAME_STRIP_SUFFIX}$",
                                         "", regex=True)
                            .str.strip())
    blank = platforms["station"].eq("")
    if blank.any():
        sys.exit(f"{int(blank.sum())} platform name(s) stripped to nothing.")
    platforms["latitude"] = platforms["stop_lat"].astype(float)
    platforms["longitude"] = platforms["stop_lon"].astype(float)

    # Which lines serve each station.
    trip_to_route = dict(zip(keep_trips["trip_id"], keep_trips["route_id"]))
    station_of = dict(zip(platforms["stop_id"], platforms["station"]))
    st = served.assign(station=served["stop_id"].map(station_of),
                       line=served["trip_id"].map(trip_to_route).map(LINE_NAMES))
    lines_by_station = st.groupby("station")["line"].apply(
        lambda s: ", ".join(sorted(set(s.dropna()))))

    stations = platforms.groupby("station").agg(
        latitude=("latitude", "mean"),
        longitude=("longitude", "mean"),
        platforms=("stop_id", "size"),
    ).reset_index()
    stations["lines"] = stations["station"].map(lines_by_station)
    print(f"\n{len(platforms)} served platforms -> {len(stations)} stations "
          f"(platform positions averaged)")

    # --- in Vancouver, in Surrey, or out of scope ---------------------------
    van = read_degrees(CITY_BOUNDARY_GEOJSON, "vancouver boundary")
    if len(van) != 22:
        print(f"  NOTE: vancouver boundary has {len(van)} local areas, not 22 "
              f"- the area check below is what decides whether that matters.")
    van_geom = van.to_crs(CRS_PROJECTED).union_all()
    area = van_geom.area / 1e6
    print(f"\nVancouver boundary: {len(van)} local areas dissolve to "
          f"{van_geom.geom_type}, {area:.1f} km2 "
          f"(expected {BOUNDARY_AREA_KM2_EXPECTED})")
    if abs(area - BOUNDARY_AREA_KM2_EXPECTED) > BOUNDARY_AREA_TOLERANCE_KM2:
        sys.exit(f"  dissolved area {area:.1f} km2 is more than "
                 f"{BOUNDARY_AREA_TOLERANCE_KM2} km2 from the expected "
                 f"{BOUNDARY_AREA_KM2_EXPECTED}. A dropped local area still "
                 f"yields a valid Polygon; this check is what catches it.")

    sur_all = read_degrees(SURREY_BOUNDARY_GEOJSON, "surrey boundary")
    sur = sur_all[sur_all[SURREY_BOUNDARY_NAME_FIELD].astype(str).str.upper()
                  == SURREY_BOUNDARY_NAME_KEEP]
    if len(sur) != 1:
        sys.exit(f"Surrey boundary: {SURREY_BOUNDARY_NAME_FIELD}="
                 f"{SURREY_BOUNDARY_NAME_KEEP!r} matched {len(sur)} features, "
                 f"expected 1. The file has 10 and 9 are TOWN CENTRES, so an "
                 f"unfiltered read tests containment against a neighbourhood.")
    sur_geom = sur.to_crs(CRS_PROJECTED).union_all()
    print(f"Surrey boundary: 1 of {len(sur_all)} features "
          f"({len(sur_all) - 1} are town centres), {sur_geom.area / 1e6:.1f} km2")

    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    gdf["in_vancouver"] = gdf.geometry.within(van_geom)
    gdf["in_surrey"] = gdf.geometry.within(sur_geom)
    both = gdf["in_vancouver"] & gdf["in_surrey"]
    if both.any():
        sys.exit(f"{int(both.sum())} station(s) fall inside BOTH boundaries, "
                 f"which is geometrically impossible - check the two layers.")
    inside = gdf["in_vancouver"] | gdf["in_surrey"]
    gdf["municipality"] = ["Vancouver" if v else "Surrey" if s else ""
                           for v, s in zip(gdf["in_vancouver"], gdf["in_surrey"])]

    region = van_geom.union(sur_geom)
    gdf["distance_outside_m"] = [
        0.0 if ins else round(p.distance(region), 1)
        for ins, p in zip(inside, gdf.geometry)]

    # Name the municipality of every dropped station from a real layer.
    munis = gpd.read_file(MUNICIPALITIES_GEOJSON)
    munis = (munis.set_crs(CRS_GEOGRAPHIC) if munis.crs is None
             else munis.to_crs(CRS_GEOGRAPHIC)).to_crs(CRS_PROJECTED)
    located = gpd.sjoin(gdf[["geometry"]],
                        munis[[MUNICIPALITIES_NAME_FIELD, "geometry"]],
                        predicate="within", how="left")
    located = located[~located.index.duplicated()]
    gdf["located_in"] = located[MUNICIPALITIES_NAME_FIELD].fillna("(unmatched)")
    unmatched_muni = gdf[~inside & (gdf["located_in"] == "(unmatched)")]
    if len(unmatched_muni):
        print(f"  WARNING: {len(unmatched_muni)} excluded station(s) could not "
              f"be placed in a municipality: {list(unmatched_muni['station'])}")

    kept = gdf[inside].drop(columns="geometry").copy()
    excluded = gdf[~inside].drop(columns="geometry").copy()
    print(f"\n{len(kept)} of {len(gdf)} stations are in scope "
          f"({len(kept) / len(gdf):.1%}); {len(excluded)} are not.")
    print("\nKept, by municipality:")
    print("  " + kept["municipality"].value_counts().to_string()
          .replace("\n", "\n  "))
    print("\nExcluded, by municipality (named, not guessed):")
    print("  " + excluded["located_in"].value_counts().to_string()
          .replace("\n", "\n  "))
    print("\nThe five closest exclusions:")
    for r in excluded.nsmallest(5, "distance_outside_m").itertuples():
        print(f"  {r.station:<28} {r.distance_outside_m:>8.1f} m outside, "
              f"in {r.located_in}")
    print("\nIn-scope stations per line (no line drops out of the map):")
    for name in LINE_NAMES.values():
        n = int(kept["lines"].fillna("").str.contains(name, regex=False).sum())
        total = int(gdf["lines"].fillna("").str.contains(name, regex=False).sum())
        print(f"  {name:<16}{n:>4} of {total:>3}")

    # --- station spacing, measured against the outer ring -------------------
    outer = RING_EDGES_METERS[-1]
    pts = gpd.GeoSeries(
        gpd.points_from_xy(kept["longitude"], kept["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED).reset_index(drop=True)
    nearest = [pts.drop(index=i).distance(pts.iloc[i]).min()
               for i in range(len(pts))]
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
    print(f"  For comparison: D.C.'s median was 962 m (not thinned), San "
          f"Francisco's street-running median 134 m (thinned).")
    print("  tightest pairs: " + ", ".join(
        f"{r.station} ({r.nearest_station_m:.0f} m)"
        for r in kept.nsmallest(5, "nearest_station_m").itertuples()))

    # --- outputs ------------------------------------------------------------
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded.assign(nearest_station_m="").sort_values(
        ["located_in", "station"])[
        ["station", "latitude", "longitude", "lines", "located_in",
         "distance_outside_m"]].to_csv(EXCLUDED_STATIONS_CSV, index=False)
    kept.sort_values(["municipality", "station"])[
        ["station", "latitude", "longitude", "lines", "municipality",
         "nearest_station_m"]].to_csv(STATION_MUNICIPALITIES_CSV, index=False)

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    kept.sort_values("station")[["station", "latitude", "longitude"]].to_csv(
        STATIONS_CSV, index=False)
    print(f"\nWrote {len(kept)} stations to {STATIONS_CSV}")
    print(f"Wrote {STATION_MUNICIPALITIES_CSV} (the regional scoping record)")
    print(f"Wrote {EXCLUDED_STATIONS_CSV} ({len(excluded)} stations out of "
          f"scope, each named with its municipality)")


if __name__ == "__main__":
    main()
