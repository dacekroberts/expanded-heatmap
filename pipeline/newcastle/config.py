"""Newcastle (Regional)-specific settings, scoped to one city per this
project's per-city folder architecture (see docs/project_context.md,
"Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/newcastle.md) and London's build, whose method this city
reuses on the five Tyne and Wear districts.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "newcastle" / "raw"
DATA_PROCESSED = ROOT / "data" / "newcastle" / "processed"
OUTPUTS = ROOT / "outputs" / "newcastle"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the five districts, with where each is (a citable scoping
# record). Every Metro station is inside them, so this is expected empty.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
#
# The register: the FSA's Food Hygiene Rating Scheme, one bulk XML per local
# authority. The five Tyne and Wear districts sit in the FSA's wider "North
# East" region (with Durham, Northumberland and the Tees Valley), so they are
# named by CODE, never by region (the brief), and each file must carry its own
# code. The authority API is not needed: it returned HTTP 500 through the
# London build.
FSA_AUTHORITIES = {
    "410": "Gateshead",
    "416": "Newcastle upon Tyne",
    "417": "North Tyneside",
    "427": "South Tyneside",
    "429": "Sunderland",
}
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, the same GB-wide file and edition as
# London's (a copy of data/london/raw/codepo_gb.zip, not a second download).
# Kept to the five districts' GSS codes (the brief).
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E08000021", "E08000022", "E08000023", "E08000024", "E08000037")
# London's centroid tier (owner, 2026-09-28): 634 storefronts (10.3%) the FSA
# gives a full postcode and no point; without it 17% would be unplaced.
PLACE_AT_CENTROIDS = True

# Rail: the Tyne and Wear Metro, operated by Nexus. OpenStreetMap's four
# light_rail relations - two refs, Green and Yellow, each a directional pair.
# One bounded query; the two Northern relations in the bbox (national rail to
# the Metrocentre) are not network=Tyne and Wear Metro and stay out.
OSM_BBOX = "54.78,-1.75,55.10,-1.30"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];("
    f'rel["type"="route"]["route"="light_rail"]["network"="Tyne and Wear Metro"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only"););out body;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# One station under two spellings in OSM (the brief): "St. James" is St James.
STATION_NAME_ALIASES = {"St. James": "St James"}
# Same-named stop nodes further apart than this are separate stations.
STATION_CLUSTER_M = 400

# Line key -> the OSM ref whose relations make it (both directions merged).
LINE_OSM_REFS = {"Green": ("Green",), "Yellow": ("Yellow",)}
# On-map label and legend name.
LINE_NAMES = {"Green": "Green line", "Yellow": "Yellow line"}
LEGEND_NAMES = {"Green": "Green line (Tyne and Wear Metro)",
                "Yellow": "Yellow line (Tyne and Wear Metro)"}
# Nexus's colours as OSM's relations carry them (the brief).
LINES = {"Green": {"hue": "#009933"}, "Yellow": {"hue": "#D39F06"}}
LINE_ORDER = list(LINES)
# `python scripts/line_colour_search.py newcastle`, run 2026-09-28: Nexus's
# hues' nearest feasible colours - Green 45.5 and Yellow 78.5 from every pin,
# 70.4 apart; both 3:1 or better on either page.
LINE_COLOURS = {"Green": "#30A800", "Yellow": "#C08800"}

# GATE 3 - the whole network against the operator's count: Nexus's 60
# stations (the brief).
OPERATOR_STATION_COUNTS = {"Metro (network)": 60}
OPERATOR_COUNTS_SOURCE = "Nexus: 60 stations (the brief, 2026-09-28)"

BRANCH_NEAR_M = 300
BRANCH_MIN_NEW_M = 1000

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# The five metropolitan districts - exactly the five FSA authorities. No Tyne
# and Wear administrative relation exists (a ceremonial county), so the union
# of the five admin_level 8 relations, each polygonised from its outer ways;
# gated on the union's area so a truncated Overpass answer cannot pass.
BOUNDARY_OSM_RELATIONS = {
    142282: "Newcastle upon Tyne", 116279: "Sunderland", 140462: "Gateshead",
    142245: "North Tyneside", 140390: "South Tyneside",
}
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_tyne_and_wear.json"
BOUNDARY_AREA_KM2 = (520, 560)   # Tyne and Wear, about 540 km2
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-1.61) falls in the -6 to 0 band. Derived per
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

# Every Metro station is kept, the Sunderland branch included (owner,
# 2026-09-28). Pelaw to Sunderland runs on Network Rail track shared with
# Northern's trains, but the route runs as the Metro, with Metro stations and
# frequencies. Measured: the branch's 12 stations add 597 storefronts to the
# rings (44.7% -> 54.4%), and without it Sunderland's 1,390 have none.
# Northern's own trains are national rail and are not drawn.

# --- Business filtering ------------------------------------------------

CITY_KEEP = "Tyne and Wear"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the five districts' extent (54.7990-55.0794 N, -1.8527 to
# -1.3457 E, measured 2026-09-28) plus ~0.02 deg. The polygon does the
# filtering; this catches a CRS or axis error.
NEWCASTLE_BBOX = {
    "lat_min": 54.78,
    "lat_max": 55.10,
    "lon_min": -1.88,
    "lon_max": -1.32,
}
