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
PLACE_REVIEWED = {}
PLACE_DROPPED = {
    "node/3954625843": "'Colonial Tramcar Restaurant Departure Point', a business's own feature under its own name",
    "node/245509493": "'Gate 4', an institution's own way, named for it",
    "node/10753062227": "'Gate 4', a description standing in for a name (owner, 2026-10-13)",
    "relation/2383266": "'Melbourne', the city boundary's center as a second place row beside the city's own: a duplicate (owner, 2026-10-13)",
    "way/113543952": "'Carlton Housing Estate', a housing estate's own way, named for the estate",
    "way/218014207": "'Kings Business Park', a business's own feature under its own name",
    "way/556369063": "'Cenotaph', a bare type word for a name (owner, 2026-10-13)",
    "way/665730564": "'Linear Park', a bare type word for a name (owner, 2026-10-13)",
    "way/25759724": "'Flemington Grandstand', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/1090140273": "'Mounting Yard', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/93507531": "'Nursery Enclosure', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/510098082": "'Main Arena', an interior section of a paid venue, which keeps its own row (owner, 2026-10-13)",
    "way/179383357": "'City-CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/716626670": "'CityLink In - Boundary Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040966862": "'CityLink In - Boundary Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040966852": "'CityLink In - Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/327700046": "'CityLink In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/980110335": "'CityLink In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/980110336": "'CityLink In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1254132458": "'CityLink In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/327695289": "'CityLink In - Lorimer Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/778984243": "'CityLink In - Lorimer Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1013257459": "'CityLink In - Lorimer Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982774814": "'CityLink In - West Gate Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/716626669": "'CityLink In-Boundary Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/958559446": "'CityLink In-Boundary Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/777804789": "'CityLink In-Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040791374": "'CityLink In-Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1094421250": "'CityLink In-Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5234962": "'CityLink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/8066129": "'CityLink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/28119399": "'CityLink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38312822": "'CityLink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/262288652": "'CityLink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/312190545": "'CityLink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/980110339": "'CityLink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1274073087": "'CityLink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/19792505": "'CityLink In-Power Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/54150982": "'CityLink In-West Gate Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1014558376": "'CityLink In-West Gate Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1014558377": "'CityLink In-West Gate Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1014558378": "'CityLink In-West Gate Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/777804788": "'Citylink In - Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040791372": "'Citylink In - Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040791373": "'Citylink In - Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/484854830": "'Citylink In - West Gate In Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040966853": "'Citylink In-Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040966863": "'Citylink In-Flemington Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5234957": "'Citylink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/484854827": "'Citylink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/484854828": "'Citylink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1078456283": "'Citylink In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5235231": "'Citylink In-Lorimer Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38312779": "'Citylink In-West Gate In Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38312931": "'Citylink In-West Gate In Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/484854831": "'Citylink In-West Gate In Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1254315758": "'Citylink In-West Gate In Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/22588354": "'Citylink In-West Gate Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/290472629": "'Citylink In-West Gate Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/10299535": "'Citylink Out-Racecourse Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1498779231": "'Citylink Out-Racecourse Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/173047913": "'Cook - West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/788539568": "'Cook-CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984782932": "'Cook-Citylink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/786275353": "'Cook-West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1083073386": "'Cook-West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5234953": "'Kings - CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775968522": "'Kings - CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1175874270": "'Kings - CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313481": "'Kings - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/980110341": "'Kings - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982774813": "'Kings - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5234964": "'Kings-CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/8066127": "'Kings-CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5235238": "'Kings-Citylink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313496": "'Kings-Citylink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5234971": "'Kings-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/706692867": "'Kings-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1383208582": "'Kings-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313359": "'Montague - CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1254450685": "'Montague - CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/780655769": "'Montague - Citylink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313364": "'Montague - West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313371": "'Montague - West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313374": "'Montague - West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/789303527": "'Montague - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/789312783": "'Montague - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1254450682": "'Montague - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313043": "'Montague-CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982206084": "'Montague-Citylink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313357": "'Montague-West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/327695288": "'Montague-West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/568351595": "'Montague-West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/568351599": "'Montague-West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775974034": "'Montague-West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/789217087": "'Montague-West Gate In Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313709": "'Montague-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/780655768": "'Montague-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982774812": "'Montague-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/39612418": "'Mount Alexander-CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040966867": "'Mount Alexander-CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040966869": "'Mount Alexander-CityLink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/172506455": "'Mount Alexander-Citylink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1040966868": "'Mount Alexander-Citylink Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/50123944": "'Power - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775976640": "'Power - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/22971433": "'Power-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/50123827": "'Power-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775984704": "'Prohasky - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/292578213": "'Prohasky-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/787544543": "'Prohasky-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/404164607": "'Todd - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775984705": "'Todd - West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/197847202": "'Todd-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1083073385": "'Todd-West Gate Out Ramp On', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984176217": "'West Gate In - Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984176218": "'West Gate In - Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984176219": "'West Gate In - Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984176220": "'West Gate In - Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984176221": "'West Gate In - Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984176222": "'West Gate In - Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1329205446": "'West Gate In - Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/26619046": "'West Gate In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/207516092": "'West Gate In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775968521": "'West Gate In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/980106010": "'West Gate In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/981208567": "'West Gate In - Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313358": "'West Gate In - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313701": "'West Gate In - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982206080": "'West Gate In - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982206081": "'West Gate In - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1254450683": "'West Gate In - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1254450684": "'West Gate In - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/22664417": "'West Gate In - Power Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/50123940": "'West Gate In - Power Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775974941": "'West Gate In - Power Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/4347066": "'West Gate In-CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/983896880": "'West Gate In-CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/585267687": "'West Gate In-Citylink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1054956684": "'West Gate In-Citylink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/22597292": "'West Gate In-Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775984703": "'West Gate In-Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984176211": "'West Gate In-Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/984176216": "'West Gate In-Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1351999117": "'West Gate In-Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1351999118": "'West Gate In-Cook Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5234777": "'West Gate In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38312866": "'West Gate In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313389": "'West Gate In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/980106009": "'West Gate In-Kings Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/568362744": "'West Gate In-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/783844082": "'West Gate In-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982206102": "'West Gate In-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1086833715": "'West Gate In-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1086833716": "'West Gate In-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5234946": "'West Gate In-Power Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/64727384": "'West Gate In-Power Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313636": "'West Gate Out - CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/199004265": "'West Gate Out - CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/235776780": "'West Gate Out - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/568354787": "'West Gate Out - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/568354789": "'West Gate Out - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/784415912": "'West Gate Out - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982206096": "'West Gate Out - Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/787544546": "'West Gate Out - Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/983201672": "'West Gate Out - Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313044": "'West Gate Out-CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/321793594": "'West Gate Out-CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/484854834": "'West Gate Out-CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/484854835": "'West Gate Out-CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/705558500": "'West Gate Out-CityLink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5607524": "'West Gate Out-Citylink Out Ramp', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5234995": "'West Gate Out-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/5235197": "'West Gate Out-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313416": "'West Gate Out-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982206094": "'West Gate Out-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982206095": "'West Gate Out-Montague Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/982777079": "'West Gate Out-Prohasky Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/22588456": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/38313045": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/775982784": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/787544547": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/983201670": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/983201671": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/983201674": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1519460541": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1519460542": "'West Gate Out-Todd Ramp Of', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
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
}
