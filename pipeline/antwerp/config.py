"""Antwerp-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

ANTWERP, on Göteborg's template (one food register, food service plus food
shops) and Den Haag's precedent for trams in tunnels drawn as `tram`. The
business leg is FAVV-AFSCA's operator list placed on Flanders' VKBO points,
shared with Ghent (`pipeline/countries/belgium_favv.py`); the rail is De
Lijn's own GTFS (`pipeline/countries/belgium_delijn.py`). The brief is
`docs/build_briefs/antwerp.md`.
"""

from pathlib import Path

SLUG = "antwerp"

# The macro map's two keys and the scope (the brief's checks compare these).
MAP_MODE = "tram"
MAP_COVERAGE = "one_bucket"
SCOPE = "city"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "antwerp" / "raw"
DATA_PROCESSED = ROOT / "data" / "antwerp" / "processed"
OUTPUTS = ROOT / "outputs" / "antwerp"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stops outside the city (drawn with their line, not ringed) with the commune
# each lies in, and the stations closed for works.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 1's caches: the city's tram stop_times (keyed on the feed version) and
# the drawn lines' shapes, so step 3 does not parse the 404 MB shapes.txt.
TRAM_STOP_TIMES_CSV = DATA_PROCESSED / "tram_stop_times.csv"
LINE_SHAPES_ZIP = DATA_PROCESSED / "tram_shapes.zip"
LINE_SHAPES_JSON = DATA_PROCESSED / "line_shapes.json"

# --- Raw inputs (fetch_sources.py; no step fetches) ------------------------------

# The communes: every admin_level 8 relation in the rail box, one Overpass
# query (pipeline/countries/belgium_fetch.py, fetch_communes). Antwerp is NIS
# 11002, 208.0 km2 as OSM draws it with Borsbeek (merged 2025-01-01); 24
# communes in the box, so a stop outside can be named.
COMMUNES_BBOX = (51.12, 4.28, 51.34, 4.58)       # south, west, north, east
OSM_COMMUNES_JSON = DATA_RAW / "osm_communes.json"
OWN_NIS = "11002"
COMMUNE_AREA_KM2 = (195.0, 220.0)

# VKBO, paged per NIS code: Antwerp's 11002 AND Borsbeek's old 11007 (the
# brief, 2026-10-03: 1,701 of the 1,876 VKBO rows in postcode 2150 already file
# under 11002, 175 under 11007).
VKBO_NIS = ("11002", "11007")
VKBO_CSV = DATA_RAW / "vkbo.csv"
VKBO_META = DATA_RAW / "vkbo.csv.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 31N: the longitude (~4.40) falls in the 0 to 6 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the in-city stations' median nearest-neighbour gap (the owner's
# spacing rule, docs/ring_rules.md: under about 550 m). Measured at the build
# (2026-10-04): see MEDIAN_GAP_BOUNDS_M, which step 1 stops outside.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (240.0, 330.0)

# --- Station scope: De Lijn's Antwerp trams, every stop in the city --------------

# Lines 3, 5, 9 and 15 are not in the current feed (the works shape, below).
LINES = ("1", "2", "4", "6", "7", "8", "10", "11", "12", "24", "A3", "A9")
# Step 1 stops if any of these returns to the feed as a tram route: the works
# shape has ended, and the closed stations below come back with them.
ABSENT_LINES = ("3", "5", "9", "15")
# "Tram <route_short_name>", Göteborg's form. A3 and A9 are the feed's short
# names (route_long_name "P+R Merksem - P+R Boechout" and "Wijnegem - Berchem
# Station"); what De Lijn calls them in public is not checked (its site is not
# used), so the labels are the lead's to confirm.
LINE_NAMES = {ln: f"Tram {ln}" for ln in LINES}
# No thinning (owner, 2026-10-03; tram-city's standing call).
STUB_MIN_SHARE = 0.5
SPACING_MIN_M = 150.0

# The feed names a station's platforms separately ("... perron 1", "... Metro
# Perron A", "... Metro"): merged into one station by name (owner,
# 2026-10-03). Matched case-insensitively at the end of the name; step 1
# asserts every name carrying a marker word matched.
PLATFORM_MARKER = r"(?i)(\s+-)?\s+(metro\s+)?perron\s+\S+$|\s+metro$"
PLATFORM_WORDS = r"(?i)\bperron\b|\bmetro\b"
# The locality De Lijn prefixes to an Antwerp stop's name, stripped for the
# label (a LEADING prefix, add-city's over-stripping rule); stops elsewhere
# keep theirs.
OWN_PREFIX = "Antwerpen "

# One station under two names: De Lijn files Gasthuishoeve's two platforms
# under two locality prefixes, 5 m apart, both served by 2, 6 and A3
# (measured 2026-10-04). PROVISIONAL, a merge of two differently named stops
# (tram-city section 2 sends it to the owner): without it the map rings one
# station twice.
NAME_ALIASES = {"Antwerpen Gasthuishoeve": "Merksem Gasthuishoeve"}

# CLOSED FOR WORKS (docs/category_rules.md, "Station scope"). Left for the
# lead: De Lijn's reopening date and its reason, from De Lijn's own notice
# (not in the data this build holds; the brief). The reason text below carries
# them once set.
CLOSED_FOR_WORKS_REOPENING = None     # e.g. "2027-03-01", as De Lijn states it
CLOSED_FOR_WORKS_WHY = None           # De Lijn's reason, in a few words
_DUE = (f"due back {CLOSED_FOR_WORKS_REOPENING}" if CLOSED_FOR_WORKS_REOPENING
        else "reopening date not yet read from De Lijn")
_WHY = f" ({CLOSED_FOR_WORKS_WHY})" if CLOSED_FOR_WORKS_WHY else ""
# {stop name as stops.txt writes it: (label, reason)}. Step 1 lists each in
# excluded_stations.csv and STOPS if a passenger can board or alight there
# again. Hoboken Jan Van de Wouwer: the feed names it "(tijdelijk afgeschaft)",
# temporarily discontinued, and every one of its stop_times is pickup 1 and
# drop-off 1 (2, 4, 6, 7 and 8 pass through without stopping; measured
# 2026-10-04 over the feed's window), so no tram serves it.
CLOSED_FOR_WORKS = {
    "Hoboken Jan Van de Wouwer (tijdelijk afgeschaft)": (
        "Hoboken Jan Van de Wouwer",
        f"temporarily discontinued, closed for works{_WHY}: trams pass without stopping; {_DUE}"),
}
# THE LEFT BANK (Linkeroever). Lines 3, 9 and 15 served it and are absent; no
# tram serves any stop there in this feed. The feed cannot say WHICH stops
# were tram stops: the left bank's stops are all still served by buses (104
# of 109 in the box, 2026-10-04), the premetro's left-bank station is not in
# stops.txt, and no replacement route is named. Listing them needs a source
# for the tram stops before the works (OSM's tram route relations, one
# Overpass query, the lead's to send, or De Lijn's notice). Until then step 1
# prints this and lists none.
CLOSED_FOR_WORKS_OPEN_QUESTION = (
    "the left-bank tram stations closed for works (lines 3, 9 and 15) are not listed: the feed "
    "cannot name them. An OSM query for the tram route relations (or De Lijn's notice) is "
    "needed, then each goes in config.CLOSED_FOR_WORKS")

# GATE 3: De Lijn's own per-line stop counts. Its line pages are
# script-rendered (no stop list in the static HTML); the lead reads them in a
# browser later. Until then, the gap is recorded.
OPERATOR_STATION_COUNTS = None
OPERATOR_COUNTS_GAP = (
    "De Lijn's line pages (delijn.be) are script-rendered: their static HTML carries no "
    "stop list (the brief, 2026-10-03). The feed is De Lijn's own data but is this "
    "build's input, so it is not an independent count. Not yet read in a browser "
    "(2026-10-04); the lead reads them later, for the count only, never republished.")
OPERATOR_COUNTS_SOURCE = None

# De Lijn's route_color per line (routes.txt, 2026-10-04); step 1 stops if the
# feed moves one. LINE_COLOURS is what is drawn (step 3).
FEED_COLOURS = {"1": "#8C2B87", "2": "#15882E", "4": "#00A6E2", "6": "#E6007E",
                "7": "#0056A4", "8": "#FC95C5", "10": "#C8D300", "11": "#FFFFFF",
                "12": "#E40521", "24": "#69C0AC", "A3": "#FFCC00", "A9": "#A85E24"}
# ONE MOVED: line 11 is white (#FFFFFF, its text colour #822A3A), 1.00:1 on
# the light page, so the line vanishes there. Darkened by the smallest HSL
# lightness step that reads 3:1 on the light page (Sheffield's measure, the
# brief's "Lille's darkening"): #949494, light 3.03:1, dark 6.17:1; CIE76 38.7
# from the feed's white, 52.1 from the nearest pin colour (Personal services,
# which the render measures though this map has none; 56.9 Food shops, 68.6
# Food service), 32.9 from line 24, the nearest line. The others keep De Lijn's
# colours (Göteborg's precedent), measured 2026-10-04, CIE76 from the nearest
# pin colour as the render prints it / contrast on the light and dark pages:
# 1 41.2 / 7.47, 2.51; 2 25.9 (Personal services) / 4.57, 4.10; 4 31.7 / 2.78,
# 6.73; 6 18.4 / 4.50, 4.16; 7 15.4 / 7.32, 2.56; 8 40.6 / 2.05, 9.13; 10 71.1
# / 1.64, 11.39; 12 43.5 / 4.84, 3.87; 24 25.0 / 2.16, 8.68; A3 88.7 / 1.51,
# 12.38; A9 54.5 / 4.89, 3.83. Closest line pair 27.5 (10 and A3). Under 3:1
# on a page and kept: 4, 8, 10, 24, A3 (light), 1, 7 (dark) - an owner call
# (keep De Lijn's colours, or run scripts/line_colour_search.py as Sheffield
# and Berlin did).
LINE_COLOURS = {**FEED_COLOURS, "11": "#949494"}
LINE_COLOUR_SHIFTS = {"11": ("#FFFFFF", "1.00:1 on the light page; darkened to 3:1, CIE76 38.7")}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "belgium_favv"

# FAVV is selected by postcode: the city's fourteen and Borsbeek's 2150
# (merged 2025-01-01). The city polygon then cuts VKBO's points.
POSTCODES = ("2000", "2018", "2020", "2030", "2040", "2050", "2060", "2100", "2140", "2150",
             "2170", "2180", "2600", "2610", "2660")
BORSBEEK_POSTCODE = "2150"

# Sanity bounds for the placed points: Antwerp's extent (VKBO's real points,
# X 142,832-159,587, Y 189,996-229,745 Lambert 72) with a margin. The commune
# polygon does the filtering; this catches an axis or CRS error.
ANTWERP_BBOX = {
    "lat_min": 51.10,
    "lat_max": 51.40,
    "lon_min": 4.20,
    "lon_max": 4.60,
}
