"""Salvador: settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/salvador.md.

Metrô de Salvador (CCR Metrô Bahia) from OpenStreetMap, whose four relations
carry no colour at all. The operator names its lines by colour - Linha
1-Vermelha and Linha 2-Azul (trilhos.motiva.com.br/metrobahia, read 2026-09-24) -
and publishes no hex, so the names are resolved through the CSS named-colour table,
Guadalajara's precedent for OSM's colour=orange.
"""

from pathlib import Path

SLUG = "salvador"
NAME = "Salvador"

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / SLUG / "raw"
DATA_PROCESSED = ROOT / "data" / SLUG / "processed"
OUTPUTS = ROOT / "outputs" / SLUG

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"
STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
UNCLASSIFIED_CSV = DATA_PROCESSED / "cnefe_unclassified.csv"
OSM_LINES_JSON = DATA_PROCESSED / "osm_lines.json"
OSM_MUNICIPIOS_JSON = DATA_RAW / "osm_municipios.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"

TAXONOMY_SYSTEM = "brazil_cnefe"

# --- Scope -------------------------------------------------------------------------
# One zip per município (IBGE code prefix). Salvador alone; the brief measured every station inside it.
CNEFE_FILES = [('29_BA', '2927408_SALVADOR.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('2927408',)
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (550, 800)   # gate on the union's area
BBOX = (-13.05, -38.6, -12.7, -38.25)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 24S: longitude ~-38.5 lies in the -42 to -36 band.
CRS_PROJECTED = "EPSG:32724"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# L1 and L2 by relation id; nothing else is in the cache. Acesso Norte is the interchange.
SYSTEM = "Metrô"
MAP_TITLE = "Salvador Metrô Business Density Heatmap"
LINE_RELATIONS = {'1': (4511874, 6774703), '2': (6771624, 7857257)}
LEFT_OUT = {}
LINE_ORDER = ('1', '2')
LINE_NAMES = {'1': 'Linha 1-Vermelha', '2': 'Linha 2-Azul'}
# The operator's colour NAMES through the CSS table: vermelha 'red' #FF0000, azul 'blue' #0000FF.
LINE_COLOURS = {'1': '#FF0000', '2': '#0000FF'}
STATION_NAME_ALIASES = {}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
GATE3 = {'lines': {'1': 10, '2': 12}, 'network': None, 'source': "the operator (trilhos.motiva.com.br/metrobahia) and pt.wikipedia 'Metrô de Salvador', read 2026-09-24: Linha 1 10 stations, Linha 2 12"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400
