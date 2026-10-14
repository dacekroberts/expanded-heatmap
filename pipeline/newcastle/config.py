"""Newcastle (Regional)-specific settings, scoped to one city per this
project's per-city folder architecture (see docs/project_context.md,
"Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/newcastle.md) and London's build, whose method this city
reuses on the five Tyne and Wear districts.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "newcastle" / "raw"
DATA_PROCESSED = ROOT / "data" / "newcastle" / "processed"
OUTPUTS = ROOT / "outputs" / "newcastle"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the five districts, with where each is (a citable scoping
# record). Every Metro station is inside them, so this is expected empty.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
#
# The register: the FSA's Food Hygiene Rating Scheme, one bulk XML per local
# authority. The five Tyne and Wear districts sit in the FSA's wider "North
# East" region (with Durham, Northumberland and the Tees Valley), so they are
# named by CODE, never by region (the brief), and each file must carry its own
# code. The authority API is not needed: it returned HTTP 500 through the
# London build.
FSA_AUTHORITIES = {
    "410": "Gateshead",
    "416": "Newcastle upon Tyne",
    "417": "North Tyneside",
    "427": "South Tyneside",
    "429": "Sunderland",
}
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, the same GB-wide file and edition as
# London's (a copy of data/london/raw/codepo_gb.zip, not a second download).
# Kept to the five districts' GSS codes (the brief).
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E08000021", "E08000022", "E08000023", "E08000024", "E08000037")
# London's centroid tier (owner, 2026-09-28): 634 storefronts (10.3%) the FSA
# gives a full postcode and no point; without it 17% would be unplaced.
PLACE_AT_CENTROIDS = True

# Rail: the Tyne and Wear Metro, operated by Nexus. OpenStreetMap's four
# light_rail relations - two refs, Green and Yellow, each a directional pair.
# One bounded query; the two Northern relations in the bbox (national rail to
# the Metrocentre) are not network=Tyne and Wear Metro and stay out.
OSM_BBOX = "54.78,-1.75,55.10,-1.30"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];("
    f'rel["type"="route"]["route"="light_rail"]["network"="Tyne and Wear Metro"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only"););out body;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# One station under two spellings in OSM (the brief): "St. James" is St James.
STATION_NAME_ALIASES = {"St. James": "St James"}
# Same-named stop nodes further apart than this are separate stations.
STATION_CLUSTER_M = 400

# Line key -> the OSM ref whose relations make it (both directions merged).
LINE_OSM_REFS = {"Green": ("Green",), "Yellow": ("Yellow",)}
# On-map label and legend name.
LINE_NAMES = {"Green": "Green line", "Yellow": "Yellow line"}
LEGEND_NAMES = {"Green": "Green line (Tyne and Wear Metro)",
                "Yellow": "Yellow line (Tyne and Wear Metro)"}
# Nexus's colours as OSM's relations carry them (the brief).
LINES = {"Green": {"hue": "#009933"}, "Yellow": {"hue": "#D39F06"}}
LINE_ORDER = list(LINES)
# `python scripts/line_colour_search.py newcastle`, run 2026-09-28: Nexus's
# hues' nearest feasible colours - Green 45.5 and Yellow 78.5 from the pins of
# that run, 70.4 apart; both 3:1 or better on either page. FOOD SHOPS OLIVE
# (#737a00, 2026-10-07) arrived later: Yellow sits 32.5 from it and Green
# 44.4, above the owner's floor of 20 and below 45, an accepted trade
# (2026-10-07).
LINE_COLOURS = {"Green": "#30A800", "Yellow": "#C08800"}

# GATE 3 - the whole network against the operator's count: Nexus's 60
# stations (the brief).
OPERATOR_STATION_COUNTS = {"Metro (network)": 60}
OPERATOR_COUNTS_SOURCE = "Nexus: 60 stations (the brief, 2026-09-28)"

BRANCH_NEAR_M = 300
BRANCH_MIN_NEW_M = 1000

CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# The five metropolitan districts - exactly the five FSA authorities. No Tyne
# and Wear administrative relation exists (a ceremonial county), so the union
# of the five admin_level 8 relations, each polygonised from its outer ways;
# gated on the union's area so a truncated Overpass answer cannot pass.
BOUNDARY_OSM_RELATIONS = {
    142282: "Newcastle upon Tyne", 116279: "Sunderland", 140462: "Gateshead",
    142245: "North Tyneside", 140390: "South Tyneside",
}
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_tyne_and_wear.json"
BOUNDARY_AREA_KM2 = (520, 560)   # Tyne and Wear, about 540 km2
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-1.61) falls in the -6 to 0 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Every Metro station is kept, the Sunderland branch included (owner,
# 2026-09-28). Pelaw to Sunderland runs on Network Rail track shared with
# Northern's trains, but the route runs as the Metro, with Metro stations and
# frequencies. Measured: the branch's 12 stations add 597 storefronts to the
# rings (44.7% -> 54.4%), and without it Sunderland's 1,390 have none.
# Northern's own trains are national rail and are not drawn.

# --- Business filtering ------------------------------------------------

CITY_KEEP = "Tyne and Wear"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the five districts' extent (54.7990-55.0794 N, -1.8527 to
# -1.3457 E, measured 2026-09-28) plus ~0.02 deg. The polygon does the
# filtering; this catches a CRS or axis error.
NEWCASTLE_BBOX = {
    "lat_min": 54.78,
    "lat_max": 55.10,
    "lon_min": -1.88,
    "lon_max": -1.32,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600116279,3600140390,3600140462,3600142245,3600142282)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
# Read and kept, 2026-10-13 (wave 1's unsure rows, settled on a one-off
# Wikidata lookup and the existing rules; owner, 2026-10-13). None carries
# a leak word, so check E takes no PLACE_REVIEWED entry; the reason is kept here.
#   way/727430398 'Anglican Mortuary Chapel (derelict)': a standing derelict chapel with a Wikidata entry of its own (no article; lookup 2026-10-13): a standing abandoned landmark stays whatever its article
PLACE_REVIEWED = {
    "Store Street": "an ordinary residential street",
}
PLACE_DROPPED = {
    "way/468507458": "'Arboretum', a description or a bare type word standing in for a name",
    "node/2168561999": "'Cenotaph', a description or a bare type word standing in for a name",
    "way/1181213030": "'Burial Chapel', a description or a bare type word standing in for a name",
    "node/8828087722": "'Open Space', a description or a bare type word standing in for a name",
    "node/434103567": "'colliery', a description or a bare type word standing in for a name",
    "node/434098524": "'colliery', a description or a bare type word standing in for a name",
    "node/434098161": "'colliery', a description or a bare type word standing in for a name",
    "node/6899046015": "'Ditched enclosure', a description or a bare type word standing in for a name",
    "node/10141542967": "'Medieval Hospital', a description or a bare type word standing in for a name",
    "way/857892383": "'Roman Baths', a description or a bare type word standing in for a name",
    "way/1280198160": "'Shingle Beach', a description or a bare type word standing in for a name",
    "way/1280222473": "'Shingles', a description or a bare type word standing in for a name",
    "way/1280222474": "'Shingles', a description or a bare type word standing in for a name",
    "node/2755123784": "'Firebrick ovens', a description or a bare type word standing in for a name",
    "node/2810811724": "'Mill race spillway', a description or a bare type word standing in for a name",
    "node/9388348913": "'Old Railway Crossing', a description or a bare type word standing in for a name",
    "node/4088698512": "'Old ferry landing', a description or a bare type word standing in for a name",
    "way/1154034309": "'Former tram stop and public toilets', a description or a bare type word standing in for a name",
    "node/314716763": "'World war 2 anti aircraft factory', a description or a bare type word standing in for a name",
    "node/5059258061": "'The old barn', a description or a bare type word standing in for a name",
    "way/278417735": "'Old Ford Football field & Childrens Play Area', a description or a bare type word standing in for a name",
    "node/13025666402": "'Whitley Bay parkrun', a description or a bare type word standing in for a name",
    "node/5992574890": "'West Backworth Medieval Settlement (English Heritage Scheduled Monument)', a description or a bare type word standing in for a name",
    "node/1817922725": "'Backworth Colliery - closed - site of', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "node/8742332205": "'Site of Kings Meadow Island', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "node/6899046016": "'Site of Ravensworth coalmill', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "node/1769979294": "'Site of The Royal Grammar School', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "node/3389916282": "'Site of old Mortuary', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/980118154": "'Greenhouse Site', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/401016625": "'Church of St Mary (closed)', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/732464213": "'Sunderland Synagogue (closed)', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "way/221457325": "'Tynemouth Outdoor Pool', vanished, razed or disused by its own tags or its own name's \"site of\" (owner, 2026-10-13: a search must not land where the thing is not)",
    "node/899001001": "'The Marsden Road Baptist Tabernacl', the name is cut short: a glitch, not repaired",
    "node/13840954634": "'Warden Law Cottages', homes, or a business's own yard or park, mapped as a locality",
    "node/312877523": "'AMEC Hadrian Yard A', homes, or a business's own yard or park, mapped as a locality",
    "node/6942678360": "'Neptune Energy Park', homes, or a business's own yard or park, mapped as a locality",
    "node/4647380858": "'Oceana Business Park', homes, or a business's own yard or park, mapped as a locality",
    "node/4655485297": "'Riverside Business Park', homes, or a business's own yard or park, mapped as a locality",
    "node/4616255498": "'Shepherd Offshore Technology Park', homes, or a business's own yard or park, mapped as a locality",
    "node/6942678361": "'Swans Offshore Energy Park', homes, or a business's own yard or park, mapped as a locality",
    "node/9499253412": "'Middle Docks (Disused)', homes, or a business's own yard or park, mapped as a locality",
    "way/470933153": "'E1', a code as a street's name (owner, 2026-10-13)",
    "way/444134674": "'E2', a code as a street's name (owner, 2026-10-13)",
    "way/444134671": "'E3', a code as a street's name (owner, 2026-10-13)",
    "way/444134686": "'E4', a code as a street's name (owner, 2026-10-13)",
    "way/444134692": "'E5', a code as a street's name (owner, 2026-10-13)",
    "way/467982085": "'E6', a code as a street's name (owner, 2026-10-13)",
    "way/1160285012": "'Link Bridge (Level 3)', a code as a street's name (owner, 2026-10-13)",
    "way/1160285011": "'Link Bridge (Level 7)', a code as a street's name (owner, 2026-10-13)",
    "way/62088153": "'Brignall C', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/62557598": "'Broadmayne Gard', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/62089790": "'Laurel G', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/67812337": "'Laygate Ro', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/84975468": "'Pensher Street E', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/67107340": "'Dumbarton Closeb', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/153253168": "'Meldon Roadb', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/369604824": "''The Black Path'', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/369604888": "''The Black Path'', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/369604889": "''The Black Path'', a street name cut short or with a stray character: a glitch (owner, 2026-10-13)",
    "way/1177651143": "'Vehicle Inspection Lane', a description as a street's name (owner, 2026-10-13)",
    "way/1177651142": "'Vehicle Inspection Lane', a description as a street's name (owner, 2026-10-13)",
    "way/1030941594": "'Vehicle Inspection Lane', a description as a street's name (owner, 2026-10-13)",
    "way/369758654": "'Arcade', a description as a street's name (owner, 2026-10-13)",
    "way/369758664": "'Arcade', a description as a street's name (owner, 2026-10-13)",
    "way/941086253": "'Lindisfarne Road (even numbers)', a description as a street's name (owner, 2026-10-13)",
    "way/941086250": "'Lindisfarne Road (odd numbers)', a description as a street's name (owner, 2026-10-13)",
    "way/253478058": "'The Bridges Shopping Centre', a shopping centre's, business park's or industrial estate's own way",
    "way/253478059": "'The Bridges Shopping Centre', a shopping centre's, business park's or industrial estate's own way",
    "way/1175559709": "'The Bridges Shopping Centre', a shopping centre's, business park's or industrial estate's own way",
    "way/155969424": "'Viking Centre', a shopping centre's, business park's or industrial estate's own way",
    "way/23936465": "'Viking Centre', a shopping centre's, business park's or industrial estate's own way",
    "way/1343593544": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/162581846": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/1258990304": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/1258990305": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/1343593535": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/1343593536": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/1343593543": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/1343597512": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/1343597513": "'Newcastle Shopping Park', a shopping centre's, business park's or industrial estate's own way",
    "way/263684357": "'Quorum Buiness Park', a shopping centre's, business park's or industrial estate's own way",
    "way/263684363": "'Quorum Buiness Park', a shopping centre's, business park's or industrial estate's own way",
    "way/263684364": "'Quorum Buiness Park', a shopping centre's, business park's or industrial estate's own way",
    "way/263684368": "'Quorum Buiness Park', a shopping centre's, business park's or industrial estate's own way",
    "way/739794876": "'Quorum Buiness Park', a shopping centre's, business park's or industrial estate's own way",
    "way/739794877": "'Quorum Buiness Park', a shopping centre's, business park's or industrial estate's own way",
    "way/862371017": "'Quorum Buiness Park', a shopping centre's, business park's or industrial estate's own way",
    "way/30885632": "'Bellway Industrial Estate', a shopping centre's, business park's or industrial estate's own way",
    "way/84981040": "'Buddle Industrial Estate', a shopping centre's, business park's or industrial estate's own way",
    "node/6899046018": "'Enclosures near Damhead wood', description: historic=archaeological_site; name is a register description; wikidata, no article (flag check, 2026-10-13)",
    "node/7890734168": "'Former Hawthorn Leslie Co Shipyard', private: historic=ruins; access=no; name begins \"Former\" (closed to the public) (flag check, 2026-10-13)",
    "node/1957261720": "'Prominent Church', description: amenity=place_of_worship; name \"Prominent Church\" (a mapper's description) (flag check, 2026-10-13)",
    "way/854562743": "'St Mark (closed)', closed: amenity=place_of_worship; name ends \"(closed)\" (the English twin of the \"(geschlossen)\" rule) (flag check, 2026-10-13)",
    "way/1280945292": "'ampitheatre', description: leisure=park; lowercase bare type word (flag check, 2026-10-13)",
    "way/1280945293": "'ampitheatre', description: leisure=park; lowercase bare type word (flag check, 2026-10-13)",
    "way/276258656": "'Church Dene footpath', description: a place name and a type word (flag check, 2026-10-13)",
    "node/9661326717": "'Dial Cottage (George Stevensons Listed Home)', named a home by its own name, no Wikidata entry and no tourism tag: a home is kept only when open to visit or tagged an attraction (wave 1's unsure rows, settled on the Wikidata lookup and the existing rules, 2026-10-13)",
    "node/467128730": "'Lizard House', place=locality; name ends 'House'; no other tag (a house mapped as a locality, as Nottingham's Wiverton Hall) (wave 1's unsure rows, settled on the Wikidata lookup and the existing rules, 2026-10-13)",
    "way/401459740": "'Society of Saint Pius X', a place of worship named only by a denomination, a body or a chain, in a form the shared rule's lists do not hold; no wikipedia tag of its own (owner's rulings, 2026-10-13)",
}
