"""Scaffold the France tram batch - the 20 French T1 cities - from the screen's
inputs, one French config per city, instead of twenty hand-filled
`scaffold_city.py` runs.

    python scripts/scaffold_france_batch.py --dry-run                 # all 20, writes nothing
    python scripts/scaffold_france_batch.py --dry-run --only nice,brest
    python scripts/scaffold_france_batch.py --preview-dir <scratch>   # the generated files, outside the repo
    python scripts/scaffold_france_batch.py --only nice --go          # REAL: build work - the owner's go first

**A real run is build work** (it writes `pipeline/<slug>/`, an app page and an
`app/cities.py` entry through `scaffold_city.py`), so it refuses without `--go`.
The owner held builds on 2026-09-29; the kit session wrote and tested this with
`--dry-run` and `--preview-dir` only.

READS (gitignored screen scratch, `data/_staging_scratch_2026-09-27/second_cities/france/`):
  cities.py              core commune INSEE code (and any extra EPCI) per city
  gtfs_urls.py           each feed's NAP resource and DECLARED licence
  stations_pure_<date>/  the station tables under the owner's pure-extract rule,
                         measured by the kit session from the day's feeds;
                         `stations/` (the screen's own collapse) when absent
  bounds/<slug>.geojson  every commune of the city's EPCI(s), with contours

WRITES, per city (real run):
  pipeline/<slug>/config.py                 the French tram config, below
  pipeline/<slug>/step2_clean_businesses.py thin over france_register (Rennes's)
  then runs scaffold_city.py for __init__.py, step3_map.py, the app page and
  the cities.py entry; its generic config.py is skipped because ours exists.

DOES NOT WRITE step1_stations.py or fetch_sources.py. Twenty copies of Rennes's
240-line step 1 is the shape `france_register.py` exists to prevent. The
`france-tram-city` skill says what the first batch build writes instead (a
shared tram module); this script prints the reminder per city.

WHAT EVERY VALUE IS. Measured values come from the inputs above and say so in
the generated comment. Proposals awaiting the owner (scope, `mode`, `coverage`,
a line to add or drop) are written as proposals. Values only the build-day
feed can supply (route_ids, colours, gate 3's independent count) are TODOs:
feeds are rolling, so they are read at build and never copied from a cache.
"""

import argparse
import csv
import json
import re
import runpy
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREEN = REPO / "data" / "_staging_scratch_2026-09-27" / "second_cities" / "france"

# Caen has no feed of its own, and Rouen's own host (api.mrn.cityway.fr) refused
# connections at the screen and again on 2026-09-30: both come from the Normandie
# regional aggregate, filtered to one agency.
NORMANDIE_URL = "https://transport.data.gouv.fr/resources/81942/download"
NORMANDIE_LICENCE = "lov2"

# The spacing rule (docs/ring_rules.md): half-size rings where the median gap
# between stations is about 550 m or less.
HALF_RINGS_MAX_MEDIAN_M = 550

HELD = {
    "angers": "HELD (owner, 2026-09-29) until the other 20 French cities are "
              "built: the Métropole bars naming IRIGO or its marks without consent",
}

# One row per city. `lines` are the feed's route_short_name values KEPT; `drop`
# names what the feed carries on rails and the map leaves out, with the reason;
# `names` are the proposed public names (verified at build). `scope`, `mode`
# and `coverage` are PROPOSALS for the owner, made in each city's brief.
# `route_types` is what the feed types those lines as - Reims and Rouen type
# theirs 1 - which is why the mode is decided per city, never from the flag.
BATCH = {
    "montpellier": dict(name="Montpellier", operator="TaM", route_types=("0",),
                        lines=["1", "2", "3", "4", "5"], scope="commune",
                        names={k: f"Tram {k}" for k in "12345"},
                        feed_notes="no feed_info.txt and NO shapes.txt: line geometry from another source, read first (licence read 2026-09-29)"),
    "nice": dict(name="Nice", operator="Lignes d'Azur", route_types=("0",),
                 lines=["L1", "L2", "L3", "B"], scope="commune",
                 names={"L1": "Tram 1", "L2": "Tram 2", "L3": "Tram 3",
                        "B": "TODO: route B's public name (Aéroport Terminal 2 - CADAM, 6 stops; an owner call to draw it)"},
                 feed_notes="feed_info.txt self-attests"),
    "strasbourg": dict(name="Strasbourg", operator="CTS", route_types=("0",),
                       lines=list("ABCDEF"), scope="commune",
                       names={k: f"Tram {k}" for k in "ABCDEF"},
                       feed_notes="no feed_info.txt, NO shapes.txt and NO parent_station column; line D runs to Kehl, Germany"),
    "bordeaux": dict(name="Bordeaux (Regional)", operator="TBM", route_types=("0",),
                     lines=list("ABCDEF"), scope="regional",
                     names={k: f"Tram {k}" for k in "ABCDEF"},
                     feed_notes="Licence Ouverte 1.0: credit Bordeaux Métropole and the feed's own date; feed_info.txt self-attests (publisher Mecatran)"),
    "nantes": dict(name="Nantes (Regional)", operator="Naolib", route_types=("0",),
                   lines=["1", "2", "3"], scope="regional",
                   names={k: f"Tram {k}" for k in "123"},
                   feed_notes="no feed_info.txt; the scope is the closest call of the batch (line 3 keeps 48.5% in the commune)"),
    "grenoble": dict(name="Grenoble (Regional)", operator="M réso", route_types=("0",),
                     lines=list("ABCDE"), scope="regional",
                     names={k: f"Tram {k}" for k in "ABCDE"},
                     feed_notes="ODbL: the §4.3 notice naming SMMAG; feed_info.txt has no dates"),
    "rouen": dict(name="Rouen (Regional)", operator="Astuce", route_types=("1",),
                  lines=["Métro"], scope="regional", mode="light_rail",
                  names={"Métro": "Métro"},
                  feed="normandie", agency_id="ATOUMOD001:Network:001:LOC",
                  feed_notes="from the Normandie aggregate (Astuce's own host refuses connections); typed route_type 1; one line, two branches"),
    "saint_etienne": dict(name="Saint-Étienne", operator="STAS", route_types=("0",),
                          lines=["T1", "T2", "T3"], scope="commune",
                          names={k: f"Tram {k}" for k in ("T1", "T2", "T3")},
                          feed_notes="no feed_info.txt and NO parent_station column"),
    "dijon": dict(name="Dijon", operator="Divia", route_types=("0",),
                  lines=["T1", "T2"], scope="commune",
                  names={k: f"Tram {k}" for k in ("T1", "T2")},
                  feed_notes="no parent_station column; T1 and T2 share one route_color (AB0672), which linecolour.py refuses: Lille's precedent"),
    "tours": dict(name="Tours", operator="Fil Bleu", route_types=("0",),
                  lines=["A"], scope="commune", names={"A": "Tram A"},
                  feed_notes="ships feed_infos.txt (sic), so no feed_info.txt"),
    "le_havre": dict(name="Le Havre", operator="LiA", route_types=("0",),
                     lines=["A", "B"], scope="commune",
                     names={"A": "Tram A", "B": "Tram B"},
                     feed_notes="ODbL; NO shapes.txt and NO route_color: the colours are the project's own (licence read 2026-09-29); the funicular is not in this feed"),
    "mulhouse": dict(name="Mulhouse", operator="Soléa", route_types=("0",),
                     lines=["1", "2", "3"], scope="commune",
                     names={k: f"Tram {k}" for k in "123"},
                     drop={"TT": "tram-train: fails the rail test (30-minute midday headway, the screen)"},
                     feed_notes="no feed_info.txt"),
    "reims": dict(name="Reims", operator="Grand Reims Mobilités", route_types=("1",),
                  lines=["TRAM"], scope="commune", names={"TRAM": "Tram"},
                  feed_notes="the feed types its tram route_type 1 (metro); it is a tram - mode 'tram'"),
    "caen": dict(name="Caen", operator="Twisto", route_types=("0",),
                 lines=["T1", "T2", "T3"], scope="commune",
                 names={k: f"Tram {k}" for k in ("T1", "T2", "T3")},
                 feed="normandie", agency_id="ATOUMOD029:Network:029:LOC",
                 feed_notes="no feed of its own: the Normandie aggregate, agency Twisto"),
    "brest": dict(name="Brest", operator="Bibus", route_types=("0",),
                  lines=["A", "B"], scope="commune",
                  names={"A": "Tram A", "B": "Tram B"},
                  pending={"C": "the cable car (route_type 6, Jean Moulin - Ateliers): an owner call - Toulouse's Téléo precedent draws route_type 6"},
                  feed_notes="feed_info.txt self-attests; ends 2026-12-20"),
    "besancon": dict(name="Besançon", operator="Ginko", route_types=("0",),
                     lines=["T1", "T2"], scope="commune",
                     names={k: f"Tram {k}" for k in ("T1", "T2")},
                     feed_notes="feed_info.txt self-attests"),
    "orleans": dict(name="Orléans", operator="TAO", route_types=("0",),
                    lines=["A", "B"], scope="commune",
                    names={"A": "Tram A", "B": "Tram B"},
                    feed_notes="feed_info.txt self-attests; parent_station on 9 of 103 platforms only"),
    "le_mans": dict(name="Le Mans", operator="SETRAM", route_types=("0",),
                    lines=["T1", "T2"], scope="commune",
                    names={k: f"Tram {k}" for k in ("T1", "T2")},
                    feed_notes="the gtfs_setram_lmm_auto resource (flex has no tram); feed_info.txt self-attests"),
    "avignon": dict(name="Avignon", operator="Orizo", route_types=("0",),
                    lines=["T1"], scope="commune", names={"T1": "Tram T1"},
                    feed_notes="no feed_info.txt and NO parent_station column"),
    "valenciennes": dict(name="Valenciennes (Regional)", operator="Transvilles", route_types=("0",),
                         lines=["T1", "T2"], scope="regional",
                         names={k: f"Tram {k}" for k in ("T1", "T2")},
                         feed_notes="two or three route_ids per line with differing route_color; the network spans two EPCIs"),
}
MODE_DEFAULT = "tram"
COVERAGE_DEFAULT = "full"   # SIRENE carries all three buckets in every French city


# --- inputs -----------------------------------------------------------------

def load_screen(screen):
    cities = runpy.run_path(str(screen / "cities.py"))["CITIES"]
    feeds = runpy.run_path(str(screen / "gtfs_urls.py"))["FEEDS"]
    return cities, feeds


def pick_stations_dir(screen, override):
    if override:
        return Path(override)
    dated = sorted(screen.glob("stations_pure_*"))
    return dated[-1] if dated else screen / "stations"


def read_stations(sdir, slug, keep):
    with open(sdir / f"{slug}.csv", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        lines = [l for l in r["lines"].split("|") if l in keep]
        if lines:
            r = dict(r, lines=lines, lat=float(r["lat"]), lon=float(r["lon"]),
                     in_core=str(r["in_core"]).strip().lower() == "true")
            out.append(r)
    return out


def median_gap_m(stations):
    """Nearest-neighbour gaps in Lambert-93 metres - never in EPSG:4326."""
    import numpy as np
    from pyproj import Transformer
    if len(stations) < 2:
        return None, None
    t = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)
    xy = np.array([t.transform(s["lon"], s["lat"]) for s in stations])
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    np.fill_diagonal(d, np.inf)
    nn = d.min(1)
    return float(np.median(nn)), float(nn.min())


def communes_geo(screen, slug):
    from shapely.geometry import shape
    gj = json.loads((screen / "bounds" / f"{slug}.geojson").read_text(encoding="utf-8"))
    return {f["properties"]["code"]: (f["properties"]["nom"], f["properties"].get("codeEpci"),
                                      shape(f["geometry"])) for f in gj["features"]}


def measure(slug, spec, screen, sdir, cities):
    from shapely.ops import unary_union
    core = cities[slug][1]
    stations = read_stations(sdir, slug, set(spec["lines"]))
    if not stations:
        sys.exit(f"{slug}: no station in {sdir.name}/{slug}.csv serves {spec['lines']}")
    per_line = {}
    for line in spec["lines"]:
        on = [s for s in stations if line in s["lines"]]
        per_line[line] = {"total": len(on), "inside": sum(s["in_core"] for s in on)}
    missing = [l for l, v in per_line.items() if not v["total"]]
    if missing:
        sys.exit(f"{slug}: line(s) {missing} have no station in {sdir.name}/ - "
                 f"a line kept in BATCH must be in the station table")
    geo = communes_geo(screen, slug)
    if core not in geo:
        sys.exit(f"{slug}: core commune {core} is not in bounds/{slug}.geojson")
    served = {}
    for s in stations:
        served.setdefault(s["commune"], [s["commune_nom"], 0])[1] += 1
    in_scope = stations if spec["scope"] == "regional" else [s for s in stations if s["in_core"]]
    med, mn = median_gap_m(in_scope)
    if spec["scope"] == "regional":
        codes = [c for c in served if c in geo]
        area = unary_union([geo[c][2] for c in codes])
    else:
        area = geo[core][2]
    minx, miny, maxx, maxy = area.bounds
    pt = geo[core][2].representative_point()
    epcis = sorted({geo[c][1] for c in served if c in geo and geo[c][1]}
                   | {geo[core][1]})
    worst = min(per_line.items(), key=lambda kv: kv[1]["inside"] / kv[1]["total"])
    return {
        "core": core, "epcis": epcis, "per_line": per_line, "served": served,
        "stations": len(stations), "in_scope": len(in_scope),
        "median_m": med, "min_m": mn, "worst": worst,
        "bbox": {"lat_min": round(miny - 0.02, 2), "lat_max": round(maxy + 0.02, 2),
                 "lon_min": round(minx - 0.02, 2), "lon_max": round(maxx + 0.02, 2)},
        "marker": (round(pt.y, 4), round(pt.x, 4)),
        "outside_epci": sorted({s["stop_name"] for s in stations if s["commune"] == "outside"}),
    }


# --- the generated files ----------------------------------------------------

CONFIG = '''"""@@NAME@@-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_france_batch.py (the France tram batch) from the
2026-09-27 screen's inputs and the station table in `@@SDIR@@`.
Read `.claude/skills/france-tram-city/SKILL.md` and
`docs/build_briefs/@@SLUG@@.md` before filling anything. Every TODO is a value
only the build-day feed or the owner can supply; none may ship.
"""

from pathlib import Path

# The national facts, shared with every French city (see pipeline/rennes/config.py).
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
DATA_RAW = ROOT / "data" / "@@SLUG@@" / "raw"
DATA_PROCESSED = ROOT / "data" / "@@SLUG@@" / "processed"
OUTPUTS = ROOT / "outputs" / "@@SLUG@@"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
@@SCOPE_PATHS@@
STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

GTFS_ZIP = DATA_RAW / "gtfs.zip"
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"
# Every commune of the EPCI(s) the network runs in, with contours: the naming
# layer for excluded stations (commune scope) or the scoping layer (regional).
METRO_COMMUNES_GEOJSON = DATA_RAW / "metropole_communes.geojson"

# --- The feed ------------------------------------------------------------

# ⚠ ROLLING. French tram feeds run four to twelve weeks ahead, so the build
# FETCHES THIS FRESH on every run and never trusts a cached copy - including the
# screen's 2026-09-27 copy that may sit in data/@@SLUG@@/raw/ already.
GTFS_URL = "@@GTFS_URL@@"
GTFS_DATASET = "@@GTFS_DATASET@@"
@@LICENCE_NOTE@@
GTFS_LICENCE = "@@LICENCE@@"
@@AGENCY_LINE@@@@FEED_NOTES@@
# TODO: re-read at build - does the build-day zip carry feed_info.txt with a
# feed_end_date? True means the page can quote the operator's own window.
GTFS_SELF_ATTESTS = None

BOUNDARY_COMMUNE_CODE = "@@CORE@@"
# ⚠ `geometry=contour`, NOT `fields=contour` (a 120-byte POINT, no error).
BOUNDARY_URL = ("https://geo.api.gouv.fr/communes/@@CORE@@"
                "?geometry=contour&format=geojson")
METROPOLE_EPCI_CODES = @@EPCIS@@
METROPOLE_COMMUNES_URLS = [
    f"https://geo.api.gouv.fr/epcis/{code}/communes"
    "?fields=nom,code&geometry=contour&format=geojson"
    for code in METROPOLE_EPCI_CODES
]

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"
# LAMBERT-93, as every French city takes it: one national grid for one national
# register, where a per-city UTM rule would split France across zones 30-32.
CRS_PROJECTED = "EPSG:2154"

# --- Ring geometry ---------------------------------------------------------
METERS_PER_MILE = 1609.344
@@RING_NOTE@@
RING_EDGES_MILES = @@RING_MILES@@
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = @@RING_LABELS@@

# --- Station scope ----------------------------------------------------------

# PROPOSED to the owner with the build (docs/build_briefs/@@SLUG@@.md):
@@SCOPE_WHY@@
#   mode     @@MODE@@ (the macro map's dot colour: what step 1 keeps, never the
#            feed's route_type flag)
#   coverage @@COVERAGE@@ (SIRENE: all three buckets)
SCOPE = "@@SCOPE@@"
MAP_MODE = "@@MODE@@"
MAP_COVERAGE = "@@COVERAGE@@"

# What the feed types the kept lines as. Matched together with the line list,
# never alone: a type flag is not a mode decision (Reims and Rouen type theirs 1).
ROUTE_TYPES_RAIL = @@ROUTE_TYPES@@
# The kept lines, by the feed's route_short_name.
LINE_KEYS = @@LINE_KEYS@@
# TODO: the build-day feed's route_id(s) for each key in LINE_KEYS. Read them
# fresh: a rolling feed may renumber. Several route_ids per key is allowed
# (Le Havre, Valenciennes) - they collapse onto the key.
ROUTE_IDS = []
@@DROP@@
# Station rule (owner, 2026-09-29, every French ODbL feed; the kit applies it
# to every French feed): the feed's own parent_station row, else the FIRST
# platform in stops.txt order per unchanged stop_name. Never a mean, never a
# rename. Measured @@SDATE@@: @@N_STATIONS@@ stations network-wide.
@@SCOPE_ASSERT@@
# GATE 3: an independent per-line count, from outside the feed.
# TODO: the operator's own stop list or OpenStreetMap's route relations.
OPERATOR_STATION_COUNTS = {}
OPERATOR_COUNTS_SOURCE = "TODO"

# route_short_name -> the name riders use. Proposed; verify each against the
# operator's own naming before it goes on the map and in the legend.
LINE_NAMES = @@LINE_NAMES@@  # TODO verify
# TODO: each line's colour, from the build-day feed's route_color where it has
# one and it is unambiguous; pipeline/linecolour.py decides a clash.
LINE_COLOURS = {}

# --- Business filtering ------------------------------------------------

# EXACT INSEE codes, from the station table's own commune placement.
# TODO: count each code in SIRENE at step 2 and look for legacy codes inside
# these contours (Lille's Lomme and Hellemmes: MEL's labels and INSEE's differ).
COMMUNE_PREFIXES = @@PREFIXES@@

CITY_KEEP = "@@NAME_UPPER@@"   # scaffold field; COMMUNE_PREFIXES is the filter

# The French precedent (Paris, Marseille, Toulouse, Lille, Rennes): both
# catch-alls excluded on INSEE's own labels. A share is a fact about a city, so
# step 2 prints this city's; a share far from the siblings' goes to the owner.
CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")

TAXONOMY_SYSTEM = "france_naf"
RAW_CLASSIFICATION_COLUMN = "naf_label"

# Sanity bounds: the @@BBOX_WHAT@@ extent plus ~0.02 deg, from the EPCI
# contours. They catch a corrupt coordinate; the commune filter scopes.
@@BBOX_NAME@@ = @@BBOX@@
'''

STEP2 = '''"""@@NAME@@ step 2: SIRENE -> the storefronts in scope.

    python pipeline/@@SLUG@@/step2_clean_businesses.py

Thin over `pipeline/countries/france_register.py`, as every French city is;
what is @@NAME@@'s own lives in `config.py`. Scaffolded by
scripts/scaffold_france_batch.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.countries.france_register import build_storefronts
from pipeline.@@SLUG@@ import config


def main():
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out = build_storefronts(config, "@@NAME@@", config.@@BBOX_NAME@@)
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\\n  {len(out):,} storefronts -> "
          f"{config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
'''


def fill(template, values):
    for key, val in values.items():
        template = template.replace(f"@@{key}@@", str(val))
    left = re.findall(r"@@[A-Z_]+@@", template)
    if left:
        sys.exit(f"template placeholders left unfilled: {sorted(set(left))}")
    return template


def comment(text, first="# ", rest="# "):
    """A prose value as wrapped comment lines, the width the configs use."""
    import textwrap
    return "\n".join(textwrap.wrap(text, width=79, initial_indent=first,
                                   subsequent_indent=rest))


def pyrepr(obj):
    """A literal that reads as the repo's own configs do (double quotes)."""
    return json.dumps(obj, ensure_ascii=False)


def render(slug, spec, m, feeds, sdir):
    feed_url = NORMANDIE_URL if spec.get("feed") == "normandie" else feeds[slug][2]
    dataset = ("Agrégat des réseaux urbains et interurbains de Normandie"
               if spec.get("feed") == "normandie" else feeds[slug][0])
    licence = NORMANDIE_LICENCE if spec.get("feed") == "normandie" else feeds[slug][1]
    licence_note = {
        "lov2": "Licence Ouverte 2.0: credit the producer and the date.",
        "fr-lo": "Licence Ouverte 1.0: credit Bordeaux Métropole and the feed's own date (read 2026-09-29).",
        "odc-odbl": ("ODbL under the NAP's Conditions Particulières: the §4.3 notice in "
                     "app/components.py, and the station table a PURE extract (read 2026-09-29)."),
    }[licence]
    agency = (f'# The aggregate carries several networks: keep this agency only.\n'
              f'GTFS_AGENCY_ID = "{spec["agency_id"]}"\n') if spec.get("agency_id") else ""
    half = m["median_m"] is not None and m["median_m"] <= HALF_RINGS_MAX_MEDIAN_M
    ring_note = (f"Median nearest-neighbour gap {m['median_m']:,.0f} m across the "
                 f"{m['in_scope']} in-scope stations (min {m['min_m']:,.0f} m), Lambert-93, "
                 f"measured from the kit's station table - "
                 + ("under ~550 m, so the half-size rings every French city takes "
                    "(docs/ring_rules.md). Step 1 re-measures." if half else
                    "OVER ~550 m, so the standard rings; the page drops the "
                    "half-size sentence. Step 1 re-measures."))
    if half:
        miles, labels = [0.0, 0.05, 0.1, 0.2, 0.3], ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]
    else:
        miles, labels = [0.0, 0.1, 0.2, 0.3, 0.6], ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

    w_line, w = m["worst"]
    share = w["inside"] / w["total"]
    if spec["scope"] == "regional":
        scope_why = (f"the worst line, {w_line}, keeps {w['inside']} of {w['total']} "
                     f"stations ({share:.0%}) in commune {m['core']}; under half goes "
                     f"regional (Lille's precedent)")
        codes = sorted(c for c in m["served"] if c != "outside")
        served = {c: m["served"][c][0] for c in codes}
        scope_paths = ("# The communes the network serves, and their union: the regional\n"
                       "# scope's own record and the map's boundary (Lille's pattern).\n"
                       'SERVED_COMMUNES_CSV = OUTPUTS / "served_communes.csv"\n'
                       'SERVED_BOUNDARY_GEOJSON = DATA_PROCESSED / "served_boundary.geojson"\n')
        scope_assert = ("# THE SERVED COMMUNES, asserted rather than trusted: every commune holding\n"
                        "# a kept station, placed in the official contours. A change is a decision.\n"
                        f"EXPECTED_SERVED_COMMUNES = {pyrepr(served)}\n"
                        f"# Per line, network-wide (the regional scope keeps every station):\n"
                        f"EXPECTED_STATIONS_PER_LINE = {pyrepr({k: v['total'] for k, v in m['per_line'].items()})}\n")
        prefixes = tuple(codes)
        bbox_what = "served communes'"
    else:
        scope_why = (f"the worst line, {w_line}, keeps {w['inside']} of {w['total']} "
                     f"stations ({share:.0%}) in commune {m['core']}; half or more stays "
                     f"commune-only (Toulouse 52%, Rennes 73%)")
        scope_paths = ("# Stations outside the commune, each with the commune it IS in.\n"
                       'EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"\n')
        scope_assert = ("# WHAT SURVIVES THE BOUNDARY, PER LINE - asserted in step 1 so the scope\n"
                        "# decision is checkable. If these move, the decision is being re-taken.\n"
                        f"EXPECTED_INSIDE_PER_LINE = {pyrepr({k: v['inside'] for k, v in m['per_line'].items()})}\n"
                        f"EXPECTED_STATIONS_PER_LINE = {pyrepr({k: v['total'] for k, v in m['per_line'].items()})}\n")
        if m["outside_epci"]:
            scope_assert += ("# ⚠ Outside every EPCI contour, so no commune file names them: "
                             f"{', '.join(m['outside_epci'])}.\n")
        prefixes = (m["core"],)
        bbox_what = "commune's"
    drop = ""
    if spec.get("drop") or spec.get("pending"):
        drop = "# On rails in the feed and NOT drawn:\nEXCLUDED_RAIL_ROUTES = {\n"
        for k, why in (spec.get("drop") or {}).items():
            drop += f'    "{k}": "{why}",\n'
        for k, why in (spec.get("pending") or {}).items():
            drop += f'    "{k}": "PENDING - {why}",  # TODO owner call\n'
        drop += "}\n"
    name_upper = re.sub(r"\s*\(REGIONAL\)$", "", spec["name"].upper())
    values = {
        "NAME": spec["name"], "NAME_UPPER": name_upper, "SLUG": slug,
        "SDIR": sdir.relative_to(REPO).as_posix() if sdir.is_relative_to(REPO) else sdir.as_posix(),
        "SDATE": sdir.name.replace("stations_pure_", "") if "pure" in sdir.name else "at the screen, 2026-09-27",
        "SCOPE_PATHS": scope_paths, "GTFS_URL": feed_url, "GTFS_DATASET": dataset,
        "LICENCE": licence,
        "LICENCE_NOTE": comment("The licence the NAP declares for this dataset. " + licence_note),
        "AGENCY_LINE": agency,
        "FEED_NOTES": comment("Measured 2026-09-30 by the kit session: "
                              + spec.get("feed_notes", "nothing further") + "."),
        "CORE": m["core"], "EPCIS": pyrepr(m["epcis"]),
        "RING_NOTE": comment(ring_note), "RING_MILES": pyrepr(miles), "RING_LABELS": pyrepr(labels),
        "SCOPE": spec["scope"],
        "SCOPE_WHY": comment(f"{spec['scope']} - {scope_why}", first="#   scope    ",
                             rest="#            "),
        "MODE": spec.get("mode", MODE_DEFAULT), "COVERAGE": spec.get("coverage", COVERAGE_DEFAULT),
        "ROUTE_TYPES": pyrepr(list(spec["route_types"])).replace("[", "(").replace("]", ",)"),
        "LINE_KEYS": pyrepr(spec["lines"]), "DROP": drop,
        "N_STATIONS": m["stations"], "SCOPE_ASSERT": scope_assert,
        "LINE_NAMES": pyrepr(spec["names"]),
        "PREFIXES": pyrepr(list(prefixes)).replace("[", "(").replace("]", ",)" if len(prefixes) == 1 else ")"),
        "BBOX_WHAT": bbox_what, "BBOX_NAME": f"{slug.upper()}_BBOX", "BBOX": pyrepr(m["bbox"]),
    }
    config_text = fill(CONFIG, values)
    step2_text = fill(STEP2, {"NAME": re.sub(r" \(Regional\)$", "", spec["name"]),
                              "SLUG": slug, "BBOX_NAME": values["BBOX_NAME"]})
    compile(config_text, f"pipeline/{slug}/config.py", "exec")
    compile(step2_text, f"pipeline/{slug}/step2_clean_businesses.py", "exec")
    return config_text, step2_text


def scaffold_supports_mode(root):
    return "--mode" in (root / "scripts" / "scaffold_city.py").read_text(encoding="utf-8")


def run_scaffold(root, slug, spec, m, dry_run, force):
    cmd = [sys.executable, str(root / "scripts" / "scaffold_city.py"),
           "--slug", slug, "--name", spec["name"], "--system-name", spec["operator"],
           "--taxonomy", "france_naf", "--lat", str(m["marker"][0]), "--lon", str(m["marker"][1]),
           "--region", "Europe", "--country", "France", "--root", str(root)]
    if scaffold_supports_mode(root):
        cmd += ["--mode", spec.get("mode", MODE_DEFAULT)]
    if dry_run:
        cmd.append("--dry-run")
    if force:
        cmd.append("--force")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    keep = [l.strip() for l in (r.stdout or "").splitlines()
            if l.strip().startswith(("would write", "write", "skip", "would edit", "edit"))]
    for line in keep:
        if line.endswith(f"pipeline/{slug}/config.py") and dry_run:
            # A real run writes the French config FIRST, so scaffold_city.py
            # finds it and skips its generic one; a dry run cannot show that.
            line += "  (superseded: skipped in a real run, the French config exists by then)"
        elif "app/pages/" in line and dry_run:
            line += "  (numbered in a real run: each city takes the next page number)"
        print(f"    scaffold_city: {line}")
    if r.returncode:
        sys.exit(f"scaffold_city.py failed for {slug}:\n{r.stderr or r.stdout}")


def write(path, text, dry_run, force, label):
    if path.exists() and not force:
        print(f"  skip (exists): {label}")
        return
    print(f"  {'would write' if dry_run else 'write'}: {label}")
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", help="comma-separated slugs (default: all 20)")
    ap.add_argument("--dry-run", action="store_true", help="print what would be written; write nothing")
    ap.add_argument("--preview-dir", help="write the generated config.py and step 2 here instead of the repo "
                                          "(scratch, for reading them); implies no scaffold_city.py run")
    ap.add_argument("--go", action="store_true", help="a REAL run: build work, the owner's go first")
    ap.add_argument("--screen", default=str(SCREEN), help="the screen's scratch folder")
    ap.add_argument("--stations-dir", help="station tables (default: the newest stations_pure_*/, else stations/)")
    ap.add_argument("--root", type=Path, default=REPO)
    ap.add_argument("--force", action="store_true", help="overwrite files that already exist")
    args = ap.parse_args()

    if not (args.dry_run or args.preview_dir or args.go):
        sys.exit("refusing a real run without --go: scaffolding the batch is build work, "
                 "held by the owner since 2026-09-29. Use --dry-run or --preview-dir.")
    screen = Path(args.screen)
    cities, feeds = load_screen(screen)
    sdir = pick_stations_dir(screen, args.stations_dir)
    slugs = args.only.split(",") if args.only else list(BATCH)
    for s in slugs:
        if s in HELD:
            sys.exit(f"{s}: {HELD[s]}")
        if s not in BATCH:
            sys.exit(f"{s}: not in the batch. Have: {', '.join(BATCH)}")
    root = args.root.resolve()
    mode = "PREVIEW" if args.preview_dir else ("DRY RUN" if args.dry_run else "REAL RUN")
    print(f"France tram batch - {len(slugs)} cities - {mode}\n  stations from {sdir}\n")
    table = []
    for slug in slugs:
        spec = BATCH[slug]
        m = measure(slug, spec, screen, sdir, cities)
        config_text, step2_text = render(slug, spec, m, feeds, sdir)
        w_line, w = m["worst"]
        print(f"{spec['name']} ({slug}): {m['stations']} stations, {m['in_scope']} in scope, "
              f"worst line {w_line} {w['inside']}/{w['total']}, median gap "
              f"{m['median_m']:,.0f} m -> scope {spec['scope']}, mode "
              f"{spec.get('mode', MODE_DEFAULT)}, coverage {spec.get('coverage', COVERAGE_DEFAULT)}")
        table.append((slug, m))
        if args.preview_dir:
            out = Path(args.preview_dir) / slug
            write(out / "config.py", config_text, False, True, f"{out / 'config.py'}")
            write(out / "step2_clean_businesses.py", step2_text, False, True,
                  f"{out / 'step2_clean_businesses.py'}")
            continue
        write(root / "pipeline" / slug / "config.py", config_text, args.dry_run, args.force,
              f"pipeline/{slug}/config.py (French tram config)")
        write(root / "pipeline" / slug / "step2_clean_businesses.py", step2_text, args.dry_run,
              args.force, f"pipeline/{slug}/step2_clean_businesses.py")
        run_scaffold(root, slug, spec, m, args.dry_run, args.force)
        if not (root / "pipeline" / "countries" / "france_tram.py").exists():
            print("    not written: step1_stations.py, fetch_sources.py - the first batch build "
                  "writes the shared tram module (france-tram-city skill, 'Step 1')")
        print()
    if not args.preview_dir and not scaffold_supports_mode(root):
        print("⚠ scaffold_city.py has no --mode yet (it arrives with the macro-legend branch):\n"
              "  set each cities.py entry's \"mode\" and \"coverage\" by hand, from its config's\n"
              "  MAP_MODE and MAP_COVERAGE:")
        for slug, _ in table:
            spec = BATCH[slug]
            print(f"    {slug:14s} mode {spec.get('mode', MODE_DEFAULT):11s} "
                  f"coverage {spec.get('coverage', COVERAGE_DEFAULT)}")
    if args.dry_run or args.preview_dir:
        print(f"\n{mode}: nothing written to the repo." if not args.preview_dir else
              f"\n{mode}: generated files are in {args.preview_dir}; the repo is untouched.")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
