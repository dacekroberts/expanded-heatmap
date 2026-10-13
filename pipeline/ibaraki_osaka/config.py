"""Ibaraki-specific settings (the city in Osaka Prefecture, slug ibaraki_osaka:
the name alone is also a prefecture), scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/ibaraki_osaka.md. Japan A/B batch (Kansai-2, 2026-10-11), on
the shared modules (pipeline/countries/japan*.py) and the Japan foundation's
rules (ALL_RULES).

Business leg: Osaka Prefecture's 理容所届出施設一覧 and 美容所届出施設一覧 on BODIK,
which cover the 32 municipalities the prefecture licenses (Osaka, Sakai and the
seven core cities license their own), so Ibaraki is in them: each kind's full
list as of 2026-03-31 plus its five monthly new-premises files to 2026-08.
Every row is assigned to Ibaraki BY ITS ADDRESS (Itami's shape): one that
begins 茨木市. One bucket, Personal services, barbers and beauty salons only:
the prefecture publishes no laundry list and no food list for these towns
(owner, 2026-10-06, the band row). Placed by a JOIN to MLIT's 位置参照情報 for
the one municipality (27211, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The Osaka Monorail's main line and Saito Line, Hankyu's Kyoto Line and
JR West's Kyoto Line, cut at the city line. English station names from
OpenStreetMap's name:en.
"""

import unicodedata
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "ibaraki_osaka" / "raw"
DATA_PROCESSED = ROOT / "data" / "ibaraki_osaka" / "processed"
OUTPUTS = ROOT / "outputs" / "ibaraki_osaka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Ibaraki (Osaka)"
SLUG = "ibaraki_osaka"
MUNICIPALITY = "茨木市"
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
    stream, cut to the rows whose address begins 茨木市 (never by the files'
    section labels), the premises columns only. A premises a monthly file
    repeats from the full list under the same address and name is read once.
    A row that names 茨木市 anywhere else stops the build (Tsu's rule): its
    municipality would be a guess. Measured 2026-10-06 (the brief): barbers
    142 + 0, beauty salons 474 + 10."""
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


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27211.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Ibaraki.
# S, W, N, E: the city's N03 extent (S 34.775, W 135.496, N 34.929, E 135.606)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.77, 135.49, 34.93, 135.61)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
# 南茨木: Hankyu's object reads "Minami-Ibaraki", the Monorail's "Minami Ibaraki"
# (2026-10-11); the hyphenated form, as Shin-Itami and Minami-Senri.
OSM_NAME_EN_TIES = {"南茨木": "Minami-Ibaraki"}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word.
OSM_NAME_EN_OVERRIDES = {
    "阪大病院前": "Handai-byoin-mae",                # Handaibyoin-Mae
    "彩都西": "Saito-nishi",                          # Saito-Nishi
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.55) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 1,048 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# the brief: 4 lines, no Shinkansen station), each cut at the city line (owner
# 2026-09-24): the Osaka Monorail's main line (3 of 14) and Saito Line (3 of
# 5), Hankyu's 京都線 (3 of 27) and JR West's 東海道線, signed the JR Kyoto
# Line (2 of 59). No line is cut to one station.
LEFT_OUT_LINES = {}
# Hankyu and JR run on into Kyoto Prefecture, the Monorail's main line into
# Hyogo (Itami): their N03 names the stations beyond the prefecture line
# (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("26", "28")
# 南茨木 (Hankyu and the Monorail, 114 m) is the one interchange group; JR 茨木
# and Hankyu 茨木市 are separate stations, kept apart as N02 keeps them.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02's 東海道線 is signed the JR Kyoto Line
# here, as on Osaka's, Kyoto's and Suita's maps.
_HK, _JR, _MO = "阪急電鉄", "西日本旅客鉄道", "大阪モノレール"
LINES = {
    "MO": {"n02": [(_MO, "大阪モノレール線")], "name": "Osaka Monorail Main Line", "name_ja": "大阪モノレール本線",
           "short": "Monorail", "hue": "#0067B0"},
    "MS": {"n02": [(_MO, "国際文化公園都市モノレール線(彩都線)")], "name": "Osaka Monorail Saito Line",
           "name_ja": "大阪モノレール彩都線", "short": "Monorail", "hue": "#0067B0"},
    "HY": {"n02": [(_HK, "京都線")], "name": "Hankyu Kyoto Line", "name_ja": "阪急京都線", "short": "Hankyu",
           "hue": "#87544B"},
    "JY": {"n02": [(_JR, "東海道線")], "name": "JR Kyoto Line", "name_ja": "JR京都線", "short": "JR",
           "hue": "#0072BC"},
}
# Colours: every line here is drawn on another city's map too, so each takes
# its one site-wide colour from pipeline/line_registry.py (owner, 2026-10-07:
# one colour per line on every map), never a value of this city's own. The
# Saito Line entered the registry with this build, in the colour Suita's map
# already drew.
_COLOURS = {
    "MO": line_registry.colour("osaka-monorail-main-line"),
    "MS": line_registry.colour("osaka-monorail-saito-line"),
    "HY": line_registry.colour("hankyu-kyoto-line"),
    "JY": line_registry.colour("jr-west-kyoto-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists inside the city (the brief:
# Monorail main line 宇野辺, 南茨木, 沢良宜; Saito Line 阪大病院前, 豊川, 彩都西;
# Hankyu 総持寺, 茨木市, 南茨木; JR JR総持寺, 茨木).
GATE3 = {"source": "The Osaka Monorail's, Hankyu's and JR West's station timetable pages, read 2026-10-06",
         "lines": {"MO": 3, "MS": 3, "HY": 3, "JY": 2}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
IBARAKI_OSAKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = IBARAKI_OSAKA_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600357872)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
PLACE_DROPPED = {}
