"""Minoh-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/minoh.md. Japan A/B batch (Kansai-2, 2026-10-11), on
the shared modules (pipeline/countries/japan*.py) and the Japan foundation's
rules (ALL_RULES).

Business leg: Osaka Prefecture's 理容所届出施設一覧 and 美容所届出施設一覧 on BODIK,
which cover the 32 municipalities the prefecture licenses (Osaka, Sakai and the
seven core cities license their own), so Minoh is in them: each kind's full
list as of 2026-03-31 plus its five monthly new-premises files to 2026-08.
Every row is assigned to Minoh BY ITS ADDRESS (Itami's shape): one that
begins 箕面市. One bucket, Personal services, barbers and beauty salons only:
the prefecture publishes no laundry list and no food list for these towns
(owner, 2026-10-06, the band row). Placed by a JOIN to MLIT's 位置参照情報 for
the one municipality (27220, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Hankyu's Minoh Line and Kita-Osaka Kyuko's Namboku Line, cut at the
city line. English station names from
OpenStreetMap's name:en.
"""

import unicodedata
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "minoh" / "raw"
DATA_PROCESSED = ROOT / "data" / "minoh" / "processed"
OUTPUTS = ROOT / "outputs" / "minoh"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Minoh"
SLUG = "minoh"
MUNICIPALITY = "箕面市"
PREFECTURE = "大阪府"

# Osaka Prefecture's two BODIK packages (organisation 270008), CC BY 4.0 by
# 大阪府オープンデータ利用規約 第1条 (https://odcs.bodik.jp/270008/tos/; DECISIONS.md,
# "Licence reads for the Japan builds"). The full lists renew twice a year;
# between them the prefecture adds one file of NEW premises per month and
# kind, and publishes no closures.
_BODIK = "https://data.bodik.jp/dataset/"
_RIYOU = _BODIK + "7ef31733-3fef-4fae-a163-b91c75f1eac2/resource/"
_BIYOU = _BODIK + "e8079500-b5cd-497f-84d9-c21999d876a2/resource/"
RIYOU_PAGE = "https://data.bodik.jp/dataset/270008_riyou-ichiran"
BIYOU_PAGE = "https://data.bodik.jp/dataset/270008_biyou-ichiran"
# key -> (file, resource id, dataset page, the last day the file covers)
_LISTS = {
    "barber": ("riyou-ichiran-0803.xlsx", _RIYOU + "96f0f303-c561-4e47-a3a4-da7f1e2a133f", RIYOU_PAGE, "2026-03-31"),
    "barber_0804": ("0804-riyou.xlsx", _RIYOU + "938f0717-b717-4171-8396-aeeab88bd06e", RIYOU_PAGE, "2026-04-30"),
    "barber_0805": ("0805-riyou.xlsx", _RIYOU + "df2aff84-df0b-4ed2-804a-6419d2468af4", RIYOU_PAGE, "2026-05-31"),
    "barber_0806": ("0806-riyou-.xlsx", _RIYOU + "60ff6fd4-6d00-4ff3-a179-8b172b85fd50", RIYOU_PAGE, "2026-06-30"),
    "barber_0807": ("0807-riyou-.xlsx", _RIYOU + "f26306ae-c008-4dec-a8ee-fb105c9a3342", RIYOU_PAGE, "2026-07-31"),
    "barber_0808": ("0808-riyou-.xlsx", _RIYOU + "8e907cf5-77cc-45e4-99bc-2b62f7539a00", RIYOU_PAGE, "2026-08-31"),
    "beauty": ("biyou-ichiran-0803.xlsx", _BIYOU + "1a4a47bb-4431-4f86-b946-c51810645de4", BIYOU_PAGE, "2026-03-31"),
    "beauty_0804": ("0804-biyou.xlsx", _BIYOU + "bbaba29f-6fba-4620-94b6-efb6a3286103", BIYOU_PAGE, "2026-04-30"),
    "beauty_0805": ("0805-biyou.xlsx", _BIYOU + "07d3a383-61e1-4ac6-981a-2187862f4dc3", BIYOU_PAGE, "2026-05-31"),
    "beauty_0806": ("0806-biyou.xlsx", _BIYOU + "fb497d52-5b14-44f2-b35c-b7f573992d3c", BIYOU_PAGE, "2026-06-30"),
    "beauty_0807": ("0807-biyou.xlsx", _BIYOU + "20723676-00d9-4169-91b4-ba6825e569ca", BIYOU_PAGE, "2026-07-31"),
    "beauty_0808": ("0808-biyou.xlsx", _BIYOU + "18d7b97a-adbe-4412-a656-02189c8b1f7d", BIYOU_PAGE, "2026-08-31"),
}
SOURCE_FILES = {k: (f, f"{res}/download/{f}", page) for k, (f, res, page, _) in _LISTS.items()}
SOURCE_AS_OF = {k: d for k, (_, _, _, d) in _LISTS.items()}
# The register's date, PINNED to the last month read (never the download's):
# an upper bound, openings added, closures since 2026-03-31 not shown (Kyoto's
# and Kochi's call).
REGISTERS_AS_OF = "2026-08-31"
FOOD_AS_OF = None  # no food leg: no list for the prefecture-licensed towns
# What step 2 reads: each kind's full list plus its monthly additions
# (source_rows); the monthly files are read inside it only.
SOURCES = {"barber": SOURCE_FILES["barber"][0], "beauty": SOURCE_FILES["beauty"][0]}
MONTHLY = {kind: tuple(k for k in _LISTS if k.startswith(kind + "_")) for kind in SOURCES}
SOURCE_ENCODING = {k: "xlsx" for k in SOURCE_FILES}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 開設者 (the operator) is REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; it is read IN MEMORY by that rule only, never kept. Never selected:
# 電話番号 / 施設電話番号.
REQUIRED_COLUMNS = {k: (("理容所名称" if k.startswith("barber") else "美容所名称"), "所在地", "開設者")
                    for k in SOURCE_FILES}
# The columns carried into step 2: the premises' own and the operator column
# for the name rule (in memory).
_KEEP = ("理容所名称", "美容所名称", "所在地", "開設者")


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _address(r):
    a = unicodedata.normalize("NFKC", (r.get("所在地") or "")).replace(" ", "").replace("　", "")
    return a[len(PREFECTURE):] if a.startswith(PREFECTURE) else a


def source_rows(key):
    """A register's rows (japan_step2 reads this hook where a city defines it):
    the prefecture's full list and every monthly addition since, in one
    stream, cut to the rows whose address begins 箕面市 (never by the files'
    section labels), the premises columns only. A premises a monthly file
    repeats from the full list under the same address and name is read once.
    A row that names 箕面市 anywhere else stops the build (Tsu's rule): its
    municipality would be a guess. Measured 2026-10-06 (the brief): barbers
    52 + 0, beauty salons 240 + 5."""
    from pipeline.countries import japan_register as jr

    seen = set()
    for k in (key, *MONTHLY[key]):
        path = source_csv(k)
        if not path.exists():
            raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
        for r in jr.city_rows(path):
            a = _address(r)
            if not a.startswith(MUNICIPALITY):
                if MUNICIPALITY in a and not a.endswith("一円"):
                    raise SystemExit(f"{path.name}: a row names {MUNICIPALITY} after its start - assign it by hand")
                continue
            name = unicodedata.normalize("NFKC", str(r.get("理容所名称") or r.get("美容所名称") or "")).strip()
            if (a, name) in seen:
                continue
            seen.add((a, name))
            yield {c: r.get(c) for c in _KEEP if c in r}


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27220.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Minoh.
# S, W, N, E: the city's N03 extent (S 34.807, W 135.437, N 34.911, E 135.526)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.80, 135.43, 34.92, 135.53)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word.
OSM_NAME_EN_OVERRIDES = {
    "箕面船場阪大前": "Minoh-semba-handai-mae",      # Minoh-semba handai-mae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.48) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 1,095 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# the brief: 2 lines, no Shinkansen), each cut at the city line (owner
# 2026-09-24): Hankyu's 箕面線 (3 of 4; its junction 石橋阪大前 is in Ikeda) and
# Kita-Osaka Kyuko's 南北線 (2 of 6, the 2024 extension to 箕面萱野). No line is
# cut to one station.
LEFT_OUT_LINES = {}
# Both lines stay inside Osaka Prefecture.
N03_NEIGHBOR_PREFS = ()
# No interchange: five stations, five groups, the nearest two 883 m apart.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour.
_HK, _KK = "阪急電鉄", "北大阪急行電鉄"
LINES = {
    "HM": {"n02": [(_HK, "箕面線")], "name": "Hankyu Minoh Line", "name_ja": "阪急箕面線", "short": "Hankyu",
           "hue": "#8B2A3A"},
    "KK": {"n02": [(_KK, "南北線")], "name": "Kita-Osaka Kyuko Namboku Line", "name_ja": "北大阪急行南北線",
           "short": "Kita-Osaka Kyuko", "hue": "#E81820"},
}
# Colours: Kita-Osaka Kyuko's line is drawn on Suita's and Toyonaka's maps
# too, so it takes its one site-wide colour from pipeline/line_registry.py
# (owner, 2026-10-07: one colour per line on every map). The Minoh Line is on
# no other map: its colour is this project's own (2026-10-11), the colour
# nearest Hankyu's maroon that reads 3:1 on both map pages, clears CIE76 45
# from every pin (47.7) and stands 20.1 from the Hankyu Takarazuka Line's
# #B7572D, which it meets at 石橋阪大前 on Toyonaka's map (the neighbour rule).
# `scripts/line_colour_search.py minoh` alone returns the Takarazuka Line's
# own colour, since it reads one map. Closest pair here 39.1 or more.
_COLOURS = {
    "HM": "#905840",
    "KK": line_registry.colour("kita-osaka-kyuko-namboku-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists inside the city (the brief: Hankyu
# 桜井, 牧落, 箕面; Kita-Osaka Kyuko 箕面船場阪大前, 箕面萱野).
GATE3 = {"source": "Hankyu's and Kita-Osaka Kyuko's station timetable pages, read 2026-10-06",
         "lines": {"HM": 3, "KK": 2}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
MINOH_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = MINOH_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600358662)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/minoh.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A description standing in for a name (owner, 2026-10-13)
    "way/82722271": "'支流(1)': 'tributary (1)': a mapper's label for an unnamed culverted stream",
    "way/82725498": "'支流(2)': 'tributary (2)': a mapper's label for an unnamed stream",
    "way/82720138": "'箕面川支流': 'tributary of the Minoh river': a description, not the stream's name",
    "node/11035174641": "'生活環境保全林': 'living-environment conservation forest': a forestry land class mapped as a locality, not a name",
    # A religious office, hall, school or residence (owner, 2026-10-13)
    "way/528257270": "'大阪聖ヨゼフ宣教修道女会 本部': headquarters (本部) of a congregation of missionary sisters tagged a place of worship; no wikidata; name is the body's, not a church's",
}
