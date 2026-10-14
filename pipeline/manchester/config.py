"""Manchester (Regional)-specific settings, scoped to one city per this
project's per-city folder architecture (see docs/project_context.md,
"Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/manchester.md). The pilot of the UK six: the shared steps
are pipeline/countries/uk.py and uk_fetch.py, and the five cities after it are
config on the same contract. Newcastle's method (several FSA authorities named
by code, Code-Point centroids, OSM rail) on the seven Metrolink districts.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

SLUG = "manchester"
CITY_NAME = "Manchester (Regional)"
ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / SLUG / "raw"
DATA_PROCESSED = ROOT / "data" / SLUG / "processed"
OUTPUTS = ROOT / "outputs" / SLUG

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the seven districts, with where each is (a citable scoping
# record). Every Metrolink stop is inside them (the brief), so this is
# expected empty.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"

# --- Raw inputs, all keyless, downloaded by fetch_sources.py ---------------
#
# The register: the FSA's Food Hygiene Rating Scheme, one bulk XML per local
# authority. Six of the seven districts sit in the FSA's North West region,
# which holds many more, so they are named by CODE, never by region, and
# exactly seven are asserted (the brief). Stockport (428), Bolton and Wigan
# have no Metrolink stop.
FSA_AUTHORITIES = {
    "405": "Bury",
    "415": "Manchester",
    "418": "Oldham",
    "419": "Rochdale",
    "422": "Salford",
    "430": "Tameside",
    "431": "Trafford",
}
FSA_AUTHORITY_COUNT = 7
FSA_FILE_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS{code}en-GB.xml"
FSA_RAW_DIR = DATA_RAW / "fsa"

# Postcode centroids: OS Code-Point Open, the same GB-wide file and edition as
# London's (a copy of data/london/raw/codepo_gb.zip, not a second download),
# kept to the seven districts' GSS codes (the brief).
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_SOURCE = ROOT / "data" / "london" / "raw" / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings
CODEPOINT_DISTRICTS = ("E08000002", "E08000003", "E08000004", "E08000005",
                       "E08000006", "E08000008", "E08000009")
# London's centroid tier (owner, 2026-09-28), as Newcastle.
PLACE_AT_CENTROIDS = True

# The seven districts (admin_level 8), each polygonised from its outer ways
# and unioned; gated on the union's area so a truncated answer cannot pass.
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_OSM_RELATIONS = {
    146656: "Manchester", 146657: "Salford", 146675: "Trafford",
    146925: "Oldham", 146926: "Rochdale", 146927: "Bury", 146655: "Tameside",
}
BOUNDARY_AREA_KM2 = (790, 850)   # the seven districts, about 822 km2

# Rail: Manchester Metrolink, OpenStreetMap. One query (uk_fetch.osm_query):
# the bbox's route=tram relations and the seven boundaries with geometry, the
# routes' member ways' tags and member nodes.
OSM_BBOX = (53.33, -2.45, 53.65, -2.05)
OSM_ROUTES = ("tram",)
OSM_JSON = DATA_RAW / "osm.json"
SCOPE_LABEL = "the seven Metrolink districts"

# OSM's 23 relations carry 11 refs, which are SERVICE names from before TfGM's
# 14 September 2026 change, not lines. All are kept for their stops and their
# track; none is drawn as itself (LINE_STOPS below).
OSM_REFS = (
    "Altrincham – Bury",
    "Piccadilly - Altrincham",
    "Bury - Manchester Piccadilly",
    "Manchester Airport - Manchester Victoria",
    "Ashton-under-Lyne – Eccles",
    "Ashton-under-Lyne – MediaCityUK",
    "Shaw and Crompton - East Didsbury",
    "Rochdale - East Didsbury",
    "Rochdale Town Centre - East Didsbury",
    "The Trafford Centre – Cornbrook",
)
# Relation 16749012 (ref ECL, network "Metrolink", operator "TfGM", "ECL OUT",
# no colour): measured 2026-10-02, no stop members, and 99.4% of its 6.8 km
# lies within 30 m of the Ashton-under-Lyne - Eccles via MediaCityUK
# relations' track. A duplicate of the Eccles line's track, so nothing to draw.
NOT_DRAWN = {
    16749012: "ECL: no stops; a duplicate of the Eccles line's track (99.4% within 30 m)",
}

# THE LINES ARE TFGM'S, routed over OSM's track (pipeline/countries/uk.py,
# routed_lines). TfGM's network map (tfgm.com/public-transport/tram/network-map,
# read 2026-10-02) names nine lines by colour, with each line's stops in order.
# Four match an OSM service (Green, Pink, Anthracite, Navy); five (Purple,
# Yellow, Burgundy, Blue, Red) run where no OSM relation does, so OSM's
# relations cannot be drawn as lines. Stop names as TfGM writes them; LINE_STOP_ALIASES fixes its two slips.
LINE_STOPS = {
    "Green": ("Altrincham", "Navigation Road", "Timperley", "Brooklands", "Sale",
              "Dane Road", "Stretford", "Old Trafford", "Trafford Bar", "Cornbrook",
              "Deansgate-Castlefield", "St Peter's Square", "Market Street", "Shudehill",
              "Victoria", "Queens Road", "Abraham Moss", "Crumpsall", "Bowker Vale",
              "Heaton Park", "Prestwich", "Besses o' th' Barn", "Whitefield", "Radcliffe",
              "Bury"),
    "Purple": ("Altrincham", "Navigation Road", "Timperley", "Brooklands", "Sale",
               "Dane Road", "Stretford", "Old Trafford", "Trafford Bar", "Cornbrook",
               "Deansgate-Castlefield", "St Peter's Square", "Piccadilly Gardens",
               "Piccadilly", "New Islington", "Holt Town", "Etihad Campus"),
    "Yellow": ("Eccles", "Ladywell", "Weaste", "Langworthy", "Broadway", "MediaCityUK",
               "Harbour City", "Anchorage", "Salford Quays", "Exchange Quay", "Pomona",
               "Cornbrook", "Deansgate-Castlefield", "St Peter's Square",
               "Piccadilly Gardens", "Piccadilly"),
    "Burgundy": ("MediaCityUK", "Harbour City", "Anchorage", "Salford Quays",
                 "Exchange Quay", "Pomona", "Cornbrook", "Deansgate-Castlefield",
                 "St Peter's Square", "Piccadilly Gardens", "Piccadilly"),
    "Blue": ("Ashton-under-Lyne", "Ashton West", "Ashton Moss", "Audenshaw", "Droylsden",
             "Cemetery Road", "Edge Lane", "Clayton Hall", "Velopark", "Etihad Campus",
             "Holt Town", "New Islington", "Piccadilly", "Piccadilly Gardens",
             "Market Street", "Shudehill", "Victoria", "Queens Road", "Abraham Moss",
             "Crumpsall", "Bowker Vale", "Heaton Park", "Prestwich", "Besses o' th' Barn",
             "Whitefield", "Radcliffe", "Bury"),
    "Pink": ("East Didsbury", "Didsbury Village", "West Didsbury", "Burton Road",
             "Withington", "St Werburgh's Road", "Chorlton", "Firswood", "Trafford Bar",
             "Cornbrook", "Deansgate-Castlefield", "St Peter's Square", "Exchange Square",
             "Victoria", "Monsall", "Central Park", "Newton Heath and Moston", "Failsworth",
             "Hollinwood", "South Chadderton", "Freehold", "Westwood", "Oldham King Street",
             "Oldham Central", "Oldham Mumps", "Derker", "Shaw and Crompton", "Newhey",
             "Milnrow", "Kingsway Business Park", "Newbold", "Rochdale Railway Station",
             "Rochdale Town Centre"),
    "Anthracite": ("East Didsbury", "Didsbury Village", "West Didsbury", "Burton Road",
                   "Withington", "St Werburgh's Road", "Chorlton", "Firswood",
                   "Trafford Bar", "Cornbrook", "Deansgate-Castlefield", "St Peter's Square",
                   "Exchange Square", "Victoria", "Monsall", "Central Park",
                   "Newton Heath and Moston", "Failsworth", "Hollinwood", "South Chadderton",
                   "Freehold", "Westwood", "Oldham King Street", "Oldham Central",
                   "Oldham Mumps", "Derker", "Shaw and Crompton"),
    # TfGM's list goes Deansgate-Castlefield > Exchange Square; the only track
    # between them runs through St Peter's Square, so the routed line passes it.
    "Red": ("The Trafford Centre", "Trafford Palazzo", "Parkway", "Village",
            "Imperial War Museum", "Wharfside", "Pomona", "Cornbrook",
            "Deansgate-Castlefield", "Exchange Square", "Victoria", "Queens Road",
            "Abramham Moss", "Crumpsall"),
    "Navy": ("Manchester Airport", "Shadowmoss", "Peel Hall", "Robinswood Road",
             "Wythenshawe Town Centre", "Crossacres", "Benchill", "Martinscroft",
             "Roundthorn", "Baguley", "Moor Road", "Wythenshawe Park", "Northern Moor",
             "Sale Water Park", "Barlow Moor Road", "St Werburgh's Road", "Chorlton",
             "Firswood", "Trafford Bar", "Cornbrook", "Deansgate-Castlefield",
             "St Peter's Square", "Market Street", "Shudehill", "Victoria"),
}
LINE_STOP_ALIASES = {"Abramham Moss": "Abraham Moss"}
LINE_ORDER = list(LINE_STOPS)
# On-map label TfGM's own line name. The legend row reads "<label> <legend
# name>" (map_common.build_legend), so the legend name is the line's ends as
# TfGM writes them: "Green line (Altrincham - Bury)".
LINE_NAMES = {k: f"{k} line" for k in LINE_ORDER}
LEGEND_NAMES = {
    "Green": "(Altrincham - Bury)",
    "Purple": "(Altrincham - Etihad Campus)",
    "Yellow": "(Eccles - Piccadilly)",
    "Burgundy": "(MediaCityUK - Piccadilly)",
    "Blue": "(Ashton-under-Lyne - Bury)",
    "Pink": "(East Didsbury - Rochdale Town Centre)",
    "Anthracite": "(East Didsbury - Shaw and Crompton)",
    "Red": "(The Trafford Centre - Crumpsall)",
    "Navy": "(Manchester Airport - Victoria)",
}
# TfGM's own colours (its network map, 2026-10-02); LINE_COLOURS below is what
# is drawn, after scripts/line_colour_search.py.
TFGM_COLOURS = {
    "Green": "#00A651", "Purple": "#60327C", "Yellow": "#FFC40C", "Burgundy": "#A71F65",
    "Blue": "#4FC0E9", "Pink": "#F287B7", "Anthracite": "#323E48", "Red": "#ED1C24",
    "Navy": "#0066AF",
}
LINES = {k: {"hue": v} for k, v in TFGM_COLOURS.items()}
# `python scripts/line_colour_search.py manchester`, run 2026-10-02: each
# TfGM hue's nearest feasible colour, 45.1 or more from the pins of that run,
# 3:1 on both pages; closest pair within 500 m 18.1 (Burgundy, Purple); the
# nine dark-mode labels distinct. FOOD SHOPS OLIVE (#737a00, 2026-10-07)
# arrived later: the Yellow line sits 36.3 from it, above the owner's floor of
# 20 and below 45, an accepted trade (2026-10-07); every other line >= 45.4
# from every pin.
LINE_COLOURS = {
    "Green": "#28A800", "Purple": "#9840A0", "Yellow": "#C88800", "Burgundy": "#C870C8",
    "Blue": "#08A0C0", "Pink": "#B880A8", "Anthracite": "#586870", "Red": "#E81020",
    "Navy": "#7898A8",
}

# GATE 3 - the whole network against TfGM's stop list
# (tfgm.com/public-transport/tram/stops, 99 stops, read 2026-10-02). A
# per-line count would be circular here: the lines ARE TfGM's sequences.
OPERATOR_STATION_COUNTS = {"network": 99}
OPERATOR_COUNTS_SOURCE = ("TfGM, tfgm.com/public-transport/tram/stops: 99 stops "
                          "(read 2026-10-02)")
# The tram floor for the station gates (Odense's 350 m, Kansas City's 150 m):
# a collapsed set under it is still platforms.
SPACING_MIN_M = 350.0
# The standard rings: the median gap in scope is 703 m (2026-10-02), over the
# spacing rule's 550 m (docs/ring_rules.md). Step 1 stops outside this band.
MEDIAN_GAP_BOUNDS_M = (620.0, 790.0)
NAPTAN_EXPLAINED = {}

# NaPTAN (DfT, OGL v3): gate 3's second independent source (owner,
# 2026-10-01). ATCO area 940 is the national tram and metro area, where
# every tram stop is filed (area 180, Greater Manchester, holds none); step 1
# reads the active MET records with these ATCO prefixes inside the scope.
NAPTAN_PREFIXES = ("9400ZZMA",)
NAPTAN_ATCO_AREAS = ("940",)
NAPTAN_RAW_DIR = DATA_RAW / "naptan"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-2.24) falls in the -6 to 0 band. Derived per
# city, not copied - see docs/project_context.md's CRS lesson. London's and
# Newcastle's distance CRS too (the brief's British National Grid is the
# Code-Point file's own CRS, read as CODEPOINT_CRS above).
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Business filtering ------------------------------------------------

CITY_KEEP = "the seven Metrolink districts"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: the seven districts' extent plus a margin, set from the
# boundary at the build. The polygon does the filtering; this catches a CRS or
# axis error.
BUSINESS_BBOX = {
    "lat_min": 53.33,
    "lat_max": 53.72,
    "lon_min": -2.52,
    "lon_max": -1.88,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

PLACE_AREA = "(id:3600146655,3600146656,3600146657,3600146675,3600146925,3600146926,3600146927)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {
    "Hotel Road": "a public road of that name at the airport, not a hotel's drive",
    "Store Street": "a public city-centre street of that name",
}
PLACE_DROPPED = {
    "node/12872978226": "'Deep Pit (Bradford Colliery)', closed and capped by its own tags (owner, 2026-10-13)",
    "node/12873039793": "'Parker Pit (Bradford Colliery)', closed and capped by its own tags (owner, 2026-10-13)",
    "node/13514237058": "'Site of Alkrington Colliery', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/480937212": "'RR712', a code standing in for a name (owner, 2026-10-13)",
    "way/480947802": "'RR712', a code standing in for a name (owner, 2026-10-13)",
    "way/577138129": "'RR712', a code standing in for a name (owner, 2026-10-13)",
    "node/10095718228": "'Ancient gatepost', a description standing in for a name (owner, 2026-10-13)",
    "node/10095718229": "'Ancient gatepost', a description standing in for a name (owner, 2026-10-13)",
    "node/10096042951": "'Flow gauge', a bare type word for a name (owner, 2026-10-13)",
    "node/10097634081": "'Farmer's Arms Pub/Benny's', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "node/10118723099": "'Car Park Beach', a description standing in for a name (owner, 2026-10-13)",
    "node/11896941738": "'Dog Walking Field', a description standing in for a name (owner, 2026-10-13)",
    "node/10095921489": "'Sunken barge', a description standing in for a name (owner, 2026-10-13)",
    "node/245040007": "'Chapel (remains of)', a bare type word for a name (owner, 2026-10-13)",
    "node/1111435542": "'Cold War Bunker', a description standing in for a name (owner, 2026-10-13)",
    "way/838127243": "'Engine Shed', a bare type word for a name (owner, 2026-10-13)",
    "node/9061773911": "'Gateposts for access to Bridgewater Colliery Railway', a description standing in for a name (owner, 2026-10-13)",
    "node/307768960": "'Historic Cargo Lift', a description standing in for a name (owner, 2026-10-13)",
    "node/1942713343": "'Industrial Chimney', a description standing in for a name (owner, 2026-10-13)",
    "node/3124731201": "'Millennium Bench', a description standing in for a name (owner, 2026-10-13)",
    "way/79665098": "'Mortuary Chapel', abandoned by its own tags (owner, 2026-10-13)",
    "node/8721258140": "'Replica of the old cross', a description standing in for a name (owner, 2026-10-13)",
    "way/175663481": "'The Nowster (Empty Pub)', a description standing in for a name (owner, 2026-10-13)",
    "relation/7587639": "'WW2 Gun Emplacement', a description standing in for a name (owner, 2026-10-13)",
    "node/2632755281": "'WWII Air Raid Shelter', a description standing in for a name (owner, 2026-10-13)",
    "node/5594304040": "'Boisko', a bare type word for a name (owner, 2026-10-13)",
    "way/175678786": "'St Peter's Presbytery', a religious residence",
    "node/778195084": "'St Edmund's Church', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/3513607341": "'Hyde Cenotaph', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/1316999460": "'(filled-in-steps)', a description standing in for a name (owner, 2026-10-13)",
    "way/1386614309": "'Carriageway', a bare type word for a name (owner, 2026-10-13)",
    "way/1386614310": "'Carriageway', a bare type word for a name (owner, 2026-10-13)",
    "way/1386615517": "'Carriageway', a bare type word for a name (owner, 2026-10-13)",
    "way/1386615518": "'Carriageway', a bare type word for a name (owner, 2026-10-13)",
    "way/506525652": "'Carriageway', a bare type word for a name (owner, 2026-10-13)",
    "way/1148005425": "'Shopping Precinct', a bare type word for a name (owner, 2026-10-13)",
    "way/80903427": "'Central Road Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/80903429": "'Central Road Service Road', a description standing in for a name (owner, 2026-10-13)",
    "way/696168386": "'Entry Road to Club', a description standing in for a name (owner, 2026-10-13)",
    "way/541161377": "'Link from pedestrian area to road', a description standing in for a name (owner, 2026-10-13)",
    "way/32401507": "'Metrolink path', a description standing in for a name (owner, 2026-10-13)",
    "way/81704161": "'Off Grove Road', a description standing in for a name (owner, 2026-10-13)",
    "way/1103195739": "'Path Northwest of Monkey Bridge', a description standing in for a name (owner, 2026-10-13)",
    "way/1103195738": "'Path Northwest of Monkey Bridge', a description standing in for a name (owner, 2026-10-13)",
    "way/158802547": "'Perimeter Path: Sale Water Park', a description standing in for a name (owner, 2026-10-13)",
    "way/1103171104": "'Creek Bridge to Doffer Fold PROW', a description standing in for a name (owner, 2026-10-13)",
    "way/1104520178": "'Coney Green to Withins Lane PROW', a description standing in for a name (owner, 2026-10-13)",
    "way/1103298674": "'Coney Green North Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/239788266": "'Coney Green South Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/1105625918": "'Coney Green South Footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/54306273": "'Canal-side footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/239790169": "'Black Lane Ponds footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/498098060": "'Green Greater Manchester footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/199675790": "'Old River footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/201775590": "'Old River footpath', a description standing in for a name (owner, 2026-10-13)",
    "way/1103180956": "'Round Oak path', a description standing in for a name (owner, 2026-10-13)",
    "way/1104391223": "'The Dip path', a description standing in for a name (owner, 2026-10-13)",
    "way/1103210366": "'Lower Withins Path', a description standing in for a name (owner, 2026-10-13)",
    "way/216201543": "'Lower Withins path', a description standing in for a name (owner, 2026-10-13)",
    "way/1078203304": "'Hawthorn Road cycle bypass', a description standing in for a name (owner, 2026-10-13)",
    "way/216194801": "'Withins Lane Wharf Access Lane', a description standing in for a name (owner, 2026-10-13)",
    "way/834795114": "'Twenty Four Steps', a description standing in for a name (owner, 2026-10-13)",
    "way/85197618": "'St. Ann's Passage (Old Exchange)', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/438455525": "'HaniWells', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/206403433": "'RIchmond House', a single building's own way, named for the building",
    "way/692965648": "'Berkeley Business Park', a business's own feature under its own name",
    "way/692965649": "'Berkeley Business Park', a business's own feature under its own name",
    "way/736542170": "'Downing Street Industrial Estate', an industrial or trading estate's own way, named for the estate",
    "way/616791777": "'Girton Street Industrial Estate', an industrial or trading estate's own way, named for the estate",
    "way/1293704005": "'Girton Street Industrial Estate', an industrial or trading estate's own way, named for the estate",
    "way/839044024": "'Hattersley Industrial Estate', an industrial or trading estate's own way, named for the estate",
    "way/22969794": "'Hattersley Industrial Estate', an industrial or trading estate's own way, named for the estate",
    "way/115431549": "'Parkway Trading Estate', an industrial or trading estate's own way, named for the estate",
    "way/115431578": "'Parkway Trading Estate', an industrial or trading estate's own way, named for the estate",
    "way/1179958721": "'Parkway Trading Estate', an industrial or trading estate's own way, named for the estate",
    "way/4966345": "'Sedgley Park Trading Estate', an industrial or trading estate's own way, named for the estate",
    "way/715302598": "'Sherborne Street Trading Estate', an industrial or trading estate's own way, named for the estate",
    "way/273029775": "'Vaughan Street Industrial Estate', an industrial or trading estate's own way, named for the estate",
    "way/746003519": "'Westwood Business Centre', a business's own feature under its own name",
    "way/1117258132": "'Westwood Business Centre', a business's own feature under its own name",
    "way/1516634398": "'Swissport Cargo', a business's own feature under its own name",
    "way/430730989": "'The Lowry Outlet Mall', a shopping centre's own way, named for it",
    "way/430730995": "'The Lowry Outlet Mall', a shopping centre's own way, named for it",
    "way/430730984": "'The Lowry Outlet Mall', a shopping centre's own way, named for it",
    "way/1101565885": "'Town Square Shopping Centre', not a street: an indoor corridor indexed as one",
    "way/1101565887": "'Town Square Shopping Centre', not a street: an indoor corridor indexed as one",
    "way/1311950308": "'Town Square Shopping Centre', not a street: an indoor corridor indexed as one",
    "way/1262970754": "'Weatherfield Precinct', a private way the private-street rule did not reach",
    "way/67219018": "'Salford Foyer', a housing estate's own way, named for the estate",
    "way/83027748": "'Sunfield Estate', a housing estate's own way, named for the estate",
    "way/825382104": "'Salisbury House', a single building's own way, named for the building",
    "way/8108487": "'Lyngarth House', a single building's own way, named for the building",
    "way/208220157": "'Halls Cottage', a single building's own way, named for the building",
    "way/552466257": "'Mill Cottage', a single building's own way, named for the building",
    "way/698423841": "'Duke's Hideaway', a single building's own way, named for the building",
    "way/171416121": "'Anglers Rest', a single building's own way, named for the building",
    "way/171416122": "'Anglers Rest', a single building's own way, named for the building",
    "way/4788068": "'Leigh Guided Busway', not a street: another kind of object indexed as one",
    "way/497937576": "'Leigh Guided Busway', not a street: another kind of object indexed as one",
    "way/1452203808": "'Albany Way', not a street: an indoor corridor indexed as one",
    "way/1452203811": "'Fitzgerald Way', not a street: an indoor corridor indexed as one",
    "way/1452203810": "'Raven Way', not a street: an indoor corridor indexed as one",
    "way/1052629139": "'Boond Street', not yet open: highway=construction",
    "way/113510046": "'Boond Street', not yet open: highway=construction",
    "way/1052629138": "'Boond Street', not yet open: highway=construction",
    "way/4995636": "'The Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/996057416": "'The Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/996057417": "'The Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/148096669": "'Manchester, Bolton & Bury Canal feeder', description: historic=canal; waterway=stream; note=Canal feeder (a feeder channel under a description) (flag check, 2026-10-13)",
    "way/176009458": "'Middleton Cons Crown Green Bowls Club', private facility: leisure=park; name is a bowls club's (a club's green tagged a park) (flag check, 2026-10-13)",
    "way/601214274": "'Sale Model Flying Club', private facility: leisure=park; name is a model flying club's (a club's field tagged a park) (flag check, 2026-10-13)",
    "way/486642351": "'Whittaker Lane Grass Patch', description: leisure=park; grass=mown; name ends \"Grass Patch\" (flag check, 2026-10-13)",
    "node/14085210191": "'Hill Top Mews', a housing development mapped as a place (owner, 2026-10-13)",
    "way/1222568239": "'North Lodge', a listed lodge under a position word and a type word; its Wikidata entry has no article and no tag marks it open to visit: a home (wave 1's unsure rows, settled on the Wikidata lookup and the existing rules, 2026-10-13)",
    # The pattern screen of 2026-10-13: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "way/557643019": "'Assembly Hall of Jehovah's Witnesses', a religious body's reading room, assembly hall or institute tagged a place of worship, not a congregation (owner, 2026-10-13, ruling 2; pattern screen)",
    "node/286960803": "'Christadelphian Hall', a place of worship named only by its body and a hall type, in a spelling the shared rule's lists do not hold (owner, 2026-10-13, the denomination ruling; pattern screen)",
}

# Public art kept by the owner's word against the article rule (place_index,
# PLACE_KEPT; owner, 2026-10-13). Each is a known work the Wikidata lookup
# cannot admit; DECISIONS.md of that date lists the works left out.
PLACE_KEPT = {
    "way/570278857": "'Albert Memorial', a known work the article rule drops for want of an article of its own (owner, 2026-10-13)",
    # A place of worship kept against the denomination rule (worship_only;
    # owner, 2026-10-13: "keep all four by id").
    "way/31231628": "'Friends Meeting House', the listed Mount Street meeting house (denomination=quaker, wikidata=Q26579212, no wikipedia tag): a known building under its hall type's name (owner, 2026-10-13)",
}
