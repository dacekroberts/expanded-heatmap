"""Madrid-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "madrid" / "raw"
DATA_PROCESSED = ROOT / "data" / "madrid" / "processed"
OUTPUTS = ROOT / "outputs" / "madrid"

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

# UTM zone 30N: the longitude (~-3.70) falls in the -6 to 0 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32630"

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
CITY_KEEP = "MADRID"

TAXONOMY_SYSTEM = "madrid_epigrafe"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "desc_epigrafe"

# Sanity bounds for the supplied lat/lng. TODO: tighten to the city's real
# extent once the boundary is known (this box is a wide starting guess).
MADRID_BBOX = {
    "lat_min": 40.02,
    "lat_max": 40.82,
    "lon_min": -4.2,
    "lon_max": -3.2,
}
