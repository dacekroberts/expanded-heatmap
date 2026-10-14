"""Nagasaki-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; the brief is docs/build_briefs/nagasaki.md
(12/12 checks, 2026-10-02). Built in the 2026-10-01 Japanese batch, on the
shared modules (pipeline/countries/japan*.py): the owner's shape (b)
(2026-10-02, "nagasaki b"), Tokyo's precedent of a frozen part beside a
current whole.

Business leg: the city's lists on BODIK (CC BY 4.0), a SNAPSHOT: every food
permit in force on 2023-06-30 (the national 推奨データセット schema, its
緯度 / 経度 empty on every row) and its barbers, beauty salons and laundries to
2023-03-31; PLUS MHLW's 食品衛生申請等システム open data, current (opt-in, field
by field), which carries the permits filed since. A premises in both is shown
once (config.SUPERSEDES). All placed by a JOIN to MLIT's 位置参照情報 for the
one municipality (no wards); where the block join misses an MHLW row, MHLW's
own point (OWN_POINT_FALLBACK). The city's own 2026 list (64426.xlsx) is NOT
permitted without the city's permission (its site default reserves all
rights): measured for the brief, never read here.

Rail: MLIT N02-25 (not GTFS, not OSM), stations kept only inside the city line
(N03). Nagasaki Electric Tramway and JR Kyushu's Nagasaki Line. English station
names from OpenStreetMap's name:en.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "nagasaki" / "raw"
DATA_PROCESSED = ROOT / "data" / "nagasaki" / "processed"
OUTPUTS = ROOT / "outputs" / "nagasaki"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs (all keyless; downloaded by fetch_sources.py) ---------------

NAME = "Nagasaki"
SLUG = "nagasaki"
MUNICIPALITY = "長崎市"
PREFECTURE = "長崎県"

# BODIK (data.bodik.jp), each dataset license_id cc-by-40-intl under the
# city's catalogue terms (odcs.bodik.jp/422011/tos/, 長崎市オープンデータ利用規約).
# Uploaded 2025-03-27 and not updated since; the upload is not the as-of.
_BODIK = "https://data.bodik.jp/dataset"
MHLW_TOP = "https://i2fas.mhlw.go.jp/"
SOURCE_FILES = {
    "food": ("422011_food_business_all.csv",
             f"{_BODIK}/4d70b9d1-9885-4045-9f59-9d1b99e02910/resource/1125a70b-ac9d-49f6-ba87-1011d0db4f1a"
             "/download/422011_food_business_all.csv", f"{_BODIK}/422011_food_business_all"),
    "mhlw": ("42201_food_business_all.csv",
             "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=42201_food_business_all.csv",
             MHLW_TOP),
    "barber": ("422011_riyosho_all.csv",
               f"{_BODIK}/ab4e452b-c72a-49f4-9b25-0379893cce3f/resource/6ccea115-9386-462c-b581-d1d959f16744"
               "/download/422011_riyosho_all.csv", f"{_BODIK}/422011_riyosho_all"),
    "beauty": ("422011_biyosho_all.csv",
               f"{_BODIK}/9508163b-44a6-4356-abb3-b631b1e4ef72/resource/7d5b0ea8-048e-4534-a8ed-bf9f772c958f"
               "/download/422011_biyosho_all.csv", f"{_BODIK}/422011_biyosho_all"),
    "laundry": ("422011_cleners_all.csv",
                f"{_BODIK}/ea649bea-a49f-4ddc-b1a1-2f55f6f6e8c0/resource/fb933c7e-f41a-4b52-8582-039390d66865"
                "/download/422011_cleners_all.csv", f"{_BODIK}/422011_cleners_all"),
}
# Dated from the rows (the brief's correction of the screen; Kyoto's rule: the
# date the list covers, never the upload's): the food list's newest 許可年月日
# is 2023-06-30 and every 許可満了日 is that date or later, a snapshot of the
# permits in force then; the personal lists' newest 確認年月日 2023-02-06,
# 2023-03-31 and 2023-03-29, dated to the end of that March. MHLW's monthly
# file states none.
SOURCE_AS_OF = {"food": "2023-06-30", "mhlw": None, "barber": "2023-03-31", "beauty": "2023-03-31",
                "laundry": "2023-03-31"}
FOOD_AS_OF = SOURCE_AS_OF["food"]
SOURCES = {k: v[0] for k, v in SOURCE_FILES.items()}
# Declared, never inferred: BODIK's are UTF-8 CSV (one quoted food field holds
# a line break); MHLW's is UTF-8 with a BOM.
SOURCE_ENCODING = {"food": "utf-8", "mhlw": "utf-8-sig", "barber": "utf-8", "beauty": "utf-8",
                   "laundry": "utf-8"}
# The columns each file must carry; fetch_sources.py and step 2 stop on a
# header without them. NO list here names an individual operator (BODIK's
# carry 法人名 only, as MHLW's and Tokyo's national-schema lists do), so the
# name rule cannot run on any Nagasaki row (Tokyo's and Fukuoka's precedent;
# the page says so). Never selected: 施設電話番号, 連絡先メールアドレス,
# 連絡先FormURL, 郵便番号, 法人名, 法人番号, 備考, and MHLW's 法人名 / 法人番号 /
# 法人住所 / phones.
_REGISTER = ("施設名称", "所在地_連結表記", "業務種別")
REQUIRED_COLUMNS = {
    "food": ("施設名称", "営業の種類", "業態", "所在地_連結表記", "許可満了日"),
    "mhlw": ("営業施設名称、屋号又は商号", "営業の種類", "業態", "営業施設所在地", "緯度", "経度", "申請区分",
             "廃業年月日", "法人名"),
    "barber": _REGISTER,
    "beauty": _REGISTER,
    "laundry": _REGISTER,
}
# As Fukuoka's and Hiroshima's (owner-approved wording, 2026-09-24): MHLW
# publishes an address only where the filer agreed to it.
ADDRESS_BY_CONSENT = {"mhlw"}
# Where the block join misses an MHLW row, MHLW's own point places it (the
# brief's check: a median 33 m from the block point, 95.9% within 250 m).
OWN_POINT_FALLBACK = {"mhlw"}
# One premises in both lists: the snapshot's row goes, MHLW's current one
# stays (the brief: 1,145 of MHLW's 1,654 block-placed restaurants share a
# block and trade name with the snapshot, its new-law rows being the same
# filings).
SUPERSEDES = {"mhlw": ("food",)}


def source_csv(key):
    return DATA_RAW / SOURCES[key]


# MLIT 位置参照情報, block (24.0a) and town-chōme (19.0b), for 42201.
ISJ_DIR = DATA_RAW / "isj"

# OpenStreetMap: station names only (name, name:en), and the tram's stops
# (railway=tram_stop, which the station query does not take). Which stations
# exist is N02's; OSM supplies the English display name.
# S, W, N, E: the city's N03 extent, rounded out; step 1 stops if the city
# leaves it.
OSM_BBOX = (32.53, 129.53, 32.98, 130.01)
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"
TRAM_OSM_JSON = DATA_RAW / "osm_tram_stop_names.json"
OSM_NAME_MATCH_M = 600
# N02's name -> OSM's (2026-10-02): OSM adds the stop's former name in
# brackets to five stops (平和公園 (松山町)) and writes 大浦海岸通 with り.
OSM_NAME_ALIASES = {
    "平和公園": "平和公園 (松山町)", "原爆資料館": "原爆資料館 (浜口町)", "めがね橋": "めがね橋 (賑橋)",
    "新地中華街": "新地中華街 (築町)", "崇福寺": "崇福寺 (正覚寺下)", "大浦海岸通": "大浦海岸通り",
}
OSM_NAME_EN_TIES = {}
# 八千代町: no OSM object in either query (2026-10-02); the operator's stop
# table (naga-den.com/pages/9/, stop 26) signs it "Yachiyo-machi".
OSM_NAME_EN_MISSING = {"八千代町": "Yachiyo-machi"}
# Cited overrides of OSM's name:en ({ja: en}, the OSM spelling replaced in a
# comment), in Hiroshima's style (2026-09-30): no macrons, 前 as -mae. OSM,
# like the operator's own stop table, TRANSLATES 13 stops (Fukuoka's trap):
# each is romanised here. スタジアムシティノース / サウス and メディカルセンター
# are English words in katakana and keep OSM's spelling.
OSM_NAME_EN_OVERRIDES = {
    "長崎大学": "Nagasaki-daigaku",             # Nagasaki University
    "平和公園": "Heiwa-koen",                   # Peace Park (Matsuyama-machi)
    "原爆資料館": "Genbaku-shiryokan",           # Atomic Bomb Museum (Hamaguchi-machi)
    "大学病院": "Daigaku-byoin",                # University Hospital (Daigakubyoin-mae)
    "浦上駅前": "Urakami-ekimae",               # Urakami Station (Urakamieki-mae)
    "長崎駅前": "Nagasaki-ekimae",              # Nagasaki Station
    "新地中華街": "Shinchi-chukagai",           # Shinchi Chinatown (Tsuki-machi)
    "崇福寺": "Sofukuji",                       # Sofukuji Temple (Shokakuji-shita)
    "めがね橋": "Meganebashi",                  # Meganebashi Bridge (Nigiwaibashi)
    "市役所": "Shiyakusho",                     # City Hall
    "諏訪神社": "Suwa-jinja",                   # Suwajinja Shrine
    "大浦天主堂": "Oura-tenshudo",              # Oura Cathedral
    "浦上車庫": "Urakami-shako",                # Urakami Tram Depot
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 52N: the longitude (~129.87) falls in the 126 to 132 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
# HALVED, on the spacing rule (docs/ring_rules.md: the halved edges where the
# median station gap is about 550 m or less): step 1 measured 219 m among the
# 43 in-city stations, 38 of them tram stops (2026-10-02), the closest-set
# network in Japan so far (Hiroshima 357 m, Matsuyama 374 m).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# Gate 1's floor: Hiroshima's, Matsuyama's, Paris's and Riga's 200 m, not a
# new number - a tram network is genuinely closer than 400 m (collapsed median
# 219 m; platforms 195 m).
SPACING_MIN_M = 200.0

# --- Station scope ----------------------------------------------------------
# Every N02 line with a station inside the city line (stub_test on N02-25,
# 2026-10-02: 6 legal lines, no Shinkansen; 長崎 on the 西九州新幹線 is dropped
# and stays a JR station): the tram's five sections (all wholly inside) and
# JR Kyushu's Nagasaki Main Line (5 of 41: 長崎, 浦上, 西浦上, 現川, 肥前古賀),
# cut at the city line (owner 2026-09-24); 道ノ尾 is 33 m outside, in 長与町.
LEFT_OUT_LINES = {}
COLLAPSE_MAX_SPREAD_M = 300

# key -> the N02 track it is drawn from, its real public name (English, then
# Japanese), the operator's hue (`hue`, where scripts/line_colour_search.py
# starts) and the project's colour. N02 files the tram under five LEGAL
# sections (本線, 赤迫支線, 桜町支線, 蛍茶屋支線, 大浦支線), all wholly inside the
# city, that no rider reads; the operator runs routes 1 (赤迫 to 崇福寺), 3
# (赤迫 to 蛍茶屋) and 5 (石橋 to 蛍茶屋) over them (route 4 suspended), which
# share most of their track. Drawn as ONE line under the operator's name,
# Matsuyama's precedent (2026-10-02).
_ND, _JK = "長崎電気軌道", "九州旅客鉄道"
LINES = {
    "TR": {"n02": [(_ND, "本線"), (_ND, "赤迫支線"), (_ND, "桜町支線"), (_ND, "蛍茶屋支線"), (_ND, "大浦支線")],
           "name": "Nagasaki Electric Tramway", "name_ja": "長崎電気軌道", "short": "Nagasaki Tram",
           "hue": "#00A0E9"},
    "JN": {"n02": [(_JK, "長崎線")], "name": "JR Nagasaki Main Line", "name_ja": "長崎本線", "short": "JR",
           "hue": "#E60012"},
}
# Colours: the project's own, from `python scripts/line_colour_search.py
# nagasaki` (2026-10-02, defaults: >= 18 within 500 m, >= 10 city-wide): each
# the feasible colour nearest its operator's hue that reads 3:1 on both map
# pages and clears CIE76 45 from every pin. The pair differs by 129.6; the
# dark-mode labels separate, 2 of 2.
_COLOURS = {"TR": "#08A0C0", "JN": "#E80010"}
for _k, _v in LINES.items():
    _v["colour"] = _COLOURS.get(_k, _v["hue"])
LINE_ORDER = list(LINES)
LINE_NAMES = {k: v["name"] for k, v in LINES.items()}
BRANCHES = {}
# Gate 3: the operator's own stop table (naga-den.com/pages/9/, read
# 2026-10-02) lists 38 stops, numbered 11 to 51, 市役所 twice (one platform
# per route) and 昭和町通 among them, against the collapsed set. It writes
# スタジアムシティノース and スタジアムシティサウス (stops 24 and 25) in
# half-width katakana, which is why the brief's search counted 36: reconciled,
# 38 = N02's 38. The JR line the city line cuts has no in-city count.
GATE3 = {"source": "Nagasaki Electric Tramway's stop table (naga-den.com/pages/9/)", "lines": {"TR": 38}}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "japan_eigyo"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "permit_type"

# Sanity bounds for the joined points: the city's N03 extent, rounded out.
NAGASAKI_BBOX = {
    "lat_min": OSM_BBOX[0],
    "lat_max": OSM_BBOX[2],
    "lon_min": OSM_BBOX[1],
    "lon_max": OSM_BBOX[3],
}
CITY_BBOX = NAGASAKI_BBOX

# Trade names read by eye as a person's own name and nothing else, on
# surnames the sign rule's list does not hold (owner, 2026-10-12: the
# sweep of every Japanese city, borderline readings included). KEYS, never
# names (pipeline/name_keys.py, over japan_register._name_key of the name).
PERSON_NAMED = (
    "98ea73c2785a506c",
)

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3604011885)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ja",)
PLACE_FOLD = "ja"
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "旧上海銀行長崎支店記念館": "a museum in a former bank branch (tourism=museum, wikidata); tags read 2026-10-13",
}
# Dropped by id on the full read of 2026-10-13 under the owner's rulings of the
# same day, each id read with its cached name (docs/decisions_drafts/search-rollout.md).
PLACE_DROPPED = {
    # station not: dropped in the full read (owner, 2026-10-13)
    "node/13589111881": "'２階のりば': \"2nd floor boarding point\": a landing of the Glover Sky Road inclined lift (location read from the coordinates, not a tag), tagged railway=station; five such rows within 100 m (full read, station not)",
    "node/13589111880": "'３階のりば': \"3rd floor boarding point\": lift landing, as above (full read, station not)",
    "node/13589111862": "'4階のりば': \"4th floor boarding point\": lift landing, as above (full read, station not)",
    "node/5825876719": "'5階のりば': \"5th floor boarding point\": lift landing, as above (full read, station not)",
    "node/3971461428": "'First floor': \"First floor\": lift landing, as above; English description as the name (full read, station not)",
    # station ride: dropped in the full read (owner, 2026-10-13)
    "node/12833741145": "'坑外停留所': stop of the Ikeshima coal mine tour trolley (network tag), a visitor ride inside a closed mine, not public transport (full read, station ride)",
    "node/13203819348": "'坑道奥部停留所': stop of the Ikeshima coal mine tour trolley, as above (full read, station ride)",
    # description: dropped in the full read (owner, 2026-10-13)
    "way/921231168": "'Lourdes apparitions': English phrase for an event (the Lourdes apparitions) on a leisure=park way; no Japanese name (full read, description)",
    "node/8670287395": "'長崎西国三十三ヶ所第六番霊場': \"Nagasaki Saigoku 33, station no. 6\": a pilgrimage number as the name, 10 m from 準提観音堂, the same object (full read, description)",
    "node/8522889970": "'222M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421889994": "'235M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421837130": "'258M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421837132": "'264M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421889995": "'269M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421837131": "'285M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421837129": "'288M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421891225": "'296M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421891226": "'299M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8430869120": "'300M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421837133": "'308M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8430863016": "'321M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8444267981": "'328M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8422054828": "'344M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8430869121": "'352M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8430869124": "'363M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8422054895": "'364M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421891266": "'365M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8430869117": "'371M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421837134": "'408M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421837135": "'415M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    "node/8421889993": "'494M': the name is the summit height alone (ele tag carries the same figure); natural=peak with no name of its own (full read, description)",
    # bare type: dropped in the full read (owner, 2026-10-13)
    "way/726601264": "'第1公園': \"Park No. 1\": a number and the type word, no place name; five of them and 近隣公園 in one housing area (full read, bare type)",
    "way/726601266": "'第2公園': \"Park No. 2\", as above (full read, bare type)",
    "way/726601166": "'第3公園': \"Park No. 3\", as above (full read, bare type)",
    "way/726601147": "'第4公園': \"Park No. 4\", as above (full read, bare type)",
    "way/726606597": "'第5公園': \"Park No. 5\", as above (full read, bare type)",
    "way/726601260": "'近隣公園': \"neighbourhood park\", the planning class of park as the whole name (full read, bare type)",
    "node/12833647798": "'観音堂': Kannon hall under its type alone (full read, bare type)",
    "node/8703317304": "'虚空蔵菩薩': a bodhisattva's name alone (rule has 文殊菩薩) (full read, bare type)",
    "node/8631608084": "'大山祇大神': a deity's name alone (Oyamatsumi), wayside shrine (full read, bare type)",
    "node/8499751046": "'山大神': \"mountain god\", wayside shrine under the deity's title alone (full read, bare type)",
    "way/766193659": "'七面堂': Shichimen hall under its type alone, same family as 大師堂 in the rule (full read, bare type)",
    "node/12833589536": "'龍神のほこら': \"the dragon god's little shrine\": a description, and 祠 is a rule word (full read, bare type)",
    "node/13651317328": "'織部灯籠': \"Oribe lantern\", a style of stone lantern (rule has 灯籠), tagged historic=monument (full read, bare type)",
    "way/804926285": "'シックナー': \"thickener\", a piece of mine plant under its type alone (full read, bare type)",
    # worship body: dropped in the full read (owner, 2026-10-13)
    "way/721182768": "'創価学会\u3000長崎平和会館': Soka Gakkai hall: the body's name plus \"Nagasaki Peace Hall\"; the rule lists 創価学会 but 会館 is not a hall word, and the name has a full-width space (full read, worship body)",
    "way/714959019": "'真如苑 長崎支部': Shinnyo-en \"Nagasaki branch\": a body's branch office, no religion tag (full read, worship body)",
    # duplicate: dropped in the full read (owner, 2026-10-13)
    "node/3828906061": "'深祟寺': same temple as 深崇寺 way/717026793 at the same point, with the middle character mistyped (full read, duplicate)",
    "way/1174875329": "'原爆落下中心碑': the hypocenter monument again, 10 m from 爆心地碑 way/375933470; its wikidata Q488 is the bombing's, not the monument's (full read, duplicate)",
    # vanished: dropped in the full read (owner, 2026-10-13)
    "node/1423807344": "'活水女子大学\u3000戸町キャンパス\u3000跡地': \"former site of the Kwassui Women's University Tomachi campus\": a gone object, MLIT import node retagged historic=ruins (full read, vanished)",
    "way/832757134": "'長崎北徳洲会病院': a hospital that moved, tagged historic=ruins; business, and its site is the next row (full read, vanished)",
    "way/832757135": "'長崎北徳洲会病院\u3000跡地': \"former site\" of the same hospital, 30 m away (full read, vanished)",
    # unsure in the full read, dropped by ruling 3: a hall named only for what it enshrines, or a deity's title alone (owner, 2026-10-13)
    "node/8689377669": "'天地神明': 天地神明, a dedication alone (deity titles alone fall under ruling 3) (unsure in the full read; ruling 3)",
    "node/8449085251": "'八天狗': 八天狗, named only for what it enshrines (unsure in the full read; ruling 3)",
    "node/8670288823": "'準提観音堂': 準提観音堂, a hall named only for the Kannon form it enshrines (my reading) (unsure in the full read; ruling 3)",
    # unsure in the full read, dropped by ruling 9: one bay or sea labeled many times, one row stays (owner, 2026-10-13)
    "node/5461068827": "'長崎港': 長崎港 labeled again; the harbour's own relation/9381185 stays (unsure in the full read; ruling 9)",
    "node/5461085980": "'長崎港': 長崎港 labeled again; the harbour's own relation/9381185 stays (unsure in the full read; ruling 9)",
    # duplicate: the pair's English-only row goes, the row with the local-language name stays (owner, 2026-10-13)
    "node/6380332923": "'Sanno Shrine': the English-only twin of 山王神社（被爆クスノキの在る神社） (node/4448589490, 15 m), which stays as the row with the Japanese name",
    "node/6380332926": "'Twenty-Six Martyrs Museum': the English-only twin of 日本二十六聖人記念館 (node/1423804998, 45 m), which stays as the row with the Japanese name",
    # the sea-crossing street row (owner, 2026-10-13)
    "way/673930211": "'国道499号（海上区間）': the sea section of National Route 499, drawn highway=planned: no road to find",
}
