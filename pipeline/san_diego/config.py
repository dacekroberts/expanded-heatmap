"""San Diego-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Deliberately NOT yet folded into a shared data/registry.yaml loader: wait
until more cities show the real common shape before generalizing (see
PLAN.md).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "san_diego" / "raw"
DATA_PROCESSED = ROOT / "data" / "san_diego" / "processed"
OUTPUTS = ROOT / "outputs" / "san_diego"

HEATMAP_HTML = OUTPUTS / "heatmap.html"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "sd_businesses_active_datasd.csv"
MUNICIPAL_BOUNDARIES_GEOJSON = DATA_RAW / "municipal_boundaries.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 11N. San Diego's longitude (~-117) falls in the -120 to -114
# band. Derived per city, not copied - see docs/project_context.md's CRS
# lesson.
CRS_PROJECTED = "EPSG:32611"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city. This is a category-definition
# choice (how far from a station counts as "walkshed"), not a city-specific
# measurement, so there's no reason to vary it yet. Revisit if a city's
# station spacing is meaningfully different.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# MTS Trolley route_ids with route_type "0" (tram/light rail) in the GTFS
# feed, i.e. Blue/Orange/Green/Copper/Silver - excludes the "MTG Event
# Line" (route_id 540), a one-off special-event shuttle, not regular
# trolley service.
TROLLEY_ROUTE_SHORT_NAMES = ["Blue", "Orange", "Green", "Copper", "Silver"]

# GTFS station names that are the same physical station split by a
# disambiguating suffix - collapse before city-boundary filtering so it
# isn't treated as two separate stations. Found by inspection of the raw
# stop_name list (2026-09-18).
GTFS_NAME_ALIASES = {
    "12th & Imperial Station (Bayside)": "12th & Imperial Station",
}

# City boundary name to filter Municipal_Boundaries.geojson (SANDAG
# regional layer, covers all San Diego County municipalities) down to.
CITY_BOUNDARY_NAME = "SAN DIEGO"

# --- Business filtering ------------------------------------------------

# Matches the raw export's own city field (address_city, uppercased).
# Restricting to this exact match - not e.g. "SAN DIEGO COUNTY" or
# suburb names like La Jolla that are technically SD neighborhoods but
# recorded under their own name in this field. Known limitation: some real
# San Diego neighborhoods (La Jolla foremost) are undercounted because
# this export's address_city field doesn't normalize them to "San
# Diego." Documented here rather than silently accepted.
CITY_KEEP = "SAN DIEGO"

TAXONOMY_SYSTEM = "naics"
# The raw export's own classification column. Step 2 renames it to the
# taxonomy's VALUE_COLUMN, then filters via pipeline.taxonomies.
RAW_CLASSIFICATION_COLUMN = "naics_code"

# Sanity bounds for the business dataset's own lat/lng. San Diego's data
# ships pre-geocoded (see step2), so this is a data-quality check on the
# supplied coordinates, not a post-geocode validation.
SAN_DIEGO_BBOX = {
    "lat_min": 32.53,
    "lat_max": 33.15,
    "lon_min": -117.32,
    "lon_max": -116.75,
}
