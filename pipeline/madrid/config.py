"""Madrid-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Step 0's evidence is in `docs/build_briefs/madrid.md` and the country profile
in `docs/spain_step0_endpoints.md`; re-run `python scripts/brief_check.py
madrid` before trusting any number here.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "madrid" / "raw"
DATA_PROCESSED = ROOT / "data" / "madrid" / "processed"
OUTPUTS = ROOT / "outputs" / "madrid"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
LINE_SHAPES_GEOJSON = DATA_PROCESSED / "line_shapes.geojson"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs ------------------------------------------------------------
#
# NO GTFS. Madrid is the first city here whose rail comes from the operator's
# ArcGIS feature services rather than a feed, and the reason is a licence
# condition rather than a preference: CRTM stopped refreshing its Metro GTFS in
# May 2025 while its licence obliges a reuser to keep displayed information
# "siempre actualizada". The feature services carry the same network and ARE
# maintained (last edited 2026-06-05). See docs/build_briefs/madrid.md, which
# records the decision, and spain_step0_endpoints.md for the measurements.
CRTM_METRO_SERVICE = (
    "https://services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services"
    "/M4_Red/FeatureServer"
)
CRTM_STATIONS_LAYER = 0   # M4_Estaciones - 293 point records
CRTM_TRAMOS_LAYER = 4     # M4_Tramos    - 560 polyline records
STATIONS_RAW_JSON = DATA_RAW / "crtm_m4_estaciones.json"
TRAMOS_RAW_JSON = DATA_RAW / "crtm_m4_tramos.json"

# THE BUSINESS DOWNLOAD URL ROTS - it embeds a build timestamp
# (`200085_20260922_053829.csv`) that changes on every refresh, so it is
# resolved at fetch time from package_show by RESOURCE ID, which is stable.
# This is the first source in the project whose URL is not durable; a hardcoded
# one 404s silently within days.
BUSINESSES_CKAN_PACKAGE = "200085-0-censo-locales"
BUSINESSES_CKAN_RESOURCE = "200085-5-censo-locales"   # locales x actividades
BUSINESSES_CKAN_API = "https://datos.madrid.es/api/3/action/package_show"
BUSINESSES_RAW_CSV = DATA_RAW / "censo_locales_200085-5.csv"

# Declared, never inferred - the file is UTF-8 WITH BOM and semicolon
# delimited, and a BOM read as data corrupts the first column name.
SOURCE_ENCODING = "utf-8-sig"
SOURCE_DELIMITER = ";"

CITY_BOUNDARY_ZIP = DATA_RAW / "termino_municipal.zip"
CITY_BOUNDARY_URL = (
    "https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL"
    "/LIMITES_ADMINISTRATIVOS/Termino_Municipal/Termino_Municipal.zip"
)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# EPSG:25830 - ETRS89 / UTM zone 30N. Madrid's longitude (~-3.70) falls in the
# -6..0 band, so the zone is 30N, derived rather than copied.
#
# THE ETRS89 FLAVOUR, NOT THE WGS84 ONE (32630), and deliberately: this is the
# CRS the premises register, the CRTM rail layers and the city's boundary are
# ALL published in, so the whole build shares one projection and the pipeline
# never reprojects for geometry - only for display. It is metres, so the
# project's never-measure-in-4326 invariant is satisfied by the source CRS
# itself. ETRS89 and WGS84 differ by well under a metre in Spain, which is
# nothing against a 160 m innermost ring.
CRS_PROJECTED = "EPSG:25830"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# Metro de Madrid only. CRTM also publishes Metro Ligero (tram, `M10_Red`) and
# Cercanías (commuter rail); Cercanías is excluded for the reason every city
# here excludes commuter rail, and Metro Ligero is left out of this first build
# so the city ships one agency's rail system, as San Diego and Chicago do.
# Both are a layer away if that is ever revisited.
#
# EIGHTEEN LINE CODES, THIRTEEN LINES, AND THE COLLAPSE IS NOT UNIFORM. This is
# the trap that lost Guadalajara a whole line, in its third form. A naive
# `distinct NUMEROLINEAUSUARIO` returns 18 and would draw Madrid as an 18-line
# system:
#
#   - plain codes                    1 2 3 4 5 8 11 R        ->  8 lines
#   - LETTERED branches              7a/7b  9A/9B  10a/10b   ->  3 lines
#   - CIRCULAR lines published as
#     two codes, each with only
#     `SENTIDO = 1`                  6-1/6-2  12-1/12-2      ->  2 lines
#
# 8 + 3 + 2 = 13, which matches the expired GTFS's 13 `route_type=1` routes and
# the OSM screen's 13 subway refs - three independent sources agreeing.
#
# NOTE THE INCONSISTENT CASE: `7a`/`7b` are lower case and `9A`/`9B` upper.
# A case-sensitive collapse silently leaves one branch of line 9 as its own
# line, so LINE_OF_CODE is keyed on the upper-cased value.
LINE_OF_CODE = {
    "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "8": "8", "11": "11",
    "R": "R",
    "7A": "7", "7B": "7",
    "9A": "9", "9B": "9",
    "10A": "10", "10B": "10",
    "6-1": "6", "6-2": "6",
    "12-1": "12", "12-2": "12",
}

# The real public names, which the project requires for BOTH the on-map label
# and the legend. Riders and the operator both say "Línea N"; `R` is the Ramal
# between Ópera and Príncipe Pío and is never called "Línea 13" - Madrid has no
# line 13. Line 6 is the circular and line 12 is MetroSur, names used in
# conversation but not on the operator's own line diagram, so the numbers stay
# canonical and the nicknames are not invented into the legend.
LINE_NAMES = {
    "1": "Línea 1", "2": "Línea 2", "3": "Línea 3", "4": "Línea 4",
    "5": "Línea 5", "6": "Línea 6", "7": "Línea 7", "8": "Línea 8",
    "9": "Línea 9", "10": "Línea 10", "11": "Línea 11", "12": "Línea 12",
    "R": "Ramal Ópera–Príncipe Pío",
}

# Metro de Madrid's official livery, used so the map's line colours come from
# the operator rather than being invented. TODO: verify each against the
# operator's own diagram before the map ships, and check every one against the
# three business-category colours for Delta-E separation (pipeline/linecolour.py).
LINE_COLOURS = {
    "1": "#30A2DA", "2": "#E1251B", "3": "#FFD200", "4": "#8E4C9C",
    "5": "#98C93C", "6": "#9C9E9F", "7": "#F0821F", "8": "#EC82B1",
    "9": "#95217C", "10": "#003DA5", "11": "#00843D", "12": "#A49A00",
    "R": "#0079C2",
}

# The operator's own municipality code for Madrid, used to CROSS-CHECK the
# spatial filter rather than to replace it. Los Angeles' `council_district` is
# the precedent for preferring an authoritative field to a name match; the
# boundary polygon stays the filter of record, per the add-city invariant.
MADRID_MUNICIPIO_CODE = "079"

# --- Business filtering ------------------------------------------------

# The censo is the Ayuntamiento's OWN register, so every row is already in
# Madrid - there is no out-of-city population to filter out, unlike San Diego's
# Trolley or Vancouver's regional data. `desc_distrito_local` (22 districts) is
# kept as the authoritative in-city field and cross-checked against the
# boundary in step 2; CITY_KEEP is deliberately unused.
DISTRICT_COLUMN = "desc_distrito_local"

# MADRID HAS 21 DISTRICTS, not the 22 the build brief claimed until 2026-09-22.
# `id_distrito_local` runs 1..21 and the names are the city's official ones -
# Centro through Barajas - so the register was complete and the claim about it
# was not. Step 2 raises if this moves.
MADRID_DISTRICT_COUNT = 21

# Keep only premises the register calls open. `Uso vivienda` (8,486) is a
# RESIDENCE SIGNAL SUPPLIED BY THE SOURCE - the unit reverted to residential
# use - which most cities in this project have to infer from a parcel join.
STATUS_COLUMN = "desc_situacion_local"
STATUS_KEEP = "Abierto"

TAXONOMY_SYSTEM = "madrid_epigrafe"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "desc_epigrafe"
TRADE_NAME_COLUMN = "rotulo"
PREMISES_ID_COLUMN = "id_local"
COORD_X_COLUMN = "coordenada_x_local"
COORD_Y_COLUMN = "coordenada_y_local"

# THE COORDINATE COLUMNS ARE 100% POPULATED AND PARTLY INVALID. 34,316 of the
# 159,787 open rows carry a literal zero, stored as the STRING '0.0' so an
# is-it-populated test passes them; in EPSG:25830 that projects to the Atlantic
# off West Africa and vanishes silently on a station-radius map. Measured
# 2026-09-22 on the full download: 21.48% of all open rows, but only 9.21% once
# the storefront filter is applied, because the zeros concentrate in tourist
# flats (85.9%), hostales (74.7%) and offices - categories this project does
# not map. Unlike Los Angeles the loss is biased AWAY from the mapped rows, so
# no geocoding step is needed.
COORD_ZERO_IS_MISSING = True

# Sanity bounds for the supplied coordinates, in the SOURCE CRS (25830 metres),
# not in degrees - the register publishes no lat/lon at all.
MADRID_BBOX_25830 = {
    "x_min": 420_000, "x_max": 460_000,
    "y_min": 4_460_000, "y_max": 4_500_000,
}
