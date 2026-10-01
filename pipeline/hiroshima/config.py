"""Hiroshima-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/hiroshima.md
(4/4 checks, 2026-09-30). The eighth Japanese city on the shared modules
(pipeline/countries/japan*.py), Fukuoka's shape: TWO food lists that split by
filing channel, and no personal services (Band B, owner 2026-09-29: food only).

Business leg: the city's own list of counter (窓口) applications, 食品営業許可施設一覧
(市内全て), the annual full list as of the end of March 2026; plus MHLW's
食品衛生申請等システム open data for the online filings the city's list leaves
out since 2023-08 (opt-in, field by field). A premises in both is shown once
(config.SUPERSEDES). All placed by a JOIN to MLIT's 位置参照情報 for the 8 wards;
where the block join misses an MHLW row, MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen left out, stations kept only
inside the city line (N03); Hiroden's streetcars drawn (owner, 2026-09-29).
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "hiroshima" / "raw"
DATA_PROCESSED = ROOT / "data" / "hiroshima" / "processed"
OUTPUTS = ROOT / "outputs" / "hiroshima"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Hiroshima"
SLUG = "hiroshima"
MUNICIPALITY = "広島市"
PREFECTURE = "広島県"

# The city's page for food-permit lists. The full list (【窓口申請】食品営業許可施設一覧
# (市内全て), 「食品営業許可施設一覧（令和8年3月末時点）」, updated 2026-03-31, once a
# year) holds every premises that applied at a counter and holds a permit in
# force: every 許可満了日 is 2026-03-31 or later, the expiry window that drops a
# closed premises (the one-clock rule's snapshot case). The page's monthly
# files (new permits only, 2025-04 on) are not added: the full list is the
# snapshot. Catalogued as DataEye dataset 5672, PDL 1.0 (owner accepted the
# reading, 2026-09-24).
CITY_PAGE = "https://www.city.hiroshima.lg.jp/business/shokuhin-eisei/1051268/1051957.html"
DATAEYE_DATASET = "https://hiroshima-opendata.dataeye.jp/datasets/5672"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms; read
# 2026-09-24 for Fukuoka). A plain GET. Credit links the top page only.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "food": ("5080331-2.xlsx",
             "https://www.city.hiroshima.lg.jp/_res/projects/default_project/_page_/001/014/315/5080331-2.xlsx",
             CITY_PAGE),
    "mhlw": ("34100_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34100_food_business_all.csv",
             MHLW_TOP),
}
SOURCE_AS_OF = {"food": "2026-03-31", "mhlw": None}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: the city's list is XLSX (two sheets, 個人 and 法人,
# header cells holding line breaks; the 個人 sheet's address header lacks its
# closing bracket, which japan_register.ADDR_COLS already spells); MHLW's is
# UTF-8 with a BOM.
SOURCE_ENCODING = {"food": "xlsx", "mhlw": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 申請者名 (the 個人 sheet's operator, a person) and 代表者名
# (the 法人 sheet's representative) are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; they are read IN MEMORY by that rule only, never kept. Never
# selected: the phones, 申請者名_カナ, 代表者カナ, 申請者住所 (an operator's own
# address), 法人番号, and MHLW's 法人名 / 法人番号 / 法人住所.
REQUIRED_COLUMNS = {
    "food": ("営業の種類", "施設名称", "申請者名", "許可条件", "自動車登録番号", "許可満了日"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日"),
}
# As Fukuoka's (owner-approved wording, 2026-09-24): MHLW publishes an address
# only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 35 m from the block point, 96.3% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both lists: the city's row goes, MHLW's stays (the brief's
# screen: 40 of MHLW's addressed restaurants, 1.2%).
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    MHLW's file as it is. The city's workbook marks a premises' form in two
    columns the shared reader does not know: 許可条件 (露店による営業, a street
    stall; 125 + 5 rows) and 自動車登録番号 (a vehicle's registration; 180 rows,
    none marked 自動車 in its type). Both are carried into 業態, where
    japan_eigyo's FORM_RULES already take stalls and vehicles out; the permit
    classes (一類の営業行為に限る...) match no form rule and change nothing."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        if key == "food":
            form = (r.get("許可条件") or "").strip()
            if (r.get("自動車登録番号") or "").strip():
                form = (form + " 自動車").strip()
            r["業態"] = form
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and Hiroden's tram stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent, rounded out; step 1 stops if the city
# leaves it.
OSM_BBOX = (34.25, 132.16, 34.63, 132.70)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-09-30): OSM writes the 丁目 number as a figure
# (横川1丁目), drops the brackets N02 keeps (広電西広島（己斐）, 広島港（宇品）), and
# spells the Astram station 祗園新橋北 with 祗 (Kyoto's 祇 / 祗 pair).
OSM_NAME_ALIASES = {
    "横川一丁目": "横川1丁目", "段原一丁目": "段原1丁目", "皆実町二丁目": "皆実町2丁目", "皆実町六丁目": "皆実町6丁目",
    "宇品二丁目": "宇品2丁目", "宇品三丁目": "宇品3丁目", "宇品四丁目": "宇品4丁目", "宇品五丁目": "宇品5丁目",
    "広電西広島（己斐）": "広電西広島", "広島港（宇品）": "広島港", "祇園新橋北": "祗園新橋北",
}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment). Signage style, as Tokyo's and Yokohama's (owner 2026-09-28): no
# macrons, Hiroden's lowercase after a hyphen kept (Funairi-hon-machi). OSM's
# Astram and JR objects carry macrons the other 110 names do not, and it
# TRANSLATED one stop (Fukuoka's trap) rather than romanising it.
OSM_NAME_EN_OVERRIDES = {
    "修大協創中高前": "Shudai-kyoso-chuko-mae",       # Hiroshima Shudo University Hiroshima Kyoso Junior and High School
    "広大附属学校前": "Hirodai-fuzoku-gakko-mae",      # Hirodaifuzokugakkou-mae
    "長楽寺": "Chorakuji",                           # Chōrakuji
    "不動院前": "Fudoin-mae",                        # Fudōin-mae
    "本通": "Hondori",                               # Hondōri
    "城北": "Johoku",                                # Jōhoku
    "県庁前": "Kencho-mae",                          # Kenchō-mae
    "河戸帆待川": "Kodo-Homachigawa",                 # Kōdo-Homachigawa
    "広域公園前": "Koiki-koen-mae",                   # Kōiki-kōen-mae
    "伴中央": "Tomo-chuo",                           # Tomo-chūō
    "大原": "Obara",                                 # Ōbara
    "大町": "Omachi",                                # Ōmachi
    "大塚": "Ozuka",                                 # Ōzuka
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~132.46) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# HALVED, on the spacing rule (docs/ring_rules.md: the halved edges where the
# median station gap is about 550 m or less): step 1 measured 357 m among the
# 124 in-city stations, most of them Hiroden's tram stops (2026-09-30).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# Gate 1's floor: Paris's, Marseille's, Amsterdam's and Riga's 200 m, not a new
# number - a tram network is genuinely closer than 400 m and still clears a
# platform-spaced set by far (the collapsed median is 357 m; platforms 324 m).
SPACING_MIN_M = 200.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-09-30: 12 lines), the Shinkansen left out. The Astram Line, JR's Kabe
# Line and six of Hiroden's seven lines lie wholly inside. JR's Sanyō (12 of
# 131), Geibi (14 of 44) and Kure (1 of 28: 矢野) lines and Hiroden's Miyajima
# Line (12 of 22) are cut at the city line (owner 2026-09-24); the Kure Line's
# one-station stub stays as cut (Kobe's JR Takarazuka Line, owner 2026-09-27).
# Hiroden's streetcars are DRAWN (owner 2026-09-29: substantial, integral trams).
# N02-25, not N02-24, because N02-24 predates Hiroden's 2025 駅前大橋 line
# (japan.N02_EDITIONS).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the Astram Line in two railway
# classes (16 for the underground 本通 terminus, 24 for the guideway), as
# Kobe's Port Liner; one (operator, line) pair takes both. Hiroden's lines are
# its seven legal lines, each signed by name (本線, 宇品線...); the numbered
# routes run over them. Line names follow JR West's signs (no macrons), as the
# station names follow OSM's.
_JR, _HD, _AS = "西日本旅客鉄道", "広島電鉄", "広島高速交通"
LINES = {
    "AS": {"n02": [(_AS, "広島新交通1号線")], "name": "Astram Line", "name_ja": "アストラムライン",
           "short": "Astram", "hue": "#E4007F"},
    "JS": {"n02": [(_JR, "山陽線")], "name": "JR Sanyo Line", "name_ja": "山陽線", "short": "JR", "hue": "#E60012"},
    "JB": {"n02": [(_JR, "可部線")], "name": "JR Kabe Line", "name_ja": "可部線", "short": "JR", "hue": "#0068B7"},
    "JG": {"n02": [(_JR, "芸備線")], "name": "JR Geibi Line", "name_ja": "芸備線", "short": "JR", "hue": "#009944"},
    "JY": {"n02": [(_JR, "呉線")], "name": "JR Kure Line", "name_ja": "呉線", "short": "JR", "hue": "#F39800"},
    "HM": {"n02": [(_HD, "本線")], "name": "Hiroden Main Line", "name_ja": "広電本線", "short": "Hiroden",
           "hue": "#00A650"},
    "HU": {"n02": [(_HD, "宇品線")], "name": "Hiroden Ujina Line", "name_ja": "宇品線", "short": "Hiroden",
           "hue": "#00A650"},
    "HE": {"n02": [(_HD, "江波線")], "name": "Hiroden Eba Line", "name_ja": "江波線", "short": "Hiroden",
           "hue": "#00A650"},
    "HY": {"n02": [(_HD, "横川線")], "name": "Hiroden Yokogawa Line", "name_ja": "横川線", "short": "Hiroden",
           "hue": "#00A650"},
    "HH": {"n02": [(_HD, "白島線")], "name": "Hiroden Hakushima Line", "name_ja": "白島線", "short": "Hiroden",
           "hue": "#00A650"},
    "HN": {"n02": [(_HD, "皆実線")], "name": "Hiroden Minami Line", "name_ja": "皆実線", "short": "Hiroden",
           "hue": "#00A650"},
    "HJ": {"n02": [(_HD, "宮島線")], "name": "Hiroden Miyajima Line", "name_ja": "宮島線", "short": "Hiroden",
           "hue": "#00A650"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# hiroshima` (2026-09-30, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Hiroden's seven lines share one
# green hue and spread over olive and khaki. Closest pair within 500 m 19.4
# (Hiroden Main / JR Geibi), anywhere 10.6 (Ujina / Miyajima, which never meet);
# the dark-mode labels separate, 12 of 12.
_COLOURS = {"AS": "#F000B8", "JS": "#E80010", "JB": "#007890", "JG": "#30A800", "JY": "#D08000", "HM": "#68A008",
            "HU": "#607808", "HE": "#586818", "HY": "#889828", "HH": "#989848", "HN": "#787838", "HJ": "#788028"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station counts for the lines wholly inside the
# city, against the collapsed set: Hiroshima Rapid Transit's 22 Astram
# stations (本通 to 広域公園前) and JR West's 14 Kabe Line stations (横川 to
# あき亀山, since the 2017 reopening to あき亀山). Hiroden's stop counts are
# N02's; the lines the city line cuts have no in-city count.
GATE3 = {"source": "operators' station lists (Hiroshima Rapid Transit, JR West)",
         "lines": {"AS": 22, "JB": 14}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
HIROSHIMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = HIROSHIMA_BBOX
