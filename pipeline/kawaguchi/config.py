"""Kawaguchi-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/kawaguchi.md (11/12 checks, 2026-10-11: the city's CSV has
a newer edition than the one built on, see FOOD_EDITIONS). Kawaguchi City
(川口市, 11203), one municipality with no wards, a core city with its own
health center: Saitama Prefecture's lists (pipeline/countries/saitama_pref.py)
do not cover it. Japan's A/B batch (East-2), on the shared modules
(pipeline/countries/japan*.py) with the Japan foundation's rules on, in
Hiroshima's shape (food only: Food service and Food shops, no personal
services) with Ichinomiya's merge (a city's own full food list kept whole plus
the months since; owner, call 126).

Business leg: the city's own open-data CSV (川口市 保健所 食品衛生課,
食品等営業許可・届出一覧), CC BY 2.1 JP (owner, call 208). One file stacks the
full list of permits and notifications on 2026-03-31 and the new premises of
April, May and July 2026; June's new premises are not in it (owner, call 177:
built on the CSV as published, June's stoppage named on the page). The list
holds permits and notifications together; the food-retail notifications
count, in Retail (the japan_eigyo module's standing rule). The city writes the
address of 1,316 rows as asterisks (a sole trader's premises, by the brief's
measurement): withheld by the publisher, never placed, counted apart. No
personal services: the city's barber, beauty and laundry lists are PDFs under
the site's reserved terms and are not used (owner, call 104). MHLW's file for
11203 holds about 5% of the city's permits and is a control only, not read
here (calls 126-127). All placed by a JOIN to MLIT's 位置参照情報 (one
municipality, no wards), the city's three private-use glyphs mapped first
(japan.CITIES' "gaiji").

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03): the Saitama Rapid Railway Line (6 of N02's 8 埼玉高速鉄道線 stations), JR
East's Keihin-Tohoku Line (2 stations on N02's 東北線) and JR East's Musashino
Line (1 of 27, a stub kept as cut). English station names from OpenStreetMap's
name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kawaguchi" / "raw"
DATA_PROCESSED = ROOT / "data" / "kawaguchi" / "processed"
OUTPUTS = ROOT / "outputs" / "kawaguchi"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Kawaguchi"
SLUG = "kawaguchi"
MUNICIPALITY = "川口市"
PREFECTURE = "埼玉県"

# The city's own CMS (no catalogue API; it sends no charset). The open-data
# page lists the CSV and states its licence (ライセンス情報: クリエイティブ
# コモンズ「表示」(CC BY), no version; read as CC BY 2.1 JP, owner's call 208).
_HOST = "https://www.city.kawaguchi.lg.jp"
FOOD_PAGE = _HOST + "/shiseijoho/ict_johoka/2/12182.html"
# source key -> (file, URL, the page that carries it). One file holds every
# edition; source_rows splits it by its Source.Name column.
SOURCE_FILES = {
    "food": ("food-business-license-notification.csv",
             _HOST + "/material/files/group/1/food-business-license-notification.csv", FOOD_PAGE),
}
# The editions inside the CSV as built on (2,095,941 bytes, Last-Modified
# 2026-08-19, downloaded 2026-10-06): the workbook each row came from, by the
# first five characters of Source.Name, with the rows each holds. No R0806:
# June 2026's new premises are missing (owner, call 177). source_rows stops on
# any other edition or count, so a re-download is re-measured, never read
# silently: the city's page was updated 2026-10-07 and the live CSV carried an
# R0808 edition on 2026-10-11 (the brief's third check).
FOOD_FULL = "R0803"
FOOD_EDITIONS = {"R0803": 8034, "R0804": 112, "R0805": 104, "R0807": 114}
# Kyoto's rule: the date each list states, never the download's. The full
# list is 令和8年3月末; the months run to July 2026.
SOURCE_AS_OF = {"food": "2026-03-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
# Calls 161 and 172 (owner, 2026-10-06): each permit's term is read against
# the last day its edition covers, never today. The full list is kept whole
# on its own date (call 126; no 終了年月日 before 2026-03-31 by the brief); the
# months against 2026-07-31, the last day the newest covers.
TERM_AS_OF = {"food": "2026-03-31", "food_new": "2026-07-31"}

# What step 2 reads. "food_new" is the three monthly editions as one source
# of the same kind as the full list (japan_step2.kind, Ichinomiya's): new
# premises only (every monthly row's first permit or notification is in 2026,
# by the brief), and one pin per premises and bucket shows a premises once.
SOURCES = {"food": SOURCE_FILES["food"][0], "food_new": "the April, May and July 2026 editions of the same file"}
SOURCE_KIND = {"food_new": "food"}
# Declared, never inferred: UTF-8 with a BOM, CRLF.
SOURCE_ENCODING = {"food": "utf-8-sig"}
# The columns the file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator columns (申請者名, filled on all 8,364
# rows, 4,154 of them without a company or cooperative marker by the brief,
# and 代表者名（法人）) are REQUIRED so the name rule
# (japan_register.name_is_operator; owner 2026-09-27) cannot silently compare
# nothing; read IN MEMORY by that rule only, never kept. Never selected:
# 営業所電話番号, 申請者住所 (an operator's own address) and 申請者電話番号.
_FOOD = ("Source.Name", "許可番号", "業種", "種目", "屋号", "営業所所在地", "申請者名", "代表者名（法人）",
         "開始年月日", "終了年月日")
REQUIRED_COLUMNS = {"food": _FOOD, "food_new": _FOOD}


def source_csv(key):
    return DATA_RAW / SOURCE_FILES["food"][0]


def file_rows(key):
    """The fetched file's rows as it stands (japan_fetch's count and header
    check, and every read below)."""
    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    return list(jr.city_rows(path))


def source_rows(key):
    """A source's rows (japan_step2 reads this hook where a city defines it).
    "food" is the full list of 2026-03-31 (Source.Name R0803...), "food_new"
    the monthly editions in the file's own order. Stops unless the file holds
    exactly FOOD_EDITIONS."""
    path = source_csv(key)
    rows = file_rows(key)
    missing = [c for c in REQUIRED_COLUMNS[key] if rows and c not in rows[0]]
    if missing:
        raise SystemExit(f"{path.name}: header lacks {missing} - not the file the brief read")
    found = {}
    for r in rows:
        ed = (r.get("Source.Name") or "").strip()[:5]
        found[ed] = found.get(ed, 0) + 1
    if found != FOOD_EDITIONS:
        raise SystemExit(f"{path.name}: editions {found}, not config.FOOD_EDITIONS {FOOD_EDITIONS} - a new "
                         f"edition of the city's CSV: re-measure it (docs/build_briefs/{SLUG}.md) before reading")
    for r in rows:
        if ((r.get("Source.Name") or "").strip()[:5] == FOOD_FULL) == (key == "food"):
            yield r


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 11203.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Kawaguchi.
# S, W, N, E: the city's N03 extent (S 35.780, W 139.675, N 35.887, E 139.788)
# rounded out; step 1 stops if the city leaves it.
OSM_BBOX = (35.78, 139.67, 35.89, 139.79)
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

# UTM zone 54N: the N03 centroid (~139.73) and the whole extent (139.675 to
# 139.788) fall in the 138 to 144 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32654"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings by the spacing rule: the
# brief's median nearest-station gap is 1,633 m (8 stations), over the 550 m
# that halves them.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-11: 3 lines, 9 station records, 8 station groups). Saitama Railway's
# line keeps 6 of N02's 8 stations (川口元郷, 南鳩ヶ谷, 鳩ヶ谷, 新井宿, 戸塚安行,
# 東川口); JR East's 東北線 2 of 155 (川口, 西川口, Keihin-Tohoku stations only:
# the Utsunomiya, Takasaki and Shonan-Shinjuku trains pass on the same legal
# line without stopping and are not drawn); JR East's Musashino Line 1 of 27
# (東川口), a JR one-station stub kept as cut (the owner's standing call of
# 2026-09-27; not an urban line, so calls 54 and 92 do not remove it). 東川口
# is one N02 group for Saitama Railway and JR (165 m apart by the brief). No
# Shinkansen station, tram or light rail in the city. No frequency floor
# (owner, 2026-10-06, calls 46 and 86): the thinnest line, the Musashino at
# 東川口, has 133 weekday departures each way (JR East's timetable, read
# 2026-10-06).
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300
# The Saitama Rapid Railway Line and the Keihin-Tohoku Line run on into Tokyo (13):
# 赤羽岩淵 and 赤羽, both in Kita Ward, are named by Tokyo's N03.
N03_NEIGHBOR_PREFS = ("13",)

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the Keihin-Tohoku Line under
# JR's legal 東北線: drawn as a `route` over it between the next station
# outside the city each way (赤羽 in Tokyo's Kita Ward, 蕨 in Warabi), as
# Tokyo's and Kawasaki's JK is. N02 files Saitama Railway's line as
# 埼玉高速鉄道線, the Saitama Rapid Railway Line, its formal name and the label
# here (owner, 2026-10-11); 埼玉スタジアム線, the Saitama Stadium Line, is the
# nickname the operator adopted on 2015-11-27 and signs on its timetable pages
# (read 2026-10-06). Line names without macrons.
_JR = "東日本旅客鉄道"
LINES = {
    "SR": {"n02": [("埼玉高速鉄道", "埼玉高速鉄道線")], "name": "Saitama Rapid Railway Line",
           "name_ja": "埼玉高速鉄道線", "short": "Saitama Railway", "hue": "#1E50A2"},
    "JK": {"route": [(_JR, "東北線", ["赤羽", "川口", "西川口", "蕨"])],
           "name": "JR Keihin-Tohoku Line", "name_ja": "京浜東北線", "short": "JR", "hue": "#00B2E5"},
    "JM": {"n02": [(_JR, "武蔵野線")], "name": "JR Musashino Line", "name_ja": "武蔵野線",
           "short": "JR", "hue": "#F15A22"},
}
# SHARED LINES: the two JR lines are drawn on other maps and take their one
# site-wide colour from pipeline/line_registry.py (owner, 2026-10-07: one
# colour per line on every map), never a value of this city's own. The
# Saitama Rapid Railway Line is new to the site (Tokyo leaves its one station out)
# and takes scripts/line_colour_search.py's colour (2026-10-11): 3:1 on both
# pages (dark 3.11, light 6.02), CIE76 77.8 from the nearest pin (Food
# service), 49.1 from the Keihin-Tohoku Line's registry colour and 119.2 from
# the Musashino Line's. The two registry colours: Keihin-Tohoku 50.6 from its
# nearest pin, Musashino 54.7; the closest pair of lines 49.1. Nothing under
# 45, so no accepted trade.
_COLOURS = {
    "SR": "#3060B8",
    "JK": line_registry.colour("jr-east-keihin-tohoku-line"),
    "JM": line_registry.colour("jr-east-musashino-line"),
}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: the operators' own stations inside the city line (the brief:
# Saitama Railway's own station list 6, JR East's Keihin-Tohoku 2 and
# Musashino 1, read 2026-10-06).
GATE3 = {"source": "Saitama Railway's own station list and JR East's own station timetables "
                   "(s-rail.ekitan.com, timetables.jreast.co.jp), read against the city line: "
                   "Saitama Rapid Railway Line 6, Keihin-Tohoku Line 2, Musashino Line 1",
         "lines": {"SR": 6, "JK": 2, "JM": 1}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
KAWAGUCHI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = KAWAGUCHI_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3601768337)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # glitch: dropped in the full read (owner, 2026-10-13)
    "way/621470725": "'川口市並木町公园': last character is the simplified Chinese form of \"park\" (园), not the Japanese one; a search in Japanese never matches it (full read, glitch)",
    # duplicate: dropped in the full read (owner, 2026-10-13)
    "node/12709313822": "'宝厳院水舎': the wash-basin shelter of the temple that already has its row (node/12709313821, 15 m away), tagged a place of worship of its own (full read, duplicate)",
    "node/12709285479": "'宝厳院仁王門': the gate of the same temple, 25 m from the temple's row (full read, duplicate)",
    "node/12709285477": "'宝厳院薬師堂': a hall of the same temple, 30 m from the temple's row (full read, duplicate)",
    "relation/20129763": "'西光院本堂': the main hall of the temple that has its own row with the article (way/596489512), 45 m away (full read, duplicate)",
    "way/1037871040": "'鳩ヶ谷氷川神社': one shrine twice, 15 m apart: this building outline and node/1986152896, which carries the English name; either may go, the node has more (full read, duplicate)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "node/12709285476": "'薬師堂': \"Yakushi hall\", the hall type alone, 20 m from the temple's row and beside the row that names the same hall with the temple's name (full read, bare type)",
    # religious office: dropped in the full read (owner, 2026-10-13)
    "node/12709273774": "'慈林薬師会館': a meeting hall (kaikan) of the same temple precinct tagged a place of worship (full read, religious office)",
    # unsure in the full read, dropped by ruling 3: a hall named only for what it enshrines, or a deity's title alone (owner, 2026-10-13)
    "way/560361350": "'阿弥陀堂': 阿弥陀堂, listed in the ruling (unsure in the full read; ruling 3)",
    "way/675351923": "'太子堂': 太子堂, listed in the ruling (unsure in the full read; ruling 3)",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "node/12709285478": "'薬師堂': the twin of node/12709285476; bare type: dropped in the full read (owner, 2026-10-13)",
}
