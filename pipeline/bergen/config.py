"""Bergen-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py, then copied from Oslo's config - the
second Norwegian city, and the first on light rail. The national facts (the
register, its columns, the contact columns never to load, the sole-trader
guard) live in `pipeline/countries/norway.py`; the shared step 2 in
`norway_register.py`. What is Bergen's own is below.

⚠ THREE OSLO SETTINGS ARE NOT COPIED, each of which would fail quietly
(docs/build_briefs/bergen.md): the route type (901, not 401/902 - Oslo's
filter draws nothing here), the UTM zone (31N, not 32N) and the ring edges
(the standard ones, not Oslo's halved edges).
"""

from pathlib import Path

from pipeline.countries.norway import (  # noqa: F401
    ADDRESS_URL_TEMPLATE,
    KOMMUNE_BOUNDARY_URL_TEMPLATE,
)

SLUG = "bergen"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "bergen" / "raw"
DATA_PROCESSED = ROOT / "data" / "bergen" / "processed"
OUTPUTS = ROOT / "outputs" / "bergen"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Every Bybanen station is inside the kommune (the airport included), so this
# file is written empty, with its header - a citable record that none is out.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all public and keyless; `fetch_sources.py` downloads them. The
# two register files are NATIONAL, cached once for the country and SHARED
# with Oslo (`norway.SHARED_RAW`): refreshing them changes Oslo's inputs.
GTFS_ZIP = DATA_RAW / "rb_sky-aggregated-gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
ADDRESS_ZIP = DATA_RAW / "Basisdata_4601_Bergen_4258_MatrikkelenAdresse_CSV.zip"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# Skyss's aggregated GTFS through Entur - the same host and licence (NLOD) as
# Ruter's feed for Oslo. ⚠ A HEAD request is not a probe on Google Storage
# (200, size 0). feed_info.txt names Entur and declares NO validity window, so
# the fetch date pins the snapshot, as Oslo's.
GTFS_URL = ("https://storage.googleapis.com/marduk-production/outbound/gtfs/"
            "rb_sky-aggregated-gtfs.zip")
GTFS_SELF_ATTESTS = False

# Kommune 4601 - Bergen (Vestland). Kartverket's own boundary. Not the
# business filter - that is the sub-unit's own beliggenhetsadresse.kommunenummer.
KOMMUNE_NUMBER = "4601"
KOMMUNE_NAME = "Bergen"
BOUNDARY_URL = KOMMUNE_BOUNDARY_URL_TEMPLATE.format(code=KOMMUNE_NUMBER)
ADDRESS_URL = ADDRESS_URL_TEMPLATE.format(code=KOMMUNE_NUMBER, name=KOMMUNE_NAME)

# No Bybanen station lies outside the kommune (the brief, measured
# 2026-09-29). Step 1 still EXITS if one ever does, naming it.
NEIGHBOUR_KOMMUNER = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM 31N. Bergen's stations lie at 5.23-5.36 E, in zone 31 (0-6 E).
# NOT Oslo's 25832, and not Norway's national UTM 33 - derived per city.
CRS_PROJECTED = "EPSG:25831"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# THE STANDARD EDGES, by the spacing rule (docs/ring_rules.md): the collapsed
# stations' median nearest-neighbour gap is 624 m, over the ~550 m line.
# Oslo's halved edges (465 m median) are NOT Bergen's.
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Bybanen, both lines: route_type 901 (EXTENDED - a basic-type reader, or
# Oslo's 401/902 filter, sees no rail at all). Ferries (1004, 1008) are not
# drawn, Oslo's and Marseille's call.
ROUTE_TYPES_RAIL = ("901",)
ROUTE_IDS = ["SKY:Line:1", "SKY:Line:2"]

# GATE 3 - NOT RUN, recorded as such. No published per-line count was found:
# English and Norwegian Wikipedia (read 2026-09-29) give 35 stops for the
# network and no split by line, against the feed's 34 stop places and 33
# names (Bergen busstasjon is two stop places 70 m apart). A number that does
# not match is not a gate, and none is invented to fit (Goyang's precedent
# for a line whose published count does not reconcile).
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = (
    "none usable: Wikipedia (en, no) gives 35 stops network-wide, no per-line "
    "split, against the feed's 34 stop places / 33 names - read 2026-09-29")

# ONE STATION UNDER TWO NAMES - none. The three pairs under 300 m were read at
# the build (the brief's table): Byparken / Kaigaten (73 m) are the two lines'
# city termini, distinct named stops served by different lines, and stay two
# (the brief's lean; Oslo kept Stortinget / Stortorvet at 142 m as two);
# Nesttun sentrum / Nesttun terminal (254 m) and Bergen busstasjon /
# Nonneseter (258 m) are distinct stops.
STATION_NAME_ALIASES = {}

SPACING_MIN_M = 400.0

# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope is
# checkable. Counted after step 1's name collapse.
EXPECTED_INSIDE_PER_LINE = {"1": 28, "2": 10}

# route_short_name -> the name riders use. The feed's names are bare numbers;
# the mode word goes with them, as Oslo's "T-bane 1".
LINE_NAMES = {"1": "Bybanen 1", "2": "Bybanen 2"}

# ⚠ NEITHER SOURCE TELLS THE LINES APART: the feed has no route_color, and
# OSM's four route relations (7271947, 7271948, 14933911, 14933918) carry one
# colour for both, #BF4525. Line 1 keeps it; Line 2 takes a colour of this
# project's choosing that clears pipeline/linecolour.py (Oslo's Trikk 15 and
# Dublin's precedent for a line with no published colour). No "Skyss colour"
# is claimed for Line 2.
# Line 2's #9c27b0 was chosen 2026-09-29 on the measure: worst pin 55.2
# (Retail), 93.6 from Line 1, 98 from the heat ramp. Oslo's teal #00a3a8 sat
# at 34.0 from Personal services and was not taken. Line 1's #bf4525 is 40.8
# from Food service: OSM's colour, below the preferred 45, recorded.
LINE_COLOURS = {"1": "#bf4525", "2": "#9c27b0"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "norway_sn2025"
RAW_CLASSIFICATION_COLUMN = "sn2025_label"
CITY_KEEP = "BERGEN"   # kept for the scaffold's templates; KOMMUNE_NUMBER filters

# The per-city catch-all verdict, on Bergen's own numbers (the screen,
# 2026-09-27): 96.990 "Andre personlige tjenester ikke nevnt annet sted" is
# 7.0% of storefronts, 83% sole traders, 8% with employees (Oslo 87% / 5%) -
# the home-based signature, dropped as in Oslo. The five retail catch-alls are
# kept, as in Oslo.
CATCH_ALL_EXCLUDE = ("96.990",)

# Sanity bounds: kommune 4601's avgrensningsboks (60.176-60.536 N,
# 5.145-5.687 E, Kartverket's kommuneinfo) plus ~0.02 deg.
BERGEN_BBOX = {
    "lat_min": 60.15,
    "lat_max": 60.56,
    "lon_min": 5.12,
    "lon_max": 5.71,
}
