"""Yokohama-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/yokohama.md.
The seventh Japanese city on the shared modules (pipeline/countries/japan*.py),
and the first page NOT built on food (owner, 2026-09-29: Band B, personal
services only): Yokohama publishes no food-permit list, so the page says so.

Business leg: the city's 環境衛生関係施設一覧 - the barber (理容所), beauty
(美容所) and laundry (クリーニング所) registers as of 2026-04-01, one CSV per
ward inside one zip per register - placed by a JOIN to MLIT's 位置参照情報 for
the 18 wards.

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen left out, stations kept only
inside the city line (N03). English station names from OpenStreetMap's name:en.
"""

import csv
import io
import zipfile
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "yokohama" / "raw"
DATA_PROCESSED = ROOT / "data" / "yokohama" / "processed"
OUTPUTS = ROOT / "outputs" / "yokohama"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Yokohama"
SLUG = "yokohama"
MUNICIPALITY = "横浜市"
PREFECTURE = "神奈川県"

# The city's 環境衛生関係施設一覧 (page last updated 2026-09-20). One zip per
# register, each holding 18 ward CSVs (UTF-16 LE with a BOM, TAB-separated,
# named .csv). The page's other six zips (bathhouses, inns, entertainment
# venues, pools, building sanitation, openings) are not personal-services
# storefronts or not a complete list, so they are not read.
DATASET_PAGE = "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/seikatsu/kaiteki/kankyodata.html"
FILE_BASE = "https://www.city.yokohama.lg.jp/kurashi/sumai-kurashi/seikatsu/kaiteki/kankyodata.files/"
# The registers' own date (令和８年４月１日現在). No closure field: the date is
# the one clock (the one-clock rule's snapshot case). The page also publishes
# each month's OPENINGS since (新規, 2026-05 to 2026-09, about 170 barbers,
# salons and laundries) but no closures, so they are not added: a snapshot
# stays a snapshot.
REGISTERS_AS_OF = "2026-04-01"
FOOD_AS_OF = None  # no food list is published
SOURCE_ENCODING = {"barber": "utf-16", "beauty": "utf-16", "laundry": "utf-16"}
SOURCES = {
    "barber": "life/20260401riyou.zip",
    "beauty": "life/20260401biyou.zip",
    "laundry": "life/20260401cleaning.zip",
}
SOURCE_FILES = {k: (f, FILE_BASE + f.split("/")[-1], DATASET_PAGE) for k, f in SOURCES.items()}
# The columns step 2 reads. The operator columns 申請者氏名 (a person's name)
# and 申請者役職 are read ONLY by japan_register.name_is_operator, in memory,
# for the owner's name rule (2026-09-27); nothing keeps them. The phone column
# 施設電話番号 is never read.
_REGISTER_COLUMNS = ("施設名称", "施設所在地", "業種", "詳細業種")
REQUIRED_COLUMNS = {k: _REGISTER_COLUMNS for k in SOURCES}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A register's rows: every ward CSV inside its zip (japan_register.city_rows
    reads only .xlsx members of a zip, so the members are read here, city-local).
    The kind of premises is in 詳細業種 (美容所(移動), a salon in a vehicle;
    無店舗取次店, a storeless laundry pick-up), while 業種 repeats the register's
    name - so 詳細業種 is the type the taxonomy reads."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if not jr.zip_member_name(info).lower().endswith(".csv"):
                continue
            text = jr.decode(zf.read(info))
            head = text.split("\n", 1)[0]
            delim = "\t" if head.count("\t") > head.count(",") else ","
            for r in csv.DictReader(io.StringIO(text), delimiter=delim):
                r["業種"] = (r.get("詳細業種") or "").strip() or r.get("業種", "")
                yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent, rounded out; step 1 stops if the city
# leaves it.
OSM_BBOX = (35.28, 139.44, 35.62, 139.74)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-09-30): OSM writes ケ where N02 writes ヶ (Tokyo's
# finding too) - Sotetsu's 鶴ヶ峰 is OSM's 鶴ケ峰 (ref SO09).
OSM_NAME_ALIASES = {"鶴ヶ峰": "鶴ケ峰"}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment). Station names follow the operators' signs, as Tokyo's do (owner
# 2026-09-28: signage style, no macrons; Tokyu's and the subway's lowercase
# after a hyphen, Higashi-hakuraku, Kita-yamata, kept). One OSM object breaks
# that style: 大船 "Ōfuna" (the only macron in the city) -> "Ofuna".
OSM_NAME_EN_OVERRIDES = {"大船": "Ofuna"}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.64) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median gap, 836 m, keeps the
# standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (Japan's standing rule:
# JR, the subway and the private railways; the Shinkansen left out, so
# Shin-Yokohama stays as a JR, subway, Tokyu and Sotetsu station). Lines
# running on beyond the city are cut at the line (owner 2026-09-24), including
# the one-station stub of the JR Nambu Line (矢向, 1 of 30; Kobe's JR Takarazuka
# Line precedent, owner 2026-09-27: keep as cut). The Kanazawa Seaside Line is an
# automated guideway (N02 class 24), drawn as Kobe's Port Liner is.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's own hue (`hue`, which scripts/line_colour_search.py
# starts from) and the project's colour.
#
# JR EAST as Tokyo's (owner 2026-09-28): N02 files JR East under its LEGAL
# lines, and one of them, 東海道線, carries four public services here - the
# Keihin-Tohoku Line (to 横浜, then 根岸線 as the Negishi Line), the Tokaido
# Line, the Yokosuka Line (over the Hinkaku track via 新川崎) and the
# Sotetsu-JR Link Line (羽沢横浜国大 to 武蔵小杉 over the freight track). Each is
# a `route` over the legal lines it runs on, stops as JR East's route maps give
# them; the first and last entry of a service running on past the city is its
# next station outside. The other JR lines are one service each (n02).
_JR = "東日本旅客鉄道"
_TOKAIDO = (_JR, "東海道線")
LINES = {
    # --- Yokohama Municipal Subway (横浜市): the Blue Line is N02's 1号線
    # (関内 to 湘南台) plus 3号線 (関内 to あざみ野)
    "B": {"n02": [("横浜市", "1号線"), ("横浜市", "3号線")],
          "name": "Blue Line", "name_ja": "ブルーライン", "short": "Subway", "hue": "#0070C0"},
    "G": {"n02": [("横浜市", "4号線")],
          "name": "Green Line", "name_ja": "グリーンライン", "short": "Subway", "hue": "#009944"},
    # --- JR East
    "JK": {"route": [(*_TOKAIDO, ["川崎", "鶴見", "新子安", "東神奈川", "横浜"]),
                     (_JR, "根岸線", ["横浜", "桜木町", "関内", "石川町", "山手", "根岸", "磯子", "新杉田", "洋光台",
                                   "港南台", "本郷台", "大船"])],
           "name": "JR Keihin-Tohoku / Negishi Line", "name_ja": "京浜東北・根岸線", "short": "JR", "hue": "#00B2E5"},
    "JT": {"route": [(*_TOKAIDO, ["川崎", "横浜", "戸塚", "大船", "藤沢"])],
           "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR", "hue": "#F68B1E"},
    "JO": {"route": [(*_TOKAIDO, ["新川崎", "~鶴見", "横浜", "保土ヶ谷", "東戸塚", "戸塚", "大船"])],
           "name": "JR Yokosuka Line", "name_ja": "横須賀線", "short": "JR", "hue": "#0070B9"},
    "SJ": {"route": [(*_TOKAIDO, ["羽沢横浜国大", "武蔵小杉"])],
           "name": "Sotetsu-JR Link Line", "name_ja": "相鉄・JR直通線", "short": "JR", "hue": "#1D2F6F"},
    "JH": {"n02": [(_JR, "横浜線")],
           "name": "JR Yokohama Line", "name_ja": "横浜線", "short": "JR", "hue": "#7AC143"},
    "JN": {"n02": [(_JR, "南武線")],
           "name": "JR Nambu Line", "name_ja": "南武線", "short": "JR", "hue": "#FFD400"},
    "JI": {"n02": [(_JR, "鶴見線")],
           "name": "JR Tsurumi Line", "name_ja": "鶴見線", "short": "JR", "hue": "#FFDD00"},
    # --- Keikyu (京浜急行電鉄)
    "KK": {"n02": [("京浜急行電鉄", "本線")],
           "name": "Keikyu Main Line", "name_ja": "京急本線", "short": "Keikyu", "hue": "#E5171F"},
    "KZ": {"n02": [("京浜急行電鉄", "逗子線")],
           "name": "Keikyu Zushi Line", "name_ja": "京急逗子線", "short": "Keikyu", "hue": "#E5171F"},
    # --- Tokyu (東急電鉄)
    "TY": {"n02": [("東急電鉄", "東横線")],
           "name": "Tokyu Toyoko Line", "name_ja": "東横線", "short": "Tokyu", "hue": "#DA0442"},
    "DT": {"n02": [("東急電鉄", "田園都市線")],
           "name": "Tokyu Den-en-toshi Line", "name_ja": "田園都市線", "short": "Tokyu", "hue": "#20A288"},
    "KD": {"n02": [("東急電鉄", "こどもの国線")],
           "name": "Tokyu Kodomonokuni Line", "name_ja": "こどもの国線", "short": "Tokyu", "hue": "#0068B7"},
    "SH": {"n02": [("東急電鉄", "東急新横浜線")],
           "name": "Tokyu Shin-yokohama Line", "name_ja": "東急新横浜線", "short": "Tokyu", "hue": "#6C5BA7"},
    # --- Minatomirai (横浜高速鉄道)
    "MM": {"n02": [("横浜高速鉄道", "みなとみらい21線")],
           "name": "Minatomirai Line", "name_ja": "みなとみらい線", "short": "Minatomirai", "hue": "#09357F"},
    # --- Sotetsu (相模鉄道)
    "SO": {"n02": [("相模鉄道", "相鉄本線")],
           "name": "Sotetsu Main Line", "name_ja": "相鉄本線", "short": "Sotetsu", "hue": "#004098"},
    "SI": {"n02": [("相模鉄道", "相鉄いずみ野線")],
           "name": "Sotetsu Izumino Line", "name_ja": "相鉄いずみ野線", "short": "Sotetsu", "hue": "#004098"},
    "SS": {"n02": [("相模鉄道", "相鉄新横浜線")],
           "name": "Sotetsu Shin-yokohama Line", "name_ja": "相鉄新横浜線", "short": "Sotetsu", "hue": "#004098"},
    # --- Yokohama Seaside Line (横浜シーサイドライン), an automated guideway
    "SL": {"n02": [("横浜シーサイドライン", "金沢シーサイドライン")],
           "name": "Kanazawa Seaside Line", "name_ja": "金沢シーサイドライン", "short": "Seaside Line",
           "hue": "#00A5DE"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# yokohama` (2026-09-30, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Closest pair within 500 m 18.0
# (Blue Line / Keihin-Tohoku), anywhere 12.4 (Kodomonokuni / Seaside Line,
# 17 km apart); the dark-mode labels separate, 20 of 20.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
# Moved so the shared colours fit (2026-10-07), hue kept as far as they allow:
# the Blue Line #08A0C0 to #007088 (pins 53.2, nearest line Tokyu Kodomonokuni
# Line 13.4, nearest beside it 19.1); the Tokyu Kodomonokuni Line #688898 to
# #486878 (pins 55.7, nearest line Blue Line 13.4, nearest beside it 18.6).
# docs/decisions_drafts/line-registry.md.
_COLOURS = {
    "B": "#007088", "G": "#30A800", "JK": line_registry.colour("jr-east-keihin-tohoku-line"),
    "JT": line_registry.colour("jr-east-tokaido-line"), "JO": line_registry.colour("jr-east-yokosuka-line"),
    "SJ": line_registry.colour("sotetsu-jr-link-line"), "JH": "#68A008",
    "JN": line_registry.colour("jr-east-nambu-line"), "JI": line_registry.colour("jr-east-tsurumi-line"),
    "KK": line_registry.colour("keikyu-main-line"), "KZ": "#F05830",
    "TY": line_registry.colour("tokyu-toyoko-line"), "DT": line_registry.colour("tokyu-den-en-toshi-line"),
    "KD": "#486878", "SH": "#C870C8", "MM": "#9840A0", "SO": "#9040C0", "SI": "#6048E0", "SS": "#C070F8",
    "SL": "#9090A0",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station counts for the lines inside the city,
# against the collapsed set: Yokohama Municipal Subway's numbering - Blue Line
# B02-B32 (B01 湘南台 is in Fujisawa), Green Line G01-G10; Yokohama Seaside
# Line 1-14; Minatomirai Line MM01-MM06; Tokyu Kodomonokuni Line (3) and Tokyu
# Shin-yokohama Line SH01-SH03 (新横浜, 新綱島, 日吉); Sotetsu Shin-yokohama Line
# SO51-SO52 plus 西谷 (SO11). The lines the city line cuts have no published
# in-city count; their stations are listed by step 1.
GATE3 = {"source": "operators' station numbering (Yokohama Municipal Subway, Yokohama Seaside Line, "
                   "Yokohama Minatomirai Railway, Tokyu, Sotetsu)",
         "lines": {"B": 31, "G": 10, "SL": 14, "MM": 6, "KD": 3, "SH": 3, "SS": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
YOKOHAMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = YOKOHAMA_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602689445,3602689482)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "シーサイドコーポ入口": "a signed junction (highway=traffic_signals) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "ドリームハイツ": "a signed junction (highway=traffic_signals) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "三井住友銀行横浜支店": "a notable historic bank building that still houses the branch its name carries (historic=building, Wikipedia): the building, not the business (the Panama Hotel precedent); tags read 2026-10-13",
    "前田ハイツ前": "a signed junction (highway=traffic_signals) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "旧東京三菱銀行横浜中央支店": "a former bank branch's historic building (historic=building, disused:amenity=bank, Wikipedia); tags read 2026-10-13",
    "海の公園駐車場": "a signed junction (highway=traffic_signals) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/yokohama.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A freight station (owner, 2026-10-13)
    "node/9216709070": "'横浜羽沢': JR Freight terminal, tagged railway=yard; no passenger service",
    "node/9235961237": "'本牧埠頭': Kanagawa Rinkai Railway Honmoku line freight station; no public_transport tag, no operator; freight status from the Wikipedia title's subject, not read from a tag",
    "node/9235961228": "'横浜本牧': Kanagawa Rinkai Railway Honmoku line freight station; no public_transport tag, no operator; freight status from the Wikipedia title's subject, not read from a tag",
    # A description standing in for a name (owner, 2026-10-13)
    "node/5500338625": "'ローラー 滑り台': roller slide: play equipment inside こどもの国 tagged place=locality",
    "way/411854014": "'記念館前広場': plaza in front of the memorial hall, place=square; a position, not a name",
    "way/1005181974": "'地蔵前': tagged place_of_worship; description says a rest space in front of the sports ground, called 地蔵前 for a Jizo statue",
    "way/54014079": "'自動車祈祷所': car-blessing station, a facility of a shrine",
    "node/3281630739": "'創建当時の手水鉢': the washbasin from the founding, a description of an object in a shrine",
    "node/4549051125": "'レンガ造り井戸遺構': brick well remains, a description",
    "node/3162356393": "'近代横浜の土木遺構': civil-engineering remains of modern Yokohama, a description",
    "node/3125367986": "'明治10年代に築造されたレンガ造りマンホールと下水管': a sentence: brick manhole and sewer pipe built in the Meiji 10s",
    "node/10228274670": "'南無阿弥陀仏': the inscription on a stone (the nembutsu) used as its name; subject:wikidata is the phrase's",
    "node/4135769751": "'弥生時代竪穴住居跡': Yayoi-period pit-dwelling site, a description",
    "way/353839010": "'竪穴住居 (古墳時代)': reconstructed pit dwelling (period in brackets) on the 三殿台遺跡 museum site; type plus period",
    "way/353839017": "'竪穴住居 (弥生時代)': reconstructed pit dwelling (period in brackets) on the 三殿台遺跡 museum site; type plus period",
    "way/353839027": "'竪穴住居 (縄文時代)': reconstructed pit dwelling (period in brackets) on the 三殿台遺跡 museum site; type plus period",
    "way/211888263": "'竪穴住居跡保護棟': shelter over the pit-dwelling remains, a description of a museum building",
    # A bare type word (owner, 2026-10-13)
    "way/1386119418": "'北門': North Gate of the zoo (よこはま動物園ズーラシア) tagged place=locality",
    "way/1386119417": "'噴水口': fountain entrance, a gate area of the zoo tagged place=locality",
    "way/1385476089": "'入口広場': entrance plaza; bare type, sub-area of an unnamed site",
    "way/1385476088": "'遊具広場': play-equipment plaza; bare type, 33 m from 入口広場",
    "node/10744697588": "'展望広場': viewing plaza; bare type, one of nine feature nodes around 山田富士公園",
    "node/13061227467": "'大花壇': big flowerbed, a feature of 里山ガーデン",
    "way/1189959380": "'子供の遊び場': children's playground, nothing else in the name",
    "way/544526752": "'休憩広場': rest plaza, nothing else in the name",
    "way/822449870": "'休憩広場': rest plaza, nothing else in the name",
    "way/451864744": "'いこいの広場': rest plaza (いこいの広場), generic",
    "node/4376980455": "'中央広場': central plaza, a node inside こどもの国",
    "way/919965979": "'三角広場': triangle plaza, shape plus type word",
    "node/4742515545": "'アスレチック': athletic (obstacle playground), bare type; node in the 若葉台 estate",
    "way/312561833": "'はらっぱ': open field (はらっぱ), bare type; access=permissive",
    "way/155090287": "'西口広場': west-exit plaza, beside 玄海田公園; a position word plus the type",
    "way/718090787": "'野外音楽堂': outdoor music stage inside 横浜国立大学's campus (14 m from its row)",
    "way/379492148": "'野鳥観察園': bird-watching garden, bare type",
    "node/8820556564": "'噴水広場': fountain plaza, place=square, bare type",
    "node/8820556562": "'橋詰広場': bridge-end plaza, place=square, bare type",
    "way/1251513064": "'サンクンガーデン': sunken garden, place=square, bare type",
    "node/606299780": "'お稲荷さん': お稲荷さん: the everyday word for any Inari shrine",
    "way/570400736": "'お稲荷さん': お稲荷さん: the everyday word for any Inari shrine",
    "node/4401908193": "'不動尊': 不動尊: the deity's title alone, no religion tag",
    "way/1047766486": "'不動明王': 不動明王: the deity's name alone",
    "node/5614821891": "'弁財天': 弁財天: the deity's name alone",
    "node/5353492532": "'馬頭観音': 馬頭観音: a wayside statue type, no religion tag",
    "node/4323455110": "'観音堂': 観音堂: Kannon hall, type word alone",
    "node/3591840311": "'聖母像': 聖母像: statue of the Virgin, type word alone; historic=wayside_shrine",
    "node/10315177065": "'境内社': 境内社: precinct sub-shrine, type word alone",
    "node/607854159": "'奥宮': 奥宮: inner shrine, type word alone",
    "way/592971949": "'大殿（本堂）': 大殿（本堂）: main hall, a building of a temple that has its own row",
    "node/7895797998": "'やぐら': やぐら: the type word for a Kamakura cave tomb",
    "node/7958450252": "'五輪塔群': 五輪塔群: group of five-ring stupas, type alone",
    "node/8024058989": "'多宝塔': 多宝塔: pagoda type alone",
    "node/7927454502": "'社号標': 社号標: shrine name-post, type alone",
    "node/7965703150": "'永代有縁墓': 永代有縁墓: perpetual communal grave, type alone",
    "way/411635694": "'転車台': 転車台: turntable, type alone (a second row 国鉄横浜機関区高島車庫転車台 carries a name)",
    "way/382196925": "'貝塚跡': 貝塚跡: shell-mound site, type alone; fenced, no entry per its note",
    "node/4030970255": "'横穴墓': 横穴墓: cave tomb, type alone; its note says the entrance was backfilled and nothing shows",
    # A zoo's zone tagged a place (ruling 8; owner, 2026-10-13)
    "way/1386119419": "'自然体験林': unsure in the full read, dropped by the owner's ruling 8",
    "way/1386110713": "'アジアの熱帯林': unsure in the full read, dropped by the owner's ruling 8",
    "way/1386110720": "'アフリカのサバンナ': unsure in the full read, dropped by the owner's ruling 8",
    "way/1386110719": "'アフリカの熱帯雨林': unsure in the full read, dropped by the owner's ruling 8",
    "way/1386110718": "'アマゾンの密林': unsure in the full read, dropped by the owner's ruling 8",
    "way/1386110714": "'オセアニアの草原': unsure in the full read, dropped by the owner's ruling 8",
    "way/1386110716": "'中央アジアの高地': unsure in the full read, dropped by the owner's ruling 8",
    "way/1386110715": "'亜寒帯の森': unsure in the full read, dropped by the owner's ruling 8",
    "way/1386110717": "'日本の山里': unsure in the full read, dropped by the owner's ruling 8",
    "node/4819642542": "'牛・羊の牧場': unsure in the full read, dropped by the owner's ruling 8",
    # A facility of an apartment estate (owner, 2026-10-13)
    "way/529967377": "'A棟前公園': park in front of Block A, access=no: a housing block's own yard",
    "way/1002275475": "'ジャンボ公園': description: the park under the apartment block, a nickname inside the 若葉台 estate",
    # A stock plaza name with no place in it (ruling 5; owner, 2026-10-13)
    "way/401934612": "'健康はらっぱ': unsure in the full read, dropped by the owner's ruling 5",
    "way/566058987": "'まちのはらっぱ': unsure in the full read, dropped by the owner's ruling 5",
    "way/436377439": "'ふれあい広場': unsure in the full read, dropped by the owner's ruling 5",
    "way/482615135": "'ふれあい広場': unsure in the full read, dropped by the owner's ruling 5",
    "node/11046749816": "'みどりの広場': unsure in the full read, dropped by the owner's ruling 5",
    # A business (owner, 2026-10-13)
    "node/13061209778": "'フォレストアドベンチャー・よこはま': Forest Adventure, a commercial ropes-course brand, tagged leisure=park with opening hours",
    "way/136169519": "'緑テニスガーデン': tennis club tagged leisure=park, sport=tennis; business status inferred from the name and sport tag, not read from an operator",
    "node/7137060251": "'ベイバイクポート高島交番横': a Bay Bike share port tagged place=square",
    "way/253766166": "'アニヴェルセル ヒルズ横浜': Anniversaire, a wedding-hall brand; building=church",
    "node/7641996794": "'湘和会堂手広': 湘和会堂 is a funeral-hall chain; business status from the chain name, no operator tag",
    # A facility of a mall (owner, 2026-10-13)
    "way/340589456": "'ジョイナス彫刻の森公園': rooftop garden of the Joinus mall: level=8, opening_hours, access=permissive",
    "node/6134577923": "'クイーンズスクエア横浜': Queen's Square Yokohama, a shopping mall, tagged place=square",
    "node/4742537879": "'ふれあい広場': description: an eating space inside 若葉台ショッピングタウン",
    # Private fenced land (owner, 2026-10-13)
    "way/575960803": "'ドコモの広場': access=no, barrier=fence, natural=grassland: a company's fenced lot tagged place=square",
    # A school's or an organisation's ground tagged a park (owner, 2026-10-13)
    "way/682390328": "'三保幼稚園グランド': a kindergarten's sports ground tagged leisure=park",
    "way/693665694": "'慶應義塾大学矢上キャンパス グラウンド': a university campus sports ground tagged leisure=park",
    # Worship named only by a body or a denomination (owner, 2026-10-13)
    "node/2264281995": "'救世軍': named only The Salvation Army",
    "node/3110465448": "'末日聖徒 イエス・キリスト教会': named only by the denomination (LDS church), two rows 12 km apart",
    "node/4257392913": "'末日聖徒 イエス・キリスト教会': named only by the denomination (LDS church), two rows 12 km apart",
    # A religious office, hall, school or residence (owner, 2026-10-13)
    "node/1791225855": "'アルペなんみんセンター': a refugee support centre (Arrupe) tagged place_of_worship",
    "way/1395251840": "'創価学会 港南文化会館': a Soka Gakkai culture hall (文化会館)",
    "node/14021361319": "'祠 伏見稲荷大社講務本庁扱所': name reads small shrine + Fushimi Inari lecture-office handling point",
    # A glitched name (owner, 2026-10-13)
    "node/5047803357": "'不動尊󠄂': 不動尊 with a variation selector glued on (U+E0102); note says the name was guessed from the torii",
    # A part of a shrine or temple that has its own row (ruling 4; owner, 2026-10-13)
    "way/34547350": "'舞殿': unsure in the full read, dropped by the owner's ruling 4",
    "way/34582197": "'齋館': unsure in the full read, dropped by the owner's ruling 4",
    "way/684563337": "'祖霊社': unsure in the full read, dropped by the owner's ruling 4",
    # A deity's title alone (ruling 3; owner, 2026-10-13)
    "way/1432001415": "'猿田彦神・猿田毘古神': unsure in the full read, dropped by the owner's ruling 3",
    # A religious body's hall or branch tagged a place of worship (ruling 2; owner, 2026-10-13)
    "way/853374064": "'浄光寺 西谷千丸台会館': unsure in the full read, dropped by the owner's ruling 2",
    # A duplicate of one object (owner, 2026-10-13)
    "way/467970071": "'横穴墓': 横穴墓: type word alone, about 35 m from the row 宮ノ前横穴墓群 (node/7740692035), whose article its wikidata Q97613655 names",
    "way/282460558": "'万騎ヶ原第十公園': 21 m from 万騎が原第十公園 (way/282460581), same park, ヶ/が spelling",
    "way/89559575": "'横浜媽祖廟': 9 m from 媽祖廟 (way/47883239, the row with wikidata); the same temple",
    "node/5246704074": "'杉山神社': 0 m from 中山杉山神社 (way/248177452); the same shrine as a node",
    "way/381661096": "'元町公園 ベーリックホール': 0 m from ベーリックホール (way/381661095, tourism=attraction with wikidata); the same building tagged a park",
    "node/1420813557": "'横浜三渓園': about 40 m from 三溪園 (way/312888383), same wikidata Q4249885; a 2006 register point tagged museum",
    "way/453730067": "'日本基督教団鎌倉教会会堂': 22 m from 日本基督教団鎌倉教会 (way/704515208); the church building beside the church's own row",
    "way/304571245": "'横浜栄養専門学校 第二校舎': second building of 横浜栄養専門学校, 89 m from its row (node/3098676837), same wikidata Q60986236",
    # An exhibit, not a place (owner, 2026-10-13)
    "way/504387758": "'横浜市電1156号': preserved tram car in a park, historic=train, no wikidata; the exhibit rule lists locomotive and railway_car but not train",
    "way/312883210": "'蒸気機関車D51 516号機': preserved steam locomotive in a park, historic=train, no wikidata; same gap in the exhibit rule",
    # One bay labeled many times (ruling 9; owner, 2026-10-13)
    "node/5780338763": "'横浜港': unsure in the full read, dropped by the owner's ruling 9",
    "node/5780338764": "'横浜港': unsure in the full read, dropped by the owner's ruling 9",
    "node/5780338765": "'横浜港': unsure in the full read, dropped by the owner's ruling 9",
    "node/5780338766": "'横浜港': unsure in the full read, dropped by the owner's ruling 9",
    "node/5780366418": "'横浜港': unsure in the full read, dropped by the owner's ruling 9",
    "node/5780366419": "'横浜港': unsure in the full read, dropped by the owner's ruling 9",
    "node/5780366420": "'横浜港': unsure in the full read, dropped by the owner's ruling 9",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/401934613": "'健康はらっぱ': the twin of way/401934612; A stock plaza name with no place in it (ruling 5; owner, 2026-10-13)",
    "way/467970072": "'横穴墓': the twin of node/4030970255; A bare type word (owner, 2026-10-13)",
}
# Kept by the owner's word, by id (place_index, PLACE_KEPT; owner, 2026-10-13):
# famous places in the cache that the rules pass over for want of a tag.
PLACE_KEPT = {
    "way/84830302": "'横浜港大さん橋国際客船ターミナル', Osanbashi pier: tagged a ferry terminal only; a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/138101264": "'日本丸', the sail training ship Nippon Maru: historic=ship with no Wikidata or Wikipedia tag; a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
