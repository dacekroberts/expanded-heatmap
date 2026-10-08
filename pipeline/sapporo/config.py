"""Sapporo-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

The brief is docs/build_briefs/sapporo.md (corrected 2026-09-28, 5/5 checks).
Japan's third city, on the shared modules Kobe built: pipeline/countries/
japan.py (rail, city line), japan_register.py (the address join),
japan_step1.py, japan_step2.py and japan_fetch.py. This file holds only what
is Sapporo's.

Business leg: Sapporo City's 札幌市内の食品営業許可施設一覧 (the food-permit
list, as of 2026-03-31) and its 札幌市内の環境衛生営業施設一覧 registers -
barber, beauty, cleaning and coin laundry (2026-07-31) - from the city's own
CKAN, placed by a JOIN to MLIT's 位置参照情報 for the 10 wards. On Sapporo's 条
grid a 条丁目 is about one block, so the town-chōme tier is near block
precision here.

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen left out (none reaches
Sapporo yet), stations kept only inside the city line (N03). English station
names from OpenStreetMap's name:en (owner, 2026-09-27).
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "sapporo" / "raw"
DATA_PROCESSED = ROOT / "data" / "sapporo" / "processed"
OUTPUTS = ROOT / "outputs" / "sapporo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Sapporo"
SLUG = "sapporo"
MUNICIPALITY = "札幌市"
PREFECTURE = "北海道"

# Sapporo's own CKAN (ckan.pf-sapporo.jp), each dataset CC BY 4.0 (read
# 2026-09-24; the registers' package re-read 2026-09-28). Fetch from this host
# ONLY: the city website's copies fall under its copyright page (brief). The
# files are the editions this build read, pinned, never "the newest".
CKAN = "https://ckan.pf-sapporo.jp/dataset"
_FOOD = f"{CKAN}/be44af14-f135-41b9-acca-08e215d8a540"
_REG = f"{CKAN}/0be3aa70-e0b3-4ac1-8674-35e995195627"
FOOD_AS_OF = "2026-03-31"
REGISTERS_AS_OF = "2026-07-31"
# source key -> (file, URL, the page that links it and carries its licence)
SOURCE_FILES = {
    "food": ("shokuhin260331.csv",
             f"{_FOOD}/resource/54618ac4-da90-493c-8a20-8df29be9d435/download/shokuhin260331.csv",
             "https://ckan.pf-sapporo.jp/dataset/sapporo_food_business_licences"),
    "barber": ("sapporo-eigyoshisetsu-riyo-r80731.csv",
               f"{_REG}/resource/c1edfb53-2440-4cda-9007-e76962d3d5eb/download/sapporo-eigyoshisetsu-riyo-r80731.csv",
               "https://ckan.pf-sapporo.jp/dataset/sapporo_environmental_hygiene_services"),
    "beauty": ("sapporo-eigyoshisetsu-biyo-r80731.csv",
               f"{_REG}/resource/78e5ffc3-19ac-4836-9bc6-fdd48d6104a9/download/sapporo-eigyoshisetsu-biyo-r80731.csv",
               "https://ckan.pf-sapporo.jp/dataset/sapporo_environmental_hygiene_services"),
    "laundry": ("sapporo-eigyoshisetsu-cleaning-r80731.csv",
                f"{_REG}/resource/4fe5d75d-2f5b-4f6d-8f36-ca91788ff23f/download/"
                "sapporo-eigyoshisetsu-cleaning-r80731.csv",
                "https://ckan.pf-sapporo.jp/dataset/sapporo_environmental_hygiene_services"),
    # Coin laundries count, in Personal services (owner 2026-09-28): near
    # transit they draw steady short-term customers. Kobe and Osaka had none.
    "coinlaundry": ("sapporo-eigyoshisetsu-coinlaundry-r80731.csv",
                    f"{_REG}/resource/2e6f12c9-9e19-4b8d-a3f7-c588c9b2df0c/download/"
                    "sapporo-eigyoshisetsu-coinlaundry-r80731.csv",
                    "https://ckan.pf-sapporo.jp/dataset/sapporo_environmental_hygiene_services"),
}
# The key is the taxonomy's `source` column.
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred (docs/data_sources.md): all five are UTF-8 with a
# BOM, comma-separated (read 2026-09-28). japan_register.decode() reads them.
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 申請者名 (food) and 開設者名 (registers) are read IN
# MEMORY by the name rule only (japan_register.name_is_operator; owner
# 2026-09-27) and never kept. 開設者住所 (an operator's own address), 開設者ﾋﾞﾙ名,
# 開設者TEL and 施設TEL are never selected.
_REGISTER_COLUMNS = ("業種区分", "施設名称", "施設所在地")
REQUIRED_COLUMNS = {
    "food": ("屋号", "業種名", "施設所在地"),
    "barber": _REGISTER_COLUMNS,
    "beauty": _REGISTER_COLUMNS,
    "laundry": _REGISTER_COLUMNS,
    "coinlaundry": _REGISTER_COLUMNS,
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (42.781-43.190 N, 140.991-141.505 E,
# measured 2026-09-28) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (42.75, 140.95, 43.22, 141.55)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
# The streetcar's stops: OSM tags them railway=tram_stop, which the station
# query does not take (Osaka's Hankai lesson; japan.osm_tram_stop_query).
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
# How far an OSM station object may be from N02's group centroid and still name
# it (as Kobe and Osaka).
OSM_NAME_MATCH_M = 600
# Where OSM's objects for one station disagree on name:en, the spelling taken:
# the operators' own signs. Filled from step 1's report.
OSM_NAME_EN_TIES = {}
# Where OSM's object has NO name:en, the English name taken instead - explicit
# and cited, never inferred; step 1 still stops on any station missing here.
OSM_NAME_EN_MISSING = {}
# Sapporo's 条 is a numbered street grid (北18条, 西線9条, 山鼻19条), so
# japan_step1 requires its numbers as figures in the English names, as it does
# every 丁目 (owner 2026-09-28). Off a grid 条 is a name (Osaka's Kujō).
JO_IS_GRID = True
# Cited overrides of OSM's name:en (owner 2026-09-28: a cited override table;
# numerals as figures in every Japanese city, especially before 丁目 / 条, which
# japan_step1 now enforces). OSM's Sapporo objects mix two styles: hyphenated
# title case with its own numeral form ("Kita-13-Jo-Higashi", "Nango-13-Chome",
# "Nakajima-Kōen-Dōri") and spelled-out lowercase ("Kita juhachi jo"). Each
# entry takes the first style; the comment is the OSM spelling it replaces
# (osm_station_names.json / osm_tram_stop_names.json, 2026-09-28). The
# operator's English pages were not reachable (city.sapporo.jp/st/english:
# 404, 2026-09-28; its route maps are images), so they are not the citation.
OSM_NAME_EN_OVERRIDES = {
    # numbers before 条 / 丁目, as figures
    "北34条": "Kita-34-Jo",                      # Kita sanjuyo jo
    "北24条": "Kita-24-Jo",                      # Kita nijuyo jo
    "北18条": "Kita-18-Jo",                      # Kita juhachi jo
    "北12条": "Kita-12-Jo",                      # Kita juni jo
    "西28丁目": "Nishi-28-Chome",                # Nishi nijuhatchome
    "西18丁目": "Nishi-18-Chome",                # Nishi juhatchome
    "西15丁目": "Nishi-15-Chome",                # Nishi jugo chome
    "西11丁目": "Nishi-11-Chome",                # Nishi juitchome
    "西8丁目": "Nishi-8-Chome",                  # Nishi hatchome
    "西4丁目": "Nishi-4-Chome",                  # Nishi yon chome
    "南郷7丁目": "Nango-7-Chome",                # Nango nanachome
    "西線6条": "Nishisen-6-Jo",                  # Nishisen-Roku-Jō
    "西線9条旭山公園通": "Nishisen-9-Jo Asahiyama-Kōen-Dōri",  # Nishisen-Ku-Jō Asahiyama-Kōen-Dōri
    "西線11条": "Nishisen-11-Jo",                # Nishisen-Jūichi-Jō
    "西線14条": "Nishisen-14-Jo",                # Nishisen-Jūyo-Jō
    "西線16条": "Nishisen-16-Jo",                # Nishisen-Jūroku-Jō
    "山鼻9条": "Yamahana-9-Jo",                  # Yamahana-Ku-Jō
    "山鼻19条": "Yamahana-19-Jo",                # Yamahana-Jūku-Jō
    # spelled-out lowercase, into the same style
    "円山公園": "Maruyama-Kōen",                 # Maruyama koen
    "豊水すすきの": "Hōsui-Susukino",            # Hosui Susukino
    "中央区役所前": "Chūō-Kuyakusho-Mae",        # Chuo kuyakusho mae
    "東区役所前": "Higashi-Kuyakusho-Mae",       # Higashi kuyakusho mae
    "環状通東": "Kanjō-Dōri-Higashi",            # Kanjo dori higashi
    "新道東": "Shindō-Higashi",                  # Shindo higashi
    "豊平公園": "Toyohira-Kōen",                 # Toyohira koen
    "東札幌": "Higashi-Sapporo",                 # Higashi Sapporo
    "新さっぽろ": "Shin-Sapporo",                # Shin Sapporo (the subway's; JR's 新札幌 is Shin-Sapporo too)
    "中島公園": "Nakajima-Kōen",                 # Nakajima-Koen (its streetcar stop is Nakajima-Kōen-Dōri)
    "月寒中央": "Tsukisamu-Chūō",                # Tsukisamu-Chuo
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~141.35) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test, 2026-09-28: 10
# N02 lines). The three subway lines and every streetcar section are 100%
# inside. JR Hokkaido is cut at the city line (owner 2026-09-24): Hakodate
# 14 of 84, Chitose 4 of 15, Sasshō (Gakuen Toshi) 10 of 14 - suburban lines,
# so no URBAN line is cut to a stub.
LEFT_OUT_LINES = {}
# Kobe's 300 m until step 1's report shows a wider real interchange.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 (operator, line) pairs it is drawn from, its real public name
# (English, then Japanese), and its colour. N02 files the streetcar's one loop
# (札幌市電, operated by 一般社団法人札幌市交通事業振興公社 since 2020) as four
# legal sections - 1条線, 都心線, 山鼻西線, 山鼻線 - drawn here as one line under
# its public name (Kobe's trap 2). 札沼線 is JR Hokkaido's Gakuen Toshi Line.
#
# COLOURS: the project's own, not the operators' (Kobe's and Osaka's rule;
# 2026-09-28). A search over the sRGB cube (step 8; 3,817 feasible colours):
# 3:1 against BOTH map pages (#0B1220 and #ffffff), CIE76 >= 45 against every
# category pin, >= 18 between lines, each nearest its operator's hue
# (lightness weighted half). Result: pins 45.0-74.8, closest line pair 18.2
# (the Tozai Line and JR Chitose, both orange). The streetcar left green for
# olive (#586818) and the Gakuen Toshi Line blue for violet (#8858F0) to fit.
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search: the
# streetcar's #586818 sat 15.8 from it, under the owner's floor of 20
# (2026-10-07), and moved to #506C30, a greener olive: the colour nearest its
# own that reads 3:1 on both pages and clears 25 from every pin and 18 from
# every other line (olive 25.6, nearest line JR Hakodate Main 40.0). Four of
# seven lines sit between 20 and 45 from olive (JR Hakodate Main #70A000 24.5,
# the streetcar 25.6, Namboku 41.4, JR Chitose 43.0), an accepted trade
# (owner, 2026-10-07).
_JR, _SC, _STR = "北海道旅客鉄道", "札幌市", "一般社団法人札幌市交通事業振興公社"
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    # Sapporo Municipal Subway (札幌市交通局)
    "N": {"n02": [(_SC, "南北線")], "name": "Namboku Line", "name_ja": "南北線", "colour": "#40A800",
          "short": "Subway"},
    "T": {"n02": [(_SC, "東西線")], "name": "Tōzai Line", "name_ja": "東西線", "colour": "#E87000",
          "short": "Subway"},
    "H": {"n02": [(_SC, "東豊線")], "name": "Tōhō Line", "name_ja": "東豊線", "colour": "#0050F0",
          "short": "Subway"},
    # The streetcar
    "SC": {"n02": [(_STR, "1条線"), (_STR, "都心線"), (_STR, "山鼻西線"), (_STR, "山鼻線")],
           "name": "Sapporo Streetcar", "name_ja": "札幌市電", "colour": "#506C30", "short": "Streetcar"},
    # JR Hokkaido (北海道旅客鉄道)
    "JH": {"n02": [(_JR, "函館線")], "name": "JR Hakodate Main Line", "name_ja": "函館本線", "colour": line_registry.colour("jr-hokkaido-hakodate-main-line"),
           "short": "JR"},
    "JC": {"n02": [(_JR, "千歳線")], "name": "JR Chitose Line", "name_ja": "千歳線", "colour": "#D08000",
           "short": "JR"},
    "JG": {"n02": [(_JR, "札沼線")], "name": "JR Gakuen Toshi Line", "name_ja": "学園都市線", "colour": "#8858F0",
           "short": "JR"},
}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}

# Branches inside one N02 line: none known before step 1's report.
BRANCHES = {}

# Gate 3: the operator's own station counts, from the Sapporo Municipal Subway's
# station numbering: Namboku N01 Asabu to N16 Makomanai; Tōzai T01 Miyanosawa
# to T19 Shin-Sapporo; Tōhō H01 Sakaemachi to H14 Fukuzumi. Every one is inside
# the city.
GATE3 = {"source": "Sapporo Municipal Subway station numbering (N01-N16, T01-T19, H01-H14)",
         "lines": {"N": 16, "T": 19, "H": 14}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"
# This taxonomy also classifies by source: keep those raw column(s) through step 2
# (they are passed to classify() by filter_to_storefront() and the map).

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SAPPORO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SAPPORO_BBOX
