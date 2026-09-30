"""Olomouc-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py, then replaced with the Czech tram
template (`.claude/skills/czech-tram-city/SKILL.md`, section 8). The national
facts live in `pipeline/countries/czechia.py`, the register chain in
`czechia_register.py`. What is Olomouc's own is below. The brief is
`docs/build_briefs/olomouc.md`.
"""

from pathlib import Path

SLUG = "olomouc"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "olomouc" / "raw"
DATA_PROCESSED = ROOT / "data" / "olomouc" / "processed"
OUTPUTS = ROOT / "outputs" / "olomouc"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_TRAM_JSON = DATA_RAW / "osm_tram.json"

# --- Scope ---------------------------------------------------------------
#
# Obec 500496, Olomouc. Businesses are scoped by RUIAN's own address list for
# the obec, never by a polygon.
SCOPE = "obec"
OBEC_CODES = ["500496"]
RUIAN_ZIPS = {o: DATA_RAW / f"ruian_adr_{o}.csv.zip" for o in OBEC_CODES}
# The RUIAN coordinate control: the town hall, Horní náměstí 583, against OSM's
# house point through Nominatim (staging, 2026-09-30).
RUIAN_CRS_CONTROLS = {"500496": ("25321960", 49.59393, 17.25164,
                                 "Olomouc Town Hall, Horní náměstí 583")}
# OSM relation 437057, "Olomouc", admin_level 8, ref CZ0712500496. ~103.3 km2
# by the Czech Statistical Office.
OSM_BOUNDARY_RELATIONS = {"500496": 437057}
BOUNDARY_AREA_KM2 = (100.0, 107.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 33N: Olomouc's longitude (~17.25 E) falls in the 12-18 band.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED ON THE SPACING RULE: the brief measured a 318 m median stop gap.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# TRAMS ONLY, from OpenStreetMap (owner, 2026-09-30): DPMO's feed declares no
# licence and colours every route white, so it is not used at all, not even
# for gate 3. Lines 1-7, every stop inside the city (36 stop names).
TRAM_SOURCE = "osm"
OSM_TRAM_OPERATOR = "Dopravní podnik města Olomouce"
OSM_TRAM_BBOX = (49.53, 17.16, 49.66, 17.40)   # (s, w, n, e), the brief's check box
LINE_ORDER = ["1", "2", "3", "4", "5", "6", "7"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
# TODO (step 1, once pipeline/osm_tram.py exists): NOT_DRAWN,
# EXPECTED_INSIDE_PER_LINE, gate 3 (DPMO's published stop lists, a count),
# and the palette from line_colour_search.py (owner, 2026-09-30).
NOT_DRAWN = {}
LINES = {}
LINE_COLOURS = {}
EXPECTED_INSIDE_PER_LINE = {}
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = ""

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CITY_KEEP = "OLOMOUC"   # kept for the scaffold's templates; OBEC_CODES filters
CATCH_ALL_EXCLUDE = ("96990", "969")   # (owner, 2026-09-29) R2

# Sanity bounds: the placed storefronts' measured extent (49.5480-49.6428 N,
# 17.1770-17.3641 E, step 2, 2026-09-30) plus ~0.02 deg.
OLOMOUC_BBOX = {
    "lat_min": 49.52,
    "lat_max": 49.67,
    "lon_min": 17.15,
    "lon_max": 17.39,
}

# --- The macro map ---------------------------------------------------------
MAP_MODE = "tram"
MAP_COVERAGE = "full"
