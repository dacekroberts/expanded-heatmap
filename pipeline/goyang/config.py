"""Goyang-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; generated from Incheon's config (the
Korean pattern: SEMAS's register, OSM rail on Busan's step 1). One of the
Gyeonggi satellites (owner, 2026-09-28: Goyang, Seongnam and Yongin first; one
page each, 2026-09-29).
"""

from pathlib import Path

from pipeline import line_registry

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "goyang" / "raw"
DATA_PROCESSED = ROOT / "data" / "goyang" / "processed"
OUTPUTS = ROOT / "outputs" / "goyang"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
RAIL_LINES_JSON = DATA_PROCESSED / "rail_lines.json"

# --- The register ----------------------------------------------------------
#
# SEMAS's 상가(상권)정보 (data.go.kr 15083033), read through
# pipeline/countries/korea_sbiz.py from the country cache (owner, 2026-09-29,
# for Incheon and the Gyeonggi satellites): the national LOCALDATA API needs a
# Korean identity check, and the city's own files are not a register
# (docs/build_briefs/gyeonggi.md).
SEMAS_SIDO = "경기도"
SEMAS_SIGUNGU = ("고양시",)   # 시군구명 prefix: the city and its 구

# --- Rail ------------------------------------------------------------------

OSM_BBOX = (37.55, 126.65, 37.77, 127.01)       # S, W, N, E: the city plus about 2 km
# The Korail lines the metropolitan subway signs (route=train), queried by ref
# beside every subway, light-rail and monorail relation in the box.
OSM_TRAIN_REFS = ('수인·분당', '경의·중앙', '경강', '서해', 'GTX-A', '경춘')
RAIL_OSM_JSON = DATA_RAW / "osm_rail_routes.json"
STATION_OSM_JSON = DATA_RAW / "osm_station_names.json"   # English names only
BOUNDARY_OSM_JSON = DATA_RAW / "osm_boundary.json"
# 고양시, admin_level 6, resolved by name 2026-09-29.
BOUNDARY_RELATION = 2409166
BOUNDARY_NAME = "고양시"
# 266 km2 measured 2026-09-29.
BOUNDARY_AREA_KM2 = (260, 272)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_REGISTER = "EPSG:4326"        # SEMAS ships WGS84
# UTM zone 52N: the longitude falls in the 126 to 132 band. Derived per city,
# not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32652"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
# Seoul's precedent applied to a satellite (2026-09-29): every metropolitan
# subway, Korail metro and light-rail line with stations in the city is drawn,
# in the operators' colours (Seoul's drawn ones where Seoul draws the line);
# GTX-A (an express) and lines that never enter the city are not. Stations
# inside the city only; lines drawn to their ends.
# key -> (OSM ref, colour, public name, label end).
# SHARED LINES: a line another city's map also draws takes its one site-wide
# colour from pipeline/line_registry.py (owner, 2026-10-07: one colour per
# line on every map), never a value of this city's own; a colour figure above
# that names such a line predates the registry.
LINES = {
    "L3": ("3", line_registry.colour("seoul-subway-line-3"), "Line 3", None),
    "GJ": ("경의·중앙", line_registry.colour("gyeongui-jungang-line"), "Gyeongui–Jungang Line", None),
}
OSM_COLOUR = {}
LINES_ROUTE_TYPES = {"subway", "light_rail", "monorail", "train"}
# Gate 3: each WHOLE line's station count, English Wikipedia's line infoboxes
# read 2026-09-29 (a SECONDARY source, as Busan's).
# The Gyeongui–Jungang Line is left out of the whole-line gate: OSM carries 55
# names (Ichon twice) against the infobox's 57, none of the gap in Goyang.
LINE_STATION_COUNTS = {"Line 3": 44}
# The Seohae Line runs on the Gyeongui–Jungang Line's track through the same
# stations in Goyang (Neunggok, Daegok, Goksan, Baengma, Pungsan, Ilsan), so
# drawing it would draw that track twice.
NOT_DRAWN = {"서해": "Seohae Line", "GTX-A": "GTX-A", "1": "Line 1", "2": "Line 2", "4": "Line 4",
             "5": "Line 5", "6": "Line 6", "9": "Line 9", "I2": "Incheon Line 2", "W": "Ui LRT",
             "김포 골드라인": "Gimpo Goldline", "인천1": "Incheon Line 1"}
NOT_DRAWN_BY_NAME = {}
STOP_NAME_FIX = {}
KEY_ALIASES = {}
ENGLISH_NAME_TAGS = ("name:en", "name:ko-Latn", "name:ko_rm")
COLLAPSE_LINK_M = 500.0
BRANCH_MIN_M = 60.0

# --- Business filtering ------------------------------------------------

CITY_PREFIX = "경기도 고양시"
TAXONOMY_SYSTEM = "korea_sbiz"
RAW_CLASSIFICATION_COLUMN = "kind"

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602409166)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("ko",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
# Read from the cached tags, 2026-10-13 (docs/decisions_drafts/search-rollout.md).
PLACE_REVIEWED = {
    "어울림마을아파트교차로": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "원당주공아파트앞": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "이마트사거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "청원오피스텔삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
    "호수공원제2주차장삼거리": "a signed junction (junction=yes) named for the building beside it: a road feature, not the building (the Seoul and Busan precedent); tags read 2026-10-13",
}
# Dropped by id on the owner's rulings of 2026-10-13 on the full read (the
# reader's verdict file data/_search_rollout/reads_rules56/goyang.tsv), each
# id read with its cached name; grouped by class.
PLACE_DROPPED = {
    # A facility of an apartment estate (owner, 2026-10-13)
    "node/4640268385": "'17단지 테니스장': 'complex 17 tennis court'; description says residents' tennis court (주민 테니스장); mapped as a park",
    "node/6223247156": "'3단지 중앙 조형물': 'complex 3 central sculpture': an apartment complex's own ornament, tagged historic=monument",
    "way/469013826": "'무원 1단지 사각정 공동 쉼터': 'Muwon complex 1 pavilion shared rest area': an apartment complex's garden (description says so), mapped as a park",
    "way/779019527": "'현대밀라트c동 중앙정원': 'Hyundai Millat block C central garden': one apartment block's garden, mapped as a park",
    "way/468976153": "'5단지 공원': 'complex 5 park' (5단지 공원): named only by an apartment complex number",
    # A bare type word (owner, 2026-10-13)
    "way/480574782": "'간이공원': 간이공원 (minor park), a type phrase",
    "way/472095764": "'저류지': 저류지 (retention basin) mapped as a park",
    "way/655130560": "'공개공지': 공개공지 (privately owned public open space), a planning term",
    "way/655205767": "'중앙광장': 중앙광장 (central plaza) alone",
    "way/655231498": "'중앙광장': 중앙광장 (central plaza) alone",
    "way/476360782": "'대성전': 대성전: the hall type every Confucian school has; one of seven halls of one school mapped by type only (ways 476360781 to 476360787)",
    "way/476360781": "'명륜당': 명륜당 (lecture hall), same school, hall type only",
    "way/476360783": "'동무': 동무 (east shrine hall), same school, hall type only",
    "way/476360784": "'서무': 서무 (west shrine hall), same school, hall type only",
    "way/476360786": "'동재': 동재 (east dormitory), same school, hall type only",
    "way/476360785": "'서재': 서재 (west dormitory), same school, hall type only",
    "way/476360787": "'전사청': 전사청 (ritual preparation hall), same school, hall type only",
    "node/10956478581": "'성랑지': 성랑지 (guard post site): the kind of remain, one of four identical rows along the fortress wall",
    "node/10956478593": "'성랑지': 성랑지: same",
    "node/10956478598": "'성랑지': 성랑지: same",
    "node/10956478604": "'성랑지': 성랑지: same",
    "node/10956478594": "'여장': 여장 (parapet): the kind of remain",
    # A description standing in for a name (owner, 2026-10-13)
    "way/469495398": "'공원놀이터 운동기구': 'park playground exercise equipment'",
    "way/657924524": "'그린스쿨 조성사업': 'green school development project': a works title mapped as a park",
    "way/655293774": "'ein grüner Garten': 'ein grüner Garten' (German: a green garden) on a place=square; no Korean name",
    "node/4634856762": "'밤가시초가 안내판': 'Bamgasi thatched house information board': a signboard tagged historic=monument; the house has its own row",
    "node/4634871337": "'정발산동 주민 안내판': 'Jeongbalsan-dong residents' notice board' tagged historic=monument",
    # A religious office, hall, school or residence (owner, 2026-10-13)
    "way/658707970": "'정발산공원 공원관리과': 'Jeongbalsan Park, parks management division': the park office, mapped as a park",
    # A business (owner, 2026-10-13)
    "node/6137514839": "'경희 KO ONEW 체육관': 'Kyunghee ... gymnasium' (체육관): a martial arts gym tagged a place of worship, religion=taoist",
    "way/470470457": "'일산 장례식장': 일산 장례식장 (Ilsan funeral hall) tagged a place of worship",
    # Worship named only by a body or a denomination (owner, 2026-10-13)
    "way/959060335": "'예수그리스도 후기성도교회': 'Church of Jesus Christ of Latter-day Saints' alone, the body's name",
    # A duplicate of one object (owner, 2026-10-13)
    "node/3149124331": "'봉성암': 봉성암 as place=locality, 9 m from the hermitage's own row (way/1390896601, a place of worship)",
    # Twin round 1 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "node/10956478592": "'성랑지': the twin of node/10956478581; A bare type word (owner, 2026-10-13)",
    "node/10956478595": "'성랑지': the twin of node/10956478581; A bare type word (owner, 2026-10-13)",
    "node/10956478600": "'성랑지': the twin of node/10956478581; A bare type word (owner, 2026-10-13)",
    # Twin round 2 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "node/10956478596": "'성랑지': the twin of node/10956478581; A bare type word (owner, 2026-10-13)",
    "node/10956478603": "'성랑지': the twin of node/10956478581; A bare type word (owner, 2026-10-13)",
    # Twin round 3 (owner, 2026-10-13): a same-named neighbouring object promoted into the place of
    # a row dropped by id; each dropped under the class of the row it replaced.
    "node/10956478597": "'성랑지': the twin of node/10956478581; A bare type word (owner, 2026-10-13)",
}
# Kept by the owner's word, by id (place_index, PLACE_KEPT; owner, 2026-10-13):
# famous places in the cache that the rules pass over for want of a tag.
PLACE_KEPT = {
    "way/32006947": "'일산호수공원', Ilsan Lake Park: a park and attraction with no Wikidata or Wikipedia tag; a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
    "way/32007357": "'서오릉', the Seooreung royal tombs: historic=yes with no Wikidata or Wikipedia tag; a famous place the rules pass over for want of a tag (owner, 2026-10-13)",
}
