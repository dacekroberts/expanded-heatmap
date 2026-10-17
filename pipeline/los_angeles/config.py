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
# The index reaches more than 25 km past the map's stations, a far corner of the
# municipality's own area: recorded for rule D of scripts/check_place_scope.py
# (measured 27.4 km on the index of 2026-10-13; remove it if a rebuild falls within 25 km).
PLACE_SCOPE_REACH_REASON = "2026-10-13: the west San Fernando Valley's edge, inside the city limits, lies 27 km past the nearest station (owner)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
# Read and kept, 2026-10-13 (the flag check of wave 1; the owner's ruling
# to settle unsure rows by the existing rules). None carries a leak word,
# so check E takes no PLACE_REVIEWED entry for it; the reason is kept here.
#   node/4773740642 '1100 Wilshire': tourism=attraction with a Wikidata entry and no home tag
#   way/414615365 'Villa Aurora': an article of its own in three languages (Wikidata lookup, 2026-10-13) and an institution's website on the object: a cultural monument, no private home by its tags
PLACE_REVIEWED = {
    "Hotel Rosslyn": "a historic building with its own article, not a trading hotel",
    "Ralphs Grocery Store": "a registered historic building with its own article",
    "The Jim Henson Company Lot": "a historic studio lot with its own article",
}
PLACE_DROPPED = {
    "node/358828771": "'Saint Athanasius Roman Catholic Church': an imported point at the same spot (0 m) as the building St Anthanasius Church (way/328299218), same denomination: one church twice. The point has... (lane 4 borderline read; owner, 2026-10-16)",
    "node/12087671469": "'Rosemary Chapel': a chapel point (place_of_worship=chapel) 29 m from Little Church of the Flowers (node/12084413563), no entry of its own; the two read as chapels... (lane 4 borderline read; owner, 2026-10-16)",
    "node/4391233440": "'Farmer's Market', a business's own feature under its own name",
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
    "way/675982020": "'Arroyo Seco Bicycle and Pedestrian Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/109932641": "'Arroyo Seco Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/166902826": "'Arroyo Seco Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/730878194": "'Arroyo Seco Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/27080854": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/27958304": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/40663318": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/129540901": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/494886057": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/494886058": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/813331046": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/958565205": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/958565206": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/958565207": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388649640": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388649641": "'Ballona Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/137062899": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/137062905": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/404184497": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/694595294": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/717380318": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/717380319": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/717380320": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/892895522": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1020713464": "'Browns Creek Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/136667610": "'Dominquez Channel Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/823679079": "'Dominquez Channel Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/823679080": "'Dominquez Channel Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/823679081": "'Dominquez Channel Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/823679089": "'Dominquez Channel Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1348381033": "'Dominquez Channel Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/335821226": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/392387715": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/494886059": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/494886060": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/662282651": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/702164539": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/702164540": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/702164541": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/702164542": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391843": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391846": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391847": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391852": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391856": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391858": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391862": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391879": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/788391931": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/812984529": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/813336680": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/813336681": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/867119534": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/867119535": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/867155581": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/867155582": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/867158564": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/867158565": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/903933509": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/903933510": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/903979032": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/914566256": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/914566258": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/914566259": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/927863274": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/927863275": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/927863276": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482390": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482391": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482393": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482394": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482395": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482396": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482397": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482398": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/952482399": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/957935197": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/957935198": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/957935199": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/973212490": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/973212491": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/973212492": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/973212493": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/973212496": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/973212497": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1052114968": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388621489": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388621490": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388621491": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1419890051": "'Expo Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/31647117": "'Hansen Dam Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/342732394": "'Hansen Dam Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/372699390": "'Hansen Dam Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/686183953": "'Jacaranda Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/364782082": "'LA Riverfront Greenway Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/658942306": "'Long Beach Bicycle Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1347244954": "'Los Angele River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/172099360": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/173389811": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/183090504": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/430277550": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/705664710": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/733806849": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/733806862": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1069087084": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1069087085": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1347244952": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1347244955": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1453407119": "'Los Angeles River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1175749703": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1175749704": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1175749705": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1175749706": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1177675923": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1177675924": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1178170954": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1178170955": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1245719398": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1245719399": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1245719400": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1379318249": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1379318250": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1379318251": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1379318252": "'Mark Bixby Memorial Bicycle-Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/4341268": "'Marvin Braude Bike Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1184901988": "'Marvin Braude Coastal Bike Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388834106": "'Marvin Braude Coastal Bike Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388834107": "'Marvin Braude Coastal Bike Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/42585446": "'Marvin's Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/133349527": "'Marvin's Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/440747712": "'Recreation Park Bicycle Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/659570581": "'Recreation Park Bicycle Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/678277410": "'Recreation Park Bicycle Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/852174413": "'Recreation Park Bicycle Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/13347909": "'Sale Avenue Walk and Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/730897842": "'San Fernando Bike Path 3', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1078090112": "'San Fernando Bike Path 3', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1078090113": "'San Fernando Bike Path 3', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469612049": "'San Fernando Bike Path 3', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1469612050": "'San Fernando Bike Path 3', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/144917759": "'San Gabriel River Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/94446314": "'Santa Monica Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/30749552": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/120257695": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/120257700": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/120257776": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/144928372": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/251521062": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/803109318": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/868105784": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/868105788": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/868105791": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/914041680": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/914041681": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1270545368": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1270545374": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1270545376": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1275431183": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1379323619": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1379323620": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1379323621": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1388840266": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1414725248": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1460635767": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1523079478": "'Shoreline Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1460635766": "'Shoreline Beach Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1460635774": "'Shoreline Beach Pedestrian Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/28773351": "'South Bay Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/822309588": "'South Bay Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/330317153": "'Tujunga Wash Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/4341259": "'Venice Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/285608124": "'Venice Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/285608130": "'Venice Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1076225288": "'Venice Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1076225296": "'Venice Beach Bike Path', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/807732516": "'Columbarium Road', a cemetery's or church ground's internal road (owner, 2026-10-13)",
    "way/304401679": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/304401684": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/378062365": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/378062366": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/632507143": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/632507144": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/670831012": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/672361027": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1149268509": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1149268510": "'Headwaters Greenway northbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/304401680": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/304571440": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/372413691": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/380028924": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1056062513": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1056091340": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1056091341": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1301828974": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1301828975": "'Headwaters Greenway southbank', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/721753881": "'Headwaters Greenway southside', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/432363600": "'Animal Science (Original Quonset Hut)', description: a department label as a building's name: historic=building; building=college; no wikidata (flag check, 2026-10-13)",
    "relation/6398915": "'Assembly Hall', description: bare type word: 'Assembly Hall'; a BARE_TYPE_NAMES word (flag check, 2026-10-13)",
    "relation/6409632": "'Case Study House #1', home: houses with an entry and no home tag: a private house; HOME_NAME misses a name that ends in a number (flag check, 2026-10-13)",
    "way/727000078": "'Great Lawn', description: 'Great Lawn', a lawn under its description, by id (flag check, 2026-10-13)",
    "node/10778795095": "'Jews for Jesus', organisation office: a mission body's name on a place-of-worship node: decided by the name, not a tag (flag check, 2026-10-13)",
    "way/892530397": "'Prospect Studios', a working studio's name on its gate, no article: a business with nothing else (flag check, settled by the existing rules, 2026-10-13)",
    "way/428021906": "'South Park Lofts', home: apartment building by building:use: RESIDENTIAL_BUILDINGS reads building= only; a rule on building:use could catch it (flag check, 2026-10-13)",
    "way/428021895": "'The Brockman Lofts', home: apartment building by building:use: homes with an article are skipped; a rule on building:use could catch it (flag check, 2026-10-13)",
    "way/302378864": "'Veterans Memorial', description: bare memorial type: 'Veterans Memorial'; a BARE_TYPE_NAMES word (flag check, 2026-10-13)",
    "node/13649941158": "'Browmstones', studio backlot set tagged a locality: five set names inside one private studio lot, by id (flag check, 2026-10-13)",
    "node/13649941154": "'Financial Dirstict', studio backlot set tagged a locality: inside a private studio lot, by id (flag check, 2026-10-13)",
    "relation/17307354": "'Los Feliz Neighborhood Council District', administrative district under its office's name: a council district, not the neighbourhood's own name, by id (flag check, 2026-10-13)",
    "way/1317154725": "'Melrose Hill Historic Preservation Overlay Zone', administrative district under its office's name: a planning overlay zone, by id (flag check, 2026-10-13)",
    "node/3758329249": "'SoHo', studio backlot set tagged a locality: inside a private studio lot, by id (flag check, 2026-10-13)",
    "node/13649941159": "'South Chicago', studio backlot set tagged a locality: inside a private studio lot, by id (flag check, 2026-10-13)",
    "way/1198465039": "'Tesoro at Porter Ranch', a housing development mapped as a place (owner, 2026-10-13)",
    "way/919002009": "'The Canyons at Porter Ranch', a housing development mapped as a place (owner, 2026-10-13)",
    "node/8551800434": "'The Heights at Porter Ranch', a housing development mapped as a place (owner, 2026-10-13)",
    "relation/12480050": "'The Heights at Porter Ranch', a housing development mapped as a place (owner, 2026-10-13)",
    "node/11035338644": "'The Legends at Cascades', a housing development mapped as a place (owner, 2026-10-13)",
    "way/1198465034": "'Tuscany at Porter Ranch', a housing development mapped as a place (owner, 2026-10-13)",
    "node/13649941155": "'Upper East Side', studio backlot set tagged a locality: inside a private studio lot, by id (flag check, 2026-10-13)",
    "way/1198465035": "'Ventana at Porter Ranch', a housing development mapped as a place (owner, 2026-10-13)",
    "way/919002011": "'Westcliffe at Porter Ranch', a housing development mapped as a place (owner, 2026-10-13)",
    "way/467345451": "'Botanical Garden', a bare type word; its Wikidata entry has an article and is also on way/158612447 'Rainforest', so the article is the whole garden's, not this section's own (wave 1's unsure rows, settled on the Wikidata lookup and the existing rules, 2026-10-13)",
    "way/1210099591": "'American Gold Star Manor', a seniors' housing complex mapped as a neighbourhood, no Wikidata entry (owner, 2026-10-13)",
    "node/12624561131": "'San Fernando Gardens', a public housing project mapped as a neighbourhood, no Wikidata entry (owner, 2026-10-13)",
    "way/563505217": "'Common Grounds', an amenity space of one housing development tagged leisure=park: facilities of an apartment estate tagged a park are dropped (owner, 2026-10-13)",
    "way/484279014": "'Kinesthetics', an amenity space of one housing development tagged leisure=park: facilities of an apartment estate tagged a park are dropped (owner, 2026-10-13)",
    "way/562954916": "'The Lounge', an amenity space of one housing development tagged leisure=park: facilities of an apartment estate tagged a park are dropped (owner, 2026-10-13)",
    "way/562958436": "'The Pointe', an amenity space of one housing development tagged leisure=park: facilities of an apartment estate tagged a park are dropped (owner, 2026-10-13)",
    # The pattern screen of 2026-10-13: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "node/358850323": "'Immaculate Conception Parish Center', a part of one church as its own row, the church's own row within 300 m (owner, 2026-10-13, ruling 4; pattern screen)",
    # The helper screens of 2026-10-13 (duplicates, parts in a church's grounds): rows that
    # fall squarely in an owner ruling, each with its ruling.
    "node/369164732": "'La Brea Tar Pits', one object under two rows within 300 m; the other row stays (owner, 2026-10-13, the duplicates class of the pattern screen and the Three Soldiers ruling; helper screen): a point 66 m from the row La Brea Tar Pits and Museum (way/913293610) under the same Wikidata entry (Q1147168); the way carries the article tag and its name contains this one, so no search is lost",
    "relation/15768202": "'Historic Filipinotown', one object under two rows within 300 m; the other row stays (owner, 2026-10-13, the duplicates class of the pattern screen and the Three Soldiers ruling; helper screen): the historic district as a landmark row, 90 m from the place row Historic Filipinotown (node/10841306582): same name, same Wikidata entry (Q3138354), same article; one neighbourhood twice, the place row is the one to keep",
    "node/2832811432": "'Fire Station No. 30, Engine Company No. 30', one object under two rows within 300 m; the other row stays (owner, 2026-10-13, the duplicates class of the pattern screen and the Three Soldiers ruling; helper screen): a point at the same spot (0 m) as the row African American Firefighter Museum (way/428152638), same Wikidata entry (Q5451472) and same article; its historic tag is a broken value (museu); one building twice. The station's name goes with it (the museum row has no alt name)",
    "node/4213558285": "'El Pueblo de Los Angeles Historical Monument', one object under two rows within 300 m; the other row stays (owner, 2026-10-13, the duplicates class of the pattern screen and the Three Soldiers ruling; helper screen): a point 71 m from the place row Pueblo de Los Angeles Historical Monument (relation/18114621), same Wikidata entry (Q6682294) and the same name bar the article; the relation is the whole district; neither has an article tag",
    # The helper screens of 2026-10-13 (duplicates, parts in a church's grounds): rows that
    # fall squarely in an owner ruling, each with its ruling.
    "relation/7014295": "'University Library Lawn', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13, the class ruled in Melbourne; helper screen): a campus lawn tagged a park (the note tag gives its former name, the Oviatt Lawn), 77 m from the row University Library (relation/6427398); no place in the name; recommend drop",
    "node/2632851990": "'President's Garden', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13, the class ruled in Melbourne; helper screen): a garden point on the Occidental College campus tagged a park, 133 m from the college's row (way/439655732); a stock name and no other tag; recommend drop",
}

# Public art kept by the owner's word against the article rule (place_index,
# PLACE_KEPT; owner, 2026-10-13). Each is a known work the Wikidata lookup
# cannot admit; DECISIONS.md of that date lists the works left out.
PLACE_KEPT = {
    "node/7857202407": "'Giant Binoculars', a known work the article rule drops for want of an article of its own (owner, 2026-10-13)",
    # A place of worship kept against the denomination rule (worship_only;
    # owner, 2026-10-13: "keep all four by id").
    "node/358828101": "'The Church of Jesus Christ of Latter-day Saints', the Wilshire Ward chapel (alt_name=Wilshire Ward, wikidata=Q8022900, an entry of its own and no wikipedia tag): a known building under its denomination's name (owner, 2026-10-13)",
    "way/438331516": "'The Queen Mary', one of the city's best-known sights, in the cache with no row (tourism=hotel, historic=ship, wikidata=Q752939; held out as a hotel): a famous place the rules pass over (owner, 2026-10-13; pattern screen)",
    "way/419974642": "'Skirball Cultural Center', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
}
