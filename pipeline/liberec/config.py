"""Liberec (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py, then replaced with the Czech tram
template (`.claude/skills/czech-tram-city/SKILL.md`, section 8). The national
facts live in `pipeline/countries/czechia.py`, the register chain in
`czechia_register.py`, which reads one RUIAN file per obec. What is this
city's own is below: TWO obce, Liberec and Jablonec nad Nisou, joined by the
interurban tram line 11. The brief is `docs/build_briefs/liberec.md`.
"""

from pathlib import Path

SLUG = "liberec"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "liberec" / "raw"
DATA_PROCESSED = ROOT / "data" / "liberec" / "processed"
OUTPUTS = ROOT / "outputs" / "liberec"

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
# REGIONAL, WITH JABLONEC NAD NISOU (owner, 2026-09-30): every line whole, where
# Liberec alone would keep line 11 at 14 of its 21 stops (67%). Businesses are
# scoped by each obec's own RUIAN address list, never by a polygon.
SCOPE = "regional"
OBEC_CODES = ["563889", "563510"]
OBEC_NAMES = {"563889": "Liberec", "563510": "Jablonec nad Nisou"}
RUIAN_ZIPS = {o: DATA_RAW / f"ruian_adr_{o}.csv.zip" for o in OBEC_CODES}
# One RUIAN coordinate control PER FILE, each against OSM (staging, 2026-09-30):
# Liberec's town hall within 0.0004 deg of OSM's square; Jablonec's within
# 0.0005 deg of the square's OSM points.
RUIAN_CRS_CONTROLS = {
    "563889": ("23653124", 50.77000, 15.05845, "Liberec Town Hall, nám. Dr. E. Beneše 1/1"),
    "563510": ("12188018", 50.72452, 15.17128, "Jablonec Town Hall, Mírové náměstí 3100/19"),
}
# OSM relations 439073 (Liberec, ref CZ0513563889) and 438931 (Jablonec, ref
# CZ0512563510). ~106.1 + ~31.4 km2 by the Czech Statistical Office.
OSM_BOUNDARY_RELATIONS = {"563889": 439073, "563510": 438931}
BOUNDARY_AREA_KM2 = (133.0, 142.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 33N: ~15.06-15.17 E falls in the 12-18 band.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED ON THE SPACING RULE: step 1 measured a 355 m median nearest-neighbour
# gap between the 39 stations across both obce (2026-09-30; the screen read 378).
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# TRAMS ONLY, from OpenStreetMap: DPMLJ's own GTFS reset the connection at the
# screen. Lines 2, 3, 5 and 11; line 11 is the interurban, 14 stops in Liberec
# and 7 in Jablonec.
TRAM_SOURCE = "osm"
CITY_NAME = "Liberec (Regional)"
# Stop positions of one name are one station, at their mean, when they lie
# within this of each other (pipeline/osm_tram.py's collapse; Aarhus's rule).
COLLAPSE_MAX_SPREAD_M = 200
# The station-spacing gate's floor for TRAM stops (pipeline/stations.py): the
# shared 400 m default is a metro figure. Riga's, Aarhus's and Brno's 200 m.
SPACING_MIN_M = 200.0
OSM_TRAM_OPERATOR = "Dopravní podnik měst Liberce a Jablonce nad Nisou"
OSM_TRAM_BBOX = (50.69, 14.95, 50.82, 15.22)   # (s, w, n, e), the brief's check box
LINE_ORDER = ["2", "3", "5", "11"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
# Every route=tram relation in the box is the operator's and is kept
# (8 relations, 2026-09-30), so nothing is NOT_DRAWN.
NOT_DRAWN = {}
# THE REGULAR NETWORK, NOT TODAY'S (owner, 2026-09-30): from 2026-06-20 to at
# least 2026-12-12 lines 2 and 3 end at Fügnerova, and Šaldovo náměstí is
# closed for the works (IDOS). OSM keeps the track and the stop only as two
# platform nodes, on no relation; both are added for lines 2 and 3, as IDOS
# has them on 2026-06-15.
STATION_ADD = {
    612457988: (("2", "3"), "Šaldovo náměstí"),
    4825357131: (("2", "3"), "Šaldovo náměstí"),
}
# Line 11 calls at Fügnerova and Sídliště Nové Vratislavice on every trip, in
# regular service and today (IDOS, 2026-06-15 and 2026-10-01); its two OSM
# relations pass both without listing them, and line 5 lists them. Each stop
# position is added to line 11 (czechia_osm_tram.add_line_stops).
LINE_STOP_ADD = {
    4538307888: ("11", "Fügnerova"),
    4538308197: ("11", "Fügnerova"),
    649882240: ("11", "Sídliště Nové Vratislavice"),
    5793026873: ("11", "Sídliště Nové Vratislavice"),
}
# TARGET hues for scripts/line_colour_search.py: evenly spaced round the
# wheel in line order, HSL (h, 70%, 45%) - no operator colours are licensed
# (owner, 2026-09-30). The search picks the feasible colour nearest each.
LINES = {"2": {"hue": "#C32222"}, "3": {"hue": "#73C322"}, "5": {"hue": "#22C3C3"}, "11": {"hue": "#7322C3"}}
# THIS PROJECT'S colours (owner, 2026-09-30), from `python
# scripts/line_colour_search.py liberec` on 2026-09-30: every line 3:1 on both
# map pages and CIE76 >= 45 from every pin; closest pair 88.3 (3, 5).
LINE_COLOURS = {"2": "#C02008", "3": "#50A800", "5": "#00A0B8", "11": "#8830D0"}
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1. Measured
# 2026-09-30: 39 stations, all inside the two obce - 33 in Liberec and 6 in
# Jablonec nad Nisou (the brief's screen read 32 + 7: one stop lies on the
# other side of the line than its stop-name count assumed). Every line whole.
# 2026-09-30, after gate 3: 40 stations - Šaldovo náměstí added on 2 and 3,
# and line 11's two missing calls.
EXPECTED_INSIDE_PER_LINE = {"2": 17, "3": 21, "5": 13, "11": 23}
# GATE 3, from IDOS's per-stop timetables (DPMLJ's own site and feed refuse
# us): both directions of each line on Monday 2026-06-15, regular service,
# five days before the works; a stop counts when either direction calls.
OPERATOR_STATION_COUNTS = {"Tram 2": 17, "Tram 3": 21, "Tram 5": 13, "Tram 11": 23}
OPERATOR_COUNTS_SOURCE = ("IDOS zastávkové jízdní řády, idos.cz/liberec/zjr, "
                          "2026-06-15, both directions (read 2026-09-30)")

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CITY_KEEP = "LIBEREC"   # kept for the scaffold's templates; OBEC_CODES filters
CATCH_ALL_EXCLUDE = ("96990", "969")   # (owner, 2026-09-29) R2

# Sanity bounds: the placed storefronts' measured extent across both obce
# (50.6999-50.8098 N, 14.9846-15.1971 E, step 2, 2026-09-30) plus ~0.02 deg.
LIBEREC_BBOX = {
    "lat_min": 50.67,
    "lat_max": 50.83,
    "lon_min": 14.96,
    "lon_max": 15.22,
}

# --- The macro map ---------------------------------------------------------
MAP_MODE = "tram"
MAP_COVERAGE = "full"
