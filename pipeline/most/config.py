"""Most (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py, then replaced with the Czech tram
template (`.claude/skills/czech-tram-city/SKILL.md`, section 8). The national
facts live in `pipeline/countries/czechia.py`, the register chain in
`czechia_register.py`, which reads one RUIAN file per obec. What is this
city's own is below: TWO obce, Most and Litvínov, which the trams join. The
brief is `docs/build_briefs/most.md`.
"""

from pathlib import Path

SLUG = "most"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "most" / "raw"
DATA_PROCESSED = ROOT / "data" / "most" / "processed"
OUTPUTS = ROOT / "outputs" / "most"

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
# REGIONAL, MOST WITH LITVÍNOV - required, not chosen: Most alone fails the stub
# test (its lines keep 12 of 24, 6 of 18 and 9 of 21 stops). Built last, as
# "Most (Regional)" (owner, 2026-09-30). Businesses are scoped by each obec's
# own RUIAN address list.
SCOPE = "regional"
OBEC_CODES = ["567027", "567256"]
OBEC_NAMES = {"567027": "Most", "567256": "Litvínov"}
RUIAN_ZIPS = {o: DATA_RAW / f"ruian_adr_{o}.csv.zip" for o in OBEC_CODES}
# One RUIAN coordinate control PER FILE (staging, 2026-09-30): Most's Magistrát,
# which RUIAN transforms to 50.50287, 13.64052; Litvínov's town hall, OSM's
# node, which RUIAN transforms to 50.59884, 13.61173.
RUIAN_CRS_CONTROLS = {
    "567027": ("25298429", 50.50284, 13.64078, "Most Town Hall (Magistrát), Radniční 1/2"),
    "567256": ("5150507", 50.59881, 13.61171, "Litvínov Town Hall, náměstí Míru 11"),
}
# OSM relations 436570 (Most, ref CZ0425567027) and 436574 (Litvínov, ref
# CZ0425567256). ~86.9 + ~40.7 km2 by the Czech Statistical Office.
OSM_BOUNDARY_RELATIONS = {"567027": 436570, "567256": 436574}
BOUNDARY_AREA_KM2 = (123.0, 132.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 33N: ~13.6 E falls in the 12-18 band.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED ON THE SPACING RULE - JUST: the brief measured a 514 m median stop gap
# across both towns, 36 m under the ~550 m line. Step 1 re-measures it; over
# 550, the standard edges come back and the page drops its half-size sentence.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# TRAMS ONLY, from OpenStreetMap: lines 1-4, 8 relations, operator Dopravní
# podnik měst Mostu a Litvínova.
TRAM_SOURCE = "osm"
OSM_TRAM_OPERATOR = "Dopravní podnik měst Mostu a Litvínova"
OSM_TRAM_BBOX = (50.46, 13.49, 50.62, 13.71)   # (s, w, n, e), the brief's check box
LINE_ORDER = ["1", "2", "3", "4"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
# TODO (step 1, once pipeline/osm_tram.py exists): NOT_DRAWN,
# EXPECTED_INSIDE_PER_LINE, gate 3, and the palette (owner, 2026-09-30).
NOT_DRAWN = {}
LINES = {}
LINE_COLOURS = {}
EXPECTED_INSIDE_PER_LINE = {}
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = ""

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CITY_KEEP = "MOST"   # kept for the scaffold's templates; OBEC_CODES filters
CATCH_ALL_EXCLUDE = ("96990", "969")   # (owner, 2026-09-29) R2

# Sanity bounds: the placed storefronts' measured extent across both obce
# (50.4711-50.6148 N, 13.5603-13.6751 E, step 2, 2026-09-30) plus ~0.02 deg.
MOST_BBOX = {
    "lat_min": 50.45,
    "lat_max": 50.64,
    "lon_min": 13.54,
    "lon_max": 13.70,
}

# --- The macro map ---------------------------------------------------------
MAP_MODE = "tram"
MAP_COVERAGE = "full"
