"""Mendoza-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

MENDOZA, ARGENTINA, the capital department alone (owner, 2026-10-03): the
Municipalidad de la Ciudad de Mendoza's "Listado Comercios por Actividad
2025" (CC BY 4.0), one point per business in Gauss-Kruger zone 2, classified
by its own activity scheme (`pipeline/taxonomies/mendoza_rama.py`); the
Metrotranvia from OpenStreetMap on the shared `pipeline/osm_tram.py`, drawn
to its end (owner, 2026-10-03), its stations outside the capital listed and
not ringed (Florence's shape, tram-city calls 17 and 21). Buenos Aires is the
country precedent, but no code of its is reused (docs/spain_retrospective.md).
"""

from pathlib import Path

SLUG = "mendoza"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "mendoza" / "raw"
DATA_PROCESSED = ROOT / "data" / "mendoza" / "processed"
OUTPUTS = ROOT / "outputs" / "mendoza"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the capital, with the department each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# "Listado Comercios por Actividad 2025" (CKAN `listado-comercios-por-actividad-2025`
# on datos.ciudaddemendoza.gob.ar, CC-BY-4.0): the JSON resource, which carries
# the points and the activity rows together. Owner-approved download
# 2026-10-03; the cached copy is checked against its sha256.
REGISTER_PACKAGE = "listado-comercios-por-actividad-2025"
REGISTER_PAGE = f"https://datos.ciudaddemendoza.gob.ar/dataset/{REGISTER_PACKAGE}"
REGISTER_URL = ("https://datos.ciudaddemendoza.gob.ar/dataset/df39f71e-0d7e-40e5-a475-c31f098fab93/"
                "resource/94e44b27-951e-4f38-a5c4-17eec535a3fe/download/comercios_limpio.json")
REGISTER_JSON = DATA_RAW / "comercios_limpio.json"
REGISTER_SHA256 = "ca6af57c5625eb9868a77d6d5bd7e112b9408a33c74de7da00cb9986b707fd17"
# The data date: open accounts at June 2025 (the package title; estado_cuenta
# ALTA on every CSV row, newest fecha_inicio 2025-07-08; the brief).
REGISTER_DATA_DATE = "June 2025"

# The register's x/y: POSGAR 2007 / Argentina zone 2 (Gauss-Kruger), the
# current frame; POSGAR 94's EPSG:22182 agrees within 0.0001 degrees (the brief).
REGISTER_CRS = "EPSG:5344"

# OSM, one query: the box's tram and light-rail relations with geometry, their
# stop nodes, and the departments (admin_level 5) the line crosses, which name
# where each station outside the capital lies.
RAIL_BBOX = (-33.00, -68.90, -32.80, -68.76)        # south, west, north, east
OSM_ROUTES = ("tram", "light_rail")
OSM_JSON = DATA_RAW / "osm.json"
# The scope: OSM's "Departamento Capital" (relation 2204157), the owner's
# choice over the portal's seccionales (2026-10-04). 106.0 km2 in UTM 19S
# (2026-10-04); step 1 stops outside these bounds, so a truncated answer
# cannot pass.
CAPITAL_AREA_KM2 = (95.0, 115.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 19S: the longitude (~-68.85) falls in the -72 to -66 band, south of
# the equator. Derived per city, not copied.
CRS_PROJECTED = "EPSG:32719"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED on the spacing rule: the capital's 7 stations sit a median 412 m apart
# (2026-10-04; the whole line's median is 556 m), under 550 m
# (docs/ring_rules.md). Step 1 stops outside 360-470 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (360.0, 470.0)

# --- Station scope: the capital's stations, the line drawn to its end -------
#
# The Metrotranvia is one line, Gutierrez (Maipu) to Avellaneda (Las Heras):
# two `route=light_rail` relations, one per direction, ref "MTM", operator
# "Sociedad de Transporte Mendoza", network MendoTRAN (2119332 line 101,
# 3413331 line 100; read 2026-10-04), each with all 25 stops. No other tram or
# light rail in the box. The whole line is drawn (owner, 2026-10-03: "yes draw
# mendoza line to end"); only the stops inside the capital get rings.
ROUTES = ("light_rail", "tram")
OPERATOR = "Sociedad de Transporte Mendoza"
LINE_REFS = ("MTM",)
NOT_DRAWN = {}
STATION_ADD = {}

# GATE 3, the whole line. The operator's own page (stmendoza.com/metrotranvia,
# read 2026-10-04) says "dos Estaciones Principales, ademas de 21 paradores",
# 23, which no list reconciles; its timetables carry 11 timing points only.
# So the count is es.wikipedia's line infobox, the brief's named SECONDARY
# fallback: 25 stations, the same 25 names OSM carries.
OPERATOR_STATION_COUNTS = {"MTM": 25}
OPERATOR_COUNTS_SOURCE = (
    "es.wikipedia, 'Metrotranvia de Mendoza', infobox 'Estaciones: 25'; SECONDARY (the "
    "operator's page states 2 stations and 21 stops, 23, unreconciled); read 2026-10-04")

SPACING_MIN_M = 150.0
# The capital's stations: the city's own stop list (paradas-metrotranvia, CC BY
# 4.0) files 14 platforms, so 7 stations, under the Ciudad de Mendoza (the
# brief); the polygon decides each, and step 1 stops if it disagrees.
EXPECTED_IN_SCOPE = 7
DRAWN_LINES = ("MTM",)
LINE_NAMES = {"MTM": "Metrotranvía"}
# OSM records colour "red"; a plain red (#C62828) sits CIE76 33.2 from the Food
# service pins. The nearest red clearing the preferred 45 from every pin and
# 3:1 on both page backgrounds (line_colour_search.py's criteria, searched in
# HSL, 2026-10-04): #CB2910, 45.4.
LINE_COLOURS = {"MTM": "#CB2910"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "mendoza_rama"
RAW_CLASSIFICATION_COLUMN = "desc_full"

# Sanity bounds for the register's points, after reprojection: the capital
# department plus a margin.
MENDOZA_BBOX = {
    "lat_min": -32.95,
    "lat_max": -32.80,
    "lon_min": -68.95,
    "lon_max": -68.78,
}
