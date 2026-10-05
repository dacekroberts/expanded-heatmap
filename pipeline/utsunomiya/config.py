"""Utsunomiya-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/utsunomiya.md
(14/14 checks, 2026-10-02). A city of the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py), in Fukuoka's two-source shape.

Business leg: two food lists split by the 2021 law. MHLW's
食品衛生申請等システム open data holds every permit since 2021-06 and the
notifications (opt-in, field by field); the city's own CC BY list holds the
old-law permits still in term (令和８年７月現在). A premises in both is shown
once (config.SUPERSEDES). Personal services: the city's barber, beauty and two
laundry registers (pick-up and general), all 令和８年７月現在. All placed by a
JOIN to MLIT's 位置参照情報 for the one municipality (no wards); where the
block join misses an MHLW row, MHLW's own point (OWN_POINT_FALLBACK).

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). The Utsunomiya Light Rail, Tobu's Utsunomiya
Line and JR's Utsunomiya and Nikko lines. English station names from
OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "utsunomiya" / "raw"
DATA_PROCESSED = ROOT / "data" / "utsunomiya" / "processed"
OUTPUTS = ROOT / "outputs" / "utsunomiya"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Utsunomiya"
SLUG = "utsunomiya"
MUNICIPALITY = "宇都宮市"
PREFECTURE = "栃木県"

# The city's CKAN catalogue (宇都宮市オープンデータ). Each dataset records
# license_id cc-by (「クリエイティブ・コモンズ 表示」, no version); the portal's
# terms (data.city.utsunomiya.tochigi.jp/terms) apply PDL 1.0 unless a dataset
# says otherwise, and both permit the map on the same conditions (read
# 2026-10-02). The files are the editions this build read, every resource
# titled 令和８年７月現在; package_show re-read 2026-10-02 found no newer one
# (the food list's resource modified 2026-08-25, the two laundry files'
# 2026-04-27 under the same July title).
CKAN = "https://catalog.city.utsunomiya.tochigi.jp/dataset"
# MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site terms §2;
# read 2026-09-24 for Fukuoka). A plain GET. Credit links the top page only.
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL, the page that links it and carries its licence)
SOURCE_FILES = {
    "mhlw": ("09201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=09201_food_business_all.csv",
             MHLW_TOP),
    "food": ("092011_seikatsueisei_shokuhin_shokuhin.csv",
             f"{CKAN}/4b5cae93-4640-4b4e-87bb-a5e18042366c/resource/a53500f2-7ba1-4e77-a906-e17dc5b60714/"
             "download/092011_seikatsueisei_shokuhin_shokuhin.csv",
             f"{CKAN}/syokuhinneigyoukyoka"),
    "barber": ("092011_seikatsueisei_kankyo_riyozyo.csv",
               f"{CKAN}/787d42bf-ef7a-4cfb-bfe3-b2d436402253/resource/0aa9d94e-369a-4e7b-8d48-5ab874f3d4da/"
               "download/092011_seikatsueisei_kankyo_riyozyo.csv",
               f"{CKAN}/riyoujoichiran"),
    "beauty": ("092011_seikatsueisei_kankyo_-biyozyo.csv",
               f"{CKAN}/dcb9f255-2a52-4930-90ab-6c1fda354c87/resource/ec507449-b946-4e29-bb6e-e921cdd5bef3/"
               "download/092011_seikatsueisei_kankyo_-biyozyo.csv",
               f"{CKAN}/ubiyouzyo"),
    "laundry_agent": ("092011_seikatsueisei_kankyo_-kuriningutoritsugi.csv",
                      f"{CKAN}/467b3c29-17b4-4b38-bd49-55b9bec46670/resource/908957e0-e854-4992-8d7e-a4b0d3556b7a/"
                      "download/092011_seikatsueisei_kankyo_-kuriningutoritsugi.csv",
                      f"{CKAN}/kuriiningutoritsugiichiran"),
    "laundry_general": ("092011_seikatsueisei_kankyo_kurininguippan.csv",
                        f"{CKAN}/8004a533-3811-4d56-b103-02f154d3e1f7/resource/6e285563-ece3-4f7b-a0fd-757cf6e93c34/"
                        "download/092011_seikatsueisei_kankyo_kurininguippan.csv",
                        f"{CKAN}/kuriininguippanichiran"),
}
# Kyoto's rule: the date the list states, never the download's. Every city
# resource is titled 令和８年７月現在, read as the month's last day; MHLW's
# monthly file states none (its newest 許可年月日 is 2026-08-28).
SOURCE_AS_OF = {"mhlw": None, "food": "2026-07-31", "barber": "2026-07-31", "beauty": "2026-07-31",
                "laundry_agent": "2026-07-31", "laundry_general": "2026-07-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# The old-law list keeps a permit until its next edition even when its
# 満了年月日3 has passed, so step 2 drops rows past expiry against this PINNED
# date (japan_register.in_term), never today. On the July edition it drops
# none: the earliest expiry is 2026-08-31 (measured 2026-10-02).
OLD_LAW_AS_OF = datetime.date(2026, 7, 31)
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The two laundry registers are one kind (japan_step2.kind): the key names the
# file, the kind decides the bucket.
SOURCE_KIND = {"laundry_agent": "laundry", "laundry_general": "laundry"}
# Declared, never inferred: MHLW's file and the city's food list are UTF-8
# with a BOM; the four registers cp932 (the header opens with №; the general
# laundry file's header cells are padded with spaces, which city_rows strips).
SOURCE_ENCODING = {"mhlw": "utf-8-sig", "food": "utf-8-sig", "barber": "cp932", "beauty": "cp932",
                   "laundry_agent": "cp932", "laundry_general": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 申請者氏名 (food), 開設者 and 代表者 (registers) are
# REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; they are read IN MEMORY by that
# rule only, never kept. Never selected: the phones, 申請者住所 and 開設者住所
# (an operator's own address), and MHLW's 法人名 / 法人番号 / 法人住所.
_REGISTER = ("営業所所在地", "開設者", "代表者")
REQUIRED_COLUMNS = {
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "food": ("営業所名称", "業種名", "営業所", "申請者氏名", "満了年月日3"),
    "barber": ("営業所名称", *_REGISTER),
    "beauty": ("名称", *_REGISTER),
    "laundry_agent": ("名称", *_REGISTER),
    "laundry_general": ("名称", *_REGISTER),
}
# MHLW publishes an address only where the filer agreed to it (Fukuoka's).
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 46 m from the block point, 96.0% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both food lists: the city's old-law row goes, MHLW's (the
# newer filing) stays. The brief's screen: 54 of MHLW's 4,712 block-tier
# restaurants (1.1%) are in the old-law list.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    The old-law food list only where its permit is in term on OLD_LAW_AS_OF
    (満了年月日3); every other file as it is."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    rows = jr.city_rows(path)
    if key == "food":
        rows = jr.in_term(rows, ("満了年月日3",), OLD_LAW_AS_OF)
    yield from rows


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 09201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and the light rail's
# stops (railway=tram_stop, which the station query does not take). Which
# stations exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 36.464, W 139.743, N 36.730, E 140.011)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (36.45, 139.73, 36.75, 140.03)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-02): OSM spells Tobu's 江曾島 with the common
# form 曽.
OSM_NAME_ALIASES = {"江曾島": "江曽島"}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen. OSM TRANSLATED nine of the light rail's 15
# in-city stops (Fukuoka's trap); each is romanised here, a katakana loanword
# (キャンパス, スタジアム, センター) kept as its English word. 宇都宮駅東口 is its
# own N02 group beside JR's 宇都宮, so it is romanised whole, never "Utsunomiya".
OSM_NAME_EN_OVERRIDES = {
    "宇都宮駅東口": "Utsunomiya-eki-higashiguchi",       # Utsunomiya Station East
    "駅東公園前": "Ekihigashi-koen-mae",                 # Ekihigashi Park
    "宇都宮大学陽東キャンパス": "Utsunomiya-daigaku Yoto Campus",  # Utsunomiya Univ. Yoto Campus
    "平石中央小学校前": "Hiraishi-chuo-shogakko-mae",     # Hiraishi-chuo Elem. Sch.
    "飛山城跡": "Tobiyama-jo-ato",                       # Tobiyama Castle Site
    "清陵高校前": "Seiryo-koko-mae",                     # Seiryo High School
    "清原地区市民センター前": "Kiyohara-chiku-shimin Center-mae",  # Kiyohara District Civic Center
    "グリーンスタジアム前": "Green Stadium-mae",          # Green Stadium
    "ゆいの杜西": "Yuinomori-nishi",                     # Yuinomori-west
    "ゆいの杜中央": "Yuinomori-chuo",                    # Yuinomori-central
    "ゆいの杜東": "Yuinomori-higashi",                   # Yuinomori-east
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the longitude (~139.88) falls in the 138 to 144 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 4 lines, no Shinkansen once 宇都宮's 東北新幹線 platform is
# dropped). The light rail keeps 15 of its 19 stops (4 in Haga), Tobu's
# Utsunomiya Line 4 of 11, JR's 東北線 3 of 155 and 日光線 2 of 7, each cut at
# the city line (owner 2026-09-24). No line is cut to a stub. JR's 烏山線 runs
# from 宝積寺 in N02, so it has no in-city station.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. JR East signs its 東北線 here as the
# Utsunomiya Line (宇都宮線), the name riders read.
_LR, _TB, _JR = "宇都宮ライトレール", "東武鉄道", "東日本旅客鉄道"
LINES = {
    "LR": {"n02": [(_LR, "宇都宮芳賀ライトレール線")], "name": "Utsunomiya Light Rail", "name_ja": "ライトライン",
           "short": "Light Rail", "hue": "#FFD400"},
    "TU": {"n02": [(_TB, "宇都宮線")], "name": "Tobu Utsunomiya Line", "name_ja": "東武宇都宮線",
           "short": "Tobu", "hue": "#0F6CC3"},
    "JU": {"n02": [(_JR, "東北線")], "name": "JR Utsunomiya Line", "name_ja": "宇都宮線", "short": "JR",
           "hue": "#F68B1E"},
    "JN": {"n02": [(_JR, "日光線")], "name": "JR Nikko Line", "name_ja": "日光線", "short": "JR", "hue": "#A2272D"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# utsunomiya` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide):
# each the feasible colour nearest its operator's hue that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. The light rail's yellow goes
# to ochre; Tobu's blue, which no blue clears Retail's pin in, to teal.
# Closest pair 28.0 (JR's two lines, which meet at 宇都宮); the dark-mode
# labels separate, 4 of 4.
_COLOURS = {"LR": "#B09000", "TU": "#08A0C0", "JU": "#E07800", "JN": "#D06840"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own stop list (miyarail.co.jp/rail-map, read
# 2026-10-02) names 19 stops, 宇都宮駅東口 to 芳賀・高根沢工業団地, as N02 does;
# its last four (芳賀台 onward) are in Haga, so 15 are inside the city. The
# lines the city line cuts have no in-city count of their own.
GATE3 = {"source": "Utsunomiya Light Rail's stop list (miyarail.co.jp/rail-map): 19 stops, 15 in the city",
         "lines": {"LR": 15}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
UTSUNOMIYA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = UTSUNOMIYA_BBOX
