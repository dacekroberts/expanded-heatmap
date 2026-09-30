"""Ostrava-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py, then replaced with the Czech tram
template (`.claude/skills/czech-tram-city/SKILL.md`, section 8). The national
facts live in `pipeline/countries/czechia.py`, the register chain in
`czechia_register.py`. What is Ostrava's own is below - including its UTM
zone, 34N, not the 33N of every other Czech city. The brief is
`docs/build_briefs/ostrava.md`.
"""

from pathlib import Path

SLUG = "ostrava"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ostrava" / "raw"
DATA_PROCESSED = ROOT / "data" / "ostrava" / "processed"
OUTPUTS = ROOT / "outputs" / "ostrava"

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
# Obec 554821, Ostrava. Businesses are scoped by RUIAN's own address list for
# the obec, never by a polygon.
SCOPE = "obec"
OBEC_CODES = ["554821"]
RUIAN_ZIPS = {o: DATA_RAW / f"ruian_adr_{o}.csv.zip" for o in OBEC_CODES}
# The RUIAN coordinate control: the Magistrát at 30. dubna 635/35, against OSM's
# town-hall node (staging, 2026-09-30); RUIAN transforms it to 49.84131, 18.28926.
RUIAN_CRS_CONTROLS = {"554821": ("3182860", 49.84130, 18.28927,
                                 "Magistrát města Ostravy, 30. dubna 635/35")}
# OSM relation 437354, "Ostrava", admin_level 8, ref CZ0806554821. ~214.2 km2
# by the Czech Statistical Office.
OSM_BOUNDARY_RELATIONS = {"554821": 437354}
BOUNDARY_AREA_KM2 = (208.0, 220.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# ⚠ UTM zone 34N: Ostrava's longitude (~18.29 E) is PAST the 18 E line, so it
# falls in the 18-24 band - not Prague's, Brno's or any other Czech city's 33N.
# Derived per city, never copied.
CRS_PROJECTED = "EPSG:32634"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED ON THE SPACING RULE: the brief measured a 424 m median stop gap.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# TRAMS ONLY, from OpenStreetMap (no reachable feed at the screen). Every
# relation tagged operator Dopravní podnik Ostrava. LINE 5, the suburban line to
# Budišovice, is LEFT OUT (owner, 2026-09-30): 3 of its 10 stops are in the city
# (30%), below every stub precedent; it costs Poruba,koupaliště and Krásné Pole.
TRAM_SOURCE = "osm"
OSM_TRAM_OPERATOR = "Dopravní podnik Ostrava"
OSM_TRAM_BBOX = (49.73, 18.10, 49.91, 18.38)   # (s, w, n, e), the brief's check box
LINE_ORDER = ["1", "2", "3", "4", "6", "7", "8", "10", "11", "12", "14", "15", "17", "18"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
# TODO (step 1, once pipeline/osm_tram.py exists): NOT_DRAWN by relation id -
# line 5 (owner), 9 and 19 (no stop members), 19177807 (an unref'd line 11
# variant) and anything else in the box - EXPECTED_INSIDE_PER_LINE, gate 3, and
# the palette from line_colour_search.py (owner, 2026-09-30).
NOT_DRAWN = {}
LINES = {}
LINE_COLOURS = {}
EXPECTED_INSIDE_PER_LINE = {}
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = ""

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CITY_KEEP = "OSTRAVA"   # kept for the scaffold's templates; OBEC_CODES filters
CATCH_ALL_EXCLUDE = ("96990", "969")   # (owner, 2026-09-29) R2

# Sanity bounds: the placed storefronts' measured extent (49.7487-49.9041 N,
# 18.1145-18.3587 E, step 2, 2026-09-30) plus ~0.02 deg.
OSTRAVA_BBOX = {
    "lat_min": 49.72,
    "lat_max": 49.93,
    "lon_min": 18.09,
    "lon_max": 18.38,
}

# --- The macro map ---------------------------------------------------------
MAP_MODE = "tram"
MAP_COVERAGE = "full"
