"""Brno-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py, then replaced with the Czech tram
template (`.claude/skills/czech-tram-city/SKILL.md`, section 8).

THE SECOND CZECH CITY AND THE FIRST CZECH TRAM MAP. The national facts - ROS02,
RES, RUIAN, the legal forms, the CRS - live in `pipeline/countries/czechia.py`
and the register chain in `czechia_register.py`, both Prague's. What is Brno's
own is below: the obec, its RUIAN control, KORDIS's tram feed, the OSM line
geometry and the halved rings. The brief is `docs/build_briefs/brno.md`.
"""

from pathlib import Path

SLUG = "brno"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "brno" / "raw"
DATA_PROCESSED = ROOT / "data" / "brno" / "processed"
OUTPUTS = ROOT / "outputs" / "brno"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the obec - line 2's Modřice branch.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# Raw inputs. `fetch_sources.py` downloads them; no step may fetch. ROS02, RES
# and the CZ-NACE codebooks are national (`czechia.SHARED_RAW`); RUIAN is per
# obec; the feed, the tram relations and the boundary are Brno's own.
GTFS_ZIP = DATA_RAW / "gtfs.zip"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_TRAM_JSON = DATA_RAW / "osm_tram.json"

# KORDIS JMK's IDS JMK feed, under KORDIS's own CC BY 4.0 grant (owner,
# 2026-09-30: fetched from kordis-jmk.cz, never data.brno.cz's copy or the stale
# content.idsjmk.cz one). Republished weekly on Sunday; NO feed_info.txt and NO
# shapes.txt, so the fetch records the calendar window and OSM draws the lines.
GTFS_URL = "https://kordis-jmk.cz/gtfs/gtfs.zip"

# --- Scope ---------------------------------------------------------------
#
# Obec 582786, Brno. The businesses are scoped by RUIAN's own address list for
# the obec (ROS02's PKODADM in it), never by a polygon.
SCOPE = "obec"
OBEC_CODES = ["582786"]
RUIAN_ZIPS = {o: DATA_RAW / f"ruian_adr_{o}.csv.zip" for o in OBEC_CODES}
# The RUIAN coordinate control, one per file (czechia_register.ruian()): the
# Nova radnice, Dominikanske namesti 196/1, against the building's published
# coordinates - a source independent of the file. Measured by staging
# 2026-09-30: the file (EPSG:5513) transforms it to 49.19392, 16.60611.
RUIAN_CRS_CONTROLS = {"582786": ("19095597", 49.1936, 16.6069, "Brno New Town Hall")}
# The boundary, for station scope and label anchoring only: OSM relation
# 438171, "Brno", admin_level 8, ref CZ0642582786 (the district code plus the
# RUIAN obec code, which step 1 checks). ~230 km2 by the Czech Statistical
# Office's figure; step 1 gates the polygon on that.
OSM_BOUNDARY_RELATIONS = {"582786": 438171}
BOUNDARY_AREA_KM2 = (225.0, 236.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 33N: Brno's longitude (~16.61 E) falls in the 12-18 band. Derived
# per city, not copied (Ostrava, at 18.29 E, is 34N). RUIAN's S-JTSK is
# converted on read and never used for this city's geometry.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED ON THE SPACING RULE (docs/ring_rules.md): step 1 measured a 336 m
# median nearest-neighbour gap between the 146 stations inside the city
# (2026-09-30; the brief's screen read 329), under the ~550 m line.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------
#
# TRAMS ONLY (owner, 2026-09-29: trams-only maps approved). The feed's
# `route_type 0` AND `route_short_name` in the 11 regular lines. H4 (heritage,
# Komenskeho namesti - Nove sady) and P1 (the Arena Brno event shuttle) run no
# weekday trips and are LEFT OUT (owner, 2026-09-30). Buses, trolleybuses
# (800), the S-trains (rail, 1,974 m median gap) and the ferry are not drawn.
TRAM_SOURCE = "kordis_gtfs"
ROUTE_TYPE_TRAM = "0"
LINE_ORDER = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12"]
LINE_NAMES = {k: f"Tram {k}" for k in LINE_ORDER}
NOT_DRAWN_ROUTES = {"H4": "heritage tram, no weekday trips (owner, 2026-09-30)",
                    "P1": "event shuttle to Arena Brno, no weekday trips (owner, 2026-09-30)"}
# The feed's own route_color (DECISIONS 2026-09-30). All eleven pass
# check_line_colours as published (read 2026-09-30); line 6's 0777C1 is the
# closest to the pins, 13.2 from Retail, recorded rather than moved (Prague's
# line C precedent). OSM's relations carry the same colours.
LINE_COLOURS = {"1": "#D40000", "2": "#4AB95D", "3": "#009E9E", "4": "#EE7E1E",
                "5": "#F31D7F", "6": "#0777C1", "7": "#939DAC", "8": "#E1CB31",
                "9": "#8C4A9A", "10": "#A05A2C", "12": "#00CCFF"}
# The line geometry, from OSM: the feed has no shapes.txt. 26 route=tram
# relations, operator exactly as OSM tags it, all 11 refs (screen, 2026-09-27).
# A line serves a station when it calls there on at least this share of its
# trips in one direction (step 1): Riga's 10%, taken per station. Measured
# 2026-09-30, it drops only the Vozovna Medlánky depot (2-5% on every line), and
# per-line membership then matches OSM's route relations on 9 of 11 lines.
STOP_MIN_SHARE = 0.10
# The station-spacing gate's floor (pipeline/stations.py), for TRAM stops: the
# shared 400 m default is a metro figure, and Brno's stops sit ~330 m apart.
# Riga's and Aarhus's 200 m, which still refuses an uncollapsed platform set
# (Brno's platforms median 42 m).
SPACING_MIN_M = 200.0
OSM_TRAM_OPERATOR = "Dopravní podnik města Brna"
OSM_TRAM_BBOX = (49.10, 16.43, 49.30, 16.73)   # (s, w, n, e)
# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1. Measured
# 2026-09-30 on the build-day feed: 148 stations, 146 inside obec 582786; line 2
# loses its two Modřice stops. A change is a decision re-taken.
EXPECTED_INSIDE_PER_LINE = {"1": 47, "2": 21, "3": 25, "4": 24, "5": 17, "6": 24,
                            "7": 24, "8": 26, "9": 23, "10": 38, "12": 19}
# GATE 3 is OSM's route relations (distinct stop names per ref), a count the
# feed did not make - left empty here so step 1 computes it on the build-day
# OSM file. 2026-09-30: 9 of 11 lines agree exactly. Lines 1 (feed 47, OSM 36)
# and 10 (38 against 27) disagree because OSM carries only their main routes:
# the feed runs line 1 via Tábor and line 10 to Technologický park and Bystrc on
# 12-21% of their trips on every sampled weekday from 2026-10-01 to 12-02, so
# these are the timetable, not a one-off diversion. Recorded, not "fixed".
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = ("OSM route relations, distinct stop names per ref (build day); "
                          "lines 1 and 10 differ, see config")

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "czech_nace2025"
RAW_CLASSIFICATION_COLUMN = "nace2025_label"
CITY_KEEP = "BRNO"   # kept for the scaffold's templates; OBEC_CODES filters
# The national catch-all rule (owner, 2026-09-29): "other personal services",
# exact codes, the bare group too because RES is ragged. 96230 stays.
CATCH_ALL_EXCLUDE = ("96990", "969")   # (owner, 2026-09-29) R2

# Sanity bounds: the placed storefronts' measured extent (49.1289-49.2824 N,
# 16.4579-16.7180 E, step 2, 2026-09-30) plus ~0.02 deg. The join to RUIAN does
# the placing; this catches a CRS or axis error, which the control catches first.
BRNO_BBOX = {
    "lat_min": 49.10,
    "lat_max": 49.31,
    "lon_min": 16.43,
    "lon_max": 16.74,
}

# --- The macro map ---------------------------------------------------------
# The two keys (the macro-legend branch, approved): all three buckets, trams.
MAP_MODE = "tram"
MAP_COVERAGE = "full"
