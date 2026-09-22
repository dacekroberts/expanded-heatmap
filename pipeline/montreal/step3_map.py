"""Step 3 - Render Montréal's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
specific to Montréal.

Input:  data/montreal/processed/stations.csv
        data/montreal/processed/businesses_clean.csv
        data/montreal/raw/gtfs.zip              (line overlay)
        data/montreal/raw/agglomeration.geojson (label anchoring)
Output: outputs/montreal/heatmap.html

It is step THREE: no geocoding step is needed, because the survey carries
`LAT`/`LONG` on 100% of rows. Only Los Angeles and Washington D.C. number
their map step 4.

ONE SHAPE PER LINE, unlike Vancouver. No Métro line branches, so none of the
four needs a tuple of shape_ids - verified to cover every stop on its line
(27 / 31 / 3 / 12).

Run:  python pipeline/montreal/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.montreal.config import (  # noqa: E402
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_COLOURS,
    LINE_LABEL_ENDS,
    LINE_NAMES,
    LINE_SHAPES,
    RING_EDGES_METERS,
    RING_LABELS,
    ROUTE_IDS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# Each spec is (shape_id, colour, real public name, label end).
LINE_SPECS = {
    route_id: (LINE_SHAPES[route_id], LINE_COLOURS[route_id],
               LINE_NAMES[route_id], LINE_LABEL_ENDS.get(route_id))
    for route_id in ROUTE_IDS
}


def mapped_area():
    """The agglomeration's own outline, for anchoring each line's label at the
    end farthest from the others.

    It matters less here than in D.C. - only 4 of 68 stations lie outside -
    but Ligne 2 reaches well into Laval, so without this anchor its label
    could be taken on a stretch the map barely shows.
    """
    b = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    return b.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP,
                 CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first "
                     f"(fetch_sources.py, then step1, step2).")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Métro de Montréal: commercial density around stations",
        city_name="Montréal",
        system_name="Métro",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "Métro"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=mapped_area(),
    )


if __name__ == "__main__":
    main()
