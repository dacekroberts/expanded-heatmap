"""Tokyo-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

The brief is docs/build_briefs/tokyo.md (7/7 checks, 2026-09-28). Japan's
sixth city and the last, on the shared modules Kobe built:
pipeline/countries/japan.py (rail, city line), japan_register.py (the address
join), japan_step1.py, japan_step2.py and japan_fetch.py. This file holds only
what is Tokyo's; WHICH wards and files is pipeline/tokyo/wards.py, the roster,
and this file builds every per-source setting from it.

Business leg: Tokyo is 23 publishers, not one (the tokyo-ward skill). Each
active ward's own food list is a source of its own, with the WARD as its
municipality (SOURCE_MUNICIPALITY): Chūō, Minato, Shinjuku, Taitō, Kōtō,
Meguro, Setagaya and Shibuya. MHLW's open-data slice is added to Chūō, Kōtō,
Minato and Shinjuku, one pin where a premises is in both (SUPERSEDES, the
ward's row kept). Personal services: the barber, beauty and laundry registers
of Minato, Taitō, Meguro and Shibuya (owner 2026-09-28: only where food is
on). All placed by a JOIN to MLIT's 位置参照情報 for the eight wards. Each
ward's share of the official restaurant count is measured every build
(OFFICIAL_SHARES) and written for the page.

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen left out, stations kept only
inside the city line - all 23 wards, the 15 without data drawn hollow
(NO_DATA_WARDS). English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline.tokyo import wards

# wards.check() runs in the steps and the fetch, NEVER here: the deployed app
# imports this module (its page reads HEATMAP_HTML) and has no data/, where the
# check would refuse every missing file.

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "tokyo" / "raw"
DATA_PROCESSED = ROOT / "data" / "tokyo" / "processed"
OUTPUTS = ROOT / "outputs" / "tokyo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; fetch_sources.py records them) ---------------

NAME = "Tokyo"
SLUG = "tokyo"
# The 23 special wards together (東京都区部); every source names its own ward
MUNICIPALITY = "東京都区部"
PREFECTURE = "東京都"


def _build_sources():
    """source key -> (kind, ward code, [files]) from the roster: a ward's food
    list, each register, and MHLW's slice where the owner added it."""
    out = {}
    for code, w in wards.ACTIVE.items():
        out[f"food_{code}"] = ("food", code, list(w["food"]))
        for kind, files in w.get("personal", {}).items():
            out[f"{kind}_{code}"] = (kind, code, list(files))
        if code in wards.MHLW_WARDS:
            out[f"mhlw_{code}"] = ("mhlw", code, [str(w["mhlw"])])
    return out


_SRC = _build_sources()
# japan_step2 iterates these keys; the value is the first file (source_rows
# reads them all)
SOURCES = {k: Path(v[2][0]).name for k, v in _SRC.items()}
# What each source IS to japan_eigyo: food, mhlw, barber, beauty, laundry
SOURCE_KIND = {k: v[0] for k, v in _SRC.items()}
# The WARD is the municipality each source's addresses are read against
SOURCE_MUNICIPALITY = {k: wards.WARDS[v[1]]["ja"] for k, v in _SRC.items()}
MUNICIPALITY_CODES = {w["ja"]: c for c, w in wards.ACTIVE.items()}
# Stations of the wards without data: drawn hollow, not counted (owner 2026-09-28)
NO_DATA_WARDS = wards.NO_DATA_WARDS


def source_rows(key):
    """A source's rows: all its files in turn (Meguro's food list is two, the
    revised-law and old-law lists, which share no permit; the brief)."""
    from pipeline.countries import japan_register as jr
    from pipeline.countries.japan_step2 import need
    return [r for f in _SRC[key][2] for r in jr.city_rows(need(DATA_RAW / f, SLUG))]


# The fetch works per FILE: key -> (file under data/tokyo/raw/, or MHLW's
# absolute path; URL; dataset page). A one-file source keeps its source key;
# Meguro's two food files are food_13110_1 and food_13110_2.
SOURCE_FILES = {}
_FILE_SOURCE = {}
for _k, (_kind, _code, _files) in _SRC.items():
    for _i, _f in enumerate(_files):
        _fk = _k if len(_files) == 1 else f"{_k}_{_i + 1}"
        SOURCE_FILES[_fk] = (_f, *wards.URLS[_f])
        _FILE_SOURCE[_fk] = _k


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


# Declared, never inferred (docs/data_sources.md), read 2026-09-28 from each
# file's bytes (BOM, then a strict decode); japan_register.city_rows sniffs
# them all. The food lists' are the roster's; MHLW's are UTF-8 with a BOM, the
# registers UTF-8 without one.
SOURCE_ENCODING = {k: (wards.WARDS[v[1]]["encoding"] if v[0] == "food" else "utf-8-sig" if v[0] == "mhlw"
                       else "utf-8") for k, v in _SRC.items()}

# As of: the newest date each list holds, or the date it states where it
# states one, read 2026-09-28 (never a portal's label: Shinjuku's server
# re-stamped its 2023 file 2026-08-31). None = the source states no date: the
# page says "Fetched <date> (no source date)" (owner's wording rule).
_FOOD_AS_OF = {
    "13102": "2022-12-28",  # permits 2021-06-01 to 2022-12-28 only
    "13103": "2026-07-31",  # 許可年月日 to 2026-07-31
    "13104": "2023-01-01",  # the ward's stated snapshot; permits to 2022-12-28
    "13106": "2026-03-31",  # 許可開始日 to 2026-03-31, the ward's stated date
    "13108": "2022-11-30",  # permits 2021-06-01 to 2022-11-30 only
    "13110": "2026-04-01",  # the ward's stated date; permits to 2026-03-31
    "13112": "2026-03-31",  # the file's own date (R080331); 188 permits start 2026-04-01 to 05-01
    "13113": "2026-09-02",  # the newest 廃業日; permits to 2026-08-31 (the item says 2026-09-09)
}
SOURCE_AS_OF = {}
for _fk, _k in _FILE_SOURCE.items():
    _kind, _code = _SRC[_k][0], _SRC[_k][1]
    if _kind == "food":
        SOURCE_AS_OF[_fk] = _FOOD_AS_OF[_code]
    elif _code == "13110":
        SOURCE_AS_OF[_fk] = "2026-03-31"  # Meguro's registers, dated in their file names
    else:
        SOURCE_AS_OF[_fk] = None  # MHLW's slices and the catalogue registers state none
FOOD_AS_OF = None  # per ward, above

# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns are REQUIRED where a list has one,
# so the name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing: read IN MEMORY by that rule only, and never kept.
# Never selected: the phones, 郵便番号, 法人住所, Taitō's food list's 営業者住所
# and the catalogue registers' 営業者_所在地_* (an operator's own address).
# The national-schema food lists (Chūō, Minato, Shinjuku, Kōtō, Shibuya) and
# MHLW's carry 法人名 only: the name rule cannot run on their rows, as on
# MHLW's in Fukuoka (DECISIONS 2026-09-28).
_NATIONAL_FOOD = ("施設名称", "営業の種類", "業態", "所在地_連結表記", "廃業年月日", "申請区分")
_CATALOGUE_REGISTER = ("名称", "所在地_連結表記", "営業者氏名", "法人代表者氏名")
_MEGURO_REGISTER = ("施設名称", "施設所在地", "施設（種別）等", "営業者名")
_COLUMNS = {
    "food_13102": _NATIONAL_FOOD,
    "food_13103": _NATIONAL_FOOD,
    "food_13104": _NATIONAL_FOOD,
    "food_13108": _NATIONAL_FOOD,
    "food_13106": ("屋号", "業種", "営業所所在地", "営業者名"),
    "food_13110": ("施設の名称", "業種", "施設所在地", "営業者氏名"),
    "food_13112": ("施設屋号", "業種", "施設所在地", "営業者名"),
    "food_13113": ("施設名称", "営業の種類もしくは営業の形態", "業態", "施設所在地_連結表記", "廃業日", "申請区分"),
    "barber_13103": ("施設名称", "施設所在地"),
    "beauty_13103": ("施設名称", "施設所在地"),
    "laundry_13103": ("施設名称", "施設所在地", "施設種別"),
    "barber_13106": _CATALOGUE_REGISTER,
    "beauty_13106": _CATALOGUE_REGISTER,
    "laundry_13106": (*_CATALOGUE_REGISTER, "営業形態"),
    "barber_13110": _MEGURO_REGISTER,
    "beauty_13110": _MEGURO_REGISTER,
    "laundry_13110": _MEGURO_REGISTER,
    "barber_13113": _CATALOGUE_REGISTER,
    "beauty_13113": _CATALOGUE_REGISTER,
    "laundry_13113": (*_CATALOGUE_REGISTER, "営業形態"),
}
for _code in wards.MHLW_WARDS:
    _COLUMNS[f"mhlw_{_code}"] = ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度",
                                 "申請区分", "廃業年月日")
# by source key (step 2) and by file key (the fetch)
REQUIRED_COLUMNS = {**_COLUMNS, **{fk: _COLUMNS[k] for fk, k in _FILE_SOURCE.items()}}

_MHLW = tuple(f"mhlw_{c}" for c in wards.MHLW_WARDS)
# MHLW publishes each field only where the filer agreed to it: a row with no
# address was withheld, not mobile (Fukuoka's mechanism).
ADDRESS_BY_CONSENT = set(_MHLW)
# Where the block join misses an MHLW row, MHLW's own point places it (Fukuoka's)
OWN_POINT_FALLBACK = set(_MHLW)
# One premises in the ward's list and MHLW's: the WARD's row is kept (the
# tokyo-ward skill; owner 2026-09-24: MHLW's slice is added, de-duplicated)
SUPERSEDES = {f"food_{c}": (f"mhlw_{c}",) for c in wards.MHLW_WARDS}
# Each ward's share is of its OWN list; MHLW's +0.1 to +3.1 pt is said once in
# prose (owner 2026-09-28)
SHARE_SKIP = _MHLW
OFFICIAL_SHARES = True

# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per active
# ward, side by side (load_city_isj keys each block by its ward).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and tram stops (the
# Arakawa Line, the Tokyu Setagaya Line). Which stations exist is N02's.
# S, W, N, E: the 23 wards' N03 extent (35.528-35.818 N, 139.563-139.919 E,
# measured 2026-09-28; Haneda and the reclaimed islands included) rounded out;
# step 1 stops if the city leaves it.
OSM_BBOX = (35.50, 139.54, 35.84, 139.94)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-09-28): OSM writes ケ where N02 writes ヶ, and gives
# three stations their subtitle in 〈〉.
OSM_NAME_ALIASES = {
    "千駄ヶ谷": "千駄ケ谷", "阿佐ヶ谷": "阿佐ケ谷", "南阿佐ヶ谷": "南阿佐ケ谷", "市ヶ谷": "市ケ谷", "西ヶ原": "西ケ原",
    "霞ヶ関": "霞ケ関",
    "二重橋前": "二重橋前〈丸の内〉", "押上": "押上〈スカイツリー前〉", "明治神宮前": "明治神宮前〈原宿〉",
}
# THE STYLE (owner 2026-09-28): the operators' own English signs, as OSM
# carries them - no macrons, Tokyo Metro's lowercase after a hyphen
# (Naka-meguro) beside JR's title case (Nishi-Nippori). Where OSM's objects for
# one station disagree, JR's title case and no macron.
OSM_NAME_EN_TIES = {
    "王子": "Oji",                         # Ōji / Oji
    "八丁堀": "Hatchobori",                # Hatchōbori / Hatchobori
    "人形町": "Ningyocho",                 # Ningyōchō / Ningyocho
    "新御徒町": "Shin-Okachimachi",        # Shin-okachimachi / Shin-Okachimachi
    "東中野": "Higashi-Nakano",            # Higashi-nakano / Higashi-Nakano
}
OSM_NAME_EN_MISSING = {}
# Tokyo's 十条 is a name (Jujo), not a street grid: no JO_IS_GRID.
# Cited overrides of OSM's name:en ({ja: en}; the comment is the OSM spelling
# replaced, osm_station_names.json of 2026-09-28). The other names are OSM's.
OSM_NAME_EN_OVERRIDES = {
    # a split vote OSM's majority settles in Tokyo Metro's lowercase; JR's case
    "西日暮里": "Nishi-Nippori",           # Nishi-nippori 2, Nishi-Nippori 1
    "新木場": "Shin-Kiba",                 # Shin-kiba 2, Shin-Kiba 1
    # the stray macrons (9 of 492 names), to the signs' spelling
    "高円寺": "Koenji",                    # Kōenji
    "新大久保": "Shin-Okubo",              # Shin-Ōkubo
    "大森海岸": "Omorikaigan",             # Ōmorikaigan
    "越中島": "Etchujima",                 # Etchūjima
    "馬喰町": "Bakurocho",                 # Bakurochō
    "石神井公園": "Shakujii-koen",         # Shakujii-kōen Station
    # defects
    "とうきょうスカイツリー": "Tokyo Skytree",   # TOKYO SKYTREE
    "下神明": "Shimo-shimmei",             # Shimo-simmei
    "二重橋前": "Nijubashimae",            # Nijubashimae 'Marunouchi'
    "押上": "Oshiage",                     # Oshiage 'SKYTREE'
    "明治神宮前": "Meiji-jingumae",        # Meiji-jingumae 'Harajuku'
    "羽田空港第1・第2ターミナル": "Haneda Airport Terminal 1·2",  # Haneda Airport Terminal 1・2
    # numerals before 丁目 as figures (owner 2026-09-28, every Japanese city)
    "六本木一丁目": "Roppongi-1-Chome",    # Roppongi-itchome
    "銀座一丁目": "Ginza-1-Chome",         # Ginza-itchome
    "青山一丁目": "Aoyama-1-Chome",        # Aoyama-itchome
    "滝野川一丁目": "Takinogawa-1-Chome",  # Takinogawa-itchome
    "町屋二丁目": "Machiya-2-Chome",       # Machiya-nichome
    "荒川二丁目": "Arakawa-2-Chome",       # Arakawa-nichome
    "四谷三丁目": "Yotsuya-3-Chome",       # Yotsuya-sanchome
    "新宿三丁目": "Shinjuku-3-Chome",      # Shinjuku-sanchome
    "本郷三丁目": "Hongo-3-Chome",         # Hongo-sanchome
    "志村三丁目": "Shimura-3-Chome",       # Shimura-sanchome
    "東尾久三丁目": "Higashi-ogu-3-Chome",  # Higashi-ogu-sanchome
    "東池袋四丁目": "Higashi-ikebukuro-4-Chome",  # Higashi-ikebukuro-yonchome
    "西ヶ原四丁目": "Nishigahara-4-Chome",  # Nishigahara-yonchome
    "西新宿五丁目": "Nishi-shinjuku-5-Chome",  # Nishi-shinjuku-gochome
    "荒川七丁目": "Arakawa-7-Chome",       # Arakawa-nanachome
}
# A platform N02 gave its own group although it is part of the station of the
# same name (japan_step1.join_groups). 両国 (JR / Toei, 386 m), 早稲田 (Metro /
# Sakura Tram, 743 m) and the TX's 浅草 (593 m) are different stations and stay
# apart, taking their operators.
GROUP_JOIN = {
    ("東日本旅客鉄道", "京葉線", "東京"): "the Keiyo Line's platforms, 424 m away, are part of Tokyo Station",
    ("東京地下鉄", "13号線副都心線", "池袋"): "356 m away; one Ikebukuro station to Tokyo Metro (F09, M25, Y09)",
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# UTM zone 54N: the longitude (~139.7) falls in the 138 to 144 band. Derived
# per city, not copied (the brief's check).
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the 23 wards (stub_test, 2026-09-28: 54
# N02 lines, 16 operators). The city line is all 23 wards; the 15 without data
# are drawn hollow. Lines running on beyond the wards are cut there (owner
# 2026-09-24): the JR lines, the private railways, Tōzai 17 of 23, Hokusō 2 of
# 15 (a one-station-scale stub of a suburban line stays as cut).
LEFT_OUT_LINES = {
    # As Fukuoka's Hakata-Minami line (owner 2026-09-28): one station inside,
    # served there by other lines, and no track of its own in the wards
    ("京成電鉄", "成田空港線"): "Narita Sky Access: only Keisei-Takasago is inside, served by three Keisei lines "
                         "and the Hokusō, whose track it runs on",
    ("埼玉高速鉄道", "埼玉高速鉄道線"): "Saitama Railway: only Akabane-Iwabuchi is inside, the Namboku Line's terminus",
}
# Tokyo's interchanges are wider than Kobe's 300 m: step 1's first run found
# six real ones over it (2026-09-28), each one named interchange under one N02
# group code - 新宿 546 m (Marunouchi to Keiō), 大手町 450, 池袋 392, 飯田橋 379,
# 浅草 366 (Toei to Tōbu), 日比谷 321. The check still stops anything wider.
COLLAPSE_MAX_SPREAD_M = 550

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), and its colour (set by the spatial colour search, after step 1).
#
# JR EAST (owner 2026-09-28): N02 files JR East under its LEGAL lines (山手線,
# 東北線, 東海道線, 中央線, 総武線, 常磐線, 京葉線, 赤羽線), and riders know the
# SERVICES. The nine services are drawn in full, each a `route` over the legal
# lines it runs on (japan_step1.route_sections), overlapping where they share
# track. Stops as JR East's route maps give them; the first and last entry of a
# service running on past the wards is its next station outside, or "~name"
# where it passes one without stopping. The Tōkaidō Line (東京, 新橋, 品川) and
# the Shōnan-Shinjuku Line are not drawn on their own: every station they serve
# in the wards is on a line below, on track they share (the page says so).
_JR, _M, _T = "東日本旅客鉄道", "東京地下鉄", "東京都"
_TOHOKU, _TOKAIDO, _CHUO, _SOBU = (_JR, "東北線"), (_JR, "東海道線"), (_JR, "中央線"), (_JR, "総武線")
LINES = {
    # --- JR East: the nine services
    "JY": {"route": [(_JR, "山手線", ["品川", "大崎", "五反田", "目黒", "恵比寿", "渋谷", "原宿", "代々木", "新宿",
                                   "新大久保", "高田馬場", "目白", "池袋", "大塚", "巣鴨", "駒込", "田端"]),
                     (*_TOHOKU, ["田端", "西日暮里", "日暮里", "鶯谷", "上野", "御徒町", "秋葉原", "神田", "東京"]),
                     (*_TOKAIDO, ["東京", "有楽町", "新橋", "浜松町", "田町", "高輪ゲートウェイ", "品川"])],
           "name": "JR Yamanote Line", "name_ja": "山手線", "short": "JR"},
    "JK": {"route": [(*_TOHOKU, ["川口", "赤羽", "東十条", "王子", "上中里", "田端", "西日暮里", "日暮里", "鶯谷", "上野",
                                 "御徒町", "秋葉原", "神田", "東京"]),
                     (*_TOKAIDO, ["東京", "有楽町", "新橋", "浜松町", "田町", "高輪ゲートウェイ", "品川", "大井町", "大森",
                                  "蒲田", "川崎"])],
           "name": "JR Keihin-Tohoku Line", "name_ja": "京浜東北線", "short": "JR"},
    "JC": {"route": [(*_TOHOKU, ["東京", "神田"]),
                     (*_CHUO, ["神田", "御茶ノ水", "四ツ谷", "新宿", "中野", "高円寺", "阿佐ヶ谷", "荻窪", "西荻窪",
                               "吉祥寺"])],
           "name": "JR Chuo Line (Rapid)", "name_ja": "中央線快速", "short": "JR"},
    "JB": {"route": [(*_CHUO, ["吉祥寺", "西荻窪", "荻窪", "阿佐ヶ谷", "高円寺", "中野", "東中野", "大久保", "新宿",
                               "代々木", "千駄ヶ谷", "信濃町", "四ツ谷", "市ヶ谷", "飯田橋", "水道橋", "御茶ノ水"]),
                     (*_SOBU, ["御茶ノ水", "秋葉原", "浅草橋", "両国", "錦糸町", "亀戸", "平井", "新小岩", "小岩", "市川"])],
           "name": "JR Chuo-Sobu Line", "name_ja": "中央・総武線各駅停車", "short": "JR"},
    "JO": {"route": [(*_TOKAIDO, ["武蔵小杉", "西大井", "品川", "新橋", "東京"]),
                     (*_SOBU, ["東京", "新日本橋", "馬喰町", "錦糸町", "新小岩", "市川"])],
           "name": "JR Yokosuka / Sobu Rapid Line", "name_ja": "横須賀・総武快速線", "short": "JR"},
    "JE": {"route": [(_JR, "京葉線", ["東京", "八丁堀", "越中島", "潮見", "新木場", "葛西臨海公園", "舞浜"])],
           "name": "JR Keiyo Line", "name_ja": "京葉線", "short": "JR"},
    "JJ": {"route": [(*_TOHOKU, ["上野", "日暮里"]),
                     (_JR, "常磐線", ["日暮里", "三河島", "南千住", "北千住", "綾瀬", "亀有", "金町", "松戸"])],
           "name": "JR Joban Line", "name_ja": "常磐線", "short": "JR"},
    "JA": {"route": [(_JR, "山手線", ["大崎", "恵比寿", "渋谷", "新宿", "池袋"]),
                     (_JR, "赤羽線", ["池袋", "板橋", "十条", "赤羽"]),
                     (*_TOHOKU, ["赤羽", "北赤羽", "浮間舟渡", "戸田公園"])],
           "name": "JR Saikyo Line", "name_ja": "埼京線", "short": "JR"},
    "JU": {"route": [(*_TOHOKU, ["東京", "上野", "尾久", "赤羽", "~川口"])],
           "name": "JR Utsunomiya / Takasaki Line", "name_ja": "宇都宮線・高崎線", "short": "JR"},
    # --- Tokyo Metro (東京地下鉄)
    "G": {"n02": [(_M, "3号線銀座線")], "name": "Ginza Line", "name_ja": "銀座線", "short": "Metro"},
    "M": {"n02": [(_M, "4号線丸ノ内線"), (_M, "4号線丸ノ内線分岐線")], "name": "Marunouchi Line",
          "name_ja": "丸ノ内線", "short": "Metro"},
    "H": {"n02": [(_M, "2号線日比谷線")], "name": "Hibiya Line", "name_ja": "日比谷線", "short": "Metro"},
    "T": {"n02": [(_M, "5号線東西線")], "name": "Tozai Line", "name_ja": "東西線", "short": "Metro"},
    "C": {"n02": [(_M, "9号線千代田線")], "name": "Chiyoda Line", "name_ja": "千代田線", "short": "Metro"},
    "Y": {"n02": [(_M, "8号線有楽町線")], "name": "Yurakucho Line", "name_ja": "有楽町線", "short": "Metro"},
    "Z": {"n02": [(_M, "11号線半蔵門線")], "name": "Hanzomon Line", "name_ja": "半蔵門線", "short": "Metro"},
    "N": {"n02": [(_M, "7号線南北線")], "name": "Namboku Line", "name_ja": "南北線", "short": "Metro"},
    # N02 files 和光市-小竹向原 (F01-F06) under the Yūrakuchō Line only; the
    # Fukutoshin's trains stop there too (Tokyo Metro's numbering)
    "F": {"n02": [(_M, "13号線副都心線")],
          "route": [(_M, "8号線有楽町線", ["和光市", "地下鉄成増", "地下鉄赤塚", "平和台", "氷川台", "小竹向原"])],
          "name": "Fukutoshin Line", "name_ja": "副都心線", "short": "Metro"},
    # --- Toei (東京都交通局)
    "A": {"n02": [(_T, "1号線浅草線")], "name": "Toei Asakusa Line", "name_ja": "都営浅草線", "short": "Toei"},
    "I": {"n02": [(_T, "6号線三田線")], "name": "Toei Mita Line", "name_ja": "都営三田線", "short": "Toei"},
    "S": {"n02": [(_T, "10号線新宿線")], "name": "Toei Shinjuku Line", "name_ja": "都営新宿線", "short": "Toei"},
    "E": {"n02": [(_T, "12号線大江戸線")], "name": "Toei Oedo Line", "name_ja": "都営大江戸線", "short": "Toei"},
    "SA": {"n02": [(_T, "荒川線")], "name": "Tokyo Sakura Tram", "name_ja": "東京さくらトラム（都電荒川線）",
           "short": "Toei"},
    "NT": {"n02": [(_T, "日暮里・舎人ライナー")], "name": "Nippori-Toneri Liner", "name_ja": "日暮里・舎人ライナー",
           "short": "Toei"},
    # --- Tokyu (東急電鉄)
    "TY": {"n02": [("東急電鉄", "東横線")], "name": "Tokyu Toyoko Line", "name_ja": "東横線", "short": "Tokyu"},
    "MG": {"n02": [("東急電鉄", "目黒線")], "name": "Tokyu Meguro Line", "name_ja": "目黒線", "short": "Tokyu"},
    "DT": {"n02": [("東急電鉄", "田園都市線")], "name": "Tokyu Den-en-toshi Line", "name_ja": "田園都市線",
           "short": "Tokyu"},
    "OM": {"n02": [("東急電鉄", "大井町線")], "name": "Tokyu Oimachi Line", "name_ja": "大井町線", "short": "Tokyu"},
    "IK": {"n02": [("東急電鉄", "池上線")], "name": "Tokyu Ikegami Line", "name_ja": "池上線", "short": "Tokyu"},
    "TM": {"n02": [("東急電鉄", "東急多摩川線")], "name": "Tokyu Tamagawa Line", "name_ja": "東急多摩川線",
           "short": "Tokyu"},
    "SG": {"n02": [("東急電鉄", "世田谷線")], "name": "Tokyu Setagaya Line", "name_ja": "世田谷線", "short": "Tokyu"},
    # --- Keiō (京王電鉄): 京王線 includes the Keiō New Line's 初台 and 幡ヶ谷
    "KO": {"n02": [("京王電鉄", "京王線")], "name": "Keio Line", "name_ja": "京王線", "short": "Keio"},
    "IN": {"n02": [("京王電鉄", "井の頭線")], "name": "Keio Inokashira Line", "name_ja": "井の頭線", "short": "Keio"},
    # --- Odakyū (小田急電鉄)
    "OH": {"n02": [("小田急電鉄", "小田原線")], "name": "Odakyu Odawara Line", "name_ja": "小田原線",
           "short": "Odakyu"},
    # --- Seibu (西武鉄道)
    "SI": {"n02": [("西武鉄道", "池袋線")], "name": "Seibu Ikebukuro Line", "name_ja": "池袋線", "short": "Seibu"},
    "SS": {"n02": [("西武鉄道", "新宿線")], "name": "Seibu Shinjuku Line", "name_ja": "新宿線", "short": "Seibu"},
    "ST": {"n02": [("西武鉄道", "豊島線")], "name": "Seibu Toshima Line", "name_ja": "豊島線", "short": "Seibu"},
    "SY": {"n02": [("西武鉄道", "西武有楽町線")], "name": "Seibu Yurakucho Line", "name_ja": "西武有楽町線",
           "short": "Seibu"},
    # --- Tōbu (東武鉄道): 伊勢崎線 is signed the Tōbu Skytree Line inside Tokyo
    "TS": {"n02": [("東武鉄道", "伊勢崎線")], "name": "Tobu Skytree Line", "name_ja": "東武スカイツリーライン",
           "short": "Tobu"},
    "TJ": {"n02": [("東武鉄道", "東上本線")], "name": "Tobu Tojo Line", "name_ja": "東上線", "short": "Tobu"},
    "TK": {"n02": [("東武鉄道", "亀戸線")], "name": "Tobu Kameido Line", "name_ja": "亀戸線", "short": "Tobu"},
    "TD": {"n02": [("東武鉄道", "大師線")], "name": "Tobu Daishi Line", "name_ja": "大師線", "short": "Tobu"},
    # --- Keisei (京成電鉄)
    "KS": {"n02": [("京成電鉄", "本線")], "name": "Keisei Main Line", "name_ja": "京成本線", "short": "Keisei"},
    "KSO": {"n02": [("京成電鉄", "押上線")], "name": "Keisei Oshiage Line", "name_ja": "京成押上線",
            "short": "Keisei"},
    "KSK": {"n02": [("京成電鉄", "金町線")], "name": "Keisei Kanamachi Line", "name_ja": "京成金町線",
            "short": "Keisei"},
    # --- Keikyū (京浜急行電鉄)
    "KK": {"n02": [("京浜急行電鉄", "本線")], "name": "Keikyu Main Line", "name_ja": "京急本線", "short": "Keikyu"},
    "KKA": {"n02": [("京浜急行電鉄", "空港線")], "name": "Keikyu Airport Line", "name_ja": "京急空港線",
            "short": "Keikyu"},
    # --- the rest, one line each
    "HS": {"n02": [("北総鉄道", "北総線")], "name": "Hokuso Line", "name_ja": "北総線", "short": "Hokuso"},
    "TX": {"n02": [("首都圏新都市鉄道", "常磐新線")], "name": "Tsukuba Express", "name_ja": "つくばエクスプレス",
           "short": "TX"},
    "R": {"n02": [("東京臨海高速鉄道", "臨海副都心線")], "name": "Rinkai Line", "name_ja": "りんかい線",
          "short": "TWR"},
    "U": {"n02": [("ゆりかもめ", "東京臨海新交通臨海線")], "name": "Yurikamome", "name_ja": "ゆりかもめ",
          "short": "Yurikamome"},
    "MO": {"n02": [("東京モノレール", "東京モノレール羽田線")], "name": "Tokyo Monorail", "name_ja": "東京モノレール",
           "short": "Monorail"},
}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Each operator's own line colour: the TARGET of the colour search
# (scripts/line_colour_search.py), never drawn as it is - the drawn colour is
# the nearest one that reads on both basemaps and clears the pins (Kobe's rule).
_HUES = {
    "JY": "#80C241", "JK": "#00B2E5", "JC": "#F15A22", "JB": "#FFD400", "JO": "#0067C0", "JE": "#C9242F",
    "JJ": "#00B261", "JA": "#00AC9A", "JU": "#F68B1E",
    "G": "#FF9500", "M": "#F62E36", "H": "#B5B5AC", "T": "#009BBF", "C": "#00BB85", "Y": "#C1A470",
    "Z": "#8F76D6", "N": "#00AC9B", "F": "#9C5E31",
    "A": "#EC6E65", "I": "#006AB8", "S": "#B0C124", "E": "#CE045B", "SA": "#E8779D", "NT": "#C0007A",
    "TY": "#DA0442", "MG": "#009CD2", "DT": "#20A288", "OM": "#F18C43", "IK": "#EE86A7", "TM": "#AE0378",
    "SG": "#FCC70D", "KO": "#DD0077", "IN": "#283C8C", "OH": "#2288CC",
    "SI": "#F08300", "SS": "#0077C0", "ST": "#F08300", "SY": "#F08300",
    "TS": "#0F6CC3", "TJ": "#004098", "TK": "#0F6CC3", "TD": "#0F6CC3",
    "KS": "#005AAA", "KSO": "#005AAA", "KSK": "#005AAA", "KK": "#E5171F", "KKA": "#E5171F",
    "HS": "#3A9AD9", "TX": "#E4002B", "R": "#00418E", "U": "#1A5CAC", "MO": "#0070C0",
}
for _k, _h in _HUES.items():
    LINES[_k]["hue"] = _h

# THE DRAWN COLOURS: `python scripts/line_colour_search.py tokyo` (2026-09-28,
# 3,817 feasible colours), the spatial form of Kobe's rule - 3:1 on both map
# pages, CIE76 >= 45 from every pin, >= 18 from every line within 500 m and >=
# 10 (HARD_FLOOR) from every other, each nearest its operator's hue in config
# order. Closest pair within 500 m 18.1 (Chuo Rapid, Tsukuba Express); anywhere
# 10.1 (Hibiya, Den-en-toshi, 1.1 km apart); all 52 dark-mode labels separate.
# As in Fukuoka, no blue clears Retail's pin, so the blue lines went slate,
# grey and mauve (Mita, Yokosuka / Sobu Rapid, the Keisei lines).
#
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search, and two
# lines sat under the owner's floor of 20 from it (2026-10-07). Each moved to
# the colour nearest its operator's hue that reads 3:1 on both pages, clears
# 20 from every pin and 18 from every other line, taking 25 where that cost
# little: the Toei Shinjuku Line #889800 (15.0) to #78A03C (olive 20.1,
# nearest line JR Yamanote 19.3; the yellow-greens leave no more room), the
# Chiyoda Line #586818 (15.8) to #007034, Tokyo Metro's green darkened (25.3
# from the green pin, 39.4 from olive). Nine of 52 lines sit between 20 and
# 45 from olive (the Shinjuku nearest, then JR Chuo-Sobu #B09000 23.2), an
# accepted trade (owner, 2026-10-07). Closest pair still 10.1; all 52
# dark-mode labels separate. DECISIONS, "Lines within 20 of the olive and
# violet pins recoloured".
_COLOURS = {
    "JY": "#60A000", "JK": "#08A0C0", "JC": "#F05820", "JB": "#B09000", "JO": "#9888A0", "JE": "#F86040",
    "JJ": "#20A800", "JA": "#207078", "JU": "#E07800", "G": "#B06800", "M": "#E81020", "H": "#909088",
    "T": "#6890A0", "C": "#007034", "Y": "#A89060", "Z": "#C870C8", "N": "#586858", "F": "#A06030",
    "A": "#E07850", "I": "#606070", "S": "#78A03C", "E": "#F000B8", "SA": "#B880A0", "NT": "#E038C0",
    "TY": "#E84028", "MG": "#8890A0", "DT": "#789090", "OM": "#D07020", "IK": "#B88088", "TM": "#B820A8",
    "SG": "#C08800", "KO": "#E060D0", "IN": "#9840A0", "OH": "#687888", "SI": "#E86800", "SS": "#906888",
    "ST": "#D08000", "SY": "#B05000", "TS": "#007890", "TJ": "#9040C0", "TK": "#C870E8", "TD": "#807080",
    "KS": "#785868", "KSO": "#8048D8", "KSK": "#406878", "KK": "#C80008", "KKA": "#F81808", "HS": "#787878",
    "TX": "#B83008", "R": "#B858C0", "U": "#B060E8", "MO": "#0050F0",
}
for _k, _c in _COLOURS.items():
    LINES[_k]["colour"] = _c

# THE ON-MAP LABEL is each line's CODE, the operators' own line letters as
# Tokyo's signs and maps show them; the legend reads code and full name, and
# the page names every line in full (owner 2026-09-28). Full names left 9 of 52
# labels unplaceable at 1000 px and short names 59 overlapping pairs at 343 px;
# the codes place all 52 at both. An operator may give several lines one code,
# as its station numbering does: Seibu SI (Ikebukuro, Toshima, Seibu
# Yurakucho), Tobu TS (Skytree, Kameido, Daishi), Keisei KS, Keikyu KK.
_CODES = {k: k for k in LINES}
_CODES.update({"KSO": "KS", "KSK": "KS", "KKA": "KK", "ST": "SI", "SY": "SI", "TK": "TS", "TD": "TS"})
for _k, _c in _CODES.items():
    LINES[_k]["code"] = _c

# Gate 3: the operators' own station counts inside the 23 wards, from their
# station numbering. Tokyo Metro: Ginza G01-G19; Marunouchi M01-M25 plus the
# Hōnanchō branch m03-m05; Hibiya H01-H22; Tōzai T01-T17 (T18 Urayasu on is in
# Chiba); Chiyoda C01-C20; Yūrakuchō Y02-Y24 and Fukutoshin F02-F16 (Y01 / F01
# Wakōshi is in Saitama); Hanzōmon Z01-Z14; Namboku N01-N19. Toei: Asakusa
# A01-A20; Mita I01-I27; Shinjuku S01-S20 (S21 Motoyawata is in Chiba); Ōedo
# E01-E38; the Sakura Tram SA01-SA30; Nippori-Toneri NT01-NT13. The JR
# services are their route lists above, so they have no independent count here.
GATE3 = {"source": "Tokyo Metro and Toei station numbering (G, M, H, T, C, Y, Z, N, F; A, I, S, E, SA, NT)",
         "lines": {"G": 19, "M": 28, "H": 22, "T": 17, "C": 20, "Y": 23, "Z": 14, "N": 19, "F": 15,
                   "A": 20, "I": 27, "S": 20, "E": 38, "SA": 30, "NT": 13}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the 23 wards' N03 extent, rounded out.
CITY_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
