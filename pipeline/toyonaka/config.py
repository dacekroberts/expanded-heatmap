"""Toyonaka-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/toyonaka.md.
Japan A/B batch (Kansai-1, 2026-10-07), on the shared modules
(pipeline/countries/japan*.py) and the Japan foundation's rules (ALL_RULES).

Business leg: the city's two BODIK datasets in the Digital Agency's national
schema (CC BY 4.0). Food: 食品等営業許可一覧（豊中市）, the full list of
permits in term on 2026-03-31 plus the monthly new and closed lists of
April to August 2026, REBUILT BY PERMIT NUMBER (the city files a renewal as
a closure of the old number and a new permit under a new number, so the
closures must be applied by number; Maebashi's and Sakai's method) and kept
while 許可満了日 is on or after the pinned AS_OF. Personal services: the
生活衛生営業施設一覧, one file of six trades, rebuilt to the same date by
number with its 2026 monthly new and closed lists (owner, call 151), split by
業種 into barbers, beauty salons and laundries (lodging, public baths and
興行場 out). Food
shops also from MHLW's notifications (partial, opt-in; call 127b's precedent),
MHLW's own point where the block join misses. All placed by a JOIN to MLIT's
位置参照情報 for the one municipality (27203, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Hankyu's Takarazuka Line, the Osaka Monorail and Kita-Osaka Kyuko,
cut at the city line. English station names from OpenStreetMap's name:en.
"""

import datetime
from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "toyonaka" / "raw"
DATA_PROCESSED = ROOT / "data" / "toyonaka" / "processed"
OUTPUTS = ROOT / "outputs" / "toyonaka"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Toyonaka"
SLUG = "toyonaka"
MUNICIPALITY = "豊中市"
PREFECTURE = "大阪府"

# BODIK (data.bodik.jp), organisation 豊中市 (272035): both datasets record
# license_id cc-by-40-intl. MHLW 食品衛生申請等システム open data, PDL 1.0
# (the system's site terms §2; read 2026-09-24 for Fukuoka). Credit links
# the MHLW top page only.
FOOD_DATASET = "https://data.bodik.jp/dataset/272035_food_business"
SANITATION_DATASET = "https://data.bodik.jp/dataset/272035_sanitation_business"
_FOOD_RES = "https://data.bodik.jp/dataset/2d6870cc-3db8-4069-841e-2a6deeb173b4/resource/"
_SAN_RES = "https://data.bodik.jp/dataset/7e383a56-704b-4c18-ae8c-f30e7e086a60/resource/"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
# The months read: April to August 2026, each a new-permit and a closure file
# (the months to 2026-03 are already in the full list, the brief: 645 of their
# 657 new permits by number, none of their closures). (month, last day, new
# resource id, closed resource id), from BODIK's package_show.
MONTHS = (
    ("04", "30", "2fe5fd7a-8902-4e75-b48c-d6469a55ed35", "d3d81645-2207-493a-824b-997f7e4a2ce3"),
    ("05", "31", "02e098c4-7f15-45ac-b5b8-640beb85bdb5", "b41a1578-de22-46b6-a9c4-6e5e81f6b180"),
    ("06", "30", "017da634-6bee-4a96-9989-0eeec0b8d75c", "4cac30b0-1c22-463f-a890-a555df8a5752"),
    ("07", "31", "84cba3fc-d186-4933-b2c6-443736fadd6b", "f3bc9d3c-e52f-4256-a4cb-611485ce55b3"),
    ("08", "31", "a11ef3d9-9cd0-407e-a24b-c43c2c31d2b4", "c822c52e-f618-4555-8073-1c3d6e51978e"),
)


# The 生活衛生 register's monthly files of 2026 (owner, call 151): (kind, month,
# file, resource id, last day), from BODIK's package_show (2026-10-07). The
# publisher names them irregularly; no new-premises file for January or March.
SAN_MONTHS = (
    ("closed", "01", "272035_sanitiation_business_closed_202601.csv", "d69158dd-7036-46c3-b6e7-ee7e79cb8b4e",
     "2026-01-31"),
    ("new", "02", "272035_sanitiation_business_new_20260201-0228.csv", "8938efa2-4da8-4055-a269-a94e14069b58",
     "2026-02-28"),
    ("closed", "02", "272035_sanitiation_business_closed_20260201-0228.csv",
     "822feacb-21c3-4342-a79c-c4538b9ba810", "2026-02-28"),
    ("closed", "03", "272035_sanitiation_business_closed_20260301-0331.csv",
     "69af5c4b-b6b3-449e-9cf7-1b237162d6e4", "2026-03-31"),
    ("new", "04", "272035_sanitiation_business_new_20260401-0430.csv", "1b79ba85-5c37-4677-beec-84f700e4915d",
     "2026-04-30"),
    ("closed", "04", "272035_sanitiation_business_closed_20260401-0430.csv",
     "ddc1151c-6820-48a5-8dd0-4a77130fa1a9", "2026-04-30"),
    ("new", "05", "272035_sanitiation_business_new_20260501-0531.csv", "4171ce76-8ef1-4055-bc71-c5c4772ccbbf",
     "2026-05-31"),
    ("closed", "05", "272035_sanitiation_business_closed_20260501-0531.csv",
     "b31a36aa-a6bb-44d3-9f74-9755886ef5e4", "2026-05-31"),
    ("new", "06", "272035_sanitiation_business_new_20260601-0630.csv", "4bb4c552-235c-406c-8083-1518404aca05",
     "2026-06-30"),
    ("closed", "06", "272035_sanitiation_business_closed_20260601-0630.csv",
     "e6382442-d258-424f-9432-bbe048838a54", "2026-06-30"),
    ("new", "07", "272035_sanitiation_business_new_20260701-0731.csv", "775b8c4d-9171-4e5f-bea8-551b50e1c575",
     "2026-07-31"),
    ("closed", "07", "272035_sanitiation_business_closed_20260701-0731.csv",
     "b617e0fa-7cec-4cf4-af77-6ded991149ad", "2026-07-31"),
    ("new", "08", "272035_sanitiation_business_new_20260801-0831.csv", "10df5778-485e-4e01-85c2-83c9a3be585e",
     "2026-08-31"),
    ("closed", "08", "272035_sanitiation_business_closed_20260801-0831.csv",
     "9dd22fd5-7e3a-411f-8333-04d7acb2f667", "2026-08-31"),
)


def _month_file(kind, m, end):
    return f"272035_food_business_{kind}_2026{m}01_2026{m}{end}.csv"


SOURCE_FILES = {
    # 全許可施設一覧: every permit in term on 2026-03-31 (uploaded 2026-05-29)
    "food": ("272035_food_business_all.csv",
             _FOOD_RES + "74c6e0d8-9fde-4503-8090-bada26639ae3/download/272035_food_business_all.csv",
             FOOD_DATASET),
    **{f"new_{m}": (_month_file("new", m, end), f"{_FOOD_RES}{rn}/download/{_month_file('new', m, end)}",
                    FOOD_DATASET) for m, end, rn, _ in MONTHS},
    **{f"closed_{m}": (_month_file("closed", m, end), f"{_FOOD_RES}{rc}/download/{_month_file('closed', m, end)}",
                       FOOD_DATASET) for m, end, _, rc in MONTHS},
    # 全施設一覧: six trades in one file (the publisher's spelling "sanitiation")
    "sanitation": ("272035_sanitiation_business.csv",
                   _SAN_RES + "849e744a-452b-4230-a783-07e1b8a11240/download/272035_sanitiation_business.csv",
                   SANITATION_DATASET),
    **{f"san_{kind}_{m}": (name, f"{_SAN_RES}{rid}/download/{name}", SANITATION_DATASET)
       for kind, m, name, rid, _ in SAN_MONTHS},
    "mhlw": ("27203_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27203_food_business_all.csv",
             MHLW_TOP),
}
# The rebuilt register's date, PINNED (Kyoto's rule: the last day the newest
# file covers, never the download date or today): the August files.
AS_OF = datetime.date(2026, 8, 31)
# The sanitation register (uploaded 2026-01-08, its latest 許可（登録）日
# 2025-12-04, no 2025-12 monthly file) rebuilt to the same date as the food
# list with its 2026 monthly files (owner, call 151).
SANITATION_BASE_AS_OF = "2025-12-31"
SANITATION_AS_OF = AS_OF.isoformat()
SOURCE_AS_OF = {"food": "2026-03-31", "sanitation": SANITATION_BASE_AS_OF, "mhlw": None,
                **{k: SANITATION_AS_OF for k in ("barber", "beauty", "laundry")},
                **{f"san_{kind}_{m}": end for kind, m, _, _, end in SAN_MONTHS},
                **{f"new_{m}": f"2026-{m}-{end}" for m, end, _, _ in MONTHS},
                **{f"closed_{m}": f"2026-{m}-{end}" for m, end, _, _ in MONTHS}}
FOOD_AS_OF = AS_OF.isoformat()
# The permit term rules (calls 161 and 172) read the food rows against this
# date, never today.
TERM_AS_OF = {"food": AS_OF.isoformat()}
# What step 2 reads: the rebuilt register, the three trades of the sanitation
# file and MHLW's notifications. The monthly files are read inside the rebuild.
SOURCES = {"food": SOURCE_FILES["food"][0], "barber": SOURCE_FILES["sanitation"][0],
           "beauty": SOURCE_FILES["sanitation"][0], "laundry": SOURCE_FILES["sanitation"][0],
           "mhlw": SOURCE_FILES["mhlw"][0]}
# Declared, never inferred: every BODIK file is UTF-8 without a BOM; MHLW's is
# UTF-8 with a BOM.
SOURCE_ENCODING = {**{k: "utf-8" for k in SOURCE_FILES}, "mhlw": "utf-8-sig"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. 法人名 (the national schema's operator, a company or a
# sole trader) and the register's 申請者氏名 and 法人代表者氏名 are REQUIRED so
# the name rule (japan_register.name_is_operator) cannot silently compare
# nothing; they are read IN MEMORY by that rule only, never kept. Never
# selected: 施設ＴＥＬ, 法人所在地 (a company's own address), and MHLW's
# 法人番号 / 法人住所 / phones.
_FOOD = ("施設名称", "営業の種類", "所在地_連結表記", "法人名", "許可番号", "許可年月日", "許可満了日",
         "廃業年月日")
REQUIRED_COLUMNS = {
    "food": _FOOD,
    # The new-permit files from June 2026 drop the empty 廃業年月日 column.
    **{f"new_{m}": _FOOD[:-1] for m, _, _, _ in MONTHS},
    **{f"closed_{m}": ("許可番号", "許可年月日", "廃業年月日") for m, _, _, _ in MONTHS},
    "sanitation": ("業種", "施設名称", "施設住所", "申請者氏名", "法人代表者氏名"),
    **{k: ("業種", "施設名称", "施設住所", "申請者氏名", "法人代表者氏名") for k in ("barber", "beauty", "laundry")},
    **{f"san_new_{m}": ("業種", "許可（登録）番号", "施設名称", "施設住所", "申請者氏名", "法人代表者氏名")
       for kind, m, _, _, _ in SAN_MONTHS if kind == "new"},
    **{f"san_closed_{m}": ("業種", "許可（登録）番号", "廃業日") for kind, m, _, _, _ in SAN_MONTHS if kind == "closed"},
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
}
# The columns a rebuilt food row carries into step 2: the premises' own, the
# dates the term rules read, and 法人名 for the name rule (in memory).
_KEEP_FOOD = ("施設名称", "営業の種類", "所在地_連結表記", "法人名", "許可番号", "許可年月日", "許可開始日",
              "許可満了日", "廃業年月日")
# The register's three trades in scope, by 業種 (the brief: barbers 237,
# beauty 736, laundries 231); 旅館業 (lodging), 公衆浴場 (public baths) and
# 興行場 (cinemas and theatres) are out (docs/category_rules.md; baths on the
# precedent that no built Japanese city carries them).
TRADES = {"barber": ("理容所",), "beauty": ("美容所",), "laundry": ("クリーニング業",)}
_KEEP_SAN = ("業種", "施設名称", "施設住所", "申請者氏名", "法人代表者氏名")
# MHLW publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# MHLW's notification rows the block join misses take MHLW's own point (the
# brief: a median 36 m from the block point, 98.2% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# A premises in both, in one bucket (a shop holding a city permit and filing
# an MHLW notification): MHLW's row stays, as in Matsuyama and Sakai.
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES[key][0]


def _read(key, keep):
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    for r in jr.city_rows(path):
        missing = [c for c in REQUIRED_COLUMNS[key] if c not in r]
        if missing:
            raise SystemExit(f"{path.name}: header lacks {missing} - not the file the brief read")
        yield {c: r.get(c) for c in keep}


def _number(r):
    return (r.get("許可番号") or "").strip()


def rebuilt_register():
    """The city's food permits in term on AS_OF, rebuilt BY PERMIT NUMBER: the
    full list (2026-03-31), then each month's new permits (a number seen again
    replaces the earlier row), less every permit a monthly closure file names
    by number where the closure falls on or after that permit's grant (so a
    permit re-granted under its old number after a closure stands), kept while
    許可満了日 is on or after AS_OF. The full list's 51 empty lines carry no
    number and are dropped. Only premises columns and the name rule's operator
    column are carried; no contact column leaves the file."""
    import sys

    from pipeline.baseline import emit
    from pipeline.countries import japan_register as jr

    by_number = {}
    base = [r for r in _read("food", _KEEP_FOOD) if _number(r)]
    for r in base:
        by_number[_number(r)] = r
    new = [r for m, _, _, _ in MONTHS for r in _read(f"new_{m}", _KEEP_FOOD) if _number(r)]
    for r in new:
        by_number[_number(r)] = r
    closures = {}
    for m, _, _, _ in MONTHS:
        for r in _read(f"closed_{m}", ("許可番号", "許可年月日", "廃業年月日")):
            if _number(r):
                closures[_number(r)] = jr.wareki_date(r.get("廃業年月日") or "")
    gone = []
    for n, closed_on in closures.items():
        r = by_number.get(n)
        granted = jr.wareki_date(r.get("許可年月日") or "") if r else None
        if r is not None and (closed_on is None or granted is None or granted <= closed_on):
            gone.append(by_number.pop(n))
    rows = list(by_number.values())
    kept = list(jr.in_term(rows, ("許可満了日",), AS_OF))
    print(f"  rebuilt register on {AS_OF}: full list {len(base):,} + new {len(new):,} "
          f"= {len(base) + len(new):,} rows, {len(rows) + len(gone):,} numbers; closed {len(gone):,} "
          f"(of {len(closures):,} closure numbers); past 許可満了日 {len(rows) - len(kept):,}; "
          f"in term {len(kept):,}", file=sys.stdout)
    emit("rebuilt_closed_matched", len(gone))
    emit("rebuilt_in_term", len(kept))
    return kept


_SAN_NUMBER = "許可（登録）番号"


def sanitation_register():
    """The 生活衛生 register rebuilt to AS_OF BY NUMBER (owner, call 151;
    Maebashi's 整理番号 rebuild): the register of the end of 2025, plus each
    2026 month's new premises, less every premises a monthly closure file names
    by 許可（登録）番号 (unique, never blank). Measured 2026-10-07: 1,255 + 17
    new - 90 closed = 1,182 rows, every closure matching a register number and
    no new number already in it. Only premises columns and the name rule's
    operator columns (in memory) are carried."""
    import sys

    from pipeline.baseline import emit

    keep = _KEEP_SAN + (_SAN_NUMBER,)
    rows = {(r.get(_SAN_NUMBER) or "").strip(): r for r in _read("sanitation", keep)}
    base = len(rows)
    new = [r for kind, m, _, _, _ in SAN_MONTHS if kind == "new" for r in _read(f"san_new_{m}", keep)]
    for r in new:
        rows[(r.get(_SAN_NUMBER) or "").strip()] = r
    closed = {(r.get(_SAN_NUMBER) or "").strip() for kind, m, _, _, _ in SAN_MONTHS if kind == "closed"
              for r in _read(f"san_closed_{m}", (_SAN_NUMBER,))}
    gone = [n for n in closed if n in rows]
    for n in gone:
        del rows[n]
    print(f"  生活衛生 register on {AS_OF}: {base:,} + new {len(new):,} - closed {len(gone):,} "
          f"(of {len(closed):,} closure numbers) = {len(rows):,}", file=sys.stdout)
    emit("san_register_closed", len(gone))
    emit("san_register_rows", len(rows))
    return list(rows.values())


def _trade(kind, row):
    """The sanitation row as `kind` reads it, or None. A laundry row's type
    is the kind in its brackets (取次のみ, ドライ, ランドリー, リネンサプライ), so
    japan_eigyo's linen rule (a type that starts with リネン) takes linen supply
    out (Osaka's 2026-09-27 precedent); a bare クリーニング業 stays as written."""
    import unicodedata

    t = unicodedata.normalize("NFKC", (row.get("業種") or "").strip())
    if not t.startswith(TRADES[kind]):
        return None
    if kind == "laundry":
        inner = t[len("クリーニング業"):].strip("()")
        row = {**row, "業種": inner or t}
    return row


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it):
    "food" is the register rebuilt by number; "barber", "beauty" and "laundry"
    are the sanitation file's three trades; "mhlw" is MHLW's file, its
    notifications only (申請区分 届出 / 届出(廃業)), since the city's list holds
    every permit (3,515 restaurants on 2026-03-31, 99.8% of the official
    count; MHLW's 67 permits are out, call 126)."""
    from pipeline.countries import japan_register as jr

    if key == "food":
        yield from rebuilt_register()
        return
    if key in TRADES:
        for r in sanitation_register():
            t = _trade(key, r)
            if t is not None:
                yield t
        return
    if key == "mhlw":
        path = source_csv("mhlw")
        if not path.exists():
            raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
        for r in jr.city_rows(path):
            if (r.get("申請区分") or "").startswith("届出"):
                yield r
        return
    raise KeyError(key)


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 27203.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Toyonaka.
# S, W, N, E: the city's N03 extent (S 34.731, W 135.441, N 34.825, E 135.508)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.72, 135.43, 34.83, 135.52)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae,
# lowercase after a hyphen for a common word (2026-10-07: 45 objects, every
# one with name:en). The other 6 are OSM's as they stand.
OSM_NAME_EN_OVERRIDES = {
    "緑地公園": "Ryokuchi-koen",                     # Ryokuchi-kōen
    "千里中央": "Senri-Chuo",                        # Senri-Chūō
    "柴原阪大前": "Shibahara-handai-mae",            # Shibahara-Handai-Mae
    "庄内": "Shonai",                                # Shōnai
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the longitude (~135.47) falls in the 132 to 138 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-group gap is 1,085 m.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25, the
# brief: 3 lines, no Shinkansen): Hankyu's 宝塚線 (6 of 19), the Osaka
# Monorail (4 of 14) and Kita-Osaka Kyuko's 南北線 (2 of 6), cut at the city
# line (owner 2026-09-24). No line is cut to one station.
LEFT_OUT_LINES = {}
# The Hankyu Takarazuka Line and the Monorail run on into Hyōgo (Ikeda's
# neighbour Kawanishi; Itami's airport): its N03 names the stations beyond the
# prefecture line (japan_step1.n03_municipalities).
N03_NEIGHBOR_PREFS = ("28",)
# 千里中央: N02 files Kita-Osaka Kyuko's and the Monorail's platforms as two
# groups 257 m apart; it is one interchange by name and by passage
# (Kawasaki's 武蔵小杉, 377 m, and Tokyo's precedents), so GROUP_JOIN joins the
# Monorail's to Kita-Osaka Kyuko's (staging, 2026-10-06, precedent applied).
GROUP_JOIN = {("大阪モノレール", "大阪モノレール線", "千里中央"): "one Senri-Chuo, 257 m (the Monorail platform)"}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour.
_HK, _MO, _KK = "阪急電鉄", "大阪モノレール", "北大阪急行電鉄"
LINES = {
    "HT": {"n02": [(_HK, "宝塚線")], "name": "Hankyu Takarazuka Line", "name_ja": "阪急宝塚線", "short": "Hankyu",
           "hue": "#B7572D"},
    "MO": {"n02": [(_MO, "大阪モノレール線")], "name": "Osaka Monorail Main Line", "name_ja": "大阪モノレール本線",
           "short": "Monorail", "hue": "#0067B0"},
    "KK": {"n02": [(_KK, "南北線")], "name": "Kita-Osaka Kyuko Namboku Line", "name_ja": "北大阪急行南北線",
           "short": "Kita-Kyu", "hue": "#E4151E"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# toyonaka` (2026-10-07, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its start (the Hankyu Takarazuka Line from
# Osaka's colour, the others from the operators' hues) that reads 3:1 on both
# map pages and clears CIE76 45 from every pin. Closest pair within 500 m
# 82.0 (Hankyu and the Monorail, at 蛍池), anywhere 39.1; the dark-mode labels
# separate, 3 of 3.
_COLOURS = {"HT": "#C06038", "MO": "#007890", "KK": "#E81820"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: no line lies wholly inside the city; step 1 lists each line's
# in-city stations.
GATE3 = {"source": "no line wholly inside the city", "lines": {}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
TOYONAKA_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = TOYONAKA_BBOX
