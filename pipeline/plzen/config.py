"""Plzeň-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py, then replaced with the Czech tram
template (`.claude/skills/czech-tram-city/SKILL.md`, section 8). The national
facts live in `pipeline/countries/czechia.py`, the register chain in
`czechia_register.py`. What is Plzeň's own is below. The brief is
`docs/build_briefs/plzen.md`.
"""

from pathlib import Path

SLUG = "plzen"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "plzen" / "raw"
DATA_PROCESSED = ROOT / "data" / "plzen" / "processed"
OUTPUTS = ROOT / "outputs" / "plzen"

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
# Obec 554791, Plzeň. Businesses are scoped by RUIAN's own address list for
# the obec (ROS02's PKODADM in it), never by a polygon.
SCOPE = "obec"
OBEC_CODES = ["554791"]
RUIAN_ZIPS = {o: DATA_RAW / f"ruian_adr_{o}.csv.zip" for o in OBEC_CODES}
# The RUIAN coordinate control (czechia_register.ruian()): the Magistrát,
# náměstí Republiky 1/1, against OSM's node for it, a source independent of
# the file. Measured by staging 2026-09-30: RUIAN transforms it to 49.74812,
# 13.37771, 0.0002 deg from OSM's node.
RUIAN_CRS_CONTROLS = {"554791": ("24570222", 49.74836, 13.37775,
                                 "Magistrát města Plzně, náměstí Republiky 1/1")}
# OSM relation 438344, "Plzeň", admin_level 8, ref CZ0323554791 (the district
# code plus the RUIAN obec code). ~137.7 km2 by the Czech Statistical Office.
OSM_BOUNDARY_RELATIONS = {"554791": 438344}
BOUNDARY_AREA_KM2 = (133.0, 142.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 33N: Plzeň's longitude (~13.38 E) falls in the 12-18 band.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED ON THE SPACING RULE (docs/ring_rules.md): the brief measured a 294 m
# median gap between the stops, under the ~550 m line. Step 1 re-measures it.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# TRAMS ONLY (owner, 2026-09-29), from OpenStreetMap: PMDP's feed carries no
# colours and no shapes (read 2026-09-30, permitted), so it can only cross-check.
# Lines 1, 2 and 4, every stop inside the city (53 stop names, the brief).
TRAM_SOURCE = "osm"
OSM_TRAM_OPERATOR = "Plzeňské městské dopravní podniky, a.s."
OSM_TRAM_BBOX = (49.68, 13.27, 49.81, 13.48)   # (s, w, n, e), the brief's check box
LINE_ORDER = ["1", "2", "4"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
# TODO (step 1, once pipeline/osm_tram.py exists): NOT_DRAWN (1X, 4X and the
# depot run from Vozovna Slovany, by relation id), EXPECTED_INSIDE_PER_LINE,
# gate 3 from PMDP's feed, and the palette from line_colour_search.py with
# evenly spaced target hues (owner, 2026-09-30).
NOT_DRAWN = {}
LINES = {}
LINE_COLOURS = {}
EXPECTED_INSIDE_PER_LINE = {}
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = ""

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CITY_KEEP = "PLZEN"   # kept for the scaffold's templates; OBEC_CODES filters
CATCH_ALL_EXCLUDE = ("96990", "969")   # (owner, 2026-09-29) R2

# Sanity bounds: the placed storefronts' measured extent (49.6883-49.8028 N,
# 13.2948-13.4583 E, step 2, 2026-09-30) plus ~0.02 deg. The RUIAN join does
# the placing; this catches a CRS or axis error after the control.
PLZEN_BBOX = {
    "lat_min": 49.66,
    "lat_max": 49.83,
    "lon_min": 13.27,
    "lon_max": 13.48,
}

# --- The macro map ---------------------------------------------------------
MAP_MODE = "tram"
MAP_COVERAGE = "full"
