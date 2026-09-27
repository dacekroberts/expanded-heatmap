"""Monterrey (Regional) settings - Mexico's third city, on the national modules
Mexico City and Guadalajara built (DENUE, scian.py, INEGI's licence and notice).
Guadalajara is the shape copied: a regional build over several municipios, rail
from OpenStreetMap, and the operator's own station counts as gate 3.

REGIONAL, owner's call 2026-09-27 ("regional scope yes"). Monterrey, San
Nicolás de los Garza, Guadalupe and General Escobedo - exactly the municipios a
0.6-mile ring reaches. A Monterrey-only build would cut Línea 2 to 8 of its 13
stations (62%, below Rennes' 11 of 15, the lowest kept commune-only) and lose
its northern leg, Universidad included.

OPENSTREETMAP IS THE RAIL GROUND, owner's call 2026-09-27 ("OSM ok"), on the
same grounds as Mexico City's per-city exception: Nuevo León publishes no
Metrorrey feed, `metrorrey.gob.mx` does not resolve, the state GIS
(`mapas.nl.gob.mx`) times out, and `datos.nl.gob.mx` is a brochure site. It was
recorded as "a real negative" on 2026-09-22 for exactly that reason, which
stopped mattering once OSM was approved as a rail source (see osm-rail).

GATE 3 RUNS IN FULL HERE, unlike Guadalajara's partial one: the operator's
network map names every station on all three lines.
"""

from pathlib import Path

from pipeline.countries.mexico import (  # noqa: F401
    DENUE_ACTIVITY_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_INTERIOR_COLUMN,
    DENUE_MUNICIPIO_CODE_COLUMN,
    DENUE_MUNICIPIO_COLUMN,
    DENUE_NAME_COLUMN,
    DENUE_STATE_COLUMN,
    FORBIDDEN_COLUMNS,
    OSM_NEVER_A_STATION,
    OVERPASS_HOSTS,
    OVERPASS_USER_AGENT,
    PREMISES_TYPE_COLUMN,
    PREMISES_TYPE_KEEP,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
    denue_member,
    denue_url,
)

# Re-exported rather than redefined, as Guadalajara's config does: each is a
# fact about DENUE or OpenStreetMap, not about this city.

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "monterrey" / "raw"
DATA_PROCESSED = ROOT / "data" / "monterrey" / "processed"
OUTPUTS = ROOT / "outputs" / "monterrey"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# Which municipio each kept station lies in - the regional-build record, as
# Guadalajara's and Miami's are.
STATION_MUNICIPIOS_CSV = OUTPUTS / "station_municipios.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs -----------------------------------------------------------
#
# 19 = Nuevo León. As in Jalisco, the entidad is NOT the city: 211,349 units
# statewide, so the scope is finished by MUNICIPIOS below.
DENUE_STATE_CODE = "19"
DENUE_URL = denue_url(DENUE_STATE_CODE)
DENUE_MEMBER = denue_member(DENUE_STATE_CODE)
DENUE_ZIP = DATA_RAW / f"denue_{DENUE_STATE_CODE}_csv.zip"

OSM_STATIONS_JSON = DATA_RAW / "osm_stations.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"

# The operator's network map, read for gate 3 and for Línea 3's colour only -
# never republished (the nl.gob.mx site terms are unread, and nothing from the
# PDF is shown). Dated 2026-05-08 in its own file name.
OPERATOR_MAP_URL = (
    "https://www.nl.gob.mx/sites/default/files/repositorio/Dependencias/"
    "Sistema%20de%20Transporte%20Colectivo%20%28Metrorrey%29/Repositorios/"
    "20260508_mapa_red_metrorrey.pdf"
)
OPERATOR_MAP_PDF = DATA_RAW / "20260508_mapa_red_metrorrey.pdf"

# --- The regional scope ---------------------------------------------------
#
# KEYED ON INEGI'S MUNICIPIO CODE, not on the name - the first Mexican city to
# do so. OSM's `INEGI:MUNID` equals DENUE's cve_ent + cve_mun, so the register
# and the boundaries join on the same code and no spelling can drift between
# them ("San Nicolás de los Garza" vs "San Nicolás"). The names are kept only to
# be ASSERTED against DENUE's own `municipio` column, so a wrong code fails
# loudly instead of scoping to some other municipio.
MUNICIPIOS = {
    "039": "Monterrey",
    "046": "San Nicolás de los Garza",
    "026": "Guadalupe",
    "021": "General Escobedo",
}
MUNIDS = tuple(DENUE_STATE_CODE + code for code in MUNICIPIOS)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 14N: the centre (~-100.31) and the whole extent (-100.47 to
# -100.12) fall in the -102 to -96 band. Mexico City is 14N too, Guadalajara
# 13N - derived per city, never copied.
CRS_PROJECTED = "EPSG:32614"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- OpenStreetMap fetch --------------------------------------------------

# south, west, north, east - the brief's bbox, which holds all four municipios.
OSM_BBOX = "25.55,-100.55,25.90,-100.05"
OSM_NETWORK = "Metrorrey"

# STATIONS COME FROM ROUTE MEMBERSHIP, AND MEMBERS COME IN TWO TYPES. 36 of the
# members are `railway=station` nodes; Cuauhtémoc and General Anaya are members
# only as `railway=stop` stop positions. So both are accepted - but only as
# members of a Metrorrey route relation, never by tag. A tag whitelist in the
# Mexico City style would admit the 11 unbuilt monorail stations below.
OSM_STATION_RAILWAY = ("station", "stop")

# 🚨 LÍNEAS 4 AND 6 ARE UNDER CONSTRUCTION, and OSM already carries 11 of their
# monorail stations as `railway=station` + `construction=yes`. They are not
# route members today, so membership keeps them out - and step 1 RAISES if a
# member ever carries a construction tag, or if a monorail route relation
# appears, because either means Línea 4 or 6 may have opened and the map must
# be re-checked rather than quietly redrawn.
OSM_CONSTRUCTION_TAGS = ("construction", "construction:railway")

# --- Station scope ----------------------------------------------------------

LINE_NAMES = {
    "1": "Línea 1",
    "2": "Línea 2",
    "3": "Línea 3",
}
# Líneas 1 and 2 are OSM's `colour` tags, checked against the operator's
# 2026-05-08 map, where they agree in hue (a yellow and a green).
#
# LÍNEA 3 IS THE OPERATOR'S RED, owner's call 2026-09-27 ("use operator's
# red"). OSM tags it #FF8000, but on the operator's map orange is Línea 6, a
# line under construction and not drawn here - so OSM's colour would have
# drawn Línea 3 in another line's colour. The PDF carries CMYK, not a hex:
# its only red, CMYK (0, 0.914, 0.726, 0), converts to #FF1646 by the device
# formula R=(1-C)(1-K) and so on. It was identified by the path it draws - the
# red runs from Línea 2's southern terminal north-east to its own terminus,
# Línea 3's route - not by hue alone. Read 2026-09-27; the PDF is not shown.
LINE_COLOURS = {
    "1": "#FEC04F",
    "2": "#6BC069",
    "3": "#FF1646",
}

# GATE 3, IN FULL. The operator's 2026-05-08 network map names exactly these
# (OPERATOR_MAP_URL above), and OSM route membership matched all three at the
# 2026-09-27 screen.
PUBLISHED_STATIONS_PER_LINE = {
    "Línea 1": 19,
    "Línea 2": 13,
    "Línea 3": 9,
}

# OSM's spelling of two names is wrong against the operator's. Applied after the
# accent-folded collapse, so they fix the displayed name only.
PUBLIC_NAME_FIXES = {
    "Ruiz Cortinez": "Ruiz Cortines",
    "Niños Heroes": "Niños Héroes",
}

# --- Business filtering ------------------------------------------------

MONTERREY_BBOX = {
    "lat_min": 25.55,
    "lat_max": 25.90,
    "lon_min": -100.55,
    "lon_max": -100.05,
}
