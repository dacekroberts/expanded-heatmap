"""Los Angeles-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Deliberately NOT yet folded into a shared data/registry.yaml loader: wait
until more cities show the real common shape before generalizing (see
PLAN.md).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent

# Los Angeles (Regional): Long Beach added for the A Line's eight stations
# there (owner, 2026-09-27; released 2026-10-02,
# landed 2026-10-03, DECISIONS.md), on Long Beach's own licence layer
# (LONG_BEACH_* below). False reproduces the city-alone build byte for byte,
# which is how the extension was proved before it was switched on.
REGIONAL = True
NAME = "Los Angeles (Regional)" if REGIONAL else "Los Angeles"
DATA_RAW = ROOT / "data" / "los_angeles" / "raw"
# data/ is one junction shared by every worktree, and master's checks read
# processed/: the regional build writes processed/regional/ (ignored) until it
# lands (docs/session_roles.md; Cleanup, 2026-10-03). Fold back on landing.
DATA_PROCESSED = ROOT / "data" / "los_angeles" / "processed" / ("regional" if REGIONAL else "")
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

# --- Gate 3: the operator's own per-line station counts ----------------------
# Whole lines, BEFORE the City of LA cut (the A Line's Long Beach and Pomona
# ends, the E Line's Santa Monica end and so on count here). An interchange
# counts once on each line it serves. Keyed as step 1 keys its lines: the
# public names in LA_METRO_LINE_NAMES.
OPERATOR_STATION_COUNTS = {
    "A Line": 48,   # Long Beach - Pomona North (Foothill 2B's four included)
    "B Line": 14,
    "C Line": 12,   # Norwalk - LAX/Metro Transit Center
    "D Line": 11,   # Union Station - Wilshire/La Cienega
    "E Line": 29,
    "K Line": 13,   # Expo/Crenshaw - Redondo Beach
}
OPERATOR_COUNTS_SOURCE = (
    "en.wikipedia.org/wiki/Los_Angeles_Metro_Rail, table of lines (A 48, B 14, "
    "C 12, D 11, E 29, K 13), read 2026-10-01 - secondary. The C Line's 12 "
    "also read from LA Metro's own C Line timetable, effective 2026-06-07 "
    "(cdn.beta.metro.net/.../803_TT_6-7-26-1.pdf, linked from "
    "metro.net/riding/guide/system-maps/), read 2026-10-01 - primary."
)

# Boundary layer: LA County's incorporated cities, one record per city; the
# City of LA is the record whose CITY_COMM_NAME is "LOS ANGELES".
CITY_BOUNDARY_FIELD = "CITY_COMM_NAME"
CITY_BOUNDARY_NAME = "LOS ANGELES"
# The cities whose stations are kept (step 1) and whose outline frames the map
# (step 4): the City of LA alone, or with Long Beach.
SCOPE_CITY_NAMES = ("LOS ANGELES", "LONG BEACH") if REGIONAL else ("LOS ANGELES",)

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

# Regional: pipeline/taxonomies/los_angeles.py dispatches on `source` - LA's
# rows through NAICS exactly as before, Long Beach's on its own categories.
TAXONOMY_SYSTEM = "los_angeles" if REGIONAL else "naics"
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

# --- Long Beach (regional only) ---------------------------------------------
# "Business Licenses Public View" (City of Long Beach, MapsLB; refreshed
# nightly from the City's Infor licensing system). PERMITTED WITH CONDITIONS
# under the MapsLB Terms of Use, the breach-only indemnity accepted by the
# owner (2026-09-30); never imply endorsement (docs/data_sources/
# united-states.md). Downloaded by fetch_long_beach.py (not a step*.py).
#
# Server-side filter: LICSTATUS 'Active', OUTSIDECITY 'No', HOMEBASED 'No'
# (the City's own flags) - 20,204 rows on 2026-10-03.
#
# PRIVACY: FULLNAME (the licence holder's name) is NEVER requested; step 2
# raises if it arrives. A row with no DBANAME (trade name) shows its street
# address, unit removed, as this page does for LA's registrant-name rows.
LONG_BEACH_URL = ("https://services6.arcgis.com/yCArG7wGXGyWLqav/arcgis/rest/"
                  "services/Business_Licenses_Public_View/FeatureServer/0/query")
LONG_BEACH_WHERE = "LICSTATUS='Active' AND OUTSIDECITY='No' AND HOMEBASED='No'"
LONG_BEACH_FIELDS = ("OBJECTID", "LICENSENO", "LICCATDESC", "CLASSDESC", "LICSTATUS",
                     "DBANAME", "SITELOCATION", "ZIP", "HOMEBASED", "OUTSIDECITY",
                     "INDCNTR", "MILESTONE", "ISSDTTM")
LONG_BEACH_FORBIDDEN = ("FULLNAME",)
LONG_BEACH_CSV = DATA_RAW / "long_beach_business_licenses.csv"
LONG_BEACH_BOUNDARY_NAME = "LONG BEACH"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600112100,3600207359)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Fire Station No. 30, Engine Company No. 30": "a registered historic fire station with its own article",
    "Hotel Rosslyn": "a historic building with its own article, not a trading hotel",
    "Ralphs Grocery Store": "a registered historic building with its own article",
    "The Jim Henson Company Lot": "a historic studio lot with its own article",
}
PLACE_DROPPED = {
    "node/4391233440": "'Farmer's Market', a business's own feature under its own name",
    "way/784708486": "'Wilshire/Fairfax', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/784708483": "'Wilshire/La Brea', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/784708484": "'Wilshire/La Brea', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/5365944604": "'Truck Scales', a description standing in for a name (owner, 2026-10-13)",
    "way/778092634": "'Lafayette Park Square', a gated community's own way, described",
    "way/441260319": "'B Squared Funding - Home Loans', a business's own feature under its own name",
    "node/6630572502": "'Solar Unlimited Encino', a business's own feature under its own name",
    "way/412826023": "'Fox Discount Mall', closed for a year or more by its own tags (owner, 2026-10-13)",
    "way/422524239": "'The Playboy Mansion', a home",
    "way/1094206197": "'Forest Glen Park', a home: an apartment complex's own feature",
    "node/358850041": "'Divine Providence Convent', a religious residence",
    "node/358850418": "'Saint Teresa Convent', a religious residence",
    "node/358850074": "'Servants of Mary Convent', a religious residence",
    "node/358850394": "'Monastery of the Angels', a religious residence",
    "node/358850587": "'Mount Carmel Priory', a religious residence",
    "way/441315296": "'Long Beach Sagely Monastery', a religious residence",
    "node/12669430552": "'Destroyed Ku Klux Klan Monument', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/40059840": "'Bowtie/G1 Parcel', not yet open by its own tags or name (owner, 2026-10-13)",
    "way/385476452": "'Caballero Creek Park (Proposed)', not yet open by its own tags or name (owner, 2026-10-13)",
    "way/1134814254": "'18300 Hampton Court', an address standing in for a name",
    "way/406492561": "'Corn Maze', a bare type word for a name (owner, 2026-10-13)",
    "node/11530070665": "'Park 2', a placeholder standing in for a name",
    "way/379320942": "'exercise area', a bare type word for a name (owner, 2026-10-13)",
    "way/289853382": "'labyrinth', a bare type word for a name (owner, 2026-10-13)",
    "node/4384577686": "'sun dial', a bare type word for a name (owner, 2026-10-13)",
    "way/393575984": "'Small Gym', a description standing in for a name (owner, 2026-10-13)",
    "way/765561249": "'VNMS Grass Field', a description standing in for a name (owner, 2026-10-13)",
    "way/315196805": "'8th Grade Lawn', a description standing in for a name (owner, 2026-10-13)",
    "way/469609881": "'Tree Disguise', a utility's own service road, named for the utility: a description",
    "node/4639089984": "'Tree Disguise', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/908232080": "'Stage 9 & 10', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/158612447": "'Rainforest', an institution's own way, named for it",
    "relation/16706940": "'West Mission Garden', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "node/2814705438": "'Church Everyday extension', a description standing in for a name (owner, 2026-10-13)",
    "node/1902218410": "'Walk of Fame', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/1086895594": "'Lockheed A-12', an exhibit inside a venue, which keeps its own row (owner, 2026-10-13)",
    "node/3571003451": "'Boys' Camp Abandoned Pool', abandoned by its own tags (owner, 2026-10-13)",
    "way/31964047": "'Alley n/o Magnolia Boulevard', a description standing in for a name (owner, 2026-10-13)",
    "way/1210164297": "'Alley s/o Riverside Drive', a description standing in for a name (owner, 2026-10-13)",
    "way/1075415604": "'Alley ‎87582 (Historic)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/176596193": "'Alley ‎87647 (Cass Estates)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/641351636": "'The Trails Equestrian Estates (Bridle Path)', a notice in parentheses glued onto the name: a glitch (owner, 2026-10-13)",
    "way/694616876": "'The Trails Equestrian Estates (Bridle Path)', a notice in parentheses glued onto the name: a glitch (owner, 2026-10-13)",
    "way/694616877": "'The Trails Equestrian Estates (Bridle Path)', a notice in parentheses glued onto the name: a glitch (owner, 2026-10-13)",
    "way/886885633": "'The Trails Equestrian Estates (Bridle Path)', a notice in parentheses glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1129272930": "'The Trails Equestrian Estates (Bridle Path)', a notice in parentheses glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1129272931": "'The Trails Equestrian Estates (Bridle Path)', a notice in parentheses glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1375447125": "'West Golf Course Equestrian Trail (Old)', a notice in parentheses glued onto the name: a glitch (owner, 2026-10-13)",
    "way/406020307": "'Vanalden Tunnel (Closed)', a notice in parentheses glued onto the name: a glitch (owner, 2026-10-13)",
    "way/30840112": "'Haines Canyon Road ANF 3N27', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/591331582": "'Haines Canyon Road ANF 3N27', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/591493810": "'Haines Canyon Road ANF 3N27', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/373846155": "'HD Area 4 Trail', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/414500543": "'Nature Center - 1 mile trail', a description standing in for a name (owner, 2026-10-13)",
    "way/414500542": "'Nature Center - 2 mile trail', a description standing in for a name (owner, 2026-10-13)",
    "way/414500544": "'Nature Center - 2 mile trail', a description standing in for a name (owner, 2026-10-13)",
    "way/617035546": "'Nature Center - 2 mile trail', a description standing in for a name (owner, 2026-10-13)",
    "way/617035554": "'Nature Center - 2 mile trail', a description standing in for a name (owner, 2026-10-13)",
    "way/617035572": "'Nature Center - 2 mile trail', a description standing in for a name (owner, 2026-10-13)",
    "way/225111583": "'Nature Center trail (combined)', a description standing in for a name (owner, 2026-10-13)",
    "way/617035557": "'Nature Center trail (combined)', a description standing in for a name (owner, 2026-10-13)",
    "way/617035561": "'Nature Center trail (combined)', a description standing in for a name (owner, 2026-10-13)",
    "way/617035562": "'Nature Center trail (combined)', a description standing in for a name (owner, 2026-10-13)",
    "way/617035565": "'Nature Center trail (combined)', a description standing in for a name (owner, 2026-10-13)",
    "way/617035567": "'Nature Center trail (combined)', a description standing in for a name (owner, 2026-10-13)",
    "way/617035570": "'Nature Center trail (combined)', a description standing in for a name (owner, 2026-10-13)",
    "way/218549704": "'Bluff Trail at One Westbluff', a description standing in for a name (owner, 2026-10-13)",
    "way/356070073": "'Palisades Trail to Aliso Canyon', a description standing in for a name (owner, 2026-10-13)",
    "way/356070074": "'Palisades Trail to Aliso Canyon', a description standing in for a name (owner, 2026-10-13)",
    "way/53144345": "'Cedar Avenue Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/13316971": "'Fulton Avenue Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/30528157": "'Reservoir Street Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1425243655": "'Reservoir Street Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/351684086": "'Park Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1482944238": "'Park Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1040733006": "'Beach Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1040740553": "'Beach Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/53055723": "'Grand Avenue Lower Level', a description standing in for a name (owner, 2026-10-13)",
    "way/286995327": "'Grand Avenue Lower Level', a description standing in for a name (owner, 2026-10-13)",
    "way/319505716": "'Grand Avenue Lower Level', a description standing in for a name (owner, 2026-10-13)",
    "way/47244870": "'Grand Avenue Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/346197545": "'Lot C service road', a description standing in for a name (owner, 2026-10-13)",
    "way/946506468": "'Lot C service road', a description standing in for a name (owner, 2026-10-13)",
    "way/179073566": "'Medical Plaza Driveway', a driveway described, not a street's name",
    "way/809446288": "'Medical Plaza Driveway', a driveway described, not a street's name",
    "way/1055417465": "'Medical Plaza Driveway', a driveway described, not a street's name",
    "way/1316727665": "'Medical Plaza Driveway', a driveway described, not a street's name",
    "way/1319999825": "'Medical Plaza Driveway', a driveway described, not a street's name",
    "way/1319999826": "'Medical Plaza Driveway', a driveway described, not a street's name",
    "way/44631314": "'Stein Plaza Driveway', a driveway described, not a street's name",
    "way/495918954": "'Stein Plaza Driveway', a driveway described, not a street's name",
    "way/495918955": "'Stein Plaza Driveway', a driveway described, not a street's name",
    "way/535613379": "'Tarzana Medical Center Driveway', a driveway described, not a street's name",
    "way/1213004703": "'Tarzana Medical Center Driveway', a driveway described, not a street's name",
    "way/13383059": "'Entry to Los Angeles River Bike Path', a description standing in for a name (owner, 2026-10-13)",
    "way/136910202": "'Future Los Angeles River Bike Path', a description standing in for a name (owner, 2026-10-13)",
    "way/190479451": "'Glade Avenue Path', a description standing in for a name (owner, 2026-10-13)",
    "way/190479452": "'Glade Avenue Path', a description standing in for a name (owner, 2026-10-13)",
    "way/136910201": "'Gilroy Street Path', a description standing in for a name (owner, 2026-10-13)",
    "way/142959238": "'Hayvenhurst Avenue connector', a description standing in for a name (owner, 2026-10-13)",
    "way/1118165358": "'Hayvenhurst Avenue connector', a description standing in for a name (owner, 2026-10-13)",
    "way/1118165359": "'Hayvenhurst Avenue connector', a description standing in for a name (owner, 2026-10-13)",
    "way/824244923": "'House Porch Path', a description standing in for a name (owner, 2026-10-13)",
    "way/205715479": "'Elysian Valley Gateway Park Path', a description standing in for a name (owner, 2026-10-13)",
    "way/1217443243": "'Elysian Valley Gateway Park Path', a description standing in for a name (owner, 2026-10-13)",
    "way/723882337": "'Elmer Ave Green Street', a description standing in for a name (owner, 2026-10-13)",
    "way/31621134": "'Old Road Grade', a description standing in for a name (owner, 2026-10-13)",
    "way/1129016017": "'Tunnel Level 1', a description standing in for a name (owner, 2026-10-13)",
    "way/356370943": "'Uphill, Downhill Running Path', a description standing in for a name (owner, 2026-10-13)",
    "way/600730211": "'Fox Plaza Catwalk', a building's own feature described, not a street",
    "way/602756940": "'Fox Plaza walkway', a building's own feature described, not a street",
    "way/133437554": "'Promenade Entrance', a description standing in for a name (owner, 2026-10-13)",
    "way/551013628": "'Promenade Entrance', a description standing in for a name (owner, 2026-10-13)",
    "way/24706675": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/24706680": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/24706750": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/24706967": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/32528593": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/32528594": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/32528600": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/32528601": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/123392676": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/123392679": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/123615723": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/148257320": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/148257321": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/148257322": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/148257324": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/581410448": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/662467554": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/662467555": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/662467556": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/662467557": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/662467558": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/662467559": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/662467561": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/827145107": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/1173348141": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/1173348142": "'I-10 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/123413355": "'I-110 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/581397637": "'I-110 Metro ExpressLanes', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/375908596": "'Cameo Woods Guest Entrance', a gated community's own way, described",
    "way/1011373483": "'Cameo Woods Guest Entrance', a gated community's own way, described",
    "way/306061209": "'Cameo Woods Main Exit', a gated community's own way, described",
    "way/1011373481": "'Cameo Woods Main Exit', a gated community's own way, described",
    "way/723272245": "'Blue Grass Country Estates Bridle Path', a private way the private-street rule did not reach",
    "way/845350039": "'Blue Grass Country Estates Bridle Path', a private way the private-street rule did not reach",
    "way/1128002471": "'Blue Grass Country Estates Bridle Path', a private way the private-street rule did not reach",
    "way/31654437": "'Cedar Bend Edison Road', a utility's own service road, named for the utility: a description",
    "way/197977704": "'Cedar Bend Edison Road', a utility's own service road, named for the utility: a description",
    "way/32150689": "'Horse Creek Edison Road', a utility's own service road, named for the utility: a description",
    "way/31654393": "'La Tuna Edison Road', a utility's own service road, named for the utility: a description",
    "way/374773066": "'Saddle Ridge Edison Road', a utility's own service road, named for the utility: a description",
    "way/1270706644": "'Saddle Ridge Edison Road', a utility's own service road, named for the utility: a description",
    "way/372654382": "'Edison Service Road Loop', a utility's own service road, named for the utility: a description",
    "way/13291761": "'Water and Power Pole Road', a utility's own service road, named for the utility: a description",
    "way/985131266": "'Water and Power Pole Road', a utility's own service road, named for the utility: a description",
    "way/13467533": "'Water and Power Road', a utility's own service road, named for the utility: a description",
    "way/31578158": "'Water and Power Road', a utility's own service road, named for the utility: a description",
    "way/31578476": "'Water and Power Road', a utility's own service road, named for the utility: a description",
    "way/31620201": "'Water and Power Road', a utility's own service road, named for the utility: a description",
    "way/31667862": "'Water and Power Road', a utility's own service road, named for the utility: a description",
    "way/143686395": "'Powerline Trail', a utility's own service road, named for the utility: a description",
    "way/372058256": "'All Nations Church Road', an institution's own way, named for it",
    "way/48226723": "'Beverly Connection Way', a shopping centre's own way, named for it",
    "way/242898188": "'Costco Drive', a business's own feature under its own name",
    "way/415102426": "'Costco Drive', a business's own feature under its own name",
    "way/48503589": "'Cemetery Road', a description standing in for a name (owner, 2026-10-13)",
    "way/48503593": "'Cemetery Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1173486763": "'Cemetery Road', a description standing in for a name (owner, 2026-10-13)",
    "way/489668080": "'Galleria Gateway', a shopping centre's own way, named for it",
    "way/489668081": "'Galleria Gateway', a shopping centre's own way, named for it",
    "way/382737937": "'Maintenance Drive', a description standing in for a name (owner, 2026-10-13)",
    "way/159714744": "'Entrance Drive', a description standing in for a name (owner, 2026-10-13)",
    "way/351720400": "'Drive Way', a bare type word for a name (owner, 2026-10-13)",
    "way/13391344": "'Channel Pointe Mall', a shopping centre's own way, named for it",
    "way/13449560": "'Japanese Village Plaza Mall', a business's own feature under its own name",
    "way/255631219": "'West USC McCarthy Way', an institution's own way, named for it",
    "way/258001698": "'Student Affairs Way', an institution's own way, named for it",
    "way/422310143": "'Student Union Lane', an institution's own way, named for it",
    "way/372654389": "'East Haul Road', a description standing in for a name (owner, 2026-10-13)",
    "way/373846143": "'West Haul Road', a description standing in for a name (owner, 2026-10-13)",
    "way/373846145": "'West Haul Road', a description standing in for a name (owner, 2026-10-13)",
    "way/372879581": "'North Haul Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1447879343": "'North Haul Road', a description standing in for a name (owner, 2026-10-13)",
    "way/186584582": "'Loop Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/290801237": "'Loop Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/32011427": "'Main Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/32011511": "'Main Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/32011617": "'Main Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/1238452696": "'Main Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/1238452697": "'Main Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/37320267": "'Horse Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/276578253": "'Horse Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/844134510": "'Pathway Trail', a bare type word for a name (owner, 2026-10-13)",
    "way/429902349": "'Hollywood RV Park Airstream Way', a housing estate's own way, named for the estate",
    "way/1023429564": "'Hollywood RV Park Angel Way', a housing estate's own way, named for the estate",
    "way/429902343": "'Hollywood RV Park Antique Avenue', a housing estate's own way, named for the estate",
    "way/1023429571": "'Hollywood RV Park BOHO Boulevard', a housing estate's own way, named for the estate",
    "way/429902345": "'Hollywood RV Park Beverly Drive', a housing estate's own way, named for the estate",
    "way/1025671143": "'Hollywood RV Park Flamingo Road', a housing estate's own way, named for the estate",
    "way/1023429574": "'Hollywood RV Park Front Street', a housing estate's own way, named for the estate",
    "way/429902346": "'Hollywood RV Park Happy Camper Road', a housing estate's own way, named for the estate",
    "way/429902350": "'Hollywood RV Park Hollywood Boulevard', a housing estate's own way, named for the estate",
    "way/1023429572": "'Hollywood RV Park Lionsgate Road', a housing estate's own way, named for the estate",
    "way/429902341": "'Hollywood RV Park Main Road', a housing estate's own way, named for the estate",
    "way/429902348": "'Hollywood RV Park Malibu Road', a housing estate's own way, named for the estate",
    "way/1023429568": "'Hollywood RV Park Melrose Avenue', a housing estate's own way, named for the estate",
    "way/1023429563": "'Hollywood RV Park Monroe Street', a housing estate's own way, named for the estate",
    "way/429902351": "'Hollywood RV Park Mulholland Drive', a housing estate's own way, named for the estate",
    "way/429902347": "'Hollywood RV Park Oscar Avenue', a housing estate's own way, named for the estate",
    "way/1023429567": "'Hollywood RV Park Peacock Lane', a housing estate's own way, named for the estate",
    "way/1023429565": "'Hollywood RV Park Rodeo Drive', a housing estate's own way, named for the estate",
    "way/429902342": "'Hollywood RV Park Rose Lane', a housing estate's own way, named for the estate",
    "way/429902344": "'Hollywood RV Park Star Avenue', a housing estate's own way, named for the estate",
    "way/1023429569": "'Hollywood RV Park Sunset Boulevard', a housing estate's own way, named for the estate",
    "way/1023429566": "'Hollywood RV Park Vintage Road', a housing estate's own way, named for the estate",
    "way/1023429570": "'Hollywood RV Park Yellow Brick Road', a housing estate's own way, named for the estate",
    "way/122839646": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122839651": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122855909": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122855910": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122855911": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122857755": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122857759": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122858000": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122858001": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122858286": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/122858287": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/123302778": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/123302784": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/123413360": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/123612566": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/123612580": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/125083392": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/148385490": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/148385853": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/173349013": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/173349015": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/173349462": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/173349463": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781634": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781637": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781639": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781649": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781659": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781670": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781681": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781697": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/182781704": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/238999381": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/238999382": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/580285686": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/581397640": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/581397641": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/609022162": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/609022165": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/609022202": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/609022206": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/609022226": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/609022232": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/667520553": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/667520554": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/915198288": "'Harbor Transitway', not a street: another kind of object indexed as one",
    "way/123594894": "'Pacific Coast Highway', not a street: another kind of object indexed as one",
    "way/123594899": "'Pacific Coast Highway', not a street: another kind of object indexed as one",
    "way/123594901": "'Pacific Coast Highway', not a street: another kind of object indexed as one",
    "way/673670443": "'Pacific Coast Highway', not a street: another kind of object indexed as one",
    "way/673670446": "'Pacific Coast Highway', not a street: another kind of object indexed as one",
    "way/673670447": "'Pacific Coast Highway', not a street: another kind of object indexed as one",
}
