"""Barcelona-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Rail comes from OpenStreetMap rather than an agency feed - see `osm-rail` - and
unlike Mexico City and Guadalajara, that is the BETTER source here rather than
the only one. TMB's GTFS exists and downloads behind a free account
(`api.tmb.cat` returns 401 unauthenticated, which `brief_check.py` watches), but
the agency route needs FOUR feeds stitched together - TMB, FGC, TRAM and TRAM
Besos - with four licences and four refresh cadences, where one OSM query
returns the whole network with every line named and coloured.
"""

from pathlib import Path

from pipeline.osm_cache import NEVER_A_STATION  # noqa: F401  (printed by step 1)

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "barcelona" / "raw"
DATA_PROCESSED = ROOT / "data" / "barcelona" / "processed"
OUTPUTS = ROOT / "outputs" / "barcelona"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

OSM_STATIONS_JSON = DATA_RAW / "osm_stations.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
BUSINESSES_RAW_CSV = DATA_RAW / "cens_locals_2022.csv"

# --- The business register -------------------------------------------------
#
# Cens de locals en planta baixa amb activitat economica - a field survey of
# ground-floor premises, not a company register, which is the shape this
# project most wants (Montreal's `locaux-commerciaux` is the other one).
#
# THE YEAR IS A DECISION, NOT A DEFAULT. The portal publishes one resource per
# survey year and they are not revisions of each other. The 2024 resource is
# GEOGRAPHICALLY INCOMPLETE - 44,000 rows against 2022's 66,088, and the
# shortfall is wildly uneven: Sant Andreu -83%, Nou Barris -76%,
# Horta-Guinardo -69%, against Ciutat Vella -5% and Eixample -16%. A census
# that narrowed its definition would shrink evenly. A map built on 2024 would
# show the outer districts as commercially dead, which is roughly what a reader
# half expects, so nothing would look broken.
#
# So: 2022, complete, and THE PAGE STATES THE SURVEY YEAR beside the source
# credit. That is also what reconciles the choice with Spanish Act 37/2007
# Article 8's "the most up-to-date data are referred to", which Barcelona's
# terms incorporate expressly - a four-year-old survey published as a stated
# decision rather than a silent one.
CKAN_BASE = "https://opendata-ajuntament.barcelona.cat/data/api/3/action"
CKAN_RESOURCE_ID = "99764d55-b1be-4281-b822-4277442cc721"   # the 2022 survey
CENSUS_YEAR = 2022
# The 2024 resource, recorded so the rejection is checkable rather than a claim.
CKAN_RESOURCE_ID_2024_INCOMPLETE = "38babeec-5c47-43d3-84e7-b13a4b89004f"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM zone 31N. The longitude (~2.17) falls in the 0-6 band, so the
# zone is 31N; the ETRS89 flavour rather than WGS84's EPSG:32631 because it is
# what the census itself publishes (`X_UTM_ETRS89` / `Y_UTM_ETRS89`), so
# rings are measured in the register's own grid. Madrid is 25830, one zone
# west - the CRS is per city and never copied, and Spain's two cities are this
# project's second worked example of that after Mexico's.
CRS_PROJECTED = "EPSG:25831"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- OpenStreetMap fetch --------------------------------------------------

OSM_BBOX = "41.30,2.03,41.50,2.30"

# BARCELONA'S STATIONS ARE `railway=station` + `station=subway`, WHICH IS
# MEXICO CITY'S SHAPE AND NOT GUADALAJARA'S. Measured 2026-09-22 in this bbox:
# 227 `railway=station` nodes, 181 of them `station=subway`; there are also
# **501 `railway=stop` nodes**, which is what Guadalajara keys on. Taking
# Guadalajara's whitelist here would have collected 501 per-direction stop
# positions instead of 181 stations. Three cities, three answers - which is the
# meta-rule `osm-rail` exists for.
# NEITHER OF THE NEXT TWO IS USED, AND THE PARAGRAPH ABOVE IS THE RECORD OF A
# REJECTED APPROACH rather than a description of this city's. They are kept
# because the counts are the evidence for rejecting it - deleting them would
# leave the decision looking arbitrary - but a reader who met them cold would
# reasonably conclude Barcelona selects stations by tag. It does not.
#
# WHAT ACTUALLY RUNS is `stations_query()` in fetch_sources.py: the member
# nodes of the cached route relations, asked for BY ID. Tag selection was
# measured and abandoned because `railway=station` boxes and the
# `stop_position` nodes a PTv2 relation contains are DIFFERENT OBJECTS with
# **no overlap at all** - 225 against 378 - so combining the two filters
# yields an empty set. See that docstring; it carries the measurement.
#
# Noticed 2026-09-23 because `check_stale_claims.py` reported OSM_STATION_KIND
# as unread. OSM_STATION_RAILWAY is equally unread HERE and was NOT reported,
# because Guadalajara defines and consumes a constant of the same name - see
# that script's own note on per-module attribution.
OSM_STATION_RAILWAY = ("station",)          # unused; rejected approach
OSM_STATION_KIND = "subway"                 # unused; rejected approach
# 468 subway entrances in this bbox. Never stations.
OSM_EXCLUDE_RAILWAY = ("subway_entrance", "proposed", "construction", "prpopsed",
                       "level_crossing", "switch", "crossing", "buffer_stop",
                       "railway_crossing", "milestone", "signal",
                       "tram_level_crossing", "tram_crossing", "tram_stop")

# DO NOT FILTER STATIONS BY `network`. Nine of the 181 carry no network tag at
# all - Moli Nou | Ciutat Cooperativa, Avinguda Carrilet (x2), Ildefons Cerda,
# Gornal, Cornella-Riera, Almeda, ZAL | Riu Vell, Port Comercial | La Factoria
# - and most of those are real L8 and L10 Sud stations. Membership of a drawn
# route relation is the filter instead, as in Guadalajara.

# --- Station scope ----------------------------------------------------------
#
# THE DRAWN SET IS ENUMERATED HERE RATHER THAN DERIVED FROM A LIVE TAG TEST,
# and the reason is measured: the Overpass mirrors disagree about this bbox.
# `overpass-api.de` calls the northern L10 segment **`L10N`**; kumi.systems
# calls it **`L10 Nord`**. A config keyed on whatever a mirror returned would
# build differently depending on which host answered, so both spellings are
# accepted and normalised to one key.
#
# WHY THESE SIXTEEN. The scope test is the OPERATORS' OWN `network` tag, not a
# judgement about what counts as a metro:
#   * 14 subway refs, every one `network=Metro de Barcelona` - which INCLUDES
#     FGC's L6, L7, L8 and L12. FGC operates them; TMB's network contains them.
#   * FM (Montjuic), operated by TMB, `network=Metro de Barcelona`. It runs
#     from Paral-lel, an L2/L3 interchange.
#   * FV (Vallvidrera), operated by FGC, `network=Metro del Valles` on
#     overpass-api.de, and route `FV` in FGC's own GTFS.
# EXCLUDED by the same test: FT (Tibidabo), operated by Barcelona de Serveis
# Municipals - the municipal parks company - with no network tag at all, being
# access to the Tibidabo funfair; and trams T1-T6, whose networks are
# `Trambaix` and `Trambesos`, neither a metro.
#
# L9 AND L10 MUST STAY SPLIT. Each runs as two disconnected segments that do
# not meet, so merging L9N with L9S would draw a line through track that does
# not exist. This is the MIRROR IMAGE of Madrid, where 28 relations collapse to
# 13 because they are directional pairs - and Barcelona has that trap too, in
# its funiculars, which are 6 relations and 3 refs. Same query shape, opposite
# correct answers, in one city. Look at the refs.
# TWO OPERATORS, TWO NAMES FOR ONE STATION BOX - Toronto's and Calgary's
# collapse problem, arriving here through a different door.
#
# FGC prefixes its Barcelona stations with the city name where TMB does not, so
# the same interchange appears twice:
#
#   Barcelona-Placa Catalunya  /  Catalunya    178 m apart
#   Barcelona-Placa Espanya    /  Espanya      198 m apart
#
# Both are among the busiest interchanges in the city, and both were counted
# twice with two markers and two overlapping ring sets. **The median-spacing
# gate cannot see this**: two bad names out of 114 moved the median not at all,
# and the collapsed set passed at 520 m. It was the nearest-neighbour MINIMUM
# that showed it.
#
# The list is exhaustive rather than illustrative: exactly two of the 166
# member-node names begin with "Barcelona", and these are they. A prefix-strip
# rule was rejected for that reason - it would be a general mechanism inferred
# from two cases, and it would not fix them anyway, since the remainder
# ("Placa Catalunya") still does not equal TMB's "Catalunya".
STATION_ALIASES = {
    "Barcelona-Plaça Catalunya": "Catalunya",
    "Barcelona-Plaça Espanya": "Espanya",
}

REF_ALIASES = {
    "L10 NORD": "L10N",
    "L10 SUD": "L10S",
    "L9 NORD": "L9N",
    "L9 SUD": "L9S",
}

# ref -> the name riders and TMB actually use.
LINE_NAMES = {
    "L1": "L1",
    "L2": "L2",
    "L3": "L3",
    "L4": "L4",
    "L5": "L5",
    "L6": "L6",
    "L7": "L7",
    "L8": "L8",
    "L9N": "L9 Nord",
    "L9S": "L9 Sud",
    "L10N": "L10 Nord",
    "L10S": "L10 Sud",
    "L11": "L11",
    "L12": "L12",
    "FM": "Funicular de Montjuïc",
    "FV": "Funicular de Vallvidrera",
}

# Straight from each relation's own `colour` tag - 16 of 16 carry one, so no
# palette is invented here. THREE ARE DARKENED ALONG THEIR OWN HUE, which
# `pipeline/linecolour.py` raised on at render time rather than letting ship:
#
#   L5    #0072CE -> #00579D   Delta-E 3.3 from Retail's #2a78d6
#   L9S   #FE5000 -> #CB4000   Delta-E 0.0 from L9 Nord - the same colour
#   L10S  #009FE3 -> #007FB6   Delta-E 5.8 from L10 Nord
#
# **L5's failure is Calgary's, to the decimal.** Calgary shipped its Blue Line
# as the agency's own #0072CE - the identical hex - at Delta-E 3.3 from Retail,
# and it went unnoticed for weeks because nobody measured it. Barcelona's L5 is
# the same TMB blue. That is the check paying for itself a second time on the
# same value.
#
# The other two are a different problem: L9 and L10 each run as two
# disconnected segments, so this map draws them as two lines with two legend
# rows - and TMB gives each PAIR one colour, because TMB brands them as one
# line. Two legend rows in the same orange are two rows a reader cannot tell
# apart. Darkening the southern segment keeps the line's identity while making
# the legend readable.
#
# Darkened to Delta-E ~18, not to PREFERRED (45). At 45 L5 becomes #002B4D, a
# near-black navy nobody would call TMB blue, and L9 Sud becomes brown. ~18
# sits inside the band the six built cities already occupy while keeping
# agency colours (13.6 New York, 16.9 Montreal, 20.1 Boston, 27.3 Boston), so
# this is the project's existing trade rather than a new one.
LINE_COLOURS = {
    "L1": "#C8102E",
    "L2": "#93328E",
    "L3": "#43B02A",
    "L4": "#F2A900",
    "L5": "#00579D",    # TMB #0072CE darkened: 3.3 -> 18.1 from Retail
    "L6": "#797FBC",
    "L7": "#B2600B",
    "L8": "#E274AA",
    "L9N": "#FE5000",
    "L9S": "#CB4000",   # TMB #FE5000 darkened: 0.0 -> 18.8 from L9 Nord
    "L10N": "#00ADEF",
    "L10S": "#007FB6",  # TMB #009FE3 darkened: 5.8 -> 18.2 from L10 Nord
    "L11": "#97D700",
    "L12": "#B2AED3",
    "FM": "#006847",
    "FV": "#0c2340",
}

DRAWN_REFS = tuple(LINE_NAMES)

# --- Business filtering ------------------------------------------------

# The census covers the municipality only, so there is no city column to filter
# on and no equivalent of Los Angeles' CITY_KEEP trap. `Nom_Districte` is the
# geography, and Barcelona has TEN districts - asserted in step 2, because a
# change in that count means the survey's geography moved and the row counts
# above stopped meaning what they say.
BARCELONA_DISTRICT_COUNT = 10

TAXONOMY_SYSTEM = "barcelona_activitat"
RAW_CLASSIFICATION_COLUMN = "Nom_Activitat"

# THE VACANCY FILTER IS MANDATORY. `Nom_Principal_Activitat` is `Actiu` on
# 58,908 rows and `Sense activitat Economica` on 7,180 - empty units for sale
# or rent. Without it, 11% of the pins are shuttered shopfronts. Barcelona
# hands this over explicitly, which most registers make you infer.
ACTIVE_COLUMN = "Nom_Principal_Activitat"
ACTIVE_VALUE = "Actiu"

# Columns pulled from CKAN. This list IS the privacy control: the census has 50
# fields and the pipeline asks for eleven. `Nom_Local` is a TRADE name and is
# 100% populated, so there is no registrant-name fallback to go wrong - the
# failure mode that would have published ~4,000 individuals' names in Los
# Angeles cannot arise here, structurally rather than by measurement.
USECOLS = (
    "ID_Global",
    "Nom_Local",
    "Nom_Activitat",
    "Nom_Grup_Activitat",
    "Nom_Sector_Activitat",
    "Nom_Principal_Activitat",
    "Nom_Districte",
    "Latitud",
    "Longitud",
    "X_UTM_ETRS89",
    "Y_UTM_ETRS89",
    "SN_CComercial",
)

PREMISES_ID_COLUMN = "ID_Global"

# Never load these, and step 2 asserts they never arrive. `Referencia_Cadastral`
# IS one of the census's 50 fields and is deliberately not requested: a cadastral
# reference identifies a property title, which is a step beyond the commercial
# fact this project publishes. The others are not in the schema today, and are
# named so that a publisher adding one would fail the build rather than quietly
# widen what gets mapped.
FORBIDDEN_COLUMNS = ("nom_propietari", "nif", "titular", "referencia_cadastral")

# Barcelona's mall, gallery and market flags are the only ones of their kind in
# this project. They are KEPT rather than used to exclude: a mall near a station
# is real commercial density a rider can reach, and excluding it would make
# Barcelona measure something different from the other sixteen cities on a map
# that invites comparison. Recorded as available-but-unused so a later decision
# can reach for them.
SITE_TYPE_FLAGS_AVAILABLE_UNUSED = ("SN_CComercial", "SN_Galeria", "SN_Mercat",
                                    "SN_Eix", "SN_Obert24h", "SN_Oci_Nocturn")

# Sanity bounds. Barcelona's municipality is compact - 101.4 km2 - so this box
# is deliberately tight; step 1 checks the boundary's own area against it.
BARCELONA_BBOX = {
    "lat_min": 41.31,
    "lat_max": 41.48,
    "lon_min": 2.05,
    "lon_max": 2.24,
}
BOUNDARY_AREA_KM2 = 101.4
BOUNDARY_AREA_TOLERANCE_KM2 = 4.0
