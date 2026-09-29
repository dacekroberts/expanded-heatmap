"""Glasgow-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/glasgow.md) and London's build, whose method this city
reuses on Scotland's scheme.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "glasgow" / "raw"
DATA_PROCESSED = ROOT / "data" / "glasgow" / "processed"
OUTPUTS = ROOT / "outputs" / "glasgow"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities). The Subway lies wholly inside Glasgow City, so this is
# expected to be empty.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
#
# The register: the FSA's open-data file for Glasgow City Council, authority
# 776, which runs Scotland's Food Hygiene Information Scheme (FHIS, SchemeType
# 2), not England's FHRS. Named by code, not read from the FSA's authority
# list: that API returned HTTP 500 through the London build, and the file
# carries its own authority code, which fetch_sources.py checks.
FSA_AUTHORITY_CODE = "776"
FSA_AUTHORITY_NAME = "Glasgow City"
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS776en-GB.xml"
FSA_XML = DATA_RAW / "fsa" / "776.xml"

# Rail: the Glasgow Subway, one 15-station loop, operated by SPT. SPT publishes
# no GTFS for it, so track and stations are OpenStreetMap's two route
# relations - the Outer and Inner Circle, the two directions of ONE loop,
# sharing the ref "Subway". One bounded query.
OSM_BBOX = "55.80,-4.40,55.92,-4.15"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:90];("
    f'rel["type"="route"]["route"="subway"]["ref"="Subway"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
# The relations' STOP members (route-relation membership, osm-rail's rule).
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only"););out body;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
EXPECTED_RELATIONS = 2

# Each relation carries all 15 stations. Govan, which the brief found missing,
# is the loop's start and end: a `stop_entry_only` and a `stop_exit_only`
# member, not a `stop` (measured at the build, 2026-09-28). Step 1 counts every
# stop role and gates on 15, so no station is added by hand.
EXPECTED_STATIONS_PER_RELATION = 15
# OSM's spelling -> the station's signed name.
STATION_NAME_ALIASES = {"St Georges Cross": "St George's Cross"}
# Same-named stop nodes further apart than this are separate stations. The
# loop's two directions stop at island or side platforms metres apart.
STATION_CLUSTER_M = 300

# GATE 3 - the whole line against the operator's count: 15 stations. English
# Wikipedia's Glasgow Subway infobox (a SECONDARY source, Prague's precedent),
# read 2026-09-28.
OPERATOR_STATION_COUNTS = {"Subway": 15}
OPERATOR_COUNTS_SOURCE = "en.wikipedia: Glasgow Subway infobox (15 stations) - secondary, read 2026-09-28"

# One line, drawn once: the public name on the map, the full name in the
# legend. The hue is OSM's Outer Circle colour, SPT's orange; the Inner
# Circle's grey is the other direction, never a second line (the brief).
LINES = {"Subway": {"hue": "#FF6600"}}
LINE_ORDER = list(LINES)
LINE_NAMES = {"Subway": "Subway"}
LEGEND_NAMES = {"Subway": "Glasgow Subway"}
# `python scripts/line_colour_search.py glasgow`, run 2026-09-28: SPT's orange's
# nearest feasible colour, 65.3 from every pin, 5.94:1 on the dark page and
# 3.15:1 on the light.
LINE_COLOURS = {"Subway": "#F86000"}

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Glasgow City council area - exactly FSA authority 776. OSM relation 1906767
# (admin_level 6, GSS S12000049), polygonised from its outer ways and gated on
# its area so a truncated Overpass answer cannot pass.
BOUNDARY_OSM_RELATION = 1906767
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_glasgow_city.json"
BOUNDARY_AREA_KM2 = (165, 185)
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-4.25) falls in the -6 to 0 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Every station of the one loop is kept: 15 stations on ~10.5 km, no surface
# stretch to thin. Glasgow's national rail (the Argyle and North Clyde lines)
# is not the Subway and is left out; the page states the coverage that costs.

# --- Business filtering ------------------------------------------------

# In-city rows: the one authority file IS Glasgow City; the polygon then drops
# any point geocoded outside it.
CITY_KEEP = "Glasgow City"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: Glasgow City's polygon extent (55.7813-55.9296 N,
# -4.3932 to -4.0717 E, measured 2026-09-28) plus ~0.02 deg. The polygon does
# the filtering; this catches a CRS or axis error.
GLASGOW_BBOX = {
    "lat_min": 55.76,
    "lat_max": 55.95,
    "lon_min": -4.42,
    "lon_max": -4.05,
}
