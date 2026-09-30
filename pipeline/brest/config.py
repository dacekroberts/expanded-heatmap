"""Brest-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_france_batch.py (the France tram batch) from the
2026-09-27 screen's inputs and the station table in `data/_staging_scratch_2026-09-27/second_cities/france/stations_pure_2026-09-30`.
Read `.claude/skills/france-tram-city/SKILL.md` and
`docs/build_briefs/brest.md` before filling anything. Every to-do marker is a value
only the build-day feed or the owner can supply; none may ship.
"""

from pathlib import Path

# The national facts, shared with every French city (see pipeline/rennes/config.py).
from pipeline.countries.france import (  # noqa: F401
    COMMUNE_COLUMN,
    DIFFUSION_COLUMN,
    DIFFUSION_PUBLIC_VALUE,
    EMPLOYEE_BAND_COLUMN,
    ENSEIGNE_COLUMNS,
    GEO_EPSG_COLUMN,
    GEO_LAT_COLUMN,
    GEO_LON_COLUMN,
    GEO_QUALITY_COLUMN,
    GEOLOC_DATASET_SLUG,
    GEOLOC_PARQUET,
    GEOLOC_RESOURCE_TITLE_CONTAINS,
    JOIN_KEY,
    METROPOLITAN_EPSG,
    NAF_COLUMN,
    SIRENE_DATASET_SLUG,
    SIRENE_PARQUET,
    SIRENE_RESOURCE_TITLE_PREFIX,
    STATE_ACTIVE_VALUE,
    STATE_COLUMN,
    USUAL_NAME_COLUMN,
)

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "brest" / "raw"
DATA_PROCESSED = ROOT / "data" / "brest" / "processed"
OUTPUTS = ROOT / "outputs" / "brest"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the commune, each with the commune it IS in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Every commune of the EPCI(s) the network runs in, with contours: the naming
# layer for excluded stations (commune scope) or the scoping layer (regional).
METRO_COMMUNES_GEOJSON = DATA_RAW / "metropole_communes.geojson"

# --- The feed ------------------------------------------------------------

# ⚠ ROLLING. French tram feeds run four to twelve weeks ahead, so the build
# FETCHES THIS FRESH on every run and never trusts a cached copy - including the
# screen's 2026-09-27 copy that may sit in data/brest/raw/ already.
GTFS_URL = "https://www.data.gouv.fr/api/1/datasets/r/583d1419-058b-481b-b378-449cab744c82"
GTFS_DATASET = "Réseau urbain Bibus"
# The licence the NAP declares for this dataset. Licence Ouverte 2.0: credit
# the producer and the date.
GTFS_LICENCE = "lov2"
# Measured 2026-09-30 by the kit session: feed_info.txt self-attests; ends
# 2026-12-20. The cable car C (route_type 6) is DRAWN (owner, 2026-09-30,
# Toulouse's Téléo precedent). The FIC_LIB1/2 stops are track switches, not
# stations.
# Read at build: the zip's feed_info.txt carries a feed_end_date, so the
# page quotes the operator's own window.
GTFS_SELF_ATTESTS = True
# The NAP dataset: fetch_sources.py reads the resource's date and window from it.
GTFS_NAP_ID = "55ffbe0888ee387348ccb97d"

BOUNDARY_COMMUNE_CODE = "29019"
# ⚠ `geometry=contour`, NOT `fields=contour` (a 120-byte POINT, no error).
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/29019"
                "?geometry=contour&format=geojson")
METROPOLE_EPCI_CODES = ["242900314"]
METROPOLE_COMMUNES_URLS = [
    f"https://geo.api.gouv.fr/epcis/{code}/communes"
    "?fields=nom,code&geometry=contour&format=geojson"
    for code in METROPOLE_EPCI_CODES
]

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# LAMBERT-93, as every French city takes it: one national grid for one national
# register, where a per-city UTM rule would split France across zones 30-32.
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# Median nearest-neighbour gap 425 m across the 39 in-scope stations (min 49
# m), Lambert-93, measured from the kit's station table - under ~550 m, so the
# half-size rings every French city takes (docs/ring_rules.md). Step 1 re-
# measures.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# APPROVED by the owner 2026-09-30, as docs/build_briefs/brest.md recommended:
#   scope    commune - the worst line, A, keeps 28 of 30 stations (93%) in
#            commune 29019; half or more stays commune-only (Toulouse 52%,
#            Rennes 73%)
#   mode     tram (the macro map's dot colour: what step 1 keeps, never the
#            feed's route_type flag)
#   coverage full (SIRENE: all three buckets)
SCOPE = "commune"
MAP_MODE = "tram"
MAP_COVERAGE = "full"

# What the feed types the kept lines as. Matched together with the line list,
# never alone: a type flag is not a mode decision (Reims and Rouen type theirs 1).
ROUTE_TYPES_RAIL = ("0", "6",)
# The kept lines, by the feed's route_short_name.
LINE_KEYS = ["A", "B", "C"]
# The build-day feed's route_ids (read by scripts/france_fill_build_day.py).
# A rolling feed may renumber: step 1 exits if they change.
ROUTE_IDS = ["A", "B", "C"]

# Station rule (owner, 2026-09-29 and 09-30): the feed's own parent_station
# row, else the FIRST platform in stops.txt order per unchanged stop_name.
# Never a mean, never a rename. On a Licence Ouverte feed ONLY, a same-name
# pair (case and accents ignored) within 150 m keeps its first row; on an ODbL
# feed, never. Fictitious FIC_ stops are not stations.
# Measured 2026-09-30: 41 stations network-wide.
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is checkable. If these move, the decision is being re-taken.
EXPECTED_INSIDE_PER_LINE = {"A": 28, "B": 11, "C": 2}
EXPECTED_STATIONS_PER_LINE = {"A": 30, "B": 11, "C": 2}

# GATE 3, recorded as the outside sources have it (2026-09-30). Tram A reads
# 25 against the feed's 30, and that is OpenStreetMap's shape, not a missing
# station: A forks at its north end into the Porte de Gouesnou and Porte de
# Guipavas branches, each OSM relation covers ONE branch (25 stops each), and
# some A trips run on to Gares. Tram B is exact. The cable car is not an OSM
# route=tram relation (it is an aerialway), so its count is the Téléphérique de
# Brest's two stations, Jean Moulin and Ateliers.
OPERATOR_STATION_COUNTS = {"A": 25, "B": 11, "C": 2}
OPERATOR_COUNTS_SOURCE = (
    "OpenStreetMap route relations for A (one branch per relation) and B; the "
    "cable car's two stations; read 2026-09-30")

# route_short_name -> the name riders use: Bibus names its tram lines A and B;
# the cable car is the Téléphérique, and the map spells out the mode, as Le
# Mans's and Toulouse's do.
LINE_NAMES = {"A": "Tram A", "B": "Tram B", "C": "Téléphérique"}
# Each line's route_color from the build-day feed (the most-used route_id's
# where a line has several); pipeline/linecolour.py decides a clash.
LINE_COLOURS = {"A": "#DE007E", "B": "#004F9E", "C": "#EA6758"}

# The map's layer and title prefix for the lines.
MAP_SYSTEM_NAME = "Tram and Téléphérique"
# Where the line GEOMETRY comes from: "gtfs" (the feed's shapes.txt) or "osm".
# Stations come from the feed either way.
LINE_GEOMETRY = "gtfs"
# OpenStreetMap route relations, for gate 3's count (geometry is the feed's):
# ONE query per city, cached by fetch_sources.py. Read 2026-09-30: the bbox
# returns Bibus's six tram relations (A in four, one per branch and direction).
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];"
    'relation["type"="route"]["route"~"^(tram|light_rail)$"]'
    "(48.34,-4.59,48.48,-4.41);"
    "out geom;")
# line key -> the relations' `ref` tag, checked against the fetched file (no
# relation for the cable car, an aerialway).
OSM_REFS = {"A": "A", "B": "B"}

# --- Business filtering ------------------------------------------------

# EXACT INSEE codes, from the station table's own commune placement.
# Legacy codes checked 2026-09-30 against geo.api.gouv.fr's communes associées
# and déléguées (Lille's 59298 and 59355 the control): none in this scope.
COMMUNE_PREFIXES = ("29019",)

CITY_KEEP = "BREST"   # scaffold field; COMMUNE_PREFIXES is the filter

# The French precedent (Paris, Marseille, Toulouse, Lille, Rennes): both
# catch-alls excluded on INSEE's own labels. A share is a fact about a city, so
# step 2 prints this city's; a share far from the siblings' goes to the owner.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the commune's extent plus ~0.02 deg, from the EPCI
# contours. They catch a corrupt coordinate; the commune filter scopes.
BREST_BBOX = {"lat_min": 48.34, "lat_max": 48.48, "lon_min": -4.59, "lon_max": -4.41}
