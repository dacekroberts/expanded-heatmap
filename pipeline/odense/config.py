"""Odense-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

THIRD DANISH CITY, on Copenhagen's national modules and Aarhus's placement:
CVR's six-file join, the columns never to load and the sole-trader guard live
in `pipeline/countries/denmark.py` and `denmark_register.py`, and the point
is OSM's DAR address point by `osak:identifier`, keyless, as Aarhus's (the
owner's call, 2026-09-27). The rail is the shared `pipeline/osm_tram.py` (the
tram-city skill). What is Odense's own is below: the kommune, the one line and
the station OSM's routes leave out, the halved rings, the colour, the
catch-all verdict.
"""

from pathlib import Path

SLUG = "odense"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "odense" / "raw"
DATA_PROCESSED = ROOT / "data" / "odense" / "processed"
OUTPUTS = ROOT / "outputs" / "odense"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Letbane stops left out, each with the reason - a citable scoping record (the
# Los Angeles rule). Every in-service station is in the kommune, so today it
# is header-only (Hospital Syd, not yet open, is a watch item, not a row).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. `fetch_sources.py` downloads them, keyless, from OpenStreetMap;
# no step may fetch. CVR is the national cache Copenhagen fetched
# (`denmark.SHARED_RAW`), read here and NEVER refreshed by this city.
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_KOMMUNER_JSON = DATA_RAW / "osm_kommuner.json"
# OSM's imported Danish address points: (osm id, lat, lon, osak:identifier),
# Overpass CSV. `osak:identifier` IS the DAR Husnummer id (DECISIONS
# 2026-09-27).
OSM_ADDRESS_POINTS_TSV = DATA_RAW / "osm_osak_points.tsv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Scope: ONE kommune ------------------------------------------------------
#
# Odense Kommune, 461 (OSM relation 2178124). The business filter is CVR's own
# `CVRAdresse_kommunekode` on the location address, never a polygon; the
# polygon decides only which stations are in the kommune (all of them).
KOMMUNER = {"461": "Odense"}                 # CVR's unpadded code
OSM_KOMMUNE_RELATION = 2178124
# Odense Kommune as OSM draws it; step 1 prints the area and stops outside
# these bounds (a polygon assembled wrong, or a different kommune).
KOMMUNE_AREA_KM2 = {"461": (295.0, 315.0)}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM 32N. Odense (~10.39 E) is in zone 32 (6-12 E) - derived per
# city, as Aarhus's; DAR's national CRS too.
CRS_PROJECTED = "EPSG:25832"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the 25 in-service stations' 441 m median gap (the brief,
# 2026-09-30; approved by the owner with the tram kit's calls). Step 1 prints
# the median again and stops outside 380-500 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (380.0, 500.0)

# --- Station scope: EVERY STOP IN SERVICE, 25 --------------------------------
#
# Odense Letbane is one street-running line, Tarup Center - Hjallese Station,
# operated by Keolis: two `route=tram` relations (one per direction) with
# ref L, 24 stop names between them (brief, 2026-09-30). No metro, no S-tog.
ROUTE = "tram"
OPERATOR = "Keolis"
LINE_REFS = ("L",)
# Every tram relation in the box is kept; a new one stops step 1 until it is
# kept or named here with a reason (osm_tram's contract).
NOT_DRAWN = {}

# SDU SYD/HOSPITAL NORD - ADDED BY NODE (owner, 2026-09-30, call approved).
# Opened 2023-08-25 with SDU's health-sciences building (Danish Wikipedia's
# station article; Odense Letbane's news item), so it is in service, but OSM's
# two route relations do not list it. It is a `railway=tram_stop` node, added
# here by id - both direction's stop nodes, 5 m apart (read 2026-09-30);
# osm_tram stops the step if OSM renames either or puts it on a route.
STATION_ADD = {
    7942163365: ("L", "SDU Syd/Hospital Nord"),
    7942163366: ("L", "SDU Syd/Hospital Nord"),
}
# (Idrætsparken's node 9034508024 is also on no relation, but it is a second
# stop position 10 m from Idrætsparken's own member node, not a station.)

# HOSPITAL SYD - OUT until the new hospital opens (due 2027). A tagged stop on
# no route: a WATCH ITEM, not an excluded station (a stop not yet in service
# is not part of the network, and What Is Excluded has no category for one).
# Step 1 stops when OSM puts it on a route or drops its tag.
NOT_YET_OPEN = {
    "Hospital Syd": "opens with the new Odense University Hospital, due 2027 "
                    "(not in service on 2026-09-30)",
}

# Gate 3: the operator's 26 stops are the 24 on OSM's routes, SDU Syd/Hospital
# Nord and Hospital Syd (brief) - so 25 in service.
OPERATOR_STATION_COUNTS = {"L": 25}
OPERATOR_COUNTS_SOURCE = ("Odense Letbane's 26 stops less Hospital Syd, not yet "
                          "open (the brief, 2026-09-30)")

SPACING_MIN_M = 350.0

DRAWN_LINES = ("L",)
# The name riders use. OSM's relation names the line "Letbanen"; riders and
# the operator say Odense Letbane.
LINE_NAMES = {"L": "Odense Letbane"}
# OSM carries no `colour` tag on either relation (brief), so the project's own
# palette, as Le Havre's and Riga's. Scored against the pins (CIE76, 2026-09-30):
# dark goldenrod 74.8 (worst: Personal services); Aarhus's #30556E was tried
# first and scored 42.7 against Retail, under the preferred 45.
LINE_COLOURS = {"L": "#b8860b"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "denmark_db25"
RAW_CLASSIFICATION_COLUMN = "db25_label"
CITY_KEEP = "ODENSE"   # kept for the scaffold's templates; KOMMUNER filters

# Where the Husnummer's point comes from - see pipeline/countries/denmark.py.
PLACEMENT = "osm_osak"

# The per-city catch-all verdict, on Odense's own numbers (the screen,
# 2026-09-27, CVR generation 505): 969900 "Andre personlige serviceydelser
# i.a.n." is 108 rows (3.6%), personally owned 84% - Copenhagen's and Aarhus's
# home-based signature, dropped as there. Step 2 prints the figures again.
CATCH_ALL_EXCLUDE = ("969900",)

# Sanity bounds: Odense Kommune plus ~0.02 deg. A corrupt coordinate is
# caught; the join does the placing.
ODENSE_BBOX = {
    "lat_min": 55.26,
    "lat_max": 55.52,
    "lon_min": 10.18,
    "lon_max": 10.60,
}
