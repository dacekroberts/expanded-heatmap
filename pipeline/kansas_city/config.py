"""Kansas City-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py.

KANSAS CITY, MISSOURI, on Houston's template (a US register, the sole-owner
name rule) and the shared `pipeline/osm_tram.py` (the tram-city skill). The
register is KCMO's Business License Holders, Socrata `kkhs-93m4`, Public
Domain, frozen on 2026-01-15, and already placed: each row carries a
`location` point, so there is no address join and no geocoder. Rail from
OpenStreetMap: RideKC's GTFS is not used (owner, 2026-09-30; the brief).
"""

from pathlib import Path

SLUG = "kansas_city"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "kansas_city" / "raw"
DATA_PROCESSED = ROOT / "data" / "kansas_city" / "processed"
OUTPUTS = ROOT / "outputs" / "kansas_city"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Streetcar stops outside the city, with the reason (the Los Angeles rule).
# Every stop is inside, so today it is header-only.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) ----------------

# KCMO Business License Holders (data.kcmo.org kkhs-93m4, Public Domain as the
# dataset declares). rowsUpdatedAt 1768519845 = 2026-01-15: frozen, so the
# page states the data date (owner, 2026-09-29, Stockholm's precedent).
# THE COLUMN NAMES MISLEAD: `dba_name` is filled on every row and holds the
# LICENCE HOLDER - "SURNAME GIVEN-NAME INITIAL" for a person, "MANREET INC" for a
# company - while `business_name`, filled on 5,835 of 15,895, is the trade name
# ("7 ELEVEN STORE NO 18711C" over MANREET INC; "BLOOMING WATERS" over a
# person). Measured 2026-09-30. Step 2 reads the holder only to decide whether
# the business is a person's, and never shows a person's name.
REGISTER_DOMAIN = "data.kcmo.org"
REGISTER_VIEW = "kkhs-93m4"
REGISTER_URL = f"https://{REGISTER_DOMAIN}/resource/{REGISTER_VIEW}.json"
REGISTER_META_URL = f"https://{REGISTER_DOMAIN}/api/views/{REGISTER_VIEW}.json"
REGISTER_FIELDS = ("id", "business_type", "address", "city", "state", "zipcode",
                   "business_name", "dba_name", "valid_license_for", "location")
REGISTER_ROWS_UPDATED = 1768519845          # 2026-01-15; fetch_sources stops if it moves
REGISTER_DATA_DATE = "2026-01-15"
REGISTER_CSV = DATA_RAW / "business_licenses.csv"

# The Census Bureau's 2022 NAICS titles (2-6 digit file; a US federal
# government work, public domain). The register writes NAICS TITLES, not
# codes, with the commas dropped ("All Other Professional Scientific and
# Technical Services"); step 2 maps each title back to its code through this
# file so the shared naics.py classifies, unchanged (the brief).
NAICS_TITLES_URL = "https://www.census.gov/naics/2022NAICS/2-6%20digit_2022_Codes.xlsx"
NAICS_TITLES_XLSX = DATA_RAW / "naics_2022_codes.xlsx"

# THE CENSUS BUREAU'S PLACE POLYGON (TIGERweb, current Incorporated Places,
# GEOID 2938000 Kansas City, Missouri; public domain) - Houston's and
# Buffalo's layer, the legal boundary the City reports to the Census.
CITY_BOUNDARY_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                     "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
CITY_GEOID = "2938000"
CITY_BOUNDARY_QUERY = {"where": f"GEOID='{CITY_GEOID}'",
                       "outFields": "GEOID,NAME,AREALAND,AREAWATER",
                       "outSR": "4326", "f": "geojson"}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary_tiger.geojson"
# The polygon's area, land and water (Census: about 815 km2 land, 13 water);
# step 1 stops outside these bounds.
CITY_AREA_KM2 = (790.0, 860.0)

# OSM: every tram relation in the streetcar's box (the brief's check box).
RAIL_BBOX = (39.02, -94.62, 39.13, -94.54)        # south, west, north, east
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 15N: the longitude (~-94.58) falls in the -96 to -90 band. Derived
# per city, not copied.
CRS_PROJECTED = "EPSG:32615"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED, on the 19 stops' 413 m median gap (the brief, 2026-09-30; the owner's
# spacing rule). Step 1 prints the median again and stops outside 350-480 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (350.0, 480.0)

# --- Station scope: EVERY STOP, 19 --------------------------------------------
#
# The KC Streetcar is one line, River Market - UMKC with the Main Street
# extension (the brief): two `route=tram` relations, one per direction,
# ref 601 (7825409 and 7825410). No metro, no other rail. Every stop is kept
# (owner: no thinning on the tram list).
ROUTE = "tram"
OPERATOR = None
LINE_REFS = ("601",)
NOT_DRAWN = {}
STATION_ADD = {}
EXPECTED_STATIONS = 19

# GATE 3: the operator's own stop count, independent of OSM. The KC Streetcar
# Authority's route map names 19 stops, River Market's Riverfront to UMKC -
# the same 19 names the build draws. Read for the count only; RideKC's GTFS
# and schedules are barred (owner) and were not used.
OPERATOR_STATION_COUNTS = {"601": 19}
OPERATOR_COUNTS_SOURCE = (
    "KC Streetcar Authority, 'Expanded KC Streetcar Route Map as of May 18, 2026' "
    "(pylon map 2978_KCSA_PylonMap_RUN-2026_Delaware, linked from "
    "https://kcstreetcar.org/route/), 19 stops; primary; read 2026-10-01")

SPACING_MIN_M = 150.0

DRAWN_LINES = ("601",)
# The line's public name (the brief). The KC Streetcar and RideKC logos are
# never used: the KC Streetcar Authority claims the logo and brand.
LINE_NAMES = {"601": "KC Streetcar"}
# OSM carries no `colour` on either relation (the brief), so the project's own
# palette, as Odense's and Riga's. Scored against the pins through
# pipeline/linecolour.py at build.
LINE_COLOURS = {"601": "#b8860b"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "naics"
RAW_CLASSIFICATION_COLUMN = "business_type"

# Licences current at the freeze (owner, call 10): valid for 2025 or 2026.
# The 1,978 valid for 2024 had lapsed by the freeze.
VALID_FOR_KEEP = ("20251231", "20261231")

# The register's fee codes in place of a NAICS title ("Misc Rate 129",
# "Flat Rate 42A"): no industry to classify, so dropped and counted on the
# page (owner, call 12).
FEE_CODE = r"^(?:Misc|Flat) Rate \d+[A-Z]?$"

# A COMPANY NAMED ONLY AS A PERSON shows the address too: Bucharest's owner
# call ("Caranica Mihai SRL") and Denmark's (a name that marks the business as
# one person's). Compared with the legal form stripped ("GIVEN-NAME SURNAME LLC" ->
# "GIVEN-NAME SURNAME"). Read by eye on 2026-09-30 from every shown name that
# residence.py's shape test reads as a person's - 271 trade names and 316 holder
# companies; all but these are shop names ("CROWS COFFEE", "SMOOTHIE KING") or
# chains named for a founder ("JOHNNY WAS", "KENDRA SCOTT", "EILEEN FISHER"),
# which are brands. The register is frozen, so the list is measured, not
# guessed; step 2 stops if one of them is no longer shown.
# Keys, not names (pipeline/name_keys.py): a new name's key is its output.
PERSON_NAMED = (
    "adfded197c319f26", "5b180c71183ee94d", "4e2b54d42e350efe", "e2f94955f17c8718",
    "39f72d9e664f9a92", "8d0b215ce1aa0d61", "dc67f68e6680e5ab", "ff1294999fc5e21b",
    "6e91c46eb1388dc7", "9c29a8022d6272d8", "b2f4fa15c37f462b", "50024764b58f3866",
    "84e140087ab9c033", "7f76d0517b6fb4be", "10c8444cf29abe14", "b08c251880946bee",
    "ef90352706036ee3", "1a7603624c76aac4", "d9cd168f6b8dfe76", "fbc2826f6f1fd51a",
    "e05777a98cb0c78d", "d10954a8a23d1c47", "4cf6280f331729dc", "406f8c76fa815d13",
    "563a766f654c596e", "d7dd6ed16acd1e58",
)

# Sanity bounds for the register's points: the city's extent plus a margin.
KANSAS_CITY_BBOX = {
    "lat_min": 38.80,
    "lat_max": 39.40,
    "lon_min": -94.80,
    "lon_max": -94.35,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600141008)"
# The index reaches more than 25 km past the map's stations, a far corner of the
# municipality's own area: recorded for rule D of scripts/check_place_scope.py
# (measured 30.9 km on the index of 2026-10-13; remove it if a rebuild falls within 25 km).
PLACE_SCOPE_REACH_REASON = "2026-10-13: the city limits' far north lies 31 km past the nearest station (owner)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Economy Parking Access Road": "a public tertiary road at the city-owned airport, no private access",
}
PLACE_DROPPED = {
    "way/620966861": "'Somberbrook HOA', a homeowners' association's residents' facilities tagged a park",
    "relation/18741305": "'Convent of Christ the King', a convent tagged a place of worship, not notable: a religious residence, by id",
    "node/358087457": "'Merry Moments Preschool', a preschool tagged a place of worship: a business",
    "way/528648886": "'Urban Christian Academy', a school tagged a place of worship: a business",
    "way/1526646550": "'Children's Center Campus Sensory Garden', a customers-only garden of a private clinic and school campus (access=customers)",
    "relation/8604575": "'Zona Rosa Town Square', a shopping centre's own green",
    "way/1535254921": "'Bier Garten', a venue's outdoor seating area indexed as a street",
    "way/498630395": "'Martin Temple Church of God', tagged demolished (demolished:building=yes): removed",
    "way/232491199": "'McConahay_ Building', a stray underscore in the name: a glitch, not repaired",
    "node/11873067269": "'Trail of Heros Memorial', a misspelt node duplicate of the park way/565937763, which stays",
    "node/14090104405": "'Christian Science', the denomination's name alone on a node: a description",
    "way/1150548105": "'North Courtyard', a position word and a type word at the airport terminal: a description",
    "node/11873001864": "'Shoal Creek Round-about', a roundabout mapped as a park node: a description",
    "way/318144384": "'Union Depot', an amusement park's ride station indexed as a station: not transit (owner, 2026-10-13)",
    "node/7784809452": "'Worlds of Fun Railroad Station', an amusement park's ride station indexed as a station: not transit (owner, 2026-10-13)",
    "way/836343385": "'Africa', a themed zone inside a paid amusement park, mapped as a locality (owner, 2026-10-13: the venue and its rides stay, the rest goes)",
    "way/1328622216": "'Americana', a themed zone inside a paid amusement park, mapped as a locality (owner, 2026-10-13)",
    "relation/18217058": "'Americana', a themed zone inside a paid amusement park, mapped as a locality (owner, 2026-10-13)",
    "way/836339089": "'Europa', a themed zone inside a paid amusement park, mapped as a locality (owner, 2026-10-13)",
    "way/836329654": "'Orient', a themed zone inside a paid amusement park, mapped as a locality (owner, 2026-10-13)",
    "way/840320373": "'Scandinavia', a themed zone inside a paid amusement park, mapped as a locality (owner, 2026-10-13)",
    "way/838072928": "'Planet Snoopy', a themed zone inside a paid amusement park; its article is the chain-wide area's (owner, 2026-10-13)",
    "node/12889677376": "'Bornean Orangutans', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/4886573536": "'Dromedary Camels', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/4886573591": "'Emus', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/4886557189": "'Lion-Tailed Macaque', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/869828686": "'Lions', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/4886573548": "'Merino sheep', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/4880585973": "'North American River Otters', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/4880585972": "'Polar Bears', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/4886573550": "'Red Kangaroo', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/12879458585": "'Sea Lion Exhibit', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/12879737395": "'Trumpeter Swans', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/4886573593": "'Wallabies', a zoo enclosure named for its species, carrying the species' wikidata (owner, 2026-10-13)",
    "node/358030106": "'Fairyland Park', a long-closed amusement park (disused=yes) with nothing there to visit (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/18647359": "'Barrybrooke Inte', a street name cut short (owner, 2026-10-13)",
    "way/18647360": "'Barrybrooke Inte', a street name cut short (owner, 2026-10-13)",
    "way/18518263": "'Highwaypass', not a name: a glitch (owner, 2026-10-13)",
    "way/18652727": "'56th', a street name cut to its number (owner, 2026-10-13)",
    "way/18417285": "'N Park', a street name cut short (owner, 2026-10-13)",
    "way/409577001": "'Wild cat Hollow turn street', a description as a street's name (owner, 2026-10-13)",
    "way/110916485": "'Downtown Underground Entrance/Exit', a description as a street's name (owner, 2026-10-13)",
    "way/111456423": "'Downtown Underground Entrance/Exit', a description as a street's name (owner, 2026-10-13)",
    "way/680864684": "'Access Road Drag Strip', a description as a street's name (owner, 2026-10-13)",
    "way/18523285": "'Access Road', a bare type as a street's name (owner, 2026-10-13)",
    "way/18534672": "'Access Road', a bare type as a street's name (owner, 2026-10-13)",
    "way/379375539": "'Access Road', a bare type as a street's name (owner, 2026-10-13)",
    "way/1047501620": "'Access track', a bare type as a street's name (owner, 2026-10-13)",
    "way/1442943347": "'Trail Access', a bare type as a street's name (owner, 2026-10-13)",
    "node/5555468725": "'3625 Park', description: a house number beside a type: '3625 Park'; CODED_TYPE could take digits + type (flag check, 2026-10-13)",
    "way/839197575": "'Cosmic Coaster', ride inside a paid venue: San Diego's config drops a paid venue's interior sections by id (owner, 2026-10-13) (flag check, 2026-10-13)",
    "way/318224808": "'Spinning Dragons', ride inside a paid venue: attraction=roller_coaster; tourism=attraction; wikipedia (flag check, 2026-10-13)",
    "node/5764089857": "'Veterans Monument', description: bare memorial type: 'Veterans Monument'; a BARE_TYPE_NAMES word (flag check, 2026-10-13)",
    "way/338427485": "'Veterans Monument', description: bare memorial type: 'Veterans Monument'; a BARE_TYPE_NAMES word (flag check, 2026-10-13)",
    "node/7404076692": "'unseencandle', business: a trade name tagged a place of worship: amenity=place_of_worship; religion=pagan; one lower-case word (flag check, 2026-10-13)",
    # The helper screens of 2026-10-13 (duplicates, parts in a church's grounds): rows that
    # fall squarely in an owner ruling, each with its ruling.
    "node/13465371242": "'Mary Grotto', a part of one church or monastery as its own row, the church's own row within 300 m (owner, 2026-10-13, ruling 4; helper screen): a Lourdes grotto (place_of_worship=lourdes_grotto) on the Rockhurst University campus, 173 m from the university's row (relation/20113421) and 224 m from the campus parish, Saint Francis-Xavier Church (way/356613075); no entry of its own and no place in the name",
}

# Public sights kept by id: in the cache, passed over by the rules (place_index,
# PLACE_KEPT; owner, 2026-10-13).
PLACE_KEPT = {
    "relation/19184935": "'Ewing and Muriel Kauffman Memorial Garden', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/14239851327": "'Kaleidoscope', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/132570887": "'Kansas City Public Library Central Library', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/4625212873": "'Money Museum', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/6171269243": "'Sea Life Aquarium Kansas City', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "node/9866172007": "'Shuttlecocks', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
}
