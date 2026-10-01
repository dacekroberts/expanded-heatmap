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
# HALVED ON THE SPACING RULE: step 1 measured a 316 m median nearest-neighbour
# gap between the 36 stations (2026-09-30; the brief's screen read 318).
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# TRAMS ONLY, from OpenStreetMap (owner, 2026-09-30): DPMO's feed declares no
# licence and colours every route white, so it is not used at all, not even
# for gate 3. Lines 1-7, every stop inside the city (36 stop names).
TRAM_SOURCE = "osm"
CITY_NAME = "Olomouc"
# Stop positions of one name are one station, at their mean, when they lie
# within this of each other (pipeline/osm_tram.py's collapse; Aarhus's rule).
COLLAPSE_MAX_SPREAD_M = 200
# The station-spacing gate's floor for TRAM stops (pipeline/stations.py): the
# shared 400 m default is a metro figure. Riga's, Aarhus's and Brno's 200 m.
SPACING_MIN_M = 200.0
OSM_TRAM_OPERATOR = "Dopravní podnik města Olomouce"
OSM_TRAM_BBOX = (49.53, 17.16, 49.66, 17.40)   # (s, w, n, e), the brief's check box
LINE_ORDER = ["1", "2", "3", "4", "5", "6", "7"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
# Every route=tram relation in the box is the operator's and is kept
# (14 relations, 2026-09-30), so nothing is NOT_DRAWN.
NOT_DRAWN = {}
# TARGET hues for scripts/line_colour_search.py: evenly spaced round the
# wheel in line order, HSL (h, 70%, 45%) - no operator colours are licensed
# (owner, 2026-09-30). The search picks the feasible colour nearest each.
LINES = {"1": {"hue": "#C32222"}, "2": {"hue": "#C3AC22"}, "3": {"hue": "#50C322"}, "4": {"hue": "#22C37E"}, "5": {"hue": "#227EC3"}, "6": {"hue": "#5022C3"}, "7": {"hue": "#C322AC"}}
# THIS PROJECT'S colours (owner, 2026-09-30), from `python
# scripts/line_colour_search.py olomouc` on 2026-09-30: every line 3:1 on both
# map pages and CIE76 >= 45 from every pin; closest pair 19.4 (3, 4), within 500 m and anywhere.
LINE_COLOURS = {"1": "#C02008", "2": "#A89000", "3": "#30A800", "4": "#68A008", "5": "#08A0C0", "6": "#7040E0", "7": "#C820B0"}
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1. Measured
# 2026-09-30: 36 stations, all inside obec 500496 (the brief's figures).
EXPECTED_INSIDE_PER_LINE = {"1": 11, "2": 14, "3": 16, "4": 20, "5": 10, "6": 14, "7": 14}
# GATE 3, from IDOS's per-stop timetables (DPMO's feed is not used at all,
# owner 2026-09-30, and its own stop lists are PDFs only): both directions of
# each line on Monday 2026-03-16, regular service; 2026-10-01 is identical. A
# stop counts when either direction calls - line 4 calls at Fibichova and
# Pavlovická toward Pavlovičky only.
OPERATOR_STATION_COUNTS = {"Tram 1": 11, "Tram 2": 14, "Tram 3": 16, "Tram 4": 20,
                           "Tram 5": 10, "Tram 6": 14, "Tram 7": 14}
OPERATOR_COUNTS_SOURCE = ("IDOS zastávkové jízdní řády, idos.cz/olomouc/zjr, "
                          "2026-03-16, both directions (read 2026-09-30)")

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
