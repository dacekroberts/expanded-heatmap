"""Sagamihara-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/sagamihara.md (17/17 checks, 2026-10-11). Sagamihara City
(相模原市, three wards: 14151 緑区, 14152 中央区, 14153 南区), a designated city
with its own health center. Japan's A/B batch (East-2), on the shared modules
(pipeline/countries/japan*.py) with the Japan foundation's rules on, in
Sakai's shape (a register rebuilt from the year-end list and the months
since, closures taken out by permit number) with Kawasaki's and Yokosuka's
page (the city's own lists, all three buckets).

Business leg: the city's own lists (相模原市 生活衛生課), CC BY 4.0 by the
city's open-data terms. Food: the list of permits in force on 2026-03-31,
REBUILT to 2026-08-31 with the five monthly files of new and closed permits
(one file a month holds both). Barbers and beauty salons: the 2026-03-31
registers rebuilt the same way from the monthly new and closed files.
Laundries: the 2026-03-31 register (yearly only). Every file is a zip of CSV
and PDF, read by this config's own reader (japan_register.city_rows reads
XLSX members of a zip only). The city's food NOTIFICATION dataset
(todokede_eigyo) is left out and never downloaded (owner, 2026-10-05), and
MHLW's open data (opt-in here, 7% of the official count) is a control, never
a source. All placed by a JOIN to MLIT's 位置参照情報 for the three wards.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03): JR East's Sagami, Yokohama and Chuo lines, Odakyu's Odawara and
Enoshima lines and Keio's Sagamihara Line, each cut at the city line.
English station names from OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "sagamihara" / "raw"
DATA_PROCESSED = ROOT / "data" / "sagamihara" / "processed"
OUTPUTS = ROOT / "outputs" / "sagamihara"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Sagamihara"
SLUG = "sagamihara"
MUNICIPALITY = "相模原市"
PREFECTURE = "神奈川県"

# The city's own CKAN catalogue. Its four 生活衛生課 datasets declare no
# licence of their own (license_id ""); the city's open-data page and terms
# (相模原市オープンデータ利用規約, 2018-03-28, §3(2)) put everything the site
# publishes under CC BY 4.0 (read 2026-10-04; re-read before each refresh,
# §1).
CKAN = "https://opendata.city.sagamihara.kanagawa.jp"
CKAN_API = CKAN + "/api/3/action"
FOOD_PAGE = CKAN + "/dataset/eigyo_kyoka"
BARBER_PAGE = CKAN + "/dataset/riyosho"
BEAUTY_PAGE = CKAN + "/dataset/biyosho"
LAUNDRY_PAGE = CKAN + "/dataset/cleaning"
_FOOD_DS = CKAN + "/dataset/3bd39977-a8cd-49d5-8160-48c0620acf11/resource/"
_BARBER_DS = CKAN + "/dataset/a8a6040a-dfff-430c-a66c-a345f40d3c9d/resource/"
_BEAUTY_DS = CKAN + "/dataset/7b1f33cd-f485-4065-8eaa-f7df440b09a8/resource/"
_LAUNDRY_DS = CKAN + "/dataset/e9b089bf-540a-4337-b5b2-ac3140ee2eb9/resource/"
# file key -> the CKAN resource id. Each resource is REPLACED in place (the
# monthly zips grow each month, the year-end zips each April), so
# fetch_sources.py reads a missing file's current URL from resource_show
# (SOURCE_RESOURCES; Yokosuka's shape) and the pinned URL records which
# edition this build read (resource_show, 2026-10-11: the sizes on disk).
_RESOURCE = {
    "food": "1be0eb65-0348-4668-a440-0ce10cad1063",
    "food_months": "007f1def-2b10-4e5d-81de-18a3e78ec51c",
    "barber": "a2a1ed31-2e2d-44db-8ddc-d14eb9bdc578",
    "barber_new": "2cfb7cf7-b129-457d-a8e3-85110761d8cb",
    "barber_closed": "99a7afc9-a7a3-4f26-b701-89e72e87aeff",
    "beauty": "09e7aa6d-483e-4fa8-8e03-9e9a0575829e",
    "beauty_new": "3703be3f-53b9-4824-a103-124834dedf41",
    "beauty_closed": "58b2d04d-f3f9-4e25-80e3-d9f5f6fe8c91",
    "laundry": "ddf60c52-d90c-4996-9dd3-2bd508347bad",
}
# file key -> (file as Step 0 named it, URL, the dataset page that carries
# it). The monthly resources' download names are a bare ".zip".
SOURCE_FILES = {
    # 営業許可施設一覧, 令和8年3月31日現在: fixed premises and vehicles, two CSVs
    "food": ("food_all_r7end.zip", _FOOD_DS + _RESOURCE["food"] + "/download/04.zip", FOOD_PAGE),
    # 新規廃業営業許可施設一覧（令和8年度）: April to August 2026, ten CSVs
    "food_months": ("food_newclosed_r8.zip", _FOOD_DS + _RESOURCE["food_months"] + "/download/.zip", FOOD_PAGE),
    "barber": ("barber_all_r7end.zip", _BARBER_DS + _RESOURCE["barber"] + "/download/09.zip", BARBER_PAGE),
    "barber_new": ("barber_new_r8.zip", _BARBER_DS + _RESOURCE["barber_new"] + "/download/.zip", BARBER_PAGE),
    "barber_closed": ("barber_closed_r8.zip", _BARBER_DS + _RESOURCE["barber_closed"] + "/download/.zip",
                      BARBER_PAGE),
    "beauty": ("beauty_all_r7end.zip", _BEAUTY_DS + _RESOURCE["beauty"] + "/download/06.zip", BEAUTY_PAGE),
    "beauty_new": ("beauty_new_r8.zip", _BEAUTY_DS + _RESOURCE["beauty_new"] + "/download/.zip", BEAUTY_PAGE),
    "beauty_closed": ("beauty_closed_r8.zip", _BEAUTY_DS + _RESOURCE["beauty_closed"] + "/download/.zip",
                      BEAUTY_PAGE),
    "laundry": ("laundry_all_r7end.zip", _LAUNDRY_DS + _RESOURCE["laundry"] + "/download/12.zip", LAUNDRY_PAGE),
}
SOURCE_RESOURCES = {k: (CKAN_API, rid) for k, rid in _RESOURCE.items()}
# The rebuilt registers' date, PINNED (Kyoto's rule: the last day the newest
# monthly file covers, never the download date or today): August 2026.
AS_OF = datetime.date(2026, 8, 31)
# The date each file states: 「令和8年3月31日現在」 on the year-end lists; the
# monthly zips run to 「令和8年8月31日」.
SOURCE_AS_OF = {"food": "2026-03-31", "food_months": "2026-08-31",
                "barber": "2026-03-31", "barber_new": "2026-08-31", "barber_closed": "2026-08-31",
                "beauty": "2026-03-31", "beauty_new": "2026-08-31", "beauty_closed": "2026-08-31",
                "laundry": "2026-03-31"}
FOOD_AS_OF = AS_OF.isoformat()
REGISTERS_AS_OF = AS_OF.isoformat()
# Calls 161 and 172 (owner, 2026-10-06): a permit's term is read against the
# last day its source covers, never today. The rebuild below already keeps
# only permits in term on AS_OF; step 2 reads the same date for a permit that
# starts after it.
TERM_AS_OF = {"food": AS_OF.isoformat()}

# What step 2 reads: the three rebuilt registers and the laundry register
# (source_rows). The monthly files are read inside the rebuilds only.
SOURCES = {"food": SOURCE_FILES["food"][0], "barber": SOURCE_FILES["barber"][0],
           "beauty": SOURCE_FILES["beauty"][0], "laundry": SOURCE_FILES["laundry"][0]}
# Declared, never inferred (japan_register.decode sniffs both): the year-end
# barber and beauty CSVs are UTF-8 with a BOM; the year-end food and laundry
# CSVs and every monthly CSV are cp932.
SOURCE_ENCODING = {"food": "cp932", "food_months": "cp932", "barber": "utf-8-sig", "barber_new": "cp932",
                   "barber_closed": "cp932", "beauty": "utf-8-sig", "beauty_new": "cp932",
                   "beauty_closed": "cp932", "laundry": "cp932"}
# The columns each file and source must carry; fetch_sources.py and step 2
# stop on a header without them. The operator columns (the food lists' 営業者名
# and 営業者代表者氏名; the registers' 開設者氏名 / 営業者氏名) are REQUIRED so the
# name rule (japan_register.name_is_operator; owner 2026-09-27) cannot
# silently compare nothing; read IN MEMORY by that rule only, never kept.
# Never read out of the files: 営業所電話番号, 施設電話番号, 営業者住所,
# 開設者住所, their 方書, 営業者電話番号, 開設者電話番号 and the 役職名 columns.
_FOOD = ("営業所所在地", "営業所名称", "営業の種類", "業態", "許可終了日", "許可指令番号", "営業者名",
         "営業者代表者氏名")
_SALON = ("施設名称", "施設所在地", "開設者名称", "開設者氏名")
_LAUNDRY = ("施設名称", "施設所在地", "種別", "営業者名称", "営業者氏名")
REQUIRED_COLUMNS = {
    "food": _FOOD, "food_months": (*_FOOD, "許可開始日", "廃業年月日"),
    "barber": _SALON, "barber_new": _SALON, "barber_closed": (*_SALON, "廃止届出年月日"),
    "beauty": _SALON, "beauty_new": _SALON, "beauty_closed": (*_SALON, "廃止届年月日"),
    "laundry": _LAUNDRY,
}
# The columns a rebuilt row carries on into step 2: the premises' own, the
# permit's dates and number, and the operator columns for the name rule.
_KEEP_FOOD = (*_FOOD, "許可年月日", "許可開始日")
# The registers name an operator in two columns: 開設者氏名 / 営業者氏名 (a
# company's representative; in japan_register.OPERATOR_COLS, compared) and
# 開設者名称 / 営業者名称, whose spelling the shared tuple does not hold.
# Recorded here as read and judged (japan_step2.check_new_city_columns): the
# column is filled only where the operator is a company (measured 2026-10-11
# on the rebuilt registers; see _companies_only, which STOPS the build on a
# value that reads as anything else), and a company's name is never withheld.
NOT_OPERATOR = {
    "開設者名称": "a company's name, filled only where the operator is a company (_companies_only stops otherwise)",
    "営業者名称": "a company's name, filled only where the operator is a company (_companies_only stops otherwise)",
}
# The food list publishes a premises' address and name only where its operator
# agreed (the list's own PDF: 「営業者が施設情報の非公開を希望した場合は…非公開と
# しています」): a row with neither is counted apart from "not a premises"
# (Kawasaki's page bullet; japan_step2).
ADDRESS_BY_CONSENT = {"food"}
# A monthly register file with nothing to report holds one row reading this.
NOTHING = "該当なし"


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _members(key):
    """(member name, rows) for each CSV member of a file's zip, a member with
    a premises address column first. The city's zips hold CSV and PDF;
    japan_register.city_rows reads XLSX members only, so the format is read
    here, with the shared decode (cp932 or UTF-8 with a BOM) and header
    cleaning (the food headers carry line breaks). Blank lines and unnamed
    trailing columns are dropped."""
    import csv
    import io
    import zipfile

    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    out = []
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            name = jr.zip_member_name(info)
            if not name.lower().endswith(".csv"):
                continue
            table = csv.reader(io.StringIO(jr.decode(zf.read(info))))
            head = [jr._head(c) for c in next(table)]
            rows = [{h: v for h, v in zip(head, r) if h} for r in table if any(c.strip() for c in r)]
            out.append((name, head, rows))
    if not out:
        raise SystemExit(f"{path.name}: no CSV member - not the file the brief read")
    out.sort(key=lambda m: "営業区域" in m[1])
    return [(name, rows) for name, _, rows in out]


def file_rows(key):
    """One fetched file's rows as it stands (japan_fetch's count and header
    check): every CSV member's rows, blank lines out."""
    return [r for _, rows in _members(key) for r in rows]


def _checked(key, rows, name):
    missing = [c for c in REQUIRED_COLUMNS[key] if rows and c not in rows[0]]
    if missing:
        raise SystemExit(f"{name}: header lacks {missing} - not the file the brief read")
    return rows


def _fixed_and_vehicles(key):
    """A food file's rows, split by what its member lists: fixed premises
    (営業所所在地) and vehicles (自動車による営業: 営業区域, no premises)."""
    fixed, vehicles = [], []
    for name, rows in _members(key):
        if rows and "営業区域" in rows[0]:
            vehicles += rows
        else:
            fixed += _checked(key, rows, name)
    return fixed, vehicles


def _number(r):
    return (r.get("許可指令番号") or "").strip()


def _rebuild_permits(base, months):
    """Sakai's rebuild for one kind of permit: the year-end rows and each
    month's new permits (廃業年月日 blank), less every permit number a monthly
    closure row names (廃業年月日 filled), kept while 許可終了日 is on or after
    AS_OF. Returns (rows in term, new, closure numbers, matched, past term)."""
    from pipeline.countries import japan_register as jr

    new = [r for r in months if not (r.get("廃業年月日") or "").strip()]
    closed = {_number(r) for r in months if (r.get("廃業年月日") or "").strip()} - {""}
    rows = base + new
    numbers = [_number(r) for r in rows]
    if "" in numbers or len(set(numbers)) != len(numbers):
        raise SystemExit("許可指令番号 is blank or repeats in the food lists: the rebuild keys on it "
                         "(unique on every row, 2026-10-11) - re-measure before trusting the closures")
    left = [r for r in rows if _number(r) not in closed]
    kept = list(jr.in_term(left, ("許可終了日",), AS_OF))
    return kept, len(new), len(closed), len(rows) - len(left), len(left) - len(kept)


def rebuilt_food():
    """The city's fixed food permits in force on AS_OF (2026-08-31). The
    vehicle permits (自動車による営業, their own CSVs, 営業区域 in place of an
    address) are rebuilt the same way and COUNTED only: a vehicle is not a
    premises, and it never reaches step 2. Do not use
    japan_register.rebuilt_register here: it keys on (address, trade name,
    type) and reads no closures, and the rows withheld at the operator's
    request carry neither address nor name (the brief: about 445 rows lost).
    Only _KEEP_FOOD is carried; the operator's address never leaves the file.

    Measured 2026-10-11: fixed 5,563 + 447 new - 442 matched closures (of 461
    closure numbers) = 5,568, 19 past 許可終了日 with no closure row, 5,549 in
    term; vehicles 592 in term."""
    from pipeline.baseline import emit

    base, base_v = _fixed_and_vehicles("food")
    months, months_v = _fixed_and_vehicles("food_months")
    kept, new, closed, matched, past = _rebuild_permits(base, months)
    print(f"  rebuilt food register on {AS_OF}: year-end {len(base):,} + new {new:,} - closed {matched:,} "
          f"(of {closed:,} closure numbers) = {len(base) + new - matched:,}; past 許可終了日 {past:,}; "
          f"in term {len(kept):,}")
    veh, vnew, vclosed, vmatched, vpast = _rebuild_permits(base_v, months_v)
    print(f"  vehicle permits (not premises, counted only): year-end {len(base_v):,} + new {vnew:,} - closed "
          f"{vmatched:,} (of {vclosed:,}) ; past term {vpast:,}; in term {len(veh):,}")

    def restaurants(rows):
        return sum(1 for r in rows if "飲食店" in (r.get("営業の種類") or "") or "喫茶店" in (r.get("営業の種類") or ""))

    print(f"  restaurant permits (飲食店営業, 喫茶店営業) in term: fixed {restaurants(kept):,} + vehicles "
          f"{restaurants(veh):,} = {restaurants(kept) + restaurants(veh):,}")
    emit("rebuilt_food_closed_matched", matched)
    emit("rebuilt_food_in_term", len(kept))
    emit("vehicle_permits_in_term", len(veh))
    emit("restaurant_permits_in_term", restaurants(kept) + restaurants(veh))
    return [{c: r.get(c) for c in _KEEP_FOOD} for r in kept]


def _premises(r):
    from pipeline.countries import japan_register as jr
    from pipeline.countries import japan_step2

    return (japan_step2.key_addr(r.get("施設所在地")), jr._name_key(r.get("施設名称")))


def _companies_only(key, rows, column):
    """Stop where a register's 名称 column (NOT_OPERATOR) holds a value with no
    company marker: the name rule does not compare that column, so it must
    never hold a person's own name."""
    from pipeline.countries import japan_register as jr

    odd = sum(1 for r in rows if (r.get(column) or "").strip() and not jr.NOT_A_PERSON.search(
        jr._name_key(r.get(column))))
    if odd:
        raise SystemExit(f"{key}: {odd} row(s) carry a {column} with no company marker - the name rule does not "
                         f"compare that column (config.NOT_OPERATOR). A parked call: add the spelling to "
                         f"japan_register.OPERATOR_COLS before this register is drawn.")


def rebuilt_salons(key):
    """A barber or beauty register on AS_OF: the year-end register and each
    month's new premises, less the premises each monthly closure row names,
    keyed on (address, trade name) since the rows carry no number. ONE row
    goes per closure row, the one inspected (検査確認日) earliest: a salon
    that changes hands is a new row and, later, the old operator's closure
    under the same address and name (one beauty salon, new 2026-06-23, closure
    2026-07-13), and the new registration stays. A month with nothing to
    report holds one 該当なし row, skipped.

    Measured 2026-10-11: barbers 468 + 2 new - 0 = 470; beauty salons 1,082 +
    11 new - 8 = 1,085 rows (1,081 distinct premises: four year-end premises
    are listed twice)."""
    import datetime

    from pipeline.baseline import emit
    from pipeline.countries import japan_register as jr

    def rows_of(k):
        return [r for name, rows in _members(k) for r in _checked(k, rows, name)
                if NOTHING not in (r.get("施設名称") or "") and NOTHING not in (r.get("施設所在地") or "")]

    base, new, closed = rows_of(key), rows_of(f"{key}_new"), rows_of(f"{key}_closed")
    rows = base + new
    by_premises = {}
    for i, r in enumerate(rows):
        by_premises.setdefault(_premises(r), []).append(i)
    gone = set()
    for c in closed:
        left = [i for i in by_premises.get(_premises(c), ()) if i not in gone]
        if left:
            gone.add(min(left, key=lambda i: jr.wareki_date(rows[i].get("検査確認日")) or datetime.date.min))
    kept = [r for i, r in enumerate(rows) if i not in gone]
    print(f"  rebuilt {key} register on {AS_OF}: year-end {len(base):,} + new {len(new):,} - closed "
          f"{len(gone):,} (of {len(closed):,} closure rows) = {len(kept):,}")
    emit(f"rebuilt_{key}_closed_matched", len(gone))
    emit(f"rebuilt_{key}", len(kept))
    _companies_only(key, kept, "開設者名称")
    return [{c: r.get(c) for c in _SALON} for r in kept]


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    "food" is the rebuilt fixed-premises register, "barber" and "beauty" their
    rebuilt registers, "laundry" the year-end register as it stands. Only the
    columns named above are carried."""
    if key == "food":
        return rebuilt_food()
    if key in ("barber", "beauty"):
        return rebuilt_salons(key)
    rows = [r for name, rs in _members(key) for r in _checked(key, rs, name)]
    _companies_only(key, rows, "営業者名称")
    return [{c: r.get(c) for c in _LAUNDRY} for r in rows]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), one pair per ward
# (14151-14153).
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Sagamihara.
# S, W, N, E: the city's N03 extent (S 35.475, W 139.066, N 35.673, E 139.458)
# rounded out; step 1 stops if the city leaves it. The box the OSM query used
# (2026-10-11, 78 objects).
OSM_BBOX = (35.47, 139.06, 35.68, 139.46)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Tokyo's signage style (owner 2026-09-28: no macrons).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 54N: the whole N03 extent (139.066 to 139.458) falls in the 138 to
# 144 band. Derived per city, not copied - see docs/project_context.md's CRS
# lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: step 1's
# median gap to the nearest station is 1,452 m (16 stations, the closest pair
# 975 m, 2026-10-11), over the 550 m that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 6 lines, 19 station records, 16 station groups; no Shinkansen
# station), each cut at the city line (owner 2026-09-24): JR East's Sagami
# Line 7 of 18 (橋本 to 相武台下) and Yokohama Line 5 of 20 (橋本 to 古淵); and
# four lines cut short, all DRAWN as cut. The Chuo Line 2 of 75 (相模湖, 藤野,
# the city's far west, about 15 km from 橋本), the Odakyu Odawara Line 2 of 47
# (相模大野, 小田急相模原) and the Odakyu Enoshima Line 2 of 17 (相模大野,
# 東林間): owner, 2026-10-05, on Kawasaki's and Higashiosaka's precedent. The
# Keio Sagamihara Line 1 of 12 (橋本, its terminus): a one-station stub stays
# as cut (owner 2026-09-27); 橋本 is one N02 group with JR's two lines.
# 相模大野 is one group for both Odakyu lines. No frequency floor (owner,
# 2026-10-06, calls 46 and 86).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# The lines run on into Tokyo (Machida, Hachioji) and Yamanashi (Uenohara) as
# well as Kanagawa: their N03 names the stations beyond the city line
# (japan_step1.n03_municipalities; Kawasaki's shape).
N03_NEIGHBOR_PREFS = ("13", "19")

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names without macrons, each as the
# other maps that draw the line spell it: Yokohama's JR Yokohama Line, Hino's
# and Tachikawa's JR Chuo Line (the same N02 line, 東日本旅客鉄道 中央線; west of
# 高尾 the operator calls this stretch the Chuo Main Line, 中央本線), Tokyo's
# and Kawasaki's Odakyu Odawara Line, Chofu's, Tama's and Kawasaki's Keio
# Sagamihara Line.
_JR, _OQ, _KO = "東日本旅客鉄道", "小田急電鉄", "京王電鉄"
LINES = {
    "JS": {"n02": [(_JR, "相模線")], "name": "JR Sagami Line", "name_ja": "相模線", "short": "JR",
           "hue": "#009793"},
    "JH": {"n02": [(_JR, "横浜線")], "name": "JR Yokohama Line", "name_ja": "横浜線", "short": "JR",
           "hue": "#7AC143"},
    "JC": {"n02": [(_JR, "中央線")], "name": "JR Chuo Line", "name_ja": "中央線", "short": "JR",
           "hue": "#F15A22"},
    "OH": {"n02": [(_OQ, "小田原線")], "name": "Odakyu Odawara Line", "name_ja": "小田原線", "short": "Odakyu",
           "hue": "#2288CC"},
    "OE": {"n02": [(_OQ, "江ノ島線")], "name": "Odakyu Enoshima Line", "name_ja": "江ノ島線", "short": "Odakyu",
           "hue": "#2288CC"},
    "KS": {"n02": [(_KO, "相模原線")], "name": "Keio Sagamihara Line", "name_ja": "京王相模原線", "short": "Keio",
           "hue": "#DD0077"},
}
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own: the Chuo, Odakyu
# Odawara and Keio Sagamihara lines. The JR Yokohama Line is Yokohama's map's
# too and had no registry entry on 2026-10-11: it takes Yokohama's #68A008
# (pipeline/yokohama/config.py, "JH") until the entry exists, then reads it
# from the registry.
# The Sagami and Odakyu Enoshima lines are new to the site: the project's
# own colours by scripts/line_colour_search.py's method with the four shared
# lines held (2026-10-11): each the feasible colour nearest its operator's hue
# that reads 3:1 on both map pages and clears CIE76 45 from every pin
# (#737a00, #C2185B, #1baf7a), 18 from each line within 500 m and
# linecolour.HARD_FLOOR from the rest. Measured, nearest pin / nearest line:
# Sagami 45.2 / 22.3, Yokohama 26.3 / 80.2, Chuo 54.7 / 91.5, Odawara 56.4 /
# 22.3, Enoshima 77.9 / 34.8, Keio Sagamihara 45.2 / 91.2. Closest pair 22.3
# (the Sagami and Odawara lines, within 500 m of each other); the dark-mode
# labels separate, 6 of 6. The Yokohama Line's 26.3 from olive Food shops sits
# between the owner's floor of 20 and the aim of 45: an accepted trade for one
# colour on both maps (owner, 2026-10-07).
_COLOURS = {
    "JS": "#008090",
    "JH": line_registry.colour("jr-east-yokohama-line"),
    "JC": line_registry.colour("jr-east-chuo-line"),
    "OH": line_registry.colour("odakyu-odawara-line"),
    "OE": line_registry.colour("odakyu-enoshima-line"),
    "KS": line_registry.colour("keio-sagamihara-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own station lists, read against the city line
# (2026-10-11). JR East's line timetables list the Sagami Line's 18 stations
# (相武台下 to 橋本 inside, 7), the Yokohama Line's 20 (古淵 to 橋本, 5) and the
# Chuo Line's 相模湖 and 藤野 between 高尾 and 上野原 (2); Odakyu's station list
# the Odawara Line's 47 (相模大野, 小田急相模原 between 町田 and 相武台前) and the
# Enoshima Line's 相模大野 and 東林間 before 中央林間; Keio's the Sagamihara
# Line's 12 to its terminus, 橋本. The thinnest stations by JR East's weekday
# timetables (read the same day): 番田 61 departures each way (Sagami Line),
# 相模湖 49 each way (Chuo Line).
GATE3 = {"source": "JR East's line timetables (timetables.jreast.co.jp), Odakyu's station list "
                   "(odakyu.jp/station/) and Keio's (keio.co.jp/train/station/), read against the city line: "
                   "Sagami Line 7, Yokohama Line 5, Chuo Line 2, Odawara Line 2, Enoshima Line 2, "
                   "Sagamihara Line 1",
         "lines": {"JS": 7, "JH": 5, "JC": 2, "OH": 2, "OE": 2, "KS": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
SAGAMIHARA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = SAGAMIHARA_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602689481)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "グリーンパーク前": "a signed junction (highway=traffic_signals) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/sagamihara.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A bare type word (owner, 2026-10-13)
    "way/591113947": "'こども広場': こども広場 (children's plaza), a type phrase with no name",
    "way/283545769": "'スポーツ 広場': スポーツ 広場 (sports ground), a type phrase with no name",
    "way/891179023": "'イベント広場': イベント広場 (event plaza), a type phrase with no name",
    "way/1423590805": "'自主管理広場': 自主管理広場 (self-managed plaza): the planning term for an open space a development's owner must keep, not a name",
    "way/1424310151": "'自主管理広場': 自主管理広場: same planning term",
    "way/1425728141": "'自主管理広場': 自主管理広場: same planning term",
    "node/4841144424": "'道祖神': 道祖神 (roadside guardian stone), the kind of object, with the alternative name 'god'",
    # A description standing in for a name (owner, 2026-10-13)
    "node/3787184062": "'お祈りスペース': お祈りスペース (prayer space): a room's label, tagged a place of worship with no religion",
    # A stock plaza name with no place in it (ruling 5; owner, 2026-10-13)
    "way/1472195055": "'水の広場': unsure in the full read, dropped by the owner's ruling 5",
    # A religious body's hall or branch tagged a place of worship (ruling 2; owner, 2026-10-13)
    "node/1371772863": "'創価学会 相模原文化会館': unsure in the full read, dropped by the owner's ruling 2",
    "node/1451303273": "'宗教真光 相模原小修験道場': unsure in the full read, dropped by the owner's ruling 2",
}
