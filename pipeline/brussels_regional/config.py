"""Brussels (Regional)-specific settings: the 18 communes of the
Brussels-Capital Region outside the City of Brussels.

Companies' establishment units from KBO/BCE Open Data (FPS Economy), placed by
joining their addresses to BeST-Address Brussels (FPS BOSA) and filtered by
four storefront rules: a different method from the City's page (hub.brussels's
street survey), said on the page; the two are never merged. Rail is STIB-MIVB
beyond the City, on the City's shared STIB module. Brief:
docs/build_briefs/brussels_regional.md.
"""

from pathlib import Path

SLUG = "brussels_regional"
# The brief's proposals, checked against app/cities.py by scripts/brief_check.py.
MAP_MODE = "metro"
MAP_COVERAGE = "narrowed"
SCOPE = "regional"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "brussels_regional" / "raw"
DATA_PROCESSED = ROOT / "data" / "brussels_regional" / "processed"
OUTPUTS = ROOT / "outputs" / "brussels_regional"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 2's cached KBO extract (parquet, rebuilt when the KBO zip changes) and
# its measurements.
KBO_EXTRACT_DIR = DATA_PROCESSED / "kbo_extract"
STEP2_REPORT_JSON = DATA_PROCESSED / "step2_report.json"

# Raw inputs. The business leg's two files are shared Belgian caches
# (pipeline/countries/belgium.py: KBO_ZIP, BEST_BRUSSELS_ZIP), verified by
# pipeline/brussels_regional/fetch_sources.py against their meta JSON. KBO is
# placed by the owner (the portal needs the owner's login; a download at least
# yearly, licence 10.5, due by KBO_DOWNLOAD_DUE); BeST may be re-fetched by
# that script's --refresh-best, which means re-running the control.
BEST_URL = "https://opendata.bosa.be/download/best/openaddress-bebru.zip"
KBO_PORTAL = "https://kbopub.economie.fgov.be/kbo-open-data/login?lang=en"
KBO_DOWNLOAD_DUE = "2027-10-02"
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "businesses.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# The control's survey side: hub.brussels's inventory of the City (2025-10-17),
# and the City page's stations for the near-a-City-station count.
HUB_JSON = ROOT / "data" / "brussels" / "raw" / "hub_brussels_commerces.json"
CITY_STATIONS_CSV = ROOT / "data" / "brussels" / "processed" / "stations.csv"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 31N: the longitude (~4.37) falls in the 0 to 6 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32631"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
# HALVED RINGS: the 145 stations kept have a 437 m median nearest-neighbour
# gap (measured 2026-10-04), under the ~550 m line in docs/ring_rules.md (the
# City's rule; its own median is 377 m).
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# STIB-MIVB's whole rail network, read from the City of Brussels page's feed
# (the same download, `pipeline/brussels/fetch_sources.py`; the owner accepted
# the portal's terms for it). Every one of STIB's 22 rail lines serves at least
# one stop in the 18 communes, so all are drawn: metro 1, 2, 5, 6 and 18 tram
# lines. The machinery, its rules and the STIB facts (regular routes, places,
# thinning, bilingual names, gate 3) are the City's, shared through
# pipeline/countries/belgium_stib.py and imported from its config here.
from pipeline.brussels.config import (  # noqa: E402
    COLLAPSE_MAX_SPREAD_M,
    CORRIDOR as CITY_CORRIDOR,
    GTFS_ZIP,
    LINE_SHAPES_JSON as _CITY_LINE_SHAPES_JSON,
    METRO_FEED_COLOURS,
    METRO_LINES,
    METRO_ROUTE_TYPE,
    OPERATOR_COUNTS_SOURCE,
    OPERATOR_STATION_COUNTS,
    PLACE_LINK_M,
    REGULAR_ROUTE_MIN_DAY_SHARE,
    REGULAR_ROUTE_MIN_TRIP_SHARE,
    ROUTE_TYPES_RAIL,
    SPACING_MIN_M,
    STOP_NAME_ALIASES,
    THIN_SPACING_MILES,
)
from pipeline.brussels.config import COMMUNES_GEOJSON, LINE_COLOURS as _CITY_COLOURS  # noqa: E402
from pipeline.brussels.config import TRAM_FEED_COLOURS as _CITY_TRAM_FEED  # noqa: E402

TRAM_LINES = ("4", "7", "8", "9", "10", "18", "19", "25", "35", "39", "44", "51", "55",
              "62", "81", "82", "92", "93")
TRAM_LINES_OUTSIDE = ()
LINE_ORDER = METRO_LINES + TRAM_LINES
LINE_NAMES = {ln: (f"Metro {ln}" if ln in METRO_LINES else f"Tram {ln}") for ln in LINE_ORDER}
LINE_SHAPES_JSON = DATA_PROCESSED / "line_shapes.json"
del _CITY_LINE_SHAPES_JSON

# The City page's colours, and the three trams the City does not draw shifted
# in HSL lightness only to clear Delta-E 13 from every other line (the City's
# rule), measured 2026-10-04: 18 #91bee7 -> #bbd7f0 (L +0.10, the same blue as
# 82), 39 #e43c2e -> #ec7369 (L +0.13, the red of 19 and 92), 44 #f3c300 ->
# #ac8a00 (L -0.14, the yellow of 51).
TRAM_FEED_COLOURS = {**_CITY_TRAM_FEED, "18": "#91bee7", "39": "#e43c2e", "44": "#f3c300"}
LINE_COLOURS = {**_CITY_COLOURS, "18": "#bbd7f0", "39": "#ec7369", "44": "#ac8a00"}

# THE CORRIDOR: STIB's parent stations (`location_type` 1) are exactly the
# underground metro and premetro stations, 70 network-wide (measured
# 2026-10-04). The City's 25 are the Brussels page's, so 45 are this page's.
CORRIDOR_COUNT = 45
# The 18 communes by NIS code: SCOPE_CODES, below with the business filters.
CITY_COMMUNE_CODE = "21004"

# --- Scope: the 18 communes, by NIS code, never by postcode ------------------

# The City's Avenue Louise strip and European quarter carry 1050 and 1040,
# Ixelles's and Etterbeek's postcodes, so a business's key is the matched BeST
# point's municipality_id, checked against the commune polygons and KBO's own
# municipality field (step 2 reports the disagreements).
SCOPE_CODES = {
    "21001": "Anderlecht", "21002": "Auderghem / Oudergem",
    "21003": "Berchem-Sainte-Agathe / Sint-Agatha-Berchem", "21005": "Etterbeek",
    "21006": "Evere", "21007": "Forest / Vorst", "21008": "Ganshoren",
    "21009": "Ixelles / Elsene", "21010": "Jette", "21011": "Koekelberg",
    "21012": "Molenbeek-Saint-Jean / Sint-Jans-Molenbeek", "21013": "Saint-Gilles / Sint-Gillis",
    "21014": "Saint-Josse-ten-Noode / Sint-Joost-ten-Node", "21015": "Schaerbeek / Schaarbeek",
    "21016": "Uccle / Ukkel", "21017": "Watermael-Boitsfort / Watermaal-Bosvoorde",
    "21018": "Woluwe-Saint-Lambert / Sint-Lambrechts-Woluwe",
    "21019": "Woluwe-Saint-Pierre / Sint-Pieters-Woluwe",
}
CITY_POSTCODES = ("1000", "1020", "1120", "1130")
# The Region's postcodes (special ones such as 1099, 1105 and 1110 included):
# the KBO extract keeps establishment addresses in this range.
REGION_POSTCODE_RANGE = (1000, 1299)

# --- Business filtering ------------------------------------------------

CITY_KEEP = "BRUSSELS (REGIONAL)"   # kept for the scaffold's templates; the scope is SCOPE_CODES
TAXONOMY_SYSTEM = "belgium_kbo"
RAW_CLASSIFICATION_COLUMN = "nace_code"

# Personal services is OFF on this page (owner, 2026-10-03, call 12):
# companies only drops most salons (0.47 times the survey's count, 51% recall).
# The bucket priority runs first, so only a personal-only unit leaves.
BUCKETS_OFF = ("Personal services",)

# The four storefront rules (the brief's definitions, exactly).
RULE_B_MIN_UNITS = 5          # companies' units at one address (box ignored), any activity
RULE_B_IN_BUCKET_SHARE = 0.5  # dropped when fewer than half of them are in a bucket
RULE_D_MIN_CODES = 10         # distinct MAIN codes, at least one outside the buckets

# The "other postcode or loose street name" join tier (0.8% in the screen):
# kept only if it holds (step 2 reports the street keys that recur in more
# than one postcode and the tier's agreement with the survey).
KEEP_LOOSE_TIER = True

# The agreement with hub.brussels inside the City (the control).
SURVEY_DATE = "2025-10-17"
MATCH_RADIUS_M = 15.0
# The control must reproduce before any count is trusted (the brief, measured
# 2026-10-03 on extract 501): the join on the City's four postcodes, and the
# agreement after rules A-D (precision, recall) per bucket.
CONTROL_JOIN = {"exact": 88.5, "placed": 97.2}
CONTROL_AGREEMENT = {"Retail": (78.2, 76.1), "Food service": (84.4, 84.0)}
CONTROL_TOLERANCE_PTS = 0.5

# Placed units near a City station but no regional one: the ring's outer edge.
NEAR_CITY_STATION_M = 0.3 * METERS_PER_MILE

# Company or commercial names read as a person's own, withheld (the dot shows
# its activity): KEYS from pipeline/name_keys.py, never the names
# (scripts/check_name_keys.py). Filled after check_personal_exposure.py.
PERSON_NAMED = frozenset()

# The Region's extent (about 4.24-4.48 E, 50.76-50.92 N), padded.
BRUSSELS_REGIONAL_BBOX = {"lat_min": 50.75, "lat_max": 50.93, "lon_min": 4.23, "lon_max": 4.49}
