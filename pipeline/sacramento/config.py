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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3606232940)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
PLACE_DROPPED = {
    "node/4124586741": "'Central Pacific Freight Depot', a tourist or heritage ride indexed as a station: not transit (owner, 2026-10-13)",
    "node/7700904748": "'Saint Francis of Assisi Friary', a religious residence",
    "way/485439022": "'Access road', a description standing in for a name (owner, 2026-10-13)",
    "way/310316492": "'future access', a business's own feature under its own name",
    "way/543059968": "'future access', a business's own feature under its own name",
    "way/10530690": "'East Entrance', a description standing in for a name (owner, 2026-10-13)",
    "way/568438840": "'dog park path', a description standing in for a name (owner, 2026-10-13)",
    "way/568440556": "'dog park path', a description standing in for a name (owner, 2026-10-13)",
    "way/568451408": "'large rock path', a description standing in for a name (owner, 2026-10-13)",
    "way/469493943": "'natomas walking path', a description standing in for a name (owner, 2026-10-13)",
    "way/568441085": "'softball path', a description standing in for a name (owner, 2026-10-13)",
    "way/469491390": "'terracina walking path', a description standing in for a name (owner, 2026-10-13)",
    "way/496384029": "'Kroy Way / 65th St walkway', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/10527289": "'57th Street 58th Street Pedestrian Path', a description standing in for a name (owner, 2026-10-13)",
    "way/112090980": "'Jedediah Smith National Recreation Trail Access', a description standing in for a name (owner, 2026-10-13)",
    "way/1214243959": "'Jedediah Smith National Recreation Trail Access', a description standing in for a name (owner, 2026-10-13)",
    "way/1214243960": "'Jedediah Smith National Recreation Trail Access', a description standing in for a name (owner, 2026-10-13)",
    "way/10509627": "'Procter and Gamble Dw', a driveway described, not a street's name",
    "way/10509629": "'Procter and Gamble Dw', a driveway described, not a street's name",
    "way/10509634": "'Procter and Gamble Dw', a driveway described, not a street's name",
    "way/10509635": "'Procter and Gamble Dw', a driveway described, not a street's name",
    "way/1396481040": "'Procter and Gamble Dw', a driveway described, not a street's name",
    "way/1396481041": "'Procter and Gamble Dw', a driveway described, not a street's name",
    "way/1396481042": "'Procter and Gamble Dw', a driveway described, not a street's name",
    "way/10515908": "'Department of Trans Dw', a driveway described, not a street's name",
    "way/10515912": "'Department of Trans Dw', a driveway described, not a street's name",
    "way/503629230": "'Department of Trans Dw', a driveway described, not a street's name",
    "way/10512327": "'Mhp Road', a housing estate's own way, named for the estate",
    "way/10512384": "'Sacramento Inn Way', a business's own way, named for the business",
    "way/615088069": "'Sacramento Inn Way', a business's own way, named for the business",
    "way/1247987642": "'Sacramento Inn Way', a business's own way, named for the business",
    "way/10527551": "'4000 Foodlink Street', a business's own feature under its own name",
    "way/1042135622": "'4000 Foodlink Street', a business's own feature under its own name",
    "way/1042135624": "'4000 Foodlink Street', a business's own feature under its own name",
    "way/1042135625": "'4000 Foodlink Street', a business's own feature under its own name",
    "way/1042135626": "'4000 Foodlink Street', a business's own feature under its own name",
    "way/1042135627": "'4000 Foodlink Street', a business's own feature under its own name",
    "way/10514770": "'Florin Perkins Landfill', not a street: another kind of object indexed as one",
    "way/10533519": "'L and D Landfill', not a street: another kind of object indexed as one",
    "way/10524194": "'Fruitridge Transfer Station', not a street: another kind of object indexed as one",
    "way/10524195": "'Fruitridge Transfer Station', not a street: another kind of object indexed as one",
    "way/358362857": "'Laguna Village', not a street: another kind of object indexed as one",
    "way/499961408": "'Laguna Village', not a street: another kind of object indexed as one",
    "way/543281544": "'Laguna Village', not a street: another kind of object indexed as one",
    "way/1061282596": "'Laguna Village', not a street: another kind of object indexed as one",
    "way/10526904": "'Rancho S Luado Drive', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/10514517": "'Coral Gablvdes Ct Meadowview Alley', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/10520690": "'Martin Luther King Boulevard 39th StreetAlley', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/560061544": "'59th St Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514500": "'Broadway 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513017": "'Broadway Burnett Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529649": "'H Street/J Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10520691": "'Martin Luther King Boulevard 39th Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/332230582": "'Vizcaya Walk U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501022": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528144": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528145": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528146": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528147": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528148": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528149": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528150": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/543271927": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
}
