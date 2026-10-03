"""São Paulo-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Brazil's first city. The business leg is IBGE's CNEFE 2022 - the census's own
walk of every block, one row per use-type per address, with the enumerator's
coordinate - so there is no register and no geocoder. Brief:
docs/build_briefs/sao-paulo.md; the country: docs/global_country_shortlist.md.

Pinned at step 2 overnight on 2026-09-24 over who writes the ONE shared
national classifier; unpinned the same morning when the owner gave it to this
build session. It is pipeline/taxonomies/brazil_cnefe.py, read through
pipeline/countries/brazil_register.py - nothing about CNEFE is São Paulo's own
except which zip to read.
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
# The unclassifiable rows' POINTS and rule label - never their text - for
# build_check.py's measure of where the dropped fifth sits.
UNCLASSIFIED_CSV = DATA_PROCESSED / "cnefe_unclassified.csv"

TAXONOMY_SYSTEM = "brazil_cnefe"

CNEFE_ZIP = DATA_RAW / "3550308_SAO_PAULO.zip"
CNEFE_ZIPS = (CNEFE_ZIP,)   # one município; a regional page lists several
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
OSM_RAIL_JSON = DATA_RAW / "osm_rail.json"
OSM_TRAIN_JSON = DATA_RAW / "osm_train.json"          # CPTM, for Line 9
OSM_MUNICIPIOS_JSON = DATA_RAW / "osm_municipios.json"  # names an excluded station
OSM_L17_BRANCH_JSON = DATA_RAW / "osm_l17_branch.json"  # Washington Luís, by id
GEOSAMPA_STATIONS_JSON = DATA_RAW / "geosampa_estacao_metro.json"
GEOSAMPA_TRAIN_STATIONS_JSON = DATA_RAW / "geosampa_estacao_trem.json"

# --- Endpoints ---------------------------------------------------------------

CNEFE_URL = ("https://ftp.ibge.gov.br/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/"
             "Censo_Demografico_2022/Arquivos_CNEFE/CSV/Municipio/35_SP/3550308_SAO_PAULO.zip")
# GeoSampa's OPERATING metro stations - for STATUS and the gate-3 count only,
# never drawn (the owner's 2026-09-23 decision: its licence is ambiguous).
GEOSAMPA_STATIONS_URL = ("https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/ows?service=WFS"
                         "&version=2.0.0&request=GetFeature&typeNames=geoportal:estacao_metro"
                         "&outputFormat=application/json")
# CPTM's operating stations, for Line 9's STATUS and gate-3 count only - the
# same rule as the metro layer above.
GEOSAMPA_TRAIN_STATIONS_URL = ("https://wfs.geosampa.prefeitura.sp.gov.br/geoserver/ows?service=WFS"
                               "&version=2.0.0&request=GetFeature&typeNames=geoportal:estacao_trem"
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
# Draw subway refs 1-5 and monorail refs 15 and 17. Ref 6 (Laranja) is in
# OSM but only in GeoSampa's PLANNED layer - Tel Aviv's trap - and step 1
# STOPS the day it appears in the operating layer, so it is added
# deliberately.
#
# LINHA 17-OURO DRAWN (owner, 2026-10-03: "investigate and then draw"). The
# monorail has carried passengers since 2026-03-31, Morumbi to Aeroporto de
# Congonhas, with Washington Luís added on 2026-06-30; from 2026-09-30 it runs
# 06:00-22:00 Monday to Saturday, still fare-free in "operação transitória",
# run by Metrô (metro.sp.gov.br's Linha 17-Ouro page lists eight stations,
# read 2026-10-03). GeoSampa's operating layer still lacks it (re-read
# 2026-10-03, unchanged since 2026-09-24), so gate 3 takes Metrô's eight
# (GATE3_ADDED below). Linha 6's first six stations have been in free
# assisted operation on weekdays 10:00-15:00 since 2026-07-03; they stay out
# pending the owner's call (docs/decisions_drafts/lane-rail.md, 2026-10-03).
#
# CPTM - LINE 9 DRAWN, THE REST NOT: the owner's call of 2026-09-24, on the
# DART / S-tog test (spacing and frequency inside the city, and districts the
# metro does not reach) that Rome's Roma-Viterbo urban service passed the same
# morning. Measured from OSM's route relations: Line 9-Esmeralda has 19
# stations in the município, median 1,778 m apart (S-tog 1,227; Metromare,
# left out, 2,171), a train every 4.5 minutes at peak on its core and about 7
# elsewhere, and 16 of the 19 with no metro station within 800 m - the
# Pinheiros river corridor, Vila Olimpia, Berrini, Santo Amaro. Lines 7, 8,
# 10, 11 and 12 fail on spacing (medians 2.1-3.4 km in the city); 13 and the
# Expresso Aeroporto have one to three stops here. Line 9's two stations in
# Osasco are recorded as excluded, like any station outside the município.
DRAW_REFS = {"subway": ("1", "2", "3", "4", "5"), "monorail": ("15", "17"), "train": ("9",)}
NOT_YET_OPEN_REFS = ("6",)
# CPTM lines measured and left out - step 1 stops on any OTHER train relation.
CPTM_NOT_DRAWN = ("7", "8", "10", "11", "12", "13", None)   # None: Expresso Aeroporto
LINE_ORDER = ("1", "2", "3", "4", "5", "15", "17", "9")
LINE_NAMES = {"1": "Linha 1-Azul", "2": "Linha 2-Verde", "3": "Linha 3-Vermelha",
              "4": "Linha 4-Amarela", "5": "Linha 5-Lilás", "15": "Linha 15-Prata",
              "17": "Linha 17-Ouro", "9": "Linha 9-Esmeralda"}
# OSM's colours (GeoSampa carries none), measured 2026-09-24 against the pins:
# all clear the floor unchanged; Linha 1 is 13.7 from Retail and recorded, as
# agency colours below the preferred 45 are. Linha 3's two direction relations
# disagree (#ef3f32 / #D9001C, 10.5 apart); the first relation's is taken.
# Line 9 is OSM's #00A88E, unchanged: 15.4 from the Personal services pins and
# 15.5 from Linha 2, both clear of the floor (measured 2026-09-24).
# Linha 17 is OSM's #DE7C00 on both direction relations, unchanged: 72.1 from
# the Food service pins (the nearest), 40.4 from Linha 3 across the city and
# 46.1 from Linha 4; 3.0:1 on the light page (measured 2026-10-03).
LINE_COLOURS = {"1": "#1266af", "2": "#008162", "3": "#ef3f32", "4": "#FFD700",
                "5": "#9200C3", "15": "#7b9192", "17": "#DE7C00", "9": "#00A88E"}
# Gate 3: GeoSampa's operating layer, 85 distinct stations (brief, 2026-09-23);
# re-counted from the cached layer at every run - with ONE recorded correction.
# The layer lacks Jardim Colonial, Linha 15's terminus, which OSM carries and
# which opened on 2021-12-29 (en.wikipedia "Line 15 (São Paulo Metro)": "11
# operational", read 2026-09-24): the agency layer is stale by one station,
# the case the brief anticipated for Lines 6 and 17. Linha 17 is absent from
# the layer altogether: its eight are Metrô's own list (the Linha 17-Ouro page,
# read 2026-10-03), and step 1 stops once GeoSampa lists any of them.
GATE3_ADDED = {"15": ("JARDIM COLONIAL",),
               "17": ("MORUMBI", "CHUCRI ZAIDAN", "VILA CORDEIRO", "CAMPO BELO",
                      "VEREADOR JOSE DINIZ", "BROOKLIN PAULISTA", "AEROPORTO DE CONGONHAS",
                      "WASHINGTON LUIS")}
# WASHINGTON LUÍS, LINHA 17's BRANCH STATION (open since 2026-06-30), is in
# neither of OSM's Linha 17 route relations (re-fetched 2026-10-03): its stop
# nodes still carry construction=station and its track is not a member. It is
# added BY ID from OSM itself (Sacramento's ADDED_STATIONS rule, with OSM
# rather than Wikidata because OSM has the objects): the stop position, and
# the branch way from the junction east of Brooklin Paulista. Step 1 STOPS
# once a Linha 17 relation carries a stop of this name, so the entry retires
# itself.
L17_BRANCH = {"station": "Washington Luís", "stop_node": 12343720433, "way": 671909900}
# One station under two spellings in OSM - an en dash and a hyphen - 6 m apart.
# Linha 17's Morumbi is the interchange with CPTM's "Morumbi - Claro" (Metrô
# lists it as integrated with Linha 9), 171 m apart: one station, under the
# name the map already showed, as Santo Amaro (257 m) and Pinheiros (194 m)
# are one each.
STATION_NAME_ALIASES = {"São Paulo – Morumbi": "São Paulo-Morumbi",
                        "Morumbi": "Morumbi - Claro"}
SPACING_MIN_M = 400.0
COLLAPSE_MAX_SPREAD_M = 400
