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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600421151)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("pt",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Shopping": "a Metrô-DF station, railway=station: the station's real name; the read of 2026-10-13",
}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/41648328": "a bus terminal in as a station, not rail",
    "way/1518011455": "a closed historic station building with no service",
    "way/615487657": "a single private plot tagged a quarter",
    "way/584475816": "a condominium's own residents' playground or square",
    "way/584447411": "a condominium's own residents' playground or square",
    "way/141491292": "a religious residence with no article",
    "node/10537673186": "a religious residence with no article",
    "node/4872524375": "a religious residence with no article",
    "node/2587338138": "a religious residence with no article",
    "way/237170559": "a religious residence with no article",
    "node/7775578148": "a religious residence with no article",
    "node/10537673185": "a religious residence with no article",
    "way/287693649": "a school tagged a place of worship",
    "way/447471796": "a private school's own gym or lawn",
    "way/543967495": "a private school's own gym or lawn",
    "node/6285091986": "a motorcycle club tagged a place of worship",
    "node/10538295099": "a newsstand described, tagged a park",
    "way/1370435572": "a name or tag that says the thing is gone or abandoned",
    "way/1207555626": "a name or tag that says the thing is gone or abandoned",
    "node/6562137812": "a name or tag that says the thing is gone or abandoned",
    "way/959202158": "a name or tag that says the thing is gone or abandoned",
    "node/14097362561": "a vehicle shown as a monument, no article of its own",
    "node/12891955690": "public art with no Wikipedia article of its own",
    "node/12399086060": "public art with no Wikipedia article of its own",
    "node/12399505347": "public art with no Wikipedia article of its own",
    "node/8115231044": "public art with no Wikipedia article of its own",
    "node/6377081578": "a plaque, sign or marker with no Wikipedia article of its own",
    "way/672792999": "a plaque, sign or marker with no Wikipedia article of its own",
    "way/1370237495": "a plaque, sign or marker with no Wikipedia article of its own",
    "node/2675388250": "a plaque, sign or marker with no Wikipedia article of its own",
    "node/6736597596": "a plaque, sign or marker with no Wikipedia article of its own",
    "node/5359225214": "a description standing in for a name",
    "way/749086648": "a description standing in for a name",
    "way/1082342811": "a description standing in for a name",
    "way/556003461": "a description standing in for a name",
    "node/12194857401": "a description standing in for a name",
    "way/867728038": "a description standing in for a name",
    "way/867728037": "a description standing in for a name",
    "way/867728036": "a description standing in for a name",
    "way/1421924164": "a description standing in for a name",
    "way/553836942": "a description standing in for a name",
    "way/1320017690": "a description standing in for a name",
    "node/6554200925": "a street name standing in for a place of worship's name",
    "node/6558530436": "a glitched name: a rating glued on",
    "way/968759159": "a glitched name: words glued together",
    "node/6554200926": "a glitched name: cut short",
    "node/7474790272": "a glitched name: cut short",
    "node/6556441905": "a glitched name: a second name glued on with a pipe",
    "way/560093699": "a glitched name: not a word",
    "way/681457635": "a glitched name: two codes run together",
    "way/962408464": "a glitched name: an English rendering of the park beside it",
    "node/6970030018": "a glitched name: a wrong word changes the name",
    "node/6566575511": "a duplicate row of the same object, the weaker one",
    "way/1355788332": "a duplicate row of the same object, the weaker one",
    "way/235301174": "a duplicate row of the same object, the weaker one",
    "way/227529528": "a duplicate row of the same object, the weaker one",
    "way/246902093": "a duplicate row of the same object, the weaker one",
    "node/11248442537": "a duplicate row of the same object, the weaker one",
    "way/1127933982": "a description standing in for a name",
    "way/1127933983": "a description standing in for a name",
    "way/474855125": "a description standing in for a name",
    "way/474855397": "a description standing in for a name",
    "way/474855468": "a description standing in for a name",
    "way/474855546": "a description standing in for a name",
    "way/474855668": "a description standing in for a name",
    "way/474855809": "a description standing in for a name",
    "way/474856768": "a description standing in for a name",
    "way/474857601": "a description standing in for a name",
    "way/474858290": "a description standing in for a name",
    "way/474858573": "a description standing in for a name",
    "way/474858994": "a description standing in for a name",
    "way/1054098704": "a description standing in for a name",
    "way/430371827": "a description standing in for a name",
    "way/1014062863": "an address number range standing in for a name",
    "way/140616817": "a mall food court",
    "way/1388864199": "a description standing in for a name",
    "way/1388864198": "a description standing in for a name",
    "way/584474414": "a condominium residents road",
    "way/240210437": "a shopping strip named for a condominium",
    "way/246554383": "a shopping strip named for a condominium",
    "way/676431728": "a shopping strip named for a condominium",
    "way/676431731": "a shopping strip named for a condominium",
    "way/245345032": "a bare type word",
    "way/245345033": "a bare type word",
    "way/629321126": "a bare type word",
    "way/629321712": "a bare type word",
    "way/240209130": "a bare type word",
    "way/470238313": "a description standing in for a name",
    "way/300885859": "a description standing in for a name",
    "way/300885860": "a description standing in for a name",
    "way/390488167": "a facility's own road",
    "way/390488024": "a facility's own road",
    "way/145483075": "a description standing in for a name",
    "way/1033980603": "a condominium residents road",
    "way/1033980604": "a condominium residents road",
    "way/257675590": "a condominium residents road",
    "way/257675591": "a condominium residents road",
    "way/257675593": "a condominium residents road",
    "way/295246451": "a condominium residents road",
    "way/418227673": "a condominium residents road",
    "way/974302547": "a condominium residents road",
    "way/278877767": "an institution's own road",
    "way/543019108": "an institution's own road",
    "way/543019109": "an institution's own road",
    "way/1059657363": "a description standing in for a name",
    "way/306336037": "a description standing in for a name",
    "way/309459087": "a description standing in for a name",
    "way/1203826288": "a hospital's own road",
    "way/391229790": "a building corridor",
    "way/490348253": "a building corridor",
    "way/501857832": "a campus building corridor",
    "way/1268182641": "a private condominium road",
    "way/1554047529": "a private condominium road",
    "way/1207642208": "a private estate road",
    "way/1207642209": "a private estate road",
    "way/442872553": "a private estate road",
    "way/442872554": "a private estate road",
    "way/1290270301": "an estate road",
    "way/159759101": "an estate road",
    "way/159759108": "an estate road",
    "way/159759110": "an estate road",
    "way/159759183": "an estate road",
    "way/245015857": "an estate road",
    "way/422706896": "an estate road",
    "way/422726976": "an estate road",
    "way/782067513": "an estate road",
    "way/782175173": "an estate road",
    "way/240210260": "a glitched name (typo)",
    "way/331604821": "a glitched name (typo)",
    "way/481458155": "a glitched name (typo)",
}
