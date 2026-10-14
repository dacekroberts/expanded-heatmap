"""Birmingham (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/birmingham.md) on Manchester (Regional)'s contract: the shared
steps are pipeline/countries/uk.py and uk_fetch.py.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

SLUG = "birmingham"
CITY_NAME = "Birmingham (Regional)"
ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / SLUG / "raw"
DATA_PROCESSED = ROOT / "data" / SLUG / "processed"
OUTPUTS = ROOT / "outputs" / SLUG

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the scope, with where each is (a citable scoping record).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs, all keyless, downloaded by fetch_sources.py ---------------
#
# Scope: the three authorities West Midlands Metro serves today (owner,
# 2026-10-01). Dudley (409) joins only when Line 2 is in passenger service
# (pre-approved); on 2026-10-02 it was not (NOT_DRAWN below). The FSA's bulk
# XML per authority, named by CODE (the FSA's West Midlands region holds many
# more), exactly 3 asserted.
FSA_AUTHORITIES = {"402": "Birmingham", "423": "Sandwell", "436": "Wolverhampton"}
FSA_AUTHORITY_COUNT = 3
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, London's file and edition (copied,
# not downloaded again), kept to the scope's GSS codes.
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E08000025", "E08000028", "E08000031")
# London's centroid tier (owner, 2026-09-28; the UK six's kit, 2026-10-01).
PLACE_AT_CENTROIDS = True

# The scope's OSM boundary relations, each polygonised from its outer ways
# and unioned; gated on the union's area so a truncated answer cannot pass.
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_OSM_RELATIONS = {162378: "Birmingham", 162485: "Sandwell", 173722: "Wolverhampton"}
BOUNDARY_AREA_KM2 = (400, 445)   # the three authorities, about 423 km2

# Rail: West Midlands Metro, OpenStreetMap. One query (uk_fetch.osm_query): the bbox's
# route=tram relations and the boundaries with geometry, the routes' member
# ways' tags and member nodes. The lead runs it; agents read the cache.
OSM_BBOX = (52.45, -2.15, 52.6, -1.85)
OSM_ROUTES = ("tram",)
OSM_JSON = DATA_RAW / "osm.json"
SCOPE_LABEL = "the three Metro authorities (Birmingham, Sandwell and Wolverhampton)"

# OSM's 7 tram relations (2026-10-02): six of ref 1, the service patterns of
# one line (Wolverhampton Station or Wolverhampton St Georges to Edgbaston
# Village, each way, and the Millennium Point branch, each way), and one of
# ref 2. The two light_rail relations in the bbox (the Stourbridge Town
# shuttle, national rail) are outside OSM_ROUTES.
OSM_REFS = ("1",)
LINE2_REASON = "Line 2 (Wednesbury - Dudley), not yet in passenger service; due 2026-11-01"
# Line 2's stops are tagged railway=construction in OSM, and the operator's maps
# page (westmidlandsmetro.com/maps/, read 2026-10-02) lists none of them: its
# 35 stops are all Line 1's. The opening missed its 28 August 2026 date.
NOT_DRAWN = {17248967: LINE2_REASON}

# The four Wolverhampton - Edgbaston Village relations list their stop nodes
# with an EMPTY role (2026-10-02): 118 role-less memberships, 25 stops no
# role-"stop" member of ref 1 carries. uk.elements() reads their named,
# stop-tagged, role-less members as role "stop", and stops once a listed
# relation has none left.
_ROLELESS = "stop members listed with an empty role (2026-10-02)"
ROLELESS_STOP_RELATIONS = {18094029: _ROLELESS, 18094030: _ROLELESS,
                           18094031: _ROLELESS, 18094032: _ROLELESS}
# One stop, two spellings across the two directions (the brief).
STATION_NAME_ALIASES = {"Dudley Street, Guns Village": "Dudley Street Guns Village"}

# One drawn line: the six ref-1 relations merged by London's branch rule, on
# Birmingham's thresholds. Measured 2026-10-02: the Eastside branch adds about
# 415 m of track beyond 30 m of the main relation and the St Georges stub 72 m,
# under the defaults (300 m, 1,000 m), which left Millennium Point 397 m,
# Albert Street 220 m and Wolverhampton St Georges 100 m off the drawn line.
# At 30 m and 50 m, 3 of the 6 relations are drawn (23.8 km) and every station
# is within 4 m of the line.
BRANCH_NEAR_M = 30
BRANCH_MIN_NEW_M = 50
LINE_OSM_REFS = {"1": ("1",)}
LINE_ORDER = list(LINE_OSM_REFS)
# The operator's maps page names no line: it lists one network's stops and
# calls the service "the Metro". With Line 2 not yet open, the label is the
# system's public name, as the one-line precedents (Odense Letbane, Sun Link,
# KC Streetcar). The legend row reads "<label> <legend name>".
LINE_NAMES = {"1": "West Midlands Metro"}
LEGEND_NAMES = {"1": "(Wolverhampton - Edgbaston Village)"}
# OSM's colour on every ref-1 relation; LINE_COLOURS below is what is drawn,
# after scripts/line_colour_search.py.
LINES = {"1": {"hue": "#ec008c"}}
# `python scripts/line_colour_search.py birmingham`, run 2026-10-02: the
# nearest feasible colour to OSM's #ec008c, 45.2 from every pin, 4.81:1 on the
# dark page and 3.89:1 on the light one; one line, so no pair to separate.
LINE_COLOURS = {"1": "#F000B8"}

# GATE 3 - the operator's stop list, counted before the scope split. The maps
# page lists 35 stops (its stop links and its zone list, read 2026-10-02), all
# on Line 1, Albert Street and Millennium Point (the Eastside extension's open
# stops) included.
OPERATOR_STATION_COUNTS = {"1": 35}
OPERATOR_COUNTS_SOURCE = ("West Midlands Metro, westmidlandsmetro.com/maps/: 35 stops "
                          "(read 2026-10-02)")
# The tram floor for the station gates (Odense's 350 m, Kansas City's 150 m):
# a collapsed set under it is still platforms.
SPACING_MIN_M = 350.0
# Halved rings: the median gap in scope is 442 m (2026-10-02, 35 stations),
# under the spacing rule's 550 m (docs/ring_rules.md). Step 1 stops outside
# this band.
MEDIAN_GAP_BOUNDS_M = (390.0, 500.0)

# NaPTAN's names for two built stops: "Centenary Square" is OSM's "Library"
# (6 m apart; the operator writes "Library Centenary Square"), and
# "Wednesbury Central" is OSM's "Wednesbury, Great Western Street" (98 m apart;
# the next stop, Wednesbury Parkway, is 537 m away; the operator writes
# "Wednesbury Great Western Street").
NAPTAN_NAME_ALIASES = {
    "Centenary Square": "Library",
    "Wednesbury Central": "Wednesbury, Great Western Street",
}
EASTSIDE_REASON = ("Eastside extension stop beyond Millennium Point, not yet in passenger "
                   "service (not on the operator's maps page, 2026-10-02)")
# NaPTAN's active MET records inside the scope that no built station matches:
# Line 2's five inside Sandwell, and three Eastside stops not yet open.
NAPTAN_EXPLAINED = {
    "Birmingham New Road": LINE2_REASON,
    "Dudley Port": LINE2_REASON,
    "Great Bridge": LINE2_REASON,
    "Horseley Road": LINE2_REASON,
    "Sedgley Road": LINE2_REASON,
    "Curzon Street": EASTSIDE_REASON,
    "Digbeth High Street": EASTSIDE_REASON,
    "Meriden Street": EASTSIDE_REASON,
}

# NaPTAN (DfT, OGL v3): gate 3's second independent source (owner,
# 2026-10-01). ATCO area 940 is the national tram and metro area, where every
# tram stop is filed; step 1 reads the active MET records with these ATCO
# prefixes inside the scope.
NAPTAN_PREFIXES = ("9400ZZWM",)
NAPTAN_ATCO_AREAS = ("940",)
NAPTAN_RAW_DIR = DATA_RAW / "naptan"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-1.89) falls in the -6 to 0 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson. London's,
# Glasgow's and Newcastle's distance CRS too; British National Grid is only
# Code-Point's own CRS (CODEPOINT_CRS above).
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# Halved (the tram-city skill, section 3; Aarhus's): the median gap is 442 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Business filtering ------------------------------------------------

CITY_KEEP = "the three Metro authorities"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the scope's extent plus a margin. The polygon does the
# filtering; this catches a CRS or axis error.
BUSINESS_BBOX = {"lat_min": 52.36, "lat_max": 52.66, "lon_min": -2.23, "lon_max": -1.7}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600162378,3600162485,3600173722)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
PLACE_DROPPED = {
    "node/1745739183": "'The Patrick Collection', closed for good, removed or the site of a vanished thing, by its own tags or name (owner, 2026-10-13)",
    "node/1314883020": "'Blue Plaque: Joseph Lucas 1834-1902', closed for good, removed or the site of a vanished thing, by its own tags or name (owner, 2026-10-13)",
    "node/1374183345": "'Site of Langley Hall', closed for good, removed or the site of a vanished thing, by its own tags or name (owner, 2026-10-13)",
    "node/12525181511": "'Site of Roman Kiln', closed for good, removed or the site of a vanished thing, by its own tags or name (owner, 2026-10-13)",
    "node/12804949365": "'Blue Plaque: Site of James Watt's Smethwick Engine', a plaque named by a description of what stood or happened there",
    "node/12424548502": "'Blue Plaque: Location of Zepplin Raid', a plaque named by a description of what stood or happened there",
    "node/1372922783": "'Burnt Mound', a description or a bare type word standing in for a name",
    "node/1372922786": "'Burnt Mound', a description or a bare type word standing in for a name",
    "node/725889895": "'Burnt Mound', a description or a bare type word standing in for a name",
    "way/170843900": "'piggery', a description or a bare type word standing in for a name",
    "way/186291477": "'Cenotaph', a description or a bare type word standing in for a name",
    "node/1337012311": "'Fluted Column', a description or a bare type word standing in for a name",
    "way/616746692": "'Gymnastic statue', a description or a bare type word standing in for a name",
    "node/9063944157": "'Flight watch area', a description or a bare type word standing in for a name",
    "way/720452313": "'Protected community nature area', a description or a bare type word standing in for a name",
    "way/877740969": "'Field 1', a description or a bare type word standing in for a name",
    "way/82556496": "'Villa Road Methodist Church, part of King Edward Grammar School', a description or a bare type word standing in for a name",
    "node/12652242566": "'Pan Jezus czeka na Ciebie', a description or a bare type word standing in for a name",
    "way/82988242": "'First Name Catholic Church', a glitched name (a stray or missing character, a placeholder, two names in one), not repaired",
    "node/13770456571": "'Church of St. Chad #7 Mark's', a glitched name (a stray or missing character, a placeholder, two names in one), not repaired",
    "way/148046011": "'Lighthouse Church | St Mary's', a glitched name (a stray or missing character, a placeholder, two names in one), not repaired",
    "node/632456219": "'Statue of Terpsichore ('The Bird Bath'', a glitched name (a stray or missing character, a placeholder, two names in one), not repaired",
    "way/203796368": "'Wednesbury Canal (Ocker Hill Branch', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/117686849": "'BentleyCanal Neachells Branch', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/277030928": "'Green Oak Academy (Kings Heath)', not the thing its tag says: a school, a club or a business under its own name, or another object's name",
    "way/23136738": "'Yew Tree Community School', not the thing its tag says: a school, a club or a business under its own name, or another object's name",
    "way/26730346": "'Oakland Young Peoples Centre', not the thing its tag says: a school, a club or a business under its own name, or another object's name",
    "way/27758829": "'Norman Street', not the thing its tag says: a school, a club or a business under its own name, or another object's name",
    "node/8832560078": "'Edgbaston Archery & Lawn Tennis Society', not the thing its tag says: a school, a club or a business under its own name, or another object's name",
    "node/13248595683": "'Yew Tree & Tame Bridge Neighbourhood Centre', not the thing its tag says: a school, a club or a business under its own name, or another object's name",
    "way/156819378": "'Bentley Canal', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/122995668": "'Darb's Basin', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/203796371": "'Highfield Basin', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/122995675": "'Horseley Heath Canal', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/203155749": "'Keyworth Basin', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/203796360": "'Millington Basin', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/116974638": "'Newfield Cutting', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/24942267": "'Tipton Green Branch', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/272434818": "'Tipton Green Branch', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/24942272": "'Tipton Green Locks Branch', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/203796359": "'Wednesbury Oak Loop Canal', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/203796357": "'Wednesbury Oak Loop Canal (Weddel Wynd Navigation)', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/116974656": "'Wellman Cutting', an abandoned canal by its own tags (abandoned=yes or a former-canal note) (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/831611723": "'Bankfield Road (BUS ONLY)', a notice glued onto the street's name: a glitch (owner, 2026-10-13)",
    "way/1060511514": "'Bankfield Road (BUS ONLY)', a notice glued onto the street's name: a glitch (owner, 2026-10-13)",
    "way/638540863": "'Sheepcote Street (BUS GATE)', a notice glued onto the street's name: a glitch (owner, 2026-10-13)",
    "way/1417716130": "'Sheepcote Street (BUS GATE)', a notice glued onto the street's name: a glitch (owner, 2026-10-13)",
    "way/1417716131": "'Sheepcote Street (BUS GATE)', a notice glued onto the street's name: a glitch (owner, 2026-10-13)",
    "way/1277667731": "'cemetry path', a description as a street's name (owner, 2026-10-13)",
    "way/1277667730": "'Cemetry path', a description as a street's name (owner, 2026-10-13)",
    "way/1277666439": "'Cemetry Path', a description as a street's name (owner, 2026-10-13)",
    "way/317367293": "'Cemetry Path 2', a description as a street's name (owner, 2026-10-13)",
    "way/821071917": "'Path from Packwood Close to Cheswick Close', a description as a street's name (owner, 2026-10-13)",
    "way/821071914": "'Pathway from Hawkswell Drive to tunnel under The Keyway', a description as a street's name (owner, 2026-10-13)",
    "way/797323388": "'Road through estate', a description as a street's name (owner, 2026-10-13)",
    "way/43072886": "'High Street Service Road', a description as a street's name (owner, 2026-10-13)",
    "way/481181221": "'New Street Drop and Go', a station's drop-off lane described (owner, 2026-10-13)",
    "way/371608827": "'New Street Drop and Go', a station's drop-off lane described (owner, 2026-10-13)",
    "way/1084619239": "'New Street Station Subway to Sorting Office', a description as a street's name (owner, 2026-10-13)",
    "way/1536364895": "'Queensway Tunnel Emergency Exit', an emergency exit described (owner, 2026-10-13)",
    "way/1536364896": "'Queensway Tunnel Emergency Exit', an emergency exit described (owner, 2026-10-13)",
    "way/1536364897": "'Queensway Tunnel Emergency Exit', an emergency exit described (owner, 2026-10-13)",
    "way/1536364900": "'Queensway Tunnel Emergency Exit', an emergency exit described (owner, 2026-10-13)",
    "way/1536364901": "'Queensway Tunnel Emergency Exit', an emergency exit described (owner, 2026-10-13)",
    "way/1536364902": "'Queensway Tunnel Emergency Exit', an emergency exit described (owner, 2026-10-13)",
    "way/1536364903": "'Queensway Tunnel Emergency Exit', an emergency exit described (owner, 2026-10-13)",
    "way/1084619252": "'Services Bridge', a description as a street's name (owner, 2026-10-13)",
    "way/143714508": "'Holder's Lane PF', a code glued onto the street's name: a glitch (owner, 2026-10-13)",
    "way/143714507": "'Holder's Lane PF', a code glued onto the street's name: a glitch (owner, 2026-10-13)",
    "way/45039401": "'Cox'sLane', words glued in the name: a glitch (owner, 2026-10-13)",
    "way/1317364203": "'West Bromwich Bus Station', a bus station indexed as a street, access=private (owner, 2026-10-13)",
    "way/1317364204": "'West Bromwich Bus Station', a bus station indexed as a street, access=private (owner, 2026-10-13)",
    "way/32815655": "'West Bromwich Bus Station', a bus station indexed as a street, access=private (owner, 2026-10-13)",
    "way/854871217": "'West Bromwich Bus Station', a bus station indexed as a street, access=private (owner, 2026-10-13)",
    "way/32816771": "'West Bromwich Bus Station', a bus station indexed as a street, access=private (owner, 2026-10-13)",
    "way/854641676": "'West Bromwich Bus Station', a bus station indexed as a street, access=private (owner, 2026-10-13)",
    "way/28580908": "'Tollgate Shopping Centre', a shopping centre's own way",
    "way/621691363": "'Great Bear Logistics', a company's own road",
    "way/1295640613": "'Great Bear Logistics', a company's own road",
    "node/1675862241": "'Francis Brett Young 1884-1954', plaque: historic=monument; memorial=plaque; openplaques:id; no wikidata (a plaque tagged historic=monument slips the plaque rule) (flag check, 2026-10-13)",
    "node/1089765441": "'Gun Emplacement', description: historic=archaeological_site; name is a type; wikidata but no article (type words only) (flag check, 2026-10-13)",
    "node/2355085127": "'Lost Property Sun', artwork, borrowed article: tourism=artwork; wikipedia=en:Albion (Blake); wikidata=Q84743226; level=-2 (the article is the work that inspired it, not this work's) (flag check, 2026-10-13)",
    "node/12814526314": "'Mirror Image (Stratford Road Interchange)', artwork, borrowed article: tourism=artwork; wikipedia=en:Sparkbrook; wikidata=Q2593284 also on place node/107429248 (the article is the district's) (flag check, 2026-10-13)",
    "node/12815616926": "'Our Future Our Hands Bench', artwork, borrowed article: tourism=artwork; amenity=bench; wikipedia=en:Q3 Academy Tipton (its operator) (the article is the school's) (flag check, 2026-10-13)",
    "node/12807071454": "'Talking about the Weather (Bartley Green Interchange)', artwork, borrowed article: tourism=artwork; wikipedia=en:Bartley Green; wikidata=Q4865443 also on place node/558701597 (the article is the district's) (flag check, 2026-10-13)",
    "way/20002348": "'Vesey Manor', business: building=retail; occupier=an antiques dealer; historic=building (a shop in a listed building) (flag check, 2026-10-13)",
    "node/1686189422": "'Victorian Sewer', description: historic=monument; name is a type; no wikidata (flag check, 2026-10-13)",
    "node/12819635574": "'Whistle Blizzard', artwork, borrowed article: tourism=artwork; wikipedia=en:Cloudburst; wikidata=Q180382 (41 wikis); level=-2 (the article is a weather term) (flag check, 2026-10-13)",
    "node/12849822859": "'City', description: place=hamlet; name \"City\"; no wikidata (bare type word on a place) (flag check, 2026-10-13)",
    "way/300020975": "'Mosque & Islamic Centre', a place of worship named only by a denomination, a body or a chain, in a form the shared rule's lists do not hold; no wikipedia tag of its own (owner's rulings, 2026-10-13)",
    # The pattern screen of 2026-10-13: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "node/9111254607": "'Christian Science Reading Room', a religious body's reading room, assembly hall or institute tagged a place of worship, not a congregation (owner, 2026-10-13, ruling 2; pattern screen)",
    "way/295736024": "'Christadelphian Hall', a place of worship named only by its body and a hall type, in a spelling the shared rule's lists do not hold (owner, 2026-10-13, the denomination ruling; pattern screen)",
    "way/95835712": "'Christadelphian Hall', a place of worship named only by its body and a hall type, in a spelling the shared rule's lists do not hold (owner, 2026-10-13, the denomination ruling; pattern screen)",
}

# Famous places kept by id: in the cache, passed over by the rules (place_index,
# PLACE_KEPT; owner, 2026-10-13).
PLACE_KEPT = {
    "way/406003396": "'Birmingham Museum and Art Gallery', one of the city's best-known sights, in the cache with no row (tourism=museum, no wikidata or wikipedia tag): a famous place the rules pass over (owner, 2026-10-13; pattern screen)",
}
