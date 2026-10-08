"""Mito-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/mito.md
(14/14 checks, 2026-10-07). Japan's A/B batch (Regional-1), on the shared
modules (pipeline/countries/japan*.py) with the Japan foundation's rules on
(2026-10-07), in Kurume's shape for food (MHLW's open data alone, the city's
own food page pointing to it) and Hamamatsu's for the registers (one file per
kind).

Business leg: MHLW's 食品衛生申請等システム open data for Mito City (every
permit and notification the city entered since 2021-06; opt-in, field by
field), its notifications kept as a partial food-retail layer (call 127b).
Personal services: the city's four 生活衛生関係施設一覧 CSVs (保健衛生課,
CC-BY with no version given), barbers, beauty salons, general laundries and
laundry pick-up counters, as of 2026-07-02. All placed by a JOIN to MLIT's
位置参照情報 (one municipality, no wards); where the block join misses an MHLW
row, MHLW's own point.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR East's Joban and Suigun lines and Kashima Rinkai's Oarai Kashima
Line; JR's seasonal 偕楽園 left out (owner, call 156). English station names
from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "mito" / "raw"
DATA_PROCESSED = ROOT / "data" / "mito" / "processed"
OUTPUTS = ROOT / "outputs" / "mito"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Mito"
SLUG = "mito"
MUNICIPALITY = "水戸市"
PREFECTURE = "茨城県"

# The city's own CMS. The dataset page 生活衛生関係施設一覧 (更新日 2026-07-15)
# states 「ライセンス CC-BY」 and 「コピーライト 水戸市役所」 with no version and
# no link; no open-data 利用規約 exists. Read 2026-10-07 by staging
# (licence-read): permitted with conditions on Bremen's precedent (call 196),
# credited "CC-BY, no version given" with the copyright line, the title, the
# page link and a modification statement; no cost clause. The page notes that
# closed premises may remain (※2).
_HOST = "https://www.city.mito.lg.jp"
_ATT = _HOST + "/uploaded/attachment/"
LIFE_PAGE = _HOST + "/site/open-data/4496.html"
# The city's 食品営業許可施設一覧 page (open-data/3745.html) holds no file: it
# points to MHLW's per-municipality download, the city's food list (Kurume's).
FOOD_PAGE = _HOST + "/site/open-data/3745.html"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2,
# termsofuse.htm; read 2026-09-24 for Fukuoka, re-read 2026-10-02). A plain
# GET. Credit links the top page only, as the site asks.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the page that carries its licence). One entry per
# file fetched (Step 0, 2026-10-06, each HTTP 200 from its publisher's own
# host). The page's fifth laundry file (71290.csv, 無店舗取次店, storeless
# pick-ups) is not premises and is not fetched (japan_eigyo, Fukushima's).
SOURCE_FILES = {
    "mhlw": ("08201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=08201_food_business_all.csv",
             MHLW_TOP),
    "barber": ("71286.csv", _ATT + "71286.csv", LIFE_PAGE),
    "beauty": ("71287.csv", _ATT + "71287.csv", LIFE_PAGE),
    "laundry": ("71288.csv", _ATT + "71288.csv", LIFE_PAGE),
    "laundry_pickup": ("71289.csv", _ATT + "71289.csv", LIFE_PAGE),
}
# The registers' file names are attachment ids, and a refresh posts new ids;
# japan_fetch.current_url's SOURCE_LINKS matches an href, not a link's text,
# so the URLs are pinned and a refresh updates them here by the link texts
# 施設一覧（理容所）, （美容所）, （クリーニング所・一般）, （クリーニング所・取次店）.
# Two laundry registers (general laundries 一般 and pick-up counters 取次店), one
# kind: the KEY names the source, the kind decides the bucket (Hamamatsu's
# SOURCE_KIND).
SOURCE_KIND = {"laundry_pickup": "laundry"}
# Kyoto's rule: the date each list states, never the download's. The four
# link texts read 令和８年７月２日現在; MHLW's monthly file states none (its
# newest 許可年月日 2026-08-31).
REGISTERS_AS_OF = "2026-07-02"
FOOD_AS_OF = None
SOURCE_AS_OF = {"mhlw": None, "barber": REGISTERS_AS_OF, "beauty": REGISTERS_AS_OF, "laundry": REGISTERS_AS_OF,
                "laundry_pickup": REGISTERS_AS_OF}
# Call 161 (owner, 2026-10-06): a permit is read against the last day its
# file covers, never today. MHLW's file covers August 2026; it still lists 80
# permits past their 許可満了日 on that date (the brief; 16 of them addressed
# restaurants). The registers carry no term.
TERM_AS_OF = {"mhlw": "2026-08-31"}

SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: MHLW's UTF-8 with a BOM; the city's four Shift_JIS
# (cp932) with CRLF, header on row 1.
SOURCE_ENCODING = {"mhlw": "utf-8-sig", "barber": "cp932", "beauty": "cp932", "laundry": "cp932",
                   "laundry_pickup": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing, and are read IN MEMORY by that rule only, never kept: MHLW's 法人名
# (a sole trader's own name as often as a company's, owner 2026-10-05) and
# the registers' 営業者氏名 and 代表者氏名 (no company marker on 234 of 258
# barbers, 606 of 821 beauty salons). Never selected: 法人番号, 法人住所,
# 営業施設電話番号 and the registers' 施設電話番号.
_REGISTER = ("屋号", "施設所在地", "営業者氏名", "代表者氏名")
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "許可満了日", "法人名"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": _REGISTER,
    "laundry_pickup": _REGISTER,
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's): a
# row without one is counted apart for the page's disclosure. 252 restaurant
# rows read only 水戸市内一円 / 茨城県内一円 / 市内一円 (vehicles and stalls
# licensed area-wide): not premises.
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses, MHLW's own point places it (call 127c; the
# brief's check: a median 64 m from the block point, 88.3% within 250 m,
# 2,998 rows).
OWN_POINT_FALLBACK = {"mhlw"}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 08201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Mito.
# S, W, N, E: the city's N03 extent (S 36.301, W 140.322, N 36.464,
# E 140.587; 内原町 merged in 2005) rounded out; step 1 stops if the city
# leaves it.
OSM_BBOX = (36.29, 140.31, 36.47, 140.60)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (no macrons, lowercase after a hyphen for a
# common word, a katakana loanword as its English word, 前 as -mae). None is
# needed: OSM's 5 names stand as they are (23 objects, 22 with name:en,
# 2026-10-07; no macron, a place name after a hyphen capitalised as Akita's
# and Fukushima's: Higashi-Mito).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~140.436) and the whole extent (140.322 to
# 140.587) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median nearest-station gap is
# 3,818 m (1,854 to 5,757), far over the spacing rule's halving line (about
# 550 m): standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-07: 3 lines, the brief's table; no Shinkansen in the city). Every
# line is cut at the city line (owner 2026-09-24): JR's Joban Line keeps 4
# of 81 station records (3 once 偕楽園 is out), Kashima Rinkai's Oarai
# Kashima Line 3 of 15 and JR's Suigun Line 1 of 45. The Suigun Line's one
# station is 水戸, its terminus, with 3.8 km of its track inside the city: a
# JR one-station stub kept as cut by the standing call (Kobe's JR Takarazuka
# Line, Akita's Oga Line), not an urban line, so no owner question. The Mito
# Line (水戸線, 小山 to 友部) has no track inside the city; its trains run
# over the Joban to 水戸 and are not a drawn line. No frequency floor (owner,
# 2026-10-06, calls 46 and 86), and no stretch runs at about 11 trains a day
# or fewer: the thinnest is the Suigun from 水戸, 26 a weekday (JR East's
# timetable, read 2026-10-06 for the brief).
LEFT_OUT_LINES = {}
# A station N02-25 still has but no train stops at (japan_step1's
# CLOSED_STATIONS, Kitakyushu's 西黒崎): dropped before the collapse and
# written nowhere.
CLOSED_STATIONS = {
    ("東日本旅客鉄道", "常磐線", "偕楽園"):
        "JR East's temporary station for the plum season at Kairakuen, with no train in the October 2026 "
        "timetable (timetables.jreast.co.jp/timetable/list0415.html, read 2026-10-06): left out by the "
        "owner, call 156 (Kyoto's Sagano and Kitakyushu's Mojiko Retro precedents)",
}
# 水戸 is one N02 group for the three lines (three records, 68 m).
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (`hue`) and the
# project's colour. Line names follow the operators' signs with no macrons and
# no "Main", as Akita's and Fukushima's JR lines. Hues: the operators' line
# colours as starting points only, since the colours are the project's own.
_JR, _KR = "東日本旅客鉄道", "鹿島臨海鉄道"
LINES = {
    "JJ": {"n02": [(_JR, "常磐線")], "name": "JR Joban Line", "name_ja": "常磐線", "short": "JR",
           "hue": "#0072BC"},
    "SG": {"n02": [(_JR, "水郡線")], "name": "JR Suigun Line", "name_ja": "水郡線", "short": "JR",
           "hue": "#3CB371"},
    "OK": {"n02": [(_KR, "大洗鹿島線")], "name": "Kashima Rinkai Oarai Kashima Line", "name_ja": "大洗鹿島線",
           "short": "Kashima Rinkai", "hue": "#E4007F"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# mito` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its starting hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. The Joban blue goes cyan (45.1 from
# Retail's pin), the Suigun green olive as Akita's Oga Line (45.0 from
# Personal services'), the Kashima Rinkai magenta toward violet (45.2 from
# Food service's). Closest pair 69.6 (Joban, Suigun); the dark-mode labels
# separate, 3 of 3.
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search: the
# Suigun Line's olive #586818 sat 15.8 from it, under the owner's floor of 20
# (2026-10-07). It takes #007430, a dark green, as Akita's Oga Line: the
# colour nearest JR East's #3CB371 that reads 3:1 on both pages and clears 25
# from every pin (25.2 from Personal services', 38.0 from olive, between 20
# and 45: an accepted trade). Closest pair now 62.3 (Joban, Suigun).
_COLOURS = {"JJ": "#08A0C0", "SG": "#007430", "OK": "#F000B8"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: JR East's own station timetable pages (timetables.jreast.co.jp, the
# index list<code>.html per station, read 2026-10-06 for the brief) list the
# Joban Line at 内原, 赤塚 and 水戸 with service inside the city (偕楽園, the
# fourth, has none: CLOSED_STATIONS) and the Suigun Line at 水戸; Kashima
# Rinkai's timetable (rintetsu.co.jp/timetable, the 2026-03-14 timetable)
# lists 水戸, 東水戸 and 常澄 inside the city.
GATE3 = {"source": "JR East's station timetable pages (timetables.jreast.co.jp): Joban Line 3 inside the city "
                   "with service, Suigun Line 1; Kashima Rinkai's timetable (rintetsu.co.jp): Oarai Kashima Line 3",
         "lines": {"JJ": 3, "SG": 1, "OK": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
MITO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = MITO_BBOX
