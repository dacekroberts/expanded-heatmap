"""Kyoto-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

The brief is docs/build_briefs/kyoto.md (8/8 checks, 2026-09-28). Japan's
fifth city, on the shared modules Kobe built: pipeline/countries/japan.py
(rail, city line), japan_register.py (the address join and the register
rebuild), japan_step1.py, japan_step2.py and japan_fetch.py. This file holds
only what is Kyoto's.

Business leg: a REBUILT register. Kyoto has published no full food-permit
list since the 2021 reform, only each month's new permits, so
japan_register.kyoto_permit_stream() stitches the 2021-03-31 full list to
every monthly list since and keeps the permits still in their term on AS_OF.
Closures are invisible: the count is an UPPER BOUND, and the page says so.
Personal services are the city's complete barber, beauty and laundry lists
(2026-03-31) plus each month's new premises since. All from the City's own
portal (data.city.kyoto.lg.jp, no API: japan_fetch.portal_file), placed by a
JOIN to MLIT's 位置参照情報 for the 11 wards.

Rail: MLIT N02 (not GTFS, not OSM), the Shinkansen left out, stations kept only
inside the city line (N03). English station names from OpenStreetMap's name:en
(owner, 2026-09-27).
"""

import datetime
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kyoto" / "raw"
DATA_PROCESSED = ROOT / "data" / "kyoto" / "processed"
OUTPUTS = ROOT / "outputs" / "kyoto"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kyoto"
SLUG = "kyoto"
MUNICIPALITY = "京都市"
PREFECTURE = "京都府"

# The City's own portal, CC BY 4.0 on every dataset and resource page (京都市
# as 著作権者; read 2026-09-24). No API: each file through the resource page's
# own download button (GET, then POST with the session cookie; owner-approved as
# equivalent to a GET). Fetch from data.city.kyoto.lg.jp ONLY: older copies on
# www.city.kyoto.lg.jp fall under a copyright page that bars copying.
PORTAL = "https://data.city.kyoto.lg.jp"
# The resources this build read, pinned by id (never "the newest"):
#   00414 食品営業許可施設一覧について: the 2021-03-31 full list (15447, an old
#         .xls) and the monthly lists for 2021-04 and 2021-05;
#   00541 食品営業許可施設一覧について（令和3年6月以降）: every monthly list,
#         2021-06 to 2026-07 (62);
#   00530 理容所・美容所・クリーニング所の施設一覧について: the complete lists as
#         of 2026-03-31 and each month's new premises since (the 2025-03-31
#         lists on disk were read for churn at the screen and are not used).
_BARBER = (21186, 21216, 21259, 21320, 21413)
_BEAUTY = (21188, 21218, 21261, 21322, 21415)
_LAUNDRY = (21190, 21263, 21324, 21417)  # no laundry file for 2026-04
PORTAL_RESOURCES = {
    "00414": (15447, 15533, 15570),
    "00541": (15820, 16122, 16250, 16384, 16495, 16632, 16634, 16714, 16766, 17015, 17082, 17092, 17132, 17230,
              17325, 17384, 17625, 17651, 17723, 17738, 17773, 17835, 17859, 17896, 18100, 18208, 18286, 18337,
              18532, 18565, 18609, 18720, 18863, 20028, 20063, 20087, 20123, 20237, 20317, 20387, 20422, 20442,
              20488, 20523, 20550, 20573, 20623, 20642, 20691, 20807, 20878, 20935, 21002, 21023, 21079, 21103,
              21158, 21244, 21246, 21288, 21409, 21424),
    "00530": (*_BARBER, *_BEAUTY, *_LAUNDRY),
}
# The rebuild's date (owner 2026-09-28): the newest monthly list covers July
# 2026, so renewals are visible up to its last day and no later. Pinned, never
# today: a step that filtered on today would drift every day.
AS_OF = datetime.date(2026, 7, 31)
FOOD_AS_OF = AS_OF.isoformat()
REGISTERS_AS_OF = "2026-03-31"
# A permit whose term is under a year is a short-term one (an event or season;
# 48 restaurants at the screen) and is not a premises (brief).
MIN_TERM_DAYS = 365

# The key is the taxonomy's `source` column.
SOURCES = {"food": "the rebuilt register", "barber": _BARBER, "beauty": _BEAUTY, "laundry": _LAUNDRY}
# The columns each source must carry; step 2 stops on a source without them.
# The rebuilt register carries only premises columns and the name rule's yes or
# no (japan_register.kyoto_permit_stream compares 申請者＿申請者名 in memory,
# owner 2026-09-27). The registers' 申請者氏名 is read IN MEMORY by the same rule
# and never kept; 申請者＿役職名 and 申請者＿代表者 are never selected.
_REGISTER_COLUMNS = ("施設名称", "施設所在地", "申請者氏名")
REQUIRED_COLUMNS = {
    "food": ("営業所所在地", "屋号", "業種", "許可開始日", "許可終了日", "name_is_operator"),
    "barber": _REGISTER_COLUMNS,
    "beauty": _REGISTER_COLUMNS,
    "laundry": _REGISTER_COLUMNS,
}


def portal_files(rids, dataset="00530"):
    out = []
    for rid in rids:
        have = sorted((DATA_RAW / dataset).glob(f"{dataset}_{rid}_*"))
        if not have:
            raise SystemExit(f"missing resource {rid}\nRun: python pipeline/kyoto/fetch_sources.py")
        out.append(have[0])
    return out


def source_rows(key):
    """What japan_step2 reads for each source: the rebuilt register (short-term
    permits out, counted), or a register's complete list plus its months."""
    import sys

    from pipeline.baseline import emit
    from pipeline.countries import japan_register as jr
    if key == "food":
        portal_files(PORTAL_RESOURCES["00414"], "00414")
        portal_files(PORTAL_RESOURCES["00541"], "00541")
        rows = jr.kyoto_permit_stream(DATA_RAW, AS_OF)
        term = [(datetime.date.fromisoformat(r["許可終了日"]) - datetime.date.fromisoformat(r["許可開始日"])).days
                if r["許可開始日"] else MIN_TERM_DAYS for r in rows]
        short = sum(t < MIN_TERM_DAYS for t in term)
        print(f"  rebuilt register on {AS_OF}: {len(rows):,} permits in term; {short} short-term (under a year) "
              f"left out", file=sys.stdout)
        emit("rebuilt_in_term", len(rows))
        emit("short_term_permits", short)
        return [r for r, t in zip(rows, term) if t >= MIN_TERM_DAYS]
    return [r for f in portal_files(SOURCES[key]) for r in jr.workbook_tables(f)]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (34.875-35.321 N, 135.559-135.878 E,
# measured 2026-09-28) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.85, 135.53, 35.35, 135.90)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
# The Randen and the Keihan Keishin Line are tramways (N02 class 21), whose
# stops OSM may tag railway=tram_stop (Osaka's Hankai lesson).
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# Where OSM's objects for one station disagree on name:en, the spelling taken.
# 西院 is one interchange by N02's group code (Hankyu's and the Randen's, 214 m
# apart), and its operators READ it differently: Hankyu's Saiin, the Randen's
# Sai. Hankyu's sign and the usual reading win (2026-09-28).
OSM_NAME_EN_TIES = {"西院": "Saiin"}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment; owner 2026-09-28). Kyoto's 条 are street names (Shijō, Gojō, Kujō),
# so no JO_IS_GRID, and no station name has a 丁目. OSM's Kyoto objects mostly
# drop macrons (Nijo, Sanjo, Kujo) where their neighbours keep them (Gojō,
# Shijō, Shichijō) and mix -mae with -Mae. Each entry takes Sapporo's and
# Fukuoka's style, hyphenated title case with macrons; the comment is the OSM
# spelling it replaces (osm_station_names.json, 2026-09-28). "Kyoto" keeps its
# English exonym without a macron, inside compounds too (Kobe's precedent:
# Kobe-Sannomiya). Two long names are cut to their first part, the Japanese
# beside them giving the rest: 茶山・京都芸術大学 is OSM's own "Chayama", and
# 等持院・立命館大学衣笠キャンパス前 was half translated. 41 entries name 42
# stations (two 十条); the other 75 are OSM's.
OSM_NAME_EN_OVERRIDES = {
    "中書島": "Chūshojima",                     # Chushojima
    "伏見桃山": "Fushimi-Momoyama",              # Fushimi-momoyama
    "祇園四条": "Gion-Shijō",                    # Gion-shijo
    "八幡前": "Hachiman-Mae",                    # Hachiman-mae
    "保津峡": "Hozukyō",                         # Hozukyo
    "一乗寺": "Ichijōji",                        # Ichijoji
    "JR藤森": "JR-Fujinomori",                   # JR Fujinomori
    "神宮丸太町": "Jingū-Marutamachi",           # Jingu-marutamachi
    "十条": "Jūjō",                              # Jujo (Kintetsu's and the subway's: two stations)
    "観月橋": "Kangetsukyō",                     # Kangetsukyo
    "烏丸御池": "Karasuma-Oike",                 # Karasuma Oike
    "清水五条": "Kiyomizu-Gojō",                 # Kiyomizu-gojo
    "九条": "Kujō",                              # Kujo
    "車折神社": "Kurumazaki-Jinja",              # Kurumazaki-jinja
    "京都河原町": "Kyoto-Kawaramachi",           # Kyoto Kawaramachi
    "京都精華大前": "Kyoto-Seikadai-Mae",        # Kyoto Seikadai-mae
    "京都市役所前": "Kyoto-Shiyakusho-Mae",      # Kyoto Shiyakusho-mae
    "松尾大社": "Matsuo-Taisha",                 # Matsuo-taisha
    "桃山南口": "Momoyama-Minamiguchi",          # Momoyama-minamiguchi
    "桃山御陵前": "Momoyama-Goryōmae",           # Momoyamagoryōmae
    "妙心寺": "Myōshinji",                       # Myoshinji
    "二条": "Nijō",                              # Nijo
    "二条城前": "Nijōjō-Mae",                    # Nijojo-mae
    "西京極": "Nishikyōgoku",                    # Nishikyogoku
    "西大路三条": "Nishiōji-Sanjō",              # Nishioji-Sanjo
    "西大路御池": "Nishiōji-Oike",               # Nishioji-oike
    "大宮": "Ōmiya",                             # Omiya
    "六地蔵": "Rokujizō",                        # Rokujizo
    "鹿王院": "Rokuōin",                         # Rokuoin
    "龍谷大前深草": "Ryūkokudai-Mae-Fukakusa",   # Ryukokudai-mae-Fukakusa
    "三条": "Sanjō",                             # Sanjo
    "三条京阪": "Sanjō-Keihan",                  # Sanjo Keihan
    "撮影所前": "Satsueisho-Mae",                # Satsueisho-mae
    "四条大宮": "Shijō-Ōmiya",                   # Shijo-Omiya
    "修学院": "Shūgakuin",                       # Shugakuin
    "鳥羽街道": "Toba-Kaidō",                    # Tobakaido
    "東福寺": "Tōfukuji",                        # Tofukuji
    "東寺": "Tōji",                              # Toji
    "等持院・立命館大学衣笠キャンパス前": "Tōjiin",  # Tōjiin・Ritsumeikan University
    "梅小路京都西": "Umekōji-Kyotonishi",        # Umekoji-Kyotonishi
    "太秦広隆寺": "Uzumasa-Kōryūji",             # Uzumasa-Koryuji
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.76) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test, 2026-09-28: 19
# N02 lines). Wholly inside: the Karasuma Line, both Randen lines, both Eiden
# lines, Keihan's Ōtō Line and Hankyu's Arashiyama Line; the Tōzai Line keeps
# 16 of 17 (六地蔵 is in Uji). Cut at the city line (owner 2026-09-24): Keihan
# Main 15 of 41, Uji 4 of 8, Keishin 3 of 7 (half a line: passes, owner
# 2026-09-24), Kintetsu Kyoto 9 of 26, Hankyu Kyoto 7 of 27, JR Nara 5 of 19,
# San'in 9 of 161, Tōkaidō 4 of 59. JR's Kosei Line keeps one station (山科):
# a one-station stub stays as cut (Kobe's JR Takarazuka Line, owner 2026-09-27).
LEFT_OUT_LINES = {
    ("嵯峨野観光鉄道", "嵯峨野観光線"): "a scenic tourist line (owner 2026-09-24)",
    # The brief's 2026-09-24 call to draw them was reversed for consistency with
    # Kobe's Maya and Rokkō funiculars (owner 2026-09-28).
    ("京福電気鉄道", "鋼索線"): "sightseeing funicular, the Eizan Cable (owner 2026-09-28)",
    ("鞍馬寺", "鞍馬山鋼索鉄道"): "sightseeing funicular, the Kurama Cable (owner 2026-09-28)",
}
# Kobe's 300 m until step 1's report shows a wider real interchange.
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 (operator, line) pairs it is drawn from, its real public name
# (English, then Japanese), and its colour. JR West signs its lines by their
# public names (the Osaka precedent): 山陰線 is the Sagano Line, and 東海道線 is
# the Biwako Line east of Kyoto and the JR Kyoto Line west of it (BRANCHES).
_SUB, _JR ="京都市", "西日本旅客鉄道"
_KH, _HQ, _KT, _RD, _ED = "京阪電気鉄道", "阪急電鉄", "近畿日本鉄道", "京福電気鉄道", "叡山電鉄"
LINES = {
    # Kyoto Municipal Subway (京都市交通局)
    "K": {"n02": [(_SUB, "烏丸線")], "name": "Karasuma Line", "name_ja": "烏丸線", "short": "Subway"},
    "T": {"n02": [(_SUB, "東西線")], "name": "Tōzai Line", "name_ja": "東西線", "short": "Subway"},
    # JR West (西日本旅客鉄道)
    "JA": {"n02": [(_JR, "東海道線")], "name": "JR Kyoto Line", "name_ja": "JR京都線", "short": "JR"},
    "JB": {"n02": [(_JR, "東海道線")], "name": "JR Biwako Line", "name_ja": "琵琶湖線", "short": "JR"},
    "JE": {"n02": [(_JR, "山陰線")], "name": "JR Sagano Line", "name_ja": "嵯峨野線", "short": "JR"},
    "JD": {"n02": [(_JR, "奈良線")], "name": "JR Nara Line", "name_ja": "奈良線", "short": "JR"},
    "JC": {"n02": [(_JR, "湖西線")], "name": "JR Kosei Line", "name_ja": "湖西線", "short": "JR"},
    # Keihan (京阪電気鉄道)
    "KM": {"n02": [(_KH, "京阪本線")], "name": "Keihan Main Line", "name_ja": "京阪本線", "short": "Keihan"},
    "KO": {"n02": [(_KH, "鴨東線")], "name": "Keihan Ōtō Line", "name_ja": "鴨東線", "short": "Keihan"},
    "KU": {"n02": [(_KH, "宇治線")], "name": "Keihan Uji Line", "name_ja": "宇治線", "short": "Keihan"},
    "KK": {"n02": [(_KH, "京津線")], "name": "Keihan Keishin Line", "name_ja": "京津線", "short": "Keihan"},
    # Hankyu (阪急電鉄)
    "HY": {"n02": [(_HQ, "京都線")], "name": "Hankyu Kyoto Line", "name_ja": "阪急京都線", "short": "Hankyu"},
    "HA": {"n02": [(_HQ, "嵐山線")], "name": "Hankyu Arashiyama Line", "name_ja": "阪急嵐山線", "short": "Hankyu"},
    # Kintetsu (近畿日本鉄道)
    "KT": {"n02": [(_KT, "京都線")], "name": "Kintetsu Kyoto Line", "name_ja": "近鉄京都線", "short": "Kintetsu"},
    # Randen (京福電気鉄道)
    "RA": {"n02": [(_RD, "嵐山本線")], "name": "Randen Arashiyama Main Line", "name_ja": "嵐山本線",
           "short": "Randen"},
    "RK": {"n02": [(_RD, "北野線")], "name": "Randen Kitano Line", "name_ja": "北野線", "short": "Randen"},
    # Eiden (叡山電鉄)
    "EM": {"n02": [(_ED, "叡山本線")], "name": "Eiden Eizan Main Line", "name_ja": "叡山本線", "short": "Eiden"},
    "EK": {"n02": [(_ED, "鞍馬線")], "name": "Eiden Kurama Line", "name_ja": "鞍馬線", "short": "Eiden"},
}
# COLOURS: the project's own, not the operators' (Kobe's rule). A search over
# the sRGB cube (step 8; 3,817 feasible colours): 3:1 against BOTH map pages
# (#0B1220 and #ffffff), CIE76 >= 45 against every category pin, >= 18 between
# lines, each nearest its operator's hue family (lightness weighted half) in
# the order below: the subway's green and vermilion, JR West's blue (Sagano
# purple, Nara brown, Kosei light blue), Keihan's green, Hankyu's maroon,
# Kintetsu's red, the Randen's Kyoto purple, Eiden's orange. Result: pins
# 45.0-74.8, closest line pair 18.0 (Hankyu's two lines). Four greens for
# Keihan left the Karasuma Line olive.
#
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search, and three
# lines sat under the owner's floor of 20 from it (2026-10-07). Each moved to
# the colour nearest its own that reads 3:1 on both pages, clears 20 from
# every pin this map draws and 18 from every other line, taking 25 where that
# cost little: the Karasuma Line #608000 (11.6) to #387C04, a greener green
# (olive 25.4); the Keihan Main Line #586818 (15.8) to #506C30 (25.6); the
# Keihan Keishin Line #909040 (16.0) to #949054 (25.2), ONE colour with
# Otsu's, which draws the same line. Six of 18 lines sit between 20 and 45
# from olive (these three, the Keihan Oto 29.1, JR Nara 33.2, Eiden Eizan
# 43.0), an accepted trade (owner, 2026-10-07). Closest pair still 18.0; the
# dark-mode labels separate, 18 of 18. DECISIONS, "Lines within 20 of the
# olive and violet pins recoloured".
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
# Moved so the shared colours fit (2026-10-07), hue kept as far as they allow:
# the Tōzai Line #E85820 to #D84810 (pins 52.3, nearest line Kintetsu Kyoto
# Line 12.2, nearest beside it 46.5). docs/decisions_drafts/line-registry.md.
COLOURS = {
    "K": "#387C04", "T": "#D84810", "JA": line_registry.colour("jr-west-kyoto-line"),
    "JB": line_registry.colour("jr-west-biwako-line"), "JE": "#C870C8",
    "JD": line_registry.colour("jr-west-nara-line"), "JC": line_registry.colour("jr-west-kosei-line"),
    "KM": line_registry.colour("keihan-main-line"), "KO": "#60A000",
    "KU": line_registry.colour("keihan-uji-line"), "KK": line_registry.colour("keihan-keishin-line"),
    "HY": line_registry.colour("hankyu-kyoto-line"), "HA": "#C88070",
    "KT": line_registry.colour("kintetsu-kyoto-line"), "RA": "#9840A0", "RK": "#B880A8", "EM": "#D08000",
    "EK": "#B05800",
}
for _k, _v in LINES.items():
    _v["colour"] = COLOURS[_k]
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}

# Branches inside one N02 line (japan_step1 walks the section graph from
# `terminus` and stops within `junction_m` of `junction`):
#   * JB: the Biwako Line is 東海道線 east of 京都 - 山科 and the track beyond
#     it toward Ōtsu; the rest of 東海道線 is the JR Kyoto Line. Kyoto
#     station's platforms are long: at the default 150 m from their centroid
#     the walk slipped through the junction and ran 32.9 km (Osaka's 大阪 needed
#     350 m for the same reason).
BRANCHES = {
    "JB": {"line": (_JR, "東海道線"), "terminus": "山科", "junction": "京都", "junction_m": 350,
           # 大津 and 膳所 are beyond the city line, but excluded_stations.csv
           # names their line: without them there they read as the JR Kyoto Line
           "stations": ("山科", "大津", "膳所"), "length_m": (5000, 20000)},
}

# Gate 3: the operators' own station counts for the lines wholly inside the
# city: the Kyoto Municipal Subway's Karasuma Line (K01 Kokusaikaikan to K15
# Takeda), Randen (A1 Shijō-Ōmiya to A13 Arashiyama; the Kitano Line B1-B9 and
# Katabiranotsuji), Eiden (E01 Demachiyanagi to E08 Yase-Hieizanguchi; the
# Kurama Line E09-E17 and Takaragaike). The Tōzai Line's Rokujizō (T01) is in Uji.
GATE3 = {"source": "operators' station numbering (Kyoto Municipal Subway K, Randen A/B, Eiden E)",
         "lines": {"K": 15, "RA": 13, "RK": 10, "EM": 8, "EK": 10}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KYOTO_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KYOTO_BBOX
