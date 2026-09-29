"""London-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "london" / "raw"
DATA_PROCESSED = ROOT / "data" / "london" / "processed"
OUTPUTS = ROOT / "outputs" / "london"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
# Brief: docs/build_briefs/london.md.
#
# The register: the Food Standards Agency's Food Hygiene Rating Scheme, one
# bulk XML per local authority. The 33 London authorities are read from the
# FSA's own authority list (RegionName "London"), never assumed as a range.
# Licence: Open Government Licence v3 (licence-read pending, 2026-09-28).
FSA_AUTHORITIES_URL = "https://api.ratings.food.gov.uk/Authorities"
FSA_API_HEADERS = {"x-api-version": "2", "Accept": "application/json"}
FSA_REGION = "London"
FSA_AUTHORITY_COUNT = 33   # the 32 boroughs and the City of London
FSA_RAW_DIR = DATA_RAW / "fsa"
FSA_AUTHORITIES_JSON = DATA_RAW / "fsa_authorities.json"
GTFS_ZIP = DATA_RAW / "gtfs.zip"   # TODO: rail source (TfL publishes no GTFS; OSM or TfL's API)
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Greater London - the 32 boroughs and the City, exactly the FSA's 33 "London"
# authorities. OSM relation 175342 (admin_level 5), polygonised from its outer
# ways; 1,595.5 km2 in UTM 30N on 2026-09-28, gated so a truncated Overpass
# answer cannot pass.
BOUNDARY_OSM_RELATION = 175342
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_greater_london.json"
BOUNDARY_AREA_KM2 = (1560, 1620)
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-0.13) falls in the -6 to 0 band. Derived per city, not copied - see docs/project_context.md's
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

# In-city rows: the 33 authority files ARE Greater London (fetch_sources.py
# asserts 33 in the FSA's "London" region); the polygon then drops any point
# geocoded outside it. CITY_KEEP is kept for the scaffold's templates.
CITY_KEEP = "London"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: Greater London's polygon extent (51.2868-51.6919 N,
# -0.5104-0.3340 E, measured 2026-09-28) plus ~0.02 deg. The polygon does the
# filtering; this catches a CRS or axis error.
LONDON_BBOX = {
    "lat_min": 51.26,
    "lat_max": 51.72,
    "lon_min": -0.54,
    "lon_max": 0.36,
}
