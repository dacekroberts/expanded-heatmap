"""Higashiosaka-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/higashiosaka.md
(12/12 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py). Food only (Band B, Hiroshima's and Sakai's
page): the city publishes no barber, beauty or laundry list (its own 環境衛生
pages and BODIK org 272272 hold none).

Business leg: the city's BODIK dataset 食品等営業許可一覧 (272272_15, CC BY 4.0,
健康部食品衛生課, the Digital Agency's national schema): every permit in force
on 2026-04-01 (全許可) plus each month's new permits to 2026-08-31, REBUILT
into one register (japan_register.rebuilt_register, Kyoto's method) and kept
while 許可満了日 is on or after the pinned AS_OF. Closures after 2026-04-01 are
not published (廃業年月日 is empty in every file), so the register is an upper
bound for five months; the page says so. Placed by a JOIN to MLIT's
位置参照情報 for the one municipality (27227, no wards). MHLW's file for the city
holds notifications only (the city files its permits in its own system): a
control, never a source (Toyama's precedent).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Kintetsu's Nara, Osaka and Keihanna lines, Osaka Metro's Chuo Line
(drawn cut to its 2 stations, owner 2026-10-02) and JR West's Osaka Higashi
and Gakkentoshi lines. English station names from OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "higashiosaka" / "raw"
DATA_PROCESSED = ROOT / "data" / "higashiosaka" / "processed"
OUTPUTS = ROOT / "outputs" / "higashiosaka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Higashiōsaka"
SLUG = "higashiosaka"
MUNICIPALITY = "東大阪市"
PREFECTURE = "大阪府"

# BODIK (data.bodik.jp), dataset b5eeed4c-... (272272_15), license_id
# cc-by-40-intl; the catalogue's terms (odcs.bodik.jp/272272/tos/,
# 東大阪市オープンデータ利用規約 2) grant CC BY 4.0 unless a dataset sets its own.
DATASET_ID = "b5eeed4c-cec0-4eef-8513-b4882d6a18ec"
DATASET_PAGE = f"https://data.bodik.jp/dataset/{DATASET_ID}"
TERMS_PAGE = "https://odcs.bodik.jp/272272/tos/"
_RES = f"{DATASET_PAGE}/resource/"
# The monthly new-permit resources since the full list's date (February and
# March 2026 predate it and are not read): (month, resource id, last day).
MONTHS = (
    ("04", "981be3b9-1f13-457f-b62e-7a6fb5be92cd", "20260430"),
    ("05", "881ae94f-bfc7-48f8-8e9e-a3d26dfe94fd", "20260531"),
    ("06", "efb9b81f-e7d8-4999-8613-daebc0e397c2", "20260630"),
    ("07", "99f4b033-12b9-4c03-afda-364203e6c45d", "20260731"),
    ("08", "10698d75-c301-4c25-84e4-55fc4cf39aa6", "20260831"),
)
SOURCE_FILES = {
    # 「（全許可）（令和8年4月1日現在）」: every permit in force then (uploaded 2026-07-16)
    "food": ("272272_food_business_all_20260401.csv",
             _RES + "a0416f70-bda0-46fe-a684-b22a95135c32/download/272272_food_business_all_20260401.csv",
             DATASET_PAGE),
    **{f"new_{m}": (f"272272_food_business_new_2026{m}01_{end}.csv",
                    f"{_RES}{rid}/download/272272_food_business_new_2026{m}01_{end}.csv", DATASET_PAGE)
       for m, rid, end in MONTHS},
}
# The rebuilt register's date, PINNED (Kyoto's rule: the last day the newest
# file covers, never the download date or today): the August list.
AS_OF = datetime.date(2026, 8, 31)
SOURCE_AS_OF = {"food": "2026-04-01",
                **{f"new_{m}": f"{end[:4]}-{end[4:6]}-{end[6:]}" for m, _, end in MONTHS}}
FOOD_AS_OF = AS_OF.isoformat()
# What step 2 reads: the rebuilt register only (source_rows("food")). The
# monthly files are read inside the rebuild.
SOURCES = {"food": SOURCE_FILES["food"][0]}
# Declared, never inferred: UTF-8 CSV with a BOM, every file.
SOURCE_ENCODING = {k: "utf-8-sig" for k in SOURCE_FILES}
# The national schema's columns each raw file must carry (fetch_sources.py
# and source_rows stop on a header without them). 法人名 holds a sole trader's
# own name as well as a company's, so it is REQUIRED and read IN MEMORY by the
# name rule only, never kept (owner 2026-10-05, reversing Okayama's call of
# 2026-10-02). Never selected: 施設電話番号, 連絡先メールアドレス, 連絡先FormURL,
# 連絡先備考_その他SNSなど and 法人番号.
RAW_COLUMNS = ("施設名称", "営業の種類", "業態", "所在地_連結表記", "許可年月日", "許可満了日", "廃業年月日",
               "法人名")
# step 2 checks the rebuilt rows (japan_register.rebuilt_register's premises
# columns) against REQUIRED_COLUMNS["food"]: the columns both shapes carry.
REQUIRED_COLUMNS = {
    "food": ("施設名称", "業態", "許可年月日", "許可満了日", "廃業年月日"),
    **{f"new_{m}": RAW_COLUMNS for m, _, _ in MONTHS},
}
# NO OWN_POINT_FALLBACK (recorded, 2026-10-03): the list's own 緯度 / 経度 are
# in the old Tokyo Datum (the brief: a median 448 m from the block point, one
# consistent offset; 37 m once shifted from EPSG:4301 to JGD2000), and 431 rows
# carry a zero point. The rebuilt rows carry no coordinates on purpose, and
# the 21 chōme-tier rows (0.4%) do not need them; japan_step2.datum_guard would
# stop a fallback on an unshifted file.


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _paths():
    """The full list, then each month oldest first, each checked for the
    national schema's columns before it is read."""
    from pipeline.countries import japan_register as jr

    paths = [source_csv("food")] + [source_csv(f"new_{m}") for m, _, _ in MONTHS]
    for p in paths:
        if not p.exists():
            raise SystemExit(f"missing {p}\nRun: python pipeline/{SLUG}/fetch_sources.py")
        head = next(iter(jr.city_rows(p)))
        missing = [c for c in RAW_COLUMNS if c not in head]
        if missing:
            raise SystemExit(f"{p.name}: header lacks {missing} - not the file the brief read")
    return paths


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    "food" is the register rebuilt from the full list of 2026-04-01 and the
    monthly new permits (Kyoto's method, japan_register.rebuilt_register):
    where (address, trade name, type without （旧）) repeats, the permit
    ending latest wins; kept while 許可満了日 is on or after AS_OF. Measured
    2026-10-03 (the brief, reproduced): 7,067 rows read, 6,709 after
    de-duplication, 6,521 in term. Only premises columns are carried, plus the
    name rule's answer; no contact or company column leaves the file."""
    from pipeline.countries import japan_register as jr

    if key != "food":
        raise KeyError(key)
    return jr.rebuilt_register(_paths(), AS_OF)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27227.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Higashiosaka.
# S, W, N, E: the city's N03 extent (S 34.632, W 135.557, N 34.704, E 135.679)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.62, 135.54, 34.72, 135.69)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word. The other 24 are OSM's as they
# stand. 高井田中央 / 高井田, JR河内永和 / 河内永和 and JR俊徳道 / 俊徳道 (39 to 79
# m apart) are separate N02 groups of different names, the operators' own
# separate stations: kept apart (Kawasaki's Mizonokuchi precedent).
OSM_NAME_EN_OVERRIDES = {
    "瓢箪山": "Hyotanyama",                          # Hyōtan-yama
    "河内小阪": "Kawachi-Kosaka",                    # Kawachi Kosaka
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.60) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 767 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-03: 6 lines, no Shinkansen): Kintetsu's Nara (11 of 19), Osaka (4
# of 49) and Keihanna (4 of 4, N02's class-21 section from 長田 to the city
# line) lines, Osaka Metro's Chuo Line (2 of 12: 高井田, 長田; an urban subway
# drawn cut, owner 2026-10-02, Sakai's Midosuji precedent) and JR West's
# Osaka Higashi (5 of 14) and Gakkentoshi (片町線, 2 of 24) lines, cut at the
# city line (owner 2026-09-24). Every line runs on into Osaka City (built),
# Yao, Daito or Ikoma; Osaka's map cuts the same lines on its side.
LEFT_OUT_LINES = {}
# The Kintetsu Nara and Keihanna lines run on into Nara prefecture (Ikoma):
# its N03 names the stations beyond the prefecture line.
N03_NEIGHBOR_PREFS = ("29",)
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. The Keihanna Line runs through onto the
# Chuo Line at 長田; N02 files each under its own legal section, so each is
# drawn under its own public name (trap 2).
_KT, _JR = "近畿日本鉄道", "西日本旅客鉄道"
LINES = {
    "KN": {"n02": [(_KT, "奈良線")], "name": "Kintetsu Nara Line", "name_ja": "近鉄奈良線", "short": "Kintetsu",
           "hue": "#E2001A"},
    "KO": {"n02": [(_KT, "大阪線")], "name": "Kintetsu Osaka Line", "name_ja": "近鉄大阪線", "short": "Kintetsu",
           "hue": "#B43009"},
    "KH": {"n02": [(_KT, "けいはんな線")], "name": "Kintetsu Keihanna Line", "name_ja": "けいはんな線",
           "short": "Kintetsu", "hue": "#00A960"},
    "C": {"n02": [("大阪市高速電気軌道", "4号線(中央線)")], "name": "Osaka Metro Chuo Line", "name_ja": "中央線",
          "short": "Osaka Metro", "hue": "#5D662A"},
    "JH": {"n02": [(_JR, "おおさか東線")], "name": "JR Osaka Higashi Line", "name_ja": "おおさか東線", "short": "JR",
           "hue": "#A28DA8"},
    "JG": {"n02": [(_JR, "片町線")], "name": "JR Gakkentoshi Line", "name_ja": "学研都市線", "short": "JR",
           "hue": "#C303A8"},
}
# The four lines Osaka's map also draws (the Kintetsu Osaka, Chuo, Osaka
# Higashi and Gakkentoshi lines) start the search from Osaka's own colours
# (pipeline/osaka/config.py), so the two maps agree where they meet; the
# Nara and Keihanna lines from Kintetsu's hues. Colours: the project's own,
# from `python scripts/line_colour_search.py higashiosaka` (2026-10-03,
# defaults: >= 18 within 500 m, >= 10 city-wide): each the feasible colour
# nearest its start that reads 3:1 on both map pages and clears CIE76 45
# from every pin; Osaka's four come back within one step of the search grid
# of Osaka's. Closest pair within 500 m and anywhere 20.7 (Kintetsu Nara /
# Osaka, at 布施); the dark-mode labels separate, 6 of 6.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "KN": line_registry.colour("kintetsu-nara-line"), "KO": line_registry.colour("kintetsu-osaka-line"),
    "KH": "#28A800", "C": line_registry.colour("osaka-metro-chuo-line"),
    "JH": line_registry.colour("jr-west-osaka-higashi-line"),
    "JG": line_registry.colour("jr-west-gakkentoshi-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no public line lies wholly inside the city (N02's Keihanna section,
# 4 of 4, is the inner end of a line that runs on to 学研奈良登美ヶ丘); step 1
# lists each line's in-city stations.
GATE3 = {"source": "no line wholly inside the city", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
HIGASHIOSAKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = HIGASHIOSAKA_BBOX
