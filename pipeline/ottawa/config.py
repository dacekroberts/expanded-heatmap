"""Ottawa-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

A FOOD-ONLY PAGE (owner, 2026-09-29: Band B's reduced-bucket bar). The one
source is Ottawa Public Health's food-safety inspection feed, published in
Yelp's LIVES format: every premises OPH inspects, with the feed's own point.
It carries NO type field, so restaurants and food shops (groceries,
convenience stores, pharmacies that sell food) are one layer, and the page
says so. Kitchener-Waterloo's food layer is the same shape.
"""

from pathlib import Path

SLUG = "ottawa"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ottawa" / "raw"
DATA_PROCESSED = ROOT / "data" / "ottawa" / "processed"
OUTPUTS = ROOT / "outputs" / "ottawa"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city. The O-Train never leaves Ottawa, so step 1
# writes this with a header and no rows (Calgary's precedent) and exits if a
# station ever falls outside.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# What step 2 left out and why, one row per premises (the names are trade
# names; the feed has no person column but the phone, never read).
EXCLUDED_PREMISES_CSV = OUTPUTS / "excluded_premises.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) --------------

# THE INSPECTION FEED (ArcGIS item 7e5a6428ed674d66a500f87c3ab0b2a1, a
# Document Link). The item says "This dataset will be retired in Q1 2026",
# yet the feed is rebuilt daily (feed_date 20260929), so it is cached on
# first fetch and never re-downloaded without --force.
# ⚠ THE HOST SITS BEHIND A BOT CHALLENGE for a client with no user agent
# (curl's default got Imperva's "Pardon Our Interruption" page, 6 KB of HTML
# with HTTP 200); the project's identifying user agent is served the zip.
# fetch_sources.py checks the zip signature, so an HTML answer never lands in
# the cache as data.
FEED_URL = "https://opendata.ottawa.ca/inspections/yelp_ottawa_healthscores_FoodSafety.zip"
FEED_ZIP = DATA_RAW / "yelp_ottawa_healthscores_FoodSafety.zip"

# THE CITY'S OWN WARDS, DISSOLVED (Wards 2022-2026, item
# 8973061e1b0c4cd09b4495088c04c310), under the same Open Government Licence -
# City of Ottawa as the feed. Vancouver's precedent: the wards tile the city,
# so their union is the city. The area gate catches a dropped ward.
CITY_BOUNDARY_URL = ("https://services.arcgis.com/G6F8XLCl5KtAlZ2G/arcgis/rest/services/"
                     "Wards_2022_2026/FeatureServer/0/query")
CITY_BOUNDARY_QUERY = {"where": "1=1", "outFields": "*", "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "wards_2022_2026.geojson"
# Ottawa is ~2,790 km2 of land (the amalgamated city); the 24 wards dissolve
# to 2,892.4 km2 (measured 2026-09-29), the difference being the Ottawa and
# Rideau rivers they reach into. The gate would catch one dropped ward.
CITY_AREA_KM2 = (2850.0, 2950.0)
WARD_COUNT = 24

OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
RAIL_BBOX = (45.20, -76.00, 45.55, -75.40)          # south, west, north, east

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 18N: Ottawa (~-75.70) falls in the -78 to -72 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32618"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: the 25 stations' median gap is 884 m (the screen), well
# over the ~550 m line. Step 1 prints and gates it.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# RAIL FROM OPENSTREETMAP (the owner's rail choice for the light-rail builds;
# OC Transpo's GTFS licence is unread). The O-Train's three lines, operator OC
# Transpo, two direction relations each. A WHITELIST on operator + ref +
# route, never the network tag alone.
ROUTE_TYPES = ("light_rail", "subway", "tram")    # what the query fetches
OPERATOR = "OC Transpo"
LINE_REFS = ("1", "2", "4")
# Relations in the box that are NOT drawn, each named with its reason; step 1
# exits on any other relation it cannot place.
NOT_DRAWN = {}

LINE_NAMES = {"1": "O-Train Line 1", "2": "O-Train Line 2", "4": "O-Train Line 4"}
# OSM carries no colour tags. OC Transpo's own network-map colours (red,
# green, gold), each moved the least distance that clears 45 Delta-E from all
# three category pins (pipeline/linecolour.py): Line 1 #DA291C -> #D41F11 (it
# sat 44.1 from Food service's magenta), Line 2 #65A233 -> #739C0D (34.2 from
# Personal services' green, and darkening alone never cleared it), Line 4
# kept. Pairwise 99.5 / 61.4 / 53.9.
LINE_COLOURS = {"1": "#D41F11", "2": "#739C0D", "4": "#F2A900"}

# OSM names a station's platforms by direction ("Blair O-Train West/Ouest",
# "Blair O-Train"), Lyon's two platforms "Lyon A" / "Lyon B", and two stations
# bilingually ("Dow's Lake / Lac Dow", "Airport / Aéroport": shown in English,
# as OSM names the other 23). Step 1 strips the direction
# suffix by rule and applies these aliases, then refuses any name whose stop
# positions spread wider than it allows.
STATION_NAME_ALIASES = {
    "Lyon A": "Lyon", "Lyon B": "Lyon",
    "UOttawa": "uOttawa", "Airport / Aéroport": "Airport", "Dow's Lake / Lac Dow": "Dow's Lake",
}
COLLAPSE_MAX_SPREAD_M = 250

SPACING_MIN_M = 550.0

# GATE 3: stations per line - Line 1 13 (Blair to Tunney's Pasture; Stage 2's
# east and west extensions not yet open), Line 2 11 (Bayview to Limebank),
# Line 4 3 (South Keys to Airport); Bayview and South Keys are shared, so 25.
# NOT OC Transpo's own pages: octranspo.com answers a scripted client 403
# (2026-09-29), and that refusal is respected, not worked around. Wikipedia's
# line infoboxes are the source, the Brazilian builds' fallback.
OPERATOR_STATION_COUNTS = {"O-Train Line 1": 13, "O-Train Line 2": 11, "O-Train Line 4": 3}
OPERATOR_COUNTS_SOURCE = ("Wikipedia's Line 1 / Line 2 / Line 4 (O-Train) infoboxes, revisions "
                          "of 2026-09-19: 13, 11 and 3 stations (octranspo.com refuses scripted "
                          "clients)")

# --- Business filtering ------------------------------------------------

# The fetch date (the feed's own feed_date). The currency clock: a premises
# counts when OPH inspected it within two years before this date - the feed
# has no status or closing date, so the inspection is the only sign of life.
AS_OF_DATE = "2026-09-29"
CURRENCY_YEARS = 2

# In-city rows are identified by point-in-boundary against the dissolved
# wards, never by `city` (OTTAWA, Ottawa, OTATWA, Manotick, Kanata...).
CITY_KEEP = None

TAXONOMY_SYSTEM = "ottawa_inspection"
RAW_CLASSIFICATION_COLUMN = "premises_kind"

# Sanity bounds: the amalgamated city's extent plus a margin.
OTTAWA_BBOX = {
    "lat_min": 44.95,
    "lat_max": 45.55,
    "lon_min": -76.40,
    "lon_max": -75.24,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3604136816)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
PLACE_DROPPED = {
    "relation/7057829": "'Chapel Hill South', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/12170991637": "'Artillery Piece', a description standing in for a name (owner, 2026-10-13)",
    "way/1289234021": "'Helicopter', a bare type word for a name (owner, 2026-10-13)",
    "way/1289234022": "'LAV', a type or model word standing in for a name (owner, 2026-10-13)",
    "node/9767324163": "'Plane', a bare type word for a name (owner, 2026-10-13)",
    "node/1772920299": "'T-33', a type or model word standing in for a name (owner, 2026-10-13)",
    "node/9767324164": "'Tank', a bare type word for a name (owner, 2026-10-13)",
    "node/12033927455": "'2017 Ottawa', a description standing in for a name (owner, 2026-10-13)",
    "node/11954817794": "'Bob Mills Plaque', a plaque or grave under a private person's name (owner, 2026-10-13)",
    "node/11340125935": "'Shea woods car', abandoned by its own tags (owner, 2026-10-13)",
    "node/4949334102": "'Naval Rod is Station 1940-1947', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "node/12319507802": "'Baxter Conservation Area back entrance', a description standing in for a name (owner, 2026-10-13)",
    "way/746264619": "'Flower gardens', a description standing in for a name (owner, 2026-10-13)",
    "way/68709999": "'NCC', an operator's initials standing in for a name",
    "way/1102388336": "'Future Elsie McGill Park', not yet open by its own tags or name (owner, 2026-10-13)",
    "way/1102388337": "'Future Mieshimin Park', not yet open by its own tags or name (owner, 2026-10-13)",
    "way/447222172": "'Chaplain Services', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/491014702": "'Photo Equatorial Building', a single building's own way, named for the building",
    "way/491014701": "'South Azimuth Building', a single building's own way, named for the building",
    "node/4485797712": "'Babs Asper Theatre', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "node/4485797711": "'Fourth Stage', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "node/2291903243": "'Southam Hall', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "node/5991684085": "'Reconciliation', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/238904302": "'Billings Estate Museum: Main House', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/526261452": "'50 (Winter Trail)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/496702956": "'53 (Winter Trail)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/930751009": "'Need to be Name path', a placeholder standing in for a name",
    "way/743011242": "'The Dog Went This way', a description standing in for a name (owner, 2026-10-13)",
    "way/475591082": "'Main Road', a description standing in for a name (owner, 2026-10-13)",
    "way/475591089": "'Main Road', a description standing in for a name (owner, 2026-10-13)",
    "way/545959909": "'Primary Path', a description standing in for a name (owner, 2026-10-13)",
    "way/743011245": "'Primary Path', a description standing in for a name (owner, 2026-10-13)",
    "way/743011232": "'Redundant Way', a mapper's note standing in for a name",
    "way/163534607": "'Stone Dust Path', a description standing in for a name (owner, 2026-10-13)",
    "way/720680367": "'Beaver Bridge ◆', a glitched name (a stray symbol), not repaired (owner, 2026-10-13)",
    "way/474206003": "'Confederation Bridge 🟦', a glitched name (a stray symbol), not repaired (owner, 2026-10-13)",
    "way/680344191": "'Piste cyclable', a bare type word for a name (owner, 2026-10-13)",
    "way/1126824853": "'McArthur Aveune Cycle Path', a description standing in for a name (owner, 2026-10-13)",
    "way/1126824854": "'McArthur Aveune Cycle Path', a description standing in for a name (owner, 2026-10-13)",
    "way/1536388116": "'McArthur Aveune Cycle Path', a description standing in for a name (owner, 2026-10-13)",
    "way/1278571389": "'Trail 24 - 3.5km', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/789366448": "'Stairs to UCU Terrace', a description standing in for a name (owner, 2026-10-13)",
    "way/714849837": "'World Exchange Plaza Level 1', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/714849838": "'World Exchange Plaza Level 1', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/714849839": "'World Exchange Plaza Level 1', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/714851527": "'World Exchange Plaza Level 1', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/714851529": "'World Exchange Plaza Level 2', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/714851530": "'World Exchange Plaza Level 2', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/545918946": "'Dead End Street', a description standing in for a name (owner, 2026-10-13)",
    "way/430405250": "'Miners Trail shortcut', a description standing in for a name (owner, 2026-10-13)",
}
