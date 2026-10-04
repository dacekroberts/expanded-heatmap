"""Charleroi-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

CHARLEROI, the Ville (INS 52011), on two shared Belgian modules: the light
metro from TEC's own GTFS (`pipeline/countries/belgium_tec.py`) and the shops
and horeca premises from Wallonia's LoGIC 2024 survey
(`pipeline/countries/belgium_logic.py`), shared with Liege. Two categories,
Retail and Food service (`narrowed`, "Two"; LoGIC's services class is a
catch-all and left out). The brief: docs/build_briefs/charleroi.md.
"""

from pathlib import Path

from pipeline.countries import belgium_tec

SLUG = "charleroi"
NAME = "Charleroi"
FETCH = "pipeline/charleroi/fetch_sources.py"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "charleroi" / "raw"
DATA_PROCESSED = ROOT / "data" / "charleroi" / "processed"
OUTPUTS = ROOT / "outputs" / "charleroi"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# M2's stops in Fontaine-l'Eveque and Anderlues: drawn with the line, not
# ringed, listed here with the commune each lies in (owner, 2026-10-03,
# Belgium build call 7).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# The owner's "measure first" (2026-10-03): LoGIC's perimeters against the
# station rings, written by step 2.
COVERAGE_JSON = DATA_PROCESSED / "logic_coverage.json"

# --- Raw inputs (fetch_sources.py installs or verifies; no step fetches) ---

# TEC's feed, one copy for both Walloon cities (data/belgium/raw/).
GTFS_ZIP = belgium_tec.FEED_ZIP
# Every municipality in the rail box, from OpenStreetMap (admin_level 8,
# ref:INS), cached by the lead's run of fetch_communes on 2026-10-04: 22
# communes, Charleroi's polygon 102.8 km2.
OSM_COMMUNES_JSON = DATA_RAW / "osm_communes.json"
COMMUNE_BBOX = (50.36, 4.22, 50.51, 4.56)          # south, west, north, east
NIS = "52011"
COMMUNE_AREA_KM2 = (95.0, 110.0)                   # the OSM polygon: 102.8 km2
# LoGIC's INS for the city (the same NIS code, read as an integer).
LOGIC_INS = 52011

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 31N: the longitude (~4.44) falls in the 0 to 6 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson. LoGIC's EPSG:3812
# is reprojected to it.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the owner's spacing rule (about 550 m or less): the in-commune
# stations' median nearest-neighbour gap is 385 m (step 1, 2026-10-04: 38
# stations; 403 m over all 48). Step 1 stops outside the bounds below.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (330.0, 450.0)

# --- Station scope: the light metro, M2, M3 and M4 ----------------------------
#
# TEC's feed types M2-M4 `route_type` 1. `mode` is `light_rail` (owner,
# 2026-10-03, Belgium build call 3): a tunnel and viaduct core with
# street-running branches, Edmonton's and Pittsburgh's shape. M1 is not a metro
# route in the feed (2026-10-04): `M1ab`, `M3ab` and `M4ab` are buses
# (route_type 3) and are not drawn. M5 (to Chatelet) is under construction.
# Matched on route_short_name: TEC's route_ids carry a version suffix
# ("gr:tec:C00M2-23368"), Calgary's trap.
ROUTE_TYPE = "1"
LINES = ("M2", "M3", "M4")
# The bare public line names (the owner's open ruling on the TEC name keeps
# the operator's name out of every label until it lands).
LINE_NAMES = {"M2": "M2", "M3": "M3", "M4": "M4"}
# Daytime (09-16) headways read on this Tuesday; the light-rail 15-minute test
# (docs/category_rules.md, "Station scope") is on the median gap: M2 every 15
# (one 16-minute gap), M3 and M4 every 10 (2026-10-04).
HEADWAY_DAY = "20261013"
HEADWAY_MAX_MIN = 15.0

# Display names are the child stops' own names without TEC's upper-case
# locality prefix and "(M)" suffix ("CHARLEROI Janson (M)" -> "Janson"). Two
# parents carry one name, Tirou's two platforms ("CHARLEROI Tirou" and
# "CHARLEROI Tirou (M)", one per direction): merged into one station (owner,
# 2026-10-03, Belgium build call 5's merge rule). Gare Centrale's two quays
# share one parent in this feed, so they collapse on parent_station alone.
NAME_ALIASES = {}
MERGED_NAMES = ("Tirou",)
COLLAPSE_MAX_SPREAD_M = 250.0
# One parent whose two platforms stand apart on the street-running Anderlues
# branch: Surschiste, 383 m (TEC's own parent_station; in Fontaine-l'Eveque,
# outside the commune, so drawn and not ringed). Measured 2026-10-04.
COLLAPSE_SPREAD_ALLOWED = {"Surschiste": 400.0}
SPACING_MIN_M = 100.0

# Gate 3: NO COUNT. The operator's site answers every path with a challenge
# page (staging's licence read, 2026-10-04), which this project does not get
# past. fr.wikipedia's "Métro léger de Charleroi" (read 2026-10-04) gives M1 25,
# M2 25, M3 28, M4 15, on a different convention (the central loop counted
# into each line, and Villette, closed for good, still listed), so it cannot
# check the feed's whole-line counts (M2 23, M3 26, M4 9 by name).
OPERATOR_STATION_COUNTS = None
OPERATOR_COUNTS_GAP = (
    "the operator's line pages refuse scripted and browser reads (a challenge page, "
    "2026-10-04); fr.wikipedia's per-line counts (M2 25, M3 28, M4 15, read 2026-10-04) "
    "count the central loop into each line and list the closed Villette, so they do not "
    "compare with the feed's whole lines (M2 23, M3 26, M4 9).")

# Each line's drawn shapes, picked by step 1 (belgium_tec.line_shapes, France's
# rule: shapes by trips, one added only where it reaches stations the others
# miss). M3 needs two: its Gosselies loop runs one way round (Leopold,
# Calvaire, Bruyerre outbound; Rue du Chemin de Fer, Emailleries, City Nord,
# Chaussee de Fleurus inbound). Step 1 stops if the pick changes.
LINE_SHAPES = {
    "M2": ("gw:tec:C00M20067",),
    "M3": ("gw:tec:C00M30072", "gw:tec:C00M30074"),
    "M4": ("gw:tec:C00M40038",),
}
# THE PROJECT'S OWN PALETTE (owner, 2026-10-03, Belgium build call 8): the
# feed gives M2, M3 and M4 one route_color, #FFCD00, and two lines in one
# colour are refused (Dijon). Measured with pipeline/linecolour.py (CIE76,
# 2026-10-04), nearest pin: M2 orange 72.2 (Food service), M3 deep purple 47.1
# (Retail), M4 dark brown 55.7 (Food service); the closest pair of lines is M3
# and M4 at 75.8. Riga's, Daugavpils's and Den Haag's palette colours.
LINE_COLOURS = {"M2": "#ff7f0e", "M3": "#4a148c", "M4": "#5d4037"}
FEED_ROUTE_COLOR = "FFCD00"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "wallonia_logic"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "NATURE"
# Scope is LoGIC's INS; the OSM commune polygon checks it. A point with the
# city's INS further than this outside the polygon stops step 2.
POLYGON_TOLERANCE_M = 100.0

# SIGNS READ AS A PERSON'S OWN NAME, withheld: the pin shows its NATURE class
# instead (owner, 2026-10-03, Belgium build call 10). Keys, never names
# (pipeline/name_keys.py). Proposed by belgium_logic.person_sign (two or three
# words, a given name or an initial at one end, no trade word) on the retail
# and horeca rows, less any sign found at two or more points in Wallonia (a
# brand); 33 rows, 2026-10-04. NOT READ BY EYE: the build agent was told never
# to print a suspect sign. Regenerate with
#   python -m pipeline.countries.belgium_logic --person-keys 52011
# Step 2 stops if a key no longer matches, or if the shape test proposes a
# sign not listed here.
PERSON_NAMED = (
    "0fa0b6fc4b139715", "1275f782fd4f2772", "14d07f1dada9eb5d", "1522db5834cffd15",
    "23ffa4bc35d5d0cb", "244ecc064dd3f0a0", "31d642e7950a4df2", "3c98607ffad65bae",
    "40266fc06335ff7c", "48e204c53fb52602", "4a66cdefe6e3ef5f", "60086354f28752ea",
    "64834eaf079f4928", "651f248494b76531", "67d2b6554a20d484", "71187b5137c2db28",
    "813af2e6de011a28", "89ff7a5e7b669ea7", "8e04d321a57f1993", "915c4962dcba1db2",
    "9d13f12eb0de2d26", "9f3e515a17240603", "a1792dda01988497", "a81a3c1b1a96902c",
    "a89e3b7dff7b76d5", "aea92861c60c738a", "b3af5fa88df211e8", "b62033f7fb729bcd",
    "bd45f5dcebef4068", "c0a85f0ab1c90432", "deea162fc897fce7", "e1620ae3cfee0716",
    "e2c8f2b6db6a020d",
)

# Sanity bounds for the points: the commune plus a margin.
CHARLEROI_BBOX = {
    "lat_min": 50.33,
    "lat_max": 50.53,
    "lon_min": 4.30,
    "lon_max": 4.58,
}
