"""Bremen-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/bremen.md). Germany's second city, and the first whose
businesses come from a retail survey: "Einzelhandelsbestand in der Region
Bremen 2022" (Kommunalverbund Niedersachsen/Bremen e.V., CC BY, no version),
classified by `pipeline/taxonomies/bremen_einzelhandel.py`. One bucket,
Retail. The rail is Odense's and Geneva's: BSAG's eight tram lines from
OpenStreetMap through the shared `pipeline/osm_tram.py`, one Overpass query
for the city, the Stadtgemeinde Bremen's OSM boundary from the same query.
"""

from pathlib import Path

SLUG = "bremen"
# What the brief's checks compare with (`brief_check.py bremen --vs-config`).
MAP_MODE = "tram"
MAP_COVERAGE = "one_bucket"
# The City of Bremen alone (owner, 2026-10-05, call 2): businesses by the
# survey's own Gemeinde field, stations by the city polygon. Lilienthal waits
# for a regional-extension add-on.
SCOPE = "city"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "bremen" / "raw"
DATA_PROCESSED = ROOT / "data" / "bremen" / "processed"
OUTPUTS = ROOT / "outputs" / "bremen"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stops of drawn lines outside the City of Bremen (line 4's Lilienthal end):
# drawn, not ringed, listed with the municipality each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# --- The retail survey (fetch_sources.py downloads; no step fetches) -----------
#
# GovData record `einzelhandelsbestand-in-der-region-bremen-2022`, metadata
# f6323bd1-bd38-4f72-a7ec-cb08209564ff; the file is hosted by the Landesamt
# GeoInformation Bremen. Fieldwork 2022-03-01 to 2022-09-30 (the record's
# temporal fields); the survey repeats every five years. Cached 2026-10-04
# (owner-approved single-file download) with a meta JSON beside it; the cached
# zip is kept, never re-taken, unless `fetch_sources.py --survey` is given.
SURVEY_URL = "https://geoportal.bremen.de/resources/data/Einzelhandelsbestand_reduziert.zip"
SURVEY_ZIP = DATA_RAW / "Einzelhandelsbestand_reduziert.zip"
SURVEY_META = DATA_RAW / "Einzelhandelsbestand_reduziert.meta.json"
SURVEY_MEMBER = "Einzelhandelsbestand_reduziert.geojson"
SURVEY_RECORD = ("https://www.govdata.de/ckan/api/3/action/package_show"
                 "?id=einzelhandelsbestand-in-der-region-bremen-2022")
SURVEY_FIELDWORK = ("2022-03-01", "2022-09-30")
SURVEY_PUBLISHER = "Kommunalverbund Niedersachsen/Bremen e.V."
SURVEY_LICENCE = "Creative Commons Namensnennung (CC-BY)"
SURVEY_LICENCE_URL = "https://opendefinition.org/licenses/cc-by/"
SURVEY_ENCODING = "utf-8"
# The six fields of the public ("reduziert") variant, all filled on all 5,573
# rows (the brief, 2026-10-05). No name, address, person or business-ID
# field; step 2 stops on any field added or gone.
SURVEY_FIELDS = ("id", "Gemeinde", "HWG_C", "HWG", "Gr_Kl_C", "Gr_Kl")
# 5,573 rows in the region on the cached file; a file far below it is a
# failed or truncated download, not a smaller region.
SURVEY_MIN_ROWS = 5_000
# The survey's own municipality label for the city, one exact value.
CITY_GEMEINDE = "Bremen"
# Rows labelled Bremen whose point lies outside the city polygon, or rows
# labelled elsewhere whose point lies inside it; step 2 stops on any other
# figure, so a disagreement is named, never absorbed. ONE on the build of
# 2026-10-07: every "Bremen" row is inside (3,153), and one row labelled
# Delmenhorst (a food shop, floor class 1) lies 238 m inside the city line,
# 1.7 km from the nearest other Delmenhorst row, so the label or the point is
# a survey slip. It stays out: the Gemeinde field decides (owner, 2026-10-05,
# call 2), and the city reads 3,153, the brief's figure.
POLYGON_DISAGREE_EXPECTED = 1

# --- OpenStreetMap: one query for the city (osm-rail) ------------------------

# S, W, N, E: BSAG's eight lines, line 4's Lilienthal end and line 1's
# Mahndorf end included, plus a margin. The city boundary is asked for by
# tag, so it comes whole whatever part of it the box covers.
RAIL_BBOX = (52.98, 8.60, 53.22, 9.06)
OSM_ALL_JSON = DATA_RAW / "osm_all.json"
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
OSM_BOUNDARY_JSON = DATA_RAW / "osm_boundary.json"
# The places a drawn stop can lie in, keyed by the Amtlicher
# Gemeindeschlüssel as OSM tags it: the Stadtgemeinde Bremen (never the Land,
# which adds Bremerhaven) and Lilienthal, where line 4 ends.
AGS_TAG = "de:amtlicher_gemeindeschluessel"
CITY_AGS = "04011000"
PLACES = {CITY_AGS: "Bremen", "03356005": "Lilienthal"}
# The Stadtgemeinde's area as OSM draws it; step 1 stops outside these bounds
# (a polygon assembled wrong, or the Land taken for the city). Relation 62559
# (admin_level 6) measures 326.0 km2 in EPSG:25832 (2026-10-07); Lilienthal,
# relation 423195, 72.4 km2. The Land's relation 62718 comes with the query
# by name and is never taken (its AGS is "04").
CITY_AREA_KM2 = (310.0, 340.0)

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# ETRS89 / UTM 32N, in metres. Bremen (~8.80 E) is in zone 32 (6-12 E); the
# derived WGS84 zone is EPSG:32632, sub-metre from this one. The survey ships
# in EPSG:25832, so the build measures in it and never moves the survey's
# points into another projected CRS (Odense's precedent).
CRS_PROJECTED = "EPSG:25832"
CRS_SURVEY = "EPSG:25832"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# HALVED: the median nearest-neighbour gap among the 154 stops in the city
# is 351 m (measured 2026-10-07 on the stations drawn; the spacing rule's line
# is about 550 m; tram-city section 3). Step 1 stops outside 310-390 m.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
MEDIAN_GAP_BOUNDS_M = (310.0, 390.0)

# --- Station scope: BSAG's eight trams, every stop in the city ------------------

ROUTES = ("tram",)
OPERATOR = None
# BSAG's base timetable lines (BSAG_S26C, the brief), in BSAG's order.
LINE_REFS = ("1", "2", "3", "4", "5", "6", "8", "10")
# Every tram relation in the box is kept or named here with a reason
# (osm_tram's contract). Read from the build's one query (osm_base
# 2026-10-07T08:56:06Z): 46 tram relations, 37 kept on refs 1-10 (the main
# routes and their short workings, 1S, 1E, 4S, 6E and line 8's centre and
# depot runs, all BSAG's own lines), 9 night-line relations out.
_NIGHT = ("BSAG night line, run only at night on the tracks and stops of the day line "
          "it shadows; listed by BSAG under its night lines, not the eight tram lines")
NOT_DRAWN = {
    965867: "N1 " + _NIGHT, 965869: "N1 " + _NIGHT, 10440733: "N1 " + _NIGHT,
    10440734: "N1 " + _NIGHT,
    966992: "N4 " + _NIGHT, 966993: "N4 " + _NIGHT, 10441530: "N4 " + _NIGHT,
    963162: "N10 " + _NIGHT, 963163: "N10 " + _NIGHT,
}
# LINE 8'S CITY-CENTRE LOOP, ADDED BY NODE. BSAG's base timetable of
# 2026-08-17 runs line 8 through Am Brill and Obernstraße one way and Radio
# Bremen, Daniel-von-Büren-Straße and Falkenstraße the other (the brief; BSAG's
# line 8 timetable, read 2026-10-07). OSM's two line 8 relations (19936,
# 963050) still run Wilhelm-Kaisen-Brücke to Domsheide direct (osm_base
# 2026-10-07T08:56:06Z): the relations lag the timetable change, the
# osm-rail skill's case. All five stops are stations of other lines already,
# so their rings do not change; the adds give line 8 its stops for gate 3 and
# the station list. Each is that stop's tagged node on no route relation, as
# osm_tram requires; osm_tram stops the step once OSM puts the stop on a
# line 8 relation. The line is drawn as OSM has it.
STATION_ADD = {
    21316758: ("8", "Am Brill (Hutfilter-/Obernstraße)"),
    21316798: ("8", "Obernstraße"),
    26048306: ("8", "Radio Bremen"),
    30343524: ("8", "Daniel-von-Büren-Straße"),
    244114968: ("8", "Falkenstraße"),
}
NAME_ALIASES = {}
# OSM names two stops by platform, where BSAG names each stop once: Am Brill
# (platforms A and B on Bürgermeister-Smidt-Straße for line 1, E and F on
# Hutfilter-/Obernstraße for lines 2, 3 and 8; BSAG's Am Brill_A to _F) and
# Bahnhof Walle (Steig A and B). Gate 3 counted each twice (line 1 45 against
# BSAG's 44, line 2 35/33, line 3 30/29, line 10 33/32, 2026-10-07). Step 1
# folds these names before the collapse, which then merges each stop within
# MAX_SPREAD_M (Am Brill's five nodes span 166 m). osm_tram's NAME_ALIASES
# cannot do it, since it needs the target spelling present, and here none is
# (Geneva's platform-letter fold, the same shape). Step 1 stops if a name
# listed here is no longer in OSM, so a stale fold cannot outlive the gap.
NAME_FOLD = {
    "Am Brill (Bgm.-Smidt-Straße), Bussteig/Gleis A": "Am Brill",
    "Am Brill (Bgm.-Smidt-Straße), Bussteig/Gleis B": "Am Brill",
    "Am Brill (Hutfilter-/Obernstraße), Bussteig E": "Am Brill",
    "Am Brill (Hutfilter-/Obernstraße), Bussteig F": "Am Brill",
    "Am Brill (Hutfilter-/Obernstraße)": "Am Brill",
    "Bahnhof Walle (Steig A)": "Bahnhof Walle",
    "Bahnhof Walle (Steig B)": "Bahnhof Walle",
}
# A STOP MEMBER WITH NO TAGS AT ALL: node 2562313293 is listed with role
# "stop" on one direction of lines 2 and 10 (relations 532076, 536338,
# Sebaldsbrück to Gröpelingen), 23 m from Gustavstraße's named stop node
# (read 2026-10-07). osm_tram stops on it, and its accept_members needs a
# name, which this node lacks. Step 1 drops the member in memory, so the stop
# is counted once per line through the named Gustavstraße stops the same
# lines carry. Step 1 stops if the node gains a tag, is no longer such a
# member, lies more than UNTAGGED_MAX_M from a named stop of that name, or
# the line has no other stop of that name: a stale entry cannot outlive the
# gap. Upstream fix: tag the node in OSM, or teach osm_tram a dropped-member
# list (a shared-module change, not made here).
UNTAGGED_STOP_MEMBERS = {2562313293: "Gustavstraße"}
UNTAGGED_MAX_M = 50.0
# The build of 2026-10-07: 164 stops on the network, 154 in the City of
# Bremen, line 4's 10 in Lilienthal (the brief: about 154 and about 10). Step 1
# stops when OSM moves them.
EXPECTED_IN_SCOPE = 154
EXPECTED_OUTSIDE = 10
# Gate 3: BSAG's own timetable index, whole lines before the scope split
# (line 4 with its Lilienthal stops), both directions' stop names, the
# platform letter dropped, "HBF-Nord/Messe" read as "Hauptbahnhof-Nord/Messe"
# (the brief's fold). 164 distinct stations, 253 line-stops.
OPERATOR_STATION_COUNTS = {"1": 44, "2": 33, "3": 29, "4": 49, "5": 14, "6": 25,
                           "8": 27, "10": 32}
OPERATOR_COUNTS_SOURCE = (
    "BSAG (Bremer Straßenbahn AG), 'Linien und Fahrpläne' "
    "https://www.bsag.de/fahrplan/linien-und-fahrplaene, the timetable index embedded "
    "in the page, base timetable BSAG_S26C 'Grundfahrplan' valid 17.8.2026 to "
    "21.03.2027; both directions, platform letter dropped; read 2026-10-05 (the "
    "brief), BSAG_S26C confirmed on the page 2026-10-07 (brief_check.py).")
SPACING_MIN_M = 80.0
MAX_SPREAD_M = 200
DRAWN_LINES = LINE_REFS
LINE_NAMES = {ref: f"Tram {ref}" for ref in LINE_REFS}
# BSAG's colours as OSM tags them, one value on every kept relation of each
# line (read 2026-10-07); step 3 asserts they are still OSM's and
# pipeline/linecolour.py measures them at render. None is under the floor of
# 10, so none moves (Göteborg's precedent: moved only below the floor). Below
# the preferred 45 and recorded, not moved (CIE76): 2 14.0 from Retail, the
# map's one pin colour (Göteborg's 3 was 14.2); 1 21.1 and 5 32.0 from
# Personal services (no such pins on this map); 3 25.9 and 10 36.1 from
# Retail. Lines 2 and 10 share both ends and differ by 30.0; the closest pair
# is 2 and 3 at 29.5.
OSM_COLOURS = {"1": "#009640", "2": "#005ca9", "3": "#009fe3", "4": "#e30613",
               "5": "#009999", "6": "#ffcc00", "8": "#95c11f", "10": "#312783"}
LINE_COLOURS = dict(OSM_COLOURS)

# --- Business filtering ------------------------------------------------

TAXONOMY_SYSTEM = "bremen_einzelhandel"
RAW_CLASSIFICATION_COLUMN = "hwg_code"

# Sanity bounds for the derived lat/lng: the City of Bremen plus ~0.02 deg.
BREMEN_BBOX = {
    "lat_min": 53.00,
    "lat_max": 53.25,
    "lon_min": 8.45,
    "lon_max": 9.01,
}
