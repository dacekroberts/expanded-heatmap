"""Step 3 - Render Calgary's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
specific to Calgary.

Input:  data/calgary/processed/stations.csv
        data/calgary/processed/businesses_clean.csv
        data/calgary/raw/gtfs.zip              (line overlay)
        data/calgary/raw/city_boundary.geojson (label anchoring)
Output: outputs/calgary/heatmap.html

It is step THREE: `point` is populated on 100% of licence rows, so no
geocoding step is needed. Only Los Angeles and Washington D.C. number their
map step 4.

`label_focus` is the city boundary, as usual - but it does less work here than
anywhere else, because the CTrain never leaves Calgary. There is no
out-of-city stretch for a label to be taken on, unlike D.C. (58 of 98 stations
outside) or SkyTrain (30 of 54).

Run:  python pipeline/calgary/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.calgary.config import (  # noqa: E402
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
    ROUTE_SHORT_NAMES,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
)

# Each spec is (shape_id, colour, real public name, label end).
LINE_SPECS = {
    short: (LINE_SHAPES[short], LINE_COLOURS[short], LINE_NAMES[short],
            LINE_LABEL_ENDS.get(short))
    for short in ROUTE_SHORT_NAMES
}


def city_boundary():
    """Calgary's own outline, for anchoring each line's label at the end
    farthest from the other."""
    b = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    if len(b) == 0 or b.geometry.isna().all():
        sys.exit("boundary has no geometry - that is the `map`-view trap. Use "
                 "the `dataset` view (erra-cqp9).")
    return b.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP,
                 CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first "
                     f"(fetch_sources.py, then step1, step2).")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Calgary CTrain: commercial density around stations",
        city_name="Calgary",
        system_name="CTrain",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "CTrain"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_boundary(),
    )


if __name__ == "__main__":
    main()
