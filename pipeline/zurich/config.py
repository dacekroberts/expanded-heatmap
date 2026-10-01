"""Zurich-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

ZURICH, the project's first Swiss city, on Stockholm's template (one city
register, the city only) with Seoul's and Gyeonggi's precedent for a partial
retail layer, and the shared `pipeline/osm_tram.py` (the tram-city skill). The
business leg is the Stadt Zürich's `Gastwirtschaftsbetriebe` register (CC0),
read through the city's WFS: food service, plus the shops, kiosks and petrol
stations licensed to sell alcohol (owner, 2026-09-30). No personal services.
Rail from OpenStreetMap: VBZ's trams.
"""

from pathlib import Path

SLUG = "zurich"

# What the brief's checks compare with (`brief_check.py zurich --vs-config`).
MAP_MODE = "tram"
MAP_COVERAGE = "narrowed"
SCOPE = "city"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "zurich" / "raw"
DATA_PROCESSED = ROOT / "data" / "zurich" / "processed"
OUTPUTS = ROOT / "outputs" / "zurich"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stops of drawn lines outside the Stadt (tram 2 in Schlieren, tram 10 in
# Opfikon and Kloten): drawn, not ringed, listed with the Gemeinde each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# The Stadt Zürich's Gastwirtschaftsbetriebe (Stadtpolizei, Fachgruppe
# Bewilligung Gastro; Open Data Zürich, CC0). THE WFS, NOT THE CKAN DOWNLOADS:
# every CKAN resource URL (`stadt-zuerich.ch/geodaten/download/...?format=`)
# returns a 35 KB Angular page, not data (the brief, re-checked 2026-09-30).
# The layer name is lower-case. GeoJSON output carries WGS84 points plus the
# register's own LV95 `ekoord`/`nkoord`.
WFS_URL = "https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Gastwirtschaftsbetriebe"
WFS_LAYER = "gastwirtschaftsbetriebe"
WFS_PARAMS = {"SERVICE": "WFS", "VERSION": "1.1.0", "REQUEST": "GetFeature",
              "typeName": WFS_LAYER, "outputFormat": "application/vnd.geo+json"}
CKAN_PACKAGE = "https://data.stadt-zuerich.ch/api/3/action/package_show?id=geo_gastwirtschaftsbetriebe"
REGISTER_JSON = DATA_RAW / "gastwirtschaftsbetriebe.geojson"
# 3,487 rows on 2026-09-30; a fetch far below it is a failed fetch.
REGISTER_MIN_ROWS = 3000
# The register's own columns, asserted at fetch and at step 2: a renamed or
# dropped column stops the build rather than reading as empty.
REGISTER_COLUMNS = {
    "objectid", "betriebsname", "betriebsart", "betriebsstatus", "jahr", "strasselang",
    "hnr", "plz", "ort", "ekoord", "nkoord", "kreislang", "kreissort", "quarlang",
    "quarsort", "statzonelang", "statzonesort", "oeffnungszeit", "geometrie_gdo",
}

# OSM: every tram and light-rail relation in the network's box, and the
# Gemeinden around it (admin_level 8), one query each, one at a time.
RAIL_BBOX = (47.32, 8.40, 47.47, 8.65)          # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_GEMEINDEN_JSON = DATA_RAW / "osm_gemeinden.json"
# Stadt Zürich: OSM relation 1682248, BFS number 261. The other Gemeinden in
# the box only name where an outside stop lies.
ZURICH_RELATION = 1682248
BFS_ZURICH = "261"
BFS_TAG = "swisstopo:BFS_NUMMER"
CITY_AREA_KM2 = (85.0, 95.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# CH1903+ / LV95, in metres: Switzerland's own grid, and the register's
# `ekoord`/`nkoord` are already in it (the tram-city skill, section 3, which
# overrides the scaffold's UTM 32N for Zurich).
CRS_PROJECTED = "EPSG:2056"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the brief's 283 m median gap among the in-city stops (the owner's
# spacing rule; recomputed at the build on the stops drawn). Step 1 prints the
# median and stops outside 240-330 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (240.0, 330.0)

# --- Station scope: VBZ's city trams, every stop in the Stadt -----------------
#
# Step 1 judges every `route=tram` and `route=light_rail` relation in the box:
# kept on its ref, or named in NOT_DRAWN with a reason (osm_tram's contract).
# Each kept line's stops are the union of its relations. The short and variant
# runs of trams 9 (the weekday-peak run on to Triemli) and 8 (the Sunday run to
# the Zoo) add no stop of their own: every stop on them is also on the line's
# everyday run (measured 2026-09-30). TRAM 10'S OERLIKON SHORT RUNS DO ADD ONE:
# their relations (10412927, 10412930: Bahnhofstrasse/HB <-> Bahnhof Oerlikon)
# end at Bahnhof Oerlikon, a stop the everyday runs (53006, 2799184) do not
# call at and ZVV's line 10 does not list (2026-10-01). LINE_NOT_AT below
# takes 10 off that station; it stays drawn and ringed for tram 50.
#
# TRAMS 50 AND 51 ARE THE 2026 TIMETABLE'S CONSTRUCTION LINES (VBZ: 14 Dec 2025
# to 12 Dec 2026, while the Bahnhofquai/HB stop is rebuilt). 50 replaces the
# northern halves of 11 and 13 (Frankental - Auzelg), 51 those of 4 and 14
# (Altstetten Nord - Seebach), so 4, 11, 13 and 14 run shortened this year and
# 50 and 51 are the only trams at their outer stops. Drawn under call 2's
# 20-minute floor: they stand in for four all-day lines, and Transit's published
# VBZ timetable shows trips every 15 minutes (read 2026-09-30; a secondary
# source - VBZ's own pages read gave no headway). When the Bahnhofquai reopens the
# lines change back and this map must be rebuilt: step 1 stops when OSM
# drops refs 50 and 51 (a kept ref with no relation exits).
ROUTES = ("tram", "light_rail")
OPERATOR = None
LINE_REFS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "13", "14", "15", "17",
             "50", "51")
_STUB12 = ("Glattalbahn: 1 of its 18 stops in the Stadt (Auzelg, also on tram 50; the "
           "brief's screen counted 2); left out as a stub (owner, call 19)")
_STUB20 = ("Limmattalbahn, operated by AVA: 4 of its 26 stops in the Stadt; left out as a "
           "stub (owner, call 25). Farbhof and Micafil are also on tram 2; Bahnhof "
           "Altstetten and Seidelhof are on no drawn line and get no ring")
_S18 = ("Forchbahn S18 (route=light_rail), a suburban railway: 4 of its 20 stops in the "
        "Stadt (Bahnhof Stadelhofen, Kreuzplatz, Hegibachplatz, Balgrist), every one also "
        "a drawn tram stop; left out and named on the page (owner, call 18)")
NOT_DRAWN = {
    1299849: "Tram 12 Flughafen - Stettbach. " + _STUB12,
    2799200: "Tram 12 Stettbach - Flughafen. " + _STUB12,
    14987051: "Tram 20 Killwangen - Altstetten. " + _STUB20,
    14987052: "Tram 20 Altstetten - Killwangen. " + _STUB20,
    2727252: "S18 Stadelhofen - Esslingen. " + _S18,
    2727409: "S18 Esslingen - Stadelhofen. " + _S18,
    20153407: "S18 Forch - Stadelhofen. " + _S18,
    20153408: "S18 Stadelhofen - Forch. " + _S18,
}
STATION_ADD = {}
NAME_ALIASES = {}
# {stop name: (line, ...)}: a line OSM puts at a stop the operator's own
# timetable does not list there. Step 1 drops those (line, stop) rows before
# the collapse, and stops if the name is gone, if the line no longer lists it
# (a stale entry), or if a stop position would be lost with them (the station
# would move). Bahnhof Oerlikon: only tram 10's short runs reach it; its stop
# positions are tram 50's (node 4881603356 is on both), so the point stays put
# (owner, "implement the station fixes", 2026-10-01).
LINE_NOT_AT = {"Bahnhof Oerlikon": ("10",)}
# The build of 2026-09-30: 195 stop names, 180 in the Stadt, 15 outside (tram 2's
# six in Schlieren; tram 10's in Opfikon, Kloten and Rümlang; tram 50's two in
# Opfikon; tram 4's Rehalp in Zollikon).
EXPECTED_IN_CITY = 180
EXPECTED_OUTSIDE = 15

# Gate 3: the stops of each line in ZVV's Linienfahrplan (the Zürcher
# Verkehrsverbund's official line timetable for VBZ's trams, both directions,
# by stop number), the whole line before the Stadt split (2's Schlieren and
# 10's Opfikon, Kloten and Rümlang stops included). 50 AND 51 ARE COUNTED FOR
# THE CURRENT TIMETABLE PERIOD ONLY (14 Dec 2025 to 12 Dec 2026), as are the
# shortened 4, 11, 13 and 14 they stand in for: re-read every figure when the
# Bahnhofquai reopens. A tram step 1 stops on a mismatch.
OPERATOR_STATION_COUNTS = {
    "2": 30, "3": 21, "4": 16, "5": 12, "6": 11, "7": 31, "8": 27, "9": 34,
    # 28 once LINE_NOT_AT takes 10 off Bahnhof Oerlikon (OSM's short runs
    # gave the build 29; fixed 2026-10-01).
    "10": 28,
    "11": 14, "13": 13, "14": 12, "15": 13, "17": 21,
    "50": 33,   # temporary construction line, current timetable period only
    "51": 27,   # temporary construction line, current timetable period only
}
OPERATOR_COUNTS_SOURCE = (
    "ZVV, 'Haltestellen- und Linienfahrpläne', Jahresfahrplan 2026 (valid "
    "2025-12-14 to 2026-12-12): https://online.fahrplaninfo.zvv.ch/frame_linie3.php"
    "?lang=de&sel_linie=|010<nn>|<n>&sel_gk=<per line>, read 2026-10-01. ZVV is the "
    "public transport authority that publishes VBZ's timetable.")

SPACING_MIN_M = 80.0
# One name, one stop: osm_tram's 200 m collapse limit, widened for ONE stop.
# Waffenplatzstrasse (trams 5 and 13) has its two directions' stop positions
# 233 m apart, both carrying the one stop code (uic_ref 8591415, read
# 2026-09-30); the next widest is Haldenegg at 168 m.
MAX_SPREAD_M = 240

DRAWN_LINES = LINE_REFS
LINE_NAMES = {ref: f"Tram {ref}" for ref in LINE_REFS}
# OSM's `colour` (VBZ's own) on every relation, except where two drawn lines
# share one or a line sits on its pins (pipeline/linecolour.py, measured
# 2026-09-30). VBZ gives 2 and 15 one red, 3 and 11 one green, 4 and 9 one
# violet, and 7, 50 and 51 black: two lines with one colour are refused (Dijon),
# so the lower number keeps VBZ's colour and the other moves (Den Haag's rule,
# "one moves"): 15 lighter red, 11 darker green, 9 a lighter violet, 50 and 51
# two greys beside 7's black. Tram 10's magenta (#CE1F75) is Delta-E 11.9 from
# the Food service pins and is darkened to 20.2 (Seoul's line 8, Toronto).
# Tram 7's pure black is drawn #262626: `linecolour.dark_label` moves a colour
# darker than the dark page's halo darker still, so #000000 can never reach
# 4.5:1 and the render raises (London drew the Northern's black as a grey).
LINE_COLOURS = {
    "2": "#CB0A25", "3": "#00923C", "4": "#322E71", "5": "#70492C", "6": "#BE8543",
    "7": "#262626", "8": "#8BC036", "9": "#8A4FA8", "10": "#8E1450", "11": "#005A25",
    "13": "#F6C828", "14": "#0093D0", "15": "#F07A86", "17": "#8D1D2C", "50": "#4D4D4D",
    "51": "#858585",
}
# VBZ's colours as OSM records them, which step 3 asserts are still OSM's, so
# a recolouring in OSM is seen rather than overridden silently.
OSM_COLOURS = {
    "2": "#CB0A25", "3": "#00923C", "4": "#322E71", "5": "#70492C", "6": "#BE8543",
    "7": "#000000", "8": "#8BC036", "9": "#322E71", "10": "#CE1F75", "11": "#00923C",
    "13": "#F6C828", "14": "#0093D0", "15": "#CB0A25", "17": "#8D1D2C", "50": "#000000",
    "51": "#000000",
}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "zurich_gastwirtschaft"
RAW_CLASSIFICATION_COLUMN = "betriebsart"

# Trade names that are a person's own name: the dot shows the street address
# instead (Kansas City's and New Orleans's rule). Read by eye on 2026-09-30
# from the 914 shown names residence.py reads as a person's (its organisation
# words are English, so most are German or Italian trade names: "Brasserie
# Lipp", "Tennisclub Seebach") and the 176 kiosk and shop names. Ambiguous
# names are listed, which only shows an address in place of a name. Four are
# alcohol-retail licences in a bare personal name on residential streets
# (Austrasse, Schönbühlstrasse, Siewerdtstrasse, Zelglistrasse); one is an
# internet shop in a person's name; one names its holder after the trade
# name. Kiosk names that carry a surname beside a trade word ("Prathees Kiosk",
# "Velauthapillai Sathiyamohan Kiosk") are the sign over a kiosk, not a home,
# and stay.
PERSON_NAMED = (
    "A. Sorkine Hornung Internetshop", "City Golf Shop / Oskar Kübli", "Danai Ioannidou",
    "Don Weber", "Hans Jaeger", "Henri Maillardet", "JAI Paramalingam", "John Reed",
    "Marco Lanter", "Markus Forster", "Seebach Vanithanathan", "Xisto Macedo",
)

# Sanity bounds for the placed points: the Stadt plus a margin.
ZURICH_BBOX = {
    "lat_min": 47.31,
    "lat_max": 47.44,
    "lon_min": 8.44,
    "lon_max": 8.63,
}
