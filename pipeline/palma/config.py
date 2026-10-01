"""Palma-specific settings, scoped to one city per this project's per-city
folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py; filled from the brief
(docs/build_briefs/palma.md).

A FOOD-ONLY PAGE (owner, 2026-09-29: Band B, Glasgow's twin). The one source
is the Consell de Mallorca's register of restaurant and entertainment
establishments, on the Govern de les Illes Balears's catalogue: every bar,
café and restaurant on the island, typed by `Grup`. It carries coordinates
for about one in eight rows; the rest are placed by joining their address to
the Dirección General del Catastro's INSPIRE address points for the
municipality (pipeline/countries/catastro.py), the address-join skill's
method.
"""

from pathlib import Path

SLUG = "palma"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "palma" / "raw"
DATA_PROCESSED = ROOT / "data" / "palma" / "processed"
OUTPUTS = ROOT / "outputs" / "palma"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the municipality, with the municipality each is in (M2's
# outer stops are in Marratxí).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# What step 2 left out and why, one row per establishment (trade names only;
# `Explotador/s`, the operator, is never read).
EXCLUDED_PREMISES_CSV = OUTPUTS / "excluded_premises.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) --------------

# THE REGISTER: Registre d'Establiments de Restauració i Entreteniment de
# Mallorca, GOIB catalogue (CKAN `empreses-restauracio-entreteniment-mallorca`),
# island-wide, ';'-separated, UTF-8 with a BOM. The resource was last modified
# 2026-09-07 (the date the page states, a condition of GOIB's terms).
REGISTER_URL = ("https://intranet.caib.es/opendatacataleg/files/dataset/"
                "empreses_restauracio_mallorca/empreses_restauracio_mallorca.csv")
REGISTER_CSV = DATA_RAW / "empreses_restauracio_mallorca.csv"
REGISTER_DATASET_URI = ("https://intranet.caib.es/opendatacataleg/dataset/"
                        "empreses-restauracio-entreteniment-mallorca")
REGISTER_UPDATED = "2026-09-07"
MUNICIPI = "PALMA"
# The columns read, by name. NEVER `Explotador/s`: it names the operator,
# sometimes a person with a tax id.
REGISTER_COLUMNS = ["Signatura", "Estat", "Grup", "Denominació comercial", "Direcció",
                    "Municipi", "Localitat", "UTM (X)", "UTM(Y)", "latitude", "longitude"]

# THE ADDRESS POINTS: Catastro's INSPIRE Addresses for Palma (07040), from
# the province-07 ATOM feed; 55,609 points in EPSG:25831, dated 2026-08-21.
# ⚠ Catastro's certificate chain fails with Python's bundled store:
# fetch_sources.py uses the OS store (truststore), never verification off.
CATASTRO_ATOM_URL = "https://www.catastro.hacienda.gob.es/INSPIRE/Addresses/07/ES.SDGC.AD.atom_07.xml"
CATASTRO_URL = ("https://www.catastro.hacienda.gob.es/INSPIRE/Addresses/07/07040-PALMA/"
                "A.ES.SDGC.AD.07040.zip")
CATASTRO_ZIP = DATA_RAW / "A.ES.SDGC.AD.07040.zip"
CATASTRO_CRS = "EPSG:25831"

# THE MUNICIPALITY: OSM relation 341321 (Palma, INE 07040), polygonised from
# its outer ways (Glasgow's method) and gated on its area (~209 km2 of land;
# the polygon takes in the bay's islets, Cabrera excepted).
BOUNDARY_OSM_RELATION = 341321
BOUNDARY_OSM_CACHE = DATA_RAW / "osm_boundary.json"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
BOUNDARY_AREA_KM2 = (190.0, 230.0)
# The neighbouring municipalities, to NAME a station outside Palma.
NEIGHBOURS_OSM_CACHE = DATA_RAW / "osm_municipalities.json"

OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
RAIL_BBOX = (39.54, 2.58, 39.70, 2.80)          # south, west, north, east

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# ETRS89 / UTM zone 31N: Palma (~2.65 E) falls in the 0 to 6 band, and
# Catastro publishes in it. Derived per city, not copied.
CRS_PROJECTED = "EPSG:25831"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: the in-city stations' median gap is about 580 m (the
# brief's 583 m), over the ~550 m line. Step 1 prints and gates it.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# RAIL FROM OPENSTREETMAP: Metro de Palma M1, operator Serveis Ferroviaris de
# Mallorca (SFM), Plaça d'Espanya (the Estació Intermodal) to ParcBit,
# purpose-built and mostly in tunnel. OSM tags it `light_rail`; SFM calls it
# metro, and the macro legend keys it as metro (Newcastle's precedent, its
# Metro also light_rail in OSM). A WHITELIST on ref + route.
#
# ONE LINE, NOT TWO (measured 2026-09-30, owner's call the same day to build
# on it): the brief's M2 (Plaça d'Espanya to Marratxí) is no longer a metro
# service. TIB, the Consorci de Transports de Mallorca's timetable site, lists
# one metro line, M1; the Marratxí corridor is served by SFM's trains T1-T3,
# suburban rail, not drawn. OSM still carries M2's two relations.
#
# M1'S TIMETABLE IS DISCLOSED, NOT DISQUALIFYING (the owner's light-rail test,
# 2026-09-29: frequency gates converted railway only, Buffalo's call): a train
# every 20 minutes in term time, every 30-40 in holidays, Saturdays until
# 15:00, no Sunday service (Wikipedia's Palma Metro, citing TIB).
ROUTE_TYPES = ("light_rail", "subway", "tram")    # what the query fetches
LINE_REFS = ("M1",)
OPERATOR = "Serveis Ferroviaris de Mallorca"
# Relations in the box that are NOT drawn, each named with its reason; step 1
# exits on any other relation it cannot place.
NOT_DRAWN = {
    4635401: "M2 to Marratxí: no longer a metro service (TIB lists M1 only; trains T1-T3)",
    7781524: "M2 from Marratxí: no longer a metro service (TIB lists M1 only; trains T1-T3)",
}

LINE_NAMES = {"M1": "Metro M1"}
# OSM's colour tag (SFM's yellow); checked against the pins in step 3 (only
# Food service is drawn here).
LINE_COLOURS = {"M1": "#f1b03e"}

STATION_NAME_ALIASES = {}
COLLAPSE_MAX_SPREAD_M = 250

SPACING_MIN_M = 550.0

# GATE 3: TIB's own stop list for M1, read in a browser 2026-09-30 (the page
# is rendered by script): stops 301-310, Estació Intermodal to ParcBit.
OPERATOR_STATION_COUNTS = {"Metro M1": 10}
OPERATOR_COUNTS_SOURCE = ("TIB's M1 line page (https://www.tib.org/en/linies-i-horaris/metro/-/"
                          "linia/M1), stops 301-310, read 2026-09-30")

# --- Business filtering ------------------------------------------------

# Active is `Estat == "Alta"`; "Baixa temporal" (temporarily closed) is out.
ACTIVE_STATES = {"Alta"}

# In-municipality rows are the register's own `Municipi`, the Consell's
# assignment; placed points are also checked against the boundary.
CITY_KEEP = MUNICIPI

TAXONOMY_SYSTEM = "palma_restauracio"
RAW_CLASSIFICATION_COLUMN = "premises_kind"

# The address join (pipeline/countries/catastro.py): the nearest listed
# number on the same side of the street within this many numbers stands in
# for a number Catastro does not list (Incheon's precedent).
NEAREST_NUMBER_MAX = 6
# A register coordinate further than this from its own joined Catastro
# address counts against the join's control (step 2 prints the distribution).
CONTROL_AGREE_M = 100

# Sanity bounds: the municipality's extent plus a margin.
PALMA_BBOX = {
    "lat_min": 39.45,
    "lat_max": 39.70,
    "lon_min": 2.50,
    "lon_max": 2.85,
}
