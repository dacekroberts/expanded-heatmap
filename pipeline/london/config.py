"""London-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "london" / "raw"
DATA_PROCESSED = ROOT / "data" / "london" / "processed"
OUTPUTS = ROOT / "outputs" / "london"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
# Brief: docs/build_briefs/london.md.
#
# The register: the Food Standards Agency's Food Hygiene Rating Scheme, one
# bulk XML per local authority. The 33 London authorities are read from the
# FSA's own authority list (RegionName "London"), never assumed as a range.
# Licence: Open Government Licence v3 (licence-read pending, 2026-09-28).
FSA_AUTHORITIES_URL = "https://api.ratings.food.gov.uk/Authorities"
FSA_API_HEADERS = {"x-api-version": "2", "Accept": "application/json"}
FSA_REGION = "London"
FSA_AUTHORITY_COUNT = 33   # the 32 boroughs and the City of London
FSA_RAW_DIR = DATA_RAW / "fsa"
FSA_AUTHORITIES_JSON = DATA_RAW / "fsa_authorities.json"
# Postcode centroids (owner, 2026-09-28): OS Code-Point Open places a food
# storefront the FSA gives a FULL postcode and no point. Never a private
# address - the FSA publishes those with no postcode or an outward code only.
CODEPOINT_META_URL = "https://api.os.uk/downloads/v1/products/CodePointOpen"
CODEPOINT_URL = ("https://api.os.uk/downloads/v1/products/CodePointOpen/downloads"
                 "?area=GB&format=CSV&redirect")
CODEPOINT_ZIP = DATA_RAW / "codepo_gb.zip"
CODEPOINT_CRS = "EPSG:27700"   # British National Grid eastings / northings

# Rail (owner, 2026-09-28): the Underground, the DLR, the Elizabeth line and
# the six Overground lines; Tramlink left out. TfL publishes no GTFS. Track
# geometry is OpenStreetMap's route relations, ONE bounded query for all 19
# lines. The Elizabeth line and most of the Overground are tagged
# network=National Rail, so they are selected by NAME, never by network
# (Dublin's DART lesson; osm-rail).
OSM_BBOX = "51.28,-0.51,51.70,0.34"
OSM_ROUTES_QUERY = (
    "[out:json][timeout:180];("
    f'rel["type"="route"]["route"="subway"]["network"="London Underground"]({OSM_BBOX});'
    f'rel["type"="route"]["route"="light_rail"]["network"="Docklands Light Railway"]({OSM_BBOX});'
    f'rel["type"="route"]["route"="train"]["name"~"Elizabeth line|Liberty|Lioness|Mildmay|'
    f'Suffragette|Weaver|Windrush"]({OSM_BBOX});'
    ");out geom;")
OSM_ROUTES_JSON = DATA_RAW / "osm_rail_routes.json"
# The same relations' STOP members (route-relation membership, osm-rail's rule;
# never a node tag filter), nodes only - cheap.
OSM_STOPS_QUERY = OSM_ROUTES_QUERY.replace(
    ");out geom;",
    ')->.r;(node(r.r:"stop");node(r.r:"stop_entry_only");node(r.r:"stop_exit_only"););out body;')
OSM_STOPS_JSON = DATA_RAW / "osm_rail_stops.json"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
# Branch selection in step 1: a relation joins its line only if it adds at
# least BRANCH_MIN_NEW_M of track more than BRANCH_NEAR_M from what is chosen.
BRANCH_NEAR_M = 300
# Same-named stop nodes further apart than this are separate stations
# (Hammersmith's two; Bethnal Green's Underground and Overground).
STATION_CLUSTER_M = 400
# One station under two names in OSM, found by step 1's close-pair list
# (2026-09-28): the National Rail name beside the Underground's, and the DLR's
# "for ExCeL". Each pair is within 180 m and TfL signs it as one station.
STATION_NAME_ALIASES = {
    "London Paddington": "Paddington",
    "London Euston": "Euston",
    "London Liverpool Street": "Liverpool Street",
    "Custom House for Excel": "Custom House",
    "Cutty Sark for Maritime Greenwich": "Cutty Sark",
}

# On-map label (the name riders use) and legend name (the full public name).
# 19 full names would not fit the label solver - Tokyo's lesson - so the map
# says "Bakerloo" and the legend "Bakerloo line" (render_heatmap's
# legend_names, which also caps the legend at the solver's 274 px).
LEGEND_NAMES = {
    **{k: f"{k} line" for k in ("Bakerloo", "Central", "Circle", "District",
                                "Hammersmith & City", "Jubilee", "Metropolitan", "Northern",
                                "Piccadilly", "Victoria", "Waterloo & City", "Elizabeth")},
    "DLR": "DLR (Docklands Light Railway)",
    **{k: f"{k} line (London Overground)" for k in ("Liberty", "Lioness", "Mildmay",
                                                    "Suffragette", "Weaver", "Windrush")},
}
# Each line's OPERATOR hue - TfL's colours as OSM's route relations carry them
# (read 2026-09-28). The drawn colour is scripts/line_colour_search.py's
# nearest feasible one (LINE_COLOURS below): the pins' blue, pink and green and
# the dark page rule some of TfL's out (the Northern's black, for one).
LINES = {
    "Bakerloo": {"hue": "#AE6017"}, "Central": {"hue": "#E42313"}, "Circle": {"hue": "#FFD329"},
    "District": {"hue": "#00A166"}, "Hammersmith & City": {"hue": "#F4A9BE"},
    "Jubilee": {"hue": "#949699"}, "Metropolitan": {"hue": "#91005A"},
    "Northern": {"hue": "#000000"}, "Piccadilly": {"hue": "#094FA3"},
    "Victoria": {"hue": "#0A9CDA"}, "Waterloo & City": {"hue": "#93CEBA"},
    "DLR": {"hue": "#00AFAD"}, "Elizabeth": {"hue": "#9364CC"},
    "Liberty": {"hue": "#61686B"}, "Lioness": {"hue": "#FFA600"}, "Mildmay": {"hue": "#006FE6"},
    "Suffragette": {"hue": "#18A95D"}, "Weaver": {"hue": "#9B0058"}, "Windrush": {"hue": "#DC241F"},
}
LINE_ORDER = list(LINES)
LINE_NAMES = {k: k for k in LINES}
# `python scripts/line_colour_search.py london` (500 m, CIE76 18), run
# 2026-09-28 on step 1's lines.geojson: closest pair within 500 m 18.3
# (Northern, Waterloo & City), anywhere 10.5 (Jubilee, Liberty); every line
# >= 45.0 from the pins of that run; 19 distinct dark-mode labels. The Retail
# pins' blue takes the Piccadilly's, which reads mauve here; the Northern's
# black is grey so it shows on the dark page.
#
# FOOD SHOPS OLIVE (#737a00, 2026-10-07) arrived after this search. The
# District's #586818 sat 15.8 from it, under the owner's floor of 20
# (2026-10-07), and moved to #00A064, the colour nearest TfL's #00A166 that
# reads 3:1 on both pages and clears 18 from every other line: olive 48.0,
# nearest line the Suffragette 40.9. Four lines sit between 20 and 45 from
# olive, an accepted trade (owner, 2026-10-07): the Circle (#B09000) 23.2, the
# Lioness 43.0, the Bakerloo 43.5 and the Suffragette 44.4. Every other line
# >= 45.0 from every pin.
LINE_COLOURS = {
    "Bakerloo": "#B06018", "Central": "#E02010", "Circle": "#B09000", "District": "#00A064",
    "Hammersmith & City": "#B88090", "Jubilee": "#909090", "Metropolitan": "#9840A0",
    "Northern": "#686060", "Piccadilly": "#805878", "Victoria": "#08A0C0",
    "Waterloo & City": "#487070", "DLR": "#5098A8", "Elizabeth": "#C068E0",
    "Liberty": "#707878", "Lioness": "#D08000", "Mildmay": "#0050F0",
    "Suffragette": "#30A800", "Weaver": "#E858D0", "Windrush": "#F86040",
}

# GATE 3 - the whole network (not cut at Greater London), against English
# Wikipedia, read 2026-09-28 (a SECONDARY source, Prague's precedent; tfl.gov.uk
# serves a Cloudflare challenge to automated reads): the London Underground
# article's table of lines; the DLR's infobox (45); the Elizabeth line's (41);
# the London Overground article's network total (113 on six lines; no per-line
# figure is published there). CIRCLE reads 35, not the table's 36: the table
# counts Paddington's two Circle stations (Praed Street and the H&C one), which
# this map draws as one station.
OPERATOR_STATION_COUNTS = {
    "Bakerloo": 25, "Central": 49, "Circle": 35, "District": 60,
    "Hammersmith & City": 29, "Jubilee": 27, "Metropolitan": 34, "Northern": 52,
    "Piccadilly": 53, "Victoria": 16, "Waterloo & City": 2, "DLR": 45,
    "Elizabeth": 41, "Overground (network)": 112,
}
# The OVERGROUND reads 112, not Wikipedia's 113: TfL's own stop lists for the
# six lines (api.tfl.gov.uk Route/Sequence, both directions, read 2026-09-28 as
# a check, nothing from it stored or published) hold 112 distinct stations, and
# the operator outranks the secondary source.
OVERGROUND_LINES = ("Liberty", "Lioness", "Mildmay", "Suffragette", "Weaver", "Windrush")
OPERATOR_COUNTS_SOURCE = ("en.wikipedia: London Underground's table of lines, the DLR (45) "
                          "and Elizabeth line (41) infoboxes, London Overground (113) - "
                          "secondary, read 2026-09-28")

# Stations OSM's route relations do not carry as stops, found by gate 3
# (2026-09-28): the Piccadilly's North Ealing and South Harrow, and the DLR's
# Woolwich Arsenal (a branch terminus). Placed at their OSM station node,
# fetched by name; step 1 STOPS once a relation carries one, so the addition
# is retired rather than doubled.
# The Overground's five (Hatch End, Watford High Street, Upper Holloway, Wood
# Street, St James Street) were found by diffing its six lines against TfL's
# own stop lists, a scratch check (108 -> 113).
STATION_ADDITIONS = {"North Ealing": "Piccadilly", "South Harrow": "Piccadilly",
                     "Woolwich Arsenal": "DLR",
                     "Hatch End": "Lioness", "Watford High Street": "Lioness",
                     "Upper Holloway": "Suffragette",
                     "Wood Street": "Weaver", "St James Street": "Weaver"}
# Relations that are not the line as TfL runs it, skipped for lines and
# stations alike: a Windrush relation starting at Battersea Park, which TfL's
# Windrush stop list does not include (2026-09-28).
RELATION_NAMES_SKIPPED = ("Windrush Line: Battersea Park",)
OSM_ADDITIONS_QUERY = (
    '[out:json][timeout:90];node["railway"="station"]["name"~"^('
    + "|".join(STATION_ADDITIONS) + f')$"]({OSM_BBOX});out body;')
OSM_ADDITIONS_JSON = DATA_RAW / "osm_station_additions.json"
BRANCH_MIN_NEW_M = 1000

# Line key -> the OSM refs whose relations make it (every direction and branch
# merged: the Northern's two branches, the District's and the DLR's five
# routes are ONE labelled line each, as TfL presents them). 173 relations on
# 2026-09-28, every one with a ref and a colour.
LINE_OSM_REFS = {
    "Bakerloo": ("Bakerloo",), "Central": ("Central",), "Circle": ("Circle",),
    "District": ("District",), "Hammersmith & City": ("Hammersmith & City",),
    "Jubilee": ("Jubilee",), "Metropolitan": ("Metropolitan",), "Northern": ("Northern",),
    "Piccadilly": ("Piccadilly",), "Victoria": ("Victoria",),
    "Waterloo & City": ("Waterloo & City",),
    "DLR": ("B-L", "B-WA", "S-L", "SI-WA", "TG-B"),
    "Elizabeth": ("Elizabeth",),
    "Liberty": ("Liberty",), "Lioness": ("Lioness",), "Mildmay": ("Mildmay",),
    "Suffragette": ("Suffragette",), "Weaver": ("Weaver",), "Windrush": ("Windrush",),
}
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Greater London - the 32 boroughs and the City, exactly the FSA's 33 "London"
# authorities. OSM relation 175342 (admin_level 5), polygonised from its outer
# ways; 1,595.5 km2 in UTM 30N on 2026-09-28, gated so a truncated Overpass
# answer cannot pass.
BOUNDARY_OSM_RELATION = 175342
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_greater_london.json"
BOUNDARY_AREA_KM2 = (1560, 1620)
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 30N: the longitude (~-0.13) falls in the -6 to 0 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32630"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Which lines count and why: see "Rail" above (owner, 2026-09-28) and
# LINE_OSM_REFS / LINE_NAMES. Every station of the 19 lines is kept - the
# spacing gate's median is 737 m, no surface stretch needs thinning.

# --- Business filtering ------------------------------------------------

# In-city rows: the 33 authority files ARE Greater London (fetch_sources.py
# asserts 33 in the FSA's "London" region); the polygon then drops any point
# geocoded outside it. CITY_KEEP is kept for the scaffold's templates.
CITY_KEEP = "London"

TAXONOMY_SYSTEM = "fsa_businesstype"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "BusinessType"

# Sanity bounds: Greater London's polygon extent (51.2868-51.6919 N,
# -0.5104-0.3340 E, measured 2026-09-28) plus ~0.02 deg. The polygon does the
# filtering; this catches a CRS or axis error.
LONDON_BBOX = {
    "lat_min": 51.26,
    "lat_max": 51.72,
    "lon_min": -0.54,
    "lon_max": 0.36,
}

# ---------------------------------------------------------------------------
# Place search (batch 3, the size tests, 2026-10-11): pipeline/place_index.py
# builds app/static/places/london.json from the caches place_index_fetch.py
# writes. The search area is the map's: Greater London, relation 175342 (admin_level 5; step 1's BOUNDARY_OSM_RELATION),
# confirmed by id 2026-10-11. Overpass area id = 3600000000 + relation id.
PLACE_AREA = "(id:3600175342)"
# The first query in tiles (place_index_fetch.fetch_split): Greater London is several times Mexico City's 402,007 elements, which took one query of about 170 s.
# Each tile is still cut by PLACE_AREA; the bbox only has to cover it.
PLACE_SPLIT = {"bbox": (51.28, -0.52, 51.7, 0.34), "rows": 3, "cols": 4}
# NEW file names: data/ is shared by every worktree.
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-11.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-11.json"
# The local language of OSM's names here: English.
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
PLACE_REVIEWED = {
    "Bank of England": "a notable historic building (tourism=attraction, Wikipedia): the building, not the business (the Panama Hotel precedent)",
    "Canal Cafe Theatre": "a theatre with a Wikipedia article",
    "HMS Wellington": "a 1934 sloop moored on the Thames (historic=ship, Wikipedia); 'Company' is in its other name, the livery company whose hall the ship is (office=ngo), in on an article of its own against its office tag (the owner's ruling of 2026-10-13); tags read 2026-10-13",
    "Honourable Artillery Company Museum": "a museum (tourism=museum, Wikipedia); 'Company' is the regiment's name. Tagged access=private: put to the owner, batch 3",
    "Store Road": "a street's own name",
    "Store Street": "a street's own name",
    # Admitted by the owner's commercial rulings of 2026-10-13 (search-rules-8, 1a0fedba): a shop or brand tag on a sight is outweighed by an article of the object's own.
    "Harrods": "the department store's listed Knightsbridge building, a sight with an article of its own (en:Harrods); 'Ltd' is in its alt name, Harrods Ltd",
    "The Old Curiosity Shop": "the 16th-century building Dickens's novel is linked to, a sight with an article of its own",
}
# OSM objects a reading by eye found to be a business or a home that no rule
# in place_index.py catches, each with why (place_index.build, `dropped`).
PLACE_DROPPED = {
    "way/146130119": "'Harvey Nichols': the article is the company's, not the building's; a store with a chain article fails the rule's own 'not the brand's article' test (lane 4 borderline read; owner, 2026-10-16)",
    # From the read of the landmarks and places (the place-read agent, batch 3, 2026-10-11: every place and every landmark that is not a park or a place of worship read with its tags, the rest screened), each id checked against its cached name.
    "way/1547913134": "a development's private drive (access=no, foot=private) drawn as a residential street and named for its car park",
    "relation/19960734": "a private country estate (access=private) tagged a locality",
    "node/709103709": "a single address tagged a locality",
    "node/10244976882": "a retirement village (operator: a care charity) tagged a neighbourhood",
    "node/12961342802": "a single block of flats tagged a neighbourhood",
    "way/1503569413": "an office campus (landuse=commercial) tagged a place",
    "way/1174879792": "an office complex (landuse=commercial) tagged a place",
    "node/306691697": "a business park tagged a place",
    "node/14185522580": "a business park tagged a place",
    "node/7910239639": "an industrial estate tagged a place",
    "node/2121765546": "a retail and leisure park tagged a place",
    "relation/2419635": "a car park carrying the old airport's name, tagged a locality",
    "node/13073412043": "a bare zone label tagged a place",
    "node/13073412044": "a bare zone label tagged a place",
    "node/13073412040": "a bare zone label tagged a place",
    "node/13073412042": "a bare zone label tagged a place",
    "node/13073412039": "a bare zone label tagged a place",
    "node/13073412041": "a bare zone label tagged a place",
    "node/7935867754": "a description standing in for a name (silt lagoons)",
    "node/7935867755": "a description standing in for a name (silt lagoons)",
    "way/603730256": "a residents' communal garden by its own name",
    "way/647782158": "a residents' park by its own name",
    "way/583725594": "a residents' communal garden by its own name",
    "way/551726466": "a residents' communal park by its own name",
    "way/77260560": "a residents' communal garden by its own name",
    "way/26987465": "a park closed to the public (access=no); the public park of the same name is another object",
    "relation/12978771": "a listed terrace of homes whose name is its register address",
    "relation/18070162": "a listed terrace of homes whose name is its register address",
    "relation/12978787": "a listed terrace of homes whose name is its register address",
    "relation/19125929": "a listed terrace of homes whose name is its register address",
    "relation/19125930": "a listed terrace of homes whose name is its register address",
    "relation/19125412": "a listed terrace of homes whose name is its register address",
    "relation/19125931": "a listed terrace of homes whose name is its register address",
    "way/41421434": "a convent (place_of_worship=convent), a religious residence, not notable",
    "way/424276002": "a religious order's house, a residence tagged a place of worship, not notable",
    "way/105702835": "a monastery, a religious residence tagged a place of worship, not notable",
    "node/245097342": "a convent, a religious residence tagged a place of worship, not notable",
    "node/1089271228": "a convent, a religious residence tagged a place of worship, not notable",
    "way/84842549": "a priory (building=convent), a religious residence tagged a place of worship, not notable",
    "way/1323414980": "a vicarage (building=vicarage), a home",
    "way/548446976": "a company's premises (building=commercial), its description advertising copy",
    "way/1081392507": "a trapeze school, a business tagged a park",
    "node/13849155689": "a private art dealer's gallery, by appointment",
    "node/5712073478": "an organisation's office tagged a place of worship",
    "way/13891699": "a rugby club's grounds tagged a park",
    "way/202827861": "a members' tennis club",
    "way/970901100": "a ruined shed under a cricket club's name",
    "node/12453353101": "a wholesale market tagged a monument, not notable",
    "way/115407414": "a person's own name alone on a place of worship",
    "node/5294728343": "a private person's grave marker, tagged a monument",
    "node/5294728348": "a private person's grave marker, tagged a monument",
    "node/5294728351": "a private person's grave marker, tagged a monument",
    "node/5294728344": "a private person's grave marker, tagged a monument",
    "node/5294728352": "a private person's grave marker, tagged a monument",
    "node/4944095032": "a private person's grave marker, tagged a monument",
    "node/5294728347": "a family's vault, tagged a monument",
    "node/5294728346": "a family's grave, tagged a monument",
    "way/112072560": "a glitched name (a former use's, with a stray comma) on a mosque",
    "way/1339072172": "room numbers standing in for a name (a campus prayer room)",
    "node/747006838": "an address pasted into a chapel's name",
    "way/469218841": "a description standing in for a name",
    "node/1504407870": "a drinking fountain under a list number",
    "node/1504408026": "a drinking fountain under a list number",
    "way/1479921330": "a footpath drawn as a river",
    "way/1479927404": "a footpath drawn as a river",
    "way/1479930760": "a footpath drawn as a river",
    "way/1479670696": "a footpath drawn as a river",
    "node/2727439498": "a temple's name on a bare monument node: a wrong object",
    "node/977469702": "a sports hall's name on a monument node: a wrong object",
    "way/393564724": "a glitched name (an abbreviation) on a college",
    "way/804315818": "a glitched name (an abbreviation) on a place of worship",
    "way/5059696": "a glitched name on a customers-only ground tagged a park",
    "way/78311287": "a council office under a mistyped historic tag",
    "node/11343117923": "a landmark's name repeated as a locality (the Tower of London is its own row)",
    # Dealers' galleries and mis-named monument nodes, by id (owner, 2026-10-11: "all right", after the gallery and monument rules were measured and not applied). A dealer's gallery is the business itself, whatever its article, as Paris's Galerie Perrotin is; public and charitable galleries stay.
    "node/5947730342": "a commercial art dealer's gallery (Imitate Modern)",
    "node/5749996583": "a commercial art dealer's gallery (Kallos Gallery)",
    "node/5764879112": "a commercial art dealer's gallery (Maddox Arts)",
    "node/452238452": "a commercial art dealer's gallery (The Fine Art Society)",
    "node/5671022803": "a commercial art dealer's gallery (Messum's)",
    "node/9425465875": "a commercial art dealer's gallery (Unit London)",
    "node/14204677385": "a commercial art dealer's gallery (Ronchini)",
    "node/6109669976": "a commercial art dealer's gallery (Alison Jacques)",
    "node/4542203078": "a commercial art dealer's gallery (Victoria Miro)",
    "way/689689540": "a commercial art dealer's gallery (Lisson Gallery)",
    "way/689445497": "a commercial art dealer's gallery (Lisson Gallery, its second building)",
    "way/553157396": "a commercial art dealer's gallery (Paul Stolper, building=retail)",
    "way/102403106": "a commercial art dealer's gallery (White Cube)",
    "way/164599237": "a commercial art dealer's gallery (Howard Griffin Gallery)",
    "node/12410053303": "a place's name alone on a bare monument node: a wrong object",
    "node/4336765075": "a street's name alone on a bare monument node: a wrong object",
    "node/2014156881": "a dock's name alone on a bare monument node: a wrong object",
    "node/6343767873": "a boundary stone under the name of the common it once marked: a wrong object",
    "way/1340893634": "'Canada Gardens - Play Area', a play area named by its location and type",
    # Second rows for one object, from the twin round of 2026-10-13: two rows of one
    # kind and name sharing one Wikidata entry; the row with fewer tags goes.
    "node/704603329": "'Rush Green', a locality node beside the suburb node of the same name and entry, 438 m off (node 12003255761)",
}
# Kept by the owner's word against the bare-type rule (place_index, PLACE_KEPT;
# owner, 2026-10-13: "keep by name"): the Greenway is a named linear park, and
# "greenway" stays a bare type word for every other object and city.
PLACE_KEPT = {
    "way/120317147": "'Greenway', a named linear park (owner, 2026-10-13)",
    "relation/17674520": "'Greenway', a named linear park (owner, 2026-10-13)",
    # Public art kept against the article rule (owner, 2026-10-13).
    "node/343354107": "'The Burghers Of Calais', its Wikidata entry has no article in any language (owner, 2026-10-13)",
}
