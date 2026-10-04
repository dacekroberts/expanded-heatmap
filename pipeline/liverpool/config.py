"""Liverpool (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/liverpool.md) on Manchester (Regional)'s contract: the
shared steps are pipeline/countries/uk.py and uk_fetch.py. The first UK map on
heavy rail: Merseyrail's Northern and Wirral Lines, drawn as a commuter-rail
exception (owner, 2026-10-03), selected by network in the one Overpass query
(OSM_ROUTE_FILTERS) and checked against NaPTAN's rail records
(NAPTAN_STOP_TYPE "RLY").
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

SLUG = "liverpool"
CITY_NAME = "Liverpool (Regional)"
ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / SLUG / "raw"
DATA_PROCESSED = ROOT / "data" / SLUG / "processed"
OUTPUTS = ROOT / "outputs" / SLUG

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the scope, with where each is (a citable scoping record).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs, all keyless, downloaded by fetch_sources.py ---------------
#
# Scope: Liverpool, Sefton, Knowsley and Wirral, the four councils holding
# Merseyrail stations (owner, 2026-10-03); St Helens (421) and Halton (889)
# hold none. The FSA files all four under its North West region, so the scope
# is the code list, exactly 4 asserted.
FSA_AUTHORITIES = {"414": "Liverpool", "424": "Sefton", "412": "Knowsley", "435": "Wirral"}
FSA_AUTHORITY_COUNT = 4
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, London's file and edition (copied,
# not downloaded again), kept to the scope's GSS codes.
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E08000012", "E08000014", "E08000011", "E08000015")
# London's centroid tier (owner, 2026-09-28; the UK six's kit, 2026-10-01).
PLACE_AT_CENTROIDS = True

# The scope's four metropolitan districts (never the Merseyside county
# relation), each polygonised from its outer ways and unioned; gated on the
# union's area so a truncated answer cannot pass. The first query selected
# them by GSS code (BOUNDARY_GSS, uk_fetch.boundary_selector), each code
# matching one relation (2026-10-04); the ids it read are below, so a re-fetch
# asks by id and the GSS codes stay as the record of what was asked for.
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_GSS = {"E08000012": "Liverpool", "E08000014": "Sefton",
                "E08000011": "Knowsley", "E08000015": "Wirral"}
BOUNDARY_OSM_RELATIONS = {172987: "Liverpool", 173023: "Sefton", 173025: "Knowsley",
                          162456: "Wirral"}
# The four, about 676 km2 with OSM's foreshore (Liverpool 133.5, Sefton 202.9,
# Knowsley 86.5, Wirral 253.2; 2026-10-04).
BOUNDARY_AREA_KM2 = (650, 700)

# Rail: Merseyrail, OpenStreetMap. One query (uk_fetch.osm_query): the box's
# route=train relations of Merseyrail's network or operator only, never every
# train route in the box (the osm-rail skill), and the boundaries with
# geometry, the routes' member ways' tags and member nodes. The lead runs it.
OSM_BBOX = (53.30, -3.25, 53.70, -2.75)
OSM_ROUTES = ("train",)
OSM_ROUTE_FILTERS = ('["network"~"Merseyrail"]', '["operator"~"Merseyrail"]')
OSM_JSON = DATA_RAW / "osm.json"
SCOPE_LABEL = "the four Merseyrail councils (Liverpool, Sefton, Knowsley and Wirral)"

# NaPTAN (DfT, OGL v3): gate 3's second independent source (owner,
# 2026-10-01). Merseyrail's stations are rail access nodes, StopType RLY in
# ATCO area 910 (the national rail area), every one prefixed 9100; step 1
# reads the active RLY records inside the scope.
NAPTAN_STOP_TYPE = "RLY"
NAPTAN_PREFIXES = ("9100",)
NAPTAN_ATCO_AREAS = ("910",)
NAPTAN_RAW_DIR = DATA_RAW / "naptan"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-2.99) falls in the -6 to 0 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson. British
# National Grid is only Code-Point's own CRS (CODEPOINT_CRS above).
CRS_PROJECTED = "EPSG:32630"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the scope's extent plus a margin. The polygon does the
# filtering; this catches a CRS or axis error. Set from the boundary's bounds
# (lon -3.264 to -2.743, lat 53.286 to 53.704, 2026-10-04).
BUSINESS_BBOX = {"lat_min": 53.25, "lat_max": 53.75, "lon_min": -3.30, "lon_max": -2.70}

# --- Step 1: the lines and stations ---------------------------------------
#
# OSM's Merseyrail relations (read 2026-10-04, the one query): ref "Northern"
# six (Southport - Hunts Cross, Liverpool Central - Ormskirk and Liverpool
# Central - Headbolt Lane, each direction), ref "Wirral" four (West Kirby, New
# Brighton, Chester and Ellesmere Port, each a round trip through the
# city-centre loop), and ref "City" three, tagged network Merseyrail but run
# by Northern Trains (the City Line), which this map does not draw.
OPERATOR = "Merseyrail"
OSM_REFS = ("Northern", "Wirral")
NOT_DRAWN = {
    289382: "the City Line to Warrington (Northern Trains): fails the 15-minute test, "
            "3 trains an hour with gaps of 31-33 minutes (the brief)",
    289383: "the City Line to Wigan (Northern Trains): fails the 15-minute test, "
            "3 trains an hour with gaps of 31-33 minutes (the brief)",
    289384: "the City Line to Crewe (tagged London Midland, a service West Midlands "
            "Trains now runs): intercity and regional services are not drawn, and "
            "the City Line fails the 15-minute test",
}
LINE_OSM_REFS = {"Northern": ("Northern",), "Wirral": ("Wirral",)}
LINE_ORDER = list(LINE_OSM_REFS)
LINE_NAMES = {"Northern": "Northern Line", "Wirral": "Wirral Line"}
# The legend row reads "<label> <legend name>" (map_common.build_legend), so
# the legend name is the line's ends.
LEGEND_NAMES = {"Northern": "(Southport, Ormskirk, Headbolt Lane - Hunts Cross)",
                "Wirral": "(West Kirby, New Brighton, Chester, Ellesmere Port - Liverpool)"}
# OSM's colours, Merseyrail's own (Northern blue, Wirral green; read
# 2026-10-04 on relations 287295 and 287847). LINE_COLOURS below is what is
# drawn, after scripts/line_colour_search.py.
LINES = {"Northern": {"hue": "#036ebc"}, "Wirral": {"hue": "#00a654"}}
# `python scripts/line_colour_search.py liverpool`, run 2026-10-04: each hue's
# nearest feasible colour, 45.1 (Northern) and 45.6 (Wirral) from the pins,
# 3:1 on both pages; the pair 94.8 apart; the two dark-mode labels distinct.
LINE_COLOURS = {"Northern": "#08A0C0", "Wirral": "#28A800"}
# NaPTAN files three of these stations under other names: Hamilton Square by
# its town, and Liverpool Central's loop platforms and Lime Street's low-level
# station each as a record of their own beside the station's.
NAPTAN_NAME_ALIASES = {
    "Birkenhead Hamilton Square": "Hamilton Square",
    "Liverpool Central Loop Line": "Liverpool Central",
    "Liverpool Lime Street Low Level": "Liverpool Lime Street",
}

# GATE 3 - per line from Merseytravel's timetable booklets, the line diagram
# on each cover (the brief's named sources, read 2026-10-04): the Northern Line
# (valid from 17 May 2026) 37 stations, Southport, Ormskirk and Headbolt Lane
# to Hunts Cross; the Wirral Line (from 20 September 2026) 34 Merseyrail
# stations, the Bidston - Wrexham line's Upton and Heswall (Transport for
# Wales) not counted. Moorfields and Liverpool Central are on both: 69 in all,
# 59 of them inside the four councils.
OPERATOR_STATION_COUNTS = {"Northern": 37, "Wirral": 34}
OPERATOR_COUNTS_SOURCE = ("Merseytravel, the Northern Line (valid from 17 May 2026) and "
                          "Wirral Line (from 20 September 2026) timetable booklets' line "
                          "diagrams: Northern 37, Wirral 34 (read 2026-10-04)")
# Heavy rail's floor for the station gates: a collapsed set under it is still
# platforms. The closest pair in scope is James Street - Moorfields.
SPACING_MIN_M = 350.0
# Standard rings: the median gap in scope is 1,182 m (2026-10-04), well over
# the spacing rule's 550 m (docs/ring_rules.md). Step 1 stops outside this band.
MEDIAN_GAP_BOUNDS_M = (1000.0, 1400.0)

# NaPTAN's rail records in the scope that are not Merseyrail stations, each on
# a line this map does not draw.
_CITY_LINE = ("on Northern Trains' City Line services from Lime Street, not drawn: "
              "the City Line fails the 15-minute test (the brief)")
NAPTAN_EXPLAINED = {
    "Broad Green Rail Station": _CITY_LINE,
    "Edge Hill Rail Station": _CITY_LINE,
    "Halewood Rail Station": _CITY_LINE,
    "Huyton Rail Station": _CITY_LINE,
    "Mossley Hill Rail Station": _CITY_LINE,
    "Prescot Rail Station": _CITY_LINE,
    "Roby Rail Station": _CITY_LINE,
    "Wavertree Technology Park Rail Station": _CITY_LINE,
    "West Allerton Rail Station": _CITY_LINE,
    "Whiston Rail Station": _CITY_LINE,
    "Heswall Rail Station": "on Transport for Wales's Bidston - Wrexham line, not drawn: "
                            "regional services are not drawn (the brief)",
    "Upton Rail Station": "on Transport for Wales's Bidston - Wrexham line, not drawn: "
                          "regional services are not drawn (the brief)",
    "Meols Cop Rail Station": "on Northern Trains' Southport - Wigan line, not drawn: "
                              "regional services are not drawn (the brief)",
}

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]
