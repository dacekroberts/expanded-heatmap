"""Paris-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "paris" / "raw"
DATA_PROCESSED = ROOT / "data" / "paris" / "processed"
OUTPUTS = ROOT / "outputs" / "paris"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. Record the exact download command for each (all public):
# TODO: gtfs.zip - the agency's GTFS feed URL.
# TODO: city_boundary.geojson - a real GIS boundary layer for the city.
# TODO: the business file - endpoint, server-side filter, and snapshot date if
#       the source is a term history (Chicago's AS_OF_DATE is the model).
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "businesses.csv"  # TODO: real file name
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# LAMBERT-93, NOT THE UTM ZONE THE SCAFFOLD DERIVED (32631, zone 31N).
# Dublin set the precedent for a national grid (EPSG:2157); this is the second,
# and unlike Dublin's it is forced by the source rather than merely permitted:
#
#   1. INSEE's geolocation file publishes `x`/`y` NATIVELY in 2154 on 99.3% of
#      rows, so reading it in 2154 means the source coordinates are never
#      reprojected at all. UTM would add a transform in front of every pin.
#   2. `pipeline/countries/france.py` already names METROPOLITAN_EPSG = 2154,
#      so this keeps the config and the country module from disagreeing.
#   3. DECIDING: metropolitan France spans UTM zones 30N, 31N and 32N, so a
#      per-city UTM rule would give the five cities of france.py's
#      BUILD_SEQUENCE three different projections while they all read ONE
#      national file. Lambert-93 is a single grid for exactly this extent -
#      that is what it was defined for. The invariant is "projected metres,
#      derived per city, never copied"; deriving it from France's own grid
#      satisfies that, and copying a UTM zone between Paris and Lille would not.
#
# The DOM are a different grid per the brief (2975 Réunion, 5490 Antilles,
# 2972 Guyane), which is why check_provenance.py's NATIONAL_GRIDS entry bounds
# this to metropolitan longitudes - a Fort-de-France build must NOT inherit it.
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# TODO: which lines count and why (one agency's rail system per city; note what
# is left out), the feed's own route_ids, and the real public line names.
# Check the rail system's shape before assuming "keep every station" (see the
# add-city skill, Step 4).
ROUTE_IDS = []
LINE_NAMES = {}  # route_id -> real public name, e.g. {"801": "A Line"}

# --- Business filtering ------------------------------------------------

# TODO: how in-city rows are identified: the dataset's own city field (check
# what it really holds) or an authoritative district field.
CITY_KEEP = "PARIS"

TAXONOMY_SYSTEM = "france_naf"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "naf_label"
# This taxonomy also classifies by naf_code: keep those raw column(s) through step 2
# (they are passed to classify() by filter_to_storefront() and the map).

# Sanity bounds for the supplied lat/lng. TODO: tighten to the city's real
# extent once the boundary is known (this box is a wide starting guess).
PARIS_BBOX = {
    "lat_min": 48.46,
    "lat_max": 49.26,
    "lon_min": 1.85,
    "lon_max": 2.85,
}
