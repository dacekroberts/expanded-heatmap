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
    "way/151116368": "'Ashton Canal - Stockport Branch', demolished or gone by its own tags or name (owner, 2026-10-13)",
    "way/1274437005": "'Ashton Canal - Stockport Branch', abandoned by its own tags (owner, 2026-10-13)",
    "way/1508130452": "'Heywood Branch Canal', abandoned by its own tags (owner, 2026-10-13)",
    "way/1164880320": "'Hollinwood Canal', abandoned by its own tags (owner, 2026-10-13)",
    "way/209385174": "'Manchester, Bolton and Bury Canal', abandoned by its own tags (owner, 2026-10-13)",
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
    "way/123226436": "'Stairs Between Beechwood Ln. and Beechwood Av.', a description standing in for a name (owner, 2026-10-13)",
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
    "way/541152053": "'Water Street cycle track', a description standing in for a name (owner, 2026-10-13)",
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
    "way/759529759": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1067402531": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1067402533": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/5556943": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/552901785": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/759529762": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/759529765": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/759529767": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1067402532": "'BT Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/946149096": "'Cadishead Way Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659636": "'Canal Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659638": "'Canal Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659637": "'Canal Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155112336": "'Canal Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916709257": "'Canal Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916709258": "'Canal Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/2954151": "'Carrington Spur Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/82479720": "'Carrington Spur Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/82479725": "'Carrington Spur Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/82479728": "'Carrington Spur Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155112338": "'Centenary Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659630": "'Centenary Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659631": "'Centenary Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659632": "'Centenary Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659633": "'Centenary Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916709250": "'Centenary Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916709251": "'Centenary Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916709255": "'Centenary Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/153968149": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/153968152": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/153968157": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/153968158": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185702560": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185702578": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185702580": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185702582": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1099295799": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1101549278": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1101549279": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1196113200": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1456475309": "'Chadderton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/121173993": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/121173997": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/121173999": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/148759865": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/818552201": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/818552206": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/818552210": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/996074680": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/996074681": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/996075341": "'Deansgate Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/70708497": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/70708499": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1328577833": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/70708488": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/888716209": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4272792": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/70708492": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/70708494": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/888716210": "'Denton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/22722351": "'Featherstall Road North Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185697904": "'Featherstall Road North Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185702558": "'Featherstall Road North Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185702572": "'Featherstall Road North Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/337897078": "'Featherstall Road North Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/337897095": "'Featherstall Road North Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/337897099": "'Featherstall Road North Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1456475298": "'Featherstall Road North Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/946167420": "'George Richards Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155111568": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155111569": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/217296357": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/217296359": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/217296362": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/217296367": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/611347757": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/611349822": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/941085648": "'Gilda Brook Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/5015475": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/697214219": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/701348201": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/701348202": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1097398910": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1104366427": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/697214220": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/697214222": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/697214221": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/701335522": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/701348203": "'Greengate Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155115512": "'Guinness Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659626": "'Guinness Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659627": "'Guinness Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659622": "'Guinness Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659623": "'Guinness Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659624": "'Guinness Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916659625": "'Guinness Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/918290064": "'Guinness Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1026422769": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1036619031": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1026419957": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1026420988": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1026422768": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1070791260": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1070791261": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/963404615": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1026419958": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1026422315": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1070791262": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1070791263": "'Hale Four Seasons Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4716554": "'Heap Bridge Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185282144": "'Heap Bridge Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185282146": "'Heap Bridge Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185282148": "'Heap Bridge Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/185282152": "'Heap Bridge Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246124628": "'Heap Bridge Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246124629": "'Heap Bridge Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4715044": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/30818322": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/30818323": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/30818324": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/187114884": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/187114885": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/187114886": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/187114887": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1136117840": "'Heywood Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/973296344": "'Irlam Locks Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155119277": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155119278": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155119279": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155119280": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/842459576": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/842459577": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/842459578": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/842459579": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1093462756": "'King Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/155112340": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/217293453": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/217294925": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/217294929": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/670256282": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/684825968": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/684825970": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/684825973": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/916711165": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/928817266": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/928817268": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/928817271": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/928817272": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/936505087": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1054271044": "'Ladywell Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/58278355": "'Lostock Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/58278359": "'Lostock Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4082528": "'Lostock Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/58278358": "'Lostock Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/333537280": "'Manchester Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1097667528": "'Manchester Street Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4748803": "'Milnrow Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4803220": "'Milnrow Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/347620473": "'Milnrow Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/667769115": "'Milnrow Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/667769116": "'Milnrow Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/987360433": "'Mottram Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/987360434": "'Mottram Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/987360432": "'Mottram Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4074553": "'Mottram Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/973294160": "'Omega Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/146417955": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/697005468": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/697005469": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/697005470": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/698069874": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/698069875": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/939531685": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/987319082": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1551304590": "'Peel Green Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/67397630": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/67397791": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/168865689": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246384938": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246384942": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246384943": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/481018964": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/481018965": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/481018966": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/956400236": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1066671516": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1067752322": "'Pendleton Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/987416868": "'Pilsworth Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4448206": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/343090144": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/343090146": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/343090147": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/619239372": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/619239378": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/619239386": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/619239392": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/619239397": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/619239404": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/619242286": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/939531684": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/941044015": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/956160926": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/956165505": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/956165506": "'Regent Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/157211350": "'Rhodes Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246124630": "'Rhodes Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/157211348": "'Rhodes Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1096034116": "'Rhodes Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/157211337": "'Rhodes Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/157211344": "'Rhodes Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1095281937": "'Rhodes Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1096034117": "'Rhodes Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4085763": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/206173251": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/206173253": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/206173254": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/206173257": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/978856150": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/978856151": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/979393300": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/979393301": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/998796123": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/998804471": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/998804472": "'Sharston Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/28179885": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/511509727": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1313330609": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/28179886": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/28179892": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/477555980": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/477555981": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/511509723": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/511509724": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/511509726": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/699903949": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/28179893": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/511509725": "'Simister Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/153877034": "'Slattocks Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/153877036": "'Slattocks Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/22720073": "'Slattocks Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/22720168": "'Slattocks Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/22720169": "'Slattocks Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1456477712": "'Slattocks Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/145852853": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204464": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204465": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204466": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204467": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204468": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204469": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204470": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204471": "'St Mark's Church Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/5007997": "'Stakehill Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246370211": "'Stakehill Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246370212": "'Stakehill Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246370478": "'Stakehill Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246370479": "'Stakehill Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/23905480": "'Tenax Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/915764670": "'Tenax Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/915764671": "'Tenax Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/915764672": "'Tenax Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/915764676": "'Tenax Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/915764677": "'Tenax Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/3991625": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/80279066": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/80279085": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/200748307": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/200748311": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/200748317": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/714491043": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/994993959": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1004068152": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1094974655": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1424892719": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1424892721": "'Terminal 2 Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4995636": "'The Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/996057416": "'The Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/996057417": "'The Island', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/151367669": "'Thornham Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/151367670": "'Thornham Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/151367671": "'Thornham Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/151367668": "'Thornham Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/157774371": "'Thorpe Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1208752508": "'Thorpe Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1214759424": "'Thorpe Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1214759425": "'Thorpe Road Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/783765601": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1051111539": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/281723210": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/641002026": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/783765600": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/783765602": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/783765609": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/914411630": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/914411631": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/914411636": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/914411637": "'Village Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4419701": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4419705": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/4419711": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/82460875": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/82460886": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/232822416": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/232822418": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/232822420": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/533360364": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/533360368": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/650864686": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/650864689": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/650867839": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/650867840": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/859327129": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/951506269": "'White City Circle', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/930715": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/73507318": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/73507322": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/73507324": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246131121": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246131122": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246131123": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/246131124": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/828579402": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/828579405": "'Whitefield Interchange', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204475": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204476": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204477": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204479": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/145852860": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204474": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204472": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204473": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
    "way/1289204478": "'Worsley Courthouse Roundabout', a roundabout, interchange or ramp named for a road, not a street (owner, 2026-10-13)",
}
