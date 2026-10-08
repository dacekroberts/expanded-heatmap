"""Himeji-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/himeji.md
(17/17 checks, 2026-10-03). Japan wave 2, on the shared modules
(pipeline/countries/japan*.py), in Kawasaki's shape: the city's own lists, all
three buckets.

Business leg: the city's CC BY 4.0 catalogue (姫路市・播磨圏域連携中枢都市圏
オープンデータカタログサイト, 保健所衛生課): the full food-permit list and the
full barber, beauty-salon and laundry registers as of 2026-09-10, placed by a
JOIN to MLIT's 位置参照情報 for the one municipality (no wards; its towns
begin with former towns' 区, so an address is never split at a 区). MHLW's
open data for Himeji holds only the opt-in online filings (2% of the
official restaurant count): not used.

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). JR West's Kobe, Sanyo, Bantan and Kishin
lines and Sanyo Electric Railway's Main and Aboshi lines. English station
names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "himeji" / "raw"
DATA_PROCESSED = ROOT / "data" / "himeji" / "processed"
OUTPUTS = ROOT / "outputs" / "himeji"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Himeji"
SLUG = "himeji"
MUNICIPALITY = "姫路市"
PREFECTURE = "兵庫県"

# The city's CKAN (under /gkan/; the files under /admin/gkan/ answer a plain
# GET). Each dataset records license_id CC-BY-4.0; the catalogue's terms
# (Terms_of_use_260430.pdf, 施行 2026-03-06) give way to that marking (1.4(1))
# and prescribe the credit's form (1.1). Each dataset keeps about a year of
# monthly 全件 resources, the newest last: the build reads the newest, pinned
# by resource id (read 2026-10-02).
GKAN = "https://city.himeji.gkan.jp"
TERMS = GKAN + "/gkan/base/doc/Terms_of_use_260430.pdf"
_DS = GKAN + "/admin/gkan/dataset/"
# source key -> (file, URL, the dataset page that carries its licence)
SOURCE_FILES = {
    "food": ("282014_kyoka-syokuhinn_20260910.xlsx",
             _DS + "3868a36d-3029-4502-817b-3094e3ed4806/resource/0738c22f-2527-43d7-a96f-df2d6abb8f9f/download/"
             "282014_kyoka-syokuhinn_20260910.xlsx", GKAN + "/gkan/dataset/shokuhinn"),
    "barber": ("282014_kyoka-riyou_20260910.xlsx",
               _DS + "7d4810cc-723a-46a8-b2e2-98cb859cb65c/resource/f7d723fa-d1f6-4dbf-8291-6acb6cccc1aa/download/"
               "282014_kyoka-riyou_20260910.xlsx", GKAN + "/gkan/dataset/riyousyo"),
    "beauty": ("282014_kyoka-biyou_20260910.xlsx",
               _DS + "77e05f08-cefc-4a8d-8749-e4e239256059/resource/6b9230ee-715e-4b34-a424-8abb84a96f82/download/"
               "282014_kyoka-biyou_20260910.xlsx", GKAN + "/gkan/dataset/biyousyo"),
    "laundry": ("282014_kyoka-kuriininngu_20260910.xlsx",
                _DS + "66a768cb-5017-4e4b-8998-2479035b9dd3/resource/8d3ab779-8035-4dfd-9b5d-2d91c6418aad/download/"
                "282014_kyoka-kuriininngu_20260910.xlsx", GKAN + "/gkan/dataset/kuriininngu"),
}
# The dates the lists state (Kyoto's rule, never the download's): each
# resource's 「（全件）（令和8年9月10日時点）」. No food row's 有効期限 has passed
# on that date (the earliest is 2026-11-30), so no in-term filter is needed.
SOURCE_AS_OF = {k: "2026-09-10" for k in SOURCE_FILES}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: four XLSX, one sheet each (食品, 理容所, 美容所,
# クリーニング所), header on row 1.
SOURCE_ENCODING = {}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 氏名, the operator on every row (an individual's own
# name or a company's), is REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; it is read IN MEMORY by that rule only, never kept. Never
# selected: 電話番号 (every file), 方書.
REQUIRED_COLUMNS = {
    "food": ("業種", "氏名", "施設名称", "所在地"),
    "barber": ("業種", "氏名", "施設名称", "施設所在地"),
    "beauty": ("業種", "氏名", "施設名称", "施設所在地"),
    "laundry": ("業種", "氏名", "施設名称", "施設所在地"),
}
# The registers' second type 「（市条例第３条第２項該当）」 (4 barbers, 182
# beauty salons) marks a premises inspected and confirmed like any other; the
# city's facility standards (its 美容所の開設手続きについて, R7.4.24) excuse the
# hot-water hair-washing basin where a premises does no hair work. Counted as
# Personal services, as the source decides (2026-10-03; the drafts entry).


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 28201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Himeji.
# S, W, N, E: the city's N03 extent (S 34.593, W 134.422, N 35.094, E 134.814;
# the 家島 islands included) rounded out; step 1 stops if the city leaves it.
# The box the OSM query used (2026-10-03).
OSM_BBOX = (34.58, 134.41, 35.11, 134.83)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style as Kitakyushu's config describes (no
# macrons, 前 as -mae, lowercase after a hyphen). OSM's Himeji names carry
# macrons on four stations and write 山陽姫路 apart where 山陽網干 and 山陽天満
# take a hyphen; the other 26 are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "京口": "Kyoguchi",               # Kyōguchi
    "香呂": "Koro",                   # Kōro
    "太市": "Oichi",                  # Ōichi
    "大塩": "Oshio",                  # Ōshio
    "山陽姫路": "Sanyo-Himeji",        # Sanyo Himeji
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~134.69) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). The brief's median gap to the nearest station
# is 1,377 m: standard rings.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25:
# 5 lines; the Shinkansen's 姫路 platform dropped, 姫路 kept as a JR station).
# Sanyo's Aboshi Line lies wholly inside (7 of 7); its Main Line keeps 9 of
# 43, JR's 山陽線 7 of 131, 播但線 7 of 18 and 姫新線 4 of 36, each cut at the
# city line (owner 2026-09-24). No line is cut to a stub. 飾磨 is one N02 group
# for both Sanyo lines; JR's 姫路 and 山陽姫路 are separate groups.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour.
#
# JR West signs N02's 山陽線 as two lines that meet at 姫路: the JR Kobe Line
# east of it (東姫路, 御着, ひめじ別所, then 曽根 in Takasago, its end) and the
# Sanyo Line west of it (英賀保, はりま勝原, 網干), each a `route` over the one
# track (Tokyo's and Kawasaki's services). The Sanyo Line ends at 網干: the
# next station, 竜野, lies beyond the 3 km step 1 draws past the city line
# (japan_step1.DRAW_BEYOND_M), so a route cannot name it.
_JR, _SY = "西日本旅客鉄道", "山陽電気鉄道"
_SANYO_LINE = (_JR, "山陽線")
LINES = {
    "JA": {"route": [(*_SANYO_LINE, ["姫路", "東姫路", "御着", "ひめじ別所", "曽根"])],
           "name": "JR Kobe Line", "name_ja": "JR神戸線", "short": "JR", "hue": "#0072BC"},
    "JS": {"route": [(*_SANYO_LINE, ["網干", "はりま勝原", "英賀保", "姫路"])],
           "name": "JR Sanyo Line", "name_ja": "山陽本線", "short": "JR", "hue": "#0072BC"},
    "JJ": {"n02": [(_JR, "播但線")], "name": "JR Bantan Line", "name_ja": "播但線", "short": "JR",
           "hue": "#A2272D"},
    "JK": {"n02": [(_JR, "姫新線")], "name": "JR Kishin Line", "name_ja": "姫新線", "short": "JR",
           "hue": "#E95295"},
    "SM": {"n02": [(_SY, "本線")], "name": "Sanyo Electric Main Line", "name_ja": "山陽電鉄本線",
           "short": "Sanyo", "hue": "#D01911"},
    "SA": {"n02": [(_SY, "網干線")], "name": "Sanyo Electric Aboshi Line", "name_ja": "山陽電鉄網干線",
           "short": "Sanyo", "hue": "#D01911"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# himeji` (2026-10-03, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. JR's one blue splits into teal
# (Kobe Line) and slate (Sanyo Line); Sanyo's red into red (Main) and
# red-orange (Aboshi). Closest pair 18.9 (Sanyo's two lines, at 飾磨); the
# dark-mode labels separate, 6 of 6.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "JA": line_registry.colour("jr-west-kobe-line"), "JS": line_registry.colour("jr-west-sanyo-line"),
    "JJ": "#D06840", "JK": "#E060D0", "SM": line_registry.colour("sanyo-electric-main-line"),
    "SA": "#F86038",
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Sanyo Electric Railway's own station index
# (sanyo-railway.co.jp/railway/station/, read 2026-10-03) names all 15
# in-city stations: the Main Line's 大塩 to 山陽姫路 (9) and the Aboshi Line's
# 飾磨 to 山陽網干 (7, 飾磨 on both).
GATE3 = {"source": "Sanyo Electric Railway's station index (sanyo-railway.co.jp/railway/station/): Main Line "
                   "大塩-山陽姫路 9 and Aboshi Line 飾磨-山陽網干 7 inside the city",
         "lines": {"SM": 9, "SA": 7}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
HIMEJI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = HIMEJI_BBOX
