"""Step 3 - Render Madrid's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Madrid-specific, per the project's don't-fork-render_heatmap rule.

Input:  data/madrid/processed/stations.csv
        data/madrid/processed/businesses_clean.csv
        data/madrid/processed/line_shapes.geojson   (written by step 1)
        data/madrid/raw/termino_municipal.zip       (label anchoring)
Output: outputs/madrid/heatmap.html

Run:  python pipeline/madrid/step3_map.py
"""

import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.linecolour import check_line_colours  # noqa: E402
from pipeline.map_common import load_geojson_line_shapes, render_heatmap  # noqa: E402
from pipeline.madrid.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_ZIP,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_NAMES,
    LINE_SHAPES_GEOJSON,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# NOT a GTFS shape_id and not an OSM ref: step 1 wrote one feature per line to
# line_shapes.geojson keyed on `line`, so the source key IS the line key. The
# 18-codes-to-13-lines collapse already happened there, where the raising check
# for an unmapped code lives.
LINE_SHAPES = {key: (key, LINE_COLOURS[key]) for key in LINE_NAMES}

# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at; the default (automatic) picks the tail end farthest from the
# other lines, on the stretch inside the city. Left empty until a rendered map
# shows one landing badly - measured, not anticipated.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    key: (source_key, colour, LINE_NAMES[key], LINE_LABEL_ENDS.get(key))
    for key, (source_key, colour) in LINE_SHAPES.items()
}

# The three business-category colours, which every line colour has to stay
# distinguishable from. Madrid keeps Metro de Madrid's OWN livery rather than an
# invented palette - the project only reaches for its own when an agency's
# colours are ambiguous or shared, and these are neither.
CATEGORY_COLOURS = {
    "Retail": "#2a78d6",
    "Food service": "#C2185B",
    "Personal services": "#1baf7a",
}


def city_geometry():
    """The término municipal in lon/lat, so each line's label goes at the tail
    of the stretch INSIDE Madrid - lines 10 and 12 run well past it."""
    with zipfile.ZipFile(CITY_BOUNDARY_ZIP) as z:
        shp = [n for n in z.namelist() if n.lower().endswith(".shp")][0]
    b = gpd.read_file(f"zip://{CITY_BOUNDARY_ZIP}!{shp}")
    if b.crs is None:
        raise SystemExit("boundary has no CRS - step 1 checks this too")
    return b.to_crs(CRS_GEOGRAPHIC).geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, LINE_SHAPES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    # Every drawn line needs a label AND a legend entry - the project invariant.
    missing = [k for k in LINE_SHAPES if k not in LINE_NAMES]
    if missing:
        sys.exit(f"lines {missing} have no public name in LINE_NAMES")

    check_line_colours({LINE_NAMES[k]: c for k, (_, c) in LINE_SHAPES.items()},
                       CATEGORY_COLOURS, city="Madrid")

    stations = pd.read_csv(STATIONS_CSV)
    businesses = pd.read_csv(BUSINESSES_CLEAN_CSV)
    print(f"{len(stations)} stations, {len(businesses):,} premises")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Madrid - storefront density around Metro stations",
        city_name="Madrid",
        system_name="Metro de Madrid",
        stations=stations,
        businesses=businesses,
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_geojson_line_shapes(LINE_SHAPES_GEOJSON, LINE_SPECS,
                                       "Metro de Madrid"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
    )


if __name__ == "__main__":
    main()
