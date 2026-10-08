"""London-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "london" / "raw"
DATA_PROCESSED = ROOT / "data" / "london" / "processed"
OUTPUTS = ROOT / "outputs" / "london"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
# Brief: docs/build_briefs/london.md.
#
# The register: the Food Standards Agency's Food Hygiene Rating Scheme, one
# bulk XML per local authority. The 33 London authorities are read from the
# FSA's own authority list (RegionName "London"), never assumed as a range.
# Licence: Open Government Licence v3 (licence-read pending, 2026-09-28).
FSA_AUTHORITIES_URL = "https://api.ratings.food.gov.uk/Authorities"
FSA_API_HEADERS = {"x-api-version": "2", "Accept": "application/json"}
FSA_REGION = "London"
FSA_AUTHORITY_COUNT = 33   # the 32 boroughs and the City of London
FSA_RAW_DIR = DATA_RAW / "fsa"
FSA_AUTHORITIES_JSON = DATA_RAW / "fsa_authorities.json"
# Postcode centroids (owner, 2026-09-28): OS Code-Point Open places a food
# storefront the FSA gives a FULL postcode and no point. Never a private
# address - the FSA publishes those with no postcode or an outward code only.
CODEPOINT_META_URL = "https://api.os.uk/downloads/v1/products/CodePointOpen"
CODEPOINT_URL = ("https://api.os.uk/downloads/v1/products/CodePointOpen/downloads"
                 "?area=GB&format=CSV&redirect")
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings

# Rail (owner, 2026-09-28): the Underground, the DLR, the Elizabeth line and
# the six Overground lines; Tramlink left out. TfL publishes no GTFS. Track
# geometry is OpenStreetMap's route relations, ONE bounded query for all 19
# lines. The Elizabeth line and most of the Overground are tagged
# network=National Rail, so they are selected by NAME, never by network
# (Dublin's DART lesson; osm-rail).
OSM_BBOX = "51.28,-0.51,51.70,0.34"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:180];("
    f'rel["type"="route"]["route"="subway"]["network"="London Underground"]({OSM_BBOX});'
    f'rel["type"="route"]["route"="light_rail"]["network"="Docklands Light Railway"]({OSM_BBOX});'
    f'rel["type"="route"]["route"="train"]["name"~"Elizabeth line|Liberty|Lioness|Mildmay|'
    f'Suffragette|Weaver|Windrush"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
# The same relations' STOP members (route-relation membership, osm-rail's rule;
# never a node tag filter), nodes only - cheap.
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only"););out body;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
# Branch selection in step 1: a relation joins its line only if it adds at
# least BRANCH_MIN_NEW_M of track more than BRANCH_NEAR_M from what is chosen.
BRANCH_NEAR_M = 300
# Same-named stop nodes further apart than this are separate stations
# (Hammersmith's two; Bethnal Green's Underground and Overground).
STATION_CLUSTER_M = 400
# One station under two names in OSM, found by step 1's close-pair list
# (2026-09-28): the National Rail name beside the Underground's, and the DLR's
# "for ExCeL". Each pair is within 180 m and TfL signs it as one station.
STATION_NAME_ALIASES = {
    "London Paddington": "Paddington",
    "London Euston": "Euston",
    "London Liverpool Street": "Liverpool Street",
    "Custom House for Excel": "Custom House",
    "Cutty Sark for Maritime Greenwich": "Cutty Sark",
}

# On-map label (the name riders use) and legend name (the full public name).
# 19 full names would not fit the label solver - Tokyo's lesson - so the map
# says "Bakerloo" and the legend "Bakerloo line" (render_heatmap's
# legend_names, which also caps the legend at the solver's 274 px).
LEGEND_NAMES = {
    **{k: f"{k} line" for k in ("Bakerloo", "Central", "Circle", "District",
                                "Hammersmith & City", "Jubilee", "Metropolitan", "Northern",
                                "Piccadilly", "Victoria", "Waterloo & City", "Elizabeth")},
    "DLR": "DLR (Docklands Light Railway)",
    **{k: f"{k} line (London Overground)" for k in ("Liberty", "Lioness", "Mildmay",
                                                    "Suffragette", "Weaver", "Windrush")},
}
# Each line's OPERATOR hue - TfL's colours as OSM's route relations carry them
# (read 2026-09-28). The drawn colour is scripts/line_colour_search.py's
# nearest feasible one (LINE_COLOURS below): the pins' blue, pink and green and
# the dark page rule some of TfL's out (the Northern's black, for one).
LINES = {
    "Bakerloo": {"hue": "#AE6017"}, "Central": {"hue": "#E42313"}, "Circle": {"hue": "#FFD329"},
    "District": {"hue": "#00A166"}, "Hammersmith & City": {"hue": "#F4A9BE"},
    "Jubilee": {"hue": "#949699"}, "Metropolitan": {"hue": "#91005A"},
    "Northern": {"hue": "#000000"}, "Piccadilly": {"hue": "#094FA3"},
    "Victoria": {"hue": "#0A9CDA"}, "Waterloo & City": {"hue": "#93CEBA"},
    "DLR": {"hue": "#00AFAD"}, "Elizabeth": {"hue": "#9364CC"},
    "Liberty": {"hue": "#61686B"}, "Lioness": {"hue": "#FFA600"}, "Mildmay": {"hue": "#006FE6"},
    "Suffragette": {"hue": "#18A95D"}, "Weaver": {"hue": "#9B0058"}, "Windrush": {"hue": "#DC241F"},
}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: k for k in LINES}
# `python scripts/line_colour_search.py london` (500 m, CIE76 18), run
# 2026-09-28 on step 1's lines.geojson: closest pair within 500 m 18.3
# (Northern, Waterloo & City), anywhere 10.5 (Jubilee, Liberty); every line
# >= 45.0 from the pins of that run; 19 distinct dark-mode labels. The Retail
# pins' blue takes the Piccadilly's, which reads mauve here; the Northern's
# black is grey so it shows on the dark page.
#
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search. The
# District's #586818 sat 15.8 from it, under the owner's floor of 20
# (2026-10-07), and moved to #00A064, the colour nearest TfL's #00A166 that
# reads 3:1 on both pages and clears 18 from every other line: olive 48.0,
# nearest line the Suffragette 40.9. Four lines sit between 20 and 45 from
# olive, an accepted trade (owner, 2026-10-07): the Circle (#B09000) 23.2, the
# Lioness 43.0, the Bakerloo 43.5 and the Suffragette 44.4. Every other line
# >= 45.0 from every pin.
LINE_COLOURS = {
    "Bakerloo": "#B06018", "Central": "#E02010", "Circle": "#B09000", "District": "#00A064",
    "Hammersmith & City": "#B88090", "Jubilee": "#909090", "Metropolitan": "#9840A0",
    "Northern": "#686060", "Piccadilly": "#805878", "Victoria": "#08A0C0",
    "Waterloo & City": "#487070", "DLR": "#5098A8", "Elizabeth": "#C068E0",
    "Liberty": "#707878", "Lioness": "#D08000", "Mildmay": "#0050F0",
    "Suffragette": "#30A800", "Weaver": "#E858D0", "Windrush": "#F86040",
}

# GATE 3 - the whole network (not cut at Greater London), against English
# Wikipedia, read 2026-09-28 (a SECONDARY source, Prague's precedent; tfl.gov.uk
# serves a Cloudflare challenge to automated reads): the London Underground
# article's table of lines; the DLR's infobox (45); the Elizabeth line's (41);
# the London Overground article's network total (113 on six lines; no per-line
# figure is published there). CIRCLE reads 35, not the table's 36: the table
# counts Paddington's two Circle stations (Praed Street and the H&C one), which
# this map draws as one station.
OPERATOR_STATION_COUNTS = {
    "Bakerloo": 25, "Central": 49, "Circle": 35, "District": 60,
    "Hammersmith & City": 29, "Jubilee": 27, "Metropolitan": 34, "Northern": 52,
    "Piccadilly": 53, "Victoria": 16, "Waterloo & City": 2, "DLR": 45,
    "Elizabeth": 41, "Overground (network)": 112,
}
# The OVERGROUND reads 112, not Wikipedia's 113: TfL's own stop lists for the
# six lines (api.tfl.gov.uk Route/Sequence, both directions, read 2026-09-28 as
# a check, nothing from it stored or published) hold 112 distinct stations, and
# the operator outranks the secondary source.
OVERGROUND_LINES = ("Liberty", "Lioness", "Mildmay", "Suffragette", "Weaver", "Windrush")
OPERATOR_COUNTS_SOURCE = ("en.wikipedia: London Underground's table of lines, the DLR (45) "
                          "and Elizabeth line (41) infoboxes, London Overground (113) - "
                          "secondary, read 2026-09-28")

# Stations OSM's route relations do not carry as stops, found by gate 3
# (2026-09-28): the Piccadilly's North Ealing and South Harrow, and the DLR's
# Woolwich Arsenal (a branch terminus). Placed at their OSM station node,
# fetched by name; step 1 STOPS once a relation carries one, so the addition
# is retired rather than doubled.
# The Overground's five (Hatch End, Watford High Street, Upper Holloway, Wood
# Street, St James Street) were found by diffing its six lines against TfL's
# own stop lists, a scratch check (108 -> 113).
STATION_ADDITIONS = {"North Ealing": "Piccadilly", "South Harrow": "Piccadilly",
                     "Woolwich Arsenal": "DLR",
                     "Hatch End": "Lioness", "Watford High Street": "Lioness",
                     "Upper Holloway": "Suffragette",
                     "Wood Street": "Weaver", "St James Street": "Weaver"}
# Relations that are not the line as TfL runs it, skipped for lines and
# stations alike: a Windrush relation starting at Battersea Park, which TfL's
# Windrush stop list does not include (2026-09-28).
RELATION_NAMES_SKIPPED = ("Windrush Line: Battersea Park",)
OSM_ADDITIONS_QUERY = (
    '[out:json][timeout:90];node["railway"="station"]["name"~"^('
    + "|".join(STATION_ADDITIONS) + f')$"]({OSM_BBOX});out body;')
OSM_ADDITIONS_JSON = DATA_RAW / "osm_station_additions.json"
BRANCH_MIN_NEW_M = 1000

# Line key -> the OSM refs whose relations make it (every direction and branch
# merged: the Northern's two branches, the District's and the DLR's five
# routes are ONE labelled line each, as TfL presents them). 173 relations on
# 2026-09-28, every one with a ref and a colour.
LINE_OSM_REFS = {
    "Bakerloo": ("Bakerloo",), "Central": ("Central",), "Circle": ("Circle",),
    "District": ("District",), "Hammersmith & City": ("Hammersmith & City",),
    "Jubilee": ("Jubilee",), "Metropolitan": ("Metropolitan",), "Northern": ("Northern",),
    "Piccadilly": ("Piccadilly",), "Victoria": ("Victoria",),
    "Waterloo & City": ("Waterloo & City",),
    "DLR": ("B-L", "B-WA", "S-L", "SI-WA", "TG-B"),
    "Elizabeth": ("Elizabeth",),
    "Liberty": ("Liberty",), "Lioness": ("Lioness",), "Mildmay": ("Mildmay",),
    "Suffragette": ("Suffragette",), "Weaver": ("Weaver",), "Windrush": ("Windrush",),
}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Greater London - the 32 boroughs and the City, exactly the FSA's 33 "London"
# authorities. OSM relation 175342 (admin_level 5), polygonised from its outer
# ways; 1,595.5 km2 in UTM 30N on 2026-09-28, gated so a truncated Overpass
# answer cannot pass.
BOUNDARY_OSM_RELATION = 175342
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_greater_london.json"
BOUNDARY_AREA_KM2 = (1560, 1620)
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-0.13) falls in the -6 to 0 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Which lines count and why: see "Rail" above (owner, 2026-09-28) and
# LINE_OSM_REFS / LINE_NAMES. Every station of the 19 lines is kept - the
# spacing gate's median is 737 m, no surface stretch needs thinning.

# --- Business filtering ------------------------------------------------

# In-city rows: the 33 authority files ARE Greater London (fetch_sources.py
# asserts 33 in the FSA's "London" region); the polygon then drops any point
# geocoded outside it. CITY_KEEP is kept for the scaffold's templates.
CITY_KEEP = "London"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: Greater London's polygon extent (51.2868-51.6919 N,
# -0.5104-0.3340 E, measured 2026-09-28) plus ~0.02 deg. The polygon does the
# filtering; this catches a CRS or axis error.
LONDON_BBOX = {
    "lat_min": 51.26,
    "lat_max": 51.72,
    "lon_min": -0.54,
    "lon_max": 0.36,
}
