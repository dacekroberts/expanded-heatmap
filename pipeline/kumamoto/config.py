"""Kumamoto-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kumamoto.md
(12/12 checks, 2026-10-02). Built in the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py): Hiroshima's two-source shape for
food, plus personal services.

Business leg: the city's own list of restaurants applied for at a counter
(窓口), 食品衛生法に基づく飲食店営業許可施設一覧, as of 2026-03-31 (PDL 1.0;
opt-outs and vehicles left out by the city), plus MHLW's 食品衛生申請等システム
open data for the online filings the city's list leaves out (opt-in, field by
field): its restaurant permits, and its other permits and notifications as the
partial food-retail bucket. A premises in both is shown once
(config.SUPERSEDES). The city's barber, beauty and laundry lists (CC BY 4.0,
2026-03-31) complete the third bucket. All placed by a JOIN to MLIT's
位置参照情報 for the five wards; where the block join misses an MHLW row,
MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The city tram, Kumamoto Electric Railway's two lines and JR Kyushu's
Kagoshima and Hohi lines. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kumamoto" / "raw"
DATA_PROCESSED = ROOT / "data" / "kumamoto" / "processed"
OUTPUTS = ROOT / "outputs" / "kumamoto"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kumamoto"
SLUG = "kumamoto"
MUNICIPALITY = "熊本市"
PREFECTURE = "熊本県"

# The city's open-data pages (熊本市オープンデータ, each 最終更新日 2026-09-14,
# 「令和8年（2026年）3月31日現在」), catalogued on BODIK. The restaurant list is
# PDL 1.0 (the page's badge, BODIK's 431001_seisaku20 and the catalogue's terms
# at odcs.bodik.jp/431001/tos/); the three registers' pages say CC BY 4.0 and
# BODIK lists them as PDL 1.0, either of which permits this use. The page's
# monthly new-permit workbooks are not added (Hiroshima's precedent: the
# annual full list is the snapshot).
_OD = "https://www.city.kumamoto.jp/dynamic/opendata/pub"
FOOD_PAGE = f"{_OD}/detail.aspx?c_id=38&id=60"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "food": ("Insyokutenneigyoukyoka.csv", f"{_OD}/Insyokutenneigyoukyoka.csv", FOOD_PAGE),
    "mhlw": ("43100_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=43100_food_business_all.csv",
             MHLW_TOP),
    "barber": ("riyoujo_list.xlsx", f"{_OD}/riyoujo_list.xlsx", f"{_OD}/detail.aspx?c_id=38&id=50"),
    "beauty": ("biyoujo_list.xlsx", f"{_OD}/biyoujo_list.xlsx", f"{_OD}/detail.aspx?c_id=38&id=51"),
    "laundry": ("kurininngujyo-list.xlsx", f"{_OD}/kurininngujyo-list.xlsx", f"{_OD}/detail.aspx?c_id=38&id=52"),
}
# The lists' own date (Kyoto's rule: the date the list states, never the
# download's): 「令和8年（2026年）3月31日現在」 on every city page; MHLW's monthly
# file states none. NO row of the city's list is dropped on 期限満了日: the
# page extends every permit expiring 2026-08-31 or 2026-11-30 to 2027-01-27
# (令和８年熊本地震に係る特定非常災害の指定), so its printed expiry is not the
# permit's.
SOURCE_AS_OF = {"food": "2026-03-31", "mhlw": None, "barber": "2026-03-31", "beauty": "2026-03-31",
                "laundry": "2026-03-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: the city's restaurant list and MHLW's file are
# UTF-8 with a BOM, comma-separated; the registers are XLSX, one sheet, header
# on row 1 (営業所所在地1, the premises, read; 営業所所在地2 / ２, the building,
# not needed by the join).
SOURCE_ENCODING = {"food": "utf-8-sig", "mhlw": "utf-8-sig", "barber": "xlsx", "beauty": "xlsx",
                   "laundry": "xlsx"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 申請者氏名, 開設者氏名 and 代表者氏名（法人のみ） are
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; they are read IN MEMORY by that
# rule only, never kept. Never selected: 備考 (it describes the glyphs of
# operators' names), 開設者住所1/2（法人のみ） (an operator's own address), the
# phones, 役職（法人のみ）, and MHLW's 法人名 / 法人番号 / 法人住所.
_REGISTER = ("施設名称", "営業所所在地1", "開設者氏名", "代表者氏名（法人のみ）")
REQUIRED_COLUMNS = {
    "food": ("業種", "屋号", "営業所所在地", "申請者氏名", "期限満了日"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": _REGISTER + ("クリーニング所形態",),
}
# As Fukuoka's and Hiroshima's (owner-approved wording, 2026-09-24): MHLW
# publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 33 m from the block point, 99.0% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both lists: the city's row goes, MHLW's stays (the brief:
# 12 of MHLW's 199 block-placed restaurants, 6.0%).
SUPERSEDES = {"mhlw": ("food",)}
# The share of the official restaurant count (e-Stat 衛生行政報告例 FY2024,
# 9,229) the two lists hold, measured every build (japan_step2.official_shares;
# Tokyo's rule: a share the page states is the one this build measured).
OFFICIAL_SHARES = True
MUNICIPALITY_CODES = {"熊本市": "43100"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and the city tram's stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 32.6603, W 130.5678, N 32.9799,
# E 130.8292), rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (32.65, 130.55, 32.99, 130.84)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-02): OSM adds a stop's bracketed landmark
# (蔚山町（護国神社前）), spells 祇園橋 with 祗 (Kyoto's 祇 / 祗 pair), and names
# the zoo stop 動植物園前 where N02 and the bureau write 動植物園入口.
OSM_NAME_ALIASES = {"蔚山町": "蔚山町（護国神社前）", "祇園橋": "祗園橋", "動植物園入口": "動植物園前"}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae. OSM
# TRANSLATED five stops (Fukuoka's trap), misspelled two (Shin-suizennji,
# Keitokuku) and wrote 西辛島町 as NishiKarashima chou; each is romanised here.
OSM_NAME_EN_OVERRIDES = {
    "本妙寺入口": "Honmyoji-iriguchi",                # Honmyoji Temple Entrance
    "熊本城・市役所前": "Kumamotojo-Shiyakusho-mae",   # Kumamoto Castle / City Hall
    "熊本駅前": "Kumamoto-ekimae",                    # Kumamoto Station
    "水前寺公園": "Suizenji-koen",                    # Suizenji Park
    "動植物園入口": "Doshokubutsuen-iriguchi",         # Zoological and Botanical Garden
    "新水前寺駅前": "Shin-Suizenji-ekimae",            # Shin-suizennji ekimae
    "西辛島町": "Nishi-Karashimacho",                 # NishiKarashima chou
    "慶徳校前": "Keitokuko-mae",                      # Keitokuku-mae
    "崇城大学前": "Sojo-daigaku-mae",                  # Sōjōdaigakumae
    "東海学園前": "Tokai-Gakuen-mae",                  # Tōkai-Gakuen-mae
    "神水交差点": "Kuwamizu-kosaten",                  # Kuwamizu Kosaten
    "九品寺交差点": "Kuhonji-kosaten",                 # Kuhonjikosaten
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~130.71) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# HALVED, on the spacing rule (docs/ring_rules.md: the halved edges where the
# median station gap is about 550 m or less): step 1 measured 362 m among the
# 61 in-city stations, 35 of them the city tram's stops (2026-10-02), as
# Matsuyama's 374 m and Hiroshima's 357 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# Gate 1's floor: Hiroshima's, Matsuyama's, Paris's and Riga's 200 m, not a
# new number - a tram network is genuinely closer than 400 m (collapsed median
# 362 m; platforms 314 m).
SPACING_MIN_M = 200.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 9 legal lines, no Shinkansen; 熊本 on the 九州新幹線 is dropped
# and stays a JR station): the city tram's five sections (all wholly inside),
# Kumamoto Electric's Fujisaki Line (3 of 3) and Kikuchi Line (9 of 16), and
# JR Kyushu's Kagoshima Main Line (9 of 99) and Hohi Line (9 of 37), cut at
# the city line (owner 2026-09-24). No line is cut to a stub. 光の森 sits 41 m
# inside the N03 line: its address is 熊本市北区武蔵ケ丘九丁目 (part of its
# grounds in 菊陽町), so the cut keeps it rightly (2026-10-02). JR's 三角線 has
# no station inside.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the city tram under five LEGAL
# sections (幹線, 水前寺線, 健軍線, 田崎線, 上熊本線), all wholly inside the
# city, that no rider reads; the bureau runs routes A (田崎橋 to 健軍町) and B
# (上熊本 to 健軍町) over them, sharing 19 stops from 辛島町 east. Drawn as ONE
# line under the tram's public name, Matsuyama's precedent (2026-10-02):
# drawing A and B would stack two lines on most of the track.
_KC, _KE, _JK = "熊本市", "熊本電気鉄道", "九州旅客鉄道"
LINES = {
    "TR": {"n02": [(_KC, "幹線"), (_KC, "水前寺線"), (_KC, "健軍線"), (_KC, "田崎線"), (_KC, "上熊本線")],
           "name": "Kumamoto City Tram", "name_ja": "熊本市電", "short": "City Tram", "hue": "#00A651"},
    "KK": {"n02": [(_KE, "菊池線")], "name": "Kumaden Kikuchi Line", "name_ja": "菊池線", "short": "Kumaden",
           "hue": "#E4007F"},
    "KF": {"n02": [(_KE, "藤崎線")], "name": "Kumaden Fujisaki Line", "name_ja": "藤崎線", "short": "Kumaden",
           "hue": "#E4007F"},
    "JK": {"n02": [(_JK, "鹿児島線")], "name": "JR Kagoshima Main Line", "name_ja": "鹿児島本線", "short": "JR",
           "hue": "#E60012"},
    "JH": {"n02": [(_JK, "豊肥線")], "name": "JR Hohi Line", "name_ja": "豊肥本線", "short": "JR", "hue": "#E60012"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kumamoto` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Closest pair 18.1 (JR's two
# lines, which share 熊本); the dark-mode labels separate, 5 of 5.
_COLOURS = {"TR": "#28A800", "KK": "#F000B8", "KF": "#E858D0", "JK": "#E80010", "JH": "#F05030"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}
# Gate 3: the operator's own stop count for the line wholly inside the city,
# against the collapsed set: the Kumamoto City Transportation Bureau's route
# map (kotsu-kumamoto.jp, read 2026-10-02) numbers 35 stops, 1 to 26 and B1
# to B9. The lines the city line cuts have no in-city count.
GATE3 = {"source": "the Kumamoto City Transportation Bureau's route map (kotsu-kumamoto.jp)",
         "lines": {"TR": 35}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KUMAMOTO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KUMAMOTO_BBOX
