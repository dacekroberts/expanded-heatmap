"""Brasília: settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/brasilia.md.

Metrô-DF, Linha Verde and Linha Laranja, from OpenStreetMap; the Federal
District's own station layer (IPEDF, public domain) is the gate-3 count and the
status reference - its five stations under construction are not drawn. The
agency draws both lines as ONE MultiLineString, so per-line geometry is OSM's.
Block addressing: the lot-aware dwelling key (brazil.address_key) applies.
"""

from pathlib import Path

SLUG = "brasilia"
NAME = "Brasília"

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
# One zip per município (IBGE code prefix). Brasília is the whole Federal District, one município (5300108).
CNEFE_FILES = [('53_DF', '5300108_BRASILIA.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('5300108',)
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (5500, 6000)   # gate on the union's area
BBOX = (-16.06, -48.3, -15.49, -47.3)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 23S: the Federal District's centre, longitude ~-47.9, lies in the -48 to -42 band.
CRS_PROJECTED = "EPSG:32723"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# Both lines by relation id; nothing else is in the cache.
SYSTEM = "Metrô-DF"
MAP_TITLE = "Brasília Metrô-DF Business Density Heatmap"
LINE_RELATIONS = {'Verde': (420554, 7733963), 'Laranja': (420556, 7733964)}
LEFT_OUT = {}
LINE_ORDER = ('Verde', 'Laranja')
LINE_NAMES = {'Verde': 'Linha Verde', 'Laranja': 'Linha Laranja'}
# OSM's colours: Verde #076C57, Laranja #EB9710.
LINE_COLOURS = {'Verde': '#076C57', 'Laranja': '#EB9710'}
STATION_NAME_ALIASES = {}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
GATE3 = {'lines': {}, 'network': 27, 'source': "pt.wikipedia 'Metrô do Distrito Federal', read 2026-09-24 - secondary: 27 stations in operation. The agency's own IPEDF layer (2023) lists 24 and marks 106 Sul, 110 Sul and Estrada Parque as under construction, though they opened in 2020 (106/110 Sul 2020-09-17, Estrada Parque January 2020) - stale by those three, as GeoSampa was by Jardim Colonial; 104 Sul and Onoyama are still being built and are in neither OSM nor the count"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400
