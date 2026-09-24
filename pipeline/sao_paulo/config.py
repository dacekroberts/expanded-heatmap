"""São Paulo-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Brazil's first city. The business leg is IBGE's CNEFE 2022 - the census's own
walk of every block, one row per use-type per address, with the enumerator's
coordinate - so there is no register and no geocoder. Brief:
docs/build_briefs/sao-paulo.md; the country: docs/global_country_shortlist.md.

PINNED 2026-09-24 AT STEP 2: the CNEFE classifier is to be ONE shared national
module under pipeline/taxonomies/ (the brief), and docs/session_roles.md gives
shared taxonomy code to the app/chrome or staging role, which was live that
night. Steps 1 and the fetch are this city's own paths and are built; step 2
waits for the owner to say who writes the national module.
"""

from pathlib import Path

SLUG = "sao_paulo"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "sao_paulo" / "raw"
DATA_PROCESSED = ROOT / "data" / "sao_paulo" / "processed"
OUTPUTS = ROOT / "outputs" / "sao_paulo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

CNEFE_ZIP = DATA_RAW / "3550308_SAO_PAULO.zip"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"
GEOSAMPA_STATIONS_JSON = DATA_RAW / "geosampa_estacao_metro.json"

# --- Endpoints ---------------------------------------------------------------

CNEFE_URL = ("https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/"
             "Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/3550308_SAO_PAULO.zip")
# GeoSampa's OPERATING metro stations - for STATUS and the gate-3 count only,
# never drawn (the owner's 2026-09-23 decision: its licence is ambiguous).
GEOSAMPA_STATIONS_URL = ("https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/ows?service=WFS"
                         "&version=2.0.0&request=GetFeature&typeNames=geoportal:estacao_metro"
                         "&outputFormat=application/json")

# --- Scope ---------------------------------------------------------------------

IBGE_MUNICIPIO = "3550308"
BOUNDARY_AREA_KM2 = (1480, 1560)   # IBGE: 1,521 km²
RAIL_BBOX = (-23.80, -46.83, -23.36, -46.36)   # s, w, n, e
SP_BBOX = {"lat_min": -24.02, "lat_max": -23.35, "lon_min": -46.83, "lon_max": -46.36}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 23S: longitude ~-46.6 falls in the -48 to -42 band, southern
# hemisphere. GeoSampa's EPSG:31983 is SIRGAS 2000 / UTM 23S, the same zone.
CRS_PROJECTED = "EPSG:32723"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Rail (the owner's 2026-09-23 decision) ------------------------------------
#
# Geometry and stations from OpenStreetMap by route-relation membership
# (osm-rail); GeoSampa only for which lines OPERATE and the station count.
# Draw subway refs 1-5 and monorail ref 15. Refs 6 (Laranja) and 17 (Ouro)
# are in OSM but only in GeoSampa's PLANNED layer - Tel Aviv's trap - and
# step 1 STOPS the day either appears in the operating layer, so it is added
# deliberately. CPTM (commuter rail) is out by the standing rule.
DRAW_REFS = {"subway": ("1", "2", "3", "4", "5"), "monorail": ("15",)}
NOT_YET_OPEN_REFS = ("6", "17")
LINE_ORDER = ("1", "2", "3", "4", "5", "15")
LINE_NAMES = {"1": "Linha 1-Azul", "2": "Linha 2-Verde", "3": "Linha 3-Vermelha",
              "4": "Linha 4-Amarela", "5": "Linha 5-Lilás", "15": "Linha 15-Prata"}
# OSM's colours (GeoSampa carries none), measured 2026-09-24 against the pins:
# all clear the floor unchanged; Linha 1 is 13.7 from Retail and recorded, as
# agency colours below the preferred 45 are. Linha 3's two direction relations
# disagree (#ef3f32 / #D9001C, 10.5 apart); the first relation's is taken.
LINE_COLOURS = {"1": "#1266af", "2": "#008162", "3": "#ef3f32", "4": "#FFD700",
                "5": "#9200C3", "15": "#7b9192"}
# Gate 3: GeoSampa's operating layer, 85 distinct stations (brief, 2026-09-23);
# re-counted from the cached layer at every run - with ONE recorded correction.
# The layer lacks Jardim Colonial, Linha 15's terminus, which OSM carries and
# which opened on 2021-12-29 (en.wikipedia "Line 15 (São Paulo Metro)": "11
# operational", read 2026-09-24): the agency layer is stale by one station,
# the case the brief anticipated for Lines 6 and 17.
GATE3_ADDED = {"15": ("JARDIM COLONIAL",)}
# One station under two spellings in OSM - an en dash and a hyphen - 6 m apart.
STATION_NAME_ALIASES = {"São Paulo – Morumbi": "São Paulo-Morumbi"}
SPACING_MIN_M = 400.0
COLLAPSE_MAX_SPREAD_M = 400
