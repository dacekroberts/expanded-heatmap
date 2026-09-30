"""Sacramento-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

The City's Business Operation Tax register (a table with NO geometry),
placed by the US Census Bureau's batch geocoder (owner, 2026-09-29) - Los
Angeles' step shape: step 2 cleans, step 3 geocodes, step 4 maps. Rail from
OpenStreetMap: SacRT's GTFS host serves an expired certificate, and SSL is
never bypassed.
"""

from pathlib import Path

SLUG = "sacramento"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "sacramento" / "raw"
DATA_PROCESSED = ROOT / "data" / "sacramento" / "processed"
OUTPUTS = ROOT / "outputs" / "sacramento"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
BUSINESSES_GEOCODED_CSV = DATA_PROCESSED / "businesses_geocoded.csv"
GEOCODE_CACHE_DIR = DATA_RAW / "geocode_cache"

# --- Raw inputs (fetch_sources.py downloads; no step fetches, and step 3's
# geocoder refuses under HEATMAP_NO_NETWORK) ---------------------------------

# The City's Business Operation Tax Information (ArcGIS table, item f4ee567a…).
# ⚠ COLUMNS NEVER TO LOAD: Principal_Owner_First_name, Principal_Owner_Last_Name,
# Primary_Phone_number and every Mail_* field. The download names its columns
# explicitly and step 2 asserts none of these arrived.
REGISTER_URL = ("https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/"
                "account_data_with_header_NEW/FeatureServer/0/query")
REGISTER_FIELDS = (
    "OBJECTID", "Account_Number", "Business_Name", "Business_Description",
    "Business_Start_Date", "Business_Close_Date", "Current_Expire_Date",
    "Current_License_Status", "Location_Street_Number", "Location_Direction",
    "Location_Street_Name", "Location_Street_Type", "Location_Unit",
    "Location_City", "Location_State", "Location_Zip_code",
)
FORBIDDEN_COLUMNS = ("Principal_Owner_First_name", "Principal_Owner_Last_Name",
                     "Primary_Phone_number", "Mail_Street_Number", "Mail_Street_Direction",
                     "Mail_Street_name", "Mail_Unit", "Mail_City", "Mail_State",
                     "Mail_Zip_code", "Mail_Street_Type")
REGISTER_WHERE = "Current_License_Status = 'Active'"
REGISTER_CSV = DATA_RAW / "business_operation_tax_active.csv"

# OSM: every light-rail relation in SacRT's box (Folsom included, so step 1 can
# name every station outside the city), and the city and county boundaries.
RAIL_BBOX = (38.45, -121.58, 38.72, -121.10)        # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_BOUNDARIES_JSON = DATA_RAW / "osm_boundaries.json"
OSM_CITY_RELATION = 6232940          # City of Sacramento, 257 km2 (the brief)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 10N: Sacramento (~-121.49) falls in the -126 to -120 band. Derived
# per city, not copied.
CRS_PROJECTED = "EPSG:32610"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: 765 m median gap (the brief), over the ~550 m line.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# SacRT light rail, Blue and Gold, stations inside the City of Sacramento.
# Frequency (SacRT's own schedule pages, 2026-09-29): Blue every 15 min
# 05:03-17:48 then every 30 to 22:48; Gold 4 an hour at Sacramento Valley
# Station by day, every 30 in the evening. Both clear the 15-minute test.
#
# ⚠ THE GREEN LINE IS NOT DRAWN: SUSPENDED since 16 June 2025 for the
# Railyards works; trains in testing since 14 September 2026, "not available
# for passenger boarding", reopening expected "by mid-October"
# (sacrt.com/greenline, read 2026-09-29). Drawn as the service runs - Berlin's
# U6 rule (owner, 2026-09-29). Its only Green-only station is recorded as
# closed for works; the others are Blue or Gold stations and stay. A dated
# PLAN item adds the line, the new 7th & Railyards station and its frequency
# once SacRT's schedules list it again.
LINE_REFS = ("Blue", "Gold")
NOT_DRAWN_REFS = {"Green": "suspended since 2025-06-16 (Railyards construction); "
                           "reopening expected mid-October 2026"}
CLOSED_FOR_WORKS = {
    "7th & Richards/Township 9": (
        "Green Line, closed for works (Railyards construction) since 16 June 2025, "
        "reopening expected mid-October 2026 (SacRT)"),
}

# ref -> the public name, with the mode word as SacRT signs it.
LINE_NAMES = {"Blue": "Blue Line", "Gold": "Gold Line"}
# OSM's relations: Gold #ffba00, Blue #002666; render_heatmap scores them.
LINE_COLOURS = {"Blue": "#002666", "Gold": "#ffba00"}

# ONE STATION PER DOWNTOWN COUPLET (owner, 2026-09-29): the one-way couplets on
# 7th and 8th Streets put one stop on each street, 124-141 m apart (measured on
# OSM's stop positions), which would draw two nearly coincident ring sets.
# Houston's Capitol/Rusk precedent. SacRT names each stop separately, so the
# merged station carries both names. 8th & O (234 m from 8th & Capitol) stays
# its own station. Explicit, never a rule.
STATION_NAME_ALIASES = {
    "7th & Capitol": "7th & Capitol / 8th & Capitol",
    "8th & Capitol": "7th & Capitol / 8th & Capitol",
    "7th & I/County Center": "7th & I / 8th & H (County Center)",
    "8th & H/County Center": "7th & I / 8th & H (County Center)",
    "St. Rose of Lima Park": "St. Rose of Lima Park / 8th & K",
    "8th & K": "St. Rose of Lima Park / 8th & K",
}

# STOP NODES OSM LEAVES UNNAMED, named from the station they belong to. Blue's
# two stop positions between Franklin and Meadowview carry no name; OSM's
# station node 4420963540 and stop area 18776735 beside them are "Morrison
# Creek", which SacRT's Blue timetable lists (read 2026-09-29). Step 1 stops
# once OSM names them, so the entry retires itself.
UNNAMED_STOP_NAMES = {12633107412: "Morrison Creek", 12633107413: "Morrison Creek"}

# STATIONS SACRT SERVES THAT OSM HAS NOT MAPPED, added BY ID with their source
# (Taoyuan's rule). Dos Rios, a Blue Line infill station on North 12th Street,
# opened 28 September 2026 and is on SacRT's Blue timetable between Globe and
# Alkali Flat/La Valentina; OSM carries no object for it. Placed at Wikidata's
# coordinate (CC0; owner, 2026-09-29: "Wikidata for now, replace with OSM when
# we can"). Step 1 STOPS once OSM's Blue relations carry a stop of this name.
ADDED_STATIONS = {
    "Dos Rios": {"wikidata": "Q107175168", "line": "Blue",
                 "between": ("Globe", "Alkali Flat/La Valentina")},
}

# GATE 3: SacRT's own timetables (sacrt.com/routes-schedules, read 2026-09-29):
# Blue lists 28 stations Watt/I-80 -> CRC; Gold 27 Historic Folsom ->
# Sacramento Valley Station. Counted per line BEFORE the couplet merge, on
# SacRT's one-direction lists.
OPERATOR_STATION_COUNTS = {"Blue Line": 28, "Gold Line": 27}
OPERATOR_COUNTS_SOURCE = "SacRT's Blue and Gold timetables, one direction each, read 2026-09-29"

SPACING_MIN_M = 400.0

# --- Business filtering ------------------------------------------------

# The fetch date: a licence expiring before it is not active (Chicago's rule;
# 2,768 Active rows were past Current_Expire_Date on the brief's read).
AS_OF_DATE = "2026-09-29"
# The City's own location city; "ON FILE" means the address is withheld
# (mostly home businesses) - unmappable by construction.
CITY_KEEP = "SACRAMENTO"

TAXONOMY_SYSTEM = "sacramento"
RAW_CLASSIFICATION_COLUMN = "business_category"

# Sanity bounds for geocoded points: the city's extent plus a margin.
SACRAMENTO_BBOX = {
    "lat_min": 38.42,
    "lat_max": 38.72,
    "lon_min": -121.60,
    "lon_max": -121.33,
}
