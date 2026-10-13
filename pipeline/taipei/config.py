"""Taipei (Regional)-specific settings: Taipei City + New Taipei City, scoped to
one page per this project's per-city folder architecture.

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/taipei.md,
the method the `taiwan-city` skill.

REGIONAL, like Dublin and Lille (owner, 2026-09-23): New Taipei completely
surrounds Taipei, and the metro crosses the boundary on several lines.

Business leg: the national business tax register (FIA; the shared cache), the
rows whose address is in either city, JOINED to each city's own door-plate file
(the shared step 2, run once per city and the two results concatenated).

Rail (owner, 2026-09-25): every metro and light-rail line in the two cities -
Taipei Metro's five lines and their branches, New Taipei's Circular Line and
Danhai and Ankeng light rail, and the Airport MRT's stations in the two cities.
Routes, stations and colours from OpenStreetMap: Taipei's network map carries no colours
and may lack New Taipei's lines (the recorded ground, osm-rail). A station is in
the region when either city's door-plate file has plates within 300 m of it.
Gate 3: Taipei Metro's own station list. NOT drawn: Taiwan Railway, high-speed
rail, the Maokong Gondola.
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "taipei" / "raw"
DATA_PROCESSED = ROOT / "data" / "taipei" / "processed"
OUTPUTS = ROOT / "outputs" / "taipei"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

# Taipei's door plates (民政局, data.taipei) - the name is the one the screen's
# control reads (scripts/screen_taiwan_join.py taipei).
TAIPEI_DOORPLATE_URL = ("https://data.taipei/api/dataset/b7c8e724-1e98-45ee-a0bd-f3840623ed97/"
                        "resource/ce76ca0c-7f94-4935-ab47-1d2a41ca2abb/download")
TAIPEI_DOORPLATE_CSV = DATA_RAW / "taipei_doorplate_20260902.csv"
TAIPEI_DOORPLATE_EDITION = "臺北市門牌位置數值資料 20260902"
# New Taipei's (data.ntpc.gov.tw), English-headed. In data/new_taipei/raw/, where
# the screen reads it.
NEW_TAIPEI_DOORPLATE_URL = "https://data.ntpc.gov.tw/api/datasets/d7b568ab-3819-40c8-a6e7-a6b199443101/csv/file"
NEW_TAIPEI_DOORPLATE_CSV = ROOT / "data" / "new_taipei" / "raw" / "new_taipei_doorplate.csv"
# The dataset's own description names the month (ROC 115/09) - read 2026-09-25.
NEW_TAIPEI_DOORPLATE_EDITION = "新北市門牌位置數值資料 11509"
# Taipei Metro's own station list (臺北捷運路線車站資料服務, data.gov.tw 131326): gate 3.
METRO_LIST_URL = ("https://data.taipei/api/dataset/8bf00fa8-86a5-437e-b5c7-9bc0fe0e2971/"
                  "resource/e3c0e67f-5916-405f-ad9a-41f52a65c2d2/download")
METRO_LIST_CSV = DATA_RAW / "taipei_metro_stations.csv"

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
)
# Bounded (osm-rail): the metro's extent in the two cities. Relations reaching
# beyond it (the Airport MRT to Taoyuan) come back whole, drawn to their ends.
OSM_BBOX = (24.93, 121.36, 25.20, 121.66)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"

# The two door-plate files' columns (read 2026-09-25): both TWD97 TM2 with a
# district CODE; Taipei's headers are Chinese, New Taipei's English.
PLATE_CRS = "EPSG:3826"
TAIPEI_PLATES = {"cols": {"street": "街路段", "lane": "巷", "alley": "弄", "num": "號",
                          "x": "橫座標", "y": "縱座標"}, "district": "鄉鎮市區代碼"}
NEW_TAIPEI_PLATES = {"cols": {"street": "street、road、section", "lane": "lane", "alley": "alley",
                              "num": "number", "x": "x_3826", "y": "y_3826"}, "district": "areacode"}
TAIPEI_PLATE_XY = ("橫座標", "縱座標")
NEW_TAIPEI_PLATE_XY = ("x_3826", "y_3826")
ADDRESS_PREFIXES = ("臺北市", "台北市", "新北市", "臺北縣", "台北縣")
CITY_PREFIXES = {"Taipei": ("臺北市", "台北市"), "New Taipei": ("新北市", "臺北縣", "台北縣")}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 51N: the longitude (~121.53) falls in the 120 to 126 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32651"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Matched on the RELATION's ref (and, where one ref holds a branch, its name),
# after printing the table. Colours are the ones OSM carries on each line's
# relations (the Seoul / Hong Kong precedent), except the Zhonghe-Xinlu Line,
# whose relations say `colour=orange` - a CSS keyword, resolved through the CSS
# named-colour table to #FFA500 (osm-rail: never invent a shade). The two
# branches carry their own colours in OSM, as on Taipei Metro's own map, so they
# are drawn as lines of their own. operator_lines: the rows of Taipei Metro's
# list each line is checked against (gate 3); New Taipei's lines and the Airport
# MRT are not in that list.
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "BR": {"ref": "BR", "colour": "#A74C00", "name": "Wenhu Line", "operator_lines": ["BR"]},
    "R": {"ref": "R", "colour": "#FF0000", "name": "Tamsui–Xinyi Line", "operator_lines": ["R"]},
    "RB": {"ref": "捷運紅線 (新北投支線)", "colour": "#F890A5", "name": "Xinbeitou Branch",
           "operator_lines": ["R-3"]},
    "G": {"ref": "G", "name_not": ("小碧潭",), "colour": "#1E7B54", "name": "Songshan–Xindian Line",
          "operator_lines": ["G"]},
    "GB": {"ref": "G", "name_has": "小碧潭", "colour": "#CEDC00", "name": "Xiaobitan Branch",
           "operator_lines": ["G-3"]},
    "O": {"ref": "O", "colour": "#FFA500", "name": "Zhonghe–Xinlu Line", "operator_lines": ["O"]},
    "BL": {"ref": "BL", "colour": "#007EC7", "name": "Bannan Line", "operator_lines": ["BL"]},
    "Y": {"ref": "Y", "colour": "#FFD900", "name": "Circular Line"},
    "LB": {"ref": "LB", "colour": "#6DB7D0", "name": "Sanying Line"},
    "V": {"ref": "V", "colour": "#FEBEB5", "name": "Danhai LRT"},
    "K": {"ref": "K", "colour": "#C3B091", "name": "Ankeng LRT"},
    "A": {"ref": "A", "colour": line_registry.colour("taoyuan-airport-mrt"), "name": "Airport MRT"},
}
NOT_DRAWN = set()
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0
# A station is in the region when a door plate of either city lies this close.
SCOPE_RADIUS_M = 300.0

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "taiwan_fia"
RAW_CLASSIFICATION_COLUMN = "industry"
OFFICE_FLOOR_MIN = 3
OFFICE_EXEMPT_ROWS_AT_ADDRESS = 20

CITY_BBOX = {"lat_min": 24.60, "lat_max": 25.35, "lon_min": 121.25, "lon_max": 122.05}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3601293250,3601527220)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("zh",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "公司田溪": "a stream with its own article (waterway=river); 公司 is part of the old place name",
    "淡水公司田溪橋遺蹟": "the remains of a bridge over that stream, with its own article",
    "臺灣菸酒公司": "the former Monopoly Bureau building, a historic building with its own article",
    "草山御賓館": "a historic guesthouse building with its own article, not a hotel",
    "菊元百貨店": "a historic department-store building with its own article; the store is gone",
    "龍山商場": "a market hall with its own article (amenity=marketplace)",
}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "node/14039090299": "a bus terminal in as a station",
    "way/1335599133": "a station under construction",
    "node/11671509524": "a description standing in for a junction name",
    "node/618865937": "a junction carrying only one road's name",
    "node/2466777786": "a private entrance of a religious residence",
    "node/12997229130": "a personal name standing as a hamlet",
    "way/1302217244": "an estate courtyard or estate green tagged a park or square",
    "way/1163836243": "an estate courtyard or estate green tagged a park or square",
    "way/587359944": "an estate courtyard or estate green tagged a park or square",
    "way/587358638": "an estate courtyard or estate green tagged a park or square",
    "way/1549081728": "an estate courtyard or estate green tagged a park or square",
    "way/232294321": "an estate courtyard or estate green tagged a park or square",
    "way/366771504": "estate grounds under a developer or estate brand name, tagged a park",
    "way/556614182": "estate grounds under a developer or estate brand name, tagged a park",
    "way/72380602": "estate grounds under a developer or estate brand name, tagged a park",
    "way/583839216": "estate grounds under a developer or estate brand name, tagged a park",
    "way/330028338": "estate grounds under a developer or estate brand name, tagged a park",
    "way/414157530": "estate grounds under a developer or estate brand name, tagged a park",
    "way/324949341": "estate grounds under a developer or estate brand name, tagged a park",
    "way/414366386": "estate grounds under a developer or estate brand name, tagged a park",
    "way/630877218": "estate grounds under a developer or estate brand name, tagged a park",
    "way/1087629543": "estate grounds under a developer or estate brand name, tagged a park",
    "way/635019770": "estate grounds under a developer or estate brand name, tagged a park",
    "way/1347029106": "a former residence tagged a park, no visiting shown",
    "node/13167332803": "a residence labelled as such, tagged a park",
    "node/4538270117": "a fortune-telling business tagged a place of worship",
    "node/8926113002": "a fortune-telling business tagged a place of worship",
    "node/13130475080": "a gym operator's listing tagged a stadium",
    "node/4033359734": "a billiard hall tagged a stadium",
    "way/865956949": "a business incubator tagged a historic building",
    "node/2828345012": "a dental practice under a surname",
    "way/1087826006": "a glassware brand's premises",
    "node/4809325621": "a counselling practice tagged a place of worship",
    "way/758996193": "a cafe tagged a park",
    "way/544384949": "a hotel forecourt tagged a park",
    "way/427777825": "a members' lodge tagged a place of worship",
    "way/1089081174": "a sports centre tagged a park",
    "way/785852305": "an agency office tagged a stadium",
    "way/1154453370": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453368": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453316": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453358": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453357": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453362": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453343": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453352": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453353": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453366": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453308": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453344": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453347": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453314": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453346": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453345": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453315": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453374": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453293": "a hospital's room, wing or driveway tagged a historic building",
    "way/1154453363": "a hospital's room, wing or driveway tagged a historic building",
    "node/6155338437": "a religious residence or retreat with no article",
    "way/660415081": "a religious residence or retreat with no article",
    "node/3721291640": "a religious residence or retreat with no article",
    "node/3721291639": "a religious residence or retreat with no article",
    "relation/16509812": "a religious residence or retreat with no article",
    "relation/13273856": "a religious residence or retreat with no article",
    "way/1366970286": "a religious residence or retreat with no article",
    "relation/16509811": "a religious residence or retreat with no article",
    "way/398005534": "a religious residence or retreat with no article",
    "node/6090416805": "a religious residence or retreat with no article",
    "node/6155338436": "a religious residence or retreat with no article",
    "node/6154225486": "a religious residence or retreat with no article",
    "way/415197452": "a religious residence or retreat with no article",
    "relation/18985603": "a religious residence or retreat with no article",
    "relation/13273855": "a religious residence or retreat with no article",
    "node/3480683962": "a religious residence or retreat with no article",
    "way/259878289": "a religious residence or retreat with no article",
    "way/386897076": "a religious residence or retreat with no article",
    "node/6183746782": "a religious residence or retreat with no article",
    "node/4834761767": "a religious residence or retreat with no article",
    "way/708022872": "a religious residence or retreat with no article",
    "way/530280720": "a religious residence or retreat with no article",
    "node/2158953453": "a religious residence or retreat with no article",
    "node/6284503808": "a religious residence or retreat with no article",
    "node/8926112883": "a religious residence or retreat with no article",
    "way/1425587273": "a religious residence or retreat with no article",
    "node/4085141434": "a religious residence or retreat with no article",
    "node/10917797645": "a religious residence or retreat with no article",
    "node/2822549352": "a religious residence or retreat with no article",
    "way/471709232": "a religious residence or retreat with no article",
    "node/3103265500": "a religious residence or retreat with no article",
    "way/388619699": "a religious residence or retreat with no article",
    "way/692406779": "a religious residence or retreat with no article",
    "way/508074606": "a religious residence or retreat with no article",
    "way/542936130": "a religious residence or retreat with no article",
    "way/779279909": "a religious residence or retreat with no article",
    "node/8636935117": "a religious residence or retreat with no article",
    "node/3469001075": "a neighbourhood-unit number or code standing in for a place name",
    "node/3469003639": "a neighbourhood-unit number or code standing in for a place name",
    "node/12756210469": "a neighbourhood-unit number or code standing in for a place name",
    "way/261084893": "a land-status description standing in for a park name",
    "way/1429882192": "a land-status description standing in for a park name",
    "way/1352272953": "a land-status description standing in for a park name",
    "way/271692177": "a description, floor label or slogan standing in for a name",
    "node/13637636162": "a description, floor label or slogan standing in for a name",
    "node/10074098709": "a description, floor label or slogan standing in for a name",
    "node/6242158930": "a description, floor label or slogan standing in for a name",
    "node/4200643113": "a description, floor label or slogan standing in for a name",
    "way/260053609": "a description, address number or a wrong object's name standing in for a name",
    "way/1187770036": "a description, address number or a wrong object's name standing in for a name",
    "way/1185697779": "a description, address number or a wrong object's name standing in for a name",
    "node/11164186010": "a description, address number or a wrong object's name standing in for a name",
    "node/13789676279": "a description, address number or a wrong object's name standing in for a name",
    "node/12390472547": "a description, address number or a wrong object's name standing in for a name",
    "node/13033211329": "a description, address number or a wrong object's name standing in for a name",
    "node/14039090293": "a description, address number or a wrong object's name standing in for a name",
    "node/2482647656": "a description, address number or a wrong object's name standing in for a name",
    "node/12686516727": "a height code standing in for a peak name",
    "node/6466685585": "a height code standing in for a peak name",
    "node/12984955428": "a height code standing in for a peak name",
    "node/6581600564": "a height code standing in for a peak name",
    "node/4201346296": "a height code standing in for a peak name",
    "node/8909354796": "a height code standing in for a peak name",
    "node/10689904035": "a height code standing in for a peak name",
    "node/1502690945": "a height code standing in for a peak name",
    "node/2300575566": "a height code standing in for a peak name",
    "node/6314240767": "a name or tag that says the thing is gone or abandoned",
    "node/12147942319": "a name or tag that says the thing is gone or abandoned",
    "node/8027396728": "a name or tag that says the thing is gone or abandoned",
    "node/7736291141": "a name or tag that says the thing is gone or abandoned",
    "node/5404823406": "a name or tag that says the thing is gone or abandoned",
    "way/343713285": "a name or tag that says the thing is gone or abandoned",
    "way/503477722": "a name or tag that says the thing is gone or abandoned",
    "way/377830145": "a former site of something moved or gone, no article",
    "node/14157037497": "a former site of something moved or gone, no article",
    "node/6073188497": "a former site of something moved or gone, no article",
    "node/5356323811": "a former site of something moved or gone, no article",
    "node/5109347815": "a former site of something moved or gone, no article",
    "node/5165233578": "a former site of something moved or gone, no article",
    "way/227654051": "a former site of something moved or gone, no article",
    "node/4033134232": "a former site of something moved or gone, no article",
    "node/5213336037": "a former site of something moved or gone, no article",
    "node/3439423190": "a displayed missile, museum contents",
    "way/542218260": "a stray invisible character in the name",
    "node/6153674648": "a phonetic symbol in place of a character",
    "node/4891439031": "a cut name",
    "node/4524318954": "a cut name",
    "node/6763209773": "a wrong-script character in the name",
    "node/8270334673": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/3999392708": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/4864484121": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/2766233227": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/13449685067": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/3452070600": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/4214932464": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/3451697499": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/12196338804": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/3703981656": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/2903088082": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/4092307411": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/2465295972": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/1502691014": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/2676684855": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/3233043648": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/12248651772": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/5637793638": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/11794764031": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/7782864783": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/5085428605": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/7976247048": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/3452070599": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/2950976520": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/8927764717": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/6050638880": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/3188482946": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/3421627293": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/7330891682": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/2629287045": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/4836651144": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/5735573258": "a grave, stele or plaque with no Wikipedia article of its own",
    "node/4092307414": "a grave, stele or plaque with no Wikipedia article of its own",
    "way/1044172128": "a facility road",
    "way/1340727897": "a facility road",
    "way/48776416": "a facility road",
    "way/551946341": "a facility road",
    "way/551946342": "a facility road",
    "way/551946353": "a facility road",
    "way/51919166": "a facility road",
    "way/51919168": "a facility road",
    "way/51919183": "a facility road",
    "way/329857370": "a utility's maintenance road",
    "way/329857371": "a utility's maintenance road",
    "way/796759366": "a utility's maintenance road",
    "way/796759367": "a utility's maintenance road",
    "way/1165343187": "a utility's maintenance road",
    "way/593707190": "a utility's maintenance road",
    "way/627244738": "a utility's maintenance road",
    "way/627244739": "a utility's maintenance road",
    "way/74355869": "a utility's maintenance road",
    "way/1113669132": "a business's own name",
    "way/1113669133": "a business's own name",
    "way/1301530458": "a business's own name",
    "way/266073584": "a business's own name",
    "way/274979028": "a business's own name",
    "way/1342161677": "a business's own name",
    "way/1342161679": "a business's own name",
    "way/1342161680": "a business's own name",
    "way/729308271": "a business's own name",
    "way/689291104": "a business's own name",
    "way/1324680349": "a campus's own name",
    "way/1301435283": "a campus's own name",
    "way/1306165292": "a campus's own name",
    "way/1301435274": "an estate or market name",
    "way/1301435277": "an estate or market name",
    "way/1307446005": "an estate or market name",
    "way/805920100": "an estate or market name",
    "way/760804200": "an estate or market name",
    "way/1101044484": "an estate or market name",
    "way/333112901": "an estate or market name",
    "way/338433723": "an estate or market name",
    "way/1187719029": "a religious residence with no article",
    "way/1187719030": "a religious residence with no article",
    "way/1187719031": "a religious residence with no article",
    "way/418202127": "a religious residence with no article",
    "way/418202128": "a religious residence with no article",
    "way/418202129": "a religious residence with no article",
    "way/426510302": "a religious residence with no article",
    "way/379550789": "a district name glued on",
    "way/948133815": "a private estate road",
    "way/948133816": "a private estate road",
    "way/948221059": "a private estate road",
    "way/301806641": "a private estate road",
    "way/824470676": "a private estate road",
    "way/825211671": "a private estate road",
    "way/825211672": "a private estate road",
    "way/1244163590": "a private estate road",
    "way/1474345405": "a private estate road",
    "way/1474345406": "a private estate road",
    "way/361069427": "a private estate road",
    "way/378491777": "a private estate road",
    "way/825223333": "a private estate road",
    "way/1030862559": "a residents-only or customers-only road",
    "way/1172350924": "a residents-only or customers-only road",
    "way/1172350925": "a residents-only or customers-only road",
    "way/1154453226": "a hospital's own road",
    "way/1545631703": "a hospital's own road",
    "way/1545631704": "a hospital's own road",
    "way/1545631709": "a hospital's own road",
    "way/1154453225": "a hospital's own road",
    "way/1154453227": "a hospital's own road",
    "way/1468767141": "a hospital's own road",
    "way/1513376098": "a campus's own road",
    "way/1513376099": "a campus's own road",
    "way/278139901": "a campus's own road",
    "way/278139894": "a campus's own road",
    "way/730666968": "a campus's own road",
    "way/1338034236": "a campus's own road",
    "way/1329308293": "a campus's own road",
    "way/1253814667": "a campus's own road",
    "way/1333444508": "a military post's own road",
    "way/294649838": "a military post's own road",
    "way/541912129": "a military post's own road",
    "way/1513018865": "a military post's own road",
    "way/1513018866": "a military post's own road",
    "way/294649835": "a military post's own road",
    "way/294649840": "a military post's own road",
    "way/663124127": "a military post's own road",
    "way/377747303": "a military post's own road",
    "way/513853105": "a station forecourt road",
    "way/1425745271": "a business's own lane",
    "way/1435152136": "a business's own lane",
    "way/1435152137": "a business's own lane",
    "way/515299002": "a business's own lane",
    "way/623967316": "a business's own lane",
    "way/419174237": "a business's own lane",
    "way/1540903853": "a business's own lane",
    "way/1540922596": "a business's own lane",
    "way/1540942757": "a business's own lane",
    "way/1531553475": "a business's own lane",
    "way/1531553478": "a business's own lane",
    "way/1531860364": "a business's own lane",
    "way/1531875725": "a business's own lane",
    "way/1531553476": "a business's own lane",
    "way/1531553477": "a business's own lane",
    "way/1548629693": "a business's own lane",
    "way/1299812263": "a business's own lane",
    "way/433743254": "a business's own lane",
    "way/402820419": "a business's own lane",
    "way/1484584672": "a driving-test course road",
    "way/1484584673": "a driving-test course road",
    "way/1484584674": "a driving-test course road",
    "way/1484584675": "a driving-test course road",
    "way/1484613322": "a driving-test course road",
    "way/1484613323": "a driving-test course road",
    "way/1484613325": "a driving-test course road",
    "way/1484613326": "a driving-test course road",
    "way/1484584663": "a driving-test course road",
    "way/1484584664": "a driving-test course road",
    "way/1484613313": "a driving-test course road",
    "way/1484613314": "a driving-test course road",
    "way/1484613315": "a driving-test course road",
    "way/1484613318": "a driving-test course road",
    "way/1484613319": "a driving-test course road",
    "way/1491796975": "a driving-test course road",
    "way/1491796976": "a driving-test course road",
    "way/1491796977": "a driving-test course road",
    "way/1491796978": "a driving-test course road",
    "way/1484584667": "a driving-test course road",
    "way/1484584668": "a driving-test course road",
    "way/1484584669": "a driving-test course road",
    "way/1484584670": "a driving-test course road",
    "way/1484584671": "a driving-test course road",
    "way/1484584665": "a driving-test course road",
    "way/1484584666": "a driving-test course road",
    "way/1485652908": "a driving-test course road",
    "way/278136544": "a path inside a building",
    "way/1332636377": "a path inside a building",
    "way/1332636380": "a path inside a building",
    "way/1337732171": "a path inside a building",
    "way/1322881946": "a station corridor or platform",
    "way/1322881945": "a station corridor or platform",
    "way/1322881944": "a station corridor or platform",
    "way/1339017223": "a station corridor or platform",
    "way/1339017224": "a station corridor or platform",
    "way/1314357468": "a station corridor or platform",
    "way/1314357469": "a station corridor or platform",
    "way/1314357470": "a station corridor or platform",
    "way/1314357471": "a station corridor or platform",
    "way/676163982": "a station corridor or platform",
    "way/676163984": "a station corridor or platform",
    "way/676163985": "a station corridor or platform",
    "way/676163986": "a station corridor or platform",
    "way/1033747064": "a station corridor or platform",
    "way/676163983": "a station corridor or platform",
    "way/1164056459": "a station corridor or platform",
    "way/1164056461": "a station corridor or platform",
    "way/1164056462": "a station corridor or platform",
    "way/1337116789": "a station corridor or platform",
    "way/474148332": "a station corridor or platform",
    "way/772602543": "a station corridor or platform",
    "way/772602544": "a station corridor or platform",
    "way/832369546": "a station corridor or platform",
    "way/474148333": "a mall link corridor",
    "way/1301665830": "a direction label standing in for a name",
    "way/1066852134": "a direction label standing in for a name",
    "way/1051240453": "a direction label standing in for a name",
    "way/1313247227": "a direction label standing in for a name",
    "way/1313247228": "a direction label standing in for a name",
    "way/1513018850": "a direction label standing in for a name",
    "way/302865682": "a direction label standing in for a name",
    "way/670995380": "a direction label standing in for a name",
    "way/671182530": "a direction label standing in for a name",
    "way/771157290": "a direction label standing in for a name",
    "way/294649848": "a name that says it is temporary",
    "way/1562529892": "a name that says it is temporary",
    "way/665825481": "a name that says it is temporary",
    "way/706947321": "a name that says it is gone",
    "way/917204743": "a name that says it is gone",
    "way/917205214": "a name that says it is gone",
    "way/209985894": "a name that says it is gone",
    "way/209985895": "a name that says it is gone",
    "way/917205911": "a name that says it is gone",
    "way/162337512": "a name that says it is gone",
    "way/446958207": "a name that says it is gone",
    "way/1394460951": "a name that says it is gone",
    "way/595747802": "a description standing in for a name",
    "way/463385826": "a description standing in for a name",
    "way/1479117101": "a description standing in for a name",
    "way/1291912746": "a description standing in for a name",
    "way/1487812935": "a description standing in for a name",
    "way/1487813301": "a description standing in for a name",
    "way/1240645787": "a description standing in for a name",
    "way/329793158": "a description standing in for a name",
    "way/683066915": "a description standing in for a name",
    "way/739801565": "a description standing in for a name",
    "way/967503748": "a description standing in for a name",
    "way/969133367": "a description standing in for a name",
    "way/420457744": "a description standing in for a name",
    "way/420457745": "a description standing in for a name",
    "way/461375866": "a description standing in for a name",
    "way/706719479": "a description standing in for a name",
    "way/1432516382": "a description standing in for a name",
    "way/303164422": "a description standing in for a name",
    "way/626324234": "a description standing in for a name",
    "way/1325597260": "a description standing in for a name",
    "way/541665354": "a second name glued on",
    "way/542202383": "a second name glued on",
    "way/333104279": "a second name glued on",
    "way/281054746": "a stray character in the name",
    "way/183178371": "a stray character in the name",
    "way/256181236": "a stray character in the name",
    "way/50160204": "a typo in the name",
    "way/350915682": "a typo in the name",
    "way/232968836": "an address number standing in for a name",
    "way/366094004": "an address number standing in for a name",
    "way/334181034": "an address number standing in for a name",
    "way/259192895": "an address number standing in for a name",
    "way/272227648": "an address number standing in for a name",
    "way/215225482": "an address number standing in for a name",
    "way/356598065": "an address number standing in for a name",
    "way/573510370": "an address number standing in for a name",
    "way/232968743": "an address number standing in for a name",
    "way/539433327": "a bare type word",
    "way/1319652909": "a bare type word",
    "way/1004711746": "a bare type word",
    "way/1004711923": "a bare type word",
    "way/1004712288": "a bare type word",
    "way/1004713203": "a bare type word",
    "way/1004821522": "a bare type word",
    "way/1004821524": "a bare type word",
    "way/1004821527": "a bare type word",
    "way/1004821528": "a bare type word",
    "way/1004821529": "a bare type word",
    "way/1004821542": "a bare type word",
    "way/1004821543": "a bare type word",
    "way/1004821545": "a bare type word",
    "way/1004821546": "a bare type word",
    "way/1004821806": "a bare type word",
    "way/1004821807": "a bare type word",
    "way/1004821808": "a bare type word",
    "way/1004821809": "a bare type word",
    "way/1004877729": "a bare type word",
    "way/1004877730": "a bare type word",
    "way/1004922694": "a bare type word",
    "way/1004922719": "a bare type word",
    "way/1004924730": "a bare type word",
    "way/1004924731": "a bare type word",
    "way/1004924732": "a bare type word",
    "way/1154900635": "a bare type word",
    "way/1154900636": "a bare type word",
    "way/1157338591": "a bare type word",
    "way/1328589036": "a bare type word",
    "way/1038717168": "a bare type word",
    "way/1089679098": "a bare type word",
    "way/1305890625": "a bare type word",
    "way/284786643": "a bare type word",
    "way/284786840": "a bare type word",
    "way/284786846": "a bare type word",
    "way/284787009": "a bare type word",
    "way/284788832": "a bare type word",
    "way/298032563": "a bare type word",
    "way/362757557": "a bare type word",
    "way/380193208": "a bare type word",
    "way/447640696": "a bare type word",
    "way/556419966": "a bare type word",
    "way/566533959": "a bare type word",
    "way/1061826087": "a bare type word",
    "way/1061826088": "a bare type word",
    "way/1086331957": "a bare type word",
    "way/1086355463": "a bare type word",
    "way/1086355479": "a bare type word",
    "way/1086355483": "a bare type word",
    "way/1086355490": "a bare type word",
    "way/1086470757": "a bare type word",
    "way/1086470777": "a bare type word",
    "way/1086491233": "a bare type word",
    "way/1086491241": "a bare type word",
    "way/1086506512": "a bare type word",
    "way/1086506514": "a bare type word",
    "way/1086506518": "a bare type word",
    "way/1086506522": "a bare type word",
    "way/1086506523": "a bare type word",
    "way/1086579122": "a bare type word",
    "way/1086579170": "a bare type word",
    "way/1086579172": "a bare type word",
    "way/1086695990": "a bare type word",
    "way/1086751415": "a bare type word",
    "way/1086751422": "a bare type word",
    "way/1086751428": "a bare type word",
    "way/804860160": "a bare type word",
}
