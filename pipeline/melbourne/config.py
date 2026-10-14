"""Melbourne-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/melbourne.md) and the 2024 census itself.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "melbourne" / "raw"
DATA_PROCESSED = ROOT / "data" / "melbourne" / "processed"
OUTPUTS = ROOT / "outputs" / "melbourne"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
# Brief: docs/build_briefs/melbourne.md.
#
# The register: the City of Melbourne's Census of Land Use and Employment
# (CLUE), "Business establishments with address and industry classification",
# one row per establishment with a trading name, an ANZSIC4 class and the
# property's point. CC BY 4.0 (licence-read 2026-09-28). The table holds every
# census 2002-2024; only 2024 is exported (owner, 2026-09-28: about 4 MB, not
# the whole table's 85 MB).
CLUE_DATASET_URL = ("https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/"
                    "business-establishments-with-address-and-industry-classification")
CLUE_YEAR = "2024"
CLUE_EXPECTED_ROWS = 19672     # the 2024 census, all industries (the brief)
CLUE_EXPORT_URL = (CLUE_DATASET_URL + "/exports/csv?delimiter=%2C&where="
                   "census_year%3Ddate%27" + CLUE_YEAR + "%27")
CLUE_CSV = DATA_RAW / "clue_2024.csv"

# Rail: Metro Trains Melbourne, from OpenStreetMap's route relations (PTV's
# GTFS is the fallback). One bounded query over the City of Melbourne's bbox;
# lines are clipped to the LGA.
OSM_BBOX = "-37.851,144.897,-37.775,144.991"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:180];("
    f'rel["type"="route"]["route"="train"]["network"="PTV - Metropolitan Trains"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only"););out body;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# The City of Melbourne LGA, OSM relation 2404870 (admin_level 6), polygonised
# from its outer ways; gated on its area (about 37.7 km2).
BOUNDARY_OSM_RELATION = 2404870
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_city_of_melbourne.json"
BOUNDARY_AREA_KM2 = (34, 41)
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 55S: the longitude (~144.96) falls in the 144 to 150 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32755"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Every Metro Trains station inside the City of Melbourne, lines drawn to the
# LGA boundary (owner, 2026-09-28). Trams (22 routes, 155 stops in the LGA) are
# LEFT OUT and the page says what they would add (96.5% -> 99.1% of
# storefronts in a ring, the brief's measure). V/Line and interstate trains
# are not drawn.
#
# DRAWN BY LINE GROUP (owner, 2026-09-28): inside the municipality the lines
# of a group run on one track (the Burnley group's four to Richmond), so
# 16 labels would stack. Metro Trains colours its lines by group, and OSM's
# relations carry those colours; each group is one labelled line, its legend
# entry naming the lines. Sandringham shares the Cross City group's colour.
# A relation is assigned by the line name before the colon in its `name`.
LINE_GROUPS = {
    "Burnley": ("Alamein Line", "Belgrave Line", "Glen Waverley Line", "Lilydale Line"),
    "Clifton Hill": ("Hurstbridge Line", "Mernda Line"),
    "Northern": ("Craigieburn Line", "Upfield Line"),
    "Cross City": ("Cross City", "Werribee Line", "Williamstown Line", "Sandringham Line"),
    "Frankston": ("Frankston Line",),
    "Metro Tunnel": ("Metro Tunnel",),
}
# Left out (owner, 2026-09-28): the Flemington Racecourse line runs on event
# days only (its Showgrounds and Flemington Racecourse stations with it), and
# the City Circle is "not a usual service" (OSM's own description) over the
# City Loop, which the regular lines already draw.
EXCLUDED_REFS = ("RCE", "CCL")


def line_key(tags):
    """The group a route relation belongs to, None for a left-out service; a
    relation matching no group stops step 1 (a scope question)."""
    if tags.get("ref") in EXCLUDED_REFS:
        return None
    line = tags.get("name", "").split(":")[0].strip()
    for key, lines in LINE_GROUPS.items():
        if line in lines:
            return key
    raise KeyError(f"route relation {tags.get('name')!r} matches no line group")


# Step 1 sets each kept relation's ref to its group, so a group is its own ref.
LINE_OSM_REFS = {k: (k,) for k in LINE_GROUPS}
LINE_NAMES = {k: k for k in LINE_GROUPS}
LEGEND_NAMES = {
    "Burnley": "Burnley group: Alamein, Belgrave, Glen Waverley and Lilydale lines",
    "Clifton Hill": "Clifton Hill group: Hurstbridge and Mernda lines",
    "Northern": "Northern group: Craigieburn and Upfield lines",
    "Cross City": "Cross City group: Werribee, Williamstown and Sandringham lines",
    "Frankston": "Frankston line",
    "Metro Tunnel": "Metro Tunnel: Sunbury, Cranbourne and Pakenham lines",
}
# Metro Trains' group colours as OSM's relations carry them (read 2026-09-28).
LINES = {"Burnley": {"hue": "#152C6B"}, "Clifton Hill": {"hue": "#BE1014"},
         "Northern": {"hue": "#FFBE00"}, "Cross City": {"hue": "#F178AF"},
         "Frankston": {"hue": "#028430"}, "Metro Tunnel": {"hue": "#279FD5"}}
LINE_ORDER = list(LINES)
# `python scripts/line_colour_search.py melbourne`, run 2026-09-28: each group
# hue's nearest feasible colour - every line 45.0 or more from every pin;
# closest pair within 500 m 36.6 (Burnley, Cross City); 6 distinct dark-mode
# labels. The Burnley group's navy reads mauve here: the Retail pins own it.
LINE_COLOURS = {"Burnley": "#805878", "Clifton Hill": "#C02008", "Northern": "#C88800",
                "Cross City": "#C870C8", "Frankston": "#60A000", "Metro Tunnel": "#08A0C0"}

BRANCH_NEAR_M = 300
BRANCH_MIN_NEW_M = 1000
STATION_CLUSTER_M = 400
STATION_NAME_ALIASES = {}

# GATE 3 - the stations inside the LGA against the brief's list: the 20 that
# OSM's railway=station nodes put inside relation 2404870 (a second OSM method),
# less the racecourse line's two event-day stations, and less RICHMOND: the
# boundary rule is the centre of the station's platforms (its stop nodes), and
# Richmond's lies just outside the LGA on Punt Road, though its station node is
# inside. The brief measured the difference at 0.0 points of coverage; it is
# listed in outputs/melbourne/excluded_stations.csv.
EXPECTED_STATIONS = {
    "Flinders Street", "Southern Cross", "Flagstaff", "Melbourne Central",
    "Parliament", "Jolimont", "North Melbourne", "Macaulay", "Flemington Bridge",
    "Royal Park", "Kensington", "South Kensington", "Arden",
    "Parkville", "State Library", "Town Hall", "Anzac",
}

# --- Business filtering ------------------------------------------------

# In-city rows: the census covers the City of Melbourne only; the OSM polygon
# then drops points outside it.
CITY_KEEP = "City of Melbourne"

TAXONOMY_SYSTEM = "anzsic_fes"
# Step 2 renames CLUE's industry_anzsic4_code / _description to the
# taxonomy's ClassificationCode / ClassificationName (Sydney's names).
RAW_CLASSIFICATION_COLUMN = "industry_anzsic4_description"

# Sanity bounds: the LGA polygon's extent (lat -37.8507 to -37.7755, lon
# 144.8970 to 144.9913, measured 2026-09-28) plus ~0.02 deg. The polygon
# does the filtering.
MELBOURNE_BBOX = {
    "lat_min": -37.87,
    "lat_max": -37.76,
    "lon_min": 144.88,
    "lon_max": 145.01,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3602404870)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
# Melbourne's public lanes are service ways named "X Place", "Court", "Mews"
# and the like, and its arcades are named footways; the shared word list
# leaves these out (owner, 2026-10-13). Measured on the 2026-10-13 cache: 208
# names on minor ways, 9 of them private on every way. "drive" is left out:
# 8 names, mostly venue roads. Re-measure if the cache is refetched.
PLACE_WAY_WORDS = ("place", "arcade", "court", "mews", "terrace", "close", "parade", "crescent",
                   "esplanade")
PLACE_REVIEWED = {}
PLACE_DROPPED = {
    "way/448062027": "'Campbell Arcade entrance', a description standing in for a name: a station entrance label",
    "way/448062028": "'Campbell Arcade entrance', a description standing in for a name: a station entrance label",
    "way/1443830592": "'Entrance/Exit 2 - Royal Parade East', a description standing in for a name: a station entrance label",
    "way/1443830593": "'Entrance/Exit 2 - Royal Parade East', a description standing in for a name: a station entrance label",
    "way/1453794762": "'Entrance/Exit 2 - Royal Parade East', a description standing in for a name: a station entrance label",
    "way/1457002174": "'Entrance/Exit 2 - Royal Parade East', a description standing in for a name: a station entrance label",
    "way/1427037793": "'Entrance/Exit 3 - Royal Parade West', a description standing in for a name: a station entrance label",
    "way/1443830586": "'Entrance/Exit 3 - Royal Parade West', a description standing in for a name: a station entrance label",
    "way/46503769": "'Kmart Centre Arcade', a store's own arcade: a business's feature",
    "way/736359880": "'Target Centre Arcade', a store's own arcade: a business's feature",
    "node/3954625843": "'Colonial Tramcar Restaurant Departure Point', a business's own feature under its own name",
    "node/245509493": "'Gate 4', an institution's own way, named for it",
    "node/10753062227": "'Gate 4', a description standing in for a name (owner, 2026-10-13)",
    "way/113543952": "'Carlton Housing Estate', a housing estate's own way, named for the estate",
    "way/218014207": "'Kings Business Park', a business's own feature under its own name",
    "way/556369063": "'Cenotaph', a bare type word for a name (owner, 2026-10-13)",
    "way/665730564": "'Linear Park', a bare type word for a name (owner, 2026-10-13)",
    "way/25759724": "'Flemington Grandstand', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1090140273": "'Mounting Yard', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/93507531": "'Nursery Enclosure', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/510098082": "'Main Arena', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/57007031": "'A Shed', not a street: another kind of object indexed as one",
    "way/57007027": "'D Shed', not a street: another kind of object indexed as one",
    "way/1388702395": "'Elizabeth Street entrance', a description standing in for a name (owner, 2026-10-13)",
    "way/46325052": "'Flinders Street entrance', a description standing in for a name (owner, 2026-10-13)",
    "way/712606596": "'Federation Square Eastern Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/10586965": "'Stadium Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/385053611": "'Stadium Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/716689898": "'Stadium Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/716689899": "'Stadium Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/24531277": "'Tennis Centre Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/198715389": "'Tennis Centre Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/220562504": "'Tennis Centre Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1211734385": "'Tennis Centre Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1352841564": "'Tennis Centre Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1352841565": "'Tennis Centre Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/580418119": "'Footscray Road Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/837329912": "'Footscray Road Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1504318456": "'Footscray Road Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1540932749": "'Rose Street to Kay Street Shimmy Path', a description standing in for a name (owner, 2026-10-13)",
    "way/92388006": "'alternative Stockmans Trail access', a description standing in for a name (owner, 2026-10-13)",
    "way/92388009": "'alternative Stockmans Trail access', a description standing in for a name (owner, 2026-10-13)",
    "way/1428195598": "'Entrance/Exit - Laurens Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1428195601": "'Entrance/Exit - Laurens Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1453493846": "'Entrance/Exit - Laurens Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1453493848": "'Entrance/Exit - Laurens Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1453493853": "'Entrance/Exit - Laurens Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1453494809": "'Entrance/Exit - Laurens Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1427026307": "'Entrance/Exit 1 - Collins Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1453811135": "'Entrance/Exit 1 - Collins Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1453811222": "'Entrance/Exit 1 - Collins Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1561889887": "'Entrance/Exit 1 - Collins Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1305336495": "'Entrance/Exit 1 - Grattan Street East', a description standing in for a name (owner, 2026-10-13)",
    "way/1426780032": "'Entrance/Exit 1 - Grattan Street East', a description standing in for a name (owner, 2026-10-13)",
    "way/1443830597": "'Entrance/Exit 1 - Grattan Street East', a description standing in for a name (owner, 2026-10-13)",
    "way/1453794765": "'Entrance/Exit 1 - Grattan Street East', a description standing in for a name (owner, 2026-10-13)",
    "way/1453780430": "'Entrance/Exit 1 - Swanston Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1425742264": "'Entrance/Exit 2 - Franklin Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1445905447": "'Entrance/Exit 2 - Swanson Street', a description standing in for a name (owner, 2026-10-13)",
    "way/1453794757": "'Entrance/Exit 4 -Grattan Street West', a description standing in for a name (owner, 2026-10-13)",
    "way/1453794759": "'Entrance/Exit 4 -Grattan Street West', a description standing in for a name (owner, 2026-10-13)",
    "way/1453794760": "'Entrance/Exit 4 -Grattan Street West', a description standing in for a name (owner, 2026-10-13)",
    "way/1123803835": "'Dryburgh Street', not a street: another kind of object indexed as one",
    "way/27462933": "'Dynon Rd Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/96009611": "'Dynon Rd Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/817791712": "'Dynon Rd Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/966091179": "'Dynon Rd Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1442729342": "'Dynon Rd Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1531135345": "'Dynon Rd Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/5150608": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/29404570": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/33109940": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/56722930": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/56722931": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1138559289": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1138559291": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1500954780": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1500954781": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1500954782": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1504294876": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/1504294877": "'Footscray Road Trail', a cycle facility named for the street it runs on: a description (owner, 2026-10-13)",
    "way/697043127": "'Old Geology Courtyard', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/697042317": "'Physics Courtyard', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/694844702": "'Zoology Lawn', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/22979222": "'North Lawn', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/1151115379": "'1888 Courtyard', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/23766733": "'1888 South Lawn', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "node/12136918864": "'South Court', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/233484534": "'University Lawn', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/22881658": "'South Lawn', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/177482300": "'MacFarland Court', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/178457735": "'University Cenotaph Garden', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/1262092867": "'Welcome Garden', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/1030920902": "'Picken Lawn', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/403420628": "'The Bulpadock', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13)",
    "way/33297408": "'Wildlife Reserve', description: leisure=park; name is type words only (flag check, 2026-10-13)",
    "node/4464271092": "'Rooftop Cinema', a rooftop cinema tagged a theatre; its Wikidata entry has no article: a business with nothing else (wave 1's unsure rows, settled on the Wikidata lookup and the existing rules, 2026-10-13)",
    # The helper screens of 2026-10-13 (duplicates, parts in a church's grounds): rows that
    # fall squarely in an owner ruling, each with its ruling.
    "node/13626510201": "'Arts Centre Melbourne (Theatres Building)', one object under two rows within 300 m; the other row stays (owner, 2026-10-13, the duplicates class of the pattern screen and the Three Soldiers ruling; helper screen): one building of the Arts Centre as its own row, 260 m from the row Arts Centre Melbourne (relation/6592679), under the same Wikidata entry (Q4801443) and the same article: the part beside the whole",
    "way/773893269": "'RMIT School of Architecture & Urban Design', one object under two rows within 300 m; the other row stays (owner, 2026-10-13, the duplicates class of the pattern screen and the Three Soldiers ruling; helper screen): one school's building under the campus's Wikidata entry (Q5123539) and article (RMIT Melbourne City campus), 232 m from the row RMIT University (way/26564452) and 233 m from RMIT University (City Campus) (way/772558888): a part under the whole's entry",
    "way/23717107": "'Chemical Engineering Lawn', a campus lawn or court named for a building or by function: a description (owner, 2026-10-13, the class ruled in Melbourne; helper screen): a campus lawn named by function, tagged a park (operator University of Melbourne): the same class as the fifteen rows this config already drops by the owner's word of 2026-10-13 (South Lawn, Zoology Lawn, Physics Courtyard and the rest); this one was missed",
    # The pattern screen of 2026-10-13, twin round of the helper screens: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "way/383402003": "'Chemical Engineering Lawn', a campus lawn or court named for a building or by function: a description; the second way of the name, beside way/23717107 (owner, 2026-10-13, the class ruled in Melbourne; twin round)",
}

# Public sights kept by id: in the cache, passed over by the rules (place_index,
# PLACE_KEPT; owner, 2026-10-13).
PLACE_KEPT = {
    "node/585344628": "'RMIT Capitol Theatre', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "relation/15629064": "'The University of Melbourne, Parkville Campus', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/1156270659": "'The University of Melbourne, Southbank Campus', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
}
