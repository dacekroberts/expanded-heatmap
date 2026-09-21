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
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 2's output BEFORE its home-business filter. fetch_parcels.py reads THIS,
# never businesses_clean.csv. Reading the filtered file leaves the already
# removed rows out of the cache, and without a cache row they are not flagged,
# so they return on the next run. Removed once on the mistaken reasoning that
# "the filter only removes rows, so the candidate set can only shrink" - true,
# but the shrinkage is exactly the rows that must stay removed.
BUSINESSES_PREFILTER_CSV = DATA_PROCESSED / "businesses_clean_prefilter.csv"

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

# --- Assessor parcels, for the home-business filter ------------------------
# San Diego was the city with NO residence signal at all: its address_suite
# holds bare values ("A", "101") with no APT/STE token, so address text cannot
# flag a residence, and 903 of its mapped pins display a name identical to the
# registered owner's. Its 0.03% reading was a MEASUREMENT GAP, not a clean
# result. Step 0 on 2026-09-21 found it is in fact the best-equipped of the
# three cities that needed this.
#
# SANDAG/SanGIS publish ONE countywide parcel layer (1,089,758 polygons), so
# the geographically split Parcels_South/_North/_East siblings are not needed.
PARCEL_SERVICE_URL = (
    "https://geo.sandag.org/server/rest/services/Hosted/Parcels/"
    "FeatureServer/0/query"
)
# `ownerocc` is 'Y' on 472,498 parcels and null otherwise - a genuine
# owner-occupancy flag, the signal this city was thought to lack.
#
# `asr_landuse` is numeric with NO coded-value domain published, so the codes
# were verified empirically rather than guessed (2026-09-21):
#   11  571,236 parcels, nucleus_use_cd 110/111, unitqty 1, mostly ownerocc='Y'
#       -> single-family detached. THIS is the residential signal.
#   17  199,972 parcels, nucleus_use_cd 171 -> condominium. EXCLUDED, for the
#       same reason as San Francisco's Multi-Family and New York's
#       multi-family lots: a unit in a shared building may be ground-floor
#       retail, and filtering it would delete real storefronts.
PARCEL_RESIDENTIAL_CODES = (11,)
# WHY THIS CITY NEEDS A NEAREST JOIN RATHER THAN A POINT-IN-PARCEL TEST.
# San Diego's business coordinates sit SYSTEMATICALLY 5-15 m from their own
# parcel: measured on 30 sampled pins, an exact point-in-parcel test matched
# 1/30, a 5 m buffer 9/30, 10 m 21/30 and 25 m 30/30. Not a precision problem -
# these carry 8 decimal places against Los Angeles' 4 - but a placement one:
# they sit at the street frontage, and SanGIS parcels exclude road
# right-of-way. So "which parcel contains this point?" has almost no answers
# here, and the question to ask is "which parcel is nearest?".
#
# REPLACED the per-point lookup on 2026-09-21. Per-point queries were the
# wrong tool for this city twice over: they answered the unanimity question
# rather than the nearest-parcel one (because these coordinates sit 5-15 m
# outside their own parcel), and ~5,000 of them got the service to block us.
# A single bulk download plus a local nearest join is both correct and politer,
# and it is what San Francisco already does.
PARCELS_CENTROIDS_CSV = DATA_RAW / "parcels_centroids.csv"
# The layer returns 2,000 features per page and supports centroid-only
# responses (supportsReturningGeometryCentroid), so no polygon geometry is
# transferred. Paging needs a stable sort - `apn` is the layer's own key.
PARCEL_PAGE_SIZE = 2000
# Covers every mapped business point plus ~400 m, measured from the data
# rather than reusing SAN_DIEGO_BBOX, which is a deliberately loose sanity
# box reaching far into the back country (861k parcels against 665k here).
PARCEL_QUERY_BBOX = {
    "lon_min": -117.280,
    "lon_max": -116.914,
    "lat_min": 32.540,
    "lat_max": 33.134,
}
# Nearest-parcel tolerance for the local join. Chosen from the measured
# offset: on 30 sampled pins an exact point-in-parcel test matched 1, a 5 m
# buffer 9, 10 m 21 and 25 m 30. 25 m accepts the frontage parcel without
# reaching across a street.
PARCEL_TOLERANCE_M = 25.0
# The registry's own structural signal, the same kind as Philadelphia's
# legalentitytype: 24,974 rows are sole proprietorships. Requiring this as
# well as a person-like name, a single-family parcel and owner occupancy makes
# this the most conservative of the three filters.
SOLE_OWNERSHIP_TYPE = "SOLE"
