"""Sydney-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/sydney.md) and the 2022 survey itself.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "sydney" / "raw"
DATA_PROCESSED = ROOT / "data" / "sydney" / "processed"
OUTPUTS = ROOT / "outputs" / "sydney"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
# Brief: docs/build_briefs/sydney.md.
#
# The register: the City of Sydney's Floor Space and Employment Survey (FES),
# "Industry of occupation" - one point per business establishment with an
# ANZSIC 2006 class, no names or addresses (stripped by the publisher). CC BY
# 4.0, credit "City of Sydney" (licence-read 2026-09-28). The layer holds the
# 2007, 2012, 2017 and 2022 surveys; only the latest is read.
FES_LAYER_URL = ("https://services1.arcgis.com/cNVyNtjGVZybOQWZ/arcgis/rest/services/"
                 "FES_Industry_of_occupation/FeatureServer/0")
FES_ITEM_URL = "https://www.arcgis.com/sharing/rest/content/items/77ac8aa96bd34bacb881cfe8e5358ba0"
FES_YEAR = "2022"
FES_EXPECTED_ROWS = 21618      # the FES2022 block total (the brief)
FES_PAGE = 2000
FES_JSON = DATA_RAW / "fes_2022.json"

# Rail: Sydney Trains and Sydney Metro, from OpenStreetMap's route relations
# (Transport for NSW's GTFS needs an API key and is not needed). One bounded
# query over the City of Sydney's bbox; lines are clipped to the LGA.
OSM_BBOX = "-33.925,151.170,-33.855,151.235"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:180];("
    f'rel["type"="route"]["route"="train"]["network"="Sydney Trains"]({OSM_BBOX});'
    f'rel["type"="route"]["route"="subway"]["network"="Sydney Metro"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only"););out body;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# The City of Sydney LGA, OSM relation 1251066 (admin_level 6), polygonised
# from its outer ways; gated on its area (about 26 km2) so a truncated
# Overpass answer cannot pass.
BOUNDARY_OSM_RELATION = 1251066
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_city_of_sydney.json"
BOUNDARY_AREA_KM2 = (24, 29)
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 56S: the longitude (~151.21) falls in the 150 to 156 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32756"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Every Sydney Trains and Sydney Metro station inside the City of Sydney, lines
# drawn to the LGA boundary (the brief's recommendation). Light rail (L1, L2,
# L3; 22 stops in the LGA) is LEFT OUT (owner, 2026-09-28) and the page says so,
# with what it would add (83.2% -> 93.0% of storefronts in a ring, the brief's
# measure) - Berlin's precedent for its trams. NSW TrainLink and interstate
# services are not drawn.
#
# Line key -> the OSM ref whose relations make it (every direction and branch
# merged, as Sydney Trains presents one line).
LINE_OSM_REFS = {k: (k,) for k in ("T1", "T2", "T3", "T4", "T8", "T9", "M1")}
# On-map label: the ref riders use; legend: the full public name.
LINE_NAMES = {k: k for k in LINE_OSM_REFS}
LEGEND_NAMES = {
    "T1": "T1 North Shore & Western Line",
    "T2": "T2 Leppington & Inner West Line",
    "T3": "T3 Liverpool & Inner West Line",
    "T4": "T4 Eastern Suburbs & Illawarra Line",
    "T8": "T8 Airport & South Line",
    "T9": "T9 Northern Line",
    "M1": "M1 Metro North West & Bankstown Line",
}
# Transport for NSW's colours as OSM's relations carry them (read 2026-09-28).
LINES = {"T1": {"hue": "#F99D1C"}, "T2": {"hue": "#0098CD"}, "T3": {"hue": "#F37021"},
         "T4": {"hue": "#005AA3"}, "T8": {"hue": "#00954C"}, "T9": {"hue": "#D11F2F"},
         "M1": {"hue": "#168388"}}
LINE_ORDER = list(LINES)
# `python scripts/line_colour_search.py sydney`, run 2026-09-28: each hue's
# nearest feasible colour - every line 45.0 or more from every pin; closest
# pair within 500 m 19.2 (M1, T4); 7 distinct dark-mode labels. T4's blue and
# M1's teal read slate here: the Retail pins own the blues.
LINE_COLOURS = {"T1": "#D08000", "T2": "#08A0C0", "T3": "#E86818", "T4": "#506878",
                "T8": "#38A800", "T9": "#E84028", "M1": "#7098A0"}

BRANCH_NEAR_M = 300
BRANCH_MIN_NEW_M = 1000
STATION_CLUSTER_M = 400
STATION_NAME_ALIASES = {}

# GATE 3 - the stations inside the LGA against the brief's list: the 16 that
# OSM's railway=station nodes put inside relation 1251066 (a second OSM method,
# station nodes rather than route membership; Transport for NSW publishes no
# per-LGA list).
EXPECTED_STATIONS = {
    "Central", "Town Hall", "Wynyard", "Circular Quay", "St James", "Museum",
    "Martin Place", "Kings Cross", "Redfern", "Green Square", "Erskineville",
    "Macdonaldtown", "Newtown", "Barangaroo", "Gadigal", "Waterloo",
}

# --- Business filtering ------------------------------------------------

# In-city rows: the survey covers the City of Sydney only; the OSM polygon
# then drops points outside it.
CITY_KEEP = "City of Sydney"

TAXONOMY_SYSTEM = "anzsic_fes"
# Classified on ClassificationCode (EXTRA_COLUMNS); the label is the value
# column, as the survey publishes it.
RAW_CLASSIFICATION_COLUMN = "ClassificationName"

# Sanity bounds: the LGA polygon's extent (lat -33.9244 to -33.8536, lon 151.1749 to
# 151.2330, measured 2026-09-28) plus ~0.02 deg. The polygon does the filtering.
SYDNEY_BBOX = {
    "lat_min": -33.94,
    "lat_max": -33.83,
    "lon_min": 151.15,
    "lon_max": 151.25,
}
