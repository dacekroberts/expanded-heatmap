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
# Each drawn line's chosen GTFS shape (step 1 writes it; step 3 and
# scripts/line_colour_search.py read it).
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
# A shape "passes" a station within this distance (platform centroid to track).
SHAPE_STATION_M = 150
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
# The CSV's commit history on GitHub, for the register's own date.
REGISTER_COMMITS_URL = ("https://api.github.com/repos/IHKBerlin/IHKBerlin_Gewerbedaten/"
                        "commits?path=data/IHKBerlin_Gewerbedaten.csv&per_page=1")
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
# Read by the app page for its snapshot caption, so it lives in outputs/ (the
# deployed app has no data/).
PROVENANCE_JSON = OUTPUTS / "provenance.json"
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

# Each line's OPERATOR hue: VBB's GTFS `route_color` (CC BY 4.0, read
# 2026-09-28). VBB colours by FAMILY - S2/S25/S26, S7/S75, S8/S85, S46/S47
# and S1/S15 share one colour each - which check_map_markup.py refuses on one
# map (CIE76 10 anywhere, 18 within 500 m), so the drawn colour is the one
# scripts/line_colour_search.py finds nearest each hue (LINE_COLOURS, below).
# Order is priority: a line earlier in LINE_ORDER keeps nearer its own hue, so
# the U-Bahn and each family's main line come first.
LINES = {
    "U1": {"hue": "#7DAD4C"}, "U2": {"hue": "#DA421E"}, "U3": {"hue": "#16683D"},
    "U4": {"hue": "#F0D722"}, "U5": {"hue": "#7E5330"}, "U6": {"hue": "#8C6DAB"},
    "U7": {"hue": "#009BD5"}, "U8": {"hue": "#224F86"}, "U9": {"hue": "#F3791D"},
    "S1": {"hue": "#DA6BA2"}, "S2": {"hue": "#007734"}, "S3": {"hue": "#0066AD"},
    "S41": {"hue": "#AD5937"}, "S42": {"hue": "#CB6418"}, "S5": {"hue": "#EB7405"},
    "S7": {"hue": "#816DA6"}, "S8": {"hue": "#66AA22"}, "S9": {"hue": "#992746"},
    "S46": {"hue": "#CD9C53"}, "S25": {"hue": "#007734"}, "S26": {"hue": "#007734"},
    "S47": {"hue": "#CD9C53"}, "S75": {"hue": "#816DA6"}, "S85": {"hue": "#66AA22"},
    "S15": {"hue": "#DA6BA2"},
}
LINE_ORDER = list(LINES)
# `python scripts/line_colour_search.py berlin` (defaults: 500 m, CIE76 18),
# run 2026-09-28 on step 1's lines.geojson: 3,817 feasible colours; closest
# pair within 500 m 18.0 (S46, S47), anywhere 10.3 (U1, S85); every line
# >= 45.0 from every pin; 25 distinct dark-mode labels. The pins' blue, pink
# and green rule out VBB's own blues and greens, so U3/S2 read olive, S3 and
# U8 grey-blue, S9 salmon - Osaka's and Tokyo's trade.
LINE_COLOURS = {
    "U1": "#608000", "U2": "#E04820", "U3": "#606848", "U4": "#A09800", "U5": "#885838",
    "U6": "#B880A8", "U7": "#08A0C0", "U8": "#506878", "U9": "#E87010", "S1": "#C870C8",
    "S2": "#586818", "S3": "#7098A8", "S41": "#B86038", "S42": "#B05000", "S5": "#D08000",
    "S7": "#805878", "S8": "#60A000", "S9": "#C88070", "S46": "#B88840", "S25": "#909040",
    "S26": "#20A800", "S47": "#806018", "S75": "#A088A0", "S85": "#809820", "S15": "#9840A0",
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
# A station belongs to a line where at least this share of the line's trips
# call (step 1 prints every pair under it): below it are the feed window's
# construction diversions and occasional short workings.
LINE_STOP_MIN_SHARE = 0.10

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
#   ihk_branch_id 477893 "Einzelhandel mit Brennstoffen": heating-fuel dealers
#                        (36), nonstore everywhere (owner, 2026-09-29,
#                        DECISIONS "Category check: the owner's calls"). Not
#                        a catch-all, but the only exact-branch filter step 2
#                        has; the rest of 4778 stays.
CATCH_ALL_EXCLUDE = {
    "ihk_branch_id": ("47122", "477893"),   # exact
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

# --- Place search (scripts/place_search_scaffold.py, 2026-10-13) ---

PLACE_AREA = "(id:3600062422)"
PLACE_OSM_JSON = DATA_RAW / "osm_places_2026-10-13.json"
PLACE_OSM_EXTRA_JSON = DATA_RAW / "osm_places_extra_2026-10-13.json"
PLACE_LANGUAGES = ("de",)
PLACE_FOLD = None
# Rows a reader held that the owner ruled to keep (2026-10-13;
# docs/decisions_drafts/search-final.md). A record only: no code reads it.
# A street is listed by name, a place by OSM id with its name. Not in
# PLACE_REVIEWED, which check E holds to names carrying a leak word.
PLACE_RULED_KEPT = {
    # Held rows kept by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    # A home, family or person row is listed by id alone.
    "Bergstr.": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Carl-Langbecker-Str.": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Goten-Str.": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Gottfried-Funeck-Weg (Wuhlesteg)": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Autobahnzubringer Dresden": "A road's own name on its mainline ways is no ramp (owner 2026-10-13, seven rulings 6: Monterrey's avenue names)",
    "Charitéplatz": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Bonhoefferweg": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "DGZ-Ring": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Bachsaiblingstraße": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Belgienstraße": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Am Güterbahnhof Halensee": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Gewerbegebiet zum Wasserwerk": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Altes Gaswerk Mariendorf": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Gewerbehof": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Am Cleantech Business Park": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Fresienweg": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Dalienweg": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Ädikulanische Treppe": "A minor way is kept with an entry or article of its own (2026-10-07)",
    "Andersen Weg": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Frau Holle Weg": "A misspelled, cut or abbreviated name is still that place and no name is repaired (owner 2026-10-13, seven rulings 1; the typo line)",
    "Lagerweg": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Platz A": "The description, code and ramp-name rules read minor or ramp-class ways only; another street keeps such a name (owner 2026-10-13: The Avenue stays; German answers 3: Weg A and Weg B)",
    "Platz E": "The description, code and ramp-name rules read minor or ramp-class ways only; another street keeps such a name (owner 2026-10-13: The Avenue stays; German answers 3: Weg A and Weg B)",
    "Parksiedlung Spruch": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Metropolitan Park": "A site's own name on a residential or larger way reads as the street's name and stays (owner 2026-10-13, fifteen answers 9, as measured)",
    "Kitaweg": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Kantinenweg": "A site's road with a street word is kept (owner 2026-10-13, fifteen answers 9; six answers 4)",
    "Niebüllerweg (Parkstraße)": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Pankeweg (Panke-Trail)": "Two real names in one stay as written (owner 2026-10-13, second batch d; fourteen answers 12; candidate 23, no rule)",
    "Stadtring Berlin": "A road's own name on its mainline ways is no ramp (owner 2026-10-13, seven rulings 6: Monterrey's avenue names)",
    "Sachsendammsteg": "Named bridges and tunnels stay as street rows (owner 2026-10-13, fourteen answers 1; fifteen answers 11)",
}
PLACE_REVIEWED = {
    "Shakespeare Company Berlin": "a theatre, not a firm (owner, 2026-10-13)",
}
# The read of 2026-10-13 (docs/decisions_drafts/search-final.md).
PLACE_DROPPED = {
    "way/779355298": "a housing complex (owner, 2026-10-13)",
    "way/779355299": "a housing complex (owner, 2026-10-13)",
    "way/11645391": "a generic path word as the whole name (owner, 2026-10-13)",
    "way/23950137": "a generic path word as the whole name (owner, 2026-10-13)",
    "way/24667659": "a generic path word as the whole name (owner, 2026-10-13)",
    "way/40233852": "a generic path word as the whole name (owner, 2026-10-13)",
    "way/47126304": "a generic path word as the whole name (owner, 2026-10-13)",
    "way/58428733": "a generic path word as the whole name (owner, 2026-10-13)",
    "way/59266966": "a generic path word as the whole name (owner, 2026-10-13)",
    "way/266583999": "a generic path word as the whole name (owner, 2026-10-13)",
    "way/253364082": "a letter code beside a path type on minor ways",
    "way/217003490": "a letter code beside a path type on minor ways",
    "way/112844760": "a letter code beside a path type on minor ways",
    "way/217003494": "a letter code beside a path type on minor ways",
    "way/136086625": "a letter code beside a path type on minor ways",
    "way/136086622": "a letter code beside a path type on minor ways",
    "way/136086628": "a letter code beside a path type on minor ways",
    "way/934990263": "a letter code beside a path type on minor ways",
    "way/22963446": "a station platform",
    "way/4693121": "a motorway ramp or interchange label",
    "way/1561958591": "a motorway interchange label",
    "way/1561958592": "a motorway interchange label",
    "way/1561958627": "a motorway interchange label",
    "way/1561958631": "a motorway interchange label",
    "way/1561958632": "a motorway interchange label",
    "way/19791144": "a motorway interchange label",
    "way/229901568": "a motorway interchange label",
    "way/24159670": "a motorway interchange label",
    "way/24159672": "a motorway interchange label",
    "way/24159675": "a motorway interchange label",
    "way/24159676": "a motorway interchange label",
    "way/24258875": "a motorway interchange label",
    "way/27184257": "a motorway interchange label",
    "way/322543960": "a motorway interchange label",
    "way/32655061": "a motorway interchange label",
    "way/32890426": "a motorway interchange label",
    "way/4525999": "a motorway interchange label",
    "way/4920940": "a motorway interchange label",
    "way/83917718": "a motorway interchange label",
    "way/83917719": "a motorway interchange label",
    "way/83917725": "a motorway interchange label",
    "way/83917726": "a motorway interchange label",
    "way/861110054": "a motorway interchange label",
    "way/217003495": "a bare letter code beside a path type on minor ways",
    "way/217003499": "a bare letter code beside a path type on minor ways",
    "way/136086612": "a bare letter code beside a path type on minor ways",
    "way/136086611": "a bare letter code beside a path type on minor ways",
    "way/136086619": "a bare letter code beside a path type on minor ways",
    "way/217003505": "a bare letter code beside a path type on minor ways",
    "way/217003506": "a bare letter code beside a path type on minor ways",
    "way/217003507": "a bare letter code beside a path type on minor ways",
    "way/5059978": "two street names glued into one",
    "way/24700633": "two street names glued into one",
    "way/109934083": "two street names glued into one",
    "way/25913689": "a numbered code as a name, on minor ways only",
    "way/29311551": "a numbered code as a name, on minor ways only",
    "way/1429015978": "a numbered code as a name, on minor ways only",
    "way/34016080": "a numbered code as a name, on minor ways only",
    "way/51899520": "a numbered code as a name, on minor ways only",
    "way/25861573": "a numbered code as a name, on minor ways only",
    "way/25514058": "a numbered code as a name, on minor ways only",
    "way/41211942": "a numbered code as a name, on minor ways only",
    "way/24220012": "a numbered code as a name, on minor ways only",
    "way/27171765": "a numbered code as a name, on minor ways only",
    "way/122944506": "a numbered code as a name, on minor ways only",
    "way/1447976286": "a numbered code as a name, on minor ways only",
    "way/1447976287": "a numbered code as a name, on minor ways only",
    "way/1447976288": "a numbered code as a name, on minor ways only",
    "way/1447976297": "a numbered code as a name, on minor ways only",
    "way/16307629": "a numbered code as a name, on minor ways only",
    "way/239488032": "a numbered code as a name, on minor ways only",
    "way/239488035": "a numbered code as a name, on minor ways only",
    "way/151742520": "a numbered code as a name, on minor ways only",
    "way/1157153090": "a numbered code as a name, on minor ways only",
    "way/1164224731": "a numbered code as a name, on minor ways only",
    "way/135777022": "a numbered code as a name, on minor ways only",
    "way/151742522": "a numbered code as a name, on minor ways only",
    "way/296125458": "a numbered code as a name, on minor ways only",
    "way/1164224733": "a numbered code as a name, on minor ways only",
    "way/135777024": "a numbered code as a name, on minor ways only",
    "way/151742523": "a numbered code as a name, on minor ways only",
    "way/153947921": "a numbered code as a name, on minor ways only",
    "way/212499225": "a numbered code as a name, on minor ways only",
    "way/24220163": "a numbered code as a name, on minor ways only",
    "way/24220027": "a numbered code as a name, on minor ways only",
    "way/50283373": "a numbered code as a name, on minor ways only",
    "way/104946132": "a numbered code as a name, on minor ways only",
    "way/23943477": "a numbered code as a name, on minor ways only",
    "way/495532539": "a numbered code as a name, on minor ways only",
    "way/990466813": "a numbered code as a name, on minor ways only",
    "way/277724056": "a numbered code as a name, on minor ways only",
    "way/1134240129": "a numbered code as a name, on minor ways only",
    "way/1134241412": "a numbered code as a name, on minor ways only",
    "way/153879696": "a numbered code as a name, on minor ways only",
    "way/376878294": "a numbered code as a name, on minor ways only",
    "way/376878295": "a numbered code as a name, on minor ways only",
    "way/1291980527": "a numbered code as a name, on minor ways only",
    "way/153879697": "a numbered code as a name, on minor ways only",
    "way/138522486": "a numbered code as a name, on minor ways only",
    "way/1494726027": "a numbered code as a name, on minor ways only",
    "way/1494726028": "a numbered code as a name, on minor ways only",
    "way/1494726030": "a numbered code as a name, on minor ways only",
    "way/1494726031": "a numbered code as a name, on minor ways only",
    "way/27475119": "a numbered code as a name, on minor ways only",
    "way/152258407": "a numbered code as a name, on minor ways only",
    "way/152258416": "a numbered code as a name, on minor ways only",
    "way/23382152": "a numbered code as a name, on minor ways only",
    "way/367488327": "a numbered code as a name, on minor ways only",
    "way/11028248": "a numbered code as a name, on minor ways only",
    "way/1038264032": "a numbered code as a name, on minor ways only",
    "way/1038264033": "a numbered code as a name, on minor ways only",
    "way/1216488981": "a numbered code as a name, on minor ways only",
    "way/138160584": "a numbered code as a name, on minor ways only",
    "way/22731043": "a numbered code as a name, on minor ways only",
    "way/840167882": "a numbered code as a name, on minor ways only",
    "way/905940429": "a numbered code as a name, on minor ways only",
    "way/15992873": "a numbered code as a name, on minor ways only",
    "way/15465842": "a numbered code as a name, on minor ways only",
    "way/38117686": "a numbered code as a name, on minor ways only",
    "way/119163833": "a numbered code as a name, on minor ways only",
    "way/15992999": "a numbered code as a name, on minor ways only",
    "way/1038266487": "a numbered code as a name, on minor ways only",
    "way/1429717669": "a letter code as a name, on minor ways only",
    "way/1429717670": "a letter code as a name, on minor ways only",
    "way/16215443": "a letter code as a name, on minor ways only",
    "way/33055775": "a letter code as a name, on minor ways only",
    "way/453721470": "a numbered code as a name, on minor ways only",
    "way/1188356970": "a facility gate's own road",
    "way/93494646": "a facility gate's own road",
    "way/1083165365": "a facility gate's own road",
    "way/1256154843": "a facility gate's own road",
    "way/729503768": "a facility gate's own road",
    "way/729503769": "a facility gate's own road",
    "way/93494648": "a facility gate's own road",
    "way/11664400": "a bare type word as the whole name",
    "way/156393017": "a bare type word as the whole name",
    "way/194074088": "a bare type word as the whole name",
    "way/4808110": "a bare type word as the whole name",
    "way/24152632": "a bare type word as the whole name",
    "way/1387293369": "a junction label of two names, not a street name",
    "way/4475630": "a junction label of two names, not a street name",
    "way/919304280": "a junction label of two names, not a street name",
    "way/524037019": "a small plot inside Gärten der Welt named only for a country (owner, 2026-10-13)",
    "way/524037023": "a small plot inside Gärten der Welt named only for a country (owner, 2026-10-13)",
    "way/524037022": "a small plot inside Gärten der Welt named only for a country (owner, 2026-10-13)",
    "way/1042056230": "a small plot inside Gärten der Welt named only for a country (owner, 2026-10-13)",
    "way/501358054": "a small plot inside Gärten der Welt named only for a country (owner, 2026-10-13)",
    "way/1042056279": "a courtyard inside a garden of Gärten der Welt, drawn as a locality (owner, 2026-10-13)",
    "way/497734026": "a courtyard inside a garden of Gärten der Welt, drawn as a locality (owner, 2026-10-13)",
    "way/497734021": "a courtyard inside a garden of Gärten der Welt, drawn as a locality (owner, 2026-10-13)",
    "node/286472713": "a grave on its subject's article, none of its own (owner's rule for graves, 2026-10-13)",
    "node/925074789": "a grave with no article of its own (owner's rule for graves, 2026-10-13)",
    "way/1020102178": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/179180924": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/66665912": "a dead railway alignment (disused:railway=disused) with no article of its own (owner, 2026-10-13)",
    "way/33740395": "a dead railway alignment (disused:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/816397837": "a dead railway alignment (disused:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/458296537": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/36953287": "a dead railway alignment (disused:railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/321744777": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/816397844": "a dead railway alignment (abandoned:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/950016907": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/44092093": "a dead railway alignment (disused:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/44092096": "a dead railway alignment (railway=disused) with no article of its own (owner, 2026-10-13)",
    "way/320978891": "a dead railway alignment (railway=disused) with no article of its own (owner, 2026-10-13)",
    "way/472647279": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/22769003": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/85985074": "a dead railway alignment (abandoned:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/1004715066": "a dead railway alignment (disused:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/45339534": "a dead railway alignment (railway=disused) with no article of its own (owner, 2026-10-13)",
    "way/223181787": "a dead railway alignment (disused:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/237806238": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/450504478": "a dead railway alignment (railway=disused) with no article of its own (owner, 2026-10-13)",
    "way/333404315": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/370079364": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/370079367": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/393979085": "a dead railway alignment (railway=abandoned) with no article of its own (owner, 2026-10-13)",
    "way/26150207": "a dead railway alignment (disused:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/26549816": "a dead railway alignment (disused:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/83796011": "a dead railway alignment (disused:railway=rail) with no article of its own (owner, 2026-10-13)",
    "way/8080757": "a home tagged an attraction, no visiting shown (owner, 2026-10-13; back in when a web check shows visiting)",
    "way/112149783": "a home tagged an attraction, no visiting shown (owner, 2026-10-13; back in when a web check shows visiting)",
    "way/27097528": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46891689": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/812548166": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/871612355": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/157585137": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/812550058": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/858121888": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/317882972": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/217003508": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/324321608": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12521949": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12522448": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12521913": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12522087": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/317882973": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12522051": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12522134": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/30886445": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/324321607": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12522309": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12521704": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/217003510": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12521760": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12522525": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12521609": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/317882974": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/12521993": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1117833201": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1117833202": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1117833209": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/178224648": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/26808155": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/662632672": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/832915142": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/26808126": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/26808078": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/178224643": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/144887144": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/144887145": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/144886451": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/144886099": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/56303550": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/144886078": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/56303548": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/56303549": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/56303545": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/56303543": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/56303544": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/56303558": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/144886079": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/37262403": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/145586626": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/178224632": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25015419": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25042817": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25796715": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/26000746": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27155052": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172364": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27604004": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/32838571": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/37262404": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/38058772": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46968062": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/47347066": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/61597306": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/6620416": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/694312370": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/941945984": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/973088321": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/14131656": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/16714150": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27603993": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/30894316": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/52718682": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/16714149": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/280138757": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27883186": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/301560426": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27603995": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/301560427": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27603994": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/47347065": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27604008": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/47347067": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/280138758": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/280138760": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1162514072": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/14131231": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/145586627": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/16714146": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/178224649": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24892805": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24892986": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25796821": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27155053": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172365": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27883178": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/28077787": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/283006277": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/28633668": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/32838552": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/37262405": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46347688": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46968061": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/61597299": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/6620432": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/92376382": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1364743762": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/165934469": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/234725001": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24892997": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25015425": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/26000704": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27155055": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172366": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27604002": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46347680": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46968060": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/486040671": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/5062569": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/627568989": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/6620394": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/769150193": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/92376366": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/92380432": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1282282812": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/129030609": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/14131326": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24897739": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25797005": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/26808501": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27155056": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172362": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27604003": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46348613": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/6620303": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/769150194": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/893914598": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/92376374": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/92380423": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/16714147": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/178224650": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24897719": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24897760": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27155057": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172368": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/280138761": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46347681": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/6620264": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/92376363": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/92380428": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/133072585": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24897683": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24897707": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27155058": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172022": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172358": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27883175": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/301560428": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/42146285": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/46348611": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/769150186": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/92380425": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/994425515": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27883180": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/280138763": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172023": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27172359": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/280138765": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/301560429": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/33881349": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1156699291": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/14131624": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/156346091": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25015418": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/280138766": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/301560430": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/42778616": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/52718701": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/941945981": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25015417": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27250292": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/280138768": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/301560431": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/52718691": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/208581397": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24038375": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25693667": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1050300941": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/132457370": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24038383": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25693699": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27598724": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/988243077": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/154946536": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/24038369": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25707294": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/284475077": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/14484644": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105196": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/132457369": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/25693835": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105167": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/14592228": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105195": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/4808193": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1152629997": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/4808225": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/4808201": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105148": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105162": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105161": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/414695002": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/325347099": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105160": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1444025652": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105650": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/1198405233": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105660": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105658": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105661": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105656": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/988235252": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/988235253": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/27105657": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/4808199": "a code beside a type on minor ways (owner, 2026-10-13)",
    "way/39917463": "a tenement named by its address",
    "way/54729387": "a vacant private villa",
    "way/666599487": "a villa's garden, in on a heritage listing",
    "way/667618844": "a country house's garden, in on a heritage listing",
    "way/4611889": "a fenced housing complex, in on the former hospital's article",
    "way/178606384": "a landlord's tenants-only recreation area, by its own name",
    "way/519758369": "an estate's communal square",
    "way/1364611379": "a club's square: a type word",
    "way/746163064": "an allotment club's square",
    "way/746169418": "an allotment club's square",
    "node/9007526622": "a private beach, by its own name",
    "node/14145248539": "a members' entrance; its description says it is not public",
    "node/5005526654": "a row of terraced houses drawn as a place",
    "node/13096460395": "a numbered building drawn as a place: a code beside a type",
    "node/13096460394": "a numbered building drawn as a place: a code beside a type",
    "way/1173511850": "a numbered block drawn as a place: a code beside a type",
    "way/1072648524": "an association's name; the settlement has its own row",
    "node/13718155010": "an optician's shop drawn as a locality",
    "way/676848100": "a developer's brand on a building site",
    "way/427502933": "a court of a commercial beach-sports site",
    "way/427502931": "a court of a commercial beach-sports site",
    "way/427502932": "a court of a commercial beach-sports site",
    "way/1446491242": "a park-management service point drawn as a park",
    "way/304102692": "the grounds of a care provider's house, named by a description",
    "node/12469014918": "a customer service point tagged a station, no rail tag",
    "node/11897068961": "a shared-vehicle hub tagged a station, no rail tag",
    "node/4917235508": "a religious residence tagged a place of worship, not notable",
    "way/14437300": "a chapel inside a closed institution (building=hospital, ref Haus 12)",
    "way/630807696": "a communal grave field tagged a place of worship: a type word",
    "way/67751848": "a description standing in for a name",
    "node/3952396497": "a relocation notice and an address in the name",
    "node/1390712121": "closed, by its own name",
    "way/551463949": "burnt down, by its own name",
    "way/1211061583": "a type word standing in for a name",
    "way/1211061584": "a type word standing in for a name",
    "way/1211061585": "a description standing in for a name",
    "node/12750948599": "a heap of earth in a customers-only playground",
    "node/11346626811": "a seat, drawn as a square",
    "node/12623936253": "a description standing in for a name",
    "way/476112244": "a code beside a type",
    "way/1183858582": "a description standing in for a name",
    "way/308245402": "a description standing in for a name",
    "relation/8726443": "a description standing in for a name",
    "way/206368759": "a sports hall drawn as a park: a type word",
    "way/390843217": "a description standing in for a name",
    "relation/20337536": "a stadium's away stand",
    "way/178629200": "a type word with an address",
    "way/229155497": "a turning siding in a tunnel, named by a description",
    "way/229155492": "an unused tunnel stub, out of service by its own name",
    "relation/9736426": "a track-register route number as a landmark",
    "way/187688054": "an abandoned motorway stub named by its section code",
    "way/1127998799": "a mast's footing, on the transmitter's Wikidata entry",
    "node/10733144583": "a spring fair, an event",
    "node/11141887401": "a genre standing in for a title",
    "way/405302873": "a razed railway (razed:railway), not there",
    "node/8679689728": "a closed goods station, by its own name",
    "node/1482191892": "a name cut short",
    "node/11582310547": "a second script glued onto the name",
    "node/11247145906": "a broken name",
    "node/11527981939": "a plaque with no article of its own, its name in brackets",
    "relation/21359023": "a mapper's note in the name; the station has its own row",
    "node/1883472919": "an exit-only stop with a mapper's note in the name; the stop has its own row",
    "way/465683464": "a station's mezzanine level",
    "node/11338877281": "a Stolperschwelle (artwork_type=stolperstein)",
    "way/255072469": "a museum exhibit on the museum's article",
    "way/17042389": "a zoo building: zoo contents",
    "way/698687608": "a delivery access (the -hof ending; owner, 2026-10-13)",
    "way/176917314": "a station exit",
    "way/269457061": "a station corridor",
    "way/271013806": "a station corridor",
    "way/279531566": "a station corridor",
    "way/279531567": "a station corridor",
    "way/269851413": "a station corridor",
    "way/269441852": "a station corridor",
    "way/269441853": "a station corridor",
    "way/279531432": "a station corridor",
    "way/269437826": "a building passage on steps and a corridor",
    "way/401040573": "a building passage on steps and a corridor",
    "way/480656435": "a building passage on a footway",
    "way/23446496": "an access stair, named by a description",
    "way/23446497": "an access stair, named by a description",
    "way/170077657": "a courtyard passage, named by a description",
    "way/170077658": "a courtyard passage, named by a description",
    "way/59212701": "a courtyard passage, named by a description",
    "way/63124372": "a courtyard passage, named by a description",
    "way/191385107": "a description standing in for a name",
    "way/1290982204": "a facility's own stair, access by permit",
    "way/1556674685": "a fire-escape stair",
    "way/1482680776": "a description standing in for a name",
    "way/34965629": "a description standing in for a name",
    "way/145579452": "a fire-brigade access path",
    "way/139118202": "a private utility tunnel",
    "way/139118203": "a private utility tunnel",
    "way/25777235": "a private utility tunnel",
    "way/25777238": "a private utility tunnel",
    "way/416419153": "a private utility tunnel",
    "way/136988251": "a description standing in for a name",
    "way/25552904": "a description standing in for a name",
    "way/60219172": "a generic phrase standing in for a name",
    "way/136699503": "a former rail route, by its own name",
    "way/36888928": "a former rail route, by its own name",
    "way/946014051": "a former rail route, by its own name",
    "way/55464120": "a former tunnel, by its own name",
    "way/55464122": "a former tunnel, by its own name",
    "way/1430511310": "an address standing in for a name",
    "way/120171902": "a private path (description=Privatweg), a code beside a type",
    "way/120171903": "a private path (description=Privatweg), a code beside a type",
    "way/119163856": "a private path (description=Privatweg), a code beside a type",
    "way/112089234": "private railway property by its own description",
    "way/137501607": "stray quotation marks in the name",
    # Held rows settled by the existing rules in three lanes and the owner's
    # rulings of 2026-10-13 (docs/decisions_drafts/search-final-held-applied.md).
    "way/292526612": "A glitched double of a street that has a clean row is dropped (owner 2026-10-11: no glitched name goes live; the reads of 2026-10-13: Brussels' 25 slash-joined doubles); held rows settled 2026-10-13",
    "way/292526613": "A glitched double of a street that has a clean row is dropped (owner 2026-10-11: no glitched name goes live; the reads of 2026-10-13: Brussels' 25 slash-joined doubles); held rows settled 2026-10-13",
    "way/292532846": "A glitched double of a street that has a clean row is dropped (owner 2026-10-11: no glitched name goes live; the reads of 2026-10-13: Brussels' 25 slash-joined doubles); held rows settled 2026-10-13",
    "way/292532858": "A glitched double of a street that has a clean row is dropped (owner 2026-10-11: no glitched name goes live; the reads of 2026-10-13: Brussels' 25 slash-joined doubles); held rows settled 2026-10-13",
    "way/859443410": "A glitched double of a street that has a clean row is dropped (owner 2026-10-11: no glitched name goes live; the reads of 2026-10-13: Brussels' 25 slash-joined doubles); held rows settled 2026-10-13",
    "way/859443414": "A glitched double of a street that has a clean row is dropped (owner 2026-10-11: no glitched name goes live; the reads of 2026-10-13: Brussels' 25 slash-joined doubles); held rows settled 2026-10-13",
    "way/231630781": "A minor-way street named by a description or a generic type word is dropped (street_description, owner 2026-10-13; six answers 3); held rows settled 2026-10-13",
    "way/270064414": "A minor-way street named by a description or a generic type word is dropped (street_description, owner 2026-10-13; six answers 3); held rows settled 2026-10-13",
    "way/35569049": "A minor-way street named by a description or a generic type word is dropped (street_description, owner 2026-10-13; six answers 3); held rows settled 2026-10-13",
    "way/217003511": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
    "way/217003512": "A code beside a path type on minor ways is dropped (owner 2026-10-13, German answers 3; third pass PATH_CODE); held rows settled 2026-10-13",
}
