"""Buffalo-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

NEW YORK'S MULTI-SOURCE PATTERN, at one city's scale (the multi-source-city
skill). Buffalo's own Business Licenses file is a regulated-activity list, so
coverage is three registries: the City's licences (food service and a retail
slice), NYS Retail Food Stores (grocery) and NYS Appearance Enhancement and
Barber businesses (personal services). `pipeline/taxonomies/buffalo.py`
dispatches on `source`.
"""

from pathlib import Path

SLUG = "buffalo"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "buffalo" / "raw"
DATA_PROCESSED = ROOT / "data" / "buffalo" / "processed"
OUTPUTS = ROOT / "outputs" / "buffalo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is. NFTA Metro Rail never leaves
# Buffalo, so step 1 writes this file with a header and no rows (Calgary's
# precedent) - and exits if a station ever falls outside.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 1 writes the line (track ways only) for load_geojson_line_shapes.
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) --------------

# RAIL FROM OPENSTREETMAP, NOT NFTA'S GTFS (owner, 2026-09-29). NFTA's feed is
# current (26FALL, 2026-08-27 to 2026-12-05) and was not rejected for being
# stale: its licence bars using "NFTA trademarks ... in association with the
# Data", and a permanent "NFTA Metro Rail" label beside the drawn Data is that
# use if NFTA claims the name as a mark. OSM's relations carry the geometry,
# the stops and the public name under ODbL, so the agreement never binds the
# map. The feed is not fetched; the page's 20-minute statement cites NFTA's
# published schedule.
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
# One Overpass query for the city box: every tram, light-rail and subway
# relation in it, so step 1 must name anything it does not draw.
RAIL_BBOX = (42.82, -78.95, 42.97, -78.79)          # south, west, north, east

# THE CENSUS BUREAU'S PLACE POLYGON (TIGERweb, current Incorporated Places,
# GEOID 3611000) - a US federal government work, public domain, the layer
# family Washington D.C. already reads. NOT the City's "City Boundary"
# (Socrata p4ak-r4fg): the licence read (2026-09-29) found that layer is Erie
# County's municipal-boundary geometry, vertex for vertex, labelled "U.S.
# Census Bureau" in error; the City's public-domain dedication may not reach
# a County work, and the County states no terms. Owner, 2026-09-29: take the
# clean title. TIGER's polygon includes 31.3 km2 of Lake Erie and Niagara
# River water, where there are no businesses and no stations.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_BOUNDARY_QUERY = {"where": "GEOID='3611000'", "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# The polygon's area as TIGER draws it, land and water, gated in step 1.
CITY_AREA_KM2 = (130.0, 142.0)

# The City's licence codes step 2 reads (`descript`), downloaded WITH their
# expired rows: `licstatus` says Active on every one of 12,131 rows (the brief,
# 2026-09-29), so expiry is applied here, by date, not by the server.
CITY_LICENCE_CODES = (
    "Restaurant", "Restaurant Take Out", "Restaurant / Dance",
    "Bakers and Confectioners", "Caterer",
    "Food Store", "Meat Fish & Poultry", "Used Car Dealer", "Second Hand Dealer",
    "Tobacco Hookah Vaping", "Pawnbroker", "Pet Shop",
    "Self-Srv Laundry / Dry Cleaner", "Clothes-Dry Cleaners Permit",
    "Sidewalk Cafe",
)

# Each source: the raw file, the endpoint, the server-side query applied at
# download, and the columns step 2 reads. `name_column` is always a TRADE
# name; no source's person-name column is ever selected.
SOURCES = {
    "city": {
        "file": DATA_RAW / "city_licences.csv",
        "endpoint": "https://data.buffalony.gov/resource/qcyy-feh8.csv",
        # Explicit $select: ids, the two names, the code, dates, parcel,
        # address and point. The file carries no licensee-person column.
        "query": {
            "$select": "uniqkey,licenseno,businessname,dbaname,code,descript,"
                       "licstatus,licensedttm,issdttm,expdttm,prclid,address,"
                       "city,zip,latitude,longitude",
            "$where": "descript in(" + ",".join(
                "'" + c + "'" for c in CITY_LICENCE_CODES) + ")",
            "$limit": "50000",
        },
        "key_column": "uniqkey",
        # ⚠ THE NAMES ARE THE OTHER WAY ROUND: `businessname` is the trade name
        # (DOLLAR GENERAL STORE #14886), `dbaname` usually the legal entity
        # (DOLGENCORP OF NEW YORK INC). Display businessname (owner).
        "name_column": "businessname",
        "category_column": "descript",
    },
    "nys_store": {
        "file": DATA_RAW / "nys_retail_food_stores.csv",
        "endpoint": "https://data.ny.gov/resource/9a8c-vfzj.csv",
        # Postal city BUFFALO reaches into Cheektowaga and Amherst: 596 rows,
        # 421 inside the city. Step 2 scopes by point-in-boundary; the city
        # filter here only bounds the download.
        "query": {
            "$select": "license_number,operation_type,estab_type,entity_name,"
                       "dba_name,street_number,street_name,address_line_2,city,"
                       "zip_code,county,georeference",
            "$where": "upper(city)='BUFFALO'",
            "$limit": "50000",
        },
        "key_column": "license_number",
        "name_column": "dba_name",
        "category_column": "estab_type",
    },
    "nys_salon": {
        "file": DATA_RAW / "nys_appearance_enhancement.csv",
        "endpoint": "https://data.ny.gov/resource/y3u4-jbgh.csv",
        # license_holder_name is NEVER selected, and step 2 asserts it.
        "query": {
            "$select": "license_number,license_type,business_name,"
                       "business_address_1,business_address_2,business_city,"
                       "business_zip,georeference",
            "$where": "upper(business_city)='BUFFALO'",
            "$limit": "50000",
        },
        "key_column": "license_number",
        "name_column": "business_name",
        "category_column": "license_type",
    },
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 17N: Buffalo (~-78.87) falls in the -84 to -78 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32617"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: the 14 stations' median gap is 594 m (the brief; the
# light-rail test's OSM read 609 m), over the ~550 m line. Step 1 prints it.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# NFTA Metro Rail: one line, 14 stations, all inside the city. OSM's two
# route relations (3517747, 11364343) carry network NFTA, ref "Metro". A
# WHITELIST on network + ref + route, never network alone.
ROUTE_TYPES = ("light_rail", "subway", "tram")    # what the query fetches
NETWORK = "NFTA"
REF = "Metro"
# Relations in the box that are NOT drawn, each named with its reason (the
# Bucheon lesson: step 1 refuses a relation it cannot place). Filled from the
# build's own read of the cache.
NOT_DRAWN = {}

LINE_KEY = "metro"
# The public name, with the agency, as the brief and the owner settled.
LINE_NAMES = {LINE_KEY: "NFTA Metro Rail"}
# OSM's relations carry #004990; render_heatmap's shared check scores it.
LINE_COLOURS = {LINE_KEY: "#004990"}

# One stop under two names (the two directions' stop nodes) - none known yet;
# explicit, never a rule.
STATION_NAME_ALIASES = {}

SPACING_MIN_M = 400.0

# GATE 3: NFTA publishes 14 stations for Metro Rail (the brief's read of its
# own rail GTFS, 2026-09-29: 14 by name, all named in the brief).
OPERATOR_STATION_COUNTS = {"NFTA Metro Rail": 14}
OPERATOR_COUNTS_SOURCE = "NFTA's rail GTFS (26FALL), read by the brief 2026-09-29: 14 stations"

# --- Business filtering ------------------------------------------------

# The fetch date: the expiry cut-off (Chicago's rule - a licence expiring
# before it is not active). Step 2 re-applies it, so a re-run and a drift
# check stay deterministic. Set by fetch_sources.py's run.
AS_OF_DATE = "2026-09-29"

# In-city rows are identified by point-in-boundary against the City's polygon,
# never by a city-name field.
CITY_KEEP = None

TAXONOMY_SYSTEM = "buffalo"
RAW_CLASSIFICATION_COLUMN = "business_category"

# Sanity bounds: the City's polygon (104.6 km2) extent plus ~0.02 deg.
BUFFALO_BBOX = {
    "lat_min": 42.80,
    "lat_max": 42.98,
    "lon_min": -78.94,
    "lon_max": -78.77,
}
