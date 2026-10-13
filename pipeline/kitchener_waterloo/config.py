"""Kitchener–Waterloo (Regional)-specific settings, scoped to one city per this
project's per-city folder architecture (see docs/project_context.md,
"Architecture").

Scaffolded by scripts/scaffold_city.py.

TWO CITIES, ONE PAGE (Regional): Kitchener and Waterloo together, the two
municipalities ION runs through; either alone is a stub (Kitchener 11 stops,
Waterloo 8). Cambridge, whose ION stage 2 is only planned, is not in scope.

THE BUSINESSES are the Region of Waterloo Public Health's two inspection
registers, each published twice: as ArcGIS point layers (the premises and its
point, no type below "Food, General") and as bulk zips (the same premises
with a SUBCATEGORY, and two years of inspections). Step 2 joins them on the
facility id (owner, 2026-09-30: use SUBCATEGORY, so food shops are their own
layer and institutional kitchens go by type).
"""

from pathlib import Path

SLUG = "kitchener_waterloo"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kitchener_waterloo" / "raw"
DATA_PROCESSED = ROOT / "data" / "kitchener_waterloo" / "processed"
OUTPUTS = ROOT / "outputs" / "kitchener_waterloo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the two cities. ION never leaves them, so step 1 writes
# this with a header and no rows (Calgary's precedent) and exits if a station
# ever falls outside.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# What step 2 left out and why, one row per premises (trade names only; the
# telephone field is never fetched).
EXCLUDED_PREMISES_CSV = OUTPUTS / "excluded_premises.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) --------------

# The Region's OpenData MapServer. Each layer is served through its own
# ArcGIS proxy id, so the two inspection layers have different bases.
MAPSERVER_FOOD = ("https://utility.arcgis.com/usrsvcs/servers/61a7a8d8775e4da381d9718658c0d842/"
                  "rest/services/OpenData/OpenData/MapServer")
MAPSERVER_PERSONAL = ("https://utility.arcgis.com/usrsvcs/servers/d96eeb0cd02e4b45ba52bc1a918c6218/"
                      "rest/services/OpenData/OpenData/MapServer")
FOOD_LAYER_URL = f"{MAPSERVER_FOOD}/17"          # Food Inspection Facilities
PERSONAL_LAYER_URL = f"{MAPSERVER_PERSONAL}/18"  # Personal Services Inspection Facilities
# The fields fetched, by name. NEVER SiteTelephone: a home-based operator's
# phone is a person's, and a field that is never fetched cannot leak.
LAYER_FIELDS = ["FacilityMasterID", "FacilityName", "Category", "SiteStreet", "SiteCity"]
FOOD_LAYER_GEOJSON = DATA_RAW / "food_facilities.geojson"
PERSONAL_LAYER_GEOJSON = DATA_RAW / "personal_facilities.geojson"

# The bulk tables. ⚠ THIS HOST FAILS PYTHON'S TLS HANDSHAKE (DH_KEY_TOO_SMALL:
# the server offers a Diffie-Hellman key OpenSSL's default security level
# refuses), so fetch_sources.py downloads them with the system curl, which
# negotiates another suite. Certificate verification stays on either way;
# the security level is never lowered. The CSVs inside are cp1252.
ZIP_BASE = "https://webapps.regionofwaterloo.ca/open-data-downloads/SSIS/Hedgehog"
FOOD_ZIP_URL = f"{ZIP_BASE}/Inspections.zip"
PERSONAL_ZIP_URL = f"{ZIP_BASE}/Inspections_PS.zip"
FOOD_ZIP = DATA_RAW / "Inspections.zip"
PERSONAL_ZIP = DATA_RAW / "Inspections_PS.zip"
FOOD_ZIP_MEMBERS = ("Facilities_OpenData.csv", "Inspections_OpenData.csv")
PERSONAL_ZIP_MEMBERS = ("Facilities_PS_OpenData.csv", "Inspections_PS_OpenData.csv")
ZIP_ENCODING = "cp1252"

# THE TWO CITIES' BOUNDARIES: the Region's own "Cities and Towns" layer
# (MapServer 15), one polygon per municipality, under the same licence as the
# registers. Kitchener measures 138.4 km2 and Waterloo 64.5 km2 (2026-09-30);
# the gates catch a changed polygon.
BOUNDARY_URL = f"{MAPSERVER_FOOD}/15"
CITY_NAMES = ("Kitchener", "Waterloo")
CITY_BOUNDARY_GEOJSON = DATA_RAW / "cities_and_towns.geojson"
CITY_AREA_KM2 = {"Kitchener": (133.0, 144.0), "Waterloo": (60.0, 69.0)}

# THE REGION'S OWN ION STOPS (MapServer 5): gate 3's count, not the drawn
# stations (those are OSM's). Stage 1's constructed LRT stops.
ION_STOPS_URL = f"{MAPSERVER_FOOD}/5"
ION_STOPS_JSON = DATA_RAW / "ion_stops.json"

OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
RAIL_BBOX = (43.38, -80.60, 43.52, -80.40)          # south, west, north, east

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 17N: the longitude (~-80.52) falls in the -84 to -78 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32617"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: the 19 stops' median gap is about 610 m (the brief's
# 613 m), over the ~550 m line. Step 1 prints and gates it.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# RAIL FROM OPENSTREETMAP (the light-rail builds' source): ION, Grand River
# Transit route 301, two direction relations. A WHITELIST on ref + route,
# never the network tag alone. ION's stage-1 bus (aBRT route 302) is a bus
# and is not drawn.
ROUTE_TYPES = ("light_rail", "subway", "tram")    # what the query fetches
LINE_REFS = ("301",)
OPERATOR = "Grand River Transit"
# Relations in the box that are NOT drawn, each named with its reason; step 1
# exits on any other relation it cannot place.
NOT_DRAWN = {}

LINE_NAMES = {"301": "ION"}
# OSM's colour tag on both relations, #244895, sat 20.9 Delta-E from the
# Retail pins' blue (the food shops), so it is moved the least distance that
# clears 46 from all three (pipeline/linecolour.py): darker, the same navy
# hue, 25.2 from the original.
LINE_COLOURS = {"301": "#12164b"}

STATION_NAME_ALIASES = {}
COLLAPSE_MAX_SPREAD_M = 250

SPACING_MIN_M = 550.0

# GATE 3: the Region's own ION Stops layer - stage 1's constructed LRT stops,
# one row per platform name (a split stop such as Frederick / Queen is two
# names there and two stations here).
OPERATOR_STATION_COUNTS = {"ION": 19}
OPERATOR_COUNTS_SOURCE = ("the Region of Waterloo's ION Stops layer (OpenData MapServer 5): "
                          "19 constructed stage-1 LRT stops")

# --- Business filtering ------------------------------------------------

# The zips' own date (every member is stamped 2026-07-03, and the inspections
# run to that day). The currency clock: a premises counts when Public Health
# inspected it within two years before this date - the registers carry no
# status or closing date (Ottawa's rule).
AS_OF_DATE = "2026-07-03"
CURRENCY_YEARS = 2

# In-city rows are identified by point-in-boundary against the two cities'
# polygons, never by `SiteCity` (82 spellings: KITCHENER, Kitchener ONT,
# "Dr., Kitchener"...).
CITY_KEEP = None

# Personal-services names read at the build as a person's own that the shared
# shape test cannot see (it takes two words; these are three). Step 2 shows
# their type instead, as it does for the two-word ones. A three-word version
# of the test was measured and rejected: it flagged 26 trade names (FIRST
# CHOICE HAIRCUTTERS, NEW AGE LASER) for this one.
# Keys, not names (pipeline/name_keys.py): a new name's key is its output.
PERSON_NAMES = {
    "6677a5860f02a84c",
}

TAXONOMY_SYSTEM = "kitchener_waterloo_inspection"
RAW_CLASSIFICATION_COLUMN = "premises_kind"

# Sanity bounds: the two cities' extent plus a margin.
KITCHENER_WATERLOO_BBOX = {
    "lat_min": 43.33,
    "lat_max": 43.56,
    "lon_min": -80.64,
    "lon_max": -80.37,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3602062153,3602062154)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
PLACE_DROPPED = {
    "node/7742395209": "'Waterloo', a tourist or heritage ride indexed as a station: not transit (owner, 2026-10-13)",
    "way/154217734": "'Joseph Schneider Haus National Historic Site', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/7985356773": "'Shelmerdine Grave', a plaque or grave under a private person's name (owner, 2026-10-13)",
    "way/43352710": "'Zion United / Rockway Mennonite', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "relation/2062154": "'Waterloo', the city boundary's center as a second place row beside the city's own: a duplicate (owner, 2026-10-13)",
    "way/385344932": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/385344933": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/385344950": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/385344952": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/385344953": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/385344955": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/489597506": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/489597508": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/796648986": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/796648987": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/1196254199": "'243 Grey Silo Road', an address standing in for a street's name: a driveway, not a street",
    "way/181920012": "'6 Upper Mercer Street', an address standing in for a street's name: a driveway, not a street",
    "way/181920703": "'6 Upper Mercer Street', an address standing in for a street's name: a driveway, not a street",
    "way/181920776": "'6 Upper Mercer Street', an address standing in for a street's name: a driveway, not a street",
    "way/1099768083": "'6 Upper Mercer Street', an address standing in for a street's name: a driveway, not a street",
    "way/182042806": "'7 Upper Mercer Street', an address standing in for a street's name: a driveway, not a street",
    "way/182042864": "'7 Upper Mercer Street', an address standing in for a street's name: a driveway, not a street",
    "way/182042877": "'7 Upper Mercer Street', an address standing in for a street's name: a driveway, not a street",
    "way/217653485": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/217653486": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/217653487": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/217653488": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/255979205": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/255979206": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/255979207": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/255979675": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/255979677": "'875 University Avenue East', an address standing in for a street's name: a driveway, not a street",
    "way/291018630": "'Alberts Alley 🟦', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/177586088": "'Path to Chandler', a description standing in for a name (owner, 2026-10-13)",
    "way/583061384": "'Path to Grand River Trail', a description standing in for a name (owner, 2026-10-13)",
    "way/547702814": "'Walter Bean Path Entrance', a description standing in for a name (owner, 2026-10-13)",
    "way/45892245": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/207231894": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/350394208": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/836255144": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/836255145": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/836255146": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/893859316": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/893859317": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/951358761": "'Main Path', a description standing in for a name (owner, 2026-10-13)",
    "way/165513425": "'Conestoga Mall Lane', a shopping centre's own way, named for it",
    "way/180723529": "'Conestoga Mall Lane', a shopping centre's own way, named for it",
    "way/229456788": "'Rim Campus Lane', an institution's own way, named for it",
    "way/447728776": "'Rim Campus Lane', an institution's own way, named for it",
    "way/447728777": "'Rim Campus Lane', an institution's own way, named for it",
    "way/447728778": "'Rim Campus Lane', an institution's own way, named for it",
    "way/471785068": "'Rim Campus Lane', an institution's own way, named for it",
    "way/471785069": "'Rim Campus Lane', an institution's own way, named for it",
    "way/471785070": "'Rim Campus Lane', an institution's own way, named for it",
    "way/471785071": "'Rim Campus Lane', an institution's own way, named for it",
    "way/471785072": "'Rim Campus Lane', an institution's own way, named for it",
    "way/471785073": "'Rim Campus Lane', an institution's own way, named for it",
    "way/471785074": "'Rim Campus Lane', an institution's own way, named for it",
    "way/1130782832": "'Rim Campus Lane', an institution's own way, named for it",
    "way/1130782840": "'Rim Campus Lane', an institution's own way, named for it",
    "way/1130782905": "'Rim Campus Lane', an institution's own way, named for it",
    "way/1130782923": "'Rim Campus Lane', an institution's own way, named for it",
    "way/1130783004": "'Rim Campus Lane', an institution's own way, named for it",
    "way/1130783005": "'Rim Campus Lane', an institution's own way, named for it",
    "way/27127252": "'University Campus Lane', a description standing in for a name (owner, 2026-10-13)",
    "way/43251459": "'University Campus Lane', a description standing in for a name (owner, 2026-10-13)",
    "way/130345764": "'University Campus Lane', a description standing in for a name (owner, 2026-10-13)",
    "way/382765103": "'University Campus Lane', a description standing in for a name (owner, 2026-10-13)",
    "way/382765146": "'University Campus Lane', a description standing in for a name (owner, 2026-10-13)",
    "way/141865697": "'The Bargain Bridge', a business's own feature under its own name",
    "way/165126457": "'The Grand Manors of Sims Estate', a housing estate's own way, named for the estate",
    "way/210695612": "'The Grand Manors of Sims Estate', a housing estate's own way, named for the estate",
    "way/750971915": "'The Grand Manors of Sims Estate', a housing estate's own way, named for the estate",
    "way/852243392": "'The Grand Manors of Sims Estate', a housing estate's own way, named for the estate",
    "way/871409692": "'The Grand Manors of Sims Estate', a housing estate's own way, named for the estate",
    "way/871409693": "'The Grand Manors of Sims Estate', a housing estate's own way, named for the estate",
    "way/1370119458": "'Copper Street Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/182091551": "'Village Green', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/152354970": "'B.C. Matthews Hall Green', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/576111990": "'Graduate House Green', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/182950659": "'Mathematics 3 Green', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/182460938": "'Science Quad', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/290274346": "'WLU Quad', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
}
