"""Step 3 - Render Edmonton's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
specific to Edmonton.

Input:  data/edmonton/processed/stations.csv
        data/edmonton/processed/businesses_clean.csv
        data/edmonton/raw/gtfs.zip              (line overlay)
        data/edmonton/raw/city_boundary.geojson (label anchoring)
Output: outputs/edmonton/heatmap.html

It is step THREE: 99.4% of storefront rows carry coordinates, so no geocoding
step is needed - and there is no national Canadian geocoder to run one with.
Only Los Angeles and Washington D.C. number their map step 4.

`label_focus` is the city boundary, as usual, and like Calgary's it does little
work: the LRT never leaves Edmonton, so there is no out-of-city stretch for a
label to be taken on.

The three lines' colours are this project's own rather than ETS's, because two
of ETS's three collide with the business-category palette. The reasoning and
the measured Delta-E figures are in config.LINE_COLOURS.

Run:  python pipeline/edmonton/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.edmonton.config import (  # noqa: E402
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
    rid: (LINE_SHAPES[rid], LINE_COLOURS[rid], LINE_NAMES[rid],
          LINE_LABEL_ENDS.get(rid))
    for rid in ROUTE_IDS
}


def city_boundary():
    """Edmonton's own outline, for anchoring each line's label at the end
    farthest from the others. qqvh-dp5m is the CURRENT corporate boundary -
    four layers on that portal share the name and two predate the 2019
    annexation."""
    b = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    if len(b) == 0 or b.geometry.isna().all():
        sys.exit("boundary has no geometry.")
    return b.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP,
                 CITY_BOUNDARY_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run the earlier steps first "
                     f"(fetch_sources.py, then step1, step2).")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Edmonton LRT: commercial density around stations",
        city_name="Edmonton",
        system_name="ETS LRT",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "ETS LRT"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_boundary(),
    )


if __name__ == "__main__":
    main()
