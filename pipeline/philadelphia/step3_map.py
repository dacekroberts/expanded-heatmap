"""Step 3 - Render Philadelphia's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Philadelphia-specific.

Input:  data/philadelphia/processed/stations.csv
        data/philadelphia/processed/businesses_clean.csv
        data/philadelphia/raw/gtfs.zip                    (for the line overlay)
        data/philadelphia/raw/city_boundary.geojson       (label anchoring)
Output: outputs/philadelphia/heatmap.html

Four line groups are drawn rather than ten routes: the shape_ids and the real
public names both live in config.py, because step 1 needs the same grouping to
decide which routes get thinned. The T group draws five branch shapes under one
legend entry, the way New York draws a trunk with its branches.

Run:  python pipeline/philadelphia/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.philadelphia.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_NAMES,
    LINE_SHAPES,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# Per-line label end override: "start" or "end" forces which end of a line its
# label goes at; the default (automatic) picks the tail end farthest from the
# other lines, on the stretch inside the city. Override only if a rendered map
# shows a label landing badly.
LINE_LABEL_ENDS = {}

LINE_SPECS = {
    key: (LINE_SHAPES[key], colour, name, LINE_LABEL_ENDS.get(key))
    for key, (name, colour) in LINE_NAMES.items()
}


def city_geometry():
    """Philadelphia's limits, so each line's label goes at the tail of the
    stretch inside the city - the L, T and G all run on past it."""
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = (boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None
                else boundary.to_crs(CRS_GEOGRAPHIC))
    # One polygon: the layer holds only the City of Philadelphia.
    return boundary.geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Philadelphia SEPTA Metro Business Density Heatmap",
        city_name="Philadelphia",
        system_name="SEPTA Metro",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "SEPTA Metro"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
    )


if __name__ == "__main__":
    main()
