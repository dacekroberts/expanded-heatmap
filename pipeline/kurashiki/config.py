"""Kurashiki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/kurashiki.md (11/11 checks, 2026-10-11). Part of the A/B
build plan's Regional-2 batch, on the shared modules
(pipeline/countries/japan*.py) with every shared rule on. Food only (Band B,
owner 2026-10-08, call 226): the city's barber and beauty lists are PDFs
under the site's all-rights-reserved terms (call 225) and no laundry list
exists.

Business leg: the city's own year-end list of food-business permits in force,
令和7年度末 (as of 2026-03-31; page 1004977, CC BY 4.0), ONE 243-page PDF and
nothing else (owner, calls 227 and 228: no monthly new-permit files, no MHLW
rows). The PDF is turned into text by pdftotext -table in fetch_sources.py and
read here as rows (source_rows; Kyoto's and Maebashi's hook). The list holds
old-law permits still in term beside the revised law's; where a permit number
carries one row of each, the old-law row goes (owner, call 229). Closures
after 2026-03-31 are not published, so the list is an UPPER BOUND on its date
(Shizuoka's and Kyoto's shape). Everything placed by a JOIN to MLIT's
位置参照情報 (one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), the Shinkansen left out, stations kept
only inside the city line (N03). The Mizushima Rinkai Railway's Mizushima Main
Line, JR West's Sanyo, Seto-Ohashi, Hakubi and Uno Minato lines and the Ibara
Railway's Ibara Line. English station names from OpenStreetMap's name:en.
"""

import datetime
import re
from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kurashiki" / "raw"
DATA_PROCESSED = ROOT / "data" / "kurashiki" / "processed"
OUTPUTS = ROOT / "outputs" / "kurashiki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kurashiki"
SLUG = "kurashiki"
MUNICIPALITY = "倉敷市"
PREFECTURE = "岡山県"

# The city's own site (no catalogue API); the file is a plain GET. Page
# 1004977 carries the CC BY 4.0 mark for its body content, the attachment
# included, and asks for the source and a statement that the data was
# processed. Read 2026-10-08 (licence-read): permitted with conditions, no
# prescribed wording, no indemnity clause (DECISIONS.md, "Kurashiki to B and
# to Regional-2").
_HOST = "https://www.city.kurashiki.okayama.jp"
FOOD_PAGE = _HOST + "/business/health-safety/1004966/1004974/1004977.html"
# source key -> (file, URL of the edition this build read, the page that
# carries its licence). One file: 令和7年度末 食品営業許可一覧, 8,034,340 B, 243
# pages, downloaded 2026-10-08 (owner, call 224) and kept under a dated name.
# The page replaces it each 15 April with the next year-end list under a new
# name; a refresh reads the page for it and re-measures everything below.
SOURCE_FILES = {
    "food": ("r07nenndinatu_2026-03-31.pdf",
             _HOST + "/_res/projects/default_project/_page_/001/004/977/r07nenndinatu.pdf", FOOD_PAGE),
}
# The PDF's text, made by fetch_sources.py and read by source_rows. It holds
# everything the PDF does (the operator column and two phone columns
# included), so it stays in data/kurashiki/raw/ and is never committed.
PDF_TEXT = DATA_RAW / "r07nenndinatu_2026-03-31.table.txt"
# xpdf's pdftotext (4.06 on the build machine). -table keeps each record on
# one line with every page's columns aligned under its header; -layout splits
# a row's dates from its type and -raw breaks some records over two lines
# (the brief, 2026-10-08).
PDFTOTEXT_ARGS = ("-table", "-enc", "UTF-8")
# Kyoto's rule: the date the list states, never the download's. Every page is
# titled 「令和８年３月３１日現在　食品営業許可一覧」.
FOOD_AS_OF = "2026-03-31"
SOURCE_AS_OF = {"food": FOOD_AS_OF}
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its file covers, never today. Every 有効期限 is on or after
# 2026-03-31 (244 rows end that day) and no permit is granted after it, so the
# rule drops nothing here (measured 2026-10-11).
TERM_AS_OF = {"food": FOOD_AS_OF}

SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The columns source_rows hands to step 2, by the PDF's own header names;
# fetch_sources.py and step 2 stop on a row without them. The operator column
# (営業者氏名: a company on about half the rows, a person's own name on the
# rest) is REQUIRED so the name rule (japan_register.name_is_operator; owner
# 2026-09-27) cannot silently compare nothing; it is read IN MEMORY by that
# rule only, never kept. Never handed on: 営業者法人電話番号 and 営業所電話番号.
REQUIRED_COLUMNS = {
    "food": ("営業者氏名", "営業所所在地", "営業所名称", "業種", "形態", "許可年月日", "有効期限", "初回許可年月日",
             "許可番号"),
}

# --- The PDF's text as rows -------------------------------------------------
# Each page of the text: a title line, a header line naming the 11 columns,
# then one line a record. The header's character offsets are the columns'
# (measured 2026-10-11: on all 6,288 records the address starts exactly at
# its header's offset). A record is read from both ends: the operator cell,
# the operator's phone cell and the address by offset; the three dates and
# the permit number from the right by pattern; then, between the trade name's
# offset and the dates, the form (where the row has one), the type and the
# premises' phone, each a whole token, leaving the trade name, which may run
# past its own column. source_rows stops on any line it cannot read this way.
_HEADER = ("営業者氏名", "営業者法人電話番号", "営業所所在地", "営業所名称", "営業所電話番号", "業種", "形態", "許可年月日",
           "有効期限", "初回許可年月日", "許可番号")
_TITLE = "食品営業許可一覧"
_FOOTER = "名称がない施設"
_DATE = r"(?:令和|平成|昭和)(?:元|\d+)年\d+月\d+日"
_TAIL = re.compile(rf"\s({_DATE})\s+({_DATE})\s+({_DATE})\s+(\d+)\s*$")
_PHONE = re.compile(r"[0-9０-９()（）][0-9０-９()（）\-－ー‐]{5,}")
# The 6 forms (形態) the list uses, all on old-law rows (granted before
# 2021-06-01); the revised law's rows carry none.
FORMS = ("普通形態", "特殊形態", "自動販売形態", "簡易形態", "卸販売及び小売販売形態", "移動販売形態")
# The old law ended on 2021-05-31: a permit granted before 2021-06-01 is an
# old-law permit.
NEW_LAW_FROM = datetime.date(2021, 6, 1)


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def pdf_rows():
    """Every record of the PDF's text as a dict keyed by the header's column
    names, the two phone columns left out. Stops on a page without a header,
    a record line that does not end in three dates and a permit number, a
    cell that overflows the address column, or a record with no type."""
    if not PDF_TEXT.exists():
        raise SystemExit(f"missing {PDF_TEXT}\nRun: python pipeline/{SLUG}/fetch_sources.py city")
    rows = []
    for n, page in enumerate(PDF_TEXT.read_text(encoding="utf-8").split("\f"), 1):
        lines = [ln for ln in page.split("\n") if ln.strip()]
        if not lines:
            continue
        head = next((ln for ln in lines if all(h in ln for h in _HEADER)), None)
        if head is None:
            raise SystemExit(f"{PDF_TEXT.name}: page {n} has no header line - not the layout this reader knows")
        o_phone, o_addr, o_name = (head.index(h) for h in _HEADER[1:4])
        for ln in lines:
            if ln is head or _TITLE in ln or _FOOTER in ln:
                continue
            tail = _TAIL.search(ln)
            if not tail or tail.start() < o_name:
                raise SystemExit(f"{PDF_TEXT.name}: page {n}: a line that is not a record "
                                 f"({len(ln)} characters, no three dates and permit number at its end)")
            phone = ln[o_phone:o_addr].strip()
            if (phone and not _PHONE.fullmatch(phone)) or (ln[o_addr - 1] != " ") or (ln[o_name - 1] != " "):
                raise SystemExit(f"{PDF_TEXT.name}: page {n}: a cell overflows its column (permit {tail.group(4)})")
            cells = ln[o_name:tail.start()].split()
            form = cells.pop() if cells and cells[-1] in FORMS else ""
            typ = cells.pop() if cells else ""
            if not typ or not re.search(r"[業機]$", typ):
                raise SystemExit(f"{PDF_TEXT.name}: page {n}: no permit type read (permit {tail.group(4)})")
            if cells and _PHONE.fullmatch(cells[-1]):
                cells.pop()
            # the trade name with its own inner spacing, the cells after it cut
            name = ln[o_name:tail.start()].strip()
            for cut in (form, typ):
                if cut:
                    name = name[:name.rindex(cut)].rstrip()
            if name and _PHONE.fullmatch(name.split()[-1]):
                name = name[:name.rindex(name.split()[-1])].rstrip()
            rows.append({"営業者氏名": ln[:o_phone].strip(), "営業所所在地": ln[o_addr:o_name].strip(),
                         "営業所名称": name, "業種": typ, "形態": form, "許可年月日": tail.group(1),
                         "有効期限": tail.group(2), "初回許可年月日": tail.group(3), "許可番号": tail.group(4)})
    return rows


def file_rows(key):
    """The file's rows as it stands, for fetch_sources.py's count and header
    check (japan_fetch): every record of the PDF, before the same-number
    rule."""
    return pdf_rows()


def source_rows(key):
    """The list's rows (japan_step2 reads this hook where a city defines it):
    the PDF's records, less the old-law row of each permit number that also
    carries a revised-law row (owner, call 229, 2026-10-08: one pin per
    permit number, the new-law row kept). A premises renewed under the 2021
    law while its old permit's term ran on is listed twice under one number;
    the brief counted 127 such pairs (108 restaurants), each one old-law and
    one new-law row. A number repeated in any other shape stops the build."""
    from pipeline.baseline import emit
    from pipeline.countries import japan_register as jr

    rows = pdf_rows()
    by_number = {}
    for r in rows:
        by_number.setdefault(r["許可番号"], []).append(r)
    drop = set()
    for number, group in by_number.items():
        if len(group) == 1:
            continue
        old = [r for r in group if jr.wareki_date(r["許可年月日"]) < NEW_LAW_FROM]
        if len(group) != 2 or len(old) != 1:
            raise SystemExit(f"permit number {number}: {len(group)} rows, {len(old)} old-law - not one old-law and "
                             "one new-law row; the same-number rule (call 229) does not cover it")
        drop.add(id(old[0]))
    emit("pdf_rows", len(rows))
    emit("old_law_rows_superseded", len(drop))
    print(f"  the PDF: {len(rows):,} records; old-law rows whose number a new-law row carries, dropped: {len(drop):,}")
    return [r for r in rows if id(r) not in drop]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 33202.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kurashiki.
# S, W, N, E: the city's N03 extent (S 34.417, W 133.602, N 34.669,
# E 133.882) rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (34.41, 133.60, 34.67, 133.89)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment). OSM's 21 names (37 objects, 36 with name:en, 2026-10-11) mix two
# styles: 19 carry no macron (Bitchu-Kurese, Kyujo-mae, Mitsubishijiko-mae)
# and two do. Brought to the one style, Okayama's next door (no macrons).
# The other 19 stand as OSM has them, Kurashikishi and Kibinomakibi among
# them (written as one word in OSM; not checked against the operators' signs).
OSM_NAME_EN_OVERRIDES = {
    "上の町": "Kaminocho",                            # Kaminochō
    "中庄": "Nakasho",                                # Nakashō
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the N03 extent (133.602 to 133.882) lies inside the 132 to
# 138 band. Derived per city, not copied - see docs/project_context.md's CRS
# lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): step 1 measured a median nearest-station gap of 1,523 m
# over the 21 drawn stations (2026-10-11; the brief's figure exactly), far
# over the halving line (about 550 m). The one pair under 200 m is JR's 倉敷
# and the Mizushima Rinkai Railway's 倉敷市, 150 m apart: two stations of two
# operators, kept apart as N02 keeps them (Kobe's Tarumi and Sanyo Tarumi).
# Re-measure if the drawn stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25: 6 public lines; the Shinkansen's 新倉敷 dropped, the station
# staying as a JR Sanyo Line station). The Mizushima Main Line lies wholly
# inside (10 of 10). Every other line is cut at the city line (owner
# 2026-09-24): JR West's Sanyo Line keeps 4 station groups of 131 records,
# the Seto-Ohashi Line 4 (本四備讃線, JR West's four records and JR Shikoku's
# one at 児島), the Ibara Line 3 of 15. JR West's Hakubi Line (倉敷, of 28)
# and Uno Minato Line (茶屋町, of 15) keep one station each: a one-station JR
# stub stays as cut (Kobe's JR Takarazuka Line, owner 2026-09-27; Okayama
# keeps 本四備讃線's 植松 the same way). No frequency floor (owner, 2026-10-06,
# calls 46 and 86): the thinnest stretch, 水島 to 三菱自工前, has 15 and 13
# trains a day by the operator's timetable of 2026-03-14.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. Line names as the neighbouring maps write
# them (Okayama's JR Sanyo, JR Seto-Ohashi and JR Uno Minato lines, Fukuyama's
# Ibara Railway Ibara Line), no macrons. 本四備讃線 is JR West's to 児島 and JR
# Shikoku's from it: one public line, the Seto-Ohashi Line, drawn once from
# both operators' track (the JR Sanyo Line's two-operator precedent,
# pipeline/line_registry.py).
_MR, _JR, _JS, _IB = "水島臨海鉄道", "西日本旅客鉄道", "四国旅客鉄道", "井原鉄道"
LINES = {
    "MZ": {"n02": [(_MR, "水島本線")], "name": "Mizushima Rinkai Railway Mizushima Main Line", "name_ja": "水島本線",
           "short": "Mizushima Rinkai", "hue": "#0068B7"},
    "JS": {"n02": [(_JR, "山陽線")], "name": "JR Sanyo Line", "name_ja": "山陽本線", "short": "JR", "hue": "#0068B7"},
    "JB": {"n02": [(_JR, "本四備讃線"), (_JS, "本四備讃線")], "name": "JR Seto-Ohashi Line", "name_ja": "瀬戸大橋線",
           "short": "JR", "hue": "#00A7A7"},
    "JH": {"n02": [(_JR, "伯備線")], "name": "JR Hakubi Line", "name_ja": "伯備線", "short": "JR", "hue": "#9ACD32"},
    "JU": {"n02": [(_JR, "宇野線")], "name": "JR Uno Minato Line", "name_ja": "宇野みなと線", "short": "JR",
           "hue": "#00A0E9"},
    "IB": {"n02": [(_IB, "井原線")], "name": "Ibara Railway Ibara Line", "name_ja": "井原線", "short": "Ibara",
           "hue": "#009944"},
}
# Colours (owner, 2026-10-07: one colour per line on every map). The JR
# Sanyo Line takes its site-wide colour from pipeline/line_registry.py. The
# Seto-Ohashi and Uno Minato lines are on Okayama's map and the Ibara Line on
# Fukuyama's: each takes that map's colour through the registry entry added
# with this build (2026-10-11). The Mizushima Main Line and the Hakubi Line are on this map
# alone: scripts/line_colour_search.py's rule with the four inherited colours
# held fixed (2026-10-11: 3:1 on both map pages, CIE76 >= 45 from every pin,
# >= 18 from a line within 500 m, >= 12 from every other line here and on
# Okayama's and Fukuyama's maps), each the feasible colour nearest its hue.
# The Mizushima line keeps its operator blue; no yellow-green clears the
# olive and green pins by 45, so the Hakubi Line goes tan. Measured: every
# line >= 45.1 from the pins (no accepted trade under 45); closest pair
# within 500 m 19.0 (Seto-Ohashi, Uno Minato, which meet at 茶屋町, both
# inherited), anywhere 15.8 (Sanyo, Seto-Ohashi, both inherited, which never
# meet here); the dark-mode labels separate, 6 of 6. Re-measure if a line or
# a pin colour changes.
_COLOURS = {"MZ": "#0068B8", "JS": line_registry.colour("jr-west-sanyo-line"),
            "JB": line_registry.colour("jr-west-seto-ohashi-line"), "JH": "#A89078",
            "JU": line_registry.colour("jr-west-uno-minato-line"),
            "IB": line_registry.colour("ibara-railway-ibara-line")}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the Mizushima Rinkai Railway's timetable
# (mizurin.co.jp/contents/time_table.html, 2026-03-14 revision, read
# 2026-10-08) heads a column for each of its 10 passenger stations, 倉敷市 to
# 三菱自工前, as N02 has 10. Every other line is cut by the city line.
GATE3 = {"source": "The Mizushima Rinkai Railway's timetable (mizurin.co.jp/contents/time_table.html, "
                   "2026-03-14): 10 stations, 倉敷市 to 三菱自工前",
         "lines": {"MZ": 10}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KURASHIKI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KURASHIKI_BBOX

# A number alone in this file's name column is a code, not a sign: 25 shown
# rows, runs of consecutive five-digit numbers, a nursery school's and a
# student dormitory's kitchens among them. Shown as the permit type
# (owner, 2026-10-12; japan_step2.run).
NUMERIC_NAME_IS_CODE = True

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3603938622)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "ホテル　ラ・レインボー(廃墟)": "a hotel's ruins (historic=ruins; the name itself says ruin), not a business (the Kyoto and Seattle precedents); tags read 2026-10-13",
}
PLACE_DROPPED = {}
