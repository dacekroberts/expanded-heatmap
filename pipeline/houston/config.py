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
