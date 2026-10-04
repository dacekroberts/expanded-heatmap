"""Brussels (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "brussels_regional" / "raw"
DATA_PROCESSED = ROOT / "data" / "brussels_regional" / "processed"
OUTPUTS = ROOT / "outputs" / "brussels_regional"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. Record the exact download command for each (all public):
# TODO: gtfs.zip - the agency's GTFS feed URL.
# TODO: city_boundary.geojson - a real GIS boundary layer for the city.
# TODO: the business file - endpoint, server-side filter, and snapshot date if
#       the source is a term history (Chicago's AS_OF_DATE is the model).
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "businesses.csv"  # TODO: real file name
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"

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

# --- Business filtering ------------------------------------------------

# TODO: how in-city rows are identified: the dataset's own city field (check
# what it really holds) or an authoritative district field.
CITY_KEEP = "BRUSSELS (REGIONAL)"

TAXONOMY_SYSTEM = "belgium_kbo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "nace_code"

# Sanity bounds for the supplied lat/lng. TODO: tighten to the city's real
# extent once the boundary is known (this box is a wide starting guess).
BRUSSELS_REGIONAL_BBOX = {
    "lat_min": 50.44,
    "lat_max": 51.24,
    "lon_min": 3.87,
    "lon_max": 4.87,
}
