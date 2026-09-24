"""Rio de Janeiro: settings for one Brazilian city on the national CNEFE modules
(.claude/skills/brazil-city/). Brief: docs/build_briefs/rio-de-janeiro.md.

MetrôRio from the city's OWN layers (IPP / DATA.RIO, pgeo3.rio.rj.gov.br
Transporte_publico, CC BY 4.0 - a notice is required): stations layer 19 with
per-line flags, lines layer 18. The VLT Carioca from OpenStreetMap, NOT the agency's
layer 9 - measured: its line flags give 20/14/11/14 stops per line where
pt.wikipedia lists 16/11/10/11 (30 in all) and OSM's relations agree with Wikipedia.
Owner's calls of 2026-09-24: the Bonde de Santa Teresa and the Trem do Corcovado
are not drawn; the Teleferico would be drawn if operating - it is not (closed
since 2016, reopening moved to June 2027); SuperVia went through the rail test -
Deodoro and Saracuruna pass and are drawn from OSM; Japeri fails; Belford Roxo and
Santa Cruz are borderline and out pending the owner (the rail comment below).
"""

from pathlib import Path

SLUG = "rio_de_janeiro"
NAME = "Rio de Janeiro"

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
# One zip per município (IBGE code prefix). Rio de Janeiro alone; the brief measured every metro and VLT station inside it.
CNEFE_FILES = [('33_RJ', '3304557_RIO_DE_JANEIRO.zip')]
CNEFE_ZIPS = tuple(DATA_RAW / name for _, name in CNEFE_FILES)
SCOPE_CODES = ('3304557',)
IBGE_MUNICIPIO = SCOPE_CODES[0]
SCOPE_AREA_KM2 = (1150, 1270)   # gate on the union's area
BBOX = (-23.08, -43.8, -22.75, -43.1)   # s, w, n, e - the fetch's OSM box
SANITY_BBOX = {"lat_min": BBOX[0], "lat_max": BBOX[2], "lon_min": BBOX[1], "lon_max": BBOX[3]}

# --- Coordinate reference systems -----------------------------------------
CRS_GEOGRAPHIC = "EPSG:4326"
# UTM 23S: longitude ~-43.2 lies in the -48 to -42 band.
CRS_PROJECTED = "EPSG:32723"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (OpenStreetMap, osm-rail; pipeline/countries/brazil_rail.py) --------
# LINE_RELATIONS are the OSM lines: the VLT's four, and the two SuperVia lines that pass the
# RAIL TEST (the owner's standing call for this batch), measured 2026-09-24 with
# scripts/measure_rail_backbone.py: DEODORO - 1,204 m median in the city, every 6-8 min at peak
# (en.wikipedia), 13 of 19 stations with no metro or VLT within 800 m; SARACURUNA to Gramacho -
# 1,314 m, every 12 min at peak (SuperVia, February 2026), 10 of 14. Japeri (3,223 m) fails;
# Belford Roxo (1,814 m, every 15 min) and Santa Cruz (2,114 m) are BORDERLINE - out pending
# the owner. The metro is METRO_* below, from the agency.
SYSTEM = "Metrô, VLT and SuperVia"
MAP_TITLE = "Rio de Janeiro Metrô, VLT and SuperVia Business Density Heatmap"
VLT_LINES = ("V1", "V2", "V3", "V4")
LINE_RELATIONS = {'V1': (6667528, 6667529), 'V2': (7064052, 7064053), 'V3': (9453118, 9453119), 'V4': (19644242, 19644243), 'SD': (1609111, 9963664), 'SS': (1306884, 9963672)}
LEFT_OUT = {285322: "MetrôRio Linha 1 - drawn from the city's own layers", 7944060: "MetrôRio Linha 1 - drawn from the city's own layers", 285324: "MetrôRio Linha 2 - drawn from the city's own layers", 4292975: "MetrôRio Linha 2 - drawn from the city's own layers", 6432700: "MetrôRio Linha 4 - drawn from the city's own layers", 6432701: "MetrôRio Linha 4 - drawn from the city's own layers", 1578053: 'SuperVia Belford Roxo - 1.8 km apart, every 15 min at peak: BORDERLINE on the rail test, out pending the owner', 9963650: 'SuperVia Belford Roxo - 1.8 km apart, every 15 min at peak: BORDERLINE on the rail test, out pending the owner', 1609112: 'SuperVia Santa Cruz - 2.1 km apart in the city: BORDERLINE on the rail test, out pending the owner', 6432130: 'SuperVia Santa Cruz - 2.1 km apart in the city: BORDERLINE on the rail test, out pending the owner', 1589649: 'SuperVia Japeri - 3.2 km apart in the city: fails the rail test', 6432247: 'SuperVia Japeri - 3.2 km apart in the city: fails the rail test', 6018221: 'SuperVia Saracuruna, Gramacho-Saracuruna shuttle - wholly outside the city', 9963666: 'SuperVia Saracuruna, Gramacho-Saracuruna shuttle - wholly outside the city', 933653: 'Trem do Corcovado - a tourist rack railway (owner, 2026-09-24)', 10334822: 'Trem do Corcovado - a tourist rack railway (owner, 2026-09-24)', 10731390: 'Bonde de Santa Teresa - a heritage tram (owner, 2026-09-24)', 10731391: 'Bonde de Santa Teresa - a heritage tram (owner, 2026-09-24)', 18531112: 'Bonde de Santa Teresa - a heritage tram (owner, 2026-09-24)', 18531113: 'Bonde de Santa Teresa - a heritage tram (owner, 2026-09-24)', 3867895: 'EFCB Carlos Sampaio - Austin - Santa Cruz link - no stops'}
LINE_ORDER = ('1', '2', '4', 'V1', 'V2', 'V3', 'V4', 'SD', 'SS')
LINE_NAMES = {'1': 'Metrô Linha 1', '2': 'Metrô Linha 2', '4': 'Metrô Linha 4', 'V1': 'VLT Linha 1', 'V2': 'VLT Linha 2', 'V3': 'VLT Linha 3', 'V4': 'VLT Linha 4', 'SD': 'SuperVia Deodoro', 'SS': 'SuperVia Saracuruna'}
# OSM's colours (the agency layers carry none); VLT 1 and 2 are CSS names in OSM ('blue',
# 'green'), resolved through the CSS table. Nine lines in shared hues, so four move in HSL
# lightness by the smallest step that clears 13 from every other line: VLT 2 #008000 -> #008500,
# VLT 3 #F1C232 -> #f3c94a, VLT 4 #EC6F29 -> #ed7837, Saracuruna #FA8835 -> #fb9a53 - the
# closest pair after is Metrô 4 / VLT 3 at 13.2.
LINE_COLOURS = {'1': '#e77405', '2': '#028F34', '4': '#FFCC29', 'V1': '#0000FF', 'V2': '#008500', 'V3': '#f3c94a', 'V4': '#ed7837', 'SD': '#F60619', 'SS': '#fb9a53'}
STATION_NAME_ALIASES = {}
# Two DIFFERENT stations share a name: MetrôRio's São Francisco Xavier (Tijuca)
# and SuperVia's, 2.8 km apart - the collapse-by-name spread cap caught it. A
# line-scoped rename keeps them apart.
LINE_STATION_RENAMES = {("SD", "São Francisco Xavier"): "São Francisco Xavier (SuperVia)"}
# Stop positions OSM leaves unnamed, named from their wikidata item's label.
NODE_NAMES = {}
# The VLT's gate is its NETWORK count. Its downtown runs as one-way loops, so a
# line serves different stops in each direction (VLT 1 outbound via Equador,
# Gamboa, Providencia; inbound via Utopia AquaRio, Santo Cristo) and its
# stations here are the union - 20 / 14 / 10 / 13. pt.wikipedia lists each
# DIRECTION (16 / 11 / 10 / 11), so per-line counts cannot be compared; its
# 30 stops in all can, and match.
# SuperVia Deodoro: en.wikipedia 'Deodoro Line' lists its 19 stations, Central to
# Deodoro. Saracuruna has no article with a count read here - it is ungated.
GATE3 = {'lines': {'SD': 19}, 'network': 30, 'source': "pt.wikipedia 'VLT Carioca', read 2026-09-24 - secondary: 30 stops in all (its per-line lists are per direction); en.wikipedia 'Deodoro Line': 19 stations"}
# --- The metro, from the city's own layers (IPP / DATA.RIO, CC BY 4.0) --------
METRO_STATIONS_JSON = DATA_RAW / "rio_metro_estacoes_19.geojson"
METRO_LINES_JSON = DATA_RAW / "rio_metro_linhas_18.geojson"
METRO_FLAGS = {"1": "flg_linha1", "2": "flg_linha2", "4": "flg_linha4"}
# Gate 3 for the metro: the agency's flags (20 / 26 / 6) agree with OSM's route
# relations line by line, and its 41 stations with pt.wikipedia's "41 estações".
# Wikipedia's own per-line table (20 / 27 / 5) counts General Osório on Linha 1
# alone, where both other sources put it on Linha 4 as well.
METRO_GATE3 = {"lines": {"1": 20, "2": 26, "4": 6}, "network": 41,
               "source": "IPP layer 19's flags, matched by OSM's relations line by line; "
                         "pt.wikipedia 'Metrô do Rio de Janeiro', read 2026-09-24: 41 stations"}
# Step 1 writes both systems' geometry here for step 3 (feature property `line`).
LINES_GEOJSON = DATA_PROCESSED / "rail_lines.geojson"
SPACING_MIN_M = 300.0
COLLAPSE_MAX_SPREAD_M = 400
