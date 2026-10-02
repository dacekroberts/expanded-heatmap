"""Hakodate-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/hakodate.md
(10/10 checks, 2026-10-02). Part of the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py). Personal services only (Band B,
owner 2026-10-01: Yokohama's page): the city publishes only a rolling twelve
months of NEW food permits, which cannot rebuild a register, and MHLW's file
holds 65 of the 3,548 restaurant permits in force.

Business leg: the city's own CC BY 2.1 JP registers of barbers, beauty salons
and laundries (環境衛生関係施設等の情報), all as of 2026-08-31. 「抜粋」 is the
COLUMNS: the rows are complete (1,100 fixed premises against the official
1,122, e-Stat 衛生行政報告例 FY2024; a measurement, not drawn). Everything
placed by a JOIN to MLIT's 位置参照情報 for the one municipality (no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The Hakodate City Tram, JR's Hakodate Line and the South Hokkaido
Railway. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "hakodate" / "raw"
DATA_PROCESSED = ROOT / "data" / "hakodate" / "processed"
OUTPUTS = ROOT / "outputs" / "hakodate"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Hakodate"
SLUG = "hakodate"
MUNICIPALITY = "函館市"
PREFECTURE = "北海道"

# The 保健所 生活衛生課's page 「環境衛生関係施設等の情報」 (公開日 2026-09-10): its
# text and data under CC BY 2.1 JP, which the site default yields to. Each
# register is posted as CSV and PDF, 「…施設一覧（抜粋）」, 「令和8年8月31日時点」.
DATASET_PAGE = "https://www.city.hakodate.hokkaido.jp/docs/2019072900024/"
_FILES = f"{DATASET_PAGE}file_contents"
SOURCE_FILES = {
    "barber": ("202608riyo.csv", f"{_FILES}/202608riyo.csv", DATASET_PAGE),
    "beauty": ("202608biyo.csv", f"{_FILES}/202608biyo.csv", DATASET_PAGE),
    "laundry": ("R80831cleaning.csv", f"{_FILES}/R80831cleaning.csv", DATASET_PAGE),
}
# The registers' own date (令和8年8月31日時点), never the download's.
REGISTERS_AS_OF = "2026-08-31"
FOOD_AS_OF = None  # no food register is published
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: cp932 CSV with one or two title rows ABOVE the
# header (two in the barber and beauty files, one in the laundry file);
# japan_register.city_rows finds the header by its address column.
SOURCE_ENCODING = {"barber": "cp932", "beauty": "cp932", "laundry": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 開設者氏名 is REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; it is read IN MEMORY by that rule only, never kept. The barber and
# beauty files carry no type column (the source decides the bucket); the
# laundry file's 種別 is 取次 / 一般 / 無店舗 (3 storeless pick-ups, not a
# premises).
_REGISTER = ("施設名称", "施設所在地", "開設者氏名")
REQUIRED_COLUMNS = {"barber": _REGISTER, "beauty": _REGISTER, "laundry": (*_REGISTER, "種別")}

# The official count the registers were measured against (the brief, owner
# approved the download 2026-10-02): e-Stat 衛生行政報告例 FY2024, 生活衛生
# 第10表 (理容所 / 美容所) and 第11表 (クリーニング所), row 北海道函館市. A
# measurement only, never drawn; recorded by fetch_sources.py estat.
ESTAT_CONTROL = {
    "estat_riyo_biyo": ("estat_eisei_r6_riyo_biyo_by_city.csv",
                        "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359178&fileKind=1"),
    "estat_cleaning": ("estat_eisei_r6_cleaning_by_city.csv",
                       "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359179&fileKind=1"),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 01202.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and the city tram's stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 41.710, W 140.692, N 42.009, E 141.188:
# the 2004 merger's eastern towns included), rounded out; step 1 stops if the
# city leaves it.
OSM_BBOX = (41.69, 140.68, 42.02, 141.2)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae, 駅前 as
# -ekimae, 町 joined (Matsuyama's Kayamachi). OSM's tram stops mix macrons,
# title case and spaces, drop the 町 or 前 of two (千歳町, 中央病院前), and
# half-translate one (函館どつく前). 函館アリーナ前 is N02's name for the stop the
# operator now signs 「アリーナ前（函館サーモン・まるなまアリーナ前）」: the English
# follows N02's Japanese, shown beside it, and leaves out the naming-rights
# name, which changes with its sponsor.
OSM_NAME_EN_OVERRIDES = {
    "青柳町": "Aoyagicho",                           # Aoyagichō
    "千歳町": "Chitosecho",                          # Chitose
    "中央病院前": "Chuo-byoin-mae",                   # Chūō Byōin
    "深堀町": "Fukaboricho",                         # Fukaborichō
    "五稜郭公園前": "Goryokaku-koen-mae",              # Goryokaku-Koen-Mae
    "五稜郭": "Goryokaku",                           # Goryōkaku
    "函館どつく前": "Hakodate-dokku-mae",              # Hakodate Dock-Mae
    "函館アリーナ前": "Hakodate-arena-mae",            # Hakodate-Arena Mae
    "函館駅前": "Hakodate-ekimae",                    # Hakodateekimae
    "堀川町": "Horikawacho",                         # Horikawachō
    "宝来町": "Horaicho",                            # Hōrai-Chō
    "柏木町": "Kashiwagicho",                        # Kashiwagichō
    "競馬場前": "Keibajo-mae",                        # Keibajo-Mae
    "桔梗": "Kikyo",                                 # Kikyō
    "駒場車庫前": "Komaba-shako-mae",                 # Komaba-Shako Mae
    "松風町": "Matsukazecho",                        # Matsukazechō
    "新川町": "Shinkawacho",                         # Shinkawa-Chō
    "市役所前": "Shiyakusho-mae",                     # Shiyakusho Mae
    "昭和橋": "Showabashi",                          # Shōwa-Bashi
    "末広町": "Suehirocho",                          # Suehirochō
    "杉並町": "Suginamicho",                         # Suginamichō
    "魚市場通": "Uoichibadori",                       # Uoichibadōri
    "湯の川温泉": "Yunokawa-onsen",                   # Yunokawa-Onsen
    "大町": "Omachi",                                # Ōmachi
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~140.73) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# HALVED, on the spacing rule (docs/ring_rules.md: the halved edges where the
# median station gap is about 550 m or less): step 1 measured 363 m among the
# 29 in-city stations, 26 of them the city tram's stops (2026-10-02), as
# Hiroshima's 357 m and Matsuyama's 374 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# Gate 1's floor: Hiroshima's, Matsuyama's, Paris's and Riga's 200 m, not a
# new number - a tram network is genuinely closer than 400 m (collapsed median
# 363 m; platforms 340 m).
SPACING_MIN_M = 200.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 6 legal lines, no Shinkansen station inside): the city tram's
# four sections (all wholly inside), JR's Hakodate Line (3 of 84: 函館, 五稜郭,
# 桔梗) and the South Hokkaido Railway (1 of 12), cut at the city line (owner
# 2026-09-24). Every station is in the pre-2004 city; the merged eastern towns
# have none.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the city tram under four LEGAL
# sections (本線, 湯の川線, 宝来・谷地頭線, 大森線) that no rider reads; the operator
# runs routes 2 (湯の川 - 谷地頭) and 5 (湯の川 - 函館どつく前) over them, sharing
# the track from 湯の川 to 十字街. Drawn as ONE line under the tram's public name,
# on Sapporo's precedent for its streetcar (and Matsuyama's, the brief's
# recommendation). The South Hokkaido Railway keeps one station inside, 五稜郭
# (1 of 12): a one-station stub, which stays as cut (owner 2026-09-27).
_HC, _JR, _SH = "函館市", "北海道旅客鉄道", "道南いさりび鉄道"
LINES = {
    "TR": {"n02": [(_HC, "本線"), (_HC, "湯の川線"), (_HC, "宝来・谷地頭線"), (_HC, "大森線")],
           "name": "Hakodate City Tram", "name_ja": "函館市電", "short": "City Tram", "hue": "#2E8B57"},
    "JH": {"n02": [(_JR, "函館線")], "name": "JR Hakodate Line", "name_ja": "函館線", "short": "JR", "hue": "#00A651"},
    "SH": {"n02": [(_SH, "道南いさりび鉄道線")], "name": "South Hokkaido Railway", "name_ja": "道南いさりび鉄道線",
           "short": "Isaribi", "hue": "#00A0E9"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# hakodate` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Closest pair 50.3 (the tram / JR);
# the dark-mode labels separate, 3 of 3.
_COLOURS = {"TR": "#586818", "JH": "#28A800", "SH": "#08A0C0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own count for the line wholly inside the city: the
# city tram's per-stop timetable index (函館市企業局, docs/2014012100939/, time/T/01
# to 26) lists 26 stops (the brief's check, re-run 2026-10-02). JR's and the
# South Hokkaido Railway's lines are cut at the city line.
GATE3 = {"source": "the Hakodate City Tram's per-stop timetable index (26 stops)", "lines": {"TR": 26}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
HAKODATE_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = HAKODATE_BBOX
