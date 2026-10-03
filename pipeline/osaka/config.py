"""Osaka-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/osaka.md.
Japan's second city, on the shared modules Kobe built: pipeline/countries/
japan.py (rail, city line), japan_register.py (the address join),
japan_step1.py and japan_step2.py. This file holds only what is Osaka's.

Business leg: Osaka City's 食品営業許可施設一覧 (the food-permit list, as of
2026-06-30) and its barber, beauty and laundry registers (2026-03-31), placed
by a JOIN to MLIT's 位置参照情報 for the 24 wards. The list's own coordinates
(its 経度 / 緯度 columns, swapped) are an independent check on the join, never
the map's source.

Rail: MLIT N02 (the N02-25 edition since 2026-10-03; not GTFS, not OSM), the
Shinkansen left out, stations kept only
inside the city line (N03). English station names from OpenStreetMap's name:en,
because N02 carries Japanese names only (owner, 2026-09-27).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "osaka" / "raw"
DATA_PROCESSED = ROOT / "data" / "osaka" / "processed"
OUTPUTS = ROOT / "outputs" / "osaka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Osaka"
SLUG = "osaka"
MUNICIPALITY = "大阪市"
PREFECTURE = "大阪府"

# Osaka City's own pages, each CC BY 4.0 (read 2026-09-24). The food list is
# re-issued each quarter under a new dated name (260630zenku.csv), so the file
# is the edition this build read, pinned, never "the newest". The portal's
# data-00000382 copy is a stale 2021 twin: not used.
CITY_HOST = "https://www.city.osaka.lg.jp"
FOOD_AS_OF = "2026-06-30"
REGISTERS_AS_OF = "2026-03-31"
# source key -> (file, URL, the page that links it and carries its licence)
SOURCE_FILES = {
    "food": ("260630zenku.csv", f"{CITY_HOST}/contents/wdu280/260630zenku.csv",
             f"{CITY_HOST}/kenko/page/0000575579.html"),
    "barber": ("ri20260331.csv", f"{CITY_HOST}/kenko/cmsfiles/contents/0000431/431136/ri20260331.csv",
               f"{CITY_HOST}/kenko/page/0000431136.html"),
    "beauty": ("bi20260331.csv", f"{CITY_HOST}/kenko/cmsfiles/contents/0000431/431136/bi20260331.csv",
               f"{CITY_HOST}/kenko/page/0000431136.html"),
    "laundry": ("cleaning20260331.csv", f"{CITY_HOST}/kenko/cmsfiles/contents/0000552/552712/cleaning20260331.csv",
                f"{CITY_HOST}/kenko/page/0000552712.html"),
}
# The key is the taxonomy's `source` column.
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred (docs/data_sources.md): all four are Shift-JIS
# (cp932) CSV, comma-separated (read 2026-09-27). japan_register.decode() reads them.
SOURCE_ENCODING = {"food": "cp932", "barber": "cp932", "beauty": "cp932", "laundry": "cp932"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 営業者名 (all four files) is read IN MEMORY by the name
# rule only (japan_register.name_is_operator; owner 2026-09-27) and never kept.
REQUIRED_COLUMNS = {
    "food": ("屋号", "業種分類", "営業所所在地"),
    "barber": ("施設名称", "施設所在地"),
    "beauty": ("施設名称", "施設所在地"),
    "laundry": ("施設名称", "施設所在地", "施設（種別）"),
}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (34.586-34.769 N, 135.344-135.599 E,
# measured 2026-09-27) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.55, 135.30, 34.80, 135.64)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
# The Hankai tram's stops: OSM tags them railway=tram_stop, which the station
# query does not take (owner approved this second query, 2026-09-27).
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
# How far an OSM station object may be from N02's group centroid and still name
# it (as Kobe: an interchange's parts sit up to ~300 m apart).
OSM_NAME_MATCH_M = 600
# Where OSM's objects for one station disagree on name:en, the spelling taken
# (2026-09-27): the operators' own signs.
OSM_NAME_EN_TIES = {
    # Osaka Metro's "Tenjinbashisuji 6-chome" against Hankyu's object's
    # "Tenjinbashisuji-rokuchome"; the Metro signs the numeral form.
    "天神橋筋六丁目": "Tenjinbashisuji 6-chome",
    # one object carries a malformed two-value tag ("Minami-morimachi;Minami-Morimachi")
    "南森町": "Minami-Morimachi",
    # JR West's and Hanshin's objects; both railways sign "Nishikujo"
    "西九条": "Nishikujo",
    # the Hankai tram's and the Sakaisuji Line's objects; both sign "Ebisucho"
    "恵美須町": "Ebisucho",
    # two Hankai tram_stop objects; Hankai signs "Matsudacho"
    "松田町": "Matsudacho",
}
# Where OSM's object has NO name:en, the English name taken instead - explicit
# and cited, never inferred; step 1 still stops on any station missing from here.
# JR 平野 (Yamatoji Line): OSM node 1727925081 has name=平野 and no name:en
# (2026-09-27); JR West signs it "Hirano", and the Metro's 平野 1.1 km away is
# "Hirano" in OSM. Owner 2026-09-27. The two become Hirano (JR) / Hirano (Metro).
# 天王寺駅前 (the Hankai Uemachi Line's terminus, HN-01): neither OSM query
# returned an object for it (2026-09-27); Hankai signs it "Tennoji-ekimae".
# Owner 2026-09-27.
OSM_NAME_EN_MISSING = {"平野": "Hirano", "天王寺駅前": "Tennoji-ekimae"}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.50) falls in the 132 to 138 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test, 2026-09-27: 34
# N02 lines), EXCEPT the Shinkansen (owner 2026-09-24, every Japanese city;
# japan.stations() drops it - Shin-Osaka stays, as a JR and subway station).
# JR and the private railways are cut at the city line (owner 2026-09-24). No
# URBAN line is cut to a stub: Osaka Metro keeps 80-100% of each line, the New
# Tram 10 of 10, the Hankai Line 17 of 32 (owner 2026-09-27: trams count) and
# the Uemachi Line 10 of 10. The short cuts are suburban lines (the Kintetsu
# Osaka Line keeps Ue-Hommachi, Tsuruhashi and Imazato; JR Gakkentoshi Kyōbashi,
# Shigino and Hanaten).
#
# Stations collapse on N02's station-group code (N02_005g), never the name
# (Kobe's lesson; japan_step1). Osaka's interchanges are wider than Kobe's
# (widest 273 m): Kyōbashi's five platforms span 387 m, Hommachi's three Metro
# lines 358 m and Shin-Osaka's 347 m (measured 2026-09-27), so the limit is
# 400 m here - still far below the 0.75-1.5 km of a wrong name merge.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 400

# key -> the N02 (operator, line) pairs it is drawn from, its real public name
# (English, then Japanese), and its colour. N02 files a public line under its
# legal name: 東海道線 is both the JR Kyoto Line (east of Osaka) and the JR Kobe
# Line (west of it), split in BRANCHES; 片町線 is the JR Gakkentoshi Line, 関西線
# the JR Yamatoji Line and 桜島線 the JR Yumesaki Line (JR West's names). The
# Chūō Line arrives in two railway classes (大阪港-コスモスクエア is class 12)
# and the New Tram in two (16 and 24), each under one line name.
#
# COLOURS: the project's own, not the operators' (2026-09-27). Each line took
# the colour nearest its operator's hue (lightness weighted half) among those
# that (a) read at 3:1 against BOTH map pages, #0B1220 and #ffffff; (b) clear
# CIE76 Delta-E 45 against every category pin; (c) clear 18 against every other
# line - a search over the sRGB cube, not an eyeballed palette (Kobe's rules,
# the japan-city skill's trap 10). 34 lines between three pins leave little
# room: without the hue pull the best pairwise floor for 34 colours is ~19.7,
# so several lines left their operator's hue (the Chūō Line olive, JR Kyoto
# slate). No exception below 45 against the pins; closest line pairs 18.0.
_JR, _M = "西日本旅客鉄道", "大阪市高速電気軌道"
LINES = {
    # Osaka Metro (大阪市高速電気軌道)
    "M": {"n02": [(_M, "1号線(御堂筋線)")], "name": "Midōsuji Line", "name_ja": "御堂筋線", "colour": "#E4151E"},
    "T": {"n02": [(_M, "2号線(谷町線)")], "name": "Tanimachi Line", "name_ja": "谷町線", "colour": "#933CA5"},
    "Y": {"n02": [(_M, "3号線(四つ橋線)")], "name": "Yotsubashi Line", "name_ja": "四つ橋線", "colour": "#00A2C3"},
    "C": {"n02": [(_M, "4号線(中央線)")], "name": "Chūō Line", "name_ja": "中央線", "colour": "#5D662A"},
    "S": {"n02": [(_M, "5号線(千日前線)")], "name": "Sennichimae Line", "name_ja": "千日前線", "colour": "#DB69CF"},
    "K": {"n02": [(_M, "6号線(堺筋線)")], "name": "Sakaisuji Line", "name_ja": "堺筋線", "colour": "#90542D"},
    "N": {"n02": [(_M, "7号線(長堀鶴見緑地線)")], "name": "Nagahori Tsurumi-ryokuchi Line",
          "name_ja": "長堀鶴見緑地線", "colour": "#7E9F1E"},
    "I": {"n02": [(_M, "8号線(今里筋線)")], "name": "Imazatosuji Line", "name_ja": "今里筋線", "colour": "#E77512"},
    "P": {"n02": [(_M, "南港ポートタウン線")], "name": "New Tram", "name_ja": "ニュートラム", "colour": "#00758A"},
    # JR West (西日本旅客鉄道)
    "JO": {"n02": [(_JR, "大阪環状線")], "name": "Osaka Loop Line", "name_ja": "大阪環状線", "colour": "#FF3C03"},
    "JY": {"n02": [(_JR, "東海道線")], "name": "JR Kyoto Line", "name_ja": "JR京都線", "colour": "#4E6375"},
    "JK": {"n02": [(_JR, "東海道線")], "name": "JR Kobe Line", "name_ja": "JR神戸線", "colour": "#755A75"},
    "JH": {"n02": [(_JR, "JR東西線")], "name": "JR Tōzai Line", "name_ja": "JR東西線", "colour": "#FF21C0"},
    "JG": {"n02": [(_JR, "片町線")], "name": "JR Gakkentoshi Line", "name_ja": "学研都市線", "colour": "#C303A8"},
    "OH": {"n02": [(_JR, "おおさか東線")], "name": "Osaka Higashi Line", "name_ja": "おおさか東線",
           "colour": "#A28DA8"},
    "JP": {"n02": [(_JR, "桜島線")], "name": "JR Yumesaki Line", "name_ja": "JRゆめ咲線", "colour": "#7293A5"},
    "JQ": {"n02": [(_JR, "関西線")], "name": "JR Yamatoji Line", "name_ja": "大和路線", "colour": "#12A500"},
    "JR": {"n02": [(_JR, "阪和線")], "name": "JR Hanwa Line", "name_ja": "阪和線", "colour": "#CF8400"},
    # Hankyu (阪急電鉄)
    "HK": {"n02": [("阪急電鉄", "神戸線")], "name": "Hankyu Kobe Line", "name_ja": "阪急神戸線", "colour": "#C9785D"},
    "HT": {"n02": [("阪急電鉄", "宝塚線")], "name": "Hankyu Takarazuka Line", "name_ja": "阪急宝塚線",
           "colour": "#B7572D"},
    "HY": {"n02": [("阪急電鉄", "京都線")], "name": "Hankyu Kyoto Line", "name_ja": "阪急京都線", "colour": "#87544B"},
    "HS": {"n02": [("阪急電鉄", "千里線")], "name": "Hankyu Senri Line", "name_ja": "阪急千里線", "colour": "#BA7E7B"},
    # Hanshin (阪神電気鉄道)
    "SH": {"n02": [("阪神電気鉄道", "本線")], "name": "Hanshin Main Line", "name_ja": "阪神本線", "colour": "#817B7B"},
    "SN": {"n02": [("阪神電気鉄道", "阪神なんば線")], "name": "Hanshin Namba Line", "name_ja": "阪神なんば線",
           "colour": "#4E665A"},
    # Keihan (京阪電気鉄道)
    "KM": {"n02": [("京阪電気鉄道", "京阪本線")], "name": "Keihan Main Line", "name_ja": "京阪本線", "colour": "#7B7B5A"},
    "KN": {"n02": [("京阪電気鉄道", "中之島線")], "name": "Keihan Nakanoshima Line", "name_ja": "京阪中之島線",
           "colour": "#969051"},
    # Kintetsu (近畿日本鉄道)
    "KT": {"n02": [("近畿日本鉄道", "難波線")], "name": "Kintetsu Namba Line", "name_ja": "近鉄難波線",
           "colour": "#FC5D3F"},
    "KO": {"n02": [("近畿日本鉄道", "大阪線")], "name": "Kintetsu Osaka Line", "name_ja": "近鉄大阪線",
           "colour": "#B43009"},
    "KA": {"n02": [("近畿日本鉄道", "南大阪線")], "name": "Kintetsu Minami-Osaka Line", "name_ja": "近鉄南大阪線",
           "colour": "#CC8142"},
    # Nankai (南海電気鉄道)
    "NM": {"n02": [("南海電気鉄道", "南海本線")], "name": "Nankai Main Line", "name_ja": "南海本線", "colour": "#9F6900"},
    "NK": {"n02": [("南海電気鉄道", "高野線")], "name": "Nankai Kōya Line", "name_ja": "南海高野線", "colour": "#B18D06"},
    "NS": {"n02": [("南海電気鉄道", "高野線")], "name": "Nankai Shiomibashi Line", "name_ja": "南海汐見橋線",
           "colour": "#7B5D18"},
    # Hankai Tramway (阪堺電気軌道)
    "RH": {"n02": [("阪堺電気軌道", "阪堺線")], "name": "Hankai Line", "name_ja": "阪堺線", "colour": "#516C00"},
    "RU": {"n02": [("阪堺電気軌道", "上町線")], "name": "Uemachi Line", "name_ja": "上町線", "colour": "#8A8A24"},
}
# The operator as a station suffix, used only where two stations share an
# English name (Kobe's Mikage (Hankyu) / Mikage (Hanshin)).
for _k, _short in {"M": "Metro", "T": "Metro", "Y": "Metro", "C": "Metro", "S": "Metro", "K": "Metro",
                   "N": "Metro", "I": "Metro", "P": "New Tram", "JO": "JR", "JY": "JR", "JK": "JR", "JH": "JR",
                   "JG": "JR", "OH": "JR", "JP": "JR", "JQ": "JR", "JR": "JR", "HK": "Hankyu", "HT": "Hankyu",
                   "HY": "Hankyu", "HS": "Hankyu", "SH": "Hanshin", "SN": "Hanshin", "KM": "Keihan",
                   "KN": "Keihan", "KT": "Kintetsu", "KO": "Kintetsu", "KA": "Kintetsu", "NM": "Nankai",
                   "NK": "Nankai", "NS": "Nankai", "RH": "Hankai", "RU": "Hankai"}.items():
    LINES[_k]["short"] = _short
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}

# Branches inside one N02 line (japan_step1 walks the section graph from
# `terminus` and stops within `junction_m` of `junction`; `length_m` stops a
# runaway walk). ORDER MATTERS: a walk never enters track an earlier one took.
# Coordinates are N02's own platform centroids (2026-09-27), used only to pick
# between same-named platforms.
#   * UF: the Umeda freight line's Umekita (大阪) - 福島 track carries only the
#     Haruka and Kuroshio limited expresses and has no station of its own: LEFT
#     OUT (owner 2026-09-27). Its 福島 row is the Loop Line's station.
#   * UK: its 新大阪 - Umekita (大阪) track carries the Osaka Higashi Line's
#     local trains (since 2023): drawn AS the Osaka Higashi Line (owner
#     2026-09-27).
#   * JK: the JR Kobe Line is 東海道線 west of 大阪.
#   * NS: the Shiomibashi Line is 高野線's 汐見橋 - 岸里玉出 section, signed
#     汐見橋線 by Nankai; the Kōya Line's own trains run from Namba on the Main
#     Line's track, so 高野線 south of 岸里玉出 is the Kōya Line.
_UMEKITA = (34.70274, 135.49316)
BRANCHES = {
    "UF": {"line": (_JR, "東海道線"), "terminus": "福島", "junction": "大阪", "junction_at": _UMEKITA,
           "stations": ("福島",), "length_m": (600, 1200), "draw_as": None,
           "label": "Umekita-Fukushima track (limited expresses only)"},
    "UK": {"line": (_JR, "東海道線"), "terminus": "大阪", "terminus_at": _UMEKITA, "junction": "新大阪",
           "junction_at": (34.73403, 135.50151), "junction_m": 400, "stations": (), "shared": ("大阪", "新大阪"),
           "length_m": (3000, 4500), "draw_as": "OH", "label": "Umekita track (Osaka Higashi Line)"},
    "JK": {"line": (_JR, "東海道線"), "terminus": "塚本", "junction": "大阪", "junction_at": (34.70250, 135.49498),
           "junction_m": 350, "stations": ("塚本",), "length_m": (8000, 13000)},
    "NS": {"line": ("南海電気鉄道", "高野線"), "terminus": "汐見橋", "junction": "岸里玉出",
           "stations": ("汐見橋", "芦原町", "木津川", "津守", "西天下茶屋"), "length_m": (4000, 5500)},
}

# Gate 3: the operators' own station counts for the in-city part of each Osaka
# Metro line, from Osaka Metro's station numbering (Midōsuji M12 Higashi-Mikuni
# to M27 Abiko; Tanimachi T13 Taishibashi-Imaichi to T35 Nagahara; Yotsubashi
# Y11-Y21; Chūō C09 Yumeshima to C21 Fukaebashi (C09 opened 2025-01-19 and is
# in N02-25, not N02-24: Osaka moved editions 2026-10-03); Sennichimae S11-S24; Sakaisuji
# K11-K20; Nagahori Tsurumi-ryokuchi N11 Taishō to N26 Yokozutsumi; Imazatosuji
# I11 Itakano to I21 Imazato; New Tram P09-P18) and JR West's Loop Line
# numbering (O01-O19). 太子橋今市 (T13 / I14) straddles the city line and counts
# on both lines, since its Tanimachi platform is inside (owner 2026-09-27). The
# lines the city line cuts elsewhere have no published in-city count; step 1
# lists them.
GATE3 = {"source": "operators' station numbering (Osaka Metro M/T/Y/C/S/K/N/I/P; JR West O01-O19)",
         "lines": {"M": 16, "T": 23, "Y": 11, "C": 13, "S": 14, "K": 10, "N": 16, "I": 11, "P": 10, "JO": 19}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"
# This taxonomy also classifies by source: keep those raw column(s) through step 2
# (they are passed to classify() by filter_to_storefront() and the map).

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
OSAKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = OSAKA_BBOX
