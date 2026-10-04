"""Ghent-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

GHENT, Antwerp's twin: FAVV-AFSCA's operator list placed on Flanders' VKBO
points (`pipeline/countries/belgium_favv.py`) and De Lijn's own GTFS
(`pipeline/countries/belgium_delijn.py`), on Göteborg's page template. The
brief is `docs/build_briefs/ghent.md`.
"""

from pathlib import Path

SLUG = "ghent"

# The macro map's two keys and the scope (the brief's checks compare these).
MAP_MODE = "tram"
MAP_COVERAGE = "one_bucket"
SCOPE = "city"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ghent" / "raw"
DATA_PROCESSED = ROOT / "data" / "ghent" / "processed"
OUTPUTS = ROOT / "outputs" / "ghent"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stops outside the city (drawn with their line, not ringed) with the commune
# each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
TRAM_STOP_TIMES_CSV = DATA_PROCESSED / "tram_stop_times.csv"
LINE_SHAPES_ZIP = DATA_PROCESSED / "tram_shapes.zip"
LINE_SHAPES_JSON = DATA_PROCESSED / "line_shapes.json"

# --- Raw inputs (fetch_sources.py; no step fetches) ------------------------------

# Ghent is NIS 44021, 157.6 km2 as OSM draws it; 12 communes in the box.
COMMUNES_BBOX = (50.97, 3.60, 51.13, 3.86)       # south, west, north, east
OSM_COMMUNES_JSON = DATA_RAW / "osm_communes.json"
OWN_NIS = "44021"
COMMUNE_AREA_KM2 = (150.0, 165.0)

# VKBO, paged for NIS 44021 (no merger touched Ghent in 2025).
VKBO_NIS = ("44021",)
VKBO_CSV = DATA_RAW / "vkbo.csv"
VKBO_META = DATA_RAW / "vkbo.csv.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 31N: the longitude (~3.72) falls in the 0 to 6 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the in-city stations' median nearest-neighbour gap (the owner's
# spacing rule, docs/ring_rules.md). Step 1 stops outside MEDIAN_GAP_BOUNDS_M.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (230.0, 320.0)

# --- Station scope: De Lijn's Ghent trams, every stop in the city ----------------

# T1, T2 and T4: there is no T3 tram in the feed (the brief).
LINES = ("T1", "T2", "T4")
ABSENT_LINES = ("T3",)
# The feed's short names, as the brief's page text writes them ("T1, T2 and
# T4"). Not checked against De Lijn's own line pages (their site is not used:
# private use only).
LINE_NAMES = {ln: ln for ln in LINES}
STUB_MIN_SHARE = 0.5
SPACING_MIN_M = 150.0

# Platform names merged into one station (owner, 2026-10-03), as Antwerp.
PLATFORM_MARKER = r"(?i)(\s+-)?\s+(metro\s+)?perron\s+\S+$|\s+metro$"
PLATFORM_WORDS = r"(?i)\bperron\b|\bmetro\b"
OWN_PREFIX = "Gent "

NAME_ALIASES = {}
# NOT LISTED, AN OPEN CONFLICT: De Lijn's T1 page (2026-10-04) marks Gent
# Bijlokehof "Halte niet bediend" until the works end; the feed passes it
# without stopping through 2026-10-14 and serves it on T1 and T4 every day
# from 2026-10-15 (measured 2026-10-04). It stays ringed until the owner rules.
CLOSED_FOR_WORKS = {}

# GATE 3, PARTIAL, as Antwerp: De Lijn's own count for T1, the whole line.
# Bijlokehof, which the page marks "Halte niet bediend" until the works end,
# is in both figures (the feed serves it from 2026-10-15). A step 1 mismatch
# stops the build.
OPERATOR_STATION_COUNTS = {"T1": 21}
OPERATOR_COUNTS_SOURCE = (
    "De Lijn's line pages (delijn.be/nl/lijnen/<id>/), read 2026-10-04 in a browser by the "
    "Belgium build session, for the count only, never republished: \"Lijn T1\" (T2 and T4 "
    "are \"Lijn T2\" and \"Lijn T4\").")
OPERATOR_COUNTS_GAP = (
    "T2 and T4 not compared: on 2026-10-04 (a Sunday) De Lijn's line pages showed the day's "
    "works-diverted service (T2 7 stops, T4 no trips that day), not the regular route the "
    "feed carries from 2026-10-15.")

# De Lijn's route_color per line (routes.txt, 2026-10-04); step 1 stops if the
# feed moves one. LINE_COLOURS is what is drawn (step 3).
FEED_COLOURS = {"T1": "#FFCC00", "T2": "#15882E", "T4": "#E40521"}
# ONE MOVED, on the brief's check (T1's yellow on the light theme, Lille's
# darkening if it fails): #FFCC00 reads 1.51:1 on the light page. Darkened by
# the smallest HSL lightness step that reads 3:1 there (Sheffield's measure):
# #B28F00, light 3.08:1, dark 6.08:1; CIE76 30.7 from the feed's yellow, 70.5
# from the nearest pin colour (Personal services, which the render measures;
# 87.7 Food service), 58.9 from T2. T2 (#15882E: 25.9 from Personal services,
# 110.8 from the two pin colours this map uses, 4.57:1 light, 4.10:1 dark) and
# T4 (#E40521: 43.5 from Food service, 4.84:1, 3.87:1) keep De Lijn's colours. Antwerp's A3 is the same yellow and is NOT
# moved (its brief names only line 11): an owner call, measured 2026-10-04.
LINE_COLOURS = {**FEED_COLOURS, "T1": "#B28F00"}
LINE_COLOUR_SHIFTS = {"T1": ("#FFCC00", "1.51:1 on the light page; darkened to 3:1, CIE76 30.7")}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "belgium_favv"

# FAVV is selected by postcode; every postcode's `GEM Nom` reads Ghent or one
# of its sections (the brief).
POSTCODES = ("9000", "9030", "9031", "9032", "9040", "9041", "9042", "9050", "9051", "9052")
BORSBEEK_POSTCODE = None

# Sanity bounds (VKBO's real points X 94,726-115,970, Y 186,462-208,371
# Lambert 72) with a margin. The commune polygon does the filtering.
GHENT_BBOX = {
    "lat_min": 50.95,
    "lat_max": 51.20,
    "lon_min": 3.55,
    "lon_max": 3.90,
}
