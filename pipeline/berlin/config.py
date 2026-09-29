"""Berlin-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "berlin" / "raw"
DATA_PROCESSED = ROOT / "data" / "berlin" / "processed"
OUTPUTS = ROOT / "outputs" / "berlin"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs, all keyless, downloaded by fetch_sources.py (never by a step).
# Brief: docs/build_briefs/berlin.md.
#
# The register: IHK Berlin's Gewerbedaten, the chamber of commerce's
# membership as premises points, CC0 1.0 on this channel (GitHub, Git LFS;
# the WFS copy is dl-de/zero-2.0). Monthly; the fetch date pins the snapshot.
# It carries NO name and NO street column - fetch_sources.py exits if one
# ever appears (the download boundary is the privacy control).
BUSINESSES_URL = ("https://media.githubusercontent.com/media/IHKBerlin/"
                  "IHKBerlin_Gewerbedaten/master/data/IHKBerlin_Gewerbedaten.csv")
# VBB's GTFS (Berlin-Brandenburg), CC BY 4.0 per VBB's own dataset page:
# credit "VBB Verkehrsverbund Berlin-Brandenburg GmbH", say it was modified.
GTFS_URL = "https://www.vbb.de/gtfs"
# ALKIS Berlin's Land boundary (SenStadt, dl-de/zero-2.0), one feature.
BOUNDARY_URL = ("https://gdi.berlin.de/services/wfs/alkis_land?SERVICE=WFS"
                "&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=alkis_land:landesgrenze"
                "&OUTPUTFORMAT=application/json&SRSNAME=EPSG:4326")
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "IHKBerlin_Gewerbedaten.csv"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
PROVENANCE_JSON = DATA_RAW / "provenance.json"
# Register columns that match fetch_sources.py's name-like fragments but are
# known to be harmless (an area's name, say). Empty: none do, as of 2026-09-28.
REGISTER_ALLOWED_NAMEISH = ()
SOURCE_ENCODING = "utf-8"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 33N: the longitude (~13.40) falls in the 12 to 18 band. Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "EPSG:32633"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# Modes, as VBB's GTFS codes them (extended route types) and who runs them.
# Matched on (route_type, agency_id) and then on route_short_name, NEVER on
# route_id: VBB carries several route_ids per line (S5 has four), and type 700
# holds each line's rail-replacement buses under the same short name.
MODES = {
    "U": {"route_type": "400", "agency_id": "796", "label": "U-Bahn (BVG)"},
    "S": {"route_type": "109", "agency_id": "1", "label": "S-Bahn (S-Bahn Berlin)"},
    "T": {"route_type": "900", "agency_id": "796", "label": "Tram (BVG)"},
}
# Which modes are drawn - U-Bahn and S-Bahn. The S-Bahn passes the spacing-
# and-frequency test Copenhagen's S-tog and Dublin's DART passed. TRAMS ARE
# LEFT OUT (owner, 2026-09-28, "Berlin's rail scope"): U+S is 275 stations and
# 82.0% of storefronts in the rings; trams would add 518 tram-only stops for
# 88.9%. The precedent of a full metro beside trams (Paris, Barcelona, Milan,
# Toronto), not of trams as the core network (Amsterdam, Rotterdam, Oslo, Riga).
DRAWN_MODES = ("U", "S")

# Stations the feed does not serve because they are CLOSED FOR WORKS, drawn as
# the timetable runs (owner, 2026-09-28): the U6's Tegel branch, closed since
# November 2022, replacement buses until about August 2027 (BVG, "U6-Nord
# Streckensanierung"). Step 1 records them as excluded and STOPS if the feed
# serves any of them again - the reopening is a re-run, not a surprise.
CLOSED_FOR_WORKS = {
    name: "U6, closed for works (Kurt-Schumacher-Platz - Alt-Tegel) since "
          "November 2022, replacement buses until about August 2027"
    for name in ("Scharnweberstr.", "Otisstraße", "Holzhauser Str.", "Borsigwerke",
                 "Alt-Tegel")
}

# Short name -> the name riders use. The feed's short names are the public
# names (BVG and S-Bahn Berlin sign "U1", "S41").
LINE_NAMES = {
    **{f"U{n}": f"U{n}" for n in range(1, 10)},
    **{s: s for s in ("S1", "S2", "S25", "S26", "S3", "S41", "S42", "S46", "S47",
                      "S5", "S7", "S75", "S8", "S85", "S9", "S15")},
}

# GATE 3, network-wide (the operators publish no per-line figure used here).
# The feed is compared with the published count LESS the stations closed for
# works (CLOSED_FOR_WORKS), which step 1 subtracts by name.
OPERATOR_STATION_COUNTS = {"U-Bahn (network)": 175, "S-Bahn (network)": 168}
OPERATOR_COUNTS_SOURCE = ("U-Bahn 175 stations, 9 lines: BVG, 'BVG in Zahlen' "
                          "(as of 31.12.2024); S-Bahn 168 stations, 16 lines: S-Bahn "
                          "Berlin, 'S-Bahn Berlin at a glance' - both read 2026-09-28")

# VBB names a stop "S+U Alexanderplatz Bhf (Berlin)": a mode prefix, a
# station-building suffix and the town. The prefix and the town are stripped
# for display (a LEADING prefix, per add-city's over-stripping rule); what is
# left is the name riders use. Stops in Brandenburg keep their town.
STATION_PREFIXES = ("S+U ", "S ", "U ")
STATION_SUFFIXES = (" (Berlin)", " Bhf")
# A collapsed name whose platforms are further apart than this is two places.
# S+U interchanges in Berlin can be a long walk (both kept as one station, as
# the operators' own maps draw them).
COLLAPSE_MAX_SPREAD_M = 450
SPACING_MIN_M = 400.0

# --- Business filtering ------------------------------------------------

# In-city rows: the register is IHK BERLIN's, so `city` is "Berlin" on every
# row (368,841 of 368,841, 2026-09-28) and carries no information. The Land
# polygon (ALKIS) is the filter: 11 rows geocoded outside it, as far as the
# Rhineland (6.67 E), are dropped by step 2.
CITY_KEEP = "Berlin"

TAXONOMY_SYSTEM = "ihk_wz2025"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "nace_desc"

# The per-city catch-all verdicts, which ihk_wz2025.py declines to make, keyed
# by the column they are read on. DECIDED 2026-09-28 (owner, DECISIONS
# "Berlin's calls"):
#
#   ihk_branch_id 47122  "Einzelhandel mit Waren verschiedener Art,
#                        Hauptrichtung Nicht-Nahrungsmittel": 12,141 rows, 24%
#                        of retail; 91% zero-employee against 57-69% for the
#                        rest of retail; within 30 m of an OSM shop 63% of the
#                        time, office level (62-77%) rather than the rest of
#                        retail's 81%. EXCLUDED - unlike Oslo, Copenhagen and
#                        Prague, which kept 47.12. Its siblings under 4712
#                        (47121, department stores, Sonderposten) stay.
#   nace_id 969          9699 n.e.c. (10,208) and 2 bare `969` rows: trade-fair
#                        hosts, hospitality services, clearance, escort and
#                        prostitution, residual codes. EXCLUDED, as Oslo's
#                        96.990 and Copenhagen's 969900 (9691 is structural).
#
# The other WZ catch-alls (4727, 4769, 4778) are kept, as in every Rev. 2.1
# city: shops by product.
#
# MATCHING DIFFERS BY COLUMN: a WZ code is a PREFIX (the taxonomy's ragged-
# depth rule), an IHK branch code is EXACT - IHK nests its own children under
# a branch, and `471221` (department stores) sits under `47122`.
CATCH_ALL_EXCLUDE = {
    "ihk_branch_id": ("47122",),   # exact
    "nace_id": ("969",),           # prefix
}

# The register's columns that step 2 reads for MEASURING and never writes out:
# with a point, they narrow a sole trader at home (the brief's "Privacy").
MEASURE_ONLY_COLUMNS = ("employees_range", "business_age", "business_type")

# Sanity bounds: the ALKIS Land polygon's extent (52.3382-52.6755 N,
# 13.0883-13.7612 E; 890.7 km2 in UTM 33N, measured 2026-09-28) plus ~0.02 deg. The polygon does the filtering; this
# catches a CRS or axis error.
BERLIN_BBOX = {
    "lat_min": 52.31,
    "lat_max": 52.70,
    "lon_min": 13.06,
    "lon_max": 13.79,
}
