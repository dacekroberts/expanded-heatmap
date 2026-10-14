"""Bergen-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py, then copied from Oslo's config - the
second Norwegian city, and the first on light rail. The national facts (the
register, its columns, the contact columns never to load, the sole-trader
guard) live in `pipeline/countries/norway.py`; the shared step 2 in
`norway_register.py`. What is Bergen's own is below.

⚠ THREE OSLO SETTINGS ARE NOT COPIED, each of which would fail quietly
(docs/build_briefs/bergen.md): the route type (901, not 401/902 - Oslo's
filter draws nothing here), the UTM zone (31N, not 32N) and the ring edges
(the standard ones, not Oslo's halved edges).
"""

from pathlib import Path

from pipeline.countries.norway import (  # noqa: F401
    ADDRESS_URL_TEMPLATE,
    KOMMUNE_BOUNDARY_URL_TEMPLATE,
)

SLUG = "bergen"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "bergen" / "raw"
DATA_PROCESSED = ROOT / "data" / "bergen" / "processed"
OUTPUTS = ROOT / "outputs" / "bergen"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Every Bybanen station is inside the kommune (the airport included), so this
# file is written empty, with its header - a citable record that none is out.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all public and keyless; `fetch_sources.py` downloads them. The
# two register files are NATIONAL, cached once for the country and SHARED
# with Oslo (`norway.SHARED_RAW`): refreshing them changes Oslo's inputs.
GTFS_ZIP = DATA_RAW / "rb_sky-aggregated-gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
ADDRESS_ZIP = DATA_RAW / "Basisdata_4601_Bergen_4258_MatrikkelenAdresse_CSV.zip"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# Skyss's aggregated GTFS through Entur - the same host and licence (NLOD) as
# Ruter's feed for Oslo. ⚠ A HEAD request is not a probe on Google Storage
# (200, size 0). feed_info.txt names Entur and declares NO validity window, so
# the fetch date pins the snapshot, as Oslo's.
GTFS_URL = ("https://storage.googleapis.com/marduk-production/outbound/gtfs/"
            "rb_sky-aggregated-gtfs.zip")
GTFS_SELF_ATTESTS = False

# Kommune 4601 - Bergen (Vestland). Kartverket's own boundary. Not the
# business filter - that is the sub-unit's own beliggenhetsadresse.kommunenummer.
KOMMUNE_NUMBER = "4601"
KOMMUNE_NAME = "Bergen"
BOUNDARY_URL = KOMMUNE_BOUNDARY_URL_TEMPLATE.format(code=KOMMUNE_NUMBER)
ADDRESS_URL = ADDRESS_URL_TEMPLATE.format(code=KOMMUNE_NUMBER, name=KOMMUNE_NAME)

# No Bybanen station lies outside the kommune (the brief, measured
# 2026-09-29). Step 1 still EXITS if one ever does, naming it.
NEIGHBOUR_KOMMUNER = {}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM 31N. Bergen's stations lie at 5.23-5.36 E, in zone 31 (0-6 E).
# NOT Oslo's 25832, and not Norway's national UTM 33 - derived per city.
CRS_PROJECTED = "EPSG:25831"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# THE STANDARD EDGES, by the spacing rule (docs/ring_rules.md): the collapsed
# stations' median nearest-neighbour gap is 624 m, over the ~550 m line.
# Oslo's halved edges (465 m median) are NOT Bergen's.
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Bybanen, both lines: route_type 901 (EXTENDED - a basic-type reader, or
# Oslo's 401/902 filter, sees no rail at all). Ferries (1004, 1008) are not
# drawn, Oslo's and Marseille's call.
ROUTE_TYPES_RAIL = ("901",)
ROUTE_IDS = ["SKY:Line:1", "SKY:Line:2"]

# GATE 3 - NOT RUN, recorded as such. No published per-line count was found:
# English and Norwegian Wikipedia (read 2026-09-29) give 35 stops for the
# network and no split by line, against the feed's 34 stop places and 33
# names (Bergen busstasjon is two stop places 70 m apart). A number that does
# not match is not a gate, and none is invented to fit (Goyang's precedent
# for a line whose published count does not reconcile).
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = (
    "none usable: Wikipedia (en, no) gives 35 stops network-wide, no per-line "
    "split, against the feed's 34 stop places / 33 names - read 2026-09-29")

# ONE STATION UNDER TWO NAMES - none. The three pairs under 300 m were read at
# the build (the brief's table): Byparken / Kaigaten (73 m) are the two lines'
# city termini, distinct named stops served by different lines, and stay two
# (the brief's lean; Oslo kept Stortinget / Stortorvet at 142 m as two);
# Nesttun sentrum / Nesttun terminal (254 m) and Bergen busstasjon /
# Nonneseter (258 m) are distinct stops.
STATION_NAME_ALIASES = {}

SPACING_MIN_M = 400.0

# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope is
# checkable. Counted after step 1's name collapse.
EXPECTED_INSIDE_PER_LINE = {"1": 28, "2": 10}

# route_short_name -> the name riders use. The feed's names are bare numbers;
# the mode word goes with them, as Oslo's "T-bane 1".
LINE_NAMES = {"1": "Bybanen 1", "2": "Bybanen 2"}

# ⚠ NEITHER SOURCE TELLS THE LINES APART: the feed has no route_color, and
# OSM's four route relations (7271947, 7271948, 14933911, 14933918) carry one
# colour for both, #BF4525. Line 1 keeps it; Line 2 takes a colour of this
# project's choosing that clears pipeline/linecolour.py (Oslo's Trikk 15 and
# Dublin's precedent for a line with no published colour). No "Skyss colour"
# is claimed for Line 2.
# Line 2's #9c27b0 was chosen 2026-09-29 on the measure: worst pin 55.2
# (Retail), 93.6 from Line 1, 98 from the heat ramp. Oslo's teal #00a3a8 sat
# at 34.0 from Personal services and was not taken. Line 1's #bf4525 is 40.8
# from Food service: OSM's colour, below the preferred 45, recorded.
LINE_COLOURS = {"1": "#bf4525", "2": "#9c27b0"}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "norway_sn2025"
RAW_CLASSIFICATION_COLUMN = "sn2025_label"
CITY_KEEP = "BERGEN"   # kept for the scaffold's templates; KOMMUNE_NUMBER filters

# The per-city catch-all verdict, on Bergen's own numbers (the screen,
# 2026-09-27): 96.990 "Andre personlige tjenester ikke nevnt annet sted" is
# 7.0% of storefronts, 83% sole traders, 8% with employees (Oslo 87% / 5%) -
# the home-based signature, dropped as in Oslo. The five retail catch-alls are
# kept, as in Oslo.
CATCH_ALL_EXCLUDE = ("96.990",)

# Sanity bounds: kommune 4601's avgrensningsboks (60.176-60.536 N,
# 5.145-5.687 E, Kartverket's kommuneinfo) plus ~0.02 deg.
BERGEN_BBOX = {
    "lat_min": 60.15,
    "lat_max": 60.56,
    "lon_min": 5.12,
    "lon_max": 5.71,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600404159)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("nb",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "node/4843690522": "'Knutepunktet', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4648154177": "'Botn', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4427011738": "'Dalen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4644216195": "'Gavlen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4676512253": "'Gjelet', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4820040732": "'Haugane', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4648151469": "'Hola', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4416815398": "'Kampen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4725822871": "'Klubben', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4939174538": "'Korsen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/5538716329": "'Kvernane', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4644216193": "'Kyrkja', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4648151468": "'Leitet', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4735185480": "'Liane', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4281046564": "'Myren', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4732029576": "'Neset', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4647570117": "'Rabben', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/5538715618": "'Setra', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/5538716452": "'Setra', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/6835335340": "'Skaret', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4750655803": "'Steinen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4644353138": "'Tangen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4750655793": "'Tangen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/291028924": "'Varden', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4195882657": "'Varden', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4644353095": "'Åsen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4086807873": "'Fjellet', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/6239376289": "'Hovden', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4095926431": "'Kampen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4648154144": "'Kampen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/10240417876": "'Kampen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4648153112": "'Klubben', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/11505839733": "'Osen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/4837590511": "'Såta', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/5029788562": "'Tangen', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "way/768568730": "'Treet', Bergen's 36 one-word terrain names stay (owner 2026-10-13, fifteen answers 6)",
    "node/5538716449": "'Borgasetra', No duplicate: no other row bears the name, so the duplicates rule does not apply (ROW_MERGE_M)",
    "node/9798473345": "'Gullstølen', No duplicate: no other row bears the name, so the duplicates rule does not apply (ROW_MERGE_M)",
    "node/4647570692": "'Riplestølen', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "way/446699596": "'Brushytten', An article of the object's own outweighs a private operator or a business reading (owner 2026-10-13, keep beats drop; dealer galleries go only without an article)",
    "way/23994272": "'Åsen batteri (Olsvik batteri)', Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "node/1808855907": "'Midtfjellet - Gullfjellet', Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "way/133607327": "'Bergen Kunsthall Project', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "way/186894043": "'Bibliotek for humaniora', A library with an article stays (owner 2026-10-13, fourth pass 39)",
    "way/199693848": "'Åsane kirke', A place of worship under a name of its own needs no article (NOTABLE_ONLY 2026-10-07; Anyang 2026-10-13: where the tags show worship or cannot tell, it stays)",
    "node/9811334757": "'Knulrtane', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "node/4702348094": "'Sanbrekkedalen', A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "way/679572967": "'KNM Brask', Statues, busts and public memorials stay, and monuments are not held to the notable rule (owner 2026-10-13, personal names 2; 2026-10-11 answer 5, measured and put back)",
    "node/318665121": "'Gamle Nordvik skole', The not-there rule reads demolished, removed or not yet open; a place that stands today stays (lifecycle 2026-10-13; was: on a place is not read)",
    "way/431495717": "a home tagged an attraction with a Wikipedia article of its own is kept (owner, 2026-10-13)",
    "node/12484079401": "'Walk of Fame', Statues, busts and public memorials stay, and monuments are not held to the notable rule (owner 2026-10-13, personal names 2; 2026-10-11 answer 5, measured and put back)",
    "node/6517695373": "'Vassenden skule', A landmark that stands, ruined, abandoned or under a former-use name, stays (owner 2026-10-13: keep all standing abandoned landmarks; third list 11: former in a name is not read as gone)",
    "Tvedtegården": "The Norwegian terrain endings are street endings (owner 2026-10-13, language calls 4)",
    "Skjentoppen": "The Norwegian terrain endings are street endings (owner 2026-10-13, language calls 4)",
    "Eidsvågtunet": "The Norwegian terrain endings are street endings (owner 2026-10-13, language calls 4)",
    "Søreidtunet": "The Norwegian terrain endings are street endings (owner 2026-10-13, language calls 4)",
    "Dokkeskjærskaien": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Sandven hageby": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Travparkvegen": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Arna Urban Vosseban-tunnelen": "Named bridges and tunnels stay as street rows (owner 2026-10-13, fourteen answers 1; fifteen answers 11)",
    "Sjøkrigsskoleveien": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
}
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    # Places of worship named only by a denomination, a body or a hall type (the flag read of 2026-10-13, applied on the owner's word;
    # docs/decisions_drafts/search-final.md).
    "node/4183335789": "a place of worship named only by its denomination, body or hall type is dropped (owner 2026-10-13, four rulings 1; fifteen answers 6; sixteen rulings 2; owner 2026-10-13, the flag read's verdicts, all approved)",
    "way/836616889": "a mall's, estate's or facility's own name on its paths, not a street (owner, 2026-10-13)",
    "way/1527765183": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1527782252": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1529682034": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1525517005": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1527783007": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1565166255": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1565527149": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1565527152": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1357775691": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1565527150": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1529669448": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/495454708": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1377721832": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "relation/18664583": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1527794774": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1529665794": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1527799712": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1325469437": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1527857530": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/723576175": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1527798427": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1565169429": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1565166254": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1528707234": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1357775690": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1529563917": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1357775689": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1565169428": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1387989913": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1528705791": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1565527151": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1529671226": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1529674789": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/645091826": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "relation/20954342": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1511049738": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1359574593": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1527783006": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1527765185": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1528707235": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1528707232": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/1528707233": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/5318178925": "an English description standing in for a name; a farmhouse ruin with no article",
    "relation/5899026": "a boat club's name on a bay",
    "way/1017790777": "an archery range tagged a park",
    "node/3572625935": "a two-letter code standing in for a name (historic=monument)",
    "node/3572625932": "a two-letter code standing in for a name (historic=monument)",
    "node/3572625927": "a two-letter code standing in for a name (historic=monument)",
    "node/3572625922": "a two-letter code standing in for a name (historic=monument)",
    "node/3572625920": "a two-letter code standing in for a name (historic=monument)",
    "node/3572625919": "a two-letter code standing in for a name (historic=monument)",
    "node/3572625918": "a two-letter code standing in for a name (historic=monument)",
    "node/3572625917": "a two-letter code standing in for a name (historic=monument)",
    "node/3572625916": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683977": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683974": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683962": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683950": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683948": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683944": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683936": "a two-letter code standing in for a name (historic=monument)",
    "node/3565684296": "a two-letter code standing in for a name (historic=monument)",
    "node/3538949785": "a two-letter code standing in for a name (historic=monument)",
    "node/3539632581": "a two-letter code standing in for a name (historic=monument)",
    "node/3539631471": "a two-letter code standing in for a name (historic=monument)",
    "node/3539632549": "a two-letter code standing in for a name (historic=monument)",
    "node/3539631469": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683975": "a two-letter code standing in for a name (historic=monument)",
    "node/3539683976": "a two-letter code standing in for a name (historic=monument)",
    "way/4733446": "a duplicate of the same name in another case",
    "way/121593086": "two path names joined in one name",
    "way/462851084": "a type word (hiking path), no name",
    "way/121758688": "a type word (bridleway), no name",
    "way/220706100": "a description (footpath between two streets), read as a way by -gaten",
    "way/1237868336": "a route description, read as a way by -vegen",
    "way/1160372588": "a route description, read as a way by -bakken",
    "way/145590613": "a route description, read as a way by -bakken",
    "way/704279161": "a typing slip for Christiania postveg, which keeps its row",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "node/4087939234": "Duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M 2026-10-08 and 2026-10-13; six answers 6: second nodes of one district dropped); held rows settled 2026-10-13",
    "node/4427011742": "Duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M 2026-10-08 and 2026-10-13; six answers 6: second nodes of one district dropped); held rows settled 2026-10-13",
    "node/4644353096": "Duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M 2026-10-08 and 2026-10-13; six answers 6: second nodes of one district dropped); held rows settled 2026-10-13",
    "node/5538716350": "Duplicates of one object are one row (NEAR_DUP_M, ROW_MERGE_M 2026-10-08 and 2026-10-13; six answers 6: second nodes of one district dropped); held rows settled 2026-10-13",
    "node/1070084018": "A wrong object's name is a glitch and goes by id (owner 2026-10-11); held rows settled 2026-10-13",
    "node/4181285524": "Museum, zoo and theme-park contents stay only with a Wikipedia article of their own (owner 2026-10-13, fifteen answers 4); held rows settled 2026-10-13",
    "node/11069317721": "A ride tagged a station is no station; where the operator's or network's name is the sign it goes by id (station_ride 2026-10-13; fifteen answers 4); held rows settled 2026-10-13",
    "node/12164308762": "A ride tagged a station is no station; where the operator's or network's name is the sign it goes by id (station_ride 2026-10-13; fifteen answers 4); held rows settled 2026-10-13",
    "node/11173604641": "A ride tagged a station is no station; where the operator's or network's name is the sign it goes by id (station_ride 2026-10-13; fifteen answers 4); held rows settled 2026-10-13",
    "node/11173604640": "A ride tagged a station is no station; where the operator's or network's name is the sign it goes by id (station_ride 2026-10-13; fifteen answers 4); held rows settled 2026-10-13",
    "node/1769605890": "A ride tagged a station is no station; where the operator's or network's name is the sign it goes by id (station_ride 2026-10-13; fifteen answers 4); held rows settled 2026-10-13",
    "way/13851029": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/13851031": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/391280999": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/391281000": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/391281001": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/24410103": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/25942042": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/25942307": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/26254255": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/26348707": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/292098126": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/391361418": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/391361419": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/391361420": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/391361422": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/393111934": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/393111936": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/417401874": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/496446607": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/496446608": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/496446610": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/496446612": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/975757816": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/975757817": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/975757822": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
    "way/975757823": "A row that is only the site's own name is dropped when minor ways alone carry it (owner 2026-10-13, fifteen answers 9); held rows settled 2026-10-13",
}
