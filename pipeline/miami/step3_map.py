"""Step 3 - Render Miami's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Miami-specific.

Input:  data/miami/processed/stations.csv
        data/miami/processed/businesses_clean.csv
        data/miami/raw/gtfs.zip                 (for the line overlay)
        data/miami/raw/municipalities.geojson   (label anchoring)
Output: outputs/miami/heatmap.html

Run:  python pipeline/miami/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.miami.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_LABEL_ENDS,
    LINE_NAMES,
    LINE_SHAPES,
    RING_EDGES_METERS,
    RING_LABELS,
    ROUTE_IDS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# Everything city-specific is in config.py, so this stays a thin assembly of
# it. Each spec is (shape_id(s), colour, real public name, label end); a tuple
# of shape_ids is one line whose physical extent needs more than one shape,
# which Metrorail (branching) and both Metromover loops (partial arcs) need.
LINE_SPECS = {
    key: (LINE_SHAPES[key], LINE_NAMES[key][1], LINE_NAMES[key][0],
          LINE_LABEL_ENDS.get(key))
    for key in ROUTE_IDS
}


def mapped_region():
    """The mapped area, for anchoring each line's label at its tail.

    Every other city passes its own city limits here, because its lines run
    beyond them. Miami is regional by design and the rail network stays inside
    Miami-Dade County, so the county - the union of the municipal layer - IS
    the mapped area, and no single municipality would be the right anchor.
    """
    muni = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    muni = (muni.set_crs(CRS_GEOGRAPHIC) if muni.crs is None
            else muni.to_crs(CRS_GEOGRAPHIC))
    return muni.geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP,
                 CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first "
                     f"(fetch_sources.py, then step1, then step2).")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Miami-Dade Metrorail and Metromover: commercial density around stations",
        # Only used for layer labels, so the honest regional name belongs here
        # rather than "Miami" - the all-businesses layer covers the county.
        city_name="Miami-Dade",
        system_name="Metrorail and Metromover",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "Metrorail and Metromover"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=mapped_region(),
        # Rings start OFF, as in New York and for the same measured reason:
        # 25 of 42 stations sit closer to a neighbour than the 966 m outer
        # ring, and all 19 Metromover stations do (median 235 m apart), so the
        # rings merge into one wash over downtown. Metrorail's own stations are
        # well separated (median 1,149 m), which is why the shared ring edges
        # are kept rather than reduced the way New York's were - the overlap is
        # confined to the Metromover loops. Businesses are assigned to their
        # NEAREST station regardless, so nothing is double-counted either way.
        rings_shown=False,
    )


if __name__ == "__main__":
    main()
