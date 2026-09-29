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
