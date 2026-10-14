"""Kitakyushu-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/kitakyushu.md
(11/11 checks, 2026-10-02). A city of the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py), in Fukuoka's two-source shape.

Business leg: two food lists split by the 2021 law. MHLW's
食品衛生申請等システム open data holds every permit since 2021-06 and the
notifications (opt-in, field by field); the city's own CC BY 4.0 list on BODIK
holds the old-law permits (as of 2026-03-31), kept only while in term on
MHLW's date. A premises in both is shown once (config.SUPERSEDES). Personal
services: the city's barber and beauty registers (2026-08-31); the city
publishes NO laundry list (Berlin's gap, disclosed). All placed by a JOIN to
MLIT's 位置参照情報 for the 7 wards; where the block join misses an MHLW row,
MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). The Kitakyushu Monorail, the Chikuho
Electric Railroad and JR Kyushu's lines. English station names from
OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kitakyushu" / "raw"
DATA_PROCESSED = ROOT / "data" / "kitakyushu" / "processed"
OUTPUTS = ROOT / "outputs" / "kitakyushu"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kitakyushu"
SLUG = "kitakyushu"
MUNICIPALITY = "北九州市"
PREFECTURE = "福岡県"

# The city's lists on BODIK (data.bodik.jp, the city's catalogue,
# odcs.bodik.jp/401005), each dataset license_id cc-by, under the catalogue's
# terms (北九州市オープンデータ利用規約 第1条: CC BY 4.0 International; read
# 2026-10-02). Each dataset's organisation and resource name are a MUST
# DISPLAY (第6条): food 保健福祉局 保健衛生課; barber and beauty 保健福祉局
# 東部・西部生活衛生課. The files are the editions this build read, pinned,
# never "the newest" (package_show re-read 2026-10-02: each is its dataset's
# newest resource).
BODIK = "https://data.bodik.jp/dataset"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2;
# read 2026-09-24 for Fukuoka). A plain GET. Credit links the top page only.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the page that links it and carries its licence)
SOURCE_FILES = {
    "mhlw": ("40100_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40100_food_business_all.csv",
             MHLW_TOP),
    "food": ("401005_shokuhineiseihotokyokashisetsuichiran_20260331.xlsx",
             f"{BODIK}/822fb681-346a-444e-b482-33c67b50cac3/resource/afce5cb5-8582-4295-8a98-494db2e25466/"
             "download/401005_shokuhineiseihotokyokashisetsuichiran_20260331.xlsx",
             f"{BODIK}/401005_shokuhineiseihotokyokashisetsuichiran"),
    "barber": ("401005_riyosyoichiran_20260831.csv",
               f"{BODIK}/8be510bd-5f67-4570-a250-b34ffdac8d37/resource/c0503e76-86d9-4f14-a052-f17ac06951d0/"
               "download/401005_riyosyoichiran_20260831.csv",
               f"{BODIK}/401005_riyosyoichian"),
    "beauty": ("401005_biyosyoichiran_20260831.csv",
               f"{BODIK}/c8266fc8-5d1f-4d3b-93aa-44486f5187ea/resource/e958d9fd-6e3d-47bf-b557-96af0c3a44ca/"
               "download/401005_biyosyoichiran_20260831.csv",
               f"{BODIK}/401005_biyosyoichiran"),
}
# The dates the lists state (Kyoto's rule, never the download's): the food
# list's sheet 「2026(令和8)年3月末時点」, the registers' resource names; MHLW's
# viewer reads 「2026年08月末現在」 (its newest 許可年月日 2026-08-31), but the
# file itself states none, so the page dates it by download.
SOURCE_AS_OF = {"mhlw": None, "food": "2026-03-31", "barber": "2026-08-31", "beauty": "2026-08-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# The resource names, as the BODIK credit must print them (第6条).
RESOURCE_NAMES = {
    "food": "食品衛生法等許可施設一覧（2026(令和8)年3月中）",
    "barber": "理容所施設一覧（2026(令和8)年8月31日時点）",
    "beauty": "美容所施設一覧（2026(令和8)年8月31日時点）",
}
# The old-law list keeps a permit until its next yearly edition even after its
# 許可終了日 has passed, so step 2 drops rows past expiry against this PINNED
# date, MHLW's end of August 2026 (japan_register.in_term), never today:
# 2,417 of 3,383 rows are in term on it, 966 dropped (measured 2026-10-02).
OLD_LAW_AS_OF = datetime.date(2026, 8, 31)
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: MHLW's file is UTF-8 with a BOM; the old-law list
# an XLSX (one sheet, header on row 1); the two registers cp932 CSV (a line
# break inside the header cell 許可（確認）年月日).
SOURCE_ENCODING = {"mhlw": "utf-8-sig", "food": "xlsx", "barber": "cp932", "beauty": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 営業者氏名 and 代表者氏名 (all three city files) are
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; they are read IN MEMORY by that
# rule only, never kept. Never selected: 代表者肩書 / 肩書, the permit numbers,
# and MHLW's 法人名 / 法人番号 / 法人住所 and phones.
_REGISTER = ("施設名称", "施設所在地", "業種", "営業者氏名", "代表者氏名")
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "food": ("屋号名称", "営業所所在地", "営業の種類", "営業者氏名", "代表者氏名", "許可終了日"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 32 m from the block point, 97.6% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both food lists: the city's old-law row goes, MHLW's (the
# newer filing) stays. The brief's screen: 71 of the 1,582 old-law
# restaurants in term share a block and trade name with an MHLW permit.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    The old-law food list only where its permit is in term on OLD_LAW_AS_OF
    (許可終了日); every other file as it is."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    rows = jr.city_rows(path)
    if key == "food":
        rows = jr.in_term(rows, ("許可終了日",), OLD_LAW_AS_OF)
    yield from rows


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kitakyushu.
# S, W, N, E: the city's N03 extent (S 33.721, W 130.673, N 34.022, E 131.039)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (33.71, 130.66, 34.04, 131.05)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen, no apostrophe before n (Fukuoka's Gannosu). OSM's
# Kitakyushu names carry macrons and run words together; the other 37 are
# OSM's as they stand. JR's and the Monorail's 城野 and 志井 are separate N02
# groups (MLIT keeps them apart, trap 1), so step 1 appends their operators.
OSM_NAME_EN_OVERRIDES = {
    "安部山公園": "Abeyama-koen",                    # Abeyamakōen
    "穴生": "Ano",                                   # Anō
    "筑豊香月": "Chikuho-Katsuki",                   # Chikuhō-Katsuki
    "平和通": "Heiwadori",                           # Heiwadōri
    "本城": "Honjo",                                 # Honjō
    "陣原": "Jinnoharu",                             # Jin'noharu
    "城野": "Jono",                                  # Jōno (both groups)
    "香春口三萩野": "Kawaraguchi-Mihagino",           # Kawaraguchi Mihagino
    "競馬場前": "Keibajo-mae",                        # Keibajōmae
    "九州工大前": "Kyushu-kodai-mae",                 # Kyūshūkōdaimae
    "門司港": "Mojiko",                              # Mojikō
    "奥洞海": "Okudokai",                            # Okudōkai
    "志井公園": "Shii-koen",                         # Shii-Kōen
    "徳力嵐山口": "Tokuriki-Arashiyamaguchi",         # Tokuriki Arashiyamaguchi
    "徳力公団前": "Tokuriki-kodan-mae",               # Tokuriki Kōdanmae
    "黒崎駅前": "Kurosaki-ekimae",                    # Kurosaki-Ekimae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~130.88) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 9 lines, no Shinkansen; 小倉 stays as a JR and Monorail
# station). The Monorail lies wholly inside (13 of 13); the Chikuho line keeps
# 14 of 21 (13 of 20 once 西黒崎 is out); JR's Kagoshima (16 of 99), Nippo (7 of
# 113), Hitahikosan (6 of 24) and Chikuho (6 of 26) lines are cut at the city
# line (owner 2026-09-24). JR Kyushu's Sanyo Line keeps one station (門司, of
# 2): a one-station stub stays as cut (Kobe's JR Takarazuka Line, owner
# 2026-09-27).
LEFT_OUT_LINES = {
    # A sightseeing funicular up Mt Sarakura (Kobe's Maya and Rokko, owner
    # 2026-09-27): never in excluded_stations.csv; the page says so.
    ("皿倉登山鉄道", "帆柱ケーブル線"): "a sightseeing funicular (Kobe's rule)",
    # A seasonal sightseeing trolley on weekends and holidays, Mojiko to
    # Kanmonkaikyo-Mekari: left out on Kyoto's Sagano precedent, with a page
    # bullet under The lines.
    ("平成筑豊鉄道", "門司港レトロ観光線"): "a seasonal sightseeing line (Kyoto's Sagano precedent)",
}
# A station N02-25 still has but the operator has closed (japan_step1).
CLOSED_STATIONS = {
    ("筑豊電気鉄道", "筑豊電気鉄道線", "西黒崎"):
        "closed 2026-07-31 (the operator's notice, chikutetsu.co.jp/data/topics/408_20260528nishikurosakihaishi.pdf)",
}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow JR Kyushu's signs (no
# macrons), as the station names follow OSM's.
_MO, _CT, _JR = "北九州高速鉄道", "筑豊電気鉄道", "九州旅客鉄道"
LINES = {
    "MO": {"n02": [(_MO, "小倉線")], "name": "Kitakyushu Monorail", "name_ja": "北九州モノレール",
           "short": "Monorail", "hue": "#0072BC"},
    "CT": {"n02": [(_CT, "筑豊電気鉄道線")], "name": "Chikuho Electric Railroad", "name_ja": "筑豊電気鉄道線",
           "short": "Chikutetsu", "hue": "#E4007F"},
    "JK": {"n02": [(_JR, "鹿児島線")], "name": "JR Kagoshima Main Line", "name_ja": "鹿児島本線", "short": "JR",
           "hue": "#E60012"},
    "JN": {"n02": [(_JR, "日豊線")], "name": "JR Nippo Main Line", "name_ja": "日豊本線", "short": "JR",
           "hue": "#0068B7"},
    "JH": {"n02": [(_JR, "日田彦山線")], "name": "JR Hitahikosan Line", "name_ja": "日田彦山線", "short": "JR",
           "hue": "#009944"},
    "JW": {"n02": [], "name": "JR Wakamatsu Line", "name_ja": "若松線", "short": "JR", "hue": "#F39800"},
    "JF": {"n02": [(_JR, "筑豊線")], "name": "JR Fukuhoku Yutaka Line", "name_ja": "福北ゆたか線", "short": "JR",
           "hue": "#8F2E14"},
    "JS": {"n02": [(_JR, "山陽線")], "name": "JR Sanyo Line", "name_ja": "山陽本線", "short": "JR", "hue": "#7F7F7F"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# kitakyushu` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. The Monorail's blue, which no
# blue clears Retail's pin in, goes teal and JR's Nippo blue slate; the Sanyo
# stub, which JR Kyushu gives no colour, is gray. Closest pair within 500 m
# 28.0 (Nippo / Monorail), anywhere 18.4 (Nippo / Sanyo); the dark-mode labels
# separate, 8 of 8.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "MO": "#08A0C0", "CT": "#F000B8", "JK": line_registry.colour("jr-kyushu-kagoshima-main-line"),
    "JN": line_registry.colour("jr-kyushu-nippo-main-line"), "JH": "#30A800", "JW": "#D08000",
    "JF": line_registry.colour("jr-kyushu-fukuhoku-yutaka-line"),
    "JS": line_registry.colour("jr-west-sanyo-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
# N02 files JR Kyushu's 筑豊本線 as one line, 若松 to 原田. Its in-city part,
# 若松 to 折尾, is the line JR Kyushu signs as the Wakamatsu Line (若松線);
# beyond 折尾 it is the Fukuhoku Yutaka Line (福北ゆたか線), which keeps one
# station inside the city (折尾) and stays as cut, as Fukuoka's.
BRANCHES = {
    "JW": {"line": (_JR, "筑豊線"), "terminus": "若松", "junction": "折尾",
           "stations": ["若松", "藤ノ木", "奥洞海", "二島", "本城"], "length_m": (8000, 13000)},
}

# Gate 3: the operator's own station count for the line wholly inside the
# city: Kitakyushu Monorail's site lists 13 stations, 小倉 to 企救丘 (read
# 2026-10-02). The Chikuho line's 13 in-city stops (20 on the operator's list
# since 西黒崎 closed) are N02's less 西黒崎; the lines the city line cuts have
# no in-city count of their own.
GATE3 = {"source": "Kitakyushu Monorail's station list (kitakyushu-monorail.co.jp)", "lines": {"MO": 13}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KITAKYUSHU_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KITAKYUSHU_BBOX

# Trade names read by eye as a person's own name and nothing else, on
# surnames the sign rule's list does not hold (owner, 2026-10-12: the
# sweep of every Japanese city, borderline readings included). KEYS, never
# names (pipeline/name_keys.py, over japan_register._name_key of the name).
PERSON_NAMED = (
    "3c84fa17041c2ce1",
    "20ff15c33b9464a2",
    "cbc3d002b582d533",
)

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604008600)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "way/1355886300": "'YASKAWAの森', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "way/1124048009": "'勝山公園', same-named parks more than 300 m apart are two rows (owner, 2026-10-13)",
    "way/1055572497": "'東田大通公園', same-named parks more than 300 m apart are two rows (owner, 2026-10-13)",
    "way/675806191": "'皇后崎公園', same-named parks more than 300 m apart are two rows (owner, 2026-10-13)",
    "way/799127854": "'UR紅梅団地公園', Kitakyushu's estate parks are kept (14 answers no. 7)",
    "way/1368221978": "'養福寺団地公園', Kitakyushu's estate parks are kept (14 answers no. 7)",
    "way/695629583": "'大蔵ビレッジ公園', Kitakyushu's estate parks are kept (14 answers no. 7)",
    "node/8487503656": "'城野団地', housing estates tagged as places are kept in the nine built cities (14 answers no. 6)",
    "node/8487541633": "'徳力団地', housing estates tagged as places are kept in the nine built cities (14 answers no. 6)",
    "way/354371264": "'九州共立大学（経済学部）', a glitched name on the object's only row stays: no clean twin, no name repair (finding 52, Onga River)",
    "way/354371263": "'九州国際大学（国際関係学部）', a glitched name on the object's only row stays: no clean twin, no name repair (finding 52, Onga River)",
    "way/354371265": "'九州栄養福祉大学（食物栄養学部）', a glitched name on the object's only row stays: no clean twin, no name repair (finding 52, Onga River)",
    "way/353920879": "'北九州市立大学（経済学部）', a glitched name on the object's only row stays: no clean twin, no name repair (finding 52, Onga River)",
    "way/400529643": "'朽網臨空公園グラウンド', a glitched name on the object's only row stays: no clean twin, no name repair (finding 52, Onga River)",
    "way/559461625": "'堺町町公園', a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "way/698515616": "'上本町ー丁目公園', a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "羽衣町大蔵1号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "元城町西川頭町1号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野10号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野11号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野12号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野19号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野20号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野21号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野22号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野23号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野24号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野25号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野26号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野28号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野31号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野34号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野3号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野4号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野7号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野8号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道浅野9号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道空港北町1号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道空港北町2号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道空港北町3号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "市道空港北町4号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "町道空港南町1号線": "Kitakyushu's official municipal road codes are kept (14 answers no. 10)",
    "都市計画道路 汐井町牧山海岸線": "the description and bare-type street rules never take a street with a way of residential class or above (street_description)",
    "公園横通り": "the description and bare-type street rules never take a street with a way of residential class or above (street_description)",
    "牡牛座の道": "the description and bare-type street rules never take a street with a way of residential class or above (street_description)",
    "297号鱒淵八幡東自転車道線": "a misspelled name is still that place (owner 2026-10-13, seven rulings no. 1)",
    "way/59967203": "'遠賀川 (Onga River)', a glitched name on the object's only row stays: no clean twin, no name repair (finding 52, Onga River)",
}
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    # A religious body's meeting halls and branches, and halls named only by a body and a hall type (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "node/6477346696": "a religious body's meeting hall or branch tagged a place of worship is dropped (ruling 2; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    # Religious offices, associations and education halls tagged a place of worship (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "node/6478103985": "a religious office, association or education hall tagged a place of worship is dropped (sixteen rulings 1, 2026-10-13; owner 2026-10-13, the flag read's verdicts, all approved)",
    "way/553454226": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/553454232": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/628456604": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/628456627": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/628456628": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/628456645": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/65457132": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88492404": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88492407": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88492413": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88492418": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88492421": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88492440": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88492454": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/88492470": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1159845905": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/1159845906": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/137539159": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/137539160": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/137539172": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/138422252": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399628": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399642": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399643": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399660": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399667": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399669": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399730": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399754": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399780": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399841": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399856": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/189705635": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/413112247": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822072114": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822072116": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822784381": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822784382": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822787272": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822787273": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822789654": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822789655": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822789656": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822789657": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/823059164": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/823059165": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399888": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399891": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399893": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399926": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399944": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399965": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399977": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144399997": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144400016": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144400049": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144400054": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/166676493": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/166676495": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/166676505": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/166676510": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/166676514": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/166676516": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/203432609": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/203433554": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/238132320": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/238132325": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/822841228": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/892753882": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/894612072": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/894612073": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/894641786": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/894641787": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144400081": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144400086": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144400097": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/144400105": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/894647307": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/121679862": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/895225865": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/895232040": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/138544702": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/437453168": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/548678511": "a duplicate row: the station building beside the station node already in",
    "node/1423757432": "a duplicate row of a museum already in under its common name",
    "way/1367616545": "an address area standing in for a park name; the area has its own place row",
    "node/12709928505": "a memorial stone with no article of its own; its wikidata is its subject's",
    "node/12627950261": "public art with no article of its own; its wikidata is the artist's",
    "way/1357936490": "a university sports field tagged a park",
    "way/1263422350": "a mall's indoor corridor with floors in the name",
    "way/1123734862": "a station free-passage corridor",
    "way/1258461239": "a station free-passage corridor",
    "way/1272777119": "a direction-label connecting passage (stairs)",
    "way/1274887621": "a bare type word (private road) as the whole name",
    "way/1274887622": "a bare type word (private road) as the whole name",
    "way/139411226": "a location description (in front of a park)",
    "way/1106143887": "an address block number standing in for a name",
    "way/598240333": "a glitched name (stray digit after the route code)",
    "way/598240334": "a glitched name (stray digit after the route code)",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "node/8154773325": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/8154773326": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/8154773328": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/8154773329": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/13387851891": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/4851161947": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/6189795868": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/9019685341": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/5487115878": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/815056105": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/5487115873": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/5487115874": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "node/6562374173": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/858485719": "duplicates of one object are one row (owner 2026-10-13, six answers no. 6; ROW_MERGE_M, NEAR_DUP_M); held rows settled 2026-10-13",
    "node/8487541618": "duplicates of one object are one row (owner 2026-10-13, six answers no. 6; ROW_MERGE_M, NEAR_DUP_M); held rows settled 2026-10-13",
    "node/12805153973": "duplicates of one object are one row (owner 2026-10-13, six answers no. 6; ROW_MERGE_M, NEAR_DUP_M); held rows settled 2026-10-13",
    "node/8487460500": "duplicates of one object are one row (owner 2026-10-13, six answers no. 6; ROW_MERGE_M, NEAR_DUP_M); held rows settled 2026-10-13",
    "way/824602430": "a home is kept only when open to visit or on an article of its own (home rule 2026-10-08; 15 answers no. 2); held rows settled 2026-10-13",
    "way/1147748611": "a pool, club, pitch or office tagged a park is dropped by id (settled read call; third list no. 15); held rows settled 2026-10-13",
    "node/6478595004": "a religious office, education hall or residence tagged a place of worship, no article of its own (owner, 2026-10-13)",
    "node/8154773321": "a religious office, education hall or residence tagged a place of worship, no article of its own (owner, 2026-10-13)",
    "way/858485720": "duplicates of one object are one row (owner 2026-10-13, six answers no. 6; ROW_MERGE_M, NEAR_DUP_M); the same-named twin of way/858485719, a row once that id was dropped; held rows settled 2026-10-13",
}
# Kept by id: admitted as rows although a rule passes them over (owner, 2026-10-13;
# docs/decisions_drafts/search-final.md).
PLACE_KEPT = {
    "node/5603043145": "'関門橋', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/660855879": "'旦過市場', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/1043377596": "'TOTOミュージアム', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "node/7467253086": "'官営八幡製鐵所旧事務所', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/742371374": "'千仏鍾乳洞', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/566364371": "'響灘緑地（グリーンパーク）', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/1123882028": "'北九州市立小倉城庭園', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "node/2959854421": "'門司港レトロハイマート展望室', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
