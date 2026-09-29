"""Buenos Aires settings - Argentina's first city, on a land-use SURVEY rather
than a register (docs/build_briefs/buenos-aires.md).

SCOPE IS CABA, the Ciudad Autónoma: the survey's area, and the whole Subte.

BUSINESSES: the Relevamiento Usos del Suelo 2022-2024 (BA Data), one row per
use observed at an address, classified by `pipeline/taxonomies/ba_usos_suelo.py`.
It carries NO coordinates and NO names; each row is placed at the centroid of
its cadastral parcel, joined on the SMP (section-block-parcel) key to BA Data's
Parcelas layer - a join, not a geocoder (address-join).

RAIL: OpenStreetMap. The city's Subte GTFS on its own CDN ships without a
`routes.txt` (add-country, "a feed that exists and is broken"), and
`osm-rail` records OSM as the ground for exactly that case.

Owner's calls, 2026-09-28: MULTICOMERCIAL (malls, arcades) and "SIN
IDENTIFICAR" shopfronts left out and disclosed; the Premetro left out unless it
covers new areas well (measured before step 1 is final).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "buenos_aires" / "raw"
DATA_PROCESSED = ROOT / "data" / "buenos_aires" / "processed"
OUTPUTS = ROOT / "outputs" / "buenos_aires"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
# Each line's SBASE track dissolved to one geometry; step 1 writes, step 3 reads.
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs -----------------------------------------------------------
#
# FROM THE CDN, NEVER THROUGH THE CKAN API: data.buenosaires.gob.ar's API
# answers the project's user agent with a 245-byte "Request Rejected" page,
# while cdn.buenosaires.gob.ar serves the files to any client (brief, Access
# traps). Both were downloaded 2026-09-28 with the owner's OK.
_CDN = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-de-desarrollo-urbano"
SURVEY_URL = f"{_CDN}/relevamiento-usos-suelo/relevamiento-usos-del-suelo-2022-2024.csv"
PARCELS_URL = f"{_CDN}/parcelas/parcelas_catastrales.csv"
SURVEY_CSV = DATA_RAW / "relevamiento-usos-del-suelo-2022-2024.csv"
PARCELS_CSV = DATA_RAW / "parcelas_catastrales.csv"
SURVEY_SHA256 = "5743336654ff9034a2f54129dd7c89011aa401c151828319b7fa1b06367fa2f1"
PARCELS_SHA256 = "f3debefdaccc02e59f0d417e60531ad95c9adefbe301c91ae9ca39099e5d7019"

# Declared, never inferred (docs/data_sources.md). The survey IS valid UTF-8;
# its accented vowels were damaged before encoding - see ba_usos_suelo.repair.
SOURCE_ENCODING = "utf-8"
SURVEY_YEARS = (2022, 2023, 2024)

# THE RAIL SOURCE: SBASE's own layers (Subterráneos de Buenos Aires, the city
# company that owns the Subte), on BA Data's `subte-estaciones` dataset,
# CC BY 2.5 AR as the survey. Agency GIS layers rank ahead of OSM (osm-rail);
# OSM stays as the cross-check and for the Premetro, which these layers omit.
# Owner's download OK 2026-09-28 (17,133 and 40,850 bytes).
_SBASE = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/sbase/subte-estaciones"
SBASE_STATIONS_URL = f"{_SBASE}/estaciones_de_subte.geojson"
SBASE_LINES_URL = f"{_SBASE}/red_subte.geojson"
SBASE_STATIONS_GEOJSON = DATA_RAW / "estaciones_de_subte.geojson"
SBASE_LINES_GEOJSON = DATA_RAW / "red_subte.geojson"
# As downloaded 2026-09-28 (both last modified 2026-09-01).
SBASE_STATIONS_SHA256 = "e392abf0d923e5ea7cebc1c463f9b7471f062ad22527fb628fe0f480d2f32cc3"
SBASE_LINES_SHA256 = "aef377072b153f7e1093c146b1fa70cf07ae66866f1589bee2180d3041b407ad"

OSM_STATIONS_JSON = DATA_RAW / "osm_stations.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 21S: CABA spans about -58.53 to -58.33, inside the -60 to -54 band,
# south of the equator. Derived per city, never copied.
CRS_PROJECTED = "EPSG:32721"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- OpenStreetMap ----------------------------------------------------------

# south, west, north, east - the brief's CABA bbox.
OSM_BBOX = "-34.71,-58.54,-34.52,-58.33"
OSM_NETWORK = "Subte de Buenos Aires"

# CABA's boundary by RELATION ID, resolved at the screen from
# ["name"="Ciudad Autónoma de Buenos Aires"]["admin_level"="4"] (area id
# 3603082668). Step 1 asserts the name and level it comes back with, so an OSM
# edit that repoints the id fails loudly.
OSM_BOUNDARY_RELATION = 3082668
OSM_BOUNDARY_NAME = "Ciudad Autónoma de Buenos Aires"
OSM_BOUNDARY_ADMIN_LEVEL = "4"

# --- Station scope ----------------------------------------------------------

# The Subte's six lines, OSM `ref` -> public name. OSM's `colour` tags are the
# operator's line colours (A #1CA4CB ... H #F4CC21), checked at the screen.
LINE_NAMES = {
    "A": "Línea A",
    "B": "Línea B",
    "C": "Línea C",
    "D": "Línea D",
    "E": "Línea E",
    "H": "Línea H",
}
LINE_COLOURS = {
    "A": "#1CA4CB",
    "B": "#C20924",
    "C": "#003EA1",
    "D": "#217861",
    "E": "#6B297E",
    "H": "#F4CC21",
}

# THE PREMETRO (OSM `route=tram`, ref P, colour #F38733, same network) is a
# surface light-rail feeder from Línea E. Out unless it covers new areas well
# (owner, 2026-09-28); step 1 counts its relations so a change is seen.
PREMETRO_REF = "P"
DRAW_PREMETRO = False

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "ba_usos_suelo"
RAW_CLASSIFICATION_COLUMN = "TIPO2"

# The survey records uses, not businesses: no name, owner or contact columns
# exist. Step 2 refuses the file if one appears.
FORBIDDEN_COLUMNS = {"nombre", "razon_social", "titular", "cuit", "telefono", "email"}

# Placement: the survey's SMP against Parcelas' `smp`, both with spaces removed
# and upper-cased (the survey writes 039-090-022a; Parcelas spaces it
# differently). Section-block fallback for the rows whose parcel is absent.
SMP_SEPARATOR = "-"

# CABA's extent with a margin; a parcel centroid outside it is a join error.
BUENOS_AIRES_BBOX = {
    "lat_min": -34.71,
    "lat_max": -34.52,
    "lon_min": -58.54,
    "lon_max": -58.33,
}
