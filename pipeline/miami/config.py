"""Miami settings. Scoped to the REGION rather than one municipality - the
only city here that is, and deliberately so.

WHY REGIONAL, WHEN EVERY OTHER CITY IS ONE MUNICIPALITY
-------------------------------------------------------
Metrorail leaves the City of Miami: its stations sit in Hialeah, Medley,
Coral Gables, South Miami and unincorporated Miami-Dade as well. Everywhere
else in this project, that would end the discussion - San Diego dropped 16
Trolley stations in neighbouring cities on the grounds that including them
needs those cities' own business data, sourced and verified separately.

Miami is the exception because that cost is not there. Miami-Dade County
licenses business tax receipts for ALL 34 of its municipalities in ONE file,
with one schema, one publisher and one set of terms - so the regional map needs
no extra sources, no cross-source dedup and no second licence review. Decided
by the project owner on 2026-09-21, and this is the first working proof of the
multi-jurisdiction idea that Seattle is planned around (where it will cost
10-12 separate registries).

Consequences carried through the rest of this file: there is no `CITY_KEEP`,
the boundary layer is a multi-municipality one used to NAME where each station
is rather than to filter, and the page is labelled "Miami (Regional)" because
a map spanning six municipalities cannot honestly be called Miami.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "miami" / "raw"
DATA_PROCESSED = ROOT / "data" / "miami" / "processed"
OUTPUTS = ROOT / "outputs" / "miami"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations genuinely dropped - only ones outside Miami-Dade County, which the
# rail network does not leave, so this is expected to be empty. Kept for the
# same reason every city has one: an empty file is evidence the check ran,
# whereas a missing file is indistinguishable from a check nobody did.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

# The regional scoping record, and the file that matters here instead: every
# station with the municipality it sits in. This is what lets a reader see the
# map deliberately spans several municipalities rather than silently leaking
# past a city boundary.
STATION_MUNICIPALITIES_CSV = OUTPUTS / "station_municipalities.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Unfiltered snapshot, written by step 2 every run for fetch_parcels-style
# lookups to consume. Kept even with no such lookup yet: the trap it avoids
# (a cache built from filtered output, so removed rows quietly return) has now
# been introduced twice in this project, in Los Angeles and San Diego.
BUSINESSES_PREFILTER_CSV = DATA_PROCESSED / "businesses_prefilter.csv"

# --- Raw inputs (see pipeline/miami/fetch_sources.py) ---------------------

# Miami-Dade "Local Business Tax", ArcGIS FeatureServer. 194,099 rows at
# 2026-09-21, all YEAR=2026, of which 175,982 are ACCSTATUS='Active'.
BUSINESS_SERVICE_URL = (
    "https://services.arcgis.com/8Pc9XBTAsYuxx9Ny/arcgis/rest/services/"
    "Local_Business_Tax_Feature_Layer_View/FeatureServer/0"
)
BUSINESS_STATUS_FILTER = "ACCSTATUS='Active'"

# Columns downloaded. OWNERNAME, MAILNAME and every MAIL* field are
# deliberately NOT here: OWNERNAME is populated on 100% of rows and is often a
# person, and the mailing address is a home address for a sole trader. BUSNAME
# is present on 100% of rows, so unlike Los Angeles (68% missing dba_name) and
# D.C. (49%) this city never has to fall back to a registrant's own name.
DOWNLOAD_FIELDS = (
    "OBJECTID",
    "RECEIPTNO",        # unique per row; NOT a premises key
    "ACCOUNTNO",
    "ACCSTATUS",
    "BUSNAME",          # the trade name
    "BUSADDR",
    "BUSCITY",
    "ZIPCODE",
    "MUNBUSLOC",        # municipality, e.g. "01 - MIAMI"
    "CATGRYNAME",       # the classification this city's taxonomy reads
    "CLASSDESC",        # coarser Florida statutory grouping, for reference
    "OCCDESC",          # free-text occupation, used for catch-all sampling
    "FOLIO",            # PARCEL id - not a premises key, see below
    "NOOFUNIT",
    "LAT",
    "LON",
)

# `transitdata.miamidade.gov` does not resolve; this host does, and is the URL
# the Mobility Database lists as official. No feed_info.txt, so no licence is
# declared in the feed - see docs/data_sources.md.
GTFS_URL = ("https://www.miamidade.gov/transit/googletransit/current/"
            "google_transit.zip")

# Miami-Dade municipal boundaries, same publisher as the business file.
# 77 polygons (municipalities are multi-polygon; dissolve by MUNICID), with
# NAME and a MUNICID that joins to MUNBUSLOC's prefix.
BOUNDARY_SERVICE_URL = (
    "https://services.arcgis.com/8Pc9XBTAsYuxx9Ny/arcgis/rest/services/"
    "Municipalitypoly_gdb/FeatureServer/0"
)

GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "businesses_active.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "municipalities.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 17N: the longitude (~-80.19) falls in the -84 to -78 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32617"

# --- Ring geometry ---------------------------------------------------------
# The shared edges. Metrorail stations are far apart (a heavy-rail line on its
# own right-of-way), so no New-York-style reduction is needed; the Metromover
# loops ARE tightly spaced, which is handled in step 1, not here.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# Miami-Dade Transit's rail, by route_id in its own feed. Four rail routes
# exist; three are drawn.
#
#   31009  REGULAR METRORAIL SERVICE            route_type 2   DRAWN
#   14457  METROMOVER INNER LOOP                route_type 0   DRAWN
#   14456  METROMOVER OMNI/BRICKELL OUTER LOOP  route_type 0   DRAWN
#   14458  AIRPORT PEOPLE MOVER (MIA Mover)     route_type 0   NOT DRAWN
#
# The airport mover is excluded because it runs terminal-to-rental-car-centre
# with no surrounding commerce to measure - the one rail route here where a
# ring would be empty by construction. Tri-Rail (commuter rail, a separate
# agency) is excluded as commuter rail is in every other city.
#
# NOTE ON METRORAIL'S NAME. Miami-Dade Transit signs Metrorail as TWO public
# lines, Green and Orange, which share the trunk and split north of Earlington
# Heights. Its GTFS publishes ONE route for both ("REGULAR METRORAIL SERVICE"),
# so there is no route_id per line to draw. Rather than invent a split the feed
# does not contain, the trunk is drawn once and labelled "Metrorail", which is
# what the system is called and what every station sign says above the line
# name. This is the mirror image of New York, where 29 GTFS services had to be
# grouped into the 11 trunks the MTA itself signs.
ROUTE_IDS = ["31009", "14457", "14456"]

# route_id -> (real public name, colour)
#
# COLOURS ARE THIS PROJECT'S OWN, NOT THE AGENCY'S, and that is the documented
# fallback rather than a departure: the add-city skill says to use an own
# palette when the official colours are ambiguous or shared, and here they
# collide with the business-category colours. MDT publishes Metrorail as
# `FF8040` (orange, against Food service's #eb6834), Metromover inner as
# `008080` and outer as `008000` (both against Personal services' #1baf7a, and
# barely distinguishable from each other). Purple / teal / brown are distinct
# from the three category colours and from one another.
LINE_NAMES = {
    "31009": ("Metrorail", "#7B1FA2"),
    "14457": ("Metromover Inner Loop", "#00838F"),
    "14456": ("Metromover Omni/Brickell Loops", "#5D4037"),
}

# Which end of each line carries its label; None = automatic (the end farthest
# from the other lines). The Metromover routes are closed LOOPS, so "the end
# farthest from the other lines" is close to meaningless for them - set
# explicitly if a rendered map lands them badly.
LINE_LABEL_ENDS = {}

# route_id -> the shape_id(s) whose geometry is drawn. A tuple means one line
# whose physical extent needs more than one shape, which map_common supports.
#
# Chosen from the real trip counts, not guessed. Metrorail publishes NINE
# shapes because the line BRANCHES and because MDT ships single-track working
# variants, so no single shape draws it:
#   211239 / 211260   Palmetto <-> Dadeland South, 22 stops, 292 pts  (Green)
#   211236 / 211251   MIA Airport <-> Dadeland South, 16 stops, 201 pts (Orange)
#   211235 / 211250   the airport spur alone, 2 stops, ~40 pts
#   211246 / 211263   "EHT - CUL SINGLE TRACK" working variants, 292 pts
#   211270            Earlington Heights -> Palmetto, 8 stops
# The Orange Line shares the Green trunk from Earlington Heights south, so the
# whole physical network is the Green trunk PLUS the airport spur: 211260 draws
# Palmetto->Dadeland South and 211250 draws Earlington Heights->MIA. The
# single-track variants are deliberately not drawn - they are the same track.
#
# Both Metromover loops publish their circuit as two or four partial arcs, so
# each needs a pair to close the loop. The outer route covers the Omni and
# Brickell loops: 123746 is the Brickell half (13 stops, 147 pts) and 123745
# the Omni half (9 stops, 78 pts); 123747/123748 are the same geometry in the
# other direction and would just overdraw it.
LINE_SHAPES = {
    "31009": ("211260", "211250"),
    "14457": ("123750", "123751"),
    "14456": ("123746", "123745"),
}

# GTFS stop names here are platform-level and messy: Metrorail has no
# `parent_station` at all, so its 46 stop_ids are 23 stations x 2 directions,
# named with four different suffix spellings ("... STATION RAIL NORTHBOUND",
# "... STAT.RAIL SOUTHBOUND", "... STAT. RAIL NORTHBOUND", "... STATION
# NORTHBOUND"). Metromover repeats each station once per loop direction and
# spells one station two ways. Step 1 strips the suffixes and then applies
# these aliases.
STATION_SUFFIX_PATTERN = (
    r"\s*(STAT\.?|STATION)?\s*(RAIL)?\s*(NORTHBOUND|SOUTHBOUND)\s*$"
    r"|\s*METROMOVER\s+STATION\s*$"
    r"|\s+STATION\s*$"
)

STATION_NAME_ALIASES = {
    # Metrorail: the feed abbreviates, and one station has since been renamed.
    "EARLINGTON HTS.": "Earlington Heights",
    "M.L. KING": "M.L. King",
    "UHEALTH JACKSON": "UHealth Jackson",
    "TRI-RAIL": "Tri-Rail",
    "HISTORIC OVERTOWN/LYRIC THEATRE": "Historic Overtown/Lyric Theatre",
    "MIAMI INTERNATIONAL AIRPORT": "Miami International Airport",
    # Metromover: the same station spelled two ways across the loops.
    "COLLEGE / BAYSIDE": "College/Bayside",
    "COLLEGE BAYSIDE": "College/Bayside",
    "WILKIE D FERGUSON": "Wilkie D. Ferguson Jr.",
    "MIAMI WORLDCENTER": "Miami Worldcenter",
    # MDT's own misspelling of its station's name. The public name is
    # Tenth Street/Promenade.
    "TENTH STREET PROMANADE": "Tenth Street/Promenade",
    # THE TWO ALIASES BELOW WERE FOUND BY MEASUREMENT, NOT BY READING NAMES,
    # and without them this feed yields two phantom stations.
    #
    # Metrorail calls the downtown interchange "GOVERNMENT CTR." and Metromover
    # calls it "GOVERNMENT CENTER". They are one station complex - the
    # uncollapsed pair sat 20.1 m apart, which is how the split surfaced.
    "GOVERNMENT CTR.": "Government Center",
    # MDT labels one inner-loop stop by its intersection rather than its
    # station name. Which station it is was NOT guessed: as its own row it fell
    # exactly 0.0 m from Bayfront Park, so the feed is describing Bayfront Park
    # by the cross-streets outside it.
    "BISCAYNE BD@E FLAGLER ST": "Bayfront Park",
}

# --- Gate 3: the operator's own per-line station counts ----------------------
# Keyed as step 1 keys its lines: the public names in LINE_NAMES. An
# interchange counts once on each line it serves (the seven downtown Metromover
# stations both drawn routes call at count on both). Nothing is cut by
# municipality here, so there is no before/after-scope distinction.
OPERATOR_STATION_COUNTS = {
    # Green and Orange Lines together: one route_id in MDT's feed, one drawn
    # line here. Palmetto - Dadeland South plus MIA.
    "Metrorail": 23,
    # The stations table marks 8 Inner Loop stations: Government Center,
    # Wilkie D. Ferguson Jr., College North, College/Bayside, First Street,
    # Bayfront Park, Knight Center, Miami Avenue.
    "Metromover Inner Loop": 8,
    # Omni Loop and Brickell Loop together (one route_id in the feed): the 7
    # downtown stations they share with the Inner Loop, Third Street, 6 Omni
    # and 6 Brickell stations. Park West is the table's older name for Miami
    # Worldcenter. 8 + 20 - 7 shared = MDT's 21.
    "Metromover Omni/Brickell Loops": 20,
}
OPERATOR_COUNTS_SOURCE = (
    "Metrorail 23: en.wikipedia.org/wiki/Metrorail_(Miami-Dade_County), read "
    "2026-10-01 - secondary (miamidade.gov's station list renders only in a "
    "browser). Metromover: 21 stations in total from Miami-Dade County's own "
    "Metromover page, miamidade.gov/global/transportation/metromover.page - "
    "primary; the per-loop split from en.wikipedia.org/wiki/Metromover's "
    "stations table - secondary. All read 2026-10-01."
)

# --- Business filtering ------------------------------------------------

# No CITY_KEEP: this map is regional. Every municipality in the county file is
# kept, and MUNBUSLOC records which one each row came from, so a reader (and a
# future bug) can see the composition. The ring assignment is what decides
# whether a business appears, exactly as in every other city.
MUNICIPALITY_COLUMN = "munbusloc"

# Encoding of this city's RAW source files, declared rather than inferred.
# pandas defaults to UTF-8 and raises on anything else - safe, but it leaves
# the next person to guess, and reaching for latin-1 to silence a
# UnicodeDecodeError corrupts accented names without ever failing. Declaring it
# makes the choice reviewable and part of the provenance. See the encoding rule
# in docs/data_sources.md; non-US cities are where this bites.
SOURCE_ENCODING = "utf-8"

TAXONOMY_SYSTEM = "miami_catgryname"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "catgryname"

# Premises key for deduplication.
#
# None of the obvious candidates is a premises: RECEIPTNO is unique per ROW
# (6,631 rows = 6,631 receipts), ACCOUNTNO is per account (6,167), and FOLIO is
# the PARCEL - 6,631 candidate rows share only 1,849 folios, because a mall or
# an office tower is one parcel holding dozens of businesses. Measured on the
# City of Miami's active storefront rows, 2026-09-21.
#
# So dedup is on name-plus-address, which gives 6,128 premises, of which 477
# (7.2%) hold licences in more than one category. The taxonomy module's
# BUCKET_PRIORITY decides which bucket such a premises lands in.
PREMISES_KEY = ["business_name", "address"]

# FOLIO is still worth carrying: it is the parcel join for a future residence
# check against Miami-Dade property data, the way San Diego uses APN and
# Philadelphia uses parcel_number.
#
# Coverage differs sharply by scope, which matters for that future check:
# 100% of active City of Miami rows carry a FOLIO, but only 45.7% of the
# regional storefront set does (13,693 of 29,979). So a residence filter built
# on it would work well inside the city and thinly outside it - measure before
# relying on it, rather than reading the city figure as the county figure.
PARCEL_COLUMN = "folio"

# Sanity bounds for the supplied LAT/LON: Miami-Dade County's real extent,
# which is the mapped area here. Measured 2026-09-21: 35,732 of 35,732 active
# City of Miami rows already fall inside this box, with no (0,0) placeholders -
# the best coordinate quality of any city in this project.
MIAMI_BBOX = {
    "lat_min": 25.13,
    "lat_max": 26.00,
    "lon_min": -80.90,
    "lon_max": -80.10,
}

# --- Place search (scripts/place_search_scaffold.py, 2026-10-12) ---

# The five municipalities the map names, then the census-designated place
# holding each station on unincorporated land (owner, 2026-10-13: "approve
# the narrowed shape"), not Miami-Dade County (1210692), which the wave's
# plan gave. Found through Nominatim and the OSM API, 2026-10-13, each
# station tested against the area's own geometry:
#   relation 1216769 Miami, 118853 Hialeah, 1216645 Coral Gables,
#   118855 Medley, 118861 South Miami;
#   way 33614621 Brownsville: Brownsville and Earlington Heights stations;
#   way 33614629 Gladeview: M.L. King station;
#   way 33614661 West Little River: Northside station (4 m outside
#     Gladeview at its full coordinates, measured on the first fetch);
#   relation 9853985 Glenvar Heights: Dadeland North station;
#   relation 1244549 Kendall: Dadeland South station.
# Miami International Airport station sits in none of them: no named area
# smaller than the county holds it (not the aerodrome, way 113657169, nor
# the City of Miami). Left outside the search area on the owner's word
# (2026-10-13: "1. leave it outside, record the exception"): the fetch's
# area line reports 1 of 42 stations outside every area, and that is the
# recorded exception, not a gap to close by widening the area.
PLACE_AREA = "(id:3601216769,3600118853,3601216645,3600118855,3600118861,2433614621,2433614629,2433614661,3609853985,3601244549)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
PLACE_LANGUAGES = ("en",)
PLACE_FOLD = None
PLACE_REVIEWED = {}
PLACE_DROPPED = {
    "node/14190528505": "'Brightline MiamiCentral Station', a description standing in for a name (owner, 2026-10-13)",
    "node/358726513": "'Monastery of the Exaltation of the Most Holy Cross', a religious residence",
    "node/358705528": "'Saint Sophias Church', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/358729276": "'Saint Kierans Church', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/358709835": "'Jose Marti Riverfront Park', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/375788345": "'Grace Evangelical', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "node/11226837657": "'Torch of Friendship', a duplicate beside the same thing's own row (owner, 2026-10-13)",
    "way/11145509": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/11145510": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/11145511": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/11145512": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/132683109": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/420897742": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/420897743": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/420897744": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/420897746": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/420897747": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/420897761": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/420897765": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/420897766": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/465982577": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/535301879": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/727945007": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1052983247": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1052983248": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1287229012": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1287229013": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1422940188": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1422940189": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1422940190": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1422940191": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1422940192": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1422940193": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1423313792": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1423317845": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1564263387": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1564263388": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1564263389": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/1564263390": "'Dadeland Mall', a shopping centre's own way, named for it",
    "way/11152692": "'Dadeland Mall Circle East', a shopping centre's own way, named for it",
    "way/1423313783": "'Dadeland Mall Circle East', a shopping centre's own way, named for it",
    "way/1423313784": "'Dadeland Mall Circle East', a shopping centre's own way, named for it",
    "way/1423313785": "'Dadeland Mall Circle East', a shopping centre's own way, named for it",
    "way/1423313786": "'Dadeland Mall Circle East', a shopping centre's own way, named for it",
    "way/968911204": "'Dadeland Mall Circle South', a shopping centre's own way, named for it",
    "way/1422940186": "'Dadeland Mall Circle South', a shopping centre's own way, named for it",
    "way/1422940187": "'Dadeland Mall Circle South', a shopping centre's own way, named for it",
    "way/314486142": "'Flooded Former Bike Path', a description standing in for a name (owner, 2026-10-13)",
    "way/1140708011": "'Florida's Turnpike Thru Lane', a description standing in for a name (owner, 2026-10-13)",
    "way/1237941689": "'Florida's Turnpike Thru Lanes', a description standing in for a name (owner, 2026-10-13)",
    "way/1237941690": "'Florida's Turnpike Thru Lanes', a description standing in for a name (owner, 2026-10-13)",
    "way/1237965580": "'Florida's Turnpike Thru Lanes', a description standing in for a name (owner, 2026-10-13)",
    "way/1237965582": "'Florida's Turnpike Thru Lanes', a description standing in for a name (owner, 2026-10-13)",
    "way/1237965584": "'Florida's Turnpike Thru Lanes', a description standing in for a name (owner, 2026-10-13)",
    "way/775090699": "'State Road 821 Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/118022775": "'WASD Access Road', a description standing in for a name (owner, 2026-10-13)",
    "way/11143024": "'Northwest 7th Avcr', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/167158237": "'Northwest 7th Avcr', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/11127596": "'Southwest 61st Ctcr', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/536843564": "'Southwest 61st Ctcr', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1163237149": "'Southwest 61st Ctcr', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/1313188612": "'Southwest 113th Plcr West', a glitched name (cut short, stray characters or two names in one), not repaired (owner, 2026-10-13)",
    "way/11132743": "'Southwest 93rd Placetiger:cfcc=A41', a notice or code glued onto the name: a glitch (owner, 2026-10-13)",
    "way/190819763": "'Northwest 11700 Block', a description standing in for a name (owner, 2026-10-13)",
    "way/11118926": "'Poinciana Closed Road', a description standing in for a name (owner, 2026-10-13)",
    "way/278805163": "'Southwest 112th Street', not a street: another kind of object indexed as one",
    "way/278805207": "'Southwest 112th Street', not a street: another kind of object indexed as one",
    "way/806890613": "'Southwest 124th Street', not a street: another kind of object indexed as one",
    "way/806890614": "'Southwest 124th Street', not a street: another kind of object indexed as one",
    "way/806890617": "'Southwest 120th Street', not a street: another kind of object indexed as one",
    "way/806890618": "'Southwest 120th Street', not a street: another kind of object indexed as one",
    "way/806899638": "'Southwest 144th Street', not a street: another kind of object indexed as one",
    "way/806899639": "'Southwest 144th Street', not a street: another kind of object indexed as one",
    "way/806899644": "'Southwest 128th Street', not a street: another kind of object indexed as one",
    "way/806899645": "'Southwest 128th Street', not a street: another kind of object indexed as one",
    "node/6942721481": "'Medley Landfill', private facility: a landfill tagged a peak: an operating waste site, by id (flag check, 2026-10-13)",
    "node/11226868716": "'HMS Bounty', glitch: GNIS artifact: a replica ship's name on a hamlet node; the ship is not there (flag check, 2026-10-13)",
    "node/153971407": "'Medley Lakeside Retirement Community', a housing development mapped as a place (owner, 2026-10-13)",
    # The pattern screen of 2026-10-13: rows that fall squarely in one of the owner's
    # class rulings of that date, each with its ruling.
    "way/552197202": "'Alhambra Tower Plaza', the grounds of an office or apartment building, or of a housing estate by its operator, tagged a park or square (owner, 2026-10-13, the estate-facility ruling as applied to Toronto; pattern screen)",
}

# Public sights kept by id: in the cache, passed over by the rules (place_index,
# PLACE_KEPT; owner, 2026-10-13).
PLACE_KEPT = {
    "node/4587210554": "'Calle Ocho Walk of Fame', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "relation/10225212": "'Fairchild Botanical Garden', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/435748157": "'Historic Black Police Precinct Courthouse and Museum', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/589514585": "'Institute of Contemporary Art, Miami', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/117926304": "'Jungle Island', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/435847255": "'Rubell Museum', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
    "way/1420651228": "'The Kampong', owner, 2026-10-13: a public sight the rules pass over for want of a tag",
}
