"""Gelsenkirchen-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/gelsenkirchen.md). Germany's second city and its first
city survey: the City of Gelsenkirchen's own survey of its commercial premises
(the Infrastrukturdatenbank's three themed layers, dl-de/zero-2.0), Liège's
shape (a municipal survey keyed to designated centres) with Brussels' and
Liège's sign rule. Trams only (tram-city): BOGESTRA's 301 and 302,
Ruhrbahn's 107 and Stadtbahn U11, from OpenStreetMap on the shared
`pipeline/osm_tram.py`, Geneva's step 1. The City of Gelsenkirchen only:
lines that run on into Bochum and Essen are cut at the city line, Berlin's
precedent (owner, 2026-10-05, call 3).
"""

from pathlib import Path

SLUG = "gelsenkirchen"
NAME = "Gelsenkirchen"
FETCH = "pipeline/gelsenkirchen/fetch_sources.py"
# What the brief's checks compare with (`brief_check.py gelsenkirchen --vs-config`).
# `mode` stays tram if OSM types U11 light rail (owner, 2026-10-05, call 4).
MAP_MODE = "tram"
MAP_COVERAGE = "narrowed"
SCOPE = "city"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "gelsenkirchen" / "raw"
DATA_PROCESSED = ROOT / "data" / "gelsenkirchen" / "processed"
OUTPUTS = ROOT / "outputs" / "gelsenkirchen"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stops of drawn lines outside the city (302's in Bochum, 107's and U11's in
# Essen): drawn with their line, never ringed, listed with the city each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- The survey (fetch_sources.py downloads; no step fetches) -----------------
#
# Stadt Gelsenkirchen, Infrastrukturdatenbank, GeoServer WFS 2.0 (capabilities
# keyword ge:constraints_dl_zero_de, Fees NONE); the same layers on the Ruhr
# portal (opendata.ruhr) under dl-zero-de/2.0. The OGC API's `properties`
# parameter is IGNORED by this GeoServer (2026-10-07: all 49 fields came
# back), so the reduced fetch is the WFS with PROPERTYNAME, which it honours,
# adding the two mandatory publish flags (Veroeffentlicht, Istonline) itself.
WFS_URL = "https://maps.gelsenkirchen.de/geoserver/infrastrukturdatenbank/wfs"
WFS_NAMESPACE = "infrastrukturdatenbank"
LICENCE_URL = "https://www.govdata.de/dl-de/zero-2-0"
LAYERS = ("gewerbe_gastronomie", "gewerbe_einzelhandel", "gewerbe_dienstleistung")
# The layer name -> the taxonomy's layer key, and the GEWERBETYPUSBEZ every
# row of that layer carries (step 2 asserts it).
LAYER_KEYS = {"gewerbe_gastronomie": "gastronomie", "gewerbe_einzelhandel": "einzelhandel",
              "gewerbe_dienstleistung": "dienstleistung"}
LAYER_TYPUS = {"gewerbe_gastronomie": "Gastronomie", "gewerbe_einzelhandel": "Einzelhandel",
               "gewerbe_dienstleistung": "Dienstleistung"}
# The only properties requested (owner, 2026-10-05, call 5). Never requested,
# so never on disk from this fetch: Telefon, EMail, Internet, DL_Vermarktung
# (owner, 2026-10-04: the probe slip), Fax, Info, Internetbeschreibung, Strasse
# and ADRKOMBI (call 5), and every planning field the map does not use.
#   Name: the sign (shown under the sign rule); KAT_GASTRO, HAUPTWARENGRUPPEBEZ,
#   KERNSORTIMENTBEZ, KAT_DL: the classification; GEWERBETYPUSBEZ: the layer
#   check; LAGEBEZ: the centre class (the personal-services gap, measured,
#   never shown); PLZ: a scope cross-check only; X, Y: EPSG:25832 eastings and
#   northings, compared with the geometry; Shape: the point.
WFS_PROPERTIES = ("id", "Name", "GEWERBETYPUSBEZ", "KAT_GASTRO", "HAUPTWARENGRUPPEBEZ",
                  "KERNSORTIMENTBEZ", "KAT_DL", "LAGEBEZ", "PLZ", "X", "Y", "Shape")
# Never requested; step 2 stops if any reaches a cached file.
NEVER_READ = ("Telefon", "EMail", "Internet", "DL_Vermarktung", "Fax", "Info",
              "Internetbeschreibung", "Strasse", "ADRKOMBI")
WFS_PAGE = 1000
# The cached reduced layers (new names; the full 2026-10-04 copies beside them
# are kept until the owner says otherwise, call 5, and never read by a step).
SURVEY_FILES = {layer: DATA_RAW / f"idb_{layer}.geojson" for layer in LAYERS}
SURVEY_META = DATA_RAW / "idb_reduced_meta.json"
# Rows per layer, 2026-10-07 (the city edits the services layer: 591 on
# 2026-10-05). A count outside the band is a failed or a changed fetch.
SURVEY_ROWS = {"gewerbe_gastronomie": (380, 430), "gewerbe_einzelhandel": (1250, 1400),
               "gewerbe_dienstleistung": (560, 640)}
# The survey's stored CRS, ETRS89 / UTM 32N; X and Y agree with the geometry
# to 5 mm (the brief). Step 2 stops above this.
CRS_SURVEY = "EPSG:25832"
XY_TOLERANCE_M = 0.05

# --- OpenStreetMap: one query for the city (osm-rail) ------------------------

# Every tram, light-rail and subway route relation with a member in the
# city's box, its member nodes, the box's tram stop nodes, and the boundaries
# of the city and its neighbours by municipality key, in ONE Overpass query,
# split into two cached files. S, W, N, E: the city (6.995-7.136 E,
# 51.485-51.622 N, the survey's extent) plus a margin.
RAIL_BBOX = (51.47, 6.97, 51.64, 7.16)
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_BOUNDARIES_JSON = DATA_RAW / "osm_boundaries.json"
# The official municipality key (Amtlicher Gemeindeschlüssel) as OSM tags it,
# which identifies the city's polygon, and the keys of the places a cut
# line's stops may lie in.
AGS_TAG = "de:amtlicher_gemeindeschluessel"
CITY_AGS = "05513000"
# The city and every municipality its lines' stops could lie in: Essen,
# Bochum, Bottrop, Gladbeck, Herten, Herne. A stop in none stops step 1.
PLACE_AGS = (CITY_AGS, "05113000", "05911000", "05512000", "05562014", "05562016",
             "05916000")
# Gelsenkirchen's area is 104.9 km2 (IT.NRW); a polygon outside the band did
# not close.
CITY_AREA_KM2 = (100.0, 110.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 32N: the survey's mean longitude, 7.078 E, falls in the 6 to 12
# band. Derived per city, not copied (docs/project_context.md's CRS lesson).
# The survey's EPSG:25832 is reprojected to it on read (sub-metre).
CRS_PROJECTED = "EPSG:32632"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
# HALVED, on the owner's spacing rule (about 550 m or less): the median
# nearest-neighbour gap among the 60 in-scope stops is 380 m (step 1,
# 2026-10-07; min 135, max 973). Step 1 stops outside the band below.
MEDIAN_GAP_BOUNDS_M = (340.0, 420.0)

# --- Station scope ------------------------------------------------------------

# OSM types U11 route=subway (both relations, 2026-10-07); `mode` stays tram
# on the owner's call 4 (2026-10-05), whose principle (a second mode sets
# `mode` only where it is the city's main network) covers subway as well as
# light rail: inside the city U11 is 3 stops and 2.3 km of track.
ROUTES = ("tram", "light_rail", "subway")
OPERATOR = None
LINE_REFS = ("301", "302", "107", "U11")
# Relations in the box with no stop and no track inside the city (measured
# 2026-10-07): Essen's and Bochum's other lines, out of scope.
_ELSEWHERE = "no stop or track in Gelsenkirchen; an Essen or Bochum line in the box"
NOT_DRAWN = {38430: f"Tram 101 ({_ELSEWHERE})", 4540371: f"Tram 106 ({_ELSEWHERE})",
             60211: f"Tram 108 ({_ELSEWHERE})", 4541957: f"Tram 108 ({_ELSEWHERE})",
             1202203: f"Tram 306 ({_ELSEWHERE})", 2003473: f"Tram 306 ({_ELSEWHERE})",
             10409640: f"Tram 316 ({_ELSEWHERE})", 10409641: f"Tram 316 ({_ELSEWHERE})",
             2000351: f"U17 ({_ELSEWHERE})", 5312040: f"U17 ({_ELSEWHERE})"}
STATION_ADD = {}
NAME_ALIASES = {}
# The build of 2026-10-07: 133 stops, 60 in the city, 73 beyond the city
# line (40 in Essen on 107 and U11, 33 in Bochum on 302). Per line (whole /
# inside / inside and served by that line alone): 301 34/34/29, 302
# 54/21/18, 107 34/10/7, U11 23/3/1. The cut keeps every line drawn, so
# no in-city stop is lost to a stub test (call 3).
EXPECTED_IN_SCOPE = 60
EXPECTED_OUTSIDE = 73
# Gate 3: the operators' own timetables, the whole line before the scope
# split, distinct stops. Counted on each file's LINE BAND (Linienband, the
# line diagram on its first page), which lists every stop: the departure
# tables list timing points only on 302 (37 of 54) and 107 (26 of 34), and a
# first count on the tables disagreed with OSM for exactly that reason
# (2026-10-07). A stop shown with two platforms (107's Overwegstr. Bstg 01
# and 02) or a turning-loop platform (Hanielstr. Schleife, Abzw Katernberg
# Schleife) counts once. Read for the count only, never republished.
#   301: 34 stops, Gelsenkirchen Hbf to Essener Str. (Horst).
#   302: 54 stops, GE-Buer Rathaus to Langendreer, Max-Planck-Institut and
#        O-Werk included, and Wattenscheid's one-way pair (Querstr. and
#        Centrumplatz one way, Vietingstr. the other) with Berger See.
#   107: 34 stops, Gelsenkirchen Hbf to Bredeney; the band puts the city
#        line between Trabrennbahn and Triple Z.
#   U11: 23 stops, GE-Buerer Str. (Horst) to Messe West-Süd/Gruga; the band
#        puts the city line between Fischerstr. and Alte Landstr.
OPERATOR_STATION_COUNTS = {"301": 34, "302": 54, "107": 34, "U11": 23}
OPERATOR_COUNTS_SOURCE = (
    "301 and 302: BOGESTRA's line timetables on its index "
    "https://www.bogestra.de/fahrplan-mobilitaet/linienfahrplaene, files "
    "301-Inter-20260902.pdf and 302-Inter-20260614.pdf; 107 and U11: Ruhrbahn's current "
    "timetables https://www.ruhrbahn.de/essen/fahrplan/linienfahrplaene/tram (107, "
    "'Gültig ab 21. September 2026', 107_21092026.pdf) and "
    "https://www.ruhrbahn.de/essen/fahrplan/linienfahrplaene/u-bahn (U11.pdf); "
    "read 2026-10-07 for the count only (owner, 2026-10-05, call 6).")
SPACING_MIN_M = 80.0
# Aarhus's collapse distance; the city-centre Stadtbahn tunnel puts
# underground platforms beside surface stops of the same name (the brief).
MAX_SPREAD_M = 200
DRAWN_LINES = LINE_REFS
LINE_NAMES = {"301": "Tram 301", "302": "Tram 302", "107": "Tram 107", "U11": "U11"}
# The operators' colours as OSM tags them on every relation of each line
# (read 2026-10-07); step 3 asserts they are still OSM's and
# pipeline/linecolour.py measures them against the pins at render.
OSM_COLOURS = {"301": "#00B2F6", "302": "#6BA5D9", "107": "#D01519", "U11": "#342A82"}
LINE_COLOURS = dict(OSM_COLOURS)

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "gelsenkirchen_gewerbe"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "category"
# A survey point further than this outside the city polygon stops step 2 (the
# collection's extent, 6.995-7.136 E, 51.485-51.622 N, sits inside the city);
# one nearer is an edge difference and stays (1 row, 1 m out, 2026-10-07).
POLYGON_TOLERANCE_M = 100.0
# Gelsenkirchen's postcodes, for the PLZ cross-check only (scope is the polygon).
CITY_PLZ = ("45879", "45881", "45883", "45884", "45886", "45888", "45889", "45891",
            "45892", "45894", "45896", "45897", "45899")

# SIGNS READ AS A PERSON'S OWN NAME, withheld: the pin shows the category
# instead (owner, 2026-10-05, call 1; Liège's and Brussels' rule). Keys, never
# names (pipeline/name_keys.py). Proposed by `signs.person_sign` on the kept
# rows, less any sign found at two or more points in the survey (a brand):
# 22 person-shaped, 4 of them brands, 18 withheld (2026-10-07). Regenerate
# with
#   python -m pipeline.gelsenkirchen.signs --person-keys
PERSON_NAMED = (
    "0a543f7ffbefcc63", "0afe53421c6f0ef7", "3314d7d343968fb4", "3cc100a8b5eb4f45",
    "560d50f56ac39c3c", "5a7927e712853cc7", "6e21deba7ce0aa99", "831d06a56281f31a",
    "917fa38c7ab945ab", "9931c824b1038085", "a72817b6c3453a03", "b9c6ca886c76effe",
    "c6dcd06c08d76d6b", "ce1676f178de36a0", "e5c23a3c85ecb3e4", "ec640ee66300c036",
    "f4abc038ed4918b7", "f9fa084cbb6b85e9",
)
# READ BY EYE (the lead build session, 2026-10-07, the owner's call 1): every
# displayed services sign, and the two-or-three-word letters-only signs at one
# location in the food (197) and retail (548) layers. Four read as a bare
# personal name with no trade word, one of them ambiguous and withheld on
# Zurich's precedent; a trade word beside a name ("Bäckerei" and a name) is
# the sign over the shop and stays. Kept apart from PERSON_NAMED so that
# regenerating the shape test's list cannot drop them.
PERSON_NAMED_BY_EYE = (
    "588fb0ac0cf69aec", "2e5050768582db3c", "77c9843d5794bffc", "26347f1d6658f89f",
)

# Sanity bounds for the points: the city plus a margin.
GELSENKIRCHEN_BBOX = {
    "lat_min": 51.47,
    "lat_max": 51.64,
    "lon_min": 6.97,
    "lon_max": 7.16,
}
