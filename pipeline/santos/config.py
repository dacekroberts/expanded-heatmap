"""Santos (Regional): settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/santos.md.

The VLT da Baixada Santista from OpenStreetMap, L1 and L2. L2's twelve new
stations opened 2025-12-01 in assisted operation, 9h-15h - drawn on the owner's
Belo Horizonte precedent (open, with limited hours), the page noting them.
REGIONAL - the owner's decision of 2026-09-23: Santos and Sao Vicente. The Bonde
Turistico is not drawn (a tourist service). EMTU's CPGSTM layers are a status
cross-check only and are never read by a step.
"""

from pathlib import Path

SLUG = "santos"
NAME = "Santos (Regional)"

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
# One zip per município (IBGE code prefix). Two municípios - the owner's regional decision of 2026-09-23.
CNEFE_FILES = [('35_SP', '3548500_SANTOS.zip'), ('35_SP', '3551009_SAO_VICENTE.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('3548500', '3551009')
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (380, 470)   # gate on the union's area
BBOX = (-24.05, -46.6, -23.85, -46.2)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 23S: longitude ~-46.3 lies in the -48 to -42 band.
CRS_PROJECTED = "EPSG:32723"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# L1 and L2 by relation id. Left out: the Bonde Turistico. Three new L2 stops carry no name in OSM,
# only a wikidata item - named from its label (NODE_NAMES); Ana Costa is named from its wikipedia tag.
# 'Sao Bento', 148 m from Valongo on the terminal loop's far side, is in no published station list
# (pt.wikipedia lists L2's 12 new stations, both Universidades, no Sao Bento) - treated as Valongo.
SYSTEM = "VLT"
MAP_TITLE = "Santos VLT Business Density Heatmap"
LINE_RELATIONS = {'L1': (7252642, 7252643), 'L2': (19185420, 20507681)}
LEFT_OUT = {19975166: 'Bonde Turístico de Santos - a heritage tourist tram'}
LINE_ORDER = ('L1', 'L2')
LINE_NAMES = {'L1': 'VLT Linha 1', 'L2': 'VLT Linha 2'}
# OSM's colours: L1 #005CA9, L2 #F26A21.
LINE_COLOURS = {'L1': '#005CA9', 'L2': '#F26A21'}
STATION_NAME_ALIASES = {'São Bento': 'Valongo'}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {12396988316: 'Mercado', 12396988312: 'Paquetá', 12396988308: 'Poupatempo'}
GATE3 = {'lines': {'L1': 15}, 'network': 27, 'source': "pt.wikipedia 'VLT da Baixada Santista', read 2026-09-24 - secondary; L1 15 stations (14 shared with L2), 12 new on L2 - 27 in all"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400
