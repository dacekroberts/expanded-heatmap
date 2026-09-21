"""Step 3 - Render Boston's heatmap to a standalone HTML file.

All rendering lives in pipeline/map_common.py; this file supplies only what is
Boston-specific.

Input:  data/boston/processed/stations.csv
        data/boston/processed/businesses_clean.csv
        data/boston/raw/gtfs.zip                  (for the line overlay)
        data/boston/raw/ma_municipalities.geojson (label anchoring)
Output: outputs/boston/heatmap.html

Run:  python pipeline/boston/step3_map.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.map_common import load_line_shapes, render_heatmap  # noqa: E402
from pipeline.boston.config import (  # noqa: E402
    BOUNDARY_TOWN_FIELD,
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_NAME,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    GTFS_ZIP,
    HEATMAP_HTML,
    LINE_LABEL_ENDS,
    LINE_NAMES,
    LINE_SHAPES,
    RING_EDGES_METERS,
    RING_LABELS,
    STATIONS_CSV,
    TAXONOMY_SYSTEM,
    TOWN_BOUNDARIES_GEOJSON,
)

# Each spec is (shape_id(s), colour, real public name, label end). Tuples
# because both branching lines need several shapes to draw their full extent:
# the Red Line splits to Ashmont and Braintree, the Green Line is four
# branches on a shared central subway.
LINE_SPECS = {
    group: (LINE_SHAPES[group], LINE_NAMES[group][1], LINE_NAMES[group][0],
            LINE_LABEL_ENDS.get(group))
    for group in LINE_NAMES
}


def city_geometry():
    """Boston's own limits, so each line's label goes at the tail of the
    stretch INSIDE the city. This matters more here than in most cities: every
    one of these lines runs well past the boundary - the Red Line to Braintree,
    the Green Line to Newton and Medford - so without this the labels would
    land in other towns."""
    towns = gpd.read_file(TOWN_BOUNDARIES_GEOJSON)
    towns = (towns.set_crs(CRS_GEOGRAPHIC) if towns.crs is None
             else towns.to_crs(CRS_GEOGRAPHIC))
    boston = towns[towns[BOUNDARY_TOWN_FIELD].str.upper() == CITY_BOUNDARY_NAME]
    if boston.empty:
        sys.exit(f"No {CITY_BOUNDARY_NAME!r} polygon in "
                 f"{TOWN_BOUNDARIES_GEOJSON.name} - check the town field.")
    return boston.geometry.union_all()


def main():
    for path in (STATIONS_CSV, BUSINESSES_CLEAN_CSV, GTFS_ZIP,
                 TOWN_BOUNDARIES_GEOJSON):
        if not path.exists():
            sys.exit(f"Missing {path}. Run fetch_sources.py, then step1, "
                     f"then step2.")

    render_heatmap(
        output_path=HEATMAP_HTML,
        map_title="Boston: commercial density around MBTA rapid-transit stations",
        city_name="Boston",
        system_name="MBTA rapid transit",
        stations=pd.read_csv(STATIONS_CSV),
        businesses=pd.read_csv(BUSINESSES_CLEAN_CSV),
        taxonomy_system=TAXONOMY_SYSTEM,
        lines=load_line_shapes(GTFS_ZIP, LINE_SPECS, "MBTA rapid transit"),
        crs_geographic=CRS_GEOGRAPHIC,
        crs_projected=CRS_PROJECTED,
        ring_edges_meters=RING_EDGES_METERS,
        ring_labels=RING_LABELS,
        label_focus=city_geometry(),
        # Rings stay ON. Boston's kept stations are the grade-separated heavy
        # rail plus a thinned Green Line, so they are well enough separated to
        # read individually - which is the point of having thinned the Green
        # Line rather than reaching for New York's rings-off lever.
    )


if __name__ == "__main__":
    main()
