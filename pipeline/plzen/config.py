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
# PMDP's GTFS - gate 3's independent count only (read 2026-09-30, PERMITTED;
# no colours, no shapes). Credited on the page's notices if used, on the
# stricter CC BY reading (the brief).
PMDP_GTFS_URL = "https://jizdnirady.pmdp.cz/jr/gtfs"
PMDP_GTFS_ZIP = DATA_RAW / "pmdp_gtfs.zip"

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
# HALVED ON THE SPACING RULE (docs/ring_rules.md): step 1 measured a 306 m
# median nearest-neighbour gap between the 53 stations (2026-09-30; the brief's
# screen read 294), under the ~550 m line.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# TRAMS ONLY (owner, 2026-09-29), from OpenStreetMap: PMDP's feed carries no
# colours and no shapes (read 2026-09-30, permitted), so it can only cross-check.
# Lines 1, 2 and 4, every stop inside the city (53 stop names, the brief).
TRAM_SOURCE = "osm"
CITY_NAME = "Plzeň"
# Stop positions of one name are one station, at their mean, when they lie
# within this of each other (pipeline/osm_tram.py's collapse; Aarhus's rule).
COLLAPSE_MAX_SPREAD_M = 200
# The station-spacing gate's floor for TRAM stops (pipeline/stations.py): the
# shared 400 m default is a metro figure. Riga's, Aarhus's and Brno's 200 m.
SPACING_MIN_M = 200.0
OSM_TRAM_OPERATOR = "Plzeňské městské dopravní podniky, a.s."
OSM_TRAM_BBOX = (49.68, 13.27, 49.81, 13.48)   # (s, w, n, e), the brief's check box
LINE_ORDER = ["1", "2", "4"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
# TODO (step 1, once pipeline/osm_tram.py exists): NOT_DRAWN (1X, 4X and the
# depot run from Vozovna Slovany, by relation id), EXPECTED_INSIDE_PER_LINE,
# gate 3 from PMDP's feed, and the palette from line_colour_search.py with
# evenly spaced target hues (owner, 2026-09-30).
NOT_DRAWN = {
    14668713: "depot run from Vozovna Slovany (no ref, no stop members)",
    14668682: "1X, depot run to Vozovna Slovany (no stop members)",
    14722301: "4X, depot run to Vozovna Slovany (no stop members)",
    # LINE 4's Bory/Univerzita -> Košutka directions carry NO operator tag in OSM
    # (2026-09-30), so the operator filter cannot keep them. Their reverse
    # directions are kept (1995933, 10427675); any stop only these two reach
    # would be listed in excluded_stations.csv - none is (step 1).
    1995932: "line 4, Bory -> Košutka: no operator tag in OSM; its reverse is kept",
    10427674: "line 4, Univerzita -> Košutka: no operator tag in OSM; its reverse is kept",
}
# TARGET hues for scripts/line_colour_search.py: evenly spaced round the
# wheel in line order, HSL (h, 70%, 45%) - no operator colours are licensed
# (owner, 2026-09-30). The search picks the feasible colour nearest each.
LINES = {"1": {"hue": "#C32222"}, "2": {"hue": "#22C322"}, "4": {"hue": "#2222C3"}}
# THIS PROJECT'S colours (owner, 2026-09-30), from `python
# scripts/line_colour_search.py plzen` on 2026-09-30: every line 3:1 on both
# map pages and CIE76 >= 45 from every pin; closest pair 124.7 (1, 2).
LINE_COLOURS = {"1": "#C02008", "2": "#00A800", "4": "#6040E8"}
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1. Measured
# 2026-09-30: 53 stations, all inside obec 554791 (the brief's 19 / 23 / 19).
EXPECTED_INSIDE_PER_LINE = {"1": 19, "2": 23, "4": 19}
# GATE 3, from PMDP's GTFS (the approved cross-check): the stop names each line
# serves on an ordinary Wednesday (2026-10-07), at Brno's 10%-of-trips rule.
# Line 2 agrees exactly. Line 1's one extra is the Vozovna Slovany depot stop;
# line 4's ten extras are a depot-bound variant over line 1's track, every stop
# of it already a station here but the depot, which is left out as Brno's
# Vozovna Medlánky is. So the station SET matches PMDP's but for the depot.
# Jízdecká and U Synagogy, which a whole-feed count added, run on ONE day only
# (service 44, no weekday flags, 2026-10-10 by calendar_dates): a diversion,
# not stops, so they are not added.
OPERATOR_STATION_COUNTS = {"Tram 1": 20, "Tram 2": 23, "Tram 4": 29}
OPERATOR_COUNTS_SOURCE = ("PMDP GTFS, stop names per line on Wed 2026-10-07 at >= 10% of "
                          "trips; 1 and 4 differ by the depot and line 4's depot variant")

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
