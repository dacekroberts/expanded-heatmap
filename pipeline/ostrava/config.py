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
# HALVED ON THE SPACING RULE: step 1 measured a 431 m median nearest-neighbour
# gap between the 92 stations (2026-09-30; the brief's screen read 424).
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
CITY_NAME = "Ostrava"
# Stop positions of one name are one station, at their mean, when they lie
# within this of each other (pipeline/osm_tram.py's collapse; Aarhus's rule).
# 330 m HERE, NOT 200, on measurement (2026-09-30): two names are interchanges
# whose stops sit on different arms of a junction - Sport Aréna 321 m (lines
# 2/7 on one arm, 11/12 on the other) and Mariánské náměstí 223 m (three stops
# round the square). Inside Riga's 300 and Osaka's 400 for real interchanges;
# the next widest name is 173 m.
COLLAPSE_MAX_SPREAD_M = 330
# The station-spacing gate's floor for TRAM stops (pipeline/stations.py): the
# shared 400 m default is a metro figure. Riga's, Aarhus's and Brno's 200 m.
SPACING_MIN_M = 200.0
OSM_TRAM_OPERATOR = "Dopravní podnik Ostrava"
OSM_TRAM_BBOX = (49.73, 18.10, 49.91, 18.38)   # (s, w, n, e), the brief's check box
LINE_ORDER = ["1", "2", "3", "4", "6", "7", "8", "10", "11", "12", "14", "15", "17", "18"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
# ONE STATION UNDER TWO NAMES, twice (step 1's close-pair note, 2026-09-30):
# OSM names two stands of one stop separately. Hranečník (St. 1) [10/14] and
# (St. 5) [4/10/12/14], 120 m apart, are stands of the one interchange; Nová Huť
# hlavní brána 1 and 2 [14, 4/14], 61 m apart, a direction pair. Each folds into
# the spelling more lines carry (osm_tram requires both spellings present, so a
# stale alias stops the step; it never invents a bare name).
STATION_NAME_ALIASES = {
    "Hranečník (St. 1)": "Hranečník (St. 5)",
    "Nová Huť hlavní brána 1": "Nová Huť hlavní brána 2",
}
NOT_DRAWN = {
    3163382: "line 5, the suburban line to Budišovice: 3 of its 10 stops in the city (owner, 2026-09-30)",
    10693394: "line 5, the suburban line to Budišovice: 3 of its 10 stops in the city (owner, 2026-09-30)",
    917552: "line 9: no stop members in OSM (a special or peak service)",
    3163171: "line 19: no stop members in OSM (a special or peak service)",
    19177807: "an unref'd line 11 variant from the Poruba depot (Poruba,vozovna - Zábřeh)",
}
# TARGET hues for scripts/line_colour_search.py: evenly spaced round the
# wheel in line order, HSL (h, 70%, 45%) - no operator colours are licensed
# (owner, 2026-09-30). The search picks the feasible colour nearest each.
LINES = {"1": {"hue": "#C32222"}, "2": {"hue": "#C36722"}, "3": {"hue": "#C3AC22"}, "4": {"hue": "#95C322"}, "6": {"hue": "#50C322"}, "7": {"hue": "#22C339"}, "8": {"hue": "#22C37E"}, "10": {"hue": "#22C3C3"}, "11": {"hue": "#227EC3"}, "12": {"hue": "#2239C3"}, "14": {"hue": "#5022C3"}, "15": {"hue": "#9522C3"}, "17": {"hue": "#C322AC"}, "18": {"hue": "#C32267"}}
# THIS PROJECT'S colours (owner, 2026-09-30), from `python
# scripts/line_colour_search.py ostrava` on 2026-09-30: every line 3:1 on both
# map pages and CIE76 >= 45 from every pin; closest pair within 500 m 18.3 (12, 14); anywhere 15.8 (10, 11).
LINE_COLOURS = {"1": "#C02008", "2": "#C06820", "3": "#A89000", "4": "#70A000", "6": "#30A800", "7": "#688008", "8": "#687028", "10": "#00A0B8", "11": "#007890", "12": "#6048E0", "14": "#8030E8", "15": "#9828C8", "17": "#C820B0", "18": "#D060C8"}
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1. Measured
# 2026-09-30: 92 stations, all inside obec 554821 (the brief's 96 less line 5's
# two own stops and the two stand pairs folded above). Min gap 168 m.
EXPECTED_INSIDE_PER_LINE = {"1": 23, "2": 25, "3": 25, "4": 28, "6": 21, "7": 23,
                            "8": 28, "10": 14, "11": 22, "12": 25, "14": 18,
                            "15": 15, "17": 22, "18": 28}
# GATE 3, PARTIAL (owner, 2026-09-30: re-check after the diversion). This map
# is the REGULAR network (owner, 2026-09-30), but DPO runs a diversion
# timetable from 2026-09-17 to about 2026-12-12 - line 6 not running, 13 and 19
# instead - and IDOS's per-stop timetables only accept dates from 2026-09-21.
# Six lines match the diversion timetable stop for stop (IDOS, 2026-10-01,
# both directions) and are counted here. The other eight are open until IDOS
# shows a regular date, about 2026-12-13: 1, 2 and 10 (Don Bosco, which IDOS
# has on no line during the works), 7 (Svinov,mosty, which IDOS's 7 calls at
# and OSM's 7 skips), and 6, 8, 12 and 14 (cut or rerouted by the works).
OPERATOR_STATION_COUNTS = {"Tram 3": 25, "Tram 4": 28, "Tram 11": 22,
                           "Tram 15": 15, "Tram 17": 22, "Tram 18": 28}
OPERATOR_COUNTS_SOURCE = ("IDOS zastávkové jízdní řády, idos.cz/ostrava/zjr, "
                          "2026-10-01, both directions, six lines the diversion "
                          "leaves whole (read 2026-09-30); the other eight open "
                          "until about 2026-12-13")

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

# The wider phone placer (map_common.DENSE_LABEL_SCRIPT), asked for by name.
# Measured live 2026-10-12 at 854 px: Tram 14's tip sits at y 37, under the
# button row (bottom 45), boxed in by Tram 1, 2 and 18, and the clamp's best
# spot left the label 2.1 px under the row. With this placer the label sits
# at y 47 to 68 and none of the 14 overlaps anything. Re-measure if a line is
# added or the button row changes.
DENSE_LABELS = True

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600437354)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("cs",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/ostrava.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A duplicate of one object (owner, 2026-10-13)
    "node/3290624267": "'Mariánské náměstí': second of three tram-stop rows named Mariánské náměstí within 221 m (node/3290624266 kept): one stop, three platform nodes",
    "node/3296974442": "'Mariánské náměstí': third of three tram-stop rows named Mariánské náměstí within 221 m (node/3290624266 kept)",
    "node/3268543065": "'VŠB-TUO': second tram-stop row named VŠB-TUO 151 m from node/660800827: one stop, two platform nodes",
    "node/3304701394": "'Hranečník (St. 5)': Hranečník terminus listed twice, the platform number glued to the name ('St. 5'; 'St. 1' is node/3301463547, about 120 m away)",
    "node/3304701398": "'Nová Huť hlavní brána 2': Nová Huť hlavní brána listed twice with the platform number glued on ('2'; '1' is node/3304701399, about 60 m away)",
    "node/2326099516": "'ZOO Ostrava': the zoo as a node inside the zoo's own outline (way/32949583), both with wikidata Q3562223 and the node's name already the outline's short_name",
    # Worship named only by a body or a denomination (owner, 2026-10-13)
    "node/13587047983": "'Církev Ježíše Krista Svatých posledních dnů': named only by the denomination; its wikidata and wikipedia are the denomination's own (Q42504), not this congregation's; the cached description holds the local name",
    "way/38028785": "'Církev bratrská': named only by the denomination (Church of the Brethren), no congregation or place name",
    "way/52605531": "'Církev československá husitská': named only by the denomination (Czechoslovak Hussite Church), no wikidata",
    # A bare type word (owner, 2026-10-13)
    "way/184549169": "'Kaplička': 'little chapel'; the chapel's own name is only in the cached description; it carries a wikidata id, which may be why the bare-type rule let it through",
    "way/59349272": "'Obecní kaple': 'municipal chapel', a type",
    "way/74404440": "'Multifunkční hala': 'multipurpose hall', a type on a stadium outline",
    "node/11985257476": "'hřbitovní stéla': 'cemetery stele', an object type, no wikidata",
    "node/13208401433": "'dekorativní stěna': 'decorative wall', an object type; carries a wikidata id of the artwork, title equally generic",
    "node/924221483": "'bludný balvan': 'erratic boulder' in lower case; the cached description gives the place; carries a wikidata id",
    # A business (owner, 2026-10-13)
    "node/4228877490": "'PROJEKTSTUDIO': a design firm's name in capitals on a node tagged only historic=monument",
}
