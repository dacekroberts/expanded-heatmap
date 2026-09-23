"""Step 3 - Render Marseille's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Marseille-specific. Scaffolded by scripts/scaffold_city.py.

Input:  data/marseille/processed/stations.csv
        data/marseille/processed/businesses_clean.csv
        data/marseille/raw/gtfs.zip                    (for the line overlay)
        data/marseille/raw/city_boundary.geojson       (label anchoring)
Output: outputs/marseille/heatmap.html

Run:  python pipeline/marseille/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.marseille.config import (  # noqa: E402
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
        map_title="Marseille Métro and Tramway Business Density Heatmap",
        city_name="Marseille",
        system_name="Métro and Tramway",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "Métro and Tramway"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
    )


if __name__ == "__main__":
    main()
