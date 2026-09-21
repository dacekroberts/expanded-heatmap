"""Los Angeles-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Deliberately NOT yet folded into a shared data/registry.yaml loader: wait
until more cities show the real common shape before generalizing (see
PLAN.md).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "los_angeles" / "raw"
DATA_PROCESSED = ROOT / "data" / "los_angeles" / "processed"
OUTPUTS = ROOT / "outputs" / "los_angeles"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Every LA Metro station outside the City of LA, with the city it is in -
# a citable record of a real scope decision (54 of 110 stations), the same
# treatment San Francisco's excluded_stations.csv gets.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
BUSINESSES_GEOCODED_CSV = DATA_PROCESSED / "businesses_geocoded.csv"
# Step 3's output BEFORE the home-business filter, written every run purely so
# fetch_parcel_residence.py has a stable, unfiltered population to look up.
# Without it the two feed each other: the fetcher would read the filtered file,
# build a cache missing the rows already removed, and those rows would silently
# come back on the next run. Gitignored, like everything in processed/.
BUSINESSES_PREFILTER_CSV = DATA_PROCESSED / "businesses_geocoded_prefilter.csv"

# Raw inputs. Download commands (all public):
#   gtfs_rail.zip  curl -sL https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip
#   la_active_businesses.csv  Socrata resource 6rrh-rzua on data.lacity.org,
#     server-filtered to rows with coordinates, only the columns step 2 uses,
#     ordered for a reproducible file:
#       curl -sG https://data.lacity.org/resource/6rrh-rzua.csv
#         --data-urlencode '$select=location_account,business_name,dba_name,street_address,city,zip_code,naics,primary_naics_description,council_district,location_start_date,location_1'
#         --data-urlencode '$where=location_1 IS NOT NULL'
#         --data-urlencode '$order=location_account' --data-urlencode '$limit=700000'
#   la_county_incorporated_cities.geojson  LA County Planning's city boundary
#     layer, incorporated cities only:
#       https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/admin_dist_SDE_DIST_DRP_CITY_COMM_BDY/FeatureServer/0/query
#       where=JURISDICTION='INCORPORATED CITY', outFields=CITY_COMM_NAME,JURISDICTION,SQ_MILES, outSR=4326, f=geojson
GTFS_ZIP = DATA_RAW / "gtfs_rail.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "la_active_businesses.csv"
CITIES_BOUNDARY_GEOJSON = DATA_RAW / "la_county_incorporated_cities.geojson"
# Census geocoder responses, cached by content hash (see pipeline/census_geocoder.py).
GEOCODE_CACHE_DIR = DATA_RAW / "geocode_cache"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 11N. Los Angeles's longitude (~-118.25) falls in the -120 to -114
# band. Derived per city, not copied - see docs/project_context.md's CRS
# lesson.
CRS_PROJECTED = "EPSG:32611"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# LA Metro Rail: the six lines in Metro's own rail GTFS feed - A, C, E, K
# (light rail, route_type 0) and B, D (subway, route_type 1). route_ids are
# the feed's own. The feed (Metro's official rail feed) is already
# rail-only, so no route_type filtering is needed here. Station spacing
# inside the City of LA is uniform (median ~0.55 mi, no dense street-
# running offshoots), so every in-city station is kept - the sub-transit-
# line filters (docs/sub_transit_line_filters.md) are not needed.
LA_METRO_ROUTE_IDS = ["801", "802", "803", "804", "805", "807"]

# Real public names: since 2020 Metro names its lines by letter (A Line, ...,
# formerly Blue, Red, Green, Expo, Purple, Silver/Crenshaw). Confirmed via
# Metro's own "line letters" post and Wikipedia's "<X> Line (Los Angeles
# Metro)" articles. The feed's route_long_name is "Metro A Line" - the
# "Metro" brand prefix is dropped, as "Blue Line" is for San Diego.
LA_METRO_LINE_NAMES = {
    "801": "A Line",
    "802": "B Line",
    "803": "C Line",
    "804": "E Line",
    "805": "D Line",
    "807": "K Line",
}

# Feed stop names that are the SAME physical station complex named per line
# (found by a pairwise distance check of all station names: four pairs under
# 200 ft apart, 2026-09-18). Collapsed before the city-boundary filter so an
# interchange isn't counted as two stations.
GTFS_NAME_ALIASES = {
    "7th Street / Metro Center Station - Metro A & E Lines": "7th Street / Metro Center Station",
    "7th Street / Metro Center Station - Metro B & D Lines": "7th Street / Metro Center Station",
    "Expo / Crenshaw E-Line Station": "Expo / Crenshaw Station",
    "Expo / Crenshaw K-Line Station": "Expo / Crenshaw Station",
    "Union Station - Metro A-Line": "Union Station",
    "Union Station - Metro B & D Lines": "Union Station",
    "Willowbrook - Rosa Parks Station - Metro A-Line": "Willowbrook - Rosa Parks Station",
    "Willowbrook - Rosa Parks Station - Metro C-Line": "Willowbrook - Rosa Parks Station",
}

# Boundary layer: LA County's incorporated cities, one record per city; the
# City of LA is the record whose CITY_COMM_NAME is "LOS ANGELES".
CITY_BOUNDARY_FIELD = "CITY_COMM_NAME"
CITY_BOUNDARY_NAME = "LOS ANGELES"

# --- Business filtering ------------------------------------------------

# The dataset's `city` field is a postal community name (VAN NUYS, NORTH
# HOLLYWOOD, SAN PEDRO, ... are all part of the City of LA), so an exact
# match on it would keep only about half the city's businesses. Instead the
# dataset's own `council_district` marks in-city rows: districts 1-15 are
# the City of LA's council districts, and 0 means the business is registered
# with LA's Office of Finance but located outside the city. Step 2 also
# prints how many in-district points fall inside the boundary polygon, as
# an independent cross-check.
IN_CITY_COUNCIL_DISTRICTS = range(1, 16)

# Encoding of this city's RAW source files, declared rather than inferred.
# pandas defaults to UTF-8 and raises on anything else - safe, but it leaves
# the next person to guess, and reaching for latin-1 to silence a
# UnicodeDecodeError corrupts accented names without ever failing. Declaring it
# makes the choice reviewable and part of the provenance. See the encoding rule
# in docs/data_sources.md; non-US cities are where this bites.
SOURCE_ENCODING = "utf-8"

TAXONOMY_SYSTEM = "naics"
# The raw export's own classification column. Step 2 renames it to the
# taxonomy's VALUE_COLUMN, then filters via pipeline.taxonomies.
RAW_CLASSIFICATION_COLUMN = "naics"

# NAICS catch-all codes excluded for THIS city, after sampling its own
# registrants (the verdict is per city - see NAICS_CATCHALL_CODES_TO_CHECK in
# pipeline/taxonomies/naics.py). Applied as its own printed filter in step 2,
# so the drop is visible in the run output rather than hidden in classify().
#
#   812990  All Other Personal Services
#     Sampled 2026-09-21 against the rendered map: of the 23,839 mapped pins,
#     7,540 (31.6%) carried a catch-all code and 812990 alone accounted for
#     2,255 of the ~4,100 pins whose displayed name looked like an
#     individual's. 68.1% of LA's raw rows have no dba_name, so those rows
#     display the registrant's own name, and 37% of the sampled ones had an
#     APT/UNIT/STE/# in the street address. That matches the national note on
#     this code (~90% non-storefront: home-based sole proprietors), so it is
#     excluded here on BOTH grounds: it is mostly not a storefront, and
#     publishing it puts individuals' names at their home addresses on a
#     public map.
#
# Still open for this city (not sampled): 812930 Parking Lots and Garages,
# 459999 All Other Miscellaneous Retailers.
NAICS_EXCLUDE_CODES = {"812990"}

# Sanity bounds for the supplied lat/lng (the City of LA spans roughly
# 33.70-34.34 N, -118.67 to -118.15 W). The source rounds coordinates to 4
# decimals (~11 m) - fine for ring bands of 160 m and up, but a limitation.
LOS_ANGELES_BBOX = {
    "lat_min": 33.65,
    "lat_max": 34.40,
    "lon_min": -118.72,
    "lon_max": -118.10,
}

# --- Assessor parcels, for the home-business filter ------------------------
# Measured 2026-09-21: a 400-point sample put 7.2% of this city's person-like
# pins on a Residential parcel claiming a homeowner's exemption - roughly
# 1,000-2,000 pins, the largest such exposure in the project. Mostly home
# beauty/barber/pet-care and catering (NAICS 812111, 812112, 812910, 722320),
# codes that are legitimate for a real storefront, which is why the 812990
# exclusion already applied here could not reach them. See DECISIONS.md.
#
# The county's own parcel layer carries everything needed - 92 fields
# including UseType, UseDescription and Roll_HomeOwnersExemp - so no second
# dataset is required. Owner names are absent by law (Cal. Gov. Code
# s7928.205), which is convenient: there is nothing here to publish by
# accident.
PARCEL_SERVICE_URL = (
    "https://public.gis.lacounty.gov/public/rest/services/"
    "LACounty_Cache/LACounty_Parcel/MapServer/0/query"
)
# An exact point-in-parcel test matches only ~49% of these pins, because the
# 9% of LA coordinates recovered by Census geocoding sit on street centrelines
# rather than inside a parcel. A 25 m buffer matched 120/120 in testing.
# Filtering on the unbuffered 49% would have been the same partial-coverage
# mistake San Francisco's 43.8% address join nearly caused.
PARCEL_BUFFER_M = 25.0
# Written by fetch_parcel_residence.py (not a step*.py, so the drift check
# stays offline). Absent rows are simply not flagged.
PARCEL_RESIDENCE_CSV = DATA_RAW / "parcel_residence.csv"
