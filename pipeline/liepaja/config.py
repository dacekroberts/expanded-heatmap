"""Liepāja-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. The brief is docs/build_briefs/liepaja.md.

SECOND LATVIAN CITY, on Riga's two layers through the shared
`pipeline/countries/latvia_register.py`:

  * FOOD SERVICE from VID's excise-licence register (Riga's national cache),
    placed on VZD's national address file `aw_eka.csv` - Riga's own address
    points cover Riga only;
  * SHOPS AND SERVICES from VZD's cadastre premise groups of use class 1230
    in ATVK 0005000, placed at the building's footprint.

The classification - the excise columns, the food pattern, the cadastre's
name rules - is Riga's, imported below from `pipeline/riga/config.py`, where
it is decided once for the country.

Rail: the one tram line, from OpenStreetMap through the shared
`pipeline/osm_tram.py` (the city's GTFS declares no licence; brief).
"""

from pathlib import Path

from pipeline.riga.config import (  # noqa: F401 - the country's rules, decided in Riga
    CADASTRE_NS,
    CRS_SOURCE_LV,
    EXCISE_COLUMNS,
    EXCISE_CURRENT,
    EXCISE_NEVER,
    FOOD_RE,
    NAME_KEEP,
    NAME_KIND,
    NAME_RULES,
    TRADE_USE_KIND,
    UNIT_SUFFIX_RE,
)

SLUG = "liepaja"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "liepaja" / "raw"
DATA_PROCESSED = ROOT / "data" / "liepaja" / "processed"
OUTPUTS = ROOT / "outputs" / "liepaja"
# The national excise register and premise groups, as Riga fetched them
# (provenance copied from outputs/riga/provenance.json). Read, never refreshed
# here: a refresh would change Riga's inputs.
NATIONAL_RAW = ROOT / "data" / "riga" / "raw"
NATIONAL_PROVENANCE = ROOT / "outputs" / "riga" / "provenance.json"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs; `fetch_sources.py` downloads them, no step may fetch.
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_CITY_JSON = DATA_RAW / "osm_city.json"
EXCISE_CSV = NATIONAL_RAW / "pdb_akclicences_odata.csv"
PREMISEGROUP_ZIP = NATIONAL_RAW / "premisegroup.zip"
ATVK = "0005000"
KK_ZIP = DATA_RAW / f"{ATVK}_kk_shp.zip"
AW_EKA_CSV = DATA_RAW / "aw_eka.csv"

# data.gov.lv's CKAN; resources are resolved by file name at fetch time.
CKAN_API = "https://data.gov.lv/dati/api/3/action/"
CADASTRAL_MAP_DATASET = "b28f0eed-73b0-4e44-94e7-b04b11bf0b69"
ADDRESS_REGISTER_DATASET = "varis-atvertie-dati"

# --- Scope: the city of Liepāja ------------------------------------------------
# ATVK 0005000; OSM relation 13048685, 68 km2 (brief). The polygon scopes both
# the stations and the businesses (Riga's step 2 keeps rows inside the city).
CITY_NAME_LV = "Liepāja"
OSM_CITY_RELATION = 13048685
CITY_AREA_KM2 = (62.0, 74.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 34N: Liepāja's longitude (~21.0) falls in the 18 to 24 band - NOT
# Riga's 35N (brief). Derived per city.
CRS_PROJECTED = "EPSG:32634"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the brief's 329 m median gap (approved by the owner with the tram
# kit's calls, 2026-09-30). Step 1 prints the median again and stops outside
# MEDIAN_GAP_BOUNDS_M.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (250.0, 450.0)

# --- Station scope: EVERY STOP ------------------------------------------------
# One tram line, ref 1, Mirdzas Ķempes iela - Brīvības iela: two route=tram
# relations, 15 stop names between them (brief, 2026-09-30).
ROUTE = "tram"
OPERATOR = None          # the relations carry no operator tag to whitelist on
LINE_REFS = ("1",)
NOT_DRAWN = {}

# THREE STOPS ADDED BY NODE, giving the screen's 18 (owner, 2026-09-30, call
# approved for "Brīvības iela and Klaipēdas iela"; the build found the third).
# All three lie on the relations' own track (read 2026-09-30); the relations
# are incomplete, not the service:
#   * Brīvības iela, the line's named terminus: a member of both relations as
#     a PLATFORM (node 897590757, also tagged railway=tram_stop); its stop
#     position 14100915105 carries no name;
#   * Klaipēdas iela, between Tukuma iela and Ventas iela: a stop position
#     each way, on neither relation;
#   * Rožu laukums, between Pētertirgus and Koncertzāle: a member of both
#     relations as a PLATFORM each way, with no stop position at all - the
#     screen's 18 counted it, the brief's prose named only the other two.
# osm_tram stops the step if OSM renames one or puts a stop of that name on a
# route.
STATION_ADD = {
    897590757: ("1", "Brīvības iela"),
    4435084037: ("1", "Klaipēdas iela"),
    4435084040: ("1", "Klaipēdas iela"),
    11676327136: ("1", "Rožu laukums"),
    11676327137: ("1", "Rožu laukums"),
}

SPACING_MIN_M = 200.0

DRAWN_LINES = ("1",)
LINE_NAMES = {"1": "Tram 1"}
# OSM records no colour (brief): this project's own, scored at render.
LINE_COLOURS = {"1": "#b8860b"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "riga_source"
RAW_CLASSIFICATION_COLUMN = "activity"

LIEPAJA_BBOX = {"lat_min": 56.44, "lat_max": 56.62, "lon_min": 20.93, "lon_max": 21.13}
