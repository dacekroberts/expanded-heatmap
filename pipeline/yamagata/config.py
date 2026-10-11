"""Yamagata-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/yamagata.md (5/7 checks, 2026-10-11: the city replaced its
August list with September's on 2026-10-10, so the two checks that name the
August file fail; the build reads the cached August edition the brief
measured). Part of the A/B build plan's Regional-2 batch, on the shared
modules (pipeline/countries/japan*.py) with every shared rule on. Food only
(Band B, owner 2026-10-06, calls 137 and 138: Hiroshima's page shape; the
city's partial barber, beauty and laundry lists stay out).

Business leg: the city's own 食品営業許可施設一覧 (健康医療部 生活衛生課, CC BY
4.0 through 山形市オープンデータ利用規約): ONE file of every food permit in term
on 2026-08-31, in the national 食品等営業許可・届出一覧 schema, republished whole
each month under a dated name, so nothing is rebuilt (Aomori's shape). MHLW's
食品衛生申請等システム open data for 06201 adds three things only (Okazaki's,
Ichinomiya's and Matsuyama's precedent): its notifications (届出) as a
partial, opt-in food-retail layer; its own point for a city row the block
join misses (POINT_DONORS); and, in memory only, the name rule's answer for
the city's rows (the owner's call 182; see source_rows). Its permits are not
added (3,006 of 3,357 are in the city's list by number and date). All placed
by a JOIN to MLIT's 位置参照情報 (one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR East's Ou, Senzan and Aterazawa lines. English station names from
OpenStreetMap's name:en.
"""

import re
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "yamagata" / "raw"
DATA_PROCESSED = ROOT / "data" / "yamagata" / "processed"
OUTPUTS = ROOT / "outputs" / "yamagata"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Yamagata"
SLUG = "yamagata"
MUNICIPALITY = "山形市"
PREFECTURE = "山形県"

# The city's own CMS (no catalogue API); the file is a plain GET under
# /_res/projects/default_project/_page_/001/012/802/. The dataset page carries
# 「この 作品 は クリエイティブ・コモンズ 表示 4.0 国際 ライセンス の下に提供されています」
# and binds a user to 山形市オープンデータ利用規約 by use; the terms prescribe the
# credit for a modified work (clause 2(3)). Read 2026-10-07 by staging
# (licence-read): permitted with conditions; clause 4, a reimbursement
# triggered by use and uncapped, accepted by the owner (call 206;
# DECISIONS.md, "Licence reads for the Japan builds"). The terms are re-read
# before each refresh (clause 1: they change without notice).
_HOST = "https://www.city.yamagata-yamagata.lg.jp"
# 健康医療部 生活衛生課: 食品営業許可・届出施設一覧, page 1012802 (refreshed
# monthly, on the 10th; 更新日 2026-10-10 when this build read it).
FOOD_PAGE = _HOST + "/kenkofukushi/eisei/1006555/1006558/1012802.html"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# source key -> (file, URL of the edition this build read, the page that
# carries its licence). One entry per file fetched (Step 0, 2026-10-06, each
# HTTP 200 from its publisher's own host: 480,181 B and 1,963,932 B).
SOURCE_FILES = {
    "food": ("062014_syokuhin_list_20260831.csv",
             _HOST + "/_res/projects/default_project/_page_/001/012/802/062014_syokuhin_list_20260831.csv",
             FOOD_PAGE),
    "mhlw": ("06201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=06201_food_business_all.csv",
             MHLW_TOP),
}
# The food file is RENAMED each month (..._20260831.csv is the list to
# 2026-08-31) and the month before is removed: on 2026-10-11 the page linked
# ..._20260930.csv and the pinned URL answered 404. fetch_sources.py reads the
# current link from the page when the file is not on disk or --force is given
# (Kawasaki's, Otsu's and Akita's SOURCE_LINKS); the pinned URL records which
# edition this build read. A refresh takes a new file name, a new FOOD_AS_OF
# and a re-measure of every figure below.
SOURCE_LINKS = {"food": r"/062014_syokuhin_list_\d{8}\.csv$"}
# Kyoto's rule: the last day each list covers, never the download's. The
# city's file name and the page's title (令和8年8月31日時点で営業中の
# 食品営業許可施設一覧) state it. MHLW's monthly file states none (its newest
# 許可年月日 is 2026-08-31).
FOOD_AS_OF = "2026-08-31"
SOURCE_AS_OF = {"food": FOOD_AS_OF, "mhlw": None}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. The city's list holds only
# permits in term (grants 2019-03-22 to 2026-08-31, every 許可満了日 on or
# after 2026-09-30; measured 2026-10-11). MHLW's notifications carry no term
# (its key is required because the file has the term columns).
TERM_AS_OF = {"food": FOOD_AS_OF, "mhlw": FOOD_AS_OF}

# What step 2 reads. "mhlw" is the notifications only (source_rows).
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: the city's file is Shift_JIS (cp932) with no BOM,
# MHLW's UTF-8 with a BOM; both CRLF, the header on line 1.
SOURCE_ENCODING = {"food": "cp932", "mhlw": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The city's file is the national schema's 34 columns
# with six filled (施設名称 3,319 of 3,584 rows, 所在地_連結表記 3,317, the type,
# the number and the two dates); its 法人名 is EMPTY on every row and is
# required only so a later edition that fills it is still compared. MHLW's
# 法人名 (a sole trader's own name as often as a company's) is REQUIRED so the
# name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing; read IN MEMORY by that rule only, never kept.
# Never selected: 法人番号, 法人住所, every phone and フリガナ column.
REQUIRED_COLUMNS = {
    "food": ("施設名称", "営業の種類", "所在地_連結表記", "法人名", "許可番号", "許可年月日", "許可満了日"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名", "許可番号", "許可年月日"),
}
REQUIRED_COLUMNS["mhlw_points"] = REQUIRED_COLUMNS["mhlw"]
# An address is published only where the operator agreed to it. MHLW's rule
# everywhere; here the city's list follows it too: 265 of its rows carry no
# name and no address (220 of them restaurants), 261 of them MHLW permits
# whose address MHLW withholds as well (the brief, 2026-10-06). Counted apart
# from "not a premises" and disclosed on the page (Hiroshima's wording).
ADDRESS_BY_CONSENT = {"food", "mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point (the
# brief: a median 43 m from the block point, 95.7% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# A city food row the block join misses takes MHLW's point for the same
# premises (town, trade name), read from the whole file under its own key,
# never drawn (the owner's call 127c; Ichinomiya's, Matsuyama's, Toyama's and
# Okazaki's mechanism).
POINT_DONORS = {"food": "mhlw_points"}
# A premises in both (a city permit and an MHLW notification of one bucket):
# MHLW's row stays (Matsuyama's, Okazaki's).
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    if key == "mhlw_points":
        key = "mhlw"
    return DATA_RAW / SOURCE_FILES[key][0]


def _permit_key(row):
    """A permit as both files number it: the digits of 許可番号 (the city
    writes R08-1234 and H31-1234, MHLW 1234 or 第1234号) and the grant date."""
    from pipeline.countries import japan_register as jr

    runs = re.findall(r"\d+", (row.get("許可番号") or "").strip())
    day = jr.wareki_date(row.get("許可年月日"))
    return (runs[-1].lstrip("0"), day) if runs and day else None


def _operator_answers():
    """{permit key: True/False}: whether a city trade name is its operator's
    own name, answered from MHLW's 法人名 for the same permit. The city's file
    publishes no operator column (法人名 empty on all 3,584 rows), while MHLW's
    file names the operator of 3,000 of them (measured 2026-10-11; the brief
    counted 3,006 of MHLW's permits in the list). The owner's call 182
    (2026-10-06): MHLW's 法人名 is read IN MEMORY through the permit match and
    the matching trade names are withheld: 3 rows on 2026-10-11 (the brief
    read 4), one of them at a fixed address. Only the answer leaves this function, never a name (Kyoto's
    precedent: a source's rows carry name_is_operator, which
    japan_register.name_is_operator reads in place of a column)."""
    from pipeline.countries import japan, japan_register as jr

    coop = "coop" in japan.city_rules(SLUG)
    operators = {}
    for r in jr.city_rows(source_csv("mhlw")):
        k = _permit_key(r)
        if k and (r.get("申請区分") or "").startswith("許可"):
            operators.setdefault(k, []).append(r.get("法人名"))
    return lambda row: (jr.same_person(row.get("施設名称") or "", operators[k], coop)
                        if (k := _permit_key(row)) in operators else None)


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    "food" is the city's list as it stands, each row that matches an MHLW
    permit carrying the name rule's answer (_operator_answers; call 182).
    "mhlw" yields only MHLW's notifications (申請区分 届出 / 届出(廃業)): its
    permits are not added, the city's list being complete (the owner's calls
    126 and 128, Ichinomiya's precedent). "mhlw_points" is the whole file,
    read by POINT_DONORS for its coordinates only."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    answer = _operator_answers() if key == "food" else None
    for r in jr.city_rows(path):
        if key == "mhlw" and not (r.get("申請区分") or "").startswith("届出"):
            continue
        if answer:
            a = answer(r)
            if a is not None:
                r["name_is_operator"] = a
        yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 06201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Yamagata.
# S, W, N, E: the city's N03 extent (S 38.143, W 140.179, N 38.352,
# E 140.531) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (38.14, 140.17, 38.36, 140.54)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment). One: OSM writes a macron on one of the 11 names and none on 蔵王
# (Zao), so the city's names are brought to one style, without macrons, as
# Okazaki's and Hiroshima's. The other 10 stand as OSM writes them (20
# objects, 19 with name:en, 2026-10-11; the one without is 天童南, outside the
# city): a hyphen after a prefix (Kita-Yamagata, Minami-Dewa, Uzen-Chitose,
# Higashi-Kanai), no translated name, no numeral.
OSM_NAME_EN_OVERRIDES = {
    "面白山高原": "Omoshiroyama-Kogen",                 # Omoshiroyama-Kōgen
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the N03 centroid (~140.369) and the whole extent (140.179 to
# 140.531) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): step 1 measured a median nearest-station gap of 2,221 m
# (minimum 1,344 m) over the 11 drawn stations (2026-10-11; the brief read
# the same), far over the halving line (about 550 m). Re-measure if the
# drawn stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 3 lines, all JR East, railway class 11). N02 files no Shinkansen
# station in the city: the Yamagata Shinkansen's trains run over the Ou
# Line's own track and are not counted (owner 2026-09-24; Akita's shape).
# Every line is cut at the city line: the Ou Line keeps 6 of 105 station
# records, the Senzan Line 5 of 18, the Aterazawa Line 2 of 11 (a rural JR
# line cut at the line, not an urban stub). 北山形 (Ou and Aterazawa) and
# 羽前千歳 (Ou and Senzan) are one N02 group each. No frequency floor (owner,
# 2026-10-06, calls 46 and 86), and no stretch is at about 11 trains a day or
# fewer: 16 to 19 weekday departures each way on every line (JR East's
# station timetables at 山形, 蔵王, 山寺 and 東金井, the 2026-10 edition, read
# 2026-10-06 for the brief).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (`hue`) and the
# project's colour. Line names carry no macrons and no "Main" for JR, as
# Akita's, Fukushima's and Aomori's JR Ou Line (the same line).
_JR = "東日本旅客鉄道"
LINES = {
    "OU": {"n02": [(_JR, "奥羽線")], "name": "JR Ou Line", "name_ja": "奥羽本線", "short": "JR",
           "hue": "#E07800"},
    "SZ": {"n02": [(_JR, "仙山線")], "name": "JR Senzan Line", "name_ja": "仙山線", "short": "JR",
           "hue": "#72BC4A"},
    "AT": {"n02": [(_JR, "左沢線")], "name": "JR Aterazawa Line", "name_ja": "左沢線", "short": "JR",
           "hue": "#00A0DE"},
}
# Colours: JR East's Ou Line takes its one site-wide colour from
# pipeline/line_registry.py (owner, 2026-10-07: one colour per line on every
# map; Akita's, Fukushima's and Aomori's maps draw it). The Senzan and
# Aterazawa lines are on this map alone: the project's own colours, from
# `python scripts/line_colour_search.py yamagata` (2026-10-11, defaults: >= 18
# within 500 m, >= 10 city-wide), each the feasible colour nearest its
# starting hue (a JR East green; a sky blue) that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Margins from the pins: Ou 53.6, Senzan
# 45.6, Aterazawa 70.6 (none between 20 and 45). Closest pair 94.2 (Ou,
# Senzan, which share 羽前千歳); the dark-mode labels separate, 3 of 3.
_COLOURS = {"OU": line_registry.colour("jr-east-ou-line"), "SZ": "#28A800", "AT": "#0098D8"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3 has no in-city count to compare: every line runs on past the city
# line (Aomori's and Fukui's shape). JR East's station timetable pages
# (timetables.jreast.co.jp) were read for four of the 11 stations (山形, 蔵王,
# 山寺, 東金井; 2026-10-06, the brief); the operator's per-line station list was
# not read, so N02's whole-line totals (Ou Line 105 records, Senzan Line 18,
# Aterazawa Line 11) stand unchecked against the operator. Step 1 reproduced
# the brief's in-city counts 2026-10-11 (6, 5, 2; 11 stations).
GATE3 = {"source": "none: no line is wholly inside the city (JR East's station timetable pages, "
                   "timetables.jreast.co.jp, read for four of the 11 stations)", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
YAMAGATA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = YAMAGATA_BBOX
