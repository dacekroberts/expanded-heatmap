"""Taichung-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/taichung.md,
and the national argument is in taipei.md and pipeline/countries/taiwan.py.

Business leg: the national business tax register (FIA, daily), the rows whose
address is in Taichung, placed by a JOIN to Taichung's own door-plate file -
the only Taiwanese door-plate file that carries WGS84 as well as TWD97.

Rail: the Taichung Metro Green Line - its stations from the operator's own
table (coordinates, Chinese and English names), its route from OpenStreetMap,
because the operator's table has no geometry (ODbL, the Toulouse/Rennes
precedent). TDX is not used (key-gated; taipei.md).
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "taichung" / "raw"
DATA_PROCESSED = ROOT / "data" / "taichung" / "processed"
OUTPUTS = ROOT / "outputs" / "taichung"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

PORTAL = "https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid="
# The door-plate INDEX: one row per monthly file, each a Google Drive link.
# Read it for the newest month; never pin one file id (the brief).
DOORPLATE_INDEX_RID = "03d9c01c-4a7c-4bd8-ae88-12ed011391b3"
DOORPLATE_INDEX_CSV = DATA_RAW / "doorplate_index.csv"
DOORPLATE_CSV = DATA_RAW / "taichung_doorplate.csv"
# Taichung Metro's own Green Line station table (data.gov.tw 144164).
STATIONS_RID = "f9511cc5-4799-4df9-98b7-0b0f89fc2be9"
STATIONS_RAW_CSV = DATA_RAW / "green_line_stations.csv"

# The door-plate file's columns (read 2026-09-23 by the screen).
PLATE_COLS = {"street": "街、路段", "lane": "巷", "alley": "弄", "num": "號",
              "lon": "WGS84經度", "lat": "WGS84緯度"}
# The district, as a CODE (the register names it); step 2 learns code -> name.
PLATE_DISTRICT_COL = "鄉鎮市區代碼"
# The register's address prefixes for Taichung, including the pre-2010
# county's (checked absent 2026-09-23, cheap to keep).
ADDRESS_PREFIXES = ("臺中市", "台中市", "臺中縣", "台中縣")

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
)
# Every name search bounded (osm-rail): the whole special municipality.
OSM_BBOX = (23.99, 120.46, 24.45, 121.46)       # S, W, N, E
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
# No boundary polygon: the whole line is in the city, and the check is the
# operator's own station addresses (every one must start with the city's name).
# Overpass 504ed on the boundary from all three mirrors on 2026-09-25, and the
# build does not need it - the register is scoped by address prefix.

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 51N: the longitude (~120.67) falls in the 120 to 126 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32651"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# One line, the Green Line, Beitun Main Station to HSR Taichung Station, all
# inside the city; every station kept (owner 2026-09-25: a full page).
LINE_KEY = "G"
LINE_NAME = "Green Line"
# The line's two OSM relations (one per direction, 18 stops each) are named
# 臺中捷運綠線…方向; matched on that name within route=subway.
LINE_MATCH = "臺中捷運綠線"
# Neither the operator's table nor OSM carries a colour (2026-09-25), and the
# licence read found none on the dataset pages. A green of this project's own,
# Delta-E 31 from the Personal services pins (owner 2026-09-25, Riga's
# precedent: the project palette); the page says so.
LINE_COLOUR = "#3B7D23"

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "taiwan_fia"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "industry"

# The head-office rule (owner 2026-09-25, as measured on Taipei): a COMPANY
# head-office or single-site row on the 3rd floor or higher, or with a room
# number (室), looks like an office - dropped, unless its address holds this
# many storefront rows or more (a market or a mall).
OFFICE_FLOOR_MIN = 3
OFFICE_EXEMPT_ROWS_AT_ADDRESS = 20

# Sanity bounds for the joined points.
CITY_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602921154)"
# Why the index reaches more than 25 km past the map's stations: read by rule D of
# scripts/check_place_scope.py once that rule lands. Re-measure with --reach if PLACE_AREA changes.
PLACE_SCOPE_REACH_REASON = ("2026-10-13: Taichung's own boundary runs east through Heping District to Nanhu Mountain, 78 km past the nearest station (owner)")
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("zh",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "node/2571583908": "'下段', duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6)",
    "node/2336767670": "'赤嵌頭', duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6)",
    "node/2569663462": "'大坑', duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6)",
    "node/9831175514": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/10804761741": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/10756054548": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/11896360779": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/11896360778": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/11896360780": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/11497259783": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/9831166744": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/11966800250": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "node/11093703448": "a peak carrying a village's name is kept (owner, 2026-10-13)",
    "way/261034490": "'日光郡動態公園', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/261034498": "'日光郡靜態公園', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/590316476": "'西班牙社區 小公園', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/1044441492": "'精銳潮社區公園', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/1370244827": "'富宇大地公園', a park tied to a housing complex only by its name stays (second batch question g); only an estate operator tag drops one (third list rule 3)",
    "way/763051487": "places of worship need no article (NOTABLE_ONLY, 2026-10-07); the tags show a place of worship",
    "way/283040767": "'天主教立德中心', places of worship need no article (NOTABLE_ONLY, 2026-10-07); the tags show a place of worship",
    "way/227105790": "'學生福音中心', places of worship need no article (NOTABLE_ONLY, 2026-10-07); the tags show a place of worship",
    "way/1013434346": "'石頭公園生態休閒農場', a tourism landmark is kept on a Wikidata entry or an article (NOTABLE_ONLY)",
    "node/3933401477": "'鼎財窩', places of worship need no article (NOTABLE_ONLY, 2026-10-07); the tags show a place of worship",
    "way/1305670144": "'外埔環保生態公園（暫時封閉）', a glitched name on a street's only row is not dropped (Onga River, seven rulings entry; no name repair); a place closed for works is kept (owner's two fixes, 2026-10-13)",
    "node/4281388091": "'耶穌基督後期聖徒教會_沙鹿', a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "node/9164530956": "'房福橋', landmarks that stand but are abandoned stay (owner 2026-10-13); a historic site needs no article (NOTABLE_ONLY covers tourism, amenity, aeroway only; SKIP_HISTORIC does not list this kind)",
    "way/219878526": "'海灣樂世界', kept on an article of the object's own (keep beats drop, owner 2026-10-13 #1)",
    "node/10718159601": "'921地震10週年紀念衛星圖根點', statues, monuments and public memorials stay without an article (personal names ruling #2, 2026-10-13; monuments not held to the notable rule)",
    "node/13438012731": "'クラウンIII', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name; a name in another script is left out only where the object has a local name; names are never repaired (_local_first, 2026-10-11)",
    "node/13397643733": "'門衛', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name",
    "node/13397643734": "'引路人', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name",
    "node/13397643736": "'巴比倫塔', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name",
    "node/13397643735": "'王冠峰', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name",
    "node/13397643731": "'將達魯姆', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name",
    "node/13397643730": "'挖嘎奈大折立', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name",
    "node/13397643729": "'女王頭', peaks need no article (NOTABLE_ONLY comment); no rule reads who uses a name",
    "way/519924945": "'北門福德詞', a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "way/519924942": "'文武里福德詞', a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "way/677540100": "'南柳福德祀', a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "興豐山莊": "the description rule never takes a street with a way of residential class or above (street_description; 15 answers #9)",
    "工三南僑": "a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
    "秀山十三": "a misspelled or glitched name is still that place (seven rulings #1; typo line, 2026-10-13)",
}
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/1137163625": "'大眾爺公廟': 大眾爺公廟 with no place (lane 4 borderline read; owner, 2026-10-16)",
    "node/2365711827": "'山神廟': 山神廟 with no place, 55 m from 無極殿 (lane 4 borderline read; owner, 2026-10-16)",
    "node/10128382796": "'山達基台中中心': 山達基台中中心, the body's city centre (lane 4 borderline read; owner, 2026-10-16)",
    "way/346917179": "'耶穌基督後期聖徒教會台中傳道部': 耶穌基督後期聖徒教會台中傳道部, the body's mission office (lane 4 borderline read; owner, 2026-10-16)",
    "relation/7052455": "'耶穌基督後期聖徒教會台中傳道部': the same name on a second building 3.5 km away (branch=南台中支聯會, a stake centre) (lane 4 borderline read; owner, 2026-10-16)",
    "way/388085257": "'慈濟臺中靜思堂': 慈濟臺中靜思堂 (branch=台中分會); the Jing Si Hall call, as in Taipei and Taoyuan (lane 4 borderline read; owner, 2026-10-16)",
    "way/1550474492": "'天晴廣場': 天晴廣場 (lane 4 borderline read; owner, 2026-10-16)",
    "node/9979649824": "'姑婆芋展演廣場': 姑婆芋展演廣場, a performance plaza named for a plant (lane 4 borderline read; owner, 2026-10-16)",
    "way/1163237342": "'平安廣場': 平安廣場 (tagged a park) (lane 4 borderline read; owner, 2026-10-16)",
    "node/4993787239": "'梨蘋廣場': 梨蘋廣場 (lane 4 borderline read; owner, 2026-10-16)",
    "way/1435167885": "'鑑心廣場': 鑑心廣場 (tagged a park) (lane 4 borderline read; owner, 2026-10-16)",
    "way/288595699": "'東光園道': a repeat label of way/288595698 (lane 4 borderline read; owner, 2026-10-16)",
    "way/441786936": "'東光園道': a repeat label of way/288595698 (lane 4 borderline read; owner, 2026-10-16)",
    "way/774649296": "'東光園道': a repeat label of way/288595698 (lane 4 borderline read; owner, 2026-10-16)",
    "way/774649301": "'東光園道': a repeat label of way/288595698 (lane 4 borderline read; owner, 2026-10-16)",
    "way/1320735263": "'21號倉庫': 21號倉庫, one of eight numbered warehouses beside the group's own row 臺中驛第二貨物倉庫群（20號倉庫群） relation/18122072 (lane 4 borderline read; owner, 2026-10-16)",
    "way/1320735262": "'22號倉庫': 22號倉庫 (lane 4 borderline read; owner, 2026-10-16)",
    "way/1320735261": "'23號倉庫': 23號倉庫 (lane 4 borderline read; owner, 2026-10-16)",
    "way/1320735260": "'24號倉庫': 24號倉庫 (lane 4 borderline read; owner, 2026-10-16)",
    "way/1320735259": "'25號倉庫': 25號倉庫 (lane 4 borderline read; owner, 2026-10-16)",
    "way/1320735258": "'26號倉庫': 26號倉庫 (lane 4 borderline read; owner, 2026-10-16)",
    "way/1320731712": "'27號倉庫': 27號倉庫 (lane 4 borderline read; owner, 2026-10-16)",
    "node/8027290610": "'水圳遺址': 水圳遺址 (canal remains), a type phrase as the whole name (lane 4 borderline read; owner, 2026-10-16)",
    "node/3262248716": "'流籠頭': 流籠頭 (cable-car head) (lane 4 borderline read; owner, 2026-10-16)",
    "node/2303353182": "'燒炭窯遺址': 燒炭窯遺址 (charcoal kiln remains) (lane 4 borderline read; owner, 2026-10-16)",
    "node/10050185988": "'索道遺跡': 索道遺跡 (cableway remains) (lane 4 borderline read; owner, 2026-10-16)",
    "node/10050198292": "'索道頭': 索道頭 (cableway head), 200 m from 索道遺跡 (lane 4 borderline read; owner, 2026-10-16)",
    # Same-named objects a drop above made a row (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "node/13529262395": "a same-named object beside a row dropped by id, which that drop made the row: dropped with it under the same ruling (finding 53; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    # Rows the owner's later rulings of 2026-10-13 decide, and the twin checks' drops (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "node/13529262394": "a same-named object beside a row dropped by id, which that drop made the row: dropped with it under the same ruling (finding 53; the twin check; owner 2026-10-13, relayed by Cleanup)",
    # Rows the read-only screen helper gave a drop verdict (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "way/1240365918": "duplicate within 300 m: duplicates of one object; block name (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/1240344546": "duplicate within 300 m: duplicates of one object (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/1240344547": "duplicate within 300 m: duplicates of one object (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/1240347186": "duplicate within 300 m: duplicates of one object; block name (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    # Rows the read-only screen helper gave a drop verdict (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "node/14111447402": "twin of a dropped row: bare type word (flag pass) (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "node/14111447404": "twin of a dropped row: bare type word (flag pass) (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/355264471": "twin of a dropped row: bare type word (flag pass) (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "node/1529078483": "peak named only by a height: rule fault class (still applied by id) (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "node/2503802481": "peak named only by a height: rule fault class (still applied by id) (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/757871190": "stock plaza name: ruling 5 (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/1122944225": "stock plaza name: ruling 5 (the screen helper's verdict; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    # A religious body's meeting halls and branches, and halls named only by a body and a hall type (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "relation/20964791": "a religious body's meeting hall or branch tagged a place of worship is dropped (ruling 2; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "node/12342946147": "a religious body's meeting hall or branch tagged a place of worship is dropped (ruling 2; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/280168181": "a religious body's meeting hall or branch tagged a place of worship is dropped (ruling 2; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/953990971": "a religious body's meeting hall or branch tagged a place of worship is dropped (ruling 2; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/637358826": "a religious body's meeting hall or branch tagged a place of worship is dropped (ruling 2; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    "way/733819888": "a religious body's meeting hall or branch tagged a place of worship is dropped (ruling 2; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    # Stock plaza names with no place in them (the pattern screen of 2026-10-13;
    # data/_search_rollout/reads_rules56/_rulings.md, docs/decisions_drafts/search-final.md).
    "way/544377823": "a stock plaza name with no place in it is dropped (ruling 5 and its follow-up; owner 2026-10-13, the rulings on the full reads applied by the pattern screen)",
    # Bare type words and type phrases (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "node/3222991417": "a bare type word or a type phrase as the whole name is dropped (BARE_TYPE_NAMES, owner 2026-10-11; seven rulings 4, 2026-10-13; owner 2026-10-13, the flag read's verdicts, all approved)",
    # Descriptions, positions and site labels standing in for a name (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "way/628214964": "a description, a position or a site label standing in for a name is dropped (seven rulings 4; owner 2026-10-13, the flag read's verdicts, all approved)",
    "way/697526455": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/878604406": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/936947006": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/550836812": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/586364762": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/303637087": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/589276434": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1063473219": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/337139392": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/553153039": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/557073275": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1169770549": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1431402548": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/1431509551": "a park named by a planning or stage code (owner, 2026-10-13)",
    "relation/8905805": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/340940429": "a park named by a planning or stage code (owner, 2026-10-13)",
    "way/648056196": "a family compound, clan hall or farmhouse ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1230978719": "a family compound, clan hall or farmhouse ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1240674784": "a family compound, clan hall or farmhouse ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/6207210698": "a family compound, clan hall or farmhouse ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/301277274": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1047206985": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1047206997": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1050627211": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1329443898": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1329566406": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1479619646": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1479619647": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1480641359": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896144886": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896144891": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896144892": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896144893": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896144901": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896144904": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896159606": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896159607": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/896172314": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/103544860": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1431706509": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1431706510": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1566726866": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1566726867": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1566726868": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1566726869": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1566726870": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/24378503": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/337701582": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/337701583": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/337701587": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/337701590": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/367396477": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/367396480": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/367396483": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/369375779": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/383939132": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/383939133": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/146337195": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/146337196": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/146337197": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/146337198": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/146337199": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/146337202": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/336263396": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/211849177": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/369375781": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/369375780": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/228487150": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831487": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831490": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831491": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831492": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831503": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831504": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831505": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831508": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831511": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831514": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831515": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1486831518": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/747647529": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/747647530": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/746940109": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/746940110": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/464505239": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/568605058": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/965292535": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/232291593": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/232291594": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891721": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891726": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891729": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891730": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891734": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891736": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891737": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891739": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891740": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/283891742": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/548856166": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/642310189": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309363453": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309866785": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310011186": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310011187": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310011188": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310025339": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310467365": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310467370": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310467371": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310896283": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310896288": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310911254": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/311209198": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/312016463": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/312016464": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313194756": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313208925": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313208927": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313355642": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313355648": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313355649": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313510715": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313510726": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313521437": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313521461": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313521464": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/314528681": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/314528684": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/314805378": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315275494": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315421006": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315421008": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315421041": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315421053": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315730023": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315869813": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315869815": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/315869818": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/316351157": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/316490581": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/316490582": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/316490586": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/316637073": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/316763770": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/316911408": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/317332509": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/317332511": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/317484617": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/317484628": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/323395972": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/323461993": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1018837802": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1192685460": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1192685469": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1192688591": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1192691648": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1192702085": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1192702088": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1192723761": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/572318981": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/572318982": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/586121779": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/588435074": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/588435075": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/603954039": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/603954040": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/641950939": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/641950940": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/308690189": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/308826606": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/308999939": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309032525": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309032532": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309032533": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309032535": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309032536": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309359897": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/309363452": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/310316131": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/312545098": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1551444169": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1551444170": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/680502975": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/802336778": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/802336794": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/878658712": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/878658713": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/949732662": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/949732663": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/949732666": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/949732668": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/949732669": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/949732671": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1214969458": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1214969459": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1551444171": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/802336774": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/802336775": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/802336781": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/949732653": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/949732660": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1153699804": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/442191321": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/269586865": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/810134981": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/316351151": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1357775721": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/772312343": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/772312344": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1103147815": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1103147816": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1159347531": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/417746857": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/623283371": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1025990191": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1053189968": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1134057320": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1304641643": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1304646289": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1313504948": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/545262456": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313943538": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/313943539": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/417755539": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/229032391": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/270043637": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1547140696": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1547140697": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/229032389": "a lane named for its mode or a generic sidewalk name (owner, 2026-10-13)",
    "way/1164511858": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/465216638": "a motorway ramp or interchange, a description (owner, 2026-10-13)",
    "way/584486672": "an estate courtyard tagged a park, English description for a name",
    "way/447947694": "an estate garden tagged a park, stray characters glued on the name",
    "way/596748585": "an estate courtyard tagged a park",
    "node/12608938544": "an estate's name stone tagged a monument",
    "way/873107595": "a religious order's residence with no article",
    "way/255784429": "a seminary with no article, a bare type word for a name",
    "node/9467644899": "a religious residence with no article",
    "way/315710452": "a religious residence with no article",
    "node/2771942345": "a religious residence with no article",
    "node/3993477568": "a religious residence with no article",
    "way/235082930": "a religious residence with no article",
    "way/1177121867": "a religious residence with no article",
    "way/1064302069": "a religious residence with no article",
    "node/13529262392": "a private family graveyard hall with no article",
    "node/8012733550": "a fortune-telling shop tagged a place of worship",
    "node/13307324001": "a temple-supplies shop tagged a place of worship",
    "node/6275626560": "a club's name sign tagged a monument",
    "way/652853354": "a theme park's ride; the article and wikidata are the park's",
    "way/1202342705": "a land-management contract and its dates standing in for a name",
    "way/1111663477": "a description standing in for a name",
    "node/13812682720": "a description standing in for a name",
    "way/472434989": "a description standing in for a name",
    "way/677269927": "a school's tennis court tagged a park",
    "way/1051186692": "a school's sports ground tagged a park",
    "way/313817354": "a school's practice field tagged a park",
    "way/1177185588": "a croquet court tagged a park",
    "way/316490599": "a description of an abandoned building standing in for a name",
    "node/11622474587": "a description of an abandoned farmhouse standing in for a name",
    "node/7913261874": "a description of an abandoned lookout standing in for a name",
    "way/355264470": "museum contents, a description for a name",
    "way/355264472": "museum contents, a description for a name",
    "node/4560301918": "a display train car with no wikidata, misspelled name",
    "node/14111447403": "a bare English type word, an exhibit with no article",
    "node/14111427565": "a plaque with no article, a bare English type word",
    "node/13608966396": "a campsite's name sign tagged a monument",
    "node/13463177463": "a park's name sign tagged a monument",
    "node/13341560911": "a survey mark, a type word for a name",
    "node/2651899973": "a survey mark, a type word and code for a name",
    "node/12541185954": "a description of a trial dig standing in for a name",
    "node/11425383092": "a teaching traffic signal, a description for a name, not a junction",
    "node/14188067111": "a vandalised name",
    "node/13729110241": "a joke entry tagged a place of worship",
    "node/8124716274": "a joke entry tagged a place of worship",
    "way/568973023": "a cut name",
    "node/6033486093": "an address number glued on the name",
    "node/3876397374": "a heritage grade glued on the name",
    "node/10605756630": "a joke name on a locality",
    "relation/4870087": "a name that says the thing is gone",
    "node/5095177073": "public art with no Wikipedia article of its own",
    "way/506832155": "a duplicate station row, the station building beside the station node",
    "way/1145589752": "a route name with a date and a contributor note glued on",
    "way/897246263": "a route name with a date and a contributor note glued on",
    "way/897246264": "a route name with a date and a contributor note glued on",
    "way/1192688584": "a facility's own road",
    "way/1192688585": "a facility's own road",
    "way/603953115": "a facility's own road",
    "way/877354323": "a facility's own road",
    "way/877354324": "a facility's own road",
    "way/1068481135": "a facility's own road",
    "way/874959784": "a facility's own road",
    "way/877354316": "a facility's own road",
    "way/874982890": "a facility's own road",
    "way/877354321": "a facility's own road",
    "way/1373253556": "a facility's own road",
    "way/513509678": "a facility's own road",
    "way/513509681": "a facility's own road",
    "way/1307191263": "a facility's own road",
    "way/1068195024": "a facility's own road",
    "way/177524023": "a facility's own road",
    "way/1047453150": "a facility's own road",
    "way/515714956": "a facility's own road",
    "way/886577656": "a facility's own road",
    "way/1329443890": "a facility's own road",
    "way/1329566412": "a facility's own road",
    "way/659704405": "a facility's own road",
    "way/1330423345": "a facility's own road",
    "way/1338928888": "a facility's own road",
    "way/1426611540": "a facility's own road",
    "way/1514602987": "a facility's own road",
    "way/1531872009": "a facility's own road",
    "way/920149793": "a facility's own road",
    "way/951232482": "a facility's own road",
    "way/959922673": "a facility's own road",
    "way/979849819": "a facility's own road",
    "way/1136248904": "a facility's own road",
    "way/877354328": "a facility's own road",
    "way/877354329": "a facility's own road",
    "way/406143321": "a facility's own road",
    "way/578229562": "a facility's own road",
    "way/1013479900": "a facility's own road",
    "way/926268032": "a facility's own road",
    "way/382892404": "a direction label standing in for a name",
    "way/382892405": "a direction label standing in for a name",
    "way/382892406": "a direction label standing in for a name",
    "way/405699737": "a direction label standing in for a name",
    "way/1075773997": "a direction label standing in for a name",
    "way/958562782": "an address number standing in for a name",
    "way/609207480": "an address number standing in for a name",
    "way/303906307": "an address number standing in for a name",
    "way/313373000": "an address number standing in for a name",
    "way/292862853": "an address number standing in for a name",
    "way/1182155269": "an address number standing in for a name",
    "way/1014958006": "an address number standing in for a name",
    "way/1119998037": "a name that says the thing is gone",
    "way/1119998039": "a name that says the thing is gone",
    "way/1119998041": "a name that says the thing is gone",
    "way/1119998044": "a name that says the thing is gone",
    "way/415752087": "a name that says the thing is gone",
    "way/1163005581": "a temporary way",
    "way/1163005611": "a temporary way",
    "way/1222030824": "a temporary way",
    "way/1222030825": "a temporary way",
    "way/1232537321": "a temporary way",
    "way/433775844": "a description standing in for a name",
    "way/331774727": "a description standing in for a name",
    "way/919998793": "a description standing in for a name",
    "way/573463470": "a description standing in for a name",
    "way/1432522662": "a description standing in for a name",
    "way/1138184912": "a description standing in for a name",
    "way/1308066511": "a description standing in for a name",
    "way/617142815": "a description standing in for a name",
    "way/1182627693": "a description standing in for a name",
    "way/1182627694": "a description standing in for a name",
    "way/1182627696": "a description standing in for a name",
    "way/1182627697": "a description standing in for a name",
    "way/1182627698": "a description standing in for a name",
    "way/1182627699": "a description standing in for a name",
    "way/1182627700": "a description standing in for a name",
    "way/1182627701": "a description standing in for a name",
    "way/1182627702": "a description standing in for a name",
    "way/1182627703": "a description standing in for a name",
    "way/1182629977": "a description standing in for a name",
    "way/1182629978": "a description standing in for a name",
    "way/1182629982": "a description standing in for a name",
    "way/1363515652": "a description standing in for a name",
    "way/1363515654": "a description standing in for a name",
    "way/1125558064": "a glitched name: code or cut name",
    "way/638737207": "a glitched name: code or cut name",
    "way/320974574": "a glitched name: code or cut name",
    "way/241896777": "a glitched name: code or cut name",
    "way/577637244": "a glitched name: English or a second name glued on",
    "way/216648103": "a glitched name: English or a second name glued on",
    "way/240795026": "a glitched name: English or a second name glued on",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "way/1324078541": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/8359194827": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/1624942562": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/2973906486": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/355264459": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/1054320949": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/14069922987": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/1190964483": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/4634894807": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/5237866663": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/6877309496": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/12119965116": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/7846571936": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/368060945": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/4838178487": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/296373875": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/211870616": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/1083194425": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/1619699653": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/2272870154": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/3508125754": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/6162415185": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "node/11361162376": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/1190964479": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/651505434": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/765573770": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/779443581": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1289338303": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1289327423": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/780115256": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/761120587": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/311369055": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/346472117": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/470653317": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/547179627": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1064302072": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/285606068": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/288270210": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1493097943": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1493869293": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/704223425": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1432522663": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "relation/14039124": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/733785896": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/13947970359": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/930881775": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/630831890": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/930882081": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/303274462": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1373674203": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1191260618": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/244259464": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/9329796854": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "relation/10116534": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/880035413": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1068687233": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/527008399": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/5692713862": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/1299160930": "a code beside a type word is no name (CODED_TYPE, owner 2026-10-12; Ostia plot codes, 15 answers #8); held rows settled 2026-10-13",
    "way/1299160931": "a code beside a type word is no name (CODED_TYPE, owner 2026-10-12; Ostia plot codes, 15 answers #8); held rows settled 2026-10-13",
    "way/1299160932": "a code beside a type word is no name (CODED_TYPE, owner 2026-10-12; Ostia plot codes, 15 answers #8); held rows settled 2026-10-13",
    "way/1067149188": "a code beside a type word is no name (CODED_TYPE, owner 2026-10-12; Ostia plot codes, 15 answers #8); held rows settled 2026-10-13",
    "node/3655363402": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/2575970216": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/2575970111": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/6207209960": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/2336767666": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/2572352929": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/2575970133": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/6207210155": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/6207210700": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "node/6207210712": "a code beside a type word is no name (CODED_TYPE, owner 2026-10-12; Ostia plot codes, 15 answers #8); held rows settled 2026-10-13",
    "node/6207210711": "a code beside a type word is no name (CODED_TYPE, owner 2026-10-12; Ostia plot codes, 15 answers #8); held rows settled 2026-10-13",
    "node/6207209958": "a code beside a type word is no name (CODED_TYPE, owner 2026-10-12; Ostia plot codes, 15 answers #8); held rows settled 2026-10-13",
    "node/2572352924": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2573120005": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2573120036": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2593999786": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2593999858": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2593999869": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2593999876": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571583892": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571583912": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571583921": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571583932": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571583953": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571583958": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571584021": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571583949": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/2571584100": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "node/6207209952": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); held rows settled 2026-10-13",
    "way/227075002": "an office or other non-worship building tagged a place of worship is dropped (settled call of the Anyang and Gwangju reads, search-final 2026-10-13); held rows settled 2026-10-13",
    "way/227103239": "an office or other non-worship building tagged a place of worship is dropped (settled call of the Anyang and Gwangju reads, search-final 2026-10-13); held rows settled 2026-10-13",
    "node/6174488233": "an office or other non-worship building tagged a place of worship is dropped (settled call of the Anyang and Gwangju reads, search-final 2026-10-13); an organization's name standing in for the hall's own is dropped (seven rulings #7, Yamagata); held rows settled 2026-10-13",
    "way/326739565": "a business with nothing else is dropped; a place named for a business (LEAK rule, 2026-10-08); held rows settled 2026-10-13",
    "node/14148572331": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); a description standing in for a name is dropped (settled call of the reads; seven rulings #4; Ostia finds named by location, 15 answers #8); held rows settled 2026-10-13",
    "way/624150383": "a park tag on a pool, club, office or other non-park is a by-id drop (third list candidate 15, narrow version); held rows settled 2026-10-13",
    "way/1064264445": "a description standing in for a name is dropped (settled call of the reads; seven rulings #4; Ostia finds named by location, 15 answers #8); held rows settled 2026-10-13",
    "node/5574016321": "bare type word or type phrase as the whole name, no article of its own (BARE_TYPE_NAMES; owner 2026-10-11; seven rulings #4, 2026-10-13); held rows settled 2026-10-13",
    "way/578867199": "Chinese shrine type word as the whole name is a bare type word (candidate 19, third pass, owner 2026-10-13); held rows settled 2026-10-13",
    "way/1231877024": "a minor-way street named by a description or a bare type or way word is dropped (street_description; six answers #3); held rows settled 2026-10-13",
    "way/406151656": "a minor-way street named by a description or a bare type or way word is dropped (street_description; six answers #3); held rows settled 2026-10-13",
    "way/510335941": "a minor-way street named by a description or a bare type or way word is dropped (street_description; six answers #3); held rows settled 2026-10-13",
    "way/358583410": "a street whose every way is private is dropped outside the three switched cities (owner 2026-10-13, private streets #3; per-city switch entry); held rows settled 2026-10-13",
    "way/922858578": "a street whose every way is private is dropped outside the three switched cities (owner 2026-10-13, private streets #3; per-city switch entry); held rows settled 2026-10-13",
    "way/922858579": "a street whose every way is private is dropped outside the three switched cities (owner 2026-10-13, private streets #3; per-city switch entry); held rows settled 2026-10-13",
    "way/1338577862": "a street whose every way is private is dropped outside the three switched cities (owner 2026-10-13, private streets #3; per-city switch entry); held rows settled 2026-10-13",
    "way/1338577863": "a street whose every way is private is dropped outside the three switched cities (owner 2026-10-13, private streets #3; per-city switch entry); held rows settled 2026-10-13",
    "way/1338577864": "a street whose every way is private is dropped outside the three switched cities (owner 2026-10-13, private streets #3; per-city switch entry); held rows settled 2026-10-13",
    "way/1338577865": "a street whose every way is private is dropped outside the three switched cities (owner 2026-10-13, private streets #3; per-city switch entry); held rows settled 2026-10-13",
    "way/24289092": "motorway ramps and interchange labels are dropped (14 answers #2; street_never); held rows settled 2026-10-13",
    "way/45556676": "motorway ramps and interchange labels are dropped (14 answers #2; street_never); held rows settled 2026-10-13",
    "way/60444893": "motorway ramps and interchange labels are dropped (14 answers #2; street_never); held rows settled 2026-10-13",
    "way/60444894": "motorway ramps and interchange labels are dropped (14 answers #2; street_never); held rows settled 2026-10-13",
    "node/2571584094": "duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M; second nodes of one name dropped, six answers #6); the same-named twin of node/2571583892, a row once that id was dropped; held rows settled 2026-10-13",
}
# Kept by id: admitted as rows although a rule passes them over (owner, 2026-10-13;
# docs/decisions_drafts/search-final.md).
PLACE_KEPT = {
    "way/560332944": "'審計新村', a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
