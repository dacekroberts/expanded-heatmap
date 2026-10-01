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
