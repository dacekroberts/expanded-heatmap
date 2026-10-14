"""Oslo-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; every scaffolded placeholder has been
replaced with a measured value, so this module ships none.

FIRST NORWEGIAN CITY. The national facts - the register, its columns, the
contact columns never to load, the sole-trader guard - live in
`pipeline/countries/norway.py`; the shared step 2 in `norway_register.py`.
What is Oslo's own is below: the kommune, the address file, the scope, the
rail, the palette and the catch-all verdict.
"""

from pathlib import Path

from pipeline.countries.norway import (  # noqa: F401
    ADDRESS_URL_TEMPLATE,
    KOMMUNE_BOUNDARY_URL_TEMPLATE,
)

SLUG = "oslo"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "oslo" / "raw"
DATA_PROCESSED = ROOT / "data" / "oslo" / "processed"
OUTPUTS = ROOT / "outputs" / "oslo"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the kommune, with the kommune each IS in - a citable
# scoping record. Twelve rows, every one on the T-bane's two western branches
# into Bærum.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all public and keyless. `fetch_sources.py` downloads them; no
# step may fetch. The two register files are NATIONAL and cached once for the
# country (`norway.SHARED_RAW`), as France's SIRENE parquets are.
GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
ADDRESS_ZIP = DATA_RAW / "adresser_0301.zip"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# Ruter's aggregated GTFS through Entur, Norway's national access point.
# ⚠ A HEAD REQUEST IS NOT A PROBE HERE: Google Storage answers 200 with size 0
# and an empty content-type, which reads exactly like an empty file. A ranged
# GET returns 206 and `PK\x03\x04`. Measured 2026-09-24 at 50,999,897 bytes.
#
# ⚠ `feed_info.txt` EXISTS BUT DECLARES NO WINDOW - publisher Entur, language
# `no`, and no feed_start_date / feed_end_date. So, like Toulouse, the fetch
# date is what pins the snapshot, and fetch_sources records it.
GTFS_URL = ("https://storage.googleapis.com/marduk-production/outbound/gtfs/"
            "rb_rut-aggregated-gtfs.zip")
GTFS_SELF_ATTESTS = False

# Kommune 0301 - Oslo. Kartverket's own boundary, 480.5 km² as measured
# (the land area usually quoted is ~454 km²; the polygon includes the inner
# fjord). ⚠ Not the business filter - that is the sub-unit's own
# `beliggenhetsadresse.kommunenummer`.
KOMMUNE_NUMBER = "0301"
KOMMUNE_NAME = "Oslo"
BOUNDARY_URL = KOMMUNE_BOUNDARY_URL_TEMPLATE.format(code=KOMMUNE_NUMBER)
ADDRESS_URL = ADDRESS_URL_TEMPLATE.format(code=KOMMUNE_NUMBER, name=KOMMUNE_NAME)

# The kommunes that hold an EXCLUDED station, fetched so step 1 can NAME each
# one's municipality offline - the Los Angeles rule. Only Bærum: all 12
# outside stations are on the T-bane's Kolsås and Østerås branches. Step 1
# exits if a station falls outside Oslo AND outside every kommune listed here.
NEIGHBOUR_KOMMUNER = {"3201": "Bærum"}
NEIGHBOURS_GEOJSON = DATA_RAW / "neighbour_kommuner.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM 32N. Oslo's longitude (~10.75 E) falls in UTM zone 32 (6-12 E),
# derived per city as the invariant asks. Kartverket publishes Oslo's address
# file in 25832 among others, so this is also the zone its own data uses here.
# (Norway's national mapping grid is UTM 33, EPSG:25833 - that is a
# country-wide convenience, not Oslo's zone, and France's national-grid
# argument does not carry: Norway spans 32-35, and there is one city so far.)
CRS_PROJECTED = "EPSG:25832"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# NEW YORK'S TIGHT EDGES, on Toulouse's measured ground rather than inherited.
# Measured 2026-09-24 across the 155 in-kommune stations (nearest neighbour,
# ETRS89 / UTM 32N metres, after the name collapse and alias):
#
#     min 138    median 465    mean 500    max 1,707
#
# At a 465 m median the 483 m outer ring very nearly TILES - each station's
# edge stops just short of its neighbour's - where the default 966 m ring
# would reach two stations deep. That is the fit argument Toulouse's 525 m
# was taken on, and Lille's 501 m and Rennes' 541 m after it; applied on that
# measurement rather than re-asked. (Madrid, Barcelona, Dublin and Milan keep
# the default edges; their networks are sparser, so the argument differs.)
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# WHAT COUNTS - owner's calls, 2026-09-24:
#
#   * T-bane lines 1-5 (`route_type 401`) AND tram lines 12, 13, 15, 17, 18, 19
#     (`902`). Oslo's trams serve corridors the T-bane does not - Grünerløkka,
#     Frogner, Torshov, Sagene - which is Marseille's and Toulouse's shape
#     rather than Paris's or Prague's dense overlay, and all six are inside
#     the kommune.
#   * NOT the 6 ferry routes (`1008`, B1-B21), on Marseille's call: dropped
#     and disclosed, revisitable.
#
# ⚠ EVERY ROUTE TYPE HERE IS EXTENDED. Not one of the feed's 386 routes uses
# the basic 0-12 set; a basic-only reader sees zero rail in Oslo - the trap
# add-country records for Berlin, Hamburg, Stockholm and Oslo itself.
ROUTE_TYPES_RAIL = ("401", "902")
ROUTE_IDS = [f"RUT:Line:{n}" for n in (1, 2, 3, 4, 5, 12, 13, 15, 17, 18, 19)]

# TRAM 13 WEST OF THUNE IS CLOSED FOR WORKS, drawn as the timetable runs
# (docs/category_rules.md, "Station scope"): Sporveien's Lilleakerbanen
# rebuild closed Thune - Lilleaker from 10 June 2026, overhead-line work due
# to finish in February 2027 (sporveien.no/prosjekter-og-arbeid/lilleakerbanen,
# read 2026-10-03). The 2026-09-24 feed runs 13 Ljabru - Thune only, and
# replacement buses 13B/13E serve the tram stops. Step 1 STOPS once a rail trip
# calls at one of these tram-only stop places again, so the closure cannot
# outlast the map. NOT YET listed in excluded_stations.csv as the precedent
# asks: Sollerud is not in the cached stops.txt at all, and Lilleaker's tram
# quays cannot be told from its bus quays there (lane-docs, 2026-10-03).
CLOSED_FOR_WORKS_STOP_PLACES = {
    "NSR:StopPlace:61067": "Hoff",
    "NSR:StopPlace:61068": "Abbediengen",
    "NSR:StopPlace:61070": "Ullern",
    "NSR:StopPlace:61072": "Furulund",
}

# ✅ OSLO KOMMUNE ONLY, owner's call 2026-09-24, on the rule the French cities
# settled: the deciding measure is the WORST line's station survival.
#
#     T-bane 1  37/37   T-bane 2  38/47   T-bane 3  29/38 (76%)
#     T-bane 4  37/37   T-bane 5  45/51   every tram line 100%
#
# Line 3's 76% is better than Toulouse's T1 (52%) and Rennes' Métro b (73%),
# both commune-only; Lille went regional because its tram was a stub. The 12
# stations outside are ALL in Bærum (3201), on the Kolsås and Østerås branches.
# SIRENE's lesson applies: the register is national, so regional was a wider
# filter away, and declined.

# GATE 3 - NETWORK-LEVEL, and a SECONDARY source, recorded as such.
#
# The T-bane has 101 stations: the feed's 101 distinct parent stations for
# `route_type 401` match the figure Norwegian Wikipedia gives, and an OBOS
# article gives the same count for Sporveien's tracks (seen through a search
# summary, not read verbatim), 2026-09-24. Sporveien's own "Om Sporveien" page
# states no count. OSM could NOT be used, unlike Lille and Rennes: its line-2
# relation lists 25 stations against the feed's 47, so its relations are
# partial here. No per-line or tram figure from outside the feed was found,
# and none is invented.
OPERATOR_STATION_COUNTS = {"T-bane (network)": 101}
OPERATOR_COUNTS_SOURCE = (
    "101 T-bane stations: Norwegian Wikipedia and OBOS (citing Sporveien), "
    "read 2026-09-24 - a secondary source; no tram figure outside the feed")

# ONE STATION UNDER TWO NAMES - the alias list, explicit rather than a rule.
# The spacing gate flagged ten stations within 200 m; read by name 2026-09-24,
# exactly one pair is one place: the tram stop "Forskningsparken T" sits 12 m
# from the T-bane station "Forskningsparken" (Ruter's " T" suffix marks a stop
# serving the T-bane). The other four pairs under 200 m are real, distinct
# stops - Kjelsås / Kjelsåsalléen 138 m, Stortinget / Stortorvet 142 m,
# Heimdalsgata / Nybrua 152 m, Frydenlund / Welhavens gate 187 m. A blanket
# "strip the T suffix" rule was rejected: it would merge by spelling, and an
# alias merges only what was looked at.
STATION_NAME_ALIASES = {"Forskningsparken T": "Forskningsparken"}

# The shared spacing gate's floor on the collapsed stations' median spacing.
# The shared 400 m floor PASSES on its own terms (network-wide collapsed
# median 475 m), so no override is passed - unlike Paris and Marseille,
# which needed 200. Kept as a named setting so a future change is visible.
SPACING_MIN_M = 400.0

# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope
# decision is CHECKABLE rather than merely written down. Counted after step
# 1's name collapse, so tram figures sit a stop or two below a count of stop
# places (Trikk 12 is 32 names across 33 places). If these move, the scope
# decision is being re-taken and should be re-taken deliberately.
EXPECTED_INSIDE_PER_LINE = {
    "1": 37, "2": 38, "3": 29, "4": 37, "5": 45,
    "12": 32, "13": 23, "15": 34, "17": 28, "18": 27, "19": 22,
}

# route_short_name -> the name riders use. Ruter numbers its lines; the mode
# word distinguishes T-bane 1 from a bus 1.
LINE_NAMES = {
    "1": "T-bane 1", "2": "T-bane 2", "3": "T-bane 3", "4": "T-bane 4",
    "5": "T-bane 5",
    "12": "Trikk 12", "13": "Trikk 13", "15": "Trikk 15", "17": "Trikk 17",
    "18": "Trikk 18", "19": "Trikk 19",
}

# ⚠ THE FEED CANNOT COLOUR THESE LINES APART: every T-bane line is `EC700C`
# and every tram line `0B91EF`. Ruter's own network maps give each line its
# own colour, and OSM carries them on the route relations (operator Sporveien
# T-banen / Sporveien Trikken, network Ruter), read 2026-09-24.
#
# Nine of the eleven are Ruter's exact colours. Two were REFUSED by the shared
# check (pipeline/linecolour.py, Delta-E floor 10) and shifted in HSL
# LIGHTNESS ONLY, hue and saturation kept - Paris's bis-line and Lille's tram
# precedent:
#
#   T-bane 1  Ruter #0073db was 6.5 from the Retail pins (#2a78d6) - it would
#             vanish under its own pins. -> #0083fa (L .43 -> .49): worst pair
#             now 14.2, still vs Retail; 9.7 from Ruter's own shade. Darker
#             was rejected: it runs into T-bane 4's navy (#004a98).
#   Trikk 12  Ruter #a066aa was 5.7 from T-bane 3's #a85fa5 - Ruter's own two
#             purples are all but identical. T-bane 3 keeps Ruter's colour as
#             the primary line; Trikk 12 -> #ae7cb6 (L .53 -> .60): worst pair
#             13.5, vs T-bane 3; 9.8 from Ruter's shade.
#
# LIGHTER, not darker, for both: the maps open on a dark basemap, which the
# check does not score, and Lille's lesson is that a dark shade the check
# approves can vanish there - so both are confirmed in the browser too.
#
# Trikk 15 has NO Ruter colour recorded anywhere read: it is not in OSM, whose
# tram relations carry line 11 instead. The feed's 15 shares 32 of its 34
# stops with line 12 - line 11's Kjelsås service rerouted while the Briskeby
# line is closed (Sporveien: reopening autumn 2027). #00a3a8, a teal no other
# line or pin is near, is this project's choice, Dublin's precedent for a
# line with no published colour, and cleared the check first time.
LINE_COLOURS = {
    "1": "#0083fa", "2": "#ec700c", "3": "#a85fa5", "4": "#004a98",
    "5": "#32aa35",
    "12": "#ae7cb6", "13": "#00b26b", "15": "#00a3a8", "17": "#ed1b2f",
    "18": "#fdb913", "19": "#f7942a",
}

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "norway_sn2025"
RAW_CLASSIFICATION_COLUMN = "sn2025_label"
CITY_KEEP = "OSLO"   # kept for the scaffold's templates; KOMMUNE_NUMBER filters

# The per-city catch-all verdict, which norway_sn2025.py declines to make.
# TAKEN 2026-09-24 from Oslo's own measured profile:
#
#     96.990  Andre personlige tjenester ikke nevnt annet sted
#             813 rows (6.0%) - employees registered on 5%, ENK parent on 87%
#
# The strongest home-based signature measured in any city here: nearly nine in
# ten are sole traders and almost none employ anyone. France's 96.09Z, on
# Oslo's own numbers. The five RETAIL catch-alls (47.120, 47.270, 47.559,
# 47.690, 47.780) are kept, as in every French city - they are shops by
# product, and SN2025's labels carry no in-store/out-of-store distinction to
# argue from either way.
CATCH_ALL_EXCLUDE = ("96.990",)

# Sanity bounds: the kommune's measured extent (59.8093-60.1351 N,
# 10.4892-10.9514 E) plus ~0.02 deg. Catches a corrupt coordinate; the join
# to Kartverket's own address file does the placing.
OSLO_BBOX = {
    "lat_min": 59.79,
    "lat_max": 60.16,
    "lon_min": 10.47,
    "lon_max": 10.97,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3602775550)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("nb",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    "node/12963921538": "'Albert Nordengen', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/2792079636": "'Amaldus Nielsen', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/12943856329": "'Arne Garborg', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/8070893062": "'Arno Berg', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/12092706789": "'Arvid Storsveen', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/13236628537": "'Civilingeniør H. E. Heyerdahl', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/12945442516": "'Edvard Grieg', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/12707314255": "'Eivind Berggrav', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/3725012224": "'Gunnar Schjelderup', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/6578285081": "'Jens Olav Walaas Selvaag', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/12092702402": "'John Collett', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/12950534556": "'Niels Henrik Abel 1802–1829', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/12978566131": "'Theodor Julius Løvstad (1843 - 1913)', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    "node/2772161019": "'MS Scandinavian Star minnesmerke', a statue or public memorial is kept on its subject's article; only public art needs its own (owner, 2026-10-13)",
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "node/1375248821": "'Bakken', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/100699900": "'Berg', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "relation/14861977": "'Berntsberg', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/100711541": "'Blåsås', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/100711547": "'Engelsrud', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/123235755": "'Grønvoll', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/25801587": "'Hallset', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/123266583": "'Halvorsrud', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/100711534": "'Hammeren', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/100699837": "'Nordre Låkeberget', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/100692479": "'Sagbakken', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/100699849": "'Salmakerstua', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/101311622": "'Steinsrud', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/101222539": "'Svingen', Oslo farms and crofts with a visiting tag (website) are kept (15 answers no. 2: 14 kept)",
    "way/1371007440": "'Biblioteksparken', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "node/1180904125": "'Sinsenkrysset (G)', a drawn or network station is never dropped for its name (owner 2026-10-13, station guard)",
    "node/30391593": "'Sinsenkrysset (H)', a drawn or network station is never dropped for its name (owner 2026-10-13, station guard)",
    "node/2454616597": "'Storo (A)', a drawn or network station is never dropped for its name (owner 2026-10-13, station guard)",
    "node/2454616596": "'Storo (B)', a drawn or network station is never dropped for its name (owner 2026-10-13, station guard)",
    "node/2194522600": "'Airship “Norge” Landing Site', a monument is not held to the article rule and nothing in its tags says artwork (measured 2026-10-11, not applied)",
    "way/1539181176": "'Dyrafjeld', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "node/7626196291": "'Grefsenkollen øst', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "node/7626196288": "'Årvollåsen nordvest', admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "Alfaset 1. industrivei": "numbered roads on larger ways stay (15 answers no. 10)",
    "Alfaset 2. industrivei": "numbered roads on larger ways stay (15 answers no. 10)",
    "Alfaset 3. industrivei": "numbered roads on larger ways stay (15 answers no. 10)",
    "Kampen hageby": "a minor way is kept on a wikidata entry (street pass, 2026-10-07)",
    "Første tverrvei": "a number beside a type gets no rule; only cemetery and estate cases go by id (candidate 24)",
    "Andre tverrvei": "a number beside a type gets no rule; only cemetery and estate cases go by id (candidate 24)",
    "Mølleparken": "a minor way is kept on a wikidata entry (street pass, 2026-10-07)",
    "Battery Road": "admitted by the index rule for its kind; no drop rule or ruling reaches it by tags or name",
    "Vulkan": "a site's road with a street word, or a site name on residential or larger ways, stays (15 answers no. 9; six answers no. 4)",
}
PLACE_REVIEWED = {}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/26552882": "a shieling mapped as a farmyard, no article (owner, 2026-10-13)",
    "way/100711546": "a shieling mapped as a farmyard, no article (owner, 2026-10-13)",
    "way/852020349": "a shieling mapped as a farmyard, no article (owner, 2026-10-13)",
    "way/102657082": "a shieling mapped as a farmyard, no article (owner, 2026-10-13)",
    "node/2284244739": "a company's name on a building (owner, 2026-10-13)",
    "node/2417487842": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487843": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487844": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487845": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487846": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487847": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487848": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487849": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487850": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487851": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487798": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487853": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487854": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487855": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487856": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487857": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487858": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487859": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487860": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487861": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487862": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487852": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487864": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487865": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487866": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487804": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487867": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487868": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487869": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487863": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487870": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487871": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487872": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487873": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487874": "a numbered sculpture group carrying another work's article and none of its own",
    "node/2417487875": "a numbered sculpture group carrying another work's article and none of its own",
    "node/7841902315": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/3067087516": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/201990033": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2010674594": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2339841280": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1312111242": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/4528237822": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/4183391945": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2044851744": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/7841902316": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2365756849": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/4136984765": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/3602443123": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/849580535": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/259421682": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/258567409": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "relation/11788446": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/270276929": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/586017858": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/49170660": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "relation/11486211": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1177750572": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/863303131": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/87173178": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/840692462": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/227942592": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/160805245": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/123065402": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/832950660": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/251129531": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/84301626": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/81106341": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/282803375": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/332680064": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/842063699": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/853741022": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2673511221": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/832473899": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/4156024496": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/839686651": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/840692464": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/150404214": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/855450700": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/108002071": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/329045994": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/221795773": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/305862807": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/839686656": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/101827998": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/102951815": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/832388783": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/844513554": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/150404216": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/171439936": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/855559383": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/798732155": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/87173184": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/849586422": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/839602287": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/858937154": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2685804657": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/199120197": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/832736111": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/872014125": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/318139908": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/835226857": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/218470359": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/852624525": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/227942594": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/831287614": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/854154580": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/280873377": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/832521217": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/13343318753": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/218470356": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/143415740": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "relation/11721268": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "relation/14618015": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/798129075": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/83678369": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/84866433": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/219149633": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/221175704": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/251129530": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/219490573": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/121952821": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/853711908": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374991454": "a historic farm or croft with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2974460938": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1375248843": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2385586710": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1177681971": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2285708273": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374970052": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1373559434": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1372925586": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374970072": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374970075": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2260489683": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1372925589": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/6418198809": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1375248888": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2302344471": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1772934740": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1375248899": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1375248901": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374970099": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374970100": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/2302267648": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374852455": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374970104": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/1374970141": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "way/116273646": "a house or cabin ruin with no article: a home until visiting is shown (owner, 2026-10-13)",
    "node/5265486872": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486874": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486875": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486876": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486877": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486878": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486879": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486880": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486881": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486882": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5265486883": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/12950209373": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/9926645094": "a section of the open-air museum on Bygdoy tagged a locality: museum contents",
    "node/5379314697": "an exhibition of the open-air museum tagged a place of worship: museum contents",
    "node/12974397863": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397864": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397866": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397867": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397869": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397870": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397871": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397875": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397877": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12974397878": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168004": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168005": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168006": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168007": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168008": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168009": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168010": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168011": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168013": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168016": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168017": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168021": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168022": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12975168025": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/5820532055": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/7790645430": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/7790645431": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/7790645432": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12952721522": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12952721524": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12952721525": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12952721527": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "node/12952721534": "a grave marker in a cemetery, tagged with the buried person's article and none of its own",
    "way/1538940350": "an information point tagged public art, carrying the promenade's article; three share one numbered name at three sites",
    "node/11435595487": "an information point tagged public art, carrying the promenade's article; three share one numbered name at three sites",
    "node/12964231370": "an information point tagged public art, carrying the promenade's article; three share one numbered name at three sites",
    "node/12964272486": "an information point tagged public art, carrying the promenade's article; three share one numbered name at three sites",
    "node/13924380545": "a plaque carrying its subject's article and none of its own",
    "node/13924380544": "a plaque carrying its subject's article and none of its own",
    "node/10974134428": "a plaque carrying its subject's article and none of its own",
    "node/682977": "public art with no article, carrying the square's name instead of its own",
    "node/12791995855": "an English description standing in for a name; closed to the public by its tags",
    "relation/3108232": "a description of a historic trail network standing in for a name",
    "node/7222675428": "a waymarker's distance text and symbol standing in for a name",
    "node/7626196289": "a test object by its own description tag",
    "node/8776909021": "a type description whose name says the thing is temporary",
    "node/12879520445": "a disused station entrance, no access",
    "way/182543236": "a dead railway alignment with no article, named by an English description",
    "way/85030626": "a building that collapsed in 2018 by its tags",
    "node/7801910943": "a farmhouse ruin with no article",
    "node/1177682039": "a villa ruin with no article",
    "node/1905710514": "an abandoned cabin's ruin named for its occupant",
    "node/2934267934": "a cabin ruin named for a person",
    "way/1299861747": "a block's back yard tagged a park (read from the name)",
    "node/13397376242": "a duplicate of the tram stop row ten metres away; the weaker of the two",
    "way/100711552": "a segment of a wall whose group relation already has the row",
    "way/149766012": "a segment of a wall whose group relation already has the row",
    "way/1091836735": "a segment of a wall whose group relation already has the row",
    "way/158265217": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/862830018": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/835441607": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "relation/11788354": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/480577338": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/293875567": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/265169155": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/866528172": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/858937153": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/837216821": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/253262643": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/220133617": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/328364390": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/258564352": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/835467047": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/859430930": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/866072925": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/169261976": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/836490850": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "relation/20589289": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/835568024": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/836228748": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/859526641": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/134212662": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/845241737": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/117958544": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/862830019": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/258567402": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/863507802": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/858790772": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/864539352": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/150819768": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/673043540": "a historic farm (historic=croft) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/288982689": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/845493022": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/155603579": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/858287633": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/837289167": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/868252073": "a historic farm (historic=croft) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/284691735": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/216763963": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/860928591": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/158322905": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/317290200": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/859314021": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/170644786": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/858595297": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/844789395": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "node/1987120009": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/288982397": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/860237543": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/844380367": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/863094749": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/860718327": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/48831372": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/840603246": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/188088022": "a historic farm (historic=farm) with no article and no tag that shows visiting; held to the home rule (owner, 2026-10-13)",
    "way/371203723": "an address number standing in for a name",
    "way/1216114436": "a code beside a path type on minor ways",
    "way/5121756": "a code beside a path type on minor ways",
    "way/1216114435": "a code beside a path type on minor ways",
    "way/5121757": "a code beside a path type on minor ways",
    "way/5121758": "a code beside a path type on minor ways",
    "way/377668732": "a description (shortcut to the bus), no name",
    "way/1007208412": "a type word (operations road), no name",
    "way/1216696778": "a type word (operations road), no name",
    "way/307957296": "a station exit's description, read as a way by -torget",
    "way/1391431246": "a closed station's entrance, read as a way by plass",
    "way/838972652": "an English description, no name",
    "way/838972654": "an English description, no name",
    "way/838972655": "an English description, no name",
    "way/838972656": "an English description, no name",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "node/9508285838": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/9508285868": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/9508285869": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/9508285872": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/9508285873": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/9508285874": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/9508285879": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/9508285880": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/13280145218": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/13280145219": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/13715634847": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/13715634848": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/13715634849": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/13715634850": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/13715596513": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "node/13715597005": "a housing development mapped as a place is dropped by id (owner 2026-10-13, four rulings no. 2); held rows settled 2026-10-13",
    "way/1058666314": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/837640491": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/335046470": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/268683600": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "way/1434402611": "bare type word or type phrase as the whole name is dropped (BARE_TYPE_NAMES; owner 2026-10-11, 2026-10-13); held rows settled 2026-10-13",
    "relation/2674312": "a historic route relation named by its course (owner, 2026-10-13)",
    "relation/1786979": "a historic route relation named by its course (owner, 2026-10-13)",
    "relation/1782816": "a historic route relation named by its course (owner, 2026-10-13)",
    "relation/6358728": "a historic route relation named by its course (owner, 2026-10-13)",
    "relation/3403035": "a historic route relation named by its course (owner, 2026-10-13)",
    "relation/4502681": "a historic route relation named by its course (owner, 2026-10-13)",
    "relation/4502680": "a historic route relation named by its course (owner, 2026-10-13)",
    "relation/1450386": "a historic route relation named by its course (owner, 2026-10-13)",
    "node/12401818916": "a pool, club, pitch or office tagged a park is dropped by id (settled read call; third list no. 15); held rows settled 2026-10-13",
    "node/12401831770": "a pool, club, pitch or office tagged a park is dropped by id (settled read call; third list no. 15); held rows settled 2026-10-13",
    "node/7240592307": "a business or a private club with nothing else and no article is dropped (business rule 2026-10-07); held rows settled 2026-10-13",
    "way/312668136": "a row that is only the site's own name, on minor ways alone, is dropped (15 answers no. 9); held rows settled 2026-10-13",
}
