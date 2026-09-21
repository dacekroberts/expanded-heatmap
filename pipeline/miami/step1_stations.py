"""Step 1 - Miami-Dade rail stations (Metrorail + both Metromover loops), with
the municipality each one sits in.

Input:  data/miami/raw/gtfs.zip               (Miami-Dade Transit GTFS)
        data/miami/raw/municipalities.geojson (Miami-Dade municipal boundaries)
Output: data/miami/processed/stations.csv
        outputs/miami/station_municipalities.csv  (the regional scoping record)
        outputs/miami/excluded_stations.csv       (expected empty - see config)

THIS CITY DOES NOT FILTER STATIONS TO A MUNICIPALITY, and that is the one way
it differs from every other city here. Metrorail runs through Hialeah, Medley,
Coral Gables, South Miami and unincorporated Miami-Dade as well as the City of
Miami, and the county licenses businesses for all of them in one file - so the
boundary layer is used to NAME where each station is, not to drop it. See
config.py's header for the reasoning and who decided it.

Two GTFS quirks this feed has and the built cities did not:

  Metrorail has NO `parent_station` at all, so its 46 stop_ids are 23 stations
  x 2 directions. They are collapsed by canonical name, which needs the suffix
  stripping in config.STATION_SUFFIX_PATTERN - the feed spells the same idea
  four ways ("... STATION RAIL NORTHBOUND", "... STAT.RAIL SOUTHBOUND",
  "... STAT. RAIL NORTHBOUND", "... STATION NORTHBOUND").

  Routes are matched on exact route_id, never a substring. A substring match
  once swept a shuttle-bus route into San Diego's build.

Run:  python pipeline/miami/step1_stations.py
"""

import re
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.miami.config import (  # noqa: E402
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    EXCLUDED_STATIONS_CSV,
    GTFS_ZIP,
    LINE_NAMES,
    RING_EDGES_METERS,
    ROUTE_IDS,
    STATION_NAME_ALIASES,
    STATION_SUFFIX_PATTERN,
    STATIONS_CSV,
    STATION_MUNICIPALITIES_CSV,
)

_SUFFIX = re.compile(STATION_SUFFIX_PATTERN)


def load(zip_path, filename):
    with zipfile.ZipFile(zip_path) as z, z.open(filename) as f:
        return pd.read_csv(f, dtype=str)


def canonical(stop_name: str) -> str:
    """Platform-level GTFS name -> the station's real public name."""
    raw = str(stop_name).strip().upper()
    prev = None
    while prev != raw:                     # suffixes can stack
        prev = raw
        raw = _SUFFIX.sub("", raw).strip()
    if raw in STATION_NAME_ALIASES:
        return STATION_NAME_ALIASES[raw]
    return raw.title()


def main():
    if not GTFS_ZIP.exists() or not CITY_BOUNDARY_GEOJSON.exists():
        sys.exit("Missing raw inputs. Run pipeline/miami/fetch_sources.py first.")

    routes = load(GTFS_ZIP, "routes.txt")
    matched = routes[routes["route_id"].isin(ROUTE_IDS)]
    missing = set(ROUTE_IDS) - set(matched["route_id"])
    if missing:
        sys.exit(f"route_id(s) {missing} are not in this feed - check "
                 f"routes.txt; MDT has renumbered routes before.")
    print("Routes drawn (exact route_id match):")
    for r in matched.itertuples():
        print(f"  {r.route_id:<8} {LINE_NAMES[r.route_id][0]:<32} "
              f"route_type={r.route_type}  ({r.route_long_name})")
    print(f"\nNOT drawn: the MIA Airport People Mover (terminal-to-rental-car, "
          f"no surrounding commerce) and Tri-Rail (commuter rail, another "
          f"agency) - see config.py.\n")

    trips = load(GTFS_ZIP, "trips.txt")
    stop_times = load(GTFS_ZIP, "stop_times.txt")
    stops = load(GTFS_ZIP, "stops.txt")

    keep_trips = trips[trips["route_id"].isin(ROUTE_IDS)]
    keep_stop_ids = set(
        stop_times[stop_times["trip_id"].isin(set(keep_trips["trip_id"]))]["stop_id"])
    sub = stops[stops["stop_id"].isin(keep_stop_ids)].copy()
    sub["stop_lat"] = sub["stop_lat"].astype(float)
    sub["stop_lon"] = sub["stop_lon"].astype(float)
    sub["station"] = sub["stop_name"].map(canonical)

    # Which line(s) serve each station, for the scoping record.
    trip_to_route = dict(zip(keep_trips["trip_id"], keep_trips["route_id"]))
    st = stop_times[stop_times["trip_id"].isin(trip_to_route)][["trip_id", "stop_id"]]
    st = st.assign(route_id=st["trip_id"].map(trip_to_route))
    stop_to_station = dict(zip(sub["stop_id"], sub["station"]))
    st = st.assign(station=st["stop_id"].map(stop_to_station)).dropna(subset=["station"])
    lines_by_station = (
        st.groupby("station")["route_id"].apply(
            lambda s: ", ".join(sorted({LINE_NAMES[r][0] for r in s})))
    )

    print(f"{len(sub)} platform-level stop_ids -> "
          f"{sub['station'].nunique()} stations after collapsing by name")

    stations = (
        sub.groupby("station", as_index=False)
        .agg(latitude=("stop_lat", "mean"), longitude=("stop_lon", "mean"))
    )
    stations["lines"] = stations["station"].map(lines_by_station)

    # --- Which municipality is each station in? ---------------------------
    muni = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    muni = (muni.set_crs(CRS_GEOGRAPHIC) if muni.crs is None
            else muni.to_crs(CRS_GEOGRAPHIC))
    gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC)
    located = gpd.sjoin(gdf, muni[["NAME", "geometry"]], predicate="within",
                        how="left")
    # A station can land in two polygons only if the layer overlaps itself;
    # keep the first and say so rather than silently multiplying rows.
    if located.index.duplicated().any():
        dupes = located.index[located.index.duplicated()].nunique()
        print(f"  NOTE: {dupes} station(s) matched more than one municipality "
              f"polygon; keeping the first match.")
        located = located[~located.index.duplicated()]
    located = located.drop(columns=["index_right", "geometry"])
    located["municipality"] = located["NAME"].fillna("(outside any municipality)")
    located = located.drop(columns=["NAME"])

    print("\nStations by municipality (this map is regional - none of these "
          "are dropped):")
    print(located["municipality"].value_counts().to_string())

    # --- Station spacing, measured against the outer ring -----------------
    # The add-city skill requires this to be a conscious choice rather than an
    # accident: where stations sit closer than the outer ring, their rings
    # overlap. The map assigns each business to its NEAREST station, so nothing
    # is double-counted, but the overlap is visible.
    outer = RING_EDGES_METERS[-1]
    proj = located.copy()
    pts = gpd.GeoSeries(
        gpd.points_from_xy(proj["longitude"], proj["latitude"]),
        crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    nearest = []
    for i in range(len(pts)):
        d = pts.distance(pts.iloc[i])
        d = d[d.index != d.index[i]]
        nearest.append(d.min())
    proj["nearest_station_m"] = [round(v, 1) for v in nearest]

    print(f"\nStation spacing vs the {outer:.0f} m outer ring:")
    for label, mask in [
        ("Metrorail only", proj["lines"].str.contains("Metrorail", na=False)),
        ("Metromover only", proj["lines"].str.contains("Metromover", na=False)
            & ~proj["lines"].str.contains("Metrorail", na=False)),
        ("all stations", pd.Series(True, index=proj.index)),
    ]:
        sel = proj[mask]
        if sel.empty:
            continue
        closer = int((sel["nearest_station_m"] < outer).sum())
        print(f"  {label:<18} n={len(sel):>3}  "
              f"median nearest {sel['nearest_station_m'].median():>7.0f} m  "
              f"min {sel['nearest_station_m'].min():>6.0f} m  "
              f"closer than the outer ring: {closer}/{len(sel)}")

    # Nothing is excluded by municipality here; only a station outside the
    # county would be, and the network does not leave it.
    excluded = proj[proj["municipality"] == "(outside any municipality)"]
    kept = proj

    out_cols = ["station", "latitude", "longitude", "lines", "municipality",
                "nearest_station_m"]
    STATION_MUNICIPALITIES_CSV.parent.mkdir(parents=True, exist_ok=True)
    proj.sort_values(["municipality", "station"])[out_cols].to_csv(
        STATION_MUNICIPALITIES_CSV, index=False)
    excluded[out_cols].to_csv(EXCLUDED_STATIONS_CSV, index=False)

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    kept.sort_values("station")[["station", "latitude", "longitude"]].to_csv(
        STATIONS_CSV, index=False)

    print(f"\nWrote {len(kept)} stations to {STATIONS_CSV}")
    print(f"Wrote {STATION_MUNICIPALITIES_CSV} (regional scoping record)")
    print(f"Wrote {EXCLUDED_STATIONS_CSV} ({len(excluded)} rows - "
          f"stations outside every municipal polygon)")


if __name__ == "__main__":
    main()
