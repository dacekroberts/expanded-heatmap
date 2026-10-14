"""Matsue-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is
docs/build_briefs/matsue.md (14/14 checks, 2026-10-11). Part of the A/B build
plan's Regional-2 batch, on the shared modules (pipeline/countries/japan*.py)
with every shared rule on. Personal services only (Band B, owner 2026-10-06:
Kochi's page shape): the city's own food list is under its site's copyright
and was not requested, and MHLW's file for 32201 holds 45 open restaurant
permits against e-Stat's 2,328 in force (1.9%), too thin to stand in.

Business leg: the city's three 生活衛生 registers on Shimane Prefecture's
portal (shimane-opendata.jp, organisation 松江市, PDL 1.0): barbers, beauty
salons and laundries, each ONE file, the full register as of 2026-08-31,
re-issued whole each month, so nothing is rebuilt and no months are merged.
The registers keep no closure date: a dot is a premises on the register, not
a business open today. Everything placed by a JOIN to MLIT's 位置参照情報
(one municipality, no wards).

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). JR West's San'in and Kisuki lines and the Ichibata Electric Railway's
Kita-Matsue Line. English station names from OpenStreetMap's name:en.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "matsue" / "raw"
DATA_PROCESSED = ROOT / "data" / "matsue" / "processed"
OUTPUTS = ROOT / "outputs" / "matsue"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Matsue"
SLUG = "matsue"
MUNICIPALITY = "松江市"
PREFECTURE = "島根県"

# Shimane Prefecture's portal (島根県 dataeye); each dataset is 松江市's, 作成頻度
# 毎月, and every monthly resource is the full list as of its month end. Each
# resource page states PDL1.0（公共データ利用規約第1.0版）. Read 2026-10-06 by a
# licence-read agent: permitted with conditions, a fault-based own-cost clause
# (DECISIONS.md, "Wave 5, second half"). Links go to shimane-opendata.jp,
# never to city.matsue.lg.jp (the city's site terms ask to be told of links).
PORTAL = "https://shimane-opendata.jp"
# key -> (dataset number, resource id, the publisher's file name). THE
# RESOURCE ID CHANGES EVERY MONTH (76779 is August's barber list; July's was
# 76656): japan_fetch.current_url has no rule for this portal, so the URLs are
# pinned to the edition this build read. A later month is a new id and a
# re-measure.
_LISTS = {
    "barber": (1254, 76779, "20260831riyousho.xlsx"),
    "beauty": (898, 76780, "20260831biyousho.xlsx"),
    "laundry": (899, 76781, "20260831cleaning.xlsx"),
}
# source key -> (file, URL of the edition this build read, the page that
# carries its licence). Step 0, 2026-10-06, each HTTP 200 from the portal's
# own host: 46,625 B, 102,585 B and 26,360 B.
SOURCE_FILES = {k: (name, f"{PORTAL}/resource_download/{rid}", f"{PORTAL}/resources/{rid}")
                for k, (_, rid, name) in _LISTS.items()}
# The date each resource states (令和8年8月31日時点), never the download's.
REGISTERS_AS_OF = "2026-08-31"
SOURCE_AS_OF = {k: REGISTERS_AS_OF for k in _LISTS}
FOOD_AS_OF = None  # no food leg (owner, 2026-10-06)
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. The operator column (営業者の名称又は氏名: no company or
# cooperative marker on 236 of 267 barber rows, 467 of 574 beauty rows and 25
# of 108 laundry rows, the shape of a sole trader's own name; the brief,
# 2026-10-06) is REQUIRED so the name rule (japan_register.name_is_operator;
# owner 2026-09-27) cannot silently compare nothing; it is read IN MEMORY by
# that rule only, never kept. Never selected: 代表者の役職及び氏名 (a company's
# representative, a person), 営業者所在地 (the operator's own address),
# 営業所電話番号, 営業所郵便番号.
_ADDR = {
    "barber": "営業所所在地（移動理容所にあっては営業区域及び車両保管場所）",
    "beauty": "営業所所在地（移動美容所にあっては営業区域及び車両保管場所）",
    "laundry": "営業所所在地",
}
_NAME, _OPERATOR, _NUMBER, _KIND = "営業所名称", "営業者の名称又は氏名", "確認番号", "クリーニング所又は取次所の別"
REQUIRED_COLUMNS = {
    "barber": (_NUMBER, _ADDR["barber"], _NAME, _OPERATOR),
    "beauty": (_NUMBER, _ADDR["beauty"], _NAME, _OPERATOR),
    "laundry": (_NUMBER, _ADDR["laundry"], _NAME, _OPERATOR, _KIND),
}
# What a build measured as dropped by source_rows, so a later edition that
# changes shape stops the build instead of passing silently (2026-08-31
# edition, measured 2026-10-11): the beauty file repeats its header as its
# first data row; one barber row is a mobile barber whose address names a
# service area and a vehicle depot in another prefecture.
SOURCE_ROWS_DROPPED = {"barber": {"mobile": 1, "header": 0}, "beauty": {"mobile": 0, "header": 1},
                       "laundry": {"mobile": 0, "header": 0}}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


def source_rows(key):
    """A register's rows (japan_step2 reads this hook where a city defines
    it), the premises and name-rule columns only (Kochi's and Shizuoka's
    column selection). Two rows are not premises and are left out here, as the
    brief prescribes (2026-10-06):

      * the beauty file's repeated header (a row whose 確認番号 cell reads
        確認番号; without this the shared mobile-salon rule would count it as a
        移動 salon, because its address cell is the column's own label);
      * the one mobile barber: the column's label allows a service area and a
        vehicle depot in place of an address, and this row names a depot in
        another prefecture. The shared mobile tests (一円, 保健所管, 移動) do not
        read that shape. The test is a prefecture other than the city's own
        in the address, never the substring 市内 (内中原町 is a town: 2 barber
        and 5 beauty addresses read 松江市内中原町).

    The counts dropped are checked against SOURCE_ROWS_DROPPED."""
    import re

    from pipeline.countries import japan_register as jr

    path = source_csv(key)
    if not path.exists():
        raise SystemExit(f"missing {path}\nRun: python pipeline/{SLUG}/fetch_sources.py")
    other_pref = re.compile(r"(?:北海道|東京都|京都府|大阪府|[^\s、,（(]{2,3}県)")
    keep = REQUIRED_COLUMNS[key]
    dropped = {"mobile": 0, "header": 0}
    rows = []
    for r in jr.city_rows(path):
        if str(r.get(_NUMBER) or "").strip() == _NUMBER:
            dropped["header"] += 1
            continue
        addr = str(r.get(_ADDR[key]) or "")
        if any(m != PREFECTURE for m in other_pref.findall(addr)):
            dropped["mobile"] += 1
            continue
        rows.append({c: r.get(c) for c in keep})
    if dropped != SOURCE_ROWS_DROPPED[key]:
        raise SystemExit(f"{path.name}: source_rows dropped {dropped}, the build measured "
                         f"{SOURCE_ROWS_DROPPED[key]} - a new edition? Re-measure (config.SOURCE_ROWS_DROPPED).")
    return rows


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 32201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en). Which stations exist is
# N02's; OSM supplies the English display name. No tram in Matsue.
# S, W, N, E: the city's N03 extent (S 35.330, W 132.875, N 35.606,
# E 133.352; the 2005 and 2011 mergers brought in eight towns) rounded out;
# step 1 stops if the city leaves it.
OSM_BBOX = (35.32, 132.87, 35.61, 133.36)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
OSM_NAME_MATCH_M = 600
OSM_NAME_ALIASES = {}
OSM_NAME_EN_TIES = {}
OSM_NAME_EN_MISSING = {}
# Cited overrides of OSM's name:en ({ja: en}). None is needed: OSM's 16 names
# stand as they are (41 objects, 40 with name:en, 2026-10-11; no macron, a
# hyphen and a capital before a place name, 温泉 or 前: Higashi-Matsue,
# Minami-Shinji, Tamatsukuri-Onsen, Matsue-Shinjiko-Onsen, Matsue English
# Garden-Mae; Matsue Vogel Park is the park's own name, not a translation).
OSM_NAME_EN_OVERRIDES = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 53N: the N03 centroid (~133.069) and the whole extent (132.875 to
# 133.352) fall in the 132 to 138 band. Derived per city, not copied - see
# docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32653"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement). Standard rings on the spacing rule
# (docs/ring_rules.md): step 1 measured a median nearest-station gap of 1,718 m
# (minimum 1,197 m) over the 16 drawn stations (2026-10-11; the brief read the
# same 1,718 m), far over the halving line (about 550 m). Re-measure if the
# drawn stations change.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (the brief's stub test
# on N02-25, reproduced 2026-10-11: 3 lines; no Shinkansen runs in Shimane).
# Every line is cut at the city line (owner 2026-09-24): the San'in Line
# keeps 7 of 161 station records, the Kisuki Line 2 of 18 (宍道, its junction,
# and 南宍道: a JR line cut at the line, drawn as cut under the standing call),
# the Kita-Matsue Line 8 of 22. 宍道 is one N02 group on both JR lines (0 m).
# All three are heavy rail (N02 classes 11 and 12); no tram or light rail.
# No frequency floor (owner, 2026-10-06, calls 46 and 86): the Kisuki Line
# runs 10 trains a weekday toward 木次 and 11 toward 宍道 at 南宍道 (JR West's
# station timetables, read 2026-10-06 for the brief), drawn and named on the
# page as low-frequency. The San'in stations run 20 to 45 a day each way and
# the Kita-Matsue Line 21 to 24.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), a starting hue for scripts/line_colour_search.py (hue) and the
# project's colour. Line names carry no macrons and no "Main" for JR, as
# Shimonoseki's JR San'in Line (the same line).
_JW, _IC = "西日本旅客鉄道", "一畑電車"
LINES = {
    "SN": {"n02": [(_JW, "山陰線")], "name": "JR San'in Line", "name_ja": "山陰本線", "short": "JR",
           "hue": "#E60012"},
    "KS": {"n02": [(_JW, "木次線")], "name": "JR Kisuki Line", "name_ja": "木次線", "short": "JR",
           "hue": "#8A6A00"},
    "IC": {"n02": [(_IC, "北松江線")], "name": "Ichibata Electric Railway Kita-Matsue Line",
           "name_ja": "北松江線", "short": "Ichibata", "hue": "#F08300"},
}
# Colours: the project's own, from scripts/line_colour_search.py matsue
# (2026-10-11, defaults: >= 18 within 500 m, >= 10 city-wide), each the
# feasible colour nearest its starting hue that reads 3:1 on both map pages
# and clears CIE76 45 from every pin. Margins from the pins: San'in 51.6,
# Kisuki 45.2, Kita-Matsue 53.6 (none between 20 and 45). Closest pair within
# 500 m 46.3 (San'in and Kisuki, which meet at 宍道); closest anywhere 24.4
# (Kisuki and Kita-Matsue, on opposite shores of the lake); the dark-mode
# labels separate, 3 of 3. The Kisuki Line's starting hue is a dark gold: a
# first run from a yellow-orange hue put it 10.8 from the Kita-Matsue Line's
# orange.
# SHARED LINE: JR West's San'in Line is also on Shimonoseki's map, and
# Tottori's draws it too: its colour, #E80010 (the search chose the same
# value independently here), is read from pipeline/line_registry.py
# (owner, 2026-10-07: one colour per line on every map).
_COLOURS = {"SN": line_registry.colour("jr-west-sanin-line"), "KS": "#A05000", "IC": "#E07800"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}

# Gate 3: Ichibata's timetable list page
# (railway.ichibata.co.jp/operate/timetable/list/, read 2026-10-06 for the
# brief and again 2026-10-11) links one PDF per station, numbered along the
# Kita-Matsue Line 01 電鉄出雲市 to 22 松江しんじ湖温泉: 22 stations, as N02 has
# 22, and numbers 15 津ノ森 to 22 are the eight N02 places inside the city
# line (13 一畑口 and 14 伊野灘 are in 出雲市). The operator's list does not say
# where the city line falls; that part is N03's. JR West: both lines run on
# past the city line; its station timetable pages (timetable.jr-odekake.net)
# were read for all 8 JR station groups (2026-10-06, the brief), station ids
# 0640732 揖屋 to 0640738 宍道 consecutive, and 0641815 南宍道.
GATE3 = {"source": "Ichibata's timetable list page (railway.ichibata.co.jp/operate/timetable/list/): 22 "
                   "Kita-Matsue Line stations, 津ノ森 to 松江しんじ湖温泉 the eight inside the city; JR West's "
                   "station timetable pages read for all 8 JR stations",
         "lines": {"IC": 8}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
MATSUE_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = MATSUE_BBOX

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604088064)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
PLACE_REVIEWED = {}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/matsue.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # Worship named only by its body or chain (owner, 2026-10-13)
    "node/3739108617": "'MOA会館': MOA (a religious body) plus the hall word 会館 only, no place or proper name",
    "way/1296963682": "'世界平和統一家庭連合': named only by the body (Family Federation for World Peace and Unification)",
    "way/1102649247": "'世界真光文明教団': named only by the body (Sekai Mahikari Bunmei Kyodan)",
    "way/1083509449": "'黒住教': named only by the body (Kurozumikyo)",
    "way/1233811182": "'黒住教': named only by the body (Kurozumikyo)",
    # A bare type word (owner, 2026-10-13)
    "way/1274758376": "'テニスコート': テニスコート = \"tennis court\", tagged leisure=stadium, no article",
    "way/557648812": "'宮庫': 宮庫 = shrine storehouse, the whole name is the type word",
    "way/616221085": "'宮庫': 宮庫 = shrine storehouse, the whole name is the type word",
    "way/631717596": "'宮庫': 宮庫 = shrine storehouse, the whole name is the type word",
    "way/647113939": "'子供広場': 子供広場 = \"children's square\"",
    "way/1271136916": "'幼児遊園': 幼児遊園 = \"toddlers' playground\"",
    "way/1115107371": "'遊具': 遊具 = \"play equipment\", tagged a park",
    "way/556737326": "'門': 門 = \"gate\", tagged a place of worship",
    "node/13394188818": "'御神木': 御神木 = \"sacred tree\", a node inside 神魂神社 tagged a place of worship",
    "way/1087660031": "'永代供養堂': 永代供養堂 = \"perpetual memorial hall\", a building of 善光寺 named by its type",
    # A religious office (owner, 2026-10-13)
    "way/1077667592": "'世界メシア教 中国教区': 世界メシア教's regional diocese (教区) office tagged a place of worship",
    "way/1084201319": "'偕和會 松江事務所': 事務所 = office of an association, tagged a place of worship",
    "way/1243083515": "'岡田茂吉研究所': 研究所 = research institute of a religious body, tagged a place of worship",
    "way/318202607": "'曹洞宗島根県第二宗務所': 宗務所 = Soto sect district administrative office, tagged a place of worship",
    "way/1077667586": "'英霊にこたえる会 島根県本部': prefectural headquarters (本部) of a veterans' association, tagged a place of worship",
    # A description standing in for a name (owner, 2026-10-13)
    "way/562739697": "'堀立柱建物': 堀立柱建物 = \"post-built building\", a reconstructed exhibit named by its type inside 田和山史跡公園",
    "way/558125768": "'掘立柱住居': 掘立柱住居 = \"post-built dwelling\", a reconstructed exhibit named by its type",
    "way/562739328": "'竪穴住居': 竪穴住居 = \"pit dwelling\", a reconstructed exhibit named by its type",
    "way/558125755": "'竪穴式住居': 竪穴式住居 = \"pit dwelling\", a reconstructed exhibit named by its type",
    # An object no longer there (owner, 2026-10-13)
    "node/10607758224": "'風見大権現跡地': 跡地 = \"former site\" of a shrine, still tagged a place of worship",
    # Unsure rows a ruling drops: a hall named only for what it enshrines, or a deity's title alone (ruling 3) (owner, 2026-10-13)
    "way/685632261": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/685636836": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/893920584": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1081527567": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1082686932": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1084140738": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1087094896": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1106535363": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1121641187": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1133083031": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1133116196": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1143876224": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1211718017": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1230074012": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1251561084": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1272713317": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1273313566": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1299967615": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1338985201": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1340909488": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1350873707": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    "way/1354144166": "'歳徳神': a hall named only for what it enshrines, or a deity's title alone",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "way/1271136917": "'幼児遊園': the twin of way/1271136916; A bare type word (owner, 2026-10-13)",
    "way/1272713318": "'歳徳神': the twin of way/685632261; Unsure rows a ruling drops: a hall named only for what it enshrines, or a deity's title alone (ruling 3) (owner, 2026-10-13)",
}
