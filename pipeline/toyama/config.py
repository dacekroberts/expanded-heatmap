"""Toyama-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/toyama.md
(12/12 checks, 2026-10-02). Built in the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py), in Matsuyama's shape.

Business leg: the city's own CC BY 4.0 lists on its CKAN (opdt.city.toyama.lg.jp):
every food permit as of 2026-06-30 (one workbook, 6月末) and full registers of
barbers, beauty salons and laundries (2026-03). MHLW's 食品衛生申請等システム open
data is NOT a source (owner, 2026-10-02: the brief's recommendation for a city
with a complete own list, so its notifications are left out); it is a point
DONOR only (config.POINT_DONORS), its own point for a city row the block join
misses. Everything else placed by a JOIN to MLIT's 位置参照情報 for the one
municipality (no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Chitetsu's city tram and Portram, its four railway lines, the Ainokaze
Toyama Railway and JR West's Takayama Line. English station names from
OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "toyama" / "raw"
DATA_PROCESSED = ROOT / "data" / "toyama" / "processed"
OUTPUTS = ROOT / "outputs" / "toyama"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Toyama"
SLUG = "toyama"
MUNICIPALITY = "富山市"
PREFECTURE = "富山県"

# The city's CKAN (富山市オープンデータ), each dataset license_id cc-by under the
# portal's terms (第１条１: CC BY 4.0 International). One dataset per list.
_CKAN = "https://opdt.city.toyama.lg.jp/dataset"
FOOD_PAGE = f"{_CKAN}/seikatsu-eisei01"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    # 食品営業許可施設(令和8年6月）: every food permit, one sheet 6月末
    "food": ("syokuhin.xlsx",
             f"{_CKAN}/fb1198c6-3ac2-42fc-ae99-81ea5ba09a2d/resource/fa38003f-accd-4690-b71b-96b1d78e1c45"
             "/download/syokuhin.xlsx", FOOD_PAGE),
    "barber": ("riyosyo202603.xlsx",
               f"{_CKAN}/afafefa1-ec7c-4c1e-97c9-ab91ccf9b55f/resource/e6b559f9-d951-4e09-a6b6-15292cb9a96c"
               "/download/riyosyo202603.xlsx", f"{_CKAN}/seikatsu-eisei02"),
    "beauty": ("biyosyo202603.xlsx",
               f"{_CKAN}/9d0ead57-7589-40bf-be73-0d550360e389/resource/8848e4a0-e719-4708-b33d-908a856714f3"
               "/download/biyosyo202603.xlsx", f"{_CKAN}/seikatsu-eisei03"),
    "laundry": ("cleaning202603.xlsx",
                f"{_CKAN}/8a268965-69f8-4a49-a8eb-bd00696950a1/resource/b2ab3395-a04d-43f1-be83-0ef860776524"
                "/download/cleaning202603.xlsx", f"{_CKAN}/seikatsu-eisei06"),
    # MHLW's file: a point donor only, never a source of rows (POINT_DONORS)
    "mhlw_points": ("16201_food_business_all.csv",
                    "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=16201_food_business_all.csv",
                    MHLW_TOP),
}
# The food list's own date (Kyoto's rule: the date the list states, never the
# download's): the resource 「食品営業許可施設(令和8年6月）」, sheet 6月末, newest
# 許可年月日 2026-06-30; every 許可満了日 is 2026-07-22 or later, so every row is
# in term on that date (japan_register.in_term would drop none). The registers
# state only their file names' month, 202603 (uploaded 2026-05-18); one beauty
# row carries an opening date of 2026-04-10. MHLW's monthly file states none.
SOURCE_AS_OF = {"food": "2026-06-30", "barber": "2026-03-31", "beauty": "2026-03-31", "laundry": "2026-03-31",
                "mhlw_points": None}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items() if k != "mhlw_points"}
# Declared, never inferred: the city's lists are XLSX, one sheet each, header
# on row 1, read with merged_header (japan_register.xlsx_rows): the food
# workbook writes 施設住所 over four columns (municipality, town, number,
# building) and 営業者住所 over five, and the laundry register has an unheaded
# building column after 施設住所. MHLW's is UTF-8 with a BOM.
SOURCE_ENCODING = {"food": "xlsx", "barber": "xlsx", "beauty": "xlsx", "laundry": "xlsx",
                   "mhlw_points": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 営業者名 is REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; it is read IN MEMORY by that rule only, never kept. The city names
# an operator only where it is a company (the brief: 2,855 of 2,913 filled food
# cells carry a company marker), so the rule compares few rows (owner,
# 2026-10-02: accepted, as MHLW's rows in Fukuoka). Never selected: 営業者住所
# (an operator's own address), and MHLW's 法人名 / 法人番号 / 法人住所 / phones.
_REGISTER = ("施設名", "所在地", "営業者名")
REQUIRED_COLUMNS = {
    "food": ("施設名", "施設住所", "営業の種類", "営業者名", "許可満了日"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": ("業種", "施設名", "施設住所", "営業者名"),
    "mhlw_points": ("営業施設名称、屋号又は商号", "営業施設所在地", "緯度", "経度", "申請区分", "廃業年月日"),
}
# A city food row the block join misses takes MHLW's point for the same
# premises (ward, town, trade name): the brief measured 614 of 738 non-block
# food rows with one, and the chōme tier a median 360 m from MHLW's point
# (78 over 1 km) against 34 m at the block. MHLW's file is read for its
# points only, under its own key. The registers have no donor.
POINT_DONORS = {"food": "mhlw_points"}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    The city's workbooks through merged_header (above); "mhlw_points" is MHLW's
    whole file, read by POINT_DONORS for its coordinates only."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    if key == "mhlw_points":
        yield from jr.city_rows(path)
        return
    yield from jr.city_rows(path, merged_header=True)


# fetch_sources.py counts and header-checks each file through the same reader
# (japan_fetch); the counts equal the default reading's (measured 2026-10-03).
file_rows = source_rows


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 16201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and the tram stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 36.3697, W 137.0282, N 36.7667,
# E 137.7055, the mountains to 有峰 included), rounded out; step 1 stops if the
# city leaves it.
OSM_BBOX = (36.35, 137.01, 36.78, 137.72)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
# Tram stops whose OSM object has no name:en (2026-10-02: 22 of the 39), named
# as Chitetsu's own English line map signs them
# (chitetsu.co.jp/english/img/trams/trams-linemap.gif, read 2026-10-02), in
# Hiroshima's style: no macrons, 前 as -mae, the map's small-type brackets (a
# sponsor's or a neighbourhood's name) left off.
OSM_NAME_EN_MISSING = {
    "粟島（大阪屋ショップ前）": "Awajima",                          # Awajima (Osaka-ya supermarket mae)
    "オークスカナルパークホテル富山前": "Oarks Canal Park Hotel Toyama-mae",
    "龍谷富山高校前（永楽町）": "Ryukokutoyamakoko-mae",              # Ryukokutoyamakoko-mae (Eirakucho)
    "新富町": "Shintomicho",
    "地鉄ビル前": "Chitetsu-Biru-mae",
    "電気ビル前": "Denki-Biru-mae",
    "トヨタモビリティ富山Gスクエア五福前（五福末広町）": "Toyota Mobility Toyama G Square Gofuku-mae",
    "県庁前": "Kencho-mae",
    "桜橋": "Sakurabashi",
    "丸の内": "Marunouchi",
    "諏訪川原": "Suwanokawara",
    "荒町": "Aramachi",
    "中町（西町北）": "Nakamachi",                                # Nakamachi (Nishicho-kita)
    "大手モール": "Ote Mall",
    "西町": "Nishicho",
    "グランドプラザ前": "Grand Plaza-mae",
    "上本町": "Kamihonmachi",
    "広貫堂前": "Kokando-mae",
    "西中野": "Nishinakano",
    "小泉町": "Koizumicho",
    "堀川小泉": "Horikawa-koizumi",                              # Horikawa koizumi
    "大町": "Omachi",                                           # Oomachi
    "南富山駅前": "Minami-Toyama-ekimae",                        # Minamitoyamaeki-mae; OSM's 南富山 is Minami-Toyama
}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), to the same style: OSM's macrons, a run-together -mae, a spaced
# name and a sponsor's bracket, each as the operator's line map writes it.
OSM_NAME_EN_OVERRIDES = {
    "婦中鵜坂": "Fuchu-Usaka",                        # Fuchū-Usaka
    "萩浦小学校前": "Hagiura-shogakko-mae",           # Hagiurashōgakkō-mae
    "蓮町（馬場記念公園前）": "Hasumachi",             # Hasumachi (Babakinenkōen-mae)
    "インテック本社前": "Intec-Honsha-mae",            # Intec-Honshamae
    "国際会議場前": "Kokusai-Kaigijo-mae",             # Kokusai Kaigijo mae
    "競輪場前": "Keirinjo-mae",                       # Keirinjomae
    "奥田中学校前": "Okuda-chugakko-mae",              # Okuda-Chugakko-Mae
    "電鉄富山駅・エスタ前": "Dentetsu-Toyama-eki Esta-mae",  # Dentetsu-Toyama-eki esta-mae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~137.21) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# HALVED, on the spacing rule (docs/ring_rules.md: the halved edges where the
# median station gap is about 550 m or less): step 1 measured 443 m among the
# 74 in-city stations, 39 of them tram stops (2026-10-02), as Matsuyama's
# 374 m and Hiroshima's 357 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# Gate 1's floor: Hiroshima's, Matsuyama's, Paris's and Riga's 200 m, not a
# new number - a tram network is genuinely closer than 400 m (collapsed median
# 443 m; platforms 349 m).
SPACING_MIN_M = 200.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 15 legal sections, no Shinkansen; 富山 on the 北陸新幹線 is
# dropped and stays an Ainokaze and JR station): the city tram's six sections
# and Portram's two (all wholly inside), Chitetsu's Fujikoshi Line (5 of 5),
# Kamidaki Line (10 of 11), Main Line (6 of 41) and Tateyama Line (2 of 14:
# 本宮 and 有峰口, a mountain stretch far from the urban area, drawn as cut by
# the standing call), the Ainokaze Toyama Railway (5 of 23) and JR West's
# Takayama Line (10 of 10), each cut at the city line (owner 2026-09-24).
# LEFT OUT: JR Central's 高山線, whose one station inside is 猪谷, the JR West /
# JR Central boundary, already a station of JR West's line; Fukuoka's
# Hakata-Minami precedent (a line whose only in-city station another drawn
# line serves). The Tateyama funicular (立山黒部貫光 鋼索線) has no station inside.
LEFT_OUT_LINES = {("東海旅客鉄道", "高山線")}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the city tram under six LEGAL
# sections (本線, 支線, 安野屋線, 呉羽線, 富山都心線, 富山駅南北接続線), all wholly
# inside the city, that no rider reads; the operator runs its routes (南富山駅前
# to 富山駅 and to 富山大学前, and the 環状線 loop) over them, overlapping on
# 本線 and 支線. Drawn as ONE line under the tram's public name, Matsuyama's
# precedent (2026-10-02). Portram is a public name of its own, 富山港線 in two
# railway classes (12, the converted JR line; 21, street track), and is drawn
# as its own line; both take the 富山駅南北接続線 section, where the two meet
# at the 富山駅 stop and the through trains run.
_CT, _AI, _JW = "富山地方鉄道", "あいの風とやま鉄道", "西日本旅客鉄道"
LINES = {
    "TR": {"n02": [(_CT, "支線"), (_CT, "安野屋線"), (_CT, "呉羽線"), (_CT, "富山都心線"), (_CT, "富山駅南北接続線")],
           "name": "Chitetsu City Tram", "name_ja": "富山地方鉄道市内電車", "short": "Chitetsu", "hue": "#E60012"},
    "PT": {"n02": [(_CT, "富山港線"), (_CT, "富山駅南北接続線")], "name": "Chitetsu Toyamako Line (Portram)",
           "name_ja": "富山港線（ポートラム）", "short": "Chitetsu", "hue": "#C8102E"},
    "CM": {"n02": [(_CT, "本線")], "name": "Chitetsu Main Line", "name_ja": "本線", "short": "Chitetsu",
           "hue": "#E60012"},
    "FJ": {"n02": [(_CT, "不二越線")], "name": "Chitetsu Fujikoshi Line", "name_ja": "不二越線",
           "short": "Chitetsu", "hue": "#E60012"},
    "KD": {"n02": [(_CT, "上滝線")], "name": "Chitetsu Kamidaki Line", "name_ja": "上滝線", "short": "Chitetsu",
           "hue": "#E60012"},
    "TY": {"n02": [(_CT, "立山線")], "name": "Chitetsu Tateyama Line", "name_ja": "立山線", "short": "Chitetsu",
           "hue": "#E60012"},
    "AI": {"n02": [(_AI, "あいの風とやま鉄道線")], "name": "Ainokaze Toyama Railway Line",
           "name_ja": "あいの風とやま鉄道線", "short": "Ainokaze", "hue": "#00A0C8"},
    "JT": {"n02": [(_JW, "高山線")], "name": "JR Takayama Line", "name_ja": "高山線", "short": "JR",
           "hue": "#0072BC"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# toyama` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Chitetsu's six share one red and
# spread over red, orange and brown. Closest pair within 500 m 18.2 (Main
# Line / city tram, at 電鉄富山); anywhere 10.2 (Main Line / Kamidaki Line,
# which never come within 500 m); the dark-mode labels separate, 8 of 8.
_COLOURS = {"TR": "#E80010", "PT": "#F86040", "CM": "#F85008", "FJ": "#C02800", "KD": "#F86028",
            "TY": "#B03800", "AI": "#08A0C0", "JT": "#406878"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
# The tram's 本線 (class 21, 3,609 m, 14 stops 南富山駅前 to 電鉄富山駅・エスタ前)
# and Chitetsu's railway 本線 (class 12, 53,132 m from 電鉄富山 east) share one
# N02 (operator, line) pair and no track: two separate components of the
# section graph (2026-10-02). The tram's is split off by walking from 南富山駅前
# and drawn as the city tram. The junction is a railway station 20 km away
# (越中三郷), so the walk takes the whole tram component; the length window
# stops it if the two ever connect.
_TRAM_MAIN = ("南富山駅前", "大町", "堀川小泉", "小泉町", "西中野", "広貫堂前", "上本町", "西町", "中町（西町北）",
              "荒町", "桜橋", "電気ビル前", "地鉄ビル前", "電鉄富山駅・エスタ前")
BRANCHES = {
    "TM": {"line": (_CT, "本線"), "terminus": "南富山駅前", "junction": "越中三郷", "stations": _TRAM_MAIN,
           "shared": (), "length_m": (3000, 4200), "draw_as": "TR", "label": "the city tram's 本線 (street track)"},
}
# Gate 3: the operator's own stop numbering, C01 to C39 across its ten
# timetables (chitetsu.co.jp/?p=70984) and its English line map (both read
# 2026-10-02): the city tram C01 to C25, and Portram C26 to C39 plus 富山駅
# (C15), the stop the two share, against the collapsed set. The railway lines
# the city line cuts have no in-city count; the Fujikoshi Line's five are N02's.
GATE3 = {"source": "Chitetsu's tram stop numbering C01-C39 (timetables at chitetsu.co.jp/?p=70984)",
         "lines": {"TR": 25, "PT": 15}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TOYAMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TOYAMA_BBOX
