"""Recife (Regional): settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/recife.md.

Metrô do Recife from OpenStreetMap: Linha Centro's two branches and Linha Sul
(electric), drawn; the two diesel VLTs failed the rail test on spacing and are not. REGIONAL - the owner's decision of 2026-09-23: Recife,
Jaboatao dos Guararapes, Cabo de Santo Agostinho and Camaragibe. The city's ODbL
station file is a cross-check only and is never read by a step.
"""

from pathlib import Path

SLUG = "recife"
NAME = "Recife (Regional)"

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
# One zip per município (IBGE code prefix). Four municípios - the owner's regional decision of 2026-09-23.
CNEFE_FILES = [('26_PE', '2611606_RECIFE.zip'), ('26_PE', '2607901_JABOATAO_DOS_GUARARAPES.zip'), ('26_PE', '2602902_CABO_DE_SANTO_AGOSTINHO.zip'), ('26_PE', '2603454_CAMARAGIBE.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('2611606', '2607901', '2602902', '2603454')
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (880, 1080)   # gate on the union's area
BBOX = (-8.4, -35.15, -7.92, -34.83)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 25S: longitude ~-34.9 lies in the -36 to -30 band.
CRS_PROJECTED = "EPSG:32725"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# THE RAIL TEST (the owner's standing call for this batch), measured 2026-09-24 with
# scripts/measure_rail_backbone.py: the VLT to Cabo 3,126 m median, the VLT to Curado 3,941 m -
# CLEAR FAILS on spacing (Metromare, left out, was 2,171), out. Cabo's only stations were
# the VLT's; the owner's regional scope is kept, so Cabo contributes storefronts and no
# station - Guadalajara's precedent.
SYSTEM = "Metrô do Recife"
MAP_TITLE = "Recife Metrô Business Density Heatmap"
LINE_RELATIONS = {'Camaragibe': (420618, 7869351), 'Jaboatao': (420619, 7869333), 'Sul': (4510097, 7869373)}
LEFT_OUT = {9699109: 'VLT Cajueiro Seco-Cabo - diesel, 3.1 km apart: fails the rail test', 4510254: 'VLT Cajueiro Seco-Cabo - diesel, 3.1 km apart: fails the rail test', 4510189: 'VLT Curado-Cajueiro Seco - diesel, 3.9 km apart: fails the rail test', 7945216: 'VLT Curado-Cajueiro Seco - diesel, 3.9 km apart: fails the rail test'}
LINE_ORDER = ('Camaragibe', 'Jaboatao', 'Sul')
LINE_NAMES = {'Camaragibe': 'Linha Centro – Camaragibe', 'Jaboatao': 'Linha Centro – Jaboatão', 'Sul': 'Linha Sul'}
# OSM's colours: Camaragibe #e77405, Jaboatao #D9001C, Sul #1a5ba3.
LINE_COLOURS = {'Camaragibe': '#e77405', 'Jaboatao': '#D9001C', 'Sul': '#1a5ba3'}
STATION_NAME_ALIASES = {}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
GATE3 = {'lines': {'Camaragibe': 15, 'Jaboatao': 14, 'Sul': 12}, 'network': None, 'source': "pt.wikipedia 'Metrô do Recife', read 2026-09-24 - secondary; Centro-Camaragibe 15, Centro-Jaboatao 14, Sul 12, VLT Cabo 6, VLT Curado 4"}
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400
