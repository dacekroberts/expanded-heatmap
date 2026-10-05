"""Fukuoka-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

The brief is docs/build_briefs/fukuoka.md (4/4 checks, 2026-09-28). Japan's
fourth city, on the shared modules Kobe built: pipeline/countries/japan.py
(rail, city line), japan_register.py (the address join), japan_step1.py,
japan_step2.py and japan_fetch.py. This file holds only what is Fukuoka's.

Business leg: the first TWO-SOURCE Japanese city. Fukuoka City's own food list
on BODIK holds only permits granted before 2021-06-01 and still held; since
then filings go through MHLW's 食品衛生申請等システム, whose open data (opt-in,
field by field) is the second food source. A renewal moves a premises from the
first to the second (config.SUPERSEDES). Personal services: the city's barber,
beauty and laundry registers on BODIK. All placed by a JOIN to MLIT's
位置参照情報 for the 7 wards; where the block join misses an MHLW row, MHLW's
own point (config.OWN_POINT_FALLBACK).

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen left out, stations kept only
inside the city line (N03). English station names from OpenStreetMap's name:en
(owner, 2026-09-27).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "fukuoka" / "raw"
DATA_PROCESSED = ROOT / "data" / "fukuoka" / "processed"
OUTPUTS = ROOT / "outputs" / "fukuoka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Fukuoka"
SLUG = "fukuoka"
MUNICIPALITY = "福岡市"
PREFECTURE = "福岡県"

# The city's lists on BODIK (data.bodik.jp, the city's designated catalogue,
# odcs.bodik.jp/401307), CC BY 4.0 through the city's own terms (第１条; read
# 2026-09-24, package_show re-read 2026-09-28). Each dataset's 作成者 (第７条,
# a MUST DISPLAY): food 保健医療局 食品安全推進課; barber and beauty 福岡市保健福祉局;
# laundry 保健福祉局 生活衛生課. The files are the editions this build read,
# pinned, never "the newest": the food list was replaced on 2026-09-25 by the
# 2026-08-31 edition (r8.8.csv, 851,761 bytes; the brief's 3,977 rows were the
# July edition).
BODIK = "https://data.bodik.jp/dataset"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2;
# read 2026-09-24). A plain GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the page that links it and carries its licence)
SOURCE_FILES = {
    "food": ("r8.8.csv",
             f"{BODIK}/5925a9fb-3326-4499-9acd-7b18c03d5e32/resource/70d22acf-2353-4bc1-b45d-f12d45da5216/"
             "download/r8.8.csv",
             f"{BODIK}/401307_insyokuteneigyoutoueigyoukyokasisetuitiran"),
    "mhlw": ("40130_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40130_food_business_all.csv",
             MHLW_TOP),
    "barber": ("202609011129.csv",
               f"{BODIK}/5ff384ca-dcc8-401f-9ce6-59d5b139e921/resource/58e0494e-bc04-4298-a031-2caa64c2e254/"
               "download/202609011129.csv",
               f"{BODIK}/401307_riyousyo_kensakakuninzumi"),
    "beauty": ("202609011112.csv",
               f"{BODIK}/bcfa330c-cfd4-4eaf-9568-52436dc0e20d/resource/f029fc9e-b2f5-46a5-a2b6-e62d8113dbc1/"
               "download/202609011112.csv",
               f"{BODIK}/401307_biyousyo_kensakakuninzumi"),
    "laundry": ("202604011019.csv",
                f"{BODIK}/81520f4a-437b-422d-b136-fdf21af38b11/resource/2c00764a-ddfb-4193-aa61-0712d35f325b/"
                "download/202604011019.csv",
                f"{BODIK}/401307_cleaning"),
}
# The resource names carry these dates (a MUST DISPLAY: generate the credit from
# the file used). MHLW's file states none: its latest 許可年月日 is 2026-08-31,
# and the page dates it by when it was downloaded (provenance.json).
SOURCE_AS_OF = {"food": "2026-08-31", "mhlw": None, "barber": "2026-08-31", "beauty": "2026-08-31",
                "laundry": "2026-03-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# The resource names, as the BODIK credit must print them (第７条).
RESOURCE_NAMES = {
    "food": "福岡市内飲食店営業等営業許可施設一覧（令和8年8月31日現在）",
    "barber": "福岡市内理容所検査確認済施設一覧（令和８年８月31日現在）",
    "beauty": "福岡市内美容所検査確認済施設一覧（令和８年８月31日現在）",
    "laundry": "福岡市内クリーニング所検査確認済施設一覧（令和８年３月31日現在）",
}
# The key is the taxonomy's `source` column: "food" and "mhlw" are both food
# lists to japan_eigyo; the other three are Personal services.
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred (docs/data_sources.md), read 2026-09-28: the food
# list and MHLW's are UTF-8 with a BOM; the three registers cp932.
# japan_register.decode() reads them all.
SOURCE_ENCODING = {"food": "utf-8-sig", "mhlw": "utf-8-sig", "barber": "cp932", "beauty": "cp932",
                   "laundry": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns are REQUIRED so that the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing: 営業者氏名 (food) and 開設者法人名（開設者氏名）(registers) are read IN
# MEMORY by that rule only, and never kept. Never selected: the phones, 郵便番号,
# 開設者法人住所 (an operator's own address), 開設者法人代表者名及び役職, and
# MHLW's 法人番号 / 法人住所. MHLW's 法人名 holds a sole trader's own name as
# well as a company's, so it is REQUIRED and read IN MEMORY by the name rule only,
# never kept (owner 2026-10-05, reversing DECISIONS 2026-09-28).
_REGISTER_COLUMNS = ("施設名称", "施設所在地", "開設者法人名（開設者氏名）")
REQUIRED_COLUMNS = {
    "food": ("屋号", "業種", "業態", "営業所所在地", "営業者氏名"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "barber": (*_REGISTER_COLUMNS, "業務種別"),
    "beauty": (*_REGISTER_COLUMNS, "業務種別"),
    "laundry": (*_REGISTER_COLUMNS, "種別"),
}
# MHLW publishes each field only where the filer agreed to it: a row with no
# address was withheld, not mobile, and is counted apart for the page's
# disclosure (owner-approved wording, 2026-09-24).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (a median
# 36 m from the block point, 97.1% within 250 m: the brief's check). Chōme-tier
# rows too: MHLW's point sits a median 111 m from the chōme centroid (owner
# 2026-09-28).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both food lists: the city's row goes, MHLW's (the newer
# filing) stays. The screen found 1.3% of MHLW's addressed restaurants there.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Fukuoka.
# S, W, N, E: the city's N03 extent (33.425-33.874 N, 130.032-130.495 E,
# measured 2026-09-28; it takes in Nokonoshima, Shikanoshima and Genkai-jima)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (33.40, 130.00, 33.90, 130.52)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
# How far an OSM station object may be from N02's group centroid and still name
# it (as Kobe, Osaka and Sapporo).
OSM_NAME_MATCH_M = 600
# Where OSM's objects for one station disagree on name:en, the spelling taken:
# the operators' own signs. Filled from step 1's report.
OSM_NAME_EN_TIES = {}
# Where OSM's object has NO name:en, the English name taken instead - explicit
# and cited, never inferred; step 1 still stops on any station missing here.
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment; owner 2026-09-28). Fukuoka's 条 is not a street grid, so no
# JO_IS_GRID, and no station name has a 丁目. OSM's Fukuoka objects mix
# styles: macrons and none (Ōhorikōen / Ohashi), hyphens and spaces
# (Hakozaki-Miyamae / Kashii Kaenmae), English glosses in brackets, and three
# names TRANSLATED rather than romanised (Kashii Shrine, Kushida Shrine, and
# "Fukuoka (Tenjin)" without its Nishitetsu). Each entry takes Sapporo's style,
# hyphenated title case with macrons (owner 2026-09-28); the comment is the OSM
# spelling it replaces (osm_station_names.json, 2026-09-28). The other 45 names
# are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    # glosses and translations, romanised
    "福工大前": "Fukkōdai-Mae",                      # Fukkodaimae (Fukuoka Institute of Technology)
    "九産大前": "Kyūsandai-Mae",                     # Kyusandaimae (Kyushu Sangyo University)
    "福岡空港": "Fukuoka-Kūkō",                      # Fukuokakūkō (Airport)
    "香椎神宮": "Kashii-Jingū",                      # Kashii Shrine
    "櫛田神社前": "Kushida-Jinja-Mae",               # Kushida Shrine
    "西鉄福岡（天神）": "Nishitetsu-Fukuoka (Tenjin)",  # Fukuoka (Tenjin)
    # into one style: hyphens, title case, macrons
    "福大前": "Fukudai-Mae",                         # Fukudaimae
    "箱崎九大前": "Hakozaki-Kyūdai-Mae",             # Hakozaki-Kyūdai-mae
    "馬出九大病院前": "Maidashi-Kyūdai-Byōin-Mae",   # Maidashi-Kyūdai-byōin-mae
    "香椎花園前": "Kashii-Kaen-Mae",                 # Kashii Kaenmae
    "大濠公園": "Ōhori-Kōen",                        # Ōhorikōen
    "薬院大通": "Yakuin-Ōdōri",                      # Yakuin-ōdōri
    "渡辺通": "Watanabe-Dōri",                       # Watanabe-dōri
    "南福岡": "Minami-Fukuoka",                      # Minami Fukuoka
    "大橋": "Ōhashi",                                # Ohashi
    "海ノ中道": "Uminonakamichi",                    # Umino Nakamichi (the park's own one-word spelling)
    "雁ノ巣": "Gannosu",                             # Gan'nosu (no apostrophe before n in Hepburn)
    "西鉄千早": "Nishitetsu-Chihaya",                # Nishitetsu Chihaya
    "西鉄平尾": "Nishitetsu-Hirao",                  # Nishitetsu Hirao
    "西鉄香椎": "Nishitetsu-Kashii",                 # Nishitetsu Kashii
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~130.40) falls in the 126 to 132 band. Derived
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
# Every N02 line with a station inside the city line (stub_test, 2026-09-28: 10
# N02 lines). The three subway lines are 100% inside, Nishitetsu Kaizuka 9 of
# 10. JR Kyushu and Nishitetsu Tenjin-Ōmuta are cut at the city line (owner
# 2026-09-24): Kagoshima Main 10 of 99, Chikuhi 5 of 31, Kashii 9 of 16,
# Tenjin-Ōmuta 8 of 50 - suburban lines. The Sasaguri Line keeps one station
# (吉塚, also on the Kagoshima Main Line): a one-station stub stays as cut
# (Kobe's JR Takarazuka Line, owner 2026-09-27).
LEFT_OUT_LINES = {
    # Hakata to Hakata-Minami (Kasuga), on Shinkansen track with Shinkansen
    # trains; only Hakata is inside, and it is served anyway (brief, handoff).
    ("西日本旅客鉄道", "博多南線"): "only Hakata is inside the city, served by every other line there (brief)",
}
# Kobe's 300 m until step 1's report shows a wider real interchange.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 (operator, line) pairs it is drawn from, its real public name
# (English, then Japanese), and its colour. 篠栗線 is signed 福北ゆたか線 by JR
# Kyushu (the Sapporo and Osaka precedent: the name on the signs).
#
# COLOURS: the project's own, not the operators' (Kobe's, Osaka's and Sapporo's
# rule). A search over the sRGB cube (step 8; 3,817 feasible colours): 3:1
# against BOTH map pages (#0B1220 and #ffffff), CIE76 >= 45 against every
# category pin, >= 18 between lines, each nearest its operator's hue family
# (lightness weighted half) in the order below: the subway's orange, blue and
# green, JR Kyushu's red, Nishitetsu's blue. Result: pins 45.0-70.5, closest
# line pair 18.1 (the Kagoshima Main and Chikuhi lines, both red). No blue
# clears Retail's pin: the Hakozaki Line went teal, Nishitetsu's lines slate
# and mauve.
_SUB, _JR, _NNR = "福岡市", "九州旅客鉄道", "西日本鉄道"
LINES = {
    # Fukuoka City Subway (福岡市交通局)
    "K": {"n02": [(_SUB, "1号線(空港線)")], "name": "Kūkō Line", "name_ja": "空港線", "colour": "#E07800",
          "short": "Subway"},
    "H": {"n02": [(_SUB, "2号線(箱崎線)")], "name": "Hakozaki Line", "name_ja": "箱崎線", "colour": "#007890",
          "short": "Subway"},
    "N": {"n02": [(_SUB, "3号線(七隈線)")], "name": "Nanakuma Line", "name_ja": "七隈線", "colour": "#28A800",
          "short": "Subway"},
    # JR Kyushu (九州旅客鉄道)
    "JK": {"n02": [(_JR, "鹿児島線")], "name": "JR Kagoshima Main Line", "name_ja": "鹿児島本線", "colour": "#E80010",
           "short": "JR"},
    "JC": {"n02": [(_JR, "筑肥線")], "name": "JR Chikuhi Line", "name_ja": "筑肥線", "colour": "#F05030",
           "short": "JR"},
    "JS": {"n02": [(_JR, "篠栗線")], "name": "JR Fukuhoku Yutaka Line", "name_ja": "福北ゆたか線", "colour": "#F86000",
           "short": "JR"},
    "JH": {"n02": [(_JR, "香椎線")], "name": "JR Kashii Line", "name_ja": "香椎線", "colour": "#B03800",
           "short": "JR"},
    # Nishitetsu (西日本鉄道)
    "NT": {"n02": [(_NNR, "天神大牟田線")], "name": "Nishitetsu Tenjin Ōmuta Line", "name_ja": "天神大牟田線",
           "colour": "#688090", "short": "Nishitetsu"},
    "NK": {"n02": [(_NNR, "貝塚線")], "name": "Nishitetsu Kaizuka Line", "name_ja": "貝塚線", "colour": "#786078",
           "short": "Nishitetsu"},
}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}

# Branches inside one N02 line: none known before step 1's report.
BRANCHES = {}

# Gate 3: the operator's own station counts, from the Fukuoka City Subway's
# station numbering: Kūkō K01 Meinohama to K13 Fukuokakūkō; Hakozaki H01
# Nakasu-Kawabata to H07 Kaizuka; Nanakuma N01 Hashimoto to N18 Hakata (the
# 2023 extension). Every one is inside the city.
GATE3 = {"source": "Fukuoka City Subway station numbering (K01-K13, H01-H07, N01-N18)",
         "lines": {"K": 13, "H": 7, "N": 18}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"
# This taxonomy also classifies by source and 業態: keep those raw columns
# through step 2 (they are passed to classify() by filter_to_storefront() and
# the map).

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
FUKUOKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = FUKUOKA_BBOX
