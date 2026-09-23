"""Scaffold the shared shape of a new city: the parts that are the same in
every built city, so the per-city work starts at the parts that differ.

Writes (never overwrites without --force):
  pipeline/<slug>/__init__.py, config.py, step<N>_map.py
  data/<slug>/raw/, data/<slug>/processed/, outputs/<slug>/
  app/pages/<n>_<Slug>_Heatmap.py, and an entry in app/cities.py
    (named from --slug, NOT --name - see page_stem() for why)
  pipeline/taxonomies/<taxonomy>.py + its registration, with --new-taxonomy

Deliberately NOT generated: step1_stations.py and step2_clean_businesses.py.
They differ per city (a spatial boundary filter, sub-transit-line filters, a
cities-boundary join plus geocoding, one-row-per-site logic for a
multi-license source...) and hold most of the per-city effort - copy the built
city nearest in shape (see .claude/skills/scaffold-city/SKILL.md).

Every value only the city's real data can supply is written as a TODO. Run
`grep -rn TODO pipeline/<slug> app/pages` afterwards; nothing should ship with
one left.

Usage:
  python scripts/scaffold_city.py --slug dallas --name Dallas --system-name DART \\
      --taxonomy naics --lat 32.7767 --lon -96.7970
  python scripts/scaffold_city.py --slug boston ... --taxonomy boston_licenses \\
      --new-taxonomy --value-column license_type --field-label "License type"
"""

import argparse
import importlib
import importlib.util
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

CONFIG = '''"""@@NAME@@-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. Every TODO is a value only this city's
real data can supply (see the add-city skill); none should ship.
"""

from pathlib import Path

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "@@SLUG@@" / "raw"
DATA_PROCESSED = ROOT / "data" / "@@SLUG@@" / "processed"
OUTPUTS = ROOT / "outputs" / "@@SLUG@@"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations outside the city, with where each is (a citable scoping record, as
# in the other cities).
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"

# Raw inputs. Record the exact download command for each (all public):
# TODO: gtfs.zip - the agency's GTFS feed URL.
# TODO: city_boundary.geojson - a real GIS boundary layer for the city.
# TODO: the business file - endpoint, server-side filter, and snapshot date if
#       the source is a term history (Chicago's AS_OF_DATE is the model).
GTFS_ZIP = DATA_RAW / "gtfs.zip"
BUSINESSES_RAW_CSV = DATA_RAW / "businesses.csv"  # TODO: real file name
CITY_BOUNDARY_GEOJSON = DATA_RAW / "city_boundary.geojson"

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# @@CRS_NOTE@@ Derived per city, not copied - see docs/project_context.md's
# CRS lesson.
CRS_PROJECTED = "@@CRS@@"

# --- Ring geometry ---------------------------------------------------------
# The same edges are used for every city (a category-definition choice, not
# a city-specific measurement).
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------

# TODO: which lines count and why (one agency's rail system per city; note what
# is left out), the feed's own route_ids, and the real public line names.
# Check the rail system's shape before assuming "keep every station" (see the
# add-city skill, Step 4).
ROUTE_IDS = []
LINE_NAMES = {}  # route_id -> real public name, e.g. {"801": "A Line"}

# --- Business filtering ------------------------------------------------

# TODO: how in-city rows are identified: the dataset's own city field (check
# what it really holds) or an authoritative district field.
CITY_KEEP = "@@NAME_UPPER@@"

TAXONOMY_SYSTEM = "@@TAXONOMY@@"
# @@RAW_NOTE@@
RAW_CLASSIFICATION_COLUMN = "@@RAW_COL@@"
@@EXTRA_NOTE@@
# Sanity bounds for the supplied lat/lng. TODO: tighten to the city's real
# extent once the boundary is known (this box is a wide starting guess).
@@BBOX_NAME@@ = {
    "lat_min": @@LAT_MIN@@,
    "lat_max": @@LAT_MAX@@,
    "lon_min": @@LON_MIN@@,
    "lon_max": @@LON_MAX@@,
}
'''

MAP = '''"""Step @@STEP@@ - Render @@NAME@@'s heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
@@NAME@@-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/@@SLUG@@/processed/stations.csv
        data/@@SLUG@@/processed/businesses_clean.csv
        data/@@SLUG@@/raw/gtfs.zip                    (for the line overlay)
        data/@@SLUG@@/raw/city_boundary.geojson       (label anchoring)
Output: outputs/@@SLUG@@/heatmap.html

Run:  python pipeline/@@SLUG@@/step@@STEP@@_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.@@SLUG@@.config import (  # noqa: E402
    STATIONS_CSV,
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    GTFS_ZIP,
    HEATMAP_HTML,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    RING_EDGES_METERS,
    RING_LABELS,
    LINE_NAMES,
    TAXONOMY_SYSTEM,
)

# TODO: route_id -> (shape_id, colour). shape_id is each line's single most-used
# trip shape (count trips per shape for the route and take the mode; if that
# shape lies outside the city, pick the one that reaches it and say why).
# Colours: the agency's own where unambiguous, else your own palette, distinct
# from the business-category colours.
LINE_SHAPES = {}
# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at; the default (automatic) picks the tail end farthest from the
# other lines, on the stretch inside the city - override only if a rendered map
# shows that landing badly.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    key: (shape_id, color, LINE_NAMES[key], LINE_LABEL_ENDS.get(key))
    for key, (shape_id, color) in LINE_SHAPES.items()
}


def city_geometry():
    """The city's limits, so each line's label goes at the tail of the stretch
    inside the city (lines that run on past it)."""
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None else boundary.to_crs(CRS_GEOGRAPHIC)
    # TODO: if the layer holds several cities, select this city's record first.
    return boundary.geometry.union_all()


def main():
    if not LINE_SHAPES:
        sys.exit("Fill in LINE_SHAPES (and LINE_NAMES in config.py) first: every drawn line needs a label and a legend entry.")
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="@@NAME@@ @@SYSTEM@@ Business Density Heatmap",
        city_name="@@NAME@@",
        system_name="@@SYSTEM@@",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "@@SYSTEM@@"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
    )


if __name__ == "__main__":
    main()
'''

PAGE = '''"""@@NAME@@ heatmap page - embeds the pre-rendered Folium HTML.

Same static-HTML-embed pattern as pages/1_San_Diego_Heatmap.py - see
Overview.py's docstring for why this is the decided pattern
for every city's detail page. Scaffolded by scripts/scaffold_city.py.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.@@SLUG@@.config import HEATMAP_HTML  # noqa: E402
from components import (  # noqa: E402
    render_city_nav,
    render_site_notices,
    set_base_font,
)

st.set_page_config(page_title="@@NAME@@ Heatmap", page_icon="\\U0001f5fa\\ufe0f", layout="wide")
set_base_font()

render_city_nav("@@NAME@@")

st.title("@@NAME@@: commercial density around @@SYSTEM@@ station areas")

# TODO: replace every TODO line below with prose true for this city: the lines
# (by name), which stations are included and what is left out and where the
# list is, the data source and any known limitation. Avoid restating counts.
st.markdown(
    """
TODO: describe the lines drawn (each is labeled directly on the map and in the
legend), the stations included and excluded (the excluded ones are listed in
`outputs/@@SLUG@@/excluded_stations.csv`), and the data source and its
limitations.

Concentric ring boundaries and the three business categories (Retail, Food
service and Personal services) are toggleable via the layer control in the top
left. When enabled, business density will display as numbered circles summing
areas when zoomed out. Zooming in will show individual dots; hover over those
to see further details.

The heat layer is illustrative. Leaflet applies a visual blur rather than a
statistical density estimate, so read the colour as "roughly where things
cluster."
"""
)

if HEATMAP_HTML.exists():
    # st.iframe embeds the HTML file (read as UTF-8) in a same-origin iframe; its
    # fixed 1000x650 matches the map (see the Leaflet.heat note in map_common.py).
    st.iframe(HEATMAP_HTML, width=1000, height=650)
else:
    st.info("No map yet. Run `python pipeline/@@SLUG@@/step@@STEP@@_map.py` to generate it.")

# The notices that publishing requires, on EVERY page rather than one -
# Chicago's terms say "at the site where the software application ... can
# be accessed". See components._NOTICES. OMITTING THIS IS A LICENCE
# BREACH, not a cosmetic gap: four city pages shipped without it because
# this template did, and on those pages the five mandatory notices were
# absent rather than collapsed.
render_site_notices()
'''

TAXONOMY = '''"""@@NAME@@ taxonomy - the city's own @@VALUE_COLUMN@@ field, not NAICS.

Scaffolded by scripts/scaffold_city.py as a SKELETON: nothing is mapped yet.
Before building the city, pull the full distinct-value list of
`@@VALUE_COLUMN@@` (with counts, restricted to the rows step 2 will keep), map
each value to one of the buckets in pipeline.taxonomies.CATEGORY_BUCKETS, and
hand-sample any catch-all values (see chicago_license.py for the worked
example, including classifying some values by a second field).

Values not listed are excluded (classify() returns None).
"""

# @@VALUE_COLUMN@@ (uppercased) -> bucket name. TODO: fill from the real
# distinct-value pull.
VALUE_TO_BUCKET = {}

FIELD_LABEL = "@@FIELD_LABEL@@"
VALUE_COLUMN = "@@VALUE_COLUMN@@"
# TODO: if some values must be classified by a second field (a catch-all that
# says nothing about the business), list its column(s) here; filter_to_storefront()
# and the map's pin grouping then pass them to classify() too.
# EXTRA_COLUMNS = ("some_other_column",)


def legend_label(bucket: str) -> str:
    return bucket


def classify(row: dict):
    """Taxonomy-module interface (see pipeline/taxonomies/__init__.py)."""
    value = (row.get(VALUE_COLUMN) or "").strip().upper()
    if not value:
        return None
    return VALUE_TO_BUCKET.get(value)
'''


def fill(template, values):
    for key, val in values.items():
        template = template.replace(f"@@{key}@@", str(val))
    return template


class Writer:
    def __init__(self, root, dry_run, force):
        self.root, self.dry_run, self.force = root, dry_run, force
        self.skipped = []

    def write(self, rel, text):
        path = self.root / rel
        if path.exists() and not self.force:
            self.skipped.append(rel)
            print(f"  skip (exists): {rel}")
            return
        print(f"  {'would write' if self.dry_run else 'write'}: {rel}")
        if not self.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")

    def mkdir(self, rel):
        if not self.dry_run:
            (self.root / rel).mkdir(parents=True, exist_ok=True)


def utm_crs(lat, lon):
    zone = int((lon + 180) // 6) + 1
    epsg = (32600 if lat >= 0 else 32700) + zone
    lo = -180 + (zone - 1) * 6
    return f"EPSG:{epsg}", f"UTM zone {zone}{'N' if lat >= 0 else 'S'}: the longitude (~{lon:.2f}) falls in the {lo} to {lo + 6} band."


def page_stem(slug):
    """The page filename's city part, built from the SLUG: `new_york` -> `New_York`.

    It used to be built from --name, and --name is a DISPLAY name: "Lille
    (Regional)" gave `24_Lille_(Regional)_Heatmap.py`, and "Montréal" or
    "Washington D.C." would carry the accent or the dots through the same way.
    app/station_scope.py derives each city's outputs/ directory back FROM this
    filename to build the live station table, so `lille_(regional)` resolved to
    nothing and check_scope_disclosure.py's property C refused it. Two sessions
    - Guadalajara's and Lille's - met that and renamed the page by hand to
    exactly the name this function now produces. The slug IS the outputs/
    directory, so a stem built from it resolves by construction.
    """
    return "_".join(part.capitalize() for part in slug.split("_"))


def load_station_scope(root):
    """app/station_scope.py from `root`, for its slug() - the live app's rule.

    Imported rather than restated, for the same reason the page and the scope
    check share it: a second copy of the rule is the one that drifts.
    """
    path = root / "app" / "station_scope.py"
    spec = importlib.util.spec_from_file_location("_station_scope", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def next_page_number(pages_dir):
    nums = [int(m.group(1)) for p in pages_dir.glob("*_Heatmap.py") if (m := re.match(r"(\d+)_", p.name))]
    return max(nums, default=0) + 1


def region_order(text):
    """REGION_ORDER as written in app/cities.py."""
    m = re.search(r"^REGION_ORDER = \[(.*?)^\]", text, re.S | re.M)
    if not m:
        sys.exit("app/cities.py: could not find `REGION_ORDER = [`.")
    return re.findall(r'^\s*"([^"]+)",', m.group(1), re.M)


def ensure_region(root, args, dry_run):
    """Refuse an unregistered region, or append it with --new-region.

    THE CHECK DUBLIN AND MILAN BOTH NEEDED. Tagging a city with a region that
    is not in REGION_ORDER makes app/cities.py raise at import - and nothing in
    a build imports the app, so the failure waits for a merge or a deploy.
    """
    path = root / "app" / "cities.py"
    known = region_order(path.read_text(encoding="utf-8"))
    if args.region in known:
        return
    if not args.new_region:
        sys.exit(
            f"app/cities.py: region {args.region!r} is not in REGION_ORDER.\n"
            f"  Known: {', '.join(known)}\n"
            f"  A city tagged with an unknown region RAISES at import, and no\n"
            f"  pipeline step imports the app - so this would surface at a\n"
            f"  merge or a deploy rather than here. Pass --new-region to add\n"
            f"  it, or use one of the regions above.")

    text = path.read_text(encoding="utf-8")
    m = re.search(r"^REGION_ORDER = \[(.*?)^\]", text, re.S | re.M)
    entry = ('    # TODO: say WHY this region exists and why it is not split.\n'
             '    # Every other entry here carries that reasoning, and the test\n'
             '    # is "whatever groups cities into ONE readable view" - Canada\n'
             '    # splits on 3,300 km rather than on nationality, and Europe\n'
             '    # stayed whole at about 2,000.\n'
             f'    "{args.region}",\n')
    print(f"  {'would edit' if dry_run else 'edit'}: app/cities.py "
          f"(REGION_ORDER += {args.region!r})")
    if not dry_run:
        path.write_text(text[:m.end(1)] + entry + text[m.end(1):],
                        encoding="utf-8", newline="\n")


def verify_app_imports(root):
    """Import app/cities.py and fail if it raises.

    The generic form of the region bug: cities.py validates itself and nothing
    in a build ever triggers that. This runs it at the one moment the caller is
    still holding the context to fix it.
    """
    import subprocess
    r = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, 'app'); import cities; "
         "print(f'  app/cities.py imports: {len(cities.CITIES)} cities, "
         "{len(cities.REGIONS)} regions')"],
        cwd=str(root), capture_output=True, text=True)
    if r.returncode:
        sys.exit("app/cities.py does NOT import after scaffolding:\n"
                 + (r.stderr or r.stdout))
    print(r.stdout.strip())


def add_city_entry(root, args, page_rel, dry_run):
    path = root / "app" / "cities.py"
    text = path.read_text(encoding="utf-8")
    if f'"name": "{args.name}"' in text:
        print(f"  skip (already listed): app/cities.py has {args.name}")
        return
    # The landing view frames the United States. Every city outside it declares
    # False; a US city is in it. Derived from the region rather than defaulted,
    # because the default is the bug - see the comment in the entry below.
    default_view = args.region.startswith("United States")
    entry = (
        "    {\n"
        f'        "name": "{args.name}",\n'
        f'        "lat": {args.lat},\n'
        f'        "lon": {args.lon},\n'
        f'        "page": "{page_rel}",\n'
        f'        "blurb": "{args.system_name} (TODO: list the lines)",\n'
        # REQUIRED since 2026-09-21: app/cities.py raises at import on a city
        # whose region is missing or not in REGION_ORDER, so a scaffold without
        # this produces a file that will not import. Mexico City found it the
        # hard way. A region NEW to the project is appended to
        # REGION_ORDER by --new-region; without it this script refuses
        # rather than writing an entry that cannot import. Dublin and
        # Milan both shipped that breakage, on separate branches,
        # before it did.
        f'        "region": "{args.region}",\n'
        # BOTH KEYS BELOW ARE WRITTEN BECAUSE THEIR ABSENCE IS NOT NEUTRAL.
        # Barcelona shipped without either on 2026-09-22 and both surfaced in
        # check_deploy_imports, the second one disguised:
        #
        #   label_offset    - pd.DataFrame fills a missing key with
        #                     float('nan'), which is not None AND is truthy.
        #                     That took the whole Overview page down earlier
        #                     the same day, via Mexico City.
        #   in_default_view - IN_DEFAULT_VIEW reads `.get(..., True)`, so a
        #                     missing key means INCLUDED. Barcelona silently
        #                     joined the landing frame and stretched it from
        #                     California to Catalonia; the five reported
        #                     failures named Calgary, Toronto, Guadalajara and
        #                     Los Angeles, and not one named a Spanish city.
        #
        # A defaulted key that is usually right is worse than a missing one,
        # because the fifteen cities that happened to carry it are what hid
        # the first of these.
        f'        "in_default_view": {default_view},\n'
        f'        # STARTING VALUE, NOT A MEASURED ONE. Offsets are PIXELS at a\n'
        f'        # pinned zoom. Run `python scripts/check_macro_labels.py`,\n'
        f'        # which scores every city in every region at three widths -\n'
        f'        # and which will first demand this city\'s label width be\n'
        f'        # MEASURED in a real browser with Space Grotesk loaded, since\n'
        f'        # it refuses a guessed one.\n'
        f'        "label_offset": ("middle", 0, -22),\n'
        "    },\n"
    )
    # Find the end of the CITIES list specifically, NOT the last "]" in the
    # file. `rfind("]")` used to do the latter, which spliced Montreal and then
    # Calgary into the IN_DEFAULT_VIEW comprehension below the list and broke
    # the module both times - each repaired by hand instead of here. Walk
    # forward from `CITIES = [` tracking bracket depth, so anything added after
    # the list is irrelevant however it is written.
    start = text.find("CITIES = [")
    if start == -1:
        sys.exit("app/cities.py: could not find `CITIES = [`.")
    depth, idx = 0, None
    for i in range(text.index("[", start), len(text)):
        ch = text[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                idx = i
                break
    if idx is None:
        sys.exit("app/cities.py: CITIES list is not closed.")
    new = text[:idx] + entry + text[idx:]
    print(f"  {'would edit' if dry_run else 'edit'}: app/cities.py (add {args.name})")
    if not dry_run:
        path.write_text(new, encoding="utf-8", newline="\n")


def register_taxonomy(root, name, dry_run):
    path = root / "pipeline" / "taxonomies" / "__init__.py"
    text = path.read_text(encoding="utf-8")
    if f'"{name}":' in text:
        print(f"  skip (already registered): {name}")
        return
    line = f'    "{name}": "pipeline.taxonomies.{name}",\n'
    marker = "    # Future, non-US"
    if marker in text:
        new = text.replace(marker, line + marker, 1)
    else:
        new = re.sub(r"(TAXONOMY_MODULES = \{\n(?:.*\n)*?)(\}\n)", lambda m: m.group(1) + line + m.group(2), text, count=1)
    print(f"  {'would edit' if dry_run else 'edit'}: pipeline/taxonomies/__init__.py (register {name})")
    if not dry_run:
        path.write_text(new, encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--slug", required=True, help="folder name, lower snake_case (dallas, new_york)")
    ap.add_argument("--name", required=True, help='display name, e.g. "New York"')
    ap.add_argument("--system-name", required=True, help='the rail system, e.g. "CTA \'L\'" or "Metro Rail"')
    ap.add_argument("--taxonomy", required=True, help="a key from TAXONOMY_MODULES, or the name of a new one with --new-taxonomy")
    ap.add_argument("--lat", type=float, required=True, help="marker latitude on the macro map (and CRS zone hint)")
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--region", required=True,
                    help="the macro map's region for this city, e.g. \"United States\", "
                         "\"Canada\", \"Mexico\". REQUIRED: app/cities.py raises at import "
                         "on an untagged city. A region NEW to the project also needs "
                         "--new-region; without it this script refuses.")
    ap.add_argument("--map-step", type=int, default=3, help="number of the map step (3, or 4 if a geocoding step is inserted)")
    ap.add_argument("--new-region", action="store_true",
                    help="the region is new to the project: append it to REGION_ORDER in app/cities.py. Without this a region not already there is REFUSED, because the entry would import-fail and nothing in a build imports the app")
    ap.add_argument("--new-taxonomy", action="store_true", help="also create and register a skeleton taxonomy module")
    ap.add_argument("--value-column", help="with --new-taxonomy: the raw classification column")
    ap.add_argument("--field-label", help="with --new-taxonomy: tooltip label for that column")
    ap.add_argument("--root", type=Path, default=REPO, help="repo root (default: this repo)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite files that already exist")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z][a-z0-9_]*", args.slug):
        sys.exit("--slug must be lower snake_case")
    if args.new_taxonomy and not args.value_column:
        sys.exit("--new-taxonomy needs --value-column")
    root = args.root.resolve()
    w = Writer(root, args.dry_run, args.force)
    print(f"Scaffolding {args.name} ({args.slug}) in {root}" + (" [dry run]" if args.dry_run else ""))

    # --- Taxonomy: reuse a built one, or scaffold a skeleton ---------------
    if args.new_taxonomy:
        w.write(f"pipeline/taxonomies/{args.taxonomy}.py", fill(TAXONOMY, {
            "NAME": args.name, "VALUE_COLUMN": args.value_column,
            "FIELD_LABEL": args.field_label or args.value_column.replace("_", " ").capitalize()}))
        register_taxonomy(root, args.taxonomy, args.dry_run)
        value_col, extra = args.value_column, ()
        raw_col, raw_note = args.value_column, "Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op."
    else:
        sys.path.insert(0, str(root))
        import pipeline.taxonomies as tx
        importlib.reload(tx)
        if args.taxonomy not in tx.TAXONOMY_MODULES:
            sys.exit(f"Unknown taxonomy {args.taxonomy!r}; registered: {sorted(tx.TAXONOMY_MODULES)}. "
                     "Pass --new-taxonomy --value-column ... to scaffold a new one.")
        mod = tx.load_taxonomy_module(args.taxonomy)
        value_col, extra = mod.VALUE_COLUMN, tuple(getattr(mod, "EXTRA_COLUMNS", ()))
        if args.taxonomy == "naics":
            raw_col, raw_note = "TODO", "TODO: the raw export's NAICS column; step 2 renames it to the taxonomy's VALUE_COLUMN."
        else:
            raw_col, raw_note = value_col, "Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op."
    extra_note = ""
    if extra:
        cols = ", ".join(extra)
        extra_note = (f"# This taxonomy also classifies by {cols}: keep those raw column(s) through step 2\n"
                      f"# (they are passed to classify() by filter_to_storefront() and the map).\n")

    crs, crs_note = utm_crs(args.lat, args.lon)
    common = {
        "NAME": args.name, "NAME_UPPER": args.name.upper(), "SLUG": args.slug, "SYSTEM": args.system_name,
        "STEP": args.map_step, "TAXONOMY": args.taxonomy, "CRS": crs, "CRS_NOTE": crs_note,
        "RAW_COL": raw_col, "RAW_NOTE": raw_note, "EXTRA_NOTE": extra_note,
        "BBOX_NAME": f"{args.slug.upper()}_BBOX",
        "LAT_MIN": round(args.lat - 0.4, 2), "LAT_MAX": round(args.lat + 0.4, 2),
        "LON_MIN": round(args.lon - 0.5, 2), "LON_MAX": round(args.lon + 0.5, 2),
    }

    # --- Pipeline, data folders, app page, cities entry -----------------------
    w.write(f"pipeline/{args.slug}/__init__.py", "")
    w.write(f"pipeline/{args.slug}/config.py", fill(CONFIG, common))
    w.write(f"pipeline/{args.slug}/step{args.map_step}_map.py", fill(MAP, common))
    for sub in ("data/%s/raw" % args.slug, "data/%s/processed" % args.slug, "outputs/%s" % args.slug):
        w.mkdir(sub)
    pages = root / "app" / "pages"
    scope = load_station_scope(root)
    # A re-run finds its page BY SLUG, the same test the live table applies, so
    # a page renamed by hand before this fix is still found rather than doubled.
    existing = sorted(p for p in pages.glob("*_Heatmap.py")
                      if scope.slug(f"pages/{p.name}") == args.slug)
    if existing and not args.force:
        page_rel = f"pages/{existing[0].name}"   # re-run: keep the page already there
    else:
        page_rel = f"pages/{next_page_number(pages)}_{page_stem(args.slug)}_Heatmap.py"
    if scope.slug(page_rel) != args.slug:
        sys.exit(f"refusing: {page_rel} resolves to outputs/{scope.slug(page_rel)}/ "
                 f"but this city's outputs are outputs/{args.slug}/. The live "
                 f"station table would show an empty row. See page_stem().")
    w.write(f"app/{page_rel}", fill(PAGE, common))
    # BEFORE the entry, not after: an unregistered region makes the entry
    # unimportable, and refusing while nothing has been written to cities.py
    # leaves the caller with a clean tree rather than a half-migration.
    ensure_region(root, args, args.dry_run)
    add_city_entry(root, args, page_rel, args.dry_run)

    # The generic form of the region bug: cities.py validates ITSELF and
    # nothing in a build ever triggers that, so the failure waits for a merge.
    # Running it here costs a subprocess and catches the next validator too.
    if not args.dry_run:
        verify_app_imports(root)

    print("\nDone." + (f" {len(w.skipped)} existing file(s) left untouched." if w.skipped else ""))
    print(f"Taxonomy: {args.taxonomy} (value column {value_col!r}" + (f", extra columns {list(extra)}" if extra else "") + ")")
    print(f"""
Still to do (nothing generated for these):
  1. add-city Step 0 evidence for the config TODOs (data, GTFS, boundary).
  2. pipeline/{args.slug}/step1_stations.py and step2_clean_businesses.py: copy the
     built city nearest in shape (see .claude/skills/scaffold-city/SKILL.md).
  3. Fill LINE_SHAPES / LINE_NAMES, the page prose and the cities.py blurb.
  4. grep -rn TODO pipeline/{args.slug} app  ->  must be empty before commit,
     AND `grep -n TODO app/cities.py` - the blurb is written there, not in
     pipeline/, so a pipeline-only grep misses it.
  5. MEASURE this city's macro-map label width in a real browser with Space
     Grotesk loaded, add it to check_macro_labels.py's TEXT_WIDTH, then run
     that script. It refuses a guessed width. The label_offset written above
     is a starting value and has not been scored against anything.
  6. python scripts/check_deploy_imports.py --ref <branch>  ->  it catches what
     a local run cannot, including a city that quietly joined the landing view.
  7. Run the steps, look at the map, drift check, deploy-verify, DECISIONS entry.""")


if __name__ == "__main__":
    main()
