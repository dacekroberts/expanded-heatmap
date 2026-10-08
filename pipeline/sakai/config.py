"""Sakai-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/sakai.md
(9/9 checks, 2026-10-02). Part of the 2026-10-01 Japanese batch, on the shared
modules (pipeline/countries/japan*.py). Food only (Band B, owner 2026-10-01:
Hiroshima's page): the city's barber, beauty and laundry lists are PDFs.

Business leg: the city's own CC BY 4.0 food-permit list, REBUILT to 2026-08-31
(Kyoto's source_rows shape): the standing list of 2026-04-01, plus the monthly
new-permit files for April to August, less the monthly closures matched by
許可番号, then kept while in term on the pinned as-of (japan_register.in_term).
MHLW's 食品衛生申請等システム open data adds its notifications (届出) only, as a
partial, opt-in food-retail bucket (Fukuoka's, Hiroshima's and Matsuyama's
precedent). Everything placed by a JOIN to MLIT's 位置参照情報 for the 7 wards.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The Hankai tram, the Midōsuji Line, Nankai's Main, Kōya and Semboku
lines and JR's Hanwa Line. English station names from OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "sakai" / "raw"
DATA_PROCESSED = ROOT / "data" / "sakai" / "processed"
OUTPUTS = ROOT / "outputs" / "sakai"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Sakai"
SLUG = "sakai"
MUNICIPALITY = "堺市"
PREFECTURE = "大阪府"

# The city's list page (食品営業許可施設一覧, 令和8年度). Its open-data paragraph
# links the 堺市オープンデータ利用規約 (3-2: CC BY 4.0 International), which
# covers the monthly files on the page too (owner, 2026-10-02, on Hiroshima's
# reading of 2026-09-24). The standing list is also BODIK dataset
# 271403__sakai_food_business_all_r8 (the same bytes, license cc-by-40-intl).
_LIST = "https://www.city.sakai.lg.jp/kenko/shokuhineisei/anzenjoho/kyokashisetsuichiran"
FOOD_PAGE = f"{_LIST}/R8kyokaichiran.html"
_FILES = f"{_LIST}/R8kyokaichiran.files"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# The months read: April to August 2026 (R0804 ... R0808), each a new-permit
# file and a closure file, posted about the 25th of the next month.
MONTHS = ("0804", "0805", "0806", "0807", "0808")
SOURCE_FILES = {
    # 「令和8年4月1日現在で許可を受けている施設」: every permit in force then
    "food": ("R80401.csv", f"{_FILES}/R80401.csv", FOOD_PAGE),
    **{f"new_{m}": (f"R{m}.csv", f"{_FILES}/R{m}.csv", FOOD_PAGE) for m in MONTHS},
    **{f"closed_{m}": (f"R{m}haigyou.csv", f"{_FILES}/R{m}haigyou.csv", FOOD_PAGE) for m in MONTHS},
    "mhlw": ("27140_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27140_food_business_all.csv",
             MHLW_TOP),
}
# The rebuilt register's date, PINNED (Kyoto's rule: the last day the newest
# file covers, never the download date or today): the August files.
AS_OF = datetime.date(2026, 8, 31)
_MONTH_END = {"0804": "2026-04-30", "0805": "2026-05-31", "0806": "2026-06-30", "0807": "2026-07-31",
              "0808": "2026-08-31"}
SOURCE_AS_OF = {"food": "2026-04-01", "mhlw": None,
                **{f"new_{m}": d for m, d in _MONTH_END.items()},
                **{f"closed_{m}": d for m, d in _MONTH_END.items()}}
FOOD_AS_OF = AS_OF.isoformat()
# What step 2 reads: the rebuilt register (source_rows("food")) and MHLW's
# notifications. The monthly files are read inside the rebuild only.
SOURCES = {"food": SOURCE_FILES["food"][0], "mhlw": SOURCE_FILES["mhlw"][0]}
# Declared, never inferred: the standing list and the new-permit files are
# UTF-8 with a BOM, the closure files cp932 (city_rows sniffs both); MHLW's is
# UTF-8 with a BOM.
SOURCE_ENCODING = {"food": "utf-8-sig", "mhlw": "utf-8-sig",
                   **{f"new_{m}": "utf-8-sig" for m in MONTHS}, **{f"closed_{m}": "cp932" for m in MONTHS}}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 営業者名 and 代表者名 are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; they are read IN MEMORY by that rule only, never kept. Never
# selected: 営業者住所 and 営業者方書 (an operator's own address, filled on 4,854
# rebuilt rows), 営業所電話番号, and MHLW's 法人名 / 法人番号 / 法人住所 / phones.
_FOOD = ("許可番号", "営業所の名称", "営業所所在地", "営業の種類", "業態", "許可満了日", "営業者名", "代表者名")
REQUIRED_COLUMNS = {
    "food": _FOOD,
    **{f"new_{m}": _FOOD for m in MONTHS},
    **{f"closed_{m}": ("許可番号", "廃業届出日") for m in MONTHS},
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# The columns a rebuilt row carries on into step 2: the premises' own, the
# dates, and the two operator-name columns for the name rule (in memory).
_KEEP_FOOD = ("許可番号", "営業所の名称", "営業所所在地", "営業の種類", "業態", "許可満了日", "申請区分",
              "営業者名", "代表者名")
_KEEP_MHLW = REQUIRED_COLUMNS["mhlw"]
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point.
OWN_POINT_FALLBACK = {"mhlw"}
# A premises in both, in one bucket (a shop holding a city permit, 食肉販売業 or
# 魚介類販売業, and filing an MHLW notification for its other lines): MHLW's
# row stays, as in Matsuyama and Hiroshima. Measured 2026-10-02 (step 2).
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _read(key, keep):
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        yield {c: r.get(c) for c in keep}


def rebuilt_register():
    """The city's food permits in force on AS_OF: the standing list
    (2026-04-01) and every monthly new-permit file, less every permit number a
    monthly closure file names, kept while 許可満了日 is on or after AS_OF.
    Measured 2026-10-02 (the brief): 10,123 + 777 new - 430 matched closures
    (of 434) = 10,470, then 383 past their expiry with no closure row."""
    import sys

    from pipeline.baseline import emit
    from pipeline.countries import japan_register as jr

    closed = {(r["許可番号"] or "").strip() for m in MONTHS for r in _read(f"closed_{m}", ("許可番号",))}
    closed.discard("")
    rows = list(_read("food", _KEEP_FOOD))
    standing = len(rows)
    new = [r for m in MONTHS for r in _read(f"new_{m}", _KEEP_FOOD)]
    rows += new
    numbers = {(r["許可番号"] or "").strip() for r in rows}
    gone = [r for r in rows if (r["許可番号"] or "").strip() in closed]
    rows = [r for r in rows if (r["許可番号"] or "").strip() not in closed]
    kept = list(jr.in_term(rows, ("許可満了日",), AS_OF))
    print(f"  rebuilt register on {AS_OF}: standing {standing:,} + new {len(new):,} - closed {len(gone):,} "
          f"(of {len(closed):,} closure numbers, {len(closed & numbers):,} matched) = {len(rows):,}; "
          f"past 許可満了日 {len(rows) - len(kept):,}; in term {len(kept):,}", file=sys.stdout)
    emit("rebuilt_closed_matched", len(gone))
    emit("rebuilt_in_term", len(kept))
    return kept


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    "food" is the rebuilt register; MHLW's file yields only its notifications
    (申請区分 届出 / 届出(廃業)), since the city's list holds every permit (8,285
    restaurants on 2026-04-01, 101% of the official 8,229). Only the columns
    named above are carried; the operator's address never leaves the file."""
    if key == "food":
        return rebuilt_register()
    return (r for r in _read(key, _KEEP_MHLW) if (r.get("申請区分") or "").startswith("届出"))


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward
# (27141-27147).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and the Hankai tram's stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 34.430, W 135.388, N 34.608, E 135.588),
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.42, 135.37, 34.62, 135.6)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-02): the small ヶ / ケ differ.
OSM_NAME_ALIASES = {"三国ヶ丘": "三国ケ丘", "泉ケ丘": "泉ヶ丘"}
OSM_NAME_EN_TIES = {}
# OSM's objects carry no name:en (2026-10-02): Nankai's own romanisation, in
# Hiroshima's style.
OSM_NAME_EN_MISSING = {"諏訪ノ森": "Suwanomori", "浜寺公園": "Hamadera-koen"}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae, 駅前 as
# -ekimae. OSM misreads two Hankai stops (寺地町 as Teradicho, 高須神社 as
# Takasujinsha: 神社 is jinja); the rest of its spellings follow Nankai's and
# Hankai's signs (Sakaihigashi, Mozuhachiman) and are kept.
OSM_NAME_EN_OVERRIDES = {
    "寺地町": "Terajicho",                           # Teradicho
    "高須神社": "Takasu-jinja",                       # Takasujinsha
    "御陵前": "Goryo-mae",                           # Goryo-Mae
    "妙国寺前": "Myokokuji-mae",                      # Myokokuji-Mae
    "浜寺駅前": "Hamadera-ekimae",                    # Hamaderaekimae
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.48) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# STANDARD, on the spacing rule (docs/ring_rules.md: halved only where the
# median station gap is about 550 m or less): step 1 measured 611 m among the
# 42 in-city stations, 15 of them the Hankai tram's stops (2026-10-02; the
# brief's figure). Re-measure if a line is added.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 6 lines, no Shinkansen), each cut at the city line (owner
# 2026-09-24): the Hankai Line 15 of 32 records (31 stops; Osaka's map draws
# the rest), the Midōsuji Line 3 of 20 (an urban line cut to a stub, DRAWN as
# cut: owner 2026-10-02), Nankai's Main 6 of 44, Kōya 9 of 43 and Semboku 5 of
# 6, and JR's Hanwa Line 8 records (7 stations) of 37. N02-25, not N02-24,
# which still files the Semboku Line under 泉北高速鉄道 (merged into Nankai
# 2025-04-01).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names as Osaka's map spells the same
# lines (Midōsuji, Nankai Kōya, Hankai Line), so one line reads alike on both
# maps.
# The Hagoromo branch (鳳 - 東羽衣, 1.7 km, 東羽衣 in Takaishi) is filed inside
# 阪和線 (trap 3) and NOT split into BRANCHES: inside the city it has no station
# of its own (鳳 is the Hanwa Line's), it is legally the Hanwa Line's branch,
# and split off it would be a second labeled line about 1 km long with no
# station to ring. Its in-city stretch is drawn as part of the Hanwa Line.
_M, _NK, _JR, _HK = "大阪市高速電気軌道", "南海電気鉄道", "西日本旅客鉄道", "阪堺電気軌道"
LINES = {
    "RH": {"n02": [(_HK, "阪堺線")], "name": "Hankai Line", "name_ja": "阪堺線", "short": "Hankai", "hue": "#5F8A00"},
    "M": {"n02": [(_M, "1号線(御堂筋線)")], "name": "Midōsuji Line", "name_ja": "御堂筋線", "short": "Osaka Metro",
          "hue": "#E5171F"},
    "NM": {"n02": [(_NK, "南海本線")], "name": "Nankai Main Line", "name_ja": "南海本線", "short": "Nankai",
           "hue": "#F18D00"},
    "NK": {"n02": [(_NK, "高野線")], "name": "Nankai Kōya Line", "name_ja": "南海高野線", "short": "Nankai",
           "hue": "#E4BE00"},
    "NB": {"n02": [(_NK, "泉北線")], "name": "Nankai Semboku Line", "name_ja": "泉北線", "short": "Nankai",
           "hue": "#0072BC"},
    "JR": {"n02": [(_JR, "阪和線")], "name": "JR Hanwa Line", "name_ja": "阪和線", "short": "JR", "hue": "#F39800"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py sakai`
# (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each the
# feasible colour nearest its operator's hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Closest pair within 500 m 18.4 (the Kōya
# Line / JR Hanwa, which meet at 三国ヶ丘); the dark-mode labels separate, 6 of
# 6.
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search: the Hankai
# Line's #689000 sat 17.4 from it, under the owner's floor of 20 (2026-10-07),
# and takes #449418 (olive 30.3), ONE colour with Osaka's for the same line
# (Osaka's config gives the search). Three of six lines sit between 20 and 45
# from olive (the Koya Line 23.2, the Hankai 30.3, JR Hanwa 34.7), an accepted
# trade (owner, 2026-10-07).
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
_COLOURS = {
    "RH": line_registry.colour("hankai-line"), "M": line_registry.colour("osaka-metro-midosuji-line"),
    "NM": line_registry.colour("nankai-main-line"), "NK": line_registry.colour("nankai-koya-line"),
    "NB": "#08A0C0", "JR": line_registry.colour("jr-west-hanwa-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own in-city counts where their numbering shows them:
# the Hankai Line's stops hn16 (大和川) to hn31 (浜寺駅前), hn30 unused, 15 in
# all (Hankai's route page, hankai.co.jp/route/, read 2026-10-02; 31 stops on
# the line, as N02); Osaka Metro's M28-M30 (北花田, 新金岡, なかもず), the
# numbering Osaka's gate reads. Nankai's and JR's in-city counts were not read
# from the operators; the city line cuts every one of their lines.
GATE3 = {"source": "operators' numbering (Hankai hn16-hn31; Osaka Metro M28-M30)", "lines": {"RH": 15, "M": 3}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SAKAI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SAKAI_BBOX
