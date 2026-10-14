"""Shizuoka-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/shizuoka.md (10/10 checks, 2026-10-11). Part of the A/B
build plan's Regional-2 batch, on the shared modules
(pipeline/countries/japan*.py) with every shared rule on. Personal services
only (Band B, owner 2026-10-04: Yokohama's page shape): MHLW's food file
publishes an address for 60.3% of the city's open restaurant permits, under
the placement bar, and the city's own old-law list (375 rows) cannot close
the gap.

Business leg: the city's three 生活衛生 registers on BODIK (organization
221007, author 生活衛生課, cc-by): barbers, beauty salons and laundries, each a
full list as of 2026-03-31 plus the monthly files of new permits since.
Closures after 2026-03-31 are not published, so each register is an UPPER
BOUND on its last month (Kyoto's call: pinned to the last month read). The
2025-03-31 lists match e-Stat's 衛生行政報告例 FY2024 (beauty 1,732 against
1,731, laundries 312 against 312; a measurement, not drawn). Everything placed
by a JOIN to MLIT's 位置参照情報 for the three wards.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The Shizuoka Railway's Shizuoka-Shimizu Line and JR Central's Tokaido
Line; the Oigawa Railway's Ikawa Line is left out (owner). English station
names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "shizuoka" / "raw"
DATA_PROCESSED = ROOT / "data" / "shizuoka" / "processed"
OUTPUTS = ROOT / "outputs" / "shizuoka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Shizuoka"
SLUG = "shizuoka"
MUNICIPALITY = "静岡市"
PREFECTURE = "静岡県"

# The city's BODIK catalogue (owner, call 11: the city's own copy, never the
# prefecture's portal, whose terms add a reimbursement clause). Each dataset's
# record declares cc-by; the city's terms make it CC BY 4.0 (read 2026-10-05).
# The monthly files hold new permits only, and a trade's month is uploaded
# only when it has one (no barber file for R8.4, R8.5, R8.7 or R8.9; no
# laundry file for R8.5, R8.6 or R8.8).
BODIK = "https://data.bodik.jp/dataset"
_PAGE = {"barber": f"{BODIK}/221007_riyoujo-20160331", "beauty": f"{BODIK}/221007_biyoujo-20160331",
         "laundry": f"{BODIK}/221007_cleaning-20160331"}
_DS = {"barber": "f4b70b46-ad92-4af7-84bb-3282d9fcfdff", "beauty": "1ea5012b-1ee2-4b62-ac8c-3b2be3458e0f",
       "laundry": "7dfdd56d-30e6-40da-9bb8-308a68aacd7e"}
# The three datasets reuse monthly file names (r8.4.csv is both a beauty and a
# laundry file), so each is kept under its dataset's prefix.
_PREFIX = {"barber": "riyoujo", "beauty": "biyoujo", "laundry": "cleaning"}
# key -> (trade, resource id, the publisher's file name, its as-of date)
_LISTS = {
    "barber": ("barber", "247daa58-9b6e-41db-9887-356f12eb4bd4", "riyosyo.csv", "2026-03-31"),
    "barber_0806": ("barber", "01e4b295-55f1-4102-a7c9-e96115683f3d", "r8.6.csv", "2026-06-30"),
    "barber_0808": ("barber", "495b4f14-256c-4a31-86a8-ebd1b3286400", "r8.8.csv", "2026-08-31"),
    "beauty": ("beauty", "ad3911f5-a842-4325-b890-36f4931d2103", "biyosyo20260331.csv", "2026-03-31"),
    "beauty_0804": ("beauty", "e486a2ed-fa07-4940-86a2-0765733d2b19", "r8.4.csv", "2026-04-30"),
    "beauty_0805": ("beauty", "5e8842d6-ec44-41e6-b8e2-697661c371c9", "r8.5.csv", "2026-05-31"),
    "beauty_0806": ("beauty", "4751e1bc-d965-41fb-bc85-31f638f388c8", "r8.6.csv", "2026-06-30"),
    "beauty_0807": ("beauty", "d533980a-8422-4c70-b6c5-b23dc2b6cd31", "-r8.7.csv", "2026-07-31"),
    "beauty_0808": ("beauty", "410dabe5-742b-4c74-ab94-d5a57341e9a9", "r8.8.csv", "2026-08-31"),
    "beauty_0809": ("beauty", "89c45ab3-e692-4a7f-8e8e-5a436f2c9353", "r8.9.csv", "2026-09-30"),
    "laundry": ("laundry", "e3d76212-bdc1-455c-b343-4ac0cb825b1a", "cleaning20260331.csv", "2026-03-31"),
    "laundry_0804": ("laundry", "91d74981-5c20-4802-953b-79aee2d1250c", "r8.4.csv", "2026-04-30"),
    "laundry_0807": ("laundry", "9b65adee-94d2-4c25-9bce-9ea7b9a1da9d", "-r8.7.csv", "2026-07-31"),
    "laundry_0809": ("laundry", "d6a03278-591d-40ab-aae5-ed02056233fa", "r8.9.csv", "2026-09-30"),
}
SOURCE_FILES = {
    k: (f"{_PREFIX[t]}_{name.lstrip('-')}", f"{BODIK}/{_DS[t]}/resource/{rid}/download/{name}", _PAGE[t])
    for k, (t, rid, name, _) in _LISTS.items()}
SOURCE_AS_OF = {k: d for k, (_, _, _, d) in _LISTS.items()}
# What step 2 reads: each trade's full list plus its monthly additions
# (source_rows); the monthly files are read inside it only.
SOURCES = {k: SOURCE_FILES[k][0] for k in ("barber", "beauty", "laundry")}
MONTHLY = {t: tuple(k for k, v in _LISTS.items() if v[0] == t and k != t) for t in SOURCES}
# Each register's date, PINNED to the last month read (never the download's):
# an upper bound, openings added, closures not. The owner asked for each
# list's date on the page (2026-10-04).
TRADE_AS_OF = {t: SOURCE_AS_OF[MONTHLY[t][-1]] for t in SOURCES}
REGISTERS_AS_OF = max(TRADE_AS_OF.values())
FOOD_AS_OF = None  # no food leg (MHLW's addresses fail placement)
# Declared, never inferred: the full barber and beauty lists are UTF-8 with a
# BOM, the laundry list cp932, and the monthly files either; city_rows sniffs
# each file.
SOURCE_ENCODING = {"barber": "utf-8-sig", "beauty": "utf-8-sig", "laundry": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (開設者氏名 and 開設者法人, a
# company's representative; the laundry months' 営業者氏名 and 法人代表者) are
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; they are read IN MEMORY by that
# rule only, never kept. Never selected: 施設電話番号, 開設者住所 / 営業者住所 (an
# operator's own address).
_FULL = ("施設名称", "施設所在地", "業種", "開設者氏名", "開設者法人")
_MONTH = ("施設名称", "施設所在地", "業種名称", "開設者氏名", "開設者法人")
_MONTH_LAUNDRY = ("施設名称", "施設所在地", "業種名称", "営業者氏名", "法人代表者")
REQUIRED_COLUMNS = {
    k: (_FULL if k in SOURCES else _MONTH_LAUNDRY if t == "laundry" else _MONTH)
    for k, (t, _, _, _) in _LISTS.items()}
# The columns carried into step 2: the premises' own, the kind (a 無店舗
# laundry agent is not a premises) and the operator columns for the name rule
# (in memory).
_KEEP = ("施設名称", "施設所在地", "業種", "業種名称", "開設者氏名", "開設者法人", "営業者氏名", "法人代表者")


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def source_rows(key):
    """A register's rows (japan_step2 reads this hook where a city defines it):
    its full list (2026-03-31) and every monthly addition since, in one
    stream, the premises and name-rule columns only. No file carries a permit
    number; the brief measured that no monthly row from R8.4 on repeats a
    full-list (address, name) pair (0 of 37), and step 2 keeps one pin per
    address, name and bucket anyway."""
    from pipeline.countries import japan_register as jr

    for k in (key, *MONTHLY[key]):
        path = source_csv(k)
        if not path.exists():
            raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
        for r in jr.city_rows(path):
            yield {c: r.get(c) for c in _KEEP if c in r}


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 22101 to 22103.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Shizuoka.
# S, W, N, E: the city's N03 extent (S 34.8985, W 138.0830, N 35.6460,
# E 138.6385) rounded out; step 1 stops if the city leaves it. The box
# reaches the Southern Alps; every drawn station lies south of 35.13 N.
OSM_BBOX = (34.88, 138.07, 35.66, 138.65)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the western edge (138.083) and 静岡 station (138.389) both
# fall in the 138 to 144 band. Derived per city, not copied (Hamamatsu, 50 km
# west, is 53N) - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): step 1 measured a median nearest-station gap of 610 m over
# the 24 drawn stations (2026-10-11; the brief read 624 m), above the ~550 m
# halving threshold; the Shizuoka
# Railway's own median is 595 m. Re-measure if the drawn stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines; the Shinkansen's 静岡 dropped). The Shizuoka-Shimizu
# Line lies wholly inside (15 of 15); JR's Tokaido Line keeps 10 of 89, cut at
# the city line (owner 2026-09-24). 草薙 is one group on both lines (176 m).
_SR, _JR, _OI = "静岡鉄道", "東海旅客鉄道", "大井川鐵道"
LEFT_OUT_LINES = {
    # A mountain scenic line (owner, 2026-10-04: leave it out): its 2 in-city
    # stations, 閑蔵 and 井川, sit about 30 km north of 静岡 and its other 12
    # in 川根本町. Kobe's and Kyoto's sightseeing precedent, so its stations
    # are not written to excluded_stations.csv.
    (_OI, "井川線"): "a mountain sightseeing line, left out whole (owner, 2026-10-04)",
}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names carry no macrons.
LINES = {
    "SS": {"n02": [(_SR, "静岡清水線")], "name": "Shizuoka-Shimizu Line", "name_ja": "静岡清水線",
           "short": "Shizutetsu", "hue": "#0068B7"},
    "JT": {"n02": [(_JR, "東海道線")], "name": "JR Tokaido Line", "name_ja": "東海道線", "short": "JR",
           "hue": "#F68B1E"},
}
# Colours: JR Central's Tokaido Line takes its one site-wide colour from
# pipeline/line_registry.py (owner, 2026-10-07: one colour per line on every
# map). The Shizuoka-Shimizu Line is on this map alone.
_COLOURS = {"SS": "#0068B8", "JT": line_registry.colour("jr-central-tokaido-line")}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the Shizuoka Railway's station index
# (train.shizutetsu.co.jp/timetable/timetable-station, read 2026-10-05 and
# re-checked 2026-10-11) links 15 station timetables, S01 新静岡 to S15
# 新清水, as N02 has 15. JR is cut at the city line.
GATE3 = {"source": "The Shizuoka Railway's station index (train.shizutetsu.co.jp/timetable/timetable-station): "
                   "15 stations, 新静岡 to 新清水",
         "lines": {"SS": 15}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SHIZUOKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SHIZUOKA_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604674742)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # worship body: dropped in the full read (owner, 2026-10-13)
    "node/1520555256": "'インナートリップセンター静岡': no religion tag; the name is a religious body's training hall (Inner Trip is the Reiyukai's name for its centres, from memory, not from a tag), not a named temple (full read, worship body)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/322456336": "'ピクニック広場': \"picnic plaza\" with no proper name; same family as the rule words 芝生広場, 多目的広場, 自由広場 (full read, bare type)",
    "node/1835094117": "'地蔵堂': Jizo hall under its type alone; the rule has 地蔵 and 大師堂 but not 地蔵堂 (full read, bare type)",
    "node/1827258314": "'文殊堂': Monju hall under its type alone (rule has 文殊菩薩, 大師堂) (full read, bare type)",
    "way/139539753": "'閻魔堂': Enma hall under its type alone (full read, bare type)",
    "node/4348068104": "'稲荷大明神': \"Inari Daimyojin\", the deity's title alone; the rule has 正一位稲荷大明神 only (full read, bare type)",
    "node/5839586855": "'忠霊塔': war-dead memorial tower under its type alone (rule has 表忠碑, 戦没記念碑); 忠霊塔公園 nearby is a separate named park and stays (full read, bare type)",
    "node/11770747381": "'耕地整理記念碑': \"land readjustment memorial stone\", a type of monument, tagged leisure=park on a node (full read, bare type)",
    # description: dropped in the full read (owner, 2026-10-13)
    "way/59331678": "'大慈悲院川の一部': \"part of the Daijihiin river\": a mapper's note as the name (note tag carries the river's name); 大慈悲院川 has its own row (full read, description)",
    "way/171793464": "'駐屯地 外曲輪': \"garrison, outer bailey\": two feature words, no proper name, tagged a park beside the Mariko castle ruins (full read, description)",
    "way/232598645": "'東キャンプ場': \"east campsite\", a part of 浜石野外センター (its own row, 150 m) (full read, description)",
    "way/232598659": "'西キャンプ場': \"west campsite\", a part of 浜石野外センター (its own row, 100 m) (full read, description)",
    # glitch: dropped in the full read (owner, 2026-10-13)
    "node/2316488038": "'延寿院\u200e': name ends in an invisible U+200E mark; a real temple with wikidata, so a repair upstream would keep it (full read, glitch)",
}
# Why this index reaches more than 25 km past the map's stations
# (scripts/check_place_scope.py, rule D): a far corner of the municipality itself.
PLACE_SCOPE_REACH_REASON = "2026-10-13: Aoi Ward runs north into the Southern Alps (三峰岳, 塩見岳) (owner)"
