"""Funabashi-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/funabashi.md (5/5 checks, 2026-10-11). Funabashi City
(船橋市, 12204), one municipality with no wards, a core city with its own
health center: Chiba Prefecture's registers do not cover it. Japan's A/B
batch (East-2), on the shared modules (pipeline/countries/japan*.py) with the
Japan foundation's rules on, in Kochi's shape. Personal services only (Band B,
owner 2026-10-04): MHLW's food file publishes an address for 52.4% of the
city's open restaurant permits, under the placement bar, so food stays off.

Business leg: the city's own CC BY 4.0 registers on BODIK (organization
122041, 生活衛生関係営業施設一覧): barbers and beauty salons as of 2026-08-01,
laundries as of 2026-07-01. Each dataset is one resource replaced in place, a
snapshot of the premises on file at its date (no closure column, no earlier
edition kept). Everything placed by a JOIN to MLIT's 位置参照情報 for the one
municipality (no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03): Keisei's Main and Matsudo lines, JR East's Sobu (local and rapid),
Musashino and Keiyo lines, the Tokyo Metro Tozai Line (2 of 23, drawn cut at
the city line; owner, call 41), the Toyo Rapid Railway Line, the Tobu Urban
Park Line and the Hokuso Line (1 of 15, a one-station stub kept as cut by the
standing call). English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "funabashi" / "raw"
DATA_PROCESSED = ROOT / "data" / "funabashi" / "processed"
OUTPUTS = ROOT / "outputs" / "funabashi"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Funabashi"
SLUG = "funabashi"
MUNICIPALITY = "船橋市"
PREFECTURE = "千葉県"

# The city's three 生活衛生関係営業施設一覧 datasets on BODIK (data.bodik.jp,
# organization 122041), each cc-by-40-intl and each holding ONE resource
# replaced in place: the dataset ids say 20260401, the resource names carry
# the edition's date (20260801 barbers and beauty salons, 20260701 laundries).
# The barber and beauty file names do not change between editions, so the
# brief's check pins each edition by its size (43,498 B, 182,360 B, 47,069 B):
# a changed size is a new edition, to re-measure. BODIK rate-blocks: space
# every request 20 s or more, never datastore_search_sql.
_BODIK = "https://data.bodik.jp/dataset/"
_FAMILY = "122041_20260401_seikatsueisei-eigyoushisetsu_"
# key -> (file, URL, the dataset page that carries it)
SOURCE_FILES = {
    "barber": ("riyouroichiranall.csv",
               _BODIK + "deb35006-3f85-4626-a2ea-c65823dae612/resource/73e5f3c8-4a05-4056-9f00-2b6b249402ce"
               "/download/riyouroichiranall.csv",
               _BODIK + _FAMILY + "riyousyo"),
    "beauty": ("biyouroichiranall1.csv",
               _BODIK + "89b146c9-d7c4-4820-921e-edeee4f396d9/resource/ff85f1bb-95c1-42f4-b176-8c4c5b43f50d"
               "/download/biyouroichiranall1.csv",
               _BODIK + _FAMILY + "biyousyo"),
    "laundry": ("kurininngu202607.csv",
                _BODIK + "f75f7b70-0657-4188-9ffa-ccecec143a6b/resource/acc812a0-ba5e-4cf1-bdd2-13d8556d8d75"
                "/download/kurininngu202607.csv",
                _BODIK + _FAMILY + "kuri-ninngu"),
}
# Kyoto's rule: the date each list states (its resource name), never the
# download's.
SOURCE_AS_OF = {"barber": "2026-08-01", "beauty": "2026-08-01", "laundry": "2026-07-01"}
REGISTERS_AS_OF = "2026-08-01"
FOOD_AS_OF = None  # no food leg (MHLW's addresses fail placement)
# No TERM_AS_OF: no source carries a permit term (a 生活衛生 confirmation does
# not expire; 確認（許可）日 is the only date and nothing reads it).

SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: UTF-8 with a BOM, comma-separated, CRLF, one
# header row, nine cells a row.
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCE_FILES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 申請者_氏名 (the operator, filled only where it is a
# company: 52 barber, 400 beauty and 139 laundry rows by the brief) and
# 代表者_氏名 (a company's representative, a person's name) are REQUIRED so the
# name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing; read IN MEMORY by that rule only, never kept.
# Never selected: 施設電話番号, 申請者所在地, 申請者電話番号, 確認（許可）日.
_REG = ("業態", "施設_名称", "施設所在地", "申請者_氏名", "代表者_氏名")
REQUIRED_COLUMNS = {k: _REG for k in SOURCE_FILES}
# The columns carried into step 2: the premises' own, the kind, and the two
# operator columns for the name rule (in memory).
_KEEP = _REG


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def source_rows(key):
    """A register's rows (japan_step2 reads this hook where a city defines
    it): the file as it stands, the premises columns only. Each file names its
    kind in 業態 (one value a file: 理容所, 美容所, クリーニング業), which
    japan_register reads as a FORM column, so the value is copied into 業種 for
    the type to read it (Amagasaki's notifications, the same route): the name
    rule's pin shows the type. The rows that are not Funabashi premises are
    left to the shared rules, counted by reason (another municipality's
    address: 3 beauty rows and 1 laundry row by the brief; the city's name
    alone: 1 beauty row)."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        row = {c: r.get(c) for c in _KEEP if c in r}
        if "業態" in row:
            row["業種"] = row["業態"]
        yield row


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 12204.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Funabashi.
# S, W, N, E: the city's N03 extent (S 35.6562, W 139.9387, N 35.7997,
# E 140.0897) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.65, 139.93, 35.8, 140.09)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons). None:
# all 30 names were read 2026-10-11 and none is translated or carries a
# macron (船橋競馬場 reads Funabashi-Keibajo, 飯山満 Hasama).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~140.02) and the whole extent (139.939 to
# 140.090) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 777 m (30 stations), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 9 lines, 38 station records, 30 station groups; no Shinkansen,
# tram or light rail). Cut at the city line (owner 2026-09-24):
#   * Keisei Matsudo Line 9 of 24 and Keisei Main Line 7 of 42;
#   * JR East's 総武線 4 of 48, 京葉線 2 of 19, 武蔵野線 2 of 27;
#   * the Toyo Rapid Railway Line 5 of 9; the Tobu Urban Park Line 4 of 35;
#   * the Tokyo Metro Tozai Line 2 of 23 (原木中山 and 西船橋, its eastern
#     terminus): an urban line cut to two stations, DRAWN cut on Sakai's and
#     Higashiosaka's precedent (owner, 2026-10-05/06, call 41; two or more
#     stations are drawn cut, one is left out);
#   * the Hokuso Line 1 of 15 (小室): a commuter railway, a one-station stub
#     kept as cut by the standing call (2026-09-27). 小室 is on no other line.
#     The Keisei Narita Sky Access runs over the Hokuso track without
#     stopping at 小室; N02 has no Sky Access station inside the city.
# N02 groups 西船橋 (JR's three lines, the Tozai and the Toyo Rapid), 船橋 (JR
# and Tobu) and 北習志野 (Keisei and the Toyo Rapid); it keeps JR's 船橋 and
# 京成船橋 (217 m) and 京成中山 and JR's 下総中山 (318 m) apart, each a walking
# interchange under two names, and so does step 1 (trap 1). No frequency floor
# (owner, 2026-10-06, calls 46 and 86): the Hokuso Line at 小室 runs three
# trains an hour each way at midday (86 and 87 weekday departures; the
# operator's timetable of 2025-12-13, read 2026-10-05).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, and the same
# as on Tokyo's map wherever Tokyo draws the line (Keisei Main Line, JR
# Chuo-Sobu Line, JR Yokosuka / Sobu Rapid Line, JR Keiyo Line, Tozai Line,
# Hokuso Line), on Kasukabe's (Tobu Urban Park Line, N02's 野田線) and on the
# five maps that draw the JR Musashino Line.
#
# JR EAST'S 総武線 carries two public services here, drawn as Tokyo draws them
# (`route`, japan_step1.route_sections; trap 2): the Chuo-Sobu local stops at
# all four stations, the Sobu Rapid at 船橋 only. Each route's first and last
# entry is the next station beyond the city line (本八幡 in Ichikawa, 津田沼 in
# Narashino); the rapid passes 本八幡 ("~") on its way from 市川.
#
# N02's 京葉線 (trap 3) is the main line through 南船橋 plus the two branches
# to 西船橋 that the Musashino Line's through trains use. JR East lists 西船橋
# as a Keiyo Line station, so the legal line is drawn whole under the one
# public name and 西船橋 counts on it, as N02 files it; the through trains
# need no line of their own.
#
# The Toyo Rapid's trains run through onto the Tozai Line at 西船橋; N02 files
# two lines and two are drawn, each under its own name. The Keisei Matsudo
# Line is the former Shin-Keisei Line (Keisei's since 2025-04-01), which N02-25
# already files as 京成電鉄 松戸線.
_JR, _KS = "東日本旅客鉄道", "京成電鉄"
_SOBU = (_JR, "総武線")
LINES = {
    "KS": {"n02": [(_KS, "本線")], "name": "Keisei Main Line", "name_ja": "京成本線", "short": "Keisei",
           "hue": "#005AAA"},
    "KM": {"n02": [(_KS, "松戸線")], "name": "Keisei Matsudo Line", "name_ja": "京成松戸線", "short": "Keisei",
           "hue": "#EF59A1"},
    "JB": {"route": [(*_SOBU, ["本八幡", "下総中山", "西船橋", "船橋", "東船橋", "津田沼"])],
           "name": "JR Chuo-Sobu Line", "name_ja": "中央・総武線各駅停車", "short": "JR", "hue": "#FFD400"},
    "JO": {"route": [(*_SOBU, ["~本八幡", "船橋", "津田沼"])],
           "name": "JR Yokosuka / Sobu Rapid Line", "name_ja": "横須賀・総武快速線", "short": "JR",
           "hue": "#0067C0"},
    "JM": {"n02": [(_JR, "武蔵野線")], "name": "JR Musashino Line", "name_ja": "武蔵野線", "short": "JR",
           "hue": "#F15A22"},
    "JE": {"n02": [(_JR, "京葉線")], "name": "JR Keiyo Line", "name_ja": "京葉線", "short": "JR",
           "hue": "#C9242F"},
    "T": {"n02": [("東京地下鉄", "5号線東西線")], "name": "Tozai Line", "name_ja": "東西線", "short": "Metro",
          "hue": "#009BBF"},
    "TR": {"n02": [("東葉高速鉄道", "東葉高速線")], "name": "Toyo Rapid Railway Line", "name_ja": "東葉高速線",
           "short": "Toyo Rapid", "hue": "#00A650"},
    "TD": {"n02": [("東武鉄道", "野田線")], "name": "Tobu Urban Park Line", "name_ja": "東武アーバンパークライン",
           "short": "Tobu", "hue": "#7FBE26"},
    "HS": {"n02": [("北総鉄道", "北総線")], "name": "Hokuso Line", "name_ja": "北総線", "short": "Hokuso",
           "hue": "#3A9AD9"},
}
# ONE COLOUR PER LINE, SITE-WIDE (owner, 2026-10-07). Eight of the ten lines
# are drawn on another map and take that map's colour, never one of this
# city's own:
#   * from pipeline/line_registry.py: the JR Musashino Line and the JR
#     Yokosuka / Sobu Rapid Line (the registry's jr-east-yokosuka-line);
#   * Tokyo's values, not yet registry entries because only Tokyo drew them:
#     Keisei Main Line #785868 (KS), JR Chuo-Sobu Line #B09000 (JB), JR Keiyo
#     Line #F86040 (JE), Tozai Line #6890A0 (T), Hokuso Line #787878 (HS);
#   * Kasukabe's value for the Tobu Urban Park Line, #60A000 (TD).
# Each of those six needs a registry entry naming this map; until one exists
# the literal here must equal the other map's.
# The two lines new to the site are from scripts/line_colour_search.py's rule
# with the eight held fixed (2026-10-11: 3:1 on both map pages, CIE76 >= 45
# from every pin, >= 18 from every line within 500 m, >= 10 from the rest,
# nearest the operator's hue): the Keisei Matsudo Line #E060D0 (the line's
# pink; 45.8 from the Food service pin, 59.6 from the nearest line) and the
# Toyo Rapid Railway Line #20A800 (45.7 from the Personal services pin, 18.8
# from the Tobu Urban Park Line, which it comes within 500 m of).
# Measured 2026-10-11, all ten: closest pair anywhere and within 500 m 11.8,
# the JR Musashino Line against the JR Keiyo Line, which share track into
# 西船橋: both colours are another map's, so neither moves here, and the pair
# sits under the 18 a side-by-side pair should have (over linecolour's hard
# floor of 10). Re-measure if either is re-registered. Next closest within
# 500 m 18.8 (Toyo Rapid, Tobu Urban Park). Accepted trades against the pins,
# each inherited with its colour: JR Chuo-Sobu 23.2 from Food shops olive
# (Tokyo's, owner 2026-10-07) and Tobu Urban Park 29.1 from it (Kasukabe's);
# the page draws no Food shops pin. The dark-mode labels separate, 10 of 10.
_COLOURS = {
    "KS": line_registry.colour("keisei-main-line"), "KM": "#E060D0",
    "JB": line_registry.colour("jr-east-chuo-sobu-line"),
    "JO": line_registry.colour("jr-east-yokosuka-line"),
    "JM": line_registry.colour("jr-east-musashino-line"),
    "JE": line_registry.colour("jr-east-keiyo-line"),
    "T": line_registry.colour("tokyo-metro-tozai-line"), "TR": "#20A800",
    "TD": line_registry.colour("tobu-urban-park-line"),
    "HS": line_registry.colour("hokuso-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS[_k]
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own stations inside the city line, for the three
# lines whose operator's list was read. The Toyo Rapid Railway's station
# guide links nine station pages, the first five (西船橋 to 船橋日大前) inside
# the city (toyokosoku.co.jp/station, read 2026-10-11); the Hokuso Railway's
# site links 14 station pages, 小室 the one inside (the brief's check,
# 2026-10-11); Tokyo Metro numbers the Tozai Line T01 to T23, T22 原木中山 and
# T23 西船橋 inside (its station numbering, as Tokyo's gate 3 reads it; its
# site refused a scripted read on 2026-10-11). JR East's services are the
# route lists above; Keisei's and Tobu's lines are cut at the city line and
# have no independent count here.
GATE3 = {"source": "The Toyo Rapid Railway's station guide (9 station pages, 5 inside the city), the Hokuso "
                   "Railway's station pages (14, 1 inside) and Tokyo Metro's station numbering (T01 to T23, "
                   "T22 and T23 inside), read against the city line",
         "lines": {"T": 2, "TR": 5, "HS": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
FUNABASHI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = FUNABASHI_BBOX
