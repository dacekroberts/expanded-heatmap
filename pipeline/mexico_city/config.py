"""Mexico City-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

MEXICO CITY IS THE FIRST CITY HERE WHOSE RAIL DOES NOT COME FROM GTFS, and the
reason is not a preference. Every `*.cdmx.gob.mx` host - the city open-data
portal, STC Metro, and STE (Tren Ligero) - returns ConnectTimeout, on `www.`
and bare, http and https, re-confirmed 2026-09-22. No block page prints an IP,
so this is a dead host from here rather than a client refusal, and the browser
does not help. The feed's S3 `direct_download` returns 403.

So the geometry comes from OpenStreetMap, approved by the owner on 2026-09-22
as a documented per-city exception rather than a new default. What that costs
is recorded honestly in two places: the city page says where the geometry came
from, and `STATION_COUNT_GATE_3` below records that the operator's published
station count CANNOT be checked, because the operator is unreachable.
"""

from pathlib import Path

from pipeline.countries.mexico import (  # noqa: F401
    DENUE_ACTIVITY_COLUMN,
    DENUE_CODE_COLUMN,
    DENUE_INTERIOR_COLUMN,
    DENUE_MUNICIPIO_COLUMN,
    DENUE_NAME_COLUMN,
    DENUE_MUNICIPIO_CODE_COLUMN,
    DENUE_PARTS,
    DENUE_STATE_COLUMN,
    FORBIDDEN_COLUMNS,
    OSM_NEVER_A_STATION,
    OVERPASS_HOSTS,
    OVERPASS_USER_AGENT,
    PREMISES_TYPE_COLUMN,
    PREMISES_TYPE_KEEP,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
    TAXONOMY_SYSTEM,
    denue_member,
    denue_members,
    denue_url,
    denue_urls,
)

# Re-exported above rather than redefined: every one of those names is a fact
# about DENUE or about OpenStreetMap, not about this city, and both Mexican
# cities were measured to agree on all of them before the split. The `noqa`
# is deliberate - these ARE unused here and are imported so that this city's
# step files keep importing them from this module, unchanged.

# --- Scope ---------------------------------------------------------------
#
# Mexico City (Regional): Ecatepec de Morelos, Nezahualcóyotl, La Paz and
# Naucalpan de Juárez added for the 11 stations of Líneas A, B and 2 that lie
# in the State of México (marked by the owner 2026-10-04; Naucalpan kept and
# the downloads approved 2026-10-06, calls 68-72; brief
# docs/build_briefs/mexico_city_regional.md). False reproduces the city-alone
# build byte for byte, which is how the extension was proved before it was
# switched on.
REGIONAL = True
NAME = "Mexico City (Regional)" if REGIONAL else "Mexico City"

# The four State of México municipios, keyed on INEGI's code as Monterrey's
# are (pipeline/monterrey/config.py): OSM's `INEGI:MUNID` equals DENUE's
# cve_ent + cve_mun, so register and boundaries join on one code. The names
# exist only to be ASSERTED against DENUE's own `municipio` column, so a wrong
# code fails loudly. Codes checked 2026-10-06 against INEGI's catalogue
# (gaia.inegi.org.mx/wscatgeo/mgem/15, 125 municipios).
REGIONAL_STATE_CODE = "15"
MUNICIPIOS = {
    "033": "Ecatepec de Morelos",
    "058": "Nezahualcóyotl",
    "070": "La Paz",
    "057": "Naucalpan de Juárez",
}
MUNIDS = tuple(REGIONAL_STATE_CODE + code for code in MUNICIPIOS)
# The 11 stations of Líneas A, B and 2 in the four, by municipio (staging's
# probe 2026-10-04, line membership re-measured 2026-10-06). Step 1 asserts
# them by point in polygon on INEGI:MUNID.
STATIONS_PER_MUNICIPIO = {"033": 5, "058": 3, "070": 2, "057": 1}

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "mexico_city" / "raw"
# data/ is one junction shared by every worktree, and master's checks read
# processed/: the regional build writes processed/regional/ until it lands
# (regional-extension, Step 1). Fold back to processed/ on landing.
DATA_PROCESSED = (ROOT / "data" / "mexico_city" / "processed"
                  / ("regional" if REGIONAL else ""))
OUTPUTS = ROOT / "outputs" / "mexico_city"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities). Lines A, B and 2 run into Estado de Mexico, where the
# city-alone build has no business data, so their 11 stations there are cut
# rather than left to anchor rings over a blank. With REGIONAL on, all 11 are
# kept and the file is written header-only.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- Raw inputs -----------------------------------------------------------
#
# BUSINESSES: INEGI DENUE. Measured for this entidad on 2026-09-22 -
# 45,439,249 bytes, a real ZIP by magic bytes. The URL shape, the member path,
# the keyless/no-CAPTCHA finding and the reason the DENUE API is not used are
# all facts about DENUE and live in pipeline/countries/mexico.py.
#
# RAIL + BOUNDARY: OpenStreetMap via Overpass, fetched by step1 (see the module
# docstring for why not the agency).
#
# 09 = Ciudad de Mexico. THE ONLY PER-CITY PART OF THE DOWNLOAD - the URL
# shape, the member path and the near-miss dictionary member are all facts
# about DENUE and live in pipeline/countries/mexico.py.
#
# The file IS the state, so no city-name filter is needed for businesses: the
# in-city question is answered by which file is downloaded, which is why
# CITY_KEEP does not exist for this city and does for Guadalajara.
DENUE_STATE_CODE = "09"
DENUE_URL = denue_url(DENUE_STATE_CODE)
DENUE_MEMBER = denue_member(DENUE_STATE_CODE)
DENUE_ZIP = DATA_RAW / f"denue_{DENUE_STATE_CODE}_csv.zip"

# 15 = State of México, read only when REGIONAL is on. INEGI publishes it in
# TWO ZIPs (pipeline/countries/mexico.py, DENUE_PARTS), 50,572,588 and
# 30,236,017 bytes, both Last-Modified 2026-05-20: the 05/2026 edition, the
# same as the cached entidad 09 file. New file names in the shared data/, so
# nothing on master's path is overwritten.
DENUE_REGIONAL_URLS = denue_urls(REGIONAL_STATE_CODE)
DENUE_REGIONAL_MEMBERS = denue_members(REGIONAL_STATE_CODE)
DENUE_REGIONAL_ZIPS = tuple(
    DATA_RAW / f"denue_{part}_csv.zip" for part in DENUE_PARTS[REGIONAL_STATE_CODE]
)

OSM_STATIONS_JSON = DATA_RAW / "osm_stations.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
# The four municipios' admin_level=6 relations, by INEGI:MUNID (REGIONAL only).
OSM_MUNICIPIOS_JSON = DATA_RAW / "osm_municipios_15.json"

# --- OpenStreetMap fetch --------------------------------------------------

# The host list and its 504 history moved to pipeline/countries/mexico.py -
# which Overpass mirrors answer is a fact about Overpass, not about this city.
#
# Wide enough for Line A to La Paz and Line B to Ciudad Azteca, both in Estado
# de Mexico. A tighter box (19.04-19.62) silently returned 159 station nodes
# against 184 - the boundary filter, not the bbox, is what scopes this city.
OSM_BBOX = "18.95,-99.45,19.75,-98.85"

# WHITELIST, NOT A BLACKLIST, and this is not a style preference. OSM carries
# 13 PROPOSED Texcoco light-rail stations in this bbox, and five of them are
# tagged `railway=prpopsed` - misspelled in the source data. Excluding
# `railway=proposed` would have let those five through and drawn rings around
# building sites, which is Israel's STATUS trap. Keeping only railway=station
# is immune to the typo.
#
# NOT ENOUGH ON ITS OWN: nine Metro stations are only `railway=stop` positions
# on their route relation, so step 1 also takes the named stop members of the
# drawn relations (pipeline/stations.py's route_stop_members), and raises if
# any stop is still left without a station (2026-10-04,
# DECISIONS.md). Proposed stations are on no
# route relation, so membership keeps the typo immunity.
OSM_RAILWAY_KEEP = ("station",)
# railway=subway_entrance is 447 nodes against 184 stations - 2.4x. Counting
# entrances as stations is the Israeli entrances trap and would inflate every
# ring. Named here so the exclusion is explicit rather than incidental.
OSM_EXCLUDE_RAILWAY = ("subway_entrance", "proposed", "construction", "prpopsed")

# Both operators are kept: STC Metro (12 lines) and STE Tren Ligero (1 line).
# Tren Ligero is a different operator and a different mode, and it is included
# on the same reasoning that put Metromover on Miami's map and the Valley Line
# on Edmonton's - it is urban rail inside the city, and dropping it would leave
# the whole southern corridor to Xochimilco blank while the register still
# counts its shops. Metrobus is BRT and is NOT rail, so it is out.
OSM_STATION_NETWORKS = ("STC Metro", "Tren Ligero")

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 14N: the longitude (~-99.13) falls in the -102 to -96 band. Derived
# per city, not copied - see docs/project_context.md's CRS lesson.
CRS_PROJECTED = "EPSG:32614"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# GATE 3 IS UNAVAILABLE FOR THIS CITY AND THAT IS RECORDED, NOT WORKED AROUND.
# pipeline/stations.py calls the operator's published count "the one check that
# can see an error every internal check agrees with" - it is what corrected
# Edmonton 33->30 and Toronto 118->110. STC Metro publishes its station counts
# on metro.cdmx.gob.mx, which is unreachable from here (see the module
# docstring). A figure typed in from memory would LOOK like gate 3 and be
# worthless, so none is.
#
# What runs instead: the spacing gate, the railway=station whitelist above, and
# cross-direction agreement inside each route relation (each line has two
# direction relations whose station membership must match). Disclosed on the
# city page.
STATION_COUNT_GATE_3 = None
STATION_COUNT_GATE_3_REASON = (
    "STC Metro's published counts live on metro.cdmx.gob.mx, which returns "
    "ConnectTimeout from this environment on every host and scheme tried "
    "(2026-09-22). No published figure is asserted here."
)

# Measured from OSM on 2026-09-22, BEFORE the boundary filter. These are
# observations of the source, not the operator's figures - the names say so.
OSM_STATIONS_MEASURED = 184          # distinct STC Metro names in OSM_BBOX
OSM_TREN_LIGERO_MEASURED = 15        # distinct Tren Ligero names
OSM_PROPOSED_EXCLUDED = 13           # Texcoco light rail, 5 of them misspelled
OSM_ENTRANCES_EXCLUDED = 447         # railway=subway_entrance, never stations

# Real public line names and the operator's own livery colours, both straight
# from the OSM route relations, where `name`, `ref`, `colour`, `network` and
# `operator` are each 100% populated across all 26 relations. Keyed by `ref`.
LINE_NAMES = {
    "1": "Línea 1",
    "2": "Línea 2",
    "3": "Línea 3",
    "4": "Línea 4",
    "5": "Línea 5",
    "6": "Línea 6",
    "7": "Línea 7",
    "8": "Línea 8",
    "9": "Línea 9",
    "A": "Línea A",
    "B": "Línea B",
    "12": "Línea 12",
    "L1": "Tren Ligero",
}
#
# TWO OF THE THIRTEEN ARE DARKENED FROM OSM'S VALUE, and both are recorded here
# rather than silently adjusted. pipeline/linecolour.py RAISED on this city -
# the first time that check has stopped a build - because two pairs sat below
# the hard floor of Delta-E 10, where two colours are the same colour at a
# glance and a line disappears under its own pins:
#
#   Línea 2 #005EB8 vs Tren Ligero #0554ba   Delta-E  9.8   both blue
#   Línea 3 #AF9800 vs Línea 12    #B0A32A   Delta-E  8.5   both olive-gold
#
# These are LINE-VS-LINE clashes, which no previously built city hit; the
# check was written for line-vs-category. Resolved by the module's own rule -
# keep the agency's hue and change only lightness - and by moving the
# secondary line of each pair, so the more prominent service keeps the colour
# riders know:
#
#   Tren Ligero  #0554ba -> #033574  (lightness -0.14)  now 21.9 from Línea 2
#   Línea 12     #B0A32A -> #877D20  (lightness -0.10)  now 21.3 from Línea 3
#
# LÍNEA 2 IS DELIBERATELY NOT CHANGED, although it measures 10.4 against the
# Retail pin colour - the closest in the project after Calgary's historic 3.3.
# It is above the floor, and the 2026-09-21 branding decision keeps agencies'
# real route colours; fourteen line colours across six cities already sit in
# the 10-45 band and are recorded rather than repainted (New York's green at
# 13.6, Montréal's blue at 16.9). Darkening it to clear Retail was measured
# (-0.08 gives #00498F at 22.1) and rejected as overturning that decision for
# a line that is legible. Revisit only if a render shows it actually vanishing.
LINE_COLOURS = {
    "1": "#F04E98",
    "2": "#005EB8",
    "3": "#AF9800",
    "4": "#6BBBAE",
    "5": "#FFD100",
    "6": "#DA291C",
    "7": "#E87722",
    "8": "#009A44",
    "9": "#512F2E",
    "A": "#981D97",
    "B": "#B1B3B3",
    "12": "#877D20",   # darkened from OSM's #B0A32A - see above
    "L1": "#033574",   # darkened from OSM's #0554ba - see above
}

# --- Business filtering ------------------------------------------------



# Sanity bounds for coordinates, tightened to CDMX's real extent plus the
# Estado de Mexico reach of Lines A and B (cut later by the boundary filter).
MEXICO_CITY_BBOX = {
    "lat_min": 18.95,
    "lat_max": 19.75,
    "lon_min": -99.45,
    "lon_max": -98.85,
}

# ---------------------------------------------------------------------------
# Place search (batch 3, the size tests, 2026-10-11): pipeline/place_index.py
# builds app/static/places/mexico_city.json from the caches place_index_fetch.py
# writes. The search area is the map's: Ciudad de Mexico, relation 1376330 (admin_level 4, ISO3166-2 MX-CMX; the one OSM_BOUNDARY_JSON holds),
# confirmed by id 2026-10-11, AND the four State of Mexico municipios the
# regional map reaches (MUNICIPIOS above), by the admin_level 6 relations
# OSM_MUNICIPIOS_JSON holds, each matched on INEGI:MUNID: Ecatepec de Morelos
# 5605754, Nezahualcoyotl 5606086, La Paz 5605964, Naucalpan de Juarez
# 5606080. The index first landed cut to Ciudad de Mexico alone, and the 11
# stations in the four had 0 or 1 places within 1 km (owner, 2026-10-12;
# check H of check_place_search.py now refuses that). Overpass area id =
# 3600000000 + relation id.
PLACE_AREA = "(id:3601376330,3605605754,3605606086,3605605964,3605606080)"
# NEW file names: data/ is shared by every worktree.
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-12.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-12.json"
# The local language of OSM's names here: Spanish.
PLACE_LANGUAGES = ("es",)
PLACE_FOLD = None
# Index rows carrying a business or home word (place_index.LEAK_WORDS) that are
# places, each with why; scripts/check_place_search.py fails on any other.
PLACE_REVIEWED = {
    # Ecatepec, from the wider area of 2026-10-12: OSM ways 777821685 (name) and
    # 168525171, 848582662 (alt_name), all highway=residential.
    "Calle Estacionamiento": "a street's own name, residential class (the service-class ways of the same name are dropped by rule)",
    "G. Canal": "a residential street whose alt_name is Calle Estacionamiento, a street's own name",
    "Cerrada 1 Estacionamiento Santo Tomás": "a street's own name in a housing unit (a cerrada named for the car park it serves), residential class",
    "Cerrada 1 Estacionamiento Vista Hermosa": "a street's own name in a housing unit (a cerrada named for the car park it serves), residential class",
    "Cerrada Estacionamiento": "a street's own name in a housing unit, residential class",
    "Privada 2 Estacionamiento Manuela Medina": "a street's own name in a housing unit, residential class",
    "Privada Estacionamiento": "a street's own name in a housing unit, residential class",
    "Cerrada la Tienda": "a street's own name",
}
# OSM objects a reading by eye found to be a business or a home that no rule
# in place_index.py catches, each with why (place_index.build, `dropped`).
PLACE_DROPPED = {
    # From the read of the 1,240 rows the wider area added (the place-read agent, 2026-10-12): every id
    # printed its cached name first. Each under a settled call (the skill's "owner's calls").
    "way/558121084": "residents-only parks of a housing complex, by the mapper's own description",
    "way/544603168": "a condominium's numbered green tagged a park",
    "way/906659808": "a condominium's numbered green tagged a park",
    "way/558126092": "a house under a family's name tagged a park",
    "node/13581286261": "a condominium-tower brand tagged a neighbourhood",
    "node/13581286471": "a gated residential brand tagged a neighbourhood",
    "node/13581286507": "a gated residential brand tagged a neighbourhood",
    "node/13588750504": "a residential-complex brand tagged a neighbourhood",
    "relation/10542712": "a religious residence tagged a place of worship, not notable",
    "way/802738147": "a shopping mall tagged a park",
    "node/5338531394": "a travel agency tagged a park",
    "node/13585104659": "a private sports club tagged a neighbourhood",
    "node/6936086418": "a sports club with opening hours tagged a park",
    "way/545099518": "a well named for the chain store beside it",
    "node/12574189307": "a minibus route's office tagged a station",
    "node/6237356685": "a person's name alone on a monument node",
    "node/10203187281": "a mapper's comment as a name",
    "node/9969120518": "a mapper's comment as a name",
    "way/555585757": "an address as a name",
    "way/1350986475": "a block and lot number as a name",
    "way/680999072": "a description: a garden on an unnamed cul-de-sac",
    "node/6377133599": "a description: the same garden's node",
    "way/1038945277": "a description: an exercise area",
    "way/1038945276": "a description: a play area with tables",
    "way/550890540": "a description: a green area with walkways",
    "way/628362796": "a description: a bridge with a park",
    "way/550775492": "a description: a kiosk and park",
    "way/549459849": "two type words as a name",
    "way/777204260": "a works area named for its use",
    "node/5320713767": "a bench with a palm tagged a place of worship",
    "node/6936071700": "a cemetery gate tagged a place of worship",
    "node/5371263214": "water tanks tagged a park",
    "way/584498564": "a description: a street corner",
    "way/557195869": "a description: football pitches",
    "node/5320852853": "a chapel named only for the market beside it",
    "node/13690861201": "a wrong object: an animal's name on a castle node",
    "way/550763786": "a former aid-post building tagged a place of worship",
    "node/5320759161": "a monument tagged a place of worship",
    "way/396783684": "a church's plot, words run together; the church is its own row",
    "node/6051688640": "a misspelled duplicate of the park's own row",
    "node/5320860500": "a locality's name with a number on a church",
    "node/13684009152": "not a word; a wrong name",
    "way/550932648": "a misspelled type word as a name",
    "node/6051688644": "a node duplicate of the garden's own row",
    "node/6051688636": "a node duplicate of the garden's own row",
    # From the read of every landmark and place (the place-read agent, batch 3, 2026-10-11), each id checked against its cached name.
    "way/469208590": "a condominium-tower brand's building tagged a neighbourhood",
    "way/465106032": "a condominium-tower brand's building tagged a neighbourhood",
    "way/571475176": "apartment towers tagged a neighbourhood",
    "way/444091330": "a single residential complex tagged a neighbourhood",
    "way/873114510": "a gated private lane tagged a neighbourhood",
    "node/13088254350": "a children's home tagged a locality",
    "node/11887866827": "a glitched name, on a ranch of seven people",
    "way/622117221": "a private residential golf club's grounds, its name a description",
    "way/668743254": "a housing unit's common area tagged a park",
    "way/737643279": "a housing unit's green tagged a park",
    "way/487272958": "a military housing unit's playground",
    "way/560262998": "an inner garden of a building, tagged a park",
    "way/553147806": "a dessert shop's name on a park",
    "way/560262110": "a pet shop's patio tagged a park",
    "way/591368620": "a supermarket's patio tagged a park",
    "way/591368623": "a business premises' patio tagged a park",
    "way/591367248": "a shopping mall's central court tagged a park",
    "way/285910421": "a shopping plaza with cinemas tagged a park",
    "way/586421201": "an event garden for hire tagged a park",
    "way/586406006": "a riding business tagged a park",
    "way/1360287761": "an events area for hire, its name a description",
    "node/5319186241": "a trade association's seat tagged a place of worship",
    "node/3974383751": "a company's name tagged a place of worship",
    "way/262581330": "a parks department works depot tagged a park",
    "way/1421923326": "a church carrying a metro station's name: a wrong name",
    "node/5796735366": "a place of worship named for one missionary, a person's own name",
    "node/5855838180": "a one-person practice tagged a place of worship, apparently under the person's name",
    "node/12417091168": "a person's own name alone on a sports ground",
    "node/12417045026": "a person's own name alone on a sports ground",
    "node/3681551990": "a convent, a religious residence tagged a place of worship, not notable",
    "node/12150858001": "a convent, a religious residence tagged a place of worship, not notable",
    "node/10617197905": "a convent, a religious residence tagged a place of worship, not notable",
    "way/470346783": "a seminary, a religious residence tagged a place of worship, not notable",
    "way/312387594": "a monastery, a religious residence tagged a place of worship, not notable",
    "node/11117725705": "a monastery, a religious residence tagged a place of worship, not notable",
    "way/611243545": "a glitched name: a church's, cut short",
    "way/608105550": "a description standing in for a name (a playground's equipment)",
    "node/10003160223": "a chapel that no longer exists (its name says so): a search would move the map to a place where it is not",
}
