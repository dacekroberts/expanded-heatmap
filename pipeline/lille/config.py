"""Lille (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; every scaffolded placeholder has been
replaced with a measured value, so this module ships none.

FOURTH FRENCH CITY, AND THE FIRST FRENCH ONE THAT IS REGIONAL. It inherits the
country module, the national NAF taxonomy, the shared parquet cache and the
Lambert-93 grid. It inherits nothing about its rail leg, which is built from
three sources rather than one feed - see the station-scope section.

WHY REGIONAL WHEN PARIS, MARSEILLE AND TOULOUSE ARE COMMUNE-ONLY. Measured
2026-09-23 against commune 59350's contour: Métro 1 keeps 13 of 18 stations,
Métro 2 **19 of 44**, and the tram **3 of 36** - a commune-only map would draw
the tram as a three-stop stub. And the reason the other French cities stayed
commune-only was never data availability: SIRENE is ONE national file under
one licence, so every neighbouring commune's businesses are already in the
parquet (Miami's situation - one register covering the region). Owner's call
2026-09-23: scope to **the communes the network actually serves**, the Dublin
and Guadalajara pattern.
"""

from pathlib import Path

# The national facts, shared with every French city. Re-exported with noqa so
# this city's step files import them from here.
from pipeline.countries.france import (  # noqa: F401
    COMMUNE_COLUMN,
    DIFFUSION_COLUMN,
    DIFFUSION_PUBLIC_VALUE,
    EMPLOYEE_BAND_COLUMN,
    ENSEIGNE_COLUMNS,
    GEO_EPSG_COLUMN,
    GEO_LAT_COLUMN,
    GEO_LON_COLUMN,
    GEO_QUALITY_COLUMN,
    GEOLOC_DATASET_SLUG,
    GEOLOC_PARQUET,
    GEOLOC_RESOURCE_TITLE_CONTAINS,
    JOIN_KEY,
    METROPOLITAN_EPSG,
    NAF_COLUMN,
    SIRENE_DATASET_SLUG,
    SIRENE_PARQUET,
    SIRENE_RESOURCE_TITLE_PREFIX,
    STATE_ACTIVE_VALUE,
    STATE_COLUMN,
    USUAL_NAME_COLUMN,
)

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "lille" / "raw"
DATA_PROCESSED = ROOT / "data" / "lille" / "processed"
OUTPUTS = ROOT / "outputs" / "lille"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# NO excluded_stations.csv, deliberately. Every other French city writes one
# because its boundary drops stations; here the scope is DEFINED by where the
# stations are, so the boundary drops none by construction. What IS excluded is
# excluded by NETWORK - three OSM `route=tram` relations that are not ilévia's -
# and never reaches step 1, because the Overpass query filters on the relation's
# network. check_scope_disclosure.py reads the file only where it exists.
# The communes the network serves, with how many stations each holds. The
# regional scope's own record, as Miami's station_municipalities.csv is.
SERVED_COMMUNES_CSV = OUTPUTS / "served_communes.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 1's per-line tram geometry, assembled from MEL's SECTIONS (see below)
# and read back by map_common.load_geojson_line_shapes.
TRAM_LINES_BY_LINE_GEOJSON = DATA_PROCESSED / "tram_lines_by_line.geojson"
# The union of the served communes - the map's boundary and label focus.
SERVED_BOUNDARY_GEOJSON = DATA_PROCESSED / "served_boundary.geojson"

# Raw inputs, all public. `fetch_sources.py` downloads them; no step may fetch
# (scripts/check_no_fetch_in_steps.py enforces it).
METRO_STATIONS_GEOJSON = DATA_RAW / "stations_metro.geojson"
TRAM_STOPS_GEOJSON = DATA_RAW / "tramway_arrets.geojson"
TRAM_LINES_GEOJSON = DATA_RAW / "tramway_lignes.geojson"
LINE_COLOURS_GEOJSON = DATA_RAW / "couleurs_lignes.geojson"
MEL_COMMUNES_GEOJSON = DATA_RAW / "mel_communes.geojson"
OSM_ROUTES_JSON = DATA_RAW / "osm_routes.json"
# SIRENE_PARQUET and GEOLOC_PARQUET are NATIONAL and imported from the country
# module above - one 3 GB cache for every French city.

# --- Sources --------------------------------------------------------------

# MEL's geOrchestra WFS. NOT Opendatasoft - its 404 body names itself, which is
# why /api/datasets paths all miss. Every layer below was checked individually
# against MEL's catalogue: Licence Ouverte 2.0. The catalogue is MIXED (13 of
# 427 records need a signed acte d'engagement, 1 is ODbL), so a new layer is
# never assumed to share these terms.
WFS_URL = "https://data.lillemetropole.fr/geoserver/wfs"
WFS_LAYERS = {
    METRO_STATIONS_GEOJSON: "mel_mobilite_et_transport:stations_metro",
    TRAM_STOPS_GEOJSON: "mel_mobilite_et_transport:tramway_arrets",
    TRAM_LINES_GEOJSON: "mel_mobilite_et_transport:tramway_lignes",
    LINE_COLOURS_GEOJSON: "dsp_ilevia:couleurs_lignes",
}

# ⚠ NEVER `mel_mobilite_et_transport:sdit_ligne` / `sdit_station`. The names
# promise line geometry and they are MEL's Schéma Directeur des
# Infrastructures de Transport - the PLANNED network: projected tram corridors
# and BHNS routes, with `status: Variante` rows for alignments still under
# study, and no métro at all. Measured 2026-09-23. It is Toulouse's
# `en_service: 2027` trap with the whole layer prospective rather than four
# rows of it.

# The Métropole Européenne de Lille, EPCI 200093201: all 95 commune contours
# in one request, from the same national API every French city's boundary
# comes from. Step 1 keeps only the communes a station falls in.
MEL_EPCI_CODE = "200093201"
MEL_COMMUNES_URL = (f"https://geo.api.gouv.fr/epcis/{MEL_EPCI_CODE}/communes"
                    "?format=geojson&geometry=contour&fields=nom,code")

# ONE Overpass query for the whole city - never one per route - and filtered on
# the RELATION's network, which osm-rail records as safe where a node-level
# network filter is not. Métro geometry only exists here; the tram relations
# come along as gate 3's independent count.
#
# ⚠ THE NETWORK FILTER IS DOING REAL WORK. The same bbox holds three more
# `route=tram` relations that are not ilévia's: two for the Amitram HERITAGE
# tourist tram in the Deûle valley, and one tagged on an ABANDONED railway
# (Saint-Amand to Hellemmes). A mode-only query would draw all three.
OSM_BBOX = (50.55, 2.95, 50.80, 3.25)
OSM_ROUTES_QUERY = (
    "[out:json][timeout:120];"
    'relation["type"="route"]["route"~"^(subway|tram)$"]["network"="Ilévia"]'
    f"({OSM_BBOX[0]},{OSM_BBOX[1]},{OSM_BBOX[2]},{OSM_BBOX[3]});"
    "out geom;")

# ⚠ ILÉVIA'S GTFS IS DELIBERATELY NOT FETCHED. It has no shapes.txt, so it
# could not draw a line anyway, and every station it would supply MEL already
# publishes first-party under lov2. Not reading it also means the brief's open
# licence question - whether media.ilevia.fr's Mentions légales, which bar
# modifying « les contenus des Services en ligne », reach the feed - never has
# to be settled. The question was sidestepped, not answered.

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# LAMBERT-93, as every French city takes it: metropolitan France spans UTM 30N,
# 31N and 32N, and all five cities read one national file. The scaffold's
# per-longitude UTM proposal is overridden deliberately. Lille is at 3.06 E,
# inside the metropolitan domain check_provenance.py bounds this entry to.
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
# FIFTH CITY ON NEW YORK'S EDGES, and on TOULOUSE'S ground rather than Paris's.
# Measured 2026-09-23 across the 91 stations, in Lambert-93 metres:
#
#     min 193    median 501    mean 502    max 1,062
#
# Paris (399 m) and Marseille (341 m) took these edges because 966 m swamped a
# tight network. Toulouse (525 m) took them because a 483 m outer ring against
# its median very nearly TILES - and Lille lands in the same place, at 501 m.
# So this applies the owner's Toulouse decision on the measurement that decided
# it, keeping all four French cities on identical bands, rather than reopening
# it: a sibling in a different regime would have been put back to the owner.
#
# The 193 m minimum was checked by name, since it is also what one station
# under two names looks like: it is Croisé Laroche (the R/T junction) and Foch,
# the next stop on T's branch - two real stops. Every pair under 300 m was
# read and all four are distinct stations.
RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]

# --- Station scope ----------------------------------------------------------

# WHAT COUNTS: ilévia's two VAL métro lines and its two tram lines, R and T.
#
# THREE SOURCES, CHOSEN LINE BY LINE IN osm-rail's DOCUMENTED ORDER - agency
# GIS layer first, OSM only where none exists:
#
#   stations, both modes   MEL `stations_metro`, `tramway_arrets`   first-party
#   tram line geometry     MEL `tramway_lignes`                     first-party
#   métro line geometry    OpenStreetMap route relations            no agency layer
#
# The métro has NO first-party line geometry: ilévia's GTFS carries no
# shapes.txt, MEL's WFS carries métro stations as points only, and the one
# layer that looked like lines (sdit_ligne, above) is the planned network.
#
# The tram layer is published in SECTIONS rather than lines - `ligne` reads
# "R", "T" or "R,T" (the shared trunk Lille - Croisé Laroche) - so step 1
# assembles one feature per line and writes it to TRAM_LINES_BY_LINE_GEOJSON.
LINES = {
    # key: (mode, OSM ref, public name)
    "M1": ("metro", "1", "Métro 1"),
    "M2": ("metro", "2", "Métro 2"),
    "R": ("tram", "R", "Tram R"),
    "T": ("tram", "T", "Tram T"),
}
LINE_NAMES = {k: v[2] for k, v in LINES.items()}

# ilévia's OWN livery, from MEL's `dsp_ilevia:couleurs_lignes` (344 rows, one
# per line on the network) - not OpenStreetMap's `colour` tags, which are
# mappers' choices: OSM has R green (#81CF00) and T blue (#0099FF).
#
# ⚠ THE OPERATOR GIVES THE TRAM ONE COLOUR, NOT TWO. Its row is
# `code_ligne_public: TRAM`, #009FE3, covering R and T together.
#
# The first build drew both lines in it, relying on each line's label to tell
# them apart - and pipeline/linecolour.py REFUSED it: "Tram R vs Tram T is
# Delta-E 0.0 from each other". It scores drawn lines against each other as
# well as against the pins, so two lines sharing a colour is the same failure
# as a line sharing a pin's colour. That was the right call; labels alone
# don't make two overlapping lines distinguishable.
#
# PARIS'S PRECEDENT, and add-city Step 6's rule for shared agency colours: keep
# the official colour on one line, shift only the other, and make the shift
# clear the sibling AND every pin (Paris's first bis-line override fixed its
# tie and landed 15.6 from a pin). So R keeps ilévia's #009FE3 and T takes the
# same hue (198 deg) darkened, lightness 0.45 -> 0.26: #005D85.
#
# Chosen by measurement, not eye. Separation rises monotonically as the shade
# darkens - the check alone would pick #003247 at 50.7 - but a near-black line
# vanishes on the DARK BASEMAP the maps open with, which the Delta-E check
# does not score. #005D85 sits at the lightness of Toulouse's T1 (#004687),
# which renders visibly there, and every separation it has clears the
# operator colour's own worst (25.9):
#
#     Tram T #005D85   vs Tram R 29.3   vs Retail pin 34.4
#     Tram R #009FE3   vs Retail pin 25.9  (below the preferred 45; the band
#                      Toulouse's T1 sits in at 24.7, kept under the branding
#                      decision)
#     Métro 1 #FDC41F  86.3 from Personal services
#     Métro 2 #E30613  49.1 from Food service
LINE_COLOURS = {"M1": "#FDC41F", "M2": "#E30613", "R": "#009FE3", "T": "#005D85"}

# THE SERVED COMMUNES, asserted rather than trusted - measured 2026-09-23 by
# placing every station point in the official commune contours. 98
# station-line pairs, each in exactly one commune:
#
#     59350 Lille              M1 13  M2 19  tram 3
#     59599 Tourcoing                 M2  9  tram 4
#     59512 Roubaix                   M2  6  tram 6
#     59009 Villeneuve-d'Ascq  M1  5  M2  2  tram 2
#     59378 Marcq-en-Barœul                  tram 8
#     59646 Wasquehal                 M2  2  tram 5
#     59163 Croix                     M2  2  tram 2
#     59410 Mons-en-Barœul            M2  3
#     59368 La Madeleine                     tram 3
#     59421 Mouvaux                          tram 3
#     59328 Lambersart                M2  1
#
# ⚠ LAMBERSART IS ABSENT FROM MEL'S OWN LABELS. MEL's `insee` field puts no
# station there; the spatial test finds one. Deriving the scope from the
# attribute would have silently dropped a commune the network serves.
EXPECTED_SERVED_COMMUNES = {
    "59009": "Villeneuve-d'Ascq", "59163": "Croix", "59328": "Lambersart",
    "59350": "Lille", "59368": "La Madeleine", "59378": "Marcq-en-Barœul",
    "59410": "Mons-en-Barœul", "59421": "Mouvaux", "59512": "Roubaix",
    "59599": "Tourcoing", "59646": "Wasquehal",
}

# --- Business filtering ------------------------------------------------

# The served communes' INSEE codes, EXACT, plus two legacy codes.
#
# ⚠ MEL codes Lomme (355) and Hellemmes (298) as communes of their own - its
# `insee` field is a 3-digit SUFFIX - but both are communes associées of Lille
# and inside 59350's contour. Measured 2026-09-23 in SIRENE:
#
#     59350  226,204 rows      59355  22      59298  2
#
# So SIRENE folds them into 59350 and MEL's separate codes are MEL's
# convention, not INSEE's. The 24 legacy-coded rows are kept: they sit inside
# the drawn area, and dropping them would be a filter nobody chose.
COMMUNE_PREFIXES = tuple(sorted(EXPECTED_SERVED_COMMUNES)) + ("59298", "59355")

CITY_KEEP = "LILLE"   # scaffold template field; COMMUNE_PREFIXES is the filter

# The per-city catch-all verdict, TAKEN 2026-09-23 from this scope's own shares:
#
#     96.09Z   Paris 9.6%  Marseille 9.8%  Toulouse 13.9%  LILLE (REG.) 11.2%  (1,519)
#     56.29B   Paris 1.0%  Marseille 1.0%  Toulouse  1.6%  LILLE (REG.)  1.6%  (  215)
#
# And the same signature that justified it in Toulouse: rows with NO employee
# band are 23.4% catch-all against 7.5% for rows that record one (Toulouse
# 26.4 / 8.8), and are the less-named group (45.8% vs 54.7%). Same shape, same
# evidence, same two codes. The three retail catch-alls are kept, as in every
# sibling - 47.78C is the largest yet at 3.3%, but INSEE's label still says
# "en magasin", which is the distinction the exclusion turns on.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the SERVED communes' measured extent plus ~0.02 deg (about
# 2 km). Their union measures 50.5991-50.7490 N, 2.9680-3.2174 E, 132.2 km2.
# The box catches a CORRUPT coordinate; the commune filter does the scoping.
LILLE_BBOX = {"lat_min": 50.58, "lat_max": 50.77,
              "lon_min": 2.95, "lon_max": 3.24}
