"""Matsuyama-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/matsuyama.md
(10/10 checks, 2026-10-02). The pilot of the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py).

Business leg: the city's own CC BY 4.0 lists, all as of 2026-03-31: food
permits in two CSVs (old law to 2021-05, new law since; every permit in force)
and full registers of barbers, beauty salons and laundries (old .xls). MHLW's
食品衛生申請等システム open data adds two things only (owner, 2026-10-02, "approve
all recommendations"): its notifications (届出) as a partial, opt-in food-retail
bucket, and its own point for a city row the block join misses
(config.POINT_DONORS). Everything placed by a JOIN to MLIT's 位置参照情報 for
the one municipality (no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). The city tram, Iyotetsu's three suburban lines and JR's Yosan Line.
English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "matsuyama" / "raw"
DATA_PROCESSED = ROOT / "data" / "matsuyama" / "processed"
OUTPUTS = ROOT / "outputs" / "matsuyama"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Matsuyama"
SLUG = "matsuyama"
MUNICIPALITY = "松山市"
PREFECTURE = "愛媛県"

# The city's open-data metadata pages (松山市オープンデータ), each ライセンス CC-BY,
# under the site's 利用規約 (令和4年4月1日): CC BY 4.0 International.
_OD = "https://www.city.matsuyama.ehime.jp/shisei/opendata/metadata"
FOOD_PAGE = f"{_OD}/shokuhin.html"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    # 食品営業許可全施設一覧: the old-law permits (granted to 2021-05-31) and
    # the new-law ones (since 2021-06-01), every permit in force on 2026-03-31
    "food_old": ("382019_food_business_all_2026031.csv",
                 f"{_OD}/shokuhin.files/382019_food_business_all_2026031.csv", FOOD_PAGE),
    "food_new": ("382019_food_business_all_2026032.csv",
                 f"{_OD}/shokuhin.files/382019_food_business_all_2026032.csv", FOOD_PAGE),
    "barber": ("riyou.zen.xls", f"{_OD}/riyoushozensisetu.files/riyou.zen.xls", f"{_OD}/riyoushozensisetu.html"),
    "beauty": ("biyou.zen.xls", f"{_OD}/biyoushozensisetu.files/biyou.zen.xls", f"{_OD}/biyoushozensisetu.html"),
    "laundry": ("clean.zen.xls", f"{_OD}/cleaningzensisetu.files/clean.zen.xls", f"{_OD}/cleaningzensisetu.html"),
    "mhlw": ("38201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=38201_food_business_all.csv",
             MHLW_TOP),
}
# 令和8年3月31日時点 on every city list (Kyoto's rule: the date the list
# states, never the download's); MHLW's monthly file states none.
SOURCE_AS_OF = {"food_old": "2026-03-31", "food_new": "2026-03-31", "barber": "2026-03-31",
                "beauty": "2026-03-31", "laundry": "2026-03-31", "mhlw": None}
FOOD_AS_OF = "2026-03-31"
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The two food lists are one kind (japan_step2.kind): the key names the file.
SOURCE_KIND = {"food_old": "food", "food_new": "food"}
# Declared, never inferred: the food lists are UTF-8 CSV in the national
# schema (the new-law file opens with an empty line, which city_rows passes
# over to the header); the registers are the old BIFF .xls, read through
# workbook_tables; MHLW's is UTF-8 with a BOM.
SOURCE_ENCODING = {"food_old": "utf-8", "food_new": "utf-8", "barber": "xls", "beauty": "xls",
                   "laundry": "xls", "mhlw": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 申請者個人名, 法人代表者氏名, 開設者氏名 and 営業者氏名 are
# REQUIRED so the name rule (japan_register.name_is_operator; owner 2026-09-27)
# cannot silently compare nothing; they are read IN MEMORY by that rule only,
# never kept. Never selected: the phones, e-mail, 郵便番号, 法人名, 法人番号,
# 役職名, and MHLW's 法人名 / 法人番号 / 法人住所.
_FOOD = ("施設名称1", "営業の種類", "所在地＿連結表記", "申請者個人名", "法人代表者氏名", "許可満了日")
REQUIRED_COLUMNS = {
    "food_old": _FOOD,
    "food_new": _FOOD,
    "barber": ("施設名称１", "施設所在地１", "開設者氏名"),
    "beauty": ("施設名称１", "施設所在地１", "開設者氏名"),
    "laundry": ("施設名称１", "施設所在地１", "営業者氏名", "クリーニング種別１"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日"),
}
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point.
OWN_POINT_FALLBACK = {"mhlw"}
# A city food row the block join misses takes MHLW's point for the same
# premises (ward, town, trade name), the brief's (a): 797 rows, block-or-own
# 81.9% to 92.7%. MHLW's file is read for its points only, under its own key.
POINT_DONORS = {"food_old": "mhlw_points", "food_new": "mhlw_points"}
# A premises in both (a konbini holding a city restaurant permit and filing
# an MHLW notification): MHLW's row stays.
SUPERSEDES = {"mhlw": ("food_old", "food_new")}


def source_csv(key):
    return DATA_RAW / SOURCES["mhlw" if key == "mhlw_points" else key]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    MHLW's file yields only its notifications (申請区分 届出 / 届出(廃業)) as
    "mhlw": the city's own list holds every permit (6,114 restaurants, 103% of
    the official count), so MHLW adds no permit (the brief). "mhlw_points" is
    the whole file, read by POINT_DONORS for its coordinates only."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 38201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and the city tram's stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent (S 33.687, W 132.491, N 34.074, E 132.927,
# the 中島 islands included), rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (33.67, 132.48, 34.09, 132.94)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-02): OSM writes the 丁目 number as a figure
# (本町6丁目), and names two tram stops with 前 / 駅前 where N02 does not.
OSM_NAME_ALIASES = {
    "本町一丁目": "本町1丁目", "本町三丁目": "本町3丁目", "本町四丁目": "本町4丁目", "本町五丁目": "本町5丁目",
    "本町六丁目": "本町6丁目", "萱町六丁目": "萱町6丁目", "平和通一丁目": "平和通1丁目", "道後公園": "道後公園前",
    "松山市駅": "松山市駅前",
}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae, a 丁目
# stop as "1-chome". OSM TRANSLATED six stops (Fukuoka's trap) and gives the
# railway's 松山市 and the tram's 松山市駅, 63 m apart, the same name; each is
# romanised here, as the operator signs them.
OSM_NAME_EN_OVERRIDES = {
    "松山市": "Matsuyama-shi",                      # Matsuyama City
    "松山市駅": "Matsuyama-shi-eki",                 # Matsuyama City (the tram stop 松山市駅前)
    "市役所前": "Shiyakusho-mae",                    # Matsuyama City Hall
    "県庁前": "Kencho-mae",                          # Ehime Pref. Office
    "警察署前": "Keisatsusho-mae",                   # Police Station
    "赤十字病院前": "Sekijuji-byoin-mae",             # Red Cross Hospital
    "道後公園": "Dogo-koen",                         # Dogo Park
    "石手川公園": "Ishitegawa-koen",                  # Ishitegawa Park
    "大手町駅前": "Otemachi-ekimae",                  # Otemachi Sta.
    "JR松山駅前": "JR Matsuyama-ekimae",              # JR Matsuyama Station-mae
    "本町一丁目": "Hommachi 1-chome",                 # Hommachi 1
    "本町三丁目": "Hommachi 3-chome",                 # Hommachi 3
    "本町四丁目": "Hommachi 4-chome",                 # Hommachi 4
    "本町五丁目": "Hommachi 5-chome",                 # Hommachi 5
    "本町六丁目": "Hommachi 6-chome",                 # Hommachi 6
    "萱町六丁目": "Kayamachi 6-chome",                # Kayamachi 6
    "平和通一丁目": "Heiwadori 1-chome",              # Heiwadori 1
    "伊予北条": "Iyo-Hojo",                          # Iyo-Hōjō
    "光洋台": "Koyodai",                             # Kōyōdai
    "大浦": "Oura",                                  # Ōura
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~132.77) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# HALVED, on the spacing rule (docs/ring_rules.md: the halved edges where the
# median station gap is about 550 m or less): step 1 measured 374 m among the
# 60 in-city stations, 28 of them the city tram's stops (2026-10-02), as
# Hiroshima's 357 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# Gate 1's floor: Hiroshima's, Paris's and Riga's 200 m, not a new number - a
# tram network is genuinely closer than 400 m (collapsed median 374 m;
# platforms 314 m).
SPACING_MIN_M = 200.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 10 legal lines, no Shinkansen): Iyotetsu's six tram sections
# (all wholly inside), its Takahama Line (10 of 10), Yokogawara Line (9 of 15)
# and Gunchū Line (5 of 12), and JR's Yosan Line (11 of 95), cut at the city
# line (owner 2026-09-24). No line is cut to a stub.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the city tram under six LEGAL
# sections (城北線, 城南線, 大手町線, 本町線, 花園線, 連絡線) that no rider reads; the
# operator runs routes 1 to 6 over them, and the Botchan train over the same
# track adds none. Drawn as ONE line under the tram's public name, on
# Sapporo's precedent for its streetcar (and Hakodate's brief): the routes
# overlap almost everywhere, so drawing each would stack five lines on one
# track.
_IY, _JR = "伊予鉄道", "四国旅客鉄道"
LINES = {
    "TR": {"n02": [(_IY, "城北線"), (_IY, "城南線"), (_IY, "大手町線"), (_IY, "本町線"), (_IY, "花園線"),
                   (_IY, "連絡線")],
           "name": "Iyotetsu City Tram", "name_ja": "伊予鉄道市内電車", "short": "Iyotetsu", "hue": "#F08300"},
    "TK": {"n02": [(_IY, "高浜線")], "name": "Iyotetsu Takahama Line", "name_ja": "高浜線", "short": "Iyotetsu",
           "hue": "#F39800"},
    "YK": {"n02": [(_IY, "横河原線")], "name": "Iyotetsu Yokogawara Line", "name_ja": "横河原線",
           "short": "Iyotetsu", "hue": "#F39800"},
    "GC": {"n02": [(_IY, "郡中線")], "name": "Iyotetsu Gunchu Line", "name_ja": "郡中線", "short": "Iyotetsu",
           "hue": "#F39800"},
    "JY": {"n02": [(_JR, "予讃線")], "name": "JR Yosan Line", "name_ja": "予讃線", "short": "JR", "hue": "#00A5E3"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# matsuyama` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. Iyotetsu's four share one orange
# and spread over amber and brown. Closest pair within 500 m 18.4 (Gunchu /
# Yokogawara, which meet only at 松山市); the dark-mode labels separate, 5 of 5.
_COLOURS = {"TR": "#E07800", "TK": "#C88800", "YK": "#A86000", "GC": "#C05008", "JY": "#08A0C0"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operator's own station counts for the lines wholly inside the
# city, against the collapsed set: Iyotetsu's station index lists the
# Takahama Line's 10 stations, 松山市 to 高浜 (read 2026-10-02). Its site gives
# no tram stop count (the brief found the same), so the tram's 28 stops are
# N02's, as Hiroden's are in Hiroshima; the lines the city line cuts have no
# in-city count.
GATE3 = {"source": "Iyotetsu's station index (iyotetsu.co.jp/information/station/)", "lines": {"TK": 10}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
MATSUYAMA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = MATSUYAMA_BBOX
