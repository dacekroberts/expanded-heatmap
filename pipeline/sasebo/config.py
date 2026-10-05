"""Sasebo-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/sasebo.md
(9/9 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Kitakyushu's food shape: MHLW's filings
plus the city's own list of pre-2021-law permits, food only.

Business leg: two food lists split by the 2021 law. MHLW's
食品衛生申請等システム open data holds every permit since 2021-06 and the
notifications (opt-in, field by field); the city's own CC BY 4.0 list on BODIK
holds the old-law permits (as of 2026-04-30), kept only while in term on
MHLW's date. A premises in both is shown once (config.SUPERSEDES). The city
publishes no barber, beauty or laundry register, so there are no personal
services (Band B, food only). All placed by a JOIN to MLIT's 位置参照情報 (one
municipality, no wards); where the block join misses an MHLW row, MHLW's own
point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The Matsuura Railway's Nishi-Kyushu Line, which leaves the city through
Saza and comes back, and JR Kyushu's Sasebo and Omura lines. English station
names from OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "sasebo" / "raw"
DATA_PROCESSED = ROOT / "data" / "sasebo" / "processed"
OUTPUTS = ROOT / "outputs" / "sasebo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Sasebo"
SLUG = "sasebo"
MUNICIPALITY = "佐世保市"
PREFECTURE = "長崎県"

# The city's list on BODIK (data.bodik.jp, the city's catalogue,
# odcs.bodik.jp/422029), license_id cc-by-40-intl, under the catalogue's terms
# (佐世保市オープンデータ利用規約 第3条(1): CC BY 4.0; read 2026-10-02). The
# file is the edition this build read, pinned. MHLW 食品衛生申請等システム open
# data, PDL 1.0 (the system's site terms §2; read 2026-09-24 for Fukuoka).
# Credit links the top page only.
BODIK = "https://data.bodik.jp/dataset"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the page that links it and carries its licence)
SOURCE_FILES = {
    "mhlw": ("42202_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=42202_food_business_all.csv",
             MHLW_TOP),
    "food": ("dataset_kaiseimaer8.4.csv",
             f"{BODIK}/571df2fc-f781-4a2c-b9d7-09e1637b15fe/resource/f7fa490e-026d-4330-8c34-10e7c367c13d/"
             "download/dataset_kaiseimaer8.4.csv",
             f"{BODIK}/422029_syokuhineigyoukyoka"),
}
# The dates the lists state (Kyoto's rule, never the download's): the old-law
# list's 「(令和8年4月末時点)法改正前食品営業許可施設一覧」; MHLW's file states
# none (its newest 許可年月日 2026-08-28), so the page dates it by download
# (provenance.json).
SOURCE_AS_OF = {"mhlw": None, "food": "2026-04-30"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# The resource name, as the city's credit must print it (第3条(2)(イ)).
RESOURCE_NAMES = {"food": "(令和8年4月末時点)法改正前食品営業許可施設一覧"}
# The old-law list keeps a permit until its next yearly edition even after its
# 終了年月日 has passed, so step 2 drops rows past expiry against this PINNED
# date, MHLW's end of August 2026 (japan_register.in_term, which reads the
# list's `R 8. 5.31` dates), never today: 452 of 607 rows are in term on it
# (the brief's count).
OLD_LAW_AS_OF = datetime.date(2026, 8, 31)
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: MHLW's file is UTF-8; the old-law list UTF-8 with
# a BOM, the header on line 1.
SOURCE_ENCODING = {"mhlw": "utf-8-sig", "food": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The old-law list's 申請者_氏名 (filled on 343 of 607
# rows; the city removes a sole trader's own name) is REQUIRED so the name
# rule (japan_register.name_is_operator; owner 2026-09-27) cannot silently
# compare nothing; it is read IN MEMORY by that rule only, never kept. Its 種目
# is read as the form of business (旅館, 自動販売機, 仕出し屋 out). Never
# selected: 施設_電話番号(固定), and MHLW's 法人名 / 法人番号 / 法人住所 and phones.
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "food": ("施設_名称", "施設_所在地", "業種", "種目", "終了年月日", "申請者_氏名"),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 41 m from the block point, 90.6% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both food lists: the city's old-law row goes, MHLW's (the
# newer filing) stays. The brief's screen: 20 of the 346 old-law restaurants in
# term share a block and trade name with an MHLW permit.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    The old-law food list only where its permit is in term on OLD_LAW_AS_OF
    (終了年月日); every other file as it is."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    rows = jr.city_rows(path)
    if key == "food":
        rows = jr.in_term(rows, ("終了年月日",), OLD_LAW_AS_OF)
    yield from rows


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one municipality.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Sasebo.
# S, W, N, E: the city's N03 extent (S 33.050, W 129.056, N 33.343, E 129.873;
# 宇久島, merged in 2006, is its western edge) rounded out; step 1 stops if the
# city leaves it.
OSM_BBOX = (33.03, 129.04, 33.36, 129.89)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen, Hepburn throughout (OSM writes two Matsuura
# stations in Kunrei or with ou, and misspells いのつき). The other 22 are OSM's
# as they stand.
OSM_NAME_EN_OVERRIDES = {
    "大塔": "Daito",                         # Daitou
    "江迎鹿町": "Emukae-Shikamachi",         # Emukaishikamachi
    "いのつき": "Inotsuki",                  # Inoysuki
    "佐世保中央": "Sasebo-chuo",             # Sasebo-Chuou
    "泉福寺": "Senpukuji",                   # Senpukuzi
    "潜竜ヶ滝": "Senryugataki",              # Senryūgataki
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~129.72) falls in the 126 to 132 band. Derived
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
# 2026-10-03: 3 lines, no Shinkansen). Every line is cut at the city line
# (owner 2026-09-24): the Matsuura Railway's 西九州線 22 of 57, JR's 佐世保線 5
# of 14 and 大村線 3 of 15. The Matsuura line leaves the city through 佐々町
# (its stations excluded) and comes back at 吉井 to 江迎鹿町 (the former
# Yoshii, Emukae and Shikamachi towns): both in-city pieces are drawn, with
# the track through Saza between them.
LEFT_OUT_LINES = {}
# JR's Sasebo Line runs on to Arita in Saga Prefecture: its N03 names the
# stations beyond the prefecture line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("41",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names follow the operators' signs
# with no macrons, as Kitakyushu's.
_MR, _JR = "松浦鉄道", "九州旅客鉄道"
LINES = {
    "MR": {"n02": [(_MR, "西九州線")], "name": "Matsuura Railway Nishi-Kyushu Line", "name_ja": "西九州線",
           "short": "MR", "hue": "#0068B7"},
    "JS": {"n02": [(_JR, "佐世保線")], "name": "JR Sasebo Line", "name_ja": "佐世保線", "short": "JR",
           "hue": "#E60012"},
    "JO": {"n02": [(_JR, "大村線")], "name": "JR Omura Line", "name_ja": "大村線", "short": "JR",
           "hue": "#009944"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# sasebo` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. The Matsuura Railway's blue, which
# no blue clears Retail's pin in, goes teal. Closest pair within 500 m 122.7,
# anywhere 92.3; the dark-mode labels separate, 3 of 3.
_COLOURS = {"MR": "#007890", "JS": "#E80010", "JO": "#30A800"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city, so the Matsuura Railway's own
# route map (matutetu.com/pages/12/, read 2026-10-03), read against the city
# line, gives the Nishi-Kyushu Line's in-city stops: 佐世保 to 真申 (16), then,
# past Saza's four, 吉井, 潜竜ヶ滝, いのつき, 高岩, 江迎鹿町 and すえたちばな (6):
# 22. JR's two lines are N02's.
GATE3 = {"source": "the Matsuura Railway's route map (matutetu.com/pages/12/), read against the city line",
         "lines": {"MR": 22}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SASEBO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SASEBO_BBOX
