"""Suita-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/suita.md.
Japan A/B batch (Kansai-1, 2026-10-07), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: the city's own 衛生管理課 open data (CC BY 4.0), five XLSX.
Food: 食品営業許可施設一覧 as of 2026-03-31 in two files, one per law (the
revised law since 2021-06-01, the old law to 2021-05-31), read together as
one food list (Matsuyama's two keys of one kind); a snapshot of the permits in
term on that date, disclosed as an upper bound for any later date (Kyoto's
disclosure). Personal services: one 確認施設一覧 per trade (barbers, beauty
salons, laundries) as of 2026-08-31 (Hamamatsu's one kind per file). Food
shops also from MHLW's notifications (partial, opt-in; call 127b), MHLW's own
point where the block join misses (127c), its permits out (126). All placed
by a JOIN to MLIT's 位置参照情報 for the one municipality (27205, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Hankyu's Senri and Kyoto lines, JR West's Kyoto Line (東海道線) and
Osaka Higashi Line, the Osaka Monorail's main line and Saito Line, and
Kita-Osaka Kyuko, cut at the city line; the Midosuji Line left out (call
165). English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "suita" / "raw"
DATA_PROCESSED = ROOT / "data" / "suita" / "processed"
OUTPUTS = ROOT / "outputs" / "suita"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Suita"
SLUG = "suita"
MUNICIPALITY = "吹田市"
PREFECTURE = "大阪府"

# The 衛生管理課 open-data page (更新日 2026-09-07): each group of files carries
# 「クリエイティブ・コモンズ 表示 4.0 国際 ライセンス」 under 吹田市オープンデータ利用規約
# (CC BY 4.0). MHLW 食品衛生申請等システム open data, PDL 1.0 (the system's site
# terms; read 2026-09-24 for Fukuoka). Credit links the MHLW top page only.
CITY_PAGE = "https://www.city.suita.osaka.jp/shisei/1018811/1017120/1017164/1017170.html"
_FILES = "https://www.city.suita.osaka.jp/_res/projects/default_project/_page_/001/017/170/"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# Each URL pinned to the edition the build read. File names carry the date
# (YYYYMMDDnew/old.xlsx; the registers YYYYMMDDnn.xlsx), so a new edition is a
# new URL: the brief's http_contains check on the page fails on it, and a
# --force re-download of a pinned name fails loudly rather than reading a
# newer edition under this edition's dates. Re-measure then (SOURCE_AS_OF,
# TERM_AS_OF, the upper bound).
SOURCE_FILES = {
    # 食品営業許可施設一覧（改正後の食品衛生法の許可（令和3年6月1日以降の許可））
    "food_new": ("20260331new.xlsx", _FILES + "20260331new.xlsx", CITY_PAGE),
    # 食品営業許可施設一覧（改正前の食品衛生法の許可（令和3年5月31日までの許可））
    "food_old": ("20260331old.xlsx", _FILES + "20260331old.xlsx", CITY_PAGE),
    # 理容所確認施設一覧, 美容所確認施設一覧, クリーニング所確認施設一覧
    "barber": ("2026090301.xlsx", _FILES + "2026090301.xlsx", CITY_PAGE),
    "beauty": ("2026090302.xlsx", _FILES + "2026090302.xlsx", CITY_PAGE),
    "laundry": ("2026090303.xlsx", _FILES + "2026090303.xlsx", CITY_PAGE),
    "mhlw": ("27205_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27205_food_business_all.csv",
             MHLW_TOP),
}
# The dates the page states (Kyoto's rule: the list's own date, never the
# download's): the food lists 令和8年3月31日時点, the registers 令和8年8月31日時点
# (Fukuoka's several-dates precedent). MHLW's monthly file states none.
FOOD_AS_OF = "2026-03-31"
REGISTERS_AS_OF = "2026-08-31"
SOURCE_AS_OF = {"food_new": FOOD_AS_OF, "food_old": FOOD_AS_OF, "barber": REGISTERS_AS_OF,
                "beauty": REGISTERS_AS_OF, "laundry": REGISTERS_AS_OF, "mhlw": None}
# The permit term rules (calls 161 and 172) read the food rows' 許可満了日
# against the lists' own date, never today: the lists hold the permits in term
# on 2026-03-31, so this keeps the snapshot whole (the 77 old-law permits
# ending that day included). Read against the registers' 2026-08-31 instead it
# would drop the 241 permits that ended by then while missing their renewals
# and every opening since April, which only a later edition shows; the page
# discloses the snapshot as an upper bound instead (Kyoto's disclosure).
TERM_AS_OF = {"food_new": FOOD_AS_OF, "food_old": FOOD_AS_OF}
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The two food lists are one kind (japan_step2.kind): the key names the file
# (Matsuyama's food_old / food_new).
SOURCE_KIND = {"food_old": "food", "food_new": "food"}
# Declared, never inferred: the city's files are XLSX; MHLW's is UTF-8 with a
# BOM.
SOURCE_ENCODING = {**{k: "xlsx" for k in SOURCE_FILES}, "mhlw": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 申請者氏名 (food), 申請者_氏名 and 代表者名 (registers)
# and MHLW's 法人名 are REQUIRED so the name rule
# (japan_register.name_is_operator) cannot silently compare nothing; they are
# read IN MEMORY by that rule only, never kept. Never selected: the registers'
# 施設_TEL and 申請者住所 (the operator's own address), and MHLW's 法人番号 /
# 法人住所 / phones. The food lists' unnamed column (66 and 9 rows, no
# building words) is not read.
_FOOD = ("申請者氏名", "屋号", "施設住所", "業種", "種目", "許可満了日")
_REGISTER = ("施設_名称", "施設所在地", "申請者_氏名", "代表者名")
REQUIRED_COLUMNS = {
    "food_new": _FOOD,
    "food_old": _FOOD,
    "barber": _REGISTER,
    "beauty": _REGISTER,
    # 種別 is the laundry's kind (取次のみ, ドライ, ランドリー, リネンサプライ):
    # japan_eigyo's linen rule takes linen supply out (Osaka's 2026-09-27
    # precedent).
    "laundry": (*_REGISTER, "種別"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point (the
# brief: a median 40 m from the block point, 94.2% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# A premises in both, in one bucket (a konbini holding a city restaurant
# permit and filing an MHLW notification): MHLW's row stays, as in Matsuyama.
SUPERSEDES = {"mhlw": ("food_old", "food_new")}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    each city file as it stands, and MHLW's file as its notifications only
    (申請区分 届出 / 届出(廃業)), since the city's two food lists hold every
    permit (3,330 restaurants on 2026-03-31, 101.1% of e-Stat's count in
    force); MHLW's 88 open permits are out (call 126)."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27205.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Suita.
# S, W, N, E: the city's N03 extent (S 34.745, W 135.487, N 34.831, E 135.555)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.74, 135.48, 34.84, 135.56)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word. The two 吹田 (JR 006779, Hankyu
# 006798, separate stations) take their operators from LINES' "short" where
# name:en does not tell them apart (Kobe's Mikage, trap 1).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.52) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule
# (docs/ring_rules.md): the median nearest-group gap among the 15 in-city
# groups is 961 m (427 m 岸辺 / 正雀 to 1,731 m 北千里; scratch measurement,
# 2026-10-07, as the brief's), well above the halving threshold of about 550 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25, the
# brief and a re-run 2026-10-07: 8 lines, no Shinkansen): Hankyu's 千里線 (7 of
# 11) and 京都線 (1 of 27, 正雀, its N02 point 14 m inside the line), JR's
# 東海道線 (2 of 59) and おおさか東線 (1 of 14, 南吹田), the Osaka Monorail's
# main line (2 of 14) and Saito Line (2 of 5), Kita-Osaka Kyuko's 南北線 (2 of
# 6), cut at the city line (owner 2026-09-24); the Hankyu Kyoto and Osaka
# Higashi one-station stubs are JR or private lines, drawn as cut under the
# standing call (Kobe's JR Takarazuka Line).
# The Midosuji Line keeps one station in the city, 江坂, whose N02 group
# (006800) also holds Kita-Osaka Kyuko's platform, 0 m apart: an URBAN line cut
# to one station whose station another line keeps is left out, and 江坂 keeps
# its ring through Kita-Osaka Kyuko (owner 2026-10-06, call 165, the
# one-station rule of calls 54 and 92 applied as written). A left-out line's
# stations are not written to excluded_stations.csv; the page discloses it.
LEFT_OUT_LINES = {
    ("大阪市高速電気軌道", "1号線(御堂筋線)"): "an urban line cut to one station, 江坂, kept through Kita-Osaka "
                                         "Kyuko (owner 2026-10-06, call 165)",
}
# Every station within the drawing distance of the city lies in Osaka
# Prefecture, so no neighbouring prefecture's N03 is needed to name the
# stations beyond the line.
N03_NEIGHBOR_PREFS = ()
# 千里中央 (in Toyonaka, beyond the line): N02 files Kita-Osaka Kyuko's and the
# Monorail's platforms as two groups 257 m apart; one interchange by name and
# by passage, joined as Toyonaka's config joins it, so the excluded list
# names it once.
GROUP_JOIN = {("大阪モノレール", "大阪モノレール線", "千里中央"): "one Senri-Chuo, 257 m (the Monorail platform)"}
# Kobe's 300 m: the widest in-city group is 山田 (Hankyu and the Monorail,
# 197 m).
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. 東海道線 here is the JR Kyoto Line (east of
# 大阪; Osaka's config). The lines Osaka's map also draws start from Osaka's
# colours; the Monorail's main line and Kita-Osaka Kyuko from Toyonaka's
# searched colours (its config, 2026-10-07), the Saito Line from the
# Monorail's own hue, where the search must move it off the main line's.
_HK, _JR, _MO, _KK = "阪急電鉄", "西日本旅客鉄道", "大阪モノレール", "北大阪急行電鉄"
LINES = {
    "HS": {"n02": [(_HK, "千里線")], "name": "Hankyu Senri Line", "name_ja": "阪急千里線", "short": "Hankyu",
           "hue": "#BA7E7B"},
    "HY": {"n02": [(_HK, "京都線")], "name": "Hankyu Kyoto Line", "name_ja": "阪急京都線", "short": "Hankyu",
           "hue": "#87544B"},
    "JY": {"n02": [(_JR, "東海道線")], "name": "JR Kyoto Line", "name_ja": "JR京都線", "short": "JR",
           "hue": "#4E6375"},
    "OH": {"n02": [(_JR, "おおさか東線")], "name": "Osaka Higashi Line", "name_ja": "おおさか東線", "short": "JR",
           "hue": "#A28DA8"},
    "MO": {"n02": [(_MO, "大阪モノレール線")], "name": "Osaka Monorail Main Line", "name_ja": "大阪モノレール本線",
           "short": "Monorail", "hue": "#007890"},
    "MS": {"n02": [(_MO, "国際文化公園都市モノレール線(彩都線)")], "name": "Osaka Monorail Saito Line",
           "name_ja": "大阪モノレール彩都線", "short": "Monorail", "hue": "#0067B0"},
    "KK": {"n02": [(_KK, "南北線")], "name": "Kita-Osaka Kyuko Namboku Line", "name_ja": "北大阪急行南北線",
           "short": "Kita-Kyu", "hue": "#E81820"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py suita`
# once step 1 has written lines.geojson (it reads the drawn track); until then
# each line is drawn in its starting hue.
_COLOURS = {}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}

# Branches inside one N02 line (japan_step1 walks the section graph from
# `terminus` and stops within `junction_m` of `junction`; `length_m` stops a
# runaway walk). Suita's own stretch of 東海道線 (吹田, 岸辺) is all the JR Kyoto
# Line, but the drawn track runs 3 km past the city line, to 新大阪 and the
# N02 sections beyond it: the main line to 大阪 (the JR Kyoto Line's own) and
# the Umekita track 新大阪 - Umekita (大阪), which carries the Osaka Higashi
# Line's trains and which Osaka's map draws AS the Osaka Higashi Line (owner
# 2026-09-27). Osaka's entry, unchanged, so the two maps agree; its
# coordinates are N02's own platform centroids (Osaka's config).
BRANCHES = {
    "UK": {"line": (_JR, "東海道線"), "terminus": "大阪", "terminus_at": (34.70274, 135.49316), "junction": "新大阪",
           "junction_at": (34.73403, 135.50151), "junction_m": 400, "stations": (), "shared": ("大阪", "新大阪"),
           "length_m": (3000, 4500), "draw_as": "OH", "label": "Umekita track (Osaka Higashi Line)"},
}

# Gate 3: no line lies wholly inside the city. The one in-city run an operator
# numbers is the Hankyu Senri Line's HK-89 吹田 to HK-95 北千里 (7 stations; HK-88
# 下新庄 is in Osaka), the station codes in Hankyu's own timetable pages the
# brief read (hankyu.co.jp/station/html/HK-89 to HK-95, 2026-10-06).
GATE3 = {"source": "Hankyu's station numbering (HK-89 Suita to HK-95 Kita-Senri)", "lines": {"HS": 7}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SUITA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SUITA_BBOX
