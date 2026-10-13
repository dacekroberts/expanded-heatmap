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
    "way/10529264": "'Congress Avenue Los Roblvdes Boulevard Alley', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/10520690": "'Martin Luther King Boulevard 39th StreetAlley', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1026250702": "'12th Street Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1026254703": "'12th Street Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1026250701": "'North 12th Street Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1026250703": "'North 12th Street Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1026255577": "'North 12th Street Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1370114250": "'Sunbeam Avenue Cycle Track', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1314252988": "'19th Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1217618961": "'21st Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1284706245": "'21st Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1284706246": "'21st Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1371939561": "'21st Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1371939562": "'21st Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1418975105": "'21st Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/694148473": "'J Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1120176825": "'J Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1120176826": "'J Street Cycleway', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/574635007": "'Alley 1', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/574635008": "'Alley 2', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/339772041": "'Alley 3', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/339772042": "'Alley 4', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/574634945": "'Alley 5', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/574635006": "'Alley 5', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/574635009": "'Alley 6', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/339772044": "'Alley 7', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/499048026": "'Alley 8', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/339772045": "'Alley 9', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/339772043": "'Alley 10', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511134": "'10th Avenue 11th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529488": "'11th Avenue 12th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529490": "'11th Avenue 12th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1108306285": "'11th Avenue 12th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10515432": "'11th Avenue 14th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500772": "'12th Ave 13th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500770": "'12th Avenue 13th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517666": "'12th Avenue Temple Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519369": "'13th Avenue 14th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505284": "'14th Avenue 15th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10515601": "'14th St 17th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10509784": "'15th Avenue 16th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516712": "'15th Avenue 16th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10526560": "'15th Street 16th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529432": "'16th Avenue 18th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513897": "'16th Avenue 19th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513898": "'16th Avenue 19th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513894": "'17th Ave 18th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517726": "'18th Avenue 19th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519878": "'18th Street 19th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505212": "'19th Avenue 20th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505213": "'19th Avenue 20th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505214": "'19th Avenue 20th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528394": "'19th Avenue 20th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517583": "'1st Avenue 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517584": "'1st Avenue 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517585": "'1st Avenue 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10509498": "'20th Avenue 21st Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514113": "'20th Street 21st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514114": "'20th Street 21st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/332230579": "'20th Street 21st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519131": "'21st Ave 22nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519130": "'21st Avenue 22nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504866": "'21st Street 22nd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504869": "'21st Street 22nd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514729": "'22nd Avenue 23rd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514730": "'22nd Avenue 23rd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530873": "'22nd Street 21st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528141": "'22nd Street 23rd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528142": "'22nd Street 23rd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513888": "'23rd Avenue Franklin Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1160955083": "'23rd Avenue Franklin Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522116": "'23rd Street 24th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518916": "'24th Street 21st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505722": "'24th Street 25th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505723": "'24th Street 25th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10515544": "'25th Street 26th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528474": "'25th Street Hermosa Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10507502": "'26th Street 27th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10531623": "'27th Street 28th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524576": "'27th Street Franklin Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/653835635": "'27th Street Franklin Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10515483": "'2nd Avenue 3rd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524885": "'2nd Avenue 3rd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/503436622": "'2nd Avenue 3rd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532350": "'32nd Street 33rd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532352": "'32nd Street 33rd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532353": "'32nd Street 33rd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525690": "'33rd Street 34th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525691": "'33rd Street 34th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525693": "'33rd Street 34th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525694": "'33rd Street 34th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524363": "'34 Street 35 Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10527127": "'34th Street 35th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10527128": "'34th Street 35th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10527129": "'34th Street 35th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518886": "'35th Street 36th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518887": "'35th Street 36th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500550": "'35th Street Santa Ynez Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10510850": "'36th Street 37th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10510851": "'36th Street 37th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1560192432": "'36th Street 37th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1560192433": "'36th Street 37th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1560192434": "'36th Street 37th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1560192435": "'36th Street 37th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516916": "'36th Street Gerber Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10520545": "'37th Street 38th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511917": "'38th Street 39th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514438": "'39th Street 40th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514439": "'39th Street 40th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516966": "'39th Street 40th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1063236316": "'39th Street 40th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505029": "'39th Street la Solidad Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525372": "'3rd Avenue 4th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525373": "'3rd Avenue 4th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525375": "'3rd Avenue 4th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525377": "'3rd Avenue 4th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/357273225": "'41st St 43rd St Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/813345603": "'41st St 43rd St Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/813345604": "'41st St 43rd St Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530049": "'41st Street 42nd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530050": "'41st Street 42nd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516176": "'42nd Street Mission Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10523849": "'47th Street 48th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10523850": "'47th Street 48th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517246": "'48 Avenue 49th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524367": "'48th Avenue 50th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10515727": "'48th Street 49th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/232484850": "'48th Street 49th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518269": "'48th Street Discovery Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518217": "'49th Street 50th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518218": "'49th Street 50th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530139": "'4th Avenue 35th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524640": "'4th Avenue 5th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500645": "'4th Avenue Marshall Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500646": "'4th Avenue Marshall Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500647": "'4th Avenue Marshall Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524960": "'4th Avenue Rears Lane Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529178": "'50th Avenue 51st Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10510064": "'50th Street 51st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/941406774": "'50th Street 51st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/941406775": "'50th Street 51st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521767": "'51st Avenue 52nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519365": "'51st Street 52nd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/941406772": "'51st Street 52nd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/941406773": "'51st Street 52nd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521635": "'52nd Avenue Edinger Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524334": "'52nd Street 53rd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524336": "'52nd Street 53rd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528221": "'52nd Street 53rd Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518008": "'53rd Street 54th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/941406769": "'53rd Street 54th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/941406770": "'53rd Street 54th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501365": "'54th Street 55th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/896440363": "'54th Street 55th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/896440365": "'54th Street 55th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/941406768": "'54th Street 55th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511505": "'55th Street 56th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501973": "'55th Street 57th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505667": "'58th Street 60th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/560061544": "'59th St Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10510263": "'59th Street 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528054": "'5th Avenue 6th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513529": "'5th Avenue Bigler Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516395": "'5th Avenue Donner Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516396": "'5th Avenue Donner Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/310420335": "'5th Avenue Donner Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10531390": "'60th Street 61st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525985": "'63rd St Fruitridge Road Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521639": "'63rd Street 64th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1106985031": "'63rd Street 64th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/939267604": "'64th Street 65th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10515223": "'65th Street 66th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521020": "'7th Ave 8th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522764": "'7th Ave 9th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521021": "'7th Avenue 8th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521022": "'7th Avenue 8th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521023": "'7th Avenue 8th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522765": "'7th Avenue 9th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524298": "'8th Avenue 9th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513525": "'9th Avenue 10th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513526": "'9th Avenue 10th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504738": "'A Street B Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10531196": "'Acari Ave Dawnelle Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10508906": "'Acoma Street Barstow Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10526268": "'Alamos Ave Las Palmas Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511479": "'Alder Street Fell Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529891": "'Altos Avenue Rio Linda Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524699": "'Arden Way el Monte Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524700": "'Arden Way el Monte Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519724": "'Ashland Way Freeport Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10527850": "'Attawa Ave 24th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10515502": "'Auburn Blvd Plover Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517405": "'Balsan Street Marysville Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10533436": "'Barstow Street Colfax Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524417": "'Beaumont Street Empress Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10503038": "'Belden Street Haywood Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501590": "'Belden Street Sendero Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517322": "'Bell Ave Katherine Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/928167759": "'Bowden Square Way Club Center Dr Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518540": "'Boxwood Street Erickson Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10502955": "'Branch Street Belden Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511157": "'Branch Street May Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511159": "'Branch Street May Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501832": "'Brand Way B Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/305458218": "'Breezy Meadow Drive Fern Glen Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514500": "'Broadway 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513017": "'Broadway Burnett Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528266": "'Burnett Way Sloat Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/313997061": "'C Street D Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528715": "'C Street Elvas Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516572": "'Calvados Avenue Arden Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/926114740": "'Calvados Avenue Arden Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/926114744": "'Calvados Avenue Arden Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/926114745": "'Calvados Avenue Arden Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529438": "'Cambridge Street Beaumont Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10517599": "'Cantalier Street Oakmont Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528897": "'Carmelita Avenue Ford Road Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10503454": "'Carnation Ave 30th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516331": "'Clay Street Dry Creek Road Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529166": "'Colfax Street Dale Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10531307": "'Cypress Street Branch Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10531308": "'Cypress Street Branch Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/313997062": "'D Street Mc Kinley Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525662": "'Dale Avenue Edgewater Road Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518391": "'Darina Ave Dixieanne Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10531178": "'Dawnelle Way Bridgecross Drive Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10523431": "'Del Paso Blvd Alamos Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10508419": "'Del Paso Blvd Calvados Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10533488": "'Del Paso Blvd Las Palmas Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529982": "'Del Paso Boulevard Eleanor Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500837": "'Del Paso Boulevard Lochbrae Road Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/930126946": "'Del Paso Boulevard Lochbrae Road Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10514959": "'Del Paso Boulevard Redwood Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516665": "'Del Paso Boulevard Rio Linda Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522016": "'Del Paso Boulevard el Monte Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10507580": "'Discovery Way 49th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10526643": "'Downey Way Miller Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532509": "'Dry Creek Road Alder Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10508524": "'E Street F Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/194706334": "'East Commerce Way Alan Shepard St. Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522264": "'Edgewater Road Fernley Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/502934393": "'El Camino Ave Darina Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10520312": "'El Camino Ave Redwood Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519609": "'El Camino Ave del Paso Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/560973092": "'El Camino Avenue Redwood Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/560988928": "'El Camino Avenue Redwood Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529065": "'El Camino Avenue Santiago Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521348": "'El Monte Avenue del Paso Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532116": "'Elm Street Fig Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530499": "'Elvas Ave F Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10503419": "'Elvas Avenue Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/807043130": "'Elvas Avenue Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516295": "'Elvas St A Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524414": "'Empress Street Boxwood Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522624": "'F St Elvas Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501620": "'F Street G Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530313": "'Fairfield Street Cantalier Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1076562110": "'Fairfield Street Cantalier Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501768": "'Fairfield Street Rio Linda Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519608": "'Fell Street High Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10502828": "'Fernley Avenue Grove Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10502245": "'Fig Street Balsam Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10503399": "'Folsom Boulevard Q Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10515278": "'Ford Road Union Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529944": "'Forrest Street Fairfield Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10508042": "'Freeport Boulevard Carmela Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10531070": "'Freeport Boulevard Fegan Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10533502": "'Freeport Boulevard La Campana Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518868": "'Freeport Boulevard Lotus Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500898": "'Frienza Avenue Santiago Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10527666": "'G Street H Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/305458226": "'Golden Willow Avenue Terracina Drive Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511180": "'Grand Avenue Lindsay Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10507558": "'Grande Ave Roanoke Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513063": "'Grove Avenue Gibson Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1059465788": "'Grove Avenue Gibson Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511280": "'Grove Avenue Hawthorne Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1562431812": "'H Street I Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529648": "'H Street J Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529649": "'H Street/J Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518706": "'Harris Avenue Morrison Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10507159": "'Haywood Street Clay Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10507160": "'Haywood Street Clay Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10527049": "'Hermosa Street Ventura Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532791": "'High Street Huron Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518974": "'Huron Street Elm Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529853": "'Ivy Street Jasmine Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504809": "'J Street K Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10508148": "'J Street M Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518422": "'Jasmine Street Kern Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501229": "'Jeffrey Avenue East Pacific Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530837": "'K Street L Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530841": "'K Street L Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521830": "'Kasner Avenue South Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519865": "'Katherine Ave Youngs Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10526248": "'Kern Street Lily Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521854": "'Kesner Avenue South Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10506848": "'L Street M Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504715": "'La Pera Ct G Parkway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504716": "'Lanatt St Fern Court Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522858": "'Lily Street Mahogany Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505746": "'Lindsay Avenue Morey Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501757": "'M Street Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501758": "'M Street Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501759": "'M Street Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1391048983": "'M Street Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519232": "'Mahogany Street Natoma Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/48146538": "'Mahogany Street Natoma Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504816": "'Markham Way 3rd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10521409": "'Marshall Way 5th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10520691": "'Martin Luther King Boulevard 39th Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511895": "'Marysville Blvd Barcon Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10507510": "'Marysville Blvd del Paso Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/503758389": "'Marysville Blvd del Paso Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/503758390": "'Marysville Blvd del Paso Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10520416": "'Marysville Boulevard Ivy Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525138": "'May Street Belden Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525139": "'May Street Belden Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10525140": "'May Street Belden Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529581": "'May Street Belden Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10508388": "'Mc Kinley Boulevard 41st Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10529157": "'Mc Laren Ave Freeport Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522596": "'Meister Way Mc Kinley Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1068094021": "'Meister Way Mc Kinley Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504462": "'Miller Way Sherman Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530155": "'Montrose Street Douglas Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/350685154": "'Moonlit Bay Way Portage Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511932": "'Morey Avenue Kesner Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10512834": "'Morrison Avenue Grand Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504131": "'N Street Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504132": "'N Street Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528055": "'Natoma Way Presidio Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10506697": "'North 12th St Ahern Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532869": "'O Donnell Ave Jean Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10503576": "'Oakmont Street Cambridge Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/926114739": "'Oakmont Street Cambridge Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/926114742": "'Oakmont Street Cambridge Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516109": "'Opal Lane Sonoma Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10508404": "'Ortega St 64th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10527716": "'P Street Q Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513475": "'Palmetto Street Cypress Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524180": "'Piedmont Dr Riverside Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532905": "'Portola Way 5th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10533580": "'Potrero Way Oregon Drive Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528178": "'Presidio Street Pinell Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1059465787": "'Redwood Ave Barrette Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10527883": "'Redwood Ave Stanford Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524763": "'Rio Linda Blvd Cypress Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10509718": "'Rio Linda Blvd del Paso Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524761": "'Rio Linda Boulevard Cypress Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524762": "'Rio Linda Boulevard Cypress Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524764": "'Rio Linda Boulevard Cypress Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10524889": "'Riverside Blvd 13th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10510411": "'Rose Street Palmetto Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1136524515": "'Rose Street Palmetto Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/281980558": "'Rose Street Rio Linda Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/560073640": "'Rose Street Rio Linda Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516074": "'S Street Serra Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10497968": "'S Street T Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504878": "'S Street T Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504879": "'S Street T Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1330053368": "'S Street T Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1330053369": "'S Street T Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1330053370": "'S Street T Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501094": "'Sandlin Way Folsom Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501573": "'Santa Ynez Way 36th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10510077": "'Santiago Ave el Camino Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/845932885": "'Santiago Ave el Camino Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10533584": "'Sendero Street Alvarado Boulevard Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516923": "'Serra Way T Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505132": "'Sherman Way Y Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/840802864": "'Sherman Way Y Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10531880": "'Silvano Street Brae Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10510029": "'Sloat Way 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10510030": "'Sloat Way 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1471847851": "'Sloat Way 2nd Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500252": "'Stockton Blvd Sherman Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522428": "'Stockton Boulevard 50th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10522430": "'Stockton Boulevard 50th Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/359214008": "'Summerwind Way Rush River Drive Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10532504": "'Sutterville Road 15th Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530893": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530895": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530897": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530899": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10530900": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/479390416": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1560418016": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1560418017": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1562253894": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1562253895": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1562253896": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/1562253897": "'T Street U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/305458236": "'Terracina Drive Yellowwood Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10516541": "'Traction Avenue Arden Way Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10533166": "'Traction Avenue Fairfield Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10509638": "'Union Street Evans Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10500134": "'V Street W Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/332230582": "'Vizcaya Walk U Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10526408": "'W Street X Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10513625": "'West Pacific Avenue Jeffrey Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10519270": "'Willow Street Ivy Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10501022": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528144": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528145": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528146": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528147": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528148": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528149": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10528150": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/543271927": "'X Street Broadway Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10507757": "'X Street Y Street Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504444": "'Y Street 1st Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504445": "'Y Street 1st Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10504446": "'Y Street 1st Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10511231": "'Youngs Ave Jessie Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10518953": "'Yreka Ave Florin Road Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
    "way/10505187": "'Zurlo Way Acari Avenue Alley', an alley named by its two cross streets or by a number: a description (owner, 2026-10-13)",
}
