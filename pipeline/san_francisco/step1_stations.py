"""Step 1 - San Francisco Muni Metro station selection.

Input:  data/san_francisco/raw/gtfs.zip           (Muni GTFS feed)
        data/san_francisco/raw/sf_county_boundary.geojson
Output: data/san_francisco/processed/stations.csv

Muni Metro is a different shape of system from San Diego's Trolley (whose
stations are uniformly sparse): it runs underground/grade-separated through
a compact downtown-to-West-Portal spine (plus the newer Chinatown Central
Subway), then surfaces onto ordinary street-running track with stops every
1-2 blocks for the rest of each line's length - out to Ocean Beach (N/L),
the Bayview/Visitacion Valley corridor (T), and the Ingleside/Ocean Ave
area (M). A real check (2026-09-18) found 74% of the 125 surface stops are more than
0.6 miles (beyond this project's outermost ring) from the nearest subway
station, median 1+ mile - so scoping to subway-only stations would miss
three whole districts the line-only network reaches, not just thin out
duplicate coverage of the same area.

The selection below is a deliberate four-filter thinning of the surface
portion (see docs/sub_transit_line_filters.md), so ring-gradient analysis stays meaningful
(a station every block would make "distance from a station" nearly
meaningless) while still reaching every district the full network does:

  1. Every subway/underground station is always kept - never subject to
     the spacing filter (3) below. These already function as the system's real
     interchange points.
  2. Each line's own two terminals (first/last stop in its own ordered
     stop sequence) are always kept.
  3. Remaining surface stops are thinned to roughly one per 0.5 mile,
     measured along the line's own real stop-to-stop path (not straight-
     line/airline distance) starting the count fresh from each kept stop
     (a terminal, a subway station, or an interchange) - not from the
     line's start regardless of what's already been kept.
  4. Any stop shared by 2+ lines (a real transfer point) is force-kept
     even where filter 3's spacing alone would have dropped it.

Run:  python pipeline/san_francisco/step1_stations.py
"""

import re
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.san_francisco.config import (  # noqa: E402
    GTFS_ZIP,
    COUNTY_BOUNDARY_GEOJSON,
    STATIONS_CSV,
    EXCLUDED_STATIONS_CSV,
    MUNI_METRO_ROUTE_IDS,
    COUNTY_BOUNDARY_NAME,
    CRS_GEOGRAPHIC,
    SUBWAY_STATION_KEYWORDS,
    STATION_SPACING_MILES,
    STATION_NAME_ALIASES,
    OPERATOR_STATION_COUNTS,
    OPERATOR_COUNTS_SOURCE,
)
from pipeline.stations import (  # noqa: E402
    check_operator_counts, haversine_miles, thin_sequence)

# Representative trip's shape_id per line (its single most-used trip
# shape - see pipeline/san_diego/step1_stations.py's sibling reasoning
# for why one direction's trip is enough to get the line's real ordered
# stop sequence). Found by inspection (2026-09-18): counted
# trips per shape_id per route and took the mode. Re-derive if the GTFS
# feed is re-downloaded.
LINE_SHAPES = {"J": "9301", "K": "9436", "L": "9501", "M": "9651", "N": "9717", "T": "354",
               "F": "19851"}   # F: its most-run shape, 426 of 852 trips (2026-09-27)

# Strips GTFS direction-suffix variants of the same physical station down
# to one canonical name (e.g. "Metro Church Station/Downtown" and
# "Metro Church Station/Outbound" are two platforms of the same station,
# not two stations) - needed before the interchange/spacing logic below,
# which reasons about physical stations, not per-direction platforms.
DIRECTION_SUFFIX_PATTERN = re.compile(
    r"\s*/\s*(Downtown|Outbound|Downtn|Outbd)$"
    r"|\s+(Northbound|Southbound|Outbound|Downtown|Downtn|Outbd)$"
)


def canonical_name(stop_name: str) -> str:
    stripped = DIRECTION_SUFFIX_PATTERN.sub("", stop_name).strip()
    return STATION_NAME_ALIASES.get(stripped, stripped)


def is_subway(canonical: str) -> bool:
    return any(k in canonical for k in SUBWAY_STATION_KEYWORDS)


# The earth radius this filter was measured with; another moves the cut
# distances in excluded_stations.csv (pipeline/stations.py haversine_miles).
HAVERSINE_RADIUS_MILES = 3958.8


def miles_between(a, b):
    """Haversine miles between two (lat, lon) points, at this city's radius."""
    return haversine_miles(a, b, radius_miles=HAVERSINE_RADIUS_MILES)


def load_gtfs_table(zip_path, filename):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(filename) as f:
            return pd.read_csv(f, dtype=str)


def ordered_stop_sequence(line: str, trips: pd.DataFrame, stop_times: pd.DataFrame,
                           stops: pd.DataFrame) -> pd.DataFrame:
    """This line's real, in-order stop sequence (one representative
    direction), as (canonical_name, latitude, longitude) rows."""
    shape_id = LINE_SHAPES[line]
    trip_row = trips[(trips["route_id"] == line) & (trips["shape_id"] == shape_id)].iloc[0]
    seq = stop_times[stop_times["trip_id"] == trip_row["trip_id"]].copy()
    seq["stop_sequence"] = seq["stop_sequence"].astype(int)
    seq = seq.sort_values("stop_sequence").merge(stops, on="stop_id")
    seq["latitude"] = seq["stop_lat"].astype(float)
    seq["longitude"] = seq["stop_lon"].astype(float)
    seq["canonical"] = seq["stop_name"].apply(canonical_name)
    return seq[["canonical", "latitude", "longitude"]].reset_index(drop=True)


def select_line_stations(line: str, ordered: pd.DataFrame, interchange_names: set):
    """Apply the four filters to one line's ordered stop sequence.

    The shared walk, pipeline/stations.py thin_sequence(), by position: the
    M starts at two "San Jose Ave & Geneva Ave" platforms, and the second is
    a cut row of its own. Filter 1 is `keep_always`, filter 2 the two ends,
    filter 3 the spacing walk in haversine miles along the line's real path,
    counted fresh from each kept stop; filter 4 is `interchange_after`, so a
    force-kept interchange never resets filter 3's count.

    Returns (kept, excluded) - excluded carries enough to document every
    cut station (name, line, why, and what it was closest to instead), so
    the thinning is auditable, not a silent drop.
    """
    names = list(ordered["canonical"])
    kept_mask, cuts = thin_sequence(
        names, list(zip(ordered["latitude"], ordered["longitude"])),
        spacing=STATION_SPACING_MILES, distance=miles_between,
        keep_always={n for n in names if is_subway(n)},
        interchange=interchange_names, interchange_after=True)

    kept = ordered[kept_mask].drop_duplicates(subset="canonical")

    excluded_rows = [{
        "station": names[i],
        "line": line,
        "latitude": ordered.iloc[i]["latitude"],
        "longitude": ordered.iloc[i]["longitude"],
        "reason": "spacing filter (surface stop, < "
                  f"{STATION_SPACING_MILES}mi since nearest kept stop)",
        "nearest_kept_station": nearest_kept,
        "miles_since_nearest_kept": round(since, 3),
    } for i, nearest_kept, since in cuts]
    excluded = pd.DataFrame(excluded_rows).drop_duplicates(subset=["station", "line"])

    return kept, excluded


def main():
    if not GTFS_ZIP.exists():
        sys.exit(
            f"No GTFS feed at {GTFS_ZIP}.\n"
            "Download it from https://www.sfmta.com/reports/gtfs-transit-data "
            "(the working mirror as of 2026-09-18 is "
            "https://muni-gtfs.apps.sfmta.com/data/muni_gtfs-current.zip - "
            "gtfs.sfmta.com itself timed out from this environment)."
        )
    if not COUNTY_BOUNDARY_GEOJSON.exists():
        sys.exit(f"No boundary file at {COUNTY_BOUNDARY_GEOJSON}.")

    trips = load_gtfs_table(GTFS_ZIP, "trips.txt")
    stop_times = load_gtfs_table(GTFS_ZIP, "stop_times.txt")
    stops = load_gtfs_table(GTFS_ZIP, "stops.txt")

    line_sequences = {
        line: ordered_stop_sequence(line, trips, stop_times, stops)
        for line in MUNI_METRO_ROUTE_IDS
    }

    # Gate 3: each line's stops before the thinning below (one direction - see
    # config.OPERATOR_STATION_COUNTS). Prints only, as verify_stations does.
    print("Gate 3 (Muni Metro and the F):")
    actual = {line: seq["canonical"].nunique() for line, seq in line_sequences.items()}
    check_operator_counts(OPERATOR_STATION_COUNTS, actual)
    print(f"    gate 3 source: {OPERATOR_COUNTS_SOURCE}\n")

    # Which canonical stop names are shared by 2+ lines - the real
    # interchange points filter 4 force-includes. Subway stations are
    # already always-kept via filter 1, so this mostly matters for
    # surface interchanges (e.g. a stop two lines both serve on their
    # way to/from the subway).
    name_to_lines = {}
    for line, seq in line_sequences.items():
        for name in seq["canonical"].unique():
            name_to_lines.setdefault(name, set()).add(line)
    interchange_names = {name for name, lines in name_to_lines.items() if len(lines) >= 2}
    print(f"Interchange stops (shared by 2+ lines): {sorted(interchange_names)}\n")

    kept_per_line = {}
    excluded_per_line = []
    for line, seq in line_sequences.items():
        selected, excluded = select_line_stations(line, seq, interchange_names)
        kept_per_line[line] = selected
        excluded_per_line.append(excluded)
        print(f"{line} Line: kept {len(selected)} of {len(seq)} stops "
              f"({seq['canonical'].nunique()} distinct physical stations)")

    # Document every cut station - which line it belonged to, why, and
    # what it was closest to instead - so the spacing filter is auditable,
    # not a silent drop. Written to outputs/
    # (committed) rather than data/processed/ (gitignored) since this is
    # a citable record of a real design decision.
    excluded_stations = pd.concat(excluded_per_line, ignore_index=True)
    excluded_stations = excluded_stations.sort_values(["line", "station"])
    EXCLUDED_STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    excluded_stations.to_csv(EXCLUDED_STATIONS_CSV, index=False)
    print(f"\n{len(excluded_stations)} surface stops cut by the spacing filter across all "
          f"{len(line_sequences)} lines - documented in {EXCLUDED_STATIONS_CSV}")

    all_selected = pd.concat(kept_per_line.values(), ignore_index=True)
    stations = (
        all_selected.groupby("canonical", as_index=False)
        .agg(latitude=("latitude", "mean"), longitude=("longitude", "mean"))
        .rename(columns={"canonical": "station"})
    )
    print(f"\n{len(stations)} distinct stations selected across all {len(line_sequences)} lines "
          f"(before the city-boundary check below).")

    # --- Spatial filter to San Francisco (its own county boundary) --------
    # Expected to keep every selected station (Muni Metro is entirely an
    # SF service - see config.py) - run for real rather than assumed, per
    # the add-city skill's Step 0.
    boundary = gpd.read_file(COUNTY_BOUNDARY_GEOJSON)
    sf_boundary = boundary[boundary["county"] == COUNTY_BOUNDARY_NAME].dissolve()
    sf_boundary = sf_boundary.set_crs(CRS_GEOGRAPHIC) if sf_boundary.crs is None \
        else sf_boundary.to_crs(CRS_GEOGRAPHIC)

    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs=CRS_GEOGRAPHIC,
    )
    joined = gpd.sjoin(stations_gdf, sf_boundary[["geometry"]], predicate="within", how="left")
    in_city = joined[~joined["index_right"].isna()].drop(columns=["geometry", "index_right"])
    out_city = joined[joined["index_right"].isna()]
    if len(out_city):
        print(f"Excluded (outside {COUNTY_BOUNDARY_NAME}): {sorted(out_city['station'].tolist())}")
    else:
        print(f"All {len(stations)} selected stations fall within {COUNTY_BOUNDARY_NAME}.")

    in_city = in_city.sort_values("station").reset_index(drop=True)
    print(f"\nFinal station list ({len(in_city)}):\n{in_city.to_string(index=False)}")

    STATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    in_city.to_csv(STATIONS_CSV, index=False)
    print(f"\nWrote {STATIONS_CSV}")


if __name__ == "__main__":
    main()
