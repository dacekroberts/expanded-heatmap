"""Dallas-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; Houston's files are the template
(docs/build_briefs/dallas.md): the same register, the same privacy rules.

The Texas Comptroller's Active Sales Tax Permit Holders (a table with NO
geometry), placed by an address join to the City's Address Points and the US
Census Bureau's geocoder for the residue - step 2 cleans, step 3 places,
step 4 maps. Rail from OpenStreetMap, DART's four light-rail lines.
"""

from pathlib import Path

SLUG = "dallas"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "dallas" / "raw"
DATA_PROCESSED = ROOT / "data" / "dallas" / "processed"
OUTPUTS = ROOT / "outputs" / "dallas"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
BUSINESSES_PLACED_CSV = DATA_PROCESSED / "businesses_geocoded.csv"   # the name every placed city uses
GEOCODE_CACHE_DIR = DATA_RAW / "geocode_cache"

# The brief's summary keys, read by brief_check.py's vs_config (owner,
# 2026-09-30: mode light_rail; coverage narrowed, as Houston on the same
# register, not the brief's "full").
MAP_MODE = "light_rail"
MAP_COVERAGE = "narrowed"
SCOPE = "city"

# --- Raw inputs (fetch_sources.py downloads; no step fetches, and step 3's
# geocoder refuses under HEATMAP_NO_NETWORK) ---------------------------------

# The Texas Comptroller's Active Sales Tax Permit Holders (data.texas.gov
# jrea-zgmq, public domain), one row per outlet - Houston's register.
# ⚠ COLUMNS NEVER TO LOAD: every taxpayer_* column except the organisation
# type. For a sole owner, taxpayer_name and taxpayer_address are a person's
# name and home or mailing address, and a Texas taxpayer number for an
# individual is built from their Social Security number. The download names
# its columns ($select) and step 2 asserts none of these arrived; the row key
# is Socrata's own `:id`.
REGISTER_DOMAIN = "data.texas.gov"
REGISTER_VIEW = "jrea-zgmq"
REGISTER_URL = f"https://{REGISTER_DOMAIN}/resource/{REGISTER_VIEW}.json"
REGISTER_FIELDS = (":id", "outlet_number", "outlet_name", "outlet_address", "outlet_city",
                   "outlet_state", "outlet_zip_code", "outlet_county_code",
                   "outlet_naics_code", "outlet_inside_outside_city_limits_indicator",
                   "outlet_permit_issue_date", "outlet_first_sales_date",
                   "taxpayer_organization_type")
FORBIDDEN_COLUMNS = ("taxpayer_number", "taxpayer_name", "taxpayer_address", "taxpayer_city",
                     "taxpayer_state", "taxpayer_zip_code", "taxpayer_county_code")
# The flag says inside SOME city's limits; step 3's point-in-boundary settles
# which. `outlet_naics_code` is a NUMBER column: a string prefix test is a 400.
REGISTER_WHERE = ("upper(outlet_city)='DALLAS' "
                  "AND outlet_inside_outside_city_limits_indicator='Y'")
REGISTER_CSV = DATA_RAW / "sales_tax_permits_dallas.csv"
# The brief's count (2026-09-30): 44,760 outlets; a fetch far short of it is a
# failed fetch, not a negative.
REGISTER_MIN_ROWS = 40000

# The City's Address Points (Development Services GIS), layer 0 "Main
# Address", 395,893 points (2026-09-30), pulled in bulk in pages of 2,000
# (the layer's maxRecordCount), WGS84 asked of the server. Licence: silent on
# reuse; the City's GIS disclaimer's open-ended indemnity ACCEPTED by the owner
# (2026-09-30). Never call the pins surveyed or exact. Only the address fields
# and ADDRESSTYPE are read: ACCOUNTNUMBER, GISPARCELID and the editors'
# fields are never requested.
ADDRESS_POINTS_URL = ("https://services2.arcgis.com/rwnOSbfKSwyTBcwN/arcgis/rest/services/"
                      "AddressPoints/FeatureServer/0/query")
ADDRESS_POINTS_FIELDS = ("OBJECTID", "HOUSENUMBER", "HOUSESUFFIX", "FULLSTREETNAME", "ZIPCODE",
                         "ADDRESSTYPE")
ADDRESS_POINTS_PAGE = 2000
ADDRESS_POINTS_CSV = DATA_RAW / "address_points.csv"
ADDRESS_POINTS_MIN = 390000

# OSM: every light-rail, tram and subway relation in DART's box.
RAIL_BBOX = (32.62, -96.98, 33.02, -96.55)        # south, west, north, east (the brief's)
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"

# THE CENSUS BUREAU'S PLACE POLYGON (TIGERweb, current Incorporated Places,
# GEOID 4819000; a US federal government work, public domain): Houston's rule,
# the legal boundary the City reports to the Census, not OSM's relation.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_BOUNDARY_QUERY = {"where": "GEOID='4819000'", "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# The polygon's area, land and water, gated in step 1: set from the fetched
# polygon's own AREALAND + AREAWATER (step 1 prints both).
CITY_AREA_KM2 = (950.0, 1050.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 14N: the longitude (~-96.80) falls in the -102 to -96 band. Derived
# per city, not copied (Houston is 15N).
CRS_PROJECTED = "EPSG:32614"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: the brief's 1,397 m median gap, far over the ~550 m line.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# DART Light Rail, all four lines, every station inside the City of Dallas;
# the lines are drawn to their ends. Purpose-built track, so frequency is
# disclosed, not gated (owner, 2026-09-29). NOT drawn: the Silver Line and the
# TRE (commuter rail, not in the light-rail query), and - the owner's call,
# 2026-09-30 - the Dallas Streetcar and the M-Line trolley (Houston draws its
# METRORail only; the M-Line is a heritage trolley).
LINE_REFS = ("RED", "BLUE", "GREEN", "ORANGE")
OSM_NETWORK = "DART"          # as OSM tags all 27 DART light-rail relations (2026-09-30)
LINE_NAMES = {"RED": "Red Line", "BLUE": "Blue Line", "GREEN": "Green Line", "ORANGE": "Orange Line"}
# The project's own colours, never DART's hexes (Houston's rule): Red and Green
# are Houston's (brick red 46.5, olive green 46.5 from the pins); Blue and
# Orange are the smallest HLS move from DART's #0055B8 and #F7931E that clears
# CIE76 46 from every pin and 30 from the other lines and reads 3:1 on both map
# pages (2026-09-30): DART's blue sits 15.5 from Retail's pin, so it moved to
# #264ded (46.4); orange darkened to #d97c0e (70.4).
LINE_COLOURS = {"RED": "#bf360c", "BLUE": "#264ded", "GREEN": "#5d6d0e", "ORANGE": "#d97c0e"}
# Relations the query brings that are named and NOT drawn, by (route, ref or
# name prefix) -> why. Step 1 stops on any relation it cannot place.
NOT_DRAWN = {("tram", "620"): "the Dallas Streetcar (owner, 2026-09-30)",
             ("tram", "M-Line"): "the M-Line heritage trolley (owner, 2026-09-30)"}

STATION_NAME_ALIASES = {}
STAGGERED_PLATFORMS_M = {}

# GATE 3, per line: English Wikipedia's line infoboxes (read 2026-09-30, a
# SECONDARY source): Red 26, Blue 23, Green 24, Orange 31, less two stations
# the map rightly lacks, each read at build:
#   * Convention Center (Red, Blue): in OSM's relations with role "inactive" -
#     closed while the convention centre is rebuilt - so not a stop; the
#     infoboxes still count it;
#   * Hidden Ridge (Orange): the Irving infill station the Orange Line article
#     lists, which OSM's relations do not yet carry; it lies outside the City
#     of Dallas, so no ring is lost.
OPERATOR_STATION_COUNTS = {"Red Line": 25, "Blue Line": 22, "Green Line": 24, "Orange Line": 30}
OPERATOR_TOTAL_STATIONS = None
OPERATOR_COUNTS_SOURCE = "English Wikipedia's DART line infoboxes, read 2026-09-30"

SPACING_MIN_M = 400.0

# --- Business filtering ------------------------------------------------

AS_OF_DATE = "2026-09-30"
CITY_KEEP = "DALLAS"

TAXONOMY_SYSTEM = "naics"
RAW_CLASSIFICATION_COLUMN = "outlet_naics_code"

# The organisation type for an individual sole owner (the Comptroller's code).
SOLE_OWNER_TYPE = "IS"

# Sanity bounds for placed points: the city's extent plus a margin.
DALLAS_BBOX = {
    "lat_min": 32.55,
    "lat_max": 33.08,
    "lon_min": -97.05,
    "lon_max": -96.50,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3606571629)"
# The index reaches more than 25 km past the map's stations, a far corner of the
# municipality's own area: recorded for rule D of scripts/check_place_scope.py
# (measured 25.3 km on the index of 2026-10-13; remove it if a rebuild falls within 25 km).
PLACE_SCOPE_REACH_REASON = "2026-10-13: the city limits' far east lies 25.3 km past the nearest station (owner)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
# Read and kept, 2026-10-13 (the flag check of wave 1; the owner's ruling
# to settle unsure rows by the existing rules). None carries a leak word,
# so check E takes no PLACE_REVIEWED entry for it; the reason is kept here.
#   node/4894832922 'gas monkey live': tourism=attraction with a Wikidata entry: a commercial attraction with a tourism tag stays
PLACE_REVIEWED = {
    "Hotel Street": "a four-lane public street of that name, not a hotel's drive",
}
PLACE_DROPPED = {
    "way/831072620": "'Alexan Lower Greenville Dog Park', a home: an apartment complex's own feature",
    "way/1451838323": "'Giants of the Savana', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1451838324": "'Wilds of Africa', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1451838325": "'Zoo North', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1451838326": "'Lacerte Family Children's Zoo', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "node/356701531": "'Carmelite Monastery', a religious residence",
    "way/473667664": "'Elm Fork Gun Club', a business's own feature under its own name",
    "way/525725014": "'The Donald and Charlotte Test Reflection Center', named for private persons: a personal name, not a place (owner, 2026-10-13)",
    "way/1337199274": "'Climbing Area', a description standing in for a name (owner, 2026-10-13)",
    "way/1327351275": "'Intramural Fields', an institution's own way, named for it",
    "way/1431713717": "'Neighborhood Public Park', a description standing in for a name (owner, 2026-10-13)",
    "way/9969387": "'Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1311185693": "'Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/10011052": "'Service Road North', a description standing in for a name (owner, 2026-10-13)",
    "way/358974885": "'Drive', a description standing in for a name (owner, 2026-10-13)",
    "way/9980280": "'De or Drive', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/9997382": "'North Canada Drive North', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/180521557": "'HerbandCollen Way', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/684448103": "'Communitiy access path', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1270205190": "'Trail Trial 1', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1425730230": "'12th Street Promenade / Oak Cliff Walk of Fame', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/355136782": "'Dog walk trail', a description standing in for a name (owner, 2026-10-13)",
    "way/1424696826": "'West sidewalk of Henderson Avenue', a description standing in for a name (owner, 2026-10-13)",
    "way/682539966": "'Richland College Walking/Jogging Path', a description standing in for a name (owner, 2026-10-13)",
    "way/1521055734": "'Richland College Walking/Jogging Path', a description standing in for a name (owner, 2026-10-13)",
    "way/9979189": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979198": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979199": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979200": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979190": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979192": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979194": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979196": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979197": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979202": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979203": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979205": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979206": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979207": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979208": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979211": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979213": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979215": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979216": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979217": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979218": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979221": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9979223": "'Brookside Village Mobile Home', a housing estate's own way, named for the estate",
    "way/9957160": "'Dell-Wood Mobile Home Park', a housing estate's own way, named for the estate",
    "way/10008910": "'Glenhaven Mhp', a housing estate's own way, named for the estate",
    "way/9974307": "'Honeysuckle Mobile Home Park', a housing estate's own way, named for the estate",
    "way/9974306": "'Honeysuckle Mobile Home Park', a housing estate's own way, named for the estate",
    "way/9984017": "'Lawson Ridge Mobile Home Park', a housing estate's own way, named for the estate",
    "way/9984019": "'Lawson Ridge Mobile Home Park', a housing estate's own way, named for the estate",
    "way/9984020": "'Lawson Ridge Mobile Home Park', a housing estate's own way, named for the estate",
    "way/9984022": "'Lawson Ridge Mobile Home Park', a housing estate's own way, named for the estate",
    "way/9984023": "'Lawson Ridge Mobile Home Park', a housing estate's own way, named for the estate",
    "way/9984024": "'Lawson Ridge Mobile Home Park', a housing estate's own way, named for the estate",
    "way/9974809": "'Mobile Home Villa', a housing estate's own way, named for the estate",
    "way/9974810": "'Mobile Home Villa', a housing estate's own way, named for the estate",
    "way/9974811": "'Mobile Home Villa', a housing estate's own way, named for the estate",
    "way/465027913": "'Mobile Home Villa', a housing estate's own way, named for the estate",
    "way/9974812": "'Mobile Home Villa', a housing estate's own way, named for the estate",
    "way/465027909": "'Mobile Home Villa', a housing estate's own way, named for the estate",
    "way/465027911": "'Mobile Home Villa', a housing estate's own way, named for the estate",
    "way/9993334": "'Highland Hills Shp Center', a shopping centre's own way, named for it",
    "way/612169544": "'Highland Hills Shp Center', a shopping centre's own way, named for it",
    "way/612169548": "'Highland Hills Shp Center', a shopping centre's own way, named for it",
    "way/10006505": "'Red Bird Center', a shopping centre's own way, named for it",
    "way/10006506": "'Red Bird Center', a shopping centre's own way, named for it",
    "way/981259224": "'Red Bird Center', a shopping centre's own way, named for it",
    "way/981259226": "'Red Bird Center', a shopping centre's own way, named for it",
    "way/9951189": "'Red Bird Mall', a shopping centre's own way, named for it",
    "way/9951191": "'Red Bird Mall', a shopping centre's own way, named for it",
    "way/1035052565": "'Red Bird Mall', a shopping centre's own way, named for it",
    "way/9951184": "'Red Bird Mall', a shopping centre's own way, named for it",
    "way/9951187": "'Red Bird Mall', a shopping centre's own way, named for it",
    "way/9951180": "'Southwest Center Mall', a shopping centre's own way, named for it",
    "way/560732066": "'Southwest Center Mall', a shopping centre's own way, named for it",
    "way/560732067": "'Southwest Center Mall', a shopping centre's own way, named for it",
    "way/564672578": "'Southwest Center Mall', a shopping centre's own way, named for it",
    "way/358974870": "'Casa Linda Plaza', a shopping centre's own way, named for it",
    "way/419239549": "'Casa Linda Plaza', a shopping centre's own way, named for it",
    "way/612106915": "'Casa Linda Plaza', a shopping centre's own way, named for it",
    "way/825454400": "'Casa Linda Plaza', a shopping centre's own way, named for it",
    "way/825454407": "'Casa Linda Plaza', a shopping centre's own way, named for it",
    "way/1435563620": "'Casa Linda Plaza', a shopping centre's own way, named for it",
    "way/1435563621": "'Casa Linda Plaza', a shopping centre's own way, named for it",
    "way/1435563623": "'Casa Linda Plaza', a shopping centre's own way, named for it",
    "way/560736798": "'Preston Center Plaza', a shopping centre's own way, named for it",
    "way/421728606": "'Royal Lane DART Station', an institution's own way, named for it",
    "way/600934380": "'Royal Lane DART Station', an institution's own way, named for it",
    "way/599521348": "'Mockingbird Station', an institution's own way, named for it",
    "way/573161504": "'Mockingbird Station', an institution's own way, named for it",
    "way/9978335": "'Mockingbird Station', an institution's own way, named for it",
    "way/599521329": "'Mockingbird Station', an institution's own way, named for it",
    "way/599521341": "'Mockingbird Station', an institution's own way, named for it",
    "way/1468557340": "'Mockingbird Station', an institution's own way, named for it",
    "way/9947306": "'Mt View College', an institution's own way, named for it",
    "way/104471102": "'Mt View College', an institution's own way, named for it",
    "way/104472362": "'Mt View College', an institution's own way, named for it",
    "way/562713978": "'Mt View College', an institution's own way, named for it",
    "way/9956743": "'Mt View College', an institution's own way, named for it",
    "way/9956756": "'Mt View College', an institution's own way, named for it",
    "way/9956767": "'Mt View College', an institution's own way, named for it",
    "way/104471139": "'Mt View College', an institution's own way, named for it",
    "way/505630072": "'Mt View College', an institution's own way, named for it",
    "way/104473807": "'Mt View College', an institution's own way, named for it",
    "way/505630071": "'Mt View College', an institution's own way, named for it",
    "way/9956768": "'Mt View College', an institution's own way, named for it",
    "way/104478210": "'Mt View College', an institution's own way, named for it",
    "way/600897483": "'Mt View College', an institution's own way, named for it",
    "way/600897486": "'Mt View College', an institution's own way, named for it",
    "way/1141827058": "'Mt View College', an institution's own way, named for it",
    "way/1143723540": "'Mt View College', an institution's own way, named for it",
    "way/15190559": "'Frankford Cemetery', an institution's own way, named for it",
    "way/15190548": "'Frankford Cemetery', an institution's own way, named for it",
    "way/448749010": "'Frankford Cemetery', an institution's own way, named for it",
    "way/448749011": "'Frankford Cemetery', an institution's own way, named for it",
    "way/9978109": "'Preston Trail Golf Club Drive', an institution's own way, named for it",
    "way/328834824": "'Preston Trail Golf Club Drive', an institution's own way, named for it",
    "way/497536284": "'Pet Station', description: a pet area under a describing label, by id (flag check, 2026-10-13)",
}
