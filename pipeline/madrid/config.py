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

# METRO LIGERO (the tram rescope, 2026-09-27): CRTM's M10 service, same host,
# same schema, same licence as the Metro layers above. 57 station-per-line
# records and 100 tramos when first fetched.
CRTM_LIGERO_SERVICE = (
    "https://services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services"
    "/M10_Red/FeatureServer"
)
LIGERO_STATIONS_RAW_JSON = DATA_RAW / "crtm_m10_estaciones.json"
LIGERO_TRAMOS_RAW_JSON = DATA_RAW / "crtm_m10_tramos.json"
# ML1 ONLY (owner, 2026-09-27). Inside Madrid: ML1's 9 stations; ML2 reaches 2
# (Estación de Aravaca, and Colonia Jardín, already Metro Línea 10's), ML3
# only Colonia Jardín, and ML4 (the Parla tram, codes 4-1/4-2) none - so ML2
# and ML3 are stubs and ML4 is another town's network. `LINEAS` on a station
# and `NUMEROLINEAUSUARIO` on a tramo carry the bare number.
LIGERO_DRAWN = {"1": "ML1"}
LIGERO_LEFT_OUT = {"2": "ML2 - a stub inside Madrid (owner, 2026-09-27)",
                   "3": "ML3 - a stub inside Madrid",
                   # Parla's STATIONS say "4"; its tramos "4-1"/"4-2" (a
                   # circular in two codes, like Metro lines 6 and 12).
                   "4": "ML4, the Parla tram - outside Madrid",
                   "4-1": "ML4, the Parla tram - outside Madrid",
                   "4-2": "ML4, the Parla tram - outside Madrid"}

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
# Metro de Madrid, and from 2026-09-27 Metro Ligero ML1 (see
# CRTM_LIGERO_SERVICE above). Cercanías (commuter rail) is excluded for the
# reason every city here excludes commuter rail. Metro Ligero was left out of
# the first build "so the city ships one agency's rail system"; the tram
# rescope reversed that because ML1 reaches Sanchinarro and Las Tablas, which
# the Metro does not (DECISIONS 2026-09-27).
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
    "ML1": "Metro Ligero ML1",
}

# Gate 3: the per-line station lists CRTM publishes, keyed as LINE_NAMES - every
# drawn line, the 13 Metro lines and ML1. Whole lines, BEFORE the término
# municipal cut (Line 12, MetroSur, lies wholly outside Madrid and counts
# here). An interchange counts once on each line it serves. The build side is
# each line's stations as its CRTM tramos reach them (step 1).
#
# The Plaza de España - Noviciado and Embajadores - Acacias pairs are each ONE
# station record whose LINEAS lists every line of the complex; counted that way
# Line 2 would read 21, Line 3 21, Line 5 33 and Line 10 32. They are counted
# by the tramos instead, which stop each line at its own platform, as CRTM's
# line lists do.
OPERATOR_STATION_COUNTS = {
    "1": 33,     # Pinar de Chamartín - Valdecarros
    "2": 20,     # Las Rosas - Cuatro Caminos
    "3": 19,     # El Casar - Moncloa
    "4": 23,     # Argüelles - Pinar de Chamartín
    "5": 32,     # Alameda de Osuna - Casa de Campo
    "6": 28,     # the circular
    "7": 31,     # Hospital del Henares - Pitis
    "8": 8,      # Nuevos Ministerios - Aeropuerto T4
    "9": 29,     # Paco de Lucía - Arganda del Rey
    "10": 31,    # Hospital Infanta Sofía - Puerta del Sur
    "11": 7,     # Plaza Elíptica - La Fortuna
    "12": 28,    # MetroSur, the circular - all outside Madrid
    "R": 2,      # Ópera - Príncipe Pío
    "ML1": 9,    # Pinar de Chamartín - Las Tablas
}
OPERATOR_COUNTS_SOURCE = (
    "Consorcio Regional de Transportes de Madrid (CRTM), the station list on "
    "each line's page: crtm.es/4__1___ ... 4__12___ and 4__R___ for Metro, "
    "crtm.es/10__51___ for Metro Ligero ML1. Read 2026-10-01. CRTM is the "
    "region's transport authority and publishes the CRTM layers the build "
    "reads, so this is the authority's own published list rather than the "
    "operator's: Metro de Madrid's line pages (metromadrid.es/es/linea/...) "
    "returned a security-block page to every request on 2026-10-01."
)

# Metro de Madrid's official livery, used so the map's line colours come from
# the operator rather than being invented.
#
# CHECKED against the three business-category pins with pipeline/linecolour.py
# on 2026-09-22, and step 3 re-runs that check on every render rather than
# trusting this comment. All 13 clear the hard floor; seven sit below the
# preferred 45 and are listed by name in the output, the closest being the
# Ramal at 14.2 against Retail and Linea 11 at 20.1 against Personal
# services. The project only substitutes its own palette when an agency's
# colours are ambiguous or shared, and Madrid's are neither.
LINE_COLOURS = {
    "1": "#30A2DA", "2": "#E1251B", "3": "#FFD200", "4": "#8E4C9C",
    "5": "#98C93C", "6": "#9C9E9F", "7": "#F0821F", "8": "#EC82B1",
    "9": "#95217C", "10": "#003DA5", "11": "#00843D", "12": "#A49A00",
    "R": "#0079C2",
    # CRTM's own colour for ML1, from the M10_Lineas service's renderer
    # (rgb 39, 84, 211; read 2026-09-27) - the station layer carries none.
    # Delta-E 15.1 from Línea 10 (#003DA5), which meets it at Las Tablas, and
    # 28.0 from the Retail pin: clears the floor, below the preferred 45.
    "ML1": "#2754D3",
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
# DESCRIPTIVE, not a switch: step 2 drops the zeros unconditionally (it
# builds the mask inline), so setting this False would change nothing. Kept
# because the measurement above is the valuable part and this names what it
# concluded.
COORD_ZERO_IS_MISSING = True

# Sanity bounds for the supplied coordinates, in the SOURCE CRS (25830 metres),
# not in degrees - the register publishes no lat/lon at all.
MADRID_BBOX_25830 = {
    "x_min": 420_000, "x_max": 460_000,
    "y_min": 4_460_000, "y_max": 4_500_000,
}
