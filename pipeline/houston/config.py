"""Houston-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

The Texas Comptroller's Active Sales Tax Permit Holders (a table with NO
geometry), placed by an address join to the City's Site Addresses and the US
Census Bureau's geocoder for the residue - step 2 cleans, step 3 places,
step 4 maps. Rail from OpenStreetMap (owner, 2026-09-29): METRO's GTFS comes
under a Data Use Agreement heavier than any this project has read, and it
never binds the map (docs/build_briefs/houston.md).
"""

from pathlib import Path

SLUG = "houston"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "houston" / "raw"
DATA_PROCESSED = ROOT / "data" / "houston" / "processed"
OUTPUTS = ROOT / "outputs" / "houston"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
BUSINESSES_PLACED_CSV = DATA_PROCESSED / "businesses_geocoded.csv"   # the name every placed city uses
SITE_ADDRESSES_PARQUET = DATA_PROCESSED / "site_addresses.parquet"
GEOCODE_CACHE_DIR = DATA_RAW / "geocode_cache"

# --- Raw inputs (fetch_sources.py downloads; no step fetches, and step 3's
# geocoder refuses under HEATMAP_NO_NETWORK) ---------------------------------

# The Texas Comptroller's Active Sales Tax Permit Holders (data.texas.gov
# jrea-zgmq, public domain), one row per outlet.
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
REGISTER_WHERE = ("upper(outlet_city)='HOUSTON' "
                  "AND outlet_inside_outside_city_limits_indicator='Y'")
REGISTER_CSV = DATA_RAW / "sales_tax_permits_houston.csv"

# The City's Site Addresses (COHGIS, public domain: "COHGIS data is in the
# public domain and may be copied without permission"), the bulk file geodatabase
# the Hub links as ArcGIS item 82f3487741d84516ae6f64680474344a. Taken whole
# rather than through the FeatureServer, which pages at 2,000.
SITE_ADDRESSES_URL = "https://mycity.houstontx.gov/mycitydocs/download/Export_SiteAddresses.zip"
SITE_ADDRESSES_ZIP = DATA_RAW / "Export_SiteAddresses.zip"

# OSM: every light-rail relation in METRO's box.
RAIL_BBOX = (29.60, -95.50, 29.90, -95.25)        # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"

# THE CENSUS BUREAU'S PLACE POLYGON (TIGERweb, current Incorporated Places,
# GEOID 4835000; a US federal government work, public domain) - Buffalo's
# layer. NOT OSM's relation 2688911: measured 2026-09-29, OSM draws 1,589.5 km2
# where TIGER draws 1,741.5 (land 1,659.7 + water 80.9), and 156 km2 of
# TIGER's polygon is missing from OSM's in annexed pieces on the west and
# north edges (the largest 23.5 km2 near 29.79 N, 95.75 W); OSM has 4 km2
# TIGER lacks. The legal boundary the City reports to the Census wins.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_BOUNDARY_QUERY = {"where": "GEOID='4835000'", "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# The polygon's area as TIGER draws it, land and water, gated in step 1.
CITY_AREA_KM2 = (1700.0, 1780.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 15N: the longitude (~-95.37) falls in the -96 to -90 band. Derived
# per city, not copied.
CRS_PROJECTED = "EPSG:32615"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: 657 m median gap (the brief), over the ~550 m line.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# METRORail, all three lines, every station inside the City of Houston (all
# 40 are). Frequency (the brief): Red every 6 min, Green and Purple every 12
# by day - all clear the 15-minute test.
LINE_REFS = ("Red", "Green", "Purple")
OSM_NETWORK = "Metro"          # as OSM tags it

# ref -> the public name (owner, 2026-09-29: "Red Line", "Green Line",
# "Purple Line" - the lowest-risk wording the licence read named; only
# "METRO" is a licensed mark).
LINE_NAMES = {"Red": "Red Line", "Green": "Green Line", "Purple": "Purple Line"}
# Chosen through pipeline/linecolour.py (CIE76 against the pin colours,
# 2026-09-29), never METRO's own hexes. A pure red sits 33-37 from Food
# service's magenta and a mid green 25-39 from Personal services', so both
# moved: brick red 46.5, olive green 46.5, purple 50.6 - each over the 45
# preference, and each still reads as its name.
LINE_COLOURS = {"Red": "#bf360c", "Green": "#5d6d0e", "Purple": "#7b1fa2"}

# ONE STATION PER DOWNTOWN COUPLET: Green and Purple run one-way on Capitol
# and Rusk, one stop on each street, 99-141 m apart (the brief), which would
# draw two nearly coincident ring sets. Merged by explicit alias, never a
# rule (Oslo's). OSM already carries Theater District and Convention District
# as one name each, and splits only Central Station. Burnett's name differs
# by direction: METRO's current one is kept.
STATION_NAME_ALIASES = {
    "Central Station Capitol": "Central Station Capitol / Rusk",
    "Central Station Rusk": "Central Station Capitol / Rusk",
    "Burnett Transit Center": "Burnett Transit Center/Casa de Amigos",
}

# DOWNTOWN RED LINE PLATFORMS ARE STAGGERED: each direction stops on its own
# block of Main Street. Main Street Square's two stop positions are 267 m
# apart on OSM (29.7576,-95.3644 and 29.7556,-95.3660), over step 1's 250 m
# merge gate; one station, allowed by name so the gate stays tight elsewhere.
STAGGERED_PLATFORMS_M = {"Main Street Square": 300}

# GATE 3, per line after the couplets merge: Red 25, Green 9, Purple 10, 40 in
# all. The 40 is the brief's count of METRO's static feed (2026-09-29, counted,
# never used); the brief's per-line "Purple 13" did not sum to it (25 + 9 + 13
# less the four shared stations is 43) and was corrected at build: Purple's
# ten are listed in order by Wikipedia's Purple Line article (read 2026-09-29),
# and OSM's two Purple relations carry the same ten.
OPERATOR_STATION_COUNTS = {"Red Line": 25, "Green Line": 9, "Purple Line": 10}
OPERATOR_TOTAL_STATIONS = 40
OPERATOR_COUNTS_SOURCE = ("METRO's static feed via the brief (40 stations), Wikipedia's "
                          "Purple Line list (10), read 2026-09-29")

SPACING_MIN_M = 300.0

# --- Business filtering ------------------------------------------------

AS_OF_DATE = "2026-09-29"
CITY_KEEP = "HOUSTON"

TAXONOMY_SYSTEM = "naics"
RAW_CLASSIFICATION_COLUMN = "outlet_naics_code"

# The organisation type for an individual sole owner (the Comptroller's code).
SOLE_OWNER_TYPE = "IS"

# Sanity bounds for placed points: the city's extent plus a margin.
HOUSTON_BBOX = {
    "lat_min": 29.45,
    "lat_max": 30.15,
    "lon_min": -95.85,
    "lon_max": -94.95,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3602688911)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
PLACE_DROPPED = {
    "way/52499737": "'Coolgreen Park', not yet open by its own tags (owner, 2026-10-13)",
    "way/1113369158": "'Apache-Elbert Triangle', a description standing in for a name (owner, 2026-10-13)",
    "way/615900993": "'Hermann Park', another object's name on this one: not the thing its name says",
    "node/356709678": "'Lamar High School', another object's name on this one: not the thing its name says",
    "way/433640048": "'Donor Walls', a description standing in for a name (owner, 2026-10-13)",
    "way/1300364802": "'Clarks', a business's own feature under its own name",
    "way/1300364803": "'Dean's Credit Clothing', a business's own feature under its own name",
    "way/1470127818": "'Family Play Area', a description standing in for a name (owner, 2026-10-13)",
    "way/615434013": "'Park for Humans and Dogs', a home: a residential complex's own feature",
    "way/595192459": "'Woodway Square Park', a home: a residential complex's own feature",
    "node/13461068252": "'Point 1', a placeholder standing in for a name",
    "node/13461068253": "'Point 2', a placeholder standing in for a name",
    "way/544153913": "'empty lot', a description standing in for a name (owner, 2026-10-13)",
    "way/1339758302": "'Houston City College Park', a placeholder standing in for a name",
    "node/9535215157": "'South Belt Central Business Park', a business's own feature under its own name",
    "node/356828135": "'Blessed Sacrament Catholic Church Convent', a religious residence",
    "way/366856860": "'Villa De Matel Convent', a religious residence",
    "node/11851085600": "'Clay Road Baptist T', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1414024242": "'Masjid', a bare type word for a name (owner, 2026-10-13)",
    "node/8398624583": "'Prayer Space', a description standing in for a name (owner, 2026-10-13)",
    "way/1418241225": "'Sanctuary', a bare type word for a name (owner, 2026-10-13)",
    "way/388945054": "'Sanctuary', a bare type word for a name (owner, 2026-10-13)",
    "way/769568484": "'Sanctuary', a bare type word for a name (owner, 2026-10-13)",
    "node/12308803991": "'Holy Cross Lutheran', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/1299354702": "'Glenbrook United Methodist Church Sanctuary', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/15450593": "'Baybrook Mall', a shopping centre's own way, named for it",
    "way/178230581": "'Baybrook Mall', a shopping centre's own way, named for it",
    "way/494709435": "'Baybrook Mall', a shopping centre's own way, named for it",
    "way/559904581": "'Baybrook Mall', a shopping centre's own way, named for it",
    "way/708326086": "'Baybrook Mall', a shopping centre's own way, named for it",
    "way/708326090": "'Baybrook Mall', a shopping centre's own way, named for it",
    "way/15431144": "'Jamestown Mall', a shopping centre's own way, named for it",
    "way/15370628": "'Tarrytown Mall', a shopping centre's own way, named for it",
    "way/15362942": "'Watertown Mall', a shopping centre's own way, named for it",
    "way/37517864": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/37517989": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/42722738": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/42722742": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/42722800": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/42853490": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/42853491": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/42854015": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/42860573": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/42860574": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/104104940": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/104104943": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/104675907": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/104746961": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/107921320": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/107921326": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/107921330": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/107921339": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/107921347": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/107921356": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875348": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875363": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875371": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875379": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875391": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875405": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875420": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875447": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/127288978": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/127288984": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/174860576": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099488": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099494": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099498": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099500": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099504": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099506": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099507": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099510": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099520": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099524": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099552": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099555": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099559": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099565": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099571": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099582": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/176099602": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/193427401": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/193427414": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/599227721": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/634591466": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/947242803": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/988092631": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/1343709181": "'US 59 (Eastex Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/15452233": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/29370388": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/45874475": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/45874619": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/45874620": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/51823903": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/104714050": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/104714060": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/104714065": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/104727136": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/106963865": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/106963882": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/107692818": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/107692822": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/108269008": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/124875408": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859681": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859691": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859693": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859696": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859697": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859701": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859710": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859719": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859721": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859722": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859725": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859730": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859881": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126859882": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860211": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860213": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860217": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860220": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860225": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860232": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860234": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860239": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860240": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/126860245": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/128437173": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/128437174": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/128437176": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/129117172": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/155972694": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/155972730": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/155981147": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/155981153": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/193478703": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/193478704": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209385913": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209385914": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209392628": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209392634": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209395104": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209395107": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209396274": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209396276": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209399178": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209399185": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209399432": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209399443": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209399617": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/209399620": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/322008893": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/527296837": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/568369282": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/568369283": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/568601910": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/568602118": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/997247304": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/998796085": "'US 59 (Southwest Freeway) HOV/HOT lane', a lane type as a street's name: a description (owner, 2026-10-13)",
    "way/423436534": "'Westpark Tollway Ramp', a description standing in for a name (owner, 2026-10-13)",
    "way/423436535": "'Westpark Tollway Ramp', a description standing in for a name (owner, 2026-10-13)",
    "way/43031561": "'Entrance 18', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1394565718": "'Entrance 18', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/1424154122": "'Entrance 18', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/15378136": "'Gate 1 Road', a description standing in for a name (owner, 2026-10-13)",
    "way/15378138": "'Gate 1 Road', a description standing in for a name (owner, 2026-10-13)",
    "way/477717613": "'Gate 1 Road', a description standing in for a name (owner, 2026-10-13)",
    "way/15427286": "'Gate 2 Road', a description standing in for a name (owner, 2026-10-13)",
    "way/443455179": "'Fuel Storage Road', a description standing in for a name (owner, 2026-10-13)",
    "way/959123653": "'Fuel Storage Road', a description standing in for a name (owner, 2026-10-13)",
    "way/48594213": "'Landfill 2 Road', a description standing in for a name (owner, 2026-10-13)",
    "way/959123656": "'Landfill 2 Road', a description standing in for a name (owner, 2026-10-13)",
    "way/15445130": "'Lower Level Road', a description standing in for a name (owner, 2026-10-13)",
    "way/15445134": "'Lower Level Road', a description standing in for a name (owner, 2026-10-13)",
    "way/498138556": "'Lower Level Road', a description standing in for a name (owner, 2026-10-13)",
    "way/15444418": "'Security Patrol Road', a description standing in for a name (owner, 2026-10-13)",
    "way/443600049": "'Security Patrol Road', a description standing in for a name (owner, 2026-10-13)",
    "way/15402304": "'Security Road', a description standing in for a name (owner, 2026-10-13)",
    "way/959123650": "'Security Road', a description standing in for a name (owner, 2026-10-13)",
    "way/983143767": "'Security Road', a description standing in for a name (owner, 2026-10-13)",
    "way/833326392": "'Coast Guard Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/15371812": "'Parcel Three', not a street: another kind of object indexed as one",
    "way/339536684": "'Olive Garden', a private way the private-street rule did not reach",
    "way/431231415": "'Olive Garden', a private way the private-street rule did not reach",
    "way/460418570": "'Olive Garden', a private way the private-street rule did not reach",
    "way/460418571": "'Olive Garden', a private way the private-street rule did not reach",
    "way/156937672": "'Terraces on Memorial', a home: an apartment complex's own feature",
    "way/258186241": "'Terraces on Memorial', a home: an apartment complex's own feature",
    "way/258186242": "'Terraces on Memorial', a home: an apartment complex's own feature",
    "way/258186243": "'Terraces on Memorial', a home: an apartment complex's own feature",
    "way/481943538": "'Terraces on Memorial', a home: an apartment complex's own feature",
    "way/481943539": "'Terraces on Memorial', a home: an apartment complex's own feature",
    "way/21871010": "'Champion Rod and Gun Club Road', a business's own way, named for the business",
    "way/15368123": "'San Jacinto College One Boulevard', an institution's own way, named for it",
    "way/15290865": "'East Rent Car Road', a description standing in for a name (owner, 2026-10-13)",
    "way/995542206": "'East Rent Car Road', a description standing in for a name (owner, 2026-10-13)",
    "way/995542207": "'East Rent Car Road', a description standing in for a name (owner, 2026-10-13)",
    "way/475862691": "'South Rent Car Road', a description standing in for a name (owner, 2026-10-13)",
    "way/587259840": "'West Rent Car Road', a description standing in for a name (owner, 2026-10-13)",
    "way/136507588": "'Mockingbird Trail Unpaved Access', a description standing in for a name (owner, 2026-10-13)",
    "way/255495201": "'Quail Trail Unpaved Access', a description standing in for a name (owner, 2026-10-13)",
    "way/985632561": "'Quail Trail Unpaved Access', a description standing in for a name (owner, 2026-10-13)",
    "way/1499088548": "'Quail Trail Unpaved Access', a description standing in for a name (owner, 2026-10-13)",
    "way/1499088884": "'Quail Trail Unpaved Access', a description standing in for a name (owner, 2026-10-13)",
    "way/1499089249": "'Quail Trail Unpaved Access', a description standing in for a name (owner, 2026-10-13)",
    "way/1134510749": "'Robin Trail Unpaved Access', a description standing in for a name (owner, 2026-10-13)",
    "way/467044277": "'White Oak Bayou Greenway Access', a description standing in for a name (owner, 2026-10-13)",
    "way/1392404381": "'White Oak Bayou Greenway Access Ramp', a description standing in for a name (owner, 2026-10-13)",
    "way/242551516": "'Reddleshire Trail Access', a description standing in for a name (owner, 2026-10-13)",
    "way/456870034": "'Reddleshire Trail Access', a description standing in for a name (owner, 2026-10-13)",
    "way/456870035": "'Reddleshire Trail Access', a description standing in for a name (owner, 2026-10-13)",
    "way/87075366": "'George Bush Hike and Bike Trail Access', a description standing in for a name (owner, 2026-10-13)",
    "way/634368182": "'East Lawn Foot Path', a description standing in for a name (owner, 2026-10-13)",
    "way/1281823910": "'East Lawn Foot Path', a description standing in for a name (owner, 2026-10-13)",
    "way/1281823911": "'East Lawn Foot Path', a description standing in for a name (owner, 2026-10-13)",
    "way/624804654": "'Junior League Foot Path', a description standing in for a name (owner, 2026-10-13)",
    "way/690355488": "'Junior League Foot Path', a description standing in for a name (owner, 2026-10-13)",
    "way/469326924": "'Woodland Oaks Park path', a description standing in for a name (owner, 2026-10-13)",
    "way/232402669": "'Tidwell Fountains Lane Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/232402670": "'Tidwell Fountains Lane Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/598265163": "'Tidwell Fountains Lane Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/598265164": "'Tidwell Fountains Lane Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/987650922": "'Tidwell Fountains Lane Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/987650923": "'Tidwell Fountains Lane Road', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
}
